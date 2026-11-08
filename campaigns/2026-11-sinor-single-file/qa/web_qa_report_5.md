# Web QA report 5: pinned 3D stages, single HTML build v7

File tested: /tmp/work/sinor-v2/out/v7.html (13,915,437 bytes), opened over file://. Source read for reference only. Nothing in the source or the copy was edited. Scratch scripts and screenshots: /tmp/work/qa5 (scripts *.mjs, screenshots in /tmp/work/qa5/shots, JSON results hold3_1440.json, hold3_390.json, pin_1440.json, pin_390.json, reg5.json).

Reviewer: independent (did not build this). Headless Chromium on Linux with SwiftShader (software GL), Playwright. Phone runs used 390x844 with hasTouch and isMobile emulation; desktop runs used 1440x900.

## Top defects (fix first)

### D1  FAIL  A ghost 3D model stays on screen on top of footer text (and on top of a drawing on Home) after a fast jump in scroll
- Routes: #seaonics, #mt-dp-chair, #mt-dynamic-positioning, Home. Both 1440x900 and 390x844 (phone emulation).
- Steps: load #seaonics, wait 3 s, then scrollTo(0, 5188) in one step (or press End, or one mouse wheel of 5000 px, or a stepped scroll of 500 px per 16 ms). Wait 1.5 s or longer.
- Result: __co.state().crane.vis stays at 0.2 forever (value did not change over time). The crane is drawn at 20 percent opacity over the footer logo, tagline and link list. On the phone it sits over the footer "Products" list. Same on Home at y 20982 (1440) and 17300 (390): the console at vis 0.2 is drawn over the blueprint drawing and its labels ("BOW TUNNEL THRUSTER" is crossed).
- Cause (from reading the source, not edited): vis moves toward its target by a fraction on each rendered update (glide 0.8 per frame). When the scroll lands in one big step and then stops, the render loop does not keep updating, so the glide freezes partway. The pose is therefore not a pure function of scroll position: it depends on how you arrived.
- Not reproduced when the scroll arrives in steps of 150 px per 16 ms (vis 0.001), nor after a reload at that position (vis 0). So it appears on End key, long jumps, anchor jumps, and possibly very fast flicks. I could not test a real finger flick.
- Evidence: /tmp/work/qa5/shots/ghost_1440_end.png, /tmp/work/qa5/shots/ghost_390_jump_4925.png, /tmp/work/qa5/shots/ghosthome_1440_20982.png
- Return to the same point gave a different state in 12 of 104 hold points at 1440 and 13 of 109 at 390 (all in the tail of the page after the last pinned section, where vis is 0.09 to 0.2 or the hidden object has a different y). Every one of these is this same defect.
- Owner: web-developer (companion3d.js applyAll / frame loop). Suggested direction: snap vis (and the other glided values) to target, or keep updating until converged, so the state is a pure function of scroll.

### D2  FAIL  On the phone the 3D object covers the heading and eyebrow of the section while it is pinned
- Route and viewport: Home at 390x844, first section ("01 CONTROL", "The whole bridge, brought into one picture."). Also #mt-dynamic-positioning at 390x844, second section ("DP 2 ARCH...", "Three controllers vote."): the console base covers the heading and the first line of body text.
- Steps: scroll to any point inside the pinned section (the object holds still, so it covers the text at every scroll point of the section, about 800 px of scroll).
- Result: the console pedestal covers the eyebrow and the middle of the h2 ("The w...ture."). Measured: object centre y 247 and size 270, h2 top at y 460. Screenshots: /tmp/work/qa5/shots/s390_021_4431.png (full size) and /tmp/work/qa5/shots/sheet_mid390.png (items 1 and 10).
- The other phone sections (MRU, davit, handling, propulsion, mTrack, helideck, installation, operator, chair, seaonics) sit above the text with no overlap in the screenshots I looked at (sheet_mid390.png).
- Owner: web-developer (phone dock size for tall console, e.g. cap console size or height on the 40svh slot).

