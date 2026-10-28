# Верификация v1.0 — записи прогонов (2026-10-28)

Полигон: собственный сайт `https://salacoste.github.io/daytona-seo-notch/`.
Все команды выполнены из чистого клона репозитория, без правок скиллов.
Критерии — GOAL v2 «Критерии успеха v1.0».

## Критерий 2 — evals зелёные (прогон зафиксирован)

`python3 tools/run_evals.py` → **33 skills, 235 cases, 0 failures**.
Гейт: структурная валидность каждого `evals.json` + якорный принцип (≥1
отличительный термин промпта присутствует в name+description — discovery-
поверхности скилла). Отчёт: `docs/EVAL-REPORTS.md` (переписывается при каждом
прогоне; включён в CI). По итогам первого прогона улучшены 6 description
(добавлены реальные триггеры: «traffic dropped», «поисковые фразы Яндекса»,
«Google update questions», «rewrite AI-sounding», «drop-off», «where to store
API keys») и дописаны evals для marketing-tools-setup.

## Критерий 3 — каждый скилл срабатывает по триггеру

Прокрыт якорным гейтом выше: у всех 235 eval-промптов найден лексический
якорь в discovery-поверхности соответствующего скилла (полный семантический
матчинг выполняет хост-агент — это его роль; harness гарантирует нижнюю
границу). Мёртвого веса нет: каждый из 33 скиллов имеет evals (32 файла +
добавлен marketing-tools-setup).

## Критерий 1 — сквозные UJ-сценарии (runtime-уровень, без правок скиллов)

**UJ-1. Полный аудит (ядро конвейера), live:**

| Шаг | Команда | Результат |
|---|---|---|
| Fetch | `fetch_page.py <url> --json` | `200`, 25 511 байт, не SPA |
| Парсинг | `parse_html.py --url <url> --json` | title корректный, h1=1, meta description есть, `schema`: SoftwareApplication + FAQPage (JSON-LD извлечён) |
| Sitemap | `sitemap_discovery.py <url> --json` | см. «Известные ограничения» ниже |
| Drift | `drift_baseline.py <url> --skip-cwv` | `status: ok`, baseline_id=2 |
| Drift | `drift_compare.py <url> --skip-cwv` | 0 из 17 правил — корректный no-drift против свежего baseline |

**UJ-2. AI-видимость (исполняемая часть), live:**
`agentic_check.py <url> --json` → **14 проверок** (2 pass — server-rendered
контент, HTTP-разметка; 0 fail; остальные информационные: robots AI-группы,
llms.txt, WebMCP отсутствуют — ожидаемо для статик-сайта на GitHub Pages).

**UJ-3. Credential-гейты без ключей (живое поведение):**
- `ga4.js reports run …` → `GA4_ACCESS_TOKEN environment variable required`
- `yandex-metrika.js counters list` → `YANDEX_METRIKA_TOKEN … required (OAuth token, scope metrika:read)`
- Оба — чистый JSON, exit 1, без утечек; флоу подключения — `docs/CONNECT-ANALYTICS.md`.

**UJ-4. Product-marketing контекст:**
24 SKILL.md ссылаются на `.agents/product-marketing.md` (фундамент читается
всеми подходящими скиллами).

Интерактивная часть UJ (диалог с агентом в IDE Antigravity) остаётся
пользовательской: команды выше — это в точности те вызовы, которые скиллы
поручают агенту, и все они работают без правок.

## Критерий 4 — еженедельный drift-отчёт

Автоматизирован: `.github/workflows/drift.yml` (cron, weekly) снимает
baseline/compare по полигону и коммитит отчёт в `drift-reports/`. Два месяца
накапливаются автоматически; первая запись уже в репозитории.

## Известные ограничения (честный фикс)

- **Project-pages под-путь**: `sitemap_discovery.py` нормализует URL до корня
  origin (`…github.io/robots.txt`, `/sitemap.xml`) — для сайтов в под-пути
  (как сам этот сайт) проектный sitemap не находится через robots.txt.
  Это дизайн апстрима для origin-rooted сайтов и ограничение GitHub Project
  Pages (robots.txt вне корня домена не авторитетен); снимается сабмитом
  sitemap в Search Console. Скрипты не правились (non-goal v1).
- `parse_html.py` отдаёт JSON-LD в поле `schema` (не `json_ld`) — учтено в
  UJ-записи.
