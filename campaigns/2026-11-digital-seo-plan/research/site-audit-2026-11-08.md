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
| A10 | DP page title tag is "DP system - Sinor Marine Services". Its meta description is the first paragraph of the page. Page body text begins "DP Systems | Sinor Marine Technology" (older brand wording). | Scrape metadata and markdown |
| A11 | No JSON-LD structured data found in the served home HTML (count of application/ld+json = 0). One H1. 31 img tags, 24 with empty alt text (some may be decorative). | grep on fetched HTML |
| A12 | No Google Analytics, Tag Manager, Meta pixel or Clarity signature found in the served home HTML. This may load another way, so treat as UNVERIFIED until checked in a browser or Tag Assistant. | grep on fetched HTML |
| A13 | Home page services form lists "Fuel Monitoring" but no fuel monitoring page exists in the sitemap. Service list on home: DP Systems, Marine Automation, Electrical Solutions, Navigation Systems, Thruster Control System (Z-Thrust, PLC based), Frequency Power Converter. | Home markdown, sitemap |
| A14 | Contact block on home shows sales@, service@, support@ addresses, +971 4 665 7162, and a separate CTA to a named person's email and mobile. | Home markdown |
| A15 | An older domain https://www.sinor-marine.com returns HTTP 200 and serves a PDF titled "SINOR MARINE TECHNOLOGIES" brochure (July 2021). Relationship to Sinor Marine Services is UNVERIFIED (stand files mention "Sinor Marine Technologies" as SMT, USER-SUPPLIED). | Search result URL, curl -I |

## B. Claims on the site (VERIFIED as written, accuracy UNVERIFIED)
| Claim | Where | Conflict |
|-------|-------|----------|
| "50+ Projects Completed" | Home, About, DP page | Stand panel said "100+ projects" (Rahul confirmed use 2026-11-06). Public LinkedIn post says "8+ Dynamic Positioning (DP) upgrade projects" (different scope). |
| "15+ Years of DP Engineering Experience" | Home | About says "20+ Years Experience" and title "Engineering Reliable Marine Automation Solutions from 2024". |
| "40+ countries served" | Home, About, DP page | Consistent. |
| "50+ Team Members" | About | Not seen elsewhere. |
| "98% Client Satisfaction" | Home, DP page | No source seen. |
| "Compliant with DNV, ABS and Lloyd's Register DP requirements" and "type-approved DP systems across all classes" | DP page | No certificate or approval basis seen. Likely OEM level claims. |
| "Class-approved service providers", "OEM-certified technicians", "Certified Engineers", "24/7 Support", "Quality Assured" | Home, About | Not evidenced in this repo. ISO certificates also not seen (company's own invoice footer only). |

## C. Search results seen (2026-11-08, one session, location not set)
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
