# Dev workflow: localhost, dist/ and the CI gate

## Auditing a dev server (Vite/Next/Astro/webpack-dev-server…)

```bash
# once per shell (or in the project's .env / direnv):
export CLAUDE_SEO_LOCAL_TARGETS=localhost:3000   # port of YOUR dev server

# then everything works against the dev URL:
tools/seo-runtime/run parse_html.py --url http://localhost:3000/ --json
/daytona-seo-notch-audit http://localhost:3000/          # in the IDE
tools/seo-runtime/run drift_baseline.py http://localhost:3000/ --skip-cwv
```

Notes:
- The allowlist is deliberately narrow: explicit `host:port` pairs only —
  never put public hosts there (SSRF surface; see `url_safety.py`).
- Dev-server HMR restarts keep the port — the variable stays valid.
- SPA frameworks: use `fetch_page.py --render auto` (or `render_page.py`)
  so JS-rendered content is judged like a crawler sees it.

## Auditing a static build (dist/, build/, out/, public/)

No dev server needed — serve the artifacts once:

```bash
cd dist && python3 -m http.server 4173 &
CLAUDE_SEO_LOCAL_TARGETS=localhost:4173 \
  tools/seo-runtime/run parse_html.py --url http://localhost:4173/ --json
```

This is the pattern to use in CI: build → serve → gate.

## CI gate: fail the PR when SEO regresses

`.github/workflows/seo-gate.yml` in the **site's own repository** (the
project being built — this library is only the checklist source when the
site repo doesn't vendor the runtime; when it does, prefer the full audit):

```yaml
name: seo-gate
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v5
        with: { node-version: 22 }
      - run: npm ci && npm run build          # produce dist/
      - name: Serve build and gate SEO
        run: |
          cd dist && python3 -m http.server 4173 &
          sleep 1
          # Fast static gate without the runtime (zero-dep):
          npx @capgo/seo-checker --dist ./dist --output json > seo-report.json
          # Gate essentials:
          python3 - <<'EOF'
          import json, sys
          r = json.load(open("seo-report.json"))
          errors = [i for i in r.get("issues", []) if i.get("severity") == "error"]
          print(f"SEO gate: {len(errors)} error(s)")
          sys.exit(1 if errors else 0)
          EOF
```

With the runtime vendored, replace the npx step with the full local audit:
`CLAUDE_SEO_LOCAL_TARGETS=localhost:4173 tools/seo-runtime/run parse_html.py
--url http://localhost:4173/ --json` per route (+ sitemap validation), or a
scheduled full `-audit` on the preview deployment.

## Preview deployments (Vercel/Netlify/Cloudflare Pages)

- Keep preview URLs `noindex` (platform setting or header) — they leak into
  the index otherwise; verify with `fetch_page.py <preview-url> --json`.
- Gate the PR on the preview URL with the same commands (no allowlist needed
  — it's a public URL).
- Never let staging share the production sitemap or analytics counter.
