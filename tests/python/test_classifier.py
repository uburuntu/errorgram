"""Shared response fixtures and decisions that must survive catalogue changes."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from errorgram import (
    CATALOGUE_VERSION,
    CONDITION_IDS,
    ApiError,
    MessageNotModified,
    catalogue,
    classify,
    to_exception,
)

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = json.loads((ROOT / "catalogue/errors.json").read_text())
FIXTURES = ROOT / "fixtures/conformance.json"


def _case_names() -> list[dict]:
    return json.loads(FIXTURES.read_text())["cases"]


@pytest.mark.parametrize("case", _case_names(), ids=lambda case: case["name"])
def test_shared_conformance(case: dict) -> None:
    result = classify(case["response"], method=case.get("method"))
    expected = case["expected"]
    assert result.status == expected["status"]
    assert result.id == expected.get("id")
    assert result.facts == expected.get("facts", {})
    assert list(result.candidates) == expected.get("candidates", [])
    assert result.response is case["response"]
    assert result.catalogue_version == CATALOGUE_VERSION


@pytest.mark.parametrize("entry", CATALOGUE["entries"], ids=lambda entry: entry["id"])
def test_every_catalogue_example(entry: dict) -> None:
    example = entry["example"]
    result = classify(example["response"], method=example.get("method"))
    assert result.status == "matched"
    assert result.id == entry["id"]
    assert result.entry == entry
    exception = to_exception(example["response"], method=example.get("method"))
    assert isinstance(exception, ApiError)
    assert type(exception) is not ApiError
    assert exception.id == entry["id"]
    assert exception.response is example["response"]


def test_generated_ids_cover_catalogue() -> None:
    assert set(CONDITION_IDS) == {entry["id"] for entry in CATALOGUE["entries"]}


def test_catalogue_metadata_is_an_independent_snapshot() -> None:
    snapshot = catalogue()
    snapshot["entries"].clear()
    snapshot["sources"].clear()
    assert catalogue() == CATALOGUE


def test_matched_metadata_cannot_change_later_classifications() -> None:
    response = CATALOGUE["entries"][0]["example"]["response"]
    result = classify(response)
    result.entry["match_any"].clear()
    result.entry["summary"] = "Changed by the application"
    fresh = classify(response)
    assert fresh.id == "message.not_modified"
    assert fresh.entry == CATALOGUE["entries"][0]


def test_concrete_exception_is_optional_and_preserves_response() -> None:
    response = CATALOGUE["entries"][0]["example"]["response"]
    error = to_exception(response)
    assert isinstance(error, MessageNotModified)
    assert str(error) == response["description"]
    assert error.response is response
    with pytest.raises(ApiError):
        raise error


def test_unknown_response_has_a_generic_exception() -> None:
    response = {"ok": False, "error_code": 499, "description": "Future condition"}
    error = to_exception(response)
    assert type(error) is ApiError
    assert error.classification.status == "unknown"
    assert error.id is None
    assert to_exception(TimeoutError("timed out")) is None
    assert to_exception({"ok": True, "result": 1}) is None


def test_colliding_entries_remain_ambiguous() -> None:
    catalogue = copy.deepcopy(CATALOGUE)
    duplicate = copy.deepcopy(catalogue["entries"][0])
    duplicate["id"] = "other.same_text"
    catalogue["entries"].append(duplicate)
    result = classify(duplicate["example"]["response"], catalogue=catalogue)
    assert result.status == "ambiguous"
    assert result.candidates == ("message.not_modified", "other.same_text")
    assert result.id is None


def test_unresolved_competitor_requires_method_context() -> None:
    catalogue = copy.deepcopy(CATALOGUE)
    duplicate = copy.deepcopy(catalogue["entries"][0])
    duplicate["id"] = "other.method_specific"
    duplicate["match_any"][0]["method"] = "getfile"
    catalogue["entries"].append(duplicate)
    response = duplicate["example"]["response"]
    assert classify(response, catalogue=catalogue).status == "insufficient_context"
    assert classify(response, method="getFile", catalogue=catalogue).status == "ambiguous"
    assert (
        classify(response, method="editMessageText", catalogue=catalogue).id
        == "message.not_modified"
    )


def test_equivalent_alternatives_do_not_require_extra_context() -> None:
    catalogue = copy.deepcopy(CATALOGUE)
    entry = catalogue["entries"][0]
    rule = dict(entry["match_any"][0], method="editmessagetext")
    entry["match_any"].insert(0, rule)
    assert classify(entry["example"]["response"], catalogue=catalogue).id == entry["id"]


@pytest.mark.parametrize(
    ("parameter", "status", "facts"),
    [(9, "unknown", {}), (5, "matched", {"n": 5}), (5.0, "matched", {"n": 5})],
)
def test_template_and_structured_facts_must_agree(
    parameter: int | float, status: str, facts: dict
) -> None:
    catalogue = copy.deepcopy(CATALOGUE)
    entry = catalogue["entries"][0]
    entry["id"] = "example.shared_fact"
    entry["match_any"] = [
        {
            "error_code": 400,
            "description_template": "value {n}",
            "capture_types": {"n": "positive_integer"},
            "required_parameters": {"n": "positive_integer"},
        }
    ]
    catalogue["entries"] = [entry]
    response = {
        "ok": False,
        "error_code": 400,
        "description": "value 5",
        "parameters": {"n": parameter},
    }
    result = classify(response, catalogue=catalogue)
    assert result.status == status
    assert result.facts == facts
    assert result.id == (entry["id"] if status == "matched" else None)


@pytest.mark.parametrize(
    "value", [True, False, 0, -1, "5", None, float("nan"), float("inf"), 2**53]
)
def test_invalid_recovery_values_never_fall_back_to_text(value: object) -> None:
    response = copy.deepcopy(CATALOGUE["entries"][0]["example"]["response"])
    response["parameters"] = {"retry_after": value}
    assert classify(response).status == "unknown"


def test_valid_parameter_with_conflicting_code_does_not_fall_back_to_text() -> None:
    response = copy.deepcopy(CATALOGUE["entries"][0]["example"]["response"])
    response["parameters"] = {"retry_after": 5}
    assert classify(response).status == "unknown"


def test_parameter_rule_takes_precedence_over_description() -> None:
    response = copy.deepcopy(CATALOGUE["entries"][0]["example"]["response"])
    response["parameters"] = {"migrate_to_chat_id": -100123}
    result = classify(response)
    assert result.id == "chat.migrated"
    assert result.facts == {"migrate_to_chat_id": -100123}


@pytest.mark.parametrize("value", [True, 0, -1, "400", float("nan"), float("inf"), 2**53])
def test_invalid_error_codes(value: object) -> None:
    response = {"ok": False, "error_code": value, "description": "Bad Request: chat not found"}
    assert classify(response).status == "not_api_error"


def test_integral_json_numbers_match_across_languages() -> None:
    response = {
        "ok": False,
        "error_code": 429.0,
        "description": "Any description",
        "parameters": {"retry_after": 5.0},
    }
    result = classify(response)
    assert result.id == "request.retry_after"
    assert result.facts == {"retry_after": 5}


def test_template_escapes_literal_regex_characters() -> None:
    response = {
        "ok": False,
        "error_code": 400,
        "description": "Bad Request: certificate size is too big X4194304 bytesY",
    }
    assert classify(response).status == "unknown"
    response["description"] = "Bad Request: certificate size is too big (4194304 bytes)\n"
    assert classify(response).status == "unknown"


def test_template_leading_zeroes_are_not_a_different_number() -> None:
    response = {
        "ok": False,
        "error_code": 400,
        "description": "Bad Request: certificate size is too big (" + "0" * 5000 + "5 bytes)",
    }
    assert classify(response).facts == {"size_bytes": 5}


def test_core_imports_without_aiogram() -> None:
    script = """
import importlib.abc
import sys
class BlockAiogram(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == 'aiogram' or fullname.startswith('aiogram.'):
            raise AssertionError('Core imported aiogram')
sys.meta_path.insert(0, BlockAiogram())
import errorgram
assert errorgram.classify({'ok': True}).status == 'not_api_error'
assert 'aiogram' not in sys.modules
"""
    subprocess.run([sys.executable, "-c", script], check=True)
