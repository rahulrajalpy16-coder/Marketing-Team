#!/usr/bin/env node
// Website QA: serves a static site locally, crawls internal pages, tests them in headless Chromium
// at 375, 768 and 1440 px wide, and writes report.md, report.json and screenshots.
// Usage: node scripts/web_qa.mjs <siteDir> <outDir> [--hash-routes]
// --hash-routes: for hash-routed single page apps. In-page links (#...) whose target id does not exist are treated as client routes and each is loaded and tested.
// Exit code 1 if any FAIL. Lab numbers are local and indicative only, not real-user data.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const HASH = process.argv.includes('--hash-routes');
const [siteArg, outArg] = process.argv.slice(2).filter(a => !a.startsWith('--'));
if (!siteArg || !outArg) { console.error('Usage: node scripts/web_qa.mjs <siteDir> <outDir>'); process.exit(2); }
const siteDir = path.resolve(siteArg);
const outDir = path.resolve(outArg);
if (!fs.existsSync(siteDir)) { console.error('Site dir not found: ' + siteDir); process.exit(2); }
fs.mkdirSync(path.join(outDir, 'shots'), { recursive: true });

let pw;
try { pw = createRequire(import.meta.url)('playwright'); }
catch { const g = execSync('npm root -g').toString().trim(); pw = createRequire(path.join(g, 'x.js'))('playwright'); }

const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.avif': 'image/avif', '.gif': 'image/gif', '.ico': 'image/x-icon', '.woff2': 'font/woff2',
  '.txt': 'text/plain', '.xml': 'application/xml' };
