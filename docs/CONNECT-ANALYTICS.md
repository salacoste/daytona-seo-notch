# Подключение аналитики: Google Analytics 4 + Яндекс Метрика

Пошаговая инструкция для пользователей daytona-seo-notch. После подключения скилл `/daytona-seo-notch-analytics` и аудит начинают работать с реальными цифрами трафика вместо оценок.

**Что даёт каждое подключение:**

| Источник | Что получаете | Где используется |
|---|---|---|
| GA4 (Google Analytics 4) | Пользователи, сессии, organic-канал, лендинги, устройства/страны | `/daytona-seo-notch-analytics`, обогащение аудита |
| Яндекс Метрика | То же + **поисковые фразы Яндекса** (`ym:s:searchPhrase`), источники с разбивкой organic.yandex / organic.google, поведенческие метрики | `/daytona-seo-notch-analytics`, обогащение аудита |
| GOOGLE_API_KEY (бесплатно) | Полевые Core Web Vitals (PSI + CrUX) | аудит, `-analytics` |
| GSC (Search Console) | Клики/показы/CTR Google, статус индексации | аудит, `-analytics` |

Всё **read-only**. Ключи хранятся только локально.

---

## Шаг 0. Где хранить ключи (один раз)

Создайте файл `.env.marketing` в корне проекта — он уже в `.gitignore`, в коммиты не попадёт:

```bash
(umask 077; set -C; : > .env.marketing)
# затем откройте в редакторе и заполняйте по мере прохождения шагов ниже
```

**Правила:** ключи не вставляются в чат, не печатаются в логах, не коммитятся. Проверка: `git check-ignore .env.marketing` должна вернуть путь.

---

## Вариант A. GA4 — быстрый путь (CLI-токен, 10 минут)

Подходит: прочитать базовые отчёты через `tools/clis/ga4.js`.

