# Retro: Sinor products brochure (2026-11-11), draft v1

## What was asked
Detailed A4 products brochure: all package systems, equipment and spares as individual items, each with photo and description, in the style of the Sinor profile brochure. Later: take products from the job register, take images online, ask Rahul for any image that is unavailable.

## What happened
- 40 minutes were lost looking for the register (not in any repo or under that name in Drive; it was a chat attachment) and I opened unrelated personal files in a mixed Drive dump by accident.
- Register mined by frequency: 69 candidate items, 66 carried into the draft (3 had no official source at all).
- 5 Firecrawl discovery agents found descriptions and image URLs; the container network blocked every image host, so exact hosts were approved in two batches of 20 or fewer.
- 41 of 69 images downloaded, 33 were correct after viewing; 36 cards need a photo from Rahul.
- Independent QA: pass with defects; majors fixed (self-reviewed).
- Not met: Part 10 style research. The catalogue-layout agent could not read any page (hosts blocked). Layout follows Sinor's own profile brochure plus design judgement only.

## Learning loop
A (applied now): image credit sheet, images-needed list, media locations updated, discovery records saved.
B (provisional lessons added to brain/lessons-learned.md): register search and Drive hygiene; Firecrawl-first image workflow and host batches; no browser-header retries on 403; view every image; Rahul's "ask me for unavailable images" rule; subagents need Firecrawl for research.
C (proposed, need approval): P-005 new skill product-catalogue-brochure; P-006 give platform-researcher the Firecrawl tools.

## Open questions for Rahul
See handoff message: authorised-partner wording, installation wording, maker/model confirmations, photos for 36 cards, whether to keep the allowed image hosts in the environment.

## Update: draft v2 (same day)
Rahul restructured the brochure (DP Systems, Position Reference Systems, Position Reference Sensors incl. MRU B1 and B2, then the rest) and asked for more photos. Done: new section order and DP pages, MRU-B1, B1.1, B2 cards, 35 new photo candidates fetched after 3 more host approvals, 48 of 64 cards now carry a photo. Independent QA v2 found 6 majors, all fixed or removed (fixes_v2_1.md).
Mistakes worth keeping: (1) my download script used hostnames as agents reported them, so www hosts were skipped and a maker photo of the wrong radar variant was used; (2) a first reseller photo carried a competitor watermark; (3) Firecrawl credits ran out so round 2 search depth was thin; (4) I wrote "SMT = Specialist Marine Technologies" from a web page against Rahul's own stated meaning in verified-facts.md: check verified-facts before printing a maker name.
Learning loop: lessons added (hostnames, credits, restructure wording). Proposed P-005 and P-006 stand; add to P-005 "use urlparse hostnames and check verified-facts for maker names".
