"""Offline reference implementation: IMPERIAL Core federated dispatch contract.

NO DATABASE, NETWORK, CRYPTOGRAPHIC ENROLLMENT OR PRODUCTION WORKER.
This lab deliberately refuses production dispatch. Its trusted records are fixtures,
NOT proof of an Ed25519 AI Passport or valid Owner approval.
"""
from dataclasses import asdict, dataclass, field
import hashlib
import hmac
import json
import re

IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{1,95}$")
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_digest(value: dict) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode())


def _valid_identifier(value: object) -> bool:
    return isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None


def _valid_digest(value: object) -> bool:
    return isinstance(value, str) and HEX64.fullmatch(value) is not None


def _valid_time(value: object) -> bool:
    return type(value) is int and value >= 0


@dataclass(frozen=True)
class TaskEnvelope:
    task_id: str
    workspace_id: str
    actor_id: str
    orchestrator_id: str
    agent_id: str
    capability: str
    idempotency_key: str
    payload_sha256: str
    expires_at: int
    external_effects: bool = False
    spend_usd: int = 0
    command_center: str = "HANTER"

    def digest(self) -> str:
        return canonical_digest(asdict(self))

    def valid(self) -> bool:
        return (
            all(_valid_identifier(x) for x in (
                self.task_id, self.workspace_id, self.actor_id,
                self.orchestrator_id, self.agent_id, self.capability,
                self.idempotency_key))
            and _valid_digest(self.payload_sha256)
            and _valid_time(self.expires_at)
            and type(self.external_effects) is bool
            and type(self.spend_usd) is int and self.spend_usd >= 0
            and self.command_center == "HANTER"
        )


@dataclass(frozen=True)
class PassportEvidence:
    task_digest: str
    workspace_id: str
    agent_id: str
    expires_at: int
    trusted_verification: bool = False


@dataclass(frozen=True)
class ApprovalEvidence:
    task_digest: str
    workspace_id: str
    expires_at: int
    trusted_verification: bool = False


@dataclass(frozen=True)
class QAEvidence:
    task_digest: str
    workspace_id: str
    output_sha256: str
    reviewer_id: str
    accepted: bool
    trusted_verification: bool = False


@dataclass
class LabTrustState:
    """Simulated pre-verified records; never load these from job payloads."""
    active_workspaces: set[str] = field(default_factory=set)
    memberships: set[tuple[str, str]] = field(default_factory=set)
    orchestrator_routes: set[tuple[str, str]] = field(default_factory=set)
    agent_scopes: set[tuple[str, str, str, str]] = field(default_factory=set)
    passports: dict[str, PassportEvidence] = field(default_factory=dict)
    approvals: dict[str, ApprovalEvidence] = field(default_factory=dict)
    guardian_releases: set[str] = field(default_factory=set)
    independent_qa: dict[str, QAEvidence] = field(default_factory=dict)
    stopped_agents: set[str] = field(default_factory=set)
    revoked_passports: set[str] = field(default_factory=set)
    stop_all: bool = False


class AuditLedgerLab:
    """Local hash chain detects edits when recomputed; NOT immutable storage."""
    def __init__(self):
        self.events: list[dict] = []

    def record(self, kind: str, task_digest: str, code: str) -> str:
        previous = self.events[-1]["hash"] if self.events else "0" * 64
        payload = {"seq": len(self.events) + 1, "prev": previous,
                   "kind": kind, "task_digest": task_digest, "code": code}
        entry = dict(payload, hash=canonical_digest(payload))
        self.events.append(entry)
        return entry["hash"]

    def verify(self) -> bool:
        previous = "0" * 64
        for number, entry in enumerate(self.events, 1):
            data = {key: entry.get(key) for key in ("seq", "prev", "kind", "task_digest", "code")}
            if entry.get("seq") != number or entry.get("prev") != previous:
                return False
            if not hmac.compare_digest(entry.get("hash", ""), canonical_digest(data)):
                return False
            previous = entry["hash"]
        return True


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    task_digest: str
    audit_hash: str


