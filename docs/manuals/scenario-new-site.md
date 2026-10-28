# Сценарий 1. Новый сайт с нуля

**Ситуация:** есть клиент или своя идея; ни кода, ни контента, ни доменной
истории. Цель — прийти к запуску с готовой SEO-стратегией и сайтом, который
проходит аудит до публикации.

## Карта пути

```
Шаг 1        Шаг 2            Шаг 3            Шаг 4              Шаг 5
Бриф    →    Запросы +    →   Стратегия    →   Верстка        →   Запуск
             частотность      и IA             (гейт на dev)      (свитч)
/daytona-    /daytona-        /daytona-        /daytona-          /daytona-
seo-notch-   seo-notch-       seo-notch-       seo-notch-         seo-notch-
brief        brief (C-D)      prelaunch        prelaunch          prelaunch
                              (Phase 0)        (Phase 1–2)        (Phase 3)
```

## Шаг 1 — Бриф клиента: `/daytona-seo-notch-brief`

1. Запустите скилл; ответьте на вопросы брифа пачками (бизнес, аудитория,
   конкуренты, рынки/языки, цели, ограничения).
2. Обязательно зафиксируйте **приоритет Яндекс vs Google** (RU/CIS) — от него
   зависят источники частотности и чек-лист запуска.
3. Артефакт: `brief-<slug>/brief-<slug>.md`.

## Шаг 2 — Запросы и частотность: `/daytona-seo-notch-brief` (стадии C–D)

1. Seed-пул: ответы брифа + лексика конкурентов (публичные страницы).
2. Расширение: `tools/seo-runtime/run keyword_planner.py ideas "<seed>"
   --limit 50 --language 1048 --location 643 --json` (RU) — при подключённых
   Google Ads креденшалах (`/marketing-tools-setup`).
3. Частотность: Keyword Planner (`volume`), DataForSEO (платно, точно),
   Wordstat — полуручной флоу (скилл подготовит ссылки; вставьте выгрузку).
4. **Гейт согласования:** таблица `queries.md` (запрос · интент · тип
   страницы · приоритет · частотность с тегом источника) подписывается
   клиентом построчно.

## Шаг 3 — Стратегия и архитектура: `/daytona-seo-notch-prelaunch` (Phase 0)

1. Тип сайта (корп. / лендинг / блог / гибрид) → плейбук из
   `references/site-types.md`.
2. IA → URL-карта: на каждый URL — запрос (из согласованных), черновик
   title, тип schema (`schema_generate.py`, шаблоны в
   `tools/seo-runtime/schema/templates.json`).
3. Правила глубины (деньжовые страницы ≤3 кликов), canonical-схема,
   hreflang-план (если мультиязычно), контент-план/календарь (для блога).
4. Артефакт: `docs/seo-plan.md`.

## Шаг 4 — Верстка с SEO-проверками: `/daytona-seo-notch-prelaunch` (Phase 1–2)

На каждом шаблоне dev-сервера (экспортируйте `CLAUDE_SEO_LOCAL_TARGETS=
localhost:<порт>`):

1. Phase 1 — проверки per-шаблон: title/meta/H1 (`parse_html.py --url
   http://localhost:<порт>/<роут> --json`), SSR-контент, JSON-LD, картинки,
   staging-noindex через env.
2. Phase 2 — гейт перед запуском:
   - `/daytona-seo-notch-audit http://localhost:<порт>` — health score как
     метрика гейта;
   - `/daytona-seo-notch-sitemap generate` — реальный sitemap.xml;
   - `/daytona-seo-notch-ai readiness` — llms.txt/robots-AI/WebMCP;
   - `/daytona-seo-notch-drift baseline` — база до запуска;
   - CI-гейт на PR (рецепт: `references/dev-workflow.md` скилла).
3. Полный печатный чек-лист: `references/prelaunch-checklist.md`.

## Шаг 5 — Запуск без импровизации: `/daytona-seo-notch-prelaunch` (Phase 3)

Свитч по порядку: HTTPS/редиректы → **снять noindex** (проверка
`fetch_page.py <url> --json`) → robots.txt + sitemap + GSC/Яндекс.Вебмастер →
аналитика GA4/Метрика (`/daytona-seo-notch-analytics`) → первый прод-aудит →
`/daytona-seo-notch-drift baseline <prod>` → IndexNow.

## Скиллы сценария (порядок)

`brief` → `prelaunch` → (`audit`, `sitemap`, `ai`, `schema`, `page` — по мере
шаблонов) → `drift` → `analytics` → `marketing-tools-setup` (подключения).

## Частые ошибки

- Придумывать запросы после верстки (IA должна расти из согласованных запросов).
- Забытый staging-noindex в прод-сборке (проверяется свитчем, шаг 2).
- Sitemap «после запуска» (генерируется в гейте, до DNS).
- Частотность «на глаз» без источника (каждое число — с тегом источника).
