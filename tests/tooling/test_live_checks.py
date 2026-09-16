"""Exercise bounded live-check behavior using synthetic responses and a mock transport."""

from __future__ import annotations

import copy
import io
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

from tools import live_checks as live
from tools.validate import load_catalogue

TOKEN = "424242:TEST_TOKEN_NOT_A_REAL_SECRET"
BOT_ID = 424242
CHAT_ID = -1009000000001
OLD_CHAT_ID = -9000000001
MESSAGE_ID = 7654321
NOW = "2026-09-16T12:00:00Z"
CATALOGUE = load_catalogue()
ENTRIES = {entry["id"]: entry for entry in CATALOGUE["entries"]}


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Unit tests must not make network requests.")

    monkeypatch.setattr(urllib.request.OpenerDirector, "open", forbidden)


def config(**kwargs) -> live.Config:
    return live.Config(TOKEN, CHAT_ID, OLD_CHAT_ID, **kwargs)


def success(result: object) -> live.HttpResult:
    return live.HttpResult(200, {"ok": True, "result": result})


def failure(identity: str) -> live.HttpResult:
    response = copy.deepcopy(ENTRIES[identity]["example"]["response"])
    if identity == "chat.migrated":
        response["parameters"]["migrate_to_chat_id"] = CHAT_ID
    return live.HttpResult(response["error_code"], response)


def initial_responses() -> list[live.HttpResult]:
    return [
        success({"id": BOT_ID, "is_bot": True, "username": "private_test_bot"}),
        failure("chat.migrated"),
        failure("file.id_missing"),
        failure("text.empty"),
        failure("format.parse_mode_unsupported"),
    ]


def message_result(**changes) -> live.HttpResult:
    return success(
        {
            "message_id": MESSAGE_ID,
            "from": {"id": BOT_ID, "is_bot": True},
            "chat": {"id": CHAT_ID},
            "text": live.MESSAGE_TEXT,
            **changes,
        }
    )


class Transport:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def __call__(self, method, parameters):
        self.calls.append((method, copy.deepcopy(parameters)))
        if not self.replies:
            raise AssertionError("The request bound was exceeded.")
        reply = self.replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        return reply


def run(transport, **options):
    return live.run_checks(
        config(**options), transport=transport, catalogue=CATALOGUE, now=lambda: NOW
    )


def test_default_checks_are_bounded_and_never_edit_or_delete():
    transport = Transport(initial_responses())
    report = run(transport)
    assert report["status"] == "passed"
    assert report["cleanup"] == "not_needed"
    assert len(transport.calls) == 5
    assert [method for method, _ in transport.calls] == [
        "getMe",
        "getChatAdministrators",
        "getFile",
        "sendMessage",
        "sendMessage",
    ]
    for method, parameters in transport.calls:
        if method == "sendMessage":
            assert parameters["text"] == "" or parameters["parse_mode"] == "ErrorgramInvalid"
    assert report["deployment"] == {"host": "api.telegram.org", "api_version": "unknown"}
    assert report["sanitization"]["success_bodies"] == "omitted"
    assert report["sanitization"]["migration_target"] == "replaced with a synthetic identifier"
    assert report["started_at"] == report["finished_at"] == NOW
    assert "response" not in report["checks"][0]


def test_opt_in_checks_clean_up_only_the_new_message():
    transport = Transport(
        initial_responses()
        + [
            message_result(),
            failure("message.not_modified"),
            success(True),
            failure("message.edit_not_found"),
            failure("message.delete_not_found"),
        ]
    )
    report = run(transport, allow_message_tests=True)
    assert report["status"] == "passed"
    assert report["cleanup"] == "succeeded"
    assert len(transport.calls) == 10
    assert transport.calls[5] == (
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": live.MESSAGE_TEXT,
            "disable_notification": True,
        },
    )
    for method, parameters in transport.calls[6:]:
        assert method in {"editMessageText", "deleteMessage"}
        assert parameters["chat_id"] == CHAT_ID
        assert parameters["message_id"] == MESSAGE_ID
    rendered = json.dumps(report)
    for private in (TOKEN, str(BOT_ID), str(CHAT_ID), str(OLD_CHAT_ID), str(MESSAGE_ID)):
        assert private not in rendered
    assert str(live.SYNTHETIC_CHAT_ID) in rendered


