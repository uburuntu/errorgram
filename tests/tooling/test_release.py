"""Exercise release guards with real Git commits and package archives."""

import io
import json
import subprocess
import tarfile
import zipfile
from pathlib import Path

import pytest

from tools.release import ReleaseError, identity, stage, verify

VERSION = "0.1.0"
COMMIT = "a" * 40


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def commit(root: Path) -> str:
    git(root, "add", ".")
    git(
        root, "-c", "user.name=Release test", "-c", "user.email=test@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-qm", "fixture",
    )
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def repository(tmp_path):
    root = tmp_path / "repository"
    (root / "js").mkdir(parents=True)
    git(root, "init", "-q")
    (root / "pyproject.toml").write_text('[project]\nname = "errorgram"\nversion = "0.1.0"\n')
    package = {"name": "errorgram", "version": VERSION}
    (root / "js/package.json").write_text(json.dumps(package))
    (root / "js/package-lock.json").write_text(
        json.dumps({**package, "packages": {"": package}})
    )
    return root, commit(root)


def test_explicit_version_and_existing_tag_bind_to_the_same_commit(repository):
    root, sha = repository
    assert identity(root, VERSION, "", sha) == {"version": VERSION, "commit": sha, "tag": ""}
    git(root, "tag", "v0.1.0")
    assert identity(root, "", "v0.1.0", sha)["version"] == VERSION


def test_stale_tag_and_changed_checkout_fail(repository):
    root, old_sha = repository
    git(root, "tag", "v0.1.0")
    (root / "README.md").write_text("A newer commit.\n")
    new_sha = commit(root)
    with pytest.raises(ReleaseError, match="immutable commit"):
        identity(root, VERSION, "", old_sha)
    with pytest.raises(ReleaseError, match="tag must point"):
        identity(root, VERSION, "", new_sha)


@pytest.mark.parametrize("filename", ["package.json", "package-lock.json"])
def test_committed_package_version_mismatch_fails(repository, filename):
    root, _ = repository
    path = root / "js" / filename
    path.write_text(path.read_text().replace("0.1.0", "0.2.0"))
    sha = commit(root)
    with pytest.raises(ReleaseError, match="name/version"):
        identity(root, VERSION, "", sha)


def test_dirty_tracked_files_fail(repository):
    root, sha = repository
    (root / "js/package.json").write_text("{}")
    with pytest.raises(ReleaseError, match="Tracked files"):
        identity(root, VERSION, "", sha)


@pytest.mark.parametrize(
    ("version", "tag"),
    [("", ""), ("0.1.0\ninjected=true", ""), ("0.1.0", "v0.2.0"), ("", "--help")],
)
def test_missing_or_ambiguous_release_input_fails(repository, version, tag):
    root, sha = repository
    with pytest.raises(ReleaseError):
        identity(root, version, tag, sha)


def write_tar(path: Path, name: str, data: bytes) -> None:
    with tarfile.open(path, "w:gz") as archive:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))


@pytest.fixture
def distributions(tmp_path):
    directory = tmp_path / "dist"
    directory.mkdir()
    metadata = b"Metadata-Version: 2.4\nName: errorgram\nVersion: 0.1.0\n"
    with zipfile.ZipFile(directory / "errorgram-0.1.0-py3-none-any.whl", "w") as archive:
        archive.writestr("errorgram-0.1.0.dist-info/METADATA", metadata)
    write_tar(directory / "errorgram-0.1.0.tar.gz", "errorgram-0.1.0/PKG-INFO", metadata)
    package = {
        "name": "errorgram", "version": VERSION,
        "repository": {"url": "git+https://github.com/uburuntu/errorgram.git"},
    }
    write_tar(
        directory / "errorgram-0.1.0.tgz", "package/package.json", json.dumps(package).encode()
    )
    return directory


def test_registry_artifacts_are_separate_and_reverified(distributions, tmp_path):
    output = tmp_path / "release"
    manifest = stage(distributions, output, VERSION, COMMIT)
    assert {path.name for path in (output / "pypi").iterdir()} == {
        "errorgram-0.1.0-py3-none-any.whl", "errorgram-0.1.0.tar.gz",
    }
    assert {path.name for path in (output / "npm").iterdir()} == {"errorgram-0.1.0.tgz"}
    assert verify(output, VERSION, COMMIT) == manifest
    with pytest.raises(ReleaseError, match="version/commit"):
        verify(output, VERSION, "b" * 40)


def test_stale_or_unexpected_distributions_fail(distributions, tmp_path):
    (distributions / "errorgram-0.0.1.tgz").write_bytes(b"stale")
    with pytest.raises(ReleaseError, match="exactly this version"):
        stage(distributions, tmp_path / "release", VERSION, COMMIT)


def test_archive_metadata_must_match_filename(distributions, tmp_path):
    write_tar(
        distributions / "errorgram-0.1.0.tar.gz", "errorgram-0.1.0/PKG-INFO",
        b"Name: another-project\nVersion: 0.1.0\n",
    )
    with pytest.raises(ReleaseError, match="metadata does not match"):
        stage(distributions, tmp_path / "release", VERSION, COMMIT)
    assert not (tmp_path / "release").exists()


def test_tampered_archive_and_extra_publish_files_fail(distributions, tmp_path):
    output = tmp_path / "release"
    stage(distributions, output, VERSION, COMMIT)
    wheel = output / "pypi/errorgram-0.1.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "a") as archive:
        archive.writestr("errorgram/changed.py", "print('changed')")
    with pytest.raises(ReleaseError, match="checksum mismatch"):
        verify(output, VERSION, COMMIT)
    (output / "pypi/another-package.whl").write_bytes(b"unapproved")
    with pytest.raises(ReleaseError, match="unexpected files"):
        verify(output, VERSION, COMMIT)


def test_manifest_path_traversal_is_rejected(distributions, tmp_path):
    output = tmp_path / "release"
    manifest = stage(distributions, output, VERSION, COMMIT)
    manifest["files"][0]["path"] = "../../unapproved.whl"
    (output / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ReleaseError, match="exactly the expected"):
        verify(output, VERSION, COMMIT)
