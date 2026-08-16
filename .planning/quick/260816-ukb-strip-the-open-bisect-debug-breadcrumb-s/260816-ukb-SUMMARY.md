---
phase: quick
plan: 260816-ukb
subsystem: build-tooling
tags: [shortcuts, python, plist-generator, ship-readiness]

requires:
  - phase: "04-close-pipeline-session-race (04-03-PLAN.md)"
    provides: "Permanent, unconditional notification() OPEN/CLOSE confirmation, independent of OPEN_BISECT — the precondition this task depended on"
provides:
  - "tools/build_state_engine.py free of debug-scaffolding toggles (OPEN_BISECT, ROUTER_TRACE, BUILD_STAMP)"
  - "Rebuilt, self-checked, validated, and signed src/PROSOCHE-Dumb.xml / Dumb.shortcut with no leftover breadcrumb strings"
  - "Refreshed MANIFEST.md Dumb rows and closed Solution item 1 of the ship-readiness-cleanup todo"
affects: [ship-readiness-cleanup, dist-03-uat]

tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - src/PROSOCHE-Dumb.xml
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut
    - artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Dumb-220924.xml
    - artifacts/shortcuts/MANIFEST.md
    - .planning/todos/pending/2026-08-15-ship-readiness-cleanup.md

key-decisions:
  - "Reworded the notification() comment at the end of open_pipeline() to drop OPEN_BISECT/breadcrumb-J references instead of leaving it dangling"
  - "Left the dated archive copy production to sign-shortcut's own built-in archival step (it already writes to the exact artifacts/shortcuts/<date>/ convention the plan specified) rather than duplicating it with a manual cp"

requirements-completed: []

coverage:
  - id: D1
    description: "OPEN_BISECT constant, BISECT_TITLE, breadcrumb() helper, and all ten breadcrumb call sites (A-J) with their explanatory comments removed from tools/build_state_engine.py"
    verification:
      - kind: other
        ref: "grep -n 'OPEN_BISECT\\|ROUTER_TRACE\\|BUILD_STAMP\\|breadcrumb(' tools/build_state_engine.py returns no matches"
        status: pass
    human_judgment: false
  - id: D2
    description: "ROUTER_TRACE constant, TRACE_MARKER/TRACE_END_MARKER, router_trace() function, its main() call, and the orphaned remove_marker_block(TRACE_MARKER, TRACE_END_MARKER) call all removed"
    verification:
      - kind: other
        ref: "grep -n 'OPEN_BISECT\\|ROUTER_TRACE\\|BUILD_STAMP\\|breadcrumb(' tools/build_state_engine.py returns no matches"
        status: pass
    human_judgment: false
  - id: D3
    description: "BUILD_STAMP constant removed; manual_emergency_restore() menu prompt now the plain literal \"PROSOCHĒ\""
    verification:
      - kind: other
        ref: "grep -n 'OPEN_BISECT\\|ROUTER_TRACE\\|BUILD_STAMP\\|breadcrumb(' tools/build_state_engine.py returns no matches"
        status: pass
    human_judgment: false
  - id: D4
    description: "Dumb artifact rebuilt, self-checked, validated at --target-macos 26 --target-platform all, and re-signed with no leftover scaffolding strings in the regenerated XML"
    verification:
      - kind: other
        ref: "python3 docs/state_engine_self_check.py exits 0; validate-shortcut reports 'Validation passed.'; grep -c 'Report the LAST letter you see' and grep -c 'ROUTER TRACE' against src/PROSOCHE-Dumb.xml both return 0; signed .shortcut is non-empty (189,792 bytes)"
        status: pass
    human_judgment: true
    rationale: "On-device OPEN-path regression confirmation is explicitly out of scope for this task (blocked on DIST-03, no connected iPhone) — a human must re-verify on-device once a device is available, per the plan's own instruction not to treat this absence as a failure."
  - id: D5
    description: "MANIFEST.md Dumb rows (source/archive/signed) refreshed with new byte counts and SHA-256 hashes; Sentient rows and header untouched. Ship-readiness-cleanup todo Solution item 1 marked done with a dated completion note, items 2-5 unchanged."
    verification:
      - kind: other
        ref: "git diff artifacts/shortcuts/MANIFEST.md and .planning/todos/pending/2026-08-15-ship-readiness-cleanup.md"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-08-16
