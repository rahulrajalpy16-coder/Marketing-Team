#!/usr/bin/env python3
"""Sinor products catalogue v2: A4 HTML -> PDF (Node Playwright).
Order (Rahul, 2026-11-11): DP Systems, Position Reference Systems, Position Reference Sensors,
Control/HMI/communication/automation, Power/spares/service kits.
Reads catalogue_v2.json (make_v2.py) and img_ready/<old_id>.jpg. No em dashes in generated text.
"""
import json, os, html, base64, subprocess, re, sys

W = '/tmp/work/products-brochure'
LOGO = '/home/user/Marketing-Team/assets/brand/sinor-logo-transparent.png'
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else 'brochure_v2'
items = json.load(open(f'{W}/catalogue_v2.json'))
for _i in items:
    _i['name_show'] = _i.get('display_name') or _i['name']
    _i['brand_show'] = _i.get('display_brand') or _i['brand']
e = html.escape

SECTIONS = {
    'DP': ('DP Systems', 'Complete dynamic positioning systems from NAVIS Engineering and Marine Technologies, supplied and supported by Sinor.'),
    'PR': ('Position Reference Systems', 'Radar, laser, acoustic, taut wire and GNSS reference systems that tell the DP system where the vessel is.'),
    'SN': ('Position Reference Sensors', 'Motion reference units, gyro compass, wind sensors and GNSS antennas that feed the DP system.'),
    'CA': ('Control, HMI and automation', 'Operator displays and joysticks, controllers, PLC and I/O, drives, networking, communication and signalling.'),
    'SP': ('Power, spares and service kits', 'Service kits, power supplies, protection devices, cables and computers.'),
}
ORDER = ['DP', 'PR', 'SN', 'CA', 'SP']


def b64(path):
    ext = os.path.splitext(path)[1].lower().strip('.')
    return f'data:image/{"png" if ext == "png" else "jpeg"};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


LOGO_URI = b64(LOGO)


def clean(t):
    return (t or '').replace('—', ', ').replace('–', '-').strip()


def short(t, n):
    t = clean(t)
    if len(t) <= n:
        return t
    out = ''
    for s in re.split(r'(?<=[.!?])\s+', t):
        if len(out) + len(s) + 1 > n:
            break
        out = (out + ' ' + s).strip()
    return out or t[:n].rsplit(' ', 1)[0].rstrip(',;:') + '.'


def photo(i, cls='ph'):
    p = f'{W}/img_ready/{i["old_id"]}.jpg'
    if os.path.exists(p):
        return f'<div class="{cls}"><img src="{b64(p)}"></div>'
    return f'<div class="{cls} missing"><span>Photo<br>to follow</span></div>'


def has_photo(i):
    return os.path.exists(f'{W}/img_ready/{i["old_id"]}.jpg')


def legacy(i):
    return '<span class="legt">Legacy spare</span>' if i.get('legacy') else ''


def meta(i, show_group=True):
    g = f'<span class="grp">{e(i["group"])}</span>' if show_group else ''
    return f'<div class="meta"><span class="id">{i["ref"]}</span><span class="brand">{e(clean(i["brand_show"]))}</span>{legacy(i)}{g}</div>'


def specs_html(i, k=3):
    rows = ''.join(f'<li><b>{e(clean(s["k"]))}</b> {e(clean(s["v"]))}</li>' for s in (i.get('specs') or [])[:k])
    if not rows:
        rows = ''.join(f'<li>{e(short(f, 70))}</li>' for f in (i.get('features') or [])[:k])
    return f'<ul class="sp">{rows}</ul>' if rows else ''


def card(i):
    return f'''<div class="card">{photo(i)}{meta(i)}<h3>{e(clean(i["name_show"]))}</h3>
<p>{e(short(i.get("description"), 230))}</p>{specs_html(i, 3)}
<div class="models"><b>Supplied models</b> {e(short(clean(i.get("model_hint", "")), 110))}</div></div>'''


def wide(i):
    feats = ''.join(f'<li>{e(short(f, 80))}</li>' for f in (i.get('features') or [])[:4])
    return f'''<div class="pkg">{photo(i, 'ph big')}<div class="pbody">{meta(i)}
<h2>{e(clean(i["name_show"]))}</h2><p>{e(short(i.get("description"), 330))}</p>
{('<ul class="fe">' + feats + '</ul>') if feats else ''}
<div class="models"><b>Supplied configuration</b> {e(short(clean(i.get("model_hint", "")), 190))}</div></div></div>'''


