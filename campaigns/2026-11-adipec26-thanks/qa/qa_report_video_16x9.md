# QA report: three 16:9 template recreations (v14): clean, dynamic, promo

Reviewer: qa-reviewer, separate from the producer. Date 2026-11-07. Files (all under /tmp/work/adipec26):
- clean: r16_clean/adipec26-thanks_linkedin_clean_16x9_v14.mp4, 14,831,670 bytes, SHA-256 9780e37a02963626...
- dynamic: r16_dynamic/adipec26-thanks_linkedin_dynamic_16x9_v14.mp4, 6,690,732 bytes, SHA-256 492e6b67c5ae1ded...
- promo: r16_promo/adipec26-thanks_linkedin_promo_16x9_v14.mp4, 19,896,373 bytes, SHA-256 0c1382e80552b324...
(First 16 hex digits only.)

## True verification scope
- Whole file, scripted: ffprobe, moov position (ffmpeg trace), volumedetect, blackdetect (d=0.1) and freezedetect (-60 dB, 0.5 s) on a 320 px decode, loudness_check.py (clean only; all three tracks measure -91.0 dB, silent).
- Frames viewed at FULL 1920x1080 resolution, one frame per image, per file: t = 0, 3.6, 6.3, 9.25, 12.2, 15.15, 18.1, 21.05, 24.0, 27.0 s (first frame, title beat, 8 hero beats incl. one at 1.2 s into each, end card). I viewed 10 frames per file (t=1.2 s was extracted for clean and dynamic but only t=0 and the beat frames were examined; promo 1.2 s viewed). Not every frame between samples was viewed.
- Transitions: 8-frame contact strips (every 2nd frame, 480 px) viewed for clean whip (7.80 s), dynamic nested frames (7.78 s), promo blurred slide (7.80 s) and promo photo-wall grid (4.84 s); dynamic letter build strip (11.28 s). The other boundaries share one code path per style and were not individually viewed.
- Motion: frame-difference series on 480x270 grayscale decodes, 0.9 to 1.5 s windows (25 fps), on at least 2 beats per file plus transitions (numbers in section 5). Phase correlation was run but returned zero shift for the clean and promo windows (dominated by static regions), so it is not usable evidence of tile drift or wall speed; the wall speed (2 px per frame) is taken from the script and the diff series.
- Logo aspect: pixel measurement on the promo end card against the alpha bounding box of each source logo.
- NOT done: audio not listened to (silent track); not played on a phone or in LinkedIn; no real-time playback; no cover images reviewed; contrast not computed by script this round (judged by eye on full frames); fidelity judgement is mine from the reference contact sheets (ref_sheet_a, det_r1, sheet_a, sheet_b), not measured. det_r2a, det_r2b and det_r3 were not opened. Scratch frames of the transition and letter strips are in qa/scratch16/.

## 1. Technical (all three identical in spec)
| Check | clean | dynamic | promo |
|---|---|---|---|
| Video | H.264 High, yuv420p, 1920x1080, 25/1, 794 frames | same | same |
| Audio | AAC LC 48 kHz stereo, mean/max -91.0 dB (silent, valid) | same | same |
| Duration | 31.76 s (script 31.75, rounding to 794 frames) | 31.76 | 31.76 |
| moov first | offset 40 | offset 40 | offset 40 |
| blackdetect | none | none | none |
| freezedetect | end-card segments 26.6 s to 31.4 s (static card with very slow tile drift, intended) | one from 26.0 s to end (end card) | one from 26.04 s to end (end card) |
| loudness_check.py | -inf LUFS, true peak PASS, "within 1.5 LU of -14" CHECK (not applicable to silence) | not run (volumedetect only) | not run (volumedetect only) |
PASS for all three on spec. Frame rate 25 and duration are within the LinkedIn spec as recorded in brain/platform-specs.md (spec row only partly verified, as noted in the earlier QA).

## 2. First frame and thank-you within 5 s
- clean: frame 0 shows the team photo in keyline with caption, tiles, "26" token. "Thank you." title card from 2.4 s. PASS.
- dynamic: frame 0 shows full-bleed team photo with "OUR TEAM" and caption. "THANK YOU." window-letters title from 2.4 s, fully formed at 3.6 s. PASS.
- promo: frame 0 shows framed team photo, TEAM chip, caption, info box on the wall. "THANK YOU" title from 2.4 s, fully in at 3.6 s. PASS.

