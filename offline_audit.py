"""Code-only review of saved Checkpoint 1 report tables. No API or model calls.

This cannot replace the course's semantic verifier or create new analyst insights.
"""
import argparse
import re
import shutil
from pathlib import Path
from common import new_run,read,save
from sec_data import ratios
from verifier import rounded

NUM=r'[-+]?\d[\d,]*(?:\.\d+)?'

def numbers(text):
    return [float(x.replace(',','')) for x in re.findall(NUM,text.replace('−','-'))]

def selected_text(report_row,folder):
    blocks=[]
    # Reuse a filename for later L ranges in the same citation.
    for file,tail in re.findall(r'([\w-]+\.txt)([^|\]]*)',report_row):
        p=folder/file
        if not p.exists(): continue
        ranges=[(int(a),int(b or a)) for a,b in re.findall(r'\bL(\d+)(?:[–—-]L?(\d+))?',tail)]
        if not ranges: continue
        for line in p.read_text().splitlines():
            m=re.match(r'L(\d+):\s?(.*)',line)
            if m and any(a<=int(m[1])<=b for a,b in ranges): blocks.append(m[2])
    return '\n'.join(blocks)

def statement_pair(text,pattern,decimal_only=False):
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if re.fullmatch(pattern,line.strip(),re.I):
            vals=[]
            for candidate in lines[i+1:i+18]:
                if re.fullmatch(r'\$?\s*'+NUM,candidate.strip()) and (not decimal_only or '.' in candidate):
                    vals.append(numbers(candidate)[0])
                if len(vals)==2:return vals
    return []

def core_rows(report):
    for row in report.splitlines():
        if not row.startswith('|'):continue
        cells=[c.strip() for c in row.strip().strip('|').split('|')]
        m=re.fullmatch(r'(\d+)\.\s*(.+)',cells[0])
        if m and len(cells)>=3:
            yield int(m[1]),m[2],cells[1],row
        elif cells[0].isdigit() and len(cells)>=5:
            yield int(cells[0]),cells[1],cells[2],row

def audit_core(folder):
    folder=Path(folder);b=read(folder/'bundle.json')
    report=(folder/'report.md').read_text() if (folder/'report.md').exists() else (folder/'report-fallback.md').read_text()
    f=b['facts'];r=ratios(f,b.get('price'))
    def v(name):return f[name]['current']['val']
    expected={1:[v('total_revenue')/1e6],2:[r['revenue_growth']['value']*100],3:[v('operating_income')/1e6,r['operating_margin']['value']*100],4:[v('net_income')/1e6],5:[v('diluted_eps')],6:[r['return_on_average_equity']['value']*100],7:[r['debt_to_equity']['value']],8:[r['free_cash_flow']['value']/1e6]}
    marks=[]
    for number,label,figure,row in core_rows(report):
        if not 1<=number<=11:continue
        block=selected_text(row,folder)
        values=numbers(figure)
        target=expected.get(number)
        arithmetic=''
        if number in (9,10):
            pair=statement_pair(block,r'(?:total\s+revenue[s]?|net operating revenues)')
            if pair:
                target=[pair[0]] if number==9 else [(pair[0]/pair[1]-1)*100]
                arithmetic=str(pair[0]) if number==9 else f'({pair[0]} / {pair[1]} - 1) * 100'
        elif number==11:
            pair=statement_pair(block,r'(?:diluted(?: net income per (?:common )?share)?|diluted net income per share)',decimal_only=True)
            if pair:target=[pair[0]]
            # Some releases put the two EPS values directly under a shorter label.
            if not target:
                lines=block.splitlines()
                for i,line in enumerate(lines):
                    if 'diluted' in line.lower():
                        vals=[numbers(x)[0] for x in lines[i+1:i+12] if re.fullmatch(r'\$?\s*'+NUM,x.strip()) and '.' in x]
                        if vals:target=[vals[0]];break
        if not block or not target or len(values)!=len(target):
            mark='unsupported'
            reason='No source range, expected statement value, or matching figure shape established.'
        else:
            numeric_tokens=re.findall(NUM,figure)
            precisions=[len(t.split('.')[1]) if '.' in t else 0 for t in numeric_tokens]
            good=all(rounded(a,d)==rounded(e,d) for a,e,d in zip(values,target,precisions))
            mark='code correct' if good else 'wrong'
            reason='Matches saved facts / recomputed arithmetic.' if good else 'Reported value differs from saved facts / recomputed arithmetic.'
        evidence=[]
        # Code-derived evidence records, not model explanations.
        if number<=8:
            keys={1:['total_revenue'],2:['total_revenue'],3:['operating_income','total_revenue'],4:['net_income'],5:['diluted_eps'],6:['net_income','equity'],7:['long_term_debt','current_debt','equity'],8:['cash_from_operations','capital_expenditures']}[number]
            for key in keys:
                for period in ('current','prior') if number in (2,6) else ('current',):
                    fact=f[key].get(period)
                    if fact:evidence.append(f"facts.json {fact['tag']} {fact['end']}: {fact['val']} {fact['unit']}")
            name={2:'revenue_growth',3:'operating_margin',6:'return_on_average_equity',7:'debt_to_equity',8:'free_cash_flow'}.get(number)
            if name:arithmetic=r[name]['arithmetic']+(' * 100 for percent' if number in (2,3,6) else '')
        evidence.append(block)
        marks.append({'core_claim':number,'label':label,'reported':figure,'expected':target,'code_mark':mark,'semantic_check':'NOT RUN — no model provider','arithmetic':arithmetic,'evidence':evidence,'reason':reason,'original_row':row})
    return report,marks,b

