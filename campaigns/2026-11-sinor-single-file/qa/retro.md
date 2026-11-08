# Retro: Sinor Marine Technologies single-file website (2026-11-07)

## What Rahul decided
Sinor Marine Technologies is an independent Singapore company, separate from Sinor Marine Services. The old website is the truth source and everything public on it may be public again. Hosting later; contact form left unconnected for now; logo with transparent background; modern, big type, image and video led; hero with words appearing and a 3D DP console that rotates on scroll; one HTML file that opens by double-click.

## What was built (outside this public repo)
One 12.5 MB HTML file with all 24 pages, 8 clips, the 3-minute film, 30 images, embedded fonts, three.js 0.149 and a procedural 3D DP console. Packed by scripts/build_single_html.py (in the repo). Source, content, people details and media live only in /tmp/work/sinor-v2 and in the files delivered to Rahul.

## Verification (true scope)
Independent reviewer, two cycles, headless Chromium on Linux with a software GPU: cycle 1 0 FAIL 8 WARN; cycle 2 W1 to W4 and W6 closed, W5 (load stall) not fixed, W9 (slowdown after route changes) found and fixed by the Director (WebGL probe released; contexts per Home visit 2 to 1; steady frame rate about 10 per second on the test machine on every visit). Director also re-ran: 25 routes offline over file://, tap heights, heading order, hero frames, leak and frame-rate measurements.
NOT verified: real iPhone or Android, Safari, Firefox, Edge, a real GPU, screen readers, a full WCAG audit, double-click behaviour on Windows or macOS, real-user speed.

## Open for Rahul
Partner and product names, people's bios and the claims on the old site carry over as he allowed; still worth a check: written permission for Marine Technologies and partner names, consent of the named people, partner figures (1,800 davits and so on), the Nautical Institute accreditation claim, the "seven countries" engineer claim vs the team page, the hero 3D is an illustration (not product CAD), the film and clips are his simulator media.

## Sorting
A. Applied: logo asset, brand-profile, verified-facts, build script.
B. Lessons added (provisional): old site as truth source, single-file packing, colour-to-alpha logo.
C. Proposed: none new.

## Revision 2 and 3 (2026-11-07)
Producer: Director with own 3D module. Independent reviewer: web-qa-reviewer, report web_qa_report_3.md (reviewed the v2 build, before the MRU additions).
Reviewer found: D1 FAIL (phone, big console covered a heading while gliding), D2 WARN (tiny object floating between sections), D3 WARN (no visible Illustration label), D4 WARN (still fallback said "turning as you scroll"), D5 NOTE (wrong data-side on every fourth slot), D6 NOTE (old DP architecture copy mentions several operator stations next to a single-station model).
Fixed by Director and re-tested by screenshots on phone and desktop, plus the 25 route offline run (0 errors, 0 requests leaving the file): D1 (narrow mobile window, zoom capped at 1 on phone), D2 (objects hidden below 22% weight), D3 (visible Illustration chip on every slot and on the hero), D4, D5. D6 left as is: the copy is from the old site and brochure about DP2 and DP3. The v3 build (MRU page, thruster station) was NOT re-reviewed independently: it is "self-reviewed" for those additions.
Not tested by anyone: real devices, Safari, Firefox, screen readers, contrast over the rendered object.
Lesson candidates (provisional, in lessons-learned): count rendered frames, not draw calls, to prove a loop is stopped.

## Revision 5 (2026-11-08)
Independent reviewer web-qa-reviewer, report web_qa_report_4.md. Found: D1 FAIL (phone, product page console started tiny and faint), D2 WARN (Illustration label hidden behind the 3D canvas because fade-in layers sit under it), D3 WARN (phone section briefly without object), D4 WARN (115 px jump while almost invisible), meta description identical on every page. Smoothness measured by the reviewer: desktop at most 30 px and 7 degrees per step, phone about the same as the page scroll.
Fixed by Director: first slot fully shown at page top, one fixed "3D models are illustrations" chip above the canvas, wider phone blend zone, "stay put" term so weak pulls never jump, animation memory reset per page, per-page meta description from the lead text. After the fixes Director measured at most 10 px and 4 degrees per 60 px step on Home, and re-ran the 25 route offline test (0 errors). The fixes were self-reviewed, not re-reviewed independently. Open (Director decision): D6 operator station copy from the old site next to a single-station model, left as is.
Not tested by anyone: real iPhone, Safari, Firefox, screen readers, real GPU speed. Rahul's further empty-console photos are still to come.

## Revision 6 and 7 (2026-11-08): hold-where-you-stop stages
Rahul's phone test: models kept moving after he stopped and grew and shrank too much. Director removed time-based easing, made the pose a pure function of scroll, added pinned stages (210 svh desktop, 190 svh phone) and a slow fade in and out.
Independent reviewer web-qa-reviewer, report web_qa_report_5.md, on v7. PASS: zero drift in 213 of 213 hold points, pinning, fallbacks, 24 routes at two widths, datasheet downloads byte exact. Found: D1 FAIL (after a fast jump such as End key a model stayed drawn at 20 percent over the footer, because the opacity glide froze part way, so the pose was not purely scroll driven), D2 FAIL (phone: console covered the heading in two sections), D3 WARN (fade too steep), D4 WARN (two models at once on desktop), D5 WARN (illustration label over footer), D6 NOTE (Home is about 27,000 px tall with pinning), D7 NOTE (turn about 30 degrees, not 90).
Fixed by Director in v8: opacity is now computed straight from scroll (no glide), fade zone widened (measured at most 0.14 change per 40 px on phone and 0.13 on desktop), turn now measured over the pinned part (90 degrees), phone objects always centred whole in their slot (the screen close-up offset had pushed the base over the text), label hidden near the page end. Checked after the fixes: End jump leaves all models at 0.000 on Home, DP and seaonics at both sizes; 25 route offline test 0 errors, 0 external requests; phone screenshots show no covered text.
These v8 fixes were self-reviewed, not re-reviewed independently. Still open: D4 (two models faintly visible together during section changes, 21 percent of scroll positions, look only), D6 (page length, Director decision). Not tested by anyone: real finger momentum, iOS Safari, Firefox, real GPU.
