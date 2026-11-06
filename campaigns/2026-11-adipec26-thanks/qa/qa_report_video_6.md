# QA report video 6 (company page, ADIPEC 2026 thank-you; 8 beats, 3 pairs, 5 partners)

Reviewer: qa-reviewer (separate from the producer). Date 2026-11-06.
Files (SHA-256):
- 4x5: /tmp/work/adipec26/render6_4x5/adipec26-thanks_linkedin_4x5_v6.mp4, 11,711,618 bytes, c3f663520a9d14dab9c8188773ba558a76371a84925f98697bb414692d39e71d
- 9x16: /tmp/work/adipec26/render6_9x16/adipec26-thanks_linkedin_9x16_v6.mp4, 15,040,794 bytes, 8ac63a6ddb2a73bb0a377ed7d7c85b4720682b984ddeaf0570f3ee2fab85ca7e

## True verification scope
- Whole-file scripted, both files: ffprobe, moov position, blackdetect (d=0.1), freezedetect (-60 dB, 0.5 s), full audio decode with volumedetect, phase-correlation shift series (256x256 patches, left and right edge, y 200, Hann window, parabolic sub-pixel peak) on every frame pair inside all 8 photo slides (steady part, crossfades excluded), plus a whole-frame difference series (270 px wide) for all 745 frames.
- Viewed: 10 frames per file at t = 0.04, 3.5, 5.6, 8.5, 11, 14.4, 17.6, 20.5, 23.5, 27 s (540 px wide per frame, so fine text only judged at that size); full-resolution crops of the NAVIS slide (4x5 video frame at 4.5 s; 9x16 from photo_01 plus overlay_01); the three 4x5 pair photo layers (photo_03 to 05, unzoomed, at 720 px). Overlay text rows measured from overlay_0N.png and end_card.png. Logo compared pixel by pixel with assets/brand/sinor-logo.png.
- NOT done: audio not listened to (silent by construction); loudness_check.py not run (volumedetect -91.0 dB mean and max, silent track); not played on a phone or inside LinkedIn; motion judged from measurements and stills, not by watching; crossfade frames not individually viewed (no black or freeze reported by detectors); end-card pixel check of the 9x16 text beyond the margin numbers was by overlay measurement plus the 4x5 view, the 9x16 end card was not viewed. Cover JPGs checked for size and a numeric match with frame 0 (4x5 mean abs diff 2.7/255), not opened.
- Scratch images: /tmp/claude-0/s6 (not in repo).

## 1. Technical spec
| Check | 4x5 | 9x16 |
|---|---|---|
| Codec, profile, pix_fmt | H.264 High, yuv420p: PASS | same: PASS |
| Dimensions | 1080x1350: PASS | 1080x1920: PASS |
| Frame rate, frames | 25/1, 745 frames: PASS (below 30 fps) | same |
| Audio | AAC LC 48 kHz stereo, decodes with no errors, mean and max -91.0 dB (silent): PASS | same |
| Duration | 29.800 s = 4.0+2.8+2.8+3.2+3.2+3.2+2.8+2.8 (24.8) + 5.0 end card: PASS | same |
| moov before mdat | moov at offset 40, mdat at 24110: PASS | moov 40, mdat 24118: PASS |
| blackdetect | none: PASS | none: PASS |
| freezedetect | one freeze from 25.24 s to end (the end card, intentional): PASS | same |
| Size | 11.7 MB (limits for ads 75 KB to 500 MB): PASS | 15.0 MB: PASS |
| Platform-specs match | PASS (4:5 and 9:16, MP4, H.264, AAC, under 30 fps). Organic LinkedIn limits remain UNVERIFIED in platform-specs.md. | PASS (same note) |
File names follow <campaign>_<platform>_<aspect>_v<n>.mp4.

