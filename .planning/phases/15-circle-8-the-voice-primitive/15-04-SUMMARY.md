---
phase: 15-circle-8-the-voice-primitive
plan: 04
subsystem: infra
tags: [shortcuts-plist-generator, python, ios-shortcuts, build-guards, static-checker, state-machine]

# Dependency graph
requires:
  - phase: 15-circle-8-the-voice-primitive
    plan: 01
    provides: "mirror() (Circle 7, shows only) and voice() (Circle 8, shows and speaks once, consent-gated) as distinct dispatch receivers, plus verify_speaktext_placement()'s enclosing_groups()-based branch-span resolution pattern this plan's guards copy"
  - phase: 15-circle-8-the-voice-primitive
    plan: 03
    provides: "VOICE_ENABLED_KEY, _voice_enabled_variables() (provenance-resolved consent-variable set) and the numeric voice_enabled seed/gate shape verify_voice_gates() asserts against"
provides:
  - "verify_voice_gates(actions): fails the build if any is.workflow.actions.speaktext site is reachable without BOTH the provenance-resolved voice_enabled > 0 consent gate and the once-per-run 'Spoken This Run' gate enclosing it -- armed on both forks"
  - "verify_voice_path_volume_silence(actions): fails the build if any is.workflow.actions.setvolume action lies inside a 'Loud Mirror' (Circle 8) dispatch branch span -- armed on both forks"
  - "docs/sequence_dispatch_check.py branch_bodies() / action_equal_pairs() / a fifth require(): fails the checker if two distinct sequence-entry names resolve to action-equal (UUID/GroupingIdentifier/OutputUUID-normalised) dispatch branch bodies -- the general form of the defect that let 'Mirror' and 'Loud Mirror' dispatch the identical function for four phases"
affects: [15-05-build-notes-and-manifest]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-gate enclosure guard: verify_voice_gates() computes enclosing_groups(actions) once and asserts a speech site's enclosing-group tuple intersects BOTH a provenance-resolved gate-shape set and a literal-name gate-shape set, rather than one flat allowlist -- the two roles (consent, once-per-run) are structurally distinct properties, not two instances of the same check"
    - "Branch-span volume-silence guard: verify_voice_path_volume_silence() reuses verify_speaktext_placement()'s per-site condition-code resolution (never a hardcoded strategy filter) to locate 'Loud Mirror' branch spans, then intersects enclosing_groups() against a resolved 'writer' action set (setvolume) instead of a resolved 'consent' set -- same enclosure machinery, opposite direction of the search"
    - "Structural branch-body comparison: docs/sequence_dispatch_check.py's branch_bodies() locates each dispatch branch's own action span by walking forward from its mode-0 conditional to the matching mode-2 endpoint sharing its GroupingIdentifier (new _branch_end() helper, no fixed action count assumed), then normalise_body() recursively strips every UUID/GroupingIdentifier/OutputUUID before two branches are compared for equality -- turns 'two renderings of the same behaviour' into byte-identical JSON and leaves two genuinely different behaviours genuinely different"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - docs/sequence_dispatch_check.py

key-decisions:
  - "verify_voice_gates() resolves its once-per-run gate ('Spoken This Run') by a NAMED LITERAL CONSTANT (SPOKEN_THIS_RUN_VARIABLE), not by provenance -- unlike the consent gate, this variable is never written to a state.json dictionary key; it is a run-scoped Shortcuts variable with no provenance chain to resolve against, so a named-literal constant (matching the EMERGENCY_RESTORE_SURFACE precedent) is the correct and only available resolution strategy for this one role"
  - "verify_voice_path_volume_silence() scopes to volume only, matching the plan's own flagged_assumptions -- brightness stays owned by verify_restore_gates()/verify_capture_persistence(), stated as deliberate non-coverage in the guard's own docstring rather than silently duplicated"
  - "docs/sequence_dispatch_check.py's action-equal check skips branches of unknown matching semantics before comparing bodies -- the UNKNOWN MATCH SEMANTICS gate already fails the run on those, so comparing an unresolvable branch's body would only add noise to a run already failing for a different, already-reported reason"

