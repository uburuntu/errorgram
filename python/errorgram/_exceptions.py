"""Optional concrete exceptions for framework-independent callers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ._classifier import Classification, classify


class ApiError(Exception):
    """A Bot API response with its classification attached."""

    def __init__(self, classification: Classification) -> None:
        self.classification = classification
        self.response = classification.response
        self.id = classification.id
        self.facts = classification.facts
        super().__init__(self.response["description"])


def to_exception(
    response: object,
    *,
    method: str | None = None,
    catalogue: Mapping[str, Any] | None = None,
) -> ApiError | None:
    """Build an exception without raising it; return None for non-API inputs."""
    from .errors import EXCEPTION_TYPES

    classification = classify(response, method=method, catalogue=catalogue)
    if classification.status == "not_api_error":
        return None
    error_type = EXCEPTION_TYPES.get(classification.id, ApiError)
    return error_type(classification)
