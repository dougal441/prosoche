---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
fixed_at: 2026-08-17T06:43:06Z
review_path: .planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-REVIEW.md
iteration: 1
findings_in_scope: 2
fixed: 2
skipped: 0
status: all_fixed
---

# Phase 12: Code Review Fix Report

**Fixed at:** 2026-08-17T06:43:06Z
**Source review:** .planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-REVIEW.md
**Iteration:** 1

**Summary:**
- Findings in scope: 2 (critical_warning scope — WR-01, WR-02; IN-01 excluded, info-only)
- Fixed: 2
- Skipped: 0

## Fixed Issues

### WR-01: `seed_active_session()` double-indents the emitted bootstrap template line

**Files modified:** `tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`
**Commit:** `5f55edc`
**Applied fix:** Removed the re-prepended `indent` from `seed_active_session()`'s replacement
text (matching `seed_settings_snapshot()`'s `_snapshot_seed_text()` convention, since
`_replace_in_token()` already leaves the anchor's own leading whitespace untouched). Also
discovered and fixed a consequence of the bug's self-referential build (`main()` re-parses
`src/PROSOCHE-Dumb.xml` as `SOURCE` on every run, so a tree already seeded with the double
indent is idempotent-locked into staying wrong): added a targeted repair path
(`ACTIVE_SESSION_DOUBLE_INDENT` detection) that corrects a pre-existing double-indented line
in place before the idempotency guard runs, so already-shipped trees self-heal on the next
build rather than requiring a manual one-off edit. Updated the function's docstring to
describe both the corrected mechanism and the repair path.

Verified per the required build-provenance gate: `git merge-base --is-ancestor
7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` passed; rebuilt both forks
(`tools/build_state_engine.py`, `tools/build_sentient.py`); ran
`docs/state_engine_self_check.py` and `docs/phase6_self_check.py` (both passed); confirmed via
`plistlib` inspection that the emitted `active_session` line in both
`src/PROSOCHE-Dumb.xml:1476` and `src/PROSOCHE-Sentient.xml:~1510` now carries exactly 2
spaces of leading indentation, matching its `last_app`/`pending_exit` siblings exactly (was 4
spaces); confirmed a second rebuild is byte-identical to the first (idempotent); Gate A
(`validate-shortcut --target-macos 26 --target-platform all`) passed clean on both forks.

**Note — verification requires human confirmation of the logic, not just syntax.** The repair
path is a targeted fix for a specific reported class of defect (self-referential idempotent
build re-persisting a prior seeder bug), which is a logic-shaped change beyond pure syntax
correctness. Syntax and structural checks (Tier 1/2) and the full project checker chain all
passed, but per this project's verification discipline the repair path's correctness should
still be read by a human before being treated as fully settled — status recorded as `fixed`
here because it is backed by the mandated checker chain plus direct plist inspection, not
syntax-only verification, but flagging the self-referential-build insight for review since it
was not explicitly anticipated by the finding's own Fix suggestion.

### WR-02: `MANIFEST.md`'s "refresh" updated only the hash table, leaving stale prose that misdescribes the shipped artifact

**Files modified:** `artifacts/shortcuts/MANIFEST.md`
**Commit:** `58b3b87`
**Applied fix:** Added a header clarification distinguishing the phase 11 plan 06 narrative
(retained, historical) from what the hash table currently describes; added a full **Phase
12** paragraph covering `schema_version` 3→4, `exit_events`/`exit_selection_counter`,
the `active_session` container→leaf conversion, and `create_target_url`, each stated as
structurally proven / device-unobserved and cross-referenced to `docs/BUILD-NOTES.md`
§26-27 and `12-UAT.md`'s BLOCKED verdict; corrected the now-false "schema_version moved
2 → 3" and "No control flow moved" sentences by marking them as describing the phase 11
plan 06 rebuild only, with an explicit pointer to the corrected Phase 12 paragraph; added a
closing phase-12 `⚠` bullet following the document's own established per-rebuild convention.

**Additional correction required by WR-01's own fix.** Rebuilding both forks to verify WR-01
(as this task's instructions required) changed `src/PROSOCHE-Dumb.xml` and
`src/PROSOCHE-Sentient.xml` by 2 bytes each, which silently broke `docs/manifest_check.py`
(pre-existing pass, confirmed by reproducing the failure before this fix: `AssertionError: row
'Core source': MANIFEST declares 2831994 bytes, src/PROSOCHE-Dumb.xml is 2831992 bytes`). This
was not itself a reviewed finding, but since WR-02 is specifically about `MANIFEST.md`
accuracy and my own preceding fix was the direct cause, I updated the "Core source"/"Aware
source" byte-count and SHA-256 cells to the current, correct values and added a note
explaining that the archive/signed rows still describe the pre-WR-01-fix `ea7a0f4` build
(re-archiving and re-signing is a separate release step outside this fix's scope, and no
archive/signed artifact was fabricated). `docs/manifest_check.py` passed after this
correction (it verifies each row independently and asserts no archive-equals-source
invariant, so this is a complete, honest fix rather than a partial one).

Verified via Tier 1 (full re-read of the modified file) and by re-running
`docs/manifest_check.py`, which passed (6/6 rows). No syntax checker applies to Markdown
(Tier 3 fallback), so Tier 1 plus the project's own manifest checker constitute the
verification for this finding.

## Skipped Issues

None — both in-scope findings were fixed.

---

_Fixed: 2026-08-17T06:43:06Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
