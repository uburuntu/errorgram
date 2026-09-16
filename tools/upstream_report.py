#!/usr/bin/env python3
"""Render a concise review summary from the committed-source upstream diff."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def render(report: dict) -> str:
    before = report["before"]["revision"]
    after = report["after"]["revision"]
    if not all(re.fullmatch(r"[0-9a-f]{40}", revision) for revision in (before, after)):
        raise ValueError("Report revisions must be full Git commit SHAs.")
    repository = "https://github.com/tdlib/telegram-bot-api"
    summary = report["summary"]
    counts = [
        ("Added candidates", summary["added_candidates"]),
        ("Removed candidates", summary["removed_candidates"]),
        ("Changed normalizers", summary["changed_normalizers"]),
        ("Changed source files", summary["changed_source_files"]),
        ("Changed call locations", summary["occurrence_changes"]),
        ("Added methods", len(report["added_methods"])),
        ("Removed methods", len(report["removed_methods"])),
    ]
    rows = "\n".join(f"| {label} | {count} |" for label, count in counts)
    changed = any(count for _, count in counts)
    status = "Source changes need review." if changed else "No scanned source changes."
    return (
        f"## Telegram Bot API upstream\n\n{status}\n\n"
        f"Baseline: [`{before[:12]}`]({repository}/commit/{before})  \n"
        f"Scanned: [`{after[:12]}`]({repository}/commit/{after})  \n"
        f"[Compare commits]({repository}/compare/{before}...{after})\n\n"
        f"| Change | Count |\n| --- | ---: |\n{rows}\n\n"
        "Download the run's `upstream-report` artifact for the full diff, baseline and snapshot. "
        "The catalogue and baseline are unchanged.\n\n"
        "Counts describe source candidates, not verified public errors or complete Bot API "
        "coverage. TDLib and remote Telegram behavior are outside this scan.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(render(json.loads(args.report.read_text())), encoding="utf-8")


if __name__ == "__main__":
    main()
