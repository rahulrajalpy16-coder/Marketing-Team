# QA photowall v7 (independent check, four LinkedIn reels)

Files (all /tmp/work/adipec26/): A wall7_4x5_v1/..._v1_4x5_v7.mp4, B wall7_4x5_v2/..._v2_4x5_v7.mp4, C wall7_9x16_v1/..._v1_9x16_v7.mp4, D wall7_9x16_v2/..._v2_9x16_v7.mp4. Deliverables not edited. Frames in /tmp/work/qa_wall7/.

## Verification scope (what was really done)
- ffprobe, moov position (ffmpeg trace), ebur128 peak=true, silencedetect (-50 dB, 0.5 s), blackdetect plus freezedetect: all four files, whole timeline. Audio was MEASURED only, not listened to.
- A (4x5 v1): 20 frames at full 1080x1350, every 1.5 s (0 to 28.5 s), plus 6 extra full-res frames (12.6, 13.2, 17.4, 20.4, 22.2, 23.4 s) and two 0.3 s strips (beat 5 and beat 9, 270 px tiles).
- B (4x5 v2): 9 full-res frames (0.2, 3.3, 6.3, 9.3, 12.3, 15.6, 18.0, 20.4, 24.5 s), roughly every 3 s plus the three Visitors beats, plus 0.3 s strips of beats 7 and 8 (270 px tiles). Not every 3 s exactly.
- C (9x16 v1): one contact sheet every 1.5 s (216 px tiles, not full-res), plus 720 px frames (down-scaled from 1080x1920) at 0.2, 20.4, 23.1, 26.5 s. Frames 3.3 and 18.0 s were extracted but not viewed. Does NOT meet the "every 1.5 s at full resolution" method.
- D (9x16 v2): one contact sheet every 3 s (216 px tiles), plus 720 px frames at 18.0 and 20.4 s. Frames 0.2, 15.6, 24.5 s were extracted but not viewed.
- Not done: full playback, listening, cover frame, transitions frame by frame, LinkedIn UI overlay safe-zone testing.

## Technical (all four files)
| Item | A | B | C | D |
|---|---|---|---|---|
| Size | 1080x1350 PASS | 1080x1350 PASS | 1080x1920 PASS | 1080x1920 PASS |
| H.264 High, yuv420p | PASS | PASS | PASS | PASS |
| BT.709 primaries/trc/matrix, tv range | PASS | PASS | PASS | PASS |
| r_frame_rate / avg_frame_rate | 30/1, 30/1 PASS | 30/1, 30/1 PASS | 30/1, 30/1 PASS | 30/1, 30/1 PASS |
| AAC-LC 48 kHz stereo | PASS | PASS | PASS | PASS |
| moov first (offset 40) | PASS | PASS | PASS | PASS |
| Duration (video = audio) | 29.40 s PASS | 27.00 s PASS | 29.40 s PASS | 27.00 s PASS |
| Total bitrate | 9.10 Mb/s | 9.08 Mb/s | 12.13 Mb/s | 11.90 Mb/s |
| File size | 33.4 MB | 30.7 MB | 44.6 MB | 40.2 MB |
| Integrated loudness (ebur128) | -15.0 LUFS PASS | -15.0 PASS | -15.0 PASS | -15.0 PASS |
| True peak (peak=true, Peak: line) | -2.5 PASS | -1.8 PASS | -2.5 PASS | -1.8 PASS |
| Silence gaps (-50 dB, 0.5 s) | none | none | none | none |
| Black frames | none | none | none | none |
| Frozen frames | only inside closing card (static by design): A 26-26.5, 28-end; B 24-26.2; C 26.3-29; D 24-26.6 | | | |

Bitrates are inside LinkedIn reported organic limits (192 kbps to 30 Mbps). Those limits are third-party reported, not official (brain/platform-specs.md). Audio file sizes: all under 5 GB. SHA-256 prefixes: A 22730bba, B cda50f78, C 151902fe, D b5278752.

## Request 1: Visitors section extended
| Item | A | B | C | D |
|---|---|---|---|---|
| Three consecutive Visitors beats, sub lines "at our stand", "who stopped by", "at ADIPEC 2026" | PASS (07/09, 08/09, 09/09) | PASS (06/08, 07/08, 08/08) | PASS (07, 08, 09 seen in sheet; 08 and 09 read at 720 px) | PASS (06 to 08 seen in sheet; 07 and 08 read) |
| Beat 2 (who stopped by): two landscape photos stacked, both fully visible above panel | PASS (19.5, 20.4 s) | PASS (18.0 s, strip) | PASS (20.4 s) | PASS (18.0 s) |
| Beat 3 (at ADIPEC 2026): two stacked photos, both fully visible, not behind panel | FAIL | PASS (20.4 s, strip 19.8-21.3) | FAIL | PASS (20.4 s) |
| No faces cut off | PASS in beats seen | PASS | PASS | PASS |

