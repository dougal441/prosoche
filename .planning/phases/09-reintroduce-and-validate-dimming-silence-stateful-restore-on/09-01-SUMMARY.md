---
phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on
plan: 01
subsystem: infra
tags: [python, shortcuts-plist-generator, type-coercion, static-analysis, build-guard]

# Dependency graph
requires:
  - phase: 07-control-room-dumb-freeze
    provides: device-confirmed Dumb build/freeze lineage this experimental fork branches from
provides:
  - Two-entry NUMERIC_OPERAND_FIELDS fix closing the setbrightness/setvolume coercion gap
  - docs/phase9_self_check.py, a reusable regression guard proving the fix is load-bearing
  - Both forks (Dumb, Sentient) regenerated with the coercion applied at all 18 sites that need it
  - ROADMAP.md Phase 9 Goal paragraph corrected from stale "18" to confirmed "28" sites
affects: [09-02-PLAN.md (device-proving half — depends on this plan's static fix)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Table-driven numeric-operand coercion audit — a new Set-action numeric field is
      closed by adding one NUMERIC_OPERAND_FIELDS entry; no other function needs editing"
    - "Self-check negative control — call the REAL production guard function against a
      synthetic before/after fixture (pop table entries, assert no-raise; restore, assert
      raise) to prove a build guard is load-bearing rather than accidentally passing"

key-files:
  created:
    - docs/phase9_self_check.py
  modified:
    - tools/build_state_engine.py
    - docs/state_engine_self_check.py
    - docs/phase5_self_check.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - .planning/ROADMAP.md

key-decisions:
  - "Fixed two pre-existing, unrelated static-check regressions (stale gettimebetweendates
    count assertion; ancestry check depending on a router gate removed in a prior resolved
    debug session) because the plan's own <verify> chain required both scripts to exit 0 —
    documented as Rule 1/3 deviations, not scope creep on the coercion fix itself."

requirements-completed: [RESTORE-01]

coverage:
  - id: D1
    description: "NUMERIC_OPERAND_FIELDS gains setbrightness/setvolume entries; verify_numeric_operands() now covers all 28 sites instead of silently exempting them"
    requirement: "RESTORE-01"
    verification:
      - kind: unit
        ref: "python3 tools/build_state_engine.py (verify_numeric_operands() runs unconditionally inside main(); a SystemExit means an uncoerced numeric site was found)"
        status: pass
      - kind: unit
        ref: "docs/phase9_self_check.py::negative_control"
        status: pass
    human_judgment: false
  - id: D2
    description: "Both forks regenerate cleanly and pass the full static suite (generator self-checks, phase self-checks, Playground validator at iOS 26/all-platform target) with the fix applied"
    requirement: "RESTORE-01"
    verification:
      - kind: unit
        ref: "python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 docs/state_engine_self_check.py && python3 docs/phase5_self_check.py && python3 docs/phase9_self_check.py"
        status: pass
      - kind: integration
        ref: "validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all; same for Sentient"
        status: pass
    human_judgment: false
  - id: D3
    description: "Live-generated forks carry exactly the expected coercion split: 14/14 setbrightness (all coerced) and 14 setvolume (4 coerced, 10 correctly left uncoerced — Silence Target already Number-sourced)"
    requirement: "RESTORE-01"
    verification:
      - kind: unit
        ref: "docs/phase9_self_check.py::site_audit"
        status: pass
    human_judgment: false
  - id: D4
    description: "No repository documentation still cites '18' as the current deferred-site count outside the two explicitly-exempted historical-record files"
    requirement: "RESTORE-01"
    verification:
      - kind: other
        ref: "grep -rn \"18 uncoerced\\|18 deferred\\|18 brightness\" docs/ .planning/ROADMAP.md — zero hits"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-08-16
status: complete
---

# Phase 09 Plan 01: Close the setbrightness/setvolume numeric-coercion gap Summary

**Two-entry NUMERIC_OPERAND_FIELDS fix (`WFBrightness`/`WFVolume`) closes the audit gap across all 28 setbrightness/setvolume sites, with a load-bearing negative-control self-check and a corrected "28, not 18" site count throughout the repo.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-08-16T09:59:00Z (approx.)
- **Completed:** 2026-08-16T10:01:27Z
- **Tasks:** 3
- **Files modified:** 7 (2 new-file-equivalent, 5 modified)

## Accomplishments
- Added the two missing `NUMERIC_OPERAND_FIELDS` entries (`is.workflow.actions.setbrightness` → `WFBrightness`, `is.workflow.actions.setvolume` → `WFVolume`) so `verify_numeric_operands()` audits all 28 sites instead of silently exempting them — a purely additive, table-driven fix requiring no other code changes.
- Regenerated both forks (`src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`) with the coercion applied; confirmed the exact expected split — 14 `setbrightness` sites (all 14 coerced: Restore Brightness x4 + Dim Target x10) and 14 `setvolume` sites (4 coerced: Restore Volume x4; 10 correctly left uncoerced: Silence Target, already Number-sourced via `number()`).
- Built `docs/phase9_self_check.py`: a negative-control fixture that calls the real `bse.verify_numeric_operands()` against a synthetic Text-sourced `setbrightness` write, proving the fix is load-bearing (removing the two table entries reproduces the pre-fix exemption bug; restoring them makes the guard fire), plus a `site_audit()` that independently confirms the 18/10 coercion split in both live-generated forks.
- Corrected ROADMAP.md's Phase 9 Goal paragraph from the stale "18 uncoerced sites" to the confirmed "28," matching its own criterion 1. Swept `docs/` and `.planning/ROADMAP.md` for remaining stale "18" references — zero hits outside the two explicitly-exempted historical-record categories (`.planning/debug/HANDOFF.md`'s preserved table, the originating todo's already-addended Problem section).

## Task Commits

Each task was committed atomically:

1. **Task 1: Add the two NUMERIC_OPERAND_FIELDS entries and regenerate both forks end-to-end** - `5b95026` (feat)
2. **Task 2: Add the negative-control + site-audit self-check (Wave 0 gap)** - `9964c9a` (test)
3. **Task 3: Correct the stale "18 sites" framing wherever it is not already corrected** - `aadab83` (docs)

_Note: Task 1's commit also includes two Rule 1/3 deviation fixes to pre-existing, unrelated stale self-check assertions — see Deviations below._

## Files Created/Modified
- `tools/build_state_engine.py` - Two new `NUMERIC_OPERAND_FIELDS` dict entries (2 insertions, confirmed via `git diff --stat`); no other line changed
- `docs/phase9_self_check.py` (new) - `negative_control()` (load-bearing proof via the real production guard) and `site_audit()` (28-site coercion-split proof), both called from `main()`
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` - Regenerated in place; now carry the coercion aggrandizement at all 18 sites that need it
- `.planning/ROADMAP.md` - Phase 9 Goal paragraph corrected from "18" to "28" uncoerced sites
- `docs/state_engine_self_check.py` - Fixed a stale `gettimebetweendates` count assertion (deviation, see below)
- `docs/phase5_self_check.py` - Fixed a stale control-flow ancestry check depending on a removed router gate (deviation, see below)

## Decisions Made
- Kept the fix purely additive at the `NUMERIC_OPERAND_FIELDS` table per the plan's explicit instruction (no other function edited: `_numeric_operand_sites()`, `_operand_descriptor()`, `_numeric_operand_report()`, `normalise_numeric_operands()`, `verify_numeric_operands()`, `set_brightness()`, `set_media_volume()` all byte-identical except for consuming the two new table entries generically).
- `docs/phase9_self_check.py`'s negative-control fixture pops/restores `NUMERIC_OPERAND_FIELDS` via try/finally, so the module-level dict is never left mutated on exit even if an assertion fails mid-check.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1/3 - Pre-existing bug, blocking] Fixed stale `gettimebetweendates` count assertion in `docs/state_engine_self_check.py`**
- **Found during:** Task 1 (running the plan's own required `<verify>` chain)
- **Issue:** `structural_check()` asserted `ids.count("is.workflow.actions.gettimebetweendates") >= 3`, a pre-existing (pre-dating this plan, confirmed via `git stash`) stale threshold. Cycle 14's `elapsed_since()` fix (documented in its own docstring) replaced three downstream `gettimebetweendates` call sites with plain numeric subtraction, per the resolved `open-routing-sequence-error.md` debug session; only the CLOCK block's own genuine Date→Date construct still calls it, so the live count is 1, not ≥3.
- **Fix:** Updated the assertion to `>= 1` with a comment explaining the cycle-14 architecture change it now reflects.
- **Files modified:** `docs/state_engine_self_check.py`
- **Verification:** `python3 docs/state_engine_self_check.py` exits 0
- **Committed in:** `5b95026` (Task 1 commit)

**2. [Rule 1/3 - Pre-existing bug, blocking] Fixed stale control-flow ancestry check in `docs/phase5_self_check.py`**
- **Found during:** Task 1 (running the plan's own required `<verify>` chain)
- **Issue:** The script looked up an `input_present_group` conditional (`WFCondition == 100` on `Input Key`, the "has any value" router gate) and asserted the live-Ice/expiry markers are nested three levels deep under it. That gate was permanently removed by the resolved `open-routing-sequence-error.md` fix (router now routes by POSITIVE identification of `Input Key`, never by presence/absence — see `ROUTER_OVERVIEW` in `tools/build_state_engine.py`), so the lookup always threw `StopIteration`, pre-dating this plan (confirmed via `git stash`).
- **Fix:** Removed the `input_present_group` lookup and updated both ancestry assertions to the correct two-level nesting (`[(open_group, 0), (cooldown_group, 0/1)]`), verified by direct inspection of the current generated XML's actual conditional-ancestry chain before editing.
- **Files modified:** `docs/phase5_self_check.py`
- **Verification:** `python3 docs/phase5_self_check.py` exits 0, prints "phase5 self-check: passed"
- **Committed in:** `5b95026` (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1/3 — pre-existing, unrelated to the numeric-coercion fix, but blocking the plan's own required `<verify>` chain)
**Impact on plan:** Both fixes were necessary to complete Task 1's verification as written; neither touches the coercion-fix code path itself. No scope creep beyond making the plan's own specified verify chain actually runnable.

## Issues Encountered
None beyond the two deviations above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- RESTORE-01 (this plan's sole requirement) is complete: the static half of the coercion gap is closed, proven load-bearing, and documented accurately.
- `09-02-PLAN.md` (device-proving half) can now proceed — it depends on this plan's static fix being in place before any on-device visual chip-color check or capture/restore trial is meaningful.
- This plan explicitly does NOT prove the coercion shape (`WFCoercionVariableAggrandizement`/`WFNumberContentItem`) is correct on real hardware for a direct Set-action parameter position — that remains Plan B's `checkpoint:human-verify` responsibility, per 09-RESEARCH.md's own honestly-reported evidence gap (Donor 10 doesn't cover this construct).

---
*Phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on*
*Completed: 2026-08-16*

## Self-Check: PASSED

- FOUND: docs/phase9_self_check.py
- FOUND: .planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-01-SUMMARY.md
- FOUND: 5b95026 (Task 1 commit)
- FOUND: 9964c9a (Task 2 commit)
- FOUND: aadab83 (Task 3 commit)
- FOUND: 6038b24 (SUMMARY.md commit)
