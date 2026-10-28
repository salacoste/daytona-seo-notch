#!/usr/bin/env python3
"""Adapt claude-seo skills into daytona-seo-notch skills for Antigravity.

Mechanical transforms only; orchestration sections are rewritten by hand
afterwards. Idempotent: wipes target dirs first.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

SRC = Path("sources/claude-seo")
DST = Path(".agents/skills")

SKILLS = {
    "seo": "daytona-seo-notch",
    "seo-audit": "daytona-seo-notch-audit",
    "seo-page": "daytona-seo-notch-page",
    "seo-technical": "daytona-seo-notch-technical",
    "seo-schema": "daytona-seo-notch-schema",
    "seo-sitemap": "daytona-seo-notch-sitemap",
    "seo-content": "daytona-seo-notch-content",
}

# Shared references keep living under the orchestrator skill.
SHARED_REFS = [
    "thinking-framework.md",
    "thinking-framework-validate-act.md",
    "quality-gates.md",
    "cwv-thresholds.md",
    "schema-types.md",
    "eeat-framework.md",
    "eeat-scoring-guide.md",
]

TOKENS = [
    # runtime launcher -> project-relative uv runner
    ('"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run', "tools/seo-runtime/run"),
    ('"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" setup', "tools/seo-runtime/run setup-browser"),
    ('"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" doctor', "tools/seo-runtime/run doctor"),
    # shared references relocation
    ("${CLAUDE_PLUGIN_ROOT}/skills/seo/references/", "../daytona-seo-notch/references/"),
    ("${CLAUDE_PLUGIN_ROOT}/skills/seo-geo/references/", "../daytona-seo-notch/references/geo/"),
    (
        "${CLAUDE_PLUGIN_ROOT}/skills/seo-agentic/references/",
        "../daytona-seo-notch/references/agentic/",
    ),
    ("${CLAUDE_PLUGIN_ROOT}/skills/", "../"),
    ("../seo/references/", "../daytona-seo-notch/references/"),
    # bundled data/templates relocation
    ("schema/templates.json", "tools/seo-runtime/schema/templates.json"),
    # sibling skill renames (longest first to avoid partial matches)
    ("seo-content-brief", "daytona-seo-notch-content-brief"),
    ("seo-audit", "daytona-seo-notch-audit"),
    ("seo-page", "daytona-seo-notch-page"),
    ("seo-technical", "daytona-seo-notch-technical"),
    ("seo-content", "daytona-seo-notch-content"),
    ("seo-schema", "daytona-seo-notch-schema"),
    ("seo-sitemap", "daytona-seo-notch-sitemap"),
    ("skills/seo/", ".agents/skills/daytona-seo-notch/"),
    ("/seo audit", "/daytona-seo-notch-audit"),
    ("/seo page", "/daytona-seo-notch-page"),
    ("/seo technical", "/daytona-seo-notch-technical"),
    ("/seo content", "/daytona-seo-notch-content"),
    ("/seo schema", "/daytona-seo-notch-schema"),
    ("/seo sitemap", "/daytona-seo-notch-sitemap"),
]

FOOTER_RE = re.compile(r"\n## Community Footer\n.*?(?=\n## )", re.DOTALL)


def fix_frontmatter(text: str, name: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise SystemExit(f"no frontmatter in {name}")
    fm = m.group(1)
    fm = re.sub(r"^name: .*$", f"name: {name}", fm, flags=re.MULTILINE)
    fm = re.sub(r'^  version: ".*"$', '  version: "0.1.0"', fm, flags=re.MULTILINE)
    if "adapted-from:" not in fm:
        fm = fm.replace(
            "  category: seo",
            "  category: seo\n  adapted-from: AgriciDaniel/claude-seo v2.5.0 (MIT)",
        )
    return f"---\n{fm}\n---\n" + text[m.end():]


def main() -> None:
    if not SRC.exists():
        SystemExit  # noqa: B018 - clarity
        sys.exit(f"missing {SRC}")

    for src_name, dst_name in SKILLS.items():
        src = SRC / "skills" / src_name
        dst = DST / dst_name
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        for item in src.iterdir():
            if item.name == "LICENSE.txt":
                continue
            if item.is_dir() and item.name == "references":
                (dst / "references").mkdir()
                for ref in item.iterdir():
                    shutil.copy2(ref, dst / "references" / ref.name)
            elif item.is_dir():
                shutil.copytree(item, dst / item.name)
            else:
                shutil.copy2(item, dst / item.name)

    # shared references -> orchestrator
    orch_refs = DST / SKILLS["seo"] / "references"
    for ref in SHARED_REFS:
        shutil.copy2(SRC / "skills" / "seo" / "references" / ref, orch_refs / ref)

    # geo/agentic knowledge needed by the core tracks lives under the
    # orchestrator until dedicated skills are ported (roadmap: E3)
    for sub, files in {
        "geo": ["google-ai-optimization-guide.md", "llmstxt-evidence.md"],
        "agentic": ["lighthouse-agentic-category.md"],
    }.items():
        (orch_refs / sub).mkdir(exist_ok=True)
        for f in files:
            shutil.copy2(SRC / "skills" / f"seo-{sub}" / "references" / f, orch_refs / sub / f)

    # transforms over every markdown file
    changed = 0
    for md in sorted(DST.glob("daytona-seo-notch*/**/*.md")) + sorted(
        DST.glob("daytona-seo-notch*/*.md")
    ):
        if "daytona-seo-notch" not in str(md.relative_to(DST)).split("/")[0]:
            continue
        text = md.read_text(encoding="utf-8")
        for old, new in TOKENS:
            text = text.replace(old, new)
        text = FOOTER_RE.sub("\n", text)
        folder = md.relative_to(DST).parts[0]
        if md.name == "SKILL.md":
            text = fix_frontmatter(text, folder)
        md.write_text(text, encoding="utf-8")
        changed += 1
    print(f"adapted {changed} markdown files across {len(SKILLS)} skills")


if __name__ == "__main__":
    main()
