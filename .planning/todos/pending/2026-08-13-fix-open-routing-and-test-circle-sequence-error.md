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

## Status — updated 2026-08-15

Debug session `open-routing-sequence-error` ran 13 cycles against this todo and is now
**paused, clean**. Resume from `.planning/debug/HANDOFF.md`.

**The two symptoms did NOT share a cause**, as this todo cautioned. Confirmed separately.

**Symptom 2 (`sequence` / Set Dictionary Value) — CLOSED, device-verified.** Two defects,
both generator-wide: `setvalueforkey` was emitting `WFInput` where the action defines
`WFDictionaryValue` (147 sites), and string-typed parameters carried a bare
`WFTextTokenAttachment` where a `WFTextTokenString` is required (367 sites).

**Symptom 1 (OPEN misrouting) — the original diagnosis was wrong, and the routing was
never the problem.** An INPUT PROBE proved the automation wrapper delivers `OPEN`
correctly (`RAW [OPEN] / NORMALISED [OPEN]`), so the Text → Run Shortcut configuration
described above is sound. The real cause was that the OPEN branch had **never executed on
device**: `Input Key` always resolved empty, so every automation run took the MANUAL arm.
Once that was fixed, a sequence of previously-unreachable defects surfaced one at a time.

Seven distinct parameter-defect axes were found and fixed, each invisible to the sweep
that caught the previous one; all are now asserted by build guards. The authoring rules are
recorded in `.claude/CLAUDE.md` § Conventions.

**Still open.** Symptom 1 is unresolved. Breadcrumb bisection has advanced it `B → C → D`
across builds `h`, `i`, `k`; build `k` reaches letter D and fails on date coercion —
`gettimebetweendates` feeds bare text templates into date-typed parameters at all five
sites. `Donor 7` has been supplied to settle the Date `CoercionItemClass` and is the first
task on resume.

## Solution

Symptom 2 is done. For symptom 1, follow the resume checklist in
`.planning/debug/HANDOFF.md` §10. Fix at the generator, never by hand-editing the generated
XML, and fix whole classes rather than site-by-site — bisection only ever reveals the
earliest remaining defect, so incremental fixing costs one device round trip per site.
