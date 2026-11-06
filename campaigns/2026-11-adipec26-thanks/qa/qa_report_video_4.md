# QA report video 4: adipec26-thanks_linkedin_4x5_v4.mp4 and _9x16_v4.mp4

Reviewer: qa-reviewer (separate from producer). Date 2026-11-06.
Files (SHA-256):
- 4x5: /tmp/work/adipec26/render4_4x5/adipec26-thanks_linkedin_4x5_v4.mp4, 4,892,727 bytes, 4485afb982770a06a195b25d4e64b83e1f70da46b4519facd2c76a154f92e268
- 9x16: /tmp/work/adipec26/render4_9x16/adipec26-thanks_linkedin_9x16_v4.mp4, 5,771,800 bytes, 7ce90f494d15d9082491a51ba59415a00c4d2638bdd0e5723d91b9c320e54802

## True verification scope
- Whole-file scripted: ffprobe, moov position, blackdetect (d=0.1), freezedetect (-60 dB, 0.5 s), audio decode, volumedetect, loudness_check.py (4x5 only; 9x16 audio is the identical anullsrc and volumedetect gives the same -91 dB), per-frame mean-difference over all 480 frames of each file, sub-pixel shift measurement (phase correlation) on 32 consecutive frames of slide 0 in each file.
- Viewed: 19 timestamps per file as 540 px contact sheets (t = 1, 2, 3.9, 4.225, 4.45, 5.5, 7.3, 7.625, 7.85, 9, 10.7, 11.025, 11.25, 12.5, 14.1, 14.425, 14.65, 17, 19.1); the crossfades (4.0-4.45, 7.4-7.85, 10.8-11.25, 14.2-14.65) are covered at start, middle and end (12 frames). Full-resolution views per file at t = 0.04, 3.95, 4.6, 7.3 (4x5 only), 11.0, 14.1 (6 for 4x5, 4 for 9x16: 0.04, 4.6, 11.0, 14.1). Slides 0-3 and end card were each seen at full resolution in at least one file; slide 2 (conversation) was seen at full resolution only in 4x5 and as a 540 px thumbnail in 9x16.
- NOT full real-time playback. Audio not listened to (silent by construction). Not played on a phone or in LinkedIn. Covers: size checked (1080x1350 and 1080x1920) and frame 0 compared numerically (mean diff 2.9/255, compression only); not opened visually.
- Scratch images: /tmp/claude-0/s4 (not in repo).

## 1. Technical spec (both files)
| Check | 4x5 | 9x16 |
|---|---|---|
| Codec / profile / pix_fmt | H.264 High, yuv420p | same |
| Dimensions | 1080x1350 | 1080x1920 |
| Frame rate | 25/1, 480 frames | 25/1, 480 frames |
| Audio | AAC LC 48 kHz stereo, decodes clean | same |
| Duration | 19.20 s | 19.20 s |
| moov before mdat | moov at offset 40 | moov at offset 40 |
| blackdetect | none | none |
| freezedetect | only freeze 14.64 s to end (end card, intentional, about 4.6 s). No other freezes: photos move. | same |
| Loudness | silent: -inf LUFS, true peak -inf dBTP (target-range check says CHECK, expected for silence); volumedetect -91 dB | same |
| Spec match (platform-specs LinkedIn row) | PASS | PASS |
Note: platform-specs says LinkedIn organic limits are partly UNVERIFIED (ads page only); sizes and ratios used are the verified maximums.

## 2. Motion quality (method and result)
Method: (a) mean absolute difference between consecutive frames, per slide; (b) phase correlation with parabolic sub-pixel interpolation on a 256x256 patch at the left edge and the right edge of slide 0, 32 consecutive frames (1.28 s); (c) static-region variance of overlay pixels across frames.
Results:
- Overlays are static. Logo card temporal std 0.006 (4x5) and 0.0 (9x16) grey levels; caption text pixels std 0.14 and 0.08 (4x5, 9x16) caused by the photo showing through anti-aliased edges only. Text does not jump. PASS.
- Photo movement is NOT smooth. Frame-to-frame difference alternates irregularly (4x5 slide 0: 1.6, 3.4, 2.7, 3.3, 1.6 ...; the 1.6 level is the static noise floor). Left-edge patch shift per frame is about 0.03 px on most frames and about -0.98 px every 3rd or 4th frame (identical pattern in both files). The correct smooth value would be about -0.3 px every frame. So the push-in advances in whole-pixel jumps every 0.12 to 0.16 s. The right-edge patch shows -0.7 / +0.3 / +0.9 px values, i.e. also unequal. This is the known ffmpeg zoompan integer-rounding of the crop position (the 2x pre-scale used in build_video.py is not enough to hide it). Expected visible effect: a faint stepped judder or shimmer on fine detail (stand panels, lanyard text) during the slow zoom; on a phone at 1080 px wide it may be subtle but is detectable in the data and likely on high-contrast edges. I did not play it back, so I cannot rate how visible it is to a viewer. FAIL (defect V4-1).
- Edge artifacts: no black or white edge visible at the picture edges in frames viewed (zoom is inward, 6 to 7.5 percent). The photo bottom edge on 4x5 slide 1 at the start of its zoom-out (t about 4.6) extends to y about 1105 and touches the accent bar at y 1096 to 1103 (see V4-4).

