# Verification Register · 4 November 2026

| Component | Evidence observed | Level | Open gate |
| --- | --- | --- | --- |
| Supabase project region | Connected project metadata reports `eu-central-1` / Central EU (Frankfurt) | Observed | No cross-provider location guarantee |
| Supabase project status | `ACTIVE_HEALTHY` at inspection | Observed point-in-time | No historical uptime claim |
| CRM-SOFFT | 11 workspace records, 21 registered NCA records | Observed counts | All records checked as not production-authorized |
| Revenue database | 0 rows in checked `payment_records` and `revenue_ledger` tables | Observed counts | This does not establish every revenue channel |
| RLS | Risks and role grants investigated | Partial security review | Independent penetration/tenant isolation |
| Supabase Advisor (2026-11-03, 20:58 UTC) | 68 policy-less RLS tables (INFO), 1 authenticated-executable security-definer function (WARN), 52 unindexed FKs, 27 unused indexes | Observed metadata; historical snapshot | Review the warned function privately and verify authorization; no production fix applied |
| Offline Advisor gate | Source, sample snapshot and unit tests committed to this repository | Tested by CI; snapshot reports BLOCK | Does not imply production security or automatically repair the database |
| CRM-SOFFT/Control direct-role exposure | Eight checked tables: RLS on, zero policies, no anon/authenticated schema USAGE or direct SELECT | Observed live catalog metadata, 2026-11-04 Kyiv | Tenant A/B API and privileged server-role behavior not verified |
| Workspace keys and dedupe | Composite task PK/unique workspace idempotency, memberships, agent-workspace permission PK, opportunity workspace FK | Observed live catalog constraints | Worker dispatch must check workspace scope beyond global agent FK |
| Offline federated dispatch | Source and negative tests for HANTER route, workspace, passport/approval fixture, Guardian, Kill Switch, idempotency, QA, hash chain | Local reference logic verified by CI | No owner Ed25519 trust, production worker, persistent audit or cryptographic QA evidence |
| HANTER ↔ NCA | Lab prototypes and CI in other repos | Lab evidence | Privileged production workers unverified |
| Val Town | Historical inventories and recovery references | Historical only | Live account/project/traces inventory unavailable |
| Public Pages | Static site + workflow in this repository | Build candidate | Published URL and search crawl to be independently confirmed |
| Google Search Console | Sitemap and structured data included | Technical prerequisites | Ownership verification and Google indexing not proven |

**Evidence rules:** no PASS without an observed test. No "live" based on diagrams, no "revenue" based on leads or quotes, no agent fleet size based on database registrations. The actual company identity in Google Search must not be described as a sovereign state or legally registered corporation without independently verified legal evidence.
