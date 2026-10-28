# Справочник скиллов (все 35)

Группы: [SEO-линейка daytona](#seo-линейка-daytona-seo-notch) ·
[Маркетинговый набор](#маркетинговый-набор-marketingskills) ·
[Инфраструктура](#инфраструктура).
Формат: назначение · когда применять · команды/артефакты · связи.

## SEO-линейка daytona-seo-notch

### `/daytona-seo-notch-brief` — intake новых проектов
Полная цепочка: бриф клиента → локальный разбор существующего кода/контента
(каждый факт с файлом-источником) → согласованные запросы (`queries.md` —
контракт стратегии) → частотность (Keyword Planner / DataForSEO /
Wordstat-флоу; каждое число с тегом источника) → handoff в стратегию.
**Когда:** новый клиент, «о чём сайт», «собрать запросы», «частотность»,
«разбери что уже есть». **Артефакты:** `brief-<slug>/`,
`local-scan.md`, `queries.md`. **Связи:** `prelaunch` (потребитель).

### `/daytona-seo-notch-prelaunch` — SEO до публикации
4 фазы: стратегия (тип сайта, IA/URL-карта из запросов, контент-план) →
сборка (проверки шаблонов на dev-сервере) → pre-launch гейт (полный аудит
`localhost`/`dist` через `CLAUDE_SEO_LOCAL_TARGETS`, sitemap-генерация,
AI-readiness, drift-база до запуска, CI-гейт) → go-live свитч (ноль решений:
noindex-снятие с верификацией, GSC/Вебмастер, аналитика, prod-baseline,
IndexNow). Плейбуки: корп. сайт / лендинг / блог. **Когда:** сайт верстается.
**Связи:** `brief`, вся аудиторская линейка.

### `/daytona-seo-notch` — хаб
Роутинг по линейке; `/daytona-seo-notch setup` (uv-окружение + Chromium) и
`doctor`; методология синтеза 10 принципов (PERCEIVE→ANALYZE→VALIDATE→ACT);
quality gates; веса health score; справочники (thinking-framework, CWV,
schema-types, E-E-A-T). **Когда:** непонятно, какой скилл нужен; сетап;
вопросы про Google-обновления (леджер `seo_updates.py`).

### `/daytona-seo-notch-audit` — полный аудит сайта
Краул ≤500 страниц (robots-уважение), треки: технический (вкл. AI-краулеры),
контент (E-E-A-T), schema, sitemap, performance (условно `GOOGLE_API_KEY`),
AI-readiness, условные обогащения (google/matomo/backlinks/drift/analytics).
Итог: **SEO Health Score 0–100**, приоритизированный план (Critical→Low),
артефакты `{domain}-audit/` (отчёт, план, `audit-data.json`, findings/).
**Когда:** «почему сайт не ранжируется», регулярные проверки, после релизов.

### `/daytona-seo-notch-page` — глубокий разбор одной страницы
On-page (title 50–60 / meta 150–160 / один H1), контент против минимумов
типа страницы, техблок (canonical, robots, OG/Twitter, hreflang), schema с
готовым JSON-LD, картинки (вкл. нюансы lazy-load), CWV-риски как флаги.
**Когда:** лендинги, ключевые страницы, «разбери эту страницу».

### `/daytona-seo-notch-technical` — технический SEO-аудит (9 категорий)
Краулинг (robots, sitemap через `sitemap_discovery.py`, noindex, глубина,
2MB-лимит Googlebot), индексируемость, безопасность, URL, мобильность, CWV,
рендеринг (JS-зависимый контент), структурированные данные, IndexNow. Вкл.
**менеджмент AI-краулеров**: таблица GPTBot vs OAI-SearchBot vs
Claude-SearchBot vs Google-Extended с правильными различиями целей.
**Когда:** «технический аудит», «заблокировать gptbot?», проблемы индексации.

### `/daytona-seo-notch-content` — контент и E-E-A-T
Тест Who/How/Why → E-E-A-T по критериям QRG (сент. 2025) → минимумы контента
по типам страниц (quality-gates) → читабельность, свежесть,
AI-citation-готовность; финальная чистка AI-штампов и невидимых Unicode-маркеров.
Скоры честно помечены как эвристики. **Когда:** «хватит ли контента чтобы
ранжироваться», «перепиши, чтоб не звучало как ИИ».

### `/daytona-seo-notch-schema` — Schema.org
Детекция (JSON-LD/microdata/RDFa через `parse_html.py`), валидация
(обязательные поля, абсолютные URL, даты, плейсхолдеры), генерация готового
JSON-LD из `schema/templates.json`; политика деприкаций: HowTo — никогда,
FAQPage — rich results закрыты с мая 2026 (Info, не удалять), QAPage для
настоящих Q&A. **Когда:** «добавить схему», «почему нет rich results».

### `/daytona-seo-notch-sitemap` — sitemap.xml
Discovery-first анализ (не объявлять «нет sitemap» до
`sitemap_discovery.py`): лимиты 50k/50MB, HTTP-200, точность W3C lastmod,
деприкейтед priority/changefreq, не-канонические/noindex/редиректы в карте;
генерация с индекс-файлами и разбивкой по типам контента. **Когда:** «sitemap»,
генерация для нового сайта.

### `/daytona-seo-notch-ai` — AI-видимость (мерж стратегии и техники)
Стратегия: аудит видимости (10–20 revenue-промптов), 3 столпа
(структура/авторитет/присутствие), платформенные различия Google vs
ChatGPT/Perplexity, prompt-портфель, machine-readable файлы (pricing.md,
llms.txt, OKF), мониторинг. Техника (исполняемо): `agentic_check.py`,
`agent_ux_check.py`, `lighthouse_agentic.py` (X/N, не проценты!),
приоритеты P0–P3, fix-mode (`agentic_fix.py`), GEO-скоринг (llms.txt — вес 0).
15+8 справочников. **Когда:** «как попасть в ответы ChatGPT/Overviews»,
«агентная готовность».

### `/daytona-seo-notch-drift` — мониторинг изменений
baseline → compare (17 правил, CRITICAL/WARNING/INFO) → history; SQLite в
`~/.cache/daytona-seo-notch/` (override `DAYTONA_DRIFT_DIR`); HTML-reports.
**Когда:** после деплоев, «что изменилось на странице», еженедельный контроль.

### `/daytona-seo-notch-analytics` — трафик GA4+Метрика+GSC
Детект креденшалов → `overview` / `organic` (сплит движков!) / `phrases`
(поисковые фразы Яндекса — этого нет в GA4) / `landing` / `compare` (честная
таблица расхождений GA4↔Метрика). Read-only. **Когда:** «сколько посещений»,
«откуда трафик», «упал Яндекс или Google».

## Маркетинговый набор (marketingskills)

Все читают `.agents/product-marketing.md` (контекст-фундамент) первым делом;
у каждого — evals.

**Фундамент:**
- `/product-marketing` — создание/обновление контекст-документа продукта
  (аудитория, персоны, позиционирование, возражения, пруфы). Создайте первым.

**Конверсии и копирайтинг:**
- `/cro` — конверсионная оптимизация страниц и форм; `/copywriting` —
  копирайтинг любых страниц; `/copy-editing` — редактура и рефреш старого;
  `/ab-testing` — дизайн экспериментов и матстатистика; `/popups` —
  попапы/оверлеи; `/onboarding` — активация после регистрации.

**Ценообразование и офферы:**
- `/pricing` — решения по ценам и упаковке; `/offers` — конструкция оффера;
  `/paywalls` — пейволлы и апселлы; `/signup` — страницы регистрации.

**Платный трафик и измерения:**
- `/ads` (Google/Meta/LinkedIn/TikTok кампании, 16 справочников),
  `/ad-creative` — генерация креативов, `/analytics` — настройка/аудит
  аналитики, `/attribution` — модели атрибуции, `/conversion-tracking` —
  внедрение конверсий (GTM-рецепты, сниппеты).

**GTM и аутрич:**
- `/cold-email` — B2B-аутрич-системы; `/launch` — запуск продукта;
  `/competitors` — страницы сравнения; `/competitor-profiling` — профили
  конкурентов по URL; `/customer-research` — исследования (интервью,
  churn/drop-off); `/prospecting` (в v1.1) — списки проспектов.

**Контент и SEO-смежные:**
- `/content-strategy` — редакторская стратегия; `/link-building` —
  стратегия ссылок/упоминаний (роли разделены с daytona-анализом);
  `/programmatic-seo` — pSEO-стратегия; `/site-architecture` — IA и
  внутренняя перелинковка; `/emails` — lifecycle-последовательности.

## Инфраструктура

### `/marketing-tools-setup` — подключение данных
Пошаговое подключение аккаунтов (GA4, Ads, GSC, Метрика, Stripe…) и
MCP-серверов: один инструмент за раз, секреты только в `.env.marketing`
(0600), read-only тест первым, бюджет-гарды для платных. Антигейт: токены
никогда в чате. **Когда:** любые «подключи API/ключи/MCP».

---

Сценарные мануалы: [новый сайт](scenario-new-site.md) ·
[в разработке](scenario-in-development.md) ·
[опубликованный](scenario-live-site.md)