## 2. Motion smoothness (re-measured, sub-pixel phase correlation, px per frame, steady part of each slide)
4x5 (L = left patch, R = right patch; whole-frame diff CV in last column):
| Slide | L mean, sd, CV | R mean, sd, CV | frame diff CV |
|---|---|---|---|
| 0 title (n=97) | +0.114, 0.010, 0.08 | -0.101, 0.012, 0.12 | 0.05 |
| 1 NAVIS (58) | -0.218, 0.064, 0.29 | +0.222, 0.026, 0.11 | 0.04 |
| 2 Sonardyne (58) | +0.193, 0.075, 0.39 | -0.159, 0.065, 0.41 | 0.03 |
| 3 pair (68) | -0.198, 0.042, 0.21 | +0.213, 0.024, 0.11 | 0.03 |
| 4 pair (68) | +0.217, 0.028, 0.13 | -0.232, 0.024, 0.10 | 0.02 |
| 5 pair (68) | -0.176, 0.020, 0.11 | +0.233, 0.018, 0.08 | 0.03 |
| 6 At the stand (58) | +0.256, 0.029, 0.11 | -0.231, 0.019, 0.08 | 0.03 |
| 7 Thank you stopping by (58) | -0.188, 0.048, 0.26 | +0.240, 0.042, 0.18 | 0.02 |
9x16: L/R patch CV 0.10 to 0.47 on slides 1 to 6 (sd 0.02 to 0.13 px), slide 0 L +0.023 sd 0.005, slide 7 CV 1.3 to 1.4 (sd 0.14 to 0.17 px, mean 0.11 to 0.13). Whole-frame diff CV 0.01 to 0.04 on all 8 slides, max/min per-frame diff ratio 1.07 to 1.25.
- Reading: whole-frame frame-to-frame difference is nearly constant (CV 0.01 to 0.05) on every slide in both files, and the edge shift sd is 0.01 to 0.13 px, versus the v4 judder of sd about 0.45 px. Higher patch CVs sit on low-texture patches (blurred bands, white wall, the 9x16 slide 7 blur band, where a patch of pure blur gives a noisy estimate near the detection limit); I cannot prove that, but the whole-frame series does not show any pumping. Pair slides (3, 4, 5) are rendered as one composite layer, so both photos and the 10 px seam move together: seam stays a clean horizontal line in all viewed frames and the pair layers; no seam shimmer, no edge artifact or black border seen in viewed frames. PASS (measured) for both files, same method as v5; v6 numbers are equivalent to v5 (v5 L CV 0.10 to 0.23).
- Limit: not watched in playback.

## 3. Text, safe margin, partner names, logo, dashes
Overlay text rows (bright opaque pixels), bottom edge vs SAFE:
| Ratio | SAFE | s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | end card |
|---|---|---|---|---|---|---|---|---|---|---|
| 4x5 | 1200 | 1160 (40) | 1164 (36) | 1173 (27) | 1164 (36) | 1174 (26) | 1164 (36) | 1164 (36) | 1174 (26) | 1149 (51) |
| 9x16 | 1620 | 1580 (40) | 1584 (36) | 1593 (27) | 1584 (36) | 1594 (26) | 1584 (36) | 1584 (36) | 1594 (26) | 1359 (261) |
(margin in brackets) No overlay text below SAFE: PASS both. The gradient reaches the bottom but has no text.
- Partner names on the end card (4x5 frame viewed; 9x16 uses the same build, text not viewed): "Sonardyne", "Fugro", "NAVIS", "Marine Technologies", "Guidance Marine": spelled exactly. PASS (4x5 viewed; 9x16 by shared code PARTNERS list, not viewed).
- Captions read: "Thank you.", "ADIPEC 2026 · ABU DHABI", "2-5 November 2026", "NAVIS console", "Sonardyne SPRINT-Nav on the stand", "Conversations at the stand", "Marine Technologies on the stand", "Welcome to our stand", "At the stand", "Thank you for stopping by". All correct and readable at 540 px in the stills. Wording is neutral: no claim about what partners supplied (consistent with verified-facts line 22).
- Logo: end card logo region vs assets/brand/sinor-logo.png (same resize): mean abs diff 0.0 in both ratios, exact. Title-slide logo card viewed, undistorted. PASS.
- Em dashes: 0 in build_video.py; none seen on screen (the middle dot is not a dash). PASS.
- Text over faces, 4x5 (caption sits over the lower photo of each pair at y 1096 to 1174): pair 3 ("Conversations") caption over the man's jacket and the touch screen, faces at about y 950 to 1015: clear. Pair 4 (Marine Technologies) caption over wall images; two small bystander heads at the very bottom of the photo are below the text. Pair 5 (Welcome) caption over the man's lanyard, hand and brochure; his face is far above. No face under text on any slide in 4x5 or 9x16 in the frames viewed. Title slide: "Thank you." and date line sit over trousers and shoes in both ratios; in 9x16 the date line touches the left man's shoe toe (cosmetic, same as v5).

