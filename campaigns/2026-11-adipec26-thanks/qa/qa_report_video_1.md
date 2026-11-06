# QA report video 1: adipec26-thanks_linkedin_4x5_v1.mp4

Reviewer: qa-reviewer (separate invocation from the producer). Date 2026-11-06.
File: /tmp/work/adipec26/render/adipec26-thanks_linkedin_4x5_v1.mp4 (3,711,030 bytes)
SHA-256: 34054930972936935b84dd1b88f09fbe922ea8df4a8a82462a1289de8e046955

## Verification scope (true)
- ffprobe, moov position, blackdetect/freezedetect and loudness_check were run on the whole file by script.
- Visual review: 18 frames extracted and viewed (3 contact sheets of 6): t = 0.0, 2.0, 4.5, 4.75, 5.0, 8.3, 8.55, 8.8, 12.1, 12.35, 12.6, 15.9, 16.15, 16.4, 19.7, 19.95, 20.2, 25.68 s. Exact list: 0.0, 2.0, 4.5, 4.75, 5.0, 8.3, 8.55, 8.8, 12.1, 12.35, 12.6, 15.9, 16.15, 16.4, 19.7, 19.95, 20.2, 25.68. That is start/middle/end of each of the 5 half-second crossfades, plus first frame, one mid-slide-0 frame and the last frame. Slides 1 to 4 mid-hold were not viewed as video frames, but the individual slide PNGs were checked via the transition endpoints and slide_02.png at half size. The slide_00, 01, 03 and 04 PNGs and the cover JPG were not opened separately.
- NOT a full real-time playback. Audio was not listened to (it is silent by construction; loudness_check confirms).
- Scratch sheets (kept in qa/): frames_sheet_1.jpg, frames_sheet_2.jpg, frames_sheet_3.jpg.

## Checks
1. Spec (ffprobe): PASS. MP4 (mov,mp4), H.264 High, yuv420p, 1080x1350 (4:5), 25 fps constant (r=avg=25/1), 643 frames, AAC LC 48 kHz stereo, duration 25.72 s, 3.7 MB. LinkedIn row (partly verified, ads): MP4, 4:5 max 1080x1350, H.264, under 30 fps, 75 KB to 500 MB: all met. Organic-post limits remain UNVERIFIED in platform-specs.md (third-party only), so organic acceptance is not confirmed by a primary source. Minor: audio 25.70 s vs video 25.72 s, harmless.
2. Fast start: PASS. First box found by ffmpeg trace is moov at offset 40 (before mdat).
3. Black and freeze: blackdetect (d=0.1) found no black frames: PASS. freezedetect (n=-60dB, d=1) reported static segments 0-4.56, 5.0-8.36, 8.84-12.16, 12.64-15.96, 16.44-19.76, 20.24-end. This matches five 0.5 s fades at about 4.5, 8.3, 12.1, 15.9, 19.7 s with static holds between. No unintended freezes: PASS. Nothing here shows a broken transition. Final hold is the end card, about 5.5 s: intentional.
4. Frames:
   - Text readable: PASS on the 1080-wide frames at 432 px thumbnail size. Headline "Thank you." and partner names are large. Weakest: date line "2-5 November 2026" (steel blue on dark gradient, 36 px) and footer "Sinor Marine Services Middle East FZCO" (30 px, steel). Readable but small at phone size (see D4).
   - Logo: PASS. End-card logo compared with assets/brand/sinor-logo.png: same shape, proportions and colour, not warped, on a white rounded card (not recoloured). Title-slide logo (250 px wide) also accurate but its "MIDDLE EAST FZCO" line is tiny (D4).
   - Faces: no face cropped badly in slide 0, 3 and 4 (all heads and shoulders complete). Slide 0 crop clips the "SINOR MARINE SERVICES" panel at the right edge and a fragment "ITION." at left (cosmetic).
   - Distortion: none seen; slides 1 and 4 are letterboxed over a blurred copy, not stretched.
   - Text over faces: slide 2 (collage): the "ADIPEC 2026" pill touches the top of the right-hand man's hair and forehead (D2). Title slide text sits over the lower bodies/legs only, not faces: PASS. Slide 4 caption overlays the lower body area only.
   - Margins: left/right 64 px; bottom text ends about 1294 of 1350 (56 px margin) on slide 0 and caption baseline near 1294 on others. Acceptable for feed; LinkedIn's bottom playback bar may overlap about the last 40 to 60 px on some devices. Not verified on a device (D5).
