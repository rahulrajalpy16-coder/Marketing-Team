# Fact review 1: Sinor digital marketing and SEO plan

Reviewer: research-verification (independent of the producer). Date checked: 2026-11-08. Plan not edited.
Tools limits: WebFetch only. I could not read HTTP headers, so redirect chains (A2) and character counts from raw HTML were not independently re-measured. No grep tool, so the em dash check was a full visual read of the plan.

## Findings

| ID | Location in plan | Issue | Severity | Suggested correction |
|----|------------------|-------|----------|----------------------|
| F1 | Section 1, conclusion 2 | Quote "accuracy creates credibility" is attributed to "whose own leader says". No source in the audit log, verified-facts or brand-profile. | MAJOR | Remove the quote, or tag it USER-SUPPLIED with the source. Suggested: "In a safety-critical industry, credibility depends on accurate claims." |
| F2 | Section 2.1, LinkedIn bullet | "Real, current LinkedIn activity, including an ADIPEC 2026 announcement and a DP upgrade proof post (search results)". The audit log has no entry for an ADIPEC announcement. The only LinkedIn post cited is the "8+ DP upgrade projects" post in section B. LinkedIn was not opened (verified-facts). | MAJOR | Add an evidence row to the audit file, or tag UNVERIFIED: "Search snippets suggest recent LinkedIn activity (not opened, UNVERIFIED)". |
| F3 | Section 2.2 row 12 | Image file names "WhatsApp-Image" and "ChatGPT-Image" are not in the audit log. The inference "unprocessed phone photos and generated art" is speculation. | MAJOR | Add the evidence to section A of the audit (URLs seen), or delete the file-name detail and write "image weight not measured". |
| F4 | Sections 3 (decision 1), 4.1 and 1 | The plan treats 100+ projects, 15+ years and 40+ countries as undecided. verified-facts (2026-11-06) says Rahul confirmed these three stand-panel figures for public use. The plan only half-acknowledges this in 4.1 ("confirmed 15+ ... subject to decision 1"). Decision 1 then asks "which is true" and lists 100+ and 15+ as open. | MAJOR | Say that Rahul confirmed 100+ projects, 15+ years and 40+ countries on 2026-11-06. The conflict is that the website shows 50+ projects and 20+ years. Ask only about 50+ team, 98%, 24/7, class-approved, OEM-certified, and the "from 2024" wording. |
| F5 | Sections 2.2 row 13, 6.2, 7 | "Naveen" is used as a LinkedIn poster and as owner "N". The name appears in no brain file, so identity and role are unverified. | MAJOR | List it as an open question: "Who is Naveen (role, consent to be named)?" Or write "second Sinor spokesperson (TBC)". |
| F6 | Section 2.2 row 9 and section 5.2 (Legacy domain) | "A live sinor-marine.com site". My fetch of https://www.sinor-marine.com/ returned raw PHP errors from a WordPress install, not a PDF. This contradicts or complicates A15, which says it serves a 2021 brochure PDF. The audit may have checked a specific PDF URL. Relationship to Sinor is still UNVERIFIED. | MAJOR | Re-word: "sinor-marine.com is reachable but its home page showed server errors on 2026-11-08, and an older brochure exists. Relationship UNVERIFIED." Tell Rahul. The error output exposes server file paths, so ask whoever hosts it to look at it. |
| F7 | Section 2.2 row 3 and Phase 1 | Home Electrical card links to /services/marine-automation/ (confirmed). Navigation card links to relative /contact (confirmed). The plan fix list is correct. | n/a | none |
| F8 | Section 5.2, home title example | Example "DP Systems, Retrofit and Marine Automation, Dubai \| Sinor Marine" is 64 characters. The plan's own limit is "about 60". | MINOR | Shorten, for example "DP Systems and Marine Automation, Dubai \| Sinor Marine" (about 52). |
| F9 | Section 5.2 header vs section 7 | Phase 1 is "weeks 1 to 3", but the roadmap puts titles, structured data, Business Profile and speed fixes in weeks 3 to 4. | MINOR | Change the header to "weeks 1 to 4", or move tasks. |
| F10 | Section 1 and 6.2 | "LinkedIn (where this buyer group is reachable)" and 5.6 "Buyers increasingly ask AI tools technical questions" are unsourced generalisations. Section 4.2 itself says buyer behaviour is UNVERIFIED. | MINOR | Tag both PROPOSAL or UNVERIFIED. |
| F11 | Section 6.2 mix | The 40/25/15/10/10 content mix is not tagged PROPOSAL (cadence is). The sum is 100. | MINOR | Add "(PROPOSAL)" to the mix. |
| F12 | Section 5.5 | "Offshore Engineer magazine (OE Digital)" is not in the audit log. | MINOR | Add it to the audit log with its source URL, or tag UNVERIFIED. |
| F13 | Section 5.5 | "confirmed address ... as in the company profile". brand-profile.md and verified-facts do not hold the address. It is on the live home page (I read it). The Claude-Agent-Team-SMS profile was not read by me. | MINOR | Cite "shown on sinormarine.com home page, 2026-11-08". Note it is not yet in verified-facts. |
| F14 | Section 5.3 | "Z-Thrust" appears as a Sinor thruster-control product name. The home page does list "Thruster Control System (Z-Thrust, PLC based)" per the audit, but whether it is Sinor's own or third-party is unverified. "Inertial-aided DVL" and "radar-based reference options" have no evidence of being Sinor offers. The plan does say "confirm each is a real offer". | MINOR | Add "(product name as shown on site; ownership UNVERIFIED)" next to Z-Thrust. Mark DVL and radar references as examples only. |
| F15 | Section 5.4 topic 2 | The SPRINT-Nav and Ranger 2 USBL statement is sourced to EQUIPMENT_SCOPE_CATALOGUE in another repo, which I did not read. verified-facts supports only "SPRINT-Nav is a hybrid acoustic-inertial navigation instrument". The plan already says to re-verify. | MINOR | Mark UNVERIFIED (not read this review). |
| F16 | Section 5.4 topic 7 and 7 roadmap | The ADIPEC takeaways article is called "timely", but the roadmap publishes it in weeks 5 to 8 (from 7 December), over a month after the event ended on 5 November. | MINOR | Move it to weeks 3 to 4 or drop "timely". |
| F17 | Section 1 conclusion 1 and 2.2 row 4 | "3 project entries with generic names": I confirmed generic slugs (dp-2-retrofit-project, dp-2-upgrade-project, successful-project). Visible titles were not read. | MINOR | Write "generic URLs" instead of "generic names". |
| F18 | Audit B (not plan) | Claim locations are slightly off. "24/7 support", "Quality Assured" and "class-approved DP solutions" are on Home. "Class-approved service providers" and "OEM-certified technicians" are on About. On About I found no "24/7" and no "Quality Assured". The audit grouped them as "Home, About". | MINOR | Fix the audit table location column. The plan's decision 1 wording is still safe. |
| F19 | Audit A10 (plan row 6, 9) | "Body text begins 'DP Systems \| Sinor Marine Technology'". My fetch of the DP page showed heading "Dynamic Positioning Systems" and did not show this string. Not contradicted, not reproduced. | MINOR | Treat the "Sinor Marine Technology wording on page text" statement as UNVERIFIED by this review. Plan 5.2 task "remove wording" stays valid only if present. Recheck in a browser. |