## 4. NAVIS slide
- 4x5 ("fith"): photo at full frame height with side bands. Logo (icon plus NAVIS plus ENGINEERING) fully visible and uncropped, checked at the highest zoom (4.5 s, full resolution). Logo bottom about y 1200 (equal to SAFE). Caption "NAVIS console" (x 64 to 403, y 1130 to 1164) ends about 15 px under the logo icon (icon bottom about y 1115, x from 360): clear but tight. PASS, with a tight-gap note.
- 9x16: photo fitted full width (no fith needed, photo fills the frame). Logo uncropped, but the caption OVERLAPS the logo: "console" runs over the lower part of the NAVIS icon and the start of "ENGINEERING" (caption x 64 to 403, y 1560 to 1590; logo spans y about 1395 to 1660, x about 300 to 670). FAIL. Also the lowest letters of "ENGINEERING" reach y about 1660, about 40 px below SAFE 1620. Defect V6-1.

## 5. Cropping of heads and key subjects
- 4x5 title (cover crop_top default): all four faces whole; heads clear of the logo card. PASS. 9x16 title: faces whole, photo shown in fit mode with blur bands; PASS.
- NAVIS: whole product, 4x5 and 9x16, screen intact. PASS (aside from V6-1).
- Sonardyne SPRINT-Nav: unit and label whole in both; PASS.
- Pair 3 top (IMG_4464): the right-hand man's hair touches the top edge in the unzoomed 4x5 layer and loses a further strip to the push-in (zoom to 7.5 percent crops about 17 px at the top of the stack). Head tight but face whole. 9x16 shows his hair with margin. Low, V6-2 (4x5 only).
- Pair 5 top (IMG_4403): curly-haired man at far right has hair close to the top edge in 4x5; same push-in effect; faces whole. Part of V6-2.
- Pair 5 bottom (IMG_4156): woman in the foreground has her back to camera, no face cut. Pair 4: both men whole. Sinor/Marine Tech panel photo bottom edge crops a few bystander heads (small, background).
- cf677e0a "At the stand" (crop_top 0.78): both men whole, feet visible; PASS. a07555b5: whole, fit mode.
- Left side of the stand/title photo is cut by the 1080 px crop (panel text cut) which is a stand panel, not a person.

## 6. Manifest check
Used in build_video.py SLIDES (11): 0f44943b, IMG_4413, IMG_4432, IMG_4464, 0bc7989f, IMG_4188, IMG_4255, IMG_4403, IMG_4156, cf677e0a, a07555b5. All 11 are "selected" in manifest.csv; the manifest lists exactly those 11 as selected. No mismatch: PASS. All 11 JPGs exist in /tmp/work/adipec26/jpg/. No backup, excluded or held-back photo is used (0CDC96B1 still has a CROPS entry in the script but is not in SLIDES).

## 7. Content a careful company might object to (listed, not edited)
Already approved by Rahul 2026-11-06: media file name readable on the stand TV in cf677e0a ("...BigCaptions 4K.mp4"); stand panel figures 15+, 100+, 40+; HEIC photos.
Not covered by an explicit approval I can see (Director to confirm with Rahul; carry-over from v5):
- Title photo and 9x16 title: third-party signage ("...NCE MARINE" LED sign, 9x16), "CHINA Pavilion" signs, other exhibitors' booths ("Machinery Co., Ltd", "Engineering Solutions").
- Bystanders and visitors identifiable in pairs 3 and 5 (visitor with lanyard badge; woman with brochure; people at the pair 3 stand; ADIPEC lanyards), none named in captions. Consent of the visitors is not documented.
- On-screen vessel position coordinates visible on the Sinor panel screen (title photo, a07555b5) and a DP HMI on the NAVIS display; no client data seen.
- Badges: lanyard name badges are present but not legible at video size.
- Pair 4: small part of a competitor-looking panel ("MAYERSK"/"CCS" signage in the HOLD POSITION photo) visible in the background; incidental.
- Content claim risk: captions say "Marine Technologies on the stand" and "NAVIS console"; verified-facts line 24 supports these as branded items on Sinor's stand. Guidance Marine and Fugro appear on the end card only, with no photo (as Rahul said); the end card says they supported "for their support", no supply claim.

