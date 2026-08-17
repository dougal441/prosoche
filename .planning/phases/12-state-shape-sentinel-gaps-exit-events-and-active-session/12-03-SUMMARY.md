---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
plan: 03
subsystem: infra
tags: [shortcuts, plist, state-json, build-guards, generator, active-session, sess-07, safe-01, exit-01, exit-02]

# Dependency graph
requires:
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-02"
    provides: "active_session seeded as a permanent four-leaf {id, started_at, declared_duration_seconds, intention} container on both forks; verify_active_session_seed() armed with a self-dissolving deferral on assertion 3, keyed on KNOWN_SENTINEL_EXISTENCE_GATES"
provides:
  - "Every emitted active_session gate converted from container-existence semantics (condition 100) to leaf semantics (condition 5 against CLEARED_SENTINEL) or absorbed into the pre-existing condition-4 ownership compare, across six generator functions"
  - "open_pipeline() writes active_session's four leaves individually; three clears (close_pipeline, live_ice_redirect, manual_emergency_restore) write only active_session.id"
  - "KNOWN_SENTINEL_EXISTENCE_GATES emptied to (); verify_sentinel_gates() and verify_active_session_seed()'s assertion 3 both run unexempted and clean on both forks"
  - "docs/state_engine_self_check.py's required setter-key literal moved from 'active_session' to 'active_session.id'"
  - "verify_sentinel_gates() demonstrated to fire against a synthetically reverted container clear, two ways: full-build (verify_active_session_seed's newly-armed assertion 3) and direct-call (verify_sentinel_gates() itself, isolated)"
