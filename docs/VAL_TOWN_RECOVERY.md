# Val Town — Two-Month Recovery Investigation

**Time window:** 2026-09-03 through 2026-11-03, inclusive.  
**Account historically reviewed:** `oromaskevic23`.  
**Report class:** PUBLIC SANITIZED EXECUTIVE SUMMARY — **NOT A COMPLETE LIVE VAL TOWN ACCOUNT AUDIT**.  
**Budget:** FREE_ONLY. **No Val Town account writes or paid upgrades.**

> **Evidence boundary:** This report reconstructs historical connected-session checks and selected publicly indexed Val Town pages. **It is not a current complete account inventory or a live two-month telemetry replay.** The authenticated Val Town connector was not available to enumerate vals, inspect logs, branches or stored data as of 2026-11-03.

## What the evidence actually says

The account's **2026-09-14** connected-surface infrastructure review documented **53 vals** and identified Val Town as the historical runtime corpus for several IMPERIAL Core NCA/HANTER/ORION projects. A second historical snapshot elsewhere mentioned **52 projects**, but no matching same-date reconciled inventory establishes whether this was a different time, an exclusion or a rename. Neither number is represented as the current count.

The original `oromaskevic23/imperial-nca-31day-runtime` returned **NOT FOUND** in an **August 29 baseline recovery audit** after an accidental soft deletion. A recovery replacement `oromaskevic23/imperial-nca-runtime-recovery` existed with **100 stored agent records and 1,700 skill bindings**. The 1,700 value means **17 bindings per 100 records**, not 1,700 independently executing AI workers. Recovery was **not proof of restoration** of the deleted project's SQLite, blobs, scheduled intervals, settings or history. This August observation is baseline context, **not a fresh September–November success**.

## Dated checkpoints

| Date | Supported finding | Verification boundary |
| --- | --- | --- |
| **2026-09-03–09-09** | Val Town marketing activity was earlier reported as `READ_ONLY_RESEARCH` and `DRAFT_ONLY`; the historical `imperialcore.val.run` check did not establish a healthy website | Draft opportunities are not clients, revenue, or app uptime |
| **2026-09-14** | Archived connected account audit recorded **53 vals**, including the recovery runtime and multiple specialized domain projects | Historical count, not the current active-worker fleet |
| **2026-09-17** | Architecture direction accepted: Val Town as minimal bootstrap/transport; protected private state, credentials, evidence and control-plane state in Supabase/private backend | Architecture decision, not completed migration |
| **2026-10-03** | Earlier connected-session test reported `imperial-astra-control-plane` and a single health endpoint HTTP 200 | Point-in-time health, not full autonomous orchestration |
| **2026-10-08–09** | Account integration / MCP access failed in some sessions | ChatGPT connector error does not imply Val Town projects were deleted |
| **2026-10-11** | Owner deferred Val Town as an Astra production dependency | Avoid silent reactivation of services |
| **2026-10-26** | Connected Library forensic audit marked current Val Town inventory and traces **NOT LIVE-READABLE** | Historical report does not become a live trace |
| **2026-11-03** | Publicly indexed project pages exist, but authenticated account listing and telemetry remain unavailable in this tool session | Public existence ≠ verified running endpoints |

## Representative historical project groups

The following is **not the full 53-val list**. Names are historical and must be checked against a fresh authorized inventory:

