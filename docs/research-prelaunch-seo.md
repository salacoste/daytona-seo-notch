# Исследование: SEO на этапе разработки (pre-launch)

Дата: 2026-10-28. Источники: EN/RU/ZH-статьи, Medium/dev.to, GitHub.
Контекст: библиотека daytona-seo-notch аудирует опубликованные сайты;
задача — работать с сайтом, который ещё верстается (корп. сайт / лендинг / блог).

## 1. Что показывает индустрия

### Фазовые чек-листы (планирование → разработка → запуск)
Тайваньская практика (dmo.com.tw, cianwang.com) organise проверку SEO по фазам
проекта: 規劃 (планирование) → 開發 (разработка) → 上線前 (до запуска) — с
конкретными критериями приёмки в каждой фазе. Западные чек-листы (Webflow
30+ items, go-live checklists) дают ту же структуру: контент/мета на этапе
верстки, техника/speed перед стартом, аналитика и индексация в момент запуска.
Вывод: **pre-launch SEO — это фазовый процесс, а не разовая проверка**.

### CI/PR-гейты («shift-left SEO»)
- SeoScoreAPI / seo-audit-action: 80+ проверок на каждый PR, «fail the build
  when SEO breaks» (dev.to) — SEO-регрессии ловятся до продакшена
- seo-monitoring (zero-dep GitHub Action): HTTP/canonical/meta-robots
  регрессии между деплоями
- Вывод: **SEO-проверки встраиваются в пайплайн сборки, а не после публикации**

### Статический аудит собранных артефактов
- **Cap-go/seo-checker** (npx @capgo/seo-checker): 1000+ правил по **собранным
  HTML-файлам в `dist/`** — метаданные, контент, доступность, structured data,
  без сервера. Конфиг под проект, JSON-вывод, CI-ready.
- Вывод: **аудировать можно билд-артефакты — сайт не обязан быть опубликован**

### Framework-эпоха (Next.js/SSR-статьи, Medium)
Мета-теги через metadata API, SSR/SSG для индексируемости, canonical на этапе
сборки, per-page уникальные title/description. Классические ловушки:
noindex на стейджинге, забытый после запуска; preview-URL в индексе;
sitemap «додумаем после релиза»; аналитика подключается в последний день.

### RU-практика
Аудит-статьи (mmr.ua, synapse-studio) в основном post-launch; свежего
pre-launch-методология меньше — ниша.

## 2. Ключевой инсайт для daytona-seo-notch

Наш рантайм **уже умеет всё необходимое для pre-launch** — проверено живьём
(2026-10-28): SSRF-слой апстрима имеет opt-in allowlist локальных таргетов:

```bash
CLAUDE_SEO_LOCAL_TARGETS=localhost:3000 \
  tools/seo-runtime/run parse_html.py --url http://localhost:3000/ --json
```

Проверено: `parse_html`, `fetch_page`, `agentic_check` работают против
`localhost:8767` (dev-сервер/статика `dist/`). Значит все аудиторские треки
(technical/schema/content/ai-readiness), drift и рендер доступны **до
публикации** — против dev-сервера или собранной статики.

## 3. Дизайн решения (реализовано в `daytona-seo-notch-prelaunch`)

| Фаза | Что делает скилл | Инструменты |
|---|---|---|
| 0. Стратегия | тип сайта (корп/лендинг/блог) → семантика, кластеры, IA/URL-структура, контент-план | методология cs plan/cluster + mk content-strategy (в библиотеке) |
| 1. Сборка | шаблоны страниц: title/meta/H1/schema на этапе верстки; SSR-требования; canonical/OG | `schema_generate.py` + `schema/templates.json`, справочники скиллов |
| 2. Pre-launch гейт | аудит localhost/dist всеми треками; staging-политика (noindex на превью); генерация sitemap.xml; hreflang; readiness для AI-агентов | `CLAUDE_SEO_LOCAL_TARGETS` + `-audit`/`-technical`/`-schema`/`-sitemap`/`-ai` |
| 3. Go-live | чек-лист переключения: снять noindex, robots, sitemap-сабмит, GSC/Метрика/IndexNow, **первый аудит = drift-baseline** | `-drift baseline` (полигон с первого дня) |

Плюс: CI-гейт для проектов-потребителей (пример workflow в справочнике скилла).

## Источники

- EN: thecssagency.com (Webflow 30+ pre-launch SEO), theadminbar.com (go-live
  SEO checklist), ajontec.com (dev checklist before launch)
- Medium/dev.to: weber-stephen (SSR/SSG/ISR и SEO), sassenthusiast (Next.js SEO
  best practices), avansledright (SEO checks in CI with GitHub Actions)
- ZH: dmo.com.tw (SEO網頁設計 15 驗收 по фазам), cianwang.com (網站上線前檢查清單),
  zhuanlan.zhihu.com (25 条谷歌 SEO 清单), terrahq.com/zh (技术SEO清单)
- GitHub: Cap-go/seo-checker (static dist audit, 1000+ rules), SeoScoreAPI
  seo-audit-action (PR-гейт 80+ checks), seo-monitoring (zero-dep action)
- Локальная верификация: `CLAUDE_SEO_LOCAL_TARGETS` механизм (url_safety.py),
  live-прогон parse/fetch/agentic_check на localhost — 2026-10-28
