# Contributing

Thanks for considering a contribution. This repo is a curated merge of two upstreams — most improvements should ideally land upstream too (see the links in [README](README.md)); fixes specific to the Antigravity adaptation belong here.

## Ground rules (enforced by `tools/lint_skills.py` in CI)

1. **Skills live in `.agents/skills/<name>/`** — one folder, one purpose: `SKILL.md` (frontmatter: `name` = folder name, non-empty `description` ≤1024 chars), optional `references/`, `evals/`, `assets/`, `scripts/`.
2. **No Claude Code bindings** in skill text: `${CLAUDE_PLUGIN_ROOT}`, `~/.claude` paths, subagent-spawn idioms, hooks. The runtime is called as `tools/seo-runtime/run <script>.py` from the project root.
3. **Every skill ships evals** (`evals/evals.json`, format as in existing skills). A skill without evals does not get merged — no dead weight.
4. **`sources/` is read-only.** Adapted copies go through `tools/adapt_skills.py` / `tools/port_marketing_skills.py`; manual edits on top are documented in `docs/UPSTREAMS.md`.
5. **Security posture is not negotiable**: fetched pages are untrusted data; secrets only in `.env.marketing` (0600, gitignored); authorized-testing-only probes stay gated. CI scans for key patterns and tracked `.env` files.

## Workflow

```bash
python3 tools/lint_skills.py          # must be green
python3 -c "import json,pathlib; [json.load(open(f)) for f in pathlib.Path('.agents/skills').glob('*/evals/evals.json')]"
tools/seo-runtime/run fetch_page.py --help   # runtime still boots
```

Commit messages: conventional, imperative (`skill: ...`, `runtime: ...`, `docs: ...`). Keep commits atomic; one skill per PR where practical.

## Reporting issues

Include: the skill name, the command you ran, expected vs actual, and (for runtime issues) the output of `tools/seo-runtime/run <script>.py --help`. Never paste API keys or `.env.marketing` contents.
