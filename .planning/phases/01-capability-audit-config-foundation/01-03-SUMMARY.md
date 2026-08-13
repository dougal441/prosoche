---
phase: 01-capability-audit-config-foundation
plan: 03
subsystem: docs
tags: [shortcuts-playground, config-block, ios26, heat, gravity, pressure, thresholds]

# Dependency graph
requires:
  - "src/CONFIG-BLOCK.md skeleton and sequences object from plan 01-01"
provides:
  - "src/CONFIG-BLOCK.md complete: one fenced JSON literal with all nine top-level keys (config_version, behavioural_day, thresholds, cooldown_seconds, sequences, heat, gravity, exits, safety)"
  - "A field-reference table with one row per leaf key, distinguishing canonical section references from PROTOTYPE DEFAULT / PROTOTYPE INTERPRETATION labelled choices"
  - "Derived-value rules for behavioural day, Gravity, Pressure, Circle resolution, and the six-step ordered Heat pipeline"
  - "The transcription recipe (Text action -> Detect Dictionary -> Get Dictionary Value with dotted key paths) and its two coercion hazards"
affects: [phase-2, phase-3, phase-5]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Every leaf key in the Config literal carries a Provenance cell: a canonical section reference, or the explicit label PROTOTYPE DEFAULT / PROTOTYPE INTERPRETATION when the strategy leaves the value open"
    - "Exactly one fenced json block is permitted in src/CONFIG-BLOCK.md; the automated verify asserts the count so no second, competing literal can drift out of sync"

key-files:
  created: []
  modified:
    - src/CONFIG-BLOCK.md

key-decisions:
  - "heat.reopen_bonus_mode = \"exclusive\": a reopen satisfying both the <2min and <10min rapid-return bands earns only the tighter band's bonus, not both stacked. Labelled PROTOTYPE INTERPRETATION; the alternative (\"cumulative\") is named; Phase 3 owns implementing STATE-04 against whichever value is set."
  - "heat.ice_expiry_relief = -1, config_version = 1, exits.exploration_rate = 0.2, exits.exploit_min_observations = 10: all four labelled PROTOTYPE DEFAULT because canonical strategy requires the field to exist but states no number."

requirements-completed: [AUDIT-08]

coverage:
  - id: D1
    description: "src/CONFIG-BLOCK.md's single fenced JSON literal holds all nine top-level keys with canonical values transcribed from strategy sections 10.1-10.5, 12, and 22"
    requirement: "AUDIT-08"
    verification:
      - kind: other
        ref: "python3 json-parse verify command in 01-03-PLAN.md task 1 (CONFIG-JSON-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Field reference, derived-value rules, and transcription recipe let a Phase 2/3 executor transcribe and implement without reinterpreting canonical strategy or guessing a key name"
    requirement: "AUDIT-08"
    verification:
      - kind: other
        ref: "grep-based structural verify command in 01-03-PLAN.md task 2 (FIELD-REFERENCE-OK)"
        status: pass
    human_judgment: false

duration: ~20min
completed: 2026-08-13
status: complete
---

# Phase 1 Plan 3: Config Block Completion Summary

**`src/CONFIG-BLOCK.md` completed with the full nine-key JSON literal (profile thresholds, Ice cooldowns, Heat coefficients, Gravity, behavioural-day offset, exit exploration rate, safety floors), a field-reference table that labels every value as canonical or a named prototype choice, and the derived-value rules a Phase 3 executor implements against.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-13
- **Tasks:** 2
- **Files modified:** 1 (`src/CONFIG-BLOCK.md`)

## Accomplishments

