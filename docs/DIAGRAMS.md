# Enterprise System Diagrams

**All diagrams depict a target architecture or logical control flow, not verified live connections.** Database region: Central EU (Frankfurt).

## 1. Federated HANTER control topology

```mermaid
flowchart TB
  O["Founder / Owner / CEO"] --> H["HANTER"]
  H --> O1["CRM-SOFFT Orchestrator"]
  H --> O2["Capital Core Orchestrator"]
  H --> O3["CONSTRUCTOR AI Orchestrator"]
  O1 --> G["Guardian Core / Approval Gateway"]
  O2 --> G
  O3 --> G
  G --> N["NCA with AI Passport"]
  N --> PG[("Supabase PostgreSQL")]
  PG --> A["Audit Ledger"]
```

## 2. Frankfurt infrastructure with external provider boundary

```mermaid
flowchart LR
  U["Authenticated Customers"] --> App["Application Runtime · Region Unverified"]
  App --> DB[("Supabase PostgreSQL\nFrankfurt eu-central-1")]
  App -. "Historical, live status unverified" .-> V["Val Town"]
  App -. "Independent provider" .-> N["Netlify / Render"]
  DB --> S["CRM / Control / Evidence Schemas"]
```

## 3. CRM-SOFFT lead-to-payment assurance

```mermaid
flowchart TD
  L["Permissioned Lead"] --> C{"Mandate Verified?"}
  C -->|No| Research["Research / Manual Qualification"]
  C -->|Yes| H["HANTER Scope Approval"]
  H --> F["Federated Domain Orchestrator"]
  F --> G{"Guardian + AI Passport + Approval?"}
  G -->|No| Deny["Deny and Audit"]
  G -->|Yes| N["Scoped NCA Task"]
  N --> QA["Independent LEGION QA"]
  QA --> Client{"Customer Acceptance?"}
  Client -->|No| Rework["Rework"]
  Client -->|Yes| Payment{"Provider Settlement Verified?"}
  Payment -->|No| Pending["Pending Reconciliation"]
  Payment -->|Yes| Confirm["PAYMENT_CONFIRMED with Proof"]
```

## 4. Zero Trust / database separation

```mermaid
flowchart TB
  Browser["Untrusted Browser"] --> API["Authenticated Private API"]
  API --> Tenant["Workspace / Tenant Validation"]
  Tenant --> RLS["RLS + Exact Grants"]
  RLS --> CRM[("crm_sofft")]
  RLS --> Jobs[("imperial_crm")]
  Guard["Guardian + Approval"] --> Control[("imperial_control")]
  Control --> Audit["Audit Ledger"]
  Public["Public GitHub / Pages"] -. "NO SECRETS" .-> CRM
  Crypto["CRYPTO IMPERIAL Boundary"] -. "Separate" .- CRM
```

## 5. Change, rollback and evidence

```mermaid
flowchart LR
  ADR["Architecture Decision"] --> Test["Isolated Migration Tests"]
  Test --> Security{"RLS / Tenancy / Secret Review"}
  Security -->|Fail| Block["Block / Correct"]
  Security -->|Pass| Owner{"Authorized Approval"}
  Owner -->|No| Hold["Hold"]
  Owner -->|Yes| Release["Controlled Release"]
  Release --> Observe["Health + Audit Evidence"]
  Observe --> Incident{"Incident?"}
  Incident -->|Yes| Stop["Stop / Revoke / Rollback"]
  Incident -->|No| Observe
```

Every privileged permission and production release requires verifiable authorization. Diagrams alone are not execution evidence.
