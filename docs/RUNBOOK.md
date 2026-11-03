# Operations and Controlled Release Runbook

## Before applying migrations

The current Supabase Advisor snapshot contains a **security WARN**, so the [offline release gate](SECURITY_ADVISOR_RUNBOOK.md) reports `BLOCK`. Re-run the live Advisors and review affected objects under Owner authority before any release; a passing source CI job is not an approval to deploy.

1. Confirm **specific** Supabase project and Frankfurt region; select isolated environment.
2. Obtain authorized Owner approval; freeze scope and record a rollback path.
3. Export metadata-only schema, permissions and dependencies via [safe SQL](../ops/readonly_inventory.sql).
4. Test RLS grants for anonymous, authenticated, intended tenant and another tenant using isolated data; review any SECURITY DEFINER functions.
5. Validate backup **restore**, not just backup metadata. No claimed RPO/RTO until measured.
6. Execute minimal migration with independent validation and transactional rollback plan.
7. Re-check frontend, private server, HANTER, CRM-SOFFT, Audit Ledger and paid-service/billing constraints. Maintain FREE_ONLY.

## Incident response

Deny new privileged jobs, revoke affected credentials, stop scoped workers and preserve sanitized evidence. **Do not claim remote shutdown** unless logs prove worker termination. Restore only after approved incident review and independent checks.

## Forbidden assumptions

No direct production updates in this repository; no client secrets in CI; no fabricated payment confirmation; no assumption that all servers physically operate in Frankfurt.
