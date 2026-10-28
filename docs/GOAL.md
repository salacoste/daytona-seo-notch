# Цель: daytona-seo-notch — курс на v1.0

**Миссия (неизменна):** профессиональная SEO/маркетинг-библиотека скиллов для Google Antigravity, работающая на измеренных данных; лучший мерж двух MIT-апстримов (claude-seo = исполнение, marketingskills = методология); платформо-нейтрально, безопасно, сопровождаемо.

**Стартовая точка (2026-10-28, v0.2):** ядро аудита готово (E1–E2) — runtime на 60 скриптах (uv, проверен на живых URL), 7 скиллов, lint зелёный, BMAD-планирование развёрнуто.

## Дальнейшие цели по этапам

**E3. AI-видимость (v0.3).** Единый домен `/daytona-seo-notch-ai`: стратегия из mk `ai-seo` (16 справочников: prompt-портфель, answer accuracy, платформенные факторы ранжирования, LinkedIn/YouTube-цитирования, OKF, format volatility) + техника из cs `seo-geo`/`seo-agentic` (llms.txt с доказательной базой, WebMCP, Lighthouse Agentic Browsing X/N, access policy, vendor matrix). Готовность: скилл отвечает и на стратегические, и на технические вопросы; треки аудита ссылаются на него вместо inline-заглушек.

**E4. Маркетинговая широта (v0.4).** Порт ~20 приоритетных скиллов mk (product-marketing, cro, copywriting, copy-editing, ab-testing, emails, analytics, attribution, conversion-tracking, pricing, offers, launch, link-building, programmatic-seo, site-architecture, content-strategy, customer-research, competitors, cold-email, ads) с `product-marketing` контекст-фундаментом. Пересечения — строго по матрице PRD §4.4 (7 доменов), без дублирования. Готовность: evals валидны, cross-link между скиллами живой.

**E5. Данные и мониторинг (v0.5).** Drift-скилл (baseline/compare/history на SQLite) в брендинге daytona; MCP-воркфлоу: `.agents/mcp_config.example.json` + guided-скилл `marketing-tools-setup` (секреты только в `.env.marketing` 0600; один инструмент за раз; read-only тест); Node CLI mk — в `tools/clis/`. Готовность: повторный `compare` даёт осмысленный diff; MCP-конфиг валиден по схеме Antigravity.

**E6. Качество и релиз (v1.0).** Eval на каждый скилл (модель mk); smoke-тесты runtime в CI; процедура обновления апстримов (`tools/adapt_skills.py` + PROVENANCE); установка «чистый клон → первый аудит ≤ 30 минут»; README с quickstart. Не-цели v1 сохраняются: без собственных MCP-серверов, UI, локализации скиллов и plugin-упаковки.

## Критерии успеха v1.0

1. Сквозные сценарии UJ-1..UJ-4 из PRD проходят в Antigravity без ручных правок скиллов.
2. Lint + evals зелёные; 0 секретов в коммитах (CI-grep).
3. Каждый из ~27 скиллов срабатывает по своему триггеру — мёртвого веса нет.
4. Еженедельный drift-отчёт по собственному полигону стабильно 2 месяца.

## Риски и реакция

- **Drift форматов Antigravity** — минимум магии: проверки формата в lint, стандарт Agent Skills как якорь.
- **Обновление апстримов** — репорт через `adapt_skills.py`, коммиты зафиксированы в PROVENANCE.
- **Разбухание библиотеки** — скилл без пройденного eval не берём (counter-metric SM-C1).
- **Сеть/доступы у пользователя** — все аудиты работают на бесплатных источниках по умолчанию; платные — опционально.

Работа ведётся по BMAD (`_bmad-output/initiative-antigravity-marketing-seo/`); каждый этап закрывается коммитом с зелёным lint и обновлением статуса в README.
