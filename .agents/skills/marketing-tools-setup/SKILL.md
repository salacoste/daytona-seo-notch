---
name: marketing-tools-setup
description: "Guided workflow for connecting marketing data accounts (Google Ads, Meta, LinkedIn, GA4, GSC, Stripe, Ahrefs, Semrush, DataForSEO, keyword tools) to this workspace safely: local CLIs in tools/clis/, MCP servers in .agents/mcp_config.json, credentials only in .env.marketing. Use when the user says 'connect', 'add API key', 'set up token', 'integrate', 'MCP setup', asks where to store API keys safely, or wants an agent to read a marketing account. One tool at a time, read-only first, secrets never in chat."
user-invocable: true
argument-hint: "[tool]"
license: MIT
metadata:
  version: "0.1.0"
  category: marketing-infra
  adapted-from: coreyhaines31/marketingskills tools/SETUP.md v2.13.9 (MIT), adapted for Antigravity
---

# Marketing Tool Connections (guided)

Bridges the [tool registry](../../../tools/REGISTRY.md), the [integration guides](../../../tools/integrations/), the [repository CLIs](../../../tools/clis/README.md) and Antigravity's MCP config. Separate from the `onboarding` skill (that one improves a product's customer activation).

**Security discipline (non-negotiable):**
- Secrets live only in `.env.marketing` (owner-private, gitignored — the repo's `.gitignore` already covers `.env.*`) or the user's secret manager. Never in chat, logs, or committed files.
- One tool at a time; only the scopes the intended read needs; read-only before anything else.
- Never ask the user to paste a token, client secret, refresh token, or private key into the conversation.

## 1. Check the environment first

For the repository CLIs: confirm this project's checkout path, run `node --version` (18+ required; `--env-file` needs 20.6+), and that the chosen CLI exists in `tools/clis/`. No dependency installation is needed — the CLIs are zero-dependency.

For hosted MCP in Antigravity: check that `.agents/mcp_config.json` is writable (copy from `.agents/mcp_config.example.json` on first use) and reload via `/mcp` after edits.

If neither path is available, explain the limitation and offer instructions for a compatible client.

## 2. Select only the needed tool

Ask which tool to connect and which account/property and environment (sandbox or production). Work on one chosen tool at a time; do not create apps, request unrelated scopes, or configure everything by default. For SEO/search/social/company data, options include the direct providers in the [registry](../../../tools/REGISTRY.md) and manual exports; partner status (◆) never selects the provider.

Keep each setup message to 3–5 lines: one action, why it is needed, the official link, and what nonsensitive confirmation to return. Wait for the user after app creation, permission approval, token generation, or account selection. Reuse completed steps and existing authorization.

## 3. Store selected credentials locally

With the user's permission create `.env.marketing` in the workspace root — owner-private, fail if it exists:

```bash
(umask 077; set -C; : > .env.marketing)
```

Build a template with only the chosen tool's variables (empty quoted values; the user fills them in a local editor — never print the completed file):

| Tool | Local variables |
|------|-----------------|
| Google Ads | `GOOGLE_ADS_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`; optional `GOOGLE_ADS_LOGIN_CUSTOMER_ID` |
| Meta Ads | `META_ACCESS_TOKEN`; optional `META_AD_ACCOUNT_ID` |
| LinkedIn Ads | `LINKEDIN_ACCESS_TOKEN` |
| GA4 | `GA4_ACCESS_TOKEN` |
| GSC | `GSC_ACCESS_TOKEN` |
| Stripe | `STRIPE_API_KEY` (restricted, customer-read, sandbox first) |
| PageSpeed/CrUX (free) | `GOOGLE_API_KEY` — also powers `tools/seo-runtime/run pagespeed_check.py` |
| Yandex Metrika | `YANDEX_METRIKA_TOKEN`; optional `YANDEX_METRIKA_COUNTER_ID` (OAuth scope `metrika:read`) |

Verify ignore rules **before** saving: `git check-ignore .env.marketing` must succeed. Refresh tokens and app secrets belong in the user's secret manager, not in this file. The CLIs consume access tokens and do not refresh them.

## 4. Complete the provider's flow

Follow the official flow for the selected tool (scoped guidance lives in `tools/integrations/<tool>.md`; the full list with boundaries is the [registry](../../../tools/REGISTRY.md)). General rules:

- Google Ads: project-level API access; single-user OAuth (Desktop App client), `adwords` scope; access token saved as `GOOGLE_ADS_TOKEN`.
- Meta/LinkedIn: app tied to the intended business/account; request `ads_read` / `r_ads`-family read scopes for a first report; check ad-access approval status before proceeding (external gate — pause that tool while pending, continue others).
- GA4/GSC: OAuth access token with `analytics.readonly` / Search Console read scope; numeric GA4 property ID (not `G-…`).
- Stripe: restricted key with customer-read only, in a sandbox.
- Yandex Metrika: OAuth app at oauth.yandex.ru with scope `metrika:read`, token into `.env.marketing`; full flow in `tools/integrations/yandex-metrika.md`. Powers `/daytona-seo-notch-analytics` (incl. Yandex search phrases).

## 5. Test a small read and inspect the response

Run from the project root (Node 20.6+ for `--env-file`):

```bash
node --env-file=.env.marketing tools/clis/google-ads.js account info
node --env-file=.env.marketing tools/clis/meta-ads.js accounts list
node --env-file=.env.marketing tools/clis/ga4.js reports run --property 123456789 --metrics activeUsers --start-date yesterday --end-date yesterday
node --env-file=.env.marketing tools/clis/google-search-console.js url inspect --url https://example.com/
node --env-file=.env.marketing tools/clis/yandex-metrika.js counters list
```

Run only the chosen line. Where supported, preview with `--dry-run` first (a preview proves request shape, not connectivity). Check both exit status **and** the provider response — some CLIs exit zero with an error payload. Record account/property, environment, operation, and outcome — without secrets or customer data. Empty results can be a valid connection.

| Failure | Next step |
|---------|-----------|
| Missing local variable | Verify variable names and how the CLI loads the file; never print values |
| Expired/invalid token | Check expiry; refresh via the authorized flow locally; do not retry repeatedly |
| Permission/project rejection | Check scopes, app approval, project access, account membership |
| Wrong account/property | Confirm the nonsensitive ID and sandbox/production context with the user |
| Rate limit or outage | Honor provider guidance; record blocked/pending, not "ready" |
| CLI route/version mismatch | Repair the checkout; never request wider permissions to mask a client defect |

## 6. Finish with first value

Report each tool as connected / waiting for user / waiting for provider / failed with a specific next step. Offer one small read-only result (account inventory, yesterday's active users, sandbox billing check) reusing the permission already granted; ask before touching another account. Route a full audit to the appropriate marketing or daytona-seo-notch skill. Campaign edits, sends, payments, and budget changes always need separate explicit authorization.

## 7. MCP servers for Antigravity

For data planes better consumed as MCP (DataForSEO, Firecrawl, AIsa, Omnia…):

1. Copy `.agents/mcp_config.example.json` → `.agents/mcp_config.json` (gitignored) and enable the chosen entry: remove `"disabled": true`, keep exactly one transport per server (`command` for local stdio, `serverUrl` for remote Streamable HTTP).
2. Keys go into the server's `env` block **by reference to `.env.marketing` values the user pastes locally in their editor** — or better, the user's secret manager; never into chat. Remote servers with OAuth (AIsa) prefer client-managed browser OAuth — then no local secret is needed at all.
3. Reload with `/mcp` in Antigravity and inspect the connection log; a listed tool set is not proof of authenticated access — run the provider's free/cheapest read before declaring the connection ready.
4. Budget-guarded providers (DataForSEO, AIsa): before any paid lookup, confirm scope, pricing, and budget authorization with the user.

## Related Skills

- `analytics`, `attribution`, `conversion-tracking`, `ads` — the consumers of these connections
- `daytona-seo-notch` (hub) — `GOOGLE_API_KEY` also unlocks the audit's Performance track; GSC/GA4 enrichment runs through `tools/seo-runtime/run google_auth.py --check`