const server = http.createServer((req, res) => {
  let p; try { p = decodeURIComponent(new URL(req.url, 'http://x').pathname); } catch { res.writeHead(400); return res.end(); }
  let f = path.join(siteDir, p);
  if (f !== siteDir && !f.startsWith(siteDir + path.sep)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404, { 'content-type': 'text/plain' }); return res.end('not found'); }
  res.writeHead(200, { 'content-type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const origin = 'http://127.0.0.1:' + server.address().port;

const findings = []; // {sev, page, vp, rule, detail}
const add = (sev, page, vp, rule, detail) => findings.push({ sev, page, vp, rule, detail });
const VIEWPORTS = [{ w: 375, h: 812 }, { w: 768, h: 1024 }, { w: 1440, h: 900 }];
const pageInfo = {};

const browser = await pw.chromium.launch({ args: ['--no-sandbox'] });
const queue = ['/'];
const seen = new Set();
const linkTargets = new Map(); // url path -> set of source pages

while (queue.length && seen.size < 50) {
  const pagePath = queue.shift();
  if (seen.has(pagePath)) continue;
  seen.add(pagePath);
  const label = pagePath === '/' ? 'index' : pagePath.replace(/^\//, '').replace(/[^\w.-]+/g, '_');
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await ctx.newPage();
    const vpl = vp.w + 'px';
    let bytes = 0, reqs = 0; const external = new Set();
    page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) add('FAIL', pagePath, vpl, 'console-error', m.text().slice(0, 200)); });
    page.on('pageerror', e => add('FAIL', pagePath, vpl, 'page-error', String(e).slice(0, 200)));
    page.on('requestfailed', r => { if (r.resourceType() === 'media' && /ERR_ABORTED/.test((r.failure() || {}).errorText || '')) return; add('FAIL', pagePath, vpl, 'request-failed', r.url().slice(0, 160)); });
    page.on('response', async r => {
      reqs++;
      const u = r.url();
      if (!u.startsWith(origin) && !u.startsWith('data:')) external.add(new URL(u).host);
      if (r.status() >= 400) add('FAIL', pagePath, vpl, 'http-' + r.status(), u.slice(0, 160));
      try { const h = r.headers()['content-length']; if (h) bytes += +h; else { const b = await r.body(); bytes += b.length; } } catch {}
    });
    await page.addInitScript(() => {
      window.__lcp = 0; window.__cls = 0;
      try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); } catch {}
      try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); } catch {}
    });
    let resp;
    try { resp = await page.goto(origin + pagePath, { waitUntil: 'networkidle', timeout: 20000 }); }
    catch (e) { add('FAIL', pagePath, vpl, 'load-failed', String(e).slice(0, 160)); await ctx.close(); continue; }
    if (!resp || resp.status() >= 400) { add('FAIL', pagePath, vpl, 'page-status', String(resp && resp.status())); await ctx.close(); continue; }
    await page.waitForTimeout(400);

    const ov = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
    if (ov.sw > ov.iw + 1) add('FAIL', pagePath, vpl, 'horizontal-overflow', `scrollWidth ${ov.sw} > ${ov.iw}`);
    await page.screenshot({ path: path.join(outDir, 'shots', `${label}_${vp.w}.png`), fullPage: true });

    if (vp.w === 1440 || vp.w === 375) {
      const d = await page.evaluate(() => {
        const q = s => [...document.querySelectorAll(s)];
        const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
        const name = el => (el.getAttribute('aria-label') || (el.tagName === 'INPUT' ? (el.type + ' input') : '') || (el.getAttribute('aria-labelledby') || '').split(/\s+/).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim() || el.textContent || el.getAttribute('title') || (el.querySelector('img[alt]') || {}).alt || '').trim();
        const meta = n => (document.querySelector(`meta[name="${n}"]`) || {}).content || '';
        const og = n => (document.querySelector(`meta[property="${n}"]`) || {}).content || '';
        const heads = q('h1,h2,h3,h4,h5,h6').filter(vis).map(h => +h.tagName[1]);
        const skips = []; heads.forEach((l, i) => { if (i && l > heads[i - 1] + 1) skips.push(`h${heads[i - 1]} to h${l}`); });
        const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2]); };
        const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return { c: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 }; };
        const bgOf = el => { let e = el; while (e) { const cs = getComputedStyle(e); if (cs.backgroundImage !== 'none') return { unknown: true }; const b = parse(cs.backgroundColor); if (b && b.a > 0.99) return { c: b.c }; e = e.parentElement; } return { c: [255, 255, 255] }; };
        const low = []; let checked = 0;
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const done = new Set();
        while (walker.nextNode()) {
          const t = walker.currentNode; const el = t.parentElement;
          if (!el || done.has(el) || !t.textContent.trim() || !vis(el) || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue;
          done.add(el);
          const cs = getComputedStyle(el); const fg = parse(cs.color); const bg = bgOf(el);
          if (!fg || bg.unknown) continue;
          checked++;
          const l1 = lum(fg.c), l2 = lum(bg.c); const ratio = (Math.max(l1, l2) + .05) / (Math.min(l1, l2) + .05);
          const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
          const large = px >= 24 || (px >= 18.66 && bold);
          if (ratio < (large ? 3 : 4.5)) low.push(`${el.tagName.toLowerCase()} "${t.textContent.trim().slice(0, 30)}" ${ratio.toFixed(2)}:1`);
        }
        const small = q('a,button,input:not([type=hidden]),select,textarea,[role=button]').filter(vis).filter(el => {
          const r = el.getBoundingClientRect(); const inline = getComputedStyle(el).display === 'inline';
          return !inline && (r.width < 24 || r.height < 24);
        }).map(el => `${el.tagName.toLowerCase()} "${name(el).slice(0, 25)}"`);
        const unlabeled = q('input:not([type=hidden]):not([type=submit]):not([type=button]),select,textarea').filter(el => {
          const id = el.id; return !(el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || (id && document.querySelector(`label[for="${id}"]`)) || el.closest('label'));
        }).map(el => el.outerHTML.slice(0, 70));
        return {
          title: document.title, desc: meta('description'), lang: document.documentElement.lang,
          viewport: meta('viewport'), canonical: !!document.querySelector('link[rel=canonical]'),
          ogTitle: og('og:title'), ogDesc: og('og:description'), favicon: !!document.querySelector('link[rel~=icon]'),
          h1: q('h1').length, skips,
          imgNoAlt: q('img').filter(i => !i.hasAttribute('alt')).map(i => i.getAttribute('src')),
          imgNoDim: q('img').filter(i => !(i.getAttribute('width') && i.getAttribute('height'))).map(i => i.getAttribute('src')),
          emptyLinks: q('a[href]').filter(a => vis(a) && !name(a)).length,
          emptyButtons: q('button').filter(b => vis(b) && !name(b)).length,
          unlabeled, small, low: low.slice(0, 8), lowCount: low.length, contrastChecked: checked,
          landmarks: { main: q('main').length, nav: q('nav').length, header: q('header').length, footer: q('footer').length },
          skipLink: !!q('a[href^="#"]').find(a => /skip/i.test(a.textContent)),
          hrefs: q('a[href]').map(a => a.getAttribute('href')),
          anchorsMissing: q('a[href^="#"]').map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1)) && !document.getElementsByName(h.slice(1)).length),
          lcp: Math.round(window.__lcp), cls: +window.__cls.toFixed(3),
          lorem: /lorem ipsum/i.test(document.body.innerText), emdash: /[\u2013\u2014]/.test([document.body.innerText, document.title, meta('description'), ...q('img').map(i => i.alt)].join(' ')),
        };
      });
      if (vp.w === 1440) {
        pageInfo[pagePath] = { title: d.title, lcpLabMs: d.lcp, clsLab: d.cls, requests: reqs, kb: Math.round(bytes / 1024), external: [...external], contrastChecked: d.contrastChecked };
        if (!d.title) add('FAIL', pagePath, 'all', 'title-missing', ''); else if (d.title.length > 65) add('WARN', pagePath, 'all', 'title-long', `${d.title.length} chars`);
        if (!d.desc) add('WARN', pagePath, 'all', 'meta-description-missing', ''); else if (d.desc.length < 70 || d.desc.length > 165) add('WARN', pagePath, 'all', 'meta-description-length', `${d.desc.length} chars`);
        if (!d.lang) add('FAIL', pagePath, 'all', 'html-lang-missing', '');
        if (!d.viewport) add('FAIL', pagePath, 'all', 'viewport-meta-missing', '');
        if (!d.canonical) add('WARN', pagePath, 'all', 'canonical-missing', '');
        if (!d.ogTitle || !d.ogDesc) add('WARN', pagePath, 'all', 'open-graph-incomplete', '');
        if (!d.favicon) add('NOTE', pagePath, 'all', 'favicon-missing', '');
        if (d.h1 !== 1) add('FAIL', pagePath, 'all', 'h1-count', `found ${d.h1}`);
        if (d.skips.length) add('WARN', pagePath, 'all', 'heading-order', d.skips.join(', '));
        if (d.imgNoAlt.length) add('FAIL', pagePath, 'all', 'img-alt-attribute-missing', d.imgNoAlt.join(', '));
        if (d.imgNoDim.length) add('WARN', pagePath, 'all', 'img-width-height-missing (layout shift risk)', d.imgNoDim.join(', '));
        if (!d.landmarks.main) add('FAIL', pagePath, 'all', 'main-landmark-missing', '');
        if (!d.landmarks.header || !d.landmarks.footer) add('WARN', pagePath, 'all', 'header-or-footer-landmark-missing', '');
        if (!d.skipLink) add('WARN', pagePath, 'all', 'skip-link-missing', '');
        if (d.anchorsMissing.length) {
          if (HASH) { for (const h of d.anchorsMissing) { const r = '/' + h; if (!seen.has(r) && !queue.includes(r)) queue.push(r); } }
          else add('FAIL', pagePath, 'all', 'broken-anchor', d.anchorsMissing.join(', '));
        }
        if (d.lorem) add('FAIL', pagePath, 'all', 'lorem-ipsum', '');
        if (d.emdash) add('WARN', pagePath, 'all', 'em-or-en-dash-in-text-title-meta-or-alt', '');
        if (external.size) add('WARN', pagePath, 'all', 'external-requests', [...external].join(', '));
        if (bytes / 1024 > 1536) add('WARN', pagePath, 'all', 'page-weight-over-1.5MB', `${Math.round(bytes / 1024)} KB`);
        if (d.lcp > 2500) add('WARN', pagePath, 'all', 'lab-LCP-over-2.5s (indicative)', `${d.lcp} ms`);
        if (d.cls > 0.1) add('WARN', pagePath, 'all', 'lab-CLS-over-0.1 (indicative)', String(d.cls));
        for (const h of d.hrefs) {
          if (/^(mailto:|tel:|javascript:|#)/i.test(h)) continue;
          let u; try { u = new URL(h, origin + pagePath); } catch { add('FAIL', pagePath, 'all', 'bad-href', h); continue; }
          if (u.origin !== origin) { add('NOTE', pagePath, 'all', 'external-link', u.href.slice(0, 120)); continue; }
          const t = u.pathname; if (!linkTargets.has(t)) linkTargets.set(t, new Set()); linkTargets.get(t).add(pagePath);
          if (!seen.has(t) && !queue.includes(t) && /(\/|\.html?)$/.test(t)) queue.push(t);
        }
      }
      // Checks that depend on what is visible run at both 375 and 1440, so mobile-only controls are tested.
      if (d.emptyLinks) add('FAIL', pagePath, vpl, 'link-without-name', String(d.emptyLinks));
      if (d.emptyButtons) add('FAIL', pagePath, vpl, 'button-without-name', String(d.emptyButtons));
      if (d.unlabeled.length) add('FAIL', pagePath, vpl, 'form-control-without-label', d.unlabeled.join(' | '));
      if (d.lowCount) add('FAIL', pagePath, vpl, `low-contrast (${d.lowCount}, approximate, ignores background images and opacity)`, d.low.join(' | '));
      if (vp.w === 375 && d.small.length) add('WARN', pagePath, vpl, 'target-smaller-than-24px (WCAG 2.5.8)', d.small.slice(0, 8).join(' | '));
    }
    await ctx.close();
  }
}
for (const [t, from] of linkTargets) {
  let tt = t; try { tt = decodeURIComponent(t); } catch {}
  const f = path.join(siteDir, tt); const ok = fs.existsSync(f) && (!fs.statSync(f).isDirectory() || fs.existsSync(path.join(f, 'index.html')));
  if (!ok) add('FAIL', [...from][0], 'all', 'broken-internal-link', t);
}
await browser.close(); server.close();
if (queue.some(q => !seen.has(q))) add('WARN', '(site)', 'all', 'crawl-stopped-at-50-pages', 'unvisited pages remain');

