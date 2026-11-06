# QA report video 8 (end card with five supplied partner logos, 5.5 s end card, updated company caption)

Reviewer: qa-reviewer, separate from the producer. Date 2026-11-06.
Files:
- 4x5: /tmp/work/adipec26/render8_4x5/adipec26-thanks_linkedin_4x5_v8.mp4, 11,742,853 bytes, SHA-256 c9fb1d9ad4a1dbd78618901cf63731f36118434171c33ac08b1252955fd79919
- 9x16: /tmp/work/adipec26/render8_9x16/adipec26-thanks_linkedin_9x16_v8.mp4, 14,949,776 bytes, SHA-256 96e71051c75f1c8222261441e4e6c0b9eccfb65dfe199c2cc14236241dbafe46
- Captions: /home/user/Marketing-Team/campaigns/2026-11-adipec26-thanks/exports/caption_company_final.txt and caption_company_plain.txt

## True verification scope
- Scripted on the whole file, both videos: ffprobe, moov position (ffmpeg trace), volumedetect over full audio decode, blackdetect d=0.1 and freezedetect (-60 dB, 0.5 s) on a 270 px scaled decode.
- End card: full-resolution end_card.png of each render viewed (4x5 at 1080 px; 9x16 viewed as the 540 px video frame at t=28 plus the full PNG). Pixel measurements on the full-resolution PNGs. Each video frame at t=28 and t=30.2 compared with its end_card.png (mean abs difference 1.4 to 1.5 of 255, compression only), so the PNG is what is in the video.
- Regression: 270 px gray frames at t = 1, 5.5, 9, 12, 15, 18.5, 21.5, 24.0 and 27 s, v7 vs v8, both ratios. Not a full-clip comparison.
- NOT done: audio not listened to (silent track); loudness_check.py not run; not played on a phone or LinkedIn; not watched in real time; the end-card crossfade (24.8 to 25.25 s) was not viewed frame by frame; cover JPGs not opened; captions not checked against LinkedIn's live renderer.
- Scratch: /tmp/claude-0/-home-user/97073612-e018-519c-bbf0-502262af6c56/scratchpad (not in repo).

## 1. End card, both files
Layout (from build_video.py and pixel measure): SMS logo card, "Thank you", two lines, five white rounded tiles 470x124 (2 + 2 + 1 centred), each with a 32 px white caption directly below.

| Partner | Source file aspect | Rendered logo aspect (content bbox) | Caption text seen |
|---|---|---|---|
| Sonardyne | 5.319 (2000x376) | 5.325 (426x80) | "Sonardyne" |
| Fugro | 2.231 (1968x882) | 2.235 (219x98) | "Fugro" |
| Navis Engineering | 3.564 (1953x548) | 3.561 (349x98) | "Navis Engineering" |
| Marine Technologies (MT) | 2.159 (894x414) | 2.163 (212x98) | "Marine Technologies" |
| Guidance Marine | 7.792 (1987x255) | 7.745 (426x55) | "Guidance Marine" |
Identical numbers in 4x5 and 9x16. Differences are under 1 percent (anti-aliasing at the bbox edge), so no distortion. Colours viewed as the source palette (Sonardyne purple-blue icon and navy word, Fugro navy, Navis blue, MT blue chrome oval, Guidance black and blue); not recoloured. Not cropped: every logo sits fully inside its tile, tiles at x 60 to 530 and 550 to 1020 (20 px gap), single tile centred at x 305 to 775, row pitch 184 px with the 124 px tile plus caption, so no overlap. Logos on white tiles: no contrast problem on the navy background.

Safe margin and balance:
| File | SAFE | Lowest bright row (Guidance Marine caption) | Margin |
|---|---|---|---|
| 4x5 | 1200 | 1151 | 49 px |
| 9x16 | 1620 | 1361 | 259 px |
Top of content: 4x5 y 87, 9x16 y 297. Both blocks are centred in the area above SAFE. 4x5 looks full and balanced. In 9x16 the content spans y 297 to 1361, so about 260 px of plain gradient sits above SAFE under the content and the lower 300 px is the reserved UI zone: acceptable, not off-balance. Readability: tile captions are 32 px on a 1080 px frame (about 11 to 12 px at a 390 pt phone width), same weight as the other end-card text; readable. The Fugro tile shows a smaller, top-weighted mark because the source image carries its own padding (see V8-2).