### D3  WARN  The fade in and out is steeper than the target
- Target in the brief: change of vis per 40 px of scroll below about 0.15.
- Measured with a frame-aware settle (10 frames after each 40 px step, so the lab frame rate does not distort it): Home 1440, console fading in: 0.08, 0.28, 0.52, 0.75, 0.92, 1.0 per step, so the maximum is 0.24 per 40 px and the fade is over about 200 px. Home 390, console fading out: 0.99, 0.72, 0.27, 0.00 per step, maximum 0.44 per 40 px, fade over about 120 px. Steps above 0.15 in the Home range tested (first two sections): 12 of 93 steps at 1440, 8 of 83 at 390. Quick first pass with a short fixed wait gave larger numbers (up to 0.73 on phone, 0.78 on #mt-dynamic-positioning phone) but that mixes in frame lag, so I rely on the settled numbers above.
- It is continuous (no pop, no single step from 0 to 1), so I rate it WARN. It will look fast on a phone: a roughly 120 px scroll takes the object from gone to full.
- Owner: web-developer (widen the blend zone on phone).

### D4  WARN  Two different models are visible at once during section changes
- Home 1440: 69 of 656 scan positions have two objects above 0.05 vis (for example console with MRU, MRU with davit, davit with crane; fully crisp at the same time in /tmp/work/qa5/shots/sheet_1440_4.png frame 6). On the phone I found 0 such positions. Neither covers readable text on desktop, so this is a look issue only.
- Owner: web-developer / designer. Decide if overlap is wanted.

### D5  WARN  The fixed label "3D MODELS ARE ILLUSTRATIONS" sits on top of page content
- It is a fixed element at bottom left. On the phone at the page end it sits on top of the footer "Company" label (ghost_390_jump_4925.png). On the phone, between sections it also crosses the "Explore the systems" button area in /tmp/work/qa5/shots/s390_018_3798.png (bottom). Desktop: it sits near the footer copyright line without overlapping.
- Owner: web-developer.

### D6  NOTE  Home page is very tall after pinning
- Home total height with 3D on: 27,128 px at 1440x900 (30.1 viewports) and 27,297 px at 390x844 (32.3 viewports). With the fallback (no 3D) the same page is 18,764 px (20.8 viewports) at 1440 and 21,303 px (25.2 viewports) at 390. So pinning adds about 8,400 px at desktop, 6,000 px on the phone. Seven pinned sections of 210 svh (1890 px at 900 high) or 190 svh (1604 px at 844 high). Other routes with 3D: DP 13,894 (1440) and 12,198 to 12,359 (390), chair 7,933 and 7,218 to 7,380, seaonics 6,560 and 6,502 to 6,664. Whether this is "absurd" is a Director decision. It is long, but every page scrolls to its very end.

### D7  NOTE  Yaw turn across the pinned hold is about 30 degrees, not 90
- Measured with the state: DP page sections, from pin start to pin end: yaw changes 3.4 to -27.5, -16.8 to -47.8, 6.9 to -22.7 (1440), and 1.9 to -24.6, -18.5 to -44.9, 5.8 to -20.7 (390). That is 26 to 31 degrees while the section is pinned. The code uses (progress - 0.5) times 90, but the section progress runs over viewport plus section height, so the pinned part gets only a third of the span. If the owner expects about 90 degrees while pinned, this is short. Director decision.

## Results by test item

### 1. HOLD (zero drift and return)
Method: __co.state() read after scroll, wait 450 ms, then also wait for at least 12 rendered frames, record (A). Wait 2 s plus 12 frames, record (B). Compare every field (x, y, px, yaw, pitch, ex, cy, vis) of every object visible (vis above 0.01) in either record. Then scroll 2500 px away, back to the same point, wait, and compare with (A). Home, #mt-dynamic-positioning, #mt-dp-chair, #seaonics, at 1440x900 and 390x844 (touch emulation). Points are evenly spread through each page plus points inside transitions (vis between 0.1 and 0.9), counts in the table (script hold3.mjs, outputs hold3_*.json).

| Route | Viewport | Hold points (of which mid transition) | Drift between A and B | Return to same point identical |
|---|---|---|---|---|
| Home | 1440 | 30 (9) | 30 of 30 below 1e-9 (max 3.3e-11; 13 exactly 0) PASS | 28 of 30 (2 fail, D1) |
| DP | 1440 | 32 (11) | 32 of 32 below 1e-9 (max 1.6e-10) PASS | 29 of 32 (3 fail, D1) |
| Chair | 1440 | 23 (7) | 23 of 23 (max 1.5e-11) PASS | 19 of 23 (4 fail, D1) |
| Seaonics | 1440 | 19 (6) | 19 of 19 (max 1.1e-12) PASS | 16 of 19 (3 fail, D1) |
| Home | 390 | 32 (11) | 32 of 32 (max 6.5e-12) PASS | 30 of 32 (2 fail, D1) |
| DP | 390 | 35 (14) | 35 of 35 (max 2.0e-11) PASS | 32 of 35 (3 fail, D1) |
| Chair | 390 | 24 (8) | 24 of 24 (max 3.4e-12) PASS | 20 of 24 (4 fail, D1) |
| Seaonics | 390 | 18 (4) | 18 of 18 (max 5.1e-13) PASS | 14 of 18 (4 fail, D1) |

- Drift: PASS. Zero drift for the visible object once frames have run: 213 of 213 points, including all 70 mid transition points. Differences of 1e-11 are floating point residue, not motion.
- Caveats on drift. (a) With a pure 450 ms wall clock wait and no frame wait, my first pass (hold2) did show drift up to 0.19 in vis and hundreds of px in y in places. That run had only 4 to 17 frames per second under SwiftShader (two browsers in parallel), so 450 ms was fewer than 12 frames. On a real GPU at 60 fps 450 ms is about 27 frames and would be settled; I could not test this. (b) The vis glide (0.8 per frame) is still a frame based ease, it is just very fast (below 1e-4 after 7 frames).
- Return to same point: FAIL for 12 of 104 points at 1440 and 13 of 109 at 390 (table), all in D1 territory (tail of page after the last section, or hidden object y). For points inside pinned sections and transitions the return state was identical (below 1e-9) in every case.
- A first sweep (hold.mjs, 450 ms only, all objects including hidden ones) is in hold_1440.json and hold_390.json. It is superseded by hold3 because hidden objects have no visible effect and the frame rate distorted it.

### 2. PINNING
- Section height: every .co-sec on Home is 1890 px at 900 high (210 svh) at 1440, and 190 svh at 390 (seaonics 1603.6 px at 844 high). PASS against the 190 to 210 spec.
- Sticky: wrapper position is sticky (checked through screenshots and measured positions; the slot and text do not move across 11 points per section).
- Home, 7 sections, 11 scroll points per section inside the pinned range, 1440: slot position identical or within 1 to 2 px (sub pixel and reveal animation), h2 position within 1 px after the reveal animation finishes (first point of some sections is 2 to 30 px off while the text reveal is still fading in: for example 297 then 295). 390: slot and h2 within 1 px at all points (h2 y 460 at every point, 458 to 461 at the section ends). PASS.
- Text vs slot rectangle overlap: none at any point (pin_1440.json, pin_390.json). Text block stays under the header (top at or below 253 px) and inside the viewport.
- Visual overlap, 47 screenshots at 1440 and 43 at 390 taken every 0.25 viewport from the top through the end of the third section (/tmp/work/qa5/shots/s1440_*.png, s390_*.png, contact sheets sheet_1440_0..5.png and sheet_390_0..5.png), plus one mid pin shot of every co-sec on Home, DP, chair and seaonics at both sizes (shots/mid_*.png, sheet_mid1440.png, sheet_mid390.png). Desktop: no object covers text at any inspected point. Phone: FAIL for the 2 cases in D2, other sections clear.
- Desktop note: the console in the first section of Home and in "Less cable, easier retrofit" is cut off by the bottom edge of the viewport (pedestal runs off the screen). This looks intentional, I list it as NOTE.

### 3. ENTER AND EXIT
- No pop: PASS. Settled vis changes smoothly over 5 to 6 steps (see D3 for the steepness).
- Scale: PASS. Object size goes from 93 percent to 100 percent while vis goes from 0 to 1 (648 to 693 px on the Home first section at 1440, 251 to 270 on phone).
- No tiny floating objects: PASS. The smallest visible size is 93 percent of the dock size, and the object disappears below vis 0.01. Nothing small was seen in the screenshots.
- Object left behind after its section: PASS when scrolling in steps (vis 0 at all 40 px stops in the tail of #seaonics, both sizes). FAIL after a jump, see D1.
- Two models at once: see D4.

### 4. FALLBACKS
Emulated prefers-reduced-motion, and WebGL off (getContext override returns null for webgl), Home, DP, chair, seaonics, 1440 and 390 (16 cases, script fb5.mjs).
- html has no co-on class in all 16 cases. All 7 Home sections are 111 svh at 1440 and 112 to 128 svh at 390 (not 190 to 210), wrapper position static. PASS.
- Stills: every .co-slot image loaded (naturalWidth above 0), opacity 1, sizes 551x661 at 1440 and 348x521 at 390. Screenshots show the console, MRU and the other stills stacked next to their text with the ILLUSTRATION tag, no blank block, no overlap (shots/sheet_fb1440.png, sheet_fb390.png, fb_*.png). PASS.
- Slot and text rectangles: no overlap (overlap false in every section). No horizontal overflow (scrollWidth equals viewport width). One h1. Zero console errors, zero external requests. PASS.
- WebGL off: the canvas element stays in the DOM with opacity 0 (display block) and the fixed label has opacity 0. Harmless, invisible. NOTE.

### 5. REGRESSION
- All 24 routes in window.SINOR_ROUTES, at 1440 and 390 (48 cases), offline (every request that was not file, data or blob aborted and logged): zero console errors, zero page errors, zero external requests, exactly one h1, no horizontal overflow, #companion canvas aria-hidden true, canvas pointer-events none, no lorem ipsum, no en or em dash in rendered text. PASS.
- Scroll reaches the end: after scrollTo(bottom), scrollY plus innerHeight equals the document height and the footer is fully in view on all 48 cases. PASS.
- Links under the canvas: a real click (desktop) and a tap (phone emulation) on "See the MRU Solution" inside the second pinned section at mid pin hit the link (elementFromPoint is the link) and changed the hash to #sinor-mru with h1 "MRU Solution". PASS. Footer links were visible and reachable (scroll end).
- Keyboard: 70 Tab presses on Home at 1440 and 390 and on #mt-dp-chair. All 7 pinned section links on Home (each "Explore the systems", "See the MRU Solution", "See davits", "See handling systems", "See propulsion", "See monitoring and control", "See helideck safety") were reached in document order, each fully in the viewport, not under the fixed header (header bottom 72 px), and the topmost element at the link centre was the link. Focus ring on every focused element: solid 3px outline (0 elements without outline). 5 large product cards on phone were 1 px past the bottom edge when focused (bottom 845 of 844), I counted that as fine. Tab order itself loops back to the top of the page after the footer (so the "monotonic" check is not meaningful past the wrap). PASS. Not tested: DP page and seaonics page by keyboard.
- Datasheet downloads: 4 buttons (a[data-doc]) on #mt-dynamic-positioning, #mt-dp-chair, #mt-jx-dp0, #sinor-mru each produced a download. Sizes 2,833,662, 715,169, 656,242, 3,286,859 bytes, start with %PDF, end with %%EOF, and SHA-256 prefixes match the source files in /tmp/work/sinor-v2/src/media/doc (e36f91c9c977, b65b81631ab3, 51ad9e52f6c4, d5371cdadc71). Byte exact. PASS. Only those four routes have a download button (the loop covered every route, no other route has one).

## What was NOT tested (true scope)
- Headless Chromium on Linux with SwiftShader software rendering only. Not tested: a real phone, real finger touch scroll and momentum (my "phone" is a Chromium viewport with touch emulation and programmatic scrolling), iOS Safari, Android Chrome, Firefox, a real GPU, screen readers, a full manual accessibility audit (WCAG), and real-user performance. Frame rate here was 4 to 30 fps under SwiftShader, which is not what the owner saw on a phone. I did not measure LCP or CLS in this round, and any lab numbers would be indicative only anyway.
- No visual check of the 3D hold under real scroll inertia. The owner's original complaint (models moving after he stops) is addressed as far as state held still for 2 s in this lab, but only a real phone test can confirm it.
- Not re-checked this round: body copy vs copy/ files, titles and meta descriptions vs design/seo-spec.md, facts vs verified-facts.md, forms. No copy or fact change was reported in the brief, I did not re-run those checks.
- Keyboard test covered Home and #mt-dp-chair only. The pin and hold tests ran on Home, DP, chair and seaonics only; the other 3D routes (#mt-thruster-control, #mt-jx-dp0, #sinor-mru and others) were only run in the regression pass, not for hold or pin.
- Pin screenshots were examined through the first three sections in full (every 0.25 viewport) and through one mid pin screenshot of every section. I did not open every frame at full size; most were read as contact sheets.

## Pass list (short)
- Hold: zero drift (below 1e-9) in 213 of 213 hold points at both sizes, including 70 mid transition points.
- Return to point: identical for all points inside sections and transitions (fails only in D1 territory).
- Pinning: sections 210 svh (desktop) and 190 svh (phone), slot and text fixed within 1 to 2 px, no rectangle overlap, no text covered on desktop, text clear below header.
- No pop, scale 93 to 100 percent, no tiny objects, stepped scroll leaves nothing behind.
- Fallbacks (reduced motion, no WebGL): not sticky, not 190 to 210 svh, stills visible, no overlap, no errors.
- 24 routes at 2 widths: zero errors, zero external requests, one h1, no overflow, aria-hidden canvas, scroll reaches the end, pinned links click through, keyboard order and visible focus on Home, PDFs byte exact.

## Verdict (plain language)
The core fix works in this lab: once the page has been scrolled to a point and rendered, nothing moves, the text and the model hold still inside each pinned section, the size change at the edges is small (93 to 100 percent), and the fallbacks, routes, keyboard and downloads are all clean. It is not ready to hand back to the owner yet, because of two real faults. On a phone, the tall console covers the heading of two sections for the whole time they are pinned (Home first section and the second section of the DP page), and after a fast jump in scroll (End key, an anchor jump, a very fast flick) a faded model can be left on screen over the footer text or a drawing until the next scroll, which also means the pose is not purely a function of scroll as intended. The fade in and out is also quicker than the target (about 120 px on a phone) and two models can show at once on desktop. I could not test a real phone or real touch momentum, so the owner's phone check is still needed after these are fixed.

## Candidate lessons for the Director
1. For "pure function of scroll" claims, test arrival path as well as position: jump directly, step slowly, and reload at the same position, then compare state. A smooth step test hides state that depends on history.
2. Measure animation settle by frame count (wait for N rendered frames), not wall clock, when the lab uses software GL at 4 to 30 fps. A 450 ms wall clock wait is not equal to 450 ms on a phone.
3. On phone, check the model's drawn extent against the text block, not only the slot rectangle. The slot never overlapped the text, but the object was drawn larger than its slot.
4. Pin height and sticky tests need the fallback page height too, to report what pinning costs (about 8,400 px on Home at desktop).
