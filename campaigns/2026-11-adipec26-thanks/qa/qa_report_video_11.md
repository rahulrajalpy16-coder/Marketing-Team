# QA report video 11 (photo mosaic design, 4:5 master and 9:16 alternative)

Reviewer: qa-reviewer, separate from the producer. Date 2026-11-06.
Files:
- 4x5: /tmp/work/adipec26/render11_4x5/adipec26-thanks_linkedin_mosaic_4x5_v11.mp4, 13,031,086 bytes, SHA-256 0fcf8ded...e44639 (full: 0fcf8deddf69af6510fc5e21ab64d6663b1c81e1ba1a742f33f57e5e59b44639)
- 9x16: /tmp/work/adipec26/render11_9x16/adipec26-thanks_linkedin_mosaic_9x16_v11.mp4, 17,786,648 bytes, SHA-256 19634587464a24d77bcb9c2fc42c6b91837f8e8a971b12936c41d40af561acbf
- Covers (opened, both): adipec26-thanks_cover_mosaic_4x5_v11.jpg and _9x16_v11.jpg, 1080x1350 and 1080x1920.

## True verification scope
- Scripted on the whole files: ffprobe, moov position (ffmpeg trace), volumedetect over all audio, blackdetect (d=0.1) and freezedetect (-60 dB, 0.5 s) on a 270 px decode, loudness_check.py (4x5 only).
- Viewed: 11 single frames per file (t = 0, 1.2, 3.9, 6.5, 9.2, 11.9, 14.6, 17.3, 20.0, 22.7, 27 s). They were extracted at FULL resolution and downscaled for viewing (4x5 to 720 px wide, 9x16 to 324 px wide in a 6-up sheet). So the 9x16 frames were seen at thumbnail size only; small text there (caption plates, end-card names) was readable but fine detail (badge text) was not judged at full size. No frame was inspected at 1080 px by eye.
- Transitions viewed: 12 frames at 80 ms steps for t = 2.1 to 3.06 s and 7.5 to 8.46 s (4x5 only).
- Motion: frame-difference and phase-correlation peak on 38 consecutive full-resolution frames, hero region and bottom tile strip, at t = 5.8 and 14.0 s (both files).
- NOT done: audio not listened to (track is silent); not played on a phone or LinkedIn; not watched in real time; the other transitions not viewed frame by frame; end-card logo aspect checked by code (single uniform scale, sc applied to both axes) plus visual, not by pixel measurement; safe-area figures are read from 720 px frames (about +/- 3 px), not pixel-scanned.
- Date check of brain files done; platform-specs LinkedIn row: ads spec only partly verified, organic limits UNVERIFIED (unchanged).

## 1. Technical (both files)
| Check | 4x5 | 9x16 |
|---|---|---|
| Container, duration | MP4, 30.300 s | MP4, 30.300 s (PASS vs about 30.3) |
| Video | H.264 High, yuv420p, 1080x1350, 25/1, 757 frames: PASS | same, 1080x1920: PASS |
| Audio | AAC LC 48 kHz stereo, decodes, mean and max -91.0 dB (silent, valid): PASS | same: PASS |
| moov first | moov at offset 40: PASS | moov at offset 40: PASS |
| blackdetect | none: PASS | none: PASS |
| freezedetect | none (the end card keeps drifting tiles): PASS | none: PASS |
| loudness_check.py | -inf LUFS, true peak -inf dBTP (silent, "within 1.5 LU of -14" reports CHECK, not applicable to silence); true peak PASS | NOT RUN |
| File name | follows pattern with "mosaic" tag: PASS | PASS |

## 2. First frame and first 5 s: PASS (both)
Frame at t = 0 (4x5 and 9x16): the 10-person team photo is already in frame, with the Sinor logo card, plate "The Sinor Marine team at ADIPEC 2026" and blue tiles; no black or blank start. The "Thank you." plate starts to whip in at about 2.4 s, is fully in by about 2.9 s and holds to about 5.0 s (frames 3.9 s). Within 5 s: PASS. Cover (frame at 1.45 s) shows the team photo with caption, legible at phone size.

