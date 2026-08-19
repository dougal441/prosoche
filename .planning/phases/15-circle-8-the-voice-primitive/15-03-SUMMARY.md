---
phase: 15-circle-8-the-voice-primitive
plan: 03
subsystem: infra
tags: [shortcuts-plist-generator, python, ios-shortcuts, build-guards, state-machine, schema-migration]

# Dependency graph
requires:
  - phase: 15-circle-8-the-voice-primitive
    plan: 01
    provides: "mirror() (Circle 7) and voice() (Circle 8) as distinct functions, both reading voice_enabled through the identical read_value()/if_block() shape this plan normalises"
provides:
  - "voice_enabled normalised to the JSON numbers 1/0 at the bootstrap writer, via normalise_voice_enabled_seed() -- both writers (bootstrap and Toggle Voice) now agree by construction, not by unaudited boolean coercion (D-05)"
  - "schema_version bumped 4 -> 5 across the three coupled literals (SCHEMA_VERSION, SCHEMA_VERSION_PREVIOUS, SCHEMA_VERSION_ACCEPTED) in one commit, so an existing state.json carrying the old boolean form is rebuilt exactly once"
  - "verify_voice_enabled_seed() build guard: fails the build if voice_enabled is ever seeded as anything but a number, or read by anything but a numeric WFCondition==2/WFNumberValue==0 gate, including the vacuous-resolution failure direction -- armed on both forks"
affects: [15-04-voice-gates-and-dispatch-invariants, 15-05-build-notes-and-manifest]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Provenance-resolved seed retarget: normalise_voice_enabled_seed() walks back from the two setvariable actions writing the intermediate variable (VOICE_ENABLED_VARIABLE) to their producing gettext actions via WFInput.Value.OutputUUID, rather than matching gettext actions by their literal true/false content -- content matching alone would also hit the unrelated Contract Respected gettext pair"
    - "Three-coupled-literal schema bump: SCHEMA_VERSION, SCHEMA_VERSION_PREVIOUS and the SCHEMA_VERSION_ACCEPTED recognition tuple move in the same commit, per fix_state_rebind()'s own documented failure mode (the tuple fails LATE, one build downstream, if it's missed)"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml

key-decisions:
  - "D-05 implemented: bootstrap's voice_enabled writer retargeted from the unquoted boolean true/false to the numeric literals 1/0, matching Toggle Voice's existing writer -- this removes voice_enabled from axis 6's unaudited-boolean-coercion class entirely rather than establishing what \"true\" coerces to"
  - "Task 1's blocking checkpoint:decision was downgraded by the developer on 2026-08-18 to a recorded sequencing constraint -- BD-06-A1 Amendment 3 (no installed base to protect) already discharged the identical gate on the Phase 11 2->3 bump. Execution proceeded through all three tasks without pausing for a decision."
  - "verify_voice_enabled_seed()'s three negative-control mutations were run in-memory against a copy of the built actions list rather than by mutating and reverting the on-disk XML -- functionally identical evidence for a build-time guard, with no risk of leaving the repo in a mutated state"

patterns-established:
  - "In-memory negative control for a build guard: mutate a deepcopy of the loaded actions list, call the guard function directly, assert SystemExit, discard the copy -- no file write, no revert step, same evidentiary value as a mutate-rebuild-revert cycle for a guard whose failure mode is purely a build-time assertion over already-emitted actions"

requirements-completed: [CIRC-08, DIST-01]

coverage:
  - id: D1
    description: "voice_enabled holds a JSON number on every write path -- bootstrap and Control Room Toggle Voice agree by construction, not by coercion (D-05)"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "python3 -c \"...WFVariableName=='Voice Normalised'...\" -> ['0', '1']"
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
    human_judgment: true
    rationale: "CIRC-08 remains device-unproven per plan 15-02's own recorded verdict (axis-4 unfilled-picker defect, not discriminated at rung 2) -- a structurally green build must not be read as a behavioural pass on hardware. This plan closes the data-layer half of CIRC-08's gate only."
  - id: D2
    description: "An existing state.json carrying the old boolean form fails the validity gate and is rebuilt exactly once, because schema_version moved 4 -> 5 (D-05)"
    requirement: "DIST-01"
    verification:
      - kind: other
        ref: "python3 -c \"...re.search(r'\\\"schema_version\\\": (\\\\d+)', t).group(1)...\" -> 5"
        status: pass
      - kind: other
        ref: "python3 tools/build_state_engine.py run twice in succession, both exit 0 -- idempotence proof"
        status: pass
    human_judgment: false
  - id: D3
    description: "verify_voice_enabled_seed() build guard fails the build if voice_enabled is seeded or gated as anything but numeric, including the vacuous-resolution direction"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "negative control (a): revert one seed gettext literal to 'true' -- assertion (1) raises naming the non-numeric pair; mutation was in-memory only, never persisted"
        status: pass
      - kind: other
        ref: "negative control (b): change one voice_enabled reader's gate to condition 4 / string 'true' -- assertion (3) raises naming the unrecognised gate shape"
        status: pass
      - kind: other
        ref: "negative control (c): sever all 13 getvalueforkey sites reading the literal key 'voice_enabled' -- assertion (2) raises rather than the build exiting 0 with a vacuous pass"
        status: pass
      - kind: other
        ref: "grep -c 'verify_voice_enabled_seed' tools/build_sentient.py -> 2 (import + call site)"
        status: pass
    human_judgment: false
  - id: D4
    description: "The unrelated Contract Respected gettext pair is untouched by the voice_enabled retarget"
    verification:
      - kind: other
        ref: "python3 -c \"...gettext true/false count...\" -> 2, both feeding Contract Respected (down from 4)"
        status: pass
    human_judgment: false

