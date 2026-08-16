---
created: 2026-08-15T21:05:00.000Z
title: Fix the WFConditionalActionString red-operator sites and the WFItems List wrapper
area: general
severity: major
files:
  - tools/build_state_engine.py
  - .planning/debug/Donor 5.shortcut
---

## Problem

Two known, unresolved defect families were carried forward, unchanged, through every
cycle of the closed `open-routing-sequence-error` debug session because both sit past
breadcrumb J and could not affect that session's OPEN-path device measurement. Both are
now safe to pick up, since the OPEN path itself is device-confirmed working.

**1. 14 `WFConditionalActionString` sites (the "Donor 5" family).** A variable is placed
directly into a conditional's TEXT-slot operand as a template (`WFConditionalActionString
= token(...)`), the same general family as the already-fixed `WFInput.Variable`
envelope defect but a structurally different slot (text template vs. variable slot), so
the evidence that settled `WFInput.Variable` does not transfer. Zero golden-corpus
coverage, zero catalog coverage (`is.workflow.actions.conditional` is entirely absent
from the bundled ToolKit catalog), zero device coverage as of session close. `Donor 5`
was captured specifically to settle this and is on disk
(`.planning/debug/Donor 5.shortcut`) but was never analysed.

A concrete, previously-unexamined site name is now available: reviewing
`.planning/debug/Screenshot 2026-08-14 at 11.55.12⁠pm.png` during this closure (it was
never referenced anywhere in the debug session or examined before) shows an `If`
action testing `Previous Respected` `is` — rendered fully RED, including the operator
picker — which corresponds directly to `if_block("Previous Respected", 4, ...)` at
`tools/build_state_engine.py:649-650` and `:1069`. This is very likely one of the 14
already-catalogued sites, not a new class, but gives a concrete starting point instead
of an abstract count.

**2. The `WFItems` List wrapper (2 confirmed instances).** iOS wraps a variable-bearing
List row as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; this artifact's List
actions omit the wrapper, so rows render blank. The same screenshot reviewed above shows
this directly: a `List` action rendering nine consecutive rows, ALL as empty "Text"
placeholders instead of their configured content — direct, on-device visual confirmation
of the defect described in `HANDOFF.md` §6 item 4. The correct shape was already
recovered from Donors 4/4.1 (`.planning/debug/Donor 4.shortcut`,
`.planning/debug/Donor 4.1.shortcut`) but has not yet been applied to the generator.

## Solution

1. Decrypt `Donor 5.shortcut` (per `.claude/CLAUDE.md` §8's `aea decrypt` + `aa extract`
   recipe) and inspect its `WFConditionalActionString` operand shape directly — this is
   the missing device-ground-truth evidence this session's evidence hierarchy requires
   before touching any of the 14 sites.
2. Cross-check the recovered shape against the concrete site found this closure
   (`if_block("Previous Respected", 4, ...)`, `tools/build_state_engine.py:649-650`,
   `:1069`) before generalising to all 14 — confirm it is genuinely the same family, per
   this project's own "fix whole classes, never site-by-site" discipline, then run a
   full-codebase sweep for every `WFConditionalActionString`-with-token site (14
   expected) rather than patching sites individually.
3. Apply the `WFItems` wrapper shape recovered from Donors 4/4.1 to both known List
   sites (re-locate by content — line numbers shift on regeneration — starting from the
   `Previous Respected`-adjacent region shown in the reviewed screenshot as one
   candidate).
4. Add build-time recurrence guards for both fixes, following this session's own
   established pattern (guard runs before the single serialize/write; sensitivity
   verified by running it against a synthetically-reverted pre-fix artifact).
5. Fold both newly-confirmed axes into `.claude/CLAUDE.md` § Conventions' numbered axis
   list once fixed and device-confirmed — `HANDOFF.md` §9 already flags this as a
   candidate follow-up (folding cycle 15's `read_value()`/`get_value()` distinction and
   cycle 16's `pending_exit` container/leaf pattern into the same list); do all three
   documentation updates together rather than in separate passes.
6. Regenerate, validate, sign, decrypt-verify, then device-test specifically the Test
   Circle menu path and any screen reachable via the fixed conditionals (both sites are
   past breadcrumb J and were never exercised by the closed OPEN-path session).
7. Propagate to `tools/build_sentient.py` / Sentient once that fork is re-run (see the
   sibling Sentient re-fork todo) — check whether the Sentient-only `If [Audit Token]
   contains` red-render (`HANDOFF.md` §6 item 6) is the same family before treating it
   as a separate investigation.

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — cycles 8–13's own
  investigation of this family (UI evidence via `IMG_5624.jpg`–`IMG_5646.jpg`, the
  `WFCoercionVariableAggrandizement` fix for the sibling numeric-operand class).
- `.planning/debug/HANDOFF.md` §6 items 4 and 5 — this todo's origin.
- `.planning/debug/Screenshot 2026-08-14 at 11.55.12⁠pm.png` — reviewed for the first
  time during this closure; shows both defects directly on-device.
