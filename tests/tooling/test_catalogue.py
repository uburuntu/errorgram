"""Keep reviewed data, generated bindings, and evidence references consistent."""

import copy
import json
from pathlib import Path

import pytest
from errorgram import classify
from jsonschema import ValidationError

from tools.generate import outputs
from tools.validate import load_catalogue, validate

ROOT = Path(__file__).resolve().parents[2]


def test_every_reviewed_example_matches_its_condition():
    for entry in load_catalogue()["entries"]:
        example = entry["example"]
        result = classify(example["response"], method=example.get("method"))
        assert result.status == "matched", entry["id"]
        assert result.id == entry["id"]


def test_generated_files_are_current_and_deterministic():
    catalogue = load_catalogue()
    generated = outputs(catalogue)
    assert generated == outputs(copy.deepcopy(catalogue))
    for relative, content in generated.items():
        assert (ROOT / relative).read_text() == content, relative


def test_metadata_change_reaches_both_languages_and_reference():
    catalogue = load_catalogue()
    original = outputs(catalogue)
    catalogue["entries"][0]["summary"] = "A revised explanation."
    updated = outputs(catalogue)
    for relative in ["python/errorgram/catalogue.json", "js/src/catalogue.ts", "docs/catalogue.md"]:
        assert original[relative] != updated[relative]
        assert "A revised explanation." in updated[relative]


@pytest.mark.parametrize("mutation", [
    lambda c: c["entries"].append(copy.deepcopy(c["entries"][0])),
    lambda c: c["entries"][0]["evidence"][0].update(source="missing-source"),
    lambda c: c["entries"][0]["evidence"][0].update(lines=[100, 1]),
    lambda c: c["entries"][0]["evidence"][0].update(path="../private.txt"),
    lambda c: c["entries"][-1]["match_any"][0].update(
        capture_types={"wrong_name": "positive_integer"}
    ),
    lambda c: c["entries"][0]["match_any"][0].update(error_code=True),
    lambda c: c["entries"][0]["match_any"][0].update(description_regex=".*"),
])
def test_invalid_catalogue_edits_are_rejected(mutation):
    catalogue = json.loads((ROOT / "catalogue/errors.json").read_text())
    mutation(catalogue)
    with pytest.raises((ValueError, ValidationError)):
        validate(catalogue)
