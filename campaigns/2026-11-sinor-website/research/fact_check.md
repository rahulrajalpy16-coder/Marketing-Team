# Fact check: Sinor website copy, version 1

Reviewer: fact-reviewer (independent, did not write the copy). Date checked: 2026-11-07.
Files checked: copy/home.md, solutions.md, service.md, about.md, contact.md (all under campaigns/2026-11-sinor-website/copy/).
Files read first: brain/brand-profile.md, brain/verified-facts.md, brain/preferences.md, brain/lessons-learned.md, .claude/skills/marine-technical-accuracy/SKILL.md, brief/brief.md, brief/strategy.md. Nothing under /tmp/work or campaigns/2026-11-sinor-site was read.
Status key: SUPPORTED (source named), UNSUPPORTED (no source found or supplied), OVERSTATED (true in part, reads as more than is known), NEEDS RAHUL CONFIRMATION, WRONG.

## Method limits (read this first)
- This session had no shell tool. I could not run grep. Checks (6) and (7) were done by reading all five files line by line, not by script. The Director should run a grep for FZCO, UAE, Middle East, Marine Services, sinor-logo, em dash and en dash on the final built HTML as a second check.
- I could not open the primary IMO text. The USCG copy of MSC.1/Circ.1580 and the USCG DP overview page returned HTTP 403 to WebFetch. The umwelt-online copy is a demo that stops before the DP definitions. The IMCA page returned 401. The USCG and IMO wording below is therefore taken from web search result summaries, not from the page itself, and is labelled "via search summary". The one page I did read directly is the IADC Lexicon entry, which quotes MSC.1/Circ.1580.
- Gate for everything: the STATED industry focus was given by Rahul for his employer (Sinor Marine Services Middle East FZCO), not for Sinor Marine Technologies. Every sentence about what the company does stays NEEDS RAHUL CONFIRMATION until he says it applies to Sinor Marine Technologies. I do not repeat this on every row; it is one blocking question (Q1 below).

## A. Technical definitions