## 3. Beats as rendered (computed from the build: start -0.3 s, hero 3.0 s, title 2.9 s, overlap 0.3 s; confirmed by viewing hold frames)
| # | Start (s) | Hold frame viewed | Caption / content as rendered | Order OK |
|---|---|---|---|---|
| 0 | -0.3 (visible from 0) | 1.2 | "The Sinor Marine team at ADIPEC 2026", s8_2, 10 people | yes |
| 1 | 2.4 | 3.9 | "Thank you." / "ADIPEC 2026 · ABU DHABI" / "2-5 November 2026" + logo card | yes |
| 2 | 5.0 | 6.5 | "Conversations at our stand", s7_1, UAE visitors | yes |
| 3 | 7.7 | 9.2 | "Visitors at our stand", s3_1, ADNOC coveralls | yes |
| 4 | 10.4 | 11.9 | "NAVIS console", IMG_4413 | yes |
| 5 | 13.1 | 14.6 | "Discussions at the Sonardyne display", IMG_4464 | yes |
| 6 | 15.8 | 17.3 | "Marine Technologies on the stand", IMG_4188 | yes |
| 7 | 18.5 | 20.0 | "Guidance Marine at our stand", a07555b5 | yes |
| 8 | 21.2 | 22.7 | "The team at our stand", s2_2, four men | yes |
| 9 | 23.9 | 27.0 | End card to 30.3 s | yes |
Order and text match the brief. Caption text has no typos. PASS in both files (9x16 viewed at thumbnail scale).

## 4. Text safety: PASS
- 4x5 (SAFE 1200): lowest caption plate bottom about 1086 (Guidance Marine beat; others about 1008 to 1060); end card bottom about 1162 (keyline about 1174); title plate about 1120 at most (title text content ends near 800). All above 1200. Margin of the end card is about 26 px: tight but inside.
- 9x16 (SAFE 1620): hero is 0.42 H so captions end near 1050 to 1120; end card bottom about 1565 (keyline about 1577). Above 1620.
- Nothing readable is cut by the frame edge except the intentional white background words (THANK / YOU / 2026 / ADIPEC fragments) and tiles. The end card in 4x5 is scaled 0.86 of the frame and touches the top edge (keyline cut at top, y about 0); the logo card inside starts about 75 px down, so no content is lost. Cosmetic (V11-5).
- Heads: no head cut by the keyline or plate in any of the 9 hero frames; plates sit below the photo (y = photo bottom + 4) so they never cover faces. NAVIS portrait photo is shown whole (logo not cropped). Hero zoom 1.065 at the end of a beat crops about 3 percent per side; viewed frames show no clipped face.
- In 4x5 the NAVIS beat shows a narrow portrait hero (about 40 percent of frame width) with large empty background: acceptable, slightly weak.

## 5. Motion quality
| Window | Region | Mean abs diff | Std | CV | Zero steps | PC peak min |
|---|---|---|---|---|---|---|
| 4x5 5.8 s (beat 2 hold) | hero | 1.27 | 0.02 | 0.02 | 0 | 0.82 |
| 4x5 5.8 s | bottom tiles | 1.61 | 0.08 | 0.05 | 0 | 0.62 |
| 4x5 14.0 s (beat 5 hold) | hero | 1.30 | 0.05 | 0.03 | 0 | 0.78 |
| 4x5 14.0 s | bottom strip (few tiles) | 0.10 | 0.10 | 1.06 | 0 | 0.83 |
| 9x16 5.8 s | hero / tiles | 0.78 / 1.50 | 0.03 / 0.06 | 0.04 | 0 | 0.77 / 0.58 |
| 9x16 14.0 s | hero / tiles | 0.74 / 1.65 | 0.13 / 0.05 | 0.18 / 0.03 | 0 | 0.69 / 0.64 |
Steady, no jumps, no frozen steps in the hold windows. (Higher CV of 1.06 at 4x5 14.0 s bottom strip is a mostly empty strip with a tile edge passing; mean diff 0.1 is tiny.) A first attempt at 6.2 s was discarded because it overlapped the beat 2 exit at 7.58 s (spike 8 to 12): that is the designed whip exit, not jitter. No shimmer, seam or flicker seen in the frames viewed; sub-pixel sampling is in the build, not independently tested beyond these numbers.
Transitions (4x5, viewed): at 2.4 to 2.5 s the team hero is semi-transparent over the title plate for about 2 frames and the title text is cut at the right edge for about 0.2 s while it whips in; caption text and "Thank you." overlap for about 0.1 to 0.2 s. At 7.9 s the same for the two heroes. In each case the unreadable window is under 0.5 s. PASS. Other transitions (4 to 5, 5 to 6, etc.) not viewed in detail; same code path.

