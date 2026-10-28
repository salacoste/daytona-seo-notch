#!/usr/bin/env node
// Yandex Metrika CLI — read-only web analytics for SEO work.
// Conventions match the other zero-dependency CLIs in tools/clis/:
// env-token auth, JSON output, --dry-run preview, no secrets in output.
//
// Env:
//   YANDEX_METRIKA_TOKEN      required — OAuth token, scope metrika:read
//   YANDEX_METRIKA_COUNTER_ID optional — default counter for stats commands
//
// Examples:
//   node tools/clis/yandex-metrika.js counters list
//   node tools/clis/yandex-metrika.js goals list --counter 123456
//   node tools/clis/yandex-metrika.js stats summary --start 2026-10-01 --end 2026-10-28
//   node tools/clis/yandex-metrika.js stats sources --start 2026-10-01 --end 2026-10-28
//   node tools/clis/yandex-metrika.js stats phrases --start 2026-10-01 --end 2026-10-28 --limit 30
//   node tools/clis/yandex-metrika.js stats query --metrics ym:s:visits --dimensions ym:s:date --start 2026-10-01 --end 2026-10-28

const rawArgs = process.argv.slice(2)
const TOKEN = process.env.YANDEX_METRIKA_TOKEN
const DEFAULT_COUNTER = process.env.YANDEX_METRIKA_COUNTER_ID
const API_BASE = process.env.YANDEX_METRIKA_API_BASE || 'https://api-metrika.yandex.net'
const LANG = process.env.YANDEX_METRIKA_LANG || 'ru'

function requestSignal() {
  const raw = args['timeout-ms'] ?? '60000'
  const ms = Number(raw)
  if (typeof raw !== 'string' || !/^\d+$/.test(raw) || !Number.isSafeInteger(ms) || ms < 1 || ms > 600000) {
    throw new Error('--timeout-ms must be an integer from 1 to 600000')
  }
  return AbortSignal.timeout(ms)
}

function parseArgs(argv) {
  const result = { _: [] }
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i]
    if (arg.startsWith('--')) {
      const key = arg.slice(2)
      const next = argv[i + 1]
      if (next && !next.startsWith('--')) {
        result[key] = next
        i++
      } else {
        result[key] = true
      }
    } else {
      result._.push(arg)
    }
  }
  return result
}

const args = parseArgs(rawArgs)
const [group, cmd, ...rest] = args._

function out(data) {
  console.log(JSON.stringify(data, null, 2))
}

function requireToken() {
  if (!TOKEN) {
    out({ error: 'YANDEX_METRIKA_TOKEN environment variable required (OAuth token, scope metrika:read). Keep it in .env.marketing, never in chat.' })
    process.exitCode = 1
    return false
  }
  return true
}

function requireCounter() {
  const counter = args.counter || DEFAULT_COUNTER
  if (!counter || !/^\d+$/.test(String(counter))) {
    out({ error: 'counter id required: pass --counter <id> or set YANDEX_METRIKA_COUNTER_ID. Find ids with: counters list' })
    process.exitCode = 1
    return null
  }
  return String(counter)
}

function validDate(value, name) {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throw new Error(`${name} must be YYYY-MM-DD (got: ${value})`)
  }
  return value
}

async function apiGet(path) {
  if (args['dry-run']) {
    return { _dry_run: true, method: 'GET', url: `${API_BASE}${path}`, headers: { Authorization: 'OAuth ***', 'Accept-Language': LANG } }
  }
  const res = await fetch(`${API_BASE}${path}`, {
    signal: requestSignal(),
    headers: { Authorization: `OAuth ${TOKEN}`, 'Accept-Language': LANG },
  })
  const text = await res.text()
  try {
    return { http_status: res.status, ...(JSON.parse(text)) }
  } catch {
    return { http_status: res.status, body: text }
  }
}

async function statsPost(counter, params) {
  const body = { id: Number(counter), params }
  if (args['dry-run']) {
    return { _dry_run: true, method: 'POST', url: `${API_BASE}/stat/v1/data`, headers: { Authorization: 'OAuth ***', 'Content-Type': 'application/json' }, body }
  }
  const res = await fetch(`${API_BASE}/stat/v1/data`, {
    signal: requestSignal(),
    method: 'POST',
    headers: { Authorization: `OAuth ${TOKEN}`, 'Content-Type': 'application/json', 'Accept-Language': LANG },
    body: JSON.stringify(body),
  })
  const text = await res.text()
  try {
    return { http_status: res.status, ...(JSON.parse(text)) }
  } catch {
    return { http_status: res.status, body: text }
  }
}

// stat/v1/data rows: [{dimensions: [{name}], metrics: [n, ...]}]
function simplifyRows(payload) {
  const rows = payload?.data ?? []
  return rows.map((row) => {
    const record = {}
    row.dimensions?.forEach((d, i) => { record[`dim${i === 0 ? '' : i}` || 'dim'] = d.name })
    row.metrics?.forEach((m, i) => { record[`m${i}`] = m })
    return record
  })
}