patterns-established:
  - "Real-build negative control for a generator-emitted guard, reverted in place: for verify_voice_gates() and verify_voice_path_volume_silence(), each mutation was made directly in voice()'s Python source (hoisting the speaktext action, deleting the Spoken This Run pair, inserting a volume write), `python3 tools/build_state_engine.py` was run for real and observed to fail with the expected message, then the source was reverted and the build re-run clean before moving on -- because verify_*() raises BEFORE SOURCE.write_bytes(), the on-disk artifact is never corrupted by a failing mutation, so no separate revert of the XML is needed."
  - "In-memory negative control for a provenance-severing or multi-guard-order mutation: where a mutation would be caught by an EARLIER guard before the one under test ever runs (severing all voice_enabled provenance also breaks verify_voice_enabled_seed() first; retargeting the dispatch tuple is caught by verify_speaktext_placement()/verify_voice_gates() before docs/sequence_dispatch_check.py's disk read could ever see it), the guard or checker function was called directly against an in-memory deepcopy or a synthetically mutated `bodies` dict instead -- functionally identical evidence, and the only way to isolate a later guard's own vacuity assertion from an earlier guard's overlapping coverage of the same underlying defect."

requirements-completed: [CIRC-08, CIRC-09, CIRC-14, DIST-01]

coverage:
  - id: D1
    description: "verify_voice_gates() fails the build if any speaktext site is reachable without both the consent gate (voice_enabled > 0, provenance-resolved) and the once-per-run gate ('Spoken This Run') enclosing it -- armed on both forks"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "negative control (a): voice()'s speaktext hoisted to branch base depth, real build run -- exits non-zero naming all 11 un-consented sites; reverted"
        status: pass
      - kind: other
        ref: "negative control (b): Spoken This Run conditional pair deleted from voice(), real build run -- exits non-zero naming all 11 sites missing the once-per-run enclosure; reverted"
        status: pass
      - kind: other
        ref: "negative control (c): all 13 getvalueforkey sites reading literal key 'voice_enabled' severed, in-memory -- raises rather than passing vacuously with the consent-variable set empty"
        status: pass
      - kind: other
        ref: "grep -c 'verify_voice_gates' tools/build_sentient.py -> 2 (import + call site)"
        status: pass
    human_judgment: true
    rationale: "CIRC-08 remains device-unproven per plan 15-02's own recorded verdict (axis-4 unfilled-picker defect, 'not discriminated at rung 2') -- a structurally green build with three measured negative controls must not be read as a behavioural pass on hardware. This plan closes only the structural-enclosure half of CIRC-08's gate."
  - id: D2
    description: "verify_voice_path_volume_silence() fails the build if any is.workflow.actions.setvolume action lies inside a 'Loud Mirror' (Circle 8) dispatch branch span -- armed on both forks"
    requirement: "CIRC-08"
    verification:
      - kind: other
        ref: "negative control (a): a volume write inserted immediately before voice()'s speaktext action, real build run -- exits non-zero naming all 11 offending sites; reverted"
        status: pass
      - kind: other
        ref: "negative control (b): every 'Loud Mirror' branch's tested literal renamed so no branch resolves, in-memory (isolates this guard's own vacuity assertion from verify_dispatch_coverage()'s earlier orphan check) -- raises rather than reporting the Voice path clean of volume writes"
        status: pass
      - kind: other
        ref: "grep -c 'verify_voice_path_volume_silence' tools/build_sentient.py -> 2"
        status: pass
      - kind: other
        ref: "python3 -c \"...setvolume count per fork...\" -> 15, unchanged baseline, all WFVolumeSetting == 'Media'"
        status: pass
      - kind: other
        ref: "python3 docs/environmental_restore_check.py -> passed"
        status: pass
    human_judgment: false
  - id: D3
    description: "docs/sequence_dispatch_check.py gates on two distinct sequence-entry names resolving to action-equal (normalised) dispatch branch bodies -- the general form of the defect this phase exists to close"
    requirement: "CIRC-14"
    verification:
      - kind: other
        ref: "negative control (a): 'Loud Mirror' -> 'Mirror' retarget simulated at the branch-bodies level (the real dispatch-tuple retarget cannot reach disk -- three earlier guards halt the build first), in-memory -- action_equal_pairs() returns [('Loud Mirror', 'Mirror')] and require() raises"
        status: pass
      - kind: other
        ref: "negative control (b): bodies computed with normalisation stripped -- every pair, including Mirror/Loud Mirror, compares as trivially distinct, proving normalisation is load-bearing"
        status: pass
      - kind: other
        ref: "python3 docs/sequence_dispatch_check.py -> 99 branches, 9 distinct names, 0 orphans, 0 unreachable, 0 unknown, 0 duplicates, 0 action-equal pairs, exits 0"
        status: pass
      - kind: other
        ref: "KNOWN_ORPHANS = {} confirmed still present and empty"
        status: pass
    human_judgment: false
  - id: D4
    description: "Circle 9 (Frozen/ice_start) and the environmental primitives are unaffected by this plan's guard additions"
    requirement: "CIRC-09"
    verification:
      - kind: other
        ref: "python3 docs/phase5_self_check.py -> passed (nine primitive names, three sequence names, Circle 9 = Frozen in all three sequences, unchanged)"
        status: pass
      - kind: other
        ref: "python3 docs/environmental_restore_check.py -> passed"
        status: pass
    human_judgment: false
  - id: D5
    description: "Both forks validate clean at gate A with all six Phase-15 guards armed (four from 15-01/15-03, two new this plan), plus 15-04's checker assertion, and 11 of 12 docs/*.py checkers pass"
    requirement: "DIST-01"
    verification:
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "11 of 12 docs/*.py checkers exit 0 (state_engine_self_check, phase5/6/7/9_self_check, sentient_audit_check, sentient_core_check, environmental_restore_check, router_ui_census, sequence_dispatch_check, note_identity_check); docs/manifest_check.py deliberately red per the phase's own standing constraint (bytes mismatch, expected until 15-05 re-signs)"
        status: pass
    human_judgment: false

