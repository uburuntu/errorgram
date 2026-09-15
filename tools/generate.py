"""Generate language bindings and the public catalogue reference."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
    python = render_python(catalogue)
    typescript = render_typescript(catalogue)
    overlap = python.keys() & typescript.keys()
    if overlap:
        raise ValueError(f"Generators share output paths: {sorted(overlap)}")
    return {**python, **typescript, "docs/catalogue.md": render_reference(catalogue)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    rendered = outputs(load_catalogue())
    stale = []
    for relative, content in rendered.items():
        path = ROOT / relative
        if not path.is_file() or path.read_text() != content:
            stale.append(relative)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if args.check and stale:
        print("Generated files are out of date:\n" + "\n".join(stale), file=sys.stderr)
        print("Run make generate.", file=sys.stderr)
        return 1
    print(f"Generated files {'verified' if args.check else 'updated'}: {len(rendered)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
