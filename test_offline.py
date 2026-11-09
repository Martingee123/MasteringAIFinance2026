"""Check real saved reports against independently saved facts, without API calls."""
import unittest
from common import ROOT,read
from offline_audit import audit_core

class OfflineEvidenceTests(unittest.TestCase):
    def test_clean_and_corrupted_real_reports(self):
        manifest=read(ROOT/'proof-manifest.json')
        for label in ('clean','seeded-eps'):
            _,marks,_=audit_core(ROOT/manifest['trials'][label])
            self.assertEqual(len(marks),11)
            eps=next(m for m in marks if m['core_claim']==5)
            self.assertEqual(eps['expected'],[manifest['known_answers']['annual_eps']])
            self.assertEqual(eps['code_mark'],'wrong' if label=='seeded-eps' else 'code correct')
            if label=='clean':self.assertTrue(all(m['code_mark']=='code correct' for m in marks))
    def test_eps_footnote_is_not_a_value(self):
        from offline_audit import statement_pair
        text='Diluted Net Income Per Share\n1\n$\n0.93\n$\n0.86'
        self.assertEqual(statement_pair(text,r'Diluted Net Income Per Share',decimal_only=True),[0.93,0.86])

    def test_growth_trial_checks_actual_operands(self):
        results=read(ROOT/'offline-proof-results.json')['results']
        self.assertGreaterEqual(results['invented-growth']['marks']['wrong'],1)
    def test_source_import_prices_preserved_as_assumptions(self):
        imports=list((ROOT/'runs').glob('*_sources'))
        self.assertGreaterEqual(len(imports),2)
        for folder in imports:
            b=read(folder/'bundle.json')
            self.assertEqual(b['price_date'],'2026-11-05')
            self.assertIn('User supplied',read(folder/'source-provenance.json')['price_status'])

if __name__=='__main__':unittest.main()
