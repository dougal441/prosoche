---
created: 2026-08-16T23:24:00.000Z
title: Dimming and Silence as distinct Circles, device-proven
area: general
severity: major
files:
  - tools/build_state_engine.py:535
  - tools/build_state_engine.py:557
  - tools/build_state_engine.py:429
  - src/CONFIG-BLOCK.md:46
---

> **COVENANT OVERHAUL (2026-08-19):** BUILT (Phases 9, 11-08, 16): coercion fix, reachability fix, capture persisted before the device changes. The 'device-proven' half of this todo's own title is exactly what remains, owned by Phase 22 / `16-UAT.md` (12 tests, blank). Under BD-09, Dim is Band B soft friction in the Ambient sequence only, and Blackout (hard dim) is parked — see canon v2 §9.1.


## Problem

**User decision, 2026-08-16: Dimming and Silence are both back, on main, each as its own
distinct Circle.** This supersedes the MVP cut in
`2026-08-15-ship-readiness-cleanup.md` item 5, which is now dead — do not execute it.

Two things are true at once and the second is the risk:

**They are built and merged.** Phase 9 (`2e2261e`) landed the numeric-coercion fix for all
28 `setbrightness` (14) / `setvolume` (14) operand sites and merged to main. `dimming()`,
`silence()`, `restore_managed_settings()` and `settings_snapshot` all ship in
`c6d8737`'s regenerated artifacts.

**They have never run on a phone, and the merge made them live.** From
`docs/BUILD-NOTES.md` §18 and the current `MANIFEST.md` warning: *"Dimming and Silence
writes now execute where they previously no-opped, making `restore_managed_settings()`
load-bearing on a path with zero device evidence."* Before the coercion fix these actions
silently did nothing. Now they actually change the device's brightness and volume — and the
code that puts them back has never once executed on hardware.

`09-UAT.md` has 12 tests. Exactly one has passed: test 1, the static "coercion chip does not
render red" gate, spot-checked. Tests 2–12 — every behavioural and every failure-mode test —
have never run.

The coercion shape itself is **analogy-based, not donor-confirmed**. Per `09-RESEARCH.md`:
`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` is the shape
device-confirmed for the Donor-4.1 *conditional operand* position, but `Donor 10.shortcut`
— the only device evidence for these two actions at all — contains no variable-fed
`WFBrightness`/`WFVolume` example. Whether the same coercion is correct at a **direct
Set-action parameter** position is genuinely unknown.

Separately, the sequences do not currently express "distinct Circle each" in all three
orderings. Classic already separates them (3 Silence, 5 Dimming), but BlackMirror combines
them into `"Silence+Mirror"` (5) and `"Dimming+Mirror"` (6).

§21 makes the safety requirement absolute, and it is the reason this cannot ship
half-proven: **if the original value cannot be captured and restored reliably, do not make
the change at all.** A dim that never restores is a worse product than no dim.

## Solution

1. **Retire the cut.** Mark `2026-08-15-ship-readiness-cleanup.md` item 5 superseded by
   this todo. Fold in the now-executed
   `2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` — its
   experimental-fork framing is spent; Phase 9 merged. Leave one live trail, not three.
2. **Run `09-UAT.md` tests 2–12 on a real iPhone.** This is the gate, not a formality. Test
   1 passing only means the parameter chip is not red. The closed-loop proof is what
   matters:
   - `Get Device Details` returns a real brightness/volume value (not empty, not
     text-typed);
   - the has-any-value guard correctly *skips* the change when the read returns nothing;
   - CLOSE restores the original value exactly;
   - **then the ugly cases** — app force-quit mid-session, device restart mid-session,
     CLOSE never firing, two overlapping sessions, screen locked mid-session. Each must
     either restore or leave the user at a safe value. Never dark. Never silent forever.
     Never loud.
3. **If test 1's coercion shape turns out wrong at this parameter position**, follow
   `09-RESEARCH.md`'s fresh-donor protocol — build a donor on device with a variable-fed
   Set Brightness and decrypt it. Do not guess a second `CoercionItemClass`.
4. **Make "distinct Circle each" true in all three sequences.** Classic already is.
   Decide what BlackMirror's `"Silence+Mirror"` / `"Dimming+Mirror"` become — either split
   them into standalone entries, or keep the combination deliberately and say why. This is
   a tuning act on the single source of truth for which primitives fire when
   (`src/CONFIG-BLOCK.md` `sequences`), so it is a decision to record, not an edit to make
   quietly.
5. **Mind the slot arithmetic.** Each sequence has exactly nine slots. Alongside the
   Exile split (`2026-08-16-split-exile-into-two-circles.md`) the primitive roster runs to
   ten candidates for nine slots. Coordinate — do not let two todos each independently
   claim the same Circle position.
6. **DEV-06 is live again.** The restore-ownership fields `changed_at` /
   `changed_by_session_id` are written at 20 sites and read nowhere. That was recorded MOOT
   *conditional on the cut proceeding*. The cut is not proceeding, so DEV-06 and the
   `Session ID` scope defect it depends on both come back (SHIP CHECKLIST items 4 and 5).
7. **Emergency Restore must recover from every failure mode found in step 2.** It is the
   backstop that makes stateful environmental friction defensible at all — and it has
   itself never been tapped on a device
   (`.planning/phases/07-control-room-dumb-freeze/07-UAT.md` test 9, pending).
8. **The corrected brightness floor — SETTLED, no longer an open item.** Phase 9 revised
   BD-02's floor clause (cited, deliberately not restated here): the user's on-device
   observation is that iOS's practical minimum is dim, not black, so avoiding a particular
   value was never itself the safety property. The safety property is capture-and-restore
   reliability. That revision was scoped to the experimental fork.
   **Settled 2026-08-18 by user decision D-01** (LOCKED 2026-08-17): the floor and the dim
   target are both `0` on the main line. Plan **16-03** implemented the code half; plan
   **16-05** implemented the record half and added `docs/retired_clause_check.py`. Authority:
   `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession note. The canonical strategy is frozen
   and was not edited. **What this does NOT settle:** the capture-and-restore loop remains
   device-unproven and is still what the rest of this todo is about — see items 1–7, all
   BLOCKED on DIST-03.

## Related

- **Supersedes:** `2026-08-15-ship-readiness-cleanup.md` item 5 (the MVP cut).
- **Absorbs:** `2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md`
  (executed as Phase 9, merged).
- `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
  — the 12 tests. `09-RESEARCH.md` — the coercion evidence gap and fresh-donor protocol.
- `docs/BUILD-NOTES.md` §18 — the live-untested-path risk record.
- `2026-08-16-device-uat-nine-circles-and-sequence-switching.md` — the meta UAT; this
  todo's step 2 is its highest-priority slice.
- Canonical strategy §11 Primitives C and E, §21, §32 (Safety acceptance criteria).