- Replaced the partial `sequences`-only literal from plan 01-01 with the complete nine-key JSON object: `config_version`, `behavioural_day` (`offset_seconds: -14400`, `key_format: "yyyy-MM-dd"`), `thresholds` (Paradise/Limbo/Inferno, transcribed verbatim from §10.5), `cooldown_seconds` (Paradise 60 / Limbo 180 / Inferno 300, §22), `sequences` (carried over byte-identical from 01-01, unchanged), `heat` (twelve coefficients from §10.2's suggested initial rule), `gravity` (`opens_per_point: 6`, `cap: 5`, §10.3), `exits` (`exploration_rate: 0.2`, `exploit_min_observations: 10`), and `safety` (brightness/dim floors and `allow_volume_increase: false`, §21).
- Verified the file contains exactly one fenced ` ```json ` block in total, satisfying the "single editable block" constraint later plans and the coverage check depend on.
- Labelled the two open ambiguities in canonical strategy as prose notes directly under the literal: `heat.reopen_bonus_mode = "exclusive"` (a reopen matching both the <2min and <10min bands earns only the tighter bonus, not both), with `"cumulative"` named as the alternative and Phase 3 named as the owner of STATE-04; and the Pressure/Circle-resolution rule (Pressure = Heat + Gravity; Circle resolution is an ordered `>=` scan, never an equality test, because Shortcuts has no numeric-equals condition code).
- Wrote a 31-row field-reference table (one row per leaf key) whose `Provenance` cell is either a canonical section reference or the explicit label `PROTOTYPE DEFAULT` (`config_version`, `exits.exploration_rate`, `exits.exploit_min_observations`, `heat.ice_expiry_relief`) or `PROTOTYPE INTERPRETATION` (`heat.reopen_bonus_mode`), plus a `Tunable range` cell stating a sane bound for a prototype tuner (e.g. `heat.cap` must exceed the highest threshold in the most aggressive profile, `safety.brightness_floor` must never reach zero).
- Wrote the derived-value rules: behavioural day (raw `Date` → `Adjust Date` Subtract → `Format Date` Custom, never string-level date math), Gravity (`floor(opens_today / opens_per_point)`, capped, routed through a `Number` action first), Pressure (`heat + gravity`), Circle resolution (bounded nine-iteration `>=` scan, equality tests explicitly forbidden), and the six-step ordered Heat pipeline (decay → open_base → reopen bonus → overrun penalty → contract relief → clamp last).
- Expanded `## How to use this file` with the concrete transcription recipe (one `Text` action → one `Detect Dictionary` action into a `Config` variable → `Get Dictionary Value` with 1-based dotted key paths) and the two coercion hazards a Phase 2/3 executor will otherwise hit: `safety.allow_volume_increase` reads back as numeric `1`/`0` not `"true"`/`"false"`, and any Dictionary Value destined for an `If` comparison must first pass through a `Text` action.

## Task Commits

Each task was committed atomically:

1. **Task 1: The complete Config JSON literal** - `b21ad36` (feat)
2. **Task 2: Field reference, derived-value rules, and the transcription recipe** - `befffba` (docs)

## Files Created/Modified

- `src/CONFIG-BLOCK.md` - Completed: single fenced JSON literal (nine top-level keys), two prose ambiguity notes, 31-row field-reference table, derived-value rules (behavioural day / Gravity / Pressure / Circle resolution / Heat pipeline), expanded transcription recipe, and a dated change log

## Decisions Made

- **`heat.reopen_bonus_mode = "exclusive"`** (PROTOTYPE INTERPRETATION): resolves the 90-second-reopen ambiguity in §10.2 by applying only the tightest matching rapid-return band. `"cumulative"` is named as the alternative; Phase 3 owns implementing STATE-04 against whichever value the key holds.
- **`config_version`, `heat.ice_expiry_relief`, `exits.exploration_rate`, `exits.exploit_min_observations`** all labelled PROTOTYPE DEFAULT: canonical strategy requires each field to exist (§16 schema versioning convention; §22's "provide Heat relief"; §9.3's "exploration percentage must be configuration") but states no number for any of them.

## Deviations from Plan

None - plan executed exactly as written. All canonical values were transcribed exactly as specified in the plan's `<action>` block; both prose ambiguity notes and both required verify commands passed on first run.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `src/CONFIG-BLOCK.md` is now a complete, self-contained specification: a Phase 2 executor can transcribe the single JSON literal directly into a Shortcuts `Text` action without inventing a key name, and a Phase 3 executor can implement the Heat/Gravity/Pressure/Circle arithmetic from the derived-value rules without reinterpreting canonical strategy.
- Two labelled open points remain for later phases to resolve with real values if testing reveals a need: `heat.reopen_bonus_mode`'s exclusive/cumulative choice (Phase 3, STATE-04) and `heat.ice_expiry_relief`'s magnitude (Phase 3, tested against whether Ice re-triggers immediately on expiry).
- No plist XML, package manifest, lockfile, or test-runner configuration was created, consistent with this phase's scope boundary. `docs/BUILD-NOTES.md` was not touched (owned by the parallel 01-02 plan in this wave).

---
*Phase: 01-capability-audit-config-foundation*
*Completed: 2026-08-13*

## Self-Check: PASSED

- FOUND: src/CONFIG-BLOCK.md
- FOUND: .planning/phases/01-capability-audit-config-foundation/01-03-SUMMARY.md
- FOUND: b21ad36 (Task 1 commit)
- FOUND: befffba (Task 2 commit)
