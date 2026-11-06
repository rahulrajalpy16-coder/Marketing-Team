# QA report: three video designs (mosaic v11 4:5 and 9:16, kinetic v12 4:5, promo v12 4:5)

Reviewer: qa-reviewer, separate from the producer. Date 2026-11-06. Files (all under /tmp/work/adipec26):
- mosaic 4:5 render11_4x5/adipec26-thanks_linkedin_mosaic_4x5_v11.mp4, 13,039,097 bytes, SHA-256 7edea3f32a23c5e9...
- mosaic 9:16 render11_9x16/adipec26-thanks_linkedin_mosaic_9x16_v11.mp4, 17,821,943 bytes, SHA-256 8ed8da7da5eb8596...
- kinetic 4:5 render12_kinetic/adipec26-thanks_linkedin_kinetic_4x5_v12.mp4, 5,325,720 bytes, SHA-256 418a347946df8c90...
- promo 4:5 render12_promo/adipec26-thanks_linkedin_promo_4x5_v12.mp4, 15,661,463 bytes, SHA-256 820d92b1d70966a2...
(The mosaic files were re-rendered after the caption fixes: sizes differ from qa_report_video_11.md. Only the first 16 hex digits of each hash were printed.)

## True verification scope
- Scripted on whole files: ffprobe, moov position (ffmpeg trace), volumedetect on all audio, blackdetect (d=0.1) and freezedetect (-60 dB, 0.5 s) on a 270 px decode, loudness_check.py on the kinetic file only (the other three have the same silent track, volumedetect only).
- Frames viewed at FULL resolution (1080 px wide as delivered by the viewer, one frame per image):
  - kinetic 4:5: 11 frames, t = 0, 1.4, 3.9, 6.75, 9.7, 12.65, 15.6, 18.55, 21.5, 24.45, 28 s = frame 1, the title, all 8 hero beats, end card.
  - promo 4:5: the same 11 times.
  - mosaic 4:5: t = 0, 14.6, 20.0, 22.7, 27 s (Sonardyne, Guidance Marine, Together beats, end card). Mosaic 9:16: the same 5 times. Not viewed this round in either mosaic file: the title beat, "Conversations", "Visitors", "NAVIS", "Marine Technologies" beats (unchanged captions; viewed only at lower scale in qa_report_video_11.md).
  - Transition frames: kinetic and promo at 7.80, 7.88, 7.96, 8.04, 8.12 s (270 px wide); 4 kinetic frames of the letter-by-letter word build (crop).
- Motion: frame difference and phase correlation on 38 consecutive full-resolution gray frames, per window and region, listed in section 5. Windows were frame-aligned (an earlier probe at t = 6.3 s gave one spurious zero-diff step caused by my seek landing between frames, not a defect in the file; re-measured at 6.2 s).
- Contrast: WCAG ratios computed by script on a few text boxes in promo frames; kinetic end card computed too.
- Logo aspect: measured by pixel bounding box on the kinetic end card (section 6) against the logo files in assets/brand/partners.
- NOT done: audio not listened to (silent track, -91 dB); not played on a phone or LinkedIn; no real-time playback; beats not viewed frame by frame except the transitions listed; not every transition inspected (all 9 share one code path per style); cover JPGs not opened; 9:16 only exists for the mosaic design, kinetic and promo have no 9:16.
- Style fidelity is a judgement of mine from the three reference contact sheets, not a measured result.

## 1. Technical
| Check | mosaic 4:5 | mosaic 9:16 | kinetic 4:5 | promo 4:5 |
|---|---|---|---|---|
| Video | H.264 High yuv420p 1080x1350, 25/1, 757 frames | 1080x1920, 25/1, 757 frames | 1080x1350, 25/1, 792 frames | 1080x1350, 25/1, 792 frames |
| Audio | AAC LC 48 kHz stereo, mean/max -91.0 dB (silent, valid) | same | same | same |
| Duration | 30.300 s (expected about 30.3) | 30.300 s | 31.700 s (expected about 31.7) | 31.700 s |
| moov first | moov at offset 40 | offset 40 | offset 40 | offset 40 |
| blackdetect | none | none | none | none |
| freezedetect | none | none | 3.24 to 4.88 s (the "THANK YOU." title hold, static by design) and 25.92 s to end (end card, static by design) | none (wall keeps scrolling 1 px per frame) |
| loudness_check.py | not run | not run | -inf LUFS, true peak -inf dBTP: true-peak PASS; "within 1.5 LU of -14" reports CHECK, not applicable to silence | not run |
| Verdict | PASS | PASS | PASS | PASS |
LinkedIn spec row in platform-specs is only partly verified (ads page); 4:5 and 9:16 at 1080 px and H.264 are consistent with it. Frame rate 25 is under the 30 fps limit quoted for ads.