## 3. Overlay text versus safe margin (measured)
Method: rows of overlay_0N.png (and end_card.png) where pixels are opaque and bright (text, accent bar, logo; the navy gradient excluded) versus SAFE.
| Ratio | SAFE | slide 0 | slides 1-2 | slide 3 | end card |
|---|---|---|---|---|---|
| 4x5 | 1200 | 48-1160 | 1096-1164 | 1096-1174 | 80-1194 |
| 9x16 | 1620 | 130-1580 | 1516-1584 | 1516-1594 | 290-1404 |
All text is above SAFE in both files. PASS. 4x5 end card bottom text ends at y 1194, 6 px above the 1200 line (within the rule, very tight, footer line 34 px type). The navy gradient itself runs to the bottom of the frame but contains no text. The 150/300 px figures are the brief's numbers; not device-tested.

## 4. Slide-by-slide visual review
- Title (0f44943b): four men with faces clear and uncropped; "Thank you." over legs and the stand floor, not over faces; date text readable. 4x5 logo card top-left on stand wall; 9x16 logo card sits half on blur band, half on photo. Logo matches the official file (white card, undistorted, no recolor). PASS.
- Slide 1 (0bc7989f), 2 (0CDC96B1 top crop) and 3 (a07555b5): captions on the band below the photo, never over faces; readable at 48 px on 1080 px width. 
- End card: logo, "Thank you", message, partner list (Sonardyne, Fugro, NAVIS, Marine Technologies), legal name. Spelling correct. All text legible; footer line is smallest (34 px).
- Crossfades: all 4 are clean dissolves, no black or cut frames. Mid-fade shows two captions overlapping (normal, but readable-garbled for 0.45 s: "Conversations at the stand" over "Thank you for stopping by" at about 11.0 s). Cosmetic.
- No em dashes in build_video.py (grep count 0) or on screen. The middle dot in "ADIPEC 2026 · ABU DHABI" is not a dash.
- Cover images: 1080x1350 and 1080x1920, identical to frame 0 (the title slide). Good cover (faces, title, logo).

## 5. Public-exposure review (4 photos used, as seen)
Same four photos as v3, so the v3 list stands, plus:
- Slide 0: ADIPEC lanyards and name badges (text not legible), "CHINA Pavilion" banners, faint third-party booth signs (FLUIDS CHEM CO, HEBEI ALL LAND STEEL PIPE..., amphicos). In 9x16 the taller photo also shows a third-party LED sign at the top ("...NCE MARINE", partly readable). Stand panel figures 100+ projects / 40+ countries partly visible.
- Slide 1: HOLD POSITION panel reads "15+ years DP engineering", 100+ projects, 40+ countries, QR code and "sinormarin..." text; background CCS and MAYEKAWA signs; unidentified visitors in the background. The zoom-out start crop trims the panel edges slightly.
- Slide 2: Sonardyne SPRINT-Nav branding; man seen from behind; second visitor in lanyard, face visible.
- Slide 3: stand screen shows coordinates 46.760942 / -92.097473 / 238.0 and a clock 12:37:10; third-party signage "...ori Machinery Co.,Ltd."; a seated woman at far left and another at right (bystanders, not subjects). Same screen coordinates are also visible during the 11.0 s crossfade.
- No media file names, e-mail addresses, phone numbers or readable badge names found. I did not identify individuals. cf677e0a is not used. Items needing Rahul's OK: stand-panel figures (15+, 100+, 40+) and the bystanders.

