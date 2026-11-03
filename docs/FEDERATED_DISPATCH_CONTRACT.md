# HANTER → Federated Orchestrators → Nano Core Agents
## Secure Dispatch Contract (Offline Reference)

**Authority:** Alexander Nikolaevich Romaskevich — Founder · Owner · CEO.
**Public repository role:** documentation + isolated reference validation.
**Production status:** **BLOCKED / NOT CONNECTED**. This repo has no deployed worker, real Owner Ed25519 trust enrollment, persistent private credential store, production Approval Gateway or durable Audit Ledger integration.

The executable [federation gate](../scripts/federation_gate.py) is a no-network Python reference that makes authorization decisions over **separately supplied lab fixtures**. Calling a fixture "trusted" or setting \`trusted_verification=True\` cannot establish a real signature, cryptographic Owner identity, or production approval. The default constructor **denies all production dispatch**.

### Canonical routing

\`\`\`mermaid
flowchart LR
  O["Architect / Owner authority"] --> H["HANTER: command intake"]
  H --> F["Federated domain orchestrator"]
  F --> A["AI Passport + Enterprise Skills"]
  A --> G["Guardian Core + Approval Gateway"]
  G --> N["Scoped Nano Core Agent"]
  N --> Q["Independent LEGION QA"]
  Q --> L["Audit Ledger + ProofGraph"]
  L --> P["Private PostgreSQL boundary"]
\`\`\`

There is **no universal unrestricted execution orchestrator**. CRM-SOFFT, Capital Core and CONSTRUCTOR AI orchestrators maintain separate organizational/workspace scopes. The CRYPTO IMPERIAL Ecosystem Boundary has no implicit execution privileges.

### Authorization contract and threat model

| Boundary | Denial condition | Verification required in a future production adapter |
| --- | --- | --- |
| HANTER task | Malformed envelope, expired deadline, unapproved command center | Canonical input hash / IntentLock from a trusted intake service |
| Workspace | Missing/deactivated workspace or membership | Fresh server-side membership lookup; never trust client-supplied role text |
| Federation | Orchestrator or NCA lacks the exact workspace and capability grant | Scoped database grants with transactional authorization checks |
| AI Passport | Missing, expired, revoked, wrong task/workspace/agent or unverified | Real Ed25519 signature + trusted Owner key registry, replay/nonce check and revocation |
| Guardian Core | No current release or Kill Switch active | Out-of-band policy decision and enforceable worker stop |
| Approval Gateway | No verified approval bound to the task digest, expiry or workspace | Independent signed approval/Owner grant with exact action and financial limits |
| Idempotency | Duplicate key or same key with different intent | Durable unique constraint + atomic insert/claim per workspace |
| NCA execution | External side effects or nonzero spending in FREE_ONLY mode | Capability sandbox, egress restrictions, cost guard and cancellation |
| Independent QA | Missing QA, self-review, wrong output digest or untrusted evidence | Separate reviewer principal and independently checked execution artifact |
| Audit Ledger | Missing event, unverified chain, inaccessible evidence | Append-only protected ledger, externally anchored/cryptographically signed checkpoints |

The lab uses SHA-256 of a canonical JSON task envelope and output bytes, scoped idempotency to \`(workspace_id, key)\`, checks eligibility **again** when a result is proposed, and records minimal decision codes without customer data.

The lab audit is an **in-memory tamper-evident hash chain**, not immutable storage or cryptographically signed evidence. It is lost on process restart. The lab's allow decision means only \`AUTHORIZED_LAB_ONLY\`: no real task is executed.

### Integration facts from the connected database (catalog only)

The existing \`crm_sofft.task_registry\` has a primary key on \`(workspace_id, task_id)\` and a unique constraint on \`(workspace_id, idempotency_key)\`. It also has a composite foreign key from \`(workspace_id, opportunity_id)\` to the matching workspace-scoped opportunity. \`workspace_memberships\` has primary key \`(workspace_id, principal_id)\`. \`agent_workspace_access\` has primary key \`(workspace_id, agent_id, permission)\`.

These are valuable **schema guardrails**, not proof that every query/API endpoint isolates tenants. In particular, the \`task_registry.executor\` foreign key points to the global agent registry, so the **workspace access check is an additional requirement**; a matching agent ID alone cannot authorize an execution.

The reviewed tables currently deny the \`anon\` and \`authenticated\` roles direct access. **Do not grant those roles access just to make a test pass.** For the full metadata observation see [tenant isolation inspection](TENANT_ISOLATION_REPORT_2026-11-04.md).

### Reproduce offline

\`\`\`bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_repo.py
\`\`\`

No \`.env\`, JWT, Supabase URL, service-role key, Owner private key, internet access, migrations, external payments or database writes are needed.

### Production acceptance is separate

Before any live worker may receive a commercial task:
1. Enroll the real Owner cryptographic verification trust chain outside GitHub; prove key custody/revocation and approval authority.
2. Verify AI Passport and signed Approval Gateway evidence using a trusted isolated service, with a real private/server-only credential boundary.
3. Enforce fresh workspace membership, agent scope, role and organization authorization at database and application layers.
4. Implement durable exactly-once **claim semantics**, unique constraints, retry/lease behavior and recoverable audit persistence in a private transaction.
5. Enforce Kill Switch at process/container level and demonstrate termination logs.
6. Execute a nonproduction, sandboxed NCA task with isolated model/runtime, bounded external effects (initially zero), output artifact and independent QA.
7. Pass two-tenant negative tests and security reviews of all exposed RPC and \`SECURITY DEFINER\` functions.
8. Obtain explicit Owner release authorization with rollback and incident runbook. Attach genuine evidence to ProofGraph.

**Lab CI success is not permission to bypass these barriers.** Read [release gates](PRODUCTION_ACTIVATION_GATES.md), [security baseline](SECURITY_BASELINE.md) and [evidence register](EVIDENCE_REGISTER.md).