## 2. First frame and thank-you within 5 s
- Kinetic: frame 1 shows the "OUR TEAM" giant word, the 10-person photo card and caption (real content). The "THANK YOU." title starts at 2.35 s and is fully built by about 3.4 s. PASS.
- Promo: frame 1 shows the Sinor logo card, the framed team photo, TEAM chip, caption and info box over the wall. Title starts at 2.35 s, fully in at about 2.9 s. PASS.
- Mosaic 4:5 and 9:16: frame 1 shows the team photo, logo card and caption plate over tiles; the "Thank you." plate comes in at 2.4 s. PASS. In both mosaic frame 1s the small meta line "ADIPEC 2026 / ABU DHABI / 02-05 N..." is cut by a tile at the right (cosmetic, tile drifts away later).

## 3. Beats and captions as rendered (all four files: order and captions identical)
1 "The Sinor Marine team at ADIPEC 2026" (s8_2) | 2 "Thank you." title | 3 "Conversations at our stand" | 4 "Visitors at our stand" | 5 "NAVIS console" | 6 "Sonardyne SPRINT-Nav on the stand" | 7 "Marine Technologies on the stand" | 8 "With Guidance Marine at our stand" | 9 "Together at our stand" | 10 end card.
- Kinetic: all 10 viewed at full resolution, text matches, no typos. Words above the cards: OUR TEAM, (title), CONVERSATIONS, VISITORS, TECHNOLOGY, DISCUSSIONS, PARTNERS, WELCOME, TEAMWORK.
- Promo: all 10 viewed at full resolution, text matches. Chips: TEAM, VISITORS, VISITORS, TECHNOLOGY, TECHNOLOGY, PARTNERS, PARTNERS, TEAM; counter 01/08 to 08/08 correct.
- Mosaic: the three changed captions (Sonardyne, With Guidance Marine, Together) verified in both 4:5 and 9:16 at full resolution: all three read exactly as specified, in both files. Beats 3, 4, 5, 7 not re-viewed (unchanged since v11 QA).
- Caption wraps: promo captions for beats 6, 7, 8 wrap to two lines with a single orphan word "stand"; kinetic beat 1 wraps with "2026" alone on line 2 (see VS-5).
PASS for order and text in all four.

## 4. Text safety (SAFE 1200 for 4:5, 1620 for 9:16), read from 1080 px frames (about +/- 5 px)
| File | Lowest text row | Margin |
|---|---|---|
| kinetic 4:5 | caption 2nd line on beat 1 ends about 1145; end card "Guidance Marine" label about 1165 | 35 to 55 px |
| promo 4:5 | info box bottom 1042 (1-line captions 973); end card label about 1155 | 45 to 160 px |
| mosaic 4:5 | Guidance plate bottom about 1087; end-card label about 1012 (panel bottom 1175) | 25 to 190 px |
| mosaic 9:16 | Guidance plate bottom about 1375; end-card label about 1122 (panel bottom about 1565) | 55 to 500 px |
- No text over faces in any hero frame (captions sit below photos). Nothing readable is cut by the frame edge except the intentional big white words in mosaic and the title cut at the frame edge during whips.
- Promo: caption, chip and info box sit on the dark wall, so text overlaps wall tiles and, in places, faces in the tiles. Contrast (script, WCAG): white captions median 9.5 to 12.1 and 90th percentile 5.8 to 7.9 against the surrounding wall; aqua title date line median 6.9, 90th percentile 3.6; the lightest spots (99th percentile) fall to 2.0 to 2.7 where a bright tile crosses the text ("SPRINT-Nav" label under the beat 6 caption, date line over a white tile). Readable at phone width in the frames viewed; small info-box text (24 px) is the weakest.
- Kinetic: navy on cream/sky 12.8:1 on the end card, white on blue and cream on navy for the other palettes; all readable.
- Small text sizes: promo info box line 24 px and mosaic plate top line about 20 px are small on a phone (about 2 percent of frame width).
PASS on safe area for all four; Low readability note for the small promo and mosaic sub-lines.

