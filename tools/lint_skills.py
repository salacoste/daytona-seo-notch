#!/usr/bin/env python3
"""Lint the daytona-seo-notch skill library (PRD FR-11).

Checks every skill under .agents/skills/ whose name starts with
daytona-seo-notch: SKILL.md presence, frontmatter validity (name = folder,
description non-empty and <= 1024 chars), forbidden Claude Code-specific
patterns, and that relative markdown links resolve.

Exit code 1 when any violation is found. CI-ready.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
PREFIX = "daytona-seo-notch"

# marketing skills ported from marketingskills (tools/port_marketing_skills.py)
MARKETING_SKILLS = {
    "product-marketing", "cro", "copywriting", "copy-editing", "ab-testing",
    "emails", "analytics", "attribution", "conversion-tracking", "pricing",
    "offers", "launch", "link-building", "programmatic-seo",
    "site-architecture", "content-strategy", "customer-research",
    "competitors", "cold-email", "ads",
    "ad-creative", "competitor-profiling", "marketing-tools-setup",
}

FORBIDDEN = [
    "CLAUDE_PLUGIN_ROOT",
    "~/.claude",
    ".claude/skills",
    ".claude/commands",
    "hooks.json",
    "subagent spawn",
    "spawn subagent",
]

LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)")

violations: list[str] = []


def check_skill(folder: Path) -> None:
    skill_md = folder / "SKILL.md"
    if not skill_md.exists():
        violations.append(f"{folder.name}: missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")

    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        violations.append(f"{folder.name}: missing frontmatter")
        return
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    if not name_m:
        violations.append(f"{folder.name}: frontmatter has no name")
    elif name_m.group(1) != folder.name:
        violations.append(f"{folder.name}: name '{name_m.group(1)}' != folder")
    desc_m = re.search(r"^description:\s*(.*)$", fm, re.MULTILINE)
    desc = desc_m.group(1).strip() if desc_m else ""
    if desc in {">", "|", ">-", "|-", ">", "|"} or set(desc) <= {">", "|", "-"}:
        # YAML block scalar: the description is the indented lines that follow
        block = re.search(
            r"^description:\s*[>|][+-]?\n((?:[ \t]+.*\n?)+)", fm, re.MULTILINE
        )
        desc = " ".join(
            ln.strip() for ln in block.group(1).splitlines() if ln.strip()
        ) if block else ""
    if not desc.strip("\"'>"):
        violations.append(f"{folder.name}: empty description")
    elif len(desc) > 1024:
        violations.append(f"{folder.name}: description > 1024 chars")

    for pattern in FORBIDDEN:
        for path in [skill_md, *sorted(folder.rglob("*.md"))]:
            if path.name == "SKILL.md" and path != skill_md:
                continue
            body = path.read_text(encoding="utf-8")
            if pattern in body:
                line = next(
                    i + 1
                    for i, ln in enumerate(body.splitlines())
                    if pattern in ln
                )
                violations.append(
                    f"{path.relative_to(ROOT)}:{line}: forbidden pattern '{pattern}'"
                )

    for path in [skill_md, *sorted(folder.rglob("*.md"))]:
        body = path.read_text(encoding="utf-8")
        for link in LINK_RE.findall(body):
            if link.startswith(("http://", "https://")):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                violations.append(
                    f"{path.relative_to(ROOT)}: broken relative link '{link}'"
                )


def main() -> int:
    if not SKILLS.exists():
        print("no .agents/skills directory", file=sys.stderr)
        return 2
    # daytona line + ported marketing skills; BMAD's own skills (bmad*/bmod*) are excluded
    folders = sorted(
        p
        for p in SKILLS.iterdir()
        if p.is_dir() and (p.name.startswith(PREFIX) or p.name in MARKETING_SKILLS)
    )
    if not folders:
        print(f"no {PREFIX}* skills found", file=sys.stderr)
        return 2
    for folder in folders:
        check_skill(folder)
    if violations:
        print(f"FAIL: {len(violations)} violation(s)")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"OK: {len(folders)} skills lint-clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
