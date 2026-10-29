"""Checks for arithmetic safety, missing data, and annual-period selection."""
import unittest
from desk import calculate, facts, ratios

class DeskTests(unittest.TestCase):
 def test_calculator_only_allows_arithmetic(self):
  self.assertAlmostEqual(calculate('(13380 / 12455 - 1) * 100'),7.4267362505)
  for expression in ['__import__("os").getcwd()', '2**100', 'True + 1']:
   with self.assertRaises(ValueError): calculate(expression)
 def test_missing_debt_is_not_zero(self):
  f={k:{'current':{'val':v}} for k,v in [('equity',10),('long_term_debt',20)]}
  self.assertEqual(ratios(f,None)['debt_to_equity']['status'],'missing inputs')
 def test_new_tag_and_annual_period(self):
  annual={'period_end':'2025-12-31','filing_date':'2026-02-20','accession':'latest'}
  def fact(value,end,start,accession): return dict(val=value,end=end,start=start,accn=accession,form='10-K',filed='2026-02-20')
  class FakeSEC:
   def js(self,url): return {'facts':{'us-gaap':{
    'Revenues':{'units':{'USD':[fact(100,'2024-12-31','2024-01-01','old')]}},
    'RevenueFromContractWithCustomerExcludingAssessedTax':{'units':{'USD':[
     fact(125,'2025-12-31','2025-01-01','latest'),fact(90,'2024-12-31','2024-01-01','latest'),fact(35,'2025-12-31','2025-10-01','latest')]}}
   }}}
  f=facts(FakeSEC(),1,annual)['total_revenue']
  self.assertEqual(f['current']['val'],125)
  self.assertEqual(f['prior']['val'],90)
  self.assertEqual(f['current']['end'],'2025-12-31')

if __name__=='__main__': unittest.main()
