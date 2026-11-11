#!/usr/bin/env python3
"""Build the Sinor products brochure (A4 HTML -> PDF via Node Playwright).
Input : catalogue_final.json  (list of items, see merge step)
        img_ready/<id>.jpg     (optional product photos)
Output: brochure.html, brochure.pdf
No em dashes anywhere in generated text.
"""
import json, os, html, base64, subprocess, sys, re

W = '/tmp/work/products-brochure'
LOGO = '/home/user/Marketing-Team/assets/brand/sinor-logo-transparent.png'
items = json.load(open(f'{W}/catalogue_final.json'))
for _i in items:
    _i['official_name'] = _i.get('display_name') or _i.get('official_name') or _i['name']
    _i['brand_shown'] = _i.get('display_brand') or _i.get('brand_shown') or _i['brand']
byid = {i['id']: i for i in items}

SECTIONS = [
    ('A', 'Package systems', 'Complete systems supplied, installed and supported as one scope.'),
    ('B', 'Position reference and sensors', 'Position reference sensors, transponders, motion, wind, heading and GNSS equipment.'),
    ('C', 'DP control, HMI and automation', 'Operator stations, displays, controllers, PLC and I/O, drives and networking.'),
    ('D', 'Power, spares and service kits', 'Service kits, power supplies, protection devices, cables and computers.'),
]
# components shown on package pages (ids of individual items)
PARTS = {
    'A01': ['B01', 'C04', 'C05', 'B05', 'D02'],
    'A02': ['B02', 'B03', 'C04', 'C05', 'D01'],
    'A03': ['D02'],
    'A04': ['B04', 'C04', 'C05'],
    'A06': ['B06', 'B07'],
    'A08': ['B08', 'B09', 'A10'],
    'A09': ['B10'],
    'A11': ['C01', 'C02', 'C03'],
    'A12': ['C03'],
    'A14': ['B16'],
    'A15': ['B16'],
}
e = html.escape


def b64(path):
    ext = os.path.splitext(path)[1].lower().strip('.')
    mime = 'png' if ext == 'png' else 'jpeg'
    return f'data:image/{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


LOGO_URI = b64(LOGO)


def photo(i, cls='ph'):
    p = f'{W}/img_ready/{i["id"]}.jpg'
    if os.path.exists(p):
        return f'<div class="{cls}"><img src="{b64(p)}"></div>'
    return f'<div class="{cls} missing"><span>Product photo<br>to be supplied</span></div>'


def clean(t):
    return (t or '').replace('—', ', ').replace('–', '-').strip()


def short(t, n):
    t = clean(t)
    if len(t) <= n:
        return t
    out = ''
    for sent in re.split(r'(?<=[.!?])\s+', t):
        if len(out) + len(sent) + 1 > n:
            break
        out = (out + ' ' + sent).strip()
    if out:
        return out
    cut = t[:n].rsplit(' ', 1)[0].rstrip(',;:')
    return cut + '.'


def specs_html(i, k=4):
    sp = i.get('specs') or []
    feats = i.get('features') or []
    rows = ''
    for s in sp[:k]:
        rows += f'<li><b>{e(clean(s["k"]))}</b> {e(clean(s["v"]))}</li>'
    if not rows:
        for f in feats[:k]:
            rows += f'<li>{e(short(f, 70))}</li>'
    return f'<ul class="sp">{rows}</ul>' if rows else ''


def card(i):
    models = clean(i.get('model_hint', ''))
    return f'''<div class="card">
  {photo(i)}
  <div class="meta"><span class="id">{i["id"]}</span><span class="brand">{e(clean(i.get("brand_shown") or i["brand"]))}</span></div>
  <h3>{e(clean(i.get("official_name") or i["name"]))}</h3>
  <p>{e(short(i.get("description") or "", 230))}</p>
  {specs_html(i, 3)}
  <div class="models"><b>Supplied models</b> {e(short(models, 110))}</div>
</div>'''


def package(i):
    parts = ''.join(
        f'<span class="chip">{pid} {e(short(byid[pid].get("official_name") or byid[pid]["name"], 38))}</span>'
        for pid in PARTS.get(i['id'], []) if pid in byid)
    feats = ''.join(f'<li>{e(short(f, 80))}</li>' for f in (i.get('features') or [])[:4])
    return f'''<div class="pkg">
  {photo(i, 'ph big')}
  <div class="pbody">
    <div class="meta"><span class="id">{i["id"]}</span><span class="brand">{e(clean(i.get("brand_shown") or i["brand"]))}</span></div>
    <h2>{e(clean(i.get("official_name") or i["name"]))}</h2>
    <p>{e(short(i.get("description") or "", 330))}</p>
    {('<ul class="fe">' + feats + '</ul>') if feats else ''}
    <div class="models"><b>Supplied configuration</b> {e(short(clean(i.get("model_hint", "")), 170))}</div>
    {('<div class="parts"><b>Components listed separately</b><div>' + parts + '</div></div>') if parts else ''}
  </div>
</div>'''


