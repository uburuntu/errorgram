"""Generation must not silently merge distinct public exception types."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.codegen_python import render


def test_generated_python_class_name_collision_is_rejected() -> None:
    source = Path(__file__).resolve().parents[2] / "catalogue/errors.json"
    catalogue = json.loads(source.read_text())
    duplicate = copy.deepcopy(catalogue["entries"][0])
    catalogue["entries"][0]["id"] = "message.not_modified"
    duplicate["id"] = "message_not.modified"
    catalogue["entries"].append(duplicate)
    with pytest.raises(ValueError, match="distinct Python class names"):
        render(catalogue)
