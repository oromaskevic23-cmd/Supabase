# Security Baseline — Zero Trust, RLS, Owner Authority

## Identity and authorization

- Protect Owner root identity. Never allow NCA code, SQL update or untrusted prompt to grant itself Founder/Owner/CEO authority.
- Require out-of-band enrollment of real Owner cryptographic trust before production permission changes. Demonstration keys are not Owner keys.
- Authenticate and authorize every tenant/business request. Validate workspace membership at the trusted service boundary and in database policy.
- Scope AI Passport and Enterprise Skills to the exact task; Guardian Core + Approval Gateway are mandatory before sensitive actions.
- Maintain a tested Owner Kill Switch with actual worker termination evidence before claiming remote stop capability.

## PostgreSQL hardening

- Read-only diagnostic queries before migrations; snapshot dependencies, grants, functions, policies and exposed schemas.
- Explicit `GRANT`/`REVOKE`; avoid global `USING (true)` RLS policies for customer or control-plane data.
- Test non-admin `anon`, `authenticated`, tenant A, tenant B and controlled service identity independently.
- Review `SECURITY DEFINER` search_path, privileges, invoker/definer behavior and schema usage.
- Execute schema changes only after nonproduction tests, reliable rollback, Owner authorization and observability.
- Keep connection strings, JWT signing keys and service-role keys in approved private storage; never in README, browser JavaScript or GitHub Pages.

## Money boundary

CRM quote ≠ invoice ≠ signed payment receipt ≠ `PAYMENT_CONFIRMED`. Settlement requires external provider evidence, beneficiary/account match, immutable audit references, reversal handling and independent review. CRYPTO IMPERIAL Ecosystem Boundary is always separate.

## CI rule

This repository's CI can prove documentation consistency and offline code checks; it cannot certify a production Supabase project, external provider or live NCA worker. See [evidence register](EVIDENCE_REGISTER.md).
