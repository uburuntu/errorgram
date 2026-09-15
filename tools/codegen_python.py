"""Render Python data, stable IDs, and concrete exception classes."""

from __future__ import annotations

import json
from typing import Any

HEADER = '"""Generated from catalogue/errors.json. Run make generate to update."""\n\n'


def _class_name(condition_id: str) -> str:
    return "".join(part.capitalize() for part in condition_id.replace(".", "_").split("_"))


def _aiogram_base(entry: dict[str, Any]) -> str:
    parameters = set().union(*(rule.get("required_parameters", {}) for rule in entry["match_any"]))
    if "retry_after" in parameters:
        return "TelegramRetryAfter"
    if "migrate_to_chat_id" in parameters:
        return "TelegramMigrateToChat"
    if entry["id"] == "server.restarting":
        return "RestartingTelegram"
    code = entry["match_any"][0]["error_code"]
    return {
        400: "TelegramBadRequest",
        401: "TelegramUnauthorizedError",
        403: "TelegramForbiddenError",
        404: "TelegramNotFound",
        409: "TelegramConflictError",
        500: "TelegramServerError",
    }.get(code, "TelegramAPIError")


def _export_block(module: str, names: list[str]) -> str:
    return f"from {module} import (\n" + "".join(f"    {name},\n" for name in sorted(names)) + ")\n"


def render(catalogue: dict[str, Any]) -> dict[str, str]:
    """Return deterministic package files for the shared generator."""
    entries = sorted(catalogue["entries"], key=lambda entry: entry["id"])
    names = [_class_name(entry["id"]) for entry in entries]
    if len(names) != len(set(names)):
        raise ValueError("Condition IDs must produce distinct Python class names.")
    ids = [entry["id"] for entry in entries]
    generated = HEADER + "from typing import Literal\n\n"
    generated += f"CATALOGUE_VERSION = {catalogue['catalogue_version']!r}\n"
    generated += "ConditionId = Literal[\n" + "".join(f"    {value!r},\n" for value in ids) + "]\n"
    generated += "CONDITION_IDS: tuple[ConditionId, ...] = (\n"
    generated += "".join(f"    {value!r},\n" for value in ids) + ")\n"

    errors = HEADER + "from ._exceptions import ApiError\n\n"
    for entry, name in zip(entries, names, strict=True):
        errors += f"\nclass {name}(ApiError):\n    {entry['summary']!r}\n\n"
    errors += "\nEXCEPTION_TYPES: dict[str | None, type[ApiError]] = {\n"
    errors += "".join(
        f"    {entry['id']!r}: {name},\n" for entry, name in zip(entries, names, strict=True)
    )
    errors += "}\n"

    bases = sorted({_aiogram_base(entry) for entry in entries})
    adapter_errors = HEADER + _export_block("aiogram.exceptions", bases)
    adapter_errors += "\nfrom ._adapter import EnrichedError\n\n"
    for entry, name in zip(entries, names, strict=True):
        adapter_errors += f"\nclass {name}(EnrichedError, {_aiogram_base(entry)}):\n"
        adapter_errors += f"    {entry['summary']!r}\n\n"
    adapter_errors += "\nEXCEPTION_TYPES: dict[str | None, type[EnrichedError]] = {\n"
    adapter_errors += "".join(
        f"    {entry['id']!r}: {name},\n" for entry, name in zip(entries, names, strict=True)
    )
    adapter_errors += "}\n"

    exports = HEADER
    exports += "from ._classifier import Classification, Status, catalogue, classify\n"
    exports += "from ._exceptions import ApiError, to_exception\n"
    exports += "from ._generated import CATALOGUE_VERSION, CONDITION_IDS, ConditionId\n"
    exports += _export_block(".errors", names)
    public = [
        "ApiError",
        "CATALOGUE_VERSION",
        "CONDITION_IDS",
        "Classification",
        "ConditionId",
        "Status",
        "catalogue",
        "classify",
        "to_exception",
        *names,
    ]
    exports += "\n__all__ = [\n" + "".join(f"    {name!r},\n" for name in sorted(public)) + "]\n"

    adapter_exports = HEADER + "from ._adapter import EnrichedError, SourceFidelity, enrich\n"
    adapter_exports += _export_block("._errors", names)
    adapter_exports += "\n__all__ = [\n"
    adapter_exports += (
        "".join(
            f"    {name!r},\n"
            for name in sorted(["EnrichedError", "SourceFidelity", "enrich", *names])
        )
        + "]\n"
    )

    return {
        "python/errorgram/catalogue.json": json.dumps(catalogue, ensure_ascii=False, indent=2)
        + "\n",
        "python/errorgram/_generated.py": generated,
        "python/errorgram/errors.py": errors,
        "python/errorgram/__init__.py": exports,
        "python/errorgram/aiogram/_errors.py": adapter_errors,
        "python/errorgram/aiogram/__init__.py": adapter_exports,
    }
