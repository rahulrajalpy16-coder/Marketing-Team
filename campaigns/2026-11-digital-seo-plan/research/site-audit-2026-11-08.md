# Evidence log: sinormarine.com audit

Collected 2026-11-08 from public pages only (Firecrawl scrape with maxAge 0, curl). No client data used in any query. Status tags: VERIFIED (read in this task), NOT MEASURED, UNVERIFIED.

## A. Site facts (VERIFIED, 2026-11-08)
| # | Fact | How checked |
|---|------|-------------|
| A1 | Built on WordPress 6.9.11 with Elementor 4.3.5, Yoast SEO sitemaps, hosted on Hostinger (LiteSpeed). | Page metadata generator tags, sitemap footer, response headers |
| A2 | Canonical host is https://sinormarine.com. http to https and www to non-www both return 301 to it. Canonical tag on home points to https://sinormarine.com/. | curl -I chain, home HTML |
| A3 | robots.txt allows all and lists https://sinormarine.com/sitemap_index.xml. | curl |
| A4 | Page sitemap lists 16 URLs: home, projects, services, 5 service pages (navigation-systems, frequency-power-converter, thruster-control, electrical-solutions, marine-automation) plus dp-system, about, mt, navis, products, blog, contact, thank-you. | page-sitemap.xml |
| A5 | Blog has 1 post (sitemap lastmod 2026-03-12). Project entries: 3, with generic slugs (dp-2-retrofit-project, dp-2-upgrade-project, successful-project). | post-sitemap.xml, sms-project-sitemap.xml |
| A6 | /thank-you/ is listed in the sitemap. | page-sitemap.xml |
| A7 | DP page "Schedule Consultation" button links to /services/contact.html, which returns HTTP 404. | curl -L |
| A8 | Home page service card "Navigation Systems" links to /contact although /services/navigation-systems/ exists. Card "Electrical Solutions" links to /services/marine-automation/ although /services/electrical-solutions/ exists. | Home links list vs sitemap |
| A9 | Home title tag is 118 characters: "Sinor Marine Services Middle East FZCO | DP System & Dynamic Positioning System Services Dubai - Sinor Marine Services". Meta description is 171 characters. | Metadata, python len() |
| A10 | DP page title tag is "DP system - Sinor Marine Services". Its meta description is the first paragraph of the page. The scrape text began "DP Systems | Sinor Marine Technology" (older brand wording); the reviewer's fetch did not reproduce this, so recheck in a browser. | Scrape metadata and markdown |
| A11 | No JSON-LD structured data found in the served home HTML (count of application/ld+json = 0). One H1. 31 img tags, 29 without usable alt text on the home page (some may be decorative; corrected by the Phase 1 raw-HTML count in section F). | grep on fetched HTML |
| A12 | No Google Analytics, Tag Manager, Meta pixel or Clarity signature found in the served home HTML. This may load another way, so treat as UNVERIFIED until checked in a browser or Tag Assistant. | grep on fetched HTML |
| A13 | Home page services form lists "Fuel Monitoring" but no fuel monitoring page exists in the sitemap. Service list on home: DP Systems, Marine Automation, Electrical Solutions, Navigation Systems, Thruster Control System (Z-Thrust, PLC based), Frequency Power Converter. | Home markdown, sitemap |
| A14 | Contact block on home shows sales@, service@, support@ addresses, +971 4 665 7162, and a separate CTA to a named person's email and mobile. | Home markdown |
| A15 | An older domain https://www.sinor-marine.com returns HTTP 200, but on 2026-11-08 its home page output raw PHP warnings (a WordPress install, file paths exposed) instead of a normal page. A "SINOR MARINE TECHNOLOGIES" brochure PDF (July 2021) on that domain also returned HTTP 200. Relationship to Sinor Marine Services is UNVERIFIED (stand files mention "Sinor Marine Technologies" as SMT, USER-SUPPLIED). Reviewer fetch confirmed the PHP errors. UPDATE 2026-11-08: Rahul states it is a separate entity with no connection to sinormarine.com. | curl, search result URL, reviewer WebFetch |
| A16 | Home page image URLs include names such as WhatsApp-Image-2026-02-04-at-19.09.38 and ChatGPT-Image-Feb-4-2026, used as service card images. | Home scrape markdown |
| A17 | About page GM message quotes "Accuracy creates credibility. Credibility creates Trust" and names Naveen Thandarath, General Manager. About says "from 2024". | About scrape |
| A18 | Company address on the home page: P.O.Box 95842, 601, Al Nokitha Building, Hamariya Port, Dubai, UAE. | Home scrape |

