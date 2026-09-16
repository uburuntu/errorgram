"""Review summaries distinguish source movement from semantic candidate changes."""

import copy
import json
from pathlib import Path

from tools.upstream import compare
from tools.upstream_report import render


def test_baseline_reports_no_changes_and_links_to_immutable_revision():
    root = Path(__file__).resolve().parents[2]
    baseline = json.loads((root / "catalogue/upstream.json").read_text())
    summary = render(compare(baseline, baseline))
    assert "No scanned source changes." in summary
    assert f"/commit/{baseline['source']['revision']}" in summary
    assert "not verified public errors" in summary


def test_call_location_changes_still_require_review():
    root = Path(__file__).resolve().parents[2]
    before = json.loads((root / "catalogue/upstream.json").read_text())
    after = copy.deepcopy(before)
    after["source"]["revision"] = "f" * 40
    after["candidates"][0]["occurrences"][0]["line"] += 1
    summary = render(compare(before, after))
    assert "Source changes need review." in summary
    assert "| Added candidates | 0 |" in summary
    assert "| Changed call locations | 1 |" in summary
