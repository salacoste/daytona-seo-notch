# Pre-launch checklist (printable)

Four phases; every item names its tool or artifact. Tick in order.

## Phase 0 — Strategy

- [ ] Site type fixed (corporate / landing / blog / hybrid)
- [ ] Target queries and markets listed (Google/Yandex weighting for RU/CIS)
- [ ] Competitors named; their strengths noted (structure, schema, freshness)
- [ ] IA → URL map: every route has primary query, title idea, schema type
- [ ] Depth rule: money pages ≤3 clicks; one URL per intent
- [ ] Canonical scheme + hreflang plan (if multi-language)
- [ ] Content plan / editorial calendar (blogs)
- [ ] Strategy doc committed (docs/seo-plan.md)

## Phase 1 — Build (per template on the dev server)

- [ ] `CLAUDE_SEO_LOCAL_TARGETS=localhost:<port>` set for the project shell
- [ ] Title unique, 50–60 chars; meta description 150–160, not a title echo
      (`metadata_template.py --title … --description … --json`)
- [ ] Exactly one H1 per page; logical H2–H6
- [ ] Canonical present, self-referencing; trailing-slash policy consistent
- [ ] OG + Twitter cards; `lang`; viewport; semantic landmarks (`main`, `nav`)
- [ ] Primary content server-rendered (fetch_page raw vs rendered equal)
- [ ] JSON-LD in initial HTML; validated per schema skill rules
- [ ] Images: width/height set, modern format, descriptive alt
- [ ] Staging `noindex` wired to env; both modes tested
- [ ] Fonts preloaded/swapped; no render-blocking chains; deferred 3rd-party

## Phase 2 — Pre-launch gate

- [ ] `/daytona-seo-notch-audit <dev-url>` — health score recorded
- [ ] All Critical/High findings fixed or explicitly accepted by the user
- [ ] sitemap.xml generated (`-sitemap generate`), referenced in robots.txt
- [ ] `/daytona-seo-notch-ai readiness <dev-url>` run; P0 items resolved
- [ ] robots.txt final draft (incl. AI-crawler policy decision)
- [ ] hreflang bidirectional and complete (if multi-language)
- [ ] 404 page real (no catch-all 200 — fails llms/ARD rules)
- [ ] Redirect map old→new ready (301 only) if replacing a site
- [ ] GA4 + Metrika counters created, not yet firing on public (staging mode)
- [ ] Favicon + OG image real (no placeholders)
- [ ] `/daytona-seo-notch-drift baseline <dev-url>` captured
- [ ] CI SEO gate on PRs enabled (references/dev-workflow.md)

## Phase 3 — Go-live switch (no decisions here, only flips + verify)

- [ ] DNS/HTTPS live; HSTS; redirect map deployed and spot-checked
- [ ] noindex removed in prod; verified: meta robots + X-Robots-Tag empty
      (`fetch_page.py <prod-url> --json`)
- [ ] robots.txt production; sitemap.xml 200; submitted in GSC; Yandex
      Webmaster added (RU)
- [ ] Analytics firing (GA4 realtime / Metrika `stats summary` today)
- [ ] `/daytona-seo-notch-audit <prod-url>` — first prod audit recorded
- [ ] `/daytona-seo-notch-drift baseline <prod-url>` — prod baseline
- [ ] IndexNow pinged for new URLs (`indexnow_submit.py`)
- [ ] Preview/staging URLs: still noindex, not linked publicly
- [ ] Week-1 watch: GSC coverage, drift compare after first content changes