# ---------- DP system pages (custom content, sources noted in sources/image_credits.csv) ----------
DP_EXTRA = {
    'A11': dict(
        cols=[('DP class 1 (DP1)', 'NavDP 4011 DP control unit with a NavDP 4001 independent joystick (IJ) unit. One DP operator station, one IJ station, mode selector, alarm printer and vertical reference sensors.'),
              ('DP class 2 (DP2)', 'NavDP 4022 DP control unit with a NavDP 4002 IJ unit. Two DP operator stations (DP A and DP B), alarm printers and vertical reference sensors.'),
              ('Upgrades and spares', 'Hardware and software upgrades of installed NAVIS systems, control computers, communication boxes, power unit with UPS, remote I/O units, third gyro interface and critical spares.')],
        scope=['Main control panel with joystick, display and control computer per station',
               'Sensor and reference interfaces for gyro, wind, vertical reference, DGPS, laser, radar, hydroacoustic and taut wire',
               'Thruster interfaces by dry contact, 4-20 mA and 0-10 V',
               'Installation, commissioning, DP trials and FMEA support by Sinor engineers']),
    'A12': dict(
        cols=[('DP 1', 'A single control computer, one operator station and separate I/O units for sensors, position references, power and thrusters. An independent joystick can be added.'),
              ('DP 2', 'Three control computers with majority voting, at least two operator stations and a dedicated I/O unit for each sensor set, reference system, power source and thruster.'),
              ('DP 3', 'Triple-redundant controllers and at least three operator stations, with a physically separate fire-safe compartment holding one control computer, one operator station and one sensor I/O unit.')],
        scope=['Integrated or stand-alone independent joystick system (IJS)',
               'DP console, UPS and DP network switch',
               'Upgrade of DP 1 to DP 2 using the same hardware modules, mid-life upgrades and critical spares',
               'Installation, commissioning, DP trials and FMEA support by Sinor engineers']),
}