@pytest.mark.parametrize(
    "failed_edit",
    [
        failure("chat.not_found"),
        success({"private": TOKEN}),
        RuntimeError("https://api.telegram.org/bot" + TOKEN),
    ],
)
def test_failed_edit_still_cleans_up_and_aborts_remaining_checks(failed_edit):
    transport = Transport(initial_responses() + [message_result(), failed_edit, success(True)])
    report = run(transport, allow_message_tests=True)
    assert report["status"] == "failed"
    assert report["cleanup"] == "succeeded"
    assert len(transport.calls) == 8
    assert transport.calls[-1] == (
        "deleteMessage",
        {"chat_id": CHAT_ID, "message_id": MESSAGE_ID},
    )
    assert TOKEN not in json.dumps(report)


def test_cleanup_failure_is_reported_without_retrying():
    transport = Transport(
        initial_responses()
        + [
            message_result(),
            failure("message.not_modified"),
            failure("message.delete_forbidden"),
        ]
    )
    report = run(transport, allow_message_tests=True)
    assert report["status"] == "failed"
    assert report["cleanup"] == "failed"
    assert len(transport.calls) == 8


def test_interrupted_edit_attempts_own_message_cleanup():
    transport = Transport(
        initial_responses() + [message_result(), KeyboardInterrupt(), success(True)]
    )
    report = run(transport, allow_message_tests=True)
    assert report["failure"] == "interrupted"
    assert report["cleanup"] == "succeeded"
    assert len(transport.calls) == 8


@pytest.mark.parametrize(
    "identity",
    [
        {"id": BOT_ID + 1, "is_bot": True},
        {"id": str(BOT_ID), "is_bot": True},
        {"id": BOT_ID, "is_bot": False},
        None,
    ],
)
def test_get_me_identity_mismatch_stops_before_chat_calls(identity):
    transport = Transport([success(identity)])
    report = run(transport, allow_message_tests=True)
    assert report["status"] == "failed"
    assert report["failure"] == "bot_identity_mismatch"
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "changes",
    [
        {"from": {"id": BOT_ID + 1, "is_bot": True}},
        {"chat": {"id": OLD_CHAT_ID}},
        {"message_id": True},
        {"message_id": 0},
        {"text": "Unexpected message"},
    ],
)
def test_unvalidated_created_message_is_never_used_as_a_delete_target(changes):
    transport = Transport(initial_responses() + [message_result(**changes)])
    report = run(transport, allow_message_tests=True)
    assert report["failure"] == "created_message_identity_mismatch"
    assert report["cleanup"] == "unavailable"
    assert len(transport.calls) == 6
    assert all(method != "deleteMessage" for method, _ in transport.calls)


def test_unexpected_success_aborts_and_omits_success_payload():
    replies = initial_responses()
    replies[1] = success({"secret": TOKEN, "chat": {"id": CHAT_ID}})
    transport = Transport(replies)
    report = run(transport)
    assert report["failure"] == "unexpected_success"
    assert len(transport.calls) == 2
    assert "response" not in report["checks"][1]
    assert TOKEN not in json.dumps(report)


def test_report_redacts_known_values_urls_and_unapproved_fields():
    replies = initial_responses()
    private_migration = -1009876543212
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    description = f"{TOKEN} {CHAT_ID} {OLD_CHAT_ID} {private_migration} private_test_bot {url}"
    description += " " + urllib.parse.quote(url, safe="")
    replies[1] = live.HttpResult(
        400,
        {
            "ok": False,
            "error_code": 400,
            "description": description,
            "parameters": {"migrate_to_chat_id": private_migration, "secret": TOKEN},
            "url": url,
            "chat_id": CHAT_ID,
        },
    )
    report = run(Transport(replies))
    assert report["status"] == "passed"
    rendered = json.dumps(report)
    for private in (
        TOKEN,
        str(BOT_ID),
        str(CHAT_ID),
        str(OLD_CHAT_ID),
        str(private_migration),
        "private_test_bot",
        url,
    ):
        assert private not in rendered
    response = report["checks"][1]["response"]
    assert set(response) == {"ok", "error_code", "description", "parameters"}
    assert response["parameters"] == {"migrate_to_chat_id": live.SYNTHETIC_CHAT_ID}


