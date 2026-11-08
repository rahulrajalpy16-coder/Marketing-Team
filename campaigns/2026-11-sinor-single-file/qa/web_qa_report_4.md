# Web QA report 4: Sinor Marine Technologies single file (build v5)

File tested: /tmp/work/sinor-v2/out/v5.html (13,438,236 bytes) over file://. Independent reviewer, did not build it. No source or copy edited. Scratch scripts, JSON, screenshots: /tmp/work/qa4 (shots in /tmp/work/qa4/shots). Date 2026-11-08. Playwright Chromium with SwiftShader.

## True verification scope
Tested: headless Chromium on Linux, software GPU only. NOT tested: real iPhone or Android, real touch scrolling (I used mouse.wheel and scrollTo only), Safari, Firefox, screen readers, a full WCAG audit, real GPU speed, real-user performance, hosting. web_qa.mjs was not run (it needs a campaign site folder; this is a single file) and there is no seo-spec for this campaign, so titles and descriptions were not compared with a spec. No word-for-word copy comparison was made. Contrast over the rendered object judged by eye only. Frame rate was not used as a measure.

Smoothness method: window.__SINOR_DEBUG=1, window.__co.state(). Per wheel step (cycle 40, 80, 120, 60, 100 px) I sampled before, 60 ms after, and 560 ms after. Only objects with vis above 0.1 counted. Five runs were in parallel on one CPU, so timing is noisy; the numbers below are indicative.

## Top defects

### D1  FAIL  #mt-dynamic-positioning, 390x844, on load: the hero console is tiny and faint until the user scrolls
- Repro: open file#mt-dynamic-positioning at 390x844 and wait 6 s. __co.state().console stays at vis 0.16, px 280, y 734 at 1 s, 3 s and 6 s. The hero slot (top 559, height 350) shows a small dim console below the buttons. It only grows once scrolling starts (vis 0.16 to 0.46 to 0.88 over the first three wheel steps of 40, 80, 120 px).
- Evidence: /tmp/work/qa4/shots/dp_390_0.png (first panel of /tmp/work/qa4/shots/m_dp.png). Chair, MRU and THCS heroes at 390 are full size on load, so it is specific to the DP page (hero slot sits low).
- Owner: 3D developer (visibility weight for a slot only partly on screen at load).

### D2  WARN  The "ILLUSTRATION" label is hidden behind the 3D object
- Home 1440x900 hero: caption reads "ILLUSTRAT... E MATE DP CONSOLE", the cabinet covers its middle (/tmp/work/qa4/shots/home_1440_0.png). #mt-dynamic-positioning 1440 at scroll 1700: label shows as "ILLUSTR" (dp_1440_1700.png). Phone: "ILLUS" cut on chair at scroll 1500 (m_chair.png), DP at 1800 (m_dp.png), THCS at 0 (m_mt.png).
- Effect: previous D3 is mostly fixed (a visible label now exists for 3D objects on every page I looked at) but it is partly unreadable when the object overlaps it. Owner: page developer (put the label above the model or give it a higher stacking level).

### D3  WARN  Home 390, scroll 4728 and 4900: a labelled slot with no object
- The "02 Motion reference" slot at those scrolls shows only the word ILLUSTRATION (plus a speck at 4728) and an empty dark band (/tmp/work/qa4/shots/d1_sheet.png). The MRU only reaches full visibility later (state sampled around scroll 5840). Reads as a gap, not a break. Owner: 3D developer.

### D4  WARN  Fast fade at one transition and 115 px jump while nearly invisible
- #mt-dynamic-positioning 1440, scroll 800 with a 40 px step: console x 1034 to 932 and y 274 to 325 (115 px) in 60 ms, but vis is only 0.17 falling to 0.07, so it is barely drawn. It breaks the 40 px target on paper, not visually.
- Vis falls from 0.98 to 0.12 across about 120 to 180 px of scroll at 390 (scroll 640 step 120). Gradual over three steps, not a pop, but quick on phone.

### D5  NOTE  Meta description is one string on all 24 routes, title is unique (24 of 24)
- Every route shows the Home description ("Sinor Marine Technologies, Singapore. Dynamic positioning, ..."). No seo-spec exists for this single-file campaign, so I cannot call it a spec failure. Owner: Director to decide.

### D6  NOTE  Object overlaps a card image
- #mt-dynamic-positioning 1440 at scroll 500: the hero console sits on top of the top of the "Illustration" diagram card (dp_1440_500.png). It is a graphic, not readable text. No text was covered in any desktop frame I looked at.

