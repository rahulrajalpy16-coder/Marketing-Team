# QA report video 2 (cycle 2): adipec26-thanks_linkedin_4x5_v2.mp4

Reviewer: qa-reviewer (separate invocation from producer). Date 2026-11-06.
File: /tmp/work/adipec26/render2/adipec26-thanks_linkedin_4x5_v2.mp4 (3,498,309 bytes), SHA-256 58f527db6de33e21e495e899f9faf4c379ead7de977468d7bd8de50840291d32

## Verification scope (true)
- Script checks on the whole file: ffprobe, moov position, blackdetect (d=0.1), freezedetect (n=-60dB, d=1), loudness_check.py.
- Viewed at full resolution: slide_00 to slide_05 PNGs (each one). Cover JPG not opened separately (it is saved from slide_00; size 320,864 bytes).
- Video frames sampled (23 frames, viewed on 2 contact sheets, 360 px wide each): t = 0, 2, 4.25, 4.5, 4.75, 6, 8.05, 8.3, 8.55, 10, 11.85, 12.1, 12.35, 14, 15.65, 15.9, 16.15, 18, 19.45, 19.7, 19.95, 22, 25.68 s. That is start, middle and end of each of the 5 crossfades (4.25/4.5/4.75, 8.05/8.3/8.55, 11.85/12.1/12.35, 15.65/15.9/16.15, 19.45/19.7/19.95) plus holds.
- NOT a full real-time playback. Audio not listened to (silent by construction). Not tested on a phone or in LinkedIn.
- Scratch images are in /tmp/claude-0/s (not in the repo). Not written to qa/ to keep it small.

## Technical re-run
- ffprobe: H.264 High, yuv420p, 1080x1350, 25/1 fps (avg=r), 643 frames; AAC LC 48 kHz stereo (1206 frames); duration 25.72 s; 3.5 MB. Same spec as v1 (PASS).
- moov: first box found is moov at offset 40 (fast start): PASS.
- blackdetect: no black frames: PASS.
- freezedetect: static holds 0-4.56, 5.0-8.36, 8.84-12.16 (reported split at 10.0), 12.64-15.96, 16.44-19.76, 20.24-end. Matches the 5 crossfades. The split at 10.0 is a one-frame detector interruption: frames at 9.96 and 10.04 differ by at most 19 levels, bbox full frame (encoder noise), no visible change. Not a defect.
- loudness_check: Integrated -inf LUFS, true peak -inf dBTP; "within 1.5 LU of -14: CHECK" (expected, digital silence); true peak PASS. Silent by design.
- Final frame: end card held about 5.5 s, intentional.

## Caption re-check
- Em dashes (U+2014) and en dashes: none in final or plain.
- Bold: 29 mathematical sans-serif bold characters (U+1D5D4 to U+1D7FF), first at index 0, last at index 32, only in the hook line "Good conversations at ADIPEC 2026"; every non-space character of the hook is bold, none elsewhere.
- Plain equals final with the hook un-bolded (NFKC): TRUE. Text length 772 characters.
- New first sentence "The exhibition at ADNEC in Abu Dhabi has come to a close, and I am grateful to everyone who visited our stand." ADNEC and Abu Dhabi are supported by fact_check 1b. Not a dated claim. OK. Caption still says "technical discussions at the stand" and names NAVIS and Marine Technologies as partners (see D1). Hashtag #ADIPEC2026 is fine.

