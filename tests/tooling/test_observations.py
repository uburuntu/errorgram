"""Keep recorded hosted evidence consistent with the catalogue it supports."""

import json
from pathlib import Path

from errorgram import classify

from tools.validate import load_catalogue

ROOT = Path(__file__).resolve().parents[2]


def test_recorded_observations_support_every_observed_condition():
    catalogue = load_catalogue()
    observed = set()
    for path in (ROOT / "observations").glob("*.json"):
        report = json.loads(path.read_text())
        assert report["status"] == "passed"
        assert report["deployment"] == {"host": "api.telegram.org", "api_version": "unknown"}
        if report["message_tests"]:
            assert report["cleanup"] == "succeeded"
        for check in report["checks"]:
            if check["expected_id"] is None:
                assert "response" not in check
                continue
            result = classify(check["response"], method=check["method"], catalogue=catalogue)
            assert result.status == "matched"
            assert result.id == check["expected_id"] == check["matched_id"]
            observed.add(result.id)
    assert observed == {
        entry["id"] for entry in catalogue["entries"] if entry["evidence_level"] == "observed"
    }
