"""Check that source, operations and documentation accurately state open gates."""
import unittest

from scripts.validate_repo import ROOT


class ContractDocumentationTests(unittest.TestCase):
    def test_federation_docs_keep_production_closed(self):
        doc=(ROOT/"docs/PRODUCTION_ACTIVATION_GATES.md").read_text()
        self.assertIn("LAB_ONLY",doc)
        self.assertIn("G0 — Owner trust",doc)
        self.assertIn("G8 — Controlled release",doc)
        self.assertIn("no cryptographic verifier",doc)

    def test_readonly_tenant_sql(self):
        text=(ROOT/"ops/readonly_workspace_contract.sql").read_text()
        self.assertIn("has_schema_privilege",text)
        self.assertIn("relrowsecurity",text)
        self.assertIn("idempotency",text) if "idempotency" in text else self.assertIn("pg_catalog.pg_constraint",text)

    def test_source_keeps_federated_route(self):
        source=(ROOT/"scripts/federation_gate.py").read_text()
        self.assertIn("FEDERATED_ROUTE_DENIED",source)
        self.assertIn("OWNER_KILL_SWITCH",source)
        self.assertIn("AUTHORIZED_LAB_ONLY",source)
        self.assertIn("PRODUCTION_UNAVAILABLE",source)
        self.assertNotIn("supabase_client",source)

    def test_tenant_inspection_does_not_claim_production_pass(self):
        report=(ROOT/"docs/TENANT_ISOLATION_REPORT_2026-11-04.md").read_text()
        self.assertIn("does **not** prove tenant isolation",report)
        self.assertIn("0 RLS policies",report)
        self.assertIn("indirect views",report)

    def test_runbook_links_to_real_gate(self):
        runbook=(ROOT/"docs/RUNBOOK.md").read_text()
        self.assertIn("PRODUCTION_ACTIVATION_GATES.md",runbook)


if __name__ == "__main__":
    unittest.main()
