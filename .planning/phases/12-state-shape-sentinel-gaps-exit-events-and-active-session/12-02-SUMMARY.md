---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
plan: 02
subsystem: infra
tags: [shortcuts, plist, state-json, build-guards, generator, active-session, sess-07, safe-01]

# Dependency graph
requires:
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-01"
    provides: "seeder+guard-sharing-one-constant convention proven end-to-end; schema_version bump to 4 already spent for this phase; seeder-ordering rule (before fix_state_rebind())"
provides:
  - "active_session seeded as a permanent four-leaf {id, started_at, declared_duration_seconds, intention} container in the bootstrap state.json template on both forks"
  - "ACTIVE_SESSION_SEED / ACTIVE_SESSION_ANCHOR module constants shared by seeder and guard"
  - "seed_active_session() -- replace-in-place seeder routed through _replace_in_token()"
  - "verify_active_session_seed() -- three-assertion guard, armed on both forks, with a self-dissolving deferral on assertion 3"
  - "PENDING_EXIT_ANCHOR re-pointed from the active_session line to the stable last_app line, closing a latent StopIteration on from-scratch regeneration"
affects: [12-03, 12-04, 12-05, active_session-gate-conversion, close_pipeline, restore_managed_settings]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Container/leaf seeder replaces an existing line in place (seed_settings_snapshot()'s mechanics), distinct from insert-after-anchor (seed_pending_exit()'s / seed_exit_events()'s mechanics) -- chosen because active_session already has a placeholder line to replace, not a gap to insert into"
    - "A guard's deferred assertion keys off a shared config constant (KNOWN_SENTINEL_EXISTENCE_GATES) rather than a literal skip, so a later plan emptying that constant arms the deferred assertion automatically"
    - "Guard sensitivity demonstrated by direct construction (calling the verifier against a pre-seed template) as well as by full-build neutralisation, restoring both source files via `git checkout --` afterward"

key-files:
  created: []
  modified:
    - "tools/build_state_engine.py"
    - "tools/build_sentient.py"
    - "src/PROSOCHE-Dumb.xml"
    - "src/PROSOCHE-Sentient.xml"

key-decisions:
  - "seed_active_session() replaces the existing \"active_session\": null, line in place, mirroring seed_settings_snapshot()'s SNAPSHOT_EMPTY replace mechanics -- not seed_pending_exit()'s insert-after-anchor, because active_session already occupies a line rather than being absent"
  - "Idempotency guard token is the collision-free '\"active_session\": {' substring, never the bare '\"active_session\"' substring, which already matches the un-seeded null line and would make the seeder a permanent no-op"
  - "PENDING_EXIT_ANCHOR re-pointed to \"last_app\": null, in the SAME commit as the seeder that destroys its former literal -- landing them separately would leave a from-scratch regeneration one StopIteration away from a bare, unmessaged crash"
  - "verify_active_session_seed()'s assertion 3 (no whole-container sentinel write) is deferred behind KNOWN_SENTINEL_EXISTENCE_GATES membership rather than skipped or omitted -- it is written now, dormant now, and arms itself automatically when a later plan (12-03) empties that constant"
  - "Guard sensitivity was demonstrated two ways: a direct call against the pre-seed template's actions (fast, no working-tree churn), and a full build with the seeder commented out and src/PROSOCHE-Dumb.xml temporarily reverted to its pre-seed content (matches the plan's literal instruction and Plan 12-01's precedent) -- both produced the identical SystemExit message"

patterns-established:
  - "Replace-in-place seeding for a key that already carries a placeholder value, versus insert-after-anchor for a key that is currently absent -- the two mechanics this file now demonstrates side by side (seed_active_session() vs seed_exit_events())"
  - "A guard whose full assertion set is not yet satisfiable stays fully written, with the unsatisfiable clause behind a shared-constant deferral -- never behind a skip, a pass, or a TODO"

requirements-completed: [SESS-07, SAFE-01]

coverage:
  - id: D1
    description: "The bootstrap state.json template declares active_session as a permanent four-leaf dictionary -- id, started_at, declared_duration_seconds, intention -- each seeded CLEARED_SENTINEL, on both forks"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "python3 -c '... _state_template + json.loads ... assert sess keys == {id, started_at, declared_duration_seconds, intention} and all values == CLEARED_SENTINEL' against src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml"
        status: pass
    human_judgment: false
  - id: D2
    description: "No seeded leaf is the empty string; the seed is the CLEARED_SENTINEL, never a fabricated value"
    requirement: "SAFE-01"
    verification:
      - kind: integration
        ref: "'' not in sess.values() assertion in Task 1's verify block; verify_active_session_seed() assertion 2 independently re-checks the same property with its own SystemExit"
        status: pass
    human_judgment: false
  - id: D3
    description: "PENDING_EXIT_ANCHOR no longer names a template line that seed_active_session() rewrites; a from-scratch regeneration finds the re-pointed anchor rather than raising StopIteration"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "B.PENDING_EXIT_ANCHOR != '\"active_session\": null,' and B.PENDING_EXIT_ANCHOR in the emitted template string, asserted in Task 1's verify block"
        status: pass
    human_judgment: false
  - id: D4
    description: "verify_active_session_seed() asserts the container shape against ACTIVE_SESSION_SEED on both forks and demonstrably fires against a reverted/malformed seed, naming the SESS-07 / SAFE-01 consequence"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "direct call against the pre-seed template's actions, and a full build with seed_active_session(actions) commented out against a reverted src/PROSOCHE-Dumb.xml -- both raised SystemExit with the identical message naming restore_managed_settings(\"Reloaded State\") and SESS-07 / SAFE-01; then restored and rebuilt clean"
        status: pass
    human_judgment: false
  - id: D5
    description: "Both forks rebuild byte-idempotently and pass gate A clean after the seed lands; KNOWN_SENTINEL_EXISTENCE_GATES still holds its pre-existing (\"active_session\",) entry unchanged"
    requirement: "SESS-07"
    verification:
      - kind: integration
        ref: "python3 docs/phase6_self_check.py (double-build byte digest compare); python3 docs/state_engine_self_check.py; python3 docs/sentient_core_check.py; python3 docs/sentient_audit_check.py; validate-shortcut on both forks --target-macos 26 --target-platform all; B.KNOWN_SENTINEL_EXISTENCE_GATES == (\"active_session\",) asserted"
        status: pass
    human_judgment: false

# Metrics
duration: 20 min
completed: 2026-08-17
status: complete
---

# Phase 12 Plan 02: active_session permanent four-leaf container Summary

**The bootstrap `state.json` template now declares `active_session` as a permanent `{id, started_at, declared_duration_seconds, intention}` sentinel container, guarded by a new `verify_active_session_seed()` armed on both forks and demonstrated to fire, with `PENDING_EXIT_ANCHOR` re-pointed off the line this seeder rewrites -- closing the SESS-07 / SAFE-01 gap ahead of the CLOSE-path gate conversion Plan 12-03 will build on it.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- **Closed the structural half of SESS-07 / SAFE-01.** `restore_managed_settings("Reloaded State")` -- the only path that restores brightness and volume after a Dimming or Silence primitive -- sits inside three nested `active_session`-derived arms in `close_pipeline()`. Every `.id` / `.started_at` / `.declared_duration_seconds` dotted read on that path now runs against a fully-declared four-leaf sentinel container instead of a bare JSON `null` parent, so none of them can raise "could not evaluate the key path" on a fresh state file.
- **Closed a latent `StopIteration` before it could ever fire.** `PENDING_EXIT_ANCHOR`'s literal was exactly the line `seed_active_session()` now rewrites. Re-pointed in the same commit to the stable `"last_app": null,` line, so a from-scratch regeneration finds the anchor instead of crashing with no message.
- **Demonstrated the new guard fires, twice.** A direct call against the pre-seed template's actions, and a full build with the seeder neutralised and `src/PROSOCHE-Dumb.xml` reverted to its pre-seed content -- both produced the identical `SystemExit` naming `restore_managed_settings` and SESS-07 / SAFE-01, recorded verbatim in the Task 2 commit body.
- **Left the gate-semantics half honestly open, not silently.** Assertion 3 (no whole-container sentinel write) is written now and deferred behind `KNOWN_SENTINEL_EXISTENCE_GATES` membership -- it will arm itself automatically the moment Plan 12-03 empties that constant. `KNOWN_SENTINEL_EXISTENCE_GATES` itself is left untouched at `("active_session",)`, exactly as the plan required.

## Task Commits

Each task was committed atomically:

1. **Task 1: Seed `active_session` as a permanent four-leaf container, re-point `PENDING_EXIT_ANCHOR`** -- `0c44160` (feat)
2. **Task 2: `verify_active_session_seed()` build guard, armed on both forks and shown to fire** -- `9ccec46` (fix)

## Files Created/Modified

- `tools/build_state_engine.py` -- added `ACTIVE_SESSION_SEED`, `ACTIVE_SESSION_ANCHOR`, `seed_active_session()`, `verify_active_session_seed()`; re-pointed `PENDING_EXIT_ANCHOR`; registered both new symbols in `main()` (seeder before `fix_state_rebind()`, guard in the verify chain alongside `verify_pending_exit_seed`/`verify_exit_events_seed`).
- `tools/build_sentient.py` -- imported and called `verify_active_session_seed`, alongside the fork's other inherited-invariant guards.
- `src/PROSOCHE-Dumb.xml` -- regenerated Core fork carrying the seeded four-leaf `active_session` container.
- `src/PROSOCHE-Sentient.xml` -- regenerated Aware fork inheriting the same seeded template.

## Decisions Made

- **Replace-in-place, not insert-after-anchor.** `active_session` already occupies the line `"active_session": null,`; `seed_active_session()` uses `seed_settings_snapshot()`'s `SNAPSHOT_EMPTY`-replace mechanics rather than `seed_pending_exit()`'s insert form, because there is a line to replace, not a gap to insert into.
- **Idempotency token is `'"active_session": {'`, not `'"active_session"'`.** The bare substring already matches the un-seeded `null` line and would make the seeder a permanent no-op.
- **`PENDING_EXIT_ANCHOR` re-pointed in the same commit as the seeder that destroys its former literal.** `seed_pending_exit()` early-returns today (`pending_exit` is already in the committed template), so the stale anchor is currently dormant -- but landing the re-point separately would leave a from-scratch regeneration one `StopIteration` away from a bare, unmessaged crash, per the plan's explicit warning.
- **Assertion 3 deferred behind a shared constant, never a literal skip.** `KNOWN_SENTINEL_EXISTENCE_GATES` membership gates whether the "no whole-container sentinel write" check runs; the assertion is fully written and will fire automatically once Plan 12-03 converts the three container clears and empties that constant.
- **Guard sensitivity demonstrated two ways.** A direct call against the pre-seed template's actions confirmed the exact failure mode with zero working-tree churn; a full build with the seeder commented out and `src/PROSOCHE-Dumb.xml` reverted to commit `930b762`'s content matched the plan's literal instruction and Plan 12-01's precedent. Both produced the identical message. Both source files were restored via `git checkout --` to their Task-1-committed state before the final clean rebuild, and the Sentient digest (`ca26fe89...`) matched byte for byte before and after.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. No guard fired unexpectedly, no build aborted for an unplanned reason, no fix-attempt limit approached. The guard-sensitivity demonstration's temporary `git checkout --` reverts (scoped to the two files this plan modifies) and the temporary source-comment-out in `main()` were both restored before the final commit, and `phase6_self_check.py`'s byte-idempotency proof plus the matching pre/post digest confirm no residue survived.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` (D-01 provenance gate) | exit 0, re-run before every builder invocation |
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, digest `ca26fe896f5baa01a1997b4ee51ad266dc5b2a348174d10b61002eca27cd3915` |
| Emitted template, Core fork | `active_session == {"id": "null", "started_at": "null", "declared_duration_seconds": "null", "intention": "null"}` |
| Emitted template, Aware fork | same four-leaf assertion holds -- the fork inherited the seed |
| `B.PENDING_EXIT_ANCHOR` | no longer `'"active_session": null,'`; new anchor literal present in the emitted template |
| `B.KNOWN_SENTINEL_EXISTENCE_GATES` | unchanged at `("active_session",)` |
| `grep -n 'SNAPSHOT_EMPTY\|PANIC_ESCAPE_ANCHOR'` | both constant definitions unchanged from HEAD |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/phase6_self_check.py` (double-build byte-idempotency) | exit 0 -- proves the `'"active_session": {'` early-return makes `seed_active_session()` idempotent |
| `python3 docs/sentient_core_check.py` | exit 0 |
| `python3 docs/sentient_audit_check.py` | exit 0 |
| `verify_active_session_seed` count in `tools/build_sentient.py` (comments filtered) | 2 (import + call) |
| No bare `assert` inside `verify_active_session_seed()`'s body | confirmed via `inspect.getsource` scan |
| `KNOWN_SENTINEL_EXISTENCE_GATES` referenced inside `verify_active_session_seed()`'s body | confirmed |
| Gate A, Core fork (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate A, Aware fork | `Validation passed.`, exit 0 |
| Guard sensitivity (direct call) | `verify_active_session_seed()` raised `SystemExit` against the pre-seed template's actions, naming `restore_managed_settings` and SESS-07 / SAFE-01 |
| Guard sensitivity (full build) | seeder commented out + `src/PROSOCHE-Dumb.xml` reverted to `930b762` -> `python3 tools/build_state_engine.py` exited 1 with the identical message before `SOURCE.write_bytes()`; both files restored via `git checkout --`, rebuilt clean, Sentient digest byte-identical to the pre-demonstration build |
| `attachmentsByRange` integrity | all four offsets still land on `U+FFFC` -- enforced by `_replace_in_token()`, a clean build is the proof |
| No file deletions in either commit | `git diff --diff-filter=D --name-only HEAD~1 HEAD` empty for both `0c44160` and `9ccec46` |

## Known Stubs

None. No hardcoded empty value, placeholder string or unwired component was introduced.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or trust-boundary schema change was introduced. `T-12-07` through `T-12-11` are mitigated as planned: all four `active_session` leaves seeded with the sentinel closes the denial-of-service risk of a mid-run hard error before the restore (`T-12-07`); `CLEARED_SENTINEL`, never `""`, closes the sentinel-vs-real-value confusion axis (`T-12-08`); `PENDING_EXIT_ANCHOR` re-pointed in the same commit as the seeder that destroys its former literal closes the latent `StopIteration` (`T-12-09`); seeder and guard share `ACTIVE_SESSION_SEED` (`T-12-10`); the deferral is keyed on `KNOWN_SENTINEL_EXISTENCE_GATES` membership, not a literal skip (`T-12-11`). This plan installed no package (`T-12-SC`).

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

**Ready.** The seed half of the container/leaf split is complete on both forks:

- `active_session` is a permanent four-leaf sentinel container; every dotted read on the `close_pipeline()` restore path is now structurally incapable of raising.
- `verify_active_session_seed()` is armed on both forks with a self-dissolving deferral on assertion 3, keyed on `KNOWN_SENTINEL_EXISTENCE_GATES`.
- `PENDING_EXIT_ANCHOR` is re-pointed and stable; no seeder in this phase rewrites the line it now names.
- `KNOWN_SENTINEL_EXISTENCE_GATES` is untouched at `("active_session",)`, exactly as scoped -- the gate conversion (`record_exit_and_route()`, `persist_contract()`'s 11 renders, `close_pipeline()`'s entry/reload gates, `route_exit()`'s Create branch, `open_pipeline()`'s container-write-to-leaf-writes conversion, and the three container clears) is Plan 12-03's business, unblocked by this plan's landing.

**Carried forward, not a blocker:** assertion 3's deferral will arm automatically the moment `KNOWN_SENTINEL_EXISTENCE_GATES` is emptied by the gate conversion -- no follow-up action needed from this plan.

## Self-Check: PASSED

- `tools/build_state_engine.py` -- FOUND
- `tools/build_sentient.py` -- FOUND
- `src/PROSOCHE-Dumb.xml` -- FOUND
- `src/PROSOCHE-Sentient.xml` -- FOUND
- Commit `0c44160` -- FOUND in `git log`
- Commit `9ccec46` -- FOUND in `git log`
- Working tree clean after both task commits (`git status --short` empty)
- No file deletions in either commit (`git diff --diff-filter=D` empty for both)

---
*Phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session*
*Completed: 2026-08-17*
