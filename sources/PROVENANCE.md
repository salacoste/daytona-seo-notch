# Vendored Sources

Third-party repositories vendored read-only into this project as adaptation sources.
Do not edit in place — adapted copies live in `.agents/skills/`.

| Folder | Upstream | Commit | Date | License |
|---|---|---|---|---|
| `claude-seo/` | https://github.com/AgriciDaniel/claude-seo (v2.5.0) | `6be93f45064ffbadced572b5d5c95f55fd263af0` | 2026-10-22 | MIT |
| `marketingskills/` | https://github.com/coreyhaines31/marketingskills (v2.13.9) | `0cd9b3a0ef4c411a1d690419ce843f2a1da32cce` | 2026-10-27 | MIT |

Both are MIT-licensed; retain upstream `LICENSE` files and per-file license headers when copying.

Refresh procedure:

```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo sources/claude-seo-new
git clone --depth 1 https://github.com/coreyhaines31/marketingskills sources/marketingskills-new
# diff, then swap folders and update the commit column above
```
