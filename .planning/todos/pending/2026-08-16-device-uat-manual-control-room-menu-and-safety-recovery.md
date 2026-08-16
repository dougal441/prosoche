---
created: 2026-08-16T00:15:00.000Z
title: Device UAT — manual Control Room menu and safety recovery
area: testing
severity: blocker
files:
  - tools/build_state_engine.py
  - .planning/phases/07-control-room-dumb-freeze
---

## Problem

Exactly one manual-menu item has any device evidence — `Open Control Room` — and even that
is **partial**: the closing device report of the `open-routing-sequence-error` session did
not explicitly confirm the `filter.notes` fix (Finding 2), so the "does a note picker still
appear?" check remains locally verified only. Every other menu item is untested on iPhone.

The menu is the product's entire administrative surface (§18): Status, Open Control Room,
Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today,
Emergency Restore — plus Toggle On-Device AI and Test Model on Sentient.

Two of those carry outsized risk:

- **Emergency Restore** is the designed escape hatch (§21). It must clear cooldown, active
  session, and any recoverable brightness/volume/colour change. If it does not work, every
  other safety argument in the product is void — it is the thing that makes stateful
  friction defensible in the first place.
- **`Test a Circle`** is the test harness the other UAT todos depend on, and it was itself
  broken on device once (the `sequence` Set Dictionary Value error). It must be confirmed
  working before it can be trusted as an instrument.

This todo also owns §32's **Safety** acceptance criteria that are recovery-shaped rather
than menu-shaped, because they are exercised the same way: corrupt/missing `state.json`
and a deleted Control Room Note must each self-heal rather than fail.

## Solution

1. **Walk every menu item on device**, confirming each does what it claims and returns
   cleanly to the menu or exits:
   - Status — shows real numbers, not blanks (the axis-2 empty-field defect presented
     exactly as plausible-looking blank text);
   - Open Control Room — **and explicitly confirm no note picker / list of every note
     appears**. This is the outstanding Finding 2 check carried over from the closed debug
     session and separately listed in `2026-08-15-ship-readiness-cleanup.md` item 4;
   - Sync My Profile — extracts the `MY PHONE, ON PURPOSE` section and mirrors it into
     `state.json` (§7.3). Confirm it does not parse the whole Note on the hot path;
   - Change Profile / Change Sequence — persist, and demonstrably change subsequent Circle
     mapping (cross-check with the Circles UAT);
   - Toggle Voice — persists and actually gates The Voice;
   - Test a Circle — all nine selectable and firing;
   - Reset Today — resets the behavioural day's counters without destroying history;
   - **Emergency Restore** — clears cooldown, clears active session, restores any managed
     setting. Test it *while* in Ice and *while* a session is active, not from a clean
     state, since a clean state proves nothing.
2. **Prove idempotence** (§32 Bootstrap): later manual runs must never overwrite existing
   state or create a second Control Room Note. Run the menu repeatedly and confirm exactly
   one Note exists.
3. **Prove the recovery cases** (§32 Safety):
   - delete the Control Room Note → next run recreates it, populated, without crashing;
   - corrupt `state.json` (malformed JSON, and separately a valid-JSON-but-wrong-schema
     file) → safe recovery, not a hard error;
   - delete `state.json` entirely → bootstrap re-runs cleanly.
   These must each be tested from *all three* invocation modes where §32 requires it —
   manual, OPEN, and CLOSE — since the self-healing chain was deliberately hoisted above
   the router for exactly that reason.
4. **Note the Sentient-only items as out of scope here** — Toggle On-Device AI and Test
   Model belong with the Sentient re-fork and the On-Device literal work, not this pass.
5. Do this **before** stripping debug scaffolding, so failures are localisable.

## Related

- Canonical strategy §18 (second manual run / menu), §21 (Emergency Restore), §17 (Note
  structure), §7.3 (profile sync), §32 (Bootstrap and Safety acceptance criteria).
- `2026-08-15-ship-readiness-cleanup.md` item 4 — the outstanding Control Room open-flow
  device check this todo absorbs.
- `2026-08-16-device-uat-nine-circles-and-sequence-switching.md` — depends on `Test a
  Circle` being confirmed here.
- `2026-08-16-device-uat-circle-ix-cooldown-and-route-out-of-ice.md` — Emergency Restore
  clearing Ice is cross-checked there.
