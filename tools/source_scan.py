"""Extract review candidates from C++; this is not a C++ compiler."""

from __future__ import annotations

import hashlib
import json
import re
from bisect import bisect_right
from dataclasses import dataclass
from typing import Any

TOKEN = re.compile(
    r"(?P<comment>//[^\n]*|/\*.*?\*/)"
    r'|(?P<raw>(?:u8|[LuU])?R"(?P<delimiter>[^ ()\\\t\r\n]{0,16})\(.*?\)(?P=delimiter)")'
    r'|(?P<string>(?:u8|[LuU])?"(?:\\.|[^"\\])*")'
    r"|(?P<char>(?:u8|[LuU])?'(?:\\.|[^'\\])*')"
    r"|(?P<word>[A-Za-z_]\w*)"
    r"|(?P<number>\d+)"
    r"|(?P<symbol>::|->|<<|>>|==|!=|&&|\|\||[^\s])",
    re.DOTALL,
)

CALLS = {
    ("fail_query",): "direct_response",
    ("fail_query_with_error",): "normalized_response",
    ("fail_query_conflict",): "conflict_response",
    ("send_http_error",): "http_response",
    ("set_retry_after_error",): "retry_response",
    ("td", "::", "Status", "::", "Error"): "status",
    ("make_object", "<", "td_api", "::", "error", ">"): "tdlib_error_object",
    ("JsonQueryError",): "response_serialization",
}


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    start: int
    end: int


def tokenize(source: str) -> list[Token]:
    return [
        Token(match.lastgroup or "symbol", match.group(), match.start(), match.end())
        for match in TOKEN.finditer(source)
        if match.lastgroup != "comment"
    ]


def fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def expression(tokens: list[Token]) -> str:
    """Token spacing preserves meaning while ignoring layout and comments."""
    return " ".join(token.text for token in tokens)


def arguments(tokens: list[Token], opening: int) -> tuple[list[list[Token]], int]:
    """Split arguments with balanced (), [] and {}; templates are not parsed."""
    stack = [")"]
    pairs = {"(": ")", "[": "]", "{": "}"}
    args: list[list[Token]] = []
    start = opening + 1
    for i in range(start, len(tokens)):
        token = tokens[i]
        if token.kind != "symbol":
            continue
        value = token.text
        if value in pairs:
            stack.append(pairs[value])
        elif value == stack[-1]:
            stack.pop()
            if not stack:
                if i != start or args:
                    args.append(tokens[start:i])
                return args, i
        elif value == "," and len(stack) == 1:
            args.append(tokens[start:i])
            start = i + 1
    raise ValueError(f"Unbalanced call at character {tokens[opening].start}")


def _decode_literal(token: Token) -> str | None:
    if token.kind == "raw":
        opening = token.text.index("(")
        delimiter = token.text[token.text.index('R"') + 2 : opening]
        return token.text[opening + 1 : -(len(delimiter) + 2)]
    if token.kind != "string":
        return None
    body = re.sub(r"^(?:u8|[LuU])", "", token.text)[1:-1]
    result: list[str] = []
    index = 0
    escapes = {
        "a": "\a",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "v": "\v",
        "\\": "\\",
        '"': '"',
        "'": "'",
        "?": "?",
    }
    while index < len(body):
        char = body[index]
        if char != "\\":
            result.append(char)
            index += 1
            continue
        index += 1
        if index == len(body):
            return None
        escaped = body[index]
        if escaped in escapes:
            result.append(escapes[escaped])
            index += 1
        elif escaped == "\n":
            index += 1
        elif escaped == "\r" and body[index : index + 2] == "\r\n":
            index += 2
        elif escaped in "01234567":
            match = re.match(r"[0-7]{1,3}", body[index:])
            assert match
            number = int(match.group(), 8)
            if number > 127:
                return None
            result.append(chr(number))
            index += len(match.group())
        elif escaped in "xuU":
            pattern = {"x": r"[0-9a-fA-F]+", "u": r"[0-9a-fA-F]{4}", "U": r"[0-9a-fA-F]{8}"}[
                escaped
            ]
            match = re.match(pattern, body[index + 1 :])
            if match is None:
                return None
            number = int(match.group(), 16)
            # Execution encodings and implementation-defined byte escapes need review.
            if number > 0x10FFFF or 0xD800 <= number <= 0xDFFF or (escaped == "x" and number > 127):
                return None
            result.append(chr(number))
            index += len(match.group()) + 1
        else:
            return None
    return "".join(result)