const uniq = []; const keys = new Set();
for (const f of findings) { const k = [f.sev, f.page, f.rule, f.detail].join('|'); if (!keys.has(k)) { keys.add(k); uniq.push(f); } }
const count = s => uniq.filter(f => f.sev === s).length;
let md = `# Web QA report (automated)\n\nSite: ${siteDir}\nPages tested: ${[...seen].join(', ')}\nViewports: 375, 768, 1440 px wide, headless Chromium on Linux\n\n`;
md += `Result: ${count('FAIL')} FAIL, ${count('WARN')} WARN, ${count('NOTE')} NOTE\n\n## Findings\n\n`;
for (const s of ['FAIL', 'WARN', 'NOTE']) for (const f of uniq.filter(x => x.sev === s)) md += `- ${s} | ${f.page} | ${f.vp} | ${f.rule}${f.detail ? ' | ' + f.detail : ''}\n`;
if (!uniq.length) md += '- none\n';
md += `\n## Per page (lab, local, unthrottled, indicative only)\n\n| Page | Title | Requests | KB | Lab LCP ms | Lab CLS | Text nodes contrast-checked |\n|---|---|---|---|---|---|---|\n`;
for (const [p, i] of Object.entries(pageInfo)) md += `| ${p} | ${String(i.title).replace(/\|/g, '/')} | ${i.requests} | ${i.kb} | ${i.lcpLabMs} | ${i.clsLab} | ${i.contrastChecked} |\n`;
md += `\n## Not covered\n\nReal devices, Safari and Firefox, screen readers, full manual WCAG audit, real-user performance, hosting and HTTPS. Contrast check is approximate: it skips text over background images and ignores semi-transparent backgrounds. Screenshots: ${path.join(outDir, 'shots')}\n`;
fs.writeFileSync(path.join(outDir, 'report.md'), md);
fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify({ pages: pageInfo, findings: uniq }, null, 2));
console.log(md);
process.exit(count('FAIL') ? 1 : 0);