def review(source):
    source=Path(source).resolve();bundle=read(source/'bundle.json')
    folder=new_run(bundle['company']['ticker'],'_offline')
    for p in source.iterdir():
        if p.is_file() and (p.suffix in ('.txt','.html') or p.name in ('bundle.json','report.md','report-fallback.md','source-provenance.json') or p.name.endswith('facts.json')):
            shutil.copy2(p,folder/p.name)
    report,marks,b=audit_core(folder)
    if not marks: raise ValueError('No supported Checkpoint 1 core-claim table found.')
    # Detect the invented-growth trial independently of the original core table.
    for m in re.finditer(r'Annual revenue growth is ('+NUM+r')%, defined as \(('+NUM+r') / ('+NUM+r') - 1\) \* 100',report):
        claimed,a,z=map(lambda x:float(x.replace(',','')),m.groups())
        expected=(a/z-1)*100
        facts=b['facts']['total_revenue']
        supported=a==facts['current']['val'] and z==facts['prior']['val']
        marks.append({'core_claim':'seeded growth','label':'Additional annual growth assertion','reported':str(claimed)+'%','expected':[expected],'code_mark':'wrong' if supported and rounded(claimed,2)!=rounded(expected,2) else 'code correct' if supported else 'unsupported','semantic_check':'NOT RUN — no model provider','arithmetic':f'({a} / {z} - 1) * 100','evidence':[f"facts.json {facts['current']['tag']} {facts['current']['end']} and {facts['prior']['end']}"],'reason':'Quoted inputs independently matched to saved annual facts.','original_row':m[0]})
    save(folder/'offline-marks.json',{'scope':'Core table and seeded growth sentence only. Numerical checks; model semantics and additional narrative/peer claims NOT audited.','marks':marks})
    def cell(x):return str(x).replace('|','/').replace('\n',' ')
    table='\n\n## Offline numerical checks — model verification not run\n\nThis is a code-only review of an existing fallback report. It is not an executed agent-team report or the complete Checkpoint 2 proof. "Code correct" does not certify period or definition. Additional narrative and peer claims are outside this offline table.\n\n| Claim | Code mark | Reported | Expected | Arithmetic / source |\n|---|---|---|---|---|\n'
    for m in marks:
        evidence=m['arithmetic']+'; '+m['evidence'][0][:350]
        table+='| '+' | '.join(cell(x) for x in [m['label'],m['code_mark'],m['reported'],m['expected'],evidence])+' |\n'
    corrected=report
    for m in marks:
        if m['code_mark']=='wrong':
            corrected=corrected.replace(m['original_row'],'[OFFLINE CORRECTION: '+m['label']+'; expected '+str(m['expected'])+'. See code evidence above. Original erroneous assertion removed.]',1)
    first,_,rest=corrected.partition('\n')
    price=''
    if b.get('price'):
        pe=b['price']/b['facts']['diluted_eps']['current']['val']
        price=f"\n\n## Supplied price scenario\n\nUser-supplied close: ${b['price']:.2f}, dated {b['price_date']}; source recorded as {b['price_source']}. This price has not been independently checked. Annual EPS P/E = {b['price']} / {b['facts']['diluted_eps']['current']['val']} = {pe:.2f}×. This uses annual GAAP EPS, not trailing-four-quarter EPS. The price is later than the saved earnings release. This scenario does not revise the historical fallback recommendation.\n"
    (folder/'offline-report.md').write_text(first+table+'\n## Saved fallback report with offline numerical corrections\n\n'+rest+price)
    save(folder/'offline-provenance.json',{'source_run':str(source),'api_calls':0,'model_semantic_check':'not run','status':'Offline work complete; live course proof remains pending.'})
    return folder

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path)
    print(review(p.parse_args().source)/'offline-report.md')