No invented numbers, prices, budgets, keyword volumes, rankings or dates found. Budget is left unknown. Partner names match verified-facts exactly (Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine) with "supported us" wording, and no dealership or authorisation claim is made. The plan never states Sinor is an OEM dealer. The market-size figures are correctly not used.

Em dashes: none seen in the full read (visual check only). Hyphens in "Sinor Marine Services: ..." use a colon.

Date arithmetic: 2026-11-08 is a Sunday, so 2026-11-09 is a Monday. Weeks 1 to 2 = 9 to 22 Nov (Mon to Sun) correct. Weeks 3 to 4 = 23 Nov to 6 Dec correct. Weeks 5 to 8 = 7 Dec to 3 Jan correct. Weeks 9 to 12 = 4 Jan to 31 Jan correct. All 12 weeks add up. ADIPEC 2026 "2 to 5 November 2026" matches verified-facts (ADNEC, 2026-11-06).

## Statements CONFIRMED (source read 2026-11-08)

- Home title text is 118 characters (my count of the title text shown in the home fetch, https://sinormarine.com/). Meta description not shown in my fetch, so the 171 figure is not re-verified.
- DP page title "DP system - Sinor Marine Services"; Schedule Consultation href is ../contact.html, which resolves to /services/contact.html; that URL returns HTTP 404 (https://sinormarine.com/services/dp-system/, https://sinormarine.com/services/contact.html). A7 confirmed.
- Navigation card goes to /contact; Electrical Solutions card goes to /services/marine-automation/ (home page). A8 confirmed.
- Page sitemap has 16 URLs, including /thank-you/ and /services/electrical-solutions/ and /services/navigation-systems/ (https://sinormarine.com/page-sitemap.xml). A4, A6 confirmed. Sitemap index has 5 sitemaps (https://sinormarine.com/sitemap_index.xml).
- Blog has 1 post (lastmod 2026-03-12); 3 project entries with the slugs given (post-sitemap.xml, sms-project-sitemap.xml). A5 confirmed.
- robots.txt is a Yoast block, allows all, lists sitemap_index.xml (https://sinormarine.com/robots.txt). A3 confirmed.
- "Fuel Monitoring" is in the form dropdown and footer with no page in the sitemap. Six service names match A13. A13 confirmed.
- Contact block shows sales@, service@, support@, +971 4 665 7162, plus a named person's email and a mobile number in the CTA. A14 confirmed. Plan correctly prints none of them.
- Claims table: 50+ projects (Home, About, DP), 40+ countries (Home, About, DP), 98% satisfaction (Home, DP), 15+ years (Home), 20+ years and "from 2024" and 50+ team (About), DNV/ABS/Lloyd's compliance and "type-approved ... across all classes" (DP page), class-approved and OEM-certified wording (About), 24/7 (Home). Confirmed on the live pages, with the location notes in F18.
- No JSON-LD or analytics script visible in my fetches. This is weak evidence only because WebFetch returns rendered text. A11 and A12 not independently proved, and the plan correctly marks A12 UNVERIFIED.
- A2 (301 redirects) and A9/A11 character and alt counts: NOT re-verified by me (no header access). Treat as the producer's evidence.
- Brand and partner facts, ADIPEC dates, 100+/15+/40+ confirmation: brain/verified-facts.md lines 12, 22, 25, 26.
- Plan PROPOSAL splits: 40/35/15/10 = 100; mix 40/25/15/10/10 = 100.

## Proposed verified-facts entries (for the Director, not applied)

| Fact | Source | Date checked |
|------|--------|--------------|
| sinormarine.com page sitemap lists 16 URLs; blog has 1 post; 3 project entries | https://sinormarine.com/page-sitemap.xml ; /post-sitemap.xml ; /sms-project-sitemap.xml | 2026-11-08 |
| sinormarine.com DP page "Schedule Consultation" button points to ../contact.html (404). Home claims on the site: 50+ projects, 40+ countries, 98% satisfaction; About: 20+ years. All are the site's own claims, accuracy unverified | https://sinormarine.com/services/dp-system/ ; /services/contact.html ; /about/ | 2026-11-08 |
| Company address shown on sinormarine.com: 601, Al Nokitha Building, Hamariya Port, Dubai, UAE (needs Rahul confirmation) | https://sinormarine.com/ | 2026-11-08 |

## Candidate lessons for the Director

- Tag every sentence that cites search results or other repos with its evidence row. A plan should not carry facts that are absent from its own audit log (F2, F3, F12).
- Check the brain files before listing a figure as an open decision (F4).
- Do not name a person in a plan unless the name is in a brain file or flagged as an open question (F5).

## Verdict

NOT READY to show Rahul as is: 0 blockers, 5 MAJOR (F1 to F6 except F7, which is no-issue) and 11 MINOR findings. Fix F1 to F6 and F8 to F9, then it can be shown.
