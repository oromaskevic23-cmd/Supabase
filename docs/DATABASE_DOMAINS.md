# PostgreSQL Domain Map

| Database schema | Purpose | Classification | Verification |
| --- | --- | --- | --- |
| `crm_sofft` | Workspaces, leads, jobs, NCA registry, receipts and money evidence | Private customer / commercial | Existing tables observed |
| `imperial_crm` | Conversion, task and orchestration state | Private execution | Existing tables observed |
| `imperial_control` | Governance, source registry, drift, evidence and approval state | Restricted control plane | Security review required |
| `imperial_federation` | Federated orchestration membership | Internal architecture | Current table detail not fully audited here |
| `imperial_memory` | Agent/system memory | Sensitive internal | Never copy into public pages |
| `public` | Selected API-facing objects | Only after explicit grants/RLS review | Schema name does not imply safe public access |

## Mandatory rules

A user-facing web app must not receive a service-role database key. Each private operation must bind an authenticated tenant to the row-level policy and explicit grants. `SECURITY DEFINER` routines require separate `EXECUTE` and schema-`USAGE` scrutiny.

A previously observed advisory found RLS disabled on multiple `imperial_crm` and `imperial_control` tables, while a separate privileges check found the tested anonymous/authenticated table rights absent. **Neither observation alone proves public exploitability.** Fix only after staged dependency and negative-authorization tests.

See [read-only SQL](../ops/readonly_inventory.sql).
