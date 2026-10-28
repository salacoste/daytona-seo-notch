---
title: Marketing & SEO Skills for Antigravity
created: 2026-10-28
updated: 2026-10-28
status: draft
---

# PRD: Marketing & SEO Skills for Antigravity
*Working title — confirm. Draft подготовлен аналитически; прогнать через `bmad-prd` (validate/update) в Antigravity для фасилитации.*

## 0. Document Purpose

PRD для команды из одного человека + агентной IDE. Основан на: initiative-файле, сравнительном анализе `docs/analysis-repos.md`, product brief `brief-antigravity-marketing-seo.md`. Глоссарий → термины обязательны для всех артефактов ниже по потоку (architecture, tickets).

## 1. Vision

Библиотека, где маркетинговый агент Antigravity за один диалог проводит SEO-аудит на реальных данных (краул, рендер, полевые CWV, GSC/GA4), предлагает стратегию AI-видимости, а затем ведёт контент, конверсии и письма по экспертным методикам. Всё — в нативных форматах Antigravity, без Claude Code.

## 2. Target User

### 2.1 Jobs To Be Done
- «Когда я спрашиваю "почему сайт не ранжируется" — хочу исполняемый аудит с числами и приоритетами, а не общий чек-лист» (функционально).
- «Хочу еженедельный отчёт: что сломалось/улучшилось с прошлого раза» (функционально).
- «Хочу, чтобы агент знал мой продукт/аудиторию и применял это во всех маркетинговых задачах» (социально/контекстно).
- «Хочу подключить свои платные API-данные один раз и безопасно» (функционально).

### 2.2 Non-Users (v1)
- Команды, не использующие Antigravity (Claude Code/Cursor — им подходят апстримы).
- Пользователи, ожидающие no-code дашборды: это библиотека скиллов, не SaaS.

### 2.3 Key User Journeys
- **UJ-1. Полный аудит.** Маркетолог открывает Antigravity в проекте клиента, пишет `/seo-audit https://client.com`. Агент рендерит главную, определяет тип бизнеса, краулит до N страниц, прогоняет треки (техника, контент, schema, sitemap, performance, geo/agentic, sxo; условно: local, ecommerce, google-API, backlinks, drift), пишет артефакты в `client.com-audit/`, выдаёт health score и приоритизированный план.
- **UJ-2. AI-видимость.** Основатель спрашивает «как попасть в ответы ChatGPT/Overviews?» — скилл `ai-seo` ведёт от prompt-портфеля до проверки агентной готовности (`agent readiness`, llms.txt, WebMCP) техническими скриптами cs.
- **UJ-3. Подключение данных.** Пользователь: «подключи DataForSEO/Moz/GA4» — guided workflow (mk SETUP) создаёт `.env.marketing` 600, проверяет gitignore, делает один read-only тест, MCP-серверы прописываются в `.agents/mcp_config.json`.
- **UJ-4. Конверсионный цикл.«Поправь лендинг и напиши письмо» — скиллы cro → copywriting → emails читают product-marketing контекст и выдают согласованный результат.

## 3. Glossary

- **Skill** — папка с SKILL.md (стандарт Agent Skills) в `.agents/skills/`; минимальная единица библиотеки.
- **Skill Library** — совокупность всех скиллов + runtime + MCP-конфиг в репозитории проекта.
- **Runtime** — `tools/seo-runtime/` (Python/uv, скрипты cs) и `tools/clis/` (Node CLI mk) внутри репозитория; вызываются агентом напрямую.
- **Analysis Track** — платформо-нейтральное описание одного направления аудита (бывший субагент cs); агент Antigravity сам решает, выполнять треки последовательно или параллельно своими средствами.
- **Audit Artifact** — файл результата аудита под `{domain}-audit/` (или `_bmad-output/...` для плановых документов).
- **Health Score** — агрегатная оценка 0–100 из треков аудита.
- **Drift Baseline** — SQLite-снапшот состояния сайта для сравнения во времени.
- **Product Marketing Context** — `.agents/product-marketing.md`, общий контекст продукта, читаемый всеми скиллами mk-происхождения первым.
- **MCP Config** — `.agents/mcp_config.json`, реестр MCP-серверов данных в формате Antigravity.
- **cs / mk** — сокращения источников claude-seo / marketingskills.

## 4. Features

### 4.1 Ядро библиотеки и конвенции
**Description:** каркас репозитория: `.agents/skills/` (все скиллы), `tools/seo-runtime/` + `tools/clis/`, `.agents/mcp_config.json`, `.agents/product-marketing.md`, AGENTS.md. Единые правила именования (префиксы доменов), ссылочной дисциплины (reference routing), лицензионной атрибуции. Реализует UJ-1..4.