## 3. Beats in order with captions as rendered (viewed at full resolution, all three)
1 "The Sinor Marine team at ADIPEC 2026" (s8_2) | 2 "Thank you." / THANK YOU. title | 3 "Conversations at our stand" | 4 "Visitors at our stand" | 5 "NAVIS console" | 6 "Sonardyne SPRINT-Nav on the stand" | 7 "Marine Technologies on the stand" | 8 "With Guidance Marine at our stand" | 9 "Together at our stand" | 10 end card. Order and text correct in all three, no typos.
- clean beat 5: caption is CUT, see CL-1.
- Decorative words: dynamic OUR TEAM, CONVERSATIONS, VISITORS, TECHNOLOGY, DISCUSSIONS, PARTNERS, WELCOME, TOGETHER. Promo chips: TEAM, VISITORS, VISITORS, TECHNOLOGY, TECHNOLOGY, PARTNERS, PARTNERS, STAND.
- PASS for order and text in dynamic and promo. clean: PASS for order, FAIL on beat 5 caption legibility (CL-1).

## 4. Text safety (SAFE line = 1010 px, bottom margin 70)
- clean: captions sit inside the hero image; lowest hero edge 835 px, end card label about 750 px, "Guidance Marine" label bottom about 760. All inside. Title "Thank you." sits 14 px from the panel edge on the left and 22 px on the right (tight, not cut). Beat 5 caption overflows its photo (CL-1).
- dynamic: caption bottom about 985 px (margin about 95). Giant words are intentional bleeds; placement over faces: see DY-1. End card: nothing below 790 px, no overlap of heading and logo tiles (heading right edge 915, tiles start 1020).
- promo: info box bottom 858 to 922 px, end card label about 780. Text block right edge about 1820 (100 px margin). Caption, chip and info box sit on the dimmed wall, so text overlaps small faces in wall tiles; contrast stays high (white on dark navy, judged by eye). Not cut anywhere.
- Text over faces: clean none (captions inside the photo's lower gradient, and the hero frame overlays only the photo's lower area; in beat 8 the caption crosses the lanyards and clothing of the two people, not faces). promo none in the heroes (the Sonardyne full-bleed title crosses the SPRINT-Nav label and a shoulder, not faces). dynamic yes, partly: DY-1.
- Phone-size readability: all captions at 46 px or more in a 1920 frame, titles far larger; promo info box 30 px (small but legible). Judged by eye on 1920 frames, not on a phone.
- End-card overlap: none in any of the three.

## 5. Motion and transitions (diff on 480x270 gray, mean / std / CV, per consecutive frame)
| File | Window | mean | std | CV | Note |
|---|---|---|---|---|---|
| clean | 6.0-7.5 s (beat 3, tile drift and hero zoom) | 0.380 | 0.025 | 0.07 | smooth |
| clean | 17.5-19.0 s (beat 7) | 0.273 | 0.049 | 0.18 | one zero step is the first diff of the window (seek duplicate, rest of series 0.24-0.33): not a file defect |
| clean | 3.0-4.5 s (title) | 0.198 | 0.021 | 0.11 | smooth |
| clean | whip 7.6-8.5 s | 19.7 | 14.4 | 0.73 | continuous 8 to 41, no popping; about 0.1 to 0.15 s of empty grey backdrop mid-whip (the reference has the same empty frame) |
| dynamic | 6.0-7.5 s (card beat) | 0.422 | 0.010 | 0.02 | smooth |
| dynamic | 17.6-19.1 s (full-bleed beat) | 0.317 | 0.003 | 0.01 | smooth |
| dynamic | letters 11.3-12.3 s | 0.442 | 0.595 | 1.35 | letters build in ~0.6 s then settle to 0.09-0.10 per frame (practically still for the remaining ~1.7 s) |
| dynamic | nested frames 7.7-8.6 s | 22.8 | 29.3 | 1.29 | colour frames close, one near-static frame at the cover peak (0.61), then open; no flicker seen in strip |
| promo | 6.0-7.5 s (wall scroll, speaker beat) | 2.067 | 0.021 | 0.01 | very even |
| promo | 17.5-19.0 s | 2.091 | 0.344 | 0.16 | first-step seek zero, rest 2.0-2.2 |
| promo | 3.0-4.5 s (title) | 2.343 | 0.120 | 0.05 | smooth |
| promo | slide 7.7-8.6 s | 16.1 | 12.0 | 0.75 | blurred slide, continuous |
| promo | slide 13.6-14.5 s | 16.0 | 11.8 | 0.73 | continuous |
- Transitions as intended: clean = perspective whip (viewed), dynamic = nested colour frames collapsing and opening (viewed), promo = blurred slide on odd boundaries and photo-wall grid on even boundaries (both viewed). No black frame. Nothing unreadable for more than about 0.6 s except during transitions (0.52 s).
- Ghosting: in the clean whip and promo slide, captions are blurred during the 0.5 s move (by design). No bug-like ghost seen.
PASS on motion for all three.

