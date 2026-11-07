# QA report video 4: adipec26-thanks_linkedin_4x5_v4.mp4

Reviewer: qa-reviewer (separate invocation from the producer; not self-reviewed). Date 2026-11-07.
File: /tmp/work/adipec-v4/out/adipec26-thanks_linkedin_4x5_v4.mp4 (12,775,620 bytes), SHA-256 d0fca4e68de542a7e598a79d64449174cd67afe1a4a6510ca2c83a9d6889086b
Companions: adipec26-thanks_cover_4x5_v4.jpg (319,014 bytes), adipec26-thanks_captions_v4.srt (607 bytes), same folder.
File name follows <campaign>_<platform>_<aspect>_v<n>.mp4.

## Verification scope (true)
- Whole file, by script: ffprobe, moov position, blackdetect, freezedetect, volumedetect, loudness_check.py, and a programmatic safe-area measurement of the saved overlay PNGs (/tmp/work/adipec-v4/out/over_00 to over_09, base_10).
- Frames: scripts/contact_sheet.py sheet (20 frames, every 2 s, 320 px wide) viewed. In addition 43 extra frames extracted with ffmpeg and viewed: for each of the 11 slides the start (after the fade, t = slide start + 0.4 s; 0 s for the title), the middle and the end (0.04 s before the next cross-fade), plus all 10 cross-fade midpoints (cross-fade start + 0.2 s: 4.2, 7.6, 11.0, 14.4, 17.8, 21.2, 24.6, 27.8, 31.0, 34.2 s). Montages were viewed at 432x540 per frame; full 1080x1350 frames were viewed for slide 0 start, slide 1 middle and end, slide 2 end, slide 3 start, slide 7 middle, slide 8 middle, slide 9 middle. The other full-size frames were only seen in montages.
- Pan smoothness: horizontal shift between consecutive frames measured by image matching for two pans (slide 1 at 4.4 to 7.2 s, slide 5 at 18.0 to 20.8 s). The other four pans were seen only as start, middle and end frames.
- NOT a full real-time playback. Nobody listened (the track is silent by design). Not tested on a phone or inside LinkedIn. The 5 source photos not named below (u2, u3, u4, u8 originals) were inspected only through the video frames; u6 and the two Drive originals were viewed as source or as slides.
- The contact sheet was written to qa/contact_sheet_v4.jpg and later removed by commit 0bf1530 (public repo policy: no visitor-face sheets). Frames are in scratch space outside the repo.

## Technical checks (command, result)
1. `ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels,bit_rate,nb_frames:format=format_name,duration,size,bit_rate -of default=nw=1 <file>`
   - Container mov,mp4 (MP4). Video H.264 High, yuv420p, 1080x1350, r_frame_rate 30/1 and avg_frame_rate 30/1, 1200 frames = 40.0 s x 30 (constant). Audio AAC LC, 48 kHz, stereo, 1876 frames. Duration 40.000 s (script expected 40.0; audio 40.000 s too). Size 12.78 MB. Total bit rate 2.56 Mbps (video 2.54 Mbps, audio about 2 kbps because it is digital silence).
   - Against the verified LinkedIn rows (brain/platform-specs.md, a7174587 and a1311816): MP4 and H.264/AAC OK; 1080x1350 inside 256x144 to 4096x2304 OK; ratio 0.8 inside 1:2.4 to 2.4:1 OK; 30 fps inside 10 to 60 OK; size 12.8 MB between 75 KB and 5 GB OK; duration 40 s inside 3 s to 10 min (Page) OK. Bit rate: the stated range is 192 Kbps to 30 Mbps; combined 2.56 Mbps OK (the audio stream alone is far under 192 Kbps, which the spec does not apply per stream; stated here so nobody is surprised). PASS.
2. Fast start: `ffmpeg -v trace -i <file> 2>&1 | grep -m1 -E "type:'moov'|type:'mdat'"` returned `type:'moov' ... sz: 45116 40` so moov is first (offset 40). PASS.
3. Black and freeze: `ffmpeg -i <file> -vf blackdetect=d=0.2,freezedetect=n=-60dB:d=1 -an -f null - 2>&1 | grep -E "black_start|freeze_start|freeze_end|freeze_dur"`.
   - blackdetect: no black segment. PASS.
   - freezedetect segments: 0 to 2 and 2 to 4 (title slide, one hold split at 2 s by the detector); 24.8 to 26 and 26 to 27.63 (slide 7, the DP console photo, a static cover slide); 28 to 30.83 (slide 8, the collage crop, static); 32 to 34 (slide 9, static); 34.4 to 40 (end card). All are the static slides by design: title, the three non-pan photo slides and the end card. No freeze was reported inside any of the six pan slides (4.4 to 24.0 s). The pans hold about 14 percent (0.5 s) at each end, shorter than the 1 s detector threshold, so no false freeze. PASS.
