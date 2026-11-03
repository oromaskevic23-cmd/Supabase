"""Independent, no-network tests for the advisor decision gate."""
import copy
import json
import unittest

from scripts.advisor_gate import evaluate, SnapshotError, main
from scripts.validate_repo import ROOT


def sample():
    return {"schema_version": 1, "observed_at_utc": "2026-11-03T20:58:01Z",
            "security": [], "performance": []}


class AdvisorGateTests(unittest.TestCase):
    def test_current_security_warning_blocks(self):
        record = json.loads((ROOT / "docs/advisor-baseline-2026-11-03.json").read_text())
        report = evaluate(record)
        self.assertEqual(report["gate"], "BLOCK")
        self.assertEqual(report["blocking_types"], 1)
        self.assertEqual(sum(f["count"] for f in report["findings"]), 148)

    def test_empty_report_is_not_proof_of_production_security(self):
        self.assertEqual(evaluate(sample())["gate"], "NO_FINDINGS_REPORTED")

    def test_info_requires_review(self):
        record = sample()
        record["security"] = [{"name": "rls_enabled_no_policy", "level": "INFO", "count": 3}]
        self.assertEqual(evaluate(record)["gate"], "REVIEW")

    def test_performance_warning_is_review_not_unilateral_ddl(self):
        record = sample()
        record["performance"] = [{"name": "unused_index", "level": "WARN", "count": 1}]
        self.assertEqual(evaluate(record)["gate"], "REVIEW")

    def test_critical_performance_finding_blocks(self):
        record = sample()
        record["performance"] = [{"name": "critical_index", "level": "ERROR", "count": 1}]
        self.assertEqual(evaluate(record)["gate"], "BLOCK")

    def test_reject_unaudited_raw_findings_and_secrets(self):
        record = sample()
        record["security"] = [{"name": "issue", "level": "WARN", "count": 1,
                               "findings": [{"secret": "never ingest"}]}]
        with self.assertRaises(SnapshotError):
            evaluate(record)

    def test_invalid_timestamp_rejected(self):
        record = sample()
        record["observed_at_utc"] = "2026-11-03"
        with self.assertRaises(SnapshotError):
            evaluate(record)

    def test_bool_count_rejected(self):
        record = sample()
        record["security"] = [{"name": "issue", "level": "INFO", "count": True}]
        with self.assertRaises(SnapshotError):
            evaluate(record)

    def test_duplicate_advisor_type_rejected(self):
        record = sample()
        record["security"] = [{"name": "issue", "level": "INFO", "count": 1}] * 2
        with self.assertRaises(SnapshotError):
            evaluate(record)

    def test_cli_blocks_known_warning(self):
        self.assertEqual(main([str(ROOT / "docs/advisor-baseline-2026-11-03.json")]), 2)

    def test_access_inventory_is_read_only_and_catalog_based(self):
        text = (ROOT / "ops/readonly_access_matrix.sql").read_text()
        self.assertIn("pg_catalog.pg_class", text)
        self.assertIn("has_function_privilege", text)


if __name__ == "__main__":
    unittest.main()
