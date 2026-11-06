# QA report copy 1: ADIPEC 2026 LinkedIn caption

Checker: qa-reviewer (independent). Date: 2026-11-06. Files checked: exports/caption_linkedin_final.txt, exports/caption_linkedin_plain.txt.
Scope: read both files in full; ran byte-level and Python checks; read brief, fact_check, preferences, skill, copy_notes; viewed 2 of the 5 named photos (0f44943b..., 0bc7989f...). The other 3 named photos were NOT viewed. Not an external fact verification: I relied on fact_check.md for sources and did not re-fetch any web page.

## Results
| Check | Result | Evidence |
|---|---|---|
| Event name, ADNEC Abu Dhabi, "come to a close" | PASS | fact_check 1a/1b: 2-5 Nov 2026, ADNEC, Abu Dhabi. Stand panel in photos reads "ADIPEC 2026, 2-5 NOV, ABU DHABI". Post date 6 Nov, so "has come to a close" is true. No expanded name used (good, 1e unverified). |
| Sonardyne | PASS | Spelling verified (2a). Sonardyne SPRINT-Nav unit and Sonardyne lanyard seen in photo 0f44943b. |
| Fugro | PASS (spelling) / partner role NOT VERIFIED from the 2 photos viewed | Spelling verified (3a). Rahul named Fugro in the brief. No Fugro item seen in the photos I viewed. |
| NAVIS | NOT VERIFIED | Written in capitals as on Rahul's stand styling. Identity as Navis Engineering is an inference (4a). Not visible in the photos viewed. |
| Marine Technologies | NOT VERIFIED | "MT" = Marine Technologies is an inference (5a). Photo 0f44943b shows a counter reading "...TECHNOLOGIES", which more likely reads as Sinor Marine Technologies, so it is not support for this name. |
| "our DP console", technical discussions, stand | PASS | DP console and "HOLD POSITION" panel visible in photo 0bc7989f; visitors and discussion consistent with the brief. |
| "Sinor colleagues, preparation and teamwork" | PASS | Generic, modest, not a fact claim that can be wrong. Photos show Sinor staff. |
| Personal-account voice | PASS | First person (I am grateful, my colleagues, send me a message), modest, appreciative, no claim of personal credit. |
| Opening | PASS | Hook "Good conversations at ADIPEC 2026" is factual and not proud/thrilled/delighted. Mild: hook is a gentle claim ("good") but fits the brief. |
| No unsupported claims, no duplicated lines | PASS | Stand-panel claims (15+ years, 100+ projects, 40+ countries), product roles and other company names are not used. "ADIPEC 2026" appears in both hook and line 1: light repetition only, not a duplicate line. |
| CTA and hashtags | PASS | Soft CTA (comment or message), no sales claim. Six hashtags, all relevant (#ADIPEC2026 #DynamicPositioning #MarineTechnology #Offshore #Maritime #AbuDhabi). One emoji. |
| No em dashes | PASS | Raw bytes: 0 occurrences of U+2014 and U+2013 and "--" in both files; no CR characters. |
| Unicode bold only on hook, correct block | PASS | Python: 29 bold characters, all in U+1D5D4 to U+1D7FF (letters U+1D5D4..U+1D5FF range, digits 2026 = U+1D7EE..U+1D7F2). Only non-ASCII besides the bold is the emoji U+1F64F. Hashtags and body are plain ASCII. No asterisks. |
| Plain = final with hook un-bolded | PASS | Python NFKC conversion of the final file equals the plain file exactly (True). |
| Encoding and paste-ready | PASS | `file`: UTF-8. No labels, notes or instructions in either file. Ends with one trailing newline. |
| Word count | INFO | 127 words including hashtags (whitespace split). |

## Defects
- D1, medium, NAVIS and Marine Technologies named as partners without confirmation of identity (fact_check 4a, 5a; copy_notes open item). Responsible: Director with Rahul. Fix: get Rahul's confirmation of the exact names before posting; he must tag the company pages manually.
- D2, low, Fugro, NAVIS and Marine Technologies "supported the stand" is Rahul's own statement in the brief and is not visible in the 2 photos I viewed. Responsible: Director. Fix: accept as USER-SUPPLIED, or check against the remaining photos.
- D3, low (optional), "ADIPEC 2026" repeated in the hook and the first sentence. Responsible: copywriter. Fix: optional, leave if the hook should stand alone.
- D4, low (account choice), personal vs company account still unanswered; the caption is personal only. Responsible: Director.

## What a marine-industry reader could object to
- Capitalised "NAVIS" and the bare "Marine Technologies" may not match the company's own naming (Navis Engineering); a wrong partner name is the main reputational risk.
- Partner list does not state each partner's role, so it cannot be misread as endorsement or class approval. No technical claims are made, so there is no DP technical-accuracy risk.
- "Clients" is not substantiated beyond Rahul's words; harmless for a thank-you.

## Verdict
PASS with open items: formatting, voice, dashes, bold, plain/final parity all pass. Hold publishing until D1 is confirmed by Rahul. Subjective copy quality is my opinion, not a performance prediction.

## Candidate lessons for the Director
- Verify bold with a Python NFKC round trip against the plain file and a block-range check, and exclude the emoji from the range test.
- Do not read "...TECHNOLOGIES" on a stand counter as Marine Technologies; it may be Sinor Marine Technologies.
