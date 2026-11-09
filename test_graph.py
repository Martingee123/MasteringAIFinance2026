"""Verify routing, isolated role inputs, bounded repair and preserved run folders."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from models import Review,FinancialOutput
from desk import make_graph,parser,PARTS
from common import ROOT,save

class FakeModel:
    model='test-double-no-api'
    def __init__(self,repair=False): self.calls=[];self.repair=repair
    def call(self,folder,name,instructions,payload,schema=None):
        self.calls.append((name,payload))
        if schema is Review:
            return Review(report='\n'.join('## '+p for p in PARTS),research_issues=['Repair insight'] if self.repair and name.endswith('-1') else [],financial_issues=[],advisor_issues=[])
        if schema is FinancialOutput:
            return FinancialOutput(markdown='Financial analysis.\nInsight: Evidence supports a financial relationship. [annual.txt L1]',calculations=[])
        return 'Sourced analysis.\nInsight: Evidence supports this claim. [annual.txt L1]'

class GraphTests(unittest.TestCase):
    def test_fixed_order_and_isolation_two_runs(self):
        self.exercise(False)
    def test_repair_bounded_and_verifier_still_last(self):
        self.exercise(True)
    def exercise(self,repair):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.mkdir()
            shutil.copytree(ROOT/'roles',root/'roles')
            b={'company':{'ticker':'TEST'},'filings':{'annual':{'accession':'test-accession','url':'https://example.test/annual'}},'facts':{},'peers':{},'ratios':{}}
            save(source/'bundle.json',b)
            for name in ('annual.txt','earnings.txt','quarterly.txt'): (source/name).write_text('L1: A synthetic filing line.')
            args=parser().parse_args(['TEST','--source-run',str(source)])
            names=[];folders=[]
            with patch('desk.ROOT',root),patch('common.ROOT',root),patch('desk.verify',return_value=[{'mark':'correct'}]) as vf:
                for _ in range(2):
                    model=FakeModel(repair);graph=make_graph(args,model,names.append)
                    result=graph.invoke({});folders.append(Path(result['folder']))
                    self.assertTrue(result['verified'])
                    advisor=next(payload for name,payload in model.calls if name=='investment_advisor-1')
                    self.assertEqual(set(advisor['context']),{'research_analyst','financial_analyst'})
                    research=next(payload for name,payload in model.calls if name=='research_analyst-1')
                    self.assertNotIn('financial_analyst',research['context'])
                    counts=json.loads((folders[-1]/'call-counts.json').read_text())
                    self.assertTrue(all(x<=2 for x in counts.values()))
                    self.assertEqual(counts['research_analyst'],2 if repair else 1)
                self.assertEqual(vf.call_count,2)
            self.assertNotEqual(*folders)
            self.assertTrue(all((p/'report.md').exists() for p in folders))
            orders=[(p/'node-order.jsonl').read_text() for p in folders]
            self.assertEqual(*orders)
            self.assertEqual(json.loads(orders[0].splitlines()[-1])['node'],'Verifier')
    def test_no_public_skip_verifier(self):
        flags={opt for a in parser()._actions for opt in a.option_strings}
        self.assertFalse(flags & {'--skip-verifier','--no-verify','--data-only'})

if __name__=='__main__':unittest.main()
