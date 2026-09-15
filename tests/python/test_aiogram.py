"""Exercise aiogram's real response parser without making network requests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import (
    ClientDecodeError,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramMigrateToChat,
    TelegramNetworkError,
    TelegramRetryAfter,
)
from aiogram.methods import (
    AnswerCallbackQuery,
    DeleteMessage,
    EditMessageText,
    GetChat,
    GetFile,
    GetMe,
    GetUpdates,
    SendMessage,
    SetWebhook,
)
from errorgram.aiogram import EnrichedError, MessageNotModified, enrich
from errorgram.aiogram._errors import EXCEPTION_TYPES

CATALOGUE = json.loads((Path(__file__).resolve().parents[2] / "catalogue/errors.json").read_text())
METHODS = {
    "answerCallbackQuery": AnswerCallbackQuery(callback_query_id="example"),
    "deleteMessage": DeleteMessage(chat_id=42, message_id=7),
    "editMessageText": EditMessageText(text="Hello", chat_id=42, message_id=7),
    "getChat": GetChat(chat_id=42),
    "getFile": GetFile(file_id="example"),
    "getMe": GetMe(),
    "getUpdates": GetUpdates(),
    "sendMessage": SendMessage(chat_id=42, text="Hello"),
    "setWebhook": SetWebhook(url="https://example.test/webhook"),
}


def parse_error(response: dict, method_name: str, *, status: int | None = None) -> TelegramAPIError:
    session = AiohttpSession()
    bot = Bot("123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi", session=session)
    with pytest.raises(TelegramAPIError) as caught:
        session.check_response(
            bot,
            METHODS[method_name],
            response["error_code"] if status is None else status,
            json.dumps(response),
        )
    return caught.value


@pytest.mark.parametrize("entry", CATALOGUE["entries"], ids=lambda entry: entry["id"])
def test_real_parser_produces_compatible_concrete_errors(entry: dict) -> None:
    example = entry["example"]
    original = parse_error(example["response"], example["method"])
    original_attributes = original.__dict__.copy()
    enriched = enrich(original)
    assert isinstance(enriched, EnrichedError)
    assert isinstance(enriched, type(original))
    assert isinstance(enriched, EXCEPTION_TYPES[entry["id"]])
    assert enriched.original is original
    assert enriched.id == entry["id"]
    assert enriched.classification.status == "matched"
    assert enriched.classification.response is not example["response"]
    assert enriched.fidelity.response == "reconstructed"
    assert enriched.fidelity.error_code == "inferred"
    assert enriched.fidelity.parameters == "partial"
    assert enriched.message == original.message
    assert enriched.method is original.method
    assert enriched.args == original.args
    assert str(enriched) == str(original)
    assert original.__dict__ == original_attributes
    assert enrich(enriched) is enriched
    with pytest.raises(type(original)):
        raise enriched


@pytest.mark.parametrize(
    ("condition_id", "parameter"),
    [("request.retry_after", "retry_after"), ("chat.migrated", "migrate_to_chat_id")],
)
def test_recovery_parameters_survive_without_rewriting_the_message_again(
    condition_id: str, parameter: str
) -> None:
    entry = next(entry for entry in CATALOGUE["entries"] if entry["id"] == condition_id)
    original = parse_error(entry["example"]["response"], "sendMessage")
    assert isinstance(original, (TelegramRetryAfter, TelegramMigrateToChat))
    enriched = enrich(original)
    assert getattr(enriched, parameter) == entry["example"]["response"]["parameters"][parameter]
    assert enriched.facts[parameter] == getattr(enriched, parameter)
    assert enriched.message.count("Original description:") == 1
    assert enriched.fidelity.description == "framework_modified"


def test_standard_bad_request_catches_still_work() -> None:
    entry = next(entry for entry in CATALOGUE["entries"] if entry["id"] == "message.not_modified")
    original = parse_error(entry["example"]["response"], "editMessageText")
    error = enrich(original)
    assert isinstance(error, MessageNotModified)
    with pytest.raises(TelegramBadRequest):
        raise error


def test_custom_exception_subclass_and_diagnostics_survive() -> None:
    class AppBadRequest(TelegramBadRequest):
        pass

    original = AppBadRequest(METHODS["getChat"], "Bad Request: chat not found")
    original.request_id = "request-123"
    original.__cause__ = ValueError("cause")
    original.add_note("Application context")
    enriched = enrich(original)
    assert isinstance(enriched, AppBadRequest)
    assert enriched.original is original
    assert enriched.request_id == "request-123"
    assert enriched.__notes__ == ["Application context"]
    assert enriched.__cause__ is original.__cause__


def test_custom_exception_slots_survive() -> None:
    class AppBadRequest(TelegramBadRequest):
        __slots__ = ("tracking_id",)

    original = AppBadRequest(METHODS["getChat"], "Bad Request: chat not found")
    original.tracking_id = "request-123"
    enriched = enrich(original)
    assert isinstance(enriched, AppBadRequest)
    assert enriched.tracking_id == "request-123"
    assert original.tracking_id == "request-123"


def test_enrichment_does_not_invoke_custom_exception_constructors() -> None:
    calls: list[str] = []

    class AppBadRequest(TelegramBadRequest):
        def __new__(cls, *args, **kwargs):
            calls.append("new")
            return super().__new__(cls)

        def __init__(self, *args, **kwargs):
            calls.append("init")
            super().__init__(*args, **kwargs)
            self.tracking_id = "request-123"

    original = AppBadRequest(METHODS["getChat"], "Bad Request: chat not found")
    assert calls == ["new", "init"]
    enriched = enrich(original)
    assert calls == ["new", "init"]
    assert enriched is not original
    assert isinstance(enriched, AppBadRequest)
    assert enriched.original is original
    assert enriched.args == original.args
    assert enriched.method is original.method
    assert enriched.message == original.message
    assert enriched.tracking_id == original.tracking_id


@pytest.mark.parametrize(
    "error",
    [
        TimeoutError("timed out"),
        ValueError("invalid arguments"),
        TelegramNetworkError(METHODS["getChat"], "Bad Request: chat not found"),
        TelegramBadRequest(METHODS["getChat"], "Bad Request: new condition"),
        ClientDecodeError("invalid JSON", ValueError("JSON"), "not JSON"),
    ],
)
def test_unknown_and_out_of_scope_exceptions_pass_through(error: Exception) -> None:
    assert enrich(error) is error


def test_inferred_code_is_never_presented_as_the_original_wire_response() -> None:
    response = {"ok": False, "error_code": 503, "description": "Internal Server Error: restart"}
    original = parse_error(response, "getMe")
    enriched = enrich(original)
    assert enriched.id == "server.restarting"
    assert enriched.classification.response["error_code"] == 500
    assert enriched.fidelity.error_code == "inferred"
    assert enriched.fidelity.response == "reconstructed"
    assert enriched.original is original