## 6. End card (logos and names)
Measured on the promo end card (dynamic and clean use the same tile function; visually the same tiles):
| Logo | source aspect | rendered aspect |
|---|---|---|
| Sonardyne | 5.319 | 5.313 |
| Fugro | 2.231 | 2.234 |
| Navis Engineering | 3.564 | 3.564 |
| Marine Technologies (MT oval) | 2.159 | 2.160 |
| Guidance Marine | 7.792 | 7.739 |
Undistorted. Name labels read exactly: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine. Sinor logo not measured (visually undistorted). Fugro and Guidance Marine logos are the thinnest-looking tiles; the Guidance Marine logo is small (46 px tall) but readable. Text: "Thank you / To every client and visitor who stopped by our stand. / And to our technology partners for their support:" reads correctly in all three. PASS.

## 7. Template fidelity (my judgement from the reference sheets)
**clean, vs reference 1.** Reproduced: ghost greyscale photo background; white-keyline hero with caption inside; blue duotone tiles that are crops of the same photo; black squares; big white tokens ("26", "AD" standing in for the template's "C0/H1"); dashed lines and plus marks; perspective camera whip with empty grey frame. Weaker or missing: true 3D depth (tiles are flat 2D sliding layers, not layered at different Z with camera push); the hero in the reference is a thin, wide photo with small text, here larger; the reference's light-leak/lens flare glints and text-block lines are only token hints (four small white lines); the tile count and overlap density is lower on some beats (NAVIS). A viewer of the reference would recognise the style. Closest of the three.
**promo, vs reference 3.** Reproduced: dark duotone photo-wall grid, left or right text block with aqua chip, outlined info box, speaker-style framed photo, a full-bleed tinted photo with left-aligned title (beat 6), blurred slide and wall-grid transition, THANK / YOU aqua block title. Missing or weaker: the purple/violet half of the palette (ours is navy only), aerial city footage and real video (stills only), a name/date lower third styled as in the speaker slides (the info box is generic), big blurred type slides (only the title), the template's logo bug. Recognisable as the same family but flatter and one-colour.
**dynamic, vs reference 2.** Reproduced: giant word with letter-by-letter build and outlined first letter state; nested colour frames wipe; text-as-window reveal on cream ("THANK YOU." with the team photo showing through); framed tilted card with word across it; cream/blue panels. Missing or weaker: the reference's saturated multi-colour palette (magenta, teal, yellow, orange) is replaced by navy, blue, sky and cream; the window reveal shows only torsos and lanyards (no faces, so it reads as dark texture); full-bleed beats only partly match (the reference's letters shift and mask a person); cards are near-still after the letters finish (frame diff about 0.10). Recognisable by the giant word and nested frames, but the colourful character is missing.
Ranking by fidelity: 1 clean, 2 promo, 3 dynamic.

## 8. Over-claims versus Rahul's statements
- Partners wording "supported us / for their support": matches the approved rule. "Marine Technologies on the stand" and "Sonardyne SPRINT-Nav on the stand" state presence only. "NAVIS console": the console carries "NAVIS Engineering" branding; the caption uses the short name (the lessons say write the full name; see CL-1 for the cut). Rahul's own "NAVIS console" wording in the beat list is retained.
- "With Guidance Marine at our stand": supported by Rahul (woman represents Guidance Marine).
- Dynamic decorative words: PARTNERS over Marine Technologies and WELCOME over the Guidance beat are consistent with the confirmed partners. DISCUSSIONS over the Sonardyne beat implies discussions (photo shows a conversation). TECHNOLOGY over the NAVIS console is fine. Promo chip "VISITORS" over "Conversations" is fine. No metrics or capability claims are made.
- Dates/location: "ADIPEC 2026 / ABU DHABI / 2-5 November 2026" matches verified-facts.
PASS, no unsupported claims found.