## 6. Tile content (background blue duotone tiles)
Duotone, partly hidden, drifting, and the tiles are mostly small. Things a careful company might still object to:
- V11-1 (Medium): clear face crops of identifiable non-Sinor people. Examples: the older white-haired man (Navis or Sonardyne side) as a large tile at the bottom of the "Conversations" beat (6.5 s), the bald man and others at 14.6 s, the Shipworkz visitor tiles, the woman at 11.9 s and 22.7 s. The code intends wide crops, but several tiles show faces about 150 to 250 px tall. Not private data and they were photographed at the stand, but their consent was not recorded; V6-5 consent items are still with Rahul.
- Other companies' branding in tiles and in the hero backgrounds: "shipworkz / ipworkz" sign (hero 0 and 8, tiles), "Nagamori Machinery Co.,Ltd." (hero 7), "ONE-MICROF / HP-LUB II", "Shipworkz" in team photo background. They are in the photos themselves, not added; low risk but not Rahul-approved specifically. The ipworkz sign sits behind the four men in the "The team at our stand" hero.
- Badge text: lanyard badges and QR codes appear in the heroes and tiles; no name was legible at the sizes viewed (not checked at full 1080 resolution).
- The Guidance Marine hero shows a TV with a coordinate readout (about 46.76, -92.10) that is small but partly readable at full size. Harmless demo data, not in Rahul's approvals list.
- SPRINT-Nav "Hire No. 3345" sticker is readable in a tile at 9.2 s (tile only, tiny). Low.
- Panel figures (15+ years, 100+ projects, 40+ countries) approved by Rahul and do appear in photos. File name photo no longer used as a hero (cf677e0a is a tile only; the file name on its TV is not legible in the tiles I saw).

## 7. End card: PASS with notes
Viewed at 4x5 (720 px) and 9x16 (thumbnail). Headline "Thank you", line "To every client and visitor who stopped by our stand.", "And to our technology partners for their support:". Five logo tiles in order Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine, names under each spelled exactly: Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine. Logos scaled with one uniform factor (min of width and height fit) so no distortion; source aspects: Sonardyne 5.319, Guidance Marine 7.792, Fugro 2.231, Navis 3.564, MT 2.159; visually undistorted. Partner wording follows Rahul's rule ("support", no supply claim). Notes: Fugro mark still smaller than the others (inherited V8-2); Guidance Marine logo thin but readable at 4x5, small in 9x16 (about 376 px tile at 1080 wide).

## 8. Claims versus Rahul's statements
Rahul (verified-facts): chose s8_2 as the "full Sinor Marine team photo"; the woman in a07555b5 represents Guidance Marine; partner list; logos; panel figures; the file name; partners supported Sinor's stand.
- "The Sinor Marine team at ADIPEC 2026" (s8_2): supported by Rahul's own words (USER-SUPPLIED). PASS. Fine to use.
- "Guidance Marine at our stand": only the woman is identified. The man is not; the caption can read as both. Low over-claim (V11-3, carried from V10-3).
- "The team at our stand" (s2_2, four men): UNSUPPORTED by Rahul's statements. Manifest says "Four Sinor team members", but no line in verified-facts identifies these four as Sinor staff. It is also a repeat of the "team" idea after the full-team beat. Needs Rahul's confirmation or a neutral caption (V11-2, Medium).
- "Visitors at our stand" (s3_1, ADNOC coveralls plus a man in kandura): the photo supports "people at the stand" but "visitors" is an assumption; ADNOC identity is from the coveralls only. Low.
- "Conversations at our stand" (s7_1): a Sinor colleague with two men in traditional dress; "UAE visitors" is the manifest's inference, caption does not say it. Fine.
- "Discussions at the Sonardyne display": the photo shows a SPRINT-Nav unit and a meeting; the word "display" is loose (unit, not a display), and "Discussions at the Sonardyne display" suggests a Sonardyne-hosted discussion. Low to Medium, a plain "Sonardyne SPRINT-Nav on the stand" (v10 wording) is safer (V11-4).
- "Marine Technologies on the stand": the photo shows an MT screen and two men; one is in a "Sinor Marine Technologies" area. The two men are not identified as Marine Technologies people; caption refers to the brand. OK.
- "NAVIS console": OK, branded console visible. Note the end card writes Navis Engineering in full; caption says NAVIS. Matches Rahul's confirmed pairing.
- Title and end-card lines: "To every client and visitor who stopped by our stand." is a thank-you, not a claim. OK.
- Em dash: 0 in build_video_mosaic.py; none seen in any rendered text.

