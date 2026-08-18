---
phase: 15-circle-8-the-voice-primitive
plan: 01
subsystem: infra
tags: [shortcuts-plist-generator, python, ios-shortcuts, build-guards, state-machine]

# Dependency graph
requires:
  - phase: 11-addendum-01-apply-build-addendum
    provides: "Circle 8 already a live dispatch entry ('Loud Mirror'), condition-4 exact-match dispatch, docs/sequence_dispatch_check.py as a hard gate with KNOWN_ORPHANS = {}"
provides:
  - "mirror() (Circle 7, shows only) and voice() (Circle 8, shows and speaks once) as two distinct designed primitives, replacing the shared interim mirror_and_voice()"
  - "verify_speaktext_placement() build guard: fails the build if Circle 8 loses its speech or Circle 7 regains it"
  - "primitive_dispatch()'s tuple retargeted: ('Mirror', mirror), ('Loud Mirror', voice)"
  - "Both forks rebuilt, gate-A clean, with 11 speaktext sites per fork (down from 22) and setvolume unchanged at 15"
affects: [15-02-mirror-picker-discriminator, 15-03-voice-enabled-normalisation, 15-04-voice-gates-and-dispatch-invariants, 15-05-build-notes-and-manifest]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Shared-body split: _mirror_body() factors the template-selection actions common to both mirror() and voice(), so the 30-template surface stays single-sourced through mirror_text()"
    - "Placement guard: verify_speaktext_placement() resolves dispatch branches by provenance (enclosing_groups() over each branch's GroupingIdentifier) rather than by index, mirroring verify_dispatch_coverage()'s per-site condition-code resolution"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - src/CONFIG-BLOCK.md
    - docs/BUILD-NOTES.md

key-decisions:
  - "D-02 implemented: speech removed from Circle 7's mirror(), moved to Circle 8's voice() -- this is what makes Circle 8 an escalation and satisfies CIRC-14"
  - "D-01 implemented: voice()'s alert is emitted before the consent gate, so voice_enabled=0 still shows a Mirror-equivalent alert; Circle 8 is never empty"
  - "D-03 implemented: voice() reuses the same 30 fact-gated templates as mirror() via the shared _mirror_body() helper -- no new copy"
  - "D-06 implemented: the Spoken This Run guard was copied byte-shape-verbatim from the retired mirror_and_voice() -- no reset, no second flag, no clear step"
  - "verify_speaktext_placement() recognises exactly one dispatch-matching shape (condition 4 'string is') and raises on anything else, deliberately avoiding any equality test against the retired condition-99 'contains' literal, per this plan's own acceptance criterion"

patterns-established:
  - "Two-mutation negative control for a placement guard: retargeting the dispatch tuple entry proves the 'went silent' failure mode, appending a speech action to the sibling primitive proves the 'regained speech' failure mode -- both measured and reverted, both outcomes recorded in the guard's own docstring"

requirements-completed: [CIRC-08, CIRC-09, CIRC-14, DIST-01]

coverage:
  - id: D1
    description: "Circle 7 (mirror()) shows a fact-gated reflection and never speaks; Circle 8 (voice()) shows the same reflection and speaks it once when voice_enabled > 0"
    requirement: "CIRC-14"
    verification:
      - kind: other
        ref: "python3 -c \"...speaktext count per fork...\" -> 11 (was 22)"
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
      - kind: other
        ref: "validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all -> Validation passed."
        status: pass
    human_judgment: true
    rationale: "CIRC-08 remains device-unproven per this plan's own standing constraint (D-04, the inherited axis-4 unfilled-picker defect on the Mirror primitive) -- a structurally green build must not be read as a behavioural pass on hardware. Plan 15-02 owns the device-evidence discrimination."
  - id: D2
    description: "verify_speaktext_placement() build guard fails the build if Circle 8's speech is lost or Circle 7's speech is regained, armed on both forks"
    requirement: "CIRC-14"
    verification:
      - kind: other
        ref: "negative control (a): retarget ('Loud Mirror', voice) -> ('Loud Mirror', mirror); python3 tools/build_state_engine.py exits 1, message names every Loud Mirror branch span holding zero speaktext sites; mutation reverted"
        status: pass
      - kind: other
        ref: "negative control (b): append speaktext to mirror(); python3 tools/build_state_engine.py exits 1, message names the site found inside a Mirror branch span; mutation reverted"
        status: pass
      - kind: other
        ref: "grep -c 'verify_speaktext_placement' tools/build_sentient.py -> 2 (import + call site)"
        status: pass
    human_judgment: false
  - id: D3
    description: "No document in the repository still describes Circle 8's implementation as an interim awaiting this phase"
    verification:
      - kind: other
        ref: "grep -c 'DELIBERATE INTERIM' tools/build_state_engine.py -> 1 (Circle-6/Eject only)"
        status: pass
      - kind: other
        ref: "grep -c 'Phase 15' src/CONFIG-BLOCK.md -> 0"
        status: pass
      - kind: other
        ref: "docs/BUILD-NOTES.md section 34 dated supersession note naming voice() as the discharge; Circle-6 Eject subsection unedited"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-08-18
status: complete
---

# Phase 15 Plan 01: Split mirror_and_voice() into mirror() and voice() Summary

**Circle 7 now shows-only via mirror(), Circle 8 shows-and-speaks-once via voice(), retargeted through primitive_dispatch()'s tuple and locked in place by a new verify_speaktext_placement() build guard measured to fail in both directions.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-08-18T10:08:22Z
- **Completed:** 2026-08-18T10:23:19Z
- **Tasks:** 3 completed
- **Files modified:** 6 (tools/build_state_engine.py, tools/build_sentient.py, src/PROSOCHE-Dumb.xml, src/PROSOCHE-Sentient.xml, src/CONFIG-BLOCK.md, docs/BUILD-NOTES.md)

