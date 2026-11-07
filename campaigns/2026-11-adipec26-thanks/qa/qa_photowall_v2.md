# QA report: LinkedIn photo-wall vertical videos (render v2 of wall v1 and wall v2)

Reviewer: qa-reviewer (independent, did not produce the files). Date: 2026-11-07. Files not edited.

Files:
- A = /tmp/work/adipec26/wall_final_v1/adipec26-thanks_linkedin_photowall_v1_9x16_v2.mp4
  SHA-256 2882dacdde9c8c61a695a8dc281194a81aa50b3cd1a3cd6d3311d2ad18d311f5
- B = /tmp/work/adipec26/wall_final_v2/adipec26-thanks_linkedin_photowall_v2_9x16_v2.mp4
  SHA-256 7ca9dfb583480de6a87aea1f9f011b1009ff1af67cbde13eea7100eac40010ea

## Verification scope (what I actually did)
- ffprobe on both files. moov atom position (ffmpeg trace). scripts/loudness_check.py. blackdetect + freezedetect (freeze d=0.7s, -60 dB). silencedetect (-50 dB, 0.3 s).
- Frames: PNGs extracted at 1.5 s steps (t = 0, 1.5, 3.0 ...) plus one frame at 28.4 s (A) and 22.8 s (B). That is 20 frames for A and 16 for B. Each was viewed at full 1080x1920. Extra frames at 16.6 s and 7.8 s (A) and a caption-strip montage at 0.5 s steps from 10.5 to 15.5 s (both files) to check caption fades. Frames are in /tmp/work/qa_wall/.
- Motion: per-frame luma difference (signalstats YDIF) on every frame (858 for A, 690 for B) to look for duplicated or dropped frames. No duplicated frames mid-clip. This detects stalls, not perceived smoothness.
- NOT done: full real-time playback. AUDIO WAS MEASURED ONLY (loudness, peak, silence). I cannot listen, so I cannot judge music quality, tone or any glitch that does not show in the levels. Rendered captions between my 1.5 s samples were not individually inspected except the 10.5 to 15.5 s strip.

## Technical results
| Check | A (28.6 s) | B (23.0 s) |
|---|---|---|
| Container, video | MP4, H.264 High, yuv420p, 1080x1920 | same |
| Frame rate | 30/1 | 30/1 |
| Duration | 28.600 s (matches 28.6) | 23.000 s (matches 23.0) |
| Audio | AAC LC, 48 kHz, stereo, ~202 kb/s | same |
| Size / video rate | 38.1 MB, ~10.4 Mb/s | 31.6 MB, ~10.8 Mb/s |
| Fast start | moov first: PASS | moov first: PASS |
| Loudness | -14.0 LUFS, LRA 2.1, TP -3.3 dBTP: PASS | -14.1 LUFS, LRA 3.2, TP -3.3 dBTP: PASS |
| Black frames | none | none |
| Frozen frames | none | none |
| Silence gaps (>0.3 s at -50 dB) | none | none |
| Mid-clip duplicate frames | none (only first and last 2 frames static, expected) | none |

Notes: brain/platform-specs says the LinkedIn help page limits ADS to under 30 fps; organic limits are unverified. Both files are exactly 30 fps. This is only a risk for ad use (see D-10).

## Defects
Severity scale: blocker (do not publish), major (fix before publishing), minor (fix if cheap). Responsible specialist is my assumption from the repo roles (video editor for composition and timing, copy for wording); the Director should map it to the right agent.