## 6. 9:16 specific
- Blur bands: every photo is fit-blurred, so the bands are large: slide 1 photo 1080x810 of 1920 (42 percent), slide 2 photo 1080x623 (32 percent), slide 3 photo 1080x810 (42 percent). Title photo is 1080x1440 (75 percent) with a 240 px blur band top and bottom. The picture is not upscaled (sources 1280 to 1600 wide are reduced to 1080), so sharpness is fine, but on a phone the video is mostly blur and the subject is small. The crop of an already wide shot makes this the weaker variant; the 4x5 master is better composed. Low severity, cosmetic (V4-3).
- Title slide seam: in the title slide the navy gradient and a hard horizontal edge appear where the photo ends at y 1680 and the plain blurred band starts (visible at full resolution, teal-to-navy step). Low (V4-3).
- Caption position: captions sit at y 1516-1594 (slide 3 down to 1594), which is 326 px to 404 px above the bottom edge, and the title lines end at 1580. The 300 px clearance follows the brief's number for LinkedIn's bottom UI. I cannot verify on a device or in LinkedIn that this clears the progress bar, caption and buttons.
- 9:16 is meant to replace, not accompany, the 4x5 master.

## 7. Manifest check
Used: 0f44943b selected, 0bc7989f selected, 0CDC96B1 selected (top crop rows 14-710; flagged softer), a07555b5 selected. PASS. cf677e0a stays "held back" (not used). Manifest 0CDC96B1 reason text still says "v3 uses only the sharp top photo": stale wording, v4 does the same (V4-5, info).

## v3 fixes still intact
D5 safe zone (measured above, now also satisfied for 9x16), D9 no media file name (viewed, none), D10 no white band on the collage (slide 2 clean at the top edge in the full-res view of 4x5; no white stripe seen). D1 (partner names) and D7 (stand figures) remain open.

## Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V4-1 | Medium | Both files, all 4 photo slides | Zoompan integer rounding: photo moves in 1 px jumps every 3 to 4 frames instead of about 0.3 px every frame (measured). Likely visible as stepped judder on fine detail. Suggested fix (not applied): pre-scale to 4 to 8 times with a smoother resampler or use a sub-pixel approach (scale with eval=frame plus crop, or render the push-in by Pillow-computed per-frame crops), then re-measure shift per frame. | Video producer |
| V4-2 | Medium (open, by design) | End card and caption | NAVIS and Marine Technologies unconfirmed by Rahul. Do not publish until confirmed. | Director to ask Rahul |
| V4-3 | Low | 9x16 | Large blur bands; small photos on slides 1-3; hard teal-to-navy edge at y 1680 on title slide. | Video producer (optional) |
| V4-4 | Low | 4x5 slide 1, about 4.0 to 5.5 s | During the zoom-out start the photo bottom edge reaches about y 1105 and overlaps the caption accent bar (y 1096-1103). | Video producer (optional) |
| V4-5 | Info | sources/manifest.csv | 0CDC96B1 reason text says "v3". | Director |
| V4-6 | Info | Photos | Stand-panel figures 15+/100+/40+ and visible coordinates/bystanders need Rahul's OK (carry-over D7). | Director |
| V4-7 | Low | 4x5 end card | Footer ends at y 1194, 6 px inside the 1200 line (tight). | Video producer (optional) |

## Comparison with v3
- Better: 19.2 s with motion on every photo (no long photo freezes), thank-you message and best photo in the first frame, text-only partner card kept, safe margin enforced and now scaled for 9:16, an alternative ratio supplied. Fixes D5, D9 and D10 are intact. Overlays are perfectly static.
- Worse or new: introduces the stepped zoom judder (V4-1), which v3 did not have because it was static. 9:16 is weaker than the master.
- Net: v4 is better as a concept and equal on compliance, but I rate it not ready to publish until V4-1 is corrected or accepted by Rahul after he plays it on his phone, and until V4-2 is resolved. I cannot say it will perform better; that is a hypothesis from research, not a measurement.

## Verdict
- 4x5 master: spec PASS, fast start PASS, black/freeze PASS, safe margin PASS, motion smoothness FAIL (V4-1), partner names open (V4-2). Not ready to publish.
- 9x16 alternative: same spec and safe-margin results, same V4-1 and V4-2, plus V4-3 cosmetic. Not ready to publish; secondary to the 4x5.

## Candidate lessons for the Director
- ffmpeg zoompan rounds the crop to whole pixels; a 2x pre-scale does not remove the stepping. Measure per-frame sub-pixel shift (phase correlation) on any slow-zoom render before declaring motion smooth.
- When overlays are composited above a moving photo, measure overlay stability separately from photo motion.