def dp_page(i):
    x = DP_EXTRA.get(i['old_id'], dict(cols=[], scope=[]))
    cols = ''.join(f'<div class="col"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in x['cols'])
    scope = ''.join(f'<li>{e(s)}</li>' for s in x['scope'])
    feats = ''.join(f'<li>{e(short(f, 90))}</li>' for f in (i.get('features') or [])[:5])
    return f'''<div class="dp">{meta(i, False)}<h1>{e(clean(i["name_show"]))}</h1>
<div class="dprow">{photo(i, 'ph dpph')}<div class="dptx"><p>{e(short(i.get("description"), 460))}</p><ul class="fe">{feats}</ul></div></div>
<div class="lab2">System configurations</div><div class="cols3">{cols}</div>
<div class="lab2">Scope Sinor supplies</div><ul class="fe two">{scope}</ul>
<div class="models"><b>Supplied models</b> {e(short(clean(i.get("model_hint", "")), 200))}</div></div>'''


CSS = '''
@page { size: 210mm 297mm; margin: 0 }
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#06111f;--bg2:#0a1a2f;--card:#081526;--line:#173452;--cy:#5bc0eb;--tx:#e8f1f8;--mu:#8fb0c9}
html{font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:var(--tx)}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;
 background:radial-gradient(1200px 700px at 85% -10%,#0f2a4a 0%,transparent 60%),linear-gradient(180deg,var(--bg2),var(--bg));padding:16mm 13mm 14mm}
.page:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(91,192,235,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(91,192,235,.045) 1px,transparent 1px);background-size:8mm 8mm;pointer-events:none}
.hd{position:absolute;left:13mm;right:13mm;top:7mm;display:flex;justify-content:space-between;align-items:center;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--cy)}
.hd .lg{background:#fff;border-radius:2mm;padding:.7mm 2mm;display:flex;align-items:center}.hd .lg img{height:6.2mm}
.ft{position:absolute;left:13mm;right:13mm;bottom:6mm;display:flex;justify-content:space-between;font-size:6.6pt;color:var(--mu);border-top:.2mm solid var(--line);padding-top:2mm}
h1,h2,h3{font-weight:650;letter-spacing:-.01em}
.rows{display:flex;flex-direction:column;gap:3.5mm;margin-top:3mm}
.row{display:grid;gap:5mm;height:81mm}.row.w{grid-template-columns:1fr}.row.s{grid-template-columns:1fr 1fr}
.card{background:var(--card);border:.2mm solid var(--line);border-radius:2.2mm;padding:2.6mm;height:81mm;overflow:hidden;display:flex;flex-direction:column}
.ph{background:#fff;border-radius:1.4mm;height:33mm;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph img{max-width:100%;max-height:100%;object-fit:contain}
.ph.big{height:50mm;width:58mm;flex:none}
.ph.missing{background:repeating-linear-gradient(45deg,#0d2036,#0d2036 3mm,#0a1a2f 3mm,#0a1a2f 6mm);color:var(--mu);font-size:7pt;text-align:center;letter-spacing:.06em;text-transform:uppercase;border:.2mm dashed var(--line)}
.meta{display:flex;gap:2mm;align-items:center;margin-top:2.2mm}
.id{font-size:6pt;font-weight:700;color:#06111f;background:var(--cy);border-radius:.9mm;padding:.3mm 1.3mm;white-space:nowrap}
.brand{font-size:6.4pt;color:var(--cy);letter-spacing:.08em;text-transform:uppercase}
.grp{margin-left:auto;font-size:5.6pt;color:var(--mu);letter-spacing:.08em;text-transform:uppercase;text-align:right}
.legt{font-size:5.6pt;border:.2mm solid #f0b84a;color:#f0b84a;border-radius:.9mm;padding:.2mm 1.2mm;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.card h3{font-size:9pt;line-height:1.15;margin-top:1mm;color:#fff}
.card p{font-size:7.3pt;line-height:1.32;color:var(--mu);margin-top:1mm}
.sp{list-style:none;margin-top:1.1mm}.sp li{font-size:6.5pt;color:var(--tx);line-height:1.3;padding-left:2mm;position:relative}
.sp li:before{content:"";position:absolute;left:0;top:1.1mm;width:.9mm;height:.9mm;background:var(--cy);border-radius:50%}
.sp b{color:var(--cy);font-weight:600}
.models{margin-top:auto;font-size:6.3pt;color:var(--mu);border-top:.2mm solid var(--line);padding-top:1.2mm;line-height:1.3}.models b{color:var(--cy);letter-spacing:.06em;text-transform:uppercase;margin-right:1mm}
.sech .lab{font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)}
.pkg{display:flex;gap:5mm;background:var(--card);border:.2mm solid var(--line);border-radius:2.4mm;padding:3mm;height:81mm;overflow:hidden}
.pbody{flex:1;display:flex;flex-direction:column;min-width:0}
.pbody h2{font-size:11.5pt;line-height:1.15;color:#fff;margin-top:1.4mm}
.pbody p{font-size:7.8pt;line-height:1.4;color:var(--mu);margin-top:1.6mm}
.fe{list-style:none;margin-top:1.6mm}.fe li{font-size:7.2pt;color:var(--tx);line-height:1.35;padding-left:2.4mm;position:relative}.fe li:before{content:"";position:absolute;left:0;top:1.3mm;width:1mm;height:1mm;background:var(--cy);border-radius:50%}
.pbody .models{margin-top:auto}
.opener .big{font-size:30pt;color:#fff;margin-top:2mm}.opener .bl{font-size:10pt;color:var(--mu);margin-top:3mm;max-width:150mm;line-height:1.5}
.opener .g{margin-top:7mm}.opener .g h4{font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:var(--cy);font-weight:600;border-bottom:.2mm solid var(--line);padding-bottom:1.2mm;margin-bottom:1.2mm}
.opener .li{display:flex;gap:3mm;font-size:8.2pt;line-height:1.7;color:var(--tx)}.opener .li .r{width:14mm;color:var(--cy);font-weight:600}.opener .li .t{flex:1}.opener .li .p{color:var(--mu)}
.toc{margin-top:6mm}.toc .row2{display:flex;gap:4mm;align-items:baseline;border-bottom:.2mm solid var(--line);padding:2.4mm 0}.toc .n{font-size:15pt;color:var(--cy);width:11mm;font-weight:650}.toc .t{flex:1}.toc .t b{font-size:10.5pt;color:#fff}.toc .t span{display:block;font-size:7.4pt;color:var(--mu);margin-top:.6mm}.toc .p{font-size:9pt;color:var(--tx)}
.sechead h1{font-size:19pt;margin-top:1mm;color:#fff}.sechead p{font-size:8pt;color:var(--mu);margin-top:1mm;max-width:150mm;line-height:1.5}
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
.disc{position:absolute;left:16mm;right:16mm;bottom:20mm;font-size:6.4pt;line-height:1.5;color:var(--mu);border-top:.2mm solid var(--line);padding-top:3mm}
.dp h1{font-size:19pt;color:#fff;margin-top:1.5mm;line-height:1.1}
.dprow{display:flex;gap:6mm;margin-top:4mm}.dpph{height:62mm;width:84mm;flex:none}.dptx p{font-size:8.4pt;line-height:1.5;color:var(--mu)}
.lab2{font-size:7pt;letter-spacing:.18em;text-transform:uppercase;color:var(--cy);margin-top:6mm;border-bottom:.2mm solid var(--line);padding-bottom:1.2mm}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:3mm}.col{background:var(--card);border:.2mm solid var(--line);border-radius:2mm;padding:3mm;min-height:46mm}.col b{font-size:9.4pt;color:#fff}.col p{font-size:7.6pt;line-height:1.45;color:var(--mu);margin-top:1.6mm}
.fe.two{columns:2;column-gap:6mm;margin-top:2.6mm}.fe.two li{break-inside:avoid;margin-bottom:1.4mm;font-size:7.8pt}
.dp .models{margin-top:6mm;font-size:6.8pt}
'''


def page(inner, label, no, cls=''):
    return f'''<section class="page {cls}"><div class="hd"><span class="lg"><img src="{LOGO_URI}"></span><span>{e(label)}</span></div>
{inner}<div class="ft"><span>Sinor Marine Services Middle East FZCO &middot; Products Catalogue 2026</span><span>sinormarine.com &nbsp;&middot;&nbsp; {no:02d}</span></div></section>'''


def layout():
    """return list of page descriptors in order after cover and contents"""
    pages = []
    for sec in ORDER:
        its = [i for i in items if i['section'] == sec]
        if not its:
            continue
        pages.append(('opener', sec, None))
        if sec == 'DP':
            for i in [x for x in its if x['style'] == 'dp']:
                pages.append(('dp', sec, [i]))
            rest = [x for x in its if x['style'] != 'dp']
        else:
            rest = its
        rows = []
        cur = None
        for i in rest:
            kind = 'w' if i['style'] == 'wide' else 's'
            cap = 1 if kind == 'w' else 2
            if cur and cur[0] == kind and len(cur[1]) < cap:
                cur[1].append(i)
            else:
                cur = (kind, [i]); rows.append(cur)
        for k in range(0, len(rows), 3):
            pages.append(('flow', sec, rows[k:k + 3]))
    return pages


def build():
    pgs = layout()
    first = 3
    pageno = {}
    secpage = {}
    for n, (kind, sec, pl) in enumerate(pgs):
        no = first + n
        if kind == 'opener':
            secpage[sec] = no
        elif kind == 'dp':
            for i in pl:
                pageno[i['ref']] = no
        else:
            for kd, its in pl:
                for i in its:
                    pageno[i['ref']] = no
    idx_no = first + len(pgs)
    back_no = idx_no + 1
    out = []
    mont_ids = [x for x in ['A01', 'A09', 'B11', 'A02'] if os.path.exists(f'{W}/img_ready/{x}.jpg')]
    mont = ''.join(f'<div class="ph"><img src="{b64(f"{W}/img_ready/{x}.jpg")}"></div>' for x in mont_ids)
    out.append(f'''<section class="page cover"><div class="lg"><img src="{LOGO_URI}"></div><div class="tag">Edition 2026</div>
<div class="ct"><div class="lab">Sinor Marine Services Middle East FZCO</div><div class="big">Products<br><em>Catalogue</em></div>
<div class="sub">DP systems, position reference systems and sensors, control and automation equipment, and spares. Supplied and supported from Dubai.</div></div>
<div class="mont">{mont}</div>
<div class="bar"><div>Head office<b>Dubai, UAE</b></div><div>Sales<b>sales@sinormarine.com</b></div><div>Phone<b>+971 4 665 7162</b></div><div>Web<b>sinormarine.com</b></div></div></section>''')
    rows = ''
    for k, sec in enumerate(ORDER, 1):
        n_it = len([i for i in items if i['section'] == sec])
        if n_it:
            t, b = SECTIONS[sec]
            rows += f'<div class="row2"><div class="n">{k}</div><div class="t"><b>{e(t)}</b><span>{e(b)} ({n_it} items)</span></div><div class="p">p. {secpage[sec]:02d}</div></div>'
    rows += f'<div class="row2"><div class="n">i</div><div class="t"><b>Item index</b><span>Every reference with its page number.</span></div><div class="p">p. {idx_no:02d}</div></div>'
    toc = f'''<div class="sechead"><div class="lab" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)">Contents</div><h1>How to use this catalogue</h1>
<p>The catalogue follows the DP system from the top: DP systems first, then the position reference systems that feed them, then the sensors, then control and automation equipment, then spares. Each card carries a reference (for example PR-03) that you can quote in an enquiry. Photos and descriptions are drawn from manufacturer and distributor published information; the supplied models line lists the variants Sinor handles. Photos are for identification and the delivered item may differ in detail.</p></div><div class="toc">{rows}</div>'''
    out.append(page(toc, 'Contents', 2))
    for n, (kind, sec, pl) in enumerate(pgs):
        no = first + n
        title, blurb = SECTIONS[sec]
        if kind == 'opener':
            k = ORDER.index(sec) + 1
            groups = []
            for i in [x for x in items if x['section'] == sec]:
                if not groups or groups[-1][0] != i['group']:
                    groups.append((i['group'], []))
                groups[-1][1].append(i)
            gh = ''
            for g, its in groups:
                lis = ''.join(f'<div class="li"><span class="r">{i["ref"]}</span><span class="t">{e(clean(i["name_show"]))}</span><span class="p">p. {pageno[i["ref"]]:02d}</span></div>' for i in its)
                gh += f'<div class="g"><h4>{e(g)}</h4>{lis}</div>'
            inner = f'<div class="opener" style="margin-top:14mm"><div class="sech"><div class="lab">Section {k}</div></div><h1 class="big">{e(title)}</h1><p class="bl">{e(blurb)}</p>{gh}</div>'
            out.append(page(inner, f'Section {k}', no))
        elif kind == 'dp':
            out.append(page(f'<div class="sech" style="margin-bottom:2mm"><div class="lab">{e(title)}</div></div>' + dp_page(pl[0]), title, no))
        else:
            body = ''
            for kd, its in pl:
                body += f'<div class="row {kd}">' + ''.join(wide(i) if kd == 'w' else card(i) for i in its) + '</div>'
            inner = f'<div class="sech"><div class="lab">{e(title)}</div></div><div class="rows">{body}</div>'
            out.append(page(inner, title, no))
    idx = ''.join(f'<div><span><b>{i["ref"]}</b>{e(short(i["name_show"], 44))}</span><span>{pageno[i["ref"]]:02d}</span></div>' for i in items)
    out.append(page(f'<div class="sechead"><div class="lab" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)">Index</div><h1>Item index</h1></div><div class="idx">{idx}</div>', 'Index', idx_no))
    disc = ("Product names, logos and trademarks belong to their respective owners and are used here only to identify the products supplied. "
            "Descriptions and specifications are taken from manufacturer and distributor published information and may change; confirm current data with Sinor before ordering. "
            "Sinor Marine Services Middle East FZCO supplies and supports the products listed as an independent company unless a specific authorisation is stated in writing. "
            "Availability, lead times and prices are quoted per enquiry.")
    out.append(f'''<section class="page back"><div class="hd"><span class="lg"><img src="{LOGO_URI}"></span><span>Get in touch</span></div>
<div class="ct"><h1>Tell us the item.<br><em>We will quote it.</em></h1><div class="cols"><div><b>Head office</b>Sinor Marine Services Middle East FZCO<br>601, Al Nokitha Building, Hamariya Port<br>P.O. Box 95842, Dubai, UAE</div>
<div><b>Contact</b>sales@sinormarine.com<br>support@sinormarine.com<br>+971 4 665 7162<br>sinormarine.com</div></div></div><div class="disc">{e(disc)}</div></section>''')
    open(f'{W}/{OUTNAME}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Sinor Products Catalogue 2026</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>')
    return len(out)


if __name__ == '__main__':
    n = build()
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{W}/{OUTNAME}.html');await p.waitForTimeout(800);"
          f"await p.pdf({{path:'{W}/{OUTNAME}.pdf',width:'210mm',height:'297mm',printBackground:true,preferCSSPageSize:true}});await b.close();}})()")
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, cwd='/tmp')
    print('pages', n, 'rc', r.returncode, r.stderr[-300:])
