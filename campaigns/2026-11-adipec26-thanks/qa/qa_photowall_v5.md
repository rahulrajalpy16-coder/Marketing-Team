# QA photowall v5 (narrow check)
Files: /tmp/work/adipec26/wall5_v1/...v1_9x16_v5.mp4 (24.6 s), wall5_v2/...v2_9x16_v5.mp4 (22.2 s). Frames: /tmp/work/qa_wall5/.

| Item | v1 | v2 |
|---|---|---|
| 1080x1920, H.264 yuv420p, 30 fps, AAC 48 kHz (ffprobe) | PASS | PASS |
| Duration | 24.6 s PASS | 22.2 s PASS |
| ebur128 peak=true, true peak | -1.9 dBTP PASS (< -1) | -2.2 dBTP PASS |
| Integrated loudness | -15.0 LUFS | -15.0 LUFS |
| Opening logo, frames 0.0/0.5/1.0/1.8 s | PASS: large, transparent, above heading, no overlap | PASS |
| Opening 2.2 s | Logo and heading are fading out together over the photo wall; ghosted overlap is part of the transition (Low, observation) | same |
| Hero caption "The Sinor Marine team" (sampled 3.8 s) | PASS: logo top-left of panel, undistorted, clear of chip and title; small but legible at phone size | PASS |
| Partner/Visitors captions | NOT VERIFIED: my sampled frames missed them, so no frame shows them | NOT CHECKED |
| End card (v1 at 24.3 s) | PASS: logo, Thank you, partner logos intact | NOT CHECKED (same template assumed, unverified) |

Defects: none above Low. D1 Low: at 2.2 s the fading logo overlaps the ghosted "ADIPEC 2026" (transition only). Owner: video-editor, optional.
Scope: audio measured only, not listened to. Frames sampled, not full playback. Partner-logo captions and the Visitors caption were not seen; v2 end card was not seen.
