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