## Check 1: smoothness (owner's main complaint)
Target: no step moves the object more than about 40 px or turns it more than about 8 degrees. Values are the maximum over the whole page (80 to 260 steps each), while vis above 0.1, sampled 60 ms after the step. "Settled" = 560 ms after the step against the state before it (includes lag from earlier steps, so it is larger than one step really moves).

| Page and viewport | max move at 60 ms | max yaw at 60 ms | max size change at 60 ms (px*vis) | settled move / yaw |
|---|---|---|---|---|
| Home 1440 (7 objects) | 30 px (cabinet/helideck), 23 console | 6.5 deg (console) | 160 (console fade, vis change 0.31) | 41 px / 8.7 deg |
| Home 390 | 52 px (davit, step 120) | 7.0 deg | 149 | 121 px / 45 deg console (scroll 4800) |
| #mt-dynamic-positioning 1440 | 114 px once (D4, vis 0.17) | 5.0 deg | 265 | 114 px / 5 deg |
| #mt-dynamic-positioning 390 | 55 px | 1.7 deg | 84 | 134 px / 4 deg |
| #mt-dp-chair 1440 | 31 px | 1.1 deg | 39 | 116 px / 4.5 deg |
| #mt-dp-chair 390 | 35 px | 1.1 deg | 54 | 126 px / 3.9 deg |

- Yaw: PASS. At 60 ms the largest turn per step is 7.0 degrees (Home 390), under 8. Settled values reach 45 degrees on Home 390 console around scroll 4800 only when the object swaps slots, so the turn is spread over about 0.5 s and several steps. WARN-level, not measured per step.
- Position: PASS on desktop except the single D4 case. On phone (390) the object lives inside the page flow, so it moves with the content: 35 to 55 px for a 60 to 120 px wheel step (and 55 px for a 60 px step at DP scroll 300). That equals page scroll, I count it as normal but it exceeds the 40 px target number on paper in about 8 of the phone steps (max 55 px).
- Appearance and disappearance: PASS. Vis traces, DP 1440 console: 0.90 (scroll 640), 0.45 (700), 0.17 (700), 0.07 (800), 0.03 (920), 0.00 (1040), 0.14 (1100), 0.37 (1200), 0.80 (1240), 0.95 (1320), 1.00 (1440). Chair 1440: 0.80 (640) to 0.01 (840), back to 1.00 by 1440. No frame went 0 to 1 in one step. Largest single-step vis change 0.39 at 60 ms (Home 390), 0.30 to 0.49 settled on other pages.
- Previous complaint about small scrolls: at 40 px steps on desktop the largest move was 114 px once at near-zero vis (D4); otherwise 40 px steps moved the object under 30 px. Frame rate not used.

## Check 2: DP console model (1440x900 hero and chapters)
Screenshots: home_1440_0.png, dp_1440_0.png, dp_1440_500.png, dp_1440_1100.png, dp_1440_1700.png. PASS: matte dark cabinet with four visible bolt heads, dark screen with red and green graphics, blue and grey control panel, white knob with arrow cross at left (visible in dp_1440_1700), ball-top joystick, keypad with oval keys, trackball with a red ball at right. No z-fighting, no parts floating, texture not mirrored, screen text is small but its layout is legible at chapter size (dp_1440_1700) and tiny at hero size (expected). The cabinet looks mid grey, not black, in the hero because of lighting. I compared against the described photograph from text only, I did not see the photograph.

## Check 3: chair, MRU, thruster station
- Chair (chair_1440_0.png, chair_1440_1200.png, m_chair.png): head and chapter two present, MT badge on headrest, two armrest touchscreens, plinth. No broken geometry seen. Docks to the right in the head and left in chapter 2 with text opposite (1440: slot left 763 then 124). Chair at 1440 scroll 1200 overlaps nothing readable.
- MRU (mru_1440_0.png) and thruster station (thr_1440_0.png): present, sensible, no overlap with text. The label is visible below them.
- Floating tiny object between sections (old D2): not found on desktop frames. Found only in D1 (phone DP hero on load).
- Overlap of readable text, phone 390: none found in the frames I looked at (chair, DP, MRU, THCS and Home 4500/4728/4900). Old Home D1 (console over "Launch and recover" at 4728): not reproduced, the console is gone at 4728 and 4900 (d1_sheet.png). Note: that section is now "02 Motion reference".
- Wrong-side docking: PASS, see D5 below in recheck. I did not capture every chapter of every page.