class FederatedDispatchGate:
    """Fail-closed reference policy with no worker invocation.

    Production mode is intentionally disabled. 'lab' uses *trusted fixture state*
    rather than production-grade verification. No task content is executed.
    """
    def __init__(self, state: LabTrustState | None = None, *, lab: bool = False):
        self.state = state if state is not None else LabTrustState()
        self.lab = lab
        self.audit = AuditLedgerLab()
        self._idempotency: dict[tuple[str, str], str] = {}
        self._accepted: dict[str, TaskEnvelope] = {}
        self._completed: set[str] = set()

    def _decision(self, status: str, reason: str, digest: str) -> Decision:
        proof = self.audit.record(status, digest, reason)
        return Decision(status, reason, digest, proof)

    def submit(self, task: TaskEnvelope, now: int) -> Decision:
        if not isinstance(task, TaskEnvelope) or not task.valid() or not _valid_time(now):
            return self._decision("DENIED", "INVALID_ENVELOPE", "0" * 64)
        digest = task.digest()
        if not self.lab:
            return self._decision("DENIED", "PRODUCTION_UNAVAILABLE", digest)
        if self.state.stop_all or task.agent_id in self.state.stopped_agents:
            return self._decision("DENIED", "OWNER_KILL_SWITCH", digest)
        if task.expires_at <= now:
            return self._decision("DENIED", "TASK_EXPIRED", digest)
        if task.external_effects or task.spend_usd != 0:
            return self._decision("DENIED", "FREE_ONLY_NO_EXTERNAL_EFFECTS", digest)
        if task.workspace_id not in self.state.active_workspaces:
            return self._decision("DENIED", "WORKSPACE_NOT_ACTIVE", digest)
        if (task.workspace_id, task.actor_id) not in self.state.memberships:
            return self._decision("DENIED", "WORKSPACE_MEMBERSHIP_DENIED", digest)
        if (task.workspace_id, task.orchestrator_id) not in self.state.orchestrator_routes:
            return self._decision("DENIED", "FEDERATED_ROUTE_DENIED", digest)
        if (task.workspace_id, task.orchestrator_id, task.agent_id, task.capability) not in self.state.agent_scopes:
            return self._decision("DENIED", "AGENT_CAPABILITY_DENIED", digest)

        passport = self.state.passports.get(digest)
        if (
            digest in self.state.revoked_passports
            or passport is None
            or passport.trusted_verification is not True
            or passport.task_digest != digest
            or passport.workspace_id != task.workspace_id
            or passport.agent_id != task.agent_id
            or not _valid_time(passport.expires_at)
            or passport.expires_at <= now
        ):
            return self._decision("DENIED", "PASSPORT_NOT_VERIFIED", digest)
        approval = self.state.approvals.get(digest)
        if (
            approval is None
            or approval.trusted_verification is not True
            or approval.task_digest != digest
            or approval.workspace_id != task.workspace_id
            or not _valid_time(approval.expires_at)
            or approval.expires_at <= now
        ):
            return self._decision("DENIED", "APPROVAL_NOT_VERIFIED", digest)
        if digest not in self.state.guardian_releases:
            return self._decision("DENIED", "GUARDIAN_DENIED", digest)

        key = (task.workspace_id, task.idempotency_key)
        prior = self._idempotency.get(key)
        if prior is not None:
            if hmac.compare_digest(prior, digest):
                return self._decision("DUPLICATE", "NO_REEXECUTION", digest)
            return self._decision("DENIED", "IDEMPOTENCY_CONFLICT", digest)
        self._idempotency[key] = digest
        self._accepted[digest] = task
        return self._decision("AUTHORIZED_LAB_ONLY", "ALL_SIMULATED_GATES_PASSED", digest)

    def record_result(self, task: TaskEnvelope, payload: bytes, now: int) -> Decision:
        if not isinstance(task, TaskEnvelope) or not task.valid() or not _valid_time(now):
            return self._decision("DENIED", "INVALID_RESULT_ENVELOPE", "0" * 64)
        digest = task.digest()
        if not self.lab:
            return self._decision("DENIED", "PRODUCTION_UNAVAILABLE", digest)
        if digest not in self._accepted:
            return self._decision("DENIED", "UNAUTHORIZED_TASK", digest)
        if digest in self._completed:
            return self._decision("DUPLICATE", "RESULT_ALREADY_RECORDED", digest)
        if self.state.stop_all or task.agent_id in self.state.stopped_agents:
            return self._decision("DENIED", "OWNER_KILL_SWITCH", digest)
        if (
            task.workspace_id not in self.state.active_workspaces
            or (task.workspace_id, task.actor_id) not in self.state.memberships
            or (task.workspace_id, task.orchestrator_id) not in self.state.orchestrator_routes
            or (task.workspace_id, task.orchestrator_id, task.agent_id, task.capability)
            not in self.state.agent_scopes
        ):
            return self._decision("DENIED", "SCOPE_REVOKED", digest)
        if digest not in self.state.guardian_releases:
            return self._decision("DENIED", "GUARDIAN_REVOKED", digest)
        passport = self.state.passports.get(digest)
        approval = self.state.approvals.get(digest)
        if (
            task.expires_at <= now
            or digest in self.state.revoked_passports
            or passport is None
            or passport.trusted_verification is not True
            or passport.task_digest != digest
            or passport.workspace_id != task.workspace_id
            or passport.agent_id != task.agent_id
            or not _valid_time(passport.expires_at)
            or passport.expires_at <= now
            or approval is None
            or approval.trusted_verification is not True
            or approval.task_digest != digest
            or approval.workspace_id != task.workspace_id
            or not _valid_time(approval.expires_at)
            or approval.expires_at <= now
        ):
            return self._decision("DENIED", "AUTHORITY_EXPIRED_OR_REVOKED", digest)
        if not isinstance(payload, bytes):
            return self._decision("DENIED", "INVALID_RESULT_PAYLOAD", digest)
        qa = self.state.independent_qa.get(digest)
        if (
            qa is None or qa.trusted_verification is not True or qa.accepted is not True
            or qa.task_digest != digest or qa.workspace_id != task.workspace_id
            or not _valid_digest(qa.output_sha256)
            or not hmac.compare_digest(qa.output_sha256, sha256(payload))
            or not _valid_identifier(qa.reviewer_id)
            or qa.reviewer_id == task.agent_id
            or qa.reviewer_id == task.actor_id
        ):
            return self._decision("DENIED", "INDEPENDENT_QA_NOT_VERIFIED", digest)
        self._completed.add(digest)
        return self._decision("ACCEPTED_LAB_QA", "DIGEST_AND_QA_MATCH", digest)