def value(tokens: list[Token]) -> dict[str, Any] | None:
    if not tokens:
        return None
    parts = [_decode_literal(token) for token in tokens]
    if all(part is not None for part in parts):
        return {"kind": "literal", "value": "".join(part for part in parts if part is not None)}
    return {
        "kind": "dynamic",
        "expression": expression(tokens),
        "literal_fragments": [part for part in parts if part is not None],
    }


def code_value(tokens: list[Token]) -> dict[str, Any] | None:
    if len(tokens) == 1 and re.fullmatch(r"0|[1-9][0-9]*", tokens[0].text):
        return {"kind": "literal", "value": int(tokens[0].text)}
    return value(tokens)


def _is_definition(tokens: list[Token], args: list[list[Token]], closing: int) -> bool:
    after = closing + 1
    while after < len(tokens) and tokens[after].text in ("const", "noexcept", "override", "final"):
        after += 1
    if after < len(tokens) and tokens[after].text in ("{", ":"):
        return True
    if not args or not args[0]:
        return False
    first = args[0]
    if first[0].text == "const" or (
        len(first) == 1
        and first[0].text in ("int", "int32", "int64", "bool", "void", "PromisedQueryPtr")
    ):
        return True
    # A qualified type followed by a parameter name, optionally with & or *.
    return bool(re.fullmatch(r"(?:\w+ :: )*\w+ (?:(?:&&|[&*]) )*\w+(?: = .*)?", expression(first)))


def _body_end(tokens: list[Token], opening: int) -> int:
    depth = 0
    for index in range(opening, len(tokens)):
        token = tokens[index]
        if token.kind != "symbol":
            continue
        if token.text == "{":
            depth += 1
        elif token.text == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unbalanced function at character {tokens[opening].start}")


def _in_log_statement(tokens: list[Token], position: int) -> bool:
    for index in range(position - 1, -1, -1):
        token = tokens[index]
        if token.kind == "symbol" and token.text in (";", "{", "}"):
            return False
        if token.kind == "word" and token.text in ("LOG", "LOG_IF", "VLOG", "VLOG_IF"):
            return True
    return False