def test_transport_exceptions_never_reach_report_or_console(capsys):
    report = run(Transport([RuntimeError(f"Request failed: https://example.test/{TOKEN}")]))
    assert report["failure"] == "transport_failed"
    assert TOKEN not in json.dumps(report)
    assert capsys.readouterr() == ("", "")


def test_real_transport_suppresses_credential_bearing_urllib_errors(monkeypatch):
    transport = live.TelegramTransport(config())

    def fail(*args, **kwargs):
        raise urllib.error.URLError(f"https://api.telegram.org/bot{TOKEN}/getMe")

    monkeypatch.setattr(transport._opener, "open", fail)
    with pytest.raises(live.CheckFailure, match="^transport_failed$") as caught:
        transport("getMe", {})
    assert caught.value.__suppress_context__ is True
    assert TOKEN not in str(caught.value)


def test_real_transport_posts_once_and_encodes_silent_flag(monkeypatch):
    transport = live.TelegramTransport(config(direct=True))
    calls = []

    def respond(request, timeout):
        calls.append(request)
        assert request.get_method() == "POST"
        assert timeout == 15
        assert urllib.parse.parse_qs(request.data.decode())["disable_notification"] == ["true"]
        response = io.BytesIO(b'{"ok":true,"result":true}')
        response.code = 200
        return response

    monkeypatch.setattr(transport._opener, "open", respond)
    assert transport("sendMessage", {"disable_notification": True}).body == {
        "ok": True,
        "result": True,
    }
    assert len(calls) == 1
    assert not any(
        isinstance(handler, urllib.request.ProxyHandler) for handler in transport._opener.handlers
    )
    assert (
        live.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.test") is None
    )


def test_http_error_body_is_read_without_exposing_url(monkeypatch):
    transport = live.TelegramTransport(config())

    def respond(*args, **kwargs):
        body = b'{"ok":false,"error_code":400,"description":"Bad Request: file_id not specified"}'
        raise urllib.error.HTTPError(
            f"https://api.telegram.org/bot{TOKEN}/getFile", 400, "Bad Request", {}, io.BytesIO(body)
        )

    monkeypatch.setattr(transport._opener, "open", respond)
    reply = transport("getFile", {"file_id": ""})
    assert reply.status == 400
    assert reply.body["error_code"] == 400
    assert TOKEN not in repr(reply)


@pytest.mark.parametrize("body", [b"not JSON", b"x" * (live.MAX_RESPONSE_BYTES + 1)])
def test_invalid_or_oversized_transport_body_is_not_exposed(monkeypatch, body):
    transport = live.TelegramTransport(config())

    def respond(*args, **kwargs):
        response = io.BytesIO(body)
        response.code = 200
        return response

    monkeypatch.setattr(transport._opener, "open", respond)
    with pytest.raises(live.CheckFailure, match="^transport_failed$"):
        transport("getMe", {})


def test_missing_configuration_writes_only_a_safe_failure_report(tmp_path, monkeypatch, capsys):
    for name in ("TELEGRAM_TEST_BOT_TOKEN", "TELEGRAM_TEST_CHAT_ID", "TELEGRAM_MIGRATED_CHAT_ID"):
        monkeypatch.delenv(name, raising=False)
    output = tmp_path / "report.json"
    assert live.main(["--output", str(output)]) == 1
    report = json.loads(output.read_text())
    assert report["failure"] == "configuration_or_startup_failed"
    assert report["checks"] == []
    assert "Traceback" not in capsys.readouterr().err


def test_local_arguments_override_environment_without_echoing_values(tmp_path, monkeypatch):
    token_file = tmp_path / "synthetic-token.txt"
    token_file.write_text(TOKEN + "\n")
    monkeypatch.setenv("TELEGRAM_TEST_BOT_TOKEN", "invalid-environment-value")
    output = tmp_path / "report.json"
    configs = []

    def fake_run(configuration):
        configs.append(configuration)
        return {"status": "passed", "checks": []}

    monkeypatch.setattr(live, "run_checks", fake_run)
    assert (
        live.main(
            [
                "--output",
                str(output),
                "--token-file",
                str(token_file),
                "--chat-id",
                str(CHAT_ID),
                "--migrated-chat-id",
                str(OLD_CHAT_ID),
                "--allow-message-tests",
                "--direct",
            ]
        )
        == 0
    )
    assert configs == [config(allow_message_tests=True, direct=True)]
    assert TOKEN not in repr(configs)
    assert TOKEN not in Path(output).read_text()
