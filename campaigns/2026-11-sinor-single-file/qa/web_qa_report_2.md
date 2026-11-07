# Web QA report 2: Sinor Marine Technologies single-file website (cycle 2 recheck)

Tested file: /tmp/work/sinor-v2/out/Sinor-Marine-Technologies-Website.html (13,132,736 bytes, repacked after report 1). file:// only, browser context offline:true. Reviewer: web-qa-reviewer, independent of the builders. Date: 2026-11-07. W7 and W8 from report 1 are accepted by the Director and not re-judged.
Scripts, raw JSON, logs and screenshots (outside the repo): /tmp/work/sinor-v2/tmp/qa/ (c2.mjs, routes.mjs, perf2.mjs, fcp.mjs, hero.mjs, inter.mjs, media.mjs, misc.mjs, lazy.mjs, news*.mjs, leak.mjs; out2/, shots2/, shots/). Report 1 results are kept in c1/.
Launch: chromium, --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist for WebGL, hero, timing and interaction runs. The layout, contrast, tap and overlap sweep (c2.mjs) used --disable-gpu --disable-webgl --disable-3d-apis with one fresh page per route and width, because SwiftShader screenshots became too slow (see W9). Consequence: in that sweep the home 3D canvas is not drawn (the still image is shown); the home hero was checked separately with WebGL.

## Verdict

0 FAIL, 2 WARN open (W5 unchanged, W9 new), 4 NOTE. W1, W2, W3, W4 and W6 are verified fixed. No regression found in the sweep.

## True verification scope

Run: headless Chromium on Linux, software GPU, Playwright, file://, offline. Real mouse and keyboard events. One emulated phone width.
NOT covered: real iPhone or Android, Safari, Firefox, Edge, a real GPU (so frame rate, smoothness and whether W9 occurs on real hardware are unknown), screen readers, a full manual WCAG audit, double-click opening on Windows or macOS, real-user performance. Timings are lab numbers on a software GPU, indicative only. Contrast values are from my own pixel sampling (below), not a certified tool.

## Status of report 1 items

| ID | Status | Result |
|---|---|---|
| W1 | FIXED | Services page head is clean at 1440, 768 and 390 (screenshots shots2/services_*.png). The drawn map no longer sits behind the breadcrumb or headline; it is dimmed and kept to the right or above. |
| W2 | FIXED | About page: the photo scene is dimmed, the burned-in HUD text is gone from behind the breadcrumb, eyebrow and headline (shots2/about_*.png). |
| W3 | FIXED | Lowest ratios found: see section 2. All at least 6.88:1 at the 10th percentile of the text box. |
| W4 | FIXED | Smallest tappable height 44 px everywhere at 390 (section 3). |
| W5 | OPEN, unchanged within noise | Section 4. |
| W6 | FIXED | Section 5. |

## New findings