## Accomplishments

- Split the interim `mirror_and_voice()` into `_mirror_body()` (shared template selection), `mirror()` (Circle 7, shows only), and `voice()` (Circle 8, shows and speaks once, consent-gated) — retired `mirror_and_voice()` outright
- Retargeted `primitive_dispatch()`'s dispatch tuple: `("Mirror", mirror)`, `("Loud Mirror", voice)`; updated the generator's own comment block above the tuple so it no longer calls Circle 8 an interim
- Added `verify_speaktext_placement()`, a new build guard armed on both forks, that fails the build if Circle 8 loses its speech or Circle 7 regains it — measured to actually fail in both directions via two reverted negative-control mutations
- Rebuilt both forks: `speaktext` sites dropped from 22 to 11 per fork (both Mirror's 11 were removed, Loud Mirror's 11 kept), `setvolume` unchanged at 15; both forks pass validator gate A clean
- Retired the "interim" declaration in `src/CONFIG-BLOCK.md` and `docs/BUILD-NOTES.md` section 34, following each file's own strike/annotate supersession convention rather than deleting history

## Task Commits

Each task was committed atomically:

1. **Task 1: End-to-end "Circle 7 shows, Circle 8 speaks"** — `ea04354` (feat)
2. **Task 2: verify_speaktext_placement() — the guard that makes the escalation structural** — `e9f39d5` (feat)
3. **Task 3: retire the interim declaration in the two documents that mirror it** — `b8c7d1d` (docs)

**Plan metadata:** (this commit, pending)

## Files Created/Modified

- `tools/build_state_engine.py` — `_mirror_body()`, `mirror()`, `voice()` replace `mirror_and_voice()`; `primitive_dispatch()`'s tuple and comment updated; `verify_speaktext_placement()` added beside `verify_dispatch_coverage()` and armed in `main()`
- `tools/build_sentient.py` — `verify_speaktext_placement` added to the import list (alphabetical position) and call site, beside `verify_dispatch_coverage()`
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` — regenerated in place; 11 `speaktext` sites each (was 22), 15 `setvolume` sites each (unchanged)
- `src/CONFIG-BLOCK.md` — Circle-8 bullet rewritten to state the shipped fact; preamble "two entries" → "one entry" (only Circle-6/Eject remains interim); Config JSON literal byte-identical
- `docs/BUILD-NOTES.md` — section 34 heading and Circle-8 subsection carry a dated supersession note naming `voice()` as the replacement; original prose retained as history; Circle-6 subsection untouched

## Decisions Made

- **D-01/D-02/D-03/D-06 implemented exactly as locked in `15-CONTEXT.md`** — see `key-decisions` in frontmatter above. No new product decisions were made in this plan; all six were pre-confirmed by the user on 2026-08-18 before planning.
- **`verify_speaktext_placement()` recognises exactly one dispatch-matching shape** (condition 4, "string is") rather than duplicating `verify_dispatch_coverage()`'s condition-99/condition-4 classification. This was a design choice made during Task 2 to satisfy the plan's own acceptance criterion that the guard's body contain no equality test against the literal `99` — the guard treats anything other than condition 4 against a plain string as unrecognised and raises, which achieves "never filter on a hardcoded code, and an unrecognised strategy raises" without ever naming the retired condition. Recorded here because it is a deliberate divergence from `verify_dispatch_coverage()`'s literal shape, not an oversight — the two guards are used for different questions (coverage vs. placement) and BD-06 already abolished the condition-99 strategy for every branch this guard inspects.

## Deviations from Plan

None — plan executed exactly as written, including its explicit non-goals (CIRC-08 remains recorded as device-unproven; `docs/manifest_check.py` is left red per the plan's own standing constraint).

## Issues Encountered

The first draft of `verify_speaktext_placement()` copied `verify_dispatch_coverage()`'s condition-99/condition-4 classification verbatim (per the pattern map's Rule 4 guidance), which put a literal `== 99` in the guard's body. Re-reading Task 2's acceptance criteria caught this before commit: the guard's body must contain no equality test against `99`. Redesigned to recognise exactly one shape (condition 4) and raise on anything else — re-ran both negative-control mutations against the redesigned guard and confirmed identical pass/fail behavior before committing. No commit was reverted; the redesign happened entirely within Task 2's single working session, before the first commit of that task's files.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `mirror()` and `voice()` are structurally correct, gate-A clean, and structurally distinguishable — ready for plan 15-02's device-evidence discrimination of the inherited axis-4 unfilled-picker defect (which follows the primitive, not the Circle, and blocks either Circle 7 or Circle 8 from actually running on a phone until resolved).
- Plan 15-03 can proceed with `voice_enabled` normalisation independently — this plan did not touch that state-shape question.
- `docs/manifest_check.py` is red as expected (measured: `MANIFEST declares 2864203 bytes, src/PROSOCHE-Dumb.xml is 2780570 bytes`) and stays red until plan 15-05 re-signs both forks and re-derives the MANIFEST rows. This is not a defect in this plan's work.
- No blockers for 15-02 through 15-05.

---
*Phase: 15-circle-8-the-voice-primitive*
*Completed: 2026-08-18*

## Self-Check: PASSED

- FOUND: ea04354 (Task 1 commit)
- FOUND: e9f39d5 (Task 2 commit)
- FOUND: b8c7d1d (Task 3 commit)
- FOUND: tools/build_state_engine.py
- FOUND: tools/build_sentient.py
- FOUND: src/PROSOCHE-Dumb.xml
- FOUND: src/PROSOCHE-Sentient.xml
- FOUND: src/CONFIG-BLOCK.md
- FOUND: docs/BUILD-NOTES.md