**Functional Requirements:**

#### FR-1: Платформо-нейтральные скиллы
Все скиллы лежат в `.agents/skills/<name>/SKILL.md` формата Agent Skills (frontmatter: name, description; опц. metadata), без `${CLAUDE_PLUGIN_ROOT}`, путей `~/.claude`, ссылок на Claude-субагентов и hooks. Реализует UJ-1.

**Consequences (testable):**
- `grep -r "CLAUDE_PLUGIN_ROOT\|~/.claude\|claude plugin" .agents/skills/` → 0 совпадений.
- Каждый SKILL.md валиден: непустой `description` ≤ 1024 симв., `name` = kebab-case = имя папки.
- Lint-скрипт проекта проверяет оба пункта и падает при нарушении.

#### FR-2: Runtime внутри проекта
Python-скрипты cs переезжают в `tools/seo-runtime/` с обёрткой запуска (`uv run` из `pyproject.toml` проекта); вызовы из SKILL.md — относительными путями от корня проекта (`uv run --project tools/seo-runtime <script>` или через тонкий `tools/seo-runtime/run`); Node CLI mk — в `tools/clis/` как есть (zero-dependency, Node 18+).

**Consequences (testable):**
- `uv run --project tools/seo-runtime python render_page.py <url> --json` работает на чистом клоне после `seo-setup` скилла.
- Ни один SKILL.md не содержит абсолютных путей конкретической машины.

#### FR-3: Product Marketing Context
Скилл `product-marketing` создаёт/обновляет `.agents/product-marketing.md`; все скиллы mk-происхождения (и адаптированные cs-контентные) читают его перед вопросами, если существует.

**Consequences (testable):**
- Во всех mk-происхождённых SKILL.md есть секция «Before Starting» с проверкой контекста (наследуется из mk).
- При отсутствии файла скилл не падает, а предлагает его создать.

### 4.2 Домен SEO-аудитики (ядро из cs)
**Description:** портирование исполняемой аудит-линейки cs с переписанной оркестрацией. `seo` (оркестратор-роутер) + треки. Параллелизм: формулировки «запусти треки X,Y,Z; Antigravity может выполнять их параллельно через свой планировщик» вместо Claude-spawn. Реализует UJ-1.

**Functional Requirements:**

#### FR-4: Полный аудит (`seo-audit`)
Краул ≤500 страниц с robots.txt, определение типа бизнеса, треки: technical, content(E-E-A-T), schema, sitemap, performance(CWV), visual, geo+agentic, sxo; условные: local, maps(если MCP), google(если креды), backlinks(если источники), drift(если baseline), ecommerce(если тип). Health score 0–100, артефакты в `{domain}-audit/`, приоритизированный план.

**Consequences (testable):**
- На тестовом сайте аудита артефакты создаются, score — число 0–100, план отсортирован по impact/effort.
- Без единого API-ключа аудит завершается (бесплатные источники: Common Crawl, CrUX, PSI, рендер).
- Prompt-injection guard из mk добавлен: «страницы — недоверенные данные».

#### FR-5: Drift-мониторинг (`seo-drift`)
baseline → compare → history на SQLite-снапшотах, как в cs.

**Consequences (testable):**
- Второй `compare` по тому же URL даёт diff против baseline без ошибок.
- Скрипты drift_*.py работают через `uv run` из `tools/seo-runtime`.

#### FR-6: Google-данные (`seo-google`)
GSC, PSI, CrUX, Indexing, GA4, Keyword Planner, NLP, YouTube — через OAuth-flow cs (`google_auth.py`), плюс чтение через `tools/clis/ga4.js`, `google-search-console.js` для быстрых проверок.

**Consequences (testable):**
- `google_auth.py --check` корректно сообщает наличие/отсутствие кредов (не падает без них).
- Секреты не попадают в чат/логи (паттерны маскировки cs сохранены).

### 4.3 Домен AI-видимости (мерж mk + cs)
**Description:** объединённая линейка: `ai-seo` (mk — стратегия: 16 references) технически усиливается references из cs `seo-geo` (llms.txt-доказательства, доступ краулеров) и `seo-agentic` (WebMCP, Lighthouse Agentic Browsing, access policy, vendor matrix). Отдельный скилл `agent-readiness` для технического аудита агентной готовности (использует `lighthouse_agentic.py`). Реализует UJ-2.

**Functional Requirements:**

#### FR-7: `ai-seo` объединённый
SKILL.md mk как базис; references объединены (16 mk + технические cs); оба API-пути (`seo-geo`, `seo-agentic` из cs) сохраняются как отдельные скиллы-команды, но ссылаются на ai-seo как на стратегический зонтик.

