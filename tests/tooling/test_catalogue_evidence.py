"""Check reviewed response paths against the pinned source survey, without network access."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = json.loads((ROOT / "catalogue/errors.json").read_text())
UPSTREAM = json.loads((ROOT / "catalogue/upstream.json").read_text())
ENTRIES = {entry["id"]: entry for entry in CATALOGUE["entries"]}

# Each row records a reviewed source literal and its route to the public response.
# The runtime classifier does not normalize descriptions; this checks catalogue evidence.
LITERAL_PATHS = [
    ("message.identifier_missing", "status", "Message identifier is not specified"),
    ("message.identifiers_missing", "status", "Message identifiers are not specified"),
    ("text.empty", "status", "Message text is empty"),
    ("text.too_long", "status", "Text is too long"),
    ("format.parse_mode_unsupported", "status", "Unsupported parse_mode"),
    ("markup.invalid_json", "status", "Can't parse reply keyboard markup JSON object"),
    ("markup.not_object", "status", "Object expected as reply markup"),
    ("markup.too_long", "normalization_output", "reply markup is too long"),
    ("file.id_missing", "direct_response", "Bad Request: file_id not specified"),
    (
        "file.unavailable",
        "status",
        "Bad Request: wrong file_id or the file is temporarily unavailable",
    ),
    ("file.url_invalid", "normalization_output", "Wrong HTTP URL specified"),
    ("file.url_fetch_failed", "normalization_output", "Failed to get HTTP URL content"),
    (
        "file.url_content_type_invalid",
        "normalization_output",
        "Wrong type of the web page content",
    ),
    ("file.url_upload_failed", "normalization_output", "can't upload file by URL"),
    ("user.deactivated", "direct_response", "Forbidden: user is deactivated"),
    ("chat.group_deleted", "direct_response", "Forbidden: the group chat was deleted"),
    (
        "member.is_administrator",
        "normalization_output",
        "user is an administrator of the chat",
    ),
    ("permissions.invalid_json", "status", "Can't parse permissions JSON object"),
    ("permissions.not_object", "status", "Object expected as permissions"),
]
for chat_type in ("group", "supergroup", "channel"):
    LITERAL_PATHS.extend(
        [
            (
                "bot.kicked",
                "direct_response",
                f"Forbidden: bot was kicked from the {chat_type} chat",
            ),
            (
                "bot.not_member",
                "direct_response",
                f"Forbidden: bot is not a member of the {chat_type} chat",
            ),
        ]
    )


def _cited(entry: dict, candidate: dict) -> bool:
    return any(
        proof.get("source") == "server-10.3"
        and proof.get("path") == occurrence["path"]
        and proof["lines"][0] <= occurrence["line"]
        and proof["lines"][1] >= occurrence["end_line"]
        for proof in entry["evidence"]
        for occurrence in candidate["occurrences"]
    )


def _literal_candidates(role: str, literal: str, field: str = "message") -> list[dict]:
    return [
        candidate
        for candidate in UPSTREAM["candidates"]
        if candidate["role"] == role
        and candidate[field] == {"kind": "literal", "value": literal}
    ]


def test_catalogue_evidence_and_survey_use_the_same_server_revision():
    source = CATALOGUE["sources"]["server-10.3"]
    assert source["revision"] == UPSTREAM["source"]["revision"]
    assert source["repository"] == UPSTREAM["source"]["repository"]


@pytest.mark.parametrize(("identity", "role", "literal"), LITERAL_PATHS)
def test_reviewed_literal_paths_have_cited_candidates(identity: str, role: str, literal: str):
    entry = ENTRIES[identity]
    candidates = _literal_candidates(role, literal)
    assert any(_cited(entry, candidate) for candidate in candidates), identity
    # These reviewed literals use the ordinary initial-character rule at Client.cpp:197-202.
    description = literal
    if not literal.startswith(("Bad Request:", "Forbidden:")):
        description = "Bad Request: " + literal[0].lower() + literal[1:]
    code = 403 if description.startswith("Forbidden:") else 400
    assert {"error_code": code, "description_exact": description} in entry["match_any"]


@pytest.mark.parametrize(
    ("identity", "literal"),
    [
        ("file.id_invalid", "invalid file_id"),
        ("message.reply_not_found", "message to be replied not found"),
    ],
)
def test_lookup_fallback_paths_cite_the_literal(identity: str, literal: str):
    candidates = _literal_candidates("normalized_response", literal, "fallback")
    entry = ENTRIES[identity]
    assert any(_cited(entry, candidate) for candidate in candidates)
    assert entry["match_any"] == [
        {"error_code": 400, "description_exact": "Bad Request: " + literal}
    ]


@pytest.mark.parametrize("operation", ["edit", "delete", "forward", "copy", "pin"])
def test_operation_specific_lookup_paths_cite_the_composition(operation: str):
    entry = ENTRIES[f"message.{operation}_not_found"]
    candidates = [
        candidate
        for candidate in UPSTREAM["candidates"]
        if candidate["role"] == "normalized_response"
        and candidate["fallback"]
        and candidate["fallback"].get("literal_fragments") == [" not found"]
        and "message_type" in candidate["fallback"].get("expression", "")
    ]
    assert any(_cited(entry, candidate) for candidate in candidates)
    assert entry["match_any"] == [
        {"error_code": 400, "description_exact": f"Bad Request: message to {operation} not found"}
    ]


@pytest.mark.parametrize(
    ("identity", "literal"),
    [
        ("format.entity_not_object", "expected an Object"),
        ("format.entity_type_unsupported", "Unsupported type specified"),
    ],
)
def test_entity_paths_cite_both_the_leaf_and_wrapper(identity: str, literal: str):
    entry = ENTRIES[identity]
    assert any(_cited(entry, candidate) for candidate in _literal_candidates("status", literal))
    wrappers = [
        candidate
        for candidate in UPSTREAM["candidates"]
        if candidate["role"] == "status"
        and candidate["code"] == {"kind": "literal", "value": 400}
        and candidate["message"]
        and candidate["message"].get("literal_fragments") == ["Can't parse MessageEntity: "]
    ]
    assert any(_cited(entry, candidate) for candidate in wrappers)
    assert entry["match_any"] == [
        {
            "error_code": 400,
            "description_exact": "Bad Request: can't parse MessageEntity: " + literal,
        }
    ]
