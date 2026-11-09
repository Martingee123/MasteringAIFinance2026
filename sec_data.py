"""Source-preserving research desk. Run with --data-only before model calls."""
import argparse
import ast
import operator
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / '.env')
load_dotenv(ROOT / '.env')
TAGS = {
 'total_revenue': ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet', 'RevenueFromContractWithCustomerIncludingAssessedTax'],
 'operating_income': ['OperatingIncomeLoss'],
 'net_income': ['NetIncomeLoss', 'ProfitLoss'],
 'diluted_eps': ['EarningsPerShareDiluted'],
 'equity': ['StockholdersEquity', 'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'],
 'long_term_debt': ['LongTermDebtNoncurrent', 'LongTermDebt', 'LongTermDebtAndCapitalLeaseObligations'],
 'current_debt': ['LongTermDebtCurrent', 'LongTermDebtAndCapitalLeaseObligationsCurrent'],
 'cash_from_operations': ['NetCashProvidedByUsedInOperatingActivities'],
 'capital_expenditures': ['PaymentsToAcquirePropertyPlantAndEquipment'],
}
PARTS = ['Overview', 'Market Positioning and Growth Outlook', 'Valuation Insights', 'Future Developments and Strategic Recommendations', 'Investment Recommendation']

class SEC:
 def __init__(self):
  ua = os.getenv('SEC_USER_AGENT', '')
  if not ua or '@' not in ua: raise ValueError('Set SEC_USER_AGENT to your name and email in .env.')
  self.session = requests.Session()
  self.session.headers['User-Agent'] = ua
  self.last = 0
 def get(self, url):
  cache = ROOT / '.cache' / __import__('hashlib').sha256(url.encode()).hexdigest()
  if cache.exists(): return cache.read_text()
  time.sleep(max(0, .15 - (time.monotonic()-self.last)))
  r = self.session.get(url, timeout=90)
  self.last = time.monotonic()
  r.raise_for_status()
  cache.parent.mkdir(exist_ok=True)
  cache.write_text(r.text)
  return r.text
 def js(self,url): return json.loads(self.get(url))

def save(path, obj): path.write_text(json.dumps(obj, indent=2))
def plain(html):
 soup = BeautifulSoup(html, 'html.parser')
 for x in soup(['script','style','ix:header']): x.decompose()
 return '\n'.join(x.strip() for x in soup.get_text('\n').splitlines() if x.strip())
def numbered(text): return '\n'.join(f'L{i}: {s}' for i,s in enumerate(text.splitlines(),1))

def filings(sec,cik,annual_only=False):
 sub = sec.js(f'https://data.sec.gov/submissions/CIK{cik:010d}.json')
 rows = sub['filings']['recent']
 records = [dict(zip(rows, vals)) for vals in zip(*rows.values())]
 for older in sub['filings'].get('files',[]):
  if any(r['form']=='10-K' for r in records) and any(r['form']=='10-Q' for r in records) and any(r['form']=='8-K' and '2.02' in r.get('items','') for r in records): break
  data=sec.js('https://data.sec.gov/submissions/'+older['name'])
  records.extend(dict(zip(data,v)) for v in zip(*data.values()))
 selected={}
 for label, form in ([('annual','10-K')] if annual_only else [('annual','10-K'),('quarterly','10-Q'),('earnings','8-K')]):
  candidates=[r for r in records if r['form']==form and (label!='earnings' or '2.02' in r.get('items',''))]
  if not candidates: raise ValueError(f'No {label} filing found')
  r=max(candidates,key=lambda x:x['filingDate'])
  base=f"https://www.sec.gov/Archives/edgar/data/{cik}/{r['accessionNumber'].replace('-','')}/"
  index_url=base+r['accessionNumber']+'-index.html'
  soup=BeautifulSoup(sec.get(index_url),'html.parser')
  accepted=soup.find(string=lambda x: x and x.strip()=='Accepted')
  accepted_value=accepted.parent.find_next_sibling().get_text(' ',strip=True) if accepted else r.get('acceptanceDateTime','unavailable')
  doc=base+r['primaryDocument']
  if label=='earnings':
   matches=[]
   for tr in soup.select('tr'):
    cells=tr.find_all('td')
    if len(cells)>=4 and cells[3].get_text(strip=True).upper()=='EX-99.1':
     link=tr.find('a',href=True)
     if link: matches.append(__import__('urllib.parse',fromlist=['urljoin']).urljoin(index_url,link['href']))
   if not matches: raise ValueError('Earnings 8-K has no Exhibit 99.1; inspect filing manually.')
   doc=matches[0].replace('/ix?doc=','')
  selected[label]={'accession':r['accessionNumber'],'accepted':accepted_value,'filing_date':r['filingDate'],'period_end':r['reportDate'],'url':doc,'index_url':index_url}
  print(label,selected[label])
 return selected