| Domain | Val names or publicly referenced assets | Evidence status |
| --- | --- | --- |
| NCA continuity | `imperial-nca-31day-runtime`, `imperial-nca-runtime-recovery`, `imperial-universal-dev-nca` | Historical recovery / presence only |
| HANTER bridge | `hanter-bridge-node-1`, `hanter-bridge-node-2-temp`, `hanter-bridge-node-3-temp`, `ag-command-center` | Historical HTTP health shells; not independent provider failover |
| ASTRA / VELION | `imperial-astra-control-plane`, `velion-legion` | Historical/control-plane code; current LLM work not attested |
| ORION | `orion-nca-collective-24x7` | Public code indexed; last successful schedule unknown |
| Security / capabilities | `cyber-hak-defense-24x7`, `imperial-capability-hub` | Public references; recent security runtime unknown |
| Specialist units | `imperial-dicon-runtime`, `imperial-morgan-runtime`, `ashton-taily-crypto-nca` | Historical inventory names only |
| Other products | `milliarder-game`, `imperial-rfq-quote-demo`, `imperial-reputation`, `aurora-kids-media` | Selected public source pages and historical names |

Selected official public Val Town references (not logged-in or endpoint-health proof):
- [Astra control-plane](https://www.val.town/x/oromaskevic23/imperial-astra-control-plane)
- [AG Command Center](https://www.val.town/x/oromaskevic23/ag-command-center)
- [ORION public source](https://www.val.town/x/oromaskevic23/orion-nca-collective-24x7/code/crypto-market-access-cycle.ts)
- [CYBER HAK branch index](https://www.val.town/x/oromaskevic23/cyber-hak-defense-24x7/branches)
- [MILLIARDER GAME source](https://www.val.town/x/oromaskevic23/milliarder-game)
- [Val Town package directory identifying the capability hub](https://www.val.town/examples/packages/%40modelcontextprotocol%2Fserver)

## Forensic gaps that block Enterprise claims

A full authenticated account audit must check every val's **code privacy and HTTP access privacy independently**, branch/commit history, file types, HTTP endpoint routes and safe HEAD/GET status, intervals and latest trace successes/failures, bounded logs, SQLite/table row counts, blob keys, secret **key names only**, attached env groups, cost/tier limits, and actual timestamps. A public page or a configured 15-minute interval alone cannot prove repeated runs.

**Special P0 incident:** Recover the original `imperial-nca-31day-runtime` via its existing account/support process; do not recreate its slug and call that a restoration. Preserve original history, blobs, DB, intervals and endpoint binding if still recoverable. The related recovery replacement must remain distinguishable.

## Federation and data ownership

`Architect → HANTER Command Center → federated Multi-Orchestrator Architecture → scoped Nano Core Agents`.

**Supabase Frankfurt / `eu-central-1`** is an independently verified database project region. It is **not** proof of Val Town server location in Frankfurt. Treat Val Town as **a separate provider**, and do not claim failover diversity by counting multiple Val Town vals as multiple clouds.

Sensitive keys, CRM-SOFFT clients, real payment evidence, AI Passport trust, Guardian Core authorization and Audit Ledger controls remain on the protected **Private Boundary**. A future Val Town worker must obtain scoped signed authorization via Approval Gateway and respect Owner Kill Switch. CRYPTO IMPERIAL Ecosystem Boundary remains separate; no automatic conversion of customer revenue into tokens.

## Recovery acceptance criteria

1. Authorized, paginated **complete account inventory** with UTC timestamps, total count and immutable response digest.
2. Preserved original recovery case and clear official resolution status of soft-deleted runtime.
3. Per-val exact code/HTTP privacy and security permission audit.
4. Per-endpoint authenticated/anonymous boundary verification and complete recent trace history — without causing external side effects.
5. Cross-provider confirmation of HANTER, Supabase CRM-SOFFT, a single real NCA task, independent QA and Owner STOP.
6. An approved **FREE_ONLY** minimal-runtime migration with staged cutover/rollback proof.

**Current result:** partial two-month forensic reconstruction and public-source cross-check are complete; **live authenticated Val Town account audit is BLOCKED**, and neither a restored lost project nor fully operational 24/7 NCA fleet is claimed.

The detailed operational chronology, incident decision matrix and internal recovery order belong in the **private IMPERIAL Core governance repository**, not public source-control pages.

**Architecture Before Implementation → Evidence Before Production Authority.**
