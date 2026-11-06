# QA report video 10 (team photo first, title on blurred team photo, new captions)

Reviewer: qa-reviewer, separate from the producer. Date 2026-11-06.
Files:
- 4x5: /tmp/work/adipec26/render10_4x5/adipec26-thanks_linkedin_4x5_v10.mp4, 11,914,343 bytes
- 9x16: /tmp/work/adipec26/render10_9x16/adipec26-thanks_linkedin_9x16_v10.mp4, 15,169,752 bytes
- SHA-256 not computed in this run.

## True verification scope
- Whole file, both videos, scripted: ffprobe, moov position (ffmpeg trace), volumedetect over the full audio, blackdetect (d=0.1) and freezedetect (-60 dB, 0.5 s) on a 270 px decode.
- Viewed: a 10-frame sheet per file (t = 1.4, 4.0, 6.8, 9.6, 12.6, 15.8, 19.0, 22.0, 24.8, 29 s, scaled to 360 px and 300 px wide), plus the composed beat-0 photo and overlay at full resolution (downscaled to 720 px for viewing) for both ratios. Pixel measurements on the full-resolution overlay_NN.png and end_card.png of each render.
- Regression: all 8 v8 photo_NN.png and overlay_NN.png compared pixel by pixel with v10 photo/overlay N+1, both ratios (full-resolution layers, not video frames).
- Motion: 25 consecutive frames at t = 0.4 and 12.0 s per file, frame-to-frame mean difference.
- NOT done: audio not listened to (silent track); loudness_check.py was run on the 4x5 file only and gives -inf LUFS (silent, so the LUFS target check is not applicable); not played on a phone or LinkedIn; not watched in real time; crossfades not viewed frame by frame; cover JPGs not opened; captions .txt files not re-reviewed (outside this task).

## 1. Requested changes (Rahul 2026-11-06), beats as rendered
Beat starts computed from the build (durations 2.8, 2.6, 2.8, 2.8, 3.2, 3.2, 3.2, 2.8, 2.8, end card 5.5); captions read in the frames and overlay layers.

| Beat | Start (s) | Caption seen | Photo |
|---|---|---|---|
| 0 | 0.0 | "The Sinor Marine team at ADIPEC 2026" + Sinor logo card top left | 0f44943b group of four |
| 1 | 2.8 | Title "Thank you." / "ADIPEC 2026 · ABU DHABI" / "2-5 November 2026" + logo card | blurred dark copy of 0f44943b |
| 2 | 5.4 | "NAVIS console" | IMG_4413 |
| 3 | 8.2 | "Sonardyne SPRINT-Nav on the stand" | IMG_4432 |
| 4 | 11.0 | "Technology on show at our stand" | pair IMG_4464 + 0bc7989f |
| 5 | 14.2 | "Marine Technologies on the stand" | pair IMG_4188 + IMG_4255 |
| 6 | 17.4 | "Conversations at our stand" | pair IMG_4403 + IMG_4156 |
| 7 | 20.6 | "Good to see you at the stand" | cf677e0a two men |
| 8 | 23.4 | "Guidance Marine at our stand" | a07555b5 |
| End | 26.2 | Thank-you end card with five partner tiles | end_card.png |

Total: container 31.72 s (video 31.72, audio 31.70); the build's sum is 31.7 s. Freeze starts at 26.64 s = card start 26.2 + 0.45 s crossfade, as expected.

| Rahul's change | Result |
|---|---|
| Start with full team photo | PASS: beat 0 is the group of four, full-frame in 4x5, whole photo on blurred bands in 9x16 |
| Then "thanks" | PASS: title beat 1 at 2.8 s |
| "Welcome to our stand" to "conversations at our stand" | PASS: pair 3 now "Conversations at our stand" |
| "At the stand" to a better caption | PASS: "Good to see you at the stand" (see V10-4 on wording) |
| "Thanks for stopping by" to Guidance Marine | PASS: "Guidance Marine at our stand" (see V10-3 on wording) |
Unrequested change: pair 1 was "Conversations at the stand" in v8 and is now "Technology on show at our stand" (needed to avoid duplicating "Conversations" in pair 3; wording is sensible, but not asked for, see V10-5).

