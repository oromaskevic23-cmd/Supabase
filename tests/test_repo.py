"""No-network, independent source and schema checks; not production penetration tests."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from scripts.validate_repo import ROOT, POLICY, check

class EnterpriseRepoTests(unittest.TestCase):
    def test_source_passes(self): check()
    def test_founder_roles_are_only_three(self):
        self.assertEqual(POLICY["owner_display_role"],"Founder · Owner · CEO")
        page=(ROOT/"site/founder/index.html").read_text()
        self.assertNotIn("Chief Systems Architect",page)
        self.assertNotIn("System Chief",page)
    def test_region_is_supabase_only(self):
        self.assertEqual(POLICY["cloud_region"]["scope"],"DATABASE_PROJECT_REGION_ONLY")
    def test_no_production_writes_enabled(self):
        self.assertFalse(POLICY["production_database_writes_allowed"])
    def test_no_claim_of_google_indexing(self):
        self.assertIn("not been confirmed", (ROOT/"docs/GOOGLE_INDEXING.md").read_text())
    def test_five_mermaid_diagrams(self):
        self.assertGreaterEqual((ROOT/"docs/DIAGRAMS.md").read_text().count("```mermaid"),5)
    def test_founder_links_to_real_github(self):
        page=(ROOT/"site/founder/index.html").read_text()
        self.assertIn("https://github.com/oromaskevic23-cmd",page)
    def test_sitemap_has_three_public_pages(self):
        tree=ET.parse(ROOT/"site/sitemap.xml")
        self.assertEqual(len(tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")),3)
    def test_private_user_data_not_indexed(self):
        page=(ROOT/"site/founder/index.html").read_text().lower()
        for key in ("passport number","date of birth:","home address:","private key:"):
            self.assertNotIn(key,page)
    def test_approval_boundary_required(self):
        for requirement in ("AI Passport","Guardian Core","Approval Gateway","Audit Ledger","Owner Kill Switch"):
            self.assertIn(requirement,POLICY["enterprise_controls"])
    def test_public_symbol_reused(self):
        self.assertIn("imperial-core-emblem.webp",POLICY["public_corporate_symbol"])
    def test_val_town_marked_unverified(self):
        self.assertIn("NOT A COMPLETE LIVE VAL TOWN ACCOUNT AUDIT",(ROOT/"docs/VAL_TOWN_RECOVERY.md").read_text())
if __name__=="__main__": unittest.main()
