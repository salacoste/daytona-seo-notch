#!/usr/bin/env python3
"""Port marketingskills skills into .agents/skills/ (E4).

Copies SKILL.md + references/ + evals/ as-is (upstream is already
Agent-Skills format), adds adapted-from metadata, and appends the
daytona integration note to the four overlap-domain skills (PRD §4.4).
Idempotent: wipes each target dir first.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

SRC = Path("sources/marketingskills/skills")
DST = Path(".agents/skills")

SKILLS = [
    "product-marketing",
    "cro",
    "copywriting",
    "copy-editing",
    "ab-testing",
    "emails",
    "analytics",
    "attribution",
    "conversion-tracking",
    "pricing",
    "offers",
    "launch",
    "link-building",
    "programmatic-seo",
    "site-architecture",
    "content-strategy",
    "customer-research",
    "competitors",
    "cold-email",
    "ads",
    "ad-creative",
    "competitor-profiling",
]

# Overlap domains (PRD §4.4): connect the mk role to the daytona counterpart.
INTEGRATION = {
    "link-building": (
        "daytona-seo-notch backlink-profile analysis (executable: Moz/Bing/Common Crawl, "
        "roadmap) measures the authority this skill earns. Use both: analyze with daytona, "
        "acquire with this skill."
    ),
    "programmatic-seo": (
        "For auditing an existing programmatic site's indexation, crawl and thin-content "
        "health, run `/daytona-seo-notch-audit`; this skill covers the build strategy."
    ),
    "site-architecture": (
        "For generating and quality-gating the XML sitemap itself, use "
        "`/daytona-seo-notch-sitemap`; this skill covers information architecture and "
        "internal-linking strategy."
    ),
    "content-strategy": (
        "For SERP-data analysis of existing content (E-E-A-T scoring, briefs), use "
        "`/daytona-seo-notch-content`; this skill covers editorial planning."
    ),
}


def add_metadata(text: str, name: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise SystemExit(f"{name}: no frontmatter")
    fm = m.group(1)
    if "adapted-from:" not in fm:
        if re.search(r"^metadata:", fm, re.MULTILINE):
            fm = fm.replace(
                "metadata:", "metadata:", 1
            ) + "\n  adapted-from: coreyhaines31/marketingskills v2.13.9 (MIT)"
        else:
            fm += (
                "\nlicense: MIT\nmetadata:\n"
                "  adapted-from: coreyhaines31/marketingskills v2.13.9 (MIT)"
            )
    return f"---\n{fm}\n---\n" + text[m.end():]


def main() -> None:
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    ported = 0
    for name in SKILLS:
        src = SRC / name
        dst = DST / name
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        shutil.copy2(src / "SKILL.md", dst / "SKILL.md")
        for sub in ("references", "evals", "assets"):
            if (src / sub).is_dir():
                shutil.copytree(src / sub, dst / sub)

        skill = dst / "SKILL.md"
        text = add_metadata(skill.read_text(encoding="utf-8"), name)
        if name in INTEGRATION:
            note = (
                f"\n## Daytona integration\n\n{INTEGRATION[name]}\n"
            )
            text = text.rstrip() + "\n" + note
        skill.write_text(text, encoding="utf-8")
        ported += 1
    print(f"ported {ported} skills")


if __name__ == "__main__":
    main()
