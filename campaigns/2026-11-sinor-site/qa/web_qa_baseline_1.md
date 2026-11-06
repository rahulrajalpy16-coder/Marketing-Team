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

---
# Update: full-site run with --hash-routes (2026-11-06, automated, Director-run, NOT an independent review)

Command: node scripts/web_qa.mjs /tmp/work/2026-11-sinor-site/site /tmp/work/2026-11-sinor-site-qa2 --hash-routes. 25 routes loaded at 375, 768 and 1440 px (75 screenshots; "/" and "/#home" are the same view, so 24 distinct views). One screenshot checked by eye (Bridge Mate DP Chair page at 1440): real content rendered. The two "Result" lines above are superseded by this section.
Result: 1 FAIL, 203 WARN, 32 NOTE. Most WARN lines are the same site-wide issue repeated per page, so read the grouped list:

## FAIL (1)
- /#services at 375 px: a paragraph reading "This site cannot send mail by ..." measures 2.50 to 1 text contrast (needs 4.5 to 1). Approximate check. It is the honest "form not connected" notice, so it is both useful and hard to read.

## Site-wide WARN (present on all 25 views)
- Meta description missing, canonical missing, Open Graph incomplete, no skip link, heading order skips (h2 to h4, h1 to h3 on product pages), images without width and height (layout shift risk), Google Fonts requested from fonts.googleapis.com and fonts.gstatic.com (breaks the no external font rule). Favicon missing (NOTE).
- 23 of 25 views: small tap targets at 375 px (breadcrumb links "Home", "Products", "Marine Technologies" under 24 px, WCAG 2.5.8 minimum; the tool does not model the spacing exception, so some may be acceptable).

## Page weight and speed (lab, local, indicative only)
- Home: 3,290 KB and 144 requests on first load (limit 1.5 MB), lab LCP about 17 s. Heavy because of the 135 film frames.
- All other views: 303 to 639 KB, 6 to 14 requests, lab LCP under 1.5 s. Heaviest: Simulator (639 KB) and DP Chair (632 KB).
- Layout shift in the lab: highest 0.029 (under the 0.1 target).
- No console errors, no failed requests, no horizontal overflow on any view. 47 to 188 text nodes contrast-checked per view.

## What this does NOT cover
Copy accuracy and claims (ISO 9001, partners, product names such as "Bridge Mate DP Chair", dates in the news items, the "Singapore" base) are unchecked against brain/verified-facts.md. Not tested: scroll film behaviour, the simulator, nav dropdowns, the contact form, video playback, keyboard and screen reader use, real devices, other browsers. 7 external links were noted but not followed.

## Suggested first fixes (for Rahul to choose, nothing changed yet)
1. Self-host the two fonts (no Google Fonts requests), after Rahul approves the font files.
2. Add per-route title and meta description, canonical, Open Graph, skip link, favicon.
3. Add width and height to images; fix heading order; enlarge breadcrumb tap targets.
4. Fix the 2.5 to 1 contrast on the contact notice.
5. Lighten the home first load (fewer or lazier film frames, poster first).

## Corrections and confirmation (same day)
- The FAIL was checked by eye and by pixels: the notice is grey-blue (#4A5B6E) on dark navy (#071A33), 2.50 to 1. Real defect. Cause: `.note{color:var(--muted)}` applies inside a dark section. Proposed fix `.dark .note{color:#B9CCE0}` gives 10.61 to 1 (computed). Not applied.
- Correction: the grouped results had 11 distinct WARN types (plus 1 FAIL and 2 NOTE types, 14 rule types in all). An earlier summary said "14 distinct warnings", which was wrong.
- Preview artifact (private): https://claude.ai/artifact/8HAdwQNy1ygne2koV5tkP1