## 2. Title and team beats
- Title (both ratios, overlay_01): all text bands centred within 0.5 to 5 px of x = 540 (Thank you. 535 because of glyph shape). Logo card bottom y 369 (4x5) / 579 (9x16), accent rule 410 / 620: 41 px clear gap, no overlap. Lowest title text y 756 (4x5) / 966 (9x16). Readable white on dark blurred background. PASS.
- Team beat 4x5: caption at y 1096 to 1164, over the men's legs and the floor; logo top left over the stand wall; no face under any overlay (faces about y 300 to 440 in the 1350 frame). PASS.
- Team beat 9x16: logo on the blurred band above the photo, clear of faces. Caption (y 1516 to 1584) and its accent rule cross the men's shoes (left man's trainer under the rule, right man's shoe under the text end). Faces clear. Cosmetic, same type as V6-4 (see V10-2).
- Title background is the blurred team photo, so no identifiable faces. PASS.

## 3. Technical (both files)
| Check | 4x5 | 9x16 |
|---|---|---|
| Video | H.264 High, yuv420p, 1080x1350, 25/1, 793 frames: PASS | same with 1080x1920: PASS |
| Audio | AAC LC 48 kHz stereo, decodes without errors, mean and max -91.0 dB (silent, valid): PASS | same: PASS |
| moov first | moov at offset 40, mdat at 25550: PASS | moov 40, mdat 25566: PASS |
| blackdetect | none: PASS | none: PASS |
| freezedetect | single freeze from 26.64 s to end (end card): PASS | same: PASS |
| Loudness script | -inf LUFS, true peak -inf dBTP (silent), run on 4x5 only; target check not applicable | NOT RUN |
Platform-spec limits for organic LinkedIn length and size remain UNVERIFIED in platform-specs.md (unchanged).

## 4. Safe area
Bright overlay pixels (text, logos, rules), lowest row versus SAFE:
| File | SAFE | Beats 0, 2 to 8 lowest | Title lowest | End card lowest | Margin |
|---|---|---|---|---|---|
| 4x5 | 1200 | 1164 to 1174 | 756 | 1151 | 26 to 36 px (captions), 49 px (end card) |
| 9x16 | 1620 | 1584 to 1594 | 966 | 1361 | 26 to 36 px (captions), 259 px (end card) |
All above SAFE: PASS. Right edge of the longest caption x 910, 170 px margin.

## 5. Regression versus v8
- Photo layers of v8 beats 1 to 7 equal v10 beats 2 to 8: max difference 0, mean 0.000, both ratios. Overlay layers: v8 NAVIS, SPRINT-Nav and MT pair identical (0). Overlays that differ (max 245, mean 0.8 to 1.4 on the full frame) are exactly the three beats with new captions (pair 1, pair 3, two men) and the Guidance Marine beat. The photo framing of every unchanged beat is therefore identical.
- End card: v10 end_card.png equals v8 end_card.png exactly (max difference 0) in both ratios. Tile logos measured (content bbox vs source aspect): Sonardyne 5.325 vs 5.319, Fugro 2.235 vs 2.231, Navis 3.561 vs 3.564, MT 2.163 vs 2.159, Guidance 7.745 vs 7.792; all within 0.6 percent, no distortion. Names under the tiles in full: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine. PASS on distortion and names.
- The producer's note that the logos were "trimmed of empty margins" and are "now larger" is NOT borne out. The five source PNGs in assets/brand/partners/ have an alpha bounding box equal to the whole image (and for alpha above 16), so the trim does nothing. The tiles are pixel-identical to v8 (V10-1). Fugro still shows a smaller mark than the others (V8-2, unchanged).

