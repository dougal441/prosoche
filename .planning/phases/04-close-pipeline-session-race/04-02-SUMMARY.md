---
phase: 04-close-pipeline-session-race
plan: 02
subsystem: state-engine
tags: [shortcuts, plist, generator, wfconditionalactionstring, python]

# Dependency graph
requires:
  - phase: 04-close-pipeline-session-race (plan 01)
    provides: CLOSE session-ownership/race-abort scaffolding this plan's fix makes reachable
provides:
  - close_pipeline()'s session-ownership comparator wired to token("Captured Session ID")
  - Every remaining "unfinished two-step WFConditionalActionString wiring" site fixed (enabled_exits, select_exit, record_exit_and_route, open_pipeline)
  - verify_conditional_action_string() build-time recurrence guard, wired into main()
  - Rebuilt, re-validated, re-signed PROSOCHĒ — Nine Circles — Dumb.shortcut
affects: [04-verify-work, phase-06-exits-exit-learning-contracts, phase-08-sentient-fork-dual-distribution]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Comparator wiring: if_block(..., string=<placeholder>) must always be followed by a token(<real variable>) reassignment to WFConditionalActionString — never left as the bare placeholder character."
    - "Missing-field guards use WFCondition 101 (\"does not have any value\") directly on the read variable, not a condition-5 comparison against a literal empty/sentinel string — condition 5 vs any fixed sentinel can never distinguish missing from present for a field with an open-ended real-data domain."

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - docs/state_engine_self_check.py
    - src/PROSOCHE-Dumb.xml
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut"
    - artifacts/shortcuts/MANIFEST.md

key-decisions:
  - "close_pipeline()'s owns_if comparator now resolves through token(\"Captured Session ID\"), matching the three already-correct sibling ownership checks (persist_contract, route_exit, record_exit_and_route)."
  - "Deviated from the plan's literal 'pass the empty string as its string argument' instruction for the three missing-value guards (select_exit()'s and record_exit_and_route()'s exit_selection_counter guards, open_pipeline()'s Stored Day guard): a literal empty WFConditionalActionString is rejected outright by the bundled validator's iter_empty_strings check (confirmed empirically, raw and WFTextTokenString-wrapped), and even if it weren't, condition 5 (\"is not <sentinel>\") is true for every real present value too, so it could never correctly distinguish missing from present. Used WFCondition 101 (\"does not have any value\") instead, needing no comparator string, matching this file's own established has-any-value idiom (\"Contract Active Session\", \"Spoken This Run\")."
  - "wrap_non_best's condition-99 (\"contains\") comparator is wired to token(\"Best Exit\") per plan instruction, with a follow-up comment flagging its condition-code semantics as a separate, unconfirmed question outside this defect class — left unchanged."
  - "Fixed a stale, unrelated assertion in docs/state_engine_self_check.py (gettimebetweendates count) that was already failing at this plan's base commit, left over from CYCLE 14's replacement of downstream elapsed-time math with plain subtraction; it blocked this plan's own required verification step."

patterns-established:
  - "verify_conditional_action_string(actions), called from main() immediately after verify_conditional_inputs(), fails the build if any is.workflow.actions.conditional If-start action still holds the bare, un-enveloped placeholder character in WFConditionalActionString."

requirements-completed: [SESS-02, SESS-03, SESS-04, SESS-05, SESS-06, SESS-07]

coverage:
  - id: D1
    description: "close_pipeline()'s session-ownership conditional resolves to token(\"Captured Session ID\") instead of a bare unwired placeholder — the confirmed root cause of G-04-1 (session duration always 0) and G-04-3 (CLOSE never switches, permanent no-op)."
    requirement: "SESS-02"
    verification:
      - kind: unit
        ref: "python3 -c '...' plistlib-decode check embedded in 04-02-PLAN.md Task 1 <verify> (CLOSE-OWNERSHIP-WIRED-OK)"
        status: pass
    human_judgment: true
    rationale: "Static plist inspection proves the comparator is wired correctly, but only an on-device OPEN->wait->CLOSE run can confirm duration_seconds is genuinely non-zero and the session-race abort actually fires — deferred to a later /gsd-verify-work pass against 04-UAT.md tests 1, 3, and 6 per this plan's own scope."
  - id: D2
    description: "Every other unfinished WFConditionalActionString wiring site swept in one pass (enabled_exits, select_exit x5, record_exit_and_route, open_pipeline x2), plus a new verify_conditional_action_string() build guard wired into main() to catch any future regression of this defect class."
    requirement: "SESS-04"
    verification:
      - kind: unit
        ref: "tools/build_state_engine.py verify_conditional_action_string(actions), invoked automatically by every python3 tools/build_state_engine.py run"
        status: pass
      - kind: unit
        ref: "python3 docs/state_engine_self_check.py"
        status: pass
    human_judgment: false
  - id: D3
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

