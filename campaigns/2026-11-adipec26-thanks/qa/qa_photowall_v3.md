# QA report: LinkedIn photo-wall vertical videos, render v3 (wall v1 and wall v2)

Reviewer: qa-reviewer (independent, did not produce the files). Date: 2026-11-07. Files not edited. Frames are in /tmp/work/qa_wall3/.

Files:
- A = /tmp/work/adipec26/wall3_v1/adipec26-thanks_linkedin_photowall_v1_9x16_v3.mp4 (31,303,765 bytes) SHA-256 30eba1eb6d75955f08e809c18badb7ef82d18298cc8f4dfbdc6a7cd54e8bfb9e
- B = /tmp/work/adipec26/wall3_v2/adipec26-thanks_linkedin_photowall_v2_9x16_v3.mp4 (28,217,081 bytes) SHA-256 f4933afd3cc77b629b01e05ab6c456604c13f47ef10fd3d583e9317266f2b104

## Verification scope (what I actually did)
- ffprobe, moov position (first 200 kB scan: moov at byte 36, mdat later), scripts/loudness_check.py, ebur128 with true peak, astats, blackdetect (d=0.2), freezedetect (-60 dB, 0.7 s), silencedetect (-50 dB, 0.3 s), per-frame luma difference (YDIF, all 738 frames of A and 666 of B).
- Frames viewed at full 1080x1920: A 16 frames (every 1.5 s) plus 0.8 s and 24.56 s; B 14 frames (every 1.5 s). Also t=0.0 (both, half size), 4 fps caption strips (A 11.0 to 15.5 s, strip made for B 10.0 to 14.5 s but not viewed), zoomed logo crops at 3 time points, and 19.0 to 19.3 s transition strip (A).
- TIMESTAMP CORRECTION: my fps=1/1.5 extraction landed 0.75 s late (I verified by pixel matching). True times of the numbered frames are 1.5k + 0.75 s (a_00/v2_00 at about 0.75 s). All times in this report are the corrected ones. Sample spacing is still 1.5 s. B frame at 22.16 s was extracted but not viewed (end card is static).
- NOT done: real-time playback. AUDIO MEASURED ONLY, I cannot listen. Captions between samples were seen only in A's 11 to 15.5 s strip. Spelling was read on viewed frames only. Cover JPGs in the same folders were not inspected. Official partner logo files were not compared; logos judged only against what is visible.

## Technical results
| Check | A (24.6 s) | B (22.2 s) |
|---|---|---|
| Video | H.264 High, yuv420p, 1080x1920, 30/1 | same |
| Duration | 24.600 s (match) | 22.200 s (match) |
| Audio | AAC LC 48 kHz stereo | same |
| Fast start | moov first: PASS | PASS |
| Integrated loudness | -14.0 to -14.2 LUFS (script -14.2, LRA 3.6): PASS | -14.2 (LRA 3.6): PASS |
| True peak | 0.0 dBTP (script says "-0.0", ebur128 "Peak -0.0 dBFS"; astats sample peak -0.02 dB one channel): FAIL, limit -1 dBTP | 0.0 dBTP (astats -0.32 dB sample peak): FAIL |
| Black frames / freezes / silence | none detected | none detected |
| Mid-clip duplicates | none (only frame 0, and static end card at about 21.4 s on, expected) | none (end card static from about 18.9 s) |

Note: true peak of 0 dBTP is at the clipping edge. No flat factor was found (astats Flat factor 0), so no sustained clipping measured, but the brief says below -1 dBTP and the earlier v2 render passed at -3.3 dBTP. This is a regression.

