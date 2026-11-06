# Baseline web QA, imported site (automated, Director-run, NOT an independent review)

Run 2026-11-06: node scripts/web_qa.mjs /tmp/work/2026-11-sinor-site/site /tmp/work/2026-11-sinor-site-qa. Headless Chromium on Linux, 375, 768, 1440 px. Result: 2 FAIL, 9 WARN, 1 NOTE. Screenshots looked at: top of the 1440 and 375 px home page only.

## What the tool found, and how much to trust it
- FAIL broken-anchor (#home, #products..., #services and others): FALSE POSITIVE. The site is a hash-routed single page app, so these are client routes, not element ids. Tool limit.
- FAIL request-failed clip/see.mp4 at 375 px: unconfirmed. Browsers often abort video loads; not shown to be a real defect.
- WARN external requests to fonts.googleapis.com and fonts.gstatic.com: real. Conflicts with the build standard (no external font service).
- WARN page weight 3.29 MB on first load (limit 1.5 MB), 144 requests; lab LCP 17.5 s locally (indicative only, not field data, but far over 2.5 s).
- WARN meta description, canonical and Open Graph missing; no skip link; heading order h2 to h4; images without width and height (11 listed in the raw report); favicon missing.
- No console errors, no horizontal overflow, 0 low-contrast text nodes among 188 checked (approximate check, skips text over images or video).

## Not tested (important)
Only the home view was loaded. Every other page (products, service, training, simulator, company, news, contact) lives behind hash routes and was NOT tested. The script needs a hash-route mode first. Not tested: the scroll film behaviour, simulator, forms, videos playing, copy accuracy, claims, real devices, other browsers, screen readers.
