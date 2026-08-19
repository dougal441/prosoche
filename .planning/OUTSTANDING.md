---
generated: 2026-08-18
updated: 2026-08-19
source: device UAT sessions 2026-08-17/18 and 2026-08-18/19
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

## ✅ UPDATE 2026-08-19 — a device UAT HAS now run against the shipped build

**The re-run the section below asks for has partly happened.** A `/gsd-verify-work` session for
phases 4, 6 and 9 ran on 2026-08-18/19 against **Core `873fa3db…9f10`, 231,148 bytes** — the
artifact currently on disk — hash-matched to `16-UAT.md`'s header before testing, on a **fresh
install with `state.json` deleted first**. Results from that session are therefore *"verified on
the shipped build"* in the sense this file demands, and the caveat below does not apply to them.

Where they landed: `04-UAT.md`, `06-UAT.md` and `16-UAT.md` (all now `status: partial`), with the
full evidence in `.planning/debug/device-state/README.md` (23 findings, five preserved state
files).

**⚠ And then Phase 15 superseded that build too, before this work merged.** Phase 15 rebuilt and
re-signed both forks and bumped `schema_version` 4 → 5, so the `873fa3db…` artifact tested above
is no longer what ships and this file's caveat now applies to the newer session as well. Most of
the findings are generator-level or are iOS runtime semantics and survive any rebuild; the one
that genuinely needs re-running is the **positive** result — the volume capture/restore proof —
because a proof should not be inherited across a re-sign. The provenance block at the top of
`.planning/debug/device-state/README.md` sets out which is which.

**The re-check is now trivial, though:** `schema_version` alone distinguishes the two builds
(4 vs 5), so the fingerprint technique below no longer even needs the `settings_snapshot` shape.

**Of the two open blockers this file names:**

- **Control Room Note resolution — RE-CONFIRMED on `873fa3db`.** It did not disappear in the
  Phase 11 rebuild. Reproduced on a **fifth** state-changing path (`Emergency Restore`), and the
  session added the clean negative control that removes the last ambiguity from its
  characterisation. Recorded in
  `.planning/todos/pending/2026-08-17-note-entity-chooser-on-clean-install.md`.
- **Mirror axis-4 unfilled picker — NOT re-checked.** Circle 7 (`Mirror` in `Classic`) was never
  reached on this build; the session topped out at Circle 6. Still open against `873fa3db`.

**One new blocker was found on the shipped build** and is filed as gap **G-06-12** in
`06-UAT.md`: `enabled_exits()` filters nothing, so exits the user has disabled are offered,
selectable and fully routable.

**A build-identity technique that removes the need for this whole caveat in future.** This file
and `16-UAT.md` both state that which build is installed cannot be determined by inspection,
because the signer strips `WFWorkflowName`. That is true of the shortcut and **false of the state
it writes**: the `settings_snapshot` seed shape is emitted by no build before decision D-02. So
*delete `state.json`, run once, read `settings_snapshot`* fingerprints the install. Finding F-8.

## ⚠ The device UAT results from the 2026-08-17/18 session are against a SUPERSEDED build

The 2026-08-17/18 device UAT ran against **Core `b07497ba…ac5b`, 233,802 bytes**, which
was the shipped artifact at the time and was hash-matched to `13-UAT.md`'s header before
testing. Phase 11 has since rebuilt and re-signed both forks; the artifact on disk is now
**Core `873fa3db…9f10`, 231,148 bytes** (`11-UAT.md` `build_identity`, commit `7352886`).

**Nothing recorded from the device is invalidated** — every finding is generator-level and
would have to be deliberately fixed to disappear — but no result may be promoted to
"verified on the shipped build" without a re-run. In particular the two open blockers (the
Mirror axis-4 unfilled picker and the Control Room Note resolution) should be re-checked
against `873fa3db` first, because a Phase 11 rebuild could plausibly have moved either.

## Why this file exists

Four built phases — **01, 02, 03, 08** — have **no `*-UAT.md` at all**. During the
2026-08-17/18 device UAT the outstanding-work picture was assembled from UAT files, so
these phases were invisible.

**Phase 11 was also on that list and no longer is:** the concurrent Phase 11 execution
stream added `11-UAT.md` (6 tests, 5 pending/blocked) while this branch was open, so
`audit-uat` now covers it. Its entry below is retained only because the FAILED truth in
`11-VERIFICATION.md` is worth reading alongside a device observation from this session.

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
