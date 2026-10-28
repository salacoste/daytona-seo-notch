# Мануалы daytona-seo-notch

Выберите ваш сценарий:

| Сценарий | Ваша ситуация | Мануал |
|---|---|---|
| **1. Новый сайт** | Клиент/продукт с нуля: ничего нет, ни кода, ни контента | [scenario-new-site.md](scenario-new-site.md) |
| **2. Сайт в разработке** | Уже есть часть кода/контента/макетов; публикации ещё нет | [scenario-in-development.md](scenario-in-development.md) |
| **3. Опубликованный сайт** | Сайт живёт в интернете; нужен аудит/рост/мониторинг | [scenario-live-site.md](scenario-live-site.md) |

Справочник по каждому скиллу (все 35, подробно): [skills-reference.md](skills-reference.md)

Общие правила для всех сценариев:
- Команды `/…` выполняются в Antigravity, открытой в папке проекта библиотеки; команды `tools/…` — из корня репозитория.
- Секреты — только в `.env.marketing` (0600, gitignored); никогда в чате.
- Порядок уровней: `/daytona-seo-notch-brief` → `/daytona-seo-notch-prelaunch` → `/daytona-seo-notch-audit` покрывают весь жизненный цикл сайта.
