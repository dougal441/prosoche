---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
plan: 04
subsystem: infra
tags: [shortcuts, plist, state-json, build-guards, generator, exit-routing, create-exit, gate-semantics, exit-01, exit-02, state-12]

# Dependency graph
requires:
  - phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
    plan: "12-03"
    provides: "active_session leaf-gated everywhere on both forks; KNOWN_SENTINEL_EXISTENCE_GATES emptied to ()"
provides:
  - "profile_snapshot.create_target_url seeded as a sentinel leaf, closing the third key nobody named: route_exit()'s Create branch's dotted read of it from Reloaded State"
  - "route_exit()'s Create branch's state-read gate converted from condition-100 (has any value) to condition-5 (string is not CLEARED_SENTINEL), per Task 1's checkpoint decision option-a"
  - "STATE_READ_SOURCE_VARIABLES = ('State', 'Reloaded State'), the named filter that lets verify_state_seed()'s scan generalise by dictionary identity rather than key root"
  - "STATE_SEED_COMPOSITE_PREFIXES = ('exit_stats.',), the named tolerance for the six legitimate exit_stats.<type>.<field> composite reads"
  - "verify_state_seed() generalised from settings_snapshot-rooted keys to every literal State/Reloaded State read, reporting zero missing keys on both forks"
  - "verify_panic_escape_seed()'s docstring note (that verify_state_seed() did not cover panic_escape_enabled) corrected to historical"
affects: [12-05, route_exit, verify_state_seed, verify_panic_escape_seed, exit-routing-create-branch, state-shape-build-guards]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Checkpoint decision recorded as a single-line marker file in the phase directory (.create-target-url-option), read by both the implementing task's verify block and a later task's verify block, so the decision cannot silently drift between the two"
    - "Sentinel-seeded leaf plus a condition-5 set/unset gate for a single dotted-read defect, reusing complete_pending_exit()'s exact idiom rather than inventing a new one -- zero new runtime semantics introduced"
    - "Two condition codes coexisting in one control-flow branch, distinguished by an inline comment naming WHY they differ (state-read leaf vs. transient user input), so a future 'harmonisation' pass does not collapse them incorrectly"
    - "Read-side build guard generalised by SOURCE VARIABLE IDENTITY (WFInput.Value.VariableName) rather than by key-root filter -- the filter that scoped a guard to one key family was, incidentally, also scoping it to reads of the right dictionary; separating the two axes explicitly (STATE_READ_SOURCE_VARIABLES) is what makes a bare 'delete the old filter' safe instead of a 74-key build failure"
    - "Composite-key tolerance widened by NAMED PREFIX rather than deleted outright, so a provably-safe runtime-resolved composite (exit_stats.<type>.<field>, every possible middle-segment value already seeded) does not trip a guard whose job is to catch genuinely unresolvable reads"
    - "Guard sensitivity demonstrated fully in-memory: a deep-in-place mutation of a copy of the template token, never written to disk, avoids the two-rebuild revert-and-restore cycle 12-03's demonstration needed because the synthetic defect never touches a generator function or a committed source file"
  key-files:
    created: []
    modified:
      - "tools/build_state_engine.py"
      - "src/PROSOCHE-Dumb.xml"
      - "src/PROSOCHE-Sentient.xml"
      - "docs/BUILD-NOTES.md"