## Check 4: datasheet downloads offline: PASS
Clicked the button on each page with the network blocked. Saved files start with %PDF- and end with %%EOF:
- #sinor-mru: Sinor-Marine-MRU-datasheet.pdf 3286859 bytes, expected 3286859.
- #mt-dynamic-positioning: Bridge-Mate-DP-brochure.pdf 2833662, expected 2833662.
- #mt-dp-chair: Bridge-Mate-DP-Chair-brochure.pdf 715169, expected 715169.
- #mt-jx-dp0: Bridge-Mate-JX-and-DP0-brochure.pdf 656242, expected 656242.
Files are in /tmp/work/qa4/dl_*.pdf. I did not read the PDF contents.

## Check 5: regression
- Routes: 24 in window.SINOR_ROUTES (the last report counted 23). At 390 and 1440 (48 cases), offline: zero console errors, zero page errors, zero external requests (every non file, data, blob request aborted and logged; none), exactly one h1, no horizontal overflow (scrollWidth equals viewport), #companion canvas aria-hidden="true". PASS.
- Click-through: PASS. Canvas pointer-events none; Home "Explore products" is the element at its own centre and a real click went to #products.
- Reduced motion (emulated) and WebGL disabled (getContext returns null for webgl), Home, DP, chair, MRU at 1440 and 390: no co-on class, hero has class "fb", all images with width above 50 px loaded (bad count 0), no overflow, one h1, zero errors, zero external requests. PASS by DOM measures. I did not open the fallback screenshots (/tmp/work/qa4/shots/rm_*, nogl_*) to look at the stacked hero, so "stacked hero" is inferred from the fb class only. In the no-WebGL runs the canvas is display block with opacity 0 (invisible, not removed).
- Old hash: setting #simulator lands on #products, h1 "Everything on the bridge and the boat deck." PASS.
- Simulator wording: Home "Induction, simulator, maintenance, familiarisation and refresher" and #training "training simulation courses" and "Simulator (Advanced)" only. No simulator or github link anywhere (0 hrefs). PASS (course names only).
- No lorem ipsum, no en or em dash in rendered text on any of the 24 routes at 1440 and 390 (regex on innerText). PASS.

## Check 6: honesty
- 3D objects: slot aria-labels begin "Illustration of ...", and a visible ILLUSTRATION tag appears under the 3D object in the hero of Home, DP, chair, MRU and THCS at 1440 and on phone (see D2 for occlusion). The Home hero caption is now display block.
- Real pictures: the MRU page shows a card labelled "SINOR MRU DATASHEET" (m_mt.png). I did not check every picture on every page.
- Facts: not re-verified this cycle beyond the verified-facts lines about the MRU, MT console and entity name. Numbers copied from partner pages remain not independently verified.

## Recheck of report 3 defects
- Old D1 (console over heading, Home 390 at 4728): FIXED at the positions tested (d1_sheet.png). Not a full sweep.
- Old D2 (tiny duplicate object floating between sections): FIXED on desktop (objects fade to 0 before the next appears, one object per type at a time). Similar symptom now only in new D1 (DP phone hero).
- Old D3 (no visible illustration label): MOSTLY FIXED, but partly hidden behind the model (new D2).
- Old D4 (aria-label "turning as you scroll"): FIXED for the console ("Illustration of a Bridge Mate DP console"). Other labels not all read.
- Old D5 (data-side mismatch): FIXED on #mt-dynamic-positioning 1440: data-side right at left 763, left at 124 for the other three slots.
- Old D6 (copy on operator stations): UNCHANGED. #mt-dp-chair still says "comes with DP 1 and DP 2 operator stations", #mt-dynamic-positioning "distributed operator stations". NOTE, Director decision.
- Old D7 (route count): now 24, NOTE only.

## Verdict
The model rebuild is good: the console, chair, MRU and thruster station look finished and nothing is broken, the downloads are byte-exact, and offline, fallback and click-through behaviour are clean. Smoothness is much better: small wheel steps now move the object under about 40 px and under 8 degrees on desktop, and objects fade in and out over several steps instead of popping. Two things should be fixed before the owner sees it. First, on a phone the DP page starts with a tiny, faint console that only grows after the first scroll (D1). Second, the ILLUSTRATION label is partly hidden behind the models (D2), which weakens the honesty labelling. Phone motion follows the page, so a step of 60 to 120 px moves the model by about the same amount, and I could not test a real finger swipe, so that should be checked on an iPhone.

## Candidate lessons for the Director
1. Measure smoothness from state per scroll distance (60 ms and settled), not fps, and do not run many SwiftShader pages at once: it distorts timing.
2. Check the first view on load per viewport; a slot that sits low on phone can leave the object at low visibility until the first scroll.
3. A visible label near a 3D object needs a stacking check against the object, not only a presence check.
