-- IMPERIAL Core | metadata-only PostgreSQL inventory.
-- REVIEW before running, under a privately authorized read-only role.
-- SELECT statements only; no client, payment or secret values.
SELECT current_database() AS database_name, current_user AS current_role,
       current_setting('transaction_read_only', true) AS transaction_read_only;
SELECT n.nspname AS schema_name,
       COUNT(*) FILTER (WHERE c.relkind IN ('r','p')) AS table_count,
       COUNT(*) FILTER (WHERE c.relkind IN ('r','p') AND NOT c.relrowsecurity) AS tables_without_rls
FROM pg_catalog.pg_namespace n
LEFT JOIN pg_catalog.pg_class c ON c.relnamespace=n.oid
WHERE n.nspname IN ('crm_sofft','imperial_crm','imperial_control','imperial_federation','imperial_memory','public')
GROUP BY n.nspname ORDER BY n.nspname;
SELECT n.nspname AS schema_name, c.relname AS table_name,
       c.relrowsecurity AS rls_enabled,
       has_table_privilege('anon', c.oid, 'SELECT') AS anon_select,
       has_table_privilege('authenticated', c.oid, 'SELECT') AS authenticated_select
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
WHERE c.relkind IN ('r','p')
  AND n.nspname IN ('crm_sofft','imperial_crm','imperial_control')
ORDER BY n.nspname,c.relname;
