# Marketing & SEO Skills for Antigravity

Единая библиотека агентных скиллов для **Google Antigravity**: техническая SEO-аудитика с реальными данными (из [claude-seo](https://github.com/AgriciDaniel/claude-seo)) + маркетинговая широта (из [marketingskills](https://github.com/coreyhaines31/marketingskills)), адаптированные под нативные форматы Antigravity.

- **Скиллы:** `.agents/skills/` — стандарт Agent Skills (SKILL.md), читается Antigravity напрямую; каждый скилл = slash-команда (`/seo-audit`, `/ai-seo`, …).
- **Планирование:** BMAD v7 (`_bmad/`, вывод в `_bmad-output/`). Инициатива: `initiative-antigravity-marketing-seo`.
- **Источники:** `sources/` (read-only вендоринг, см. `sources/PROVENANCE.md`).

## Документы

| Что | Где |
|---|---|
| **Цель проекта (≤3500 симв.)** | `docs/GOAL.md` |
| Сравнительный анализ двух репозиториев | `docs/analysis-repos.md` |
| Product brief (draft) | `_bmad-output/initiative-antigravity-marketing-seo/brief-antigravity-marketing-seo/` |
| PRD с матрицей «что берём откуда» (draft) | `_bmad-output/initiative-antigravity-marketing-seo/prd-antigravity-marketing-seo/` |

## Статус

- [x] Анализ источников (2026-10-28)
- [x] BMAD установлен и настроен (v6.13.0-next, initiative создана)
- [x] Product brief + PRD draft + Goal (`docs/GOAL.md`)
- [x] **E1–E2: каркас + ядро аудита end-to-end** — runtime `tools/seo-runtime/` (60 скриптов, uv, проверен на живых URL) + 7 скиллов `daytona-seo-notch*` (orchestrator, audit, page, technical, content, schema, sitemap), lint зелёный
- [x] **E3: AI-видимость (v0.3)** — `daytona-seo-notch-ai`: стратегия mk ai-seo (15 справочников + evals) + исполняемая агентная готовность cs (agentic_check / lighthouse_agentic / agent_ux_check / agentic_fix, приоритеты P0–P3, GEO-скоринг, WebMCP/llms.txt/UCP-справочники); трек аудита и technical-скилл ссылаются на него
- [x] **E4: маркетинговая широта (v0.4)** — 22 скилла mk перенесены (product-marketing фундамент + cro/copywriting/ab-testing/emails/analytics/attribution/conversion-tracking/pricing/offers/launch/link-building/programmatic-seo/site-architecture/content-strategy/customer-research/competitors/cold-email/ads/ad-creative/competitor-profiling); evals 23/23 валидны; cross-link доменов-пересечений; integration-гайды в `tools/integrations/`
- [x] **E5: данные и мониторинг (v0.5)** — `daytona-seo-notch-drift` (baseline/compare/history, SQLite `~/.cache/daytona-seo-notch/`, живой тест: 17 правил, верный no-drift); `marketing-tools-setup` (guided-подключения: секреты только в `.env.marketing` 0600, read-only тест, MCP-секция Antigravity); `tools/clis/` — 66 zero-dependency Node CLI (проверены); MCP-пример валиден по схеме (1 транспорт/сервер)
- [x] **E6: качество и релиз (v1.0)** — evals на всю daytona-линейку (9 скиллов, 20 кейсов; итого 33 файла evals); CI (`.github/workflows/ci.yml`): lint + evals-валидация + secrets-grep + runtime smoke (uv bootstrap, 60 скриптов компилируются, Node CLI); `docs/UPSTREAMS.md` — процедура обновления апстримов; README quickstart
- [x] Архитектура: каркас соответствует PRD; интерактивный прогон `bmad-architecture` в Antigravity — по желанию
- [ ] Архитектура (`bmad-architecture` в Antigravity) — прогнать черновик PRD интерактивно

## Quickstart (чистый клон → первый аудит)

```bash
git clone <repo> && cd seo_antigravity_skills
# открыть папку в Antigravity, затем:
#   1) /daytona-seo-notch setup        — uv-окружение + headless Chromium (~3 мин)
#   2) /daytona-seo-notch-audit https://ваш-сайт   — полный аудит на бесплатных данных
```

Опционально: `GOOGLE_API_KEY` в `.env.marketing` (файловые CWV: PSI/CrUX) → см. `/marketing-tools-setup`; платные данные (DataForSEO, Firecrawl, AIsa) — через `.agents/mcp_config.json` (шаблон `.agents/mcp_config.example.json`). Обновление апстримов — `docs/UPSTREAMS.md`. CI: lint + evals + secrets + runtime smoke.

## Работа с проектом

Открыть папку в Antigravity и:

- `/daytona-seo-notch` — SEO-хаб; `-audit`, `-page`, `-technical`, `-content`, `-schema`, `-sitemap`, `-ai`, `-drift` — линейка аудита;
- `/product-marketing` (контекст-фундамент), `/cro`, `/copywriting`, `/ads`, `/emails` и др. — маркетинговый набор (22 скилла);
- `/marketing-tools-setup` — безопасное подключение API/MCP;
- `/bmad` — помощь и следующий шаг по BMAD; `/bmad-prd`, `/bmad-architecture`, `/bmad-build` — флоу BMAD; `/bmad-toolsmith` (Smithy) — сборка/конвертация скиллов.

Скиллы BMAD ставились вручную (npm registry недоступен в этой сети) из клона `bmad-code-org/BMAD-METHOD`@`61e01f8` (2026-10-18) в `.agents/skills/` — это эквивалент `npx skills add bmad-code-org/BMAD-METHOD -a antigravity`. При появлении сети можно перевести на `npx skills update`.

## Лицензии

MIT (оба источника; файлы LICENSE сохранены в `sources/`). FLOW-промпты — CC BY 4.0 (если переносятся — атрибуция обязательна).
