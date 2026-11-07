# Web QA report 1: Sinor Marine Technologies single-file website

Tested file: /tmp/work/sinor-v2/out/Sinor-Marine-Technologies-Website.html (13,130,838 bytes), opened only via file:// with the browser context set to offline:true. Reviewer: web-qa-reviewer (independent of the builders; I did not build or edit anything). Date: 2026-11-07.
Scripts and raw results (outside the repo): /tmp/work/sinor-v2/tmp/qa/ (*.mjs, out/*.json, out/*.log, shots/*.png). scripts/web_qa.mjs was not used (it needs an http server and a folder).
Launch: chromium, args --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist (plus --enable-precise-memory-info for the heap run; --disable-gpu --disable-webgl --disable-3d-apis for the no-WebGL run).

## Verdict

0 FAIL, 8 WARN, 7 NOTE. The site loads and works offline over file:// with no errors, no external requests and all 24 routes plus the not-found page rendering. Content fidelity against the old site is very high (no old line missing except one UI label). The WARNs are layout and legibility on page-top image bands, tap size, load stall, and heading order.

## True verification scope

Run: headless Chromium on Linux with a software GPU (SwiftShader), Playwright, file:// only, offline context. Real mouse and keyboard events through Playwright (hover, click, Tab, Enter, Escape, wheel). One phone viewport emulated (390x844 and 375, 320 widths) in desktop Chromium.
NOT covered: real iPhone or Android, Safari, Firefox, Edge, a real GPU (frame rate and 3D smoothness unknown), screen readers, a full manual WCAG audit, double-click opening on Windows or macOS (including browser file:// policies such as blob URL or video behaviour), real-user performance. Lab timings below are indicative only and inflated by software rendering. Contrast figures come from my own pixel sampling method (below), not a certified tool.

## Defects

| ID | Sev | Route and location | Finding | Owner |
|---|---|---|---|---|
| W1 | WARN | #services, page head at 1440 | The drawn network-map canvas sits behind the breadcrumb and the H1. Map labels (UAE, Singapore, Indonesia) collide with the headline text; the label under "starts" is garbled by the letters. Screenshot: shots/top_services.png. Headline stays readable, the label does not. | page builder |
| W2 | WARN | #about, page head at 1440 | The photo canvas scene has burned-in HUD text ("INTEGRATED BRIDGE SYS...", "TAUT WIRE", "RADASCAN VIEW") running behind the breadcrumb, the eyebrow "OUR STORY" and the start of the H1. Screenshot: shots/top_about.png. | page builder |
| W3 | WARN | #mt-dynamic-positioning, #vestdavit, #services (1440), breadcrumb and eyebrow over image bands | Measured contrast of 12.8 px breadcrumb text against the real band pixels: 2.37 to 2.87 (Marine Technologies and Bridge Mate DP crumbs on the DP page), 3.38 (Service), 3.94 (Vestdavit crumb), 3.72 (eyebrow on the DP page). All below 4.5:1 for small text. Cause: no scrim under the crumb row on bright image areas. | page builder |
| W4 | WARN | all routes at 390 wide, footer link lists, breadcrumbs, phone link on #contact | Tap targets below the 44 px in the brief: footer links 350x30, breadcrumb links 24 px high (Home is 36x24), the phone link on #contact 350x32. The mobile menu itself passes (every item and the burger at least 44 high, at least 48 wide). | page builder |
| W5 | WARN | #home first load | Main thread is blocked for a long time at load. Time from navigation to the first evaluable document and to the first fully visible H1 and first non-blank 3D region: about 6.9 s in the instrumented run (earlier plain runs 4.4 s and 2.7 s for the h1 at 1440 and 390). Frame log: no animation frame between about 1.0 s and 2.7 s, so the word-by-word H1 stagger jumped from all words hidden to all visible and could not be observed frame by frame. Software GPU and a 13 MB parse inflate this, so indicative only, but a real device may show a blank or stalled first screen. | 3D module (scene build, shader compile) and page builder (decode of base64 assets) |
| W6 | WARN | #products, #products-marine-technologies, #team, #news | Heading order skips a level (h1 then h3, e.g. 1,3,3,3 then 2,2). Other routes are in order. Landmarks are fine (header 1, main 1, footer 1, nav present). | page builder |
| W7 | WARN | #home, hero 3D vs caption (design intent) | Not a defect in steady state, but during caption hand-offs two captions overlap while blurred (for example "From bridge to boat deck" and "Across Asia and Oceania" at scroll about 2100 px of 3780 at 1440). Not garbled once settled. Kept at WARN because the overlap is on the same lines, not side by side. | page builder |
| W8 | WARN | #home, text wording changes (content fidelity) | New home wording with no counterpart line in the old text: "The whole bridge, brought into one picture." and its support line (assembled from old phrases "from yachts and tugs to offshore and cruise vessels"), "Every position reference, in the simulator.", the labels "Radar and laser references" and "Satellite and taut wire", the counters "01 / 03 to 03 / 03 . Vessel systems simulator" in place of the old "01 . SEE INSIDE" (the one old line reported missing on any route), and "Explore the systems". No new numbers, names, dates, places or certifications. Owner (Rahul) should confirm he accepts new headings on a site where the old text is the truth source. | page builder |
| N1 | NOTE | all routes | Failed requests: only blob: range requests for video, net::ERR_ABORTED (browser abort when a clip leaves view). No other failures. | none |
| N2 | NOTE | #home mobile 390 | A soft vertical glow band (page colour about 5,10,18 rising to about 19,35,52 at the right edge) runs the full stage height beside and below the 3D. Not the canvas rectangle (see hero checks); reads as the intended soft glow but looks like a stripe on the phone. | page builder |
| N3 | NOTE | meta | One static meta description on all routes (checked the head on the routes visited), theme-color set, lang=en, viewport set. No per-route description, no canonical, no Open Graph. No design/seo-spec.md exists for this campaign, so no comparison could be made. Titles change per route (list below). | page builder |
| N4 | NOTE | #mt-dynamic-positioning | No view-mode tabs on this page (they exist on #home and #mt-dp-chair, 5 tabs each, all working). Brief lists the DP tabs generally, so confirm intent. | page builder |
| N5 | NOTE | memory | JS heap after load 12.6 MB; after three full passes over all 25 routes it settled at 5.2 to 5.4 MB (after forced GC). DOM nodes grew slightly each pass (1780, 1858, 1934), Documents stayed at 7, listeners at 37. No leak in heap, a small node drift worth a glance. | page builder |
| N6 | NOTE | #home hero | The build notes mention Partners-page stats (10, 9, 7, 6) but the rendered #partners page does not show them. Notes are out of date, not the site. | page builder (notes) |
| N7 | NOTE | external links | 7 external hosts, all target=_blank with rel noopener: the 6 principals' sites and the online simulator on github.io (a personal account page named Sinor-marine-Demo-; the brief approves the link). They need internet by design. | owner decision |

Not defects, recorded to avoid re-testing: the first run flagged the skip link as not first Tab stop. That was my script (focus had been set by a prior click); a clean run showed "Skip to content" as the first stop, visible at 141x39 (position 16,12), and Enter moves focus to main#view.

## 1. All routes at 320, 375, 768 and 1440 (script: routes.mjs, scroll.mjs)

Command: node /tmp/work/sinor-v2/tmp/qa/routes.mjs, then scroll.mjs (scrolls each page fully so lazy images load). 24 routes plus unknown route zz-unknown-route, 4 widths, one page per width with hash changes.
- Exactly one h1 on every route and width: PASS (100 of 100 route/width cases).
- Console errors and page errors: none, all cases. Failed requests: only the aborted video blobs (N1).
- Horizontal overflow (documentElement and body scrollWidth vs clientWidth): none at any width. Full-width blurred copy images (IMG.bl) extend past the viewport but are clipped (no scrollbar).
- Broken images: none among images that are rendered. The first run listed images with currentSrc empty; these are loading=lazy images (hidden hover previews and mobile or desktop-only card variants with display none, never needed) and images below the fold, so not defects. After scrolling each page fully, 0 visible broken images at 375 and 1440.
- Titles change per route (1440): home "Sinor Marine Technologies"; others "<page> | Sinor Marine Technologies": Products, Marine Technologies, Dynamic Positioning, Integrated Bridge System, Thruster Control System, DP Chair, JX and DP 0, Davits and launch systems, Handling systems, Controllable pitch propellers, Monitoring and control, Helideck safety and firefighting, Service, Training, Simulator, Our story, Team, Partner network, News, the three news items, Contact, "Page not found". Every route differs from the previous one: PASS.
- Scroll resets: scrolled to 3000 px then changed hash; scrollY was 5 or less on every route: PASS.
- Request hosts logged over the whole run (every request of 4 contexts): file: 4, blob: 258, nothing else. No http or https request at all.

## 2. Content fidelity (script: fid.py)

Method: old route text from /tmp/work/sinor-old-data/routes.json split into lines; new page text is document.body.innerText at 1440 after route change. Whitespace, case, quotes and arrows normalised; UI words ignored (Home, Scroll, Illustration, From the simulator, Explore, Read, slash, arrows). A line counts as present if it appears inside the normalised new text. Limits: line matching, one viewport (1440), text hidden by CSS display:none is not in innerText (mobile-only variants not compared).
- Old lines missing from the new page: 1 across all 24 routes (home: the label "01 . SEE INSIDE", W8). 23 routes: 0 missing.
- Old footer lines (the shell data: tagline, link lists, three contact lines, copyright line, owners line) all present in the new text.
- New text with no old counterpart (main view): home 11 lines (listed in W8, plus the hero image caption "Bridge Mate DP console, 3D illustration", which the brief asked for), #mt-dynamic-positioning 3 lines ("DIAGRAM" tags). All other routes 0. None contains a new number, name, date, place or certification.
- Sales email, phone number, office address: the email and phone found on every route match the old site's values exactly (set comparison, 0 mismatches over 25 routes; old data holds 3 distinct emails and 2 phones, the new site shows subsets of them). The office address, a 1-line item, is in the old shell footer and the contact route (36 lines of old contact text, 0 missing). Values are not quoted here on purpose.
- Company line "Pte Ltd" in the footer is as the old site has it.

## 3. Forbidden content (rendered text of 25 routes, and raw HTML with base64 stripped)

Terms: Sinor Marine Services, FZCO, Middle East, linkedin, NEEDED FROM RAHUL, lorem, em dash, en dash. Result: 0 hits in rendered text and 0 in raw HTML for all of them. "UAE": 3 rendered hits (home, services, partners) and 4 in raw source, all as a country in the service or partner lists, as permitted. Also in raw HTML: no tracker, analytics or cookie code was found by the request log (zero network) and by the three term searches; I did not run a separate search for analytics script names.

## 4. Hero (script: hero.mjs, misc.mjs, words.mjs, rs.mjs)

Home runway scrolled in 50 px steps (1440x900: 58 steps, runway 3780 px; 390x844: 48 steps with 50 px steps, runway 3207 px). Twelve screenshots each in shots/hero_1440_*.png and shots/hero_390_*.png (sheets: shots/sheet_1440.png, sheet_390.png). I looked at all of them.
- Four captions: all appear in order. Caption opacity at 1440 reached 1 for "Hold the vessel where it needs to be." (0 to about 600), "Built to keep working." (750 to 1200), "From bridge to boat deck." (1500 to 1950), "Across Asia and Oceania." (2250 to end). Same order on the phone. PASS.
- Words appear progressively: NOT verified frame by frame. Frame log shows a long stall (W5); all words were visible by the first screenshot. Lead and buttons did appear later than the H1 (lead opacity 0 at 1.0 s, 1 at 2.9 s).
- 3D canvas: renders and is non-blank at every sampled step; the twin-station console (two angled screens, joystick panels with red buttons, cabinet) is visible at every position. It rotates and changes pose with scroll (front view, three-quarter, top-down tilt, exploded-looking separated screens, then front view again): PASS.
- Lighter canvas rectangle: sampled 4 px outside and inside each canvas edge at 1440 and 390 (scroll 0): largest per-channel step 1 of 255 (invisible). The build notes' open issue appears fixed. One sample at scroll 800 on the phone gave a step of 32 at the top edge; that sample point is the header's bottom border line, not the canvas, so I discount it.
- Text overlap with the 3D: none. Desktop text column right edge 730 px, canvas left edge 773 px. Phone: canvas 76 to 383 px, text from 423 px, no overlap.
- Resize test: 1440 to 390 to 1440 to 390 to 768 to 1440: no horizontal overflow at any step, canvas buffer size follows the layout (603x730, 350x307, 699x390), burger and nav swap correctly, caption state identical to a fresh load at the same scroll, no errors. PASS.
- Fallbacks (screenshots shots/fb_*.png): reducedMotion emulated and WebGL disabled (confirmed no WebGL context in that browser), at 1440 and 390: hero gets class fb, the s70 still is shown (732 px wide image loaded), canvas display none, all four captions visible at once (opacity 1, visible), caption reads "From the simulator", counters show final numbers. No page errors. PASS.

## 5. Interactions with real mouse and keyboard (script: inter.mjs, media.mjs)

PASS: skip link (see note above); nav dropdown opens on hover, toggles aria-expanded on click, Escape closes it, a dropdown item navigates; product chips (5 chips: All 10 cards, Control 6, Handling 2, Propulsion 1, Safety 1, aria-pressed follows); partner country selector (China selected: 3 items, aria-pressed true); training accordion (6 items, aria-expanded false to true to false by mouse then Enter, panel visible); DP tabs on #home and #mt-dp-chair (5 tabs each, the active image index follows the tab); mobile menu (opens with aria-expanded true, focus moves to the first item, Escape closes and focus returns to the burger, a menu link navigates and closes it); Tab order on home (skip link, logo, nav items, hero buttons, then page links) and contact (breadcrumb, email link, phone link, name, email, message, submit, footer); focus ring on every stop: 3 px solid #8CC4F2 outline.
Forms (contact, services, training; same behaviour on all three): fields labelled via for/id (every input and textarea has a label); empty submit shows "Please enter your name."; invalid email shows "Please enter a valid email address."; valid input shows the prepared message in a read-only box; Copy puts the text on the clipboard and the label becomes "Copied"; the Open in email app link is a mailto to the sales address with subject and body; the form note says "This site cannot send mail by itself"; nothing says sent, thank you or received. The old "prepared" behaviour matches the brief.
Not tested: submit by Enter key inside a field, Copy fallback path when the clipboard API is denied, focus trapping inside the open mobile menu by Tab, keyboard operation of the DP tabs, Space and arrow keys on chips, hover states other than the dropdown.

## 6. Media (script: media.mjs)

- Film (#simulator, 180.6 s, 854 wide, controls, preload none): play() resolved, currentTime advanced to 2.9 s in 3 s, readyState 4, audio decoded bytes counted (17,875), not muted. Poster shown before play (all 8 posters load at 720x480).
- Clips: all 7 clips on #simulator reached readyState 4 and currentTime advanced (about 3.5 s after 3.5 s in view). Out of view all 8 videos were paused (IntersectionObserver works). Full quality of playback frames not inspected beyond this.
- Fonts: document.fonts.check true for Outfit (700) and DM Sans (400); both loaded from the embedded file (faces Outfit 100 to 900, DM Sans 100 to 1000, status loaded); headings use Outfit, body DM Sans.
- Logos: header mark 56x26 shown from a 640x298 PNG, aspect ratio preserved; pixel read of the image: corners alpha 0, about 75 percent transparent, 100 percent of opaque pixels near white, 0 percent blue, no background colour on the element or parent. Full logo on #about: 1500x489, 80 percent transparent, 100 percent white. Footer logo visible in shots/footer_1440.png as a white mark and wordmark on dark with no white box. The pixel read of the footer logo returned 100 percent transparent because the lazy image had not decoded at the moment; I rely on the screenshot for the footer. Header logo has empty alt next to the visible text wordmark (acceptable).

## 7. Accessibility basics that can be machine-checked

- Landmarks: header 1, main 1, footer 1, nav 2 or 3 per route (home has 2, others add breadcrumbs). One h1 per route. Heading order: W6.
- Image alt: every img has an alt attribute (0 missing on all routes at 375 and 1440); decorative ones use empty alt. Quality of the alt text was not judged.
- Form labels: PASS (section 5). Error text is in a role=alert paragraph; inputs get aria-invalid.
- Contrast: 461 text elements sampled at 1440 and 390 on home (8 scroll positions), products, about, services, training, contact, partners, news, team, simulator, DP page, Vestdavit. Method: hide all text, screenshot, take the real background pixels under each text box, composite the computed text colour with its effective opacity, compute WCAG ratios, judge the 10th percentile of the box (worst areas). Lowest results: the six items below 4.5:1 (W3 covers five; the sixth, 2.69 for a hero line, was caught at 44 percent opacity in the middle of a caption cross-fade and is not a steady-state value). Elements under the sticky header (top less than 76 px) were excluded after the first run produced false hits from sampling the header. Body text in steady state: 4.5:1 or higher in every sampled case other than W3.
- Tap targets on the phone menu: all at least 44 px high and 48 px wide. Elsewhere W4.
- prefers-reduced-motion: CSS has a reduced-motion rule and the hero fallback was verified; clips get controls under reduced motion by script (not visually checked); counters end at final numbers (verified).

## 8. Performance and robustness (indicative only, software GPU, not real-user)

- Navigation to first evaluable document and to the first fully visible H1 and first non-blank 3D region: about 6.9 s (instrumented run, includes 150 ms polling cost); other runs 4.4 s (1440) and 2.7 s (390) to the H1. Wide variation between runs; see W5.
- JS heap after load: 12.6 MB (after forced garbage collection); 5.2 to 5.4 MB after route passes.
- Three passes over all 25 routes: heap flat, nodes drift (N5).
- Resize 1440 to 390 and back: works (section 4).
- Mouse wheel scroll moves the page: PASS.
- Lab LCP and CLS were not measured; no real-user numbers exist.

## Titles listed against a spec

design/seo-spec.md does not exist for this single-file campaign, so titles were checked only for presence, uniqueness and brand suffix. Not compared with any approved copy.

## Candidate lessons for the Director (not recorded by me)

1. A single-file site opened over file:// with all media as blob URLs still shows lazy images as "broken" to a naive checker: scroll the full page before judging images, and count only rendered elements.
2. Contrast checks on pages with image bands need the text hidden and the real pixels sampled; the sticky header and mid-fade states give false hits, so exclude them and say so.
3. When a hero keeps many video and image bands in one document, measure the longest main-thread stall at load; a 1.7 s frame gap hid the headline stagger from the animation log.
4. Page-head text over drawn canvas scenes (service map, about photo scene) needs a scrim or a lower-contrast scene region; the build tests did not cover text collision with canvas labels.
5. Build notes drift from the build (partner stats mentioned, not rendered). Ask builders to refresh notes after final edits.
