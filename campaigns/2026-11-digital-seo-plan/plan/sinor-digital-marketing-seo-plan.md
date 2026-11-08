# Sinor Marine Services: Digital Marketing and SEO Plan

Prepared 2026-11-08 for Rahul Raj. Status: DRAFT for your decisions. Nothing has been published, sent or changed on the website.

Tags: VERIFIED (read this session, see research/site-audit-2026-11-08.md), USER-SUPPLIED, UNVERIFIED, PROPOSAL (my recommendation, not a fact).

---

## 1. The short version

Sinor sells high-value, technical, trust-driven work (DP systems, reference systems, thruster control, automation, commissioning, service) to a small number of buyers. A buyer is a vessel owner, operator, ship manager, technical superintendent or shipyard. So the goal is not traffic. The goal is **a steady flow of qualified RFQs and technical conversations**, measured from first touch to quotation.

Three conclusions from the audit:

1. **The website is a decent shell but a thin proof engine.** It is clean WordPress with correct canonical redirects and a sitemap. But it has 1 blog post, 3 project entries with generic URLs, a broken main button, mislinked service cards, no structured data and no analytics found in the served code. Search engines and buyers get little proof of expertise.
2. **The claims on the site contradict each other** (50+ vs 100+ projects, 15+ vs 20+ years, "from 2024", an unsourced 98% satisfaction figure). The About page itself says "Accuracy creates credibility. Credibility creates Trust" (GM message, read 2026-11-08), so inconsistent numbers undercut Sinor's own stated principle. This is the first thing to fix, before any marketing spend.
3. **Sinor's strongest asset is real expertise plus technology partners plus a live LinkedIn presence.** The plan therefore leans on expert-led content, partner co-marketing and LinkedIn (PROPOSAL: where this buyer group is likely reachable, UNVERIFIED for Sinor), supported by SEO that captures people already searching. Paid ads are a small, measured test, not the engine.

Recommended order: **fix trust and measurement (weeks 1 to 4), build proof content (weeks 5 to 8), then scale what the data shows works (weeks 9 to 12).**

---

## 2. Where Sinor stands today (audit findings)

All VERIFIED 2026-11-08 unless marked. Evidence IDs refer to the audit file.

### 2.1 What is working
- Canonical setup is correct: http and www both 301 to https://sinormarine.com (A2).
- Yoast sitemap and robots.txt in place, nothing blocked (A3).
- Brand queries return Sinor first (home, LinkedIn page, DP page). In one generic DP retrofit query the DP page also appeared first, but that is a single run (section C of the audit), not a ranking study.
- Clear service structure: DP, automation, electrical, navigation, thruster control, frequency converter (A13).
- Search snippets show recent company LinkedIn activity, including an ADIPEC 2026 exhibiting announcement and a DP upgrade proof post (audit section C). The pages were not opened on LinkedIn, so treat this as UNVERIFIED.
- Your own ADIPEC 2026 thank-you assets and a verified partner list already exist in this repo.

### 2.2 Problems, ranked by impact
| # | Issue | Evidence | Why it matters |
|---|-------|----------|----------------|
| 1 | Conflicting company claims | Audit section B | Buyers and class-conscious clients notice. Also a legal and reputational risk if a number cannot be backed. |
| 2 | Main DP page CTA goes to a 404 | A7 | The best-ranking service page loses its enquiry button. |
| 3 | Mislinked service cards (Navigation, Electrical) | A8 | Visitors miss dedicated pages that exist. |
| 4 | Almost no proof content | A5 | One post, three project entries with generic URLs. Weak E-E-A-T and nothing to rank for beyond service pages. |
| 5 | No analytics or conversion tracking seen | A12 (UNVERIFIED, confirm in browser) | Without it, no baseline, no ROI, no learning. |
| 6 | Weak titles and descriptions | A9, A10 | Home title is 118 characters (will be cut off). DP page title is "DP system - Sinor Marine Services". |
| 7 | No structured data seen | A11 | Misses rich results and clearer entity signals for search and AI answers. |
| 8 | Thank-you page in the sitemap | A6 | Invites indexing of a conversion page and muddies reporting. |
| 9 | Legacy brand wording and an older domain | A10, A15 | sinor-marine.com is reachable, and on 2026-11-08 its home page showed raw PHP warnings that expose server file paths. A 2021 "Sinor Marine Technologies" brochure exists on it. Older "Sinor Marine Technology" wording appeared in the DP page text in one scrape (not reproduced by the reviewer, recheck in a browser). Relationship to Sinor UNVERIFIED. Whoever hosts that site should look at the errors. |
| 10 | Empty image alt text on most images | A11 | Lost image search and accessibility value. |
| 11 | "Fuel Monitoring" offered in the form, no page | A13 | Demand signal with no landing page, or an offer that is not real. |
| 12 | Core Web Vitals unknown | Audit section D | Possibly heavy images. Several image URLs on the home page contain "WhatsApp-Image" or "ChatGPT-Image" (audit A16), which suggests unprocessed images, but this is an inference. NOT MEASURED. |
| 13 | A named person's mobile and email on the home CTA | A14 | Enquiries depend on one inbox. Use the shared sales address plus a form. |

