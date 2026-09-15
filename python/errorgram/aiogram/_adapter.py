"""Opt-in aiogram exception enrichment."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from types import MemberDescriptorType
from typing import Any, Literal

from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramNetworkError,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramUnauthorizedError,
)

from .._classifier import Classification, _default_catalogue, classify


@dataclass(frozen=True)
class SourceFidelity:
    """What aiogram retained, and what the adapter had to infer."""

    response: Literal["reconstructed"] = "reconstructed"
    error_code: Literal["inferred"] = "inferred"
    description: Literal["preserved", "framework_modified"] = "preserved"
    parameters: Literal["partial"] = "partial"


class EnrichedError:
    """Metadata added to an aiogram exception without changing its message."""

    original: TelegramAPIError
    classification: Classification
    fidelity: SourceFidelity
    id: str
    facts: dict[str, Any]


_STATUS_TYPES: tuple[tuple[type[TelegramAPIError], int], ...] = (
    (TelegramBadRequest, 400),
    (TelegramUnauthorizedError, 401),
    (TelegramForbiddenError, 403),
    (TelegramNotFound, 404),
    (TelegramConflictError, 409),
    (TelegramServerError, 500),
)


@lru_cache(maxsize=128)
def _compatible_type(
    condition: type[EnrichedError], original_type: type[TelegramAPIError]
) -> type[EnrichedError]:
    if issubclass(condition, original_type):
        return condition
    return type(
        condition.__name__, (condition, original_type), {"__module__": condition.__module__}
    )


def enrich(error: Exception) -> Exception:
    """Return a more precise aiogram exception, or the original if it cannot be identified.

    The attached classification uses a reconstructed response. aiogram does not
    retain the wire error code or every response parameter.
    """
    from ._errors import EXCEPTION_TYPES

    if (
        isinstance(error, EnrichedError)
        or not isinstance(error, TelegramAPIError)
        or isinstance(error, TelegramNetworkError)
    ):
        return error

    parameters: dict[str, Any] = {}
    modified = False
    if isinstance(error, TelegramRetryAfter):
        codes = [429]
        parameters["retry_after"] = error.retry_after
        modified = True
    elif isinstance(error, TelegramMigrateToChat):
        codes = [400]
        parameters["migrate_to_chat_id"] = error.migrate_to_chat_id
        modified = True
    else:
        codes = [code for kind, code in _STATUS_TYPES if isinstance(error, kind)]
        if not codes:
            # aiogram has no dedicated class for status codes such as 421.
            represented = {code for _, code in _STATUS_TYPES} | {429}
            codes = sorted(
                {
                    rule["error_code"]
                    for entry in _default_catalogue()["entries"]
                    for rule in entry["match_any"]
                    if rule["error_code"] not in represented
                }
            )

    method_name = getattr(error.method, "__api_method__", None)
    matches: list[Classification] = []
    for code in codes:
        reconstructed = {
            "ok": False,
            "error_code": code,
            "description": error.message,
            "parameters": parameters,
        }
        classification = classify(reconstructed, method=method_name)
        if classification.status == "matched":
            matches.append(classification)
    if len(matches) != 1:
        return error
    classification = matches[0]
    condition = EXCEPTION_TYPES.get(classification.id)
    if condition is None:
        return error

    try:
        enriched_type = _compatible_type(condition, type(error))
        enriched = BaseException.__new__(enriched_type)
    except TypeError:
        # A custom exception layout may not support a compatible subclass.
        return error
    BaseException.__init__(enriched, *error.args)
    enriched.__dict__.update(error.__dict__)
    for base in type(error).__mro__:
        for descriptor in vars(base).values():
            if isinstance(descriptor, MemberDescriptorType):
                try:
                    value = descriptor.__get__(error, type(error))
                except AttributeError:
                    continue
                descriptor.__set__(enriched, value)
    enriched.__traceback__ = error.__traceback__
    enriched.__cause__ = error.__cause__
    enriched.__context__ = error.__context__
    enriched.__suppress_context__ = error.__suppress_context__
    enriched.original = error
    enriched.classification = classification
    enriched.fidelity = SourceFidelity(
        description="framework_modified" if modified else "preserved"
    )
    enriched.id = classification.id
    enriched.facts = classification.facts
    return enriched
