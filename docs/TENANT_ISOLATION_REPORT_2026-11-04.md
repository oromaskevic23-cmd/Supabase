# CRM-SOFFT / NCA Multi-Tenant Isolation — Catalog Inspection

**Inspection window:** 4 November 2026 (Europe/Kyiv).  
**Project:** connected Supabase project, region \`eu-central-1\`.  
**Method:** authorized read-only SQL over \`information_schema\` and \`pg_catalog\`; no tenant rows, private credentials, JWTs, API calls, worker invocations or production writes.

## Observed direct-role boundary

For the eight tables below, the live catalog reports \`relrowsecurity = true\`, **0 RLS policies**, **no \`anon\` or \`authenticated\` schema USAGE**, and **no direct SELECT privileges** for either role. The checked \`authenticated\` INSERT privilege was also false. The observation concerns these SQL objects and roles, not every endpoint or server credential.

| Schema | Table | RLS | Policies | Direct anon/auth access |
| --- | --- | --- | ---: | --- |
| \`crm_sofft\` | \`workspace_registry\` | enabled | 0 | denied |
| \`crm_sofft\` | \`workspace_memberships\` | enabled | 0 | denied |
| \`crm_sofft\` | \`agent_registry\` | enabled | 0 | denied |
| \`crm_sofft\` | \`agent_workspace_access\` | enabled | 0 | denied |
| \`crm_sofft\` | \`task_registry\` | enabled | 0 | denied |
| \`imperial_control\` | \`nca100_passport_issuance\` | enabled | 0 | denied |
| \`imperial_control\` | \`nca_one_internal_skill_jobs\` | enabled | 0 | denied |
| \`imperial_control\` | \`nca_worker_one_control\` | enabled | 0 | denied |

**Interpretation:** This is a credible direct-table deny-all boundary for the checked roles. It does **not** prove tenant isolation for privileged database roles, server-side services, grant tables, \`SECURITY DEFINER\` functions, indirect views, external tools or Data API configurations.

## Existing relational constraints (verified metadata)

- \`workspace_registry\`: primary key \`workspace_id\`.
- \`workspace_memberships\`: composite primary key \`(workspace_id, principal_id)\`, workspace foreign key.
- \`agent_workspace_access\`: composite primary key \`(workspace_id, agent_id, permission)\`, separate foreign keys to agent and workspace registries.
- \`task_registry\`: primary key \`(workspace_id, task_id)\`, unique \`(workspace_id, idempotency_key)\`, foreign key to workspace registry, composite \`(workspace_id, opportunity_id)\` foreign key to the matching opportunity.
- \`task_registry.executor\` and \`reviewer\` reference the agent registry only; foreign key presence is **not** a proof of role approval, professional qualification or workspace authority.

## Deployment implications

1. Do not add blanket \`USING (true)\` RLS policies or grants to clear an informational linter warning. Deny-all may be intentional.
2. If browser/Data API access is eventually required, create a reviewed, minimal API contract with membership and workspace predicates, explicit grants, fresh identity checks, two-tenant negative tests and rollback.
3. First review the separate Supabase Advisor warning about \`public.imperial_commercial_draft_intake\` being callable by \`authenticated\`. The global access picture cannot be called secure while that privileged RPC remains unreviewed.
4. Never seed real customers or owner passports into test fixtures. Simulate **tenant A vs tenant B** with synthetic identities and negative assertions.
5. Test server-role access independently. Database grants + RLS do not by themselves prove the server application respects organization boundaries.
6. Preserve the Public/Private Boundary, Guardian Core, Approval Gateway, Audit Ledger and Owner Kill Switch.

Run the auditable [metadata-only queries](../ops/readonly_workspace_contract.sql) with a permitted read-only database role. The [offline dispatch tests](../tests/test_federation_gate.py) are a separate, deterministic policy demonstration and do not hit the live database.

## Relevant Supabase platform change

Supabase announced that the default for newly created public-schema objects requires **explicit Data API grants**, enforced for existing projects on **30 October 2026**. Existing object grants remain unchanged. This does not automatically make custom CRM-SOFFT schemas client-accessible.

Source: [Supabase — Data API auto-exposure breaking change](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically).

## Open verification gates

Real two-tenant sessions, server-role queries, RPC authorization review, production signature trust, durable idempotency and isolated worker termination **have not yet been demonstrated**. Record execution logs, code SHA, exact test environment and independently reviewed evidence before upgrading these statuses.
