# Search volume (частотность) — sources and honest limits

The question "сможем ли находить частотность?" — answer: **yes, with the
right credential per source**; below is exactly what works today and what
each path costs.

## 1. Google Keyword Planner (in the runtime, live commands)

```bash
# ideas (expansion) and volume (lookup), any market:
tools/seo-runtime/run keyword_planner.py ideas "установка окон" --limit 50 \
  --language 1048 --location 643 --json     # RU language, Russia geo
tools/seo-runtime/run keyword_planner.py volume "установка окон,окна москва" \
  --language 1048 --location 643 --json
```

- **Credentials:** Google Ads API access (developer/project approved) + OAuth
  in the runtime (`uv sync --group google`, then `google_auth.py`). Connect
  via `/marketing-tools-setup`.
- **Data honesty:** accounts without active ad spend get **ranged volumes**
  (e.g. 1K–10K); with spend, monthly ranges tighten. Google volumes are
  Google-demand only — for RU markets they understate Yandex.
- **IDs:** defaults are English/US (`--language 1000 --location 2840`).
  Common: Russian language `1048`, Russia `643`, Kazakhstan `2438`,
  Belarus `2437` — verify against the Google Ads constants reference before
  quoting to a client (wrong ID = wrong market silently).

## 2. DataForSEO (exact volumes, paid)

MCP route (`mcp_config.example.json` → `dataforseo`): keyword data for both
Google and Yandex (they resell Yandex Wordstat-derived datasets), plus SERP
overlaps. Budget-guarded per `/marketing-tools-setup` — confirm spend with
the user before any bulk lookup.

## 3. Yandex Wordstat — the RU primary, semi-manual by default

Wordstat's public site has no open API; the official API path requires a
**Yandex Direct advertiser token**. Flows:

- **Client has Direct access (rare):** note the token request in the brief;
  wiring a CLI is a small follow-up (same pattern as yandex-metrika.js).
- **Default semi-manual flow:**
  1. Build the agreed query list (Stage C).
  2. Generate per-query links for the user:
     `https://wordstat.yandex.ru/#!/?text=<urlencoded query>` (+ region tab
     note when geo matters).
  3. User pastes back the frequencies (or exports CSV → paste).
  4. Merge into `queries.md` marked `wordstat · manual · <date>`.
- Never fabricate or "estimate" Wordstat numbers; blank + follow-up note only.

## 4. Google Trends (free, relative only)

Direction and seasonality comparisons between queries (works for RU too via
`hl=ru&geo=RU` URLs). No absolute volumes — use for prioritization color,
not for the volume column.

## Merging rules for queries.md

- One `source` tag per number (`kp · ranged | kp | dfs | wordstat·manual | trends`).
- Ranged values stored as ranges, not midpoints.
- RU+global projects: show Google and Yandex demand side by side when both
  exist; never blend into one "volume" column.
- Missing volume never blocks agreement — priority can be decided on intent
  and business value, volume refines it later.