## 5. Motion quality (38 frames each, full resolution, gray)
| File | Window and region | Mean abs diff | Std | CV | Zero steps | PC peak min | Result |
|---|---|---|---|---|---|---|---|
| kinetic | 6.2 s card (beat 3 hold) | 1.29 | 0.02 | 0.02 | 0 | 0.77 | smooth zoom/tilt, no jump |
| kinetic | 12.2 s card (beat 5 hold) | 0.34 | 0.01 | 0.03 | 0 | 0.89 | smooth |
| kinetic | 20.6 s card (beat 8 hold) | 1.37 | 0.02 | 0.01 | 0 | 0.84 | smooth |
| promo | 6.2 s hero | 1.11 | 0.02 | 0.02 | 0 | 0.80 | smooth zoom |
| promo | 6.2 s wall | 1.67 | 0.03 | 0.02 | 0 | 0.88 | PC shift dy = +1.00 px every step, std 0.00: perfectly uniform scroll |
| promo | 15.0 s hero | 1.04 | 0.05 | 0.05 | 0 | 0.81 | smooth |
| promo | 15.0 s wall | 1.82 | 0.03 | 0.02 | 0 | 0.89 | uniform 1 px/frame |
| mosaic 4:5 | 5.84 s hero / tiles | 1.37 / 1.60 | 0.02 / 0.08 | 0.02 / 0.05 | 0 | 0.74 / 0.62 | smooth |
| mosaic 4:5 | 14.0 s hero / tiles | 1.32 / 0.36 | 0.06 / 0.04 | 0.04 / 0.11 | 0 | 0.76 / 0.82 | smooth |
| mosaic 9:16 | 5.84 s hero / tiles | 1.36 / 1.47 | 0.02 / 0.06 | 0.02 / 0.04 | 0 | 0.75 / 0.59 | smooth |
| mosaic 9:16 | 14.0 s hero / tiles | 1.32 / 0.67 | 0.06 / 0.07 | 0.04 / 0.10 | 0 | 0.76 / 0.73 | smooth |
A first kinetic window at 20.0 s gave CV 1.36 and max 21.5; it overlapped the end of the wipe and the card entry (designed motion), so it is discarded and replaced by 20.6 s. No jitter, no flicker, no frozen steps in any hold window.

Transitions (270 px frames, 8 ms-scale series 7.72 to 8.12 s):
- Kinetic wipe: a flat colour block slides across (step diffs 5 to 50, one solid-colour frame around 7.96 s, about 0.12 s), then the next beat appears with the card fading in. Old caption is cut by the wipe for about 3 frames. Text unreadable under the wipe about 0.2 s. PASS (under 0.5 s). Letter-by-letter words: letters rise and fade in sequentially (checked at 5.28 and 5.40 s), no popping, no overlap of unreadable text. But see VS-3 (letter spacing).
- Promo slide: 10 frames (about 0.4 s) of horizontal slide with blur; step diffs 24 to 35, uniform. The blur is a 5-tap shifted average, so at peak speed the frame shows discrete ghost copies and wrap-around edge streaks rather than smooth blur (frames 7.96 and 8.04). Text unreadable about 0.4 s (under 0.5 s). Reads as "fast slide", slightly crude. PASS with Low note VS-4.
- Mosaic: unchanged from v11 QA (2 frame overlap of heroes and a title cut at the right edge, under 0.5 s); not re-measured in transitions this round.

