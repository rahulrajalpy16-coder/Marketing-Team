# QA report video 3 (cycle 3): adipec26-thanks_linkedin_4x5_v3.mp4

Reviewer: qa-reviewer (separate from producer). Date 2026-11-06.
File: /tmp/work/adipec26/render3/adipec26-thanks_linkedin_4x5_v3.mp4 (2,732,536 bytes), SHA-256 3f422134799476722514d9f9003312514379fbb1a5751f2fa58642cfa025b11d

## Verification scope (true)
- Whole-file script checks: ffprobe, moov position, blackdetect (d=0.1), freezedetect (-60dB, 1 s), audio decode, volumedetect, loudness_check.py.
- Programmatic text-position test: rebuilt each slide from build_video.py with text, rectangles and the logo card suppressed, diffed against the saved slide PNG (rebuild with text matched the saved PNG exactly, max diff 0).
- Viewed at full resolution: slide_00 to slide_04 (all 5). Cover JPG not opened separately (saved from slide_00 by the script).
- Video frames sampled and viewed on contact sheets (360 px wide): t = 4.5, 4.75, 5.0, 8.3, 8.55, 8.8, 12.1, 12.35, 12.6, 15.9, 16.15, 16.4 (start, middle, end of each of the 4 crossfades = 12 frames) plus holds at 1, 3, 6, 10, 14, 21.5 and 21.8 s. 19 frames in total.
- NOT full real-time playback. Audio not listened to (silent by construction). Not tested on a phone or in LinkedIn.
- Scratch images: /tmp/claude-0/s3 (not in repo).

## Technical re-run
- ffprobe: H.264 High, yuv420p, 1080x1350, 25/1 fps, 548 frames; AAC LC 48 kHz stereo, 1028 frames; duration 21.92 s (script expected 21.9); 2.7 MB. PASS.
- moov: first box found is moov at offset 40 (fast start). PASS.
- blackdetect: no black frames. PASS.
- freezedetect: holds 0-4.56, 5.0-8.36, 8.84-10 / 10-12.16 (detector split at 10.0, same encoder-noise artefact as v2, not a defect), 12.64-15.96, 16.44-end. Matches 4 crossfades. PASS.
- Audio: decodes cleanly end to end; volumedetect mean/max -91 dB (digital silence). loudness_check: -inf LUFS, true peak -inf dBTP; "within 1.5 LU of -14: CHECK" is expected for a silent track; true peak PASS. Silent by design.
- Final frame: end card held about 5.5 s, intentional.

## Cycle-2 defects
| ID | Status | Evidence |
|----|--------|----------|
| D1 NAVIS / Marine Technologies names | Unchanged by design, still open | PARTNERS list unchanged; end card still shows both. Needs Rahul's confirmation before publishing. |
| D5 Bottom 150 px safe zone | Fixed | Programmatic: rows containing overlay pixels (text, accent bar, logo) span slide_00 48-1160, slides 01-02 1096-1164, slide_03 1096-1175, end card 360-1167. Maximum 1175, so nothing at or below y=1200 (1350-150). Slide_03 range is slightly larger only because of the "y" descender of "stopping by". Not device-tested; the safe-zone figure is the brief's number. |
| D9 media file name on TV | Fixed (photo held back) | cf677e0a no longer in SLIDES; slide_03 is a07555b5. Viewed: no media file name anywhere in the 5 slides. See manifest flag M1. |
| D10 white band on collage top | Fixed | slide_02 pixel rows: 355-362 blurred bg (58,69,87), row 363 onward picture (about 130-146 grey-blue); no white band (a white stripe would read near 255). Viewed zoomed rows 340-420 data and the full slide: clean top edge. |

