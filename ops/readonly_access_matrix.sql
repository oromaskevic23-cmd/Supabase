-- IMPERIAL Core / Supabase: metadata-only permission and RLS inventory.
-- Run manually as an authorized database operator in a read-only transaction.
-- These queries NEVER read user rows, issue grants, or change policy.
-- Verify exposed schemas in Supabase Data API settings; public is not always the only one.
-- In a public report, publish only reviewed counts and redacted findings.

SELECT n.nspname AS schema_name,
       c.relname AS object_name,
       c.relkind AS object_kind,
       c.relrowsecurity AS rls_enabled,
       c.relforcerowsecurity AS rls_forced,
       CASE WHEN c.relkind = 'v'
         THEN COALESCE('security_invoker=true' = ANY(c.reloptions), FALSE)
         ELSE NULL END AS view_security_invoker,
       has_schema_privilege('anon', n.oid, 'USAGE') AS anon_schema_usage,
       has_schema_privilege('authenticated', n.oid, 'USAGE') AS authenticated_schema_usage,
       has_table_privilege('anon', c.oid, 'SELECT') AS anon_select,
       has_table_privilege('authenticated', c.oid, 'SELECT') AS authenticated_select,
       has_table_privilege('anon', c.oid, 'INSERT') AS anon_insert,
       has_table_privilege('authenticated', c.oid, 'INSERT') AS authenticated_insert,
       has_table_privilege('anon', c.oid, 'UPDATE') AS anon_update,
       has_table_privilege('authenticated', c.oid, 'UPDATE') AS authenticated_update,
       has_table_privilege('anon', c.oid, 'DELETE') AS anon_delete,
       has_table_privilege('authenticated', c.oid, 'DELETE') AS authenticated_delete
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','p','v')
  AND n.nspname IN ('public','crm_sofft','imperial_crm','imperial_control',
                   'imperial_federation','imperial_memory','imperial_astra6')
ORDER BY n.nspname, c.relname;

SELECT n.nspname AS schema_name,
       p.proname AS function_name,
       pg_catalog.pg_get_function_identity_arguments(p.oid) AS argument_types,
       p.prosecdef AS security_definer,
       has_function_privilege('anon', p.oid, 'EXECUTE') AS anon_can_execute,
       has_function_privilege('authenticated', p.oid, 'EXECUTE') AS authenticated_can_execute
FROM pg_catalog.pg_proc p
JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace
WHERE p.prokind = 'f'
  AND p.prosecdef
  AND n.nspname IN ('public','crm_sofft','imperial_crm','imperial_control',
                   'imperial_federation','imperial_memory','imperial_astra6')
ORDER BY n.nspname, p.proname;
