---
phase: 01-capability-audit-config-foundation
plan: 01
subsystem: docs
tags: [shortcuts-playground, capability-audit, ios26, color-filters, config-block]

# Dependency graph
requires: []
provides:
  - "docs/BUILD-NOTES.md with the seven-section schema, the closed four-value verdict vocabulary, the seven-column audit table, and the CAP-20 row (NOT AVAILABLE, evidence-backed)"
  - "The do-not-fabricate protocol and evidence protocol (BUILD-NOTES.md §2-3), binding on every later plan's capability rows"
  - "docs/CAPABILITY-DECISIONS.md with the BD-01..BD-05 table of contents and a complete BD-01 (Ash/Color Filters) decision record"
  - "src/CONFIG-BLOCK.md with the sequences object (Classic/BlackMirror/Ambient) transcribed verbatim from canonical strategy section 12"
affects: [01-02, 01-03, 01-04, 01-05, phase-2, phase-5]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Every capability audit row cites the exact ToolKit JSON file(s) and internal key path queried, per the evidence protocol in BUILD-NOTES.md section 3"
    - "Every deviation entry carries five labelled fields (Capability, Wanted, Verified, Substituted, Runnability) traceable to a blocker decision"
    - "Every blocker decision carries seven labelled fields (Question, Evidence, Options considered, Decision, Rationale, Consequence for later phases, Requirement)"

key-files:
  created:
    - docs/BUILD-NOTES.md
    - docs/CAPABILITY-DECISIONS.md
    - src/CONFIG-BLOCK.md
  modified: []

key-decisions:
  - "BD-01: Ash is degraded to a non-environmental variant (a verified, self-contained low-salience visual pause) rather than a system Color Filters toggle, because no iOS-available read-and-restore mechanism for Color Filters exists in any bundled ToolKit snapshot"
  - "CAP-20 verdict is NOT AVAILABLE, confirmed by a live re-run of the ToolKit lookup rather than copied from the research base unchecked"

patterns-established:
  - "Pattern: capability audit rows require the executor to re-run the lookup itself and record what it actually finds, including any divergence from the prior research base"

requirements-completed: [AUDIT-01, AUDIT-02, AUDIT-07]

