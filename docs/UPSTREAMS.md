# Обновление апстримов

Процедура синхронизации библиотеки с двумя источниками. Апстримы вендорены в `sources/` (read-only), провенанс — `sources/PROVENANCE.md`.

## 1. Обновить вендоры

```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo /tmp/claude-seo-new
git clone --depth 1 https://github.com/coreyhaines31/marketingskills /tmp/mk-new
rsync -a --delete --exclude='.git' /tmp/claude-seo-new/ sources/claude-seo/
rsync -a --delete --exclude='.git' --exclude='__pycache__' /tmp/mk-new/ sources/marketingskills/
# обновить коммит/версию в sources/PROVENANCE.md
```

## 2. Пере-адаптировать daytona-линейку (claude-seo)

```bash
python3 tools/adapt_skills.py
```

Идемпотентен: пересобирает 7 скиллов ядра из `sources/claude-seo/skills/`. **Внимание:** ручные правки поверх автоматических (оркестрация в hub/audit, roadmap-заметки) будут перезаписаны — после запуска сверьте diff и восстановите ручные секции (они описаны в коммитах E1–E2). Скрипты runtime не трогает: при изменении апстримных скриптов пересинхронизируйте вручную:

```bash
cp sources/claude-seo/scripts/*.py tools/seo-runtime/scripts/
cp sources/claude-seo/data/google-updates.json tools/seo-runtime/data/
cp sources/claude-seo/schema/templates.json tools/seo-runtime/schema/
# затем повторно примените патч пути drift (DAYTONA_DRIFT_DIR, см. коммит E5)
```

## 3. Пере-портить маркетинговые скиллы (marketingskills)

```bash
python3 tools/port_marketing_skills.py
```

Пересобирает 22 скилла + `assets/`. После запуска повторите точечные фиксы ссылок (см. коммит E4): ads→conversion-tracking ссылка, `link-building` → `../../../tools/integrations/`, при необходимости довендорьте новые integration-гайды в `tools/integrations/`.

## 4. Проверить и закрыть

```bash
python3 tools/lint_skills.py          # 32 скилла должны быть чистыми
python3 -c "import json,pathlib; [json.load(open(f)) for f in pathlib.Path('.agents/skills').glob('*/evals/evals.json')]"
tools/seo-runtime/run fetch_page.py --help
git diff --stat                        # ревью изменений
```

Обновить статус в README и закоммитить: `upstream: refresh claude-seo@<commit> marketingskills@<commit>`.

## Политика

- Минорные обновления апстримов — та же лицензия (MIT), провенанс обязателен.
- FLOW-промпты (CC BY 4.0) — только с атрибуцией; при порте `seo-flow` проверить заголовок лицензии.
- Ломающие изменения апстримных скриптов (CLI-интерфейсы) проверяются smoke-тестами CI до мержа.
