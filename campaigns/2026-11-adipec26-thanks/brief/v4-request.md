# v4 request: more visitor photos, LinkedIn-optimised video (2026-11-07)

Rahul's words: "Extend the visitors section little more with showing more visitors good photos. Also make the video format optimized for LinkedIn post."
Reading used (stated to Rahul, correctable): this is the ADIPEC 2026 thank-you video (v3 used 4 of the photos). Not the Sinor Marine Technologies website, which has no visitors section.

## State of the photos (Drive Inbox: Adipec26, listed 2026-11-07)
21 files: 9 JPG (already reviewed in v1 to v3) and 12 iPhone HEIC (7 known earlier plus 5 new: IMG_4156, IMG_4464, IMG_4163, IMG_4403, IMG_4188). No tool here can decode the HEIC portrait-mode files. Rahul declined an install of pillow-heif and will upload JPG copies himself, so v4 waits for those uploads.

## LinkedIn format (see brain/platform-specs.md, verified 2026-11-07)
MP4 H.264 High, AAC 48 kHz, 1080x1350 (4:5), constant 30 fps, key text inside the safe area, custom thumbnail, optional SRT, duration well under the limit. v3 was 25 fps; v4 moves to 30 fps.

## Plan for v4 (when the JPGs arrive)
1. Download the new JPGs from the Drive folder; inspect every photo (identity, incidental on-screen text such as media file names, quality).
2. Extend the visitors section: more visitor photos, plus a collage slide that shows several visitors in one frame; keep the held-back photo out (a media file name is readable on the TV).
3. Rebuild with build_video.py (30 fps), new cover image, optional SRT; independent QA with the video-qa-checklist; log in brain/deliveries.md.
Open questions that stay open: personal or company account to post from; the partner names (unconfirmed since v1).
