"""Retired generated pages must not stay published or delete authored content."""

import json

import pytest

from tools import generate


def write_manifest(root, paths):
    (root / "site").mkdir()
    (root / "site/generated-manifest.json").write_text(
        json.dumps({"generator": "tools/codegen_docs.py", "paths": paths})
    )


def test_retired_condition_removes_only_its_generated_exports(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    retired = [
        "site/src/content/docs/errors/retired.condition.md",
        "site/public/errors/retired.condition.md",
        "site/public/errors/retired.condition.json",
    ]
    retained = "site/public/catalogue.json"
    write_manifest(tmp_path, [*retired, retained])
    assert generate.obsolete_outputs({retained: "{}"}) == sorted(retired)


@pytest.mark.parametrize("path", [
    "README.md",
    "site/src/content/docs/python.md",
    "site/public/errors/../../../README.md",
    "/tmp/unrelated.md",
])
def test_manifest_cannot_remove_authored_or_external_files(tmp_path, monkeypatch, path):
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    write_manifest(tmp_path, [path])
    with pytest.raises(ValueError, match="unowned path"):
        generate.obsolete_outputs({})
