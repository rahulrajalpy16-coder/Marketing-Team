# QA photowall v6 (narrow check, independent of producer)

Files: /tmp/work/adipec26/wall6_v1/adipec26-thanks_linkedin_photowall_v1_9x16_v6.mp4 and /tmp/work/adipec26/wall6_v2/adipec26-thanks_linkedin_photowall_v2_9x16_v6.mp4

## Scope actually run
- ffprobe (both files). ebur128 peak=true (both files). Audio measured only, not listened to.
- Frames sampled every 0.5 s across each beat: v1 SPRINT-Nav 7.0 to 10.0 s, v1 Guidance 14.2 to 17.2 s, v2 SPRINT-Nav 4.6 to 7.6 s, v2 Guidance 11.8 to 14.8 s. Frames were viewed as contact sheets (540 px wide for v1, 360 px wide for v2), NOT full-resolution. Fine face detail was not inspected at 1080x1920.
- v1 opening (frame 5) and v1 end card (frame 730). v2 opening and end card not viewed.
- Not checked: the rest of the timeline, other beats, captions elsewhere, transitions, cover.

## Results
| # | Item | v1 | v2 |
|---|------|----|----|
| 1 | SPRINT-Nav close-up AND four-person group (plinth in middle, 2 Sonardyne left, 2 Sinor right) side by side in the focal area, not hidden | PASS | PASS |
| 2 | Guidance beat: two-person photo AND four-person photo with the woman side by side, both visible | PASS | PASS |
| 3 | Faces not cut off in those beats | PASS | PASS |
| 4 | Captions and logos readable ("Sonardyne SPRINT-Nav", "With Guidance Marine", logos) | PASS | PASS |
| 5 | 1080x1920, H.264, yuv420p, 30 fps, AAC 48 kHz | PASS | PASS |
| 6 | Duration | 24.6 s PASS | 22.2 s PASS |
| 7 | True peak below -1 dBTP | -1.9 PASS | -2.2 PASS |
| 8 | Opening and end card sanity | PASS | not viewed |

Loudness: both files integrated -15.0 LUFS (ebur128 I). The peak figures came from the tool's "Peak:" line, labeled dBFS in the output. It was run with peak=true, so it is the true-peak value.

## Observations and defects
- D1 (minor, Video editor): during both beats the lower part of each focal photo sits behind the translucent caption panel. In the Sonardyne beat, the group photo's legs and feet and the plinth base are covered or dimmed. In the Guidance beat, the feet of the four-person photo and the lower body of the two-person photo are covered. Faces, the SPRINT-Nav label and the SMS stand sign remain clear. Does not fail the client request.
- D2 (minor, Video editor): the SPRINT-Nav label on the close-up is cut at the right edge ("SPRINT-Na") in the v1 and v2 tiles. This comes from the source crop and the tile crop and does not hide any face. Optional fix.
- D3 (info, Video editor): in the first ~0.5 s of the v1 beat (7.0 s) and the last frame of each sheet, the focal pair is not yet in place. The wall is still moving, so the pair is only present during the settled part of the beat. In v1 the pair is settled from about 8.0 s, and in v2 from about 5.0 s, until the beat ends. A frame-exact beat boundary was not measured.
- No blocking defects found within the checked scope.

## Candidate lesson for the Director
Place focal photos so the caption panel covers only the bottom edge of the tile, or move the panel lower, when the client asks for two specific photos to be "clearly visible".