affects: [12-04, 12-05, active_session-gate-conversion, close_pipeline, persist_contract, record_exit_and_route, restore_managed_settings]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Container/leaf gate conversion: at a site already carrying a condition-4 ownership compare, the .id read doubles as the gate and the flat container existence-read/condition-100 pair is deleted outright (persist_contract, record_exit_and_route, close_pipeline's reload gate) -- one read, one conditional, no net addition"
    - "Container/leaf gate REPLACEMENT (not deletion) at a site with no ownership compare beneath it: close_pipeline()'s entry gate swaps its condition-100 container existence test for a condition-5 leaf gate on active_session.id, the complete_pending_exit() idiom"
    - "A site whose bare .id read already had no enclosing container gate needs no change once the container is a seeded invariant -- route_exit()'s Create branch was flagged as a defect under the old shape and is the target shape under the new one"
    - "Wholesale container write -> N independent leaf set_value() calls, each through the shared normalize_setters() full-dictionary-rebind pass, net action-count reduction with no new identifier or parameter key"
    - "Sensitivity demonstration for a deferred-then-emptied guard constant, two ways: full build (whichever guard sits earlier in main()'s verify chain fires first) and a direct-call script that skips the earlier guard to isolate the target guard's own message"

key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "docs/state_engine_self_check.py"
    - "src/PROSOCHE-Dumb.xml"
    - "src/PROSOCHE-Sentient.xml"

key-decisions:
  - "Site 3 (close_pipeline()'s entry gate) is the only one of the six that REPLACES its existence gate rather than deleting it outright -- it has no ownership compare beneath it (it captures state before the interleaved-OPEN wait), so a leaf gate on active_session.id is genuinely needed, not merely redundant with an existing compare"
  - "route_exit()'s Create branch (Site 5) received NO code change -- its bare .id read with no enclosing gate was correct under the new container-as-invariant shape and would have been a regression to 'fix'"
  - ".intention is explicitly cleared in open_pipeline()'s new leaf-write block even though read nowhere today, to reproduce the old wholesale-replace semantics exactly and avoid leaving stale cross-session data as unintentional drift"
  - "The four leaves are three set_value() calls plus one number()-bound numeric write (active_session.declared_duration_seconds), using the same number() helper select_exit() already uses, because today's emitted session JSON serialises that field unquoted"
  - "Guard sensitivity was demonstrated two ways because the full-build revert exercises verify_active_session_seed()'s assertion 3 first (it runs earlier in main()'s chain) rather than verify_sentinel_gates() -- a direct-call script that skips the earlier guard was used to isolate and capture verify_sentinel_gates()'s own SystemExit message, mirroring 12-02's precedent for demonstrating a guard two ways"

patterns-established:
  - "Container/leaf gate conversion has two distinct shapes depending on whether an ownership compare already sits beneath the existence gate: absorption (delete the gate, the compare already excludes the sentinel) versus replacement (swap condition-100 for condition-5, when no compare exists to absorb the check)"
  - "When two build guards would both fire against the same synthetic defect and one runs earlier in the pipeline, demonstrate the later guard by a direct-call script that constructs the same actions and skips the earlier guard -- rather than trying to force the full build past the earlier guard"

requirements-completed: [SESS-07, SAFE-01, EXIT-01, EXIT-02]

coverage:
  - id: D1
    description: "No condition-100 existence gate stands over any variable read from active_session anywhere in either emitted fork -- the four flat container reads and their conditionals are gone, replaced by the leaf reads that were already nested inside them"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "verify_sentinel_gates(actions) called unexempted (KNOWN_SENTINEL_EXISTENCE_GATES == ()) against both src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml"
        status: pass
    human_judgment: false
  - id: D2
    description: "active_session is never written or cleared as a whole container: open_pipeline() writes four leaves, and all three clears write active_session.id with the cleared sentinel"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "python3 -c '...' asserting 'active_session' not in setk, setk.count('active_session.id')>=4, and all three named leaves present -- Task 1's verify block"
        status: pass
    human_judgment: false
  - id: D3
    description: "The session-ownership compare survives untouched at all four owner sites -- condition 4 against the WFConditionalActionString token for Session ID / Captured Session ID"
    requirement: "SAFE-01"
    verification:
      - kind: integration
        ref: "git diff -- tools/build_state_engine.py showing no +/- prefix on any WFConditionalActionString assignment line"
        status: pass
    human_judgment: false
  - id: D4
    description: "KNOWN_SENTINEL_EXISTENCE_GATES is the empty tuple and verify_sentinel_gates() runs unexempted with zero offenders on both forks"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "B.KNOWN_SENTINEL_EXISTENCE_GATES == () asserted; verify_sentinel_gates(actions), verify_active_session_seed(actions), verify_restore_gates(actions), verify_compound_value_reads(actions) all clean on both forks"
        status: pass
    human_judgment: false
  - id: D5
    description: "restore_managed_settings() still runs before notification() and save_state() in close_pipeline()'s owner arm; brightness/volume writes stay behind a numeric greater-than-zero gate"
    requirement: "SAFE-01"
    verification:
      - kind: integration
        ref: "python3 docs/environmental_restore_check.py; python3 docs/phase5_self_check.py; python3 docs/phase9_self_check.py -- all exit 0"
        status: pass
    human_judgment: false
  - id: D6
    description: "Exit routing (six routes, exact-match condition 4) and their state keys survive the refactor unchanged"
    requirement: "EXIT-01"
    verification:
      - kind: integration
        ref: "python3 docs/phase6_self_check.py -- exit 0, double-build byte-idempotency"
        status: pass
    human_judgment: false
  - id: D7
    description: "docs/state_engine_self_check.py's required setter-key tuple names active_session.id rather than bare active_session, edited in the same commit as the emission change"
    requirement: "EXIT-02"
    verification:
      - kind: integration
        ref: "python3 docs/state_engine_self_check.py exit 0; count-equality check that every 'active_session' substring in the file is part of 'active_session.id'"
        status: pass
    human_judgment: false
  - id: D8
    description: "verify_sentinel_gates() demonstrated to fire against a synthetically reverted artifact, not merely observed to pass"
    verification:
      - kind: integration
        ref: "live_ice_redirect()'s clear temporarily reverted to a container clear; full build raised verify_active_session_seed()'s assertion 3, direct-call script (skipping that earlier guard) raised verify_sentinel_gates() itself naming 19 offenders; both restored and rebuilt byte-identical (Sentient digest 300247df...)"
        status: pass
    human_judgment: false

# Metrics
duration: 10 min
completed: 2026-08-17
status: complete
---

# Phase 12 Plan 03: active_session container-to-leaf gate conversion Summary

**Converted every emitted `active_session` gate, write and clear from container-existence semantics to leaf semantics across six generator functions (persist_contract, record_exit_and_route, close_pipeline's two gates, route_exit's Create branch, open_pipeline's write), then emptied `KNOWN_SENTINEL_EXISTENCE_GATES` and proved `verify_sentinel_gates()` fires against a synthetically reverted artifact.**

## Performance

- **Duration:** 10 min
- **Tasks:** 2
- **Files modified:** 4 (tools/build_state_engine.py, docs/state_engine_self_check.py, src/PROSOCHE-Dumb.xml, src/PROSOCHE-Sentient.xml)

## Accomplishments

- **Converted 34 measured emitted offenders across six generator functions, one commit.** `persist_contract()` (renders 11x) and `record_exit_and_route()` (renders 2x) each lost a flat container read and its condition-100 existence gate, absorbed into the pre-existing condition-4 ownership compare that already excludes the cleared sentinel. `close_pipeline()`'s reload gate got the identical treatment. `close_pipeline()`'s entry gate — the one site with no ownership compare beneath it — had its existence gate REPLACED with a condition-5 leaf gate on `active_session.id`, the `complete_pending_exit()` idiom. `route_exit()`'s Create branch and `close_pipeline()`'s `.declared_duration_seconds` read needed no change at all.
- **Replaced the last wholesale container write.** `open_pipeline()` now writes four independent leaves (`.id`, `.started_at`, `.declared_duration_seconds` via a fresh `number()`-bound `"Session Declared Duration"` variable, `.intention` cleared to reproduce the old wholesale-replace semantics) instead of building and writing a whole session dictionary — a net reduction of three actions, no new identifier or parameter key.
- **All three clears now write the leaf, never the container.** `close_pipeline()`, `live_ice_redirect()` and `manual_emergency_restore()` all clear `active_session.id` only, each carrying the "Clear the LEAF, never the container" comment `complete_pending_exit()` established.
- **Emptied `KNOWN_SENTINEL_EXISTENCE_GATES` and rewrote both documentation blocks honestly.** The 24-line note beside `CLEARED_SENTINEL` now records the closure (34 offenders, six functions, SESS-07/SAFE-01 consequence) instead of describing a latent defect. `verify_sentinel_gates()`'s docstring records both `pending_exit` and `active_session` as closed with the tuple empty.
- **Proved the guard has teeth, not just that it passes.** Reverting one leaf clear back to a container clear and rebuilding fired `verify_active_session_seed()`'s newly-armed assertion 3 (it runs earlier in `main()`'s verify chain); a direct-call script that skipped that earlier guard isolated and captured `verify_sentinel_gates()`'s own `SystemExit`, naming 19 offenders. Both source files restored and rebuilt byte-identical to the pre-demonstration state.

## Task Commits

Each task was committed atomically:

1. **Task 1: Convert every active_session gate, write and clear to leaf semantics — one class, one commit** — `8125d25` (feat)
2. **Task 2: Empty KNOWN_SENTINEL_EXISTENCE_GATES, correct the two documentation blocks, and prove the guard now has teeth** — `43a2f4b` (fix)

## Files Created/Modified

- `tools/build_state_engine.py` — six generator functions converted (`persist_contract`, `record_exit_and_route`, `close_pipeline`, `open_pipeline`, `live_ice_redirect`, `manual_emergency_restore`); `KNOWN_SENTINEL_EXISTENCE_GATES` emptied; the 24-line note beside `CLEARED_SENTINEL` and `verify_sentinel_gates()`'s docstring rewritten.
- `docs/state_engine_self_check.py` — required setter-key literal moved from `"active_session"` to `"active_session.id"`, with a comment naming why.
- `src/PROSOCHE-Dumb.xml` — regenerated Core fork, zero sentinel-existence-gate offenders.
- `src/PROSOCHE-Sentient.xml` — regenerated Aware fork, inherits the same conversion.

## Decisions Made

- **`close_pipeline()`'s entry gate is the sole REPLACEMENT site.** All other five sites either delete a now-redundant existence gate (absorbed by an existing ownership compare) or need no change; this one site genuinely needs a new leaf gate because it captures state before the interleaved-OPEN wait, with no ownership compare beneath it yet.
- **`route_exit()`'s Create branch received zero code changes.** Its bare `.id` read with no enclosing container gate was flagged as a defect under the old container-existence shape; under the new container-as-invariant shape it is already correct, and "fixing" it would have been a regression. Recorded in the commit body per the plan's explicit instruction.
- **`.intention` is cleared in `open_pipeline()`'s new leaf-write block even though it is read nowhere today.** The former wholesale write destroyed any prior `.intention` on every OPEN; the plan is explicit that leaving it unwritten would let stale cross-session data survive as unintentional drift, so the fourth write reproduces the old semantics exactly.
- **Guard sensitivity required two demonstration paths, not one.** `main()`'s verify chain calls `verify_active_session_seed()` before `verify_sentinel_gates()`, so a full-build revert fires the former's newly-armed assertion 3 first. A direct-call script (mirroring 12-02's own two-ways technique) was written to skip the earlier guard and isolate `verify_sentinel_gates()`'s own message, satisfying the plan's specific acceptance criterion.

## Deviations from Plan

None — plan executed exactly as written. The guard-sensitivity demonstration surfaced that `verify_active_session_seed()` fires before `verify_sentinel_gates()` in the full-build path (an accurate observation of the existing pipeline order, not a defect), which is why the direct-call isolation technique was used in addition to the full-build demonstration — both are recorded verbatim above and in the Task 2 commit body, satisfying the plan's letter and its intent.

## Issues Encountered

None. No guard fired unexpectedly during normal (non-sensitivity-demo) rebuilds, no fix-attempt limit approached, no unplanned working-tree residue — the sensitivity demonstration's temporary revert was restored and the Sentient digest matched byte-for-byte before and after (`300247df47b41d736b794778800daf81a20f436cd1aea1d98fe16a9bfcaabffd`), and the Dumb fork rebuilt byte-identical to its Task 1 committed state.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` (D-01 provenance gate) | exit 0, re-run before every builder invocation |
| Precondition: `verify_active_session_seed()` against pre-existing `src/PROSOCHE-Dumb.xml` | passed before Task 1 began |
| `python3 tools/build_state_engine.py` | exit 0, both tasks |
| `python3 tools/build_sentient.py` | exit 0, digest `300247df47b41d736b794778800daf81a20f436cd1aea1d98fe16a9bfcaabffd` |
| Structural verify (`active_session` bare key absent, `.id` count ≥4, three other leaves present, five dead variable names absent, eight live variable names present) | passed |
| `docs/state_engine_self_check.py` | exit 0; count-equality check on `active_session` substring occurrences passed |
| `python3 docs/phase5_self_check.py`, `phase6_self_check.py`, `phase7_self_check.py`, `phase9_self_check.py` | all exit 0 |
| `python3 docs/environmental_restore_check.py` | exit 0 |
| `python3 docs/sentient_audit_check.py`, `sentient_core_check.py` | exit 0 |
| `python3 docs/router_ui_census.py`, `sequence_dispatch_check.py`, `note_identity_check.py` | exit 0 |
| `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| Gate B (advisory, never blocking) on both forks | exit 1, exactly one line each — the permanently waived `com.apple.mobilenotes.SharingExtension` / `WFCreateNoteInput` finding, nothing else |
| `git diff` on `WFConditionalActionString` assignment lines | no `+`/`-` prefix on any — ownership compares byte-identical |
| `git diff tools/build_state_engine.py` inside `route_exit()` | empty — Create branch untouched |
| `B.KNOWN_SENTINEL_EXISTENCE_GATES == ()` | confirmed after Task 2 |
| `verify_sentinel_gates`, `verify_active_session_seed`, `verify_restore_gates`, `verify_compound_value_reads` unexempted on both forks | all clean |
| Guard sensitivity (full build, live_ice_redirect clear reverted) | `verify_active_session_seed()`'s assertion 3 raised `SystemExit`: "active_session is still written with the sentinel as a WHOLE CONTAINER at action(s) [216] …" |
| Guard sensitivity (direct call, earlier guard skipped) | `verify_sentinel_gates()` raised `SystemExit` naming 19 offenders, e.g. "action 684: dotted read 'active_session.id' hangs beneath 'active_session' …" |
| Post-restore rebuild | Sentient digest byte-identical; Dumb fork byte-identical to Task 1's committed state |
| No file deletions in either commit | `git diff --diff-filter=D --name-only HEAD~1 HEAD` empty for both `8125d25` and `43a2f4b` |
| No stray untracked files after either commit | `git status --short` empty |

## Known Stubs

None. No hardcoded empty value, placeholder string or unwired component was introduced.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern, or trust-boundary schema change was introduced. `T-12-12` through `T-12-17` are mitigated as planned: the condition-4 ownership compare at all four owner sites is verbatim-preserved (`T-12-12`); `restore_managed_settings()` stays reachable and gated numerically (`T-12-13`); no clear replaces a sub-dictionary with a string (`T-12-14`); the checker literal moved rather than being silently skipped (`T-12-15`); the sentinel can never collide with a real `session-<epoch>-<random>` ID (`T-12-16`); both documentation blocks were rewritten in the same commit as the change they describe, so no stale-defect claim survives (`T-12-17`). This plan installed no package (`T-12-SC`).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**Ready.** The container/leaf split for `active_session` is fully closed:

- Zero condition-100 existence gates and zero dotted reads stand over a sentinel-written key on either fork; `KNOWN_SENTINEL_EXISTENCE_GATES` is the empty tuple.
- `active_session` is never written or cleared as a whole container anywhere in either emitted fork; `open_pipeline()` writes four leaves, three sites clear `.id` only.
- The condition-4 ownership compare is byte-identical at all four owner sites — the V3 (ASVS) integrity control that stops a superseded CLOSE from writing state is unweakened.
- `docs/state_engine_self_check.py` asserts `active_session.id` and passes.
- Eleven checkers green, gate A clean on both forks, byte-idempotent rebuilds confirmed twice (once naturally, once via the sensitivity-demo restore).
- Both `verify_sentinel_gates()` and `verify_active_session_seed()`'s assertion 3 demonstrated to fire against synthetically reverted artifacts, not merely observed to pass.

**Carried forward, not a blocker:** Plan 12-05 owns `manifest_check.py` (excluded from this plan's eleven-checker chain pending re-signing) and the UAT document; device evidence for the exit-recording and active-session paths remains at rung 1 (file-level and build-guard evidence only), as flagged in the plan's `<flagged_assumptions>`.

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND
- `docs/state_engine_self_check.py` — FOUND
- `src/PROSOCHE-Dumb.xml` — FOUND
- `src/PROSOCHE-Sentient.xml` — FOUND
- Commit `8125d25` — FOUND in `git log`
- Commit `43a2f4b` — FOUND in `git log`
- Working tree clean after both task commits (`git status --short` empty)
- No file deletions in either commit (`git diff --diff-filter=D` empty for both)

---
*Phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session*
*Completed: 2026-08-17*