4. Loudness: `python3 scripts/loudness_check.py <file>` gives Integrated -inf LUFS, true peak -inf dBTP, LRA 0.0. The "within 1.5 LU of -14: CHECK" line is expected for a silent track; true peak line PASS. `volumedetect`: mean and max -91.0 dB (digital silence). Reported as silent by design, neither a loudness pass nor fail.
5. SRT: `cat` of the file. Valid SubRip: 10 numbered cues, blank-line separated, comma milliseconds, increasing times, no overlap. Cue times (each starts 0.4 s into its slide, ends 0.2 s before the next cross-fade) match the slide table: 4.4 to 7.2, 7.8 to 10.6, 11.2 to 14.0, 14.6 to 17.4, 18.0 to 20.8, 21.4 to 24.2, 24.8 to 27.4, 28.0 to 30.6, 31.2 to 33.8, 34.4 to 39.8 s. Text of cues 1 to 9 equals the on-screen captions exactly. Cue 10 is a one-line summary, not the end card text word for word (it leaves out the four partner names). The title slide ("Thank you. ADIPEC 2026 Abu Dhabi, 2-5 November 2026") has no cue. PASS with NOTE N3.
6. Cover: 1080x1350, 319,014 bytes (under 2 MB). It is the title slide as rendered (mean pixel difference to the video frame at 0 s is 2.7 of 255, max 68, JPEG and H.264 compression). PASS.

## Slide table checked against build_video.py
| # | Time (s) | Photo | Caption | Pill | Match |
|---|----------|-------|---------|------|-------|
| 0 | 0 to 4 | 0f44943b | Thank you. / ADIPEC 2026 · ABU DHABI / 2-5 November 2026, logo card | no | yes |
| 1 | 4 to 7.4 | u7 pan | Welcome to the stand | yes | yes |
| 2 | 7.4 to 10.8 | u1 pan | Hands-on with the DP console | yes | yes |
| 3 | 10.8 to 14.2 | u5 pan | Questions at the console | yes | yes |
| 4 | 14.2 to 17.6 | u8 pan | Technical discussions | yes | yes |
| 5 | 17.6 to 21 | u3 pan | Face to face | yes | yes |
| 6 | 21 to 24.4 | u4 pan | Sharing experience | yes | yes |
| 7 | 24.4 to 27.6 | u6 crop | DP console on the stand | no | yes |
| 8 | 27.6 to 30.8 | u2 top photo | Conversations at the stand | yes | yes |
| 9 | 30.8 to 34 | a07555b5 | Thank you for stopping by | no | yes |
| 10 | 34 to 40 | end card | Thank you / To every client and visitor who stopped by our stand. / And to our technology partners for their support: Sonardyne, Fugro, NAVIS, Marine Technologies / Sinor Marine Services Middle East FZCO | no | yes |

Photo order and captions match the script. No spelling errors found. No em or en dashes on screen. The held-back cf677e0a is not in /tmp/work/adipec-v4/jpg and no frame shows the two men at the stand TV or any media file name: confirmed on all sampled frames.

## Safe area and layout
- Programmatic (overlay pixels that are not the navy gradient): text and pill x range 64 to 786 on all content slides, so the 64 px left margin holds and nothing nears the right edge. Lowest overlay pixel y is 1175 (a descender), so nothing in the bottom 150 px (y 1200 and below). The OUR VISITORS pill sits at x 64, y 64 to about 110, inside the margin. End card content spans x 213 to 866, y 80 to 1167. PASS except W1 below.
- Not text clipping seen on any caption or title in viewed frames.
- Faces: the video is built from full-height pans so no face is stretched; aspect ratios were preserved (the box slides 8 and 9 keep the native ratio on a blurred band). Slide 8 uses only the sharp top photo; no collage seam visible. Slide 7 crop is a clean crop.
- Face cuts at the ends of pans (viewed): slide 1 start, the laughing visitor at the far left has his head cut by the left edge (cut in the source too, pan starts at 0.0); slide 1 end, a bearded man in profile is cut by the right edge; slide 2 start, the blue-shirt man at the left edge is partly cut; slide 4 start and end, partial heads at the left and right edges; slide 5 start, a back-of-head fills the left. Main subjects (faces being addressed) are whole at rest. See W2.
- Slide 5 (u3 "Face to face"): the pan goes from a face (start), through a frame that is almost all the back of a head (middle, the travel point), to the grey-haired man's face at the end where his chin and mouth are covered by the foreground shoulder. See N2.
- Slide 7: the caption "DP console on the stand" runs over the console screen, a thumb and the lanyard of the man at the left. Legible but cluttered. See W3.