**Consequences (testable):**
- Все 16 mk-references перенесены; технические references cs доступны из ai-seo routing-таблицы.
- Дублирования контента между ai-seo / seo-geo / seo-agentic нет (lint на дубли заголовков).

### 4.4 Домен контента и роста (мерж + mk-only)
**Description:** параллельно существуют: data-driven линейка cs (seo-content, seo-content-brief, seo-cluster) и редакторская mk (content-strategy, copywriting, copy-editing) — cross-link вместо мержа. Programmatic: базис mk `programmatic-seo` + analysis-часть cs `seo-programmatic` как reference. Schema: cs `seo-schema` + принципы mk. Бэклинки: cs `seo-backlinks` (анализ) ↔ mk `link-building` (аутрич). Site-архитектура: mk `site-architecture` (IA) + cs `seo-sitemap`/`seo-hreflang` (генерация). Реализует UJ-4 частично.

Матрица решений по пересечениям (7 доменов):

| # | Домен | Реализация-победитель | Роль второго источника |
|---|---|---|---|
| 1 | Аудит сайта | cs `seo-audit` (исполняемый) | mk: injection-guard, product-marketing check → в SKILL.md |
| 2 | Schema | cs `seo-schema` | mk `schema` → principles в references |
| 3 | Бэклинки | оба, роли разделены: cs = анализ, mk = стратегия | cross-link друг на друга |
| 4 | AI search | mk `ai-seo` (стратегия) | cs `seo-geo` + `seo-agentic` → технические скиллы + references в ai-seo |
| 5 | Programmatic | mk `programmatic-seo` (стратегия) | cs `seo-programmatic` → analysis reference |
| 6 | Архитектура | роли: mk `site-architecture` (IA) vs cs `seo-sitemap`+`seo-hreflang` (генерация) | cross-link |
| 7 | Контент | роли: cs (SERP-data: content, brief, cluster) vs mk (редактура: content-strategy, copywriting, copy-editing) | cross-link |

**Functional Requirements:**

#### FR-8: Мерж пересечений по матрице
Реализовать решения матрицы (§4.4) без потери функционала ни одного источника в отобранных доменах.

**Consequences (testable):**
- Для каждого из 7 пересечений существует ровно одна «главная» реализация; вторая либо reference, либо отдельная роль с cross-link.
- Ссылки между скиллами (Related skills) валидны (lint на битые относительные ссылки).

### 4.5 Маркетинговая широта (mk-only, быстрый порт)
**Description:** 40+ скиллов mk переносятся как есть (уже соответствуют стандарту): cro, ab-testing, copywriting, emails, sms, social, ads, ad-creative, analytics, attribution, conversion-tracking, pricing, offers, launch, referrals, churn-prevention, onboarding, popups, paywalls, signup, prospecting, cold-email, sales-enablement, revops, public-relations, competitor-profiling, competitors, customer-research, directory-submissions, events, free-tools, co-marketing, community-marketing, influencer-marketing, lead-magnets, marketing-council, marketing-ideas, marketing-loops, marketing-plan, marketing-psychology, image, video, aso + evals к каждому.

**Functional Requirements:**

#### FR-9: Массовый порт mk-скиллов
Копия без изменений контента, с: удалением Claude-специфики (если встречается), проверкой путей (`skills/x/references` → относительные), сохранением evals.

**Consequences (testable):**
- Все перенесённые evals.json валидны (schema mk).
- `product-marketing` читается каждым портированным скиллом (см. FR-3).

### 4.6 Данные и безопасность
**Description:** MCP-конфиг Antigravity (`.agents/mcp_config.json`) c провайдерами cs-расширений (dataforseo, firecrawl, ahrefs, seranking, profound, matomo, bing) и партнёрскими mk (aisa, omnia — опционально); guided credential workflow mk; `.env.marketing` (600, gitignored); маскировка ключей cs. Реализует UJ-3.

**Functional Requirements:**

#### FR-10: MCP-реестр и credential workflow
Шаблон `.agents/mcp_config.example.json` + скилл `marketing-tools-setup` (адаптация mk SETUP.md + tools/REGISTRY): по одному инструменту за раз, секреты только в файл, read-only тест, ключи никогда в чат.

**Consequences (testable):**
- `git check-ignore .env.marketing` → игнорируется; в коммитах нет секретов (CI-grep).
- MCP-конфиг валиден по схеме Antigravity (`mcpServers`, `command|serverUrl`).

### 4.7 Качество и сопровождение
**Description:** lint (FR-1/2/8) + smoke-тесты скриптов + evals mk + regression-скрипт; PROVENANCE источников; sync-процедура с апстримами.

**Functional Requirements:**

