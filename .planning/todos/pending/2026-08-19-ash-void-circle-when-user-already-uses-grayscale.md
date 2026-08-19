---
created: 2026-08-19T00:00:00.000Z
title: Void or skip the Black and White circle when the user already runs grayscale
area: safety
severity: major
files:
  - tools/build_state_engine.py
  - docs/CAPABILITY-DECISIONS.md
  - .planning/spikes/005-ios-color-filters-identifier/README.md
---

## Problem

Phase 14 ships Black and White (Circle 2) as an unconditional Color Filters toggle: on when the
Circle fires, off when the app closes. **It deliberately assumes the user was not already running
Color Filters** — user decision 2026-08-19, taken to keep the phase simple and shippable.

That assumption is wrong for a real population. Someone who runs Color Filters deliberately — for
colour-blindness, migraine, or low vision — has their own setting switched **off** by PROSOCHĒ every
time they close a tracked app. The product silently degrades an accessibility accommodation it did
not set.

There is no detection available today. Spike 005 established that **no `Get*`/`Query*` intent exists
for any accessibility setting** across all 35 intents in `AccessibilityUtilities.framework`, so
"read the current state and leave it alone" cannot be built the obvious way.

## Solution

**The desired behaviour is decided already: if the user already uses grayscale, this Circle fires a
blank** — it is voided or skipped, not adapted. It must not toggle anything. What is undecided is
how to know.

Two candidate mechanisms, in cost order:

1. **Ask once, at onboarding.** A single import question or first-run prompt — "Do you use Color
   Filters / grayscale yourself?" — written to a Config flag. If yes, the Black and White Circle is
   skipped for that user and the sequence falls through to the next primitive. Cheap, honest, no new
   capability required, and it works today. The cost is one more onboarding question and it trusts
   the user's answer.

2. **Probe the `state` response parameter.** Spike 005 recorded an untested lead: every `Toggle*`
   intent in the framework declares a `state` **response** parameter. If it is consumable as a magic
   variable, and if a Turn-On response reports the state as it was *before* the operation, then
   detection is possible without asking. Both halves are unproven. This was originally scoped into
   Phase 14 as spike 011 and **cut on 2026-08-19** to keep that phase simple. If it works it is
   strictly better than asking; if it does not, option 1 stands.

Also decide what "skipped" means for the sequence: does the Circle fire a genuine no-op and the user
experiences nothing at that level, or does the sequence substitute a different primitive? Firing a
blank is the user's stated intent; confirm it does not leave a Circle that appears to do nothing at
all in a way that reads as a bug.

## Related

- Phase 14 — ships the unconditional toggle this item makes conditional.
- `.planning/spikes/005-ios-color-filters-identifier/README.md` — the no-read-back finding, and the
  `state` response-parameter lead in its Open Questions.
- `docs/CAPABILITY-DECISIONS.md` BD-01-R2 — the Ash capability record.
- Canonical strategy §21 — "do not override a pre-existing accessibility state". This item is the
  outstanding half of that rule; Phase 14 satisfies the rest.