| ID | Sev | Route and location | Finding | Owner |
|---|---|---|---|---|
| W5 | WARN (open) | #home load | First paint is early (first-paint and first-contentful-paint 76 to 80 ms in 3 runs), but the main thread then stalls: animation-frame gaps of about 0.65 s starting near 0.35 s and about 1.9 to 2.2 s starting near 1.0 s (3 runs). Longest gap 2.4 to 2.7 s at 1440 and 1.6 to 1.7 s at 390 in the second instrument. First non-blank 3D region by wall clock: 6.2, 6.5, 6.6 s at 1440 and 4.1, 4.2, 4.2 s at 390 (includes screenshot polling cost). All words of the H1 fully visible about 3.2 s (1440) and 2.7 s (390) after document start. Report 1 saw a similar stall (no frame between about 1.0 s and 2.7 s), so this is not fixed; I cannot show it is better. The first screen paints, but it does not animate during the stall. Software GPU inflates all of this. | 3D module (scene build, shader compile) and page builder |
| W9 | WARN (new) | all routes, WebGL-enabled Chromium with SwiftShader | Rendering gets progressively slower as routes are changed in one tab. Screenshot time grew 4.7 s, 15 s, 17 s, 22 s and then timed out (25 to 30 s limit) over five route changes starting from #news; the same sequence with GPU and WebGL disabled took 0.1 to 0.2 s per shot. The page itself stays responsive in script terms (requestAnimationFrame 52 to 121 callbacks per 2 s, 8 fps at the worst point), no WebGL context is created on non-home routes, and no animation loop or video accumulates (leak.mjs: callbacks stay about 120 per 2 s; 2D canvas contexts are created per visit, 3 on news, 1 on partners and services). In report 1, screenshots on the same routes took about 1 to 2 s each, so this looks new since cycle 1, but cause not isolated and I had no cycle 1 file to compare. May be only the software GPU compositing the 2D canvas scenes; a real GPU was not available. Worth a check on a real device. | page builder (canvas scenes) |
| N1 | NOTE | #partners at 390, network map | Inside the drawn map the labels Malaysia, Singapore and Indonesia overlap each other (shots2/partners_390.png). Not overlapping HTML text. Readable at 1440. | page builder |
| N2 | NOTE | #news-partner-seminar-2019, #news-servogear-hub-2017, #news-vestdavit-agreement-2017 at 390 | A "News" back link is 41 px wide and 44 px high (the only tappable under 44 in either direction). | page builder |
| N3 | NOTE | lazy media | Clip posters and sources are now attached shortly before a video comes into view (videos 2 to 8 had no poster or source at load, then poster set and playing within 150 ms of scrolling in). Film poster shown before play (720x480 loads). Footer logo is a 1x1 placeholder until the footer nears view, then 1500x489 at 240x78. Behaves correctly; recorded because a screenshot taken before scrolling shows no poster. | none |
| N4 | NOTE | report 1 N-items | N1 to N7 of report 1 unchanged except as noted here (aborted video blob requests still the only failed requests; DP tabs only on #home and #mt-dp-chair). | none |

## 1. Canvas text vs HTML text (W1, W2), all 24 routes plus unknown, 1440, 768, 390

Method (c2.mjs): for each route and width at two scroll positions, collect every HTML text box for the h1, breadcrumb, eyebrow and lead; screenshot with text hidden, screenshot again with all canvases hidden, count pixels in each text box that change by more than a threshold when canvases are hidden (shows canvas content under the text). Result: 1158 text boxes sampled, 0 breadcrumb, eyebrow, h1 or lead boxes with more than 1 percent canvas content under them (highest h1 value 0.3 percent, Services at 1440; the only larger value, 11 percent, was a small "Illustration" tag over a scene on #seaonics at 390). Limits: the check finds canvas pixels, not specifically canvas-drawn glyphs; I looked at screenshots to confirm. Looked at: services, about, partners, mt-dynamic-positioning (product page) at 1440 and 390 (shots2/sheet_desktop.png, sheet_mobile.png) plus 768 files and vestdavit. No collisions between canvas text and HTML text.

## 2. Contrast of real pixels (W3), 1440, 768 and 390, all routes

Method: hide all text, screenshot, take the real background pixels under each text box (only boxes below the sticky header and fully opaque), apply the computed text colour, compute WCAG ratios, judge the 10th percentile worst pixel area (and also the single worst pixel). 1158 elements: h1 96, breadcrumb 204, eyebrow 161, lead 160, button 134, other 403.
Lowest per class (10th percentile / single worst pixel):
- h1 13.66 / 5.47 (training at 1440, large text)
- breadcrumb 9.81 / 9.81 (team and partners at 1440)
- eyebrow 9.77 / 9.77 (mt-dynamic-positioning, 1440, second scroll position)
- lead 8.01 / 7.79 (home at 390)
- button label 17.47 / 17.35 (home at 768)
- any other text 6.88 (large partner-name headings on home at 768); smallest single pixel 1.87 under a form label edge at 1440 (10th percentile 8.21).
Elements below 4.5:1 (3:1 for large text) at the 10th percentile: 0.
Not covered: the home hero text was sampled over the still image layout in the no-WebGL sweep (the text column sits over the plain dark stage, left of the 3D); text over video frames while playing.

## 3. Tap targets (W4), 390 wide, all 25 routes

Every visible link, button, input, textarea, summary and tabbable element, excluding the off-screen skip link, closed menu items and links inside running text: 644 elements measured. Smallest height 44 px; 0 below 44 px high. Width under 44: 3 (N2). Previously 24 to 32 px items (footer links, breadcrumbs, phone link) are now 44 px high. Open mobile menu items: min 44 high, 48 wide (inter.mjs).

## 4. Hero, load and fallbacks (W5 and regression)

- Timing: see W5.
- Captions (hero.mjs at 1440, 58 steps of 50 px, and 390, 48 steps): all four captions reach opacity 1 in order (same scroll ranges as report 1); text and 3D do not overlap (text right edge 730 vs canvas left 773 at 1440; phone canvas 76 to 383, text from 423); 3D non-blank, rotates and changes pose across the run (looked at 15 frames in shots/sheet2.png and the 1440 and 390 hero screenshots). Canvas edge versus page background: largest step 1 of 255 at scroll 0 (one 390 sample at scroll 800 hits the header border line, not the canvas). No errors.
- Fallbacks, 1440 and 390, reducedMotion emulated and WebGL disabled (no WebGL context confirmed): class fb, still image shown (732 px image loaded), canvas hidden, all four captions visible, caption reads "From the simulator", counters show final numbers, no errors. PASS.
- Resize 1440 to 390 and back was passed in report 1 and not repeated.

## 5. Heading order (W6)

75 route and width cases (25 routes x 3 widths): exactly one h1 each and no skipped heading level in any. Report 1 had skips on #products, #products-marine-technologies, #team, #news.

## 6. Regression sweep

- routes.mjs, 24 routes plus unknown, at 320, 375, 768, 1440: one h1 each; 0 console or page errors; no horizontal overflow; no broken images (the earlier false hits from lazy images are gone); titles unchanged from report 1 and all differ from the previous route; scroll position resets. Only failed requests: 5 aborted video blob requests (net::ERR_ABORTED when a clip leaves view). Request hosts across the whole sweep: file: 4, blob: 154, nothing else.
- Interactions (inter.mjs, real mouse and keyboard): dropdown hover, click, Escape, navigation; product chips (5); country selector; accordion by mouse and Enter; DP tabs on home and DP chair (5 each); forms contact, services and training (labelled fields, empty and invalid email messages, prepared message, Copy label "Copied" and clipboard content, mailto to the sales address, no sent claim, note says the site cannot send mail); mobile menu opens, Escape closes it and focus returns to the burger, a link navigates and closes it; focus rings 3 px solid #8CC4F2. Two items printed FAIL by my script are script artifacts as in report 1 (skip link test after a click; DP tabs looked for on a page that has none); media.mjs shows the skip link first stop, visible at 141x39, and Enter focuses main.
- Media (media.mjs, lazy.mjs): film plays (currentTime advances, audio decoded), seven clips play when in view, all paused when out of view, posters load, Outfit and DM Sans loaded. Logos: header mark transparent and white (75 percent transparent pixels, 100 percent near white opaque); full logo white on dark in footer and about.
- Content fidelity (fid.py): 23 of 24 routes 0 old lines missing; home 1 (the accepted W8 label). Extra text lines identical to W8 and the three "DIAGRAM" tags.
- Sales email, phone, address: email and phone values on all 25 routes are subsets of the old site's values (0 mismatches); contact route 0 of 23 old lines missing; 0 old footer lines missing. Values not quoted here.
- Forbidden terms (rendered text of 25 routes and raw HTML with base64 stripped): Sinor Marine Services, FZCO, Middle East, linkedin, NEEDED FROM RAHUL, lorem, em dash, en dash: 0 hits each. UAE: 3 rendered and 4 raw hits, all as a country name in service and partner lists.

## Not run this cycle

Resize round trip, memory over repeated route passes (report 1: flat), fonts check repeated only through media.mjs, keyboard operation of DP tabs, focus trap inside the mobile menu, Copy fallback when clipboard is denied.

## Candidate lessons for the Director

1. Under SwiftShader a long single-tab session with canvas scenes slows screenshots until they time out; use one fresh page per route for screenshot-heavy checks, and say so.
2. Measure canvas-under-text by toggling canvas visibility and diffing pixels in each text box; it is cheaper and more objective than eyeballing, but still confirm with screenshots.
3. A fast first paint can hide a long main-thread stall; record both first paint and the longest animation-frame gap.
