---
name: marine-technical-accuracy
description: Use when verifying or writing marine, offshore, Dynamic Positioning (DP), position reference, propulsion, thruster, marine electrical or automation claims and terminology, in posts, emails, quotations or proposals. Prevents invented specifications, certifications and capabilities.
---

# Marine technical accuracy

Data root: where this skill says `<MARKETING_ROOT>`, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/workspace.py" root marketing`. If there is no workspace (for example in chat), keep the fact-check list in the reply instead of a file.

1. Establish the claim set from Rahul's supplied material first. Do not add products, partners, specifications, certifications or project names that are not in the source or in `<MARKETING_ROOT>/brain/verified-facts.md`.
2. Check each term against a reliable source: manufacturer documentation, classification society or IMO/IMCA material, or an official company page. Record claim, verdict, source URL or file, and date checked.
3. Terminology care: Dynamic Positioning (DP) and DP classes are defined by IMO MSC.1/Circ.1580 and class rules; position reference systems (for example DGNSS, HPR, laser-based or taut-wire systems) differ in principle and must not be interchanged; do not state a vessel's DP class, a system's accuracy or a certification unless a source supports it.
4. Keep capitalization and naming exactly as the owner writes it (product names, partner names, vessel names). When uncertain, flag it as an open question for Rahul instead of fixing it silently.
5. Never describe capabilities the footage or document does not show. No fake demonstrations.
6. Do not publish client names, vessel details, locations or commercial terms unless Rahul has authorized it for this use.
7. Return unverified items as "unverified" in the fact-check file and let the director or supervisor raise them in the handoff.

Note: item 3 contains reference knowledge to be confirmed against current official documents on first use; the fact-reviewer must cite sources and log them in `<MARKETING_ROOT>/brain/verified-facts.md`.
