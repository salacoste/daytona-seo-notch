# Yandex Metrika

Web analytics for Yandex-ecosystem traffic: visits, sources, behavior, goals — and the actual Yandex search phrases (`ym:s:searchPhrase`) that GA4 does not expose.

- API base: `https://api-metrika.yandex.net` (Management `v1`, Stats `stat/v1/data`)
- Auth: OAuth token, scope `metrika:read`
- Cost: free (counter required; Logs API is not used by our tooling)
- CLI: `tools/clis/yandex-metrika.js` (zero-dependency, read-only)
- MCP alternative: [askads/mcp-yandex-metrica](https://github.com/askads/mcp-yandex-metrica) (add to `.agents/mcp_config.json` if you prefer interactive exploration over scripted reads)

## Local variables

```dotenv
YANDEX_METRIKA_TOKEN=""        # OAuth token, scope metrika:read
YANDEX_METRIKA_COUNTER_ID=""   # optional default counter id
```

## Token flow (user performs locally; never paste tokens into chat)

1. Create an OAuth app at [oauth.yandex.ru](https://oauth.yandex.ru) (or reuse an existing one); requested scope: `metrika:read`.
2. Authorize in the browser: `https://oauth.yandex.ru/authorize?response_type=token&client_id=<APP_ID>` — the token arrives in the redirect URL fragment; the user copies it into `.env.marketing` locally.
3. Confirm nonsensitively: counter access can be verified with `counters list` below.

## Read-only test (first value)

```bash
node --env-file=.env.marketing tools/clis/yandex-metrika.js counters list
node --env-file=.env.marketing tools/clis/yandex-metrika.js stats summary --start 2026-10-01 --end 2026-10-28
```

Expect a counters list and period totals (visits/users/pageviews/bounce/duration). HTTP 403 → token lacks `metrika:read` or no counter access; 400 with `missed_parameter` → check counter id.

## Boundaries

- Only `management/v1` GET and `stat/v1/data` are used; no writes, no Logs API (visitor-level data stays out)
- Sampling: large periods may return `sample_share > 0` — report it, use proportions
- Rate limits: the CLI retries nothing; on 429 back off and widen the period