## 2. Technical
| Check | 4x5 | 9x16 |
|---|---|---|
| Video | H.264 High, yuv420p, 1080x1350, 25/1, 758 frames: PASS | same with 1080x1920: PASS |
| Audio | AAC LC 48 kHz stereo, decodes with no errors, mean and max -91.0 dB (silent, valid): PASS | same: PASS |
| Duration | format 30.32 s, video 30.32 s, audio 30.30 s (expected 30.3): PASS | same: PASS |
| moov before mdat | moov at 40, mdat at 24502: PASS | moov 40, mdat 24518: PASS |
| blackdetect | none: PASS | none: PASS |
| freezedetect | one freeze, starts 25.24 s, runs to end (end card, intentional, about 5.1 s): PASS | same: PASS |
The freeze starts at 25.24 s, not 24.8 s: the 0.45 s crossfade into the end card runs 24.8 to 25.25 s, so the card is static from the end of the fade. Consistent with the build (END_DUR 5.5, XFADE 0.45). Platform-specs match: MP4, H.264, AAC, under 30 fps. Organic LinkedIn length and size limits remain UNVERIFIED in platform-specs.md (unchanged from v7).

## 3. Regression beats 0 to 7 vs v7
Mean absolute difference of 270 px gray frames, v7 vs v8: exactly 0.000 (max 0) at t = 1, 5.5, 9, 12, 15, 18.5, 21.5 s in both ratios. At 24.0 s the difference is 0.31 (max 9) in 4x5 and 0.23 (max 4) in 9x16, i.e. imperceptible, likely encode noise at the start of the end-card crossfade; not investigated further. At 27 s the frames differ fully, as expected (new end card). Beats 0 to 7 are unchanged at the sampled times; not every frame was compared.

## 4. Caption (final and plain)
- Em dash U+2014: 0 in both. En dash U+2013: 0 in both (python on raw bytes).
- "[[": 0. CRLF: none. Both end with one newline.
- Names, each exactly once in both files: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine. No "NAVIS" all caps in the caption.
- Bold: 29 characters in U+1D5D4 to U+1D7FF, all in the first line (index 0 to 32); NFKC of that run reads "Good conversations at ADIPEC 2026". No other bold. The only other non-ASCII character is the prayer-hands emoji in the CTA.
- Plain equals final after NFKC: True (also equal after stripping).
- Content: "ADNEC in Abu Dhabi" and the event dates match fact_check.md 1a and 1b. Partners are called "technology partners", supplied by Rahul (fact_check_guidance G4c, USER-SUPPLIED); the sentence says only "thank you for supporting us at the stand", with no dealership, authorisation or product claim. CTA is a soft comment or message ask; 6 hashtags, suitable. Paste-ready.

## 5. Logo usage
- Logos supplied by Rahul in chat, kept in assets/brand/partners/ with README stating scale only, no recolour or distortion. Verified undistorted and uncoloured (section 1).
- Framing is a thank-you to named partners, on neutral white tiles, with the full name under each. No claim of endorsement, authorisation, dealership or certification appears on the card or in the caption. The MT logo shows only "MT"; the caption "Marine Technologies" resolves it. Per fact_check.md 5a, "MT = Marine Technologies" is from the supplier's own site and Rahul's instruction, not independently confirmed for this stand (see V8-3).
- The README notes the repo is public and the logos are third-party property: Rahul has already been told to decide if they should live elsewhere. Third-party logo permission itself is not something this check can verify.

## 6. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V8-1 | Info | 9x16 end card | About 260 px plain gradient between the last caption and SAFE and blank UI zone below; centred in the safe area, acceptable | Video producer (optional) |
| V8-2 | Info | Fugro tile, both | Source image has internal padding so the mark looks smaller and top-weighted than the others; not distortion. Fix only by trimming the source file, which the producer must not do without Rahul | Director to ask Rahul (optional) |
| V8-3 | Info | End card and caption | "Marine Technologies" and "Navis Engineering" mapping and "technology partners" rely on Rahul's supplied logos and words, not independent verification | Director to note |
| V8-4 | Info | Process | Not played on a phone, audio silent and not listened to, loudness script not run | Director, Rahul to play both once |
| V6-4, V6-5 | Info, still open | From v7 | 9x16 date line touches a shoe toe; third-party signage and bystander consent not individually approved | as in v7 |
No Medium or High defects found.

## 7. Verdict
- 4x5 master: PASS (spec, fast start, black and freeze, end card logos and names, safe margin, regression at sampled times, caption). Technically ready; publishing approval and V6-5 remain with Rahul.
- 9x16 alternative: PASS on the same checks. Technically ready.
Verdicts rest on measurements and sampled frames, not full playback.

## Candidate lessons for the Director
- When a logo set is user-supplied, verify aspect ratio of rendered logos against each source file by measuring the content bounding box inside the tile, and check the tile geometry first (rounded corners fool a plain white-pixel search).
- A freezedetect start equals end of the crossfade, not the nominal card start; set the expected value as card start plus fade length.