5. On-screen text (from script and viewed frames): "Thank you.", "ADIPEC 2026 · ABU DHABI", "2-5 November 2026", "DP console on the stand", "Technical discussions at the stand", "Meeting visitors at the stand", "Thank you for stopping by", "Thank you / To every client and visitor who stopped by our stand. / And to our technology partners for their support: / Sonardyne / Fugro / NAVIS / Marine Technologies / Sinor Marine Services Middle East FZCO". Spelling correct. Sonardyne and Fugro match fact_check 2a, 3a. Dates match 1a (ADNEC listing). "ABU DHABI" matches 1b. "ADIPEC" only, no expansion: correct per 1e. No em dashes in the script text (middle dot used; grep for the em dash found none). Partner names: see D1 and D3.
   Claims versus photo:
   - "Technical discussions at the stand" (slide 2): photo shows people seated at a table beside a Sonardyne SPRINT-Nav; it is a conversation, "technical" is an assumption (D6, low).
   - "DP console on the stand" (slide 1): supported (screen and joystick console under HOLD POSITION panel).
   - "Meeting visitors at the stand" (slide 3): two men standing for a photo; not shown to be visitors rather than staff. Brief says people are unidentified. Mild over-claim (D6).
   - "Thank you for stopping by" over slide 4 (two staff-style badges): intent rather than claim. OK.
   - End card thanks four partners, but the photos show only Sonardyne branding clearly; Fugro, NAVIS, Marine Technologies are not visible in any photo. Acceptable as a text thank-you, not a claim of product presence, but see D3.
   - Stand panel in slide 1 (and background of slide 0) shows "15+ ... 100+ ... 40+" figures. The brief said these claims are not to be used until Rahul confirms. They appear only as small photographed text, not as video copy: note only (D7).
6. Manifest: PASS. Used files: 0f44943b (selected), 0bc7989f (selected), 0CDC96B1 (selected), cf677e0a (selected), a07555b5 (selected). No excluded file (0c488f3f, b8be5c13) and no backup file used. All five files exist in /tmp/work/adipec26/jpg/. Coverage gap acknowledged in the brief: 7 HEIC not decoded, so not "all main images" yet. This is the stated open item, not a defect of this render.
7. Audio: PASS as a valid, intentionally silent track. AAC LC, 48 kHz, stereo, 1206 frames. loudness_check.py output: "Integrated: -inf LUFS | True peak: -inf dBTP | LRA: 0.0 LU; Loudness within +/-1.5 LU of -14.0: CHECK; True peak at or below -1.0 dBTP: PASS". The CHECK is expected (digital silence, no loudness to measure). Matches the "no music supplied" decision. LinkedIn feed autoplays muted, so no impact.
8. Industry or company objections: see defects D1 to D3. No person is shown unflatteringly in a held slide. Transition frames overlap two photos (ghosting of faces at 4.75, 8.55, 12.35, 16.15, 19.95) for about 0.5 s each; normal for crossfade, no single frame is unflattering. Slide 2 shows a blurred, mid-speech man in the lower half of the collage (soft focus, from the supplied collage): acceptable but the weakest photo (D2).
9. Delivery metadata: name follows campaign_platform_aspect_vN. Size and SHA-256 recorded above. Cover jpg 319,809 bytes is a copy of slide_00 (title slide), suitable and legible; not viewed separately beyond its source frame at t=0.

## Defect list
| ID | Severity | Location | Issue | Owner |
|----|----------|----------|-------|-------|
| D1 | Medium | End card, 3rd partner line | "NAVIS" is Rahul's stand-logo styling. fact_check 4b says brand is "Navis Engineering"; 4a says the link to the stand console is an inference. Also 5a: "Marine Technologies" is an inference for "MT". Both unconfirmed by Rahul. Do not publish until confirmed. | Director to ask Rahul; video producer to re-render if names change |
| D2 | Low | Slide 2 (about 5.0 to 8.8 s) | "ADIPEC 2026" pill touches the top of the right-hand man's hair/forehead; photo is a stacked collage with a visible seam and the lower half shows a blurred face. | Video producer (move pill or crop_top for this slide) |
| D3 | Low | End card | Partner list order and the claim of "for their support" rest on Rahul's dictation. "SMT for Fugro" (Sinor Marine Technologies / SMT UK) is not represented; partners with unstated roles correctly omitted. Needs Rahul's decision, not a video defect. | Director |
| D4 | Low | Slide 0 date line; slide 0 logo "MIDDLE EAST FZCO"; end-card footer | Small steel-blue text on dark gradient is legible but marginal at phone size. Suggest larger or whiter text. | Video producer |
| D5 | Low | Bottom 56 px of all slides | Bottom margin may sit under LinkedIn's playback bar on some devices; not tested on device. NOT VERIFIED. | Video producer (optional: raise captions about 20 px) |
| D6 | Low | Slides 2 and 3 captions | "Technical discussions" and "Meeting visitors" claim slightly more than the photos show (seated conversation; two men standing). Consider "Conversations at the stand" and "At the stand". | Copywriter / Director |
| D7 | Info | Slides 0 and 1 photographed panel | Panel figures (15+, 100+, 40+) are visible in photos though brief withholds these claims pending Rahul. Tiny and not copy; confirm acceptable. | Director |
| D8 | Info | Platform spec | LinkedIn organic limits unverified in primary sources; file is well within every figure listed. | Director |

## Verdict
No blocking technical defect: file plays by spec, fast-start, no black or unintended frozen frames, logo accurate, only manifest-selected photos used, no em dashes. Verdict: PASS on technical and visual checks as sampled; CONDITIONAL on Rahul confirming partner names (D1) before publishing. Not a full playback review. Audio not auditioned.

## Candidate lessons for the Director
- Check that overlay pills do not touch faces on collage or cover-cropped slides; offer a per-slide pill position.
- Keep small steel-blue secondary text at 40 px or larger on dark gradients for phone viewing.
- Captions on people photos should describe only what is visible ("At the stand") unless roles are confirmed.
