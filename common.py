import json
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / '.env')
load_dotenv(ROOT / '.env')

def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def new_run(ticker, label=''):
    import re
    if not re.fullmatch(r'[A-Za-z0-9.^-]{1,15}', ticker):
        raise ValueError('Use a valid ticker, without spaces or directory separators.')
    folder = ROOT / 'runs' / (ticker.upper() + '_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + label)
    folder.mkdir(parents=True, exist_ok=False)
    return folder

class Model:
    def __init__(self, model=None, provider='openai'):
        self.provider=provider
        self.model=model or ('claude-sonnet-4-6' if provider=='anthropic' else 'gpt-4.1')
        if provider=='anthropic':
            from anthropic import Anthropic
            key=os.getenv('ANTHROPIC_API_KEY')
            if not key: raise ValueError('Set ANTHROPIC_API_KEY in the parent .env.')
            self.client=Anthropic(api_key=key,timeout=240,max_retries=1)
        else:
            key=os.getenv('API_KEY') or os.getenv('OPENAI_API_KEY')
            if not key: raise ValueError('Set API_KEY or OPENAI_API_KEY in the parent .env.')
            self.client=OpenAI(api_key=key,timeout=240,max_retries=1)

    def call(self, folder, name, instructions, payload, schema=None):
        save(folder / f'{name}-input.json', {'instructions': instructions, 'payload': payload, 'model': self.model, 'provider':self.provider})
        limit=24000 if name=='verifier' else 14000
        if self.provider=='anthropic':
            kw=dict(model=self.model,system=instructions,messages=[{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],max_tokens=limit)
            if schema:
                response=self.client.messages.parse(**kw,output_format=schema)
                result=response.parsed_output
            else:
                response=self.client.messages.create(**kw)
                result=''.join(b.text for b in response.content if b.type=='text')
            if response.stop_reason=='max_tokens':
                raise ValueError(f'{name}: output was truncated; no success is claimed.')
        else:
            kw=dict(model=self.model,instructions=instructions,input=json.dumps(payload,ensure_ascii=False),max_output_tokens=limit)
            if schema:
                response=self.client.responses.parse(**kw,text_format=schema)
                result=response.output_parsed
            else:
                response=self.client.responses.create(**kw)
                result=response.output_text
            if response.status!='completed':
                raise ValueError(f'{name}: incomplete response; no success is claimed.')
        if result is None or (isinstance(result,str) and not result.strip()):
            raise ValueError(f'{name}: model refused or returned empty output.')
        if schema:
            save(folder / f'{name}-output.json',result.model_dump())
        else:
            (folder / f'{name}-output.md').write_text(result)
        save(folder / f'{name}-usage.json',{'response_id':response.id,'model':response.model,'provider':self.provider,'usage':response.usage.model_dump() if response.usage else None})
        return result
