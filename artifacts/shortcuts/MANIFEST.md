# Shortcut Distribution Manifest

Rebuilt 2026-08-16 after the Phase 9 merge, with Shortcuts Playground target
`--target-macos 26 --target-platform all`.

Both forks were regenerated from the post-merge generator rather than carrying either
pre-merge side's artifact forward: `src/PROSOCHE-*.xml` are generated files, and git's
textual auto-merge of a ~2.2 MB plist is not a trustworthy build. Regenerating is the only
way the shipped artifact provably matches `tools/build_state_engine.py` at this commit.

| Fork | Source / archive / signed artifact | Bytes | SHA-256 |
|---|---|---:|---|
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,236,198 | `c305b2a011d2dc5d8418ae02e51c9bc376c474bd3be72cc4f4537df57763af46` |
| Dumb archive | `artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Dumb-230439.xml` | 2,236,198 | `c305b2a011d2dc5d8418ae02e51c9bc376c474bd3be72cc4f4537df57763af46` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 190,052 | `ade373f90fbc356860165714322377581b07c155a552b62c20a47a87e5b2c7d1` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,272,878 | `cd40f8da0c48b6a589bfef0fec4577c6e5db517b283256cdf04a122fed52ae6f` |
| Sentient archive | `artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Sentient-230447.xml` | 2,272,878 | `cd40f8da0c48b6a589bfef0fec4577c6e5db517b283256cdf04a122fed52ae6f` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 193,785 | `3773f527945bcffcf93890ac7b2bb8dd24e3cf8992674f4d6cdafc0832195681` |

Both signed files and both dated archives were verified non-empty. The source checksums
differ by design. Both forks passed `validate_shortcut.py` and all four static self-checks
(`state_engine`, `phase5`, `phase9`, plus the generator's own build guards) at this commit.

> **⚠ These artifacts carry the Phase 9 dimming/silence coercion fix, which is UNTESTED on
> device.** Dimming and Silence writes now execute where they previously no-opped, making
> `restore_managed_settings()` load-bearing on a path with zero device evidence. Read
> `docs/BUILD-NOTES.md` §18 before distributing or relying on these builds, and run
> `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
> when a device is available.
