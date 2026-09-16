#!/usr/bin/env python3
"""Run bounded Telegram checks and write a sanitized observation report."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from errorgram import classify

if __package__:
    from .validate import load_catalogue
else:
    from validate import load_catalogue

HOST = "api.telegram.org"
SYNTHETIC_CHAT_ID = -1001234567890
MESSAGE_TEXT = "Errorgram verification"
MAX_RESPONSE_BYTES = 65536
MAX_REQUESTS = 10
SANITIZATION = {
    "success_bodies": "omitted",
    "descriptions": "URLs, credentials and known values redacted; limited to 4096 characters",
    "migration_target": "replaced with a synthetic identifier",
    "parameters": "only migrate_to_chat_id and retry_after retained",
}
METHODS = {
    "getMe",
    "getChatAdministrators",
    "getFile",
    "sendMessage",
    "editMessageText",
    "deleteMessage",
}


class CheckFailure(ValueError):
    """A fixed, non-sensitive failure code; never wrap raw transport messages."""


@dataclass(frozen=True)
class Config:
    token: str = field(repr=False)
    chat_id: int = field(repr=False)
    migrated_chat_id: int = field(repr=False)
    allow_message_tests: bool = False
    direct: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.token, str) or not re.fullmatch(
            r"[1-9][0-9]*:[A-Za-z0-9_-]+", self.token
        ):
            raise CheckFailure("configuration_invalid")
        for value in (self.chat_id, self.migrated_chat_id):
            if type(value) is not int or not -(2**52) < value < 0:
                raise CheckFailure("configuration_invalid")

    @property
    def bot_id(self) -> int:
        return int(self.token.split(":", 1)[0])


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: object = field(repr=False)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class TelegramTransport:
    """Use one HTTPS request per call; redirects and retries are disabled."""

    def __init__(self, config: Config):
        self._token = config.token
        handlers: list[Any] = [NoRedirect()]
        if config.direct:
            handlers.append(urllib.request.ProxyHandler({}))
        self._opener = urllib.request.build_opener(*handlers)

    def __call__(self, method: str, parameters: dict[str, Any]) -> HttpResult:
        if method not in METHODS:
            raise CheckFailure("method_not_allowed")
        try:
            request = urllib.request.Request(
                f"https://{HOST}/bot{self._token}/{method}",
                data=urllib.parse.urlencode(
                    {
                        key: str(value).lower() if type(value) is bool else value
                        for key, value in parameters.items()
                    }
                ).encode("utf-8"),
                headers={"User-Agent": "Errorgram verification"},
                method="POST",
            )
            try:
                response = self._opener.open(request, timeout=15)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                status = response.code
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise CheckFailure("response_too_large")
            return HttpResult(status, json.loads(raw))
        except Exception:
            # urllib exceptions can contain the complete credential-bearing URL.
            raise CheckFailure("transport_failed") from None


class Redactor:
    def __init__(self, config: Config):
        self._values: set[str] = set()
        for value in (
            config.token,
            config.token.split(":", 1)[1],
            config.bot_id,
            config.chat_id,
            config.migrated_chat_id,
        ):
            self.add(value)

    def add(self, value: object) -> None:
        if type(value) in (str, int) and str(value):
            self._values.add(str(value))

    def text(self, value: str) -> str:
        for private in sorted(self._values, key=len, reverse=True):
            for representation in {private, urllib.parse.quote(private, safe="")}:
                if re.fullmatch(r"-?[0-9]+", representation):
                    pattern = r"(?<![0-9])" + re.escape(representation) + r"(?![0-9])"
                    value = re.sub(pattern, "[redacted]", value)
                else:
                    value = value.replace(representation, "[redacted]")
        value = re.sub(
            r"https?(?:://|%3A%2F%2F)[^\s<>\"']+", "[redacted URL]", value, flags=re.IGNORECASE
        )
        value = re.sub(r"\b[0-9]+:[A-Za-z0-9_-]{10,}", "[redacted token]", value)
        return value[:4096]

    def envelope(self, body: object) -> dict[str, Any] | None:
        if not isinstance(body, dict) or body.get("ok") is not False:
            return None
        code, description = body.get("error_code"), body.get("description")
        if type(code) is not int or not 0 < code <= 2**53 - 1 or not isinstance(description, str):
            return None
        parameters = body.get("parameters")
        if isinstance(parameters, dict):
            self.add(parameters.get("migrate_to_chat_id"))
        result: dict[str, Any] = {
            "ok": False,
            "error_code": code,
            "description": self.text(description),
        }
        clean_parameters = {}
        if isinstance(parameters, dict):
            migration = parameters.get("migrate_to_chat_id")
            if type(migration) is int and migration != 0:
                clean_parameters["migrate_to_chat_id"] = SYNTHETIC_CHAT_ID
            delay = parameters.get("retry_after")
            if type(delay) is int and 0 < delay <= 2**53 - 1:
                clean_parameters["retry_after"] = delay
        if clean_parameters:
            result["parameters"] = clean_parameters
        return result


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


class Runner:
    def __init__(
        self, config: Config, transport: Callable, catalogue: dict, now: Callable[[], str]
    ):
        self.config, self.transport, self.catalogue, self.now = config, transport, catalogue, now
        self.redactor = Redactor(config)
        self.report: dict[str, Any] = {
            "format_version": 1,
            "deployment": {"host": HOST, "api_version": "unknown"},
            "sanitization": dict(SANITIZATION),
            "started_at": now(),
            "message_tests": config.allow_message_tests,
            "status": "failed",
            "checks": [],
            "cleanup": "not_needed",
        }

    @staticmethod
    def fail(record: dict, reason: str) -> None:
        record["status"] = "failed"
        raise CheckFailure(reason)

    def request(self, method: str, parameters: dict, expected_id: str | None = None) -> tuple:
        checks = self.report["checks"]
        if len(checks) >= MAX_REQUESTS or method not in METHODS:
            raise CheckFailure("request_bound_exceeded")
        record: dict[str, Any] = {
            "method": method,
            "time": self.now(),
            "http_status": None,
            "expected_id": expected_id,
            "matched_id": None,
            "status": "failed",
        }
        checks.append(record)
        try:
            reply = self.transport(method, parameters)
        except Exception:
            raise CheckFailure("transport_failed") from None
        if not isinstance(reply, HttpResult) or type(reply.status) is not int:
            raise CheckFailure("invalid_transport_result")
        if not 100 <= reply.status <= 599 or not isinstance(reply.body, dict):
            raise CheckFailure("invalid_transport_result")
        record["http_status"] = reply.status
        envelope = self.redactor.envelope(reply.body)
        if envelope is not None:
            record["response"] = envelope
        classification = classify(reply.body, method=method, catalogue=self.catalogue)
        record["matched_id"] = classification.id
        if expected_id is not None:
            if reply.body.get("ok") is True:
                self.fail(record, "unexpected_success")
            if classification.status != "matched" or classification.id != expected_id:
                self.fail(record, "condition_mismatch")
        elif reply.status != 200 or reply.body.get("ok") is not True:
            self.fail(record, "expected_success")
        record["status"] = "passed"
        return record, reply.body.get("result")

    def message_checks(self) -> None:
        self.report["cleanup"] = "unavailable"
        record, message = self.request(
            "sendMessage",
            {"chat_id": self.config.chat_id, "text": MESSAGE_TEXT, "disable_notification": True},
        )
        if not isinstance(message, dict):
            self.fail(record, "created_message_identity_mismatch")
        sender, chat = message.get("from"), message.get("chat")
        message_id = message.get("message_id")
        if (
            not isinstance(sender, dict)
            or type(sender.get("id")) is not int
            or sender.get("id") != self.config.bot_id
            or sender.get("is_bot") is not True
            or not isinstance(chat, dict)
            or chat.get("id") != self.config.chat_id
            or type(message_id) is not int
            or message_id <= 0
            or message.get("text") != MESSAGE_TEXT
        ):
            self.fail(record, "created_message_identity_mismatch")
        self.redactor.add(message_id)
        target = {"chat_id": self.config.chat_id, "message_id": message_id}
        self.report["cleanup"] = "pending"
        try:
            self.request(
                "editMessageText", {**target, "text": MESSAGE_TEXT}, "message.not_modified"
            )
        finally:
            self.report["cleanup"] = "failed"
            record, deleted = self.request("deleteMessage", target)
            if deleted is not True:
                self.fail(record, "cleanup_not_confirmed")
            self.report["cleanup"] = "succeeded"
        self.request("editMessageText", {**target, "text": MESSAGE_TEXT}, "message.edit_not_found")
        self.request("deleteMessage", target, "message.delete_not_found")

    def run(self) -> dict[str, Any]:
        try:
            record, identity = self.request("getMe", {})
            if not isinstance(identity, dict) or identity.get("is_bot") is not True:
                self.fail(record, "bot_identity_mismatch")
            for value in identity.values():
                self.redactor.add(value)
            if type(identity.get("id")) is not int or identity["id"] != self.config.bot_id:
                self.fail(record, "bot_identity_mismatch")
            self.request(
                "getChatAdministrators", {"chat_id": self.config.migrated_chat_id}, "chat.migrated"
            )
            self.request("getFile", {"file_id": ""}, "file.id_missing")
            self.request("sendMessage", {"chat_id": self.config.chat_id, "text": ""}, "text.empty")
            self.request(
                "sendMessage",
                {
                    "chat_id": self.config.chat_id,
                    "text": MESSAGE_TEXT,
                    "parse_mode": "ErrorgramInvalid",
                },
                "format.parse_mode_unsupported",
            )
            if self.config.allow_message_tests:
                self.message_checks()
            self.report["status"] = "passed"
        except CheckFailure as error:
            self.report["failure"] = str(error)
        except KeyboardInterrupt:
            self.report["failure"] = "interrupted"
        except Exception:
            self.report["failure"] = "internal_error"
        self.report["finished_at"] = self.now()
        return self.report


def run_checks(
    config: Config,
    *,
    transport: Callable | None = None,
    catalogue: dict | None = None,
    now: Callable[[], str] = utc_now,
) -> dict[str, Any]:
    return Runner(
        config,
        transport if transport is not None else TelegramTransport(config),
        catalogue if catalogue is not None else load_catalogue(),
        now,
    ).run()


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, "Invalid command-line options; use --help.\n")


def configuration(args: argparse.Namespace, environment: Mapping[str, str]) -> Config:
    try:
        token = (
            args.token_file.read_text(encoding="utf-8")
            if args.token_file
            else environment.get("TELEGRAM_TEST_BOT_TOKEN", "")
        ).strip()
        chat_id = int(args.chat_id or environment.get("TELEGRAM_TEST_CHAT_ID", ""))
        migrated = int(args.migrated_chat_id or environment.get("TELEGRAM_MIGRATED_CHAT_ID", ""))
        return Config(token, chat_id, migrated, args.allow_message_tests, args.direct)
    except Exception:
        raise CheckFailure("configuration_invalid") from None


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Sanitized JSON report path.")
    parser.add_argument("--token-file", type=Path, help="Read the token from a private local file.")
    parser.add_argument("--chat-id", help="Dedicated test group; overrides the environment.")
    parser.add_argument("--migrated-chat-id", help="Old group ID; overrides the environment.")
    parser.add_argument(
        "--allow-message-tests",
        action="store_true",
        help="Create one silent message and check edits and deletion.",
    )
    parser.add_argument("--direct", action="store_true", help="Bypass environment proxy settings.")
    args = parser.parse_args(argv)
    try:
        report = run_checks(configuration(args, os.environ))
    except Exception:
        report = {
            "format_version": 1,
            "deployment": {"host": HOST, "api_version": "unknown"},
            "sanitization": dict(SANITIZATION),
            "status": "failed",
            "failure": "configuration_or_startup_failed",
            "finished_at": utc_now(),
            "checks": [],
        }
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except Exception:
        print("Could not write the sanitized verification report.", file=sys.stderr)
        return 2
    print(
        "Live verification passed."
        if report["status"] == "passed"
        else "Live verification failed; review the sanitized report."
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
