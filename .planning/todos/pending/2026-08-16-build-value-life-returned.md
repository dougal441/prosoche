---
created: 2026-08-16T00:00:00.000Z
title: Build the VALUE / LIFE RETURNED functionality
area: measurement
severity: major
files:
  - tools/build_state_engine.py
  - src/CONFIG-BLOCK.md
  - docs/BUILD-NOTES.md
---

## Problem

`VALUE / LIFE RETURNED` exists today only as an honest placeholder heading in the Control
Room Note (deliberately left un-embellished per Phase 7's ROOM-08 and canonical strategy
§17). The underlying requirements `VAL-01..04` were **deferred to v2** at requirements
definition and are recorded as such in `.planning/STATE.md`'s Deferred Items table. This
todo promotes them back into scope.

This is the feature that makes PROSOCHĒ worth keeping installed after the novelty of the
Circles wears off, and it is a hard prerequisite for the support/contribution ask (see
`2026-08-16-build-support-prosoche-low-salience.md` — "pay after value" is meaningless
with no value display).

The canonical strategy is unusually strict about *how* this must be built, and the
strictness is the point (§24):

- **Observed metrics may be stated directly** — opens interrupted, rapid returns broken,
  exits accepted, median session duration then vs. now. These are counts PROSOCHĒ already
  has or can derive.
- **Estimated attention reclaimed must be labelled an estimate**, must use a *personal*
  rolling-median counterfactual baseline (not a global assumption), and must be lower-
  bounded at zero. `100 blocked opens = X hours saved` is explicitly forbidden without
  evidence. §15's rules also apply: prefer medians to means, don't invent trends, only
  make comparative claims when enough data exists.

The engineering risk is not the arithmetic — it is that `state.json` may not currently
retain the right shape of history to compute an honest baseline. The strategy mandates
rolling windows plus aggregates (§16: last ~20 sessions, last ~10 contracts, per-exit
aggregates, bounded daily records), so any baseline design must work from bounded data —
"just keep more history" is not available.

## Solution

1. **Audit what `state.json` can actually support today.** Before designing any metric,
   enumerate which of §23's measurement list is already recorded, derivable, or absent:
   OPEN count, rapid-return count, session duration, declared duration, contract overrun,
   Circle distribution, redirects, exit selected, time-to-next-return, daily Heat maxima,
   resets, profile changes. Write the answer down — the gap list drives everything after.

2. **Extend the schema deliberately, with bounded aggregates.** Add whatever daily/rolling
   aggregate records are needed, respecting §16's bounded-array rule. Every new key must be
   **seeded in the bootstrap template** — this project has now hit the STATE-SHAPE axis
   (axis 7) three separate times on device (`settings_snapshot`, `pending_exit`, and
   `exit_events` still open); a flat read of an entirely-absent key is a hard runtime
   error. Add a `verify_*_seed()` build guard for each new key, matching the existing
   `verify_pending_exit_seed()` precedent.

3. **Build the observed-metrics display first.** Counts only, no estimation. This is
   deliverable on its own, is honest by construction, and lets the Note section become
   real instead of a placeholder. Surface it in the manual menu and in the Note's
   `VALUE / LIFE RETURNED` section.

4. **Then design the estimate, and label it.** `expected comparable session duration −
   observed session duration`, lower bound zero, baseline from personal rolling medians
   conditioned on (at minimum) app and contract type — deliberate vs. automatic. Present
   as **Estimated Attention Reclaimed** / **Estimated Life Returned**, never as an exact
   figure, and suppress it entirely until the sample size supports it (§15).

5. **Treat Screen Time telemetry as a separate, later question.**
   `com.apple.intelligenceplatform...CalculateAppUsageIntent` ("Get App & Website
   Activity") is VERIFIED present in the ToolKit with a full parameter schema, but §24 is
   explicit that its **runtime granularity must be inspected on device before use** — do
   not assume arbitrary historical querying. The value feature must be fully useful
   without it; treat it as an optional enrichment, and if it is picked up, verify the
   `during`/`activityType` enum cases via donor evidence rather than guessing.

6. **Do not let the model near any of this.** §5.6 and the project's determinism
   constraint both forbid the model from doing arithmetic. Sentient may *phrase* a value
   summary; it may never compute one.

## The Attention Receipt (added 2026-08-16)

A second deliverable within this feature: a **separate local Note** — the *Attention
Receipt* — designed to be screenshotted and shared. Two jobs at once:

**1. Mythology.** It names the Circle the user reached, in the Dante vocabulary
(`Limbo` … `Treachery` / `Frozen`, per Build Addendum 01 §1/§5). "I hit the ninth circle
last night" is a shareable sentence in a way that "my screen time was 4h12m" is not. The
naming is already the most distinctive thing about the product; the receipt is what makes
it legible to someone who has never installed it.

**2. Value, framed positively.** The counts should lead with what the user *did*, not what
they were stopped from doing:

- intentional exits taken, and the thing they went and did instead;
- contracts kept — sessions that stopped when the user said they would;
- rapid-return loops broken;
- automatic opens interrupted;
- estimated attention reclaimed, **labelled as an estimate**.

Design constraints, all inherited and non-negotiable:

- **It is a receipt, not a scoreboard.** No streaks, no scores, no shame, no comparison to
  other people. §29 requires occasional acknowledgement of success and explicitly warns
  against a learned association that opening an app always produces criticism — a receipt
  that only ever tallies failures would build exactly that.
- **Honest arithmetic, same rules as the rest of this todo** (§24). Never
  `100 blocked opens = X hours saved`. Suppress the estimate entirely until the sample
  supports it. A shared artifact makes an inflated number worse, not better — it gets
  screenshotted and repeated.
- **Local and user-initiated.** It is a Note the user chooses to open and share. PROSOCHĒ
  does not post, does not upload, does not phone home (§27). Sharing is an act the user
  performs entirely outside the product.
- **Never shown while the user is being blocked.** Same rule as the support ask (§25) — an
  intervention is not a marketing surface.
- **The user's own data is on it.** Before suggesting sharing anywhere in the copy,
  consider that the receipt may carry app names and behavioural detail. Default to
  including only what is safe to show a stranger, and let anything more specific be opt-in.

Open design questions to settle when this is picked up: whether the receipt is generated on
a cadence (daily/weekly), on a milestone, or on demand from the manual menu; and whether it
is a Note at all versus something more visual — a Note is the honest default given the
architecture (§5.4), and the strategy's no-second-machine-store rule means it must be
human-readable output, not a new data store.

## Related

- Canonical strategy §23 (measurement list), §24 (Life Returned — record now, design
  later, with the honesty constraints), §15 (longitudinal memory rules), §16 (bounded
  JSON state).
- `.planning/STATE.md` Deferred Items — `VAL-01..04` currently marked deferred to v2;
  update that row if this todo is actioned.
- `2026-08-16-build-support-prosoche-low-salience.md` — depends on this landing first.
- `2026-08-15-close-state-shape-sentinel-gaps.md` — same state-shape discipline; worth
  closing before adding new keys.
