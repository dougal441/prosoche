---
created: 2026-08-16T00:17:00.000Z
title: Reintroduce and validate Dimming/Silence stateful restore on an experimental fork
area: general
severity: major
files:
  - tools/build_state_engine.py
  - docs/BUILD-NOTES.md
---

## Problem

**⚠️ This todo deliberately conflicts with `2026-08-15-ship-readiness-cleanup.md`, and the
conflict is intentional — user decision, 2026-08-16.**

`2026-08-15-ship-readiness-cleanup.md` carries an explicit user decision to **cut
brightness/volume manipulation from the MVP**. That cut still stands and should still be
executed on the main line. This todo does **not** reverse it. Instead it runs the opposite
experiment in parallel, on a separate fork, so the cut is made on evidence rather than on
the current state of the code:

- **main line:** cut proceeds — `restore_managed_settings`, `dim()`, `silence()`,
  `settings_snapshot` and the 18 uncoerced `setbrightness`/`setvolume` sites come out;
- **experimental fork:** the stateful capture-and-restore design is finished properly and
  tested on device;
- **later:** if it demonstrably works and is safe, it may be brought back into main. If it
  does not, the cut was correct and is now justified rather than merely convenient.

Whoever picks either one up must know the other exists. Both files cross-reference.

The underlying substance: Dimming (§11 Primitive E) and Silence (§11 Primitive C) were
originally specified to degrade to non-stateful message-only variants, then **promoted** to
full stateful capture-and-restore when CAP-17/CAP-19 verified brightness and volume
read-back via `Get Device Details`' `WFDeviceDetail` enum (`Current Brightness`,
`Current Volume`, both cross-platform tagged). That promotion was never finished: the 18
numeric-operand sites were left uncoerced during the cycle-14 type audit (axis 6b,
`docs/BUILD-NOTES.md` §8 table — the only offenders left unfixed), so what ships today is
a stateful design with a known-defective operand layer, tested by nobody.

§21 makes the requirement absolute and it is the reason this cannot be half-built:
**if the original value cannot be captured and restored reliably, do not make the change
at all.** A dim that never restores is a worse product than no dim.

## Solution

1. **Let the main-line cut proceed independently.** Do not block
   `2026-08-15-ship-readiness-cleanup.md` on this work, and do not quietly leave the code
   in because this experiment exists.
2. **Branch from the device-confirmed Dumb build** (`2026-08-15o` lineage, provenance
   guard passing) so the experiment inherits every fix from the closed debug session.
3. **Fix the 18 deferred sites properly** — `setbrightness.WFBrightness` (14) and
   `setvolume.WFVolume` (4) need the coercion aggrandizement per axis 6. Establish the
   correct `CoercionItemClass` from donor or corpus evidence; do not guess it. Extend the
   numeric-audit build guard to stop exempting them.
4. **Prove capture-and-restore as a closed loop on device**, which is the entire point:
   - read current brightness/volume via `Get Device Details` and confirm a real value
     comes back (not empty, not text-typed);
   - apply the change, confirm the has-any-value guard correctly skips the change when the
     read returns nothing;
   - restore on CLOSE and confirm the original value returns exactly;
   - **then test the ugly cases**: app force-quit mid-session, device restart mid-session,
     CLOSE never firing, two overlapping sessions. Each must either restore or leave the
     user at a safe value — never dark, never silent-forever, never loud.
5. **Hold the §21 safety floors as pass/fail**: never zero brightness (~10–15% prototype
   dim), never raise volume as punishment, never startling output.
6. **Emergency Restore must recover from every failure mode found** (§21) — it is the
   backstop that makes the experiment defensible.
7. **DEV-06 (restore-ownership check — `changed_at`/`changed_by_session_id`, written at 20
   sites, read nowhere) becomes live again if this succeeds.** It was recorded as MOOT
   *conditional on the cut proceeding*; on this fork it is not moot, and the `Session ID`
   scope defect it depends on comes back with it (SHIP CHECKLIST items 4 and 5).
8. **Report a verdict, not just a diff.** The deliverable is an answer to "does stateful
   environmental friction work safely on iOS 26 Shortcuts?" — a clear yes with evidence, or
   a clear no that retires the idea.

## Related

- **Conflicts with (deliberately):** `2026-08-15-ship-readiness-cleanup.md` — the
  brightness/volume MVP cut, which proceeds on main regardless.
- Canonical strategy §11 Primitives C and E, §21 (environmental state safety — the
  capture-or-skip rule), §32 (Safety acceptance criteria).
- `docs/BUILD-NOTES.md` §8 type-audit table (the 18 deferred sites), §17 (DEV-06 and the
  SHIP CHECKLIST items 4/5 this revives).
- `docs/CAPABILITY-DECISIONS.md` BD-02, BD-03 (the promotion to stateful design).