def scan_source(source: str, path: str) -> dict[str, Any]:
    tokens = tokenize(source)
    newlines = [match.start() for match in re.finditer("\n", source)]
    sites: list[dict[str, Any]] = []
    normalizers: list[dict[str, Any]] = []
    normalizer_ranges: list[tuple[int, int]] = []
    methods: set[str] = set()

    def occurrence(start: int, end: int) -> dict[str, Any]:
        return {
            "path": path,
            "line": bisect_right(newlines, tokens[start].start) + 1,
            "end_line": bisect_right(newlines, tokens[end].end - 1) + 1,
        }

    def site(role: str, call: str, start: int, end: int, **fields: Any) -> None:
        item: dict[str, Any] = {
            "role": role,
            "call": call,
            "code": None,
            "message": None,
            "fallback": None,
            "forwarded_error": None,
            "retry_after": None,
        }
        item.update(fields)
        item["occurrence"] = occurrence(start, end)
        sites.append(item)

    for i, token in enumerate(tokens):
        if token.kind != "word":
            continue
        if tuple(t.text for t in tokens[i : i + 4]) == ("methods_", ".", "emplace", "("):
            args, _ = arguments(tokens, i + 3)
            method = value(args[0]) if args else None
            if method and method["kind"] == "literal":
                methods.add(method["value"])
        for signature, role in CALLS.items():
            if tuple(t.text for t in tokens[i : i + len(signature)]) != signature:
                continue
            opening = i + len(signature)
            if opening >= len(tokens) or tokens[opening].text != "(":
                continue
            if _in_log_statement(tokens, i):
                continue
            args, closing = arguments(tokens, opening)
            if _is_definition(tokens, args, closing):
                if (
                    role == "normalized_response"
                    and closing + 1 < len(tokens)
                    and tokens[closing + 1].text == "{"
                ):
                    end = _body_end(tokens, closing + 1)
                    name = (
                        "fail_query_with_error(" + ", ".join(expression(arg) for arg in args) + ")"
                    )
                    normalizers.append(
                        {
                            "name": name,
                            "fingerprint": fingerprint(expression(tokens[closing + 1 : end + 1])),
                            "occurrence": occurrence(i, end),
                        }
                    )
                    if any(t.text == "error_message" for arg in args for t in arg):
                        normalizer_ranges.append((closing + 1, end))
                continue

            fields: dict[str, Any] = {}
            if role == "retry_response":
                fields = {
                    "code": {"kind": "literal", "value": 429},
                    "retry_after": code_value(args[0]) if args else None,
                }
            elif role == "conflict_response":
                fields = {
                    "code": {"kind": "literal", "value": 409},
                    "message": value(args[0]) if args else None,
                }
            elif role == "status" and len(args) == 1:
                fields = {"message": value(args[0])}
            elif role == "normalized_response" and len(args) >= 2:
                second = expression(args[1])
                scalar = len(args) >= 4 or (
                    len(args) == 3
                    and (
                        bool(re.fullmatch(r"\d+", second))
                        or bool(re.search(r"\b\w*code_?(?: \( \))?$", second))
                    )
                )
                if scalar:
                    fields = {
                        "code": code_value(args[1]),
                        "message": value(args[2]),
                        "fallback": value(args[3]) if len(args) >= 4 else None,
                    }
                else:
                    fields = {
                        "forwarded_error": value(args[1]),
                        "fallback": value(args[2]) if len(args) >= 3 else None,
                    }
            elif len(args) >= 2:
                fields = {"code": code_value(args[0]), "message": value(args[1])}
            site(role, "".join(signature), i, closing, **fields)

    for start, end in normalizer_ranges:
        for i in range(start, end):
            if tokens[i].text != "error_message" or i + 1 >= end:
                continue
            operator = tokens[i + 1].text
            if operator in ("==", "!="):
                finish = i + 2
                while finish < end and tokens[finish].kind in ("string", "raw"):
                    finish += 1
                if finish > i + 2:
                    site(
                        "normalization_input",
                        "error_message " + operator,
                        i,
                        finish - 1,
                        message=value(tokens[i + 2 : finish]),
                    )
            elif operator == "=":
                finish = i + 2
                while finish < end and tokens[finish].text != ";":
                    finish += 1
                if finish < end:
                    site(
                        "normalization_output",
                        "error_message =",
                        i,
                        finish,
                        message=value(tokens[i + 2 : finish]),
                    )
            elif i >= start + 2 and tokens[i - 1].text in ("==", "!="):
                begin = i - 2
                while begin >= start and tokens[begin].kind in ("string", "raw"):
                    begin -= 1
                if begin < i - 2:
                    site(
                        "normalization_input",
                        "error_message " + tokens[i - 1].text,
                        begin + 1,
                        i,
                        message=value(tokens[begin + 1 : i - 1]),
                    )

    return {"sites": sites, "normalizers": normalizers, "registered_methods": sorted(methods)}


def group_candidates(sites: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for site in sites:
        identity = {key: item for key, item in site.items() if key != "occurrence"}
        key = fingerprint(identity)
        if key not in groups:
            groups[key] = {"id": key, **identity, "occurrences": []}
        groups[key]["occurrences"].append(site["occurrence"])
    for group in groups.values():
        group["occurrences"].sort(key=lambda item: (item["path"], item["line"], item["end_line"]))
    return sorted(groups.values(), key=lambda item: item["id"])
