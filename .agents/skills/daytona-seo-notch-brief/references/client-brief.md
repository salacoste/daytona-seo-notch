# Client brief — question set

Small batches, conversation-first; fields marked **[scan]** may be answered by
the local scan (references/local-scan.md) before asking. Artifact template at
the bottom.

## 1. Business (what the site sells)

- What does the company/product do, in one sentence? **[scan: README]**
- Offerings to show on the site: products/services list with priorities **[scan: pages]**
- What makes it different from competitors (the honest version)?
- Business model: leads / sales / subscriptions / content monetization?

## 2. Audience and markets

- Who decides and who uses? (buyer vs user for B2B)
- Segments to prioritize on the site
- Geography and languages **[scan: i18n files]**; for RU/CIS: **Yandex vs
  Google priority** (changes volume sources and launch checklist)
- Where do customers come from today?

## 3. Competitors

- 2–5 named competitors (URLs) — used for public-page vocabulary, not attacks
- What do they do better / where do we win? **[scan: their categories]**

## 4. Goals and constraints

- The site's #1 job in 6 months (leads? signups? calls?)
- Success metrics the client already trusts (incl. GA4/Metrika access —
  `daytona-seo-notch-analytics`)
- Brand voice / design constraints / forbidden words
- Deadlines and launch expectations (feeds prelaunch phases)
- Existing domain history: new domain vs replacement of an old site
  (redirect map) vs redesign keeping URLs

## 5. Content reality

- Who writes content and how often (blog projects) **[scan: content files]**
- Existing materials to reuse (docs, cases, articles) **[scan: repo]**
- Languages the client can actually maintain (hreflang honesty)

## Artifact template

```markdown
---
client: <name>
project: <slug>
date: YYYY-MM-DD
status: draft|agreed
---
# Brief: <project>

## Answers
<per section; mark each fact [scan:<file>] or [client]>

## Open questions
- …

## Handoff
- Site type (corporate/landing/blog/hybrid):
- Markets/languages; Yandex↔Google priority:
- Agreed queries artifact: queries.md
- Next: /daytona-seo-notch-prelaunch Phase 0
```
