---
phase: 04-close-pipeline-session-race
plan: 03
subsystem: state-engine
tags: [shortcuts, plist, generator, notification, ux]

# Dependency graph
requires:
  - phase: 04-close-pipeline-session-race (plan 02)
    provides: close_pipeline()'s ownership conditional resolved to token("Captured Session ID"); build-time WFConditionalActionString recurrence guard
provides:
  - notification(title, body) helper (mirrors alert()'s minimal-params shape)
  - Unconditional OPEN completion Notification (Circle/Pressure/Heat), independent of OPEN_BISECT
  - Unconditional CLOSE completion Notification (session duration), independent of declared contract
  - universal_leaving() menu prompt names the active Circle instead of the bare string "PROSOCHĒ"
  - ship-readiness-cleanup todo records the delivered replacement signal as a satisfied precondition for its own breadcrumb-strip step
affects: [04-verify-work, 06-exits-exit-learning-contracts]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "notification(title, body): non-blocking on-device confirmation, same minimal-params shape as alert() (no WFNotificationActionSound, no WFInput), added to STRING_ENVELOPE_PARAMS alongside alert()."
    - "Display-facing WFMenuPrompt can carry a text_token() (WFTextTokenString) directly, same as alert()'s WFAlertActionMessage -- first variable-carrying menu prompt in this file."

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - src/PROSOCHE-Dumb.xml
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut"
    - artifacts/shortcuts/MANIFEST.md
    - .planning/todos/pending/2026-08-15-ship-readiness-cleanup.md

key-decisions:
  - "notification() calls are placed as plain list entries in open_pipeline()/close_pipeline()'s Python action lists (not inside any if_block), so they are structurally unconditional -- confirmed by inspecting breadcrumb()'s own implementation (a flat list return with no wrapping control flow), and by the plan's own verify script finding exactly 2 is.workflow.actions.notification calls in the built artifact."
  - "Reused knock()'s exact 'Circle X · pressure Y · heat Z' phrasing for the OPEN notification body, per the plan's explicit instruction, for wording consistency across the two on-device confirmation surfaces."
  - "universal_leaving()'s menu prompt is only ever called from open_pipeline() (single call site, after 'Circle Next' is already set at breadcrumb I), so naming that variable in the prompt is always safe -- verified via grep before editing."

patterns-established:
  - "notification() helper: the same minimal-params, no-sound, no-input shape as alert() -- reuse for any future non-blocking on-device confirmation."

requirements-completed: [SESS-02, SESS-03, SESS-04, SESS-05, SESS-06, SESS-07]

coverage:
  - id: D1
    description: "OPEN fires an unconditional, non-blocking Notification (title 'PROSOCHĒ', body 'Circle X · pressure Y · heat Z') after breadcrumb J's position, independent of OPEN_BISECT's on/off state."
    requirement: "SESS-02"
    verification:
      - kind: unit
        ref: "python3 -c '...' plistlib-decode check embedded in 04-03-PLAN.md Task 1 <verify> (NOTIFICATIONS-AND-MENU-COPY-OK) -- confirms exactly 2 is.workflow.actions.notification calls exist"
        status: pass
    human_judgment: true
    rationale: "Static plist inspection proves the Notification actions exist and are structurally unconditional (not nested in any if_block), but only an on-device OPEN run can confirm the banner actually appears with correct text -- deferred to a later /gsd-verify-work pass against 04-UAT.md tests 4, 5, and 6 per this plan's own explicit scope."
  - id: D2
    description: "CLOSE fires an unconditional, non-blocking Notification (title 'PROSOCHĒ', body 'Session closed · <duration> sec') in the owns_if TRUE branch, independent of whether a contract was declared."
    requirement: "SESS-03"
    verification:
      - kind: unit
        ref: "Same plistlib-decode check as D1 (NOTIFICATIONS-AND-MENU-COPY-OK)"
        status: pass
    human_judgment: true
    rationale: "Same as D1 -- on-device confirmation deferred to the later /gsd-verify-work pass."
  - id: D3
    description: "universal_leaving()'s menu prompt now names the active Circle ('Circle <N> opened. Leave now, or continue?') instead of the bare string 'PROSOCHĒ', disambiguating the OPEN-only menu from a CLOSE-path signal."
    requirement: "SESS-05"
    verification:
      - kind: unit
        ref: "Same plistlib-decode check as D1 -- asserts WFMenuPrompt is a dict (text_token) containing 'Circle Next'"
        status: pass
    human_judgment: true
    rationale: "Structural check confirms the prompt is variable-carrying, but the actual on-screen wording and Circle value can only be confirmed by an on-device OPEN run -- deferred to the later /gsd-verify-work pass."
  - id: D4
    description: "Rebuilt src/PROSOCHE-Dumb.xml validates cleanly and a freshly signed, non-empty PROSOCHĒ — Nine Circles — Dumb.shortcut is produced; MANIFEST.md's three Dumb-fork rows updated."
    requirement: "SESS-06"
    verification:
      - kind: unit
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all"
        status: pass
      - kind: unit
        ref: "sign-shortcut src/PROSOCHE-Dumb.xml --name \"PROSOCHĒ — Nine Circles — Dumb\" --output-dir artifacts/shortcuts (non-empty output confirmed)"
        status: pass
    human_judgment: false
  - id: D5
    description: "ship-readiness-cleanup todo's Solution step 1 records the delivered replacement signal as a satisfied precondition, so its own breadcrumb-strip step is now safe to run."
    requirement: "SESS-07"
    verification:
      - kind: unit
        ref: "grep -q '04-03-PLAN.md' .planning/todos/pending/2026-08-15-ship-readiness-cleanup.md"
        status: pass
    human_judgment: false

# Metrics
duration: 20min
completed: 2026-08-16
status: complete
---

# Phase 4 Plan 3: OPEN/CLOSE unconditional Notification confirmations Summary

**Added a permanent, unconditional Notification confirmation for both OPEN (Circle/Pressure/Heat) and CLOSE (session duration), and gave the Leaving/Continue menu real explanatory copy naming the active Circle, closing gap G-04-4b that blocked UAT tests 4-6.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-08-16T20:00 (immediately after 04-02's plan-metadata commit)
- **Completed:** 2026-08-16T20:04
- **Tasks:** 2
- **Files modified:** 5 (`tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml`, signed `.shortcut`, `MANIFEST.md`, ship-readiness-cleanup todo) plus one new dated archive XML

## Accomplishments

- Added `notification(title, body)` helper, mirroring `alert()`'s minimal-params shape (no `WFNotificationActionSound`/`WFInput`), wired into `STRING_ENVELOPE_PARAMS`.
- `open_pipeline()` now fires an unconditional `Notification` immediately after breadcrumb J's position (Circle/Pressure/Heat, reusing `knock()`'s exact phrasing) -- the permanent replacement for breadcrumb J's de facto confirmation role, independent of `OPEN_BISECT`.
- `close_pipeline()` now fires an unconditional `Notification` (session duration) in the `owns_if` TRUE branch, independent of whether a contract was declared -- unlike the existing conditional "Contract" alert.
- `universal_leaving()`'s menu prompt changed from the bare string `"PROSOCHĒ"` to a `text_token()` naming the active Circle (`"Circle <N> opened. Leave now, or continue?"`), disambiguating the OPEN-only dismissal menu from a CLOSE-path signal.
- `ship-readiness-cleanup` todo's Solution step 1 now records this delivered signal as a satisfied precondition, so its breadcrumb-strip step is safe to run afterward.
- Rebuilt, validated (`--target-macos 26 --target-platform all`, zero errors), and re-signed `PROSOCHĒ — Nine Circles — Dumb.shortcut`; `MANIFEST.md`'s three Dumb-fork rows updated with fresh byte counts and SHA-256 hashes.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add unconditional Notification confirmations for OPEN and CLOSE, and give the Leaving menu real copy** - `564eb47` (feat)
2. **Task 2: Record the replacement signal in the ship-readiness-cleanup todo, then validate, sign, and re-verify** - `c5ad62c` (build)

_No plan-metadata commit was made separately in the usual STATE.md-mutating sense; ROADMAP.md/REQUIREMENTS.md updates and this SUMMARY.md are committed as part of finishing this plan's `/gsd-execute-phase` step. STATE.md is deliberately NOT touched per this dispatch's explicit project_state_override (project is mid-Phase-8 UAT; this is Phase-4 gap-closure work)._

## Files Created/Modified

- `tools/build_state_engine.py` - New `notification()` helper; `STRING_ENVELOPE_PARAMS` entry; unconditional calls wired into `open_pipeline()` and `close_pipeline()`; `universal_leaving()`'s menu prompt made variable-carrying.
- `src/PROSOCHE-Dumb.xml` - Regenerated artifact reflecting all of the above.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` - Freshly signed, non-empty.
- `artifacts/shortcuts/2026-08-16/PROSOCHĒ — Nine Circles — Dumb-200329.xml` - Dated archive produced by the signer, matching MANIFEST.md's "Dumb archive" row.
- `artifacts/shortcuts/MANIFEST.md` - Dumb-fork rows (source, archive, signed) updated with new byte counts/hashes.
- `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md` - Solution step 1 now records the delivered replacement signal as a satisfied precondition.

## Decisions Made

- Confirmed both `notification()` call sites are structurally unconditional by inspecting `breadcrumb()`'s own implementation (a flat list with no control-flow wrapping) before placing the OPEN call directly after it, and by placing the CLOSE call inside `owns_if`'s TRUE branch only (never in an `otherwise` arm).
- Confirmed `universal_leaving()` has exactly one call site (`open_pipeline()`, after `"Circle Next"` is already set) via grep before referencing that variable in the menu prompt, avoiding an unset-variable risk at any other call site.
- Reused `knock()`'s exact wording for the OPEN notification body per the plan's explicit instruction, keeping the two on-device confirmation surfaces (in-Circle alert vs. completion notification) textually consistent.

## Deviations from Plan

None - plan executed exactly as written. Both tasks' `<verify>` and `<done>` criteria were met without needing any Rule 1-4 auto-fix.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The rebuilt, signed `PROSOCHĒ — Nine Circles — Dumb.shortcut` carries both unconditional Notification calls and the improved Leaving-menu copy, ready for on-device re-import.
- On-device confirmation that the Notifications and menu copy actually appear as intended (UAT tests 4, 5, and 6) is deferred to a later `/gsd-verify-work` pass, per this plan's own explicit scope -- not performed here.
- The `ship-readiness-cleanup` todo's breadcrumb-strip step (item 1) is now safe to execute without leaving OPEN/CLOSE with zero on-device confirmation signal; its other four items remain open and untouched.

---
*Phase: 04-close-pipeline-session-race*
*Completed: 2026-08-16*

## Self-Check: PASSED

All modified/created files confirmed present on disk; all task commit hashes confirmed in `git log`.
