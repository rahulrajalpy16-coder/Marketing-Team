# Web QA report 3: Sinor Marine Technologies single file (travelling 3D companion build)

File tested: /tmp/work/sinor-v2/out/Sinor-Marine-Technologies-Website.html (2,538,554 bytes), opened over file://.
Reviewer: independent web QA (did not build it). No source or copy file was edited. Scratch scripts, screenshots and logs: /tmp/work/qa3 (shots in /tmp/work/qa3/shots).
Date: 2026-11-07. Engine: headless Chromium with SwiftShader (software GPU), Playwright.

## True verification scope

Tested: headless Chromium on Linux with a software GPU only. Not tested: real iPhone or Android, Safari, Firefox, screen readers, a full manual WCAG audit, real-user performance, hosting or HTTPS. Frame rates and draw counts here come from a software renderer and say nothing about real devices. Memory numbers are a lab sample only. Not run: web_qa.mjs (it needs a campaign site folder and this is a single file, so I wrote my own scripts), the title and meta check against design/seo-spec.md (this campaign has no seo-spec, only a build spec), a word-for-word copy comparison against the old site, and pixel-level contrast measured over the rendered 3D object.

## Top defects (fix first)

### D1  FAIL  Home, 390x844, scroll about 4728 px: the 3D console covers a heading
- Page: #home. Location: the "02 Launch and recover" section heading, where the object glides from the console section to the davit section.
- Reproduce: open the file at 390x844, go to #home, run scrollTo(0, 4728), wait 1.5 s. The console cabinet (drawn on the fixed canvas, z-index 20, pointer-events none) is about 350 px wide and reaches down to about y=555. It sits on top of the "Launch and recover," line, so that line reads as "Launch ... recover" with the cabinet across it. The line below it, "swiftly, silently, safely.", is partly clipped by the base ring.
- Evidence: /tmp/work/qa3/shots/home390_08.png. The render loop was running (232 draw calls in 500 ms), so this is the steady glide state, not a stale frame.
- Cause: the canvas sits above page text, and between two slots the object is drawn at a size and position that covers the next section's text.
- Responsible: 3D and page developer (companion3d.js dock blend and size while between slots; or give text a higher stacking level than the canvas or fade the object when it would overlap text).
- Not found at 1440x900 in the frames I looked at (see passes), but phone is where text and object share the same column.

### D2  WARN  A second, tiny copy of the next object floats in empty space between sections
- Pages and viewports: Home at 1440x900 (davit large at the top while a tiny winch sits at the lower right, /tmp/work/qa3/shots/home1440_10.png); #mt-dynamic-positioning, #vestdavit and #training at 1440x900 at scroll 630 (a small object hangs in a blank band with the large slot scrolled away, sheets sheet_mtdp1440_0.png, sheet_vest1440_0.png, sheet_train1440_0.png).
- Reproduce: open the page, scroll 630 px, wait 1.8 s.
- Effect: looks like a stray artefact or a duplicate. On Home it is two different objects on screen at once.
- Responsible: 3D developer (shrink-and-hold behaviour of the docked object when its slot leaves view; fade to zero instead).