# Metrics
duration: 45min
completed: 2026-08-16
status: complete
---

# Phase 4 Plan 2: CLOSE-pipeline WFConditionalActionString sweep Summary

**Wired close_pipeline()'s session-ownership comparator and every other unfinished `WFConditionalActionString` site to real `token()` references (or a validator-safe `WFCondition 101` presence test where a literal comparator was fundamentally unworkable), added a build-time `verify_conditional_action_string()` recurrence guard, and shipped a freshly validated, signed Dumb `.shortcut`.**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-08-16T09:XX (see debug docs read at session start)
- **Completed:** 2026-08-16
- **Tasks:** 3
- **Files modified:** 5 (`tools/build_state_engine.py`, `docs/state_engine_self_check.py`, `src/PROSOCHE-Dumb.xml`, signed `.shortcut`, `MANIFEST.md`)

## Accomplishments

- Fixed the confirmed root cause of G-04-1 (session duration always 0) and G-04-3 (CLOSE session race never switches, permanent no-op): `close_pipeline()`'s `owns_if` conditional now resolves through `token("Captured Session ID")`.
- Swept the identical "abandoned two-step wiring idiom" defect class at every other confirmed site: `enabled_exits()` ("Enabled Exit Candidate" vs `token("Canonical Exit")`), `select_exit()` (exit_selection_counter missing-value guard, "Candidate Exit" vs `token("Best Exit")` at two sites, two regressed literal-"0" comparators restored to their original correct form), `record_exit_and_route()` (exit_selection_counter missing-value guard), `open_pipeline()` (Stored Day missing-value guard and same-day comparison vs `token("Behavioural Day")`).
- Added `verify_conditional_action_string()`, wired into `main()` right after `verify_conditional_inputs()`, so this exact defect class fails the build automatically if it ever regresses.
- Rebuilt, validated (`--target-macos 26 --target-platform all`, zero errors), and re-signed `PROSOCHĒ — Nine Circles — Dumb.shortcut`; `MANIFEST.md`'s three Dumb-fork rows updated with fresh byte counts and SHA-256 hashes.

## Task Commits

Each task was committed atomically:

1. **Task 1: Wire close_pipeline()'s session-ownership comparator** - `da9ae39` (fix)
2. **Task 2: Sweep the same unfinished wiring idiom, add a build-time recurrence guard** - `6d5498e` (fix)
   - **Follow-up correction discovered while running Task 3's validator** - `f4c093f` (fix) — see Deviations below
3. **Task 3: Validate, sign, and re-verify the rebuilt Dumb artifact** - `fcc5c3f` (build)

_No plan-metadata commit was made separately; ROADMAP.md/REQUIREMENTS.md are updated as part of finishing this plan's `/gsd-execute-phase` step, and STATE.md is deliberately NOT touched per this dispatch's explicit override (project is mid-Phase-8 UAT; this is Phase-4 gap-closure work)._

## Files Created/Modified

