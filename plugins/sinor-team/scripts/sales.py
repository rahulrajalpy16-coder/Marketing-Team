#!/usr/bin/env python3
"""Local deterministic sales controls. No model API client or network requests.

Data lives in the sales root of the Sinor workspace (scripts/workspace_lib.py), never in the plugin.
Global option: --workspace <folder> (otherwise SINOR_WORKSPACE, project folder, saved setup).
"""
import argparse, hashlib, json, os, re, shutil, sys, uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import workspace_lib

ROOT = workspace_lib.resolve_root('sales')  # None when no workspace is set up yet

def write_record(root, kind, data):
    ident = kind + '-' + uuid.uuid4().hex
    data = dict(data, id=ident, created_at=datetime.now(timezone.utc).isoformat())
    path = root / 'records' / kind / (ident + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    with temporary.open('x', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    temporary.replace(path)
    return data

def extract(path):
    suffix = path.suffix.lower()
    if suffix in {'.txt','.md','.csv','.json','.xml','.html'}:
        return path.read_text(encoding='utf8'), 'extracted'
    if suffix == '.docx':
        from docx import Document
        doc = Document(path)
        text = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            text += [' | '.join(c.text for c in row.cells) for row in table.rows]
        return '\n'.join(text), 'extracted-body-and-tables'
    if suffix == '.pdf':
        from pypdf import PdfReader
        pages = [p.extract_text() or '' for p in PdfReader(path).pages]
        text = '\n'.join(f'[Page {n+1}]\n{t}' for n,t in enumerate(pages))
        return text, 'extracted' if pages and all(t.strip() for t in pages) else 'OCR_REQUIRED'
    if suffix == '.xlsx':
        from openpyxl import load_workbook
        wb = load_workbook(path, data_only=False, read_only=True)
        text = '\n'.join(f'[{s.title}!{n}] '+ ' | '.join(str(v) if v is not None else '' for v in row) for s in wb for n,row in enumerate(s.values,1))
        wb.close()
        return text, 'extracted-formulas-not-recalculated'
    return '', 'MANUAL_EXTRACTION_REQUIRED'

def register(root, source, category, status, reference):
    source = Path(source).resolve()
    if not source.is_file(): raise ValueError('Source file does not exist')
    if status not in {'draft','approved','superseded'}: raise ValueError('Invalid document status')
    data = source.read_bytes(); digest = hashlib.sha256(data).hexdigest()
    dest = root / 'sources' / digest / source.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists(): shutil.copyfile(source,dest)
    text, extraction = extract(dest)
    return write_record(root,'documents',dict(filename=source.name, stored_path=str(dest.relative_to(root)), sha256=digest, category=category, status=status, reference=reference, text=text, extraction_status=extraction))

def search(root, query, approved_only=False):
    words = query.lower().split()
    results=[]
    for p in (root/'records').glob('*/*.json'):
        r=json.loads(p.read_text())
        if approved_only and r.get('status') != 'approved': continue
        hay=json.dumps(r,ensure_ascii=False).lower()
        score=sum(w in hay for w in words)
        if words and score == len(words): results.append(dict(r,match_score=score))
    return sorted(results,key=lambda r:r['created_at'],reverse=True)

def number(value, name, maximum=None):
    try: n=Decimal(str(value))
    except InvalidOperation: raise ValueError(f'{name}: invalid number')
    if not n.is_finite() or n < 0 or (maximum is not None and n >= maximum): raise ValueError(f'{name}: outside allowed range')
    return n

def money(n): return str(n.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))

def calculate(spec):
    currency=spec.get('currency','')
    if not re.fullmatch('[A-Z]{3}',currency): raise ValueError('Explicit three-letter currency required; no automatic FX')
    if not spec.get('items'): raise ValueError('At least one priced item required')
    margin=number(spec.get('margin_pct',0),'margin',100)/100
    markup=number(spec.get('markup_pct',0),'markup')/100
    if margin and markup: raise ValueError('Choose margin OR markup, not both')
    tax=number(spec.get('tax_pct',0),'tax',101)/100
    rows=[]; subtotal=Decimal(0)
    for item in spec['items']:
        if item.get('unit_cost') is None and item.get('unit_sell') is None: raise ValueError('PRICE REQUIRES MANUAL CONFIRMATION')
        q=number(item.get('quantity',1),'quantity')
        if q == 0: raise ValueError('Quantity must be positive')
        if item.get('unit_sell') is not None: unit=number(item['unit_sell'],'unit sell')
        else: unit=number(item['unit_cost'],'unit cost')*(1+markup)/(1-margin)
        unit=Decimal(money(unit)); total=Decimal(money(q*unit)); subtotal+=total
        rows.append(dict(description=item.get('description',''),quantity=str(q),unit_sell=money(unit),line_total=money(total),price_source=item.get('price_source','USER INPUT - provenance requires review')))
    discount=Decimal(money(number(spec.get('discount',0),'discount')))
    if discount > subtotal: raise ValueError('Discount exceeds subtotal')
    net=subtotal-discount; vat=Decimal(money(net*tax))
    return dict(currency=currency,items=rows,subtotal=money(subtotal),discount=money(discount),net=money(net),tax=money(vat),total=money(net+vat),rounding='Unit and line rounded half-up to 2 decimals; tax on discounted net',status='DRAFT')

def remember(root, text, source, approved=False):
    if not text.strip() or not source.strip(): raise ValueError('Memory requires text and source task/instruction')
    return write_record(root,'memory',dict(text=text,source=source,status='approved' if approved else 'proposed'))

def task(root, instruction):
    r=write_record(root,'tasks',dict(instruction=instruction,status='open'))
    folder=root/'tasks'/r['id']; folder.mkdir(parents=True)
    (folder/'original_instruction.txt').write_text(instruction)
    (folder/'TASK.md').write_text('# '+r['id']+'\n\nStatus: OPEN\n\n## Requirements\n| ID | Requirement | Owner | Evidence | Status |\n|---|---|---|---|---|\n\n## Sources and template\n\n## Plan, model choices and file ownership\n\n## Pricing basis and unresolved items\n\n## QA and issue approval\n')
    (folder/'outputs').mkdir()
    return dict(r,folder=str(folder.relative_to(root)))

def fill_template(source, output, fields):
    from docx import Document
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve(): raise ValueError('Never overwrite controlled template')
    if output.exists(): raise ValueError('Output exists; use a new revision filename')
    doc=Document(source)
    paragraphs=[]
    def collect(container):
        paragraphs.extend(container.paragraphs)
        for table in container.tables:
            for row in table.rows:
                for cell in row.cells: collect(cell)
    collect(doc)
    for section in doc.sections:
        for part in [section.header,section.footer,section.first_page_header,section.first_page_footer,section.even_page_header,section.even_page_footer]: collect(part)
    missing=set()
    for p in paragraphs:
        missing.update(k for k in re.findall(r'\{\{([\w.-]+)\}\}',p.text) if k not in fields)
    if missing: raise ValueError('Unresolved template fields: '+', '.join(sorted(missing)))
    seen=set()
    for p in paragraphs:
        if id(p._p) in seen: continue
        seen.add(id(p._p))
        for match in reversed(list(re.finditer(r'\{\{([\w.-]+)\}\}',p.text))):
            start,end=match.span(); offset=0; inserted=False
            for run in p.runs:
                text=run.text; a,b=offset,offset+len(text); offset=b
                if b<=start or a>=end: continue
                left=text[:max(0,start-a)]; right=text[max(0,end-a):] if end<b else ''
                run.text=left+(str(fields[match.group(1)]) if not inserted else '')+right
                inserted=True
            if not inserted: raise ValueError('Unsupported template structure; requires manual editing')
    output.parent.mkdir(parents=True,exist_ok=True); doc.save(output)
    return {'output':str(output),'status':'DRAFT - render and inspect all pages before issue'}

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--workspace',default=None); sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('register'); p.add_argument('file'); p.add_argument('--category',required=True); p.add_argument('--status',choices=['draft','approved','superseded'],default='draft'); p.add_argument('--reference',required=True)
    p=sub.add_parser('search'); p.add_argument('query'); p.add_argument('--approved-only',action='store_true')
    p=sub.add_parser('calc'); p.add_argument('spec')
    p=sub.add_parser('remember'); p.add_argument('text'); p.add_argument('--source',required=True); p.add_argument('--approved',action='store_true',help='Use only for explicit user approval/standing instructions')
    p=sub.add_parser('task'); p.add_argument('instruction')
    p=sub.add_parser('fill'); p.add_argument('template'); p.add_argument('fields'); p.add_argument('output')
    a=parser.parse_args()
    root=workspace_lib.resolve_root('sales',workspace=a.workspace) if a.workspace else ROOT
    needs_root = a.command in {'register','search','remember','task'}
    if needs_root and root is None:
        print(json.dumps({'error':workspace_lib.unresolved_message('sales',workspace=a.workspace)}),file=sys.stderr); sys.exit(2)
    try:
        if a.command=='register': r=register(root,Path(a.file),a.category,a.status,a.reference)
        elif a.command=='search': r=search(root,a.query,a.approved_only)
        elif a.command=='calc': r=calculate(json.loads(Path(a.spec).read_text()))
        elif a.command=='remember': r=remember(root,a.text,a.source,a.approved)
        elif a.command=='task': r=task(root,a.instruction)
        else: r=fill_template(a.template,a.output,json.loads(Path(a.fields).read_text()))
        print(json.dumps(r,indent=2,ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr); sys.exit(1)
if __name__=='__main__': main()