---

## 3. Decisions I need from you (answer on your phone, short)

I proceeded with assumptions so none of these block the plan.

1. **One official set of claims.** You confirmed on 2026-11-06 that 100+ projects, 15+ years of DP engineering and 40+ countries may be used publicly. The website still shows 50+ projects and, on the About page, 20+ years, so please say which the site should carry. Still open: team size (50+ on About), "98% client satisfaction" (backed by a survey, or remove?), "from 2024" on the About page, and whether "24/7 support", "class-approved service provider" and "OEM-certified technicians" are accurate. Until answered, my plan treats the open ones as UNVERIFIED and does not use them in new copy.
2. **Is sinor-marine.com (Sinor Marine Technologies, 2021 brochure) yours?** If yes, we redirect or consolidate. If no, we add brand disambiguation.
3. **Priority services and markets.** My assumption (PROPOSAL): DP upgrades and retrofits, reference systems (supply, installation, commissioning), thruster control and service support, for UAE first, then GCC, then Indian Ocean and Far East operators working in the Gulf.
4. **Budget for paid tests.** Amount unknown. The plan gives percentage splits, not figures.
5. **Who edits the website** (you, a web person, an agency)? I draft; someone with login publishes after your approval.
6. **Posting voices.** The About page names Naveen Thandarath as General Manager. Is he happy to post on LinkedIn and be named as an author? Which engineers may be named? I wrote "Naveen" into the plan as a proposed second voice only.

---

## 4. Positioning and audience

### 4.1 Positioning (PROPOSAL, for your edit)
"DP and marine control specialists for offshore vessels: retrofit, reference systems, commissioning and service, from Dubai."

Proof pillars: engineering depth (15+ years DP engineering, confirmed by you 2026-11-06 for public use; the site must be aligned to it, see decision 1), technology partners who support Sinor (Sonardyne, Fugro, Navis Engineering, Marine Technologies, Guidance Marine, per your 2026-11-06 confirmation, wording "supported us", no dealership claims), hands-on delivery, and responsiveness.

Tone follows brain/brand-profile.md: company account confident and accurate, personal account modest and relationship-led. No "proud", "thrilled" or "delighted" openers.

### 4.2 Buyer groups
| Group | What they search or care about | Best channels |
|-------|-------------------------------|---------------|
| Technical superintendents, fleet managers | Reliable DP upgrade or fault support, downtime, class acceptance | LinkedIn, Google search, email, trade media |
| Vessel owners and operators (OSV, AHTS, survey, cable lay and similar) | Cost of retrofit vs replacement, lead time, who can mobilise | LinkedIn, Google search, WhatsApp, events |
| Ship managers and procurement | Supplier credibility, documentation, response time | Website proof pages, email, LinkedIn |
| Shipyards and integrators | Interface and commissioning capability | LinkedIn, direct outreach, partner introductions |
| OEMs and partners (Sonardyne, Navis Engineering, Marine Technologies, Guidance Marine, Fugro) | Visibility of joint work | Partner co-marketing (needs their approval) |

Buyer behaviour is UNVERIFIED for Sinor specifically. First-party evidence from your own enquiries (see section 8) should refine this within 60 days.

---

## 5. SEO plan

### 5.1 Principles
- Win **intent-rich, low-volume** searches. A few right buyers beat many wrong visitors.
- Every page needs a technical expert's accuracy. Marine technical content is drafted by the marine-technical-engineer agent and fact-checked against OEM documents before publication (marine-technical-accuracy skill). No claim about class, compatibility or performance without a source.
- Content must be **experience-based** (what Sinor engineers actually do), which is also what search engines and AI answer tools reward.
- Keyword volumes are UNKNOWN here. Authorise Ahrefs, Similarweb or Supermetrics, or export from Google Search Console, and I will add volumes and difficulty.

