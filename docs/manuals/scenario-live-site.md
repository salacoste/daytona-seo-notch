# Сценарий 3. Опубликованный сайт

**Ситуация:** сайт доступен в интернете. Цели: понять состояние, расти,
следить за изменениями, подключить данные.

## Карта пути

```
Шаг 1          Шаг 2            Шаг 3             Шаг 4            Шаг 5
Первичный  →   Глубина по     →  Данные        →  Рост          →  Мониторинг
аудит          находкам          (аналитика,      (контент,         (drift
                                 ключи)           ссылки, AI)       + re-audit)
/daytona-      /daytona-         /daytona-         /daytona-        /daytona-
seo-notch-     seo-notch-…       seo-notch-        seo-notch-       seo-notch-
audit                            analytics        content/ai/…      drift
```

## Шаг 1 — Первичный аудит: `/daytona-seo-notch-audit https://ваш-сайт`

Работает на бесплатных источниках сразу, без ключей. Что сделает: рендер
главной → определение типа бизнеса → краул ≤500 страниц → треки
(техника+AI-краулеры, контент/E-E-A-T, schema, sitemap, CWV-сигналы; условно:
performance при `GOOGLE_API_KEY`, drift при существующей базе, analytics при
подключённых креденшалах) → **SEO Health Score 0–100** + приоритизированный
план → артефакты в `{domain}-audit/`.

Правила чтения отчёта: Critical — немедленно; у каждой рекомендации —
принцип, зависимости, проверка «как поймём, что не сработало».

## Шаг 2 — Глубина по находкам (по необходимости)

| Находка аудита | Скилл |
|---|---|
| Технические проблемы (роботсы, индексация, рендер, безопасность) | `/daytona-seo-notch-technical` |
| Schema отсутствует/битая | `/daytona-seo-notch-schema <url>` — валидация + готовый JSON-LD |
| Sitemap-проблемы | `/daytona-seo-notch-sitemap <url или generate>` |
| Слабый контент, тонкие страницы | `/daytona-seo-notch-content <url>` (Who/How/Why, E-E-A-T) |
| Одна важная страница (лендинг, цена) | `/daytona-seo-notch-page <url>` |
| Плохие цитирования AI / агентная готовность | `/daytona-seo-notch-ai` (+ `readiness <url>`) |
| «Трафик упал» | сначала `/daytona-seo-notch-seo_updates`-леджер (через хаб), потом аудит + `analytics` |

## Шаг 3 — Подключить данные: `/marketing-tools-setup` → `/daytona-seo-notch-analytics`

1. GA4 (токен или OAuth-рантайм), Яндекс Метрика (`metrika:read`), GSC —
   по шагам: `docs/CONNECT-ANALYTICS.md`.
2. `/daytona-seo-notch-analytics overview` — кросс-движковая сводка;
   `organic` — сплит Яндекс/Google; `phrases` — поисковые фразы Яндекса;
   `compare` — честные расхождения GA4↔Метрика.
3. Бесплатный `GOOGLE_API_KEY` → полевые CWV (PSI/CrUX) в каждом аудите.

## Шаг 4 — Рост

- **Контент:** `/daytona-seo-notch-content` → брифы новых страниц из
  согласованных запросов; для блогов — `content-strategy` (маркетинг-нать).
- **AI-видимость:** `/daytona-seo-notch-ai` — prompt-портфель, извлекаемая
  структура, llms.txt-решение, присутствие на третьих площадках.
- **Конверсии страниц:** `cro`, `copywriting`, `ab-testing` (маркетинг-нать,
  читают product-marketing контекст — создайте `/product-marketing`).
- **Ссылки/упоминания:** `link-building` (стратегия) — анализ профилей
  через рантайм-скрипты (`backlinks_auth.py --check`).

## Шаг 5 — Мониторинг

1. `/daytona-seo-notch-drift baseline https://ваш-сайт` — один раз.
2. После каждого деплоя/правки контента: `/daytona-seo-notch-drift compare`
   — 17 правил, CRITICAL/WARNING/INFO.
3. Пере-аудит: раз в месяц или после крупных релизов; сравнивайте health
   score и `{domain}-audit/` артефакты.
4. Еженедельный drift-бот уже работает в этом репозитории (пример
   автоматизации) — `drift-reports/`.

## Скиллы сценария (порядок)

`audit` → (по находкам) → `marketing-tools-setup` → `analytics` →
(`content`/`ai`/`cro`/`link-building`/…) → `drift` → цикл.

## Частые ошибки

- Чинить всё сразу: порядок = приоритеты аудита (Critical → High → …).
- Валить падение трафика на контент до проверки леджера Google-обновлений.
- Смешивать числа GA4 и Метрики в одну колонку (см. `analytics compare`).
- Один audit-навсегда: сайт меняется — drift-база должна существовать.
