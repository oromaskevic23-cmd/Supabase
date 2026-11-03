"""Offline validation of the IMPERIAL Core Supabase public Enterprise repo."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PAGES=ROOT/"site"
POLICY=json.loads((ROOT/"policies/enterprise_baseline.json").read_text())
BASE=POLICY["google_site"]
def check():
    if POLICY["owner_display_role"]!="Founder · Owner · CEO":
        raise AssertionError("Public founder titles must be Founder, Owner and CEO only")
    if POLICY["cloud_region"]["region"]!="eu-central-1":
        raise AssertionError("Cloud location mismatch")
    if POLICY["architecture"]!="Federated Multi-Orchestrator Architecture":
        raise AssertionError("Federated architecture missing")
    for relative in ("README.md","docs/ARCHITECTURE.md","docs/DIAGRAMS.md",
                     "docs/FRANKFURT.md","docs/DATABASE_DOMAINS.md",
                     "docs/SECURITY_BASELINE.md","docs/SECURITY_ADVISOR_RUNBOOK.md","docs/EVIDENCE_REGISTER.md",
                     "docs/VAL_TOWN_RECOVERY.md","docs/GOOGLE_INDEXING.md",
                     "docs/RUNBOOK.md","site/index.html",
                     "site/founder/index.html","site/frankfurt/index.html"):
        text=(ROOT/relative).read_text(encoding="utf-8")
        if re.search(r"Chief Systems Architect|System Chief|System Boss",text,re.I):
            raise AssertionError(f"Unapproved public title in {relative}")
    diagrams=(ROOT/"docs/DIAGRAMS.md").read_text()
    if diagrams.count("```mermaid")<5:
        raise AssertionError("Five architecture diagrams required")
    for file in ("index.html","founder/index.html","frankfurt/index.html"):
        text=(PAGES/file).read_text()
        expected=BASE+("" if file=="index.html" else file.replace("index.html",""))
        if f'href="{expected}"' not in text:
            raise AssertionError(f"Wrong canonical link: {file}")
        if "<title>" not in text or 'name="description"' not in text:
            raise AssertionError(f"Missing search metadata in {file}")
        if 'name="robots" content="index,follow' not in text:
            raise AssertionError(f"Page is not index-ready: {file}")
    home=(PAGES/"index.html").read_text()
    founder=(PAGES/"founder/index.html").read_text()
    if POLICY["public_corporate_symbol"] not in home or POLICY["public_corporate_symbol"] not in founder:
        raise AssertionError("Canonical GitHub symbol must be reused")
    if "Founder · Owner · CEO" not in founder:
        raise AssertionError("Public founder attribution inconsistent")
    if '"jobTitle":"Founder, Owner, CEO"' not in founder:
        raise AssertionError("Person structured data missing exact roles")
    for term in ("Founder","Owner","CEO"):
        if term not in founder: raise AssertionError(f"Founder term missing: {term}")
    sitemap=ET.parse(PAGES/"sitemap.xml").getroot()
    links={x.text for x in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    if links!={BASE,BASE+"founder/",BASE+"frankfurt/"}:
        raise AssertionError("Sitemap/canonical coverage mismatch")
    robots=(PAGES/"robots.txt").read_text()
    if f"Sitemap: {BASE}sitemap.xml" not in robots:
        raise AssertionError("Sitemap not discoverable")
    for sql_path in ("ops/readonly_inventory.sql", "ops/readonly_access_matrix.sql"):
        sql=(ROOT/sql_path).read_text()
        statements=re.sub(r"(?m)^\s*--.*$","",sql).strip().split(";")
        for part in statements:
            cleaned=part.strip()
            if cleaned and not cleaned.upper().startswith("SELECT "):
                raise AssertionError(f"Forbidden SQL: {sql_path} must be SELECT-only")
    if POLICY["production_database_writes_allowed"] is not False:
        raise AssertionError("Production writes must be denied")
    print("IMPERIAL_SUPABASE_ENTERPRISE_SOURCE_PASS: founder roles, five diagrams, Frankfurt, sitemap, SEO, source controls, SELECT-only SQL")
if __name__=="__main__": check()
