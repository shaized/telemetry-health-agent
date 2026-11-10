import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_missing_observation_is_unknown(self):
        self.assertEqual(
            [row["status"] for row in analyze(self.data)["findings"]],
            ["fresh", "stale", "unknown"],
        )

    def test_exact_threshold_is_fresh(self):
        self.data["sources"][0]["last_seen"] = "2026-01-15T11:45:00Z"
        self.assertEqual(analyze(self.data)["findings"][0]["status"], "fresh")
        self.data["sources"][0]["last_seen"] = "2026-01-15T11:44:59Z"
        self.assertEqual(analyze(self.data)["findings"][0]["status"], "stale")

    def test_future_event_is_not_healthy(self):
        self.data["sources"][0]["last_seen"] = "2026-01-15T12:01:00Z"
        self.assertEqual(
            analyze(self.data)["findings"][0]["status"], "future_timestamp"
        )

    def test_maintenance_preserves_underlying_freshness(self):
        self.data["sources"][1]["maintenance_until"] = "2026-01-15T13:00:00Z"
        row = analyze(self.data)["findings"][1]
        self.assertEqual(row["status"], "maintenance")
        self.assertEqual(row["freshness"], "stale")

    def test_expired_maintenance_does_not_hide_gap(self):
        self.data["sources"][1]["maintenance_until"] = "2026-01-15T12:00:00Z"
        self.assertEqual(analyze(self.data)["findings"][1]["status"], "stale")

    def test_negative_threshold_is_rejected(self):
        self.data["sources"][0]["max_silence_seconds"] = -1
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_empty_inventory_does_not_claim_all_sources_healthy(self):
        self.data["sources"] = []
        self.assertEqual(analyze(self.data)["summary"]["expected_sources"], 0)
        self.assertTrue(analyze(self.data)["limitations"])


if __name__ == "__main__":
    unittest.main()
