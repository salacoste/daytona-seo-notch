---
name: daytona-seo-notch-prelaunch
description: "SEO for a site that is still being built: strategy, templates and audits BEFORE publication. Use when the user is developing or designing a website (corporate site, landing page, or blog) and asks about SEO at the development stage, pre-launch optimization, what to do before going live, staging checks, localhost/dev-server audits, dist-folder checks, or an SEO plan for a new site. Covers four phases: strategy → build → pre-launch gate → go-live switch. Works against a local dev server or built files — no published URL needed. Triggers: pre-launch, before launch, новый сайт, на этапе разработки, до запуска, верстаем сайт."
user-invocable: true
argument-hint: "[phase|gate] [url-or-dist]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
  design-note: research-based (docs/research-prelaunch-seo.md) — phase checklists (ZH/EN practice), dist-artifact auditing (Cap-go pattern), CI gates, plus the CLAUDE_SEO_LOCAL_TARGETS mechanism verified live
---

# Pre-Launch SEO: build it right before anyone can crawl it

The rest of the daytona-seo-notch line audits published sites. This skill runs
the same machinery **before publication** — against a dev server or built
files — and adds the phases that only exist pre-launch: strategy, page
templates, the launch gate and the go-live switch.

**How local auditing works (verified):** the runtime's SSRF layer has an
opt-in allowlist. Audit any local target by allowing it explicitly:

```bash
CLAUDE_SEO_LOCAL_TARGETS=localhost:3000 \
  tools/seo-runtime/run parse_html.py --url http://localhost:3000/ --json
```

Export the variable once per shell (or put it in the project's env setup); it
applies to every runtime script — `fetch_page`, `parse_html`, `render_page`,
`agentic_check`, `drift_*`, and therefore to `/daytona-seo-notch-audit` and
all track skills pointed at the dev URL. Never allow public hosts in this
variable. To audit a static build without any server:
`cd dist && python3 -m http.server 4173` (then allow `localhost:4173`).

**Site-type playbooks:** [references/site-types.md](references/site-types.md) — corporate site, landing page, blog; each phase below lists the type-specific deltas.

## Phase 0 — Strategy (before the first component is written)

1. **Fix the site type** with the user: corporate / landing / blog / hybrid —
   it changes everything downstream (see site-types reference).
2. **Demand and semantics:** target queries, language(s)/markets (Yandex vs
   Google weighting), competitors. Use the hub's industry detection in
   reverse: define signals now, so detection later confirms rather than
   surprises. For blogs: topic clusters and one owning page per fact family
   (see `daytona-seo-notch-ai` query fan-out).
3. **Information architecture → URLs:** routes named from search intent, flat
   depth (money pages ≤3 clicks), one URL per intent, canonical scheme, hreflang
   plan if multi-language. Review with `../daytona-seo-notch-sitemap`
   generation rules in mind — the sitemap is designed here, generated in
   Phase 2.
4. **Content plan:** page inventory with primary query, title idea and schema
   type per URL (generate skeletons with `tools/seo-runtime/run
   schema_generate.py`; templates in `tools/seo-runtime/schema/templates.json`).
   Blogs: editorial calendar mapped to clusters.

Output: `_bmad-output/…/` or `docs/seo-plan.md` — strategy the user owns.

## Phase 1 — Build (while pages are being coded)

Checks to run **per template/page as it appears on the dev server** (all
against `http://localhost:PORT` via the allowlist):

- **Every page:** unique title (50–60 chars) and meta description (150–160),
  exactly one H1 matching intent, descriptive H2+, canonical present and
  self-referencing, OG/Twitter cards, `lang`, viewport, semantic landmarks.
  Use `parse_html.py --url <dev-url>/<route> --json` per route.
- **Renderability:** server-rendered primary content (no JS-only text) —
  `fetch_page.py` compares raw vs rendered; JS-only content fails both search
  and AI agents (see `daytona-seo-notch-ai` readiness).
- **Schema:** JSON-LD in initial HTML for time-sensitive types (Product/Offer
  especially); validate with `daytona-seo-notch-schema` rules.
- **Images:** dimensions set (CLS), modern formats, alt text naming the
  subject — caught now per-template, not across 500 pages later.
- **Staging policy from day one:** preview/staging must be `noindex,
  nofollow` + not listed anywhere public; production builds must NOT carry
  the flag — wire it to an env variable now and test both modes.
- **Performance hygiene at build:** fonts swapped/preloaded, no render-
  blocking chains, third-party scripts deferred — cheaper before CMS content
  lands on top.

## Phase 2 — Pre-launch gate (the audit, before DNS points anywhere)

Run the full machinery against the dev server or a production build of
`dist/`:

1. `/daytona-seo-notch-audit <dev-url>` — full tracks: technical, content,
   schema, sitemap, AI-readiness. The health score is your gate metric.
2. `/daytona-seo-notch-sitemap generate` — produce and validate the real
   sitemap.xml from the built site; reference it from robots.txt now.
3. `/daytona-seo-notch-ai readiness <dev-url>` — llms.txt decision, robots
   AI-crawler policy, Markdown delivery, WebMCP for forms (landing pages).
4. `/daytona-seo-notch-drift baseline <dev-url>` — capture the pre-launch
   baseline NOW: every subsequent change is measured as drift.
5. Type-specific gate items: [references/prelaunch-checklist.md](references/prelaunch-checklist.md)
   (the full checklist, printable) — incl. redirects plan if replacing an old
   site, analytics counters prepared (GA4/Metrika per
   `../marketing-tools-setup`), favicon/OG image real, 404 page real.

**CI gate (recommended):** fail PRs that regress SEO on the preview build —
example workflow in [references/dev-workflow.md](references/dev-workflow.md).

## Phase 3 — Go-live switch (launch day, zero improvisation)

Ordered switch checklist (details in prelaunch-checklist.md):

1. DNS/deploys live → verify HTTPS, HSTS, redirect map (old→new, 301 only).
2. **Remove every noindex** (staging flag off in prod) — then verify with
   `fetch_page.py <prod-url> --json` (meta robots + X-Robots-Tag).
3. robots.txt production version + sitemap.xml reachable; submit sitemap in
   Google Search Console; add site to Yandex Webmaster (RU markets).
4. Analytics live: GA4 + Metrika counters firing (realtime check per
   `daytona-seo-notch-analytics`).
5. `/daytona-seo-notch-audit <prod-url>` — first production audit; then
   `/daytona-seo-notch-drift baseline <prod-url>` (prod baseline; weekly
   monitoring starts).
6. IndexNow ping for new URLs (`tools/seo-runtime/run indexnow_submit.py`).

**Golden rule:** the go-live switch must contain zero decisions — everything
decided in Phases 0–2; launch day only flips switches and verifies.

## Security

- `CLAUDE_SEO_LOCAL_TARGETS` allows only explicit local targets; never put
  public hosts or proxy ranges there (see `url_safety.py` design).
- Auditing staging of a client project is still read-only; no WAF probing
  (`--ua-matrix`) even on localhost without need.
- Preview URLs and analytics IDs are not secrets, but preview deployments
  should not be publicly linked (they will be indexed otherwise).

## Related Skills

- `daytona-seo-notch-audit|technical|schema|sitemap|ai|drift` — the machinery this skill aims at unbuilt sites
- `daytona-seo-notch-analytics` — go-live analytics verification
- `marketing-tools-setup` — GA4/Metrika counters before launch
- `content-strategy` (marketing suite) — Phase 0 editorial planning for blogs