key-decisions:
  - "Task 1 checkpoint resolved option-a (sentinel seed plus a condition-5 leaf gate) -- the planner's own recommendation, auto-selected under the orchestrator's autonomous run per the gate='blocking' (not 'blocking-human') carve-out, and independently re-confirmed sound by the plan-checker's re-verification pass against the live tree before this plan was handed off for execution."
  - "The Create branch's SECOND gate (over the Ask action's Provided Input) was deliberately left at condition 100 -- it tests a transient user input whose unset representation is genuinely empty, not a sentinel-seeded state leaf, so has-any-value is the correct test there. An inline comment at the converted first gate names why the two codes now differ, specifically to prevent a future pass from 'harmonising' them incorrectly."
  - "verify_state_seed()'s generalisation deletes the key-root filter but ADDS a source-variable filter rather than doing a bare deletion -- 12-RESEARCH.md and 12-PATTERNS.md both described the change as 'a deletion', and the plan's own executor-facing correction (independently measured this session) is what prevented implementing that incomplete framing, which would have failed the build on 74 legitimate Config/Previous Session reads."
  - "The composite-key branch is widened by a named prefix tolerance (STATE_SEED_COMPOSITE_PREFIXES), not deleted -- an unconstrained composite read of State/Reloaded State remains a build error, and only the six measured exit_stats.<type>.<field> reads (provably safe because every possible <type> value is seeded) are exempted."
  - "The guard-sensitivity demonstration mutates an in-memory copy of the template token and never writes to disk -- unlike 12-03's demonstration (which had to revert a generator function, rebuild, observe, then restore and rebuild again), this task's synthetic defect (a missing seeded key) can be constructed and observed without touching any committed file, so no restore-and-rebuild cycle was needed."

patterns-established:
  - "A read-side state-shape build guard scopes by SOURCE VARIABLE IDENTITY, not key root, once more than one key family shares the same guard -- key-root filters conflate 'which key family' with 'which dictionary', and the two axes must be separated explicitly the moment a second key family needs the same guard."
  - "A checkpoint decision that changes an emitted gate's runtime semantics is recorded in three independent places (a phase-directory marker file consumed by a later verify block, the commit body, and BUILD-NOTES.md), so the decision is both machine-checkable and human-auditable without needing to reconstruct it from the diff."

requirements-completed: [EXIT-01, EXIT-02, STATE-12]

coverage:
  - id: D1
    description: "profile_snapshot.create_target_url resolves in the bootstrap seed, so route_exit()'s Create branch no longer performs a dotted read of a leaf the bootstrap does not establish"
    requirement: "EXIT-01"
    verification:
      - kind: integration
        ref: "verify_state_seed(actions) (generalised, Task 3) resolves profile_snapshot.create_target_url against both src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml with zero missing keys"
        status: pass
    human_judgment: false
  - id: D2
    description: "The Create branch's set/unset gate reads FALSE on a clean install, so a fresh user is asked where Create should open rather than having openurl invoked on a placeholder value"
    requirement: "EXIT-02"
    verification:
      - kind: integration
        ref: "Task 2's verify block: exactly 4 mode-0 conditionals test Create Target URL per fork (2 per route_exit() render), 2 carry condition 5 and 2 carry condition 100, resolved via _tested_variable(); emitted profile_snapshot.create_target_url == CLEARED_SENTINEL on both forks"
        status: pass
    human_judgment: false
  - id: D3
    description: "verify_state_seed()'s read-side scan covers every literal dictionary key read from State or Reloaded State, not only settings_snapshot-rooted ones"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "B.STATE_READ_SOURCE_VARIABLES == ('State', 'Reloaded State'); verify_state_seed(actions) clean on both forks; an independent re-implementation of the scan in the verify block reports an empty missing list against the regenerated Core fork"
        status: pass
    human_judgment: false
  - id: D4
    description: "The generalised scan excludes Config and Previous Session reads by named constant, and tolerates only the named exit_stats composites"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "STATE_READ_SOURCE_VARIABLES filters by dictionary identity (measured: 30 literal/23 composite Config reads, 3 Previous Session reads excluded); STATE_SEED_COMPOSITE_PREFIXES == ('exit_stats.',) tolerates exactly the six measured exit_stats composites"
        status: pass
    human_judgment: false
  - id: D5
    description: "The generalised guard reports zero missing keys against both regenerated forks -- the same set the pre-phase sweep reported as eight unresolved key/source rows"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "verify_state_seed(actions) raises nothing on either fork; independent sweep confirms empty missing list"
        status: pass
    human_judgment: false
  - id: D6
    description: "The generalised guard has teeth, not merely a clean observation -- demonstrated to fire against a synthetic mutation it was structurally blind to before this change"
    requirement: "STATE-12"
    verification:
      - kind: integration
        ref: "in-memory strip of the seeded exit_events line from a copy of the template token raised SystemExit naming exit_events in the missing list; no committed file was mutated, confirmed by git diff --stat empty on both src/PROSOCHE-*.xml after a post-demo rebuild"
        status: pass
    human_judgment: false
  - id: D7
    description: "read_value() of a JSON-null leaf is never exercised by the shipped artifact under the chosen option, so no untested Shortcuts coercion semantic is relied on"
    requirement: "EXIT-02"
    verification:
      - kind: backstop
        ref: "Option A was chosen (sentinel seed, condition-5 gate) -- the seed is never JSON null, so read_value() of a null leaf is structurally never exercised by any Create-branch gate on the shipped artifact"
        status: pass
    human_judgment: false
  - id: D8
    description: "The Create Owner ID condition-4 ownership compare and its WFConditionalActionString idiom are unmodified by the gate conversion"
    requirement: "EXIT-01"
    verification:
      - kind: integration
        ref: "git diff HEAD~3 HEAD -- tools/build_state_engine.py shows no +/- line touching the Create Owner ID compare"
        status: pass
    human_judgment: false

