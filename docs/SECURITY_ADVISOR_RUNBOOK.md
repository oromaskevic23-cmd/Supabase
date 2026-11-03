# Supabase Advisor Evidence and Release Gates

**Scope:** IMPERIAL Core Supabase database project in Central EU (Frankfurt), `eu-central-1`. This is a security review procedure, **not** a declaration that production is secure. No automatic production DDL is authorized by this repository.

## Observed snapshot — 3 November 2026, 20:58 UTC

The connected Supabase Advisor returned four finding types. See the machine-readable **sanitized** [snapshot](advisor-baseline-2026-11-03.json) (counts only; no customer data, raw function bodies, credentials, or rows).

| Advisor finding | Count | Provider severity | Engineering interpretation |
| --- | ---: | --- | --- |
| `rls_enabled_no_policy` | 68 | INFO | Often deliberate deny-all. Inspect actual access requirements; do not add open policies to eliminate the alert. |
| `authenticated_security_definer_function_executable` | 1 | WARN | Requires a priority privilege/code review before production authorization. |
| `unindexed_foreign_keys` | 52 | INFO | Potential workload-dependent performance degradation; measure first. |
| `unused_index` | 27 | INFO | Not a safe basis for immediate removal; inspect workloads and observation window. |

The warned function is `public.imperial_commercial_draft_intake(p_issue_number bigint, p_receipt_sha256 text)`. An `authenticated` user can execute it under the current privilege model according to the advisor. **This is a risk signal, not evidence of exploitation.** The function should be reviewed privately for authorization checks, business-logic abuse, effective search path, identity-to-workspace binding, input validation, abuse limits and transactional behavior. Avoid publishing its body or customer-specific findings.

## Implementation delivered in this repository

- [Read-only access inventory](../ops/readonly_access_matrix.sql): catalog metadata for RLS flags, table grants, `security_invoker` views and callable `SECURITY DEFINER` functions. It does not read private records or modify a role.
- [Advisor gate](../scripts/advisor_gate.py): offline parser for a **manually sanitized** JSON snapshot; rejects unknown fields, invalid types and ambiguous time zones. No credentials or network connection.
- [Independent unit tests](../tests/test_advisor_gate.py): demonstrate that the current security WARN produces `BLOCK`, information findings produce `REVIEW`, and malformed inputs fail closed.

Run locally with Python 3.11+:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_repo.py
python3 scripts/advisor_gate.py docs/advisor-baseline-2026-11-03.json
```

**Expected gate exit code: 2 (BLOCK)** for the historical snapshot. Exit 0 means only that no blocking **reported** findings were present in the supplied offline input; it is never a production-security certificate. Invalid input exits 3. CI checks the expected rejection in a unit test and must not overwrite this known open issue as PASS.

## Controlled remediation sequence

1. Reconfirm the actual **Data API exposed schemas** in the project dashboard; distinguish schema `USAGE`, object grants, RLS and policies. Note that newer projects do not automatically expose new tables via grants; verify the project's actual settings.
2. Privately review the warned commercial RPC, its callers, dependencies, privilege escalation surface and workspace/Owner authorization. Revoke client execution **only after** a dependency review, nonproduction regression tests and an approved rollback plan. Do not change it blindly to `SECURITY INVOKER`.
3. For each of the 68 policy-less tables, classify `DENY_ALL_INTENTIONAL`, `SERVER_ONLY` or `CLIENT_ACCESS_REQUIRED`. For required client access, use explicit grants and least-privilege, tenant-isolated RLS conditions. Never solve this with a global `USING (true)` policy.
4. Independently test `anon`, `authenticated` (including anonymous sign-in cases), two separate workspace identities and the privileged server identity. Test SELECT/INSERT/UPDATE/DELETE and both row visibility and ownership reassignment; record only sanitized evidence.
5. Review all 52 FK index notices with representative `EXPLAIN (ANALYZE, BUFFERS)` on **nonproduction test data**, existing index definitions and realistic workload. Do not bulk-create indexes. Preserve the 27 unused indexes until history and query patterns justify a safe plan.
6. For a change, require explicit Owner authorization, scoped migration, recoverable backup, rollback, independent QA, Audit Ledger reference and evidence of successful post-change advisor recheck. Keep ZERO TRUST, FREE_ONLY and Public/Private Boundary intact.

## Provenance and freshness

The snapshot is a point-in-time observation, **not** a live monitor, active regression probe or proof that the alerted objects are exploitable. Refresh through the authenticated Supabase Advisors before any actual release decision; record observation time and publish only sanitized counts. The current repository cannot issue AI Passports or replace the Approval Gateway.

## Authoritative Supabase references

- [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Securing your Data API](https://supabase.com/docs/guides/api/securing-your-api)
- [Database Linter: callable security-definer function](https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable)
- [Database Linter: RLS without a policy](https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy)
- [2026 Data API grants change](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically)