## Cycle-1 defects
| ID | Status | Evidence |
|----|--------|----------|
| D1 NAVIS / Marine Technologies names | Unchanged by design, still open | build_video.py PARTNERS unchanged; end card slide_05 and caption still say "NAVIS" and "Marine Technologies". fact_check 4a, 5a remain inferences. Needs Rahul's confirmation before publishing. |
| D2 Pill on collage hair | Fixed | Pill removed from content slides; collage now cropped to top photo (0,0,1206,710) and shown fit-with-blur. No overlay near faces in slide_02. New minor issue D10 below. |
| D3 Partner order and "for their support" | Unchanged by design, open for Rahul | Same end card text. |
| D4 Small steel-blue text | Fixed | Date line now 40 px LIGHT (196,218,240) and end-card secondary text LIGHT; "MIDDLE EAST FZCO" in the logo is part of the official logo image and remains small. Viewed: date line and footer legible. Footer 34 px is still the smallest text (low). |
| D5 Bottom margin | Partly fixed | Captions now at y 1208 (48 px type, ends about 1260); slide 0 date line at y 1220 to about 1262; end card footer at y 1236 to about 1270. This leaves roughly 80 to 90 px clear, but the stated 150 px safe zone is NOT met. Not verified on a device. Remaining: low. |
| D6 Over-claiming captions | Fixed in video | "Conversations at the stand", "At the stand" now. The caption text still says "technical discussions" (copy, low, Director's call). |
| D7 Stand panel figures 15+/100+/40+ | Unchanged, info | Still visible in the photos on slides 0 and 1 (not as copy). Needs Rahul's OK. |
| D8 Platform spec organic limits | Unchanged, info | Not a video matter. |

## Remaining and new defects
| ID | Severity | Location | Issue | Owner |
|----|----------|----------|-------|-------|
| D1 | Medium | End card (slide_05, about 20 to 25.7 s) and caption | NAVIS and Marine Technologies names unconfirmed by Rahul. | Director to ask Rahul |
| D9 | Medium | Slide 3, "At the stand" (about 12.6 to 16.2 s), TV screen right of the man in the grey suit, at roughly x 790-1060, y 490-510 of the slide | A media file name is readable on the on-stand TV: "Sinor_Original_BigCaptions_4K.mp4", overlapped by a subtitle line ("At ... reliably ... expected,"). It looks like an unprofessional leftover and reads as double-printed text. Unreadable overlap but the file name is legible at full size. Fix options: choose another photo (backup f9c048ec? check first), crop it out (the crop would cut the SMS sign), or blur that strip. Requires a photo-treatment decision. | Video producer, Director decides |
| D10 | Low | Slide 2 (about 8.8 to 12.6 s), top edge of the photo at y 359-370 of the slide | A white band about 12 px along the top of the photo: the collage's own white border (source rows 0 to 12 are white). It shows as a white stripe above the picture. Suggest start the crop at y=14 (crop 0,14,1206,710). | Video producer |
| D5 | Low | Bottom text on all slides | Text ends about y 1262 to 1270, inside the 150 px bottom zone (1200 to 1350). Text begins at y about 1208. Not device-tested. Optional: raise by about 50 px. | Video producer |
| D11 | Low | Slides 1, 2 (blur bands) | Fit-with-blur leaves large blurred bands (top about 270 px on slide 1 and 4; about 360 px top on slide 2). Looks acceptable but photo is small in the frame on slide 2 (1080x637 of 1350 px). Cosmetic. | Video producer (optional) |

## Public-exposure review (photos, as seen; nothing edited)
- Slide 3 (cf677e0a): media file name "Sinor_Original_BigCaptions_4K.mp4" and a subtitle fragment on the stand TV (D9). Other stand branding visible in background: "CHINA Pavilion" banners, "FLUIDS CHEM CO.", "HEBEI ALL LAND STEEL PIPE MANUFACTURING CO., LTD", an amphicos / EEI / YASKAWA partition (small), a Sonardyne tablet. Four unknown bystanders partly at the edges (one at the right edge, cropped). Badges: ADIPEC lanyards with QR codes; badge names are not legible at source resolution.
- Slide 4 (a07555b5): the stand screen shows coordinates (46.760942, -92.097473, 238.0) and a Windows taskbar and clock "12:37:10". The coordinates are illegible at phone width but readable full size; they look like a demo, which is a US location (not Gulf). Background shows "...ori Machinery Co.,Ltd." signage and a woman seated, unidentified, at the right; another person partly visible at the left edge. Badges have QR codes; names not legible.
- Slide 1 (0bc7989f): signage "CCS", "MAYEKAWA MYCOM" in the background (other companies' branding), plus panel text with figures 15+, 100+, 40+ and a QR code with "sinormarin..." (the stand's own). Several visitors in the background are unidentifiable. Badge text not legible.
- Slide 0 (0f44943b): four named-badge people, badge text unreadable; panel figures 100+ and 40+; "CHINA Pavilion" banners; other booths' signs ("amphicos", "Fluids Chem") faint. SMT logo partly cut.
- Slide 2 (0CDC96B1): no readable personal data; Sonardyne SPRINT-Nav branding and lanyards.
- Identification of the individuals is not something I did; the Director should confirm that the people shown consented/are appropriate to show (brief says unidentified).

## Other checks
- Spelling of all on-screen text: "Thank you.", "ADIPEC 2026 · ABU DHABI", "2-5 November 2026", "DP console on the stand", "Conversations at the stand", "At the stand", "Thank you for stopping by", end card: "To every client and visitor who stopped by our stand.", "And to our technology partners for their support:", Sonardyne, Fugro, NAVIS, Marine Technologies, footer. Correct; date and ADNEC/Abu Dhabi match fact_check 1a, 1b. No ADIPEC expansion. No em dashes.
- Logo: end-card logo and title-slide logo viewed against the official logo shape: accurate, on a white rounded card, not recoloured or warped.
- Faces: no text overlaps any face on any slide. Text on slide 0 sits over the lower bodies and the "Thank you." descender touches the area around knees only. Slide 3 caption sits over the man's legs/shoes only.
- Cover: the same image as slide_00, suitable and legible (not viewed separately).
- Manifest (sources/manifest.csv): 0f44943b selected, 0bc7989f selected, 0CDC96B1 selected (note: "softer (lowest sharpness)", flagged), cf677e0a selected, a07555b5 selected. No excluded or backup files used: PASS.

## Verdict
Technical spec, fast start, no black or unintended freeze, silent track, caption formatting: PASS as checked. Cycle-1 D2, D4 and D6 fixed; D5 partly. NOT READY TO PUBLISH: new medium defect D9 (media file name visible on the TV in slide 3) needs a fix, and D1 still needs Rahul's confirmation. D10 low. This is a sampled review, not full playback; audio not auditioned.

## Candidate lessons for the Director
- Zoom into screens, TVs and badges in every source photo before use; a file name or subtitle on an on-stand display is a recurring risk in event photos.
- Collage crops must start inside the photo, not on the collage's white border.
- Treat the bottom 150 px as the text-free zone for LinkedIn video when practical.
