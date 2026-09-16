#!/usr/bin/env python3
"""Validate a release identity and the exact distributions approved for publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
SHA = re.compile(r"[0-9a-f]{40}")


class ReleaseError(ValueError):
    """A release cannot be tied to the intended version, commit or files."""


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments], check=False, capture_output=True, text=True
    )
    if result.returncode:
        raise ReleaseError(result.stderr.strip() or "Git release check failed.")
    return result.stdout.strip()


def validate_version(version: str) -> str:
    if not VERSION.fullmatch(version):
        raise ReleaseError("Use a stable version in X.Y.Z form, without a v prefix.")
    return version


def identity(root: Path, version: str, tag: str, expected_sha: str) -> dict[str, str]:
    if not version and not tag:
        raise ReleaseError("Supply an explicit version or an existing vX.Y.Z tag.")
    if tag and not re.fullmatch(r"v" + VERSION.pattern, tag):
        raise ReleaseError("Release tags must use vX.Y.Z form.")
    version = validate_version(version or tag[1:])
    if tag and tag != f"v{version}":
        raise ReleaseError("The requested version and release tag disagree.")
    if not SHA.fullmatch(expected_sha):
        raise ReleaseError("Expected commit must be a full Git SHA.")
    if git(root, "rev-parse", "HEAD") != expected_sha:
        raise ReleaseError("The checkout differs from the workflow's immutable commit.")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise ReleaseError("Tracked files differ from the release commit.")

    python = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    npm = json.loads((root / "js/package.json").read_text())
    lock = json.loads((root / "js/package-lock.json").read_text())
    for label, package in (
        ("Python", python), ("npm", npm), ("npm lockfile", lock),
        ("npm lockfile root", lock["packages"][""]),
    ):
        if package.get("name") != "errorgram" or package.get("version") != version:
            raise ReleaseError(f"{label} name/version does not match errorgram {version}.")

    existing = git(root, "tag", "--list", f"v{version}")
    if tag or existing:
        revision = git(root, "rev-parse", "--verify", f"refs/tags/v{version}^{{commit}}")
        if revision != expected_sha:
            raise ReleaseError("The release tag must point to the workflow's commit on main.")
    return {"version": version, "commit": expected_sha, "tag": tag or existing}


def filenames(version: str) -> dict[str, str]:
    validate_version(version)
    return {
        f"errorgram-{version}-py3-none-any.whl": "pypi",
        f"errorgram-{version}.tar.gz": "pypi",
        f"errorgram-{version}.tgz": "npm",
    }


def inspect_distribution(path: Path, version: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise ReleaseError(f"Distribution is not a regular file: {path.name}")
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            metadata_names = [
                name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
            ]
            if metadata_names != [f"errorgram-{version}.dist-info/METADATA"]:
                raise ReleaseError("Wheel has unexpected or duplicate package metadata.")
            metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
    else:
        with tarfile.open(path, "r:gz") as archive:
            member_name = (
                "package/package.json" if path.suffix == ".tgz"
                else f"errorgram-{version}/PKG-INFO"
            )
            members = [member for member in archive.getmembers() if member.name == member_name]
            if len(members) != 1 or not members[0].isfile():
                raise ReleaseError(f"Missing or duplicate package metadata: {path.name}")
            stream = archive.extractfile(members[0])
            if stream is None:
                raise ReleaseError(f"Cannot read package metadata: {path.name}")
            if path.suffix == ".tgz":
                package = json.load(stream)
                metadata = {"Name": package.get("name"), "Version": package.get("version")}
                repository = package.get("repository", {})
                if repository.get("url") != "git+https://github.com/uburuntu/errorgram.git":
                    raise ReleaseError("npm repository must match the trusted GitHub repository.")
            else:
                metadata = BytesParser().parsebytes(stream.read())
    if metadata["Name"] != "errorgram" or metadata["Version"] != version:
        raise ReleaseError(f"Distribution metadata does not match errorgram {version}: {path.name}")


def stage(dist: Path, output: Path, version: str, commit: str) -> dict:
    expected = filenames(version)
    if not SHA.fullmatch(commit):
        raise ReleaseError("Expected commit must be a full Git SHA.")
    actual = {path.name for path in dist.iterdir()} - {".gitignore"}
    if actual != set(expected):
        raise ReleaseError("dist must contain exactly this version's wheel, sdist and npm tarball.")
    if output.exists():
        raise ReleaseError("Use a new output directory to avoid stale release artifacts.")
    for name in expected:
        inspect_distribution(dist / name, version)
    files = []
    for name, registry in expected.items():
        target = output / registry / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dist / name, target)
        files.append({
            "path": f"{registry}/{name}",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        })
    manifest = {"version": version, "commit": commit, "files": files}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def verify(directory: Path, version: str, commit: str) -> dict:
    expected = {f"{registry}/{name}" for name, registry in filenames(version).items()}
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("version") != version or manifest.get("commit") != commit:
        raise ReleaseError("Artifact version/commit differs from the approved release.")
    files = manifest.get("files", [])
    if len(files) != 3 or {item["path"] for item in files} != expected:
        raise ReleaseError("Release manifest must name exactly the expected three distributions.")
    actual = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*") if path.is_file() or path.is_symlink()
    }
    if actual != expected | {"manifest.json"}:
        raise ReleaseError("Release artifact contains missing or unexpected files.")
    for item in files:
        path = directory / item["path"]
        inspect_distribution(path, version)
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise ReleaseError(f"Distribution checksum mismatch: {path.name}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser(
        "identity", help="Check committed package versions and release tag."
    )
    check.add_argument("--root", type=Path, default=ROOT)
    check.add_argument("--version", default="")
    check.add_argument("--tag", default="")
    check.add_argument("--commit", required=True)
    check.add_argument("--github-output", type=Path)
    prepare = commands.add_parser(
        "stage", help="Separate registry files and record SHA-256 hashes."
    )
    prepare.add_argument("--dist", type=Path, default=ROOT / "dist")
    prepare.add_argument("--output", type=Path, required=True)
    audit = commands.add_parser("verify", help="Recheck downloaded files before publication.")
    audit.add_argument("--directory", type=Path, required=True)
    for command in (prepare, audit):
        command.add_argument("--version", required=True)
        command.add_argument("--commit", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "identity":
            result = identity(args.root, args.version, args.tag, args.commit)
            if args.github_output:
                with args.github_output.open("a") as stream:
                    stream.write(f"version={result['version']}\ncommit={result['commit']}\n")
        elif args.command == "stage":
            result = stage(args.dist, args.output, args.version, args.commit)
        else:
            result = verify(args.directory, args.version, args.commit)
        print(json.dumps(result, indent=2))
    except (
        ReleaseError, OSError, ValueError, KeyError, TypeError, AttributeError,
        tarfile.TarError, zipfile.BadZipFile,
    ) as error:
        print(f"Release validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
