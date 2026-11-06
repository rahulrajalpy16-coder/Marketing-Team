# QA report video 7 (focused re-check of v6 defects plus regression)

Reviewer: qa-reviewer (separate from the producer). Date 2026-11-06.
Files:
- 4x5: /tmp/work/adipec26/render7_4x5/adipec26-thanks_linkedin_4x5_v7.mp4, 11,642,963 bytes, SHA-256 0d937d955a95e2c672c6dd0f8ac1434f5d27dda228d8e568d2b35463c96799ef
- 9x16: /tmp/work/adipec26/render7_9x16/adipec26-thanks_linkedin_9x16_v7.mp4, 14,823,218 bytes, SHA-256 7dbd49f10681a53f326788cea8c2cd06573fc3014be8fafb082d0848af9d2d34

## True verification scope
- Scripted on the whole file, both: ffprobe, moov position (ffmpeg trace), blackdetect d=0.1, freezedetect -60 dB 0.5 s, volumedetect over the full audio decode.
- Overlay text rows measured from overlay_00..07.png and end_card.png (bright opaque pixels).
- Viewed frames (ffmpeg stills, reduced size): 4x5 and 9x16 each at t = 4.0, 4.5 (NAVIS, 720 px wide), 4.45 (full-resolution crop of the logo and caption area, 1080 px wide), and an 8-frame sheet at t = 0.04, 7.5, 11.5, 14.5, 18, 21.5, 24, 27 (360 px wide each); end cards at t = 28 (540 px wide, both files). 4x5 pair top crops (1080x480 scaled to 720) at t = 10.05 (pair 3 at about max zoom) and 16.45 (pair 5), plus a 16.05 frame that was still in the crossfade (pair 4 shown, not used for judgement). Total about 14 distinct stills per file.
- Motion: whole-frame mean absolute difference series (270 px wide, gray) on 2 slides per file (NAVIS 4.5 to 6.75 s, pair 3 10.1 to 12.75 s). This is a smaller test than the v6 phase-correlation series, so it is not a like-for-like comparison.
- NOT done: audio not listened to (silent track, volumedetect only); loudness_check.py not run; not played on a phone or in LinkedIn; not watched in real time; most crossfades not individually viewed; cover JPGs not opened; slides 2, 4, 6, 7 motion not re-measured in v7 (unchanged code path from v6).
- Scratch images: /tmp/claude-0/s7 (not in repo).

## 1. V6 defect re-check
V6-1 (9x16 NAVIS caption collision): FIXED. Frame at 4.45 s, full-resolution crop viewed. "fith" height is now 1500 (SAFE-120). Logo (icon plus NAVIS plus ENGINEERING) fully visible and uncropped, the lowest letters of ENGINEERING end at about y 1320 (read from the 1080 px crop: row 120 of a crop starting at 1200). SAFE is 1620, so the logo sits about 300 px above SAFE. Caption bar starts at y 1516 and the text glyphs at about y 1550 to 1584; gap between the lowest logo letter and the caption bar is about 196 px. Caption x 64 to 403, logo x about 336 to 645 at its widest. No overlap in either axis. The y values are read from a viewed crop, accurate to about 10 px; an automatic blue-pixel mask gave 1305 and was less reliable on the dark lowest letters.
V6-3 (4x5 NAVIS gap): FIXED. Frame at 4.45 s, full-resolution crop viewed. Logo icon bottom about y 1032; ENGINEERING lowest letters about y 1108 (x about 440 to 625). Caption bar at y 1096 to 1104 (x 64 to 136) and text at about y 1130 to 1164 (x 64 to 403). The icon-to-caption-text vertical gap is about 98 px. Under the ENGINEERING word the horizontal gap is about 35 px (caption text ends x 403, ENGINEERING starts about x 440), and the logo bottom is 92 px above SAFE 1200. v6 gap was about 15 px.
V6-2 (4x5 pair headroom): FIXED. Pair slides start at y 60 and the top photo is cropped from its bottom. At max zoom 1.075 the top photo edge sits at y about 14 px on screen, so no photo content is cut at the frame top. Pair 3 at 10.05 s: the right-hand man's hair top is about 40 px below the photo's top edge (v6: touching). Pair 5 at 16.45 s: the curly-haired man's hair is about 160 px below the photo top. Faces whole in both. Pair 4 top photo (men at the MT display) has large headroom, seen in the sheet at 14.5 s.

## 2. Technical spec (regression)
| Check | 4x5 | 9x16 |
|---|---|---|
| Codec, profile, pix_fmt | H.264 High, yuv420p: PASS | same: PASS |
| Dimensions | 1080x1350: PASS | 1080x1920: PASS |
| Frame rate, frames | 25/1, 745 frames: PASS | same |
| Audio | AAC LC 48 kHz stereo, decodes with no errors, mean and max -91.0 dB (silent, valid): PASS | same |
| Duration | 29.800 s: PASS | 29.800 s: PASS |
| moov before mdat | moov at offset 40, mdat at 24110: PASS | moov 40, mdat 24118: PASS |
| blackdetect | none: PASS | none: PASS |
| freezedetect | one freeze from 25.24 s to end (end card, intentional): PASS | same |
| Size | 11.6 MB | 14.8 MB |
Platform-specs: 4:5 and 9:16 MP4, H.264, AAC, under 30 fps match; organic LinkedIn limits remain UNVERIFIED in platform-specs.md, as in v6.