## 8. Pacing (honest comparison)
- v6: 29.8 s, 8 photo beats plus 5.0 s end card. Beat lengths 4.0 (title), 2.8, 2.8, 3.2, 3.2, 3.2, 2.8, 2.8 s, crossfades 0.45 s. Hook: thank-you title, logo and strongest group photo are on screen from frame 0 and hold 4.0 s; the first cut is at about 4.0 s, so the hook window (first 5 s) is covered by the title plus the first 1 s of the NAVIS slide. The three pair slides each show two photos for 3.2 s (1.6 s per photo equivalent), which is quick; captions are 2.8 to 3.2 s on screen, readable in the stills but short for the longest caption ("Sonardyne SPRINT-Nav on the stand", 2.8 s).
- v5: 19.2 s, 4 photo slides of about 3.4 s plus a 4.0 s end card (v5 report). v6 is 55 percent longer and shows 11 photos instead of 4, with the partner end card now 5 s. I do not have the v3 file here; from the v5 report v3 was static slides. I cannot say whether the longer length helps or hurts completion; that is a hypothesis, not a measurement. v6 carries more content and more partners on screen, at the cost of faster beats.
- End card 5.0 s with the five names: enough to read (five 50 px lines).

## 9. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V6-1 | Medium | 9x16 slide 1 (6.8 to 9.6 s... i.e. 4.0 to 6.8 s; NAVIS) | Caption "NAVIS console" overlaps the NAVIS logo icon and "ENGINEERING"; lowest logo letters about 40 px below SAFE 1620. Fix: move the caption or the photo up/down in 9x16 for this beat, or drop the caption in 9x16. | Video producer |
| V6-2 | Low | 4x5 pair slides 3 and 5, top photo, with push-in | Right-hand head close to or touching the top edge; the zoom trims about 17 px more. Fix: shift the stack down 20 px or lower the zoom on pairs, or use crop_top. | Video producer |
| V6-3 | Low | 4x5 NAVIS slide | Caption clears the logo icon by only about 15 px at max zoom. Optional spacing. | Video producer |
| V6-4 | Info | 9x16 title | Date line touches the left man's shoe; hard teal to navy edge as in v5 (V4-3 unfixed); large blur bands on 9x16. | Video producer (optional) |
| V6-5 | Info | Photos | Section 7 items not individually approved (signage, bystander consent, screen coordinates). | Director to ask Rahul |
| V6-6 | Info | Process | Not played on a phone; audio silent; 9x16 end card not viewed. Rahul should play both once. | Director |
V6-1 correction: the NAVIS beat in the timeline is 4.0 to 6.8 s (beat index 1).

## 10. Verdict
- 4x5 master: spec PASS, fast start PASS, black/freeze PASS, safe margin PASS, motion smoothness PASS (measured), partner names PASS (viewed), logo PASS, manifest PASS, NAVIS logo uncropped and clear PASS. Technically ready; open: V6-2 and V6-3 (low), approvals in V6-5, publishing approval.
- 9x16 alternative: spec, fast start, motion, margin, names (by code), logo, manifest PASS; NAVIS slide FAIL (V6-1, caption collides with logo). Do not use until V6-1 is fixed.

## Candidate lessons for the Director
- When one slide mode differs by ratio (fith in 4x5, fit in 9x16), check the caption collision per ratio: a fix that clears a logo in one ratio can leave it overlapping in the other.
- Pair/stack layouts cropped with a centre crop plus a push-in clip heads at the top; leave 20 to 30 px of headroom or reduce zoom on pairs.
- A reusable shift-measurement script in scripts/ would save re-writing it each cycle (second recommendation).
