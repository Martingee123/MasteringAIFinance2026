"""Prepare immutable evidence copies and run the course's three verifier trials."""
import argparse
import re
import shutil
from pathlib import Path
from common import ROOT, new_run, read, save
from desk import parser,run


def prepare(source):
    source=Path(source).resolve()
    bundle=read(source/'bundle.json');ticker=bundle['company']['ticker']
    eps=bundle['facts']['diluted_eps']['current']['val']
    current=bundle['facts']['total_revenue']['current']
    prior=bundle['facts']['total_revenue']['prior']
    annual=bundle['filings']['annual']
    paths={}
    for label in ('clean','seeded-eps','invented-growth'):
        folder=new_run(ticker,'_'+label)
        for p in source.iterdir():
            if p.is_file() and (p.suffix in ('.txt','.html') or p.name in ('bundle.json','report.md','filings.json') or p.name.endswith('facts.json')):
                shutil.copy2(p,folder/p.name)
        if not (folder/'report.md').exists():
            shutil.copy2(source/'report-fallback.md',folder/'report.md')
        paths[label]=folder
    seeded=paths['seeded-eps']/'report.md';text=seeded.read_text()
    # Target a row/line which explicitly identifies annual diluted EPS; do not change source files.
    lines=text.splitlines();changed=False
    number=f'{eps:.2f}';wrong=f'{eps+1:.2f}'
    for i,line in enumerate(lines):
        if re.search(r'annual.*(?:GAAP\s+)?diluted EPS',line,re.I) and number in line:
            lines[i]=line.replace(number,wrong,1)+f' [Seeded false source quotation: "Annual diluted EPS {wrong}".]'
            changed=True;break
    if not changed: raise ValueError('No explicit annual diluted EPS line found; choose a report with that claim.')
    seeded.write_text('\n'.join(lines)+'\n')
    growth=(current['val']/prior['val']-1)*100
    invented=paths['invented-growth']/'report.md'
    sentence=f"\nAnnual revenue growth is {growth+4:.2f}%, defined as ({current['val']} / {prior['val']} - 1) * 100. Inputs: revenue {current['val']} USD [facts.json; {current['tag']}; {current['end']}], prior revenue {prior['val']} USD [facts.json; {prior['tag']}; {prior['end']}]. The claimed rate is a seeded test error.\n"
    # Place the test before the disclosure, not as metadata excluded from the audit.
    text=invented.read_text();text=text.replace('## Valuation Insights','## Valuation Insights\n'+sentence,1)
    if sentence not in text: text+=sentence
    invented.write_text(text)
    manifest={'source_run':str(source),'trials':{k:str(v.relative_to(ROOT)) for k,v in paths.items()},'known_answers':{'annual_eps':eps,'seeded_eps':eps+1,'revenue_growth_percent':growth,'invented_growth_percent':growth+4},'status':'Prepared, not model-verified. Run with --execute when provider access is available.'}
    save(ROOT/'proof-manifest.json',manifest)
    return paths


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('--execute',action='store_true');p.add_argument('--model',default=None);p.add_argument('--provider',choices=['openai','anthropic'],default='openai')
    a=p.parse_args();paths=prepare(a.source)
    if a.execute:
        results={}
        for label,path in paths.items():
            args=parser().parse_args(['--verify-only',str(path),'--provider',a.provider]+(['--model',a.model] if a.model else []))
            result=run(args);results[label]=str(result.relative_to(ROOT))
        save(ROOT/'proof-results.json',results)
    print('Prepared trials:',ROOT/'proof-manifest.json')

if __name__=='__main__':main()
