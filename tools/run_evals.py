#!/usr/bin/env python3
"""Deterministic eval runner for the skill library (goal criteria 2 & 3).

Two gates per skill:
  A. evals.json is valid JSON, skill_name matches, every entry has a prompt,
     expected_output and >=1 assertion (structural eval).
  B. trigger anchors: every eval prompt must share at least one distinctive
     term with the skill's discovery surface (name + description) — the
     lexical floor of "the skill fires by its trigger". Host agents dispatch
     semantically; the harness cannot grade that, so it guards the floor:
     a prompt with zero lexical anchors in name+description would rely on
     guesswork. Mean coverage is reported for information, not gated.

Writes a dated Markdown report to docs/ and exits 1 on any failure.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
REPORT = ROOT / "docs" / "EVAL-REPORTS.md"

# Prompts that are conversational wrappers don't carry trigger terms; the
# harness matches prompt terms against description with these heuristics:
MIN_TERM_LEN = 4
STOP = {
    "the", "and", "for", "our", "you", "your", "with", "this", "that", "from",
    "want", "wants", "user", "asks", "ask", "about", "how", "what", "when",
    "does", "did", "has", "have", "was", "were", "not", "are", "can", "get",
    "into", "after", "them", "they", "then", "there", "their", "some", "just",
    "like", "also", "make", "made", "run", "ran", "use", "using", "need",
    "should", "would", "will", "show", "see", "look", "check", "set", "add",
    "out", "one", "two", "all", "any", "who", "why", "help", "please",
}


def _stem(w: str) -> str:
    # light, language-agnostic: tracked/tracking/track, keys/key, фразы/фраза
    for tail in ("ing", "ed", "es", "s", "ы", "а", "я"):
        if w.endswith(tail) and len(w) - len(tail) >= 3:
            return w[: -len(tail)]
    return w


def terms(text: str) -> set[str]:
    # unicode-aware: latin + cyrillic (RU eval prompts are first-class)
    return {
        _stem(w) for w in re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", text.lower())
        if len(w) >= MIN_TERM_LEN and w not in STOP
    }


def skill_description(skill_md: Path) -> str:
    t = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.DOTALL)
    if not m:
        return ""
    fm = m.group(1)
    desc_m = re.search(r"^description:\s*(.*)$", fm, re.MULTILINE)
    desc = desc_m.group(1).strip() if desc_m else ""
    if set(desc) <= {">", "|", "-"}:
        block = re.search(r"^description:\s*[>|][+-]?\n((?:[ \t]+.*\n?)+)", fm, re.MULTILINE)
        desc = " ".join(ln.strip() for ln in block.group(1).splitlines()) if block else ""
    return desc.strip("\"'>")


def main() -> int:
    rows: list[dict] = []
    failures = 0
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        name = skill_md.parent.name
        if name.startswith(("bmad", "bmod")):
            continue
        evals_p = skill_md.parent / "evals" / "evals.json"
        if not evals_p.exists():
            rows.append({"skill": name, "evals": 0, "trigger": "—", "fail": "no evals.json"})
            failures += 1
            continue
        try:
            data = json.loads(evals_p.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append({"skill": name, "evals": 0, "trigger": "—", "fail": f"invalid JSON: {e}"})
            failures += 1
            continue
        evals = data.get("evals", [])
        struct_bad = [
            i for i, ev in enumerate(evals, 1)
            if not ev.get("prompt") or not ev.get("expected_output") or not ev.get("assertions")
        ]
        desc = skill_description(skill_md)
        # discovery surface = skill name (slash-command invocations) + description
        desc_terms = terms(name) | terms(name.replace("-", " ")) | terms(desc)
        ratios: list[float] = []
        uncovered: list[str] = []
        for ev in evals:
            prompt_terms = sorted(terms(ev.get("prompt", "")))
            if not prompt_terms:
                ratios.append(0.0)
                continue
            covered = [
                t for t in prompt_terms
                if t in desc_terms
                or any(t.startswith(d) or d.startswith(t) for d in desc_terms if len(d) >= 5)
            ]
            ratios.append(len(covered) / len(prompt_terms))
            uncovered += [t for t in prompt_terms if t not in covered]
        mean_cov = sum(ratios) / len(ratios) if ratios else 0.0
        # anchor gate: each prompt needs >= 1 covered distinctive term
        anchorless = sum(1 for r in ratios if r == 0.0)
        ok_struct = data.get("skill_name") == name and not struct_bad
        ok_trigger = anchorless == 0
        status = "PASS" if (ok_struct and ok_trigger) else "FAIL"
        if status == "FAIL":
            failures += 1
        note = []
        if not ok_struct:
            note.append(f"struct: entries {struct_bad} or skill_name mismatch")
        if not ok_trigger:
            note.append(f"{anchorless} prompt(s) with zero lexical anchors")
        rows.append({
            "skill": name, "evals": len(evals), "trigger": status,
            "cov": f"{mean_cov:.0%}",
            "fail": "; ".join(note) if note else "",
        })

    lines = [
        "# Eval reports",
        "",
        "Deterministic harness (`tools/run_evals.py`, runs in CI): structural",
        "validity of every `evals.json` + trigger coverage (eval-prompt terms",
        "present in the skill description the host agent sees).",
        "",
        f"## Run {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        f"**{len(rows)} skills, {sum(r['evals'] for r in rows)} eval cases, {failures} failure(s)**",
        "",
        "| Skill | Eval cases | Trigger gate | Mean coverage | Notes |",
        "|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['skill']} | {r['evals']} | {r['trigger']} | {r.get('cov', '—')} | {r['fail'] or 'ok'} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"evals: {len(rows)} skills, {sum(r['evals'] for r in rows)} cases, {failures} failure(s) [gate: structural + >=1 anchor per prompt]")
    for r in rows:
        if r["fail"]:
            print(f"  FAIL {r['skill']}: {r['fail']}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
