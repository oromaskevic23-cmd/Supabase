"""Independent offline simulation checks: not production integration tests."""
from dataclasses import replace
import unittest

from scripts.federation_gate import (
    ApprovalEvidence, FederatedDispatchGate, LabTrustState,
    PassportEvidence, QAEvidence, TaskEnvelope, sha256,
)


class FederationGateTests(unittest.TestCase):
    def setUp(self):
        self.payload = b"non-sensitive deterministic simulation"
        self.task = TaskEnvelope(
            task_id="mission-001", workspace_id="CRM-ALPHA",
            actor_id="operator-A", orchestrator_id="CRM-SOFFT",
            agent_id="NCA-100", capability="offline-analysis",
            idempotency_key="idempotency-A", payload_sha256=sha256(b"request"),
            expires_at=2000,
        )
        self.state = LabTrustState(
            active_workspaces={"CRM-ALPHA", "CRM-BETA"},
            memberships={("CRM-ALPHA", "operator-A")},
            orchestrator_routes={("CRM-ALPHA", "CRM-SOFFT")},
            agent_scopes={("CRM-ALPHA", "CRM-SOFFT", "NCA-100", "offline-analysis")},
        )
        self.seed(self.task)
        self.gate = FederatedDispatchGate(self.state, lab=True)

    def seed(self, task):
        digest = task.digest()
        self.state.passports[digest] = PassportEvidence(digest, task.workspace_id, task.agent_id, 1900, True)
        self.state.approvals[digest] = ApprovalEvidence(digest, task.workspace_id, 1900, True)
        self.state.guardian_releases.add(digest)
        self.state.independent_qa[digest] = QAEvidence(
            digest, task.workspace_id, sha256(self.payload), "independent-reviewer", True, True)

    def assert_denied(self, task, reason, gate=None):
        result = (gate or self.gate).submit(task, now=1000)
        self.assertEqual((result.status, result.reason), ("DENIED", reason))

    def test_happy_path_is_lab_only(self):
        decision = self.gate.submit(self.task, now=1000)
        self.assertEqual(decision.status, "AUTHORIZED_LAB_ONLY")
        qa = self.gate.record_result(self.task, self.payload, now=1100)
        self.assertEqual(qa.status, "ACCEPTED_LAB_QA")
        self.assertTrue(self.gate.audit.verify())

    def test_default_production_is_closed(self):
        gate = FederatedDispatchGate(self.state)
        self.assert_denied(self.task, "PRODUCTION_UNAVAILABLE", gate)

    def test_missing_membership_denied(self):
        other = replace(self.task, actor_id="operator-B")
        self.assert_denied(other, "WORKSPACE_MEMBERSHIP_DENIED")

    def test_cross_workspace_denied_even_if_workspace_exists(self):
        other = replace(self.task, workspace_id="CRM-BETA")
        self.assert_denied(other, "WORKSPACE_MEMBERSHIP_DENIED")

    def test_cross_workspace_with_membership_still_needs_route(self):
        self.state.memberships.add(("CRM-BETA", "operator-A"))
        other = replace(self.task, workspace_id="CRM-BETA")
        self.assert_denied(other, "FEDERATED_ROUTE_DENIED")

    def test_route_cannot_be_escalated_by_task(self):
        other = replace(self.task, orchestrator_id="CAPITAL-CORE")
        self.assert_denied(other, "FEDERATED_ROUTE_DENIED")

    def test_capability_cannot_be_escalated(self):
        other = replace(self.task, capability="send-money")
        self.assert_denied(other, "AGENT_CAPABILITY_DENIED")

    def test_agent_cannot_be_substituted(self):
        other = replace(self.task, agent_id="NCA-101")
        self.assert_denied(other, "AGENT_CAPABILITY_DENIED")

    def test_no_passport(self):
        self.state.passports.clear()
        self.assert_denied(self.task, "PASSPORT_NOT_VERIFIED")

    def test_self_report_cannot_be_used_as_verified_passport(self):
        p = self.state.passports[self.task.digest()]
        self.state.passports[self.task.digest()] = replace(p, trusted_verification=False)
        self.assert_denied(self.task, "PASSPORT_NOT_VERIFIED")

    def test_revoked_passport(self):
        self.state.revoked_passports.add(self.task.digest())
        self.assert_denied(self.task, "PASSPORT_NOT_VERIFIED")

    def test_expired_passport(self):
        p = self.state.passports[self.task.digest()]
        self.state.passports[self.task.digest()] = replace(p, expires_at=1000)
        self.assert_denied(self.task, "PASSPORT_NOT_VERIFIED")

    def test_wrong_workspace_in_passport(self):
        p = self.state.passports[self.task.digest()]
        self.state.passports[self.task.digest()] = replace(p, workspace_id="CRM-BETA")
        self.assert_denied(self.task, "PASSPORT_NOT_VERIFIED")

    def test_missing_approval(self):
        self.state.approvals.clear()
        self.assert_denied(self.task, "APPROVAL_NOT_VERIFIED")

    def test_unverified_approval(self):
        p = self.state.approvals[self.task.digest()]
        self.state.approvals[self.task.digest()] = replace(p, trusted_verification=False)
        self.assert_denied(self.task, "APPROVAL_NOT_VERIFIED")

    def test_expired_approval(self):
        p = self.state.approvals[self.task.digest()]
        self.state.approvals[self.task.digest()] = replace(p, expires_at=999)
        self.assert_denied(self.task, "APPROVAL_NOT_VERIFIED")

    def test_guardian_denial(self):
        self.state.guardian_releases.clear()
        self.assert_denied(self.task, "GUARDIAN_DENIED")

    def test_owner_kill_switch(self):
        self.state.stop_all = True
        self.assert_denied(self.task, "OWNER_KILL_SWITCH")

    def test_agent_kill_switch(self):
        self.state.stopped_agents.add("NCA-100")
        self.assert_denied(self.task, "OWNER_KILL_SWITCH")

    def test_external_effects_denied_even_with_approval(self):
        other = replace(self.task, external_effects=True)
        self.assert_denied(other, "FREE_ONLY_NO_EXTERNAL_EFFECTS")

    def test_spending_denied_even_with_approval(self):
        other = replace(self.task, spend_usd=1)
        self.assert_denied(other, "FREE_ONLY_NO_EXTERNAL_EFFECTS")

    def test_expires_at_boundary(self):
        self.assertEqual(self.gate.submit(self.task, now=2000).reason, "TASK_EXPIRED")

    def test_incorrect_command_center(self):
        other = replace(self.task, command_center="OTHER")
        self.assert_denied(other, "INVALID_ENVELOPE")

    def test_wrong_payload_hash_format(self):
        other = replace(self.task, payload_sha256="hello")
        self.assert_denied(other, "INVALID_ENVELOPE")

    def test_bool_spend_rejected(self):
        other = replace(self.task, spend_usd=True)
        self.assert_denied(other, "INVALID_ENVELOPE")

    def test_duplicate_submission_not_rescheduled(self):
        self.assertEqual(self.gate.submit(self.task, now=1000).status, "AUTHORIZED_LAB_ONLY")
        later = self.gate.submit(self.task, now=1100)
        self.assertEqual((later.status, later.reason), ("DUPLICATE", "NO_REEXECUTION"))

    def test_idempotency_conflict_same_workspace(self):
        self.gate.submit(self.task, now=1000)
        collision = replace(self.task, task_id="mission-002")
        self.seed(collision)
        self.assert_denied(collision, "IDEMPOTENCY_CONFLICT")

    def test_different_workspaces_do_not_share_idempotency_keys(self):
        self.gate.submit(self.task, now=1000)
        other = replace(self.task, workspace_id="CRM-BETA")
        self.state.memberships.add(("CRM-BETA", "operator-A"))
        self.state.orchestrator_routes.add(("CRM-BETA", "CRM-SOFFT"))
        self.state.agent_scopes.add(("CRM-BETA", "CRM-SOFFT", "NCA-100", "offline-analysis"))
        self.seed(other)
        self.assertEqual(self.gate.submit(other, now=1000).status, "AUTHORIZED_LAB_ONLY")

    def test_unauthorized_result_cannot_pass(self):
        decision = self.gate.record_result(self.task, self.payload, now=1000)
        self.assertEqual(decision.reason, "UNAUTHORIZED_TASK")

    def test_result_requires_independent_qa(self):
        self.gate.submit(self.task, now=1000)
        self.state.independent_qa.clear()
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "INDEPENDENT_QA_NOT_VERIFIED")

    def test_executor_cannot_self_approve_qa(self):
        self.gate.submit(self.task, now=1000)
        qa = self.state.independent_qa[self.task.digest()]
        self.state.independent_qa[self.task.digest()] = replace(qa, reviewer_id="NCA-100")
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "INDEPENDENT_QA_NOT_VERIFIED")

    def test_initiator_cannot_self_approve_qa(self):
        self.gate.submit(self.task, now=1000)
        qa = self.state.independent_qa[self.task.digest()]
        self.state.independent_qa[self.task.digest()] = replace(qa, reviewer_id="operator-A")
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "INDEPENDENT_QA_NOT_VERIFIED")

    def test_qa_must_be_verified(self):
        self.gate.submit(self.task, now=1000)
        qa = self.state.independent_qa[self.task.digest()]
        self.state.independent_qa[self.task.digest()] = replace(qa, trusted_verification=False)
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "INDEPENDENT_QA_NOT_VERIFIED")

    def test_qa_must_match_output_digest(self):
        self.gate.submit(self.task, now=1000)
        self.assertEqual(self.gate.record_result(self.task, b"tampered", now=1100).reason,
                         "INDEPENDENT_QA_NOT_VERIFIED")

    def test_stop_after_dispatch_blocks_result(self):
        self.gate.submit(self.task, now=1000)
        self.state.stop_all = True
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "OWNER_KILL_SWITCH")

    def test_revoke_after_dispatch_blocks_result(self):
        self.gate.submit(self.task, now=1000)
        self.state.revoked_passports.add(self.task.digest())
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).reason,
                         "AUTHORITY_EXPIRED_OR_REVOKED")

    def test_qa_result_cannot_be_recorded_twice(self):
        self.gate.submit(self.task, now=1000)
        self.gate.record_result(self.task, self.payload, now=1100)
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=1100).status, "DUPLICATE")

    def test_audit_chain_detects_tampering(self):
        self.gate.submit(self.task, now=1000)
        self.assertTrue(self.gate.audit.verify())
        self.gate.audit.events[0]["code"] = "TAMPERED"
        self.assertFalse(self.gate.audit.verify())

    def test_invalid_payload_rejected(self):
        self.gate.submit(self.task, now=1000)
        self.assertEqual(self.gate.record_result(self.task, "untrusted string", now=1100).reason,
                         "INVALID_RESULT_PAYLOAD")

    def test_stale_result_rejected(self):
        self.gate.submit(self.task, now=1000)
        self.assertEqual(self.gate.record_result(self.task, self.payload, now=2000).reason,
                         "AUTHORITY_EXPIRED_OR_REVOKED")


if __name__ == "__main__":
    unittest.main()
