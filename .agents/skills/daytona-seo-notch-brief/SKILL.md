---
name: daytona-seo-notch-brief
description: "Intake for NEW client sites and projects: run the client brief (what the site is about, audience, markets), scan already-developed content/code/files locally to extract topics and existing SEO signals, mine and AGREE the core search queries, attach search volume where credentials allow, and hand off a strategy to daytona-seo-notch-prelaunch. Use when the user says 'новый сайт клиента', 'бриф', 'о чём сайт', 'собрать запросы', 'частотность', 'разбери что уже есть', 'папка проекта', 'существующий контент', 'keyword research for a new project', 'analyze existing content/code before planning', or starts an SEO engagement for an unbuilt or partially built site."
user-invocable: true
argument-hint: "[project-path-or-name]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# Project intake: brief → local scan → agreed queries → strategy handoff

The entry point for new-site engagements. Four stages, each produces an
artifact the next stage consumes; everything lands in
`_bmad-output/initiative-…/` or `docs/` as agreed with the user.

```
A. Client brief ──► B. Local scan of what exists ──► C. Query set (agreed)
                                                          │
                                          D. Volume + strategy handoff
```

## Stage A — Client brief (what is this site about)

Run the structured interview from
[references/client-brief.md](references/client-brief.md) — grouped questions
(business, audience, offer, markets/languages, competitors, constraints,
success criteria) with a fill-as-you-go artifact. Rules:
- Ask in small batches (3–5 questions), not a wall; skip what Stage B already
  answers from the code.
- RU/CIS clients: ask about Yandex-vs-Google priority explicitly — it changes
  volume sources (Wordstat vs Keyword Planner) and the go-live checklist.
- Output: `brief-<slug>/brief-<slug>.md` (frontmatter: client, date, status).

## Stage B — Local scan of already-developed material

When any part of the project exists (code, content, files, design), mine it
BEFORE asking the client what the site is about — often it answers half the
brief. The method is in [references/local-scan.md](references/local-scan.md);
essentials:

- **Business truth:** README/docs/landing copy → what the product is, for
  whom, with what promise; pricing pages → segments.
- **Content inventory:** `.md/.mdx/.html/.astro/.jsx/.tsx` content files;
  existing `<title>`/meta/OG/H1s in templates; draft sitemaps; I18n files →
  market list.
- **Stack signals:** `package.json`/frameworks → SSR/SSG/SPA (crawlability
  expectations), CMS (content workflow), analytics snippets already present.
- **Extracted queries:** terms the project itself uses (product categories,
  feature names) — native vocabulary matters more than generic keyword lists.

Output: `brief-<slug>/local-scan.md` — findings mapped to brief fields
("answered from code" vs "ask the client"), plus a first candidate-query
list with source per term. Nothing invented: every extracted fact cites its
file.

## Stage C — Core query set (extracted → discussed → AGREED)

1. Seed pool = brief answers + Stage B vocabulary + competitor domains if
   provided (their categories/page names via `fetch_page.py` on public
   competitors).
2. Expand: `tools/seo-runtime/run keyword_planner.py ideas "<seed>" --limit 50
   --json` (needs Google Ads credentials, Stage D) — or, without any keys,
   cluster the pool manually by intent: transactional / informational /
   navigational / comparison.
3. **Agreement gate:** present the table (query · intent · target page type ·
   priority · status: candidate/proposed/agreed) and get explicit user
   sign-off per core query. This artifact is the contract for strategy —
   never proceed to planning on an unagreed set.

Output: `brief-<slug>/queries.md` — the agreed core set + parked candidates.

## Stage D — Search volume (частотность) + strategy handoff

**What volume sources the library actually has** (be honest with the client):

| Source | Command | Needs | Coverage |
|---|---|---|---|
| Google Keyword Planner | `tools/seo-runtime/run keyword_planner.py volume "q1,q2" --json` (+ `ideas`) | Google Ads credentials (`uv sync --group google`, ads OAuth; free API tier returns ranged volumes) | Google demand, any language/location (RU: `--language 1048 --location 643` — verify IDs against the Google Ads reference) |
| DataForSEO | MCP tools (`/marketing-tools-setup`) | paid budget | exact volumes + SERP data, RU+global |
| Yandex Wordstat | semi-manual flow (below) | Яндекс ID | RU demand — the primary RU source |
| Google Trends | relative only | nothing | trend direction, no absolute volume |

**Wordstat semi-manual flow (honest default for RU without Direct API):**
Wordstat's API requires a Yandex Direct advertiser token — when the client
has one, offer to wire it later; otherwise: (1) build the exact query list,
(2) give the user per-query `wordstat.yandex.ru/…?text=<q>` links (URL-encoded),
(3) the user pastes back the exported CSV/text (or just the frequency
numbers), (4) parse and merge into the table, marking values as
"wordstat, <date>, manual". Never fabricate frequencies; missing value =
`—` with the follow-up noted.

**Finish:** merge volumes into `queries.md`, rank by priority × demand, and
hand off: `/daytona-seo-notch-prelaunch` Phase 0 consumes the brief + agreed
queries and continues into IA/URL map and content plan. State which volume
source produced each number.

## Security

- Client materials are confidential: artifacts stay in the project repo;
  never send content to third-party APIs beyond the volume lookups above
  (queries only — not client content).
- Competitor fetching is read-only public data.

## Related Skills

- `daytona-seo-notch-prelaunch` — the consumer of this intake (Phases 0–3)
- `daytona-seo-notch-analytics` — GA4/Metrika for markets question in the brief
- `marketing-tools-setup` — connecting Keyword Planner / DataForSEO credentials
- `content-strategy` (marketing suite) — editorial side for blog projects