## 3. Text, safe margin, names, faces, dashes
Overlay text bottom edge vs SAFE (margin in brackets), measured from overlay PNGs and the end card:
| Ratio | SAFE | s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | end card |
|---|---|---|---|---|---|---|---|---|---|---|
| 4x5 | 1200 | 1160 (40) | 1164 (36) | 1173 (27) | 1164 (36) | 1174 (26) | 1164 (36) | 1164 (36) | 1174 (26) | 1149 (51) |
| 9x16 | 1620 | 1580 (40) | 1584 (36) | 1593 (27) | 1584 (36) | 1594 (26) | 1584 (36) | 1584 (36) | 1594 (26) | 1359 (261) |
No overlay text below SAFE: PASS both. The NAVIS logo (photo content, not overlay) is above SAFE in both: 4x5 by about 92 px, 9x16 by about 300 px.
- End cards viewed in both files (t = 28 s): "Sonardyne", "Fugro", "NAVIS", "Marine Technologies", "Guidance Marine" spelled exactly in both. The 9x16 end card is viewed this time (it was not in v6). Footer "Sinor Marine Services Middle East FZCO" correct. Logo card undistorted. PASS both.
- Captions read in the sheets: "Thank you.", "ADIPEC 2026 · ABU DHABI", "2-5 November 2026", "Sonardyne SPRINT-Nav on the stand", "Conversations at the stand", "Marine Technologies on the stand", "Welcome to our stand", "At the stand", "Thank you for stopping by", "NAVIS console". Correct, no claim about supply. The 4x5 caption "Marine Technologies on the stand" runs across wall images with no person under it.
- Text over faces: none in the viewed frames. Pair 3 lower photo (4x5 and 9x16): faces sit just above the caption (about 25 px above in 4x5) but are clear. Pair 5: caption over the lanyard, hand and brochure, face far above. Title: text over trousers, shoes and floor. In 9x16 the date line still touches the left man's shoe toe (cosmetic, carried as V6-4).
- Em dashes: 0 in build_video.py (grep). None seen on screen.

## 4. Motion smoothness (whole-frame difference, 270 px wide gray, consecutive frames)
| File | Slide | Frames | Mean | SD | CV | Min to max |
|---|---|---|---|---|---|---|
| 4x5 | 1 NAVIS | 58 | 0.548 | 0.077 | 0.14 (0.04 without the one zero) | 0.517 to 0.608 |
| 4x5 | 3 pair | 68 | 0.980 | 0.122 | 0.125 (0.02 without) | 0.952 to 1.037 |
| 9x16 | 1 NAVIS | 58 | 0.678 | 0.092 | 0.14 (0.03 without) | 0.656 to 0.733 |
| 9x16 | 3 pair | 68 | 0.980 to 1.002 | 0.125 | 0.12 (0.02 without) | 0.987 to 1.058 |
- Each series contains one exact-zero difference at index 0 (the first frame pair after my seek, so a seek/crossfade boundary duplicate, which inflates the raw CV). Excluding it, CV is 0.02 to 0.04 and the max/min ratio is 1.07 to 1.18, in line with the v6 whole-frame CV of 0.01 to 0.05. No pumping or judder visible in the numbers. Not a phase-correlation re-run, not watched in playback. Possible single duplicated frame at the end of the crossfade into a slide: low, not confirmed (seek artefact cannot be excluded).

## 5. Manifest
All 11 photos used in SLIDES (0f44943b, IMG_4413, IMG_4432, IMG_4464, 0bc7989f, IMG_4188, IMG_4255, IMG_4403, IMG_4156, cf677e0a, a07555b5) have status "selected" in sources/manifest.csv, and each exists once in /tmp/work/adipec26/jpg/. The grep count of "selected" is 11. No excluded or backup photo is used. PASS.

## 6. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V6-1 | Closed | 9x16 NAVIS 4.45 to 6.8 s | Fixed, see section 1 | Video producer |
| V6-2 | Closed | 4x5 pair 3, pair 5 | Fixed, see section 1 | Video producer |
| V6-3 | Closed | 4x5 NAVIS | Fixed, see section 1 | Video producer |
| V6-4 | Info, still open | 9x16 title 0 to 4 s | Date line touches the left man's shoe toe; hard teal to navy edge; large blur bands on 9x16 | Video producer (optional) |
| V6-5 | Info, still open | Photos | Third-party signage, bystander consent, screen coordinates not individually approved | Director to ask Rahul |
| V7-1 | Info | Process | Not played on a phone, audio silent and not listened to, slides 2, 4, 6, 7 not re-measured | Director, Rahul to play both once |
No new Medium or High defects found.

## 7. Verdict
- 4x5 master: spec, fast start, black and freeze, safe margin, names (viewed), logo, manifest, V6-2 and V6-3 fixes PASS (measured or viewed as stated). Technically ready; open: V6-4 (info), V6-5 approvals, publishing approval.
- 9x16 alternative: spec, margin, names (end card viewed), manifest PASS; V6-1 fixed (logo uncropped, about 196 px clear of the caption, above SAFE). Technically ready; same open items.
Both verdicts are sampled-frame and measurement based, not full playback.

## Candidate lessons for the Director
- Verify a caption-collision fix per aspect ratio with a full-resolution crop at the clip's max zoom; automatic colour masks undercount dark logo letters.
- A seek-based frame-difference series shows one zero at index 0; trim the first pair or start 0.04 s later to avoid inflating the CV.