## Caption contrast (computed)
Method: for each caption (and the title slide text), text pixels taken from the saved overlay PNG, background taken from the actual video frame in a 2 to 6 px ring around the letters, WCAG contrast of white text against the 95th percentile (brightest 5 percent) of that background; frames at slide start, middle and end.
- Lowest 95th percentile contrast: 2.51:1 (slide 1, "Welcome to the stand", end frame, white text over a white thobe and light sleeve). Other low values: slide 3 2.59, slide 7 2.70, slide 0 title 2.96, slide 4 2.86 (middle frame).
- Worst single bright pixel in any ring: 1.89:1 (slide 4 middle). Slides 8, 9 (blurred band) 6.3:1 to 6.7:1; slide 5 3.7 to 4.7; slide 2 and slide 6 range between 2.4 and 7.3 depending on pan position.
- Text is 48 px semi-bold on 1080 px width (large text). 3:1 is the usual floor for large text; slides 1, 2, 3, 4, 7 and the title dip below 3:1 on bright clothing. Captions were still readable by eye in every viewed full-size frame, but slide 1 is the weakest. See W4. This is a measurement of contrast, not proof of readability on a phone.

## Pan smoothness and cross-fades
- Measured frame-to-frame shift, slide 1: 0, 0, 0, 0, 0 then 2, 2, 2, 4, 6 ... peak 20 px per frame ... 8, 6, 6, 4, 4, 4. Slide 5: same shape, peak 24 px per frame. Both rise and fall with no reversal or jump (a 14 percent rest at each end, smoothstep between). No jitter found in the two pans measured. The shift value is quantised to 2 px by my search step, so sub-pixel jitter is not excluded. Peak speed about 600 to 700 px per second (about 2 percent of the width per frame) is brisk for slide 5 but smooth.
- Cross-fade midpoints (all 10 viewed): all are straight dissolves, no black or cut frame. Overlapping captions at 4.2 (title text over "Welcome to the stand"), 7.6, 11.0, 14.4, 17.8, 21.2, 24.6, 27.8, 31.0 and 34.2 s show two lines of white text superimposed for about 0.4 s: for example "Hands-on with the DP console" over "Technical discussions" is garbled at the midpoint (letters overlap), most obviously at 11.0, 14.4 and 31.0 s. At 34.2 s the end-card lines overprint the slide 9 caption. It lasts 0.4 s and each side is readable before and after. NOTE N1.

## Logo and end card
- Logo: assets/brand/sinor-logo.png (1041x396, ratio 2.629) placed by the script with a proportional resize onto a white rounded plate; viewed on the title slide (top left) and the end card (top centre): the blue SMS ellipse with ship, "SINOR MARINE SERVICES" and "MIDDLE EAST FZCO" are intact and undistorted. It is the repo's recorded approved logo (brain/brand-profile.md; "needs Rahul's confirmation for marketing use" remains in verified-facts). The Services logo is correct for this campaign (Sinor Marine Services Middle East FZCO), not the Technologies logo. PASS.
- End card text matches build_video.py and the caption file. Partner list Sonardyne, Fugro, NAVIS, Marine Technologies is still unconfirmed by Rahul (verified-facts: NAVIS an inference, Fugro awaiting confirmation). See F1.
- Final frame: end card held 5.6 s with all text static, intentional. Gap between "Marine Technologies" and the footer line is only about 30 px (same as the earlier D12), cosmetic.
- Title logo card starts at x 48, y 48, the one element outside the 64 px side margin (16 px short). See W1.

