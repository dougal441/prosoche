---
created: 2026-08-16T00:11:00.000Z
title: Device UAT — nine Circles and sequence switching
area: testing
severity: blocker
files:
  - tools/build_state_engine.py
  - src/CONFIG-BLOCK.md
  - .planning/phases/05-nine-primitives-environmental-safety/VERIFICATION.md
---

## Problem

Exactly **one** Circle has ever fired on a real device: Circle 1, once, on build
`2026-08-15o` (`Leaving / Continue` menu, Pressure 0.1667, Heat 0). Circles 2 through 9
have never executed on iPhone. Phase 5's `passed` verdict is static analysis of the
generated graph.

The nine primitives are also the most *heterogeneous* code in the product — each one uses
different actions, and several use actions this project has already found to behave
differently on device than the plist implies. Specific known exposure:

- **Ash** currently ships as a degraded non-environmental pause (grayscale is NOT
  AVAILABLE on iOS) — its actual on-device feel is unknown and may be indistinguishable
  from The Knock, which would make two Circles effectively identical.
- **Dimming and Silence** carry 18 uncoerced `setbrightness`/`setvolume` numeric-operand
  sites deliberately deferred (axis 6b, `docs/BUILD-NOTES.md` §8 table) and are subject to
  a pending MVP-cut decision — so whatever ships today is unproven either way.
- **The Voice** (`speaktext`) had its parameter key corrected late (DEV-C3-03, `WFText`
  not `WFInput`) and has never been heard on device.
- **Ice** is covered by its own UAT todo, not this one.

Beyond individual primitives, §32 requires two structural properties that only a device
run can show: the **sequence can be changed** (Classic / Black Mirror / Ambient) with
Circle mapping changing accordingly, and **a stronger Circle does not necessarily show
every earlier prompt** — i.e. Circles compose as designed rather than stacking into an
unusable pile of dialogs.

## Solution

1. **Use `Test a Circle` from the manual menu** as the primary harness — it exists
   precisely for this and avoids having to grind real Pressure up to 20 to see Circle 9.
   Note that `Test a Circle` was itself broken on device once already (the `sequence`
   Set Dictionary Value error, since closed) so confirm it works before trusting it as a
   test instrument.
2. **Fire all nine, in all three sequences.** For each: does the intervention appear, is
   the copy correct and non-empty, is the exit/dismiss path present and reachable, how
   long does it take, and does it return control cleanly. Blank text is the specific
   failure to watch for — the `WFTextTokenString` envelope defect (axis 2, 367 sites)
   presented exactly as silently-empty fields, and the `WFItems` List-wrapper defect
   (still open) is known from a screenshot to render list rows blank.
3. **Confirm the three sequences genuinely differ**, and that Circle mapping follows the
   Config threshold tables per profile (§10.5 — Paradise/Limbo/Inferno). A sequence
   change that does not change what the user sees is a silent failure.
4. **Judge composition, not just firing.** §32: a stronger Circle must not necessarily
   replay every earlier prompt. Count total taps at Circles 6–9 and sanity-check against
   §30's intervention-fatigue failure mode.
5. **Note but do not fix UX here.** Copy and interaction-cost rewriting belongs to
   `2026-08-16-optimise-ux-onboarding-and-functionality.md`; this todo establishes what
   actually happens today so that work has a baseline.
6. **Safety floors are pass/fail, not observations** (§21, §32): no zero brightness, no
   unsafe volume, nothing that strands accessibility. Any violation is a stop-the-line
   defect regardless of how the rest of the run went.

## Related

- Canonical strategy §11 (the nine primitives), §12 (candidate sequences and the testing
  philosophy), §21 (environmental state safety), §32 (Circles acceptance criteria).
- `docs/BUILD-NOTES.md` §8 type-audit table (the 18 deferred brightness/volume sites).
- `2026-08-16-grayscale-ash-capability-donor-test.md` — may change what Ash is.
- `2026-08-16-reintroduce-and-validate-dimming-and-silence-stateful-restor.md` — may
  change what Dimming/Silence are.
- `2026-08-16-device-uat-circle-ix-cooldown-and-route-out-of-ice.md` — Circle 9 is
  covered there, not here.
