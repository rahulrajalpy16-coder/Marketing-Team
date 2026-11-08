#!/usr/bin/env python3
"""Read-only check of the live sinormarine.com against the approved Phase 1 pack.
Run: python3 -I verify_phase1.py   (from this folder). Makes only GET requests. Uses a cache-busting query."""
import re,json,html,time,urllib.request,os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
B='https://sinormarine.com'
def get(path):
    u=path if path.startswith('http') else B+path
    sep='&' if '?' in u else '?'
    r=urllib.request.urlopen(urllib.request.Request(u+sep+'nc='+str(int(time.time())),headers={'User-Agent':'Mozilla/5.0'}),timeout=30)
    return r.read()
def text(h): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(script|style).*?</\1>','',h))))
R=[]
def chk(n,name,ok,detail=''): R.append((n,name,bool(ok),detail))
home=get('/').decode('utf8','ignore'); dp=get('/services/dp-system/').decode('utf8','ignore')
about=get('/about/').decode('utf8','ignore'); contact=get('/contact/').decode('utf8','ignore'); ty=get('/thank-you/').decode('utf8','ignore')
prod=get('/products/').decode('utf8','ignore')
# 1
chk(1,'DP button no longer points to contact.html','contact.html' not in dp and re.search(r'href="(/|https://sinormarine.com/)contact/?"',dp))
# 2
def card(h,label):
    m=re.search(r'<a[^>]*href="([^"]*)"[^>]*>[^<]*Learn More',h[h.find(label):]) if label in h else None
    return m.group(1) if m else None
nav=card(home,'Navigation Systems'); el=card(home,'Electrical Solutions')
chk(2,'Navigation card -> /services/navigation-systems/','navigation-systems' in (nav or ''),str(nav))
chk(2,'Electrical card -> /services/electrical-solutions/','electrical-solutions' in (el or ''),str(el))
# 3
exp=json.load(open(os.path.join(HERE,'expected-meta.json')))
bad=[]
for e in exp:
    h=get(e['path']).decode('utf8','ignore')
    t=html.unescape((re.search(r'<title>(.*?)</title>',h,re.S) or [0,''])[1]).strip()
    d=html.unescape((re.search(r'<meta name="description" content="(.*?)"',h,re.S) or [0,''])[1]).strip()
    if t!=e['title'] or d!=e['desc']: bad.append(e['path'])
chk(3,'Titles and descriptions match on all 15 pages',not bad,'differs: '+', '.join(bad) if bad else '')
chk(3,'DP description no longer mentions "Sinor Marine Technology"','Sinor Marine Technology' not in dp)
# 4
smap=get('/page-sitemap.xml').decode('utf8','ignore')
chk(4,'thank-you is noindex','noindex' in (re.findall(r'<meta name="robots"[^>]*>',ty) or [''])[0].lower())
chk(4,'thank-you not in page sitemap','/thank-you/' not in smap)
# 5
ld=re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',home,re.S)
ok=False
for b in ld:
    try:
        j=json.loads(b); ok|=('ProfessionalService' in json.dumps(j) and 'Sinor Marine Services Middle East FZCO' in json.dumps(j))
    except Exception: pass
chk(5,'Organisation JSON-LD present and valid on home',ok,f'{len(ld)} block(s)')
# 6
imgs=re.findall(r'<img\b[^>]*>',home); noalt=[i for i in imgs if not re.search(r'alt="[^"]+"',i)]
chk(6,'Home images all have alt text',not noalt,f'{len(noalt)} of {len(imgs)} missing')
pi=re.findall(r'<img\b[^>]*>',prod)
chk(6,'Products images all have alt text',all(re.search(r'alt="[^"]+"',i) for i in pi))
# 7
srcs=[]
for i in imgs:
    m=re.search(r'\bsrc="([^"]+)"',i)
    if m and m.group(1) not in srcs: srcs.append(m.group(1))
tot=0
for s in srcs:
    try: tot+=len(get(s))
    except Exception: pass
chk(7,'Home unique images total under 1500 KB',tot<1500*1024,f'{tot//1024} KB across {len(srcs)} images (was about 5440 KB)')
# 8
chk(8,'Analytics tag present on home',re.search(r'googletagmanager\.com/gtag|gtag\(|GTM-',home) is not None)
chk(8,'Click-tracking snippet present','click_to_call' in home)
# 9
ht=text(home); at=text(about)
chk(9,'Home shows 100+ and 15+, no 98% and no 50+ projects','100+' in ht and '15+' in ht and '98%' not in ht and not re.search(r'50\+\s*Projects',ht))
chk(9,'About: no "from 2024", no 50+ team, no 20+ years','from 2024' not in at and not re.search(r'50\+\s*Team',at) and '20+' not in at,'')
# 10
chk(10,'Fuel Monitoring removed from home and contact forms','Fuel Monitoring' not in home and 'Fuel Monitoring' not in contact)
# 11
chk(11,'Home email link uses sales@ not a personal address','mailto:rahul@' not in home and 'mailto:sales@sinormarine.com' in home)
w=max(len(r[1]) for r in R)
for n,name,ok,det in R: print(f'Item {n:>2}  {"PASS" if ok else "FAIL"}  {name:<{w}}  {det}')
p=sum(1 for r in R if r[2]); print(f'\n{p}/{len(R)} checks pass')
sys.exit(0 if p==len(R) else 1)
