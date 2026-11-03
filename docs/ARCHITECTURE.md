# Enterprise Architecture — IMPERIAL Core × Supabase

**Founder · Owner · CEO:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Regional database:** Central EU (Frankfurt), `eu-central-1`.  
**Implementation:** architecture and tested components vary; no blanket operational claim.

The system has an Owner-governed command center **HANTER**, multiple **federated** orchestrators for different industries and dynamically sized **Nano Core Agent (NCA)** squads. Each execution needs a scoped AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, IntentLock, Audit Ledger and Owner Kill Switch.

| Layer | Canonical role | Boundary |
| --- | --- | --- |
| Founder / Owner / CEO | Corporate project direction and final authority | Never transferred by agent-written code |
| HANTER | Central command center and task routing | Not a universal unrestricted execution operator |
| Domain orchestrators | CRM-SOFFT, Capital Core, CONSTRUCTOR AI and more | Independent scopes, bounded permissions |
| Nano Core Agents | Skills-based work, independent LEGION QA | No self-issuing credentials or unapproved outreach |
| Supabase PostgreSQL | Private tenant/business state in Frankfurt region | RLS, SQL grants, restricted server credentials |
| Audit Ledger / ProofGraph | Evidence and state provenance | A local hash alone is not a trusted external signature |
| CYBER HAK | Defensive security controls | Public/Private Boundary and Zero Trust |
| CRYPTO IMPERIAL Ecosystem | Separate architectural crypto domain | No implicit access to customer funds |

See [diagrams](DIAGRAMS.md) and [schema matrix](DATABASE_DOMAINS.md).

### Implemented federation reference (isolated)

The repository contains an [offline dispatch policy](../scripts/federation_gate.py) with negative tests for cross-workspace NCA routing, task-specific approvals, revocation, independent QA and local audit-chain integrity. Each domain orchestrator must remain within its workspace scope and `FREE_ONLY` limits. The [live catalog inspection](TENANT_ISOLATION_REPORT_2026-11-04.md) validates selected grants and relational constraints but **does not** validate application-level tenant isolation. See [production gates](PRODUCTION_ACTIVATION_GATES.md).

### Verified limitations

Database existence, table counts and GitHub CI are not evidence of continuous 24/7 autonomous agents or settled commercial payments. Owner's actual cryptographic enrollment, a managed server worker, professional examination and verified remote stop require separately observed production evidence. No paid resource is provisioned by this repository.
