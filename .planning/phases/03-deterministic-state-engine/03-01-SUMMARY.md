---
phase: 3
plan: 1
subsystem: shortcut-state-engine
tags: [shortcuts, plist, state, heat, circle]
provides: [OPEN-state-pipeline, deterministic-circle]
affects: [phase-4, phase-5]
status: complete
---

# Phase 3 Plan 1: Deterministic State Engine Summary

Semantic OPEN-anchor replacement now computes and persists the deterministic state engine from the full State dictionary.

## Completed

- Behavioural-day rollover resets only the daily open counter.
- OPEN uses timestamp debounce, cooldown no-inflation, ordered decay/base/reopen/previous-session adjustment, final clamp, Gravity, Pressure, and a nine-step profile threshold scan.
- Each dictionary mutation rebinds the returned full dictionary before the next mutation; the result is saved once per active OPEN path.
- `docs/state_engine_self_check.py` proves the arithmetic examples and plist wiring shape.

## Verification

- `python3 .../validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` — passed.
- `python3 docs/state_engine_self_check.py` — passed.

## Deviations from Plan

None — merged context executed directly.

## Self-Check: PASSED

- `src/PROSOCHE-Dumb.xml` exists and retains actions 0–4.
- OPEN semantic anchor is replaced and no OPEN stub remains.