duration: ~20min
completed: 2026-08-18
status: complete
---

# Phase 15 Plan 04: Voice Gates, Volume Silence, and the Dispatch Action-Equality Assertion Summary

**Two new build guards (consent-and-once-per-run enclosure over every speaktext site; zero volume writes inside any Circle-8 branch span) armed on both forks, plus a fifth `docs/sequence_dispatch_check.py` assertion that no two differently-named sequence entries may ever again resolve to action-equal dispatch bodies -- all three measured failing on synthesised defects, including every vacuous-resolution direction.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-08-18 (session start; PLAN_START_TIME not separately recorded)
- **Completed:** 2026-08-18T21:34:11+10:00 (final commit timestamp)
- **Tasks:** 3 completed
- **Files modified:** 3 (tools/build_state_engine.py, tools/build_sentient.py, docs/sequence_dispatch_check.py)

## Accomplishments

- Added `verify_voice_gates(actions)` to `tools/build_state_engine.py`, sited beside `verify_speaktext_placement()`: for every `is.workflow.actions.speaktext` site, asserts the enclosing-group tuple (computed by `enclosing_groups()`, a single structural stack pass) contains both a provenance-resolved `voice_enabled > 0` consent gate (via `_voice_enabled_variables()`, never a variable-name literal) and the once-per-run `Spoken This Run` gate (`WFCondition == 101`, D-06's guard kept verbatim). Two non-vacuity raises (resolved speech-site set, resolved consent-variable set) so the guard cannot report a clean enclosure it never actually checked.
- Added `verify_voice_path_volume_silence(actions)`, sited beside it: locates every `Loud Mirror` (Circle 8) dispatch branch span the same way `verify_speaktext_placement()` does (per-site condition-code resolution, never a hardcoded filter), then asserts zero `is.workflow.actions.setvolume` actions lie inside any of those spans, that the resolved branch set is non-empty, and that the artifact-wide `setvolume` count is non-zero -- so the guard cannot pass either by finding no branch or by volume writing having vanished from the product.
- Armed both guards on the Aware fork: `tools/build_sentient.py`'s import list and call site, alphabetically positioned beside `verify_speaktext_placement`.
- Added `branch_bodies()`, `normalise_body()`, `action_equal_pairs()` and a fifth `require(...)` to `docs/sequence_dispatch_check.py`: no two distinct sequence-entry names may resolve to action-equal dispatch branch bodies, once every `UUID`/`GroupingIdentifier`/`OutputUUID` reference is normalised away. This is the general form of the defect the whole phase exists to close -- `Mirror` and `Loud Mirror` dispatched the identical function for four phases while every existing check in this file, plus `verify_dispatch_coverage()`, the validator, the ToolKit catalog and a decrypt of the signed container, all stayed green.
- All three new checks measured failing on synthesised defects in every direction their assertions cover -- seven negative-control mutations total across the three guards/checker, five run as real builds (source edited, `python3 tools/build_state_engine.py` run for real, reverted) and two run in-memory where a real build would be intercepted by an earlier, unrelated guard before the mutation under test could ever be observed.
- Rebuilt both forks: gate A clean on both (`--target-macos 26 --target-platform all`, `Validation passed.`); measured 11 speech sites, 11 once-per-run conditionals, 15 Media-scoped `setvolume` sites (unchanged baseline), 99 dispatch branches / 9 distinct names / 0 action-equal pairs. `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` are **byte-identical** to their pre-plan state -- every change in this plan is a pure assertion or a read-only checker addition, none of it emits a different action.

## Task Commits

Each task was committed atomically, with one process deviation noted below:

1. **Task 1: `verify_voice_gates()` -- speech unreachable outside consent + once-per-run gates** - `8e6092c` (feat) -- this commit's diff also contains `verify_voice_path_volume_silence()`'s implementation (Task 2's guard function and its `main()`/`build_sentient.py` registration), authored in the same file edit per the plan's own instruction to site it "immediately beside" `verify_voice_gates()`.
2. **Task 2: record `verify_voice_path_volume_silence()`'s negative-control measurements** - `e62e237` (docs) -- Task 2's guard code shipped in commit `8e6092c` above; this commit records the two measured negative controls specific to that guard in its docstring, after they were run and observed.
3. **Task 3: the action-equality assertion -- two names must not mean one behaviour** - `ca28c61` (feat)

**Plan metadata:** (this commit, pending)

## Files Created/Modified

- `tools/build_state_engine.py` -- `SPOKEN_THIS_RUN_VARIABLE` constant; `verify_voice_gates()` and `verify_voice_path_volume_silence()` added beside `verify_speaktext_placement()`; both registered in `main()`'s `verify_*` block
- `tools/build_sentient.py` -- both new guards added to the import list (alphabetical position) and call site, beside `verify_speaktext_placement`
- `docs/sequence_dispatch_check.py` -- `_branch_end()`, `normalise_body()`, `branch_bodies()`, `action_equal_pairs()` added; a fifth `require(...)` and an `ACTION-EQUAL PAIRS` report section wired into `main()`; module docstring extended to name the new gate; `KNOWN_ORPHANS = {}` unchanged
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` -- **not modified**, confirmed byte-identical (`git status --short -- src/` empty after every rebuild in this plan) -- every guard added here is a pure assertion over already-emitted actions, and the checker is read-only

## Decisions Made

- **`verify_voice_gates()`'s once-per-run gate is resolved by a named literal constant, not by provenance.** Unlike the consent gate (`voice_enabled`, which has a `state.json` provenance chain to resolve against via `_voice_enabled_variables()`), `Spoken This Run` is a run-scoped Shortcuts variable with no dictionary-key provenance at all -- it is never read from or written to State. `SPOKEN_THIS_RUN_VARIABLE = "Spoken This Run"` is therefore a deliberate named constant (matching the existing `EMERGENCY_RESTORE_SURFACE` precedent), not an oversight of "never hardcode a literal" -- there is no provenance to resolve for this role.
- **`verify_voice_path_volume_silence()` covers volume only**, per the plan's own `flagged_assumptions`. Brightness stays owned by `verify_restore_gates()`/`verify_capture_persistence()`; the guard's own docstring states this is deliberate non-coverage rather than an oversight.
- **The action-equal check in `docs/sequence_dispatch_check.py` skips branches of unknown matching semantics** before comparing bodies, since the pre-existing `UNKNOWN MATCH SEMANTICS` gate already fails the run on those -- comparing an unresolvable branch's body would add noise to a run already failing for an unrelated, already-reported reason.

## Deviations from Plan

**Process deviation, not a functional one: Tasks 1 and 2's guard code was authored and committed together.** The plan's own action text says `verify_voice_path_volume_silence()` should be "sited beside `verify_voice_gates()`" -- both functions were written in one file edit adjacent to each other, and splitting that single edit into two separate tool calls each touching interleaved lines of the same function block would have been artificial. Commit `8e6092c` therefore contains both guards' implementations and both `main()`/`build_sentient.py` registrations; commit `e62e237` records Task 2's specific negative-control measurements (run and observed after the code landed) in that guard's own docstring. All of Task 2's acceptance criteria were independently verified (gate A on both forks, `grep -c` counts, the 15-site volume census, both negative controls) before either commit landed. No functional requirement of either task was skipped or under-delivered.

**Negative-control methodology split between real-build and in-memory, by necessity rather than convenience.** Five of the seven mutations across this plan's three checks (`verify_voice_gates` mutations a/b, `verify_voice_path_volume_silence` mutation a, plus their respective observations) were run as real builds: the relevant line(s) in `voice()` were temporarily edited, `python3 tools/build_state_engine.py` was run for real and its exit code/message observed, then the edit was reverted and the build re-run clean. The remaining two (`verify_voice_gates` mutation c, severing all 13 `voice_enabled` provenance sites; `verify_voice_path_volume_silence` mutation b, renaming every `Loud Mirror` branch's tested literal; and both `docs/sequence_dispatch_check.py` mutations) were run in-memory against a `copy.deepcopy()` of the already-built actions list or the checker's own `bodies` dict, calling the guard/checker function directly. This split is not a preference: for the in-memory cases, the mutation under test is caught by an EARLIER, different guard before the real build could ever reach the assertion being tested (severing all `voice_enabled` provenance is caught by `verify_voice_enabled_seed()` first; retargeting the dispatch tuple away from `voice` is caught by `verify_speaktext_placement()`/`verify_voice_gates()` before `docs/sequence_dispatch_check.py`'s disk read could ever see a changed artifact). Calling the function directly is the only way to isolate that specific assertion's own vacuity behaviour from the earlier guard's overlapping coverage of the same underlying defect. This methodology matches the in-memory pattern plan 15-03 already established in this same phase for an analogous multi-site provenance mutation.

One same-name-preserving variable rename was tried first for `verify_voice_gates()` mutation (c) and did NOT sever provenance -- discovered during measurement, not assumed. `_read_variable_keys()`'s provenance walk tracks the emitted data-flow graph (action outputs and named variables linked by reference), not variable-name literals, so a variable renamed consistently at both its write site and its read site keeps exactly the provenance it had. This is a correct property of the provenance-resolution design (a legitimate future rename must survive these guards), not a defect; the docstring records both the initial failed attempt and the correct 13-site source-severing mutation that actually exercises the assertion.

## Issues Encountered

None requiring a fix beyond the methodology corrections recorded above. No commit was reverted; the docstring text for each guard's negative-control section was refined in the same working session, before any commit, once the actual measured mutation and outcome were known.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- All six Phase-15 build guards (`verify_speaktext_placement`, `verify_voice_enabled_seed` from 15-01/15-03, plus this plan's `verify_voice_gates` and `verify_voice_path_volume_silence`) are armed on both forks, and `docs/sequence_dispatch_check.py`'s fifth assertion is a permanent standing invariant guard for the `mirror_and_voice` -> `mirror` + `voice` split: if a future pass ever re-merges them, this checker goes red.
- `docs/manifest_check.py` is red as expected (measured: `MANIFEST declares 2864203 bytes, src/PROSOCHE-Dumb.xml is 2780563 bytes`) and stays red until plan 15-05 re-signs both forks and re-derives the MANIFEST rows. This is not a defect in this plan's work -- `src/*.xml` did not change in this plan at all, so the pre-existing mismatch from earlier waves is untouched.
- **CIRC-08 remains recorded as device-unproven**, per plan 15-02's own verdict (the axis-4 unfilled-picker defect was "not discriminated at rung 2"). This plan's guards prove the consent and once-per-run enclosures are structurally correct and cannot silently erode -- they do not and cannot prove Circle 8 fires audibly on a real iPhone. No step in this plan claims device evidence it does not have.
- No blockers for 15-05.

---
*Phase: 15-circle-8-the-voice-primitive*
*Completed: 2026-08-18*

## Self-Check: PASSED

- FOUND: 8e6092c (Task 1 commit)
- FOUND: e62e237 (Task 2 commit)
- FOUND: ca28c61 (Task 3 commit)
- FOUND: tools/build_state_engine.py
- FOUND: tools/build_sentient.py
- FOUND: docs/sequence_dispatch_check.py
