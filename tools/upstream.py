#!/usr/bin/env python3
"""Survey a pinned Telegram Bot API revision and review source changes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .source_scan import group_candidates, scan_source
else:
    from source_scan import group_candidates, scan_source


REPOSITORY = "https://github.com/tdlib/telegram-bot-api"
FORMAT_VERSION = 1
SOURCE_EXTENSIONS = {".cpp", ".h", ".hpp", ".cc"}


class SurveyError(ValueError):
    """An input cannot be surveyed reliably."""


def git(root: Path, *arguments: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise SurveyError("Git is required to read upstream revisions.") from error
    if result.returncode:
        detail = result.stderr.decode(errors="replace").strip()
        raise SurveyError(detail or "Git could not read this revision.")
    return result.stdout


def survey(root: Path, ref: str = "HEAD") -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise SurveyError(f"Source directory does not exist: {root}")
    if not ref or ref.startswith("-"):
        raise SurveyError("Use a commit, tag or branch name for --ref.")
    top = Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if top != root:
        raise SurveyError(f"--source must name the repository root: {top}")
    revision = (
        git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()
    )
    tree: dict[str, tuple[str, str]] = {}
    for record in git(root, "ls-tree", "-r", "-z", revision).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        _, kind, object_id = metadata.decode().split()
        tree[raw_path.decode()] = kind, object_id
    paths = sorted(
        path
        for path, (kind, _) in tree.items()
        if kind == "blob"
        and path.startswith("telegram-bot-api/")
        and Path(path).suffix in SOURCE_EXTENSIONS
    )
    if not paths or "CMakeLists.txt" not in tree:
        raise SurveyError("This revision has no Telegram Bot API source tree and CMakeLists.txt.")

    cmake = git(root, "show", f"{revision}:CMakeLists.txt")
    version_match = re.search(rb"project\(\s*TelegramBotApi\s+VERSION\s+([\d.]+)", cmake)
    if version_match is None:
        raise SurveyError("The TelegramBotApi version is missing from CMakeLists.txt.")
    sites: list[dict[str, Any]] = []
    files: list[dict[str, str]] = []
    normalizers: list[dict[str, Any]] = []
    methods: set[str] = set()
    for path in paths:
        contents = git(root, "show", f"{revision}:{path}")
        try:
            extracted = scan_source(contents.decode("utf-8"), path)
        except (ValueError, UnicodeDecodeError) as error:
            raise SurveyError(f"Cannot scan {path}: {error}") from error
        sites.extend(extracted["sites"])
        normalizers.extend(extracted["normalizers"])
        methods.update(extracted["registered_methods"])
        files.append({"path": path, "sha256": hashlib.sha256(contents).hexdigest()})
    files.append({"path": "CMakeLists.txt", "sha256": hashlib.sha256(cmake).hexdigest()})
    files.sort(key=lambda item: item["path"])
    candidates = group_candidates(sites)
    tdlib = tree.get("td")
    dirty = bool(
        git(
            root,
            "status",
            "--porcelain",
            "--untracked-files=no",
            "--ignore-submodules=all",
            "--",
            "telegram-bot-api",
            "CMakeLists.txt",
        )
    )
    return {
        "format_version": FORMAT_VERSION,
        "source": {
            "repository": REPOSITORY,
            "revision": revision,
            "version": version_match.group(1).decode(),
            "content": "committed_git_blobs",
            "local_worktree_dirty": dirty,
            "tdlib_revision": tdlib[1] if tdlib and tdlib[0] == "commit" else None,
        },
        "scope": "source_candidates",
        "limitations": [
            "Candidates are source evidence, not verified public errors or a coverage estimate.",
            "Server C++ includes internal, command-line and webhook diagnostics.",
            "TDLib, remote Telegram behavior and dependency-generated responses are not scanned.",
            "The lexer does not resolve macros, templates, types, reachability or expressions.",
            "Normalizer inputs and assignments are source strings; public descriptions may differ.",
            "Working-tree changes are ignored; all scanned content comes from the recorded commit.",
        ],
        "summary": {
            "source_files": len(paths),
            "candidate_sites": len(sites),
            "candidate_groups": len(candidates),
            "candidates_by_role": dict(
                sorted(Counter(item["role"] for item in candidates).items())
            ),
            "registered_methods": len(methods),
            "normalizer_functions": len(normalizers),
        },
        "files": files,
        "registered_methods": sorted(methods),
        "normalizers": sorted(
            normalizers, key=lambda item: (item["name"], item["occurrence"]["path"])
        ),
        "candidates": candidates,
    }


def read_snapshot(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        snapshot = json.load(stream)
    if not isinstance(snapshot, dict) or snapshot.get("format_version") != FORMAT_VERSION:
        raise SurveyError(f"Unsupported snapshot format: {path}")
    for field in ("files", "candidates", "normalizers", "registered_methods"):
        if not isinstance(snapshot.get(field), list):
            raise SurveyError(f"Snapshot is missing {field}: {path}")
    if not isinstance(snapshot.get("source"), dict) or not snapshot["source"].get("revision"):
        raise SurveyError(f"Snapshot is missing its source revision: {path}")
    ids = [item.get("id") for item in snapshot["candidates"] if isinstance(item, dict)]
    if len(ids) != len(snapshot["candidates"]) or None in ids or len(set(ids)) != len(ids):
        raise SurveyError(f"Snapshot has invalid or duplicate candidate IDs: {path}")
    return snapshot


def compare(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    old = {item["id"]: item for item in before["candidates"]}
    new = {item["id"]: item for item in after["candidates"]}
    added = [new[key] for key in sorted(new.keys() - old.keys())]
    removed = [old[key] for key in sorted(old.keys() - new.keys())]
    occurrence_changes = [
        {"id": key, "before": old[key]["occurrences"], "after": new[key]["occurrences"]}
        for key in sorted(old.keys() & new.keys())
        if old[key]["occurrences"] != new[key]["occurrences"]
    ]
    old_files = {item["path"]: item["sha256"] for item in before["files"]}
    new_files = {item["path"]: item["sha256"] for item in after["files"]}
    file_changes = [
        {"path": path, "before": old_files.get(path), "after": new_files.get(path)}
        for path in sorted(old_files.keys() | new_files.keys())
        if old_files.get(path) != new_files.get(path)
    ]

    def normalizer_keys(snapshot: dict[str, Any]) -> dict[tuple[str, str], str]:
        return {
            (item["occurrence"]["path"], item["name"]): item["fingerprint"]
            for item in snapshot["normalizers"]
        }

    old_normalizers, new_normalizers = normalizer_keys(before), normalizer_keys(after)
    normalizer_changes = [
        {
            "path": path,
            "name": name,
            "before": old_normalizers.get((path, name)),
            "after": new_normalizers.get((path, name)),
        }
        for path, name in sorted(old_normalizers.keys() | new_normalizers.keys())
        if old_normalizers.get((path, name)) != new_normalizers.get((path, name))
    ]
    return {
        "format_version": FORMAT_VERSION,
        "before": before["source"],
        "after": after["source"],
        "summary": {
            "added_candidates": len(added),
            "removed_candidates": len(removed),
            "retained_candidates": len(old.keys() & new.keys()),
            "occurrence_changes": len(occurrence_changes),
            "changed_source_files": len(file_changes),
            "changed_normalizers": len(normalizer_changes),
        },
        "added": added,
        "removed": removed,
        "normalizer_changes": normalizer_changes,
        "occurrence_changes": occurrence_changes,
        "file_changes": file_changes,
        "added_methods": sorted(
            set(after["registered_methods"]) - set(before["registered_methods"])
        ),
        "removed_methods": sorted(
            set(before["registered_methods"]) - set(after["registered_methods"])
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan", help="Read committed source at a pinned revision.")
    scan.add_argument("--source", type=Path, required=True, help="Local upstream repository root.")
    scan.add_argument(
        "--ref", default="HEAD", help="Commit, tag or branch; resolved to an immutable commit."
    )
    diff = commands.add_parser(
        "diff", help="Compare candidate identities, ignoring source line shifts."
    )
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    for command in (scan, diff):
        command.add_argument(
            "--output", type=Path, help="Write JSON here; default: standard output."
        )
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            result = survey(args.source, args.ref)
        else:
            result = compare(read_snapshot(args.before), read_snapshot(args.after))
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(json.dumps(result["summary"], sort_keys=True), file=sys.stderr)
        else:
            print(rendered, end="")
    except (SurveyError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"errorgram upstream: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
