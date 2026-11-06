---
name: video-qa-checklist
description: Use to independently check a rendered video (and its cover, captions and subtitles) against Part 14 before handoff. Runnable procedure for the qa-reviewer.
---
# Video QA checklist

Run each step on the actual file. Record the command used and the result. State exactly what was sampled.

1. Playability and spec: ffprobe -v error -show_entries stream=codec_name,pix_fmt,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels:format=duration,size -of default=nw=1 <file>. Compare to the verified entry in brain/platform-specs.md (container MP4, codec, pixel format, dimensions, frame rate, duration, audio).
2. Fast start: confirm the moov atom is at the start (ffmpeg -v trace -i <file> 2>&1 | grep -m1 -E "moov|mdat" shows moov first), or confirm -movflags +faststart in the render log.
3. Loudness: python3 scripts/loudness_check.py <file>. Compare to the target in the spec (about -14 LUFS, true peak at or below -1 dBTP as a starting point).
4. Frames: python3 scripts/contact_sheet.py <file> campaigns/<name>/qa/contact_sheet.jpg 2 5 320. View it. Look for black gaps, frozen frames, broken transitions, cropped faces or equipment, unreadable text, text in interface zones.
5. Black and freeze detection: ffmpeg -i <file> -vf blackdetect=d=0.2,freezedetect=n=-60dB:d=1 -an -f null - 2>&1 | grep -E "black_start|freeze_start".
6. Titles and subtitles: read every overlay and SRT line against the source facts and audio. Check marine terms and names by hand.
7. Facts and branding: logos accurate and official, claims supported, no invented capabilities, correct partner names.
8. Final frame intentional. Cover image suitable and legible at phone size.
9. Delivery metadata: file name follows <campaign>_<platform>_<aspect>_v<n>.mp4; size and SHA-256 recorded.
10. Write the defect report with ID, severity, timestamp or location, responsible specialist. Report the true verification scope: a sampled review is not full playback.

Never report a check that was not run. If independence was not possible, write "self-reviewed".
