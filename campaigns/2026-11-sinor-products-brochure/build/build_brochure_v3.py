#!/usr/bin/env python3
"""Sinor products catalogue v3: each system shown as a tree of everything that comes with it.
Audience: non-technical client teams. Reuses helpers and CSS of build_brochure_v2.
"""
import json, os, re, subprocess, sys, importlib.util

W = '/tmp/work/products-brochure'
sys.argv = [sys.argv[0]] + (sys.argv[1:] or ['brochure_v3'])
OUTNAME = sys.argv[1]
spec = importlib.util.spec_from_file_location('v2', f'{W}/build_brochure_v2.py')
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
spec2 = importlib.util.spec_from_file_location('sy', f'{W}/systems_v3.py')
sy = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(sy)
spec3 = importlib.util.spec_from_file_location('pn', f'{W}/plain_notes.py')
pn = importlib.util.module_from_spec(spec3); spec3.loader.exec_module(pn)
e, clean, short, b64, LOGO_URI = v2.e, v2.clean, v2.short, v2.b64, v2.LOGO_URI
items = json.load(open(f'{W}/catalogue_v3.json'))

SECTIONS = {
    'DP': ('DP Systems', 'Dynamic Positioning systems keep a ship exactly where it needs to be. Here are the two systems we supply, with everything that comes with them.'),
    'PR': ('Position Reference Systems', 'These systems tell the DP system where the ship is. Each page shows the system and the equipment that comes with it, so you can see at a glance what you are buying and what we can support.'),
    'SN': ('Position Reference Sensors', 'Sensors that feed the DP system: motion, heading, wind and satellite antennas. They can be added to any system.'),
    'CA': ('Control, screens and automation', 'Operator screens, joysticks, controllers, drives and networking equipment around the DP and automation systems.'),
    'SP': ('Power, spares and service kits', 'Service kits, power supplies, protection devices, cables and computers kept ready as spares.'),
}
ORDER = ['DP', 'PR', 'SN', 'CA', 'SP']