## 9. Content a careful company might object to (for Rahul to decide, not blockers)
- Visitor faces: ADNOC-coverall visitors and UAE visitors are clearly recognisable in the hero photos and, as blue duotone, in clean's tiles; promo's wall holds dozens of small duotone faces of people at the stand (team, visitors, partner staff). Photos are Rahul-selected in the manifest; no separate consent is recorded.
- Other brands readable: Shipworkz (neighbouring stand) in the team photo and the Together photo, in all three videos; "ONE-MICROF / HP-LUB II / ENGINEERING SOLUTIONS" and an adjacent stand's panels in the Visitors photo; "Nagamori Machinery Co.,Ltd." in the Marine Technologies and Guidance photos; "i4it" and "Sonardyne" screens in the team photo. Clean's duotone tiles and the grey ghost carry the same shapes. Duotone reduces but does not remove readability (Shipworkz, SPRINT-Nav and "HOLD POSITION" panels are legible in the promo wall).
- Lanyard badges: names are small and mostly illegible; in the dynamic TOGETHER full-bleed frame the third man's badge text is partly legible ("SINOR MARINE SERVICES MIDDLE EAST FZCO" and a name line).
- Manifest: all eight hero photos used are "selected" (s8_2, s7_1, s3_1, IMG_4413, IMG_4464, IMG_4188, a07555b5, s2_2). Background tiles and wall use extra photos, including ones marked "tile only", which is their approved role. PASS.
- Em dashes: none in the script's on-screen strings (grep for U+2014 and U+2013 returned 0); none seen in the frames. PASS.

## Defects
| ID | Severity | File and location | Defect | Responsible |
|---|---|---|---|---|
| CL-1 | Major | clean, beat 5 (11.0-13.95 s) | "NAVIS console" caption is cut at the right edge of the portrait hero (reads "NAVIS consol"), and the caption sits on top of the NAVIS Engineering logo on the console. Cause: caption is 46 px type on a hero only about 352 px wide. | video producer (build script: scale or wrap the caption, or place it outside the photo for portrait heroes) |
| DY-1 | Major | dynamic, WELCOME beat (19.85-22.8 s, viewed at 21.05 s) | Giant word covers the top of the heads of the Guidance Marine woman and the Sinor colleague. Minor on VISITORS beat (about 8.05-11.0 s): letters cross the chin or face of at least two visitors. | video producer (move the word to the card's lower third, or lower its opacity over heads) |
| DY-2 | Minor | dynamic, title and beats 1-3 | Full-bleed s7_1 and s2_2 are 1206-px-wide source crops upscaled about 1.7x: visibly soft. | video producer (offer a card layout for those) |
| DY-3 | Minor | dynamic, TECHNOLOGY beat | White letters "L" over the card's white border lose their edge (letters still legible). Card beats are near-still after the letters finish. | video producer |
| DY-4 | Minor | dynamic, THANK YOU title | Window letters show only torsos and lanyards: reads as dark texture, weaker reveal than the reference. | video producer |
| FD-1 | Minor | clean | 3D depth and light-leak details of the reference are not reproduced. | video producer (disclose to Rahul) |
| FD-2 | Minor | promo | Purple palette half, aerial footage and speaker lower third of reference not reproduced. | video producer (disclose to Rahul) |
| FD-3 | Minor | dynamic | Reference's saturated multi-colour palette not reproduced. | video producer (disclose to Rahul) |
| PR-1 | Minor | promo, beats 8 and 9 (caption blocks) | Orphan word "stand" on the third line in "Sonardyne SPRINT-Nav on the / stand" and "With Guidance Marine at our / stand". | video producer |
| CL-2 | Minor | clean title card | "Thank you." sits 14 and 22 px from the panel edge (tight). | video producer |
| ALL-1 | Note | all three | Neighbouring-stand brands, visitor faces and partly legible badges are visible (section 9). Decision for Rahul. | Director to ask Rahul |
| ALL-2 | Note | all three | Silent audio track by design (-91 dB). Loudness check is not meaningful. | none |

## Verdicts
- clean v14: FAIL until CL-1 is fixed (otherwise technically PASS). Best fidelity.
- dynamic v14: FAIL until DY-1 is fixed (heads covered by the giant word). Weakest fidelity.
- promo v14: PASS (minor PR-1 only; disclose FD-2 and ALL-1).
Everything else passes the checks above within the stated sampling.

## Candidate lessons for the Director
1. Portrait heroes need caption sizing based on the actual photo width; test every beat with the narrowest hero.
2. Full-bleed giant words need a face-avoidance check (words over heads) per photo; place them at the lower third or use card layouts for photos with heads in the lower half.
3. When recreating paid templates, state fidelity gaps (palette, depth, footage) to Rahul instead of claiming "same template".
