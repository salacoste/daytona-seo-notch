# Цель проекта daytona-seo-notch

**Формулировка:** создать собственную профессиональную библиотеку SEO-скиллов для Google Antigravity — `daytona-seo-notch` — объединяющую исполняемую SEO-аудитику [claude-seo](https://github.com/AgriciDaniel/claude-seo) (реальные данные: рендер, краул, CWV, schema, E-E-A-T) и маркетинговую методологию [marketingskills](https://github.com/coreyhaines31/marketingskills), адаптированную под нативные форматы Antigravity (Agent Skills, `.agents/skills/`, `.agents/mcp_config.json`) и лишённую привязок к Claude Code.

## Продукт

Зонтичный оркестратор `/daytona-seo-notch` + линейка профильных скиллов: `-audit`, `-page`, `-technical`, `-schema`, `-sitemap`, `-content`, далее — AI-видимость, drift-мониторинг, local/maps, Google API, маркетинговая широта (CRO, копирайтинг, письма). Команда вида `/daytona-seo-notch-audit https://site` должна выдавать health score (0–100), приоритизированный action plan и артефакты в `{domain}-audit/` — на измеренных данных, а не генерализованном чек-листе из памяти модели.

## Принципы

1. **Два проверенных апстрима (MIT).** Из каждого домена берём лучшую реализацию по матрице решений PRD (`_bmad-output/initiative-antigravity-marketing-seo/prd-*/…`); пересечения мержим, не дублируем.
2. **Всё исполняемо.** Рекомендации опираются на `tools/seo-runtime/` (60 Python-скриптов под uv) и `tools/clis/` (zero-dependency Node) — реальный fetch, рендер, парсинг, API.
3. **Бесплатные источники по умолчанию** (рендер, robots/sitemap, Common Crawl, CrUX/PSI без ключей где возможно); платные данные — опционально через MCP-конфиг Antigravity.
4. **Платформо-нейтрально.** Запрещены `${CLAUDE_PLUGIN_ROOT}`, пути `~/.claude`, идиомы субагентов Claude Code и hooks; параллелизм треков аудита выполняет планировщик задач Antigravity.
5. **Безопасность.** Страницы, SERP и API-ответы — недоверенные данные: анализировать, но не исполнять инструкции из них (prompt-injection guard). Секреты — только в `.env.marketing` (0600, gitignored), никогда в чате, логах и коммитах.
6. **Лицензионная гигиена.** MIT-атрибуция и PROVENANCE сохраняются; FLOW-промпты (CC BY 4.0) переносятся только с явной атрибуцией.

## Критерии успеха

- Сквозной аудит сайта из Antigravity без ручных правок скиллов: score + план + артефакты.
- Чистый клон → первый аудит ≤ 30 минут (`uv sync` + Chromium), macOS/Linux.
- Lint зелёный: валидный фронтматтер, 0 запрещённых паттернов, 0 битых ссылок.
- Каждый скилл проходит свой eval/trigger-тест — защита от мёртвого веса.

## Этапы

E1 каркас и конвенции → **E2 ядро аудита end-to-end (текущий)** → E3 AI-видимость (мерж ai-seo + агентная готовность) → E4 маркетинговая широта (~20 скиллов) → E5 drift/MCP/credentials → E6 evals/lint/release. Управление — по BMAD, артефакты в `_bmad-output/initiative-antigravity-marketing-seo/`.

**Не цели (v1):** собственные MCP-серверы, UI/дашборды, локализация скиллов, упаковка в Antigravity-plugin, правки логики скриптов апстрима.