## Client correction requests, pass or fail
| # | Request | A | B |
|---|---|---|---|
| 1 | Logo transparent, no white card | FAIL. A semi-transparent grey-white rectangle (about x48-258, y92-172) is visible behind the logo on every tile frame (zoom crops at 3.75, 6.75 s). On dark or mid tiles it looks like a smudged card and the dark blue text loses contrast. On the opening veil (0.75 s) the logo is a clean white version: PASS there. | FAIL, same box. Visible at 2.25, 3.75, 5.25 s etc. |
| 2 | Opening wall mostly Sinor staff | PARTIAL PASS. Opening tiles (0.75 s): three 2 to 4 person Sinor shots, the 10-person team photo, two Sonardyne+Sinor group tiles, but also a console tile, a blank wall tile and the large UAE meeting tile. Mostly people, majority staff. | PARTIAL. Opening is about 70 percent Sinor-and-partner group shots, with 3 console or wall tiles. Team photo is almost hidden under "ADIPEC". Sonardyne staff appear in many tiles, so not "mostly Sinor staff". |
| 3 | SPRINT-Nav hero from the close-up; group photo in surrounding tiles | PASS for hero (close-up at 8.25 s, caption 03/07). Group photo only PARTIAL: around the hero the group tiles are cropped to legs and feet (8.25 s) or two of four people (9.75 s). Full group is visible earlier at 6.75 s. | PASS. Hero at 5.25 to 6.75 s; full four-person group tile directly above and beside it (5.25 s), plus the Sonardyne-staff and Sinor duo tile. |
| 4 | Partner logos on captions, transparent, clean; end card logos transparent, original colours, full names | PASS for design: Sonardyne, Navis Engineering, MT oval, Guidance Marine logos sit on the plate without boxes, colours look original. End card has five logos with full names, no boxes. Caveat D-05 (logo fade). | PASS, same. |
| 5 | Last caption "Visitors", five-person photo; blue-coverall photo only in wall | PASS. 07/07 "Visitors at our stand" at 18.75 s, five-person tile featured. Blue-coverall tile seen only as a small wall tile (11.25 s). See D-08 on wording. | PASS. 06/06 "Visitors at our stand" at 15.75 s, five-person tile featured. Blue-coverall tile not seen in any sampled frame. |
| 6 | Professional look, LinkedIn spec | Format PASS, loudness integrated PASS, true peak FAIL. Look: clean, consistent type and plates; defects D-01 to D-07 hold it back. | same |

## Defects
Owner names are my assumption from repo roles: video editor = composition, timing, compositing; copy = wording; audio = mix and master.

| ID | File | Time | Severity | Defect | Corrective action | Owner |
|---|---|---|---|---|---|---|
| D-01 | A, B | all wall frames after the veil, top-left y92-172 (best seen 3.75, 6.75, 11.25 s) | blocker (client item 1) | Logo is NOT transparent: a faint rectangular grey-white haze with hard edges sits behind it. It reads as a card and is visible on dark tiles. Dark blue logo text on dark or mid tiles has weak contrast, and it overlaps tile text (A 18.75 s doubles with the "SINOR MARINE SERVICES" sign; A 11.25 s covers the MT oval). | Re-key or re-export the logo with true alpha (no matte), check the PNG alpha channel has 0 outside the glyphs. For legibility use a light and a dark variant switched per tile, or a very soft shadow, not a box. | video editor |
| D-02 | A, B | whole file | blocker | True peak 0.0 dBTP (limit -1 dBTP). Previous render was -3.3 dBTP. Risk of inter-sample clipping after LinkedIn re-encode. | Re-master with a limiter at -1.5 dBTP, re-render, re-run scripts/loudness_check.py. | audio / video editor |
| D-03 | A, B | 0.0 s | minor | First frame (the LinkedIn auto-thumbnail) has no title and no logo, only a dark wall; title and logo fade in after. Cover JPG not inspected. | Hold a title in frame 0 or supply a cover image at upload. | video editor |
| D-04 | A, B | 0.75 s to about 2.4 s | minor | Opening title "ADIPEC 2026" sits over the team tile (A: over the 10-person photo at y750-950, hiding bodies and crowding faces; B: over staff torsos). Subtitle "ABU DHABI . 2-5 NOVEMBER 2026" is grey-white on mixed tiles and thin; at 2.25 s as the veil lifts it is nearly unreadable. Repeats v2 D-01 and D-02 at lower severity because the veil now helps. | Keep the 10-person photo clear of the title in A, keep the veil darker until the subtitle has gone, add weight to the subtitle. | video editor |
| D-05 | A, B | caption fade-in and fade-out (A 12.75 and 14.25 s MT; 15.75 s Guidance; B 12.75 and 14.25 s Guidance) | minor | During the roughly 0.3 s fades the partner logo stays more opaque than the plate. A dark logo (Guidance Marine black text) floats over a busy tile (A 15.75 s over the SPRINT-Nav label; B 12.75 s same), looking messy for a few frames. Solid hold is short, about 1.25 to 1.75 s (from the A strip). | Fade logo, text and plate with one opacity curve; lengthen hold to about 2.5 s if timeline allows. | video editor |
| D-06 | B | about 17.25 s (end card cross-fade) | minor | Mid-dissolve frame shows wall tiles ghosting through "Thank you.", the partner logos and labels for part of a second. A does it with a fast whip (peak luma difference about 57 per frame at 19.2 s) and lands clean. | Shorten the dissolve or fade the wall out faster than the card fades in. | video editor |
| D-07 | A | 8.25 and 9.75 s | minor (client item 3 partial) | Group photo around SPRINT-Nav hero is cropped to legs, feet or half the people, so it is hard to recognise as the Sonardyne and Sinor group shot. | Place the full group tile (uncropped aspect) adjacent to the hero while its caption is on screen, as B does. | video editor |
| D-08 | A, B | A 18.75 s, B 15.75 s | minor, needs client confirmation | "Visitors at our stand" over the five-person photo. Nothing in brain/verified-facts identifies those people as visitors. Two of the five wear clothing and look similar to people shown in the Sinor tiles; this is a visual impression only, I cannot verify identity. The client asked for this caption, so I record it as an open question, not a fault. | Rahul to confirm all five are visitors; if not, use a neutral line. | Director |
| D-09 | A, B | 0.75 s through the wall, repeated in many tiles | minor | Neighbouring stand text still legible: "shipworkz" and "shipworkz.com" (large next to the team tile), "Nagamori Machinery", "ONE-MICROF / HP-LUB", "CCS", "MAYEKAWA MYCOM", "Maritime Theatre", "CHINA Pavilion". Carried over from v2 D-11. | Crop the Shipworkz tiles or confirm acceptable with Rahul. | video editor / Director |
| D-10 | A, B | whole file | minor | File names still do not follow <campaign>_<platform>_<aspect>_v<n>.mp4 (photowall, concept v1/v2 plus render v3). | Rename at delivery and log. | Director |
| D-11 | A, B | end card, 20.25 s onward (A), 18.75 s (B) | minor | Layout is clean and balanced, all text above y1570 (bottom 300 px clear). Small points: the "Navis Engineering" label sits very close under its logo; MT and Fugro logos are optically smaller than Sonardyne. | Add 10 to 15 px under the NAVIS logo; optional logo size balance. | video editor |
| D-12 | A, B | 10-person team caption (A 3.75 s, B 3.75 s) | note | A: "The Sinor Marine team at ADIPEC 2026" is shown while the team tile is the featured tile: aligned. B: plate sits under the team tile too. No defect, recorded as improved from v2 D-06. | none | n/a |

