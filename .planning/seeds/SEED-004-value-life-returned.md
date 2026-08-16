---
id: SEED-004
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: after the device-UAT backlog closes and state-shape discipline is settled — this feature adds new bounded-history keys and must not repeat the axis-7 state-shape defect class
scope: large — a full milestone; schema audit, observed-metrics display, estimate design, plus the Attention Receipt sub-feature
---

# SEED-004: Build the VALUE / LIFE RETURNED functionality

## Why This Matters

`VALUE / LIFE RETURNED` exists today only as an honest placeholder heading in the Control
Room Note (`VAL-01..04` deferred to v2). This is the feature that makes PROSOCHĒ worth
keeping installed after the novelty of the Circles wears off, and it is a hard prerequisite
for SEED-003 (the support/contribution ask) — "pay after value" is meaningless with no
value display.

The canonical strategy is unusually strict about *how* this must be built (§24): observed
metrics (opens interrupted, rapid returns broken, exits accepted, session duration
then-vs-now) may be stated directly. Estimated attention reclaimed must be **labelled an
estimate**, use a *personal* rolling-median counterfactual baseline (not a global
assumption), and be lower-bounded at zero — `100 blocked opens = X hours saved` is
explicitly forbidden without evidence.

The engineering risk is not the arithmetic — it's that `state.json` may not retain the
right shape of history to compute an honest baseline, and the strategy mandates bounded
rolling windows (§16), so "just keep more history" isn't available. Any new key must be
seeded in the bootstrap template with a build guard — this project has hit the STATE-SHAPE
axis three separate times on device already.

**A second deliverable within this feature**, added 2026-08-16: the **Attention Receipt**
— a separate, local, screenshotable Note that (1) names the Circle reached in the Dante
vocabulary ("I hit the ninth circle last night" is shareable in a way "4h12m screen time"
isn't), and (2) frames value positively — intentional exits, kept contracts, broken
rapid-return loops, estimated attention reclaimed. It is a receipt, not a scoreboard: no
streaks, no scores, no shame, never shown while the user is being blocked, local and
user-initiated, honest arithmetic with the same suppression-until-supported rule as the
main feature.

## When to Surface

**Trigger:** after the device-UAT backlog closes and the state-shape sentinel-gap
discipline is fully settled — this feature adds new bounded-history keys on top of a
schema that has already produced three device-confirmed defects of exactly this class.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches
measurement, the Control Room Note's VALUE/LIFE RETURNED section, or user-facing
value/impact display.

## Scope Estimate

**Large.** Audit what `state.json` already supports, extend the schema with bounded
aggregates and build guards, ship observed-metrics display first (deliverable on its own),
then design and label the estimate, then the Attention Receipt as a second artifact with
its own open design questions (cadence, format). Screen Time telemetry integration is
explicitly a separate, later question.

## Breadcrumbs

- Canonical strategy §23 (measurement list), §24 (Life Returned — honesty constraints),
  §15 (longitudinal memory rules), §16 (bounded JSON state), §29 (occasional
  acknowledgement of success, avoid a learned "opening always produces criticism"
  association), §5.6 (model never does arithmetic).
- `.planning/STATE.md` Deferred Items — `VAL-01..04`.
- SEED-003 (Support PROSOCHĒ) — depends on this landing first.
- `.planning/phases/999.*` device-UAT backlog and the state-shape sentinel-gap discipline
  — same class of risk this feature's new keys must not repeat.

## Notes

Originally captured as a standalone todo (`2026-08-16-build-value-life-returned.md`) with
the full "Attention Receipt" design constraints written out in detail; full original text
preserved in git history —
`git log -p -- .planning/todos/pending/2026-08-16-build-value-life-returned.md`.