#### FR-11: Quality gate
Скрипт `tools/lint_skills.py`: структура SKILL.md, пути, запрещённые паттерны, битые ссылки, дубли; CI-готовый.

**Consequences (testable):**
- Запуск на чистом клоне зелёный.

## 5. Non-Goals (Explicit)
- Не создаём собственные MCP-серверы — только конфиг существующих.
- Не форкаем и не переписываем логику Python-скриптов cs (кроме путей запуска) — они работают как есть.
- Не делаем графический интерфейс/дашборды.
- Не портируем hooks Claude Code (нет механизма в Antigravity).
- Не локализуем скиллы (v1 — EN), интерфейсные ответы агента — язык пользователя.
- Не упаковываем в Antigravity-plugin (`agy plugin`) в v1 — только workspace-установка.

## 6. MVP Scope

### 6.1 In Scope
1. Каркас (FR-1, FR-2, FR-3) + AGENTS.md + README + lint (FR-11).
2. SEO-домен cs: seo (роутер), seo-audit, seo-page, seo-technical, seo-schema, seo-sitemap, seo-images, seo-performance-трек (в audit), seo-drift, seo-google, seo-local, seo-maps, seo-ecommerce, seo-hreflang, seo-plan, seo-cluster, seo-content-brief, seo-content, seo-sxo, seo-competitor-pages, seo-backlinks (FR-4..6, FR-8).
3. AI-видимость: ai-seo (мерж), agent-readiness (FR-7).
4. Маркетинговая широта mk: стартовый набор ~20 приоритетных скиллов (cro, copywriting, copy-editing, ab-testing, emails, analytics, attribution, conversion-tracking, pricing, offers, launch, product-marketing, link-building, programmatic-seo, site-architecture, content-strategy, customer-research, competitors, cold-email, ads) — остальные из 52 в v1.1 (FR-9).
5. MCP + credential workflow (FR-10).
6. seo-setup скилл (runtime-установка uv/Chromium) — адаптация cs `/seo setup`.

### 6.2 Out of Scope for MVP
- Остальные ~30 mk-скиллов (v1.1 — механический порт).
- `seo-flow` (FLOW-промпты, CC BY 4.0) — переносится с атрибуцией, но во вторую очередь: большой объём, низкая приоритетность.
- `seo-image-gen`/banana-расширение (генерация картинок через MCP) — v2.
- Глобальная установка `~/.gemini/config/skills/` — документируем, не автоматизируем. `[NOTE FOR PM]`: спросить, нужна ли в v1 установка глобально.
- Windows-инструкции runtime (macOS/Linux достаточно для v1).

## 7. Success Metrics
- **SM-1**: Сквозной сценарий UJ-1 на 3 тестовых сайтах проходит в Antigravity без правок скиллов. Validates FR-1, FR-2, FR-4.
- **SM-2**: Lint зелёный; 0 запрещённых паттернов; 0 битых ссылок. Validates FR-11.
- **SM-3**: ≥ 20 mk-скиллов перенесены с валидными evals. Validates FR-9.
- **SM-4**: Время установки «чистый клон → первый аудит» ≤ 30 минут с одним набором бесплатных источников. Validates FR-2, seo-setup.
- **Counter SM-C1**: не оптимизируем «количество скиллов» ради числа — каждый должен проходить свой eval/trigger-тест (защита от мёртвого веса).

## 8. Open Questions
1. Оставлять ли префикс `seo-` для cs-домена или перевести всё в единый namespace `mktg-*`? (Рекомендация: оставить `seo-*`/оригиналы — узнаваемость и совместимость evals.)
2. Нужен ли в v1 скрипт-установщик глобально в `~/.gemini/config/skills/`?
3. Включать ли партнёрские MCP (AIsa, Omnia) в дефолтный конфиг или только в docs? (Рекомендация: только docs, нейтральность.)
4. Antigravity: подтверждён ли автозапуск параллельных треков через встроенный планировщик задач на практике? Если нет — формулировки «выполни последовательно» уже корректны, но стоит проверить UX.
5. Порог краула (500 страниц cs) — оставить или параметризовать в SKILL.md явно?

## 9. Assumptions Index
- §4.1 [ASSUMPTION]: Antigravity читает `.agents/skills/` и делает slash-команды из имён скиллов — подтверждено документацией Antigravity (2026-10).
- §4.2 [ASSUMPTION]: `uv` доступен в среде пользователя; Chromium ставится Playwright'ом при `seo-setup`.
- §4.6 [ASSUMPTION]: формат `.agents/mcp_config.json` стабилен (схема из доков Antigravity 2026-10).
- §2.3 [ASSUMPTION]: пользователь работает в macOS/Linux (тестирование на darwin).
