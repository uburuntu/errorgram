"""Match Bot API responses without changing application behavior."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from functools import lru_cache
from importlib.resources import files
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from ._generated import ConditionId

Status = Literal["matched", "unknown", "ambiguous", "insufficient_context", "not_api_error"]
MAX_SAFE_INTEGER = 2**53 - 1
_ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")
_PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")


@dataclass(frozen=True)
class Classification:
    """A classification and the untouched input that produced it."""

    status: Status
    response: Any
    catalogue_version: str
    id: ConditionId | str | None = None
    facts: dict[str, Any] = field(default_factory=dict)
    candidates: tuple[str, ...] = ()
    entry: Mapping[str, Any] | None = None


@lru_cache(maxsize=1)
def _default_catalogue() -> dict[str, Any]:
    return json.loads(files("errorgram").joinpath("catalogue.json").read_text(encoding="utf-8"))


def catalogue() -> dict[str, Any]:
    """Return a fresh copy of the catalogue, including evidence sources."""
    return deepcopy(_default_catalogue())


def _integer(value: object, kind: str) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if isinstance(value, float) and (not math.isfinite(value) or not value.is_integer()):
        return False
    if abs(value) > MAX_SAFE_INTEGER:
        return False
    if kind == "positive_integer":
        return value > 0
    if kind == "nonzero_integer":
        return value != 0
    return False


@lru_cache(maxsize=256)
def _template_pattern(template: str) -> re.Pattern[str]:
    parts: list[str] = []
    offset = 0
    for placeholder in _PLACEHOLDER.finditer(template):
        parts.append(re.escape(template[offset : placeholder.start()]))
        parts.append(f"(?P<{placeholder.group(1)}>-?[0-9]+)")
        offset = placeholder.end()
    parts.append(re.escape(template[offset:]))
    return re.compile("".join(parts))


def _match_base(
    rule: Mapping[str, Any], response: Mapping[str, Any], parameters: Mapping[str, Any]
) -> dict[str, Any] | None:
    if response["error_code"] != rule["error_code"]:
        return None
    facts: dict[str, Any] = {}
    if "description_exact" in rule and response["description"] != rule["description_exact"]:
        return None
    if "description_template" in rule:
        match = _template_pattern(rule["description_template"]).fullmatch(response["description"])
        if match is None:
            return None
        for name, kind in rule.get("capture_types", {}).items():
            captured = match.groupdict().get(name)
            if captured is None:
                return None
            digits = captured.lstrip("-").lstrip("0") or "0"
            if len(digits) > 16:
                return None
            value = int(digits) * (-1 if captured.startswith("-") else 1)
            if not _integer(value, kind):
                return None
            facts[name] = value
    for name, kind in rule.get("required_parameters", {}).items():
        value = parameters.get(name)
        if not _integer(value, kind):
            return None
        if name in facts and facts[name] != value:
            return None
        facts[name] = int(value)
    return facts


def classify(
    response: object,
    *,
    method: str | None = None,
    catalogue: Mapping[str, Any] | None = None,
) -> Classification:
    """Identify a Bot API error. Unknown responses remain unknown."""
    data = _default_catalogue() if catalogue is None else catalogue
    version = str(data["catalogue_version"])

    def result(status: Status, **kwargs: Any) -> Classification:
        return Classification(status, response, version, **kwargs)

    if (
        not isinstance(response, Mapping)
        or response.get("ok") is not False
        or not _integer(response.get("error_code"), "positive_integer")
        or not isinstance(response.get("description"), str)
        or ("parameters" in response and not isinstance(response["parameters"], Mapping))
    ):
        return result("not_api_error")

    parameters = response.get("parameters", {})
    parameter_types: dict[str, set[str]] = {}
    parameter_ids: dict[str, set[str]] = {}
    for entry in data["entries"]:
        for rule in entry["match_any"]:
            for name, kind in rule.get("required_parameters", {}).items():
                parameter_types.setdefault(name, set()).add(kind)
                parameter_ids.setdefault(name, set()).add(entry["id"])
    present = parameter_types.keys() & parameters.keys()
    if any(
        not any(_integer(parameters[name], kind) for kind in parameter_types[name])
        for name in present
    ):
        return result("unknown")
    for group in data.get("matching", {}).get("exclusive_parameter_groups", []):
        conflicting = present.intersection(group)
        if len(conflicting) > 1:
            candidates = sorted(set().union(*(parameter_ids[name] for name in conflicting)))
            return result("ambiguous", candidates=tuple(candidates))

    normalized_method = method.translate(_ASCII_LOWER) if isinstance(method, str) else None
    matches: list[tuple[int, Mapping[str, Any], dict[str, Any], bool]] = []
    for entry in data["entries"]:
        for rule in entry["match_any"]:
            structured = bool(rule.get("required_parameters"))
            if present and not structured:
                continue
            facts = _match_base(rule, response, parameters)
            if facts is None:
                continue
            required_method = rule.get("method")
            if required_method and normalized_method is not None:
                if normalized_method != required_method:
                    continue
            missing_method = bool(required_method and normalized_method is None)
            matches.append((int(structured), entry, facts, missing_method))

    if not matches:
        return result("unknown")
    priority = max(match[0] for match in matches)
    preferred = [match for match in matches if match[0] == priority]
    candidates = tuple(sorted({match[1]["id"] for match in preferred}))
    resolved = {match[1]["id"] for match in preferred if not match[3]}
    if any(match[3] and match[1]["id"] not in resolved for match in preferred):
        return result("insufficient_context", candidates=candidates)
    if len(candidates) > 1:
        return result("ambiguous", candidates=candidates)
    _, entry, facts, _ = next(match for match in preferred if not match[3])
    return result("matched", id=entry["id"], entry=deepcopy(entry), facts=facts)
