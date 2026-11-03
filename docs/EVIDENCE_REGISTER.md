# Verification Register · 3 November 2026

| Component | Evidence observed | Level | Open gate |
| --- | --- | --- | --- |
| Supabase project region | Connected project metadata reports `eu-central-1` / Central EU (Frankfurt) | Observed | No cross-provider location guarantee |
| Supabase project status | `ACTIVE_HEALTHY` at inspection | Observed point-in-time | No historical uptime claim |
| CRM-SOFFT | 11 workspace records, 21 registered NCA records | Observed counts | All records checked as not production-authorized |
| Revenue database | 0 rows in checked `payment_records` and `revenue_ledger` tables | Observed counts | This does not establish every revenue channel |
| RLS | Risks and role grants investigated | Partial security review | Independent penetration/tenant isolation |
| HANTER ↔ NCA | Lab prototypes and CI in other repos | Lab evidence | Privileged production workers unverified |
| Val Town | Historical inventories and recovery references | Historical only | Live account/project/traces inventory unavailable |
| Public Pages | Static site + workflow in this repository | Build candidate | Published URL and search crawl to be independently confirmed |
| Google Search Console | Sitemap and structured data included | Technical prerequisites | Ownership verification and Google indexing not proven |

**Evidence rules:** no PASS without an observed test. No "live" based on diagrams, no "revenue" based on leads or quotes, no agent fleet size based on database registrations. The actual company identity in Google Search must not be described as a sovereign state or legally registered corporation without independently verified legal evidence.