## Incidental content review (what a viewer could read at 1080 px)
No names were recorded in this report. "Legible" means a viewer can read the characters at 1080 px width without zoom (on a phone feed the video is about 1080 px wide at most).
| ID | Photo / slide and approx. position | Content | Legible at 1080 px? | Recommendation |
|----|-----|------|------|------|
| I1 | u6 (slide 7), stand panel at the left | The panel "15+ years DP engineering, 100+ projects, 40+ countries" is in the full photo. The slide 7 crop starts at x 520 and removes the whole panel. | Not in the video: no panel text appears in slide 7 frames. | Good. Keep the crop. |
| I2 | Title slide 0 and cover JPG, left edge, y about 175 to 335 | Same stand panel (a different, larger print): "100+ PROJECTS" and "40+ COUNTRIES" with "SITION." (HOLD POSITION cut by the frame) | The numerals "100+" and "40+" are legible, the words PROJECTS and COUNTRIES are small (about 8 px high) but readable on a close look. "15+ years" is cut off. This is also the LinkedIn thumbnail. | WARN. These claims are not confirmed by Rahul for public use. Get his confirmation or shift the title crop so the panel is out of frame. |
| I3 | u1 (slide 2), upper right, x about 840 to 1060, y 190 to 530 | The same panel, "HOLD POSITION." and numerals "15+", "100+", "40+" | "HOLD POSITION" and the numerals are legible at the middle and end of the pan; the labels beneath ("YEARS ENGINEERING", "PROJECTS", "COUNTRIES") are 6 to 8 px high and not legible. The bullet list is not legible. | WARN. Same recommendation as I2. |
| I4 | u7 (slide 1) at the end of the pan, right, x 810 to 1080, y 130 to 650 | A screen of another exhibitor (an Amphicos tank monitoring display: "Previous Day Consumption 973.12", "22593.80", "Tank-1") | Legible | NOTE. Third-party data on another company's screen; not Sinor content. Optional: pan end earlier. |
| I5 | u7 (slide 1) and u5 (slide 3) | Another exhibitor's stand banner "amphicos / ENGINEERING SOLUTIONS, For a safer, smarter and more reliable marine, oil and gas industry", with "amphicos.com" | Banner name and headline legible across slides 1 and 3; small URL borderline | NOTE. Other exhibitor's brand shown behind visitors; ask Rahul if acceptable. |
| I6 | u7 (slide 1), u1 (slide 2), u5 (slide 3), u6 (slide 7), a07555b5 (slide 9), title slide | Other third-party names and signs: "FLUIDS CHEM CO.,LTD", "QA TEST CENTER", "shipworkz" (large lit sign), "CHINA Pavilion", "WELLTEC" (partly), "HP-LUB II", "HEBEI ALL LAND STEEL PIPE" (partly), "CCS" and "MAYEKAWA MYCO" (slide 7), "...ori Machinery Co.,Ltd." (slide 9, partial), "Sonardyne SPRINT-Nav" on the housing (own partner, expected) | Legible on slides 1, 2, 3, 7; "shipworkz" and "CHINA Pavilion" most obvious | NOTE. Normal for an exhibition hall. Optional: Rahul to decide. |
| I7 | u7 (slide 1, 4 s to 7.4 s), right, y about 960 to 1110 | A visitor badge with a small photo and printed lines | Illegible (printed lines below photo, QR code at the foot). Badge photo of the wearer is visible. | NOTE. No name or ID number could be read. |
| I8 | All people shots (slides 0, 1, 2, 3, 4, 5, 6, 9) | Lanyards with the ADIPEC logo and badges | Badge text illegible in every viewed frame; on slide 5 ("Face to face") lanyard and badge are at the frame edge and illegible; slide 9 two badges with QR codes and tiny lines, illegible | NOTE. A visitor badge, name illegible. Nothing readable. |
| I9 | a07555b5 (slide 9), centre screen, x 270 to 400, y 560 to 800 | The stand's own screen showing coordinates "46.760942, -92.097473, 238.0" and a clock "12:37:10" and a Windows taskbar | Coordinates are small but readable on the top-left of the screen (about 10 px high); the clock is borderline | NOTE. Demo data on the stand screen; ask Rahul that this is demo data, not a client position. Same as the earlier QA video 3. |
| I10 | a07555b5 (slide 9), left of the table, around x 300 to 400, y 1040 to 1070 | A phone or tablet and papers on the counter | Illegible | NOTE. |
| I11 | u8 (slide 4) | A visitor holds a phone or small device in the hand | Illegible; the screen is not visible | NOTE. |
| I12 | u1 (slide 2) upper right | A staff man holds a phone to his ear | No screen visible | NOTE. |
| I13 | u6 (slide 7), bottom right of the source | A laptop screen on the next stand | Cropped out of the video | none |
| I14 | All sampled frames | Media file names (like the held-back TV) | None found. cf677e0a absent. | PASS. |
| I15 | Many visitors and several unnamed people in the backgrounds (slides 1 to 6, 9) | Identifiable faces of visitors and staff | Faces are plainly identifiable on every photo slide | NOTE. Rahul should confirm he has consent or is content to show these visitors on a public post. I did not identify anyone. |

