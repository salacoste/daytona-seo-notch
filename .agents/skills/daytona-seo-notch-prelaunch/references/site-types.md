# Site-type playbooks

Deltas per site type across the four phases.

## Corporate site (multi-page: services, about, contacts, cases)

- **Phase 0:** money pages = services + case studies; one service page per
  query family; company-level entities (Organization schema, sameAs set) and
  local signals if offline presence (LocalBusiness — see hub references).
  RU/CIS: Yandex weighting high → Metrika + Yandex Webmaster from day one.
- **Phase 1:** template checks apply per page type (service/contact/case);
  breadcrumb schema + trail UI; consistent NAP in footer if local.
- **Phase 2:** every service page passes the content gates (thin-content
  thresholds per page type — quality-gates.md); cases carry results/proof.
- **Phase 3:** Organization entity verified in GSC; local: GBP linked.

## Landing page (single page, one conversion goal)

- **Phase 0:** one intent, one promise; query set narrow; success = conversion
  SEO is secondary but the page must be findable — title matches the offer.
- **Phase 1:** above-fold content server-rendered (both crawlers and AI
  agents read it); single H1 = the offer; FAQ section with real questions
  (QAPage only if genuine Q&A — FAQ rich results are retired for Google);
  WebMCP tools for the form (see `-ai`); OG image = the creative (shares).
- **Phase 2:** CWV strict (LCP hero under control, no layout shift on CTA);
  `/daytona-seo-notch-page <dev-url>` deep single-page pass is the main gate;
  conversion tracking verified per `conversion-tracking` skill.
- **Phase 3:** UTM/redirect rules for campaigns; drift baseline immediately
  (landing iterates often — compare after every copy change).

## Blog (many articles over time)

- **Phase 0:** topic clusters designed up-front (pillar + spokes; one owning
  page per fact family); URL scheme `/blog/<slug>`; author entities planned
  (E-E-A-T: real bios, credentials).
- **Phase 1:** article template: title/description fields required, one H1,
  date + lastmod fields, author block, Article/BlogPosting JSON-LD, TOC
  anchors, image handling with dimensions; listing pagination noindex-follow
  where appropriate.
- **Phase 2:** seed articles pass content gates (Who/How/Why test,
  thin-content minimums); internal links pillar↔spokes exist; sitemap split
  by content type (posts vs pages).
- **Phase 3:** GSC submission of the posts sitemap; publishing workflow:
  every new post → drift compare + IndexNow ping; content refresh cadence
  (recency is a citation factor — see `-ai` authority model).

## Hybrid (e.g. corporate + blog)

Run corporate for the shell, blog for the content hub; sitemap split by
type; one IA review covering both trees.
