"""Validate the catalogue's schema, identities, and source references."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


def validate(catalogue: dict, schema: dict | None = None) -> None:
    """Reject records that cannot produce consistent bindings or evidence links."""
    if schema is None:
        schema = json.loads((ROOT / "catalogue/schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(catalogue)
    ids: set[str] = set()
    class_names: set[str] = set()
    known_parameters: set[str] = set()
    for entry in catalogue["entries"]:
        identity = entry["id"]
        class_name = "".join(part.capitalize() for part in re.split(r"[._]", identity))
        if identity in ids or class_name in class_names:
            raise ValueError(f"Duplicate condition ID or generated class name: {identity}")
        ids.add(identity)
        class_names.add(class_name)
        for rule in entry["match_any"]:
            known_parameters.update(rule.get("required_parameters", {}))
            if "description_template" in rule:
                template = rule["description_template"]
                names = re.findall(r"\{([a-z][a-z0-9_]*)\}", template)
                remaining = re.sub(r"\{[a-z][a-z0-9_]*\}", "", template)
                if (
                    len(names) != len(set(names))
                    or set(names) != set(rule["capture_types"])
                    or "{" in remaining
                    or "}" in remaining
                ):
                    raise ValueError(f"Template captures do not match their types: {identity}")
        for evidence in entry["evidence"]:
            source = catalogue["sources"].get(evidence["source"])
            if source is None:
                raise ValueError(f"Unknown evidence source: {evidence['source']}")
            if source["kind"] == "server_source" and "path" not in evidence:
                raise ValueError(f"Source evidence needs a file and line range: {identity}")
            if "path" in evidence:
                path = PurePosixPath(evidence["path"])
                if path.is_absolute() or ".." in path.parts or "\\" in evidence["path"]:
                    raise ValueError(
                        f"Evidence path must be relative to its repository: {identity}"
                    )
                if evidence["lines"][0] > evidence["lines"][1]:
                    raise ValueError(f"Evidence line range is reversed: {identity}")
    for group in catalogue["matching"]["exclusive_parameter_groups"]:
        if not set(group) <= known_parameters:
            raise ValueError("Exclusive parameters must have matching rules in the catalogue.")


def load_catalogue() -> dict:
    catalogue = json.loads((ROOT / "catalogue/errors.json").read_text())
    validate(catalogue)
    return catalogue


if __name__ == "__main__":
    try:
        data = load_catalogue()
    except ValidationError as error:
        location = ".".join(map(str, error.absolute_path)) or "root"
        raise SystemExit(f"Catalogue validation failed at {location}: {error.message}") from error
    except (ValueError, OSError) as error:
        raise SystemExit(f"Catalogue validation failed: {error}") from error
    print(f"Catalogue valid: {len(data['entries'])} conditions.")
