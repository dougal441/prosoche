---
created: 2026-08-16T00:00:00.000Z
title: Build the low-salience "Support PROSOCHĒ" contribution path
area: product
severity: minor
files:
  - tools/build_state_engine.py
  - src/CONFIG-BLOCK.md
---

## Problem

`SUPPORT PROSOCHĒ` is, like its sibling, an honest placeholder heading in the Control Room
Note. Requirements `PAY-01..02` are recorded as **deferred to v2** in
`.planning/STATE.md`. This todo promotes them, with the explicit user constraint that the
ask must be **low salience**.

The product must stay free, open source, un-gated, ad-free, and must never sell
behavioural data (§25, §35). The monetization philosophy is **pay after value**: PROSOCHĒ
creates measurable value first, and only then offers a way to support the project.

Low salience is the design constraint that makes this hard to get wrong-by-default. The
canonical strategy's prohibitions are absolute and worth restating because they are easy
to violate accidentally:

- **never display the payment ask while the user is being blocked** — an intervention is
  not a conversion surface, and mixing them would poison the intervention itself;
- never use guilt;
- never threaten loss of functionality;
- never transmit the user's attention history to the creator to calculate anything.

The last point is architecturally load-bearing: the milestone that triggers the ask is
computed **locally**, and nothing about it leaves the device. The user only ever
*chooses* to open a link.

## Solution

1. **Gate on the value feature.** This cannot ship before
   `2026-08-16-build-value-life-returned.md` — "pay after value" with no value display is
   just an ask. The trigger threshold should reference a real local metric (§25 suggests
   ~100 automatic opens interrupted, a threshold of estimated attention reclaimed, or ~30
   active days). Put the threshold in the Config block so it is tunable, not hardcoded.

2. **Place it where it has near-zero salience.** Default placement is the `SUPPORT
   PROSOCHĒ` section of the Note plus, at most, one manual-menu item — surfaces the user
   reaches *deliberately*. Explicitly out of bounds: any OPEN-path Circle, any
   intervention screen, any Ice/cooldown screen, any notification.

3. **Ask at most once, and honour "never".** Offer exactly three options — `Support
   PROSOCHĒ` / `Not now` / `Never ask again` — and persist the answer in `state.json`
   (seeded in the bootstrap template with a build guard, per the state-shape discipline
   this project has been bitten by three times). `Never ask again` must be permanent and
   must never be re-prompted by a later milestone.

4. **Copy tone.** Follow §25's own example: state the observed numbers, state that
   PROSOCHĒ is free and open source permanently, then offer pay-what-you-think-it-was-
   worth. No urgency, no scarcity, no guilt, no exclamation marks.

5. **The link itself.** A single `Open URL` to the user's own site / GitHub Sponsors /
   pay-what-you-want link. Confirm the destination URL with the project owner before
   building it in — it is the one outward-facing element in an otherwise fully local
   product, and it should not be guessed. Note that opening an external link is the only
   moment PROSOCHĒ leaves the device; the README's privacy statement (§26) should say so
   plainly rather than claiming an unqualified "nothing ever leaves the phone."

6. **Keep it removable.** Since the product is open source and forkable (§26), the ask
   should be a clean, single-toggle removal in the generator, not threaded through the
   engine.

## Related

- Canonical strategy §25 (pay after value, with the four prohibitions), §26 (open-source
  principles), §27 (privacy model), §34 Phase C, §35 (payment: free forever).
- `2026-08-16-build-value-life-returned.md` — hard prerequisite.
- `.planning/STATE.md` Deferred Items — `PAY-01..02` currently deferred to v2.
