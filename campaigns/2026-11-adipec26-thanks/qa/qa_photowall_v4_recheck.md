# QA re-check: photo-wall v4 (v1 24.6 s, v2 22.2 s)

Reviewer: qa-reviewer (independent). Date 2026-11-07. Files not edited. Frames in /tmp/work/qa_wall4/.
Files: /tmp/work/adipec26/wall4_v1/adipec26-thanks_linkedin_photowall_v1_9x16_v4.mp4 (A), /tmp/work/adipec26/wall4_v2/adipec26-thanks_linkedin_photowall_v2_9x16_v4.mp4 (B).

## Scope (what I did)
- ffprobe, moov position (first 200 kB), ebur128 with true peak, astats (peak, flat factor), silencedetect (-50 dB, 0.3 s).
- Frames extracted with -ss (exact times), viewed: A at 0, 0.8, 3.75, 6.75, 7.5, 8.25, 9.0, 9.75, 11.25, 15.75, 18.75, 24 s (logo crops for 0.8, 3.75, 6.75, 11.25, 18.75); B at 0 (full), 3.75, 5.25, 11.25, 15.75, 21 s (logo crops for 3.75, 5.25, 11.25). 8 logo crops in total across both files, plus the dark veil.
- NOT done: real-time playback, blackdetect/freezedetect, per-frame review of captions between samples. AUDIO WAS MEASURED, NOT LISTENED TO. Logos not compared with official files.

## Results
| Item | Result |
|---|---|
| Specs, both files | PASS: H.264 yuv420p, 1080x1920, 30/1, AAC 48 kHz stereo, durations 24.600 / 22.200 s, moov at byte 36 (before mdat) |
| D-02 loudness | PASS: A -15.0 LUFS (LRA 0.9), B -15.0 LUFS (LRA 0.9) |
| D-02 true peak | PASS: ebur128 peak A -1.9 dBTP, B -2.2 dBTP (limit below -1). astats sample peak -2.17 dB (A), -2.17 dB (B); flat factor 0 on all channels. |
| Silence gaps | PASS: none detected in either file |
| D-01 rectangle/hard edge | PASS: no rectangle, box or hard edge behind the logo on any viewed frame (8 crops, light tiles, dark/blue tiles, dark veil). Scrim fades smoothly. |
| D-01 logo legibility | PARTIAL PASS (minor, new D-13). Logo is crisp and white on the dark veil (0.8 s, 0 s) and on light tiles at 24 s end card. On tile frames it is dark blue on a pale scrim and legibility depends on the tile: weak on dark clothing tiles (A 3.75 s, B 11.25 s: "SINOR MARINE SERVICES" blends into the dark jacket), and it overlaps tile text/logos (A 6.75 s over the Marine Technologies sign, A 18.75 s doubles with the "SINOR MARINE SERVICES" stand sign, B 5.25 s over a tile). Readable but not clean on roughly half the sampled tile frames. |
| First frame (t=0) | PASS: A and B both show "ADIPEC" and a faint "2026" plus the white logo at t=0 (viewed full-size). |
| A: group photo above SPRINT-Nav hero (7.0 to 9.5 s) | FAIL (minor, D-07 persists). At 8.25 and 9.0 s the tile above the hero is the group cropped at the waist (legs and shoes visible, no faces); at 7.5 s the full group tile is present only as a small tile at left, with faces tiny. Faces are not shown directly above the hero as requested. B (not requested) shows the group tile beside the hero at 5.25 s as before. |
| Hero caption "Sonardyne SPRINT-Nav" 03/07 with Sonardyne logo | PASS (A 8.25 s) |
| Partner captions with logos | PASS: Guidance Marine caption 06/07 (A 15.75 s) clean, logo on plate, no box |
| "Visitors" caption | PASS: A 07/07 at 18.75 s, B 06/06 at 15.75 s, five-person tile featured. D-08 (confirm they are visitors) stays an open question for Rahul. |
| End card | PASS: five logos with full names, "Thank you.", no boxes, bottom 300 px clear (A 24 s, B 21 s). |
| Em dashes on viewed frames | none seen |

## Defects
| ID | File | Time | Severity | Defect | Action | Owner |
|---|---|---|---|---|---|---|
| D-07 (open) | A | 7.5 to 9.75 s | minor | Tile above the SPRINT-Nav hero is legs/torso, no faces | Put the uncropped (or face-centred) group tile adjacent to the hero | video editor |
| D-13 (new) | A, B | tile frames, e.g. A 3.75, 6.75, 18.75 s; B 11.25 s | minor | Dark-blue logo over the pale scrim loses contrast on dark tiles and collides with tile signage | Optional: white logo with soft shadow on a slightly stronger scrim, or avoid placing busy/dark tiles under the logo | video editor |

Older minor items (D-04, D-05, D-06, D-09, D-10) were not re-checked in this pass and are unchanged in status.

## Verdict
- D-01 (box): resolved. D-02 (peak): resolved. First frame: resolved. A group-above-hero request: not resolved (minor).
- Both files meet the technical spec and loudness limits. No serious new defects. Release decision for the Director: A has one open minor item (D-07), B has none from this re-check apart from D-13 logo contrast on dark tiles.

## Candidate lessons
1. After a scrim replaces a box, check logo contrast per tile, not only the absence of the box.
2. Confirm a tile's crop by frame at the caption time; asking for "faces" needs the crop to be checked, not only the tile choice.