duration: ~25min
completed: 2026-08-18
status: complete
---

# Phase 15 Plan 03: voice_enabled Type Normalisation and Schema Bump Summary

**Retargeted the bootstrap voice_enabled writer from unquoted boolean true/false to the numeric literals 1/0 (matching Toggle Voice's existing writer), bumped schema_version 4->5 across all three coupled literals in one commit, and added verify_voice_enabled_seed() -- a build guard measured to fail in all three directions including vacuous resolution -- armed on both forks.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-08-18T21:00:00+10:00 (approx, first file read)
- **Completed:** 2026-08-18T21:13:17+10:00
- **Tasks:** 3 completed
- **Files modified:** 4 (tools/build_state_engine.py, tools/build_sentient.py, src/PROSOCHE-Dumb.xml, src/PROSOCHE-Sentient.xml) plus this SUMMARY.md

## Accomplishments

- Recorded the schema-bump sequencing constraint (Task 1): build/install Phase 15 before the Pressure-accumulation UAT session, never after, and corrected the stale premise that a `.shortcut` re-install wipes `state.json` (it does not -- only the `schema_version` bump forces the rebuild)
- Added five module constants (`VOICE_ENABLED_KEY`/`VARIABLE`/`SEED_TRUE`/`SEED_FALSE`/`LEGACY`) and `normalise_voice_enabled_seed()` + `_voice_enabled_seed_gettexts()`, which retarget the two bootstrap gettext actions feeding the `Voice Normalised` intermediate variable from the legacy booleans `true`/`false` to the numbers `1`/`0`, resolved by walking back from the two `setvariable` actions writing that variable via `WFInput.Value.OutputUUID` -- never by content match, which would also hit the unrelated `Contract Respected` gettext pair (measured: exactly 2 `true`/`false` gettext actions remain, both feeding `Contract Respected`, down from 4)
- Moved the three coupled schema-version literals in the same commit: `SCHEMA_VERSION` `4`->`5`, `SCHEMA_VERSION_PREVIOUS` `3`->`4`, `SCHEMA_VERSION_ACCEPTED` recognition tuple gains `"5"`
- Added `verify_voice_enabled_seed()` (with `_voice_enabled_variables()`, resolved through `_read_variable_keys()` by provenance, never by a hardcoded variable-name literal), asserting: the seed pair is numeric; the resolved variable set is non-empty; every gate reading a resolved variable uses `WFCondition==2`/`WFNumberValue==0`; the set of matched gates is non-empty. Armed in `main()`'s verify block on Dumb and in `tools/build_sentient.py`'s import list and call site on Sentient
- Measured all three negative-control directions in-memory against a copy of the built actions (no file mutation, no revert needed): reverted seed literal, string-comparison gate, and severed provenance all raise correctly; outcomes recorded verbatim in the guard's own docstring
- Rebuilt both forks twice in succession (idempotence proof), both pass gate A clean (`--target-macos 26 --target-platform all`), and `docs/state_engine_self_check.py`, `docs/sequence_dispatch_check.py`, `docs/phase5_self_check.py`, `docs/router_ui_census.py` all exit 0

## Task Commits

Each task was committed atomically:

1. **Task 1: record the schema-bump sequencing constraint (downgraded from a blocking checkpoint)** - `2830168` (docs)
2. **Task 2: normalise the bootstrap voice_enabled seed to numeric, and move the three coupled schema literals** - `46d60ba` (feat)
3. **Task 3: verify_voice_enabled_seed() -- hold the type and the read shape at build time** - `78e6459` (feat)

**Plan metadata:** (this commit, pending)

## Files Created/Modified

- `tools/build_state_engine.py` -- `VOICE_ENABLED_KEY`/`VARIABLE`/`SEED_TRUE`/`SEED_FALSE`/`LEGACY` constants; `_voice_enabled_seed_gettexts()`, `normalise_voice_enabled_seed()`, `_voice_enabled_variables()`, `verify_voice_enabled_seed()` added; `SCHEMA_VERSION`/`SCHEMA_VERSION_PREVIOUS`/`SCHEMA_VERSION_ACCEPTED` bumped; both registered in `main()`'s seeder and verify blocks
- `tools/build_sentient.py` -- `verify_voice_enabled_seed` added to the import list (alphabetical position) and call site, beside `verify_panic_escape_seed()`
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` -- regenerated in place; `voice_enabled`'s two seed literals are now `1`/`0`; `schema_version` in the bootstrap template reads `5`
- `.planning/phases/15-circle-8-the-voice-primitive/15-03-SUMMARY.md` -- this file

## Decisions Made

- **D-05 implemented exactly as locked in `15-CONTEXT.md`.** No new product decisions were made in this plan.
- **Task 1's checkpoint was downgraded, not skipped.** The developer's 2026-08-18 downgrade (recorded in the plan's `<critical_project_rules>`) meant Task 1 became a plain recording task rather than a blocking gate; execution proceeded straight through to Task 2 as instructed, with the sequencing constraint and the re-install correction both written into this file.
- **In-memory negative controls, not mutate-and-revert.** `verify_voice_enabled_seed()`'s three negative-control mutations (Task 3) were run against a `copy.deepcopy()` of the loaded actions list via a standalone script, never written back to `src/PROSOCHE-Dumb.xml`. This is functionally identical evidence for a build-time guard (the guard only ever sees an in-memory `actions` list) and removes any risk of leaving the repository in a mutated state between measurement and revert.

## Deviations from Plan

None -- plan executed exactly as written, including its explicit non-goals (CIRC-08 remains device-unproven per plan 15-02's verdict; `docs/manifest_check.py` is left red per the plan's own standing constraint, re-confirmed still red at the end of this plan).

## Issues Encountered

None requiring a fix. One process note: the grep-based verification command in Task 1's `<verify>` block required its two matched substrings to each sit on a single line (grep does not match across a hard line wrap in prose); the sequencing-constraint prose was written with that in mind after an initial wrap caused the first verification attempt to fail, then passed once corrected.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- `voice_enabled` is numeric on every write path and guarded by `verify_voice_enabled_seed()` on both forks; CIRC-08's consent-gate data layer no longer rests on an unaudited boolean coercion.
- `docs/manifest_check.py` is red as expected (measured: `MANIFEST declares 2864203 bytes, src/PROSOCHE-Dumb.xml is 2780563 bytes`) and stays red until plan 15-05 re-signs both forks and re-derives the MANIFEST rows. This is not a defect in this plan's work.
- Plan 15-05's `docs/BUILD-NOTES.md` authoring should carry forward this plan's schema-bump sequencing constraint (see the `## Schema bump — sequencing constraint` section below) into the device UAT instrument, per Task 1's own instruction.
- No blockers for 15-04 or 15-05.

---
*Phase: 15-circle-8-the-voice-primitive*
*Completed: 2026-08-18*

## Schema bump — sequencing constraint

**Recorded 2026-08-18, Task 1 of this plan. This is a sequencing constraint, not a decision** —
the blocking `checkpoint:decision` that previously occupied this slot was downgraded by the
developer on 2026-08-18 because it was framed as destroying user data, and there are no users.
`docs/CAPABILITY-DECISIONS.md` BD-06-A1 Amendment 3 (the developer's own 2026-08-17 statement)
already answered the question it asked: PROSOCHĒ is a new, as-yet-undeployed product, the only
installs are the developer's own testing, and old `state.json` files are explicitly not a
consideration. That amendment discharged the identical gate on the 2 → 3 `schema_version` bump
in Phase 11, and it discharges this one the same way.

**The ordering rule.** Build and install Phase 15 BEFORE the Pressure-accumulation UAT session, never after. The `schema_version` 4 → 5 bump this plan carries (Task 2) wipes
`heat`, `gravity`, `pressure`, every rolling window, the session record, `exit_events` and every
`exit_stats[*].samples` on the developer's own iPhone at the first run of the new build. Measured
at planning time that fixture is close to empty — `07-UAT.md` observed `pressure: 0`,
`10-UAT.md` expects `pressure: 1` at the first interruption, and `.planning/STATE.md` still names
accumulating Pressure to >=2 as a step yet to be taken — so the wipe costs approximately nothing
**today**. The cost is entirely one of ordering and inverts once the accumulation session
happens: running the Pressure-accumulation UAT first and only then installing a Phase-15-bumped
build throws that session away and forces it to be repeated, and that session is the prerequisite
for roughly thirty queued tests across phases 06, 12 and 13.

**Correction to a stale premise.** Re-installing a `.shortcut` does **not** wipe `state.json` —
the two are separate files, and the shortcut re-install alone leaves accumulated state intact.
The `schema_version` bump is specifically and solely what forces the rebuild. An earlier draft of
this plan claimed the device "has to re-install for Phase 15 anyway" as though that made the wipe
incidental; it does not — the shortcut re-install and the state wipe are two independent events,
and only the schema bump causes the second one.

Plan 15-05 carries the same constraint into the device UAT instrument so whoever runs it sees the
ordering rule before touching the phone.

Execution reached Task 2 without pausing for a decision — this plan carries no decision
checkpoint and no blocking gate.

## Self-Check: PASSED

- FOUND: 2830168 (Task 1 commit)
- FOUND: 46d60ba (Task 2 commit)
- FOUND: 78e6459 (Task 3 commit)
- FOUND: tools/build_state_engine.py
- FOUND: tools/build_sentient.py
- FOUND: src/PROSOCHE-Dumb.xml
- FOUND: src/PROSOCHE-Sentient.xml
