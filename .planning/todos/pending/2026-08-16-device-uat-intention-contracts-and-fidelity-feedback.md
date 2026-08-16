---
created: 2026-08-16T00:12:00.000Z
title: Device UAT — intention contracts and fidelity feedback
area: testing
severity: blocker
files:
  - tools/build_state_engine.py
  - .planning/phases/06-exits-exit-learning-contracts/06-VERIFICATION.md
---

## Problem

The Confession / Intention Contract primitive (§11 Primitive D) has never run on a
device. Phase 6 has **two** verification files with conflicting verdicts —
`06-VERIFICATION.md` says `passed`, `VERIFICATION.md` says `gaps_found` with four
`status: failed` entries. That discrepancy alone should be resolved as part of this work;
right now the project does not have a single agreed answer about whether contracts were
verified even statically.

Contracts are the mechanism the strategy leans on hardest for its distinctive claim.
§6.7's contract-fidelity metric (intended vs. actual use) is named as potentially **more
informative than total screen time**, and §14.2 makes contract auditing — not lie
detection — the entire basis of what Sentient is allowed to do. If contracts do not work,
the product degrades into a timer with dramatic naming.

The specific device risk is that contracts are the most *stateful* interaction in the
product: free text in, a duration choice in, both persisted across an app session, then
compared against a CLOSE-measured duration, then fed back into the next OPEN's Heat. Every
one of those hops crosses a boundary this project has already been burned at — text
envelopes, numeric coercion, state-shape seeding, and the CLOSE measurement itself (which
is separately unverified).

## Solution

1. **Resolve the Phase 6 verification conflict first.** Read both files, determine which
   is current, and record which one stands. Do not run a device session against an
   unclear static baseline.
2. **Depends on CLOSE.** Contract fidelity is `actual / intended`, and `actual` comes from
   the CLOSE pipeline. Run `2026-08-16-device-uat-close-pipeline-and-session-race.md`
   first — a contract test on an unverified duration measurement cannot distinguish a
   contract defect from a CLOSE defect.
3. **Cases to prove on device**, from §11 D, §13.2 and §32:
   - free-text intention is accepted and persisted verbatim (watch for silently-empty
     fields — the axis-2 envelope defect presented exactly that way);
   - each duration option works (2 / 5 / 10 / 15 / Custom), including Custom;
   - **deliberate leisure is accepted** — "watch stupid videos for ten minutes" must be a
     valid contract, not a challenge trigger. §6.1 and §32 both make this explicit, and
     getting it wrong turns the product moralistic, which §12 names as the killing failure;
   - a contract **kept** is recorded as kept, and reduces Heat on the next OPEN (§10.2
     rule 5);
   - a contract **overrun** is recorded with the overrun, and adds Heat per §10.2 rule 4
     (>50% and >2 min);
   - a blank/vague response behaves per §13.2 without attempting to parse sincerity.
4. **Check the numbers in `state.json`, not just the dialogs.** `recent_contracts` must
   hold the last ~10 per §16's bounded-window rule, and the fidelity figures must be
   arithmetically right. Recompute by hand for at least two cases.
5. **Do not let a Mirror message claim a contract that does not exist.** §13.1 is explicit:
   do not show a time-overrun message if there was no contract. Test the no-contract path
   deliberately.

## Related

- Canonical strategy §11 Primitive D, §13.2 (Dumb intent gate), §6.1 (deliberate leisure
  is legitimate), §6.7 (contract fidelity as the better signal), §23 (metrics), §32
  (contracts acceptance criteria).
- `2026-08-16-device-uat-close-pipeline-and-session-race.md` — prerequisite.
- `.planning/phases/06-exits-exit-learning-contracts/` — the two conflicting verification
  files to reconcile.
