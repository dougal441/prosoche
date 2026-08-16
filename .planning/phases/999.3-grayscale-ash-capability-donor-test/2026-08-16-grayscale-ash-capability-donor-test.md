---
created: 2026-08-16T00:16:00.000Z
title: Grayscale / Ash capability donor test
area: general
severity: minor
files:
  - docs/CAPABILITY-DECISIONS.md
  - docs/BUILD-NOTES.md
  - tools/build_state_engine.py
---

## Problem

Ash (§11 Primitive B) is the one intervention primitive that was **cut rather than built**.
CAP-20 was resolved `NOT AVAILABLE` and BD-01 degraded Ash to a self-contained
non-environmental visual pause, on the basis that:

- the only Color Filters action anywhere in the bundle is
  `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent`, tagged
  `macOS 27` only in the v78 parameter catalog;
- it is **absent from the bundled iOS-27-Simulator snapshot entirely** (direct lookup
  returned `False`) — unlike the Notes actions, which were absent from the catalog but
  obviously real on iOS;
- no read-back mechanism exists, so §21's "do not blindly disable a pre-existing
  accessibility state" rule could not be satisfied even if a toggle existed.

That verdict was reached from **bundled catalog data only**. This project has since
established, repeatedly and expensively, that the catalog is incomplete and that the
decisive evidence channel is a **user-built donor shortcut decrypted from the target
iPhone** — it sits at the top of the evidence hierarchy in `.claude/CLAUDE.md`, above the
golden corpus and the catalog. A donor has never been built for this question.

This matters because §6.5 gives grayscale the **strongest single piece of research support
in the entire strategy**: a preregistered randomized field experiment (112 participants)
found grayscale produced an immediate significant reduction in objectively measured screen
time, larger and faster than goal-setting. Ash may be the highest-evidence primitive in the
product, and it is currently the only one not implemented as designed.

A `Set Colour Filters.shortcut` file already sits in `.planning/debug/` — it was never
analysed.

## Solution

1. **Decrypt the donor already on disk.** `.planning/debug/Set Colour Filters.shortcut`
   exists and has never been opened. Run the `aea decrypt` + `aa extract` recipe
   (`.claude/CLAUDE.md` §8) against it first — it may settle the whole question with no
   new device work at all. Establish: does the action exist on iOS 26, what identifier
   does the device actually emit, and what is its real parameter shape?
2. **If it does exist**, the capability answer is only half the problem. §21 and BD-01 both
   turn on **read-back**: PROSOCHĒ must not clobber a user who already runs Color Filters
   deliberately (colour-blindness, migraine, low vision). Establish whether current state
   is readable — probably via `Get Device Details`, whose enum was already the surprise
   answer for brightness/volume read-back (CAP-17/19). If state cannot be read, §21's rule
   stands and the honest options are the ones BD-01 already named: skip it, or require the
   user to opt into a known PROSOCHĒ-managed configuration.
3. **If it does not exist on iOS**, close CAP-20 as confirmed-by-donor rather than
   confirmed-by-absence-from-a-snapshot, and leave BD-01's fallback standing. That is a
   materially stronger record than what exists today and costs one decryption.
4. **Update the audit trail either way** — `docs/CAPABILITY-DECISIONS.md` BD-01 and
   `docs/BUILD-NOTES.md` CAP-20. A verdict reached from a donor supersedes a verdict
   reached from the catalog; say so explicitly rather than quietly overwriting.
5. **Only then decide whether to rebuild Ash.** If it becomes buildable with safe
   read-back, it should be reinstated as the designed primitive — but treat that as new
   authoring against all seven parameter axes, and re-run the Circles UAT.
6. **Do not guess the identifier or the enum cases** under any circumstance. This is the
   exact class the project's do-not-fabricate rule exists for.

## Outcome — 2026-08-16 (steps 1–4 done, step 5 open)

Resolved by `.planning/spikes/005-ios-color-filters-identifier/`. Note the premise of this
todo was itself out of date: BD-01-R had already reversed CAP-20 to `VERIFIED` from catalog
reasoning before the donor was ever opened. The donor confirmed that conclusion and
**corrected its build recipe**, which mattered more.

1. ✅ **Decrypted three donors** — the one on disk, plus `Donor 9` and `Donor 9.1`, built to
   order mid-spike, each correcting a conclusion the previous pass had drawn from schema
   rather than from a device. Color Filters exists on iOS 26 as
   `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`. Both
   BD-01 and BD-01-R argued the question using `UAToggleColorFiltersIntent` — the macOS
   twin. The iOS identifier is in none of the three bundled snapshots, so no amount of
   catalog work could have found it. Serialization: **`state` is a bool-as-integer, `1` = On
   and `0` = Off**; `operation` is a string case id that is **elided when Turn**, so
   authoring omits it; no `ShowWhenRun`.

   ✅ **Both legs are donor-confirmed** — apply (`state = 1`) and restore (`state = 0`). No
   gate remains on CIRC-02's write path.
2. ✅ **Read-back: still none.** No `Get*`/`Query*` intent exists for any accessibility
   setting across all 35 intents in `AccessibilityUtilities.framework`. §21's opt-in remedy
   (`safety.ash_managed_color_filters`) therefore stands exactly as BD-01-R wrote it. One
   untested lead recorded: every `Toggle*` intent declares a `state` *response* parameter,
   which could support a toggle-probe read at the cost of one visible flicker.
3. n/a — it does exist.
4. ✅ **Audit trail updated.** `docs/CAPABILITY-DECISIONS.md` BD-01-R2 (supersedes BD-01-R's
   Action/Parameters/Design); `docs/BUILD-NOTES.md` CAP-20 row, summary table, DEV-01 marked
   withdrawn, §7 closure claims corrected, new §9 revisions table.
5. ⬜ **Open — rebuild Ash.** Now fully unblocked, but out of scope here: it is new authoring
   against all seven parameter axes plus a re-run of the Circles UAT.
6. ✅ Nothing shipped as a guess — but the spike did assert two wrong values from Apple's
   `.intentdefinition` before donors refuted them (`operation` as an integer, then
   `state = 2` for Off). The second would have shipped a restore leg that leaves users stuck
   in grayscale. Lesson recorded in `CONVENTIONS.md`: an `.intentdefinition` describes the
   intent's type system, not the plist encoding, and does not outrank a donor.

**One optional follow-on** remains in the spike README's Open Questions: whether the `state`
*response* parameter is consumable as a magic variable. If it is, Ash could detect and
preserve a user's pre-existing filter instead of requiring them to opt out — an enhancement
to §21 compliance, not a gate.

## Related

- Canonical strategy §6.5 (grayscale evidence — the strongest research support in the
  document), §11 Primitive B, §21 (accessibility safety, do not override a pre-existing
  state).
- `docs/CAPABILITY-DECISIONS.md` BD-01, `docs/BUILD-NOTES.md` CAP-20.
- `.planning/debug/Set Colour Filters.shortcut` — the unanalysed donor.
- `.planning/debug/HANDOFF.md` §5 (donor channel has been decisive every time it was used).
- `2026-08-16-device-uat-nine-circles-and-sequence-switching.md` — Ash's on-device feel is
  assessed there; this todo may change what Ash is first.
