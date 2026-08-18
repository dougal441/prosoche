---
generated: 2026-08-18
source: device UAT session 2026-08-17/18
purpose: the items `gsd-tools query audit-uat` cannot see, plus a pointer to the ones it can
---

# Master outstanding list — the non-UAT-file items

`gsd-tools query audit-uat` is the canonical cross-phase instrument and, since the
2026-08-18 parser fix, it correctly reports every `*-UAT.md` and `*-VERIFICATION.md`
item. **Run it first** — this file exists only for outstanding work that lives in
neither shape, and which a UAT-file-shaped view therefore cannot surface.

```bash
node ~/.claude/gsd-core/bin/gsd-tools.cjs query audit-uat --raw
```

## Why this file exists

Five built phases — **01, 02, 03, 08, 11** — have **no `*-UAT.md` at all**. During the
2026-08-17/18 device UAT the outstanding-work picture was assembled from UAT files, so
these phases were invisible. Three genuinely open items were missed.

## The missed items

### Phase 08 — Sentient/Aware fork, real-device behaviour unclaimed

`08-VERIFICATION.md`: `status: human_needed`, `automated_score: 22/22`,
**`human_score: 0/1`**. Its own verdict:

> both requested artifacts are built, validated, archived, signed, and delivered;
> real-device behavior is not claimed.

**Scope:** the entire Aware fork and the dual-distribution surface. Nothing about the
Aware build has ever been observed on hardware. The Aware artifact
(`212598cff4dd…`, hash-verified 2026-08-18) is **not installed** on the test device —
only Core is — so this is untested by construction.

**Linked:** `13-UAT.md` Test 6 (repeat the wrapper test on Aware) cannot run until the
Aware fork is installed. Settling both together is one device session.

### Phase 11 — a FAILED truth, still open

`11-VERIFICATION.md`: `status: gaps_found`, with this truth marked **failed**:

> The nine primitives named by BD-06 Decision 3 each perform their intervention when
> dispatched — `dimming()` and `silence()` gate on the `settings_snapshot` CONTAINER at
> condition 100.

This is the **axis-7 existence-gate trap** named in `.claude/CLAUDE.md` Conventions
rule 7: a condition-100 (`has any value`) test over a seeded container is either
unreachable or trivially true, because the container is always present. The documented
fix is to gate on a string is-not-sentinel test (condition 5) or a numeric `> 0` test.

**Corroborating device observation, 2026-08-18:** `Test a Circle → Circle 3 · Gluttony`
ran to completion with **no visible effect and no error** — consistent with a primitive
whose gate never opens. Recorded as "unclassified" in `07-UAT.md` Test 7b at the time;
this failed truth is the most likely explanation and the two should be read together.

### Phase 11 — three deferred items

From `.planning/phases/11-.../deferred-items.md`. `audit-uat` *does* surface these (3
items); they are restated here because they were dropped from the 2026-08-18 master
table and one is now device-confirmed.

1. **`src/CONFIG-BLOCK.md:36-38` threshold drift** — the doc mirror still shows the
   pre-Phase-10 curve while the live Config literal carries the raised one. Documentation
   defect; `docs/state_engine_self_check.py:10-17` holds the correct values.
2. **The header comment still says "Dumb fork"** — `WFWorkflowActions[0]`'s
   `WFCommentActionText` opens `PROSOCHE - Nine Circles (Dumb fork).` in **both** forks.
   ✅ **DEVICE-CONFIRMED 2026-08-18**: visible in the Shortcuts editor on the installed
   Core build. Cosmetic, editor-only, no user-facing run shows it.
3. **The Aware Note's static settings block reads `- AI: not used by this fork`** — the
   literal lives both in the hand-authored Note and in `manual_note_refresh()`'s shared
   snapshot template, so fixing one alone leaves them disagreeing after the first manual
   run. Needs a fork-aware template, not a string edit.

## Phases with no UAT file and nothing outstanding

- **01** — `01-VERIFICATION.md` `status: passed`, no human items.
- **02** — `02-VERIFICATION.md` `status: passed`, no human items.
- **03** — `03-VERIFICATION.md` has no `status:` field but records no gaps and no human
  items. Worth a glance if Phase 03 behaviour is ever in question, but nothing is
  formally outstanding.

## Maintenance

When a phase gains a `*-UAT.md`, delete its entry here — `audit-uat` will cover it.
This file should shrink to nothing.
