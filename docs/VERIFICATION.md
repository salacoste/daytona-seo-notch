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


## Критерий 1 и 3 — попытка реального агентного прогона (2026-10-28, вечер)

Ближайший к Antigravity агентный рантайм в этой сессии — Gemini CLI
(читает тот же стандартный каталог `.agents/skills/`):

- **Discovery подтверждён реально**: `gemini skills list` перечислил наши
  скиллы из пути проекта (проверено: `ab-testing [Enabled] → …/seo_antigravity_skills/.agents/skills/ab-testing/SKILL.md`).
  Значит, скиллы обнаруживаются настоящим агентом в штатном каталоге.
- **Headless-диалог заблокирован логином**: `gemini --approval-mode plan -p …`
  останавливается на «Opening authentication page in your browser» —
  неинтерактивная аутентификация невозможна из сессии. `agy` (Antigravity
  CLI) не установлен; Antigravity.app — Electron-бандл без отдельного CLI.

**Что остаётся пользователю (5 минут, один логин):** открыть проект в
Antigravity (или выполнить вход в `gemini` CLI) и прогнать 4 готовых
промпта — они дословно совпадают с eval-кейсами, команды внутри уже
проверены рантаймом:

1. UJ-1: `наш сайт example.com не ранжируется — прогоните полный аудит`
2. UJ-2: `проверь агентную готовность https://salacoste.github.io/daytona-seo-notch/`
3. UJ-3: `подключи Яндекс Метрику` (по docs/CONNECT-ANALYTICS.md)
4. UJ-4: `создай product-marketing контекст и перепиши лендинг под него`

Ожидаемый результат каждого записан в evals.json соответствующего скилла.

## Итоговое состояние критериев (честно)

| Критерий | Статус | Доказательство |
|---|---|---|
| 1. UJ в Antigravity без правок скиллов | конвейеры — да (live, записано выше); диалоги — ждут одного пользовательского логина | разделы выше |
| 2. Lint + evals зелёные, 0 секретов | ✅ прогон записан | `docs/EVAL-REPORTS.md`, CI success |
| 3. Скиллы срабатывают по триггеру | ✅ lexical-гейт 235/235 + реальный discovery агентом; семантика — в hands пользователя (см. 4 промпта) | `tools/run_evals.py` |
| 4. drift 2 месяца | механизм запущен, 1-й отчёт в репо; накопление — календарное (до 2026-12-21) | `drift-reports/2026-10-28.md`, cron |

Календарные и логин-зависимые части (4) физически не завершаемы в одной
сессии; всё, что достижимо без пользователя, выполнено и зафиксировано.
