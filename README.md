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
- [ ] E3: AI-видимость (мерж ai-seo + агентная готовность)
- [ ] E4: маркетинговая широта (~20 скиллов mk)
- [ ] E5: drift/MCP/credential workflow
- [ ] E6: evals + release packaging
- [ ] Архитектура (`bmad-architecture` в Antigravity) — прогнать черновик PRD интерактивно

## Работа с проектом

Открыть папку в Antigravity и:

- `/bmad` — помощь и следующий шаг по BMAD;
- `/bmad-prd`, `/bmad-architecture`, `/bmad-build` — флоу BMAD;
- `/bmad-toolsmith` (Smithy) — сборка/конвертация скиллов (пригодится для адаптации).

Скиллы BMAD ставились вручную (npm registry недоступен в этой сети) из клона `bmad-code-org/BMAD-METHOD`@`61e01f8` (2026-10-18) в `.agents/skills/` — это эквивалент `npx skills add bmad-code-org/BMAD-METHOD -a antigravity`. При появлении сети можно перевести на `npx skills update`.

## Лицензии

MIT (оба источника; файлы LICENSE сохранены в `sources/`). FLOW-промпты — CC BY 4.0 (если переносятся — атрибуция обязательна).