async function main() {
  if (!group || group === 'help' || args.help) {
    out({
      tool: 'yandex-metrika.js',
      groups: {
        counters: 'list [--search q]',
        goals: 'list [--counter id]',
        stats: 'summary | sources | phrases | pages | devices | query --start YYYY-MM-DD --end YYYY-MM-DD [--counter id] [--limit n] [--metrics a,b] [--dimensions a,b] [--filter expr]',
      },
      env: ['YANDEX_METRIKA_TOKEN', 'YANDEX_METRIKA_COUNTER_ID (optional)'],
      notes: 'read-only; POST is used only for the stat/v1/data reporting endpoint; --dry-run previews the request',
    })
    return
  }

  if (group === 'counters' && cmd === 'list') {
    if (!requireToken()) return
    const search = args.search ? `&search=${encodeURIComponent(args.search)}` : ''
    out(await apiGet(`/management/v1/counters?fieldNames=counter_id,counter_name,site,metrika_type,status${search}`))
    return
  }

  if (group === 'goals' && cmd === 'list') {
    if (!requireToken()) return
    const counter = requireCounter()
    if (!counter) return
    out(await apiGet(`/management/v1/counter/${counter}/goals`))
    return
  }

  if (group === 'stats') {
    if (!requireToken()) return
    const counter = requireCounter()
    if (!counter) return
    const limit = Math.min(Number(args.limit ?? 20) || 20, 10000)
    const date1 = validDate(args.start, '--start')
    const date2 = validDate(args.end, '--end')

    if (cmd === 'summary') {
      const payload = await statsPost(counter, {
        metrics: ['ym:s:visits', 'ym:s:users', 'ym:s:pageviews', 'ym:s:bounceRate', 'ym:s:avgVisitDurationSeconds'],
        dimensions: [],
        date1, date2, limit: 1, accuracy: 'full',
      })
      if (payload?._dry_run) { out(payload); return }
      const totals = payload?.totals
      out({
        counter: Number(counter),
        period: { start: date1, end: date2 },
        visits: totals?.[0] ?? null,
        users: totals?.[1] ?? null,
        pageviews: totals?.[2] ?? null,
        bounce_rate: totals?.[3] ?? null,
        avg_visit_duration_seconds: totals?.[4] ?? null,
        _raw_keys: ['totals', 'sample_share', 'sample_size'],
        sample_share: payload?.sample_share ?? null,
      })
      return
    }

    const presets = {
      sources: { dimensions: ['ym:s:lastTrafficSource'], metrics: ['ym:s:visits', 'ym:s:users', 'ym:s:bounceRate'], sort: '-ym:s:visits' },
      phrases: { dimensions: ['ym:s:searchPhrase'], metrics: ['ym:s:visits'], sort: '-ym:s:visits' },
      pages: { dimensions: ['ym:pv:URLPath'], metrics: ['ym:pv:pageviews', 'ym:pv:avgVisitDurationSeconds'], sort: '-ym:pv:pageviews' },
      devices: { dimensions: ['ym:s:deviceCategory'], metrics: ['ym:s:visits'], sort: '-ym:s:visits' },
    }

    if (presets[cmd]) {
      const payload = await statsPost(counter, { ...presets[cmd], date1, date2, limit, accuracy: 'full' })
      if (payload?._dry_run) { out(payload); return }
      out({
        counter: Number(counter),
        period: { start: date1, end: date2 },
        query: presets[cmd],
        rows: simplifyRows(payload),
        totals: payload?.totals ?? null,
        sample_share: payload?.sample_share ?? null,
      })
      return
    }

    if (cmd === 'query') {
      if (rest.length && !args.metrics) throw new Error('stats query requires --metrics (and optional --dimensions), comma-separated, e.g. ym:s:visits,ym:s:users')
      const metrics = String(args.metrics || 'ym:s:visits').split(',').map((s) => s.trim()).filter(Boolean)
      const dimensions = String(args.dimensions || '').split(',').map((s) => s.trim()).filter(Boolean)
      const params = { metrics, dimensions, date1, date2, limit, accuracy: 'full' }
      if (args.filter) params.filters = String(args.filter)
      if (args.sort) params.sort = String(args.sort)
      const payload = await statsPost(counter, params)
      if (payload?._dry_run) { out(payload); return }
      out({
        counter: Number(counter),
        period: { start: date1, end: date2 },
        query: params,
        rows: simplifyRows(payload),
        totals: payload?.totals ?? null,
        sample_share: payload?.sample_share ?? null,
      })
      return
    }

    throw new Error(`unknown stats command: ${cmd}. Use summary | sources | phrases | pages | devices | query`)
  }

  throw new Error(`unknown group: ${group}. Use counters | goals | stats (or help)`)
}

main().catch((error) => {
  out({ error: error.message })
  process.exitCode = 1
})
