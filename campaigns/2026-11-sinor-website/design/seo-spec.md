# SEO specification: Sinor Marine Technologies website, version 1

Date: 2026-11-07. Author: seo-a11y-specialist, pass 2. Status: draft for the Director.
This file is the single source of truth for every page title and meta description. It wins over any title or meta text in copy/.
Sources read: website-build-standards SKILL.md, brain/brand-profile.md, verified-facts.md, preferences.md, lessons-learned.md, brief.md, strategy.md, sitemap.md, wireframes.md, and all five files in copy/. Nothing under /tmp/work or campaigns/2026-11-sinor-site was read.
Labels: STATED (Rahul said it), HYPOTHESIS (reasoning only, no data), CLAIM TO VERIFY (depends on the STATED scope, given for Rahul's employer, to be confirmed for Sinor Marine Technologies), NEEDED FROM RAHUL.

Entity rule: the site is for Sinor Marine Technologies (STATED 2026-11-07). No FZCO, no UAE, no Middle East, no sinor-marine-services LinkedIn page, no repo logo anywhere in this spec or in metadata.

## 0. Placeholders that must be replaced

| Placeholder | Where used | Replace when |
|---|---|---|
| https://DOMAIN.example | every canonical, og:url, JSON-LD url, sitemap loc, robots.txt Sitemap line | Rahul confirms the domain (www.sinormarine.com is only FOUND, not confirmed, and may belong to the Services company) |
| (omitted) og:image and twitter:image | all pages | an image exists that Rahul has supplied or licensed |

Rule for the builder: write the placeholder exactly as https://DOMAIN.example with no path variation, so one find-and-replace fixes the whole site. QA should grep for DOMAIN.example and count occurrences before and after.

## 1. Character count record

Limits used (own rules, HYPOTHESIS that these avoid truncation, not guarantees): title 30 to 60 characters, meta description 120 to 160 characters. The 404 title is under 30 to 60 only in being a utility page and is allowed at 42.
Counting method: this run had no shell tool, so the python script could not be executed. Counts below were made by an explicit character-by-character tally, done twice per string (word lengths plus separators), and they match the copywriter's figures except where a text changed. The Director or QA must run the script below once to confirm before build. Any mismatch means this table is wrong, not the script.

```python
# python3 count.py : prints length of each title and description
import re
t = open("seo-spec.md", encoding="utf-8").read()
for m in re.finditer(r"^- (Title|Description): (.+)$", t, re.M):
    print(m.group(1), len(m.group(2)), m.group(2))
```
(The per page blocks in section 3 use the exact line form "- Title: ..." and "- Description: ..." so the script reads them. Lines that start with those words elsewhere are only in section 3.)

## 2. Changes from the copywriter's drafts

| Page | Field | Change | Reason |
|---|---|---|---|
| Home | title | none (58) | within 60, unique, brand and sector words present |
| Home | description | none (143) | within 160, unique, states scope with CLAIM TO VERIFY |
| Solutions | title | none (55) | unique, keyword "solutions" present |
| Solutions | description | none (150) | unique, within 160 |
| Service | title | none (57) | unique |
| Service | description | none (141) | unique |
| About | title | none (55) | unique |
| About | description | CHANGED: replaced "See what the company does and how the work flows from discovery to support" with "Read what the company does, from Dynamic Positioning to service and technical support" (old 142, new 153) | fit: "discovery" and "Design" steps are wireframe proposals, not STATED by Rahul (about.md 5.3). A meta description is public text that search engines can show, so it should use only STATED words. New text is unique among the pages. |
| Contact | title | none (51) | unique |
| Contact | description | none (154) | within 160. It tells the truth that the form is not live. Must be edited the day the form is connected (see 3.6 note). |
| 404 | title | none (42) | utility page, noindex, not shown in search |

Uniqueness check: all six titles and all six descriptions differ from each other. Every title ends or starts with the company name, so brand is consistent. No title or description contains a slot, a partner name, ISO, a number claim, FZCO, UAE or Middle East.

## 3. Per page specification

Common to every page (head):
- lang: `<html lang="en-GB">`. HYPOTHESIS: the copy uses British spelling (enquiry, organisation), so en-GB. English only (strategy DECISION). Confirm with Rahul.
- `<meta charset="utf-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- One `<title>`, one meta description, one canonical `<link rel="canonical">`, one robots meta.
- Open Graph on every indexable page: og:type website, og:site_name "Sinor Marine Technologies", og:title (same text as title), og:description (same text as description), og:url (same as canonical), og:locale en_GB. No og:image (no image exists; do not invent one, omit the tag).
- Twitter card on every indexable page: twitter:card "summary" (the no image variant), twitter:title, twitter:description (same texts). No twitter:image, no twitter:site (no handle supplied).
- No favicon claim: a favicon is not specified here because none exists. Omit `<link rel="icon">` until a file is supplied, or the builder may ship a plain SVG mark only with Rahul's approval. Listed in section 9.
- Robots meta value `index, follow` is the LAUNCH value. Until Rahul approves publishing, every page ships `noindex, nofollow` (see section 6).

### 3.1 Home: index.html
- Title: Sinor Marine Technologies | Marine and Offshore Technology
- Description: Sinor Marine Technologies: Dynamic Positioning, reference systems, marine electrical and automation, propulsion and thruster controls, service.
- Canonical: https://DOMAIN.example/
- Robots: index, follow (launch). og:url: https://DOMAIN.example/
- Twitter and OG texts: same as title and description above.
- JSON-LD: the Organization block in section 4, on this page only.
- Heading outline to verify: h1 "Dynamic Positioning and marine control" (exactly one; the earlier "Hold position at sea" was rejected by the fact check as overstated). h2 "Areas of work". h2 "What the work includes" with four h3 (Discover, Design, Install and commission, Support). h2 "After the system is in service". h2 "Credentials and references" (slots only, removed at publish if empty). h2 "About the company". Footer group headings "Pages" and "Find us" are small h2 or labelled nav landmarks (wireframes 8); prefer labelled nav landmarks so the outline stays clean. No heading level skipped. Four beat captions are list items, not headings.
- CLAIM TO VERIFY: description states scope.

### 3.2 Solutions: solutions.html
- Title: Marine Technology Solutions | Sinor Marine Technologies
- Description: Sinor Marine Technologies solutions: Dynamic Positioning, reference systems, electrical and automation, propulsion and thruster controls, integration.
- Canonical: https://DOMAIN.example/solutions.html
- Robots: index, follow (launch).
- Heading outline: h1 "Find your system". h2 "Jump to an area" (visually small). Then six h2 in order: Dynamic Positioning, Reference systems, Marine electrical and automation, Propulsion and thruster controls, Integration, Upgrades. "What the work covers" is a list label, use a p or a visually styled label, not a heading.
- Note: the h1 has no keyword. The title carries the keyword, which is acceptable. Not changed because the h1 is copy's decision.
- CLAIM TO VERIFY: scope.

### 3.3 Service and support: service.html
- Title: Service and Technical Support | Sinor Marine Technologies
- Description: Commissioning, service and technical support for marine and offshore systems from Sinor Marine Technologies, with a route to request support.
- Canonical: https://DOMAIN.example/service.html
- Robots: index, follow (launch).
- Heading outline: h1 "Service and support". h2 "After supply" with three h3 (Commissioning, Service, Technical support). h2 "How to reach support". h2 "What to include in a support request". The upgrades cross-link card has no heading.
- CLAIM TO VERIFY: scope.

### 3.4 About: about.html
- Title: About Sinor Marine Technologies | What the Company Does
- Description: Sinor Marine Technologies works in marine and offshore technology. Read what the company does, from Dynamic Positioning to service and technical support.
- Canonical: https://DOMAIN.example/about.html
- Robots: index, follow (launch).
- Heading outline: h1 "About Sinor Marine Technologies". h2 "The company". h2 "How the company works" with four h3. h2 "Certifications and partners" (slots, removed if empty). h2 "Team" (slot, removed if empty). h2 "Photos" (omitted if empty).
- CLAIM TO VERIFY: sector and scope.

### 3.5 Contact: contact.html
- Title: Contact Sinor Marine Technologies | Send an Enquiry
- Description: Send an enquiry to Sinor Marine Technologies about Dynamic Positioning, automation, thrusters or support. The form is not connected yet; see other routes.
- Canonical: https://DOMAIN.example/contact.html (always without the ?topic= query and without #enquiry, so every topic link consolidates to one URL).
- Robots: index, follow (launch).
- Heading outline: h1 "Contact Sinor Marine Technologies". h2 "Send an enquiry" (id="enquiry", tabindex -1). h2 "Other ways to reach the team". The error summary heading "There is a problem" and the status heading "Not sent" appear only after submit; give them h2 inside the form region so no level is skipped.
- Note for the day the form is connected: remove "The form is not connected yet; see other routes." from the description, from og:description and from twitter:description in the same change as the notice removal (copy/contact.md says the same). Replace with an approved sentence only.

### 3.6 Page not found: 404.html
- Title: Page not found | Sinor Marine Technologies
- Description: omit the meta description tag (utility page).
- Canonical: omit (a 404 has no canonical).
- Robots: noindex, follow. Never listed in sitemap.xml. No Open Graph or Twitter tags (not shared).
- Heading outline: h1 "Page not found" only, plus the nav and footer landmarks.
- Technical note for the builder: a static host serves 404.html at whatever wrong URL was requested, so relative asset and link paths (css/, js/, index.html) would break on a deep wrong path. Use root-absolute paths in this file only (for example /css/site.css, /index.html, /contact.html). This conflicts with sitemap.md section 1 (plain relative links) and needs the Director's decision. The 404 HTTP status is a host setting that cannot be verified from files; do not use a meta refresh.

## 4. JSON-LD Organization block (Home page only)

Rule: only STATED or VERIFIED facts. The only such fact is the name (STATED 2026-11-07). The url uses the placeholder.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Sinor Marine Technologies",
  "url": "https://DOMAIN.example/"
}
</script>
```

Deliberately absent, with the slot that unlocks each property:

| Property | Needs | Slot |
|---|---|---|
| logo | the official Sinor Marine Technologies logo with approval | S29 |
| legalName | legal entity name and registration | S30 |
| sameAs (LinkedIn) | the Sinor Marine Technologies LinkedIn page address | S31 |
| email, telephone (contactPoint) | public contact details Rahul approves | S01, S02 |
| address | public address | S03, S23 |
| foundingDate | confirmed founding year | S24 |
| areaServed | confirmed regions | S25 |
| description, knowsAbout, hasOfferCatalog | not added: the scope is a CLAIM TO VERIFY, so it stays out of structured data until Rahul confirms it applies to this entity | none |
| aggregateRating, review, award, hasCredential | never, no data exists | none |

Do not add LocalBusiness, Product, Service or FAQ markup. The sinor-marine-services LinkedIn URL must never appear in sameAs. QA check: the block parses as valid JSON and contains no property beyond @context, @type, name, url until the slots are filled.

## 5. sitemap.xml (site root)

Five indexable pages. 404.html is excluded. No lastmod, changefreq or priority are given because no real modification data or priority data exists (search engines may ignore them). Replace the domain at publish.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://DOMAIN.example/</loc></url>
  <url><loc>https://DOMAIN.example/solutions.html</loc></url>
  <url><loc>https://DOMAIN.example/service.html</loc></url>
  <url><loc>https://DOMAIN.example/about.html</loc></url>
  <url><loc>https://DOMAIN.example/contact.html</loc></url>
</urlset>
```

Home is listed as the bare root, matching its canonical. The builder must not also publish a second copy at /index.html as an indexable URL: the canonical on index.html points to the root, which handles it.

## 6. robots.txt (site root) and the launch gate

Launch version (use only after Rahul approves publishing and the domain is known):
```
User-agent: *
Allow: /

Sitemap: https://DOMAIN.example/sitemap.xml
```
404.html is not blocked in robots.txt on purpose: blocking would stop crawlers from seeing its noindex tag.

Pre-launch rule: until Rahul approves publishing, the repo build ships `<meta name="robots" content="noindex, nofollow">` on every page and a robots.txt of `User-agent: *` with `Disallow: /`, and no sitemap line. Both are flipped to the launch values in one step at launch. Reason: a preview or staging copy must not be indexed. QA must check the state matches the launch status Rahul has approved. Nothing is published or shared by this spec.

## 7. Internal linking rules

1. Use only the plain relative links defined in sitemap.md, except 404.html (section 3.6). Home link in nav and logo goes to index.html (the canonical is the root).
2. Descriptive link text, never "click here". Every link text must make sense out of context: "Send an enquiry", "See all solutions", "Service and support", "About the company".
3. Same destination, same text. Links to the same page use the same visible label across the site, so repeated "Discuss this system" links get unique visually hidden suffixes (for example "about Dynamic Positioning"), as copy defines.
4. Topic links use contact.html?topic=<value>#enquiry with only the eight values from sitemap.md section 4. The canonical stays on contact.html. No other query parameters are added to internal links.
5. Anchors: Home area rows link to solutions.html#<id> using the ids dynamic-positioning, reference-systems, electrical-automation, propulsion-thrusters, integration, upgrades. Service ids: commissioning, service, technical-support. QA checks every fragment resolves to an existing id on the target page.
6. Every indexable page must be reachable from the header nav and the footer in one click, and every page ends with the enquiry action (strategy, section 4). Zero orphan pages, zero broken internal links (build standard).
7. Home links to all four other pages in the main body: Solutions (area rows and "See all solutions"), Service and support, About, Contact.
8. External links: only the Sinor Marine Technologies LinkedIn page, and only once supplied (S31). Link text "LinkedIn page", with visible text "opens linkedin.com". Use rel="noopener noreferrer" with target="_blank" only if a new tab is used; prefer same tab. No other external links, no partner links, no trackers.
9. Slots are never links. A slot placeholder must not contain a mailto or tel link.

## 8. Image and alt text rules

1. No raster images exist, so og:image and twitter:image are omitted. Do not generate or invent an image for sharing. When Rahul supplies one, the spec gains: og:image as an absolute URL on the real domain, og:image:alt, twitter:card changes to summary_large_image, recommended size 1200 by 630 (HYPOTHESIS, check platform specs at that time).
2. Decorative graphics (canvas scene, inline SVG vessel and ring, ring motif, arrow glyphs, hairlines): empty alt or aria-hidden="true", no title attribute, no text alternative (copy/home.md and wireframes agree).
3. Informative images, when ever added: alt text states what the photo actually shows in under 125 characters, no "image of", no keyword stuffing, no claims. Photo alt text is NEEDED FROM RAHUL for S12.
4. Logo, when supplied (S29): alt "Sinor Marine Technologies logo" if the logo is the only content of the link, but then the link name must be "Sinor Marine Technologies, home". If the wordmark text is also visible, use alt="" to avoid double reading.
5. Text is never baked into images. All text is DOM text.
6. Each image under 300 KB, total under 2 MB (build standard). Provide width and height attributes to prevent layout shift.

## 9. Keyword list (HYPOTHESIS, no data)

No search volume, ranking, traffic or competitor data was supplied or looked up. These phrases are only the STATED scope words, grouped by the page that already covers them. They are candidate wording to check against Google Search Console or another tool if Rahul approves one. No ranking is promised or implied by this list.

| Page | Candidate phrases (HYPOTHESIS) |
|---|---|
| Home | Sinor Marine Technologies; marine and offshore technology; Dynamic Positioning |
| Solutions | Dynamic Positioning systems; DP systems; reference systems; marine electrical and automation; propulsion and thruster controls; marine systems integration; DP upgrades |
| Service and support | marine commissioning; marine technical support; marine systems service |
| About | Sinor Marine Technologies company |
| Contact | contact Sinor Marine Technologies; marine technology enquiry |

Rules: brand name appears in every title. No product, trademark or partner phrase is used (none approved). Do not add place names such as UAE or Singapore until the base (S23) is resolved. Avoid keyword stuffing: each page keeps its single topic. British "enquiry" spelling may differ from what some searchers type (HYPOTHESIS), so the body copy could also use "inquiry" once if Rahul prefers; not changed.

## 10. Other technical SEO requirements for the build

1. One h1 per page, matching the page job; title and h1 may differ (see 3.2).
2. All pages valid HTML5 with `lang`, a title, a viewport tag and one main landmark. Headings in order, no skipped levels.
3. URLs: lowercase file names as in sitemap.md. No trailing duplicates: index.html canonical is the root.
4. No render-blocking third party, no external fonts, no CDN, no tracker, no cookie. Core Web Vitals gates from the build standard: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less (lab run is indicative only).
5. All content in the DOM at load. Without JavaScript the pages are complete (strategy), so crawlers see the full text.
6. No hidden text for search. The visually hidden link suffixes are accessibility text only.
7. No analytics tag is specified. Whether to use one is Rahul's decision (section 11).
8. The slot register means no "NEEDED FROM RAHUL" text may reach the published site, including titles, descriptions and JSON-LD. QA greps for it.

## 11. What cannot be done without Rahul

1. Domain: canonical, og:url, sitemap, robots Sitemap line and JSON-LD url stay as https://DOMAIN.example until he confirms the domain. Nothing is indexable until he approves publishing.
2. Analytics decision: strategy section 8 needs visits and entry pages. The build standards forbid trackers and cookies by default. A cookie-free server log or privacy-first tool needs his decision. Search Console verification also needs access to the real domain and his approval.
3. og:image: no image exists. Social shares will show text only until he supplies a licensed image.
4. Logo (S29): no logo in JSON-LD or favicon until supplied. The repo logo belongs to the Services company and is not used.
5. Legal entity (S30), base (S23), founding year (S24), regions (S25): none go into structured data until supplied.
6. LinkedIn page (S31): sameAs and footer link wait for the Sinor Marine Technologies page.
7. Contact details (S01 to S04): no contactPoint, email, telephone or address in JSON-LD until he approves.
8. Confirmation that the stated scope applies to Sinor Marine Technologies: five descriptions carry it.
9. Language variant: en-GB is an inference.
10. A working form endpoint (S27): the contact description must change on that day.
11. Favicon: none supplied.

## 12. QA checklist for this spec

- Each page has exactly the title and description in section 3 (string match), one canonical, and robots matching the launch state.
- No title above 60 or description above 160 characters (run the script in section 1).
- The 404 has noindex and is absent from sitemap.xml.
- JSON-LD parses and has only four keys.
- grep for DOMAIN.example finds every canonical, og:url, sitemap loc and the JSON-LD url.
- grep finds no "FZCO", "UAE", "Middle East", "sinor-marine-services", "ISO" in site files.
- No em dash and no en dash in any metadata.

## 13. Candidate lessons for the Director (not written to brain/)

1. A sandbox may lack a shell. When a spec asks for a script count, state the manual method, include the script, and have QA run it.
2. A page title and description are public, structured text: unverified wireframe proposals (such as the "discovery" step) must not be copied into them.
3. Contact meta that admits the form is not live must be edited in the same change that connects the form; add it to the connection checklist.
4. A 404 file on a static host needs root-absolute paths; this conflicts with the relative-links rule and should be decided once.
5. Pre-launch builds should ship noindex and Disallow, flipped at launch, so a preview is never indexed.
