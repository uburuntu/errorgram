"""Render the public error reference and Markdown exports from reviewed data."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

from tools.codegen_python import _aiogram_base, _class_name

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://errorgram.rmbk.me"
GUIDES = (
    "index",
    "getting-started",
    "playground",
    "python",
    "javascript",
    "matching",
    "contributing",
    "updating",
    "agents",
)
MANIFEST = "site/generated-manifest.json"
_ID = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+")
_PREDICATES = {
    "positive_integer": "a positive safe integer",
    "nonzero_integer": "a nonzero safe integer",
}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _python_literal(value: Any, depth: int = 0) -> str:
    """Format a JSON value as readable, executable Python without changing strings."""
    indent = "    " * depth
    if isinstance(value, dict) and value:
        rows = [
            f"{indent}    {json.dumps(key, ensure_ascii=False)}: "
            f"{_python_literal(item, depth + 1)},"
            for key, item in value.items()
        ]
        return "{\n" + "\n".join(rows) + f"\n{indent}}}"
    if isinstance(value, list) and value:
        rows = [f"{indent}    {_python_literal(item, depth + 1)}," for item in value]
        return "[\n" + "\n".join(rows) + f"\n{indent}]"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    return repr(value)


def _prose(value: Any) -> str:
    """Treat catalogue prose as literal text, never as Markdown or HTML."""
    text = " ".join(str(value).split())
    text = html.escape(text, quote=False)
    text = re.sub(r"([\\`*_\[\]#!|])", r"\\\1", text)
    text = re.sub(r"^(\d+)\.", r"\1\\.", text).removeprefix("\ufeff")
    return re.sub(r"^([-+])(?=\s)", r"\\\1", text)


def _code(value: Any) -> str:
    text = " ".join(str(value).split())
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    delimiter = "`" * (longest + 1)
    return f"{delimiter} {text} {delimiter}" if longest else f"`{text}`"


def _fence(value: str, language: str = "") -> str:
    longest = max((len(run) for run in re.findall(r"`+", value)), default=0)
    delimiter = "`" * max(3, longest + 1)
    return f"{delimiter}{language}\n{value.rstrip(chr(10))}\n{delimiter}"


def _url(value: str) -> str:
    if urlsplit(value).scheme not in {"https", "http"}:
        raise ValueError(f"Documentation links require an HTTP(S) URL: {value!r}")
    return quote(value, safe=":/?#[]@!$&'*+,;=%-")


def _link(label: str, url: str) -> str:
    return f"[{_prose(label)}]({_url(url)})"


def _frontmatter(title: str, description: str, slug: str, label: str) -> str:
    # JSON string literals are valid YAML scalars and cannot inject new fields.
    def scalar(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    return (
        "---\n"
        f"title: {scalar(title)}\n"
        f"description: {scalar(description)}\n"
        f"slug: {scalar(slug)}\n"
        'editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"\n'
        "sidebar:\n"
        f"  label: {scalar(label)}\n"
        "---\n\n"
    )


def _rule(rule: dict[str, Any], number: int, multiple: bool) -> list[str]:
    lines = [f"### Rule {number}", ""] if multiple else []
    lines += [f"- JSON {_code('error_code')}: **{rule['error_code']}**."]
    if "method" in rule:
        lines.append(f"- Required method: {_code(rule['method'])}, ignoring ASCII case.")
    for name, predicate in sorted(rule.get("required_parameters", {}).items()):
        lines.append(f"- {_code('parameters.' + name)}: {_PREDICATES[predicate]}.")
    lines.append("")
    if "description_exact" in rule:
        lines += ["Exact description:", "", _fence(rule["description_exact"], "text"), ""]
    elif "description_template" in rule:
        lines += [
            "Description template; literal text must match exactly:",
            "",
            _fence(rule["description_template"], "text"),
            "",
        ]
        for name, predicate in sorted(rule["capture_types"].items()):
            lines.append(
                f"- {_code(name)}: {_PREDICATES[predicate]}, captured from the description."
            )
        lines.append("")
    else:
        lines += ["The structured parameter decides the match; the description may vary.", ""]
    return lines


def _example(entry: dict[str, Any], catalogue: dict[str, Any]) -> list[str]:
    example = entry["example"]
    method = example.get("method")
    response = example["response"]
    python_method = f", method={method!r}" if method is not None else ""
    js_method = f", {{ method: {json.dumps(method)} }}" if method is not None else ""
    python = (
        "from errorgram import classify\n\n"
        f"response = {_python_literal(response)}\n"
        f"result = classify(response{python_method})\n\n"
        f"assert result.id == {entry['id']!r}\n"
        "print(result.entry[\"summary\"])\n"
    )
    typescript = (
        'import { classify } from "errorgram";\n\n'
        f"const response = {_json(response).rstrip()};\n"
        f"const result = classify(response{js_method});\n\n"
        f"if (result.status === \"matched\" && result.id === {json.dumps(entry['id'])}) {{\n"
        "  console.log(result.entry.summary);\n"
        "}\n"
    )
    lines = [
        "## Example",
        "",
        _prose(catalogue["coverage"]["examples"]),
        "",
    ]
    if method is not None:
        lines += [f"API method: {_code(method)}.", ""]
    lines += [
        _fence(_json(response), "json"),
        "",
        "### Python",
        "",
        _fence(python, "python"),
        "",
        "### JavaScript and TypeScript",
        "",
        _fence(typescript, "ts"),
        "",
    ]
    return lines


def _facts(entry: dict[str, Any]) -> list[str]:
    fields = {}
    for rule in entry["match_any"]:
        for name, predicate in rule.get("required_parameters", {}).items():
            fields[(name, "parameters." + name)] = predicate
        for name, predicate in rule.get("capture_types", {}).items():
            fields[(name, "description")] = predicate
    lines = ["## Facts", ""]
    if fields:
        lines += ["Values extracted into `result.facts`:", ""]
        for (name, origin), predicate in sorted(fields.items()):
            lines.append(f"- {_code(name)}: {_PREDICATES[predicate]}, from {_code(origin)}.")
        lines.append("")
    else:
        lines += ["This condition adds no extracted facts; `result.facts` is empty.", ""]
    if entry.get("facts"):
        lines += [
            "Version-specific metadata is available in `result.entry` under `facts`.",
            "These values are catalogue metadata, not measurements from the response.",
            "",
            _fence(_json(entry["facts"]), "json"),
            "",
        ]
    return lines


def _evidence(entry: dict[str, Any], catalogue: dict[str, Any]) -> list[str]:
    lines = ["## Evidence", ""]
    for evidence in entry["evidence"]:
        source = catalogue["sources"][evidence["source"]]
        if "path" in evidence:
            start, end = evidence["lines"]
            fragment = f"#L{start}" + (f"-L{end}" if end != start else "")
            url = (
                f"{source['repository'].rstrip('/')}/blob/{source['revision']}/"
                f"{quote(evidence['path'], safe='/')}{fragment}"
            )
            location = f"{evidence['path']}:{start}" + (f"–{end}" if start != end else "")
            label = f"Bot API {source['version_label']} · {location}"
            detail = f"Revision {_code(source['revision'])}."
        else:
            url = source["url"]
            label = (
                "Official documentation"
                if source["kind"] == "official_documentation"
                else "Recorded observation"
            )
            detail = f"Accessed {_prose(source['accessed_on'])}."
        lines += [
            f"- {_link(label, url)}. {_prose(evidence['note'])} {detail}",
        ]
    lines += [
        "",
        "Source references identify the reviewed revision, not the first release",
        "that introduced this response.",
        "",
    ]
    return lines


def _entry_body(entry: dict[str, Any], catalogue: dict[str, Any]) -> str:
    condition_id = entry["id"]
    class_name = _class_name(condition_id)
    level = entry["evidence_level"].replace("_", " ")
    lines = [
        f"**Stable ID:** {_code(condition_id)} · **Evidence:** {_prose(level)}",
        "",
        _prose(entry["summary"]),
        "",
        _prose(entry["diagnostic_limits"]),
        "",
        "## When it matches",
        "",
        "Every field in a rule must match. Alternative rules are joined with OR.",
        "Codes below are JSON response fields, not inferred HTTP statuses.",
        "",
    ]
    rules = entry["match_any"]
    for number, rule in enumerate(rules, 1):
        lines.extend(_rule(rule, number, len(rules) > 1))
    lines += [
        f"See {_link('matching rules', SITE + '/matching/')} for parameter precedence",
        "and unknown or ambiguous results.",
        "",
    ]
    scope = entry["scope"]
    if scope["method_examples"]:
        methods = ", ".join(_code(method) for method in scope["method_examples"])
        qualifier = "Complete list" if scope["exhaustive"] else "Illustrative methods"
        lines += [f"**{qualifier}:** {methods}.", ""]
    if scope.get("deployment"):
        lines += [_prose(scope["deployment"]), ""]
    lines += ["## Possible causes", ""]
    lines += [f"- {_prose(cause)}" for cause in entry["possible_causes"]]
    guidance = entry["guidance"]
    lines += [
        "",
        "## Before deciding what to do",
        "",
        f"**Application decision:** {_prose(guidance['action'].replace('_', ' '))}.",
        f"**Repeat request:** {_prose(guidance['repeat_request'].replace('_', ' '))}.",
        "",
    ]
    lines += [f"- {_prose(condition)}" for condition in guidance["preconditions"]]
    if guidance.get("delay_parameter"):
        lines += ["", f"Delay parameter: {_code(guidance['delay_parameter'])}."]
    lines += [
        "",
        "These are application choices. Errorgram does not retry, suppress the error,",
        "or change bot state.",
        "",
    ]
    lines.extend(_facts(entry))
    lines.extend(_example(entry, catalogue))
    lines += [
        "## Framework names",
        "",
        "| Integration | Type or ID |",
        "| --- | --- |",
        f"| Python | {_code('errorgram.' + class_name)} |",
        f"| aiogram | {_code('errorgram.aiogram.' + class_name)} "
        f"extends {_code(_aiogram_base(entry))} |",
        f"| grammY | `EnrichedGrammyError` with `classification.id` "
        f"equal to {_code(condition_id)} |",
        "",
        "Enrichment is explicit and keeps framework catch compatibility.",
        f"Follow the {_link('Python and aiogram guide', SITE + '/python/')} or",
        f"{_link('JavaScript, TypeScript, and grammY guide', SITE + '/javascript/')}.",
        "",
    ]
    lines.extend(_evidence(entry, catalogue))
    lines += [
        "## Data and versions",
        "",
        f"Catalogue {_code(catalogue['catalogue_version'])} · "
        f"schema {_code(catalogue['schema_version'])} · "
        f"reviewed {_prose(catalogue['reviewed_on'])}.",
        "",
        " · ".join([
            _link("Markdown", f"{SITE}/errors/{condition_id}.md"),
            _link("Condition JSON", f"{SITE}/errors/{condition_id}.json"),
            _link("Full catalogue and sources", f"{SITE}/catalogue.json"),
            _link("JSON Schema", f"{SITE}/schema.json"),
        ]),
        "",
    ]
    return "\n".join(lines)


def _guide(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError(f"Missing authored documentation: {path.relative_to(ROOT)}")
    text = path.read_text()
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    if match is None:
        raise ValueError(f"Documentation needs YAML frontmatter: {path.relative_to(ROOT)}")
    metadata, body = match.groups()
    title_match = re.search(r"^title:[ \t]+(.+)$", metadata, re.MULTILINE)
    if title_match is None:
        raise ValueError(f"Documentation needs a single-line title: {path.relative_to(ROOT)}")
    title = title_match[1].strip()
    if title.startswith('"'):
        title = json.loads(title)
    elif title.startswith("'") and title.endswith("'"):
        title = title[1:-1].replace("''", "'")
    if not isinstance(title, str) or not title or title in {"|", ">", "|-", ">-"}:
        raise ValueError(f"Documentation needs a single-line title: {path.relative_to(ROOT)}")
    # Authored guide links are absolute; root-relative links are also safe to export.
    body = re.sub(r"(?<=\]\()/(?!/)", SITE + "/", body.strip())
    return title, body + "\n"


def _catalogue_page(catalogue: dict[str, Any]) -> str:
    lines = [
        f"**{len(catalogue['entries'])} conditions** · "
        f"catalogue {_code(catalogue['catalogue_version'])} · "
        f"reviewed {_prose(catalogue['reviewed_on'])}",
        "",
        "Start with the response text, a stable ID, or a framework exception name.",
        "Each page explains the match, its limits, and the evidence behind it.",
        "",
        _prose(catalogue["coverage"]["scope"]),
        _prose(catalogue["coverage"]["examples"]),
        "",
    ]
    if not catalogue["coverage"]["complete"]:
        lines += ["Coverage is incomplete. Unrecognized responses remain unknown.", ""]
    lines += ["| Condition | Meaning |", "| --- | --- |"]
    for entry in sorted(catalogue["entries"], key=lambda item: item["id"]):
        lines.append(
            f"| {_link(entry['id'], SITE + '/errors/' + entry['id'] + '/')} "
            f"| {_prose(entry['summary'])} |"
        )
    lines += [
        "",
        f"Download the {_link('catalogue JSON', SITE + '/catalogue.json')} or",
        f"{_link('JSON Schema', SITE + '/schema.json')}. For programmatic retrieval,",
        f"see {_link('AI agents', SITE + '/agents/')}.",
        "",
    ]
    return "\n".join(lines)


def render(catalogue: dict[str, Any]) -> dict[str, str]:
    """Return static reference pages and agent exports; perform no writes."""
    entries = sorted(catalogue["entries"], key=lambda entry: entry["id"])
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)) or any(_ID.fullmatch(value) is None for value in ids):
        raise ValueError("Documentation requires unique, safe condition IDs.")
    files = {
        "site/public/catalogue.json": _json(catalogue),
        "site/public/schema.json": _json(json.loads((ROOT / "catalogue/schema.json").read_text())),
    }
    index_body = _catalogue_page(catalogue)
    index_plain = "# Error catalogue\n\n" + index_body
    files["site/src/content/docs/catalogue.md"] = _frontmatter(
        "Error catalogue",
        "Telegram Bot API error conditions, stable IDs, matching rules, and source evidence.",
        "catalogue",
        "Error catalogue",
    ) + index_body.replace(SITE + "/", "/")
    files["site/public/catalogue.md"] = index_plain
    llms = [
        "# Errorgram",
        "",
        "> An open inventory of Telegram Bot API errors, with stable IDs and bindings",
        "> for Python, JavaScript, TypeScript, aiogram, and grammY.",
        "",
        "Use the JSON catalogue for matching rules and Markdown for explanations.",
        "IDs describe observable conditions; they do not prove one underlying cause.",
        "Transport failures and framework validation are outside this inventory.",
        "Enrichment is opt-in. Errorgram does not retry, suppress errors, or change bot state.",
        "",
        _prose(catalogue["coverage"]["scope"]),
        _prose(catalogue["coverage"]["examples"]),
        "",
        f"Catalogue {catalogue['catalogue_version']} · schema {catalogue['schema_version']} · "
        f"reviewed {catalogue['reviewed_on']}.",
        "",
        "## Documentation",
        "",
    ]
    full = [
        "# Errorgram documentation",
        "",
        f"Canonical site: {SITE}/",
        "",
        f"Catalogue {catalogue['catalogue_version']} · schema {catalogue['schema_version']} · "
        f"reviewed {catalogue['reviewed_on']}.",
        "",
    ]
    for slug in GUIDES:
        title, body = _guide(ROOT / f"site/src/content/docs/{slug}.md")
        canonical = SITE + ("/" if slug == "index" else f"/{slug}/")
        plain = f"# {_prose(title)}\n\nCanonical page: {canonical}\n\n{body}"
        files[f"site/public/{slug}.md"] = plain
        llms.append(f"- {_link(title, SITE + '/' + slug + '.md')}")
        full += [plain.rstrip(), "", "---", ""]
    llms += [
        f"- {_link('Error catalogue', SITE + '/catalogue.md')}",
        "",
        "## Structured data",
        "",
        f"- {_link('Catalogue JSON', SITE + '/catalogue.json')}: complete records and sources.",
        f"- {_link('JSON Schema', SITE + '/schema.json')}: validates catalogue structure.",
        f"- {_link('Full documentation', SITE + '/llms-full.txt')}: guides and all conditions.",
        "",
        "## Error conditions",
        "",
    ]
    full += [index_plain.rstrip(), "", "---", ""]
    for entry in entries:
        condition_id = entry["id"]
        label = condition_id.replace(".", " ").replace("_", " ").capitalize()
        title = f"{label} · {condition_id}"
        body = _entry_body(entry, catalogue)
        files[f"site/src/content/docs/errors/{condition_id}.md"] = _frontmatter(
            title, entry["summary"], f"errors/{condition_id}", condition_id
        ) + body.replace(SITE + "/", "/")
        canonical = f"{SITE}/errors/{condition_id}/"
        plain = f"# {_prose(title)}\n\nCanonical page: {canonical}\n\n{body}"
        files[f"site/public/errors/{condition_id}.md"] = plain
        files[f"site/public/errors/{condition_id}.json"] = _json(entry)
        llms += [
            f"- {_link(condition_id, canonical)}: {_prose(entry['summary'])} "
            f"({_link('Markdown', SITE + '/errors/' + condition_id + '.md')}; "
            f"{_link('JSON', SITE + '/errors/' + condition_id + '.json')})",
        ]
        full += [plain.rstrip(), "", "---", ""]
    files["site/public/llms.txt"] = "\n".join(llms) + "\n"
    files["site/public/llms-full.txt"] = "\n".join(full).rstrip() + "\n"
    files[MANIFEST] = _json({"generator": "tools/codegen_docs.py", "paths": sorted(files)})
    return files
