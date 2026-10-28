# Local scan — mining an existing project before asking anything

Run against the client's project folder (repo checkout). Read-only. Goal:
answer brief fields from evidence and build a first candidate-query list with
native vocabulary.

## Scan order

1. **Identity files** — `README*`, `docs/`, `ABOUT*`, landing copy files.
   Extract: what the product is, audience, promise, pricing tiers → segments.
2. **Content inventory** — `content/`, `posts/`, `articles/`, `pages/`,
   `*.mdx`, `*.html`, `*.astro`, `src/**/page*`. Record per file: path, H1,
   existing `<title>`/meta description (present? unique? templated?), word
   count band, language. Flag: empty/draft pages, duplicated metadata
   (`metadata_template.py` heuristics), missing dates/authors.
3. **SEO signals already in code** — JSON-LD in templates/components,
   sitemap/robots drafts, canonical handling, OG components, i18n routing
   (`locales/`, `i18n/`) → market list.
4. **Stack** — `package.json`/`requirements`/frameworks: SSR/SSG/SPA verdict
   (crawlability expectation for prelaunch Phase 1), CMS/headless (content
   workflow), analytics snippets present (GA4/Metrika already wired?).
5. **Native vocabulary** — product category names, feature names, industry
   terms used consistently in copy → seed queries. Native beats generic.

## Output artifact (`local-scan.md`)

```markdown
# Local scan — <project>, YYYY-MM-DD

## What the site is (from evidence)
- <statement> [README]
- <segments> [pricing page]

## Stack verdict
SSR|SSG|SPA: … ; CMS: … ; analytics: present|absent

## Content inventory
| Path | Lang | H1 | Title/meta | Words | Flags |

## Brief fields answered from code
<field> → value [source file]

## Candidate queries (native vocabulary)
| Query | Source file | Intent guess |
```

Rules: every fact cites a file path; unknown stays unknown (no guessing);
draft/empty content counted, not judged.