## Remaining defects
| ID | Severity | Location | Issue | Owner |
|----|----------|----------|-------|-------|
| D1 | Medium | End card (about 16.4 to 21.9 s) and caption | NAVIS and Marine Technologies unconfirmed as partners (inference only). Do not publish until Rahul confirms. | Director to ask Rahul |
| M1 | Low | sources/manifest.csv | cf677e0a row selection column says "held back" (reason updated). The task note said it still lists "selected": the file I read says "held back" with reason, so no change needed. The photos used are all "selected" (see below). | Director (nothing to do unless Rahul approves the photo) |
| D12 | Low (cosmetic) | End card, 1105 to 1140 px | Gap between "Marine Technologies" and the footer line is only about 30 px, and the end card has about 180 px of unused space under the footer, so the footer looks attached to the partner list. The logo card to "Thank you" gap is also tight (about 30 px). Suggest moving the footer to about y 1180 or leave. | Video producer (optional) |
| D7 | Info | Slides 0 and 1 | Stand panel figures (15+ years, 100+ projects, 40+ countries) visible in the photos. Needs Rahul's OK. | Director |
| D11 | Low | Slides 1, 2, 3 | Large blurred bands above and below the photo (slide 2 photo 1080x623 of 1350). Cosmetic, unchanged. | Video producer (optional) |

## Layout check (viewed)
- Title slide: "Thank you." (y 910-1040) and event/date lines sit over the men's legs and trousers; faces and badges are untouched. The lead heading crosses the legs and the gradient is heavy there, but people are still readable; no cropped faces. Logo card top-left clear of faces (partly over the stand wall).
- Content slides: captions sit on the blurred or gradient band under the photo (slide 1 and 3, caption begins at the photo bottom edge y 1080 with the accent bar at 1096) and do not touch any person. Slide 2 is fully on the blur band. Readable at phone width (48 px type on 1080 wide).
- End card: all text legible; secondary lines LIGHT colour; footer 34 px is the smallest text (low legibility but readable).
- Crossfades: all 4 are clean dissolves with no black or cut frames; the mid-fade double text is the normal overlap.
- Spelling of all on-screen text correct; no em dashes; date and Abu Dhabi match earlier fact checks (as recorded in qa_report_video_2).
- Logo: end card and title logo cards accurate, undistorted, on white rounded card.

## Public-exposure review (4 photos used, as seen)
- Slide 0 (0f44943b): four people with ADIPEC lanyards and name badges (text not legible at full size); Sonardyne SPRINT-Nav housing; "CHINA Pavilion" banners; faint third-party booth signage ("FLUIDS CHEM CO", "HEBEI ALL LAND STEEL PIPE MANUFACTURING CO., LTD", "amphicos"); stand panel figures 100+ / 40+.
- Slide 1 (0bc7989f): HOLD POSITION panel with "15+ years DP engineering", 100+ projects, 40+ countries, a QR code and "sinormarin..." text; background signage "CCS" and "MAYEKAWA MYCOM"; several unidentified visitors in the background; badge text not legible.
- Slide 2 (0CDC96B1 top crop): Sonardyne SPRINT-Nav branding; one man seen from behind; lanyards with logos; a second standing visitor partly cropped. No readable personal data.
- Slide 3 (a07555b5): stand screen with coordinates 46.760942, -92.097473, 238.0 (visible, small), a Windows taskbar and a clock "12:37:10"; third-party signage "...ori Machinery Co.,Ltd."; a seated woman at the right and another person at the left edge (not subjects); badges with QR codes, text not legible.
- No media file names, e-mail addresses, phone numbers or readable badge names found in these four. I did not identify any individual; the Director should confirm the people shown are fine to show.

## Manifest check
Used files: 0f44943b selected, 0bc7989f selected, 0CDC96B1 selected (note: softer, flagged), a07555b5 selected: PASS. cf677e0a is "held back" in the manifest (not used). No excluded or backup file used.

## Verdict
Technical spec, fast start, black/freeze, silent track: PASS. D5, D9, D10 fixed; D1 still open by design. Video is technically ready; do NOT publish until Rahul confirms the NAVIS and Marine Technologies names (D1) and the stand panel figures (D7). Sampled review, not full playback; audio not auditioned; not phone-tested.

## Candidate lessons for the Director
- Verify text position by diffing a text-free render against the final slide instead of estimating by eye.
- When a photo is held back for a legibility issue, record it in the manifest in the same cycle.