# Metrics
duration: ~15 min
completed: 2026-08-17
status: complete
---

# Phase 12 Plan 04: state-shape sentinel gap — profile_snapshot.create_target_url and the generalised read-side guard Summary

**Closed the third key nobody named (a dotted read of `profile_snapshot.create_target_url` on `route_exit()`'s Create branch that hard-errors on a clean install), then generalised `verify_state_seed()`'s read-side scan from `settings_snapshot`-rooted keys to every literal `State`/`Reloaded State` read — converting the whole state-shape defect family into a permanent build error.**

## Performance

- **Duration:** ~15 min
- **Tasks:** 3 (1 checkpoint:decision, 2 auto)
- **Files modified:** 4 (tools/build_state_engine.py, src/PROSOCHE-Dumb.xml, src/PROSOCHE-Sentient.xml, docs/BUILD-NOTES.md)

## Accomplishments

- **Resolved Task 1's blocking checkpoint decision** (`gate="blocking"`) to `option-a` — sentinel seed plus a condition-5 leaf gate, the planner's own recommendation (PD-2), auto-selected under the orchestrator's autonomous run per the `blocking`/`blocking-human` carve-out and independently re-confirmed by the plan-checker's own re-verification pass. Recorded in three places: the phase-directory marker file, the commit body, and `docs/BUILD-NOTES.md` §26.
- **Seeded `profile_snapshot.create_target_url`.** `CREATE_TARGET_URL_SEED = CLEARED_SENTINEL`; `seed_create_target_url()` inserts the leaf immediately before `profile_snapshot`'s trailing, comma-less final key (`"note_content_hash": null`), keeping the object valid JSON without a second comma edit. Registered in `main()` before `fix_state_rebind()`, alongside `seed_exit_events()`/`seed_active_session()`.
- **Converted route_exit()'s Create branch's first gate** from `if_block("Create Target URL", 100)` to `if_block("Create Target URL", 5, string=CLEARED_SENTINEL)` — the same set/unset idiom `complete_pending_exit()` already uses for `pending_exit.type`. The second gate (over the Ask action's `Provided Input`) is left at condition 100, untouched, with an inline comment naming why the two condition codes in one branch now differ.
- **Generalised `verify_state_seed()`'s read-side scan.** Corrected the incomplete "just delete the filter" framing both `12-RESEARCH.md` and `12-PATTERNS.md` used: the old `settings_snapshot`-root filter was doing double duty as a dictionary-identity filter. Replaced it with `STATE_READ_SOURCE_VARIABLES = ("State", "Reloaded State")`, filtering by the measured `WFInput.Value.VariableName` accessor path, and added `STATE_SEED_COMPOSITE_PREFIXES = ("exit_stats.",)` to tolerate exactly the six legitimate runtime-resolved composite reads `complete_pending_exit()`/`select_exit()` build.
- **Corrected `verify_panic_escape_seed()`'s docstring**, which previously recorded (accurately, at the time) that `verify_state_seed()` did not cover `panic_escape_enabled`; that note is now historical, with the still-load-bearing two assertions (no dotted read, only numeric gates) preserved.
- **Demonstrated the generalised guard has teeth**, entirely in-memory: stripped the seeded `"exit_events": []` line from a copy of the template token (never written to disk) and confirmed `verify_state_seed()` raised `SystemExit` naming `exit_events` in the missing list — a key the pre-generalisation scan was structurally blind to.

## Task Commits

Each task was committed atomically:

1. **Task 1: Decide the seed value and gate shape for profile_snapshot.create_target_url** — `5dc86e8` (docs, checkpoint resolution recorded)
2. **Task 2: Implement the chosen create_target_url option** — `949382b` (feat)
3. **Task 3: Generalise verify_state_seed()'s read-side scan** — `5c484d7` (fix)

## Files Created/Modified

- `tools/build_state_engine.py` — `CREATE_TARGET_URL_SEED`, `CREATE_TARGET_URL_ANCHOR`, `seed_create_target_url()` added; `route_exit()`'s Create branch first gate converted to condition 5; `STATE_READ_SOURCE_VARIABLES`, `STATE_SEED_COMPOSITE_PREFIXES` added; `verify_state_seed()` generalised (docstring, scan, error message); `verify_panic_escape_seed()`'s docstring note corrected to historical.
- `src/PROSOCHE-Dumb.xml` — regenerated Core fork, `create_target_url` leaf present, Create-branch gate converted.
- `src/PROSOCHE-Sentient.xml` — regenerated Aware fork, inherits the same change.
- `docs/BUILD-NOTES.md` — new §26 recording the checkpoint decision, why option A over B/C, the implementation, and the verified evidence.

## Decisions Made

- **Option A selected at Task 1's checkpoint.** See `key-decisions` above and `docs/BUILD-NOTES.md` §26 for the full comparison against options B and C.
- **The Create branch's second gate stays condition 100.** It tests the Ask action's `Provided Input` (a transient user input whose unset representation is genuinely empty), not a sentinel-seeded state leaf — converting it too would have been a regression, not a fix. Recorded inline at the site.
- **`verify_state_seed()`'s generalisation adds a source-variable filter rather than performing a bare deletion.** The plan's own executor-facing correction (measured this session against the live tree: 141+6 State, 44 Reloaded State, 30+23 Config, 3 Previous Session reads) is what prevented the incomplete "just delete the filter" framing from breaking the build on 74 foreign-dictionary reads.
- **The composite-key branch is widened by named prefix, not deleted.** `STATE_SEED_COMPOSITE_PREFIXES` tolerates exactly the six measured `exit_stats.<type>.<field>` reads; any other unresolvable composite read of `State`/`Reloaded State` remains a build error.

## Deviations from Plan

None — plan executed exactly as written, including the executor-facing correction the plan itself called out (generalisation is filter-and-add, not bare deletion) and the guard-sensitivity demonstration technique (in-memory, no restore-and-rebuild cycle needed since the synthetic mutation never touched a generator function or committed file).

## Issues Encountered

None. No guard fired unexpectedly during normal (non-sensitivity-demo) rebuilds, no fix-attempt limit approached, no unplanned working-tree residue.

## Verification Results

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` (D-01 provenance gate) | exit 0, re-checked before every builder invocation |
| `python3 tools/build_state_engine.py` | exit 0, all three tasks |
| `python3 tools/build_sentient.py` | exit 0 |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/phase6_self_check.py` | `phase6 self-check: passed` |
| Task 2 structural verify (4 Create Target URL gates per fork, 2×cond-5 + 2×cond-100, `profile_snapshot.create_target_url == CLEARED_SENTINEL`) | passed on both forks |
| Task 3: `B.STATE_READ_SOURCE_VARIABLES == ('State', 'Reloaded State')`, `'exit_stats.' in B.STATE_SEED_COMPOSITE_PREFIXES` | confirmed |
| `verify_state_seed`, `verify_sentinel_gates`, `verify_active_session_seed`, `verify_exit_events_seed`, `verify_restore_gates`, `verify_compound_value_reads` | all clean, both forks |
| Independent re-implementation of the read-side sweep (verify block, not calling the guard) | empty missing list against the regenerated Core fork |
| `python3 docs/state_engine_self_check.py`, `phase5_self_check.py`, `phase6_self_check.py`, `phase7_self_check.py`, `phase9_self_check.py`, `sentient_audit_check.py`, `sentient_core_check.py`, `environmental_restore_check.py`, `router_ui_census.py`, `sequence_dispatch_check.py`, `note_identity_check.py` | all eleven exit 0 |
| `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| Guard sensitivity (in-memory, `exit_events` line stripped from a copy of the template token) | `SystemExit`: "bootstrap state.json does not establish every state key that is read (Get Dictionary Value on a missing key is a HARD RUNTIME ERROR, so a condition-100 guard cannot protect the read): exit_events" |
| Post-demo rebuild vs. committed forks | `git diff --stat` empty on both `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` — no file was ever mutated by the demonstration |
| `git diff` on `Create Owner ID` condition-4 compare / `WFConditionalActionString` lines | empty across all three task commits |
| No file deletions in any commit | `git diff --diff-filter=D --name-only` empty for `5dc86e8`, `949382b`, `5c484d7` |
| No stray untracked files after any commit | `git status --short` empty after each |

## Known Stubs

None. No hardcoded empty value, placeholder string or unwired component was introduced.

## Threat Flags

None. All threats named in this plan's `<threat_model>` are addressed by the work above: T-12-18 (Create-branch hard error) mitigated by the seed; T-12-19 (openurl on a placeholder) mitigated by choosing option A, avoiding the untested-coercion risk option B carried; T-12-20 (future unseeded reads) mitigated by the permanent generalised guard; T-12-21 (naive generalisation failing on 74 legitimate reads) mitigated by `STATE_READ_SOURCE_VARIABLES`; T-12-22 (undocumented one-way decision) mitigated by the three-place record; T-12-23 (unnamed filter smuggled in) mitigated by every exclusion being a named, commented constant plus an independent verify-block re-implementation. T-12-SC (package legitimacy) is n/a — no package installed, matching the plan's own audit.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**Ready.** All three known state-shape sentinel gaps this phase was chartered to close (`exit_events`, `active_session`, `profile_snapshot.create_target_url`) are now closed, and the closing mechanism (`verify_state_seed()`) is generalised to catch any future instance of the same class permanently:

- Zero missing keys reported by the generalised `verify_state_seed()` on either fork, cross-checked by an independent re-implementation of the scan.
- `route_exit()`'s Create branch cannot reach a hard "could not evaluate the key path" error on a clean install; its state-read gate correctly distinguishes cleared from captured.
- The generalisation is demonstrated to have teeth, not merely observed to pass.
- Eleven checkers green, gate A clean on both forks, byte-idempotent rebuilds confirmed (including after the in-memory sensitivity demonstration).

**Carried forward, not a blocker:** Plan 12-05 owns `manifest_check.py` (excluded from this plan's eleven-checker chain pending re-signing) and the UAT document; device evidence for the Create exit route and the generalised guard's real-world behaviour remains at rung 1 (file-level and build-guard evidence only), consistent with this plan's `<flagged_assumptions>` A2 (dotted-read-on-missing-final-segment inference) and the phase's standing DIST-03 blocker (no connected iPhone).

## Self-Check: PASSED

- `tools/build_state_engine.py` — FOUND
- `src/PROSOCHE-Dumb.xml` — FOUND
- `src/PROSOCHE-Sentient.xml` — FOUND
- `docs/BUILD-NOTES.md` — FOUND
- `.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/.create-target-url-option` — FOUND, contains `option-a`
- Commit `5dc86e8` — FOUND in `git log`
- Commit `949382b` — FOUND in `git log`
- Commit `5c484d7` — FOUND in `git log`
- Working tree clean after all three task commits (`git status --short` empty)
- No file deletions in any commit (`git diff --diff-filter=D` empty for all three)

---
*Phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session*
*Completed: 2026-08-17*
