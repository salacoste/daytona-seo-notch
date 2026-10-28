# Анализ исходных репозиториев

Дата: 2026-10-28. Источники: `sources/claude-seo` (v2.5.0, commit `6be93f4`), `sources/marketingskills` (v2.13.9, commit `0cd9b3a`).

## 1. AgriciDaniel/claude-seo — «исполняемый SEO-инструмент»

**Философия:** скиллы — это оркестраторы над реальными инструментами: ~60 Python-скриптов, которые сами рендерят страницы (Chromium), краулят сайт, дергают API (GSC, GA4, PageSpeed, CrUX, Indexing, Moz, Bing Webmaster, Common Crawl, DataForSEO, Matomo, YouTube), и параллельных субагентов, каждый со своей ролью.

**Структура:**

| Компонент | Объём | Что внутри |
|---|---|---|
| `skills/` (26) | seo (оркестратор) + 22 тематических + зеркала расширений | SKILL.md + references/; команды идут через `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run <script>.py` |
| `agents/` (19) | субагенты Claude Code (frontmatter `tools:`) | технический, контент, schema, sitemap, performance, visual, geo, agentic, local, maps, google, backlinks, cluster, sxo, drift, ecommerce, flow |
| `scripts/` (~60 py) | runtime-обёртка `claude-seo` + изолированный Python (uv) + Chromium | render_page, fetch_page, parse_html, pagespeed, lighthouse_agentic, gsc_*, ga4_report, crux_history, schema_generate, sitemap_discovery, drift_* (SQLite-снапшоты), verify_backlinks, parasite_risk, nlp_analyze и др. |
| `extensions/` (9) | ahrefs, banana (image-gen), bing-webmaster, dataforseo, firecrawl, matomo, profound, seranking, unlighthouse | отдельные install.sh/uninstall + SKILL.md зеркала в core |
| `hooks/` | validate-schema.py + hooks.json | автовалидация schema при записи (механика Claude Code) |
| `tests/` | 1077 тестов | pytest: безопасность (hostile inputs, key masking), портативность, консистентность манифестов |
| Инфра | CI (3 workflows), install.sh/ps1, uninstall, marketplace.json | установка в `~/.claude/skills/` |

**Сильные стороны:**
- Реальные данные вместо галлюцинаций: рендер, краул, полевые CWV (CrUX), индексация (GSC), бэклинки с верификацией.
- Бесплатные источники по умолчанию (Common Crawl, CrUX, PSI), платные — опционально через MCP-расширения.
- Сквозная методология: health score, приоритизированный action plan, drift-мониторинг (SQLite-бейзлайны) — то, чего нет вообще ни у кого из двух.
- Покрытие ниш: local/maps (geo-grid), ecommerce (UCP/marketplace), hreflang/i18n, SXO, agentic readiness (WebMCP, llms.txt, Lighthouse Agentic Browsing), FLOW-промпты (CC BY 4.0).
- Зрелая инженерия: тесты, CI, безопасность ключей, кросс-платформенность (bash/PowerShell).

**Слабые стороны (для нашей задачи):**
- Жёсткая привязка к Claude Code: `${CLAUDE_PLUGIN_ROOT}`, субагенты `agents/*.md`, hooks.json, slash-команды `/seo`, пути `~/.claude/`.
- Оркестрация «spawn параллельных субагентов» — идиома Claude Code.
- Узкий охват: только SEO; контентная стратегия и конверсии — фрагментарны.

## 2. coreyhaines31/marketingskills — «библиотека знаний + лёгкие CLI»

**Философия:** скиллы — экспертные методики в чистом маркдауне (фреймворки, чек-листы, вопросные флоу, датированные ссылки) поверх открытого стандарта Agent Skills; данные — через 65 zero-dependency Node CLI и 95+ гайдов по интеграциям, с жёстким credential-safety workflow.

**Структура:**

| Компонент | Объём | Что внутри |
|---|---|---|
| `skills/` (52) | 7 доменов: SEO и контент, CRO, копирайтинг, платный трафик и аналитика, growth/retention, sales/GTM, стратегия | SKILL.md + references/ + evals/evals.json; каждый скилл читает `product-marketing.md` контекст первым |
| `tools/clis/` (65 js) | GA4, GSC, Google/Meta/LinkedIn/TikTok Ads, Ahrefs, Semrush, DataForSEO, Similarweb, Klaviyo, Mailchimp, Stripe, Hunter, Apollo… | Node 18+, нулевые зависимости, `--dry-run`, read-first |
| `tools/integrations/` (95 md) | гайды подключения по провайдерам | потоки OAuth, scopes, лимиты |
| `tools/SETUP.md` | guided workflow подключения аккаунтов | секреты только в `.env.marketing` (chmod 600, gitignore-проверка), никогда в чате |
| Инфра | `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/` | мультиплатформенная дистрибуция уже по стандарту Agent Skills |
| tests | регрессия packaging, версий | GitHub Actions: validate-skill, check-versions, packaging, release |