## 6. End cards
Viewed at full resolution in all four files. Headline "Thank you", "To every client and visitor who stopped by our stand.", "And to our technology partners for their support:" then five tiles in the order Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine, names under each in exact spelling (all four files). Wording follows Rahul's rule (support, no supply claim).
- Logo aspect, measured on the kinetic card (rendered bounding box vs file bbox): Sonardyne 5.26 vs 5.319; Fugro 2.23 vs 2.231; Navis 3.50 vs 3.564; MT 2.19 vs 2.159; Guidance 7.61 vs 7.792. All within about 2 percent (threshold-based bbox, anti-aliasing), so no distortion. The same partner_tile code is used in promo and mosaic; visually identical proportions in those frames (not measured separately).
- Kinetic: navy/blue text on cream, 12.8:1 and around 8:1 for the blue line; a 1 px blue line runs across the very top edge (code line 283, VS-5). Fugro mark is the smaller of the five (inherited).
- Promo: white and aqua text on the dark navy overlay (aqua 7:1 median); faint tile faces show through the overlay (opacity 170/255) behind the text, not distracting. Guidance Marine logo is thin but readable.
- Mosaic 4:5: panel from y 40 to 1175, readable. Mosaic 9:16: the panel content ends at about 1125 while the panel runs to about 1565, so the lower 40 percent of the card is empty navy (VS-6).
PASS in all four.

## 7. Style fidelity (honest assessment, judged from the reference contact sheets)
- Mosaic vs reference 1 ("photo mosaic"): good. Light grey vignette, thin keyline hero, blue duotone tiles drifting, big white type behind, small dark squares, thin hairlines and tick marks all appear. Gaps: the reference has rotated 3D-ish tiles, flares and a much denser overlapping of tiles; here tiles are flat rectangles and the hero is dominant. Closest match of the three.
- Kinetic vs reference 2 ("dynamic colorful"): partial. Matches: colour-block backgrounds that change per beat, giant geometric words built letter by letter, white-bordered tilted photo cards with soft shadow, colour wipes. Gaps: the reference is full of saturated, contrasting colours (magenta, teal, orange), full-bleed photos, words that mask over the photos, paired cards (small + tall). The Sinor version uses only brand navy, blue, sky and cream, one card at a time, and large empty areas at the bottom (about 200 px of empty colour below each caption). It reads as a calm brand-safe cousin of the reference, not an equivalent. Different from the other two designs: yes, clearly (light flat colours, no tiles).
- Promo vs reference 3 ("corporate event promo"): good. Dark duotone photo wall, framed hero, big white type, aqua chips, outlined info box, counter, fast slides with blur and the aqua "YOU" block all echo the reference. Gaps: reference wall is a clean grid of portraits that is revealed in the title and uses purple/teal; blur is cruder (VS-4). Distinct from the mosaic: yes in layout (dark, scrolling wall, bottom-left text block, slides) though both use blue duotone tiles and white type, so the promo and mosaic share the "blue tiles behind photo" feel at a glance.

## 8. Claims versus Rahul's statements
Rahul approved (per the task brief; see VS-9): s8_2 as the full team photo, partners, logos, the woman in a07555b5 as Guidance Marine.
- "The Sinor Marine team at ADIPEC 2026" with OUR TEAM / TEAM: supported by Rahul's approval of s8_2. OK.
- "Sonardyne SPRINT-Nav on the stand", "NAVIS console", "Marine Technologies on the stand": supported by photo content and verified-facts (units and branded displays visible). The new SPRINT-Nav wording fixes V11-4. OK.
- "With Guidance Marine at our stand": supported for the woman (Rahul); wording "With Guidance Marine" is acceptable and the earlier ambiguity (V11-3) is reduced. WELCOME and PARTNERS chip with it: fine (partner status confirmed by Rahul).
- "Together at our stand" caption: neutral and safe. But the decorative TEAMWORK (kinetic) and TEAM chip (promo) on the same photo claim these four are Sinor's team. Nothing in verified-facts identifies them. In the frame the man on the left wears a black lanyard, a different badge and a round company logo on his shirt, and stands in front of a Shipworkz banner, while the other three wear the blue lanyards of the other attendees; he may not be a Sinor team member. The manifest note "Four Sinor team members" is not Rahul's statement. Mosaic has no such word, so it is unaffected (VS-1).
- VISITORS word and chip on s3_1 (ADNOC coveralls plus man in kandura) and on s7_1 (two UAE men with a Sinor colleague): "visitors" is an inference (inherited, Low). CONVERSATIONS, DISCUSSIONS, TECHNOLOGY, WELCOME: descriptive, no claim.
- "PARTNERS" chip/word on the Marine Technologies photo: Rahul confirmed MT as a partner that supported the stand. The two men are not identified. The photo also shows a "SINOR MARINE TECHNOLOGIES" nameplate (SMT), a Sinor entity per Rahul's stand files, next to the MT-branded screen; a viewer could read the pairing as MT = SMT. Low.
- End card and title lines: thank-you wording only, no claims.
- Dates "2-5 November 2026", ADIPEC, Abu Dhabi: VERIFIED (verified-facts row 12).
- Panel figures (15+, 100+, 40+) are not on screen as text by the build; they remain in photos.
- Em dashes: 0 in build_video_styles.py and build_video_mosaic.py (grep for the em dash and en dash characters, both 0); none seen in any rendered frame.