| # | File and line | Claim | Status | Notes, rewording, source (date read 2026-11-07) |
|---|---|---|---|---|
| A1 | home.md 63; solutions.md 31 | DP: a vessel holds or maintains its position and heading with its thrusters | SUPPORTED, with a wording note | IMO MSC.1/Circ.1580 (16 June 2017), via search summary of the USCG-hosted text: a DP system automatically maintains position and/or heading (fixed location, relative location or predetermined track) by means of thruster force. USCG DP overview, via search summary: "a computer-based control system used to automatically maintain a vessel's heading and position without the use of mooring lines and/or anchors". Note: IMO says "position and/or heading", copy says "and". The copy is a fair plain-language version. Safer neutral wording: "automatically maintains a vessel's position and/or heading using its thrusters". URLs: https://www.dco.uscg.mil/Portals/9/OCSNCOE/References/DP-Guidance/IMO/MSC.1-Circ.1580.pdf ; https://www.dco.uscg.mil/OCSNCOE/DP/Overview/ (both 403 to direct fetch). |
| A2 | solutions.md 31 | "computer-controlled system that automatically maintains ... by using its thrusters and propellers" | SUPPORTED, minor note | USCG overview (via search summary): the thruster system may include main propellers and rudders, azimuth thrusters, tunnel thrusters and drop-down thrusters, so "thrusters and propellers" is right. Caption home.md 63 says only "its own thrusters"; acceptable, no change needed. Note that under the IMO text the full "DP system" also includes the power system and thruster system as well as the DP control system (IADC Lexicon attributes this to API RP 96 for the DP system, and to MSC.1/Circ.1580 for the DP control system). "computer-controlled system" is a simplification; "a computer-based control system" is closer to the USCG phrase. |
| A3 | solutions.md 31 | "It lets a vessel hold position without anchors or moorings." | SUPPORTED | USCG overview (via search summary): "without the use of mooring lines and/or anchors". Same URL as A1. |
| A4 | solutions.md 45 | "A DP system needs to know where the vessel is. Position reference systems supply that measurement." | SUPPORTED | USCG overview (via search summary): "In order for the DP System to keep a vessel in a desired position, it must utilize a Position Reference System (PRS)", position absolute or relative to a target. IADC Lexicon, read directly, quoting IMO MSC.1/Circ.1580: the DP control system comprises "position reference system(s)" among its components. https://iadclexicon.org/?p=59118 . Note: heading comes from a gyrocompass, not the PRS, so the copy is correct to speak of position only. |
| A5 | home.md 64, 83; solutions.md 45 | Reference systems are "the position measurements the vessel is held against" / "a DP system relies on" | SUPPORTED | Same sources as A4. Plain wording, ranks no type. |
| A6 | solutions.md 45 | "Different types work on different principles, so one type cannot simply stand in for another." | OVERSTATED (wording risk) | The first half is consistent with the skill (item 3) and with general DP practice. The second half can be read as "one type is never a substitute", yet DP practice deliberately uses several PRS of different principles together for redundancy, and IMO guidance for equipment class 2 and 3 expects at least three independent PRS available to the DP control system (MSC.1/Circ.1580 clause 3.4.8, via search summary; IMCA M 252, April 2020, via search summary). The "must not be interchanged" line in the skill is the repo's own unconfirmed reference note, not a cited source. Suggested neutral wording: "Different types work on different principles and suit different conditions." Sources: https://legacy.imca-int.com/?p=331715 (search summary only) ; the IMO PDF URL in A1. |
| A7 | solutions.md 73 | "On a DP vessel, the DP system sends thrust commands to these controls." (DP to thruster control relationship) | SUPPORTED in principle, wording note | USCG overview (via search summary): the controller works out the force and direction needed, "Thrusters then execute the commands given from the system". The copy says commands go to "controls". I found no source that states the interface in those words; architectures vary. Suggested neutral wording: "On a DP vessel, the DP system commands the thrusters to apply the force needed." |
| A8 | solutions.md 73; home.md 86 | "Propulsion and thruster controls command the units that move and position a vessel" / "Controls for the units that move and position a vessel" | UNSUPPORTED (low risk, generic) | No authoritative source read for this plain description. It is consistent with the USCG thruster description but is not a quoted definition. Acceptable as generic text if Rahul agrees. |
| A9 | home.md 84; solutions.md 59 | "Electrical and automation systems run and control equipment on board a vessel or offshore unit." | UNSUPPORTED (low risk, generic) | No source read. Plain description, no specifics. Acceptable as generic text. |
| A10 | solutions.md 59 | "They need to work reliably with the navigation, positioning and propulsion systems around them." | OVERSTATED | "reliably" is a quality adjective and reads as a promise. It is also a sector term with class-specific meaning (redundancy and fault tolerance under DP equipment classes). Remove. Suggested wording: "They need to work together with the navigation, positioning and propulsion systems around them." |
| A11 | solutions.md 87; home.md 87 | Integration "connects separate systems so they share information and work together"; "Bringing separate vessel systems together to work as one" | UNSUPPORTED (generic) with two soft spots | No source read. The Nautical Institute describes DP as "a vessel capability provided through the integration of a variety of individual systems and functions" (via search summary, https://www.nautinst.org/resource-library/technical-library/dynamic-positioning.html), which fits the idea but is not the same claim. "work as one" is stronger than "work together"; "It matters most where..." (solutions.md 87) is an unsourced superlative. Suggested: "Integration connects separate systems so they share information and work together on board. It applies where positioning, electrical, automation and propulsion systems have to exchange information." |
| A12 | solutions.md 100 | "An upgrade brings an existing system up to date. It can extend what a system does or replace parts that no longer meet the need." | UNSUPPORTED (generic) | No source. Plain meaning, no technical claim. Acceptable. |
| A13 | service.md 25 | "Commissioning brings a newly installed or upgraded system into service. It checks that the system works as intended on the vessel before handover." | UNSUPPORTED (generic), mild promise | No source read. "works as intended" and "before handover" describe a process Sinor may or may not follow. Suggested: "Commissioning is the testing and bringing into service of a newly installed or upgraded system." |
| A14 | service.md 30, 35 | "Service keeps installed systems in working order." "Technical support helps engineers and operators with questions and faults." | OVERSTATED (service wording) | "keeps ... in working order" reads as an outcome promise. Suggested: "Service covers the upkeep of installed systems." Technical support line is acceptable as a description of the activity, once Q1 is answered. |

## B. Adjectives and words that can read as a promise (check 4)
- solutions.md 59 "reliably": OVERSTATED, remove (A10).
- service.md 21 "Three stages keep a system working once it is on board": OVERSTATED. Suggested: "Three kinds of work follow supply." Also see C3 for "supply".
- home.md 66 "the whole system, supported": OVERSTATED. Implies full coverage of every system on board. Suggested: "Integration, commissioning and service."
- home.md 98, about.md 32 "It follows the system through its life on board" / "not only to delivery": OVERSTATED. Implies lifecycle support and that Sinor delivers equipment, neither stated. Suggested: "Work includes commissioning, service and technical support after installation."
- home.md 103, about.md 37 "Keep the system working after handover": OVERSTATED, same cause. Suggested: "Provide service and technical support after handover."
- solutions.md 87 "matters most": unsourced superlative, soften (A11).
- Words checked and not found as promises in what I read: no "leading", "best", "world class", "expert", "trusted", "proven", "guarantee", "24/7", "fast", "safe". "Automatically" is used only in the DP definition, where the IMO text uses it. "Computer-controlled" is acceptable (A2).

## C. Process and scope claims the copywriter said Rahul did not state (check 5)

| # | File and line | Claim | Status | Notes and rewording |
|---|---|---|---|---|
| C1 | home.md 100 to 103; about.md 34 to 37 | Four-step flow: Discover, Design, Install and commission, Support, in that order | NEEDS RAHUL CONFIRMATION | Rahul stated commissioning, service and technical support only. "Discover", "Design" and "Install" and the order are not stated. No outside source can confirm how this company works. Neutral fallback using only stated words: heading "What the work includes"; items "Integration", "Commissioning", "Service", "Technical support", with no order implied. |
| C2 | about.md 34, 35 | "Questions come before any proposal." "The plan covers how new equipment connects to existing systems." | NEEDS RAHUL CONFIRMATION | These describe the company's own working method and a sales sequence. Not stated, no source. Cut unless Rahul confirms. |
| C3 | home.md 98; service.md 21; service.md 20 "After supply"; about.md 32 | Wording that the company supplies equipment ("supply", "delivery", "Fit the equipment") | NEEDS RAHUL CONFIRMATION | The stated focus lists integration, upgrades, commissioning, service and support. It does not say Sinor supplies, sells or installs equipment. Brand profile line 19 says products and partnerships are TO BE SUPPLIED. Suggested: replace "supply" and "delivery" with "installation" only if confirmed, otherwise "After installation" is also unconfirmed; use "Commissioning, service and technical support". |
| C4 | about.md 9 (meta) | "how the work flows from discovery to support" | NEEDS RAHUL CONFIRMATION | Depends on C1. Neutral meta: "See what the company does: marine and offshore technology, from Dynamic Positioning to service." |
| C5 | solutions.md 104, 107 | "Upgrades to DP, reference, electrical, automation and propulsion control systems" (upgrades apply to every area) | NEEDS RAHUL CONFIRMATION | Copywriter flagged this. Rahul listed "upgrades" as one item in a flat list, not as a service within each area. |
| C6 | solutions.md 36 to 39, 50 to 52, 64 to 67, 78 to 81, 92 to 94, 104 to 106 | "What the work covers" lists repeat integration, upgrades, commissioning, service and technical support under each of the six areas | NEEDS RAHUL CONFIRMATION (not flagged by the copywriter) | The same issue as C5 applies to every list, not only Upgrades. A flat stated list does not prove each activity applies to each system (for example commissioning of electrical systems, or upgrades to reference systems). Either Rahul confirms the full matrix or each page shows only the area name plus the generic description. Also "Connecting new equipment to existing systems" (solutions.md 92) is not stated. |
| C7 | home.md 78, 79; solutions.md 15; brand-profile line 41 | "Six areas of marine and offshore technology" | OVERSTATED (derived structure) | Rahul's list has ten items: marine and offshore technology, DP, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support (brand-profile line 17). "Six areas" is a Director grouping, and integration and upgrades are activities rather than "areas of marine and offshore technology". Suggested: "The company's work includes:" with the list. The count of six is internally consistent across the copy (checked home.md 82 to 87, solutions.md 22). |
| C8 | about.md 21, 22; home.md 77; home.md 36 | Label "Industry focus as stated by the company" and public line "Industry focus as stated by the company, not independently verified" | NEEDS RAHUL CONFIRMATION | The label attributes the statement to Sinor Marine Technologies, whereas Rahul gave it for his employer. The disclaimer text is honest for a draft but is not suitable as final public copy. Remove once Q1 is answered. |

## D. Company name and forbidden identifiers (check 6)
Read-through result, all five files, not script-confirmed.
- Name: every public string reads "Sinor Marine Technologies" (titles, metas, H1s, header and footer, alt text, slots). I found no bare "Sinor" or "Sinor Marine" in public text. SUPPORTED by Rahul's statement of 2026-11-07, recorded in brain/brand-profile.md lines 40 to 41, with the caveat in verified-facts line 24 that this is stated, not independently verified.
- FZCO, UAE, Middle East, Marine Services, sinor-logo.png and the Services LinkedIn page do appear as words in the files, but only in author notes and build slot instructions, never in visitor-facing strings: home.md line 5 (names FZCO, Middle East, UAE as excluded), line 17 (names assets/brand/sinor-logo.png as not to be used), line 30 and contact.md line 87 (Services page "must NOT be used"), about.md line 4. Verdict: SUPPORTED (no visitor-facing leak). Risk: the builder must not copy these notes into HTML. A grep of the built HTML is recommended.
- UAE versus Singapore base: not mentioned in any public string; slots S23 and S30 hold it. SUPPORTED.
- No LinkedIn URL, logo file or entity line is used. SUPPORTED.

## E. Inventions check (check 7)
- Partner, dealership, certification (ISO), project, client, testimonial, product name, trademark: none found in the five files. SUPPORTED. The 15+ years, 100+ projects, 40+ countries stand figures are explicitly excluded (home.md 122).
- Year, number of staff, regional coverage, hours, response times: none stated. The only numerals are structural counts (six areas, four captions, three stages, three items) and character counts in notes. Character counts were not re-counted except the Home title (58, correct); the rest are UNVERIFIED but low importance.
- Email, phone, address, URL: none. contact.md uses name@example.com only as an error-message format example; this is a reserved example domain pattern and not a contact detail. SUPPORTED.
- Contact form: honest about not being connected (contact.md 18, 19, 69). SUPPORTED. Two inconsistencies to flag: (1) the header and band pills "Send an enquiry" and the meta (contact.md 8) invite an action that cannot complete; the notice mitigates this, but the site must not go public in this state. (2) contact.md 88, the collapse text "Use the form.", and service.md 55, "Use the Contact page to request support", would point visitors to a form that sends nothing if slots are removed before S27 is solved. Both are launch blockers, not fact errors.
- "Offshore units" (home.md 84, solutions.md 59): a standard sector term, consistent with the stated focus on marine and offshore technology. SUPPORTED by Rahul's stated focus, subject to Q1.

## F. Headlines (check 8)
The copy proposes one Home H1 with two alternates (home.md 49, 50) and four other page H1s. The task refers to five; I checked all seven.

| Headline | Status | Notes |
|---|---|---|
| "Hold position at sea" (home.md 49) | OVERSTATED | It is an imperative that reads as an outcome the company delivers, and "at sea" narrows DP, which is also used at offshore structures and nearshore. It is the generic DP idea, not a measured claim, as the copywriter says, but a visitor will read it as what Sinor does. Neutral: "Dynamic Positioning and marine systems". |
| "Marine technology, supported" (alternate) | SUPPORTED (conditional on Q1) | Matches the stated "marine and offshore technology" and "technical support". Least risky of the three. |
| "Systems that hold position" (alternate) | OVERSTATED | Implies Sinor makes or supplies the systems. Not stated (C3). |
| "Find your system" (solutions.md 14) | SUPPORTED | No factual claim. Implies the page has a match for any system; the intro line limits it to six areas. |
| "Service and support" (service.md 13) | SUPPORTED (conditional on Q1) | Service and technical support are stated. |
| "About Sinor Marine Technologies" (about.md 14) | SUPPORTED | Name stated by Rahul 2026-11-07. |
| "Contact Sinor Marine Technologies" (contact.md 13) | SUPPORTED | Same. |

## G. Verified versus not verified
Verified (with source, 2026-11-07):
1. DP definition in plain terms (A1 to A3), by search summaries of IMO MSC.1/Circ.1580 and USCG text, plus the IADC Lexicon page read directly for the DP control system. Confidence: good on meaning, wording not read at source.
2. DP needs a position reference system; PRS are a component of the DP control system (A4, A5). IADC page read directly; USCG via summary.
3. Thrusters carry out DP system commands (A7), USCG via summary.
4. Company name (D), as stated by Rahul only.
5. No forbidden identifiers or invented items in visitor-facing strings (D, E), by manual read only.

Not verified or not verifiable by me:
1. That the stated focus applies to Sinor Marine Technologies (Q1).
2. The four-step flow, the per-area activity lists, supply or installation as a service, and the "six areas" grouping (C1 to C7).
3. The direct wording of MSC.1/Circ.1580 clause 1.2 for "DP system" and "DP vessel" (primary pages blocked).
4. Generic descriptions A8, A9, A11 to A13 (no authoritative source read; plain-language, low risk).
5. Character counts in titles and metas other than Home title.

## H. Open questions for Rahul
Q1. Does the stated focus (DP, reference systems, marine electrical and automation, propulsion and thruster controls, integration, upgrades, commissioning, service, technical support) describe Sinor Marine Technologies?
Q2. Does Sinor Marine Technologies supply equipment, install it, or only integrate, commission and service? This decides the words "supply", "delivery", "fit".
Q3. Which of integration, upgrades, commissioning, service and support apply to which areas (C5, C6)?
Q4. Is the four-step flow (Discover, Design, Install and commission, Support) how the company works, or use only the stated words (C1, C2)?
Q5. Which headline is wanted, given the notes in section F?

## I. Proposed verified-facts entries (for the Director to add; I did not edit brain/)
| Fact | Source | Date checked |
|---|---|---|
| IMO MSC.1/Circ.1580 (Guidelines for vessels and units with dynamic positioning (DP) systems) was issued 16 June 2017 | https://iadclexicon.org/?p=59118 (read directly) | 2026-11-07 |
| Under MSC.1/Circ.1580 the DP control system comprises all control components and systems, hardware and software necessary to dynamically position the vessel, including computer or joystick system, sensors, control stations and displays, position reference system(s), cabling and networks | https://iadclexicon.org/?p=59118 (read directly) | 2026-11-07 |
| DP in plain terms: a computer-based system that automatically maintains a vessel's position and/or heading using thruster force, without mooring lines or anchors. Wording from search summaries of the IMO circular and USCG overview; primary pages returned 403, so re-confirm at source before quoting verbatim | https://www.dco.uscg.mil/OCSNCOE/DP/Overview/ ; https://www.dco.uscg.mil/Portals/9/OCSNCOE/References/DP-Guidance/IMO/MSC.1-Circ.1580.pdf | 2026-11-07 (partial) |
| A DP system uses a position reference system to know the vessel's position, absolute or relative to a target; the controller computes the force needed and the thrusters execute it. USCG, via search summary | https://www.dco.uscg.mil/OCSNCOE/DP/Overview/ | 2026-11-07 (partial) |
| DP vessels commonly use several position references together; for equipment class 2 and 3, at least three independent PRS are expected available to the DP control system. Via search summary of MSC.1/Circ.1580 clause 3.4.8 and IMCA M 252 (April 2020) | https://legacy.imca-int.com/?p=331715 | 2026-11-07 (partial) |
| Rahul's stated industry focus is NOT yet confirmed for Sinor Marine Technologies (it was given for Sinor Marine Services Middle East FZCO). Do not treat site copy about the company's scope as verified | brain/brand-profile.md; brief item 11 | 2026-11-07 |

## J. Candidate lessons for the Director
1. Government and class-society pages (dco.uscg.mil, imca-int.com) refuse WebFetch with 403 or 401 in this environment. For future DP checks, plan on search summaries plus the IADC Lexicon (fetchable) and label the confidence honestly, or ask Rahul for the PDF.
2. A flat stated capability list must not be turned into a service matrix per area. Copywriters flagged "upgrades" but the same issue sits in every "What the work covers" list.
3. Lifecycle and supply language ("supply", "delivery", "life on board", "keeps working") smuggles in claims about what the company sells and promises. Add these words to the copy review checklist next to "reliably".
4. Give fact-reviewers a shell or grep tool for identifier sweeps on copy and built HTML; this run had none, so check (6) is a manual read.
