# QA report: company-page caption (copy check)

Date: 2026-11-06. Checker: qa-reviewer (independent of producer). Files: exports/caption_company_final.txt, exports/caption_company_plain.txt.
Scope: read both files; python byte/codepoint checks; read brief, fact_check.md, fact_check_guidance.md, brand-profile, preferences, SKILL, copy notes (claims table re-verified, not trusted); viewed 6 photos (0f44943b, IMG_4413, IMG_4432, IMG_4188, IMG_4255, IMG_4464). Not viewed: the other 15 photos.

## Verdict: PASS with 2 low-severity suggestions. No blocking defects.

## Checks
| Check | Result | Evidence |
|---|---|---|
| Event, venue | PASS | ADIPEC, ADNEC, Abu Dhabi verified (fact_check 1a, 1b); "ADIPEC" only, unverified expansion not used (1e) |
| "has come to a close" vs dates | PASS | Event 2-5 Nov 2026 (ADNEC listing), today 6 Nov, so it has ended. Stand panel in photo 0f44943b reads "2-5 NOV" |
| Partner spelling | PASS | Sonardyne, Fugro, Marine Technologies, Guidance Marine match fact_check 2a, 3a, 5b, G1a; no "Limited"/"LLC" added |
| NAVIS spelling | PASS, see risk R1 | Matches Rahul's instruction and the stand panel styling |
| Company voice | PASS | we/our/us throughout, no "I/my"; confident, warm, customer-focused |
| Opening | PASS | Hook "Good conversations at ADIPEC 2026" is not proud/thrilled/delighted/excited; first sentence does not repeat it. Mildly soft rather than strongly factual (S1) |
| No ownership of partner equipment | PASS | No "our console/our sensor"; no products or roles named |
| No claim beyond "supported us at the stand" | PASS | Exact wording used. Photos show Sonardyne SPRINT-Nav, Navis Engineering console, MT display, Fugro Seastar and Marine Technologies screens; Guidance Marine not visible in the 6 photos viewed (confirmed by Rahul, fact_check_guidance G4c), so wording correctly stays generic |
| Unsupported or duplicate lines | PASS | "technical discussions" supported by IMG_4464 and the visitor/partner photos; team thanks is generic, from Director instruction (brand-neutral, no claim). "at the stand" repeated 3 times in different sentences; acceptable |
| CTA | PASS | Soft (comment or message), matches brief, no sales claim |
| Hashtags | PASS | 6 relevant tags, none touched by bold. #ADIPEC2026 usage not verified as an active tag (low) |
| Em/en dashes | PASS | Python on raw codepoints, both files: U+2014 0, U+2013 0, U+2212 0, U+2012 0, ASCII hyphen 0 |
| Asterisks | PASS | 0 in both files |
| Unicode bold | PASS | Only line 1 contains U+1D5D4-U+1D7FF; line 1 is entirely bold chars plus spaces (digits 2026 bold); hashtags/URLs plain; only other non-ASCII is U+1F64F (emoji) |
| Plain equals final un-bolded | PASS | NFKC(final) == plain: True |
| Encoding | PASS | UTF-8, no BOM, LF endings, trailing newline, 845 bytes final / 758 bytes plain |
| Paste-ready | PASS | No labels, brackets or comments in either file |
| Word count | PASS | Plain: 122 words total, 116 excluding hashtag line, 755 characters. Copy notes say about 118/110: small inaccuracy, not material |

## Risks and suggestions (non-blocking)
- R1 (low) NAVIS vs "Navis Engineering": the console in IMG_4413 shows the logo "NAVIS ENGINEERING", the company's own brand is "Navis Engineering" (fact_check 4b). A marine reader will recognise NAVIS, and Rahul chose it, so it is not an error. For the company page, "Navis Engineering" is the safer, more accurate form and also helps when tagging their page. Owner: copywriter/Rahul decision.
- R2 (low) Order and ranking: the list follows Rahul's dictation order, with Guidance Marine appended last. It could be read as a ranking, and Guidance Marine last may look like an afterthought. Fix options: add "in no particular order" or sort alphabetically (Fugro, Guidance Marine, Marine Technologies, NAVIS, Sonardyne). Owner: copywriter.
- S1 (info) Hook is a pleasant label, not a factual statement. Alternative hook 1 in the notes ("Thank you to everyone who visited us at ADIPEC 2026") is more directly factual if Rahul wants it.
- S2 (info) Partner LinkedIn pages must be tagged manually in the composer (not written in caption). Guidance Marine's page URL is in fact_check_guidance.md G3. Navis and MT tags depend on Rahul confirming the identities (fact_check 4a, 5a); the photos support both (Navis Engineering logo, MT logo and Marine Technologies screen).
- Reminder for handoff: Unicode bold is styled text and may render differently on some devices and screen readers.

## Not verified
- Whether LinkedIn displays the bold hook correctly on every device (not tested).
- Sinor team preparation statement: generic, not independently verifiable.
- Current existence/activity of #ADIPEC2026 on LinkedIn.

## Candidate lessons for the Director
- Check list order for ranking implications when adding a late partner to a dictated list.
- Prefer the logo text visible on equipment in photos (here "NAVIS ENGINEERING") when naming partners on a company page.