CSS = '''
@page { size: 210mm 297mm; margin: 0 }
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#06111f;--bg2:#0a1a2f;--card:#081526;--line:#173452;--cy:#5bc0eb;--tx:#e8f1f8;--mu:#8fb0c9;--bl:#0d4a85}
html{font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:var(--tx)}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;
  background:radial-gradient(1200px 700px at 85% -10%,#0f2a4a 0%,transparent 60%),linear-gradient(180deg,var(--bg2),var(--bg));
  padding:16mm 13mm 14mm}
.page:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(91,192,235,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(91,192,235,.045) 1px,transparent 1px);background-size:8mm 8mm;pointer-events:none}
.hd{position:absolute;left:13mm;right:13mm;top:7mm;display:flex;justify-content:space-between;align-items:center;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--cy)}
.hd .lg{background:#fff;border-radius:2mm;padding:.7mm 2mm;display:flex;align-items:center}.hd .lg img{height:6.2mm}
.ft{position:absolute;left:13mm;right:13mm;bottom:6mm;display:flex;justify-content:space-between;font-size:6.2pt;color:var(--mu);border-top:.2mm solid var(--line);padding-top:2mm}
h1,h2,h3{font-weight:650;letter-spacing:-.01em}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:4mm}
.card{background:var(--card);border:.2mm solid var(--line);border-radius:2.2mm;padding:2.6mm;height:81mm;overflow:hidden;display:flex;flex-direction:column}
.ph{background:#fff;border-radius:1.4mm;height:33mm;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph img{max-width:100%;max-height:100%;object-fit:contain}
.ph.big{height:50mm;width:58mm;flex:none}
.ph.missing{background:repeating-linear-gradient(45deg,#0d2036,#0d2036 3mm,#0a1a2f 3mm,#0a1a2f 6mm);color:var(--mu);font-size:7pt;text-align:center;letter-spacing:.06em;text-transform:uppercase;border:.2mm dashed var(--line)}
.meta{display:flex;gap:2mm;align-items:center;margin-top:2.2mm}
.id{font-size:6pt;font-weight:700;color:#06111f;background:var(--cy);border-radius:.9mm;padding:.3mm 1.3mm}
.brand{font-size:6.4pt;color:var(--cy);letter-spacing:.08em;text-transform:uppercase}
.card h3{font-size:9pt;line-height:1.15;margin-top:1mm;color:#fff}
.card p{font-size:7pt;line-height:1.32;color:var(--mu);margin-top:1mm}
.sp{list-style:none;margin-top:1.1mm}.sp li{font-size:6.5pt;color:var(--tx);line-height:1.3;padding-left:2mm;position:relative}
.sp li:before{content:"";position:absolute;left:0;top:1.1mm;width:.9mm;height:.9mm;background:var(--cy);border-radius:50%}
.sp b{color:var(--cy);font-weight:600}
.models{margin-top:auto;font-size:6pt;color:var(--mu);border-top:.2mm solid var(--line);padding-top:1.2mm;line-height:1.3}.models b{color:var(--cy);letter-spacing:.06em;text-transform:uppercase;margin-right:1mm}
.sech{margin-top:2mm}.sech .lab{font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)}.sech h1{font-size:19pt;margin-top:1mm;color:#fff}.sech p{font-size:8pt;color:var(--mu);margin-top:1mm;max-width:130mm}
.pkg{display:flex;gap:5mm;background:var(--card);border:.2mm solid var(--line);border-radius:2.4mm;padding:3mm;height:81mm;margin-top:3.5mm;overflow:hidden}
.pbody{flex:1;display:flex;flex-direction:column;min-width:0}
.pbody h2{font-size:11.5pt;line-height:1.15;color:#fff;margin-top:1.4mm}
.pbody p{font-size:7.8pt;line-height:1.4;color:var(--mu);margin-top:1.6mm}
.fe{list-style:none;margin-top:1.6mm}.fe li{font-size:7.2pt;color:var(--tx);line-height:1.35;padding-left:2.4mm;position:relative}.fe li:before{content:"";position:absolute;left:0;top:1.3mm;width:1mm;height:1mm;background:var(--cy);border-radius:50%}
.parts{margin-top:auto}.parts b{font-size:6pt;color:var(--cy);letter-spacing:.08em;text-transform:uppercase}.parts div{display:flex;flex-wrap:wrap;gap:1.2mm;margin-top:1mm}
.chip{font-size:6pt;border:.2mm solid var(--line);color:var(--tx);border-radius:5mm;padding:.5mm 2mm;background:#0c2038}
.pbody .models{margin-top:2mm}
.toc{margin-top:6mm}.toc .row{display:flex;gap:4mm;align-items:baseline;border-bottom:.2mm solid var(--line);padding:2.1mm 0}.toc .n{font-size:15pt;color:var(--cy);width:11mm;font-weight:650}.toc .t{flex:1}.toc .t b{font-size:10.5pt;color:#fff}.toc .t span{display:block;font-size:7.2pt;color:var(--mu);margin-top:.6mm}.toc .p{font-size:9pt;color:var(--tx)}
.idx{columns:3;column-gap:6mm;margin-top:4mm;font-size:6.6pt;line-height:1.55}.idx div{break-inside:avoid;display:flex;justify-content:space-between;gap:2mm;border-bottom:.15mm solid #10283f}.idx span{color:var(--mu)}.idx b{color:var(--cy);font-weight:600;margin-right:1mm}
.cover{padding:0}.cover .ct{position:absolute;left:16mm;right:16mm;top:92mm}
.cover .big{font-size:33pt;line-height:1.05;color:#fff;font-weight:700;letter-spacing:-.02em}.cover .big em{font-style:normal;color:var(--cy)}
.cover .lab{font-size:7.6pt;letter-spacing:.22em;color:var(--cy);text-transform:uppercase}
.cover .sub{font-size:10pt;color:var(--mu);margin-top:5mm;max-width:130mm;line-height:1.5}
.cover .lg{position:absolute;left:16mm;top:16mm;background:#fff;border-radius:2.6mm;padding:1.6mm 3.4mm}.cover .lg img{height:13mm;display:block}
.cover .tag{position:absolute;right:16mm;top:20mm;font-size:7pt;letter-spacing:.2em;color:var(--cy);text-transform:uppercase}
.cover .mont{position:absolute;left:16mm;right:16mm;bottom:40mm;display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.cover .mont .ph{height:30mm}
.cover .bar{position:absolute;left:16mm;right:16mm;bottom:14mm;border:.2mm solid var(--line);border-radius:2mm;padding:3mm 4mm;display:flex;justify-content:space-between;font-size:7pt;color:var(--mu);background:rgba(8,21,38,.8)}.cover .bar b{display:block;color:#fff;font-size:8pt;margin-top:.6mm}
.back .ct{position:absolute;left:16mm;right:16mm;top:70mm}.back h1{font-size:26pt;line-height:1.1;color:#fff}.back h1 em{font-style:normal;color:var(--cy)}
.back .cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:14mm}.back .cols b{display:block;font-size:6.6pt;letter-spacing:.18em;text-transform:uppercase;color:var(--cy);margin-bottom:1.6mm}.back .cols div{font-size:9pt;line-height:1.55;color:var(--tx)}
.disc{position:absolute;left:16mm;right:16mm;bottom:20mm;font-size:6.2pt;line-height:1.5;color:var(--mu);border-top:.2mm solid var(--line);padding-top:3mm}
'''