def facts(sec,cik,annual):
 data=sec.js(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json')
 concepts=data['facts'].get('us-gaap',{})
 target=annual['period_end']
 out={}
 for name,tags in TAGS.items():
  unit='USD/shares' if name=='diluted_eps' else 'USD'
  pool=[]
  for priority,tag in enumerate(tags):
   for item in concepts.get(tag,{}).get('units',{}).get(unit,[]):
    if item.get('form')!='10-K' or item.get('filed','')>annual['filing_date']: continue
    if 'start' in item:
     days=(datetime.fromisoformat(item['end'])-datetime.fromisoformat(item['start'])).days
     if not 330<=days<=380: continue
    pool.append(dict(item,tag=tag,unit=unit,priority=priority))
  current=[x for x in pool if x['end']==target]
  if not current:
   out[name]={'status':'missing','period_end':target,'reason':'No matching annual fact; inspect filing. Zero is not assumed.'}; continue
  chosen=max(current,key=lambda x:(x.get('accn')==annual['accession'],-x['priority'],x.get('filed','')))
  prior=[x for x in pool if 330<=(datetime.fromisoformat(target)-datetime.fromisoformat(x['end'])).days<=380]
  prev=max(prior,key=lambda x:(x['end'],x.get('accn')==annual['accession'],-x['priority'],x.get('filed',''))) if prior else None
  out[name]={'current':chosen,'prior':prev,'definition':concepts[chosen['tag']].get('description','')}
 return out

def ratios(f,price):
 def v(k,period='current'): return f.get(k,{}).get(period,{}).get('val') if f.get(k,{}).get(period) else None
 out={}
 def calc(name,inputs,formula,fn):
  if any(x is None for x in inputs): out[name]={'status':'missing inputs'}; return
  try: out[name]={'value':fn(*inputs),'arithmetic':formula.format(*inputs)}
  except ZeroDivisionError: out[name]={'status':'undefined: zero denominator'}
 calc('revenue_growth',[v('total_revenue'),v('total_revenue','prior')],'({0} / {1}) - 1',lambda a,b:a/b-1)
 calc('operating_margin',[v('operating_income'),v('total_revenue')],'{0} / {1}',lambda a,b:a/b)
 calc('return_on_average_equity',[v('net_income'),v('equity'),v('equity','prior')],'{0} / (({1} + {2}) / 2)',lambda a,b,c:a/((b+c)/2))
 calc('debt_to_equity',[v('long_term_debt'),v('current_debt'),v('equity')],'({0} + {1}) / {2}',lambda a,b,c:(a+b)/c)
 calc('free_cash_flow',[v('cash_from_operations'),v('capital_expenditures')],'{0} - {1}',lambda a,b:a-b)
 calc('price_to_earnings',[price,v('diluted_eps')],'{0} / {1}',lambda a,b:a/b)
 return out

def data_run(sec,args):
 print('Step 1: resolve ticker')
 listing=sec.js('https://www.sec.gov/files/company_tickers.json')
 row=next((x for x in listing.values() if x['ticker'].upper()==args.ticker.upper()),None)
 if not row: raise ValueError('Ticker not found')
 cik=row['cik_str']
 folder=ROOT/'runs'/f"{row['ticker']}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
 folder.mkdir(parents=True)
 if args.step==1: save(folder/'company.json',row); return folder,None
 print('Step 2: select filings')
 selected=filings(sec,cik)
 save(folder/'filings.json',selected)
 if args.step==2: return folder,None
 print('Step 3: download filings and Exhibit 99.1')
 for kind,meta in selected.items():
  html=sec.get(meta['url']); (folder/f'{kind}.html').write_text(html)
  (folder/f'{kind}.txt').write_text(numbered(plain(html)))
 if args.step==3: return folder,None
 print('Step 4: annual facts')
 f=facts(sec,cik,selected['annual'])
 save(folder/'facts.json',f)
 for k,x in f.items(): print(k,json.dumps(x.get('current',x)))
 if args.step==4: return folder,None
 print('Step 5: calculator')
 r=ratios(f,args.price); save(folder/'ratios.json',r); print(json.dumps(r,indent=2))
 if args.step==5: return folder,None
 print('Step 6: quarterly source lines')
 release=(folder/'earnings.txt').read_text()
 lines=release.splitlines(); hits=set()
 for i,line in enumerate(lines):
  if re.search(r'revenue|diluted|net income|cash and cash',line,re.I): hits.update(range(max(0,i-2),min(len(lines),i+12)))
 excerpts='\n'.join(lines[i] for i in sorted(hits))
 (folder/'quarterly-excerpts.txt').write_text(excerpts)
 print(excerpts[:8000])
 if args.step==6: return folder,None
 print('Step 7: peers')
 peers={}
 for ticker in filter(None,args.peers.split(',')):
  peer=next((x for x in listing.values() if x['ticker'].upper()==ticker.strip().upper()),None)
  if not peer: raise ValueError('Peer ticker not found: '+ticker)
  fs=filings(sec,peer['cik_str'],annual_only=True); pf=facts(sec,peer['cik_str'],fs['annual'])
  peer_html=sec.get(fs['annual']['url'])
  (folder/f'{ticker.upper()}-annual.txt').write_text(numbered(plain(peer_html)))
  peers[ticker]={'filings':fs,'facts':pf,'ratios':ratios(pf,None),'margin_definition':'operating income / total revenue'}
 save(folder/'peers.json',peers)
 bundle={'company':row,'filings':selected,'facts':f,'ratios':r,'peers':peers,'price':args.price,'price_date':args.price_date,'price_source':args.price_source}
 save(folder/'bundle.json',bundle)
 return folder,bundle

def calculate(expression):
 """Evaluate numeric arithmetic only; never execute model-provided code."""
 operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
 def visit(node):
  if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
  if isinstance(node, ast.BinOp) and type(node.op) in operators: return operators[type(node.op)](visit(node.left), visit(node.right))
  if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return -visit(node.operand)
  raise ValueError('Only numeric constants and + - * / are allowed.')
 if len(expression)>300: raise ValueError('Expression too long')
 return visit(ast.parse(expression, mode='eval').body)