## 9. Honest comparison with v10 and the reference style
- Reference match (judged only from the producer's description in the build docstring and brief; I did not see the reference video): the elements named (grey vignette, white keyline hero, blue duotone parallax tiles, big white type, dark squares, thin lines, whip entries) are all present and visible in the frames. It plausibly follows the style. Whether Rahul will agree is not testable by me.
- Versus v10 slideshow: more dynamic and more "designed"; it keeps the same facts and the same order, with a better first frame (full team photo already in frame). It is also busier: in 9x16 the hero is only about 42 percent of the height, tiles are dense, and several tiles show recognisable faces. v10 was cleaner, with full-frame photos and a safer caption set; v11 adds new third-party face and branding exposure (V11-1). Verdict: better for visual interest and match to Rahul's request, slightly worse for caution and for photo size, especially 9x16. Overall "better, with caveats". This is a reviewer's judgement, not a measured result.

## 10. Manifest: PASS
Hero photos: s8_2 selected, s7_1 selected, s3_1 selected, IMG_4413 selected, IMG_4464 selected, IMG_4188 selected, a07555b5 selected, s2_2 selected. All eight are `selected` in sources/manifest.csv (read in full). No near-duplicate or excluded photo is a hero. Note: manifest lines for s2_2 and s3_1 mark them "selected" with notes on content, not on person identity.

## 11. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| V11-1 | Medium | Background tiles, many beats (e.g. 6.5 s, 11.9 s, 14.6 s, 22.7 s) | Tiles with clear faces of identifiable non-Sinor people and other companies' signage; no consent record. Options: darken or blur tiles with faces, enlarge crop, or get Rahul's say-so. Not a legal ruling | Video producer (fix), Director (ask Rahul) |
| V11-2 | Medium | Beat 8, 21.2 s, "The team at our stand" | Not supported by Rahul's statements that these four are Sinor staff | Director (confirm), copywriter |
| V11-3 | Low | Beat 7, 18.5 s | "Guidance Marine at our stand": only the woman is identified; man unidentified. Consider "Guidance Marine representative at our stand" | Copywriter, Director |
| V11-4 | Low | Beat 5, 13.1 s | "Discussions at the Sonardyne display": loose wording, may imply a Sonardyne-hosted discussion; the photo shows the SPRINT-Nav unit | Copywriter |
| V11-5 | Low | 4x5 end card | Card is 0.86 of frame height and its keyline touches the top edge; bottom about 26 px above SAFE. Cosmetic | Video producer (optional) |
| V11-6 | Low | 9x16 all beats | Hero only about 42 percent of height, dense tiles; the team photo is small. Verified at thumbnail scale only | Video producer (optional) |
| V11-7 | Info | Whole video | 4x5 title plate has empty lower third; Fugro mark smaller (V8-2); not played on phone, audio not heard; 9x16 viewed only at thumbnail size; V6-5 consent items still with Rahul | Director |
No High defects. No spec failure.

## 12. Verdict
- 4x5 master: PASS on spec, fast start, black and freeze, first frame, beat order, safe area, motion samples, end card, manifest. Open: V11-1 and V11-2 (Medium) for the Director and Rahul before publishing.
- 9x16 alternative: PASS on the same checks (with the thumbnail-scale limitation). Same open items, plus V11-6 (Low).
Verdicts rest on measurements and sampled frames, not full playback. Approval of the draft is not approval to publish.

## Candidate lessons for the Director
- Background tiles that show faces need a stated rule (blur, or only Sinor staff) and a consent check; a duotone does not make a face unrecognisable at tile sizes above about 150 px.
- A caption that names a group ("The team") needs a matching USER-SUPPLIED line in verified-facts; the manifest's content notes are not identity confirmation.
- When a motion window overlaps an exit, the frame-difference spike is design, not jitter: compute hold windows from the beat list before measuring.
- Full-resolution frame review of the 9x16 was skipped for memory reasons; if wanted, run a second pass with crops at 1080 px.
