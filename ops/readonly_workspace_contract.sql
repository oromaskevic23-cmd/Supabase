-- IMPERIAL Core: read-only CRM-SOFFT tenant/agent authority catalog audit.
-- Metadata only. No principal UUIDs, customer rows, passports, or secrets.
-- Execute only with a permitted read-only database session.
SELECT n.nspname AS schema_name,
       c.relname AS object_name,
       c.relrowsecurity AS rls_enabled,
       c.relforcerowsecurity AS rls_forced,
       COUNT(DISTINCT p.oid) AS rls_policy_count,
       has_schema_privilege('anon', n.oid, 'USAGE') AS anon_schema_usage,
       has_schema_privilege('authenticated', n.oid, 'USAGE') AS authenticated_schema_usage,
       has_table_privilege('anon', c.oid, 'SELECT') AS anon_select,
       has_table_privilege('authenticated', c.oid, 'SELECT') AS authenticated_select,
       has_table_privilege('authenticated', c.oid, 'INSERT') AS authenticated_insert,
       has_table_privilege('authenticated', c.oid, 'UPDATE') AS authenticated_update
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_catalog.pg_policy p ON p.polrelid = c.oid
WHERE n.nspname IN ('crm_sofft','imperial_control')
  AND c.relname IN (
    'workspace_registry','workspace_memberships','agent_registry',
    'agent_workspace_access','task_registry','nca_one_internal_skill_jobs',
    'nca_worker_one_control','nca100_passport_issuance'
  )
  AND c.relkind IN ('r','p')
GROUP BY n.nspname,c.relname,c.relrowsecurity,c.relforcerowsecurity,c.oid,n.oid
ORDER BY n.nspname,c.relname;

SELECT n.nspname AS schema_name,
       c.relname AS table_name,
       a.attname AS column_name,
       pg_catalog.format_type(a.atttypid,a.atttypmod) AS column_type,
       a.attnotnull AS not_null
FROM pg_catalog.pg_attribute a
JOIN pg_catalog.pg_class c ON c.oid = a.attrelid
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname IN ('crm_sofft','imperial_control')
  AND c.relname IN (
    'workspace_registry','workspace_memberships','agent_registry',
    'agent_workspace_access','task_registry','nca_one_internal_skill_jobs',
    'nca_worker_one_control','nca100_passport_issuance'
  )
  AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY n.nspname,c.relname,a.attnum;

SELECT n.nspname AS schema_name, c.relname AS table_name,
       con.conname AS constraint_name,
       con.contype AS constraint_type,
       pg_catalog.pg_get_constraintdef(con.oid) AS constraint_definition
FROM pg_catalog.pg_constraint con
JOIN pg_catalog.pg_class c ON c.oid = con.conrelid
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'crm_sofft'
  AND c.relname IN (
    'workspace_registry','workspace_memberships','agent_registry',
    'agent_workspace_access','task_registry'
  )
  AND con.contype IN ('p','u','f')
ORDER BY c.relname, con.conname;