## B. Claims on the site (VERIFIED as written, accuracy UNVERIFIED)
| Claim | Where (corrected after review) | Conflict |
|-------|-------|----------|
| "50+ Projects Completed" | Home, About, DP page | Stand panel said "100+ projects" (Rahul confirmed public use 2026-11-06). Public LinkedIn post says "8+ Dynamic Positioning (DP) upgrade projects" (different scope). |
| "15+ Years of DP Engineering Experience" | Home (Rahul confirmed 15+ for public use 2026-11-06) | About says "20+ Years Experience" and title "Engineering Reliable Marine Automation Solutions from 2024". |
| "40+ countries served" | Home, About, DP page | Consistent. |
| "50+ Team Members" | About | Not seen elsewhere. |
| "98% Client Satisfaction" | Home, DP page | No source seen. |
| "Compliant with DNV, ABS and Lloyd's Register DP requirements" and "type-approved DP systems across all classes" | DP page | No certificate or approval basis seen. Likely OEM level claims. |
| "24/7 Support", "Quality Assured", "Certified Engineers", "class-approved" DP solutions | Home. "Class-approved service providers" and "OEM-certified technicians": About | Not evidenced in this repo. ISO certificates also not seen (company's own invoice footer only). |

## C. Search results seen (2026-11-08, one session, location not set)
- LinkedIn snippets in the same search: company page text "will be exhibiting at ADIPEC 2026"; a post snippet "8+ Dynamic Positioning (DP) upgrade projects". Pages not opened on LinkedIn.
- Offshore Engineer magazine (oedigital.com/dynamic-positioning) appeared as a result in the first search.
- Query "Sinor Marine Services Middle East FZCO Dubai Dynamic Positioning": Sinor home page was result 1, company LinkedIn page 2, DP page 3. Brand queries are expected to favour the brand, so this proves little about non-brand ranking.
- Query "DP system upgrade retrofit UAE Dubai marine automation thruster control service company": Sinor DP page was result 1 in this one run. Others seen: Subsea Connect, Thrustmaster of Texas, Marine Technologies (OEM), Navis Engineering (OEM), ABS guide PDF, market-report sites. Single run, not a ranking study.
- UAE dynamic positioning market size: two sources disagree (USD 244.8 million for 2025 vs USD 470 million for 2025). NOT used in the plan.
- Other names seen in results, offering and location not verified: SMTS Marine Solutions LLC (smtsmarine.com), a UAE based propulsion control service engineer on LinkedIn.

## D. Not measured
- Core Web Vitals and Lighthouse scores: PageSpeed Insights API returned HTTP 429 (shared daily quota exceeded).
- Keyword volumes, difficulty, backlinks, competitor traffic: Ahrefs, Similarweb and Supermetrics connectors need Rahul to authorise them; no volume data exists in this plan.
- Search Console, GA4, LinkedIn analytics, Google Business Profile: no access, so no baseline.
- Company LinkedIn follower count and post performance: not read.

## E. Internal sources (no confidential content copied here)
- brain/brand-profile.md, brain/verified-facts.md, brain/preferences.md, brain/lessons-learned.md
- Claude-Agent-Team-SMS knowledge/company/SINOR_COMPANY_PROFILE.md and knowledge/technical/EQUIPMENT_SCOPE_CATALOGUE.md (service and equipment scope, used only at category level)

## F. Phase 1 raw-HTML evidence (2026-11-08)
- Title and meta description checked on all 16 pages: 12 pages have no meta description (only home, DP, thruster and frequency converter pages have one). Home has 29 of 31 image tags without alt text, /products/ has 1, other pages 0. No JSON-LD on any page.
- DP page meta description begins "DP Systems | Sinor Marine Technology" (raw HTML).
- Home images: 19 unique, total about 5.4 MB, two ChatGPT-Image PNGs of about 2.1 MB each. Partner strip shows 12 logos: Siemens, DEIF, Marine Technologies, Navis Engineering, Sonardyne, Fugro, Guidance Marine, SMT, Woodward, Vacon, Schneider Electric, ABB.
- Form dropdown options: DP Systems, Navigation Systems, Marine Automation, Fuel Monitoring, Electrical Solutions, Thruster Control System, Frequency Power Converter, Other.
- One exact-phrase search of the DP page wording found no other site with the same text.
