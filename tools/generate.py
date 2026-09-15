"""Generate language bindings and the public catalogue reference."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.codegen_docs import render as render_docs
from tools.codegen_python import render as render_python
from tools.codegen_typescript import render as render_typescript
from tools.validate import ROOT, load_catalogue


def render_reference(catalogue: dict) -> str:
    lines = [
        "# Catalogue",
        "",
        f"Version **{catalogue['catalogue_version']}** · "
        f"**{len(catalogue['entries'])} conditions**",
        "",
        "Each ID describes an observable failure. Read its evidence before drawing conclusions",
        "about the cause. Examples are source-derived and synthetic; coverage is incomplete.",
        "",
        "| ID | Meaning | Evidence |",
        "| --- | --- | --- |",
    ]
    for entry in sorted(catalogue["entries"], key=lambda item: item["id"]):
        evidence = entry["evidence"][0]
        source = catalogue["sources"][evidence["source"]]
        if "path" in evidence:
            url = (
                f"{source['repository']}/blob/{source['revision']}/{evidence['path']}"
                f"#L{evidence['lines'][0]}"
            )
        else:
            url = source["url"]
        summary = entry["summary"].replace("|", "\\|").replace("\n", " ")
        label = entry["evidence_level"].replace("_", " ")
        lines.append(f"| `{entry['id']}` | {summary} | [{label}]({url}) |")
    lines.extend([
        "",
        "[Full records](../catalogue/errors.json) include matching rules, context, "
        "possible causes,",
        "guidance, and source references. [Matching rules](design.md) "
        "explain how classification works.",
        "",
        "Generated from `catalogue/errors.json`. Run `make generate` after editing the catalogue.",
        "",
    ])
    return "\n".join(lines)


def outputs(catalogue: dict) -> dict[str, str]:
    result = {"docs/catalogue.md": render_reference(catalogue)}
    for render in (render_python, render_typescript, render_docs):
        generated = render(catalogue)
        overlap = result.keys() & generated.keys()
        if overlap:
            raise ValueError(f"Generators share output paths: {sorted(overlap)}")
        result.update(generated)
    return result


def obsolete_outputs(rendered: dict[str, str]) -> list[str]:
    """Remove retired pages only from the documentation generator's owned paths."""
    manifest = ROOT / "site/generated-manifest.json"
    if not manifest.exists():
        return []
    previous = json.loads(manifest.read_text())
    if previous.get("generator") != "tools/codegen_docs.py":
        raise ValueError("Unrecognized documentation manifest generator.")
    paths = previous.get("paths")
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        raise ValueError("Documentation manifest paths must be a list of strings.")
    allowed = re.compile(
        r"(?:site/src/content/docs/errors/[a-z][a-z0-9_.]*\.md"
        r"|site/public/errors/[a-z][a-z0-9_.]*\.(?:md|json)"
        r"|site/src/content/docs/catalogue\.md"
        r"|site/public/(?:index|getting-started|python|javascript|matching|"
        r"contributing|updating|agents|catalogue)\.md"
        r"|site/public/(?:catalogue|schema)\.json"
        r"|site/public/llms(?:-full)?\.txt)"
    )
    for path in paths:
        if not allowed.fullmatch(path):
            raise ValueError(f"Documentation manifest contains an unowned path: {path}")
    return sorted(set(paths) - rendered.keys())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    rendered = outputs(load_catalogue())
    obsolete = [path for path in obsolete_outputs(rendered) if (ROOT / path).exists()]
    stale = []
    for relative, content in rendered.items():
        path = ROOT / relative
        if not path.is_file() or path.read_text() != content:
            stale.append(relative)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if args.check and (stale or obsolete):
        print("Generated files are out of date:\n" + "\n".join(stale), file=sys.stderr)
        if obsolete:
            print("Retired pages must be removed:\n" + "\n".join(obsolete), file=sys.stderr)
        print("Run make generate.", file=sys.stderr)
        return 1
    if not args.check:
        for relative in obsolete:
            (ROOT / relative).unlink()
    print(f"Generated files {'verified' if args.check else 'updated'}: {len(rendered)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