status: complete
---

# Quick Task 260816-ukb: Strip the OPEN_BISECT debug breadcrumb scaffolding Summary

**Removed all three debug-scaffolding toggles (OPEN_BISECT/ROUTER_TRACE/BUILD_STAMP) and their ten breadcrumb call sites from `tools/build_state_engine.py`, rebuilt and re-signed the Dumb artifact, and refreshed MANIFEST.md.**

## Performance

- **Duration:** ~15 min
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments
- `tools/build_state_engine.py` no longer contains any OPEN_BISECT/ROUTER_TRACE/BUILD_STAMP scaffolding or breadcrumb call sites — confirmed via the plan's own grep, zero matches
- `src/PROSOCHE-Dumb.xml` regenerated cleanly: `state_engine_self_check.py` exits 0, `validate-shortcut --target-macos 26 --target-platform all` reports zero errors, and the re-signed `.shortcut` is non-empty with no `_signed` suffix
- `MANIFEST.md`'s three Dumb rows and the `2026-08-15-ship-readiness-cleanup.md` todo's Solution item 1 are up to date, with the DIST-03 on-device-verification caveat explicitly recorded

## Task Commits

1. **Task 1: Strip the three debug-scaffolding toggles from tools/build_state_engine.py** - `708847a` (refactor)
2. **Task 2: Rebuild, self-check, validate, and sign the Dumb artifact** - `5b1d2e6` (chore)
3. **Task 3: Refresh MANIFEST.md Dumb rows and close ship-readiness todo item 1** - `154b998` (docs)

_No plan-metadata commit — this quick task's docs commit (SUMMARY.md/STATE.md) is handled by the orchestrator, not by this executor._

## Files Created/Modified
- `tools/build_state_engine.py` - Removed OPEN_BISECT/BISECT_TITLE/breadcrumb(), ROUTER_TRACE/TRACE_MARKER/TRACE_END_MARKER/router_trace(), BUILD_STAMP, all ten breadcrumb call sites, the orphaned `remove_marker_block(TRACE_MARKER, TRACE_END_MARKER)` call, and reworded the adjacent notification() comment and manual-menu prompt
- `src/PROSOCHE-Dumb.xml` - Regenerated from the cleaned generator
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` - Re-signed
- `artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Dumb-220924.xml` - New dated archive copy (produced automatically by `sign-shortcut`)
- `artifacts/shortcuts/MANIFEST.md` - Dumb rows' byte counts and SHA-256 hashes refreshed
- `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` - Solution item 1 marked done with a dated completion note

## Decisions Made
- Kept the plan's exact grep verification command as the completeness gate for task 1 rather than eyeballing the diff
- Did not run the plan's manual `mkdir -p ... && cp ...` archive command separately, because `sign-shortcut` already produces a dated archive copy at the identical `artifacts/shortcuts/<date>/<name>-<HHMMSS>.xml` path as a side effect of signing — running the manual copy afterward would have just duplicated the same bytes under a different timestamp

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ship-readiness-cleanup todo item 1 is closed; items 2-5 (`.gitignore`, further MANIFEST.md refresh scope, Control Room note-picker on-device tap, brightness/volume MVP cut) remain open and untouched by this task
- On-device OPEN-path regression confirmation for this rebuild stays blocked on DIST-03 (no connected iPhone via `xcrun devicectl`) — re-run once a device is available, per STATE.md's existing note

---
*Quick task: 260816-ukb*
*Completed: 2026-08-16*

## Self-Check: PASSED

All modified files (tools/build_state_engine.py, src/PROSOCHE-Dumb.xml, the signed .shortcut,
the dated archive XML, MANIFEST.md, and the ship-readiness-cleanup todo) confirmed present on
disk. All three task commits (708847a, 5b1d2e6, 154b998) confirmed present in git log.