ICONS = {
 'sensor': '<path d="M4 15a8 8 0 0 1 16 0z"/><path d="M3 18h18M9 21h6"/>',
 'computer': '<rect x="4" y="5" width="16" height="11" rx="1"/><path d="M9 20h6M12 16v4"/>',
 'monitor': '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4"/>',
 'keyboard': '<rect x="3" y="7" width="18" height="10" rx="1"/><path d="M6 10h1M9 10h1M12 10h1M15 10h1M18 10h0M7 14h10"/>',
 'mouse': '<circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 'beacon': '<circle cx="12" cy="13" r="3"/><path d="M7 8a7 7 0 0 0 0 10M17 8a7 7 0 0 1 0 10M4 5a11 11 0 0 0 0 16M20 5a11 11 0 0 1 0 16"/>',
 'prism': '<path d="M12 3l8 6-8 12L4 9z"/><path d="M4 9h16M12 3v18"/>',
 'cable': '<path d="M3 17c4 0 4-10 9-10s5 10 9 10"/><circle cx="3" cy="17" r="1.5"/><circle cx="21" cy="17" r="1.5"/>',
 'tool': '<path d="M14 6a4 4 0 0 0 5 5l-9 9a2 2 0 0 1-3-3l9-9z"/>',
 'box': '<path d="M3 8l9-5 9 5v9l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v9"/>',
 'power': '<path d="M13 2L5 14h6l-1 8 8-12h-6z"/>',
 'document': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 'card': '<rect x="4" y="6" width="16" height="12" rx="1"/><path d="M8 10h3v4H8zM14 10h2M14 14h2"/>',
 'antenna': '<path d="M12 21V9M8 21h8"/><path d="M7 6a7 7 0 0 1 10 0M4 3a11 11 0 0 1 16 0"/>',
 'network': '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v5M12 12l-6 5M12 12l6 5"/>',
 'joystick': '<circle cx="12" cy="6" r="3"/><path d="M12 9v6"/><rect x="5" y="15" width="14" height="5" rx="1"/>',
 'compass': '<circle cx="12" cy="12" r="9"/><path d="M15 9l-2 6-4 0 2-6z"/>',
 'wind': '<path d="M3 9h11a3 3 0 1 0-3-3M3 15h15a3 3 0 1 1-3 3M3 12h7"/>',
 'software': '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13 6l-2 12"/>',
 'support': '<path d="M5 14v-2a7 7 0 0 1 14 0v2"/><rect x="3" y="14" width="4" height="6" rx="1"/><rect x="17" y="14" width="4" height="6" rx="1"/><path d="M19 20a4 4 0 0 1-4 2h-2"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="#5bc0eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, ICONS["box"])}</svg>'


def leaf(l):
    nm, note, img, ic, pno = l
    p = f'{W}/img_ready/{img}.jpg' if img else ''
    if img and os.path.exists(p):
        vis = f'<div class="lp ph2"><img src="{b64(p)}"></div>'
    else:
        vis = f'<div class="lp ic">{icon(ic)}</div>'
    pn_html = (f'<div class="lno">{e(pno[1:])}</div>' if pno.startswith('~') else f'<div class="lno">Part no. {e(pno)}</div>') if pno else ''
    return f'<div class="leaf"><div class="lh">{vis}<b>{e(clean(nm))}</b></div><span class="ln">{e(clean(note))}</span>{pn_html}</div>'


def tree(s, big=False, cfg=''):
    groups = s['groups']
    n = len(groups)
    cols = ''.join(f'<div class="g"><div class="gt">{e(g)}</div><div class="leaves">{"".join(leaf(x) for x in ls)}</div></div>' for g, ls in groups)
    sup = ''.join(f'<span class="chip">{e(x)}</span>' for x in sy.SUPPORT)
    ph = v2.photo({'old_id': s['img']}, 'ph hero' + (' big' if big else ''))
    return f'''<div class="tree {'tbig' if big else 'thalf'}"><div class="thead">{ph}<div class="tinfo">
<div class="meta"><span class="id">{s['ref']}</span><span class="brand">{e(clean(s['brand']))}</span></div>
<h2>{e(clean(s['name']))}</h2>
<div class="what"><b>What it does</b> {e(clean(s['what']))}</div><div class="plainx">{e(clean(s['plain']))}</div></div></div>
{cfg}
<div class="root"><span>{e(clean(s['name']))}: complete system</span></div>
<div class="groups" style="--n:{n}">{cols}</div>
<div class="sup"><b>Depending on the system, we can support you with</b>{sup}</div></div>'''


GL_HTML = '<div><b>Dynamic Positioning (DP)</b><span>Keeps a ship in one place, or moves it exactly where you want, by controlling the thrusters automatically.</span></div><div><b>DP class 1, 2 and 3</b><span>How much backup a DP system has. Higher classes can keep working after a failure; class 3 also separates parts physically, for example against fire.</span></div><div><b>Position reference system</b><span>Equipment that tells the DP system where the ship is: radar, laser, underwater sound, a wire to the seabed, or satellites.</span></div><div><b>Responder, transponder, reflector</b><span>A small coded beacon, or a set of mirror-like reflectors, placed on a platform or tool. The ship equipment looks for it and measures distance and direction.</span></div><div><b>Interrogator</b><span>The ship-side unit that asks transponders for their position and measures distance and direction (used in the RADius system).</span></div><div><b>USBL</b><span>An underwater positioning method. A unit under the hull uses sound to find transponders in the water.</span></div><div><b>ROV</b><span>Remotely operated underwater vehicle, a small robot submarine used for inspection and work below the surface.</span></div><div><b>GNSS and DGPS</b><span>Satellite positioning (GPS and similar systems). DGPS adds correction signals for better accuracy.</span></div><div><b>MRU (motion reference unit)</b><span>Measures how the ship moves: heave (up and down), roll (side to side tilt) and pitch (front to back tilt).</span></div><div><b>Gyro compass</b><span>A compass that finds true north without using magnetism, so it is not affected by the ship steel.</span></div><div><b>Taut wire</b><span>A weight on a wire is lowered to the seabed. The angle of the wire shows how the ship has moved.</span></div><div><b>IJ or IJS (independent joystick)</b><span>A separate backup joystick system with its own computer.</span></div><div><b>UPS</b><span>A battery backup that keeps equipment running if the power drops.</span></div><div><b>PLC and I/O</b><span>A programmable controller and its input and output cards, which read signals from sensors and switch equipment on and off.</span></div><div><b>HMI</b><span>The screen and controls a person uses to operate a system.</span></div><div><b>FMEA</b><span>A structured test of what happens if each part fails. It is used to prove a DP system to the class society.</span></div><div><b>Set-up and sea trial</b><span>Set-up means installing, configuring and testing equipment. A sea trial is a test with the ship at sea.</span></div><div><b>Spares and service kits</b><span>Parts that wear out, such as belts and seals, or that you keep on board in case of failure.</span></div>'

ICON_FOR = {'B05': 'beacon', 'B17': 'beacon', 'B15': 'compass', 'C04': 'monitor', 'C05': 'mouse', 'C08': 'joystick', 'C23': 'joystick',
            'C07': 'card', 'C09': 'card', 'C10': 'computer', 'C11': 'card', 'C13': 'computer', 'C17': 'power', 'D01': 'box', 'D02': 'box', 'D07': 'power'}


def photo3(i):
    p = f'{W}/img_ready/{i["old_id"]}.jpg'
    if os.path.exists(p):
        return f'<div class="ph"><img src="{b64(p)}"></div>'
    return f'<div class="ph icp">{icon(ICON_FOR.get(i["old_id"], "box"))}</div>'


def card3(i):
    pl = pn.PLAIN.get(i['old_id'], '')
    return f'''<div class="card">{photo3(i)}{v2.meta(i)}<h3>{e(clean(i["name_show"]))}</h3>
<p class="pl">{e(pl)}</p><p>{e(short(i.get("description"), 160))}</p>{v2.specs_html(i, 2)}
<div class="models"><b>Supplied models</b> {e(short(clean(i.get("model_hint", "")), 100))}</div></div>'''


CSS3 = v2.CSS + '''
.ph.icp{background:#0c2038;border:.2mm solid var(--line)}.ph.icp svg{width:17mm;height:17mm}
.gl{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:5mm}.gl div{background:var(--card);border:.2mm solid var(--line);border-radius:1.8mm;padding:2.4mm 3mm}.gl b{display:block;font-size:9pt;color:#fff}.gl span{display:block;font-size:7.8pt;line-height:1.4;color:#bcd2e4;margin-top:.8mm}
.id{font-size:6.6pt}.brand{font-size:6.8pt}.grp{font-size:6.2pt}.legt{font-size:6.2pt}.models{font-size:6.7pt}.disc{font-size:6.8pt}.what b{font-size:6.8pt}.card p{font-size:7.4pt;color:#bcd2e4}.card .pl{font-size:7.9pt}.sech{padding-top:2.5mm}.ft{font-size:6.8pt}
.opener .g2{margin-top:7mm}.opener .g2 h4{font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:var(--cy);font-weight:600;border-bottom:.2mm solid var(--line);padding-bottom:1.2mm;margin-bottom:1.2mm}
.tree{background:var(--card);border:.2mm solid var(--line);border-radius:2.4mm;padding:3mm;position:relative}
.thalf{margin-top:3.5mm;min-height:116mm}.tbig{margin-top:2mm}
.thead{display:flex;gap:4mm}.hero{height:40mm;width:54mm;flex:none}.hero.big{height:48mm;width:64mm}
.tinfo h2{font-size:13pt;color:#fff;margin-top:1.2mm;line-height:1.15}.tbig .tinfo h2{font-size:16pt}
.what{font-size:8pt;line-height:1.4;color:var(--tx);margin-top:1.4mm}.what b{color:var(--cy);font-size:6.2pt;letter-spacing:.1em;text-transform:uppercase;margin-right:1.2mm}
.tbig .what{font-size:9pt}
.plainx{font-size:7.6pt;line-height:1.4;color:var(--mu);margin-top:1.2mm}.tbig .plainx{font-size:8.4pt}
.root{position:relative;text-align:center;margin-top:3mm;height:7mm}.root span{display:inline-block;background:var(--cy);color:#06111f;font-weight:700;font-size:7pt;border-radius:5mm;padding:1.1mm 4mm}
.root:after{content:"";position:absolute;left:50%;top:6.3mm;height:2.2mm;border-left:.4mm solid #2a6ea6}
.groups{position:relative;display:grid;grid-template-columns:repeat(var(--n),1fr);gap:2.6mm;margin-top:2.2mm;padding-top:3mm}
.groups:before{content:"";position:absolute;top:0;left:calc(50% / var(--n));right:calc(50% / var(--n));border-top:.4mm solid #2a6ea6}
.g{position:relative;min-width:0}
.g:before{content:"";position:absolute;top:-3mm;left:50%;height:3mm;border-left:.4mm solid #2a6ea6}
.gt{font-size:7.2pt;font-weight:700;color:#fff;background:#0c2a4a;border:.25mm solid #2a6ea6;border-radius:1.4mm;text-align:center;padding:1mm 1mm;line-height:1.2}
.leaves{margin:1.4mm 0 0 2mm;padding-left:2mm;border-left:.4mm solid #2a6ea6}
.leaf{position:relative;margin:0 0 2.2mm 0}.lh{display:block;overflow:hidden;line-height:1.15;font-size:7pt}.lh .lp{float:left;margin-right:1.6mm}.lh b{font-size:7.8pt;color:#fff;line-height:1.2;overflow-wrap:break-word}.ln{display:block;clear:both;font-size:7.2pt;color:#bcd2e4;line-height:1.3;margin-top:.8mm}
.leaf:before{content:"";position:absolute;left:-2mm;top:4.2mm;width:2mm;border-top:.4mm solid #2a6ea6}
.lp{width:9.4mm;height:9.4mm;flex:none;border-radius:1.2mm;display:flex;align-items:center;justify-content:center;overflow:hidden}
.lp.ic{background:#0c2038;border:.2mm solid var(--line);padding:1.1mm}.lp.ic svg{width:100%;height:100%}
.lp.ph2{background:#fff}.lp.ph2 img{max-width:100%;max-height:100%;object-fit:contain}

.lno{font-size:6.5pt;color:var(--cy);margin-top:.4mm}.tbig .lp{width:9mm;height:9mm}.tbig .lh .lp{margin-right:1.2mm}.tbig .lh b{font-size:7.7pt}.tbig .ln{font-size:7.5pt}.tbig .lno{font-size:6.8pt}.tbig .gt{font-size:8.2pt;padding:1.6mm 1mm}.tbig .leaf{margin-bottom:2.4mm}.tbig .leaf:before{top:4.4mm}.tbig .groups{gap:3mm}
.sup{position:static;margin-top:4mm;display:flex;flex-wrap:wrap;gap:1.4mm;align-items:center;border-top:.2mm solid var(--line);padding-top:2.2mm}
.sup b{font-size:6.8pt;color:var(--cy);letter-spacing:.08em;text-transform:uppercase;margin-right:1mm}.chip{font-size:7pt;border:.25mm solid #2a6ea6;color:#e8f1f8;border-radius:5mm;padding:.6mm 2.4mm;background:#0c2038}.thalf .sup{margin-top:3mm}
.cfg{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:3mm}.cfg div{background:#0a1c33;border:.2mm solid var(--line);border-radius:1.6mm;padding:2mm}.cfg b{font-size:7.6pt;color:#fff}.cfg p{font-size:6.6pt;line-height:1.35;color:var(--mu);margin-top:.8mm}
.cfgl{font-size:6.2pt;letter-spacing:.14em;text-transform:uppercase;color:var(--cy);margin-top:3mm}
.card .pl{font-size:7.6pt;color:#fff;font-weight:600;line-height:1.3;margin-top:1.1mm}
'''


def dp_cfg(s):
    x = v2.DP_EXTRA.get(s['old'])
    if not x:
        return ''
    cols = ''.join(f'<div><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in x['cols'])
    return f'<div class="cfgl">Choose the level of backup you need</div><div class="cfg">{cols}</div>'


def page(inner, label, no, cls=''):
    return v2.page(inner, label, no, cls)


def layout():
    pgs = []
    for sec in ORDER:
        its = [i for i in items if i['section'] == sec]
        if not its:
            continue
        pgs.append(('opener', sec, None))
        trees = [i for i in its if i['kind'] == 'tree']
        cards = [i for i in its if i['kind'] == 'card']
        if sec == 'DP':
            for t in trees:
                pgs.append(('dp', sec, [t]))
        else:
            buf = []
            for t in trees:
                if t['sysdata'].get('size') == 'full':
                    if buf:
                        pgs.append(('trees', sec, buf)); buf = []
                    pgs.append(('trees', sec, [t]))
                else:
                    buf.append(t)
                    if len(buf) == 2:
                        pgs.append(('trees', sec, buf)); buf = []
            if buf:
                pgs.append(('trees', sec, buf))
        rows = []
        for i in cards:
            if rows and len(rows[-1]) < 2:
                rows[-1].append(i)
            else:
                rows.append([i])
        for k in range(0, len(rows), 3):
            pgs.append(('cards', sec, rows[k:k + 3]))
    return pgs


def build():
    pgs = layout()
    first = 4
    pageno = {}; secpage = {}
    for n_, (kind, sec, pl) in enumerate(pgs):
        no = first + n_
        if kind == 'opener':
            secpage[sec] = no
        elif kind in ('dp', 'trees'):
            for t in pl:
                pageno[t['ref']] = no
        else:
            for r in pl:
                for i in r:
                    pageno[i['ref']] = no
    idx_no = first + len(pgs); out = []
    mont_ids = [x for x in ['A01', 'A09', 'B11', 'A02'] if os.path.exists(f'{W}/img_ready/{x}.jpg')]
    mont = ''.join(f'<div class="ph"><img src="{b64(f"{W}/img_ready/{x}.jpg")}"></div>' for x in mont_ids)
    out.append(f'''<section class="page cover"><div class="lg"><img src="{LOGO_URI}"></div><div class="tag">Edition 2026</div>
<div class="ct"><div class="lab">Sinor Marine Services Middle East FZCO</div><div class="big">Products<br><em>Catalogue</em></div>
<div class="sub">See every system we supply and everything that comes with it, from the main unit to the screens, targets, cables and spare parts. Supplied and supported from Dubai.</div></div>
<div class="mont">{mont}</div>
<div class="bar"><div>Head office<b>Dubai, UAE</b></div><div>Sales<b>sales@sinormarine.com</b></div><div>Phone<b>+971 4 665 7162</b></div><div>Web<b>sinormarine.com</b></div></div></section>''')
    rows = ''
    for k, sec in enumerate(ORDER, 1):
        n_t = len([i for i in items if i['section'] == sec and i['kind'] == 'tree'])
        n_c = len([i for i in items if i['section'] == sec and i['kind'] == 'card'])
        desc = (f'{n_t} systems' if n_t else '') + (' and ' if n_t and n_c else '') + (f'{n_c} individual items' if n_c else '')
        rows += f'<div class="row2"><div class="n">{k}</div><div class="t"><b>{e(SECTIONS[sec][0])}</b><span>{e(SECTIONS[sec][1])} ({desc})</span></div><div class="p">p. {secpage[sec]:02d}</div></div>'
    rows += f'<div class="row2"><div class="n">i</div><div class="t"><b>Item index</b><span>Every reference with its page number.</span></div><div class="p">p. {idx_no:02d}</div></div>'
    toc = f'''<div class="sechead"><div class="lab" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)">Contents</div><h1>How to read this catalogue</h1>
<p>If a word is new to you, see the Plain words guide on the next page. Each system page shows the system at the top and, underneath it like the branches of a tree, everything that comes with it: the main unit, screens and controls, targets, cables, and the spares and service kits that keep it running. Every part can also be ordered on its own. Quote the reference (for example PR-01) in your enquiry and we will quote exactly what you need. Photos and descriptions are drawn from manufacturer and distributor published information; photos are for identification and the delivered item may differ in detail.</p></div><div class="toc">{rows}</div>'''
    out.append(page(toc, 'Contents', 2))
    out.append(page('<div class="sechead"><div class="lab" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)">Plain words guide</div><h1>What the words mean</h1><p>A short guide to the terms used in this catalogue. If a word is new to you, it is probably here.</p></div><div class="gl">' + GL_HTML + '</div>', 'Plain words guide', 3))
    for n_, (kind, sec, pl) in enumerate(pgs):
        no = first + n_
        title, blurb = SECTIONS[sec]; k = ORDER.index(sec) + 1
        if kind == 'opener':
            groups = []
            for i in [x for x in items if x['section'] == sec]:
                g = i['group']
                if not groups or groups[-1][0] != g:
                    groups.append((g, []))
                groups[-1][1].append(i)
            gh = ''
            for g, its in groups:
                lis = ''.join(f'<div class="li"><span class="r">{i["ref"]}</span><span class="t">{e(clean(i["name_show"]))}</span><span class="p">p. {pageno[i["ref"]]:02d}</span></div>' for i in its)
                gh += f'<div class="g2"><h4>{e(g)}</h4>{lis}</div>'
            out.append(page(f'<div class="opener" style="margin-top:14mm"><div class="sech"><div class="lab">Section {k}</div></div><h1 class="big">{e(title)}</h1><p class="bl">{e(blurb)}</p>{gh}</div>', f'Section {k}', no))
        elif kind == 'dp':
            s = pl[0]['sysdata']; s = dict(s, ref=pl[0]['ref'])
            out.append(page(f'<div class="sech" style="margin-bottom:1mm"><div class="lab">{e(title)}</div></div>' + tree(s, True, dp_cfg(s)), title, no))
        elif kind == 'trees':
            body = ''.join(tree(dict(t['sysdata'], ref=t['ref']), t['sysdata'].get('size') == 'full') for t in pl)
            out.append(page(f'<div class="sech"><div class="lab">{e(title)}</div></div>{body}', title, no))
        else:
            body = ''.join('<div class="row s">' + ''.join(card3(i) for i in r) + '</div>' for r in pl)
            out.append(page(f'<div class="sech"><div class="lab">{e(title)}</div></div><div class="rows">{body}</div>', title, no))
    idx = ''.join(f'<div><span><b>{i["ref"]}</b>{e(short(i["name_show"], 44))}</span><span>{pageno[i["ref"]]:02d}</span></div>' for i in sorted(items, key=lambda x: x['ref']))
    out.append(page(f'<div class="sechead"><div class="lab" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--cy)">Index</div><h1>Item index</h1></div><div class="idx">{idx}</div>', 'Index', idx_no))
    disc = ("Product names, logos and trademarks belong to their respective owners and are used here only to identify the products supplied. "
            "Descriptions and specifications are taken from manufacturer and distributor published information and may change; confirm current data with Sinor before ordering. "
            "Sinor Marine Services Middle East FZCO supplies and supports the products listed as an independent company unless a specific authorisation is stated in writing. "
            "Availability, lead times and prices are quoted per enquiry.")
    out.append(f'''<section class="page back"><div class="hd"><span class="lg"><img src="{LOGO_URI}"></span><span>Get in touch</span></div>
<div class="ct"><h1>Tell us the system.<br><em>We will quote everything that comes with it.</em></h1><div class="cols"><div><b>Head office</b>Sinor Marine Services Middle East FZCO<br>601, Al Nokitha Building, Hamariya Port<br>P.O. Box 95842, Dubai, UAE</div>
<div><b>Contact</b>sales@sinormarine.com<br>support@sinormarine.com<br>+971 4 665 7162<br>sinormarine.com</div></div></div><div class="disc">{e(disc)}</div></section>''')
    open(f'{W}/{OUTNAME}.html', 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sinor Products Catalogue 2026</title><style>{CSS3}</style></head><body>{"".join(out)}</body></html>')
    return len(out)


if __name__ == '__main__':
    n = build()
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{W}/{OUTNAME}.html');await p.waitForTimeout(900);"
          f"await p.pdf({{path:'{W}/{OUTNAME}.pdf',width:'210mm',height:'297mm',printBackground:true,preferCSSPageSize:true}});await b.close();}})()")
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, cwd='/tmp')
    print('pages', n, 'rc', r.returncode, r.stderr[-300:])