## Defects
- V7-1 | MAJOR | A at about 22.5 to 23.9 s (09/09 beat); C at about 22.5 to 23.9 s (frame 23.1 s) | In the third Visitors beat the lower of the two stacked photos (two men looking at a phone) extends below the top of the caption panel. In A it starts at y=713 and the panel starts at y=1002, so roughly the lower third of the photo (legs, hands, phone) is hidden. In C the lower photo starts at y=785 (720 px frame) with the panel at 857, so most of it (about 70 percent of its height) is covered; only the top portion with faces remains. This breaks client request 1 ("both fully visible and not hidden behind the caption panel"). Faces stay visible. B and D do not show this because their pair sits above the panel. Corrective action (video editor): for the 09 beat in A and C, size and place the two stacked tiles as in B and D (top tile ends about y=548, bottom tile ends at or above the panel top, in 4:5 and the 9:16 equivalent), then re-render and re-check at 22.2, 23.0 and 23.6 s.
- V7-2 | MINOR | A, B, C, D, top-left logo, most of the timeline | The small "SINOR MARINE SERVICES" logo (blue on a light wall) sits on top of photo tiles and loses contrast over dark or busy tiles (A 4.5 s, 7.5 s, 10.5 s, 12.0 s: dark suits, badges, faces of non-focal tiles; B 12.3 s over the Navis logo). Readable at full res, weaker at phone size. It covers non-focal tiles only. Corrective action (video editor, optional): add a faint light plate or soft scrim behind it, or keep it on a fixed light strip.
- V7-3 | MINOR | A about 12.0 to 12.6 s and 13.9 to 14.4 s (beat 5), also seen in C 12 s and D sheet | The caption panel fades in late and out early, so for about 0.6 s at the start and 0.5 s at the end of the Marine Technologies beat the caption is a ghost (semi-transparent text over photos) or absent. Same pattern in other beats (A 4.5 s and 9.0 s show no panel). Panel is fully legible about 1.0 to 1.5 s per beat. Corrective action (video editor, optional): hold the panel for the whole beat or shorten the fades, and avoid ghost text over photos.
- V7-4 | MINOR | A at 1.5 s (opening to wall transition) | The opening title, logo and date linger as a ghost over the wall for a moment. Intentional-looking cross-fade; noted only.
- V7-5 | INFO | C and D process | Frame review of C and D was at lower resolution than requested. Fine detail (face crops, text at 1080x1920) in C and D outside the viewed frames was not inspected.

## Request 2: LinkedIn optimisation, 4:5 layout (A and B, full-res frames)
| Item | A | B |
|---|---|---|
| 1080x1350 main feed format | PASS | PASS |
| Opening: SMS logo above ADIPEC 2026 heading, date line "ABU DHABI . 2-5 NOVEMBER 2026", no overlaps, nothing outside frame (heading right edge about x=1040, margin about 40 px) | PASS | PASS |
| Caption panels inside frame (x 48 to 1032, y 1002 to 1302), logo and text readable | PASS | PASS |
| Panel covers focal-photo faces | PASS in beats 1 to 8 (focal faces above y=1002). Beat 9 lower photo: see V7-1 | PASS |
| Panel counter and title text accurate (no em dashes, names "Sonardyne SPRINT-Nav", "Navis Engineering", "Marine Technologies", "With Guidance Marine") | PASS | PASS |
| Top-left logo present and inside frame | PASS (contrast, see V7-2) | PASS |
| Closing card: all inside frame, no overlap, five logos with full names (Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine), text "technology partners for their support" | PASS | PASS |
| Closing card fills last 5.4 s (A from 24.0 s, B from 21.6 s) | PASS | PASS |

9x16 (C, D): opening and closing card checked at 720 px (C opening and end card; D sheet only): inside frame, five logos with full names. PASS within that scope. LinkedIn UI overlay zones not tested.

## Other observations
- Beat sequence: A has 9 beats (team, Conversations, Sonardyne, Navis, Marine Technologies, Guidance, 3 Visitors). B has 8 (team, Sonardyne, Navis, Marine Technologies, Guidance, 3 Visitors). Consistent with the brief.
- The "Guidance" photo with the woman is fully visible in A (15.0 s) and beats seen.
- Photos with incidental on-screen text (stand screens, "Hire No. 3345" label on the SPRINT-Nav) are real product labels; previously accepted by Rahul for file-name issue only. Not re-listed.

## Verdict
- B and D: no blocking defects within the checked scope.
- A and C: one MAJOR defect (V7-1) against client request 1. Not ready to send until fixed. Technical specs pass for all four.
- Audio measured only, not listened to. Visual verification is sampled, not full playback.

## Candidate lessons for the Director
- When the client asks for stacked photos "not behind the caption panel", test every beat's tile geometry against the panel rectangle in each aspect ratio. A layout fixed in one beat or one aspect ratio can still fail in another.
- Sample frames at the moment the panel is fully up (about 1 s after beat start), not only at beat midpoints.