- `tools/build_state_engine.py` - Wired `close_pipeline()`'s ownership comparator and 9 other unfinished `WFConditionalActionString` sites; added `verify_conditional_action_string()`.
- `docs/state_engine_self_check.py` - Fixed a stale, pre-existing `gettimebetweendates` count assertion left over from CYCLE 14 (unrelated to this defect class, but blocked this plan's own required verification).
- `src/PROSOCHE-Dumb.xml` - Regenerated artifact reflecting every fix.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` - Freshly signed, non-empty.
- `artifacts/shortcuts/MANIFEST.md` - Dumb-fork rows (source, archive, signed) updated with new byte counts/hashes.

## Decisions Made

- Mirrored the three already-correct sibling ownership-check sites exactly for Task 1 (kept the existing bare-placeholder line for structural consistency, appended the real `token()` reassignment after it, matching `persist_contract()`'s established three-line idiom).
- For the `wrap_non_best` site (condition 99, "contains"), wired the comparator to `token("Best Exit")` per plan instruction but left a comment flagging its condition-code semantics as a separate, unconfirmed follow-up question — not touched, per plan's explicit scope boundary.
- Deviated from the plan's literal "pass the empty string as its string argument" instruction for three missing-value guards (see Deviations below) after confirming empirically that a literal empty `WFConditionalActionString` is rejected by the bundled validator, and that condition 5 vs any fixed sentinel cannot correctly express "field is missing" for an open-ended-value field regardless of sentinel choice.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Plan's literal "pass empty string" instruction is unimplementable; used WFCondition 101 instead**
- **Found during:** Task 2, while running Task 3's `validate-shortcut` (the failure surfaced downstream of Task 2's own `<verify>`, which only checks `python3 tools/build_state_engine.py` and `docs/state_engine_self_check.py`, neither of which runs the Shortcuts Playground validator)
- **Issue:** The plan's Task 2 instructed passing a literal empty string directly into `if_block(..., 5, string="")` for three "missing value" guards (`select_exit()`'s and `record_exit_and_route()`'s `exit_selection_counter` guards, `open_pipeline()`'s `Stored Day` guard). This produces a plist that `validate-shortcut --target-macos 26 --target-platform all` rejects outright: the validator's `iter_empty_strings` check flags any empty `WFConditionalActionString` (confirmed both raw and `WFTextTokenString`-wrapped forms are rejected — there is no encoding of "compare against literal empty text" that passes), and a second, independent validator rule requires `WFConditionalActionString` to be truthy for any string-condition code. Separately, and independent of the validator: condition 5 ("is not `<sentinel>`") is mathematically true for every real, present field value too (a real day string or counter number will essentially never equal an arbitrary fixed sentinel), so even a validator-compatible non-empty sentinel could never actually distinguish "missing" from "present" for these open-domain fields — unlike `complete_pending_exit()`'s `CLEARED_SENTINEL` guard, which works only because `pending_exit.type` has a closed, app-controlled value domain (either a real exit-type string or the literal `"null"` the app itself writes when clearing it).
- **Fix:** Switched all three sites from `if_block(<name>, 5, string="")` to `if_block(<name>, 101)` ("does not have any value") — no comparator string needed at all, TRUE correctly maps to "field is missing" for each guard's own reset branch, and it matches this file's own already-established has-any-value idiom (`if_block("Contract Active Session", 100)`, `if_block("Spoken This Run", 101)`).
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** `python3 tools/build_state_engine.py` exits 0; `python3 docs/state_engine_self_check.py` exits 0; `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` reports zero errors.
- **Committed in:** `f4c093f`

**2. [Rule 3 - Blocking] Fixed a stale, pre-existing assertion in docs/state_engine_self_check.py**
- **Found during:** Task 2's own `<verify>` command, which chains `python3 docs/state_engine_self_check.py` as a hard requirement
- **Issue:** `structural_check()` asserted `ids.count("is.workflow.actions.gettimebetweendates") >= 3`. This was already failing at this plan's base commit (confirmed by testing against commit `b21542d` directly, before any of this plan's edits) — CYCLE 14 had replaced every downstream elapsed-time computation with plain numeric subtraction (`elapsed_since()`), leaving only the CLOCK block's single `Get Time Between Dates` action. The assertion was never updated to match.
- **Fix:** Changed the assertion to `== 1`, matching the current, documented architecture (`elapsed_since()`'s own docstring: "Donor 7's device-confirmed chain... remains the CLOCK block's own construct for producing 'Now Epoch' itself").
- **Files modified:** `docs/state_engine_self_check.py`
- **Verification:** `python3 docs/state_engine_self_check.py` exits 0.
- **Committed in:** `6d5498e`

---

**Total deviations:** 2 auto-fixed (1 bug — plan instruction unimplementable, 1 blocking — pre-existing stale assertion)
**Impact on plan:** Both deviations were necessary to satisfy this plan's own literal `<verify>`/`<done>` criteria. Neither changes the scope or intent of the fix (still exactly the same defect class, same set of ~10 sites, same recurrence guard). No scope creep beyond what was required to make the plan's own verification pass.

## Issues Encountered

None beyond the two deviations documented above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The rebuilt, signed `PROSOCHĒ — Nine Circles — Dumb.shortcut` is ready for on-device re-import.
- On-device re-verification of `.planning/phases/04-close-pipeline-session-race/04-UAT.md` tests 1, 3, and 6 (session duration, session-race abort, and the associated end-to-end flow) is deferred to a later `/gsd-verify-work` pass, per this plan's own explicit scope — not performed here.
- `verify_conditional_action_string()` now runs on every build going forward, so any future regression of this specific defect class fails the build immediately rather than shipping silently.

---
*Phase: 04-close-pipeline-session-race*
*Completed: 2026-08-16*

## Self-Check: PASSED

All modified/created files confirmed present on disk; all task and metadata commit hashes confirmed in `git log`.
