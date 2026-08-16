---
created: 2026-08-16T00:14:00.000Z
title: Device UAT — Circle IX cooldown and the route out of Ice
area: testing
severity: blocker
files:
  - tools/build_state_engine.py
  - src/CONFIG-BLOCK.md
---

## Problem

Circle IX — Ice (`Treachery` / **Frozen** under Build Addendum 01) is the only Circle that
can leave the user in a *persistent* state rather than a momentary one, and it has never
run on a device.

It gets its own UAT separate from the other eight Circles for three reasons:

1. **It is the only failure that traps the user.** Every other Circle ends when its dialog
   ends. Ice holds a `cooldown_until` timestamp and changes behaviour on every subsequent
   OPEN until it expires. A defect here does not annoy — it strands. §22 is unambiguous:
   *"There must be a route out. The product should not trap the user in permanent
   escalating punishment."*
2. **`cooldown_until` uses a sentinel** that was explicitly downgraded to "device-verified
   safe, leave untouched" during the debug session — meaning it was reasoned about, not
   exercised through a real cooldown cycle. Its inertness was confirmed for runs that
   never entered Ice.
3. **It must be model-free.** §11 Primitive I, §14.4 and §22 all require Ice to be
   deterministic; the Sentient fork must not be able to influence it. That is a property
   to *verify*, not assume, once Sentient is back in play.

## Solution

1. **Reaching Ice legitimately is itself part of the test**, but grinding Pressure to 20
   by hand is impractical — use `Test a Circle` for the mechanics, then do at least one
   run that reaches Ice through genuine accumulated Pressure to confirm the threshold
   mapping actually gets there. A Circle that is unreachable in practice is a different
   bug from one that misbehaves.
2. **Cases to prove**, from §22 and §32:
   - entering Ice applies the deterministic cooldown for the active profile (~60s
     Paradise / ~3m Limbo / ~5m Inferno — Config-tunable prototype values);
   - a target-app OPEN **during** Ice ejects/redirects immediately;
   - **blocked attempts during Ice do not endlessly inflate Heat** (§22) — this is the
     specific runaway to check, since it would compound the trap;
   - remaining cooldown is shown if practical;
   - **Ice expires on its own**, provides Heat relief, and clears `cooldown_until`;
   - the user is genuinely out afterwards — the next OPEN behaves normally.
3. **Verify `cooldown_until` across the whole cycle**, reading `state.json` at each stage:
   unset → set with a real future timestamp → observed as active → cleared on expiry. The
   sentinel's behaviour under a real cycle is exactly what has never been exercised.
4. **Test the interruption cases**, because they are how a trap actually happens in the
   wild: device restart mid-cooldown, behavioural-day rollover mid-cooldown, and clock
   change. Ice must not survive as an unexpirable state in any of them.
5. **Confirm Emergency Restore clears Ice** (§21) — it is the designed escape hatch and
   is covered functionally in the Control Room UAT, but the Ice-specific case belongs here.
6. **Confirm no model involvement** (§14.4: Circle IX has no model). Re-check after the
   Sentient re-fork lands, since that is when the property could regress.
7. If the physical-unlock idea proceeds
   (`2026-08-16-physical-unlock-for-circle-ix-ice.md`), this UAT is its prerequisite and
   its safety floor: the time-bound expiry proven here is what guarantees an unreachable
   QR code or NFC tag cannot convert a cooldown into an indefinite lockout.

## Related

- Canonical strategy §11 Primitive I, §22 (Circle IX — Ice, and the route out), §21
  (Emergency Restore), §14.4 (Circle IX has no model), §32 (Circles acceptance criteria).
- `.planning/debug/HANDOFF.md` §6 — `cooldown_until` sentinel left as historical context.
- `2026-08-16-physical-unlock-for-circle-ix-ice.md` — depends on this.
