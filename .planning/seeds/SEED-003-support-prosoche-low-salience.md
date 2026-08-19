---
id: SEED-003
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: after SEED-004 (VALUE / LIFE RETURNED) ships — "pay after value" is meaningless with no value display
scope: small — one Note section, one manual-menu item, one Open URL action, three-option persisted choice
---

> **COVENANT OVERHAUL (2026-08-19):** Owned by Phase 28 (renumbered from 24). BD-12's licence change removes the MIT tension this seed's pay-after-value path inherited.


# SEED-003: Build the low-salience "Support PROSOCHĒ" contribution path

## Why This Matters

`SUPPORT PROSOCHĒ` is an honest placeholder heading in the Control Room Note.
Requirements `PAY-01..02` were deferred to v2. The monetization philosophy is **pay after
value**: PROSOCHĒ creates measurable value first, only then offers a way to support the
project — free, open source, un-gated, ad-free, and never selling behavioural data (§25,
§35).

The design constraint that makes this hard to get wrong is **low salience**, and the
canonical strategy's prohibitions are absolute:

- never display the payment ask while the user is being blocked (an intervention is not a
  conversion surface);
- never use guilt, never threaten loss of functionality;
- never transmit attention history to the creator — the trigger threshold is computed
  **locally**, and the user only ever *chooses* to open a link.

## When to Surface

**Trigger:** after `2026-08-16-build-value-life-returned` (SEED-004) lands — this is a
hard prerequisite, not a nice-to-have sequencing preference.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches
monetization, the Control Room Note's SUPPORT PROSOCHĒ section, or the manual menu.

## Scope Estimate

**Small.** Gate on a real local metric (Config-tunable threshold), place in the Note
section plus at most one manual-menu item, three-option ask (`Support PROSOCHĒ` / `Not
now` / `Never ask again`) persisted in `state.json` with a build guard, one `Open URL`
action to a destination confirmed with the project owner first. Clean single-toggle
removal in the generator since the product must stay forkable.

## Breadcrumbs

- Canonical strategy §25 (pay after value, four prohibitions), §26 (open-source
  principles), §27 (privacy model), §34 Phase C, §35 (payment: free forever).
- `.planning/STATE.md` Deferred Items — `PAY-01..02` currently deferred to v2.
- SEED-004 (VALUE / LIFE RETURNED) — hard prerequisite.
- SEED-002 (Open-source release readiness) — the privacy statement this feature's outbound
  link must be qualified against.

## Notes

Originally captured as a standalone todo
(`2026-08-16-build-support-prosoche-low-salience.md`); full original text preserved in git
history — `git log -p -- .planning/todos/pending/2026-08-16-build-support-prosoche-low-salience.md`.