## Checks with no defect
- Names and spelling on viewed frames: Sonardyne SPRINT-Nav, Navis Engineering, Marine Technologies, Guidance Marine, Fugro, ADIPEC 2026, "With Guidance Marine at our stand" (rep identity is USER-SUPPLIED per verified-facts). No em dashes on viewed frames. "Our team" over-claim from v2 is gone. Partner captions describe equipment visible in the photos and do not claim supply.
- Safe zones: caption plates occupy y1285-1585, above the bottom 300 px. End card content ends about y1570. Logo is at y92-172, partly inside the top 150 px zone (minor, same as v2 D-03, accepted in design).
- No file names seen on tiles in the viewed frames (the v2 stand-video-wall file name was not seen this time; not exhaustively checked).
- Motion: no duplicated or stalled frames mid-clip. Average luma difference per frame is 15.9 (A) and 14.6 (B), peaks about 57 (A, 19.2 s) and 55 (B, 16.8 s) at the transition to the end card. That is a fast whip, a taste point.
- Faces under overlay text: only the title in the opening (D-04) and the caption plates, which cover lower halves of tiles but not the featured tile.
- Private information: badges and QR codes visible in tiles; not read or logged.

## Verdict
- File A (24.6 s): NOT READY. Fix D-01 (logo box, client item 1) and D-02 (true peak). Then D-04, D-05, D-07, D-09 recommended. Format, duration, codec, fast start and integrated loudness pass.
- File B (22.2 s): NOT READY. Fix D-01 and D-02. Then D-04, D-05, D-06, D-09 recommended. B satisfies item 3 better than A.
- A re-check of the re-rendered files is required; this report does not cover them.

## Candidate lessons for the Director (not saved by me)
1. After any re-master, re-run the loudness script; v3 regressed from -3.3 to 0.0 dBTP.
2. A logo "transparent background" needs the PNG alpha inspected (value 0 outside the glyphs), then a zoomed crop on dark and light tiles; a faint matte survived into the render.
3. fps=1/1.5 frame extraction can be offset by 0.75 s; verify sample times (pixel match or -ss) before quoting timestamps.
4. Fade logos and plate text with one opacity curve.
5. Hold a title in frame 0 or supply a cover image, since LinkedIn uses it as the thumbnail.