## Defects and findings
| ID | Severity | Location | Issue | Responsible |
|----|----------|----------|-------|-------------|
| F1 | WARN (publish blocker) | End card 34 to 40 s, SRT cue 10, caption_linkedin_plain.txt | NAVIS and Marine Technologies (and Fugro, "Grog" in dictation) are still unconfirmed partner names. Do not post until Rahul confirms all four. Unchanged since v1. | Director to ask Rahul |
| F2 | WARN (publish blocker) | Title slide 0 (also cover JPG) and slide 2 pan (7.4 to 10.8 s), see I2 and I3 | The unconfirmed stand claims "15+ years, 100+ projects, 40+ countries" appear legibly in two places: "100+" and "40+" with PROJECTS and COUNTRIES on the title slide and the cover, and "15+", "100+", "40+" on the small panel in slide 2. The u6 slide itself does not show them (crop removes the panel). Rahul has not confirmed them for public use. | Director (ask Rahul) then video producer (recrop title or accept) |
| W1 | WARN | Title slide 0, logo card x 48 and y 48 | Logo card sits 16 px outside the stated 64 px side margin (and the top margin). All other text is inside. Likely still safe in the LinkedIn feed, but the brief number is 64 px. | Video producer |
| W2 | WARN | Slide 1 end (about 6.7 s), slide 2 start, slide 4 start and end | Secondary faces cut by the frame edge at the ends of pans, notably a bearded man in profile at the right edge at the end of slide 1. The principal face is whole. | Video producer (adjust pan end to about 0.7 on slide 1 or accept) |
| W3 | WARN | Slide 7, 24.8 to 27.4 s | Caption runs over the console screen, a thumb and the left man's badge strap; busier than other slides and only 2.70:1 against the brightest background. | Video producer |
| W4 | WARN | Slides 0, 1, 2, 3, 4, 7 | Caption contrast against the brightest nearby pixels is 2.5 to 3.0:1 (95th percentile), below 3:1; lowest 2.51 on slide 1 (white thobe). The gradient starts at y 930 and is thin behind the text at y 1118 to 1175. | Video producer (deepen gradient by 10 to 20 percent or start it higher) |
| N1 | NOTE | All 10 cross-fades | Overlapping captions are garbled for about 0.4 s at each midpoint; no black, no cut frames. Unchanged design. | none, optional |
| N2 | NOTE | Slide 5, 18 to 20.8 s | The pan crosses a frame that is almost entirely the back of a man's head, and the second face has its mouth under the foreground shoulder at the end. Smooth, not broken. | Video producer (optional) |
| N3 | NOTE | SRT | No cue for the title slide text; cue 10 shortens the end card (no partner names). Fine for an accessibility track, but state this to Rahul. | Director |
| N4 | NOTE | Audio | A silent AAC track, about 2 kbps. LinkedIn bit rate limit speaks about the file, no issue found. | none |
| N5 | NOTE | Incidental list I4 to I15 | Third-party names, an exhibitor screen and demo coordinates are legible; badge text is not. See table. | Director (decide with Rahul) |

No FAIL-level technical defect. The file plays, meets every verified LinkedIn row and the safe area.

## Earlier fixes (qa_report_video_3) still hold
- D5 bottom 150 px safe zone: holds (maximum overlay y 1175).
- D9 media file name on the TV: holds (cf677e0a absent, no file name on any frame).
- D10 collage seam and white band: holds (slide 8 uses only the top photo, clean edge, no band; viewed full size).
- D1 partner names: still open (F1). D7 stand panel claims: still open and now also in the title slide and cover (F2).
- D12 footer gap on the end card: unchanged, cosmetic.

## Verdict
Technically ready: spec, fast start, constant 30 fps, no black or false freezes, silent track, safe-area text, cover under 2 MB, SRT valid. Not ready to publish until Rahul answers F1 (partner names) and F2 (the stand claims, visible on the title slide and cover and small on slide 2). Contrast and edge-cut warnings W1 to W4 are polish items. Sampled review only, not full playback; nobody listened; not phone-tested or tested inside LinkedIn.

## Candidate lessons for the Director
- A crop that removes a claim on one slide does not remove it from other slides that show the same stand panel: check every slide for the same incidental text, including the title slide and the cover.
- Measure caption contrast from the real pixels behind the text (overlay mask plus video frame) instead of judging by eye; white text on light clothing fell under 3:1 on six slides.
- Cross-fade midpoint overlap of captions is expected; check that it is brief and mention it, rather than raising it as a defect each time.
- The contact sheet script writes into the repo; visitor-face sheets must go to scratch space (repo ignores them now), so run it with an output path outside the repo.
