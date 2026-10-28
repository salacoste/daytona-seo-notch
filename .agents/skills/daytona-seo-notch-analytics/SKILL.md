---
name: daytona-seo-notch-analytics
description: "Traffic intelligence from web analytics for SEO: pulls Google Analytics 4, Yandex Metrika and Google Search Console data the user already has, cross-engine. Use when the user asks about traffic, visits, organic performance, Yandex Metrika, GA4, 'сколько посещений', 'откуда трафик', search phrases in Yandex, landing pages, traffic drop investigation, or wants analytics enrichment for an audit. Read-only; credentials detected, never requested in chat."
user-invocable: true
argument-hint: "overview|organic|phrases|landing|compare <url-or-counter>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
  design-note: closes the analytics gap identified 2026-10-28; patterns researched from mcp-yandex-metrica (askads), GA4 Analytics MCP and the mk CLI conventions
---

# Traffic Intelligence (GA4 + Yandex Metrika + GSC)

Cross-engine traffic analysis for SEO work. One skill, three read-only data
paths — used only with credentials the user already configured (via
`marketing-tools-setup`); never ask for tokens in chat.

**Why Metrika matters for SEO:** Yandex Metrika reports the actual search
phrases users typed (`ym:s:searchPhrase`) and behavioral metrics per visit —
data GA4 deliberately does not provide (not provided in GA4 keyword reports).
For RU/CIS markets Metrika is the primary source of query-level truth; for
global markets GA4+GSC cover it. This skill speaks both.

## Credential detection (run first, report what is available)

| Path | Check command | Needs |
|---|---|---|
| GA4 (runtime, full reports) | `tools/seo-runtime/run google_auth.py --check` | `uv sync --group google` + OAuth in `tools/seo-runtime/` |
| GA4 (CLI, quick reads) | `GA4_ACCESS_TOKEN` in `.env.marketing` | token via `marketing-tools-setup` |
| Yandex Metrika | `YANDEX_METRIKA_TOKEN` (+ optional `YANDEX_METRIKA_COUNTER_ID`) in `.env.marketing` | OAuth token, scope `metrika:read` |
| Search Console | `GSC_ACCESS_TOKEN` / google auth | see `marketing-tools-setup` |

Report which paths are live and proceed with those; say explicitly what was
not available. Never block the whole analysis on one missing source.

## Commands

### `overview` — period snapshot across every connected engine

- GA4: `tools/seo-runtime/run ga4_report.py <property> --start <date> --end <date>` (or `node --env-file=.env.marketing tools/clis/ga4.js reports run --property <id> --metrics activeUsers,sessions --start-date --end-date`)
- Metrika: `node --env-file=.env.marketing tools/clis/yandex-metrika.js stats summary --start <date> --end <date>`
- GSC (when configured): `tools/seo-runtime/run gsc_query.py <domain> --start <date> --end <date>`

Output: one table — period, engine, visits/sessions, users, bounce, duration,
plus GSC clicks/impressions/CTR when live. Dates: ISO `YYYY-MM-DD`; default
period = last 28 days.

### `organic` — organic traffic sources per engine

- Metrika: `stats sources --start --end` then filter rows where `dim` starts with `organic` (`ym:s:lastTrafficSource` values: `organic.yandex`, `organic.google`, …) — this single report shows the Yandex/Google split GA4 cannot give per query
- GA4: sessionDefaultChannelGroup == `Organic Search` via `ga4_report.py`/CLI
- Interpret: diverging engine splits → indexing/quality issues on one engine (correlate with `daytona-seo-notch-technical` findings), not a tracking bug

### `phrases` — Yandex search phrases (Metrika-only gold)

`node --env-file=.env.marketing tools/clis/yandex-metrika.js stats phrases --start --end --limit 50`

- Treat phrases as a keyword-research source: cluster them into topics, map to landing pages
- Cross-reference with GSC queries (Google side) to find query spaces where Yandex sends traffic but Google does not (or vice versa) — candidate content/intent gaps
- Sampled data caveat: if `sample_share > 0`, report it and treat proportions, not absolutes

### `landing` — top landing pages by engine

- Metrika: `stats pages --start --end`
- GA4/GSC equivalents
- Pages with high visits but poor GSC CTR → titles/descriptions work to route to `daytona-seo-notch-page`

### `compare` — GA4 vs Metrika reconciliation

The two counters will not match, and the report must say why up front:

| Difference | Cause |
|---|---|
| Session definition | Metrika: 30 min inactivity, GA4: session_start model with campaign timeout |
| Attribution | Metrika last-source (with lookback), GA4 data-driven last-click defaults |
| Bots | Metrika filters bots by default with its list; GA4 bot filtering differs |
| Consent/no-cookie | both lose users differently per region and consent setup |

Use `compare` for trend direction and engine split, never for absolute
reconciliation. Present both raw numbers side by side with the caveats table.

## Integration with the audit

`daytona-seo-notch-audit` treats this skill as its analytics enrichment track:
when any credential path is live, the audit's Performance/traffic sections use
field numbers instead of estimates. Report the enrichment source explicitly
(`data: metrika+ga4+gsc` / partial) in the audit envelope.

## Security

- Read-only: the CLI uses `stat/v1/data` and `management/v1` GET endpoints only; never call write endpoints
- Tokens stay in `.env.marketing` (0600, gitignored); `--dry-run` previews requests with masked auth
- Counters are account-level identifiers — fine to show; visitor-level data is never requested (no Logs API in this skill)

## Related Skills

- `marketing-tools-setup` — how to connect each source step by step
- `daytona-seo-notch-audit` — consumes this skill as enrichment
- `analytics` / `attribution` (marketing suite) — measurement design and attribution modeling; this skill is the SEO-facing read path
- MCP alternative: `mcp-yandex-metrica` (askads) can be enabled in `.agents/mcp_config.json` for interactive exploration; the CLI here stays the scripted path for audits
