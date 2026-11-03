# Production Activation Gates — HANTER, CRM-SOFFT and NCA

**Default state:** \`DENY / LAB_ONLY / FREE_ONLY\`. No production worker launches, paid platform outreach or commercial monetary actions are authorized by this repository.

| Gate | Required proof | Status |
| --- | --- | --- |
| G0 — Owner trust | Real Ed25519 Owner enrollment, key custody, rotation/revocation and signing proof | **OPEN** |
| G1 — Server trust boundary | Authenticated private API, bound principals, restricted secrets, independent approval verification | **OPEN** |
| G2 — Workspace isolation | Tenant A/B negative tests against real application/API and intended database roles, scoped grants | **OPEN** |
| G3 — AI Passport | Signature verification, exact task/agent/workspace hash, lease/replay protection | **OPEN** |
| G4 — Guardian + Approval | Fresh policy decision, separate Approval Gateway and Owner Kill Switch enforcement | **OPEN** |
| G5 — Durable execution | Atomic \`workspace_id\` + idempotency claim, persisted ledger, restart/retry/lease tests | **OPEN** |
| G6 — Independent QA | Sandbox task, distinct reviewer, artifact digest and independently reproduced result | **OPEN** |
| G7 — Security remediation | Review \`public.imperial_commercial_draft_intake\`, re-run Supabase Advisors and approve change | **OPEN** |
| G8 — Controlled release | Signed release/rollback manifest, backups/restore proof and real stop evidence | **OPEN** |

**What is actually implemented:** the [lab dispatch contract](../scripts/federation_gate.py), unit tests, README/documentation, metadata-only inspection and CI. The code gates simulated decisions but contains **no cryptographic verifier, no persistent production queue, no database write adapter, no live LLM/NCA executor and no externally anchored ledger**.

### Authorization before deployment

The Founder/Owner approves a narrowly scoped implementation proposal, but this is not equivalent to an enrolled cryptographic key or proof of a production launch. Approval Gateway must reject fabricated signatures and expired/foreign/scoped-out permits even if the task was requested by a privileged user.

### Rollback / response

If a gate fails: disable new claims, block further side effects, revoke affected permits, preserve sanitized evidence, and restore from reviewed infrastructure state. Do not claim a true remote stop until runtime termination and restart-denial are demonstrated. No automatic migrations or service configuration updates are permitted by this public repository.