## 6. Motion spot check
Consecutive 25 frames at 0.4 s (beat 0) and 12.0 s (beat 4), per file: mean frame difference 0.58 to 0.66 (4x5, 0.4 s), 0.73 to 0.76 (4x5, 12 s), 0.56 to 0.62 and 0.75 to 0.79 (9x16). No zero steps, no jumps: smooth, steady push-in/drift. Two slides per file only.

## 7. Captions and claims
- "The Sinor Marine team at ADIPEC 2026": rests on Rahul's words ("full sinor marine team photo", read as the group of four; he may mean another photo). The manifest note says everyone faces the camera, not who they are. A careful reader could object that "team" is unconfirmed for all four people. The man in the white shirt and the man in the grey suit also appear alone in beat 7 ("Good to see you at the stand"), so the video says the same two people are the team and are being greeted, which reads slightly oddly (V10-4). Director should confirm with Rahul that all four are Sinor staff.
- "Guidance Marine at our stand": Rahul said the woman represents Guidance Marine. The man beside her is NOT identified anywhere. The caption can be read as both people being Guidance Marine, which claims more than stated (V10-3). A narrower wording such as "Guidance Marine representative at our stand" would match Rahul's statement; Director decides. USER-SUPPLIED in verified-facts.md, not independently verified.
- "Technology on show at our stand", "Marine Technologies on the stand", "NAVIS console", "Sonardyne SPRINT-Nav on the stand": describe visible items, no supply, dealership or product claim. "NAVIS console" matches the branded console seen (the end card spells Navis Engineering in full).
- Em dash U+2014: 0 in build_video.py, caption_company_final.txt, caption_company_plain.txt, caption_linkedin_final.txt. Not scanned inside the MP4 frames beyond reading them.

## 8. Manifest
All 11 photos used (0f44943b, IMG_4413, IMG_4432, IMG_4464, 0bc7989f, IMG_4188, IMG_4255, IMG_4403, IMG_4156, cf677e0a, a07555b5) are `selected` in sources/manifest.csv (read through the full listing of the file; the one sheet column check for HEIC rows was cut by commas, so selection for IMG_4413 and IMG_4255 was read from the earlier full text). Near-duplicates 72c998bc and 0c488f3f are not used.

## 9. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V10-1 | Low | End card, both | Brief says logos were trimmed and are now larger; end card is identical to v8 (trim no-op, source PNGs have no empty margin). Statement to Rahul must not claim a larger logo. Fugro mark still looks smaller (V8-2). If wanted, trim by pixel content, with Rahul's say-so. | Director (wording), video producer (optional) |
| V10-2 | Low | 9x16 beat 0, 0 to 2.8 s | Caption and accent rule cross the men's shoes; faces clear | Video producer (optional) |
| V10-3 | Low | Beat 8, 23.4 s | "Guidance Marine at our stand" may be read as covering both people; the man is unidentified | Copywriter, Director |
| V10-4 | Low | Beats 0 and 7 | "team" unconfirmed for all four people; two of them reappear in "Good to see you at the stand" | Director to confirm with Rahul |
| V10-5 | Info | Beat 4, 11.0 s | Unrequested caption change (from "Conversations at the stand"), reasonable to avoid duplicate; tell Rahul | Director |
| V8-4 and earlier open info items | Info | Process | Not played on a phone, audio silent and unheard, V6-5 consent items still with Rahul | Director |
No Medium or High defects found.

## 10. Verdict
- 4x5 master: PASS on spec, fast start, black/freeze, safe area, requested changes, regression, motion sample. Four Low wording/claim points above for the Director.
- 9x16 alternative: PASS on the same checks; plus cosmetic V10-2.
Verdicts rest on measurements and sampled frames, not full playback.

## Candidate lessons for the Director
- When a brief says an asset was trimmed or enlarged, compare the rendered output with the previous version pixel by pixel before repeating the claim; a trim based on alpha bbox does nothing if the source has no transparent margin.
- A caption that names a company beside a photo of two people should say who is meant ("representative") when only one is identified.
- Before reusing the same photo twice in a row (team photo then blurred title), confirm the viewer is not expected to read the repeat as a duplicate; here the blur and overlay make it distinct.
