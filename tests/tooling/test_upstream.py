"""Git-backed tests keep scans tied to committed source, without network access."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.upstream import SurveyError, compare, read_snapshot, survey

SCRIPT = Path(__file__).resolve().parents[2] / "tools/upstream.py"


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "upstream"
    root.mkdir()
    git(root, "init", "--quiet")
    (root / "CMakeLists.txt").write_text("project(TelegramBotApi VERSION 10.3 LANGUAGES CXX)\n")
    (root / "telegram-bot-api").mkdir()
    (root / "telegram-bot-api/Client.cpp").write_text(
        'fail_query(400, "Bad Request: before", query);\n'
    )
    commit(root)
    return root


def commit(root):
    git(root, "add", "--all")
    git(
        root,
        "-c",
        "user.name=Errorgram test",
        "-c",
        "user.email=test@example.invalid",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "--quiet",
        "-m",
        "fixture",
    )
    return git(root, "rev-parse", "HEAD")


def test_revision_version_fingerprints_and_tdlib_pin(repo):
    revision = git(repo, "rev-parse", "HEAD")
    git(repo, "update-index", "--add", "--cacheinfo", f"160000,{revision},td")
    git(
        repo,
        "-c",
        "user.name=Errorgram test",
        "-c",
        "user.email=test@example.invalid",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "--quiet",
        "-m",
        "pin TDLib",
    )
    snapshot = survey(repo)
    assert snapshot["source"]["revision"] == git(repo, "rev-parse", "HEAD")
    assert snapshot["source"]["version"] == "10.3"
    assert snapshot["source"]["content"] == "committed_git_blobs"
    assert snapshot["source"]["tdlib_revision"] == revision
    assert snapshot["scope"] == "source_candidates"
    assert len(snapshot["files"]) == 2
    assert all(len(file["sha256"]) == 64 for file in snapshot["files"])
    assert snapshot["summary"]["candidate_groups"] == 1
    assert snapshot["source"]["local_worktree_dirty"] is False


def test_dirty_worktree_and_staged_changes_do_not_leak_into_pinned_scan(repo):
    before = survey(repo)
    (repo / "telegram-bot-api/Client.cpp").write_text('fail_query(500, "dirty", query);\n')
    (repo / "CMakeLists.txt").write_text("project(TelegramBotApi VERSION 99.0)\n")
    git(repo, "add", "CMakeLists.txt")
    (repo / "telegram-bot-api/Untracked.cpp").write_text('fail_query(400, "untracked", query);')
    after = survey(repo)
    assert after["source"]["local_worktree_dirty"] is True
    assert after["source"]["version"] == "10.3"
    assert after["files"] == before["files"]
    assert after["candidates"] == before["candidates"]


def test_line_shifts_change_locations_but_not_candidate_identities(repo):
    before = survey(repo)
    source = repo / "telegram-bot-api/Client.cpp"
    source.write_text("// Documentation added.\n\n" + source.read_text())
    commit(repo)
    after = survey(repo)
    diff = compare(before, after)
    assert diff["added"] == []
    assert diff["removed"] == []
    assert diff["summary"]["retained_candidates"] == 1
    assert diff["summary"]["occurrence_changes"] == 1
    assert diff["summary"]["changed_source_files"] == 1


def test_added_removed_candidates_and_methods(repo):
    source = repo / "telegram-bot-api/Client.cpp"
    source.write_text(source.read_text() + 'methods_.emplace("old", &Client::old);\n')
    before_revision = commit(repo)
    source.write_text(
        'fail_query(403, "Forbidden: after", query);\nmethods_.emplace("new", &Client::new);\n'
    )
    after_revision = commit(repo)
    diff = compare(survey(repo, before_revision), survey(repo, after_revision))
    assert len(diff["added"]) == len(diff["removed"]) == 1
    assert diff["added"][0]["message"]["value"] == "Forbidden: after"
    assert diff["removed"][0]["message"]["value"] == "Bad Request: before"
    assert diff["added_methods"] == ["new"]
    assert diff["removed_methods"] == ["old"]


def test_normalizer_mapping_and_branch_changes_are_visible(repo):
    source = repo / "telegram-bot-api/Client.cpp"
    body = """
        void Client::fail_query_with_error(Query query, int32 error_code,
                                          td::CSlice error_message) {
            if (error_message == "MESSAGE_NOT_MODIFIED") {
                error_code = 400;
                error_message = "message is not modified";
            }
            fail_query(error_code, error_message, query);
        }
    """
    source.write_text(body)
    first = commit(repo)
    source.write_text(body.replace('"message is not modified"', '"message is unchanged"'))
    second = commit(repo)
    changed_message = compare(survey(repo, first), survey(repo, second))
    assert changed_message["summary"]["added_candidates"] == 1
    assert changed_message["added"][0]["role"] == "normalization_output"
    assert len(changed_message["normalizer_changes"]) == 1
    source.write_text(source.read_text().replace("error_code = 400", "error_code = 403"))
    third = commit(repo)
    changed_branch = compare(survey(repo, second), survey(repo, third))
    assert changed_branch["added"] == changed_branch["removed"] == []
    assert len(changed_branch["normalizer_changes"]) == 1


def test_normalizer_layout_changes_do_not_change_semantics(repo):
    source = repo / "telegram-bot-api/Client.cpp"
    source.write_text("""
        void Client::fail_query_with_error(Query query, int32 error_code,
                                          td::CSlice error_message) {
            if (error_message == "OLD") { error_message = "new"; }
        }
    """)
    first = commit(repo)
    source.write_text(source.read_text().replace("if (", "// Description.\n            if ("))
    second = commit(repo)
    diff = compare(survey(repo, first), survey(repo, second))
    assert diff["added"] == diff["removed"] == diff["normalizer_changes"] == []


def test_historical_ref_is_read_without_switching_checkout(repo):
    first = git(repo, "rev-parse", "HEAD")
    (repo / "CMakeLists.txt").write_text("project(TelegramBotApi VERSION 10.4)\n")
    current = commit(repo)
    assert survey(repo, first)["source"]["version"] == "10.3"
    assert survey(repo, "HEAD")["source"]["version"] == "10.4"
    assert git(repo, "rev-parse", "HEAD") == current
    assert "10.4" in (repo / "CMakeLists.txt").read_text()


@pytest.mark.parametrize("ref", ["not-a-revision", "--help", ""])
def test_invalid_refs_fail(repo, ref):
    with pytest.raises(SurveyError):
        survey(repo, ref)


def test_missing_source_and_nested_repository_paths_fail(repo, tmp_path):
    with pytest.raises(SurveyError, match="does not exist"):
        survey(tmp_path / "absent")
    with pytest.raises(SurveyError, match="repository root"):
        survey(repo / "telegram-bot-api")


def test_cli_writes_json_and_diff_without_changing_checkout(repo, tmp_path):
    output = tmp_path / "new-directory/snapshot.json"
    scan = subprocess.run(
        [sys.executable, str(SCRIPT), "scan", "--source", str(repo), "--output", str(output)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert scan.stdout == ""
    assert json.loads(scan.stderr)["candidate_groups"] == 1
    snapshot = read_snapshot(output)
    diff = subprocess.run(
        [sys.executable, str(SCRIPT), "diff", str(output), str(output)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(diff.stdout)["summary"]["added_candidates"] == 0
    assert snapshot["source"]["revision"] == git(repo, "rev-parse", "HEAD")
    assert git(repo, "status", "--porcelain") == ""


def test_cli_reports_invalid_snapshot_concisely(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text('{"format_version": 999}')
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "diff", str(broken), str(broken)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Unsupported snapshot format" in result.stderr
    assert "Traceback" not in result.stderr


def test_duplicate_candidate_ids_are_rejected(repo, tmp_path):
    snapshot = survey(repo)
    snapshot["candidates"].append(snapshot["candidates"][0])
    output = tmp_path / "duplicate.json"
    output.write_text(json.dumps(snapshot))
    with pytest.raises(SurveyError, match="duplicate candidate IDs"):
        read_snapshot(output)