coverage:
  - id: D1
    description: "docs/BUILD-NOTES.md created with the seven-section schema, verdict vocabulary, and one fully populated CAP-20 row backed by a live ToolKit lookup"
    requirement: "AUDIT-01"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-01-PLAN.md task 1 (TRACER-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The Ash primitive (Color Filters/grayscale) blocker resolved to a recorded go/no-go decision (BD-01) with rationale tied to canonical strategy section 21 and PITFALLS C4"
    requirement: "AUDIT-02"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-01-PLAN.md task 1 (TRACER-OK)"
        status: pass
    human_judgment: true
    rationale: "BD-01 selects one of three D-08-named options at Claude's discretion; whether the selected option (degrade Ash to a non-environmental variant) is the right product call for Phase 5 to build against is a judgment call a human should confirm before Phase 5 implements CIRC-02."
  - id: D3
    description: "src/CONFIG-BLOCK.md created with the sequences object (Classic/BlackMirror/Ambient) transcribed verbatim from canonical strategy section 12, with Ash preserved in all three orderings per BD-01"
    requirement: "AUDIT-07"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-01-PLAN.md task 1 (TRACER-OK)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Do-not-fabricate protocol and reproducible evidence protocol documented in BUILD-NOTES.md sections 2-3, with a runnable lookup snippet and worked CAP-20 example"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-01-PLAN.md task 2 (EVIDENCE-PROTOCOL-OK)"
        status: pass
    human_judgment: false

duration: ~15min
completed: 2026-08-13
status: complete
---

# Phase 1 Plan 1: Ash / Color Filters Tracer Slice Summary

**Ash (Color Filters/grayscale) traced end to end through a live ToolKit lookup, a NOT-AVAILABLE audit row, a numbered deviation, a recorded BD-01 decision (degrade to non-environmental variant), and its preserved slot in all three config sequence orderings.**

## Performance

- **Duration:** ~15 min
- **Completed:** 2026-08-13
- **Tasks:** 2
- **Files modified:** 3 (all newly created)

## Accomplishments
- Ran a live, reproducible ToolKit lookup (not a copy of the research base) against all three identifier snapshots and the OS27 parameter catalog for `UAToggleColorFiltersIntent`, confirming it independently: present in `toolkit-v63`/`toolkit-v78` generic snapshots, tagged `macOS 27` only in every parameter, absent from `toolkit-v78-ios27-tool-ids.json`. No divergence from `.planning/research/STACK.md` was found.
- Established the durable schema every later plan (01-02 through 01-05) will extend: the seven-section `docs/BUILD-NOTES.md` structure, the closed four-value verdict vocabulary, the seven-column audit table, the five-field deviation-entry shape, and the seven-field decision-record shape.
- Recorded `BD-01` in `docs/CAPABILITY-DECISIONS.md`: Ash is redefined as a non-environmental, self-contained low-salience visual pause rather than a system Color Filters toggle, with rationale tied to canonical strategy §21's absolute rule and PITFALLS.md C4's accessibility-clobbering hazard. Named `CIRC-02` and Phase 5 explicitly as the consequence.
- Created `src/CONFIG-BLOCK.md` with the `sequences` object (`Classic`, `BlackMirror`, `Ambient`), each a verbatim nine-entry transcription from canonical strategy §12, with `Ash` and `Ash+Confession` preserved in every ordering and an explicit note that BD-01 redefines Ash's implementation without deleting it from the sequence table.
- Documented the do-not-fabricate protocol (binding on both Dumb and Sentient forks) and a reproducible evidence protocol — including a runnable Python lookup snippet and a worked example reproducing the CAP-20 Evidence cell — so every later plan re-runs the identical query rather than improvising.

## Task Commits

Each task was committed atomically:

1. **Task 1: Ash / Color Filters end to end — audit row, deviation, decision, config entry** - `b061682` (feat)
2. **Task 2: Do-not-fabricate protocol and reproducible evidence protocol** - `8605eb9` (docs)

## Files Created/Modified
- `docs/BUILD-NOTES.md` - Seven-section capability-audit document: purpose/scope, do-not-fabricate protocol, evidence protocol, audit table (CAP-20), deviation log (DEV-01), and placeholder headings for sections owned by later plans
- `docs/CAPABILITY-DECISIONS.md` - Blocker-decision record: BD-01..BD-05 table of contents plus the complete BD-01 (Ash/Color Filters) decision
- `src/CONFIG-BLOCK.md` - Config literal skeleton: `## How to use this file` plus the `sequences` JSON object; remaining sections left as placeholders for plan 01-03

## Decisions Made
- **BD-01 (Ash / Color Filters):** Selected "degrade Ash to a non-environmental variant" (option 3 of the three D-08 names) over substituting Dimming (would collapse two distinct sequence primitives into one) or requiring user opt-in (still requires trusting an unconfirmable accessibility state, since no read-back mechanism exists at all). Rationale ties directly to canonical strategy §21's "skip dynamic grayscale" branch and PITFALLS.md C4.
- **CAP-20 verdict:** Set to `NOT AVAILABLE` (not softened to `UNVERIFIED` or `VERIFIED (identifier only)`) because the identifier's own parameter catalog entry is macOS-27-only-tagged with zero iOS provenance anywhere in the bundle, and per D-07 this is treated as a correct, expected research outcome.

## Deviations from Plan

None — plan executed exactly as written. `DEV-01` in `docs/BUILD-NOTES.md` §5 is itself the plan-mandated deviation-log entry for the Ash capability (a planned artifact of Task 1, not an unplanned executor deviation from Rules 1-4).

## Issues Encountered

None. The precondition check (ToolKit data directory and all five required snapshot files) passed on first verification; the live lookup confirmed the research base's findings for CAP-20 with no divergence.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plans 01-02 through 01-05 can extend `docs/BUILD-NOTES.md` (35 more capability rows, more deviations, user action items UA-01+, coverage check), `docs/CAPABILITY-DECISIONS.md` (BD-02 through BD-05), and `src/CONFIG-BLOCK.md` (profile thresholds, Heat coefficients, Gravity, Ice cooldowns, exploration rate) against the exact schema this plan demonstrated once — no new structure should need to be invented.
- Phase 5 has a named, binding target for the Ash primitive's implementation (`CIRC-02`, per BD-01) rather than an open question.
- No plist XML, package manifest, lockfile, or test-runner configuration was created, consistent with this phase's scope boundary.

---
*Phase: 01-capability-audit-config-foundation*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: docs/BUILD-NOTES.md
- FOUND: docs/CAPABILITY-DECISIONS.md
- FOUND: src/CONFIG-BLOCK.md
- FOUND: .planning/phases/01-capability-audit-config-foundation/01-01-SUMMARY.md
- FOUND: b061682 (Task 1 commit)
- FOUND: 8605eb9 (Task 2 commit)
