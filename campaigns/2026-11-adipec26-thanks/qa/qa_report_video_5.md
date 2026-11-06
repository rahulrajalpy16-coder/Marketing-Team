# QA report video 5 (second QA cycle for the v4/v5 redesign)

Reviewer: qa-reviewer (separate from the producer). Date 2026-11-06.
Files (SHA-256):
- 4x5: /tmp/work/adipec26/render5_4x5/adipec26-thanks_linkedin_4x5_v5.mp4, 5,721,995 bytes, fc8e5036a555485c991c5f5f5c8a3d0f1f8cdf933475edbb33ce8aaf4bbc7333
- 9x16: /tmp/work/adipec26/render5_9x16/adipec26-thanks_linkedin_9x16_v5.mp4, 6,910,316 bytes, 46ca975cc85dd8188200d841193233f5ad5ac263d67c01b0b1100ac1afd919c6

## True verification scope
- Whole-file scripted, both files: ffprobe, moov position, blackdetect (d=0.1), freezedetect (-60 dB, 0.5 s), full audio decode, volumedetect, phase-correlation shift series, per-frame difference series over all 480 frames.
- Motion: sub-pixel phase correlation (numpy FFT, Hann window, parabolic peak interpolation, 256x256 patches at left edge, right edge and centre) on consecutive frames inside each of the four photo slides (about 65 to 87 frames per slide), v4 and v5, both ratios. Also 8-frame windows at the start and end of every photo slide, and a sharpness (Laplacian variance) series per slide.
- Viewed at full resolution (1080x1350 and 1080x1920): t = 0.04, 2, 5.5, 9, 12.5, 17 s per file (title, slides 1 to 3, end card), 12 frames per file. Crossfades: 12 frames per file at 360 px wide, three per crossfade (start, middle, end): 4.0 / 4.225 / 4.45, 7.4 / 7.625 / 7.85, 10.8 / 11.025 / 11.25, 14.2 / 14.425 / 14.65 s. Plus a 700x140 crop around the caption at 4.6 s and 6.0 s (4x5).
- NOT done: audio not listened to (silent by construction); loudness_check.py not re-run, volumedetect gives -91 dB mean and max for both (silent track); not played on a phone or inside LinkedIn; motion judged from measurements and still frames, not by watching playback. Cover files: size checked (1080x1350, 1080x1920) and compared numerically with frame 0 (mean abs diff reported below), not opened visually.
- Scratch images: /tmp/claude-0-s5 (not in repo).

## 1. Technical spec (both files)
| Check | 4x5 | 9x16 |
|---|---|---|
| Codec / profile / pix_fmt | H.264 High, yuv420p | same |
| Dimensions | 1080x1350 | 1080x1920 |
| Frame rate | 25/1, 480 frames | 25/1, 480 frames |
| Audio | AAC LC 48 kHz stereo, decodes with no errors | same |
| Duration | 19.200 s | 19.200 s |
| moov before mdat | moov at offset 40 (first atom after ftyp) | same |
| blackdetect | none | none |
| freezedetect | one freeze from 14.64 s to end (end card, intentional) | same |
| Silent audio | mean and max -91.0 dB | same |
| Spec match (platform-specs LinkedIn row) | PASS (4:5 1080x1350, 9:16 1080x1920, MP4 H.264 AAC, 25 fps below 30, size well under 500 MB) | PASS |
Note: organic LinkedIn limits remain partly UNVERIFIED in platform-specs.md (ads page only).
Covers: both cover JPGs match frame 0 of the video (see section 6 note).