### D3  WARN  The 3D objects carry no visible "illustration" label while 3D is running
- All pages with slots. In 3D mode the hero caption "Illustration of a Bridge Mate DP console" is hidden by CSS (html.co-on .hero-cap display none; measured display:none on #home). The six Home tour objects, the product page heads and the chapter slots have only an aria-label (role="img"), nothing visible. The visible "ILLUSTRATION" tags found (Home 4, #mt-dynamic-positioning 3, #vestdavit 2 and so on) belong to the 2D diagram and card images, not the 3D object.
- Fallback mode does show the caption in the hero only (seen in /tmp/work/qa3/shots/nogl_sheet.png). Fallback stills in slots on product pages have no visible label.
- No text calls any of it a product photo, CAD or the real product (see honesty pass), so nothing is false. But check 7 asks for each object to be labelled or described as an illustration, and the visual label is missing.
- Responsible: page developer (a small visible "3D illustration" tag near each slot, or one persistent note near the hero).

### D4  WARN  Slot accessible name says "turning as you scroll" even when nothing turns
- The console slot aria-label reads "Illustration of a Bridge Mate DP console, turning as you scroll". In reduced-motion and no-WebGL modes the slot shows a still, so the name is wrong for those users. Same label on #training, where the still is a console desk view.
- Responsible: page developer.

### D5  NOTE  data-side value disagrees with layout on every fourth chapter slot
- #mt-dynamic-positioning, 1440 wide: the "exploded" slot has data-side="right" but sits at left=124 px (text is on the right). The slot is on the left because the page flips every odd chapter, while the side value cycles on i % 4. The object docks to the slot rectangle, so position is right. Only the turning direction (yaw sign) is mirrored for those slots. Not visible as a defect in my frames.
- Responsible: page developer (app.js line with i % 4 === 1 ? 'left' : 'right').

### D6  NOTE  Copy about several operator stations sits near a single-operator console model
- No text mentions two operator stations, twin consoles or a twin station for the console itself (searched rendered text on 14 pages: zero hits for two operator, twin, dual operator, second operator). The hero and the "One station, every control in reach" chapter say a single station.
- Architecture copy (old-site content) does say "distributed operator stations" (#mt-dynamic-positioning), the DP2 and DP3 diagrams show two or three "OPERATOR STATION" boxes, DP3 text says "a minimum of three operator stations", and #mt-dp-chair says it "comes with DP 1 and DP 2 operator stations". These describe system architecture, not the console, but a reader next to a single 3D console may be confused. No change needed unless Rahul wants a one-line clarifier.
- Responsible: copywriter or Director to decide.

### D7  NOTE  Route count is 23, not 24
- window.SINOR_ROUTES has 23 entries. That is expected after removing the simulator route (old list had 24).

## Check 1: Vessel Systems Simulator must not appear: PASS

- Visited all 23 routes at 1440x900 (fresh page each). Rendered body text, every link href, and every img, video and source src: no match for "github", no href containing "simul", no simulator src. Zero rendered "Launch the simulator", "Try the simulator", "From the simulator" or "Vessel Systems".
- Raw HTML with base64 stripped (805,325 chars left): github.io 0, "Vessel Systems" 0, "Launch the simulator" 0, "Try the simulator" 0, rahulraj 0, lorem 0, "Sinor Marine Services" 0, FZCO 0. The word "simulator" occurs 3 times in code and data: one JS comment ("photo from the Sinor Marine simulator film"), one service blurb, one redirect line for the old hash.
- Legitimate course wording only: Home and #services "Induction, simulator, maintenance, familiarisation and refresher"; #training "Dynamic Positioning Operator Basic (Induction) and Simulator (Advanced)", "DP Operator Induction and Simulator courses", "training simulation courses".
- No video elements remain on the 23 pages (one video template exists in code, unused). Media list contains only r_*.jpg renders and logos, no simulator screens.
- Nav and footer: no Simulator link (read the nav and footer text on all routes via innerText, no "Simulator" item).
- Old hash: #simulator lands on #products (location.hash "#products", h1 "Everything on the bridge and the boat deck.").
- External hrefs only to partner and maker sites (www.marine-technologies.com, partner domains), opening in a new tab.

## Check 2: travelling 3D object

- Home hero: four poses of the console at 1440 and 390 (frames home1440_00..04 and home390_00..04): front, profile, desk, front again. It is a single-operator console (one angled screen, one joystick panel, cabinet). Text and object do not overlap in the hero at either width (1440: text left, object right; 390: object top, text below). My automated overlap test flagged the hero at 390, but those hits are the hero's placeholder spans overlapping text boxes; the screenshots show no overlap. PASS.
- Home six sections: console (01 Control), davit, winch, propeller, control cabinet, helideck, one per section, in that order, with the matching headings (frames home1440_09..16, home390_07..17). PASS for content and order.
- Product pages: object in the page head and in every second chapter on #mt-dynamic-positioning (console), #vestdavit (davit), #matre (helideck), #seaonics, #servogear, #scantrol slot lists (winch, prop, cabinet cabinet). Slot counts: DP 4, integrated bridge 2, thruster 3, DP chair 2, JX 2, others 2. I looked at scroll screenshots for #mt-dynamic-positioning (1440 and 390), #vestdavit (1440), #matre (390), #services (1440, list only), #training (1440), Home (1440 and 390). I did not look at scroll frames for #seaonics, #servogear, #scantrol, #mt-thruster-control, #mt-dp-chair, #mt-jx-dp0, #mt-integrated-bridge.
- Left and right docking: at 1440 the slot rectangles alternate right (x=763) and left (x=124), and the text sits on the opposite side. In the frames the object sits in its slot with the text opposite. PASS (see D5 for the label mismatch).
- Cut off: objects are cut by the viewport edge or the header only while sliding in or out (for example home1440_10 davit apex under the header, matre390 idx 0 helideck at the bottom edge). Natural for a scroll effect, NOTE only.
- Two objects on screen at once: see D2.
- Stale ghost frames: PASS with D2 caveat. At #mt-dynamic-positioning 390 scroll 3546 and 4137 (slots mostly out of view) I took screenshots after 1.5 s: no leftover object (A_sheet.png). Scrolled to the bottom: no object visible. After navigating #vestdavit to #news the canvas class "on" is removed and opacity is 0. After resize 1440 to 390 to 1440 the canvas is 1440x900 again, no errors.
- Render loop stops when no slot is near: PASS. Counting gl.clear calls (one per rendered frame) on #mt-dynamic-positioning at 1440: 10, 5, 19, 11, 24 and 10 frames per 1.5 s at scroll positions where a slot is on screen or within about one screen of it; 0 frames at scroll 8820 (nearest slot 3,000 px above) and 0 frames on #news. Note: draw-call counts alone are misleading, because the loop can run with zero draw calls when nothing is visible. I used frame counts to decide.
- Draw calls per 500 ms with a slot visible: 28 to 696 (software GPU, not representative).

## Check 3: fallbacks: PASS

- Reduced motion (emulated) and WebGL off (browser flags --disable-gpu --disable-webgl --disable-3d-apis, and a getContext override returning null for webgl): 5 pages each (home, #mt-dynamic-positioning, #vestdavit, #matre, #training) at 1440 and 390. In every case: html has no co-on class, canvas not shown (display none in reduced motion; opacity 0 otherwise), all slot stills loaded and visible (naturalWidth above 0, counts 6, 4, 2, 2, 1), no slot collapsed (min height above 50 px), no horizontal overflow, one h1, zero console errors, zero external requests. The hero gets class "fb", all four captions at opacity 1 and visibility visible, hero stills load at width 1600, and the hero stacks normally (text then a still panel with the caption "Illustration of a Bridge Mate DP console"). Screenshots: shots/nogl_sheet.png, shots/fb_*.png.
- Note: my first getContext override had a bug and showed errors on one run; I rewrote it (t6.mjs) and the correct override gave zero errors. The flags-based run was clean throughout.

## Check 4: offline: PASS

- All non-file, non-blob, non-data requests were aborted by a route handler and recorded. Result over all 23 routes at 1440x900: 0 requests, 0 console errors, 0 page errors. Also 0 and 0 across the 33 route changes in check 6, all scroll runs, and the fallback runs.

## Check 5: accessibility

- One h1 per page and no skipped heading level (h1 to h4) on all 23 routes: PASS.
- #companion has aria-hidden="true": PASS (read from DOM on all routes). Hero placeholder spans are aria-hidden. Each of the other slots has role="img" and an aria-label naming the object (count equals slots): PASS (see D4 wording issue).
- Clicks through the canvas: PASS. The canvas covers the whole viewport with pointer-events none. On Home at 1440, "Explore the systems" sits fully inside the canvas area; elementFromPoint returned the link, and a real click went to #products-marine-technologies. On #vestdavit at 390 the "Request a quote" button at the top clicked through to #contact.
- Keyboard Tab through Home (45 stops): first stop "Skip to content", then logo, nav, hero buttons, tour buttons, product list, DP viewer tabs (Front, Side, Controls, Screen, Exploded), then cards and news. Every stop had a visible 3 px solid outline, no stop inside the canvas or slots, none with zero size. Order matches visual order. PASS for the sequence I pressed; I did not test Shift+Tab, the open menus or the mobile menu this cycle.
- Horizontal overflow: 23 routes at 320, 390, 768 and 1440 wide (92 cases): 0 pages wider than the viewport (document and body scrollWidth). PASS.
- Contrast: computed from the CSS colours only: #F2F6FA on the three stage colours 15.3 to 18.3; muted #A9B8C9 on them 8.2 to 9.8; accent #5BA4E0 6.2 to 7.4; focus ring #8CC4F2 8.9 to 10.7. All above 4.5. I did not measure contrast of text over the rendered object. By eye the only frame where object and text coincide is D1.

## Check 6: contexts and memory: PASS

- WebGL contexts: 33 route changes (3 rounds of 11 routes including Home, DP, davit, winch, propeller, cabinet, helideck, services, training, news, products). The getContext('webgl') counter read 2 on page load and stayed at 2 after every round (one for a capability probe and one for the renderer). Not more than 2. The renderer is created once and reused.
- Memory: JS heap after a forced GC at the start and after each round: 5.6, 5.6, 5.6, 5.7 MB; DOM nodes 824 each time; event listeners 36 each time. Canvas elements in the page: 15 each round (no growth). This does not measure GPU memory, which headless software rendering cannot report meaningfully.

## Check 7: honesty

- No text in 14 pages calls the 3D or the renders a photo, photograph, CAD, real product or rendering (zero hits for those words), and no "twin" or "two operator" wording about the console (see D6). Slots are named "Illustration of ..." for the console, propeller, davit, winch, control cabinet and helideck (aria-labels). Visible labelling gap: D3.
- No lorem ipsum, no em dash or en dash in rendered text on any route, no Sinor Marine Services, FZCO or LinkedIn link text. Page titles are unique (23 of 23) in the pattern "Name | Sinor Marine Technologies" with Home titled "Sinor Marine Technologies".
- Facts I could verify against brain/verified-facts.md: entity name Sinor Marine Technologies, Singapore (stated by Rahul). The numbers on the pages I looked at (for example Vestdavit 1,800 and 1975, Matre 1953, Servogear 1,750, Scantrol 1,000) come from the old site and are not in verified-facts.md; they are partner-attributed as before, but they are not independently verified here. I did not re-check the old site this cycle.

## Full pass list

- PASS: no simulator product anywhere (24 hash routes list is 23 now, #simulator redirects to #products).
- PASS: single canvas, one renderer, 2 context calls in total over 33 route changes.
- PASS: render loop idle when far from slots and on routes without slots.
- PASS: reduced-motion and no-WebGL fallbacks (5 pages, 2 widths each, three methods).
- PASS: offline, zero external requests, zero console errors.
- PASS: one h1, ordered headings, canvas aria-hidden, slot names, click-through, keyboard order, no overflow at 320, 390, 768, 1440.
- PASS: no ghost frame after route change or scroll to the bottom; resize round trip clean.
- PASS: heap flat across 33 route changes.
- WARN: D2, D3, D4. FAIL: D1. NOTE: D5, D6, D7.

## What I could not test

Real touch devices, Safari, Firefox, screen readers, hover states on the 3D slots, performance on a real GPU, the mobile menu while the 3D is running, Shift+Tab, scroll frames at 768 and 320 with 3D on (only overflow tested there), scroll frames for six of the product pages listed above, and the last part of the Home 1440 scroll run (the screenshot run timed out near the footer, which has no 3D). Contrast over the object was judged by eye, not measured.

## Candidate lessons for the Director

1. Draw-call counts cannot prove a render loop is stopped, because a loop with nothing visible issues zero draws. Count frames (gl.clear) instead.
2. A fixed canvas above page text needs a text-versus-object check at phone width between slots, not only at slot positions; the glide state is where overlap happens.
3. When faking "no WebGL", override getContext by capturing the original function in a closure; a prototype lookup can recurse and create false console errors.
4. Under SwiftShader, one fresh page per route and scroll steps of 0.7 viewport keep screenshots from timing out.
