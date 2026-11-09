"""Adversarial checks of source grounding and ratio arithmetic, no API required."""
import unittest
from models import Claim,Evidence
from verifier import check_claim,check_evidence

class VerifierTests(unittest.TestCase):
    def setUp(self):
        self.sources={'facts.json':{'eps':{'current':{'tag':'EarningsPerShareDiluted','end':'2025-12-31','val':5.25}}},'annual.txt':'L1: Year ended December 31, 2025\nL2: Diluted EPS $5.25\nL3: Revenue 110 and prior revenue 100\nL4: The figure 15.25 is different.'}
    def evidence(self,**kw):
        data=dict(file='facts.json',line_start=0,line_end=0,quote='',tag='EarningsPerShareDiluted',period='2025-12-31',value=5.25,scale=1)
        return Evidence(**(data|kw))
    def claim(self,**kw):
        data=dict(label='Annual diluted EPS',report_quote='EPS $5.25',reported_value=5.25,decimals=2,kind='fact',definition='Annual GAAP diluted EPS',evidence=[self.evidence()],expression='',semantic_mark='correct',semantic_reason='Annual EPS for the stated year',corrected_text='EPS $5.25')
        return Claim(**(data|kw))
    def test_clean_eps(self):
        self.assertEqual(check_claim(self.claim(),self.sources)['mark'],'correct')
    def test_seeded_eps_one_dollar_higher(self):
        r=check_claim(self.claim(reported_value=6.25),self.sources)
        self.assertEqual(r['mark'],'wrong');self.assertEqual(r['expected'],5.25)
    def test_invented_growth_four_percentage_points(self):
        a=self.evidence(file='annual.txt',line_start=3,line_end=3,quote='Revenue 110 and prior revenue 100',value=110,tag='')
        b=a.model_copy(update={'value':100})
        c=self.claim(kind='ratio',reported_value=14,decimals=2,definition='Revenue growth percent',evidence=[a,b],expression='(110 / 100 - 1) * 100')
        r=check_claim(c,self.sources)
        self.assertEqual(r['mark'],'wrong');self.assertAlmostEqual(r['expected'],10)
    def test_wrong_period_semantic_check_cannot_be_overridden(self):
        self.assertEqual(check_claim(self.claim(semantic_mark='wrong',semantic_reason='Correct number but wrong quarter'),self.sources)['mark'],'wrong')
    def test_no_source(self):
        self.assertEqual(check_claim(self.claim(evidence=[]),self.sources)['mark'],'unsupported')
    def test_undefined_equity_definition(self):
        c=self.claim(kind='ratio',definition='',expression='5.25 / 1')
        self.assertEqual(check_claim(c,self.sources)['mark'],'unsupported')
    def test_wrong_tag_or_period(self):
        for e in [self.evidence(tag='WrongTag'),self.evidence(period='2024-12-31')]:
            self.assertEqual(check_claim(self.claim(evidence=[e]),self.sources)['mark'],'unsupported')
    def test_quoted_line_must_exist(self):
        e=self.evidence(file='annual.txt',line_start=2,line_end=2,quote='Diluted EPS $6.25',value=6.25)
        self.assertFalse(check_evidence(e,self.sources)[0])
    def test_whitespace_allowed(self):
        e=self.evidence(file='annual.txt',line_start=2,line_end=2,quote='Diluted   EPS\n $5.25')
        self.assertTrue(check_evidence(e,self.sources)[0])
    def test_number_substring_not_accepted(self):
        e=self.evidence(file='annual.txt',line_start=4,line_end=4,quote='The figure 15.25 is different.')
        self.assertFalse(check_evidence(e,self.sources)[0])
    def test_ratio_unsourced_operand(self):
        c=self.claim(kind='ratio',expression='5.25 / 999',definition='ratio')
        self.assertEqual(check_claim(c,self.sources)['mark'],'unsupported')
    def test_code_execution_rejected(self):
        c=self.claim(kind='ratio',expression='__import__("os").getcwd()',definition='ratio')
        self.assertEqual(check_claim(c,self.sources)['mark'],'unsupported')
    def test_usd_scale_exact(self):
        self.sources['facts.json']['revenue']={'current':{'tag':'Revenues','end':'2025-12-31','val':110000000}}
        self.assertTrue(check_evidence(self.evidence(tag='Revenues',value=110,scale=1000000),self.sources)[0])

if __name__=='__main__': unittest.main()