## 2. V4-1 motion judder: FIXED in both files
Measurement: horizontal shift per frame (px) of 256x256 patches, consecutive frames, steady part of each slide (crossfades excluded). Left edge patch (L), right edge patch (R).
| File / slide | v4 L mean, sd, CV | v5 L mean, sd, CV | v5 R mean, sd, CV |
|---|---|---|---|
| 4x5 slide 0 (title) | +0.253, 0.450, 1.78 | +0.119, 0.015, 0.13 | -0.111, 0.014, 0.13 |
| 4x5 slide 1 | -0.345, 0.494, 1.43 | -0.195, 0.019, 0.10 | +0.201, 0.021, 0.10 |
| 4x5 slide 2 | +0.347, 0.486, 1.40 | +0.186, 0.033, 0.17 | -0.198, 0.020, 0.10 |
| 4x5 slide 3 | -0.376, 0.487, 1.29 | -0.222, 0.050, 0.23 | +0.190, 0.019, 0.10 |
| 9x16 slide 0 | +0.252, 0.451, 1.79 | +0.115, 0.011, 0.09 | -0.078, 0.010, 0.13 |
| 9x16 slide 1 | -0.343, 0.496, 1.45 | -0.194, 0.019, 0.10 | +0.201, 0.023, 0.11 |
| 9x16 slide 2 | +0.347, 0.491, 1.42 | +0.187, 0.034, 0.18 | -0.197, 0.022, 0.11 |
| 9x16 slide 3 | -0.380, 0.493, 1.30 | -0.220, 0.048, 0.22 | +0.190, 0.020, 0.10 |
- Per-frame shift standard deviation fell from about 0.45 to 0.56 px (v4, comparable to the mean itself) to about 0.01 to 0.05 px (v5). CV fell from about 1.3 to 2.0 down to about 0.1 to 0.23. Slides 2 and 3 have the highest v5 CV (0.17 to 0.23) because those patches have little texture (blur band, plain wall), so the measurement itself is noisier there; the shift is still within +-0.05 px of the mean on average. Centre patches are about 0 as expected for a zoom about the centre.
- The mean shift is also continuous: v5 is about 0.2 px per frame at the edges (the zoom from 6 to 7.5 percent over 4.4 to 3.9 s), where v4 alternated 0 and about -1 px.
- Slide start and end (first and last 8 frames of each photo slide, left-edge shift): values in 0.10 to 0.17 (slide 0), -0.15 to -0.23 (slide 1), 0.13 to 0.27 (slide 2), -0.14 to -0.37 (slide 3). No jump or reversal at the start or end of any slide in either file. Slide 3 (and to a lesser extent slide 2) shows a +-0.1 px period-3 wobble in that low-texture patch, which I read as measurement noise near the detection limit, not a visible effect; I cannot prove which.
- Sharpness (Laplacian variance of the central band) changes monotonically within slides (title 955 to 727 as it pushes in, 4x5 slide 1 563 to 364); it varies smoothly with no pumping (no oscillation seen in the series; steady-state sd/mean 0.06 to 0.10 across the slide because the scene content changes with zoom). Not a shimmer. Edge artifacts: none seen at picture edges in the full-resolution frames, no black or white edge, no shimmer on fine detail in the stills at 0.04 / 2 / 5.5 / 9 / 12.5 s.
- Per-frame mean difference: title slide is flat (4x5 mean 1.04, sd 0.05, CV 0.04; 9x16 1.01, 0.03, 0.03), meaning constant motion every frame. Photo slide windows with crossfades inside show larger CV only because the crossfade changes the frame; not a judder.
- Limit: this is a data result plus stills. I did not watch playback, so I cannot rate visibility to a viewer, but the cause measured in v4 (1 px steps every 3 to 4 frames) is gone.
Status: V4-1 closed (measured) for both files.

## 3. Other V4 defects
- V4-3 (9x16, low): NOT fixed. Blur bands unchanged (slide 1 photo is the 810 px strip with about 540 px of blur above and 540 below; slide 2 about 640 px photo; title photo 1440 px, 240 px blur bands). Hard teal-to-navy edge at y 1680 on the title slide still visible in the full-res frame at 0.04 s. Optional.
- V4-4 (4x5 slide 1, low): NOT fixed. At 4.6 s the photo bottom edge is at about y 1106 and the accent bar (y 1096 to 1103) sits on top of the photo edge; at 6.0 s it still straddles the edge (see crop). Text itself is on the plain band. Cosmetic.
- V4-7 (4x5 end card footer): FIXED. End card lowest bright pixel row is now y 1180 (was 1194), margin to SAFE 1200 is 20 px.
- V4-5 (manifest wording) is a manifest note: the 0CDC96B1 reason in manifest.csv now reads "v3 and v4 use only the sharp top photo"; still does not mention v5 (info, trivial).

## 4. Overlay text versus safe margin (measured, rows of bright opaque pixels in the overlay PNGs and end_card.png)
| Ratio | SAFE | slide 0 | slide 1 | slide 2 | slide 3 | end card |
|---|---|---|---|---|---|---|
| 4x5 | 1200 | 48-1160 (40 px margin) | 1096-1164 (36) | 1096-1164 (36) | 1096-1174 (26) | 66-1180 (20) |
| 9x16 | 1620 | 130-1580 (40) | 1516-1584 (36) | 1516-1584 (36) | 1516-1594 (26) | 276-1390 (230) |
All text above SAFE in both files: PASS. (The navy gradient reaches the frame bottom but contains no text.) 150/300 px are the brief's figures, not device-tested.