| ID | File | Time | Severity | Defect | Corrective action | Owner |
|---|---|---|---|---|---|---|
| D-01 | A, B | 0.0 s (first frame; ghost still visible at 1.5 s) | major | Opening title "ADIPEC 2026" is giant white text sitting directly across faces of the tiles behind it (A: the 10-person team photo is the tile under "ADIPEC"; B: faces of three men and a console tile). Lesson 2026-11-07 says full-bleed word overlays must avoid faces. The first frame is also what LinkedIn shows as the thumbnail. | Move or shrink the title, or place it over tiles without faces (consoles, sign, ship images), or dim the tile under it more. In A, Rahul's rule is to open with the team photo, so the team tile should be clear of the title. | video editor |
| D-02 | A, B | 0.0 s to ~1.5 s | major | Subtitle "ABU DHABI . 2-5 NOVEMBER 2026" is thin grey-white text on mid-grey photo tiles. At phone size it is barely readable, and it is the only place the dates and venue appear. | Increase weight and contrast (darker scrim strip or solid plate), same style as the lower-third plates. | video editor |
| D-03 | A, B | all frames (logo watermark at top left, y 92 to 172) | minor | The persistent Sinor logo chip sits inside the top ~150 px zone and partly overlaps faces on moving tiles (B at 4.5 s: it clips the left man's face; A at 0 s: sits over the MT screen tile). | Move the chip below y 150 or to a face-free corner, or fade it out in the middle section. | video editor |
| D-04 | A | 0.0 s and 1.5 s | minor | One tile crops the stand sign to "NOR MARINE SERVICES" (the "SI" is cut off) and it is prominent in the opening frame. Reads as a misspelled brand at phone size. Other tiles crop to "SINOR MARINE SERV..." at the edge, which is normal. | Re-crop that tile so the full "SINOR" shows, or move it off the first frames. | video editor |
| D-05 | B | 3.0 s (caption 01/06 "Our team on the stand") | major | Over-claim risk. The featured tile shows three men; one wears a white shirt with a different company badge and an oval logo, and his ADIPEC pass appears to read a Marine Technologies affiliation. "Our team" is not supported by any verified fact for these three people. (Lesson 2026-11-06: do not write "our" for things or people not confirmed as Sinor's.) | Change to a neutral line such as "On the stand" or "Conversations on the stand", or have Rahul confirm who the three are. | copy / video editor |
| D-06 | A | 3.0 s (01/08 "The Sinor Marine team at ADIPEC 2026") and B at 15.0 s (06/06, same text) | minor | Claim is supported for the 10-person photo (Rahul identified it as the full Sinor team, verified-facts 2026-11-06). The caption plate at 01/08 appears while the 10-person tile is mostly off-screen in A (the plate covers the lower half; the team tile is at the top). In B, at 15.0 s the plate "The Sinor Marine team" sits under a different featured tile (the Emirati meeting and a small tile pair), not the team photo; the team photo is further down-left at that moment. Caption and image do not line up. | Retime the plate so the team tile is the featured/centred tile when its caption is shown. | video editor |
| D-07 | A | 13.5 s (07/08 "Visitors at our stand") | minor | "Visitors" is applied to a tile of people in blue ADNOC-style coveralls. They are unidentified, and nothing in verified-facts says they are visitors or clients. Plausible but not verified. It is also generic, which Rahul rejected earlier ("At the stand"). | Keep only if Rahul confirms; otherwise "Conversations at our stand". | copy |
| D-08 | A | 15.0 s (08/08 "Together at our stand") | minor | Featured tile is the four-man group with a different-company white shirt (same person as D-05) plus the MT screen tile. "Together at our stand" is vague and implies they are all Sinor. Not strictly false. Also, at 15.0 s the plate hides the lower half of the MT tile, so the caption and photo again do not match. | Align timing and use a specific neutral wording. | copy / video editor |
| D-09 | A, B | caption plates 05 ("Marine Technologies on the stand") at ~12.0 to 13.5 s | minor | Plates fade in and out slowly. At the 1.5 s sample points (12.0 s and 13.5 s in both files) the plate is mid-fade (semi-transparent text on busy tiles), and the solid state lasts roughly 1.5 to 2 s per plate. Short hold for muted viewing and the ghost state looks messy. The caption is accurate: Marine Technologies is a confirmed partner and the MT logo/screen is in the photo. | Shorten the fade, lengthen the hold to about 2.5 to 3 s. | video editor |
| D-10 | A, B | whole file | minor | Frame rate is exactly 30 fps. brain/platform-specs notes the LinkedIn ads help page says "under 30 fps" for ADS; organic limits are unverified (third-party reports 10 to 60 fps). Not a defect for an organic feed post as far as known, but unverified. | If the post will be boosted or used as an ad, re-encode at 29.97 fps or confirm the spec; otherwise record as unverified. | Director (spec) |
| D-11 | A, B | throughout wall section | minor | Unrelated or neighbouring-stand brands and text are legible in tiles: "shipworkz" and "www.shipworkz.com" (large, next to the team photo, repeated in several tiles), Nagamori Machinery, CCS, Mayekawa Mycom, "ONE-MICROF / HP-LUB II", "China Pavilion", "Maritime Theatre". "amphicos.com" is the verified shared-stand partner (verified-facts), so that one is fine. Shipworkz is the most prominent: it reads as a partner logo beside the team. | Crop tiles to hide the Shipworkz signage where possible, or Rahul confirms they are acceptable. | video editor / Director to ask Rahul |
| D-12 | A | ~16.5 s tile region near the ship wall | minor | A tiny on-screen file name is visible on a tile (stand video wall, text reading like "Sinor_Captions_BigCaptions_AI_Kimpad"). Brain notes say Rahul approved that photo with a visible file name earlier. Not seen in B. | Confirm Rahul still accepts it in this version, or blur/crop. | video editor |
| D-13 | A, B | end card, bottom of the stack | minor | End card layout is correct: Sinor logo, "Thank you.", client line, partner line, five logos each with the full name in text (Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine). Spelling is right and no em dashes. Issues: (a) the teal line "And to our technology partners for their support:" is low contrast against the busy dimmed background (A and B); (b) in B the "Fugro" label has a "Shipwor..." tile ghost behind it and the "Marine Technologies" label has a man's face behind it; in A the faces behind "Thank you." are visible. All labels are above the bottom 300 px zone (lowest label ends near y 1565). | Raise the end-card scrim opacity, or put a solid plate behind the teal line; drop the bright tiles from behind the labels. | video editor |
| D-14 | A, B | file names | minor | File names do not match the checklist pattern <campaign>_<platform>_<aspect>_v<n>.mp4 (extra "photowall" token and a double version "v1 ... _v2"). Ambiguous: file A is "v1" of the wall concept at render "v2". | Rename at delivery to e.g. adipec26-thanks_linkedin_9x16_v3.mp4 and keep a log of what each version is. | Director |

## Checks with no defect
- Names and spelling: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine, SPRINT-Nav, ADIPEC, "Sonardyne SPRINT-Nav on the stand", "Navis Engineering console on the stand" (A at 6.0 s, B at 7.5 s). All consistent with verified-facts. The NAVIS and Sonardyne captions describe equipment visible in the photos (labelled NAVIS Engineering console, Sonardyne SPRINT-Nav unit) and do not claim ownership or supply.
- "With Guidance Marine at our stand" is attached to the photo a07555b5 in the build script (exports/build_photowall.py), matching Rahul's statement. I cannot independently verify the identity of the woman; this is USER-SUPPLIED. The caption wording "With Guidance Marine" is acceptable under that statement.
- Partner names on the end card are full names. Partner logos are the user-supplied ones; I did not compare them to official brand files, only against what I could see (Fugro logo renders as the stylised "FUGRO"; MT oval is shown with the "Marine Technologies" label as required).
- No black frames, no frozen frames, no silent gaps, no audio clipping (true peak -3.3 dBTP).
- Motion: no duplicated frames mid-clip. The wall scroll is fast (average frame difference 20 to 40 luma levels per frame in the faster seconds, around 7 s, 14 s, 19 s in both files). Tiles are readable on still frames, but fast sections may look busy on a phone; this is a taste point, not a defect.
- Last frame is intentional (end card) and holds ~4.6 s (A) and ~4 s (B) with slow drift. Final frames are static, which is expected.
- No private information seen beyond event badges. Many badges and QR codes appear in tiles; badge text was not readable at 1080x1920 except where ADIPEC pass layouts are visible. Not read or logged.
- Both files are in the correct vertical 9:16 1080x1920 format; the brief originally asked for 4:5 (1080x1350). If Rahul later asked for 9:16 only, fine; I did not find a record in the brief of the switch, so confirm.

## Verdict
- File A (28.6 s): NOT READY. Fix D-01 and D-02 (major). Minor items D-03, D-04, D-06 to D-09, D-11 to D-14 should be cleared or accepted by Rahul. Technical specs and loudness pass.
- File B (23.0 s): NOT READY. Fix D-01, D-02 and D-05 (over-claim "Our team", major). Minor items D-03, D-06, D-09 to D-11, D-13, D-14 as above. Technical specs and loudness pass.
- Both pass the technical gate. The remaining issues are legibility, caption accuracy and tidy-up. After the fixes a re-check of the affected frames is needed; this report does not cover them.

## Candidate lessons for the Director (not saved by me)
1. Opening title cards for photo walls: keep the biggest title off faces and off the team photo; test the first frame as a LinkedIn thumbnail.
2. A caption plate must be shown when its photo is the featured tile; check sync by extracting the frame at the plate's peak opacity.
3. Neighbouring-stand brands (Shipworkz) show up in tiles; crop them out or get Rahul's OK.
4. Never write "Our team" over a photo unless the people are confirmed as Sinor staff.
5. Name render versions clearly (concept version vs render version).