1. **Возьмите access token своего Google-аккаунта.** Проще всего через `gcloud`:
   ```bash
   gcloud auth application-default print-access-token
   ```
   (нет gcloud — установите [Google Cloud CLI](https://cloud.google.com/cli) или используйте [OAuth Playground](https://developers.google.com/oauthplayground): слева `Analytics API v4` → Authorize → Exchange → Access Token; на Playground отметьте свою доменную почту.)

2. **Узнайте числовой ID ресурса GA4:** Admin → Data Settings → Data Streams — нет, нужен **Admin → Property Settings → Property ID** (число вида `123456789`). Это НЕ измерительный ID `G-XXXXXXX`.

3. **Запишите в `.env.marketing`:**
   ```dotenv
   GA4_ACCESS_TOKEN="ya29...."
   GA4_PROPERTY_ID="123456789"
   ```

4. **Тест (первое значение):**
   ```bash
   node --env-file=.env.marketing tools/clis/ga4.js reports run \
     --property 123456789 --metrics activeUsers,sessions \
     --start-date 2026-10-21 --end-date 2026-10-28
   ```

⚠️ Access-токены живут ~1 час. Для регулярной работы используйте вариант B.

---

## Вариант B. GA4 — полный путь (OAuth runtime, надёжно)

Подходит: постоянная работа, отчёты аудита, автопродление токенов.

1. **Установите Google-зависимости рантайма:**
   ```bash
   cd tools/seo-runtime && uv sync --group google && cd ../..
   ```

2. **Самый быстрый путь — Application Default Credentials (для своих ресурсов):**
   ```bash
   gcloud auth application-default login \
     --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/analytics.readonly
   ```

3. **Либо явный OAuth-флоу скриптом** (сам покажет инструкции):
   ```bash
   tools/seo-runtime/run google_auth.py --setup    # что создать в Google Cloud
   tools/seo-runtime/run google_auth.py --auth     # браузерный вход (нужен client_secret.json)
   tools/seo-runtime/run google_auth.py --exchange --code "URL_из_адресной_строки"  # ручной обмен
   ```

4. **Пропишите property ID** (см. A.2) в `~/.config/claude-seo/google-api.json` (`ga4_property_id`) или в `.env.marketing` (`GA4_PROPERTY_ID`).

5. **Бесплатный бонус — API-ключ для PSI/CrUX:** Google Cloud → APIs & Services → Credentials → Create API key → в `.env.marketing`:
   ```dotenv
   GOOGLE_API_KEY="AIza..."
   ```

6. **Проверка:**
   ```bash
   tools/seo-runtime/run google_auth.py --check
   ```
   Должно стать `[OK] Google Analytics Data API` и `[OK] PageSpeed Insights`.

---

## Яндекс Метрика (15 минут)

1. **Создайте OAuth-приложение:** [oauth.yandex.ru](https://oauth.yandex.ru) → «Зарегистрировать новое приложение»:
   - Название: любое (например, `daytona-seo-notch`)
   - Платформа: «Веб-сервисы», Redirect URI: `https://oauth.yandex.ru/verification_code` (или свой)
   - Доступы: **Яндекс.Метрика → Управление счётчиками (`metrika:read`)** — только чтение

2. **Получите токен** — откройте в браузере (подставьте свой ClientID):
   ```
   https://oauth.yandex.ru/authorize?response_type=token&client_id=<ВАШ_CLIENT_ID>
   ```
   Разрешите доступ — токен появится в адресной строке (`#access_token=...`). Скопируйте **локально**.

3. **Запишите в `.env.marketing`:**
   ```dotenv
   YANDEX_METRIKA_TOKEN="y0_AgAAAA..."
   # необязательно — счётчик по умолчанию:
   YANDEX_METRIKA_COUNTER_ID="12345678"
   ```

4. **Найдите ID счётчика** (если не знаете): Admin → Monitoring → Log… нет — просто:
   ```bash
   node --env-file=.env.marketing tools/clis/yandex-metrika.js counters list
   ```
   Вернёт список счётчиков (`counter_id`, имя, сайт).

5. **Тест (первое значение):**
   ```bash
   node --env-file=.env.marketing tools/clis/yandex-metrika.js stats summary \
     --start 2026-10-01 --end 2026-10-28
   ```
   Ожидайте: визиты, посетители, просмотры, отказы, время визита.

---

## Проверка всей связки и использование

Откройте проект в Antigravity и попросите:

```
/daytona-seo-notch-analytics overview
```

Скилл сам проверит все три пути (GA4-рантайм, GA4-CLI, Метрика), сообщит что живо, и соберёт сводку за период. Дальше:

| Запрос | Что получите |
|---|---|
| `analytics organic` | Разбивка organic по движкам (organic.yandex vs organic.google) |
| `analytics phrases` | Поисковые фразы Яндекса — источник ключевых слов |
| `analytics landing` | Топ лендингов по движкам |
| `analytics compare` | GA4 vs Метрика с объяснением расхождений |
| `/daytona-seo-notch-audit https://ваш-сайт` | Аудит с полевыми данными трафика (обогащение включается автоматически при наличии ключей) |

Подключение пошагово с вопросами-подсказками: `/marketing-tools-setup`.

---

## Траблшутинг

| Симптом | Причина и решение |
|---|---|
| `GA4_ACCESS_TOKEN environment variable required` | Файл не подхвачен: запускайте с `node --env-file=.env.marketing` (Node 20.6+) |
| GA4 `401` / `Invalid Credentials` | Токен истёк (~1 час) — обновите (вариант A) или перейдите на B |
| GA4 `403 PERMISSIOn_DENIED` | Токен без `analytics.readonly` или нет доступа к ресурсу; проверьте Property ID — числовой, не `G-...` |
| Метрика `403` | Токен без scope `metrika:read` или у аккаунта нет доступа к счётчику |
| Метрика `400 missed_parameter: id` | Не передан счётчик: `--counter N` или `YANDEX_METRIKA_COUNTER_ID` |
| Числа «странные» / `sample_share > 0` | Сэмплирование Метрики на больших периодах — используйте доли, не абсолюты |
| `429` / rate limit | Не ретрайте сразу: увеличьте период или подождите; CLI не повторяет запросы |
| GA4 ≠ Метрика по визитам | Это норма: разные определения сессии, атрибуции, фильтры ботов (см. `analytics compare`) |

## Безопасность

- Всё read-only: GA4 — `analytics.readonly` scope; Метрика — `metrika:read`, эндпоинты `management/v1` (GET) и `stat/v1/data`
- `.env.marketing` — права 600, в `.gitignore`; CI сканирует коммиты на утечки ключей
- Токены не вставляются в чат: агент просит только нечувствительные подтверждения (ID счётчика, номер ресурса)
- Посетительские данные (Logs API Метрики) библиотекой не запрашиваются
