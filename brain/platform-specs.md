# Platform specs

ALL ENTRIES BELOW ARE UNVERIFIED STARTING POINTS from the first-run prompt (Part 7). They are not facts. Before first use on a deliverable, look up current official documentation, then fill in the source URL and date and change the status to verified. Re-verify when older than 30 days.

| Platform | Placement | Format starting point | Status | Last verified | Source URL |
|----------|-----------|-----------------------|--------|---------------|------------|
| LinkedIn | Feed video | MP4, H.264, AAC. 16:9 1920x1080, 1:1 1080x1080, 4:5 1080x1350, 9:16 1080x1920. Choose ratio from footage and story. Burn in concise subtitles (often watched muted). Check whether photos and video can be mixed in one post before promising it. PARTLY VERIFIED 2026-11-06 for VIDEO ADS only (LinkedIn Marketing Solutions spec page): MP4; ratios 4:5, 9:16, 16:9, 1:1; 4:5 max 1080x1350; file 75 KB to 500 MB; help page says H.264 or VP8 and frame rate under 30 fps for ads. Organic post limits (reported 5 GB, 10 min for a Page, 10 to 60 fps) come only from third-party blogs: UNVERIFIED. | partly verified (ads) | 2026-11-06 | https://business.linkedin.com/advertise/ads/sponsored-content/video-ads/specs ; https://www.linkedin.com/help/lms/answer/a424737 |
| Instagram | Reels and Stories | 9:16, 1080x1920 | unverified | never | to be filled |
| Instagram | Feed | 4:5 or 1:1 | unverified | never | to be filled |
| YouTube | Standard | 16:9, 1920x1080 or higher | unverified | never | to be filled |
| YouTube | Shorts | 9:16, 1080x1920 | unverified | never | to be filled |
| TikTok | Video | 9:16, 1080x1920 | unverified | never | to be filled |
| Facebook | Video | 4:5, 9:16 or 16:9 | unverified | never | to be filled |
| X | Video | 16:9 or 1:1; 9:16 where supported | unverified | never | to be filled |

Still to determine per platform when verifying: maximum duration, maximum file size, caption length, safe zones, subtitle rules, cover image size.

General: keep titles and faces inside interface-safe zones, keep text readable at phone size, match source frame rate unless the platform requires otherwise. Target length, hook timing and posting time are hypotheses to test, not rules.

## Website (verified 2026-11-06)
| Item | Value | Status | Last verified | Source URL |
|------|-------|--------|---------------|------------|
| LCP good | 2.5 s or less | verified | 2026-11-06 | https://web.dev/articles/vitals |
| INP good | 200 ms or less | verified | 2026-11-06 | https://web.dev/articles/vitals |
| CLS good | 0.1 or less | verified | 2026-11-06 | https://web.dev/articles/cls |
| Text contrast (WCAG 2.2 SC 1.4.3, AA) | 4.5:1 normal text, 3:1 large text | verified | 2026-11-06 | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html |
| Pointer target size (WCAG 2.2 SC 2.5.8, AA) | at least 24 by 24 CSS px | verified | 2026-11-06 | https://www.w3.org/TR/WCAG22/ |
Notes: search excerpts were read, not the full pages. Web.dev frames the Core Web Vitals as real-user field metrics. Title length (50 to 60) and meta description length (120 to 155) used in agent files are working guidelines, not verified standards. Re-verify after 2027-02-04.

## LinkedIn organic video posts (VERIFIED 2026-11-07 against LinkedIn Help, first-party pages read in full)
| Item | Value | Source |
|------|-------|--------|
| Personal profile video post | Max 5 GB, min 75 KB; duration 3 s minimum from desktop (2 s from the mobile app) up to 15 minutes; resolution 256x144 to 4096x2304; aspect ratio 1:2.4 to 2.4:1; frame rates 10 to 60 fps; bit rates 192 Kbps to 30 Mbps | https://www.linkedin.com/help/linkedin/answer/a7174587 |
| LinkedIn Page video post | Same limits but maximum duration 10 minutes; supported file types include MP4 and H264/AVC with AAC audio; MOV, QuickTime and AVI no longer supported | https://www.linkedin.com/help/linkedin/answer/a1311816 |
| Safe zones | Keep key elements, text and logos away from the top, bottom and side edges so the LinkedIn interface does not cover them | a7174587 |
| Thumbnail and captions | A custom video thumbnail can be uploaded; captions by SRT file upload or auto captions (10 languages) | a7174587 |
| Video ads (if ever boosted) | MP4, ratios 4:5, 9:16, 16:9, 1:1; 4:5 max 1080x1350; 75 KB to 500 MB; thumbnail max 2 MB | https://business.linkedin.com/advertise/ads/sponsored-content/video-ads/specs |
Our default for the ADIPEC thank-you video: MP4, H.264 High, AAC 48 kHz, 4:5 at 1080x1350 (best use of the mobile feed; also valid for ads), constant 30 fps, silent track, key text inside the safe area, plus a custom thumbnail and an optional SRT. The 4:5 ratio being "best for mobile" is a common recommendation in third-party guides, not a LinkedIn rule.