### 5.2 Phase 1: technical fixes (weeks 1 to 4, mostly small web tasks)
| Task | Detail |
|------|--------|
| Fix 404 CTA | Point the DP page button (and any other /services/contact.html links) to /contact/. |
| Fix service card links | Navigation card to /services/navigation-systems/, Electrical card to /services/electrical-solutions/. |
| Rewrite titles and descriptions | Titles up to about 60 characters, descriptions up to about 155. Example home title (PROPOSAL, 54 characters): "DP Systems and Marine Automation, Dubai | Sinor Marine". |
| Thank-you page | Set to noindex, remove from sitemap, use it as the conversion event. |
| Structured data | Add Organization, ProfessionalService with the Hamariya Port address, Service for each service page, FAQPage where FAQs exist, Article for posts. Validate in Google's Rich Results Test. |
| Image alt text and weight | Descriptive alt text on informative images. Prefer real project photography or clean graphics over generated art, compressed, WebP where possible. Check the largest images first. |
| Measure speed | Run PageSpeed Insights or Search Console Core Web Vitals (my attempt hit a quota limit). Fix the worst offenders. |
| Analytics | Install GA4 and Google Search Console, verify the domain, submit the sitemap. Confirm whether tracking already exists. |
| Shared enquiry path | Contact form with fields that qualify the lead (see 8.2), sales@ shared inbox, click-to-call and WhatsApp click tracking. |
| Legacy domain | If sinor-marine.com is yours, fix its server errors and 301 it to the right pages. Remove "Sinor Marine Technology" wording from page text if it is present. |
| Resolve "Fuel Monitoring" | Build a page if it is a real offer, otherwise remove it from the form. |

### 5.3 Phase 2: on-page rebuild of money pages (weeks 3 to 8)
Each service page gets: a clear promise in the H1, who it is for, scope (what Sinor does and does not do), typical process (survey, design, supply, install, commission, trials, handover), supporting partner technology, an FAQ of 5 to 8 real questions, a case study link, and one clear next step.

Pages to build or expand (PROPOSAL; confirm each is a real Sinor offer first):
| Page | Primary intent |
|------|----------------|
| DP system upgrade and retrofit | "dp retrofit", "dp system upgrade", "dp2 retrofit" (volumes UNKNOWN) |
| DP reference systems: supply, installation, commissioning | "dp reference system installation", USBL, inertial-aided DVL and radar-based reference options (examples only, confirm which Sinor offers) |
| Thruster control and manoeuvring control ("Z-Thrust" is the product name shown on the site, ownership UNVERIFIED) | "thruster control retrofit" |
| Marine automation and electrical | "vessel automation upgrade Dubai" |
| Commissioning, sea trials and service support | "dp commissioning", "marine service engineers Dubai" |
| Technology partners hub | Navis Engineering, Marine Technologies, Sonardyne, Guidance Marine, Fugro (each with partner approval and without dealership claims) |
| Vessel types served | OSV, AHTS, survey, cable lay and others where Sinor has real work |
| Case studies | Anonymised unless the client approves naming |

Brand-plus-product searches (for example a specific Sonardyne or Navis product name) are valuable but carry a claims risk. Create them only as "installation and integration" content and only after you confirm what Sinor may say about its relationship with each OEM.

### 5.4 Phase 3: content engine (weeks 5 onward)
Cadence PROPOSAL: 2 articles a month plus 1 case study a quarter. Each article is reused on LinkedIn, in the email newsletter and as a short video script.