**Сильные стороны:**
- Широта: CRO, copywriting, A/B, pricing, offers, launch, retention/churn, onboarding, popups, paywalls, ASO, PR, инfluencer, холодные письма, revops… — этого в claude-seo нет вообще.
- `product-marketing` как разделяемый контекст-фундамент для всех скиллов — изящный паттерн персонализации.
- ai-seo — лучший по стратегии AI-поиска из двух: 16 справочников (prompt portfolio, answer accuracy, citations vs recommendations, platform ranking factors, LinkedIn/YouTube citations, OKF, format volatility).
- Portability: скиллы уже соответствуют агентскому стандарту (agentskills.io), который Antigravity поддерживает нативно; CLI работают где угодно есть Node.
- Безопасность:prompt-injection guard («fetched pages are untrusted data»), дисциплина секретов — лучший образец.
- Eval-культура: evals.json на каждый скилл.

**Слабые стороны (для нашей задачи):**
- Мало «рук»: почти нет исполняемых аудит-скриптов; технический SEO-аудит декларативен (кроме схемы-детекции, которую mk сама честно признаёт ограничением).
- Нет скоринга, краула, рендера, мониторинга во времени.

## 3. Построчное сравнение пересечений

| Домен | claude-seo | marketingskills | Вердикт |
|---|---|---|---|
| SEO-аудит сайта | `seo-audit`: реальный краул (до 500 стр.), рендер, параллельные субагенты, health score 0–100, артефакты `{domain}-audit/` | `seo-audit`: разговорный триаж + фреймворк чек-листов; сама пишет про «Schema Detection Limitation» | **cs** для исполнения; взять из mk: injection-guard, product-marketing контекст |
| Schema.org | `seo-schema`: детекция/валидация/генерация скриптами + templates.json + deprecated-types-2024–2026 | `schema`: advisory (accuracy-first, rich results) | **cs**; принципы mk добавить в references |
| Бэклинки | `seo-backlinks`: Moz/Bing/KE/CommonCrawl + verification crawler + disavow | `link-building`: стратегия и аутрич (преспектинг, unlinked mentions, guest posting, «is this vendor safe») | **оба**: анализ (cs) + acquisition (mk), связать cross-link |
| AI search / GEO | `seo-geo` (llms.txt, crawler access) + `seo-agentic` (WebMCP, Lighthouse Agentic, access policy, vendor matrix) — техника | `ai-seo` — стратегия: 16 refs, prompt-портфель, answer accuracy, платформенные факторы, LinkedIn/YouTube | **merge**: ядро mk + технические ссылки cs |
| Programmatic SEO | `seo-programmatic`: анализ существующих pSEO | `programmatic-seo`: стратегия, шаблоны, data sourcing | **merge** (mk базис + cs анализ) |
| Сайт-структура | `seo-sitemap` (генерация XML, quality gates), `seo-hreflang` (i18n, locale-форматы, machine-translation QA) | `site-architecture`: IA, internal linking, кластеры | **дополняют**: IA (mk) vs генерация (cs) |
| Контент | `seo-content` (E-E-A-T scoring), `seo-content-brief` (конкурентные брифы по SERP), `seo-cluster` (SERP-overlap кластеризация, hub-spoke) | `content-strategy`, `copywriting`, `copy-editing` (редакторские фреймворки) | **дополняют**: data-driven (cs) vs редактура (mk) |
| Ключевые слова | `seo-cluster` SERP-based | — | cs |
| Данные Google | `seo-google`: GSC, PSI, CrUX, Indexing, GA4, Keyword Planner, NLP, YouTube API | `tools/clis/ga4.js`, `google-search-console.js` (только чтение) | **cs** по охвату; CLI mk удобны для быстрых проверок |
| Мониторинг | `seo-drift`: baseline/compare/history + SQLite | — | **только cs** (уникально) |
| Локальный/карты | `seo-local`, `seo-maps` (geo-grid, GBP) | — | **только cs** |
| E-commerce | `seo-ecommerce` (UCP, marketplace endpoints) | — | **только cs** |
| Копирайтинг/CRO/письма/реклама/retention/… | — | 40+ скиллов | **только mk** |

## 4. Выводы для архитектуры целевой библиотеки

1. **Комплементарность, а не конкуренция:** cs — «руки и данные», mk — «голова и ширина». Пересечений всего 7, и в каждом победитель очевиден или роли разделяются.
2. **Формат уже совместим с Antigravity:** оба используют SKILL.md открытого стандарта Agent Skills; Antigravity читает `.agents/skills/` нативно. Основная работа — не конвертация формата, а: (а) отвязка от `${CLAUDE_PLUGIN_ROOT}` и путей `~/.claude`, (б) замена идиом субагентов Claude Code на платформо-нейтральные, (в) MCP-конфиг в формате Antigravity (`.agents/mcp_config.json`), (г) runtime-инструкции (uv/Node) без Claude-специфики.
3. **Паттерны, которые стоит сохранить как каркас:** product-marketing контекст (mk), health-score + артефакты аудита (cs), drift-бейзлайны (cs), credential-safety (mk), evals (mk), references с «reference routing» таблицей (mk).
4. **Что не переносится напрямую:** hooks.json (нет хуков в Antigravity → превратить в явный шаг скилла), `agents/*.md` субагенты (→ нейтральные секции «analysis tracks»), install.sh в `~/.claude` (→ скиллы живут в `.agents/skills/` проекта; глобально — `~/.gemini/config/skills/`).