## 5. Regression
- Faces: in all full-resolution frames viewed, no text over faces. Title "Thank you." and the date line sit over legs, shoes and floor (4x5 and 9x16); logo card over wall/ceiling area, not over a face. Captions on bands below photos. In 9x16 the date line touches the toe of the left man's shoe and the "Thank you." overlaps trousers; not faces. Also third-party sign letters "...HNOLOGIES" behind "Thank you." (background, not legible after overlay).
- Spelling: "Thank you.", "ADIPEC 2026 · ABU DHABI", "2-5 November 2026", "DP console on the stand", "Conversations at the stand", "Thank you for stopping by", end card text and partner list read correctly. No em dashes in build_video.py (grep count 0) or on screen. The middle dot is not a dash.
- Logo: end_card.png logo region versus assets/brand/sinor-logo.png resized with the build's own resize: mean absolute pixel difference 0.0 in both ratios (exact). Logo card on title slide viewed, undistorted, white card, no recolor. PASS.
- Manifest: used photos 0f44943b selected, 0bc7989f selected, 0CDC96B1 selected (top crop), a07555b5 selected. cf677e0a stays "held back" and is not in build_video.py SLIDES (comment only) and was not seen in any frame. PASS.
- Crossfades: all 4 are clean dissolves in both files, no black, cut or stuck frames. Mid-fade frames show both captions overlapping for about 0.45 s (readable-garbled), cosmetic, same as v4.
- Covers: both 1080x1350 and 1080x1920; the first-frame mean abs difference against video frame 0.04 s is 2.7/255 (4x5) and 2.5/255 (9x16), compression only; not opened visually.
- Public-exposure items unchanged from v4 (stand-panel figures 15+/100+/40+, coordinates on slide 3 screen, bystanders, ADIPEC lanyards, third-party signage including "...NCE MARINE" LED sign in the 9x16 title photo). Carry-over for Rahul's OK (V4-6).

## 6. Defects (open)
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V4-2 / V5-1 | Medium (open, by design) | End card | NAVIS and Marine Technologies remain unconfirmed by Rahul (verified-facts.md lists them as inference). Do not publish until confirmed. | Director to ask Rahul |
| V4-3 | Low | 9x16 | Large blur bands; hard teal-to-navy edge at y 1680 on title slide. | Video producer (optional) |
| V4-4 | Low | 4x5 slide 1, 4.0 to about 5.5 s | Accent bar straddles the zoomed photo bottom edge. | Video producer (optional) |
| V4-6 | Info | Photos | Panel figures, screen coordinates, bystanders need Rahul's OK. | Director |
| V5-2 | Info | Process | Motion fix verified by data and stills only; not watched in playback or on a phone. Rahul should play it once. | Director |
Closed: V4-1 (measured), V4-7. 

## 7. v5 versus v3
- v5 is better than v3 as a concept: motion on every photo (v3 was static slides), thank-you message and strongest photo in the first frame, larger overlays, safe margin enforced for both ratios, tidy end card. With V4-1 fixed there is no remaining technical regression against v3: spec, fast start, black, freeze, safe margin, logo, manifest all pass, same as v3. The motion adds soft downsides measured or seen: small sharpness drift during zoom, and the accent bar overlap (V4-4).
- Versus v4: better (smooth motion, end card margin). Same otherwise.
- I cannot say v5 will perform better with the audience; that is a hypothesis, not a measurement.

## Verdict
- 4x5 master: spec PASS, fast start PASS, black/freeze PASS, safe margin PASS, motion smoothness PASS (measured), partner names open. Technically ready; publish only after Rahul confirms NAVIS and Marine Technologies and approves publishing.
- 9x16 alternative: same PASS results, plus the cosmetic V4-3 (weaker variant than 4x5). Same publishing condition.

## Candidate lessons for the Director
- Render slow zooms with sub-pixel resampling (Pillow AFFINE bicubic or equivalent) rather than ffmpeg zoompan; verify with phase correlation (shift sd should be well under 0.1 px).
- Keep a shift-measurement script as a reusable QA tool (scripts/), since this is the second job where visual smoothness could not be judged by eye in this environment.
