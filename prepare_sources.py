"""Import a saved source set without running analysts or claiming verification."""
import argparse
import shutil
from pathlib import Path
from common import new_run,read,save
from sec_data import ratios

def prepare(source,price,price_date,price_source):
    source=Path(source).resolve();bundle=read(source/'bundle.json')
    folder=new_run(bundle['company']['ticker'],'_sources')
    for p in source.iterdir():
        if p.is_file() and (p.suffix in ('.txt','.html') or p.name in ('facts.json','filings.json','peers.json')):
            shutil.copy2(p,folder/p.name)
    bundle.update(price=price,price_date=price_date,price_source=price_source,ratios=ratios(bundle['facts'],price))
    save(folder/'bundle.json',bundle);save(folder/'ratios.json',bundle['ratios'])
    for ticker,peer in bundle['peers'].items(): save(folder/f'{ticker.upper()}-facts.json',peer['facts'])
    save(folder/'source-provenance.json',{'source_run':str(source),'status':'Source import only; no model analysis or verification.', 'price_status':'User supplied; not independently checked; later than the earnings release.'})
    return folder

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('--price',required=True,type=float);p.add_argument('--price-date',required=True);p.add_argument('--price-source',required=True)
    a=p.parse_args();print(prepare(a.source,a.price,a.price_date,a.price_source))