def page(inner, label, no, extra_cls=''):
    return f'''<section class="page {extra_cls}">
<div class="hd"><span class="lg"><img src="{LOGO_URI}"></span><span>{e(label)}</span></div>
{inner}
<div class="ft"><span>Sinor Marine Services Middle East FZCO &middot; Products Catalogue 2026</span><span>sinormarine.com &nbsp;&middot;&nbsp; {no:02d}</span></div>
</section>'''


def build():
    pages = []  # (html_builder(no)->str, section_letter, label, item_ids)
    # cover handled separately (page 1); contents page 2
    seq = []  # list of (kind, payload)
    for letter, title, blurb in SECTIONS:
        its = [i for i in items if i['section'] == title or i['id'].startswith(letter)]
        its = sorted([i for i in items if i['id'].startswith(letter)], key=lambda x: x['id'])
        if not its:
            continue
        seq.append(('divider', (letter, title, blurb, len(its))))
        if letter == 'A':
            for k in range(0, len(its), 3):
                seq.append(('pkgpage', (letter, title, its[k:k + 3])))
        else:
            for k in range(0, len(its), 6):
                seq.append(('cardpage', (letter, title, its[k:k + 6])))
    first_no = 3
    nos = {}
    secstart = {}
    for n, (kind, pl) in enumerate(seq):
        no = first_no + n
        if kind == 'divider':
            secstart[pl[0]] = no
        else:
            for i in pl[2]:
                nos[i['id']] = no
    last_no = first_no + len(seq)
    idx_no = last_no  # item index page
    back_no = idx_no + (1 if len(items) > 0 else 0)

    out = []
    # cover
    mont = ''.join(photo(byid[x]) for x in ['A01', 'A09', 'B11', 'A02'] if x in byid)
    out.append(f'''<section class="page cover">
<div class="lg"><img src="{LOGO_URI}"></div><div class="tag">Edition 2026</div>
<div class="ct"><div class="lab">Sinor Marine Services Middle East FZCO</div>
<div class="big">Products<br><em>Catalogue</em></div>
<div class="sub">Package systems, equipment and spares for dynamic positioning, position reference, marine automation and electrical systems. Supplied, installed and supported from Dubai.</div></div>
<div class="mont">{mont}</div>
<div class="bar"><div>Head office<b>Dubai, UAE</b></div><div>Sales<b>sales@sinormarine.com</b></div><div>Phone<b>+971 4 665 7162</b></div><div>Web<b>sinormarine.com</b></div></div>
</section>''')
    # contents
    rows = ''
    for letter, title, blurb in SECTIONS:
        n_items = len([i for i in items if i['id'].startswith(letter)])
        if n_items:
            rows += f'<div class="row"><div class="n">{letter}</div><div class="t"><b>{e(title)}</b><span>{e(blurb)} ({n_items} items)</span></div><div class="p">p. {secstart[letter]:02d}</div></div>'
    toc = f'''<div class="sech"><div class="lab">Contents</div><h1>How to use this catalogue</h1>
<p>Section A shows complete package systems. Sections B, C and D show the individual items, so any component or spare can be ordered on its own. Every card carries a reference (for example B02) that you can quote in an enquiry. Photos and descriptions are drawn from the manufacturers' published information; the supplied models line lists the variants Sinor handles.</p></div>
<div class="toc">{rows}<div class="row"><div class="n">i</div><div class="t"><b>Item index</b><span>Every reference with its page number.</span></div><div class="p">p. {idx_no:02d}</div></div></div>'''
    out.append(page(toc, 'Contents', 2))
    for n, (kind, pl) in enumerate(seq):
        no = first_no + n
        if kind == 'divider':
            letter, title, blurb, cnt = pl
            inner = f'<div class="sech" style="margin-top:70mm"><div class="lab">Section {letter}</div><h1 style="font-size:30pt">{e(title)}</h1><p style="font-size:10pt">{e(blurb)}</p><p style="margin-top:6mm;color:var(--cy)">{cnt} items</p></div>'
            out.append(page(inner, f'Section {letter}', no))
        elif kind == 'pkgpage':
            letter, title, its = pl
            inner = f'<div class="sech"><div class="lab">{letter} &middot; {e(title)}</div></div>' + ''.join(package(i) for i in its)
            out.append(page(inner, title, no))
        else:
            letter, title, its = pl
            inner = f'<div class="sech"><div class="lab">{letter} &middot; {e(title)}</div></div><div class="grid">' + ''.join(card(i) for i in its) + '</div>'
            out.append(page(inner, title, no))
    # index page
    idx = ''.join(f'<div><span><b>{i["id"]}</b>{e(short(i.get("official_name") or i["name"], 44))}</span><span>{nos.get(i["id"], 0):02d}</span></div>' for i in sorted(items, key=lambda x: x['id']))
    out.append(page(f'<div class="sech"><div class="lab">Index</div><h1>Item index</h1></div><div class="idx">{idx}</div>', 'Index', idx_no))
    # back
    disc = ('Product names, logos and trademarks belong to their respective owners and are used here only to identify the products supplied. '
            'Descriptions and specifications are taken from manufacturers\' published information and may change; confirm current data with Sinor before ordering. '
            'Sinor Marine Services Middle East FZCO supplies and supports the products listed as an independent company unless a specific authorisation is stated in writing. '
            'Availability, lead times and prices are quoted per enquiry.')
    out.append(f'''<section class="page back"><div class="hd"><span class="lg"><img src="{LOGO_URI}"></span><span>Get in touch</span></div>
<div class="ct"><h1>Tell us the item.<br><em>We will quote it.</em></h1>
<div class="cols"><div><b>Head office</b>Sinor Marine Services Middle East FZCO<br>601, Al Nokitha Building, Hamariya Port<br>P.O. Box 95842, Dubai, UAE</div>
<div><b>Contact</b>sales@sinormarine.com<br>support@sinormarine.com<br>+971 4 665 7162<br>sinormarine.com</div></div></div>
<div class="disc">{e(disc)}</div></section>''')
    doc = f'<!doctype html><html><head><meta charset="utf-8"><title>Sinor Products Catalogue 2026</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>'
    open(f'{W}/brochure.html', 'w').write(doc)
    return len(out)


if __name__ == '__main__':
    n = build()
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{W}/brochure.html');await p.waitForTimeout(800);"
          f"await p.pdf({{path:'{W}/brochure.pdf',width:'210mm',height:'297mm',printBackground:true,preferCSSPageSize:true}});await b.close();}})()")
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, cwd='/tmp')
    print('pages', n, 'rc', r.returncode, r.stderr[-300:])