Starter topics (informational and buyer-guide intent). Technical content to be written by the marine-technical-engineer agent and verified by research-verification against OEM and class documents before it goes live:
1. What to check before a DP system retrofit (decision checklist for superintendents).
2. DP reference systems explained in plain language: when acoustic, inertial or radar-based references make sense. Use only OEM-verified statements (for example, Sinor's own earlier proposals, summarised in the other repo's EQUIPMENT_SCOPE_CATALOGUE, repeat Sonardyne's guidance that SPRINT-Nav suits shallow water and Ranger 2 USBL suits deeper water or ROV and diver tracking. That statement is UNVERIFIED here and must be re-verified against current Sonardyne datasheets before publishing).
3. DP retrofit versus replacement: how to frame the decision.
4. What happens during DP commissioning and trials (timeline, who does what).
5. Thruster control upgrades: symptoms that mean it is time.
6. Lessons from a DP upgrade (anonymised, your own project, with client permission).
7. ADIPEC 2026 takeaways for DP and automation (the event ran 2 to 5 November 2026, so publish this first, in weeks 3 to 4).
8. Lead times and mobilisation: what operators in the Gulf should plan for (only with figures Sinor confirms; quotation lead times are historical and must be re-confirmed).

Each article: author byline of a named Sinor engineer (with consent), date, last-reviewed date, sources cited, and an explicit "talk to an engineer" call to action.

### 5.5 Authority and local
- **Google Business Profile** for Hamariya Port, Dubai (verify as a service business, correct categories, photos, services). Add Bing Places and Apple Business Connect.
- **Consistent business details everywhere** (name, address, phone), using the address shown on the sinormarine.com home page (601, Al Nokitha Building, Hamariya Port, Dubai), which you confirmed to the earlier team on 2026-10-20. It is not yet in this repo's verified-facts.
- **Partner links:** ask each technology partner about a listing or news mention on their site (their decision, not ours).
- **Industry mentions:** one expert quote or guest article a quarter in marine and offshore trade media. Candidate title seen in search results (audit section C): Offshore Engineer magazine (OE Digital). Build the full target list from verified sources before pitching.
- **Event pages:** a short page per event attended (ADIPEC 2026 first) with photos, which also feeds backlinks from organiser and partner sites.
- No paid link schemes, no bulk directory spam.

### 5.6 Visibility in AI answer tools
Buyers may increasingly ask AI tools technical questions (PROPOSAL assumption, UNVERIFIED for this market). The same discipline helps either way: plain definitions, FAQ sections, named expert authors, dated and sourced pages, structured data, consistent company details, and presence on LinkedIn and partner sites. No tricks. This is UNVERIFIED as a measurable channel for Sinor, so track it manually: ask five buyer-style questions each month and log whether Sinor appears.

---

## 6. Digital marketing plan

### 6.1 Channel roles
| Channel | Role | Priority | Notes |
|---------|------|----------|-------|
| Website and SEO | Capture and convert intent, host proof | 1 | Sections 5 and 8 |
| LinkedIn (company page, Rahul, Naveen, engineers) | Reach and trust with the buyer group | 1 | Section 6.2 |
| Email (permission based) | Nurture existing contacts and quote follow-up | 2 | Section 6.3 |
| Partner co-marketing | Borrowed credibility and reach | 2 | With partner approval |
| Events (follow-up engine) | Turn meetings into pipeline | 2 | Section 6.4 |
| Google Search ads | Fast test of high-intent terms | 3 | Small, measured |
| LinkedIn ads | Account-based reach to named companies and job titles | 3 | After organic content exists |
| YouTube and short video | Explainers and project stories | 3 | Reuse stand and project footage |
| WhatsApp Business | Fast enquiry channel common in the region | 3 | Click-to-chat tracked |

### 6.2 LinkedIn (the main organic engine)
- **Cadence (PROPOSAL):** company page 3 posts a week, Rahul 2, Naveen 1, engineers occasionally as guest authors. Employees share company posts.
- **Mix (PROPOSAL):** 40% proof (projects, installs, commissioning), 25% technical teaching, 15% partners, 10% people and culture, 10% direct offers.
- **Rules from the brain files:** company voice confident and accurate, personal voice modest. Bold uses scripts/unicode_bold.py with a plain-text version supplied. Partner names written in full. No claims about equipment ownership unless confirmed (lesson from the ADIPEC job).
- **Per post checklist:** one idea, one proof point, one invitation (comment, message or enquire). Facts checked by fact-reviewer before publishing.
- **Company page hygiene:** banner and tagline matching the site, services section, featured post, link to the contact page with UTM tags, "Showcase" content for partners.
- **Unknown:** follower counts and past performance. Send me an analytics export and I will set a real baseline.
- **Approval:** drafting is pre-approved. **Publishing or scheduling anything needs your explicit approval.**

### 6.3 Email and follow-up
- Start with people who already know Sinor: existing clients, quotation recipients, ADIPEC contacts. Confirm each contact can be emailed for marketing. Check UAE personal data protection rules and GDPR for any EU contacts. I am not giving legal advice, so have someone confirm before a first campaign.
- **ADIPEC follow-up this week:** a personal short note to each stand contact within days of the event, plus a thank-you post (the drafts already exist in campaigns/2026-11-adipec26-thanks).
- **Sequences (PROPOSAL):** (1) new contact, 3 emails over 3 weeks, each with one useful technical resource; (2) quotation follow-up, 3 touches at sensible intervals; (3) quarterly newsletter. Draft with the marketing:email-sequence skill when you approve.
- Sending any email or message outside this session needs your approval.

### 6.4 Events and partners
- Build an events calendar for the next 12 months from organiser sites. Dates are NOT included here because none were verified this session.
- For each event: pre-event outreach, a booking page or a calendar link, on-stand content capture plan, 48-hour follow-up, 2-week content recap (post, article, email).
- Offer each partner a simple co-marketing menu: joint LinkedIn post, case study (with client approval), joint webinar or technical note. Their approval is required for anything with their name or logo, and you control the wording.

### 6.5 Paid media (small, measured test, after the website is fixed)
- Send no paid traffic to a page with broken buttons or no tracking. Start only after Phase 1 is done and conversion tracking is verified.
- **Google Search:** exact and phrase match on service and retrofit terms, GCC targeting first, negative keywords (jobs, courses, free, training), call and form conversions. Check search terms weekly.
- **LinkedIn:** target named operator companies and relevant job titles (superintendent, fleet manager, marine manager, DP engineer). Promote the best organic posts and one downloadable guide.
- **Split of whatever budget you set (PROPOSAL):** 40% Google Search, 35% LinkedIn, 15% retargeting and content promotion, 10% reserve for new tests. Review after 30 days of data.
- Success is judged on qualified RFQs and cost per qualified RFQ, not clicks.

---

## 7. 90-day roadmap

Start date assumed: week of 2026-11-09. Owners: R = Rahul, N = Naveen, W = web editor, E = Sinor engineer, M = marketing team (me and specialist agents).

### Weeks 1 to 2 (9 to 22 November): decide, fix, measure
| Task | Owner |
|------|-------|
| Answer the five decisions in section 3 | R, N |
| ADIPEC follow-up to every stand contact, thank-you post | R, M drafts |
| Fix the 404 CTA and the two mislinked cards | W |
| Install and verify GA4, Search Console, GA4 conversion events | W, M specifies |
| Set up the lead log (section 8.2) | R, M |
| Export LinkedIn analytics and Search Console data to me for baseline | R |
| Agree the single official claim set and update home, about and DP pages | R, N, W |

### Weeks 3 to 4 (23 November to 6 December): foundations
| Task | Owner |
|------|-------|
| New titles and descriptions for all 16 pages, thank-you noindex | W, M drafts |
| Structured data and image alt text | W |
| Google Business Profile, Bing Places, Apple Business Connect | R or W |
| Page speed measurement and fixes | W |
| First two cornerstone pages drafted (DP retrofit, reference systems) | M, E reviews |
| ADIPEC 2026 takeaways article (topic 7), while the event is fresh | M, E reviews, W |
| LinkedIn calendar for 8 weeks drafted and approved | M, R |

### Weeks 5 to 8 (7 December to 3 January): proof and content
| Task | Owner |
|------|-------|
| Publish cornerstone pages and partner hub (with partner approval) | W |
| Publish 2 more articles (topics 1 and 2 in 5.4) | M, E, W |
| One anonymised case study with client permission | E, M |
| Partner outreach for co-marketing and listings | R |
| Email sequence 1 and 2 drafted, contact permission confirmed | M, R |
| Small Google Search test begins only if tracking verified | M |

### Weeks 9 to 12 (4 January to 31 January): learn and scale
| Task | Owner |
|------|-------|
| First proper review against baseline (section 9) | M, R |
| Double down on what produced enquiries, stop what did not | R, M |
| Outreach for trade media quote or guest article | R, M |
| Events calendar built and booked for the year | R, N |
| Month 4 to 6 plan agreed | R, M |

### Months 4 to 12 (PROPOSAL)
Add vessel-type and region pages where there is real work; a downloadable guide for lead capture; quarterly case studies; a video series from project footage; LinkedIn ABM campaigns by named account; review Arabic or other language pages only if enquiry data justifies it; yearly site refresh and claims audit.

---

## 8. Lead handling and funnel

### 8.1 Funnel
Visit or social touch, then enquiry (form, call, email, WhatsApp), then qualified RFQ, then quotation issued, then won or lost. Marketing owns the first two stages. Sales owns the rest. Both use the same lead record.

### 8.2 Enquiry form fields that qualify (PROPOSAL)
Name, company, role, email, phone or WhatsApp, vessel type, service needed (dropdown matching real offers), location of vessel, timeline, short description. Required fields kept few for mobile.

### 8.3 Response standard
Acknowledge every enquiry the same business day. Name one owner per lead. Log source (UTM, referrer or "event"). Close the loop in the lead log after the quotation outcome.

### 8.4 Join to the existing records
The Executive Team repo already holds quotation and client records. PROPOSAL: add a `source` field to each quotation record so won and lost work can be traced to a channel. That means changing tools in that repo, so it needs your approval and is not done.

### 8.5 Case study pipeline
Sinor's own library of delivered work is the richest content source. For each candidate project: client permission in writing, remove all commercial data, technical review, then publish. Never reuse client names, prices or commercial terms without permission. (This repo may be public, so none of those details are stored here.)

---

## 9. Measurement

### 9.1 Set up first
GA4 with these events: form submission, click to call, click to email, click to WhatsApp, document download, thank-you page view. Google Search Console. UTM naming rule: source, medium, campaign in lowercase, for example utm_source=linkedin&utm_medium=social&utm_campaign=2026-11-adipec-followup. A lead log (sheet) with the fields in 8.2.

### 9.2 Metrics
| Level | Metric | Read from |
|-------|--------|-----------|
| Activity (leading) | Pages fixed, pages published, posts published, outreach sent | Plan tracker |
| Visibility | Search impressions, non-brand clicks, branded search, LinkedIn impressions and followers, profile views | Search Console, LinkedIn |
| Engagement | Engagement rate on LinkedIn, time on key pages, scroll depth on service pages | LinkedIn, GA4 |
| Conversion | Enquiries by source, enquiry-to-qualified rate | GA4, lead log |
| Business | Qualified RFQs, quotations issued, won value, cost per qualified RFQ | Lead log, records |

### 9.3 Targets
**No numeric outcome targets are set yet, on purpose.** There is no baseline, and inventing one would break the "never invent metrics" rule. Plan: collect 60 days of baseline from the setup in 9.1, then you and I set targets for each metric. Activity targets (pages and posts published) are in the roadmap and can be judged right away.

### 9.4 Reporting
Monthly one-page report (marketing:performance-report skill): what we did, what changed, what we learn, next month. Only real numbers from your accounts. Anything not measured is labelled NOT MEASURED.

---

## 10. Risks and guardrails
| Risk | Control |
|------|---------|
| Unsupported or inconsistent claims | One approved claim set (decision 1). Fact-reviewer checks every public item. |
| Wrong technical statement damages credibility | Engineer writes, research-verification checks sources, QA reviews. |
| Partner or client names used without consent | Written approval first. Wording "supported us", no dealership claims. |
| Confidential data in a possibly public repo | No client names, prices or terms in this repo. Confirm repo visibility. |
| Paid spend without tracking | Spend only after conversion tracking is verified. |
| Email rules | Confirm consent and legal basis before sending. |
| Single points of failure (one inbox, one poster) | Shared inbox, three LinkedIn voices, documented process. |
| Over-reliance on AI-written content | Named engineer reviews every technical article. |

---

## 11. Effort estimate (PROPOSAL, not measured)
Rahul about 2 to 3 hours a week (approvals, partner and client conversations, posting as himself). Engineers about 1 to 2 hours a week for reviews and article input. Web editor about 4 to 6 hours a week in weeks 1 to 8, then about 2. Marketing team drafts, research, QA and reporting. These are planning assumptions, adjust to reality after month one.

---

## 12. What was not done and why
- No keyword volumes, difficulty, backlinks or competitor traffic: Ahrefs, Similarweb and Supermetrics need your authorisation in Claude settings (connectors). I cannot start that sign-in myself.
- No Core Web Vitals scores: PageSpeed Insights quota error.
- No baseline traffic, rankings or LinkedIn numbers: no access to Search Console, GA4 or LinkedIn analytics.
- Competitors seen only in search snippets. No competitive benchmark was produced.
- The two UAE DP market-size figures found disagree widely (USD 244.8 million and USD 470 million for 2025), so neither is used.

---

## Simplified explanation
Sinor sells specialist DP and marine control work to a small group of serious buyers. Those buyers choose people they trust, so the plan is about proving Sinor is trustworthy and easy to contact. First, fix the website's broken button and the numbers that disagree with each other, and install tracking. Then publish real expert articles, project stories and partner posts on the website and LinkedIn so Google and buyers see the expertise. Only after that, try a small amount of paid advertising and keep what brings real quotation requests. We measure success by how many real RFQs come in and which channel they came from, and we set numeric targets after 60 days of honest baseline data.
