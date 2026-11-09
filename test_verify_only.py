"""Verify report layout, input isolation, and non-destructive verify-only operation."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from common import save
from desk import parser,run
from models import Audit,Claim,Evidence

class AuditModel:
    model='test-double-no-api'
    def __init__(self):self.payload=None
    def call(self,folder,name,instructions,payload,schema):
        self.payload=payload
        evidence=Evidence(file='facts.json',line_start=0,line_end=0,quote='',tag='EarningsPerShareDiluted',period='2025-12-31',value=5.25,scale=1)
        claim=Claim(label='Annual EPS',report_quote='Annual EPS is $6.25.',reported_value=6.25,decimals=2,kind='fact',definition='Annual GAAP diluted EPS',evidence=[evidence],expression='',semantic_mark='wrong',semantic_reason='Annual EPS differs from saved facts.',corrected_text='Annual EPS is $5.25. [facts.json EarningsPerShareDiluted 2025-12-31]')
        return Audit(claims=[claim],excluded_thesis='No thesis assessed.',coverage_notes='One synthetic test claim; semantic verdict supplied by test double.')

class VerifyOnlyTests(unittest.TestCase):
    def test_copies_sources_and_only_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'original';source.mkdir()
            original='annual: test-accession https://example.test/annual\n\nAnnual EPS is $6.25.\n'
            (source/'report.md').write_text(original)
            (source/'annual.txt').write_text('L1: Diluted EPS 5.25')
            save(source/'facts.json',{'eps':{'current':{'tag':'EarningsPerShareDiluted','end':'2025-12-31','val':5.25}}})
            save(source/'bundle.json',{'company':{'ticker':'TEST'}})
            (source/'research_analyst-output.md').write_text('This must not reach the Verifier.')
            fake=AuditModel();args=parser().parse_args(['--verify-only',str(source)])
            with patch('common.ROOT',root),patch('desk.Model',return_value=fake),patch('desk.make_graph') as graph:
                folder=run(args,emit=lambda _:None)
            graph.assert_not_called()
            self.assertEqual((source/'report.md').read_text(),original)
            self.assertNotEqual(folder,source)
            report=(folder/'verified-report.md').read_text()
            self.assertEqual(report.splitlines()[0],original.splitlines()[0])
            self.assertIn('## Verifier marks',report)
            self.assertIn('Annual EPS is $5.25',report)
            self.assertEqual(set(fake.payload['context']),{'report','saved_sources'})
            self.assertNotIn('This must not reach',str(fake.payload))

if __name__=='__main__':unittest.main()