## 9. Visible things a careful company might object to (photos and promo wall tiles)
- Promo wall (270 px tiles, duotone, darkened 38 percent plus vignette): clear faces of non-Sinor people (examples at 6.75 s and 9.7 s: the smiling man and the woman in the lower rows; the white-haired and bald men at 12.65 s; the man on the right at 28 s). Faces are about 70 to 110 px tall, recognisable though dark. Other brands readable in tiles: "SPRINT-Nav", Sonardyne, "MT Two Way Sailing Autopilot", "SINOR MARINE SERVICES". Partly hidden by the framed hero but about half the wall is visible in every beat. Consent not recorded (Rahul's V6-5 items open).
- Mosaic tiles: larger and brighter than the promo wall; faces up to about 250 px tall in 9:16 (smiling woman tile at 14.6 s, bald man at 22.7 s, smiling man at 27 s in 4:5 end-card gap). Same as VS-2.
- Kinetic: no tiles, so no extra faces beyond the hero photos. Hero photos show other exhibitors' signage unduotoned: "ipworkz Technical Solutions / Leading Marine Engineering Service Provider" banner (beat 9), "ONE-MICROF / HP-LUB II" and a partly readable company name strip (beat 4), "Nagamori Machinery Co.,Ltd." and a person seated at the neighbouring stand (beat 8), "shipworkz" (beat 1). These are in the photos themselves and are the same in the mosaic.
- Beat 8 photo: a TV shows a coordinate readout (46.76, -92.10), readable, harmless demo data.
- Badge text and QR codes: lanyard badges and QR codes appear in heroes; no name was legible at the 1080 px frames viewed.
- Duotone does not hide identity at these tile sizes.

## 10. Manifest and records
- Hero photos selected in sources/manifest.csv (read in full): s8_2, s7_1, s3_1, IMG_4413, IMG_4464, IMG_4188, a07555b5, s2_2: all `selected`. PASS.
- Stale manifest notes: s2_2 reason still says Hero beat "The team at our stand" (caption now "Together at our stand"); a07555b5 says "hero beat in the mosaic video (v11)". Low, Director.
- Record gap: verified-facts row 27 still says the photo 0f44943b is Rahul's "full Sinor Marine team photo" ("he may mean another"), while the videos use s8_2, which the brief for this QA states Rahul approved. I could not find a USER-SUPPLIED line for s8_2 in brain/ or the campaign brief (VS-9).

## 11. Defects
| ID | Severity | Location | Issue | Owner |
|---|---|---|---|---|
| VS-1 | Medium | Kinetic and promo, beat 9 (22.75 to 25.7 s) | Decorative "TEAMWORK" (kinetic) and chip "TEAM" (promo) over s2_2 present these four men as Sinor's team; not supported by any Rahul statement; left man wears a different lanyard and badge, in front of a Shipworkz banner. Fix: change to a neutral word ("AT OUR STAND" or "TOGETHER") or get Rahul to confirm all four are Sinor staff | Director (ask Rahul), video producer (swap word) |
| VS-2 | Medium | Promo wall (all beats) and mosaic tiles (all beats) | Recognisable faces of non-Sinor people and other brands in tiles, no consent record. Kinetic is free of this. Options: blur/darken faces, crop tiles to equipment and stand only, or Rahul's explicit say-so. Not a legal ruling | Video producer (fix), Director (ask Rahul) |
| VS-3 | Low | Kinetic, "PARTNERS" (beat 7, about 16.9 s on) and "CONVERSATIONS" (beat 3) | Per-letter drawing ignores pair kerning: the A overlaps the R in PARTNERS, T and I touch in CONVERSATIONS. Visible for the whole beat | Video producer |
| VS-4 | Low | Promo, all 9 slides (about 0.4 s each) | Motion blur is a 5-tap shifted average: stepped ghost copies and wrap-around edge streaks instead of smooth blur; text unreadable about 0.4 s (under 0.5 s) | Video producer (optional) |
| VS-5 | Low | Kinetic and promo captions | Orphan words: "2026" alone (kinetic beat 1), "stand" alone (promo beats 6, 7, 8). Kinetic end card has a 1 px blue line across the very top edge; about 200 px empty colour under each kinetic caption | Video producer (optional) |
| VS-6 | Low | Mosaic 9:16 end card (23.9 s on); both mosaics at 0 s | 9:16 end-card panel content ends near y 1125 of a 1565 panel, lower 40 percent empty; meta line "ADIPEC 2026 / ABU DHABI / 02-05 N" cut by a tile at 0 s | Video producer (optional) |
| VS-7 | Low | Kinetic and promo, beats 3, 4, 7 | "VISITORS" word/chip is an inference (visitors vs partner staff, same as V11); "PARTNERS" next to a visible "SINOR MARINE TECHNOLOGIES" nameplate may blur MT with SMT | Copywriter, Director |
| VS-8 | Low | Promo info box and mosaic plate sub-line | 24 px and about 20 px sub-lines are small at phone width; bright tiles reduce local contrast to about 2:1 in spots | Video producer (optional) |
| VS-9 | Info | brain/verified-facts.md row 27; manifest notes | s8_2 approval not recorded (row 27 names 0f44943b); manifest notes for s2_2 and a07555b5 stale | Director |
No High defects and no spec failures.

## 12. Verdicts
- Mosaic 4:5 (v11): PASS on spec, first frame, caption text for the three changed beats, safe area, motion, end card, manifest. Open: VS-2 (Medium), VS-6, VS-8 (Low). No VS-1 (caption is neutral, no decorative word).
- Mosaic 9:16 (v11): PASS on the same checks. Open: VS-2, VS-6 (end card empty lower half), VS-8.
- Kinetic 4:5 (v12): PASS on spec, first frame, text, safe area, motion, end card, manifest. Open: VS-1 (Medium), VS-3, VS-5, VS-7 (Low). Cleanest on faces. Fidelity to its reference is partial.
- Promo 4:5 (v12): PASS on spec, first frame, text, safe area, motion, end card, manifest. Open: VS-1 and VS-2 (Medium), VS-4, VS-5, VS-7, VS-8 (Low).
Ranking by polish (reviewer's judgement, not a measured result): promo, then mosaic, then kinetic (kinetic is calm and brand-safe but plain, with kerning slips and large empty areas). Ranking by caution on faces and claims: kinetic, then mosaic, then promo. Verdicts rest on measurements and sampled frames, not full playback. Approval of a draft is not approval to publish.

## Candidate lessons for the Director
- Decorative words and chips (TEAMWORK, TEAM, PARTNERS, VISITORS) are claims; they need the same source check as captions. Put a rule in the build brief that decorative labels are drawn from an approved list tied to verified-facts.
- A caption can be made safe while a decorative word on the same frame re-introduces the claim; check both layers when a caption is fixed.
- Per-letter text animation needs kerning-aware positioning (x from the kerned prefix width and a pair-adjust, or draw the word to a layer then reveal by mask) to avoid overlap in pairs such as AR and TI.
- Duotone photo walls at 270 px tiles still show recognisable faces; decide a standing rule (blur faces in background tiles, or use equipment and stand shots only) instead of re-raising it each design.
- Probe motion on frame-aligned times (multiples of 0.04 s at 25 fps); a seek between frames creates a false zero-diff step.
- Record the s8_2 team-photo approval in verified-facts (row 27 still names 0f44943b).
