---
created: 2026-08-13T12:04:27.110Z
title: Fix OPEN routing and Test Circle sequence error
area: general
severity: blocker
files:
  - tools/build_state_engine.py:1045
  - tools/build_state_engine.py:1067
  - src/PROSOCHE-Dumb.xml:27277
  - src/PROSOCHE-Dumb.xml:27283
  - src/PROSOCHE-Dumb.xml:28185
  - src/PROSOCHE-Sentient.xml:28519
  - src/PROSOCHE-Sentient.xml:28525
  - src/PROSOCHE-Sentient.xml:29427
---

## Problem

On-device testing of the manually created app-open automation does not enter the expected OPEN path. The automation wrapper has a Text action containing exactly `OPEN`, followed by Run Shortcut with its Input set to that Text magic variable. Opening a configured target app nevertheless displays the manual menu (`Status`, `Open Control Room`, `Sync My Profile`, and so on) instead of immediately firing the Circle 1 intervention.

A second failure is observable from that unexpected menu. Choosing **Test a Circle** displays nine buttons labelled Circle 1 through Circle 9, but selecting a Circle produces this error:

> No value provided. No value was provided to the Set Dictionary Value action for the key "sequence".

It is not yet known whether the OPEN misrouting and missing `sequence` value share one cause. Record them together because they were observed in the same first on-device automation test, but do not assume they are causally related.

## Status — CLOSED 2026-08-15

Debug session `open-routing-sequence-error` ran 16 cycles against this todo and is now
**RESOLVED, archived** at `.planning/debug/resolved/open-routing-sequence-error.md`.
Both symptoms are CLOSED and device-verified. This todo is fully resolved; no further
action required against it.

**The two symptoms did NOT share a cause**, as this todo cautioned. Confirmed separately.

**Symptom 2 (`sequence` / Set Dictionary Value) — CLOSED, device-verified.** Two defects,
both generator-wide: `setvalueforkey` was emitting `WFInput` where the action defines
`WFDictionaryValue` (147 sites), and string-typed parameters carried a bare
`WFTextTokenAttachment` where a `WFTextTokenString` is required (367 sites).

**Symptom 1 (OPEN misrouting) — CLOSED, device-verified 2026-08-15.** The original
diagnosis was wrong, and routing itself was never the problem. An INPUT PROBE proved the
automation wrapper delivers `OPEN` correctly (`RAW [OPEN] / NORMALISED [OPEN]`); the real
cause was that the OPEN branch had never executed on device (`Input Key` always resolved
empty, so every run took the MANUAL arm). Once fixed, nine distinct parameter-defect axes
surfaced one at a time across 16 cycles, each invisible to the sweep that caught the
previous one — full taxonomy in `.claude/CLAUDE.md` § Conventions. The terminal blocker
(`pending_exit` absent from the bootstrap `state.json` template, plus a compounding
gate-semantics defect) was closed in cycle 16 (build `2026-08-15o`) and confirmed on
device 2026-08-15: every breadcrumb A–J fired, the Leaving/Continue intervention menu
displayed, and Circle 1 fired with Pressure=0.166666666666667 (1/6) / Heat=0.

## Solution

Both symptoms closed. Residual follow-up work spun off as standalone todos during
closure — see `.planning/debug/resolved/open-routing-sequence-error.md`'s closing
Resolution section and `.planning/debug/HANDOFF.md` for the full index
(`2026-08-15-fork-sentient-post-openpath-fix.md`,
`2026-08-15-close-state-shape-sentinel-gaps.md`,
`2026-08-15-fix-red-operator-and-list-wrapper-defects.md`,
`2026-08-15-ship-readiness-cleanup.md`).
