---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 02
subsystem: evidence-and-capability-audit
tags: [coercion, operand-types, setbrightness, setvolume, simulator, rung-2, probe, evidence-hierarchy, recording-duty]
requires:
  - "16-RESEARCH.md Finding 2 (the narrowed coercion question) and Finding 3 (the simulator import channel)"
  - "tools/build_state_engine.py, READ-ONLY — the emitted shapes the probe reproduces"
  - ".planning/spikes/CONVENTIONS.md — layout, README-first, standalone-probe rules"
provides:
  - "spike 010: a signed, gate-A-clean, simulator-tested coercion probe in three artifacts"
  - "research assumption A5 CLOSED — the synthesized tap completes the simulator import"
  - "the retirement of spike 007's 'the simulator cannot import' claim, in four places"
  - "CAP-08: setbrightness.WFBrightness is optional and defaults to 50%"
  - "a name-scoped provenance confirmation of assumption A2 and a written disposition of the 11 uncoerced setvolume sites"
  - "spike 007 upgraded PARTIAL -> VALIDATED"
affects:
  - ".claude/CLAUDE.md section 9 (rung-2 row and Rung 2's ceiling)"
  - ".claude/skills/spike-findings-prosoche/references/evidence-and-probes.md"
  - ".planning/spikes/CONVENTIONS.md"
  - "docs/BUILD-NOTES.md section 29"
  - "the eventual device session's scope — two questions removed, one sharpened"
tech-stack:
  added: []
  patterns:
    - "the control leg: a deliberately-uncoerced sibling, without which a green chip is unfalsifiable"
    - "the negative control as refutation instrument, not confirmation instrument"
    - "two probe variants from one source of truth, asserted identical on whatever is under test"
    - "CGEventPost fraction-mapped simulator input, with every dead-end channel recorded"
key-files:
  created:
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/README.md
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Probe.shortcut
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Probe Breadcrumbs.shortcut
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Negative Control.shortcut
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/build_coercion_probe.py
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/build_negative_control.py
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/assert_probe_shape.py
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/audit_silence_target_sourcing.py
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/sim_input.py
    - .planning/spikes/010-coercion-at-a-direct-set-parameter/screenshots/ (14 PNGs)
  modified:
    - docs/BUILD-NOTES.md
    - .claude/CLAUDE.md
    - .claude/skills/spike-findings-prosoche/references/evidence-and-probes.md
    - .planning/spikes/CONVENTIONS.md
    - .planning/spikes/MANIFEST.md
    - .planning/spikes/007-unresolvable-picker-failure-mode/README.md
decisions:
  - "Verdict PARTIAL, not VALIDATED and not INVALIDATED — the fresh-donor protocol is NOT triggered, and no replacement CoercionItemClass exists anywhere"
  - "The plist was authored directly rather than via shortcut-builder, under CONVENTIONS.md's own stated exception, because leg B is a value an agent would 'correct'"
  - "Legs sequenced C->A->B->D so the capture precedes every write — a safety property, not presentation"
  - "The 11 uncoerced setvolume sites are correctly uncoerced; the asymmetry is a sourcing artifact"
metrics:
  duration: ~44 min
  completed: 2026-08-18
  tasks: 3
  commits: 3
status: complete
---

# Phase 16 Plan 02: The Aimed Coercion Probe Summary

Closed at rungs 1–2 and zero device cost what a free rung could close of the
`WFNumberContentItem`-at-a-direct-Set-parameter question — and found that the instrument the phase
intended to use for it, the coercion-chip gate, **cannot work at that position at all**.

## What Was Built

One spike, `.planning/spikes/010-coercion-at-a-direct-set-parameter/`, holding **three signed
artifacts**, five re-runnable scripts, and 14 screenshots.

| artifact | purpose |
|---|---|
| `PROSOCHE Coercion Probe.shortcut` | **silent** — no blocking UI; the variant a simulator can run end to end |
| `PROSOCHE Coercion Probe Breadcrumbs.shortcut` | the A–D breadcrumb ladder, for a **device** session where a human can tap |
| `PROSOCHE Coercion Negative Control.shortcut` | one `Set Brightness` with no operand — the control that refuted the run-time inference |

Four legs, sequenced **C → A → B → D**: the device read runs **before** either write, so the restore
leg restores the true original rather than the probe's own test value. Leg A reproduces
`restore_managed_settings()`'s emitted shape exactly — a `gettext`-fed named variable feeding
`WFBrightness` with the coercion **first** in `Aggrandizements` — which is the highest-stakes
production instance of that wiring. Leg B is the identical chain **deliberately bare**.

Gate A clean on every artifact. Gate B recorded verbatim as advisory and chained into nothing.

## The Verdict: PARTIAL

**Nothing observed contradicts `WFNumberContentItem`. The fresh-donor protocol is NOT triggered.**
No replacement `CoercionItemClass` appears anywhere in this plan, and `assert_probe_shape.py` fails
the build if one ever does.

### Settled

**1. Research assumption A5 is CLOSED — explicitly YES, the synthesized tap completes the import.**
`xcrun simctl openurl <udid> "file:///…"` renders the import sheet and one synthesized tap on "Add
Shortcut" completes it; the editor opened on the imported probe.

This **retires spike 007's** recorded finding, and the correction runs the *opposite* way to what was
expected: `.claude/CLAUDE.md` §9's **original** rung-2 row was right, and spike 007's narrowing of it
was wrong. Spike 007 tried five channels and generalised from five failures; its `file://` row was
measured against the **MCP simulator tool's** scheme allowlist, not against `simctl`. Its other four
rows stand, including `shortcuts://import-shortcut` genuinely requiring an iCloud link (re-measured —
`silent=true` does not bypass it, because the URL is refused first).

**2. The chip gate CANNOT discriminate at a direct Set-action parameter.** The coerced and uncoerced
legs render **identically**. A conditional's operator picker is populated from the operand's static
type, so a mismatch renders red; **`Set Brightness` has no operator picker**, so there is nothing for
a type mismatch to break. **`09-UAT.md` Test 1 was never evidence about `WFBrightness`/`WFVolume`** —
a green chip there is not weak evidence, it is *no* evidence.

The uncoerced control leg is what exposed this. Without it, "leg A rendered fine" would have been
recorded as a pass, and the pass would have been vacuous.

**3. CAP-08 — `setbrightness.WFBrightness` is OPTIONAL and defaults to 50%.** An absent operand
renders as "Set brightness to 50%" and does **not** raise the unfilled-parameter error. So an
unresolved operand fails **silently**, applying an unrequested 50% with no capture, rather than
halting. Directly relevant to SAFE-01 / CIRC-05, and a direct requirement on the device instrument.

### Not settled — and now known to be unsettleable at rung 2

**Whether `Set Brightness` actually CONSUMES a Number-coerced operand at run time** (backstop truth 1)
and **whether `Get Device Details` current-brightness returns a usable typed value on hardware**
(backstop truth 2) are both **UNVERIFIED**, per §9's rung-2 ceiling. `Set Brightness` cannot succeed
on a simulator at all, and the simulator reads brightness as `0`. Real-hardware environmental
behaviour, Personal Automations, the Note path and Apple Intelligence are untouched.

That is not a gap in the work — it is the useful part of the result. It means **no further simulator
effort will help**, so the device session must carry it and should not be spent re-deriving that.

## The Inference That Was Refuted

The coerced leg's run produced *"Could Not Run Set Brightness — There was a problem setting the
brightness"* — a **capability** error, not the **parameter** error this project names as the signature
of an operand-type defect. The tempting conclusion: *Shortcuts cleared parameter validation and
reached the OS call, so the operand resolved.*

**A one-action negative control with no operand at all produced the same message.** Both reach the OS
call; both fail identically because the simulator has no backlight. The channel **cannot** distinguish
a resolved operand from an absent one.

That control cost one small artifact and overturned the conclusion this spike was about to record.
`.claude/CLAUDE.md`'s *"read the error text, not just the letter"* is what caught it.

## Disposition of the 11 Uncoerced `setvolume` Sites

**Correctly left uncoerced** — on a name-scoped provenance check, not by analogy to brightness.
`audit_silence_target_sourcing.py`, read-only against both shipped forks:

| | Dumb | Sentient |
|---|---:|---:|
| `Set Variable "Silence Target"` assignments | **11** | **11** |
| …**Number-sourced** (`is.workflow.actions.number`) | **11** | **11** |
| …**not** Number-sourced | **0** | **0** |
| `setvolume` sites / fed by `Silence Target` / coerced | 15 / **11** / 4 | 15 / **11** / 4 |

**The arithmetic closes exactly:** 11 + 4 = 15. The uncoerced sites are precisely those fed by a
variable whose every definition is `number()`-sourced. **Assumption A2 holds**, now on provenance
rather than on a count — which matters, because a count proves the split is *stable* and can never
prove it is *correct*.

**The 15/15-brightness vs 4/15-volume asymmetry is a SOURCING ARTIFACT, not a gap.** Brightness
operands are `gettext`-sourced (Text) and need the coercion; the silence target is `number()`-sourced
and already Number-typed, so the generator correctly skips it. The four coerced `setvolume` sites are
the **restore** operands, which come back out of state through `read_value()` and are therefore Text.
**Do not "fix" the asymmetry by pattern-matching brightness.**

The failure mode the name-scoped check rules out is one this project has already paid for: one
text-sourced definition of that name anywhere would poison all 11 operands and the count-based
`site_audit()` would still pass — exactly how `Circle Next` produced 30 offenders.

## Free-Ride: Spike 007 Resolved, PARTIAL → VALIDATED

Run while the channel was open. An unresolvable picker renders **silently EMPTY**; a **fabricated**
one renders **silently WRONG** — a TikTok descriptor resolved to **AirDrop**, in red. Nothing fails at
import and nothing warns. `WFSelectedApp` is **load-bearing even for an installed first-party app**
(leg B, Reminders, descriptor omitted → "Open App", empty). The editor **trusts a stored descriptor's
Name and never re-resolves it** from the bundle id.

**PROSOCHĒ is unaffected** — `open_app()` emits the full descriptor triple for all six apps — but
spike 006's Class-A verdict holds *because the descriptor is written*, not because the bundle id would
have carried it.

## Deviations from Plan

**1. [Documented exception] The plist was authored directly rather than via `shortcut-builder`.**
CONVENTIONS.md requires delegating the build, **and** records the exception this falls inside: *"when
a donor already gives the exact byte shape and the spike's purpose is to vary it deliberately, author
the plist directly — an agent will tend to 'correct' the very values under test."* Leg B is an operand
deliberately missing its coercion; an agent that "fixed" it would leave the probe valid, signable and
silently unable to discriminate. Every byte is transcribed from `tools/build_state_engine.py`
(read-only). Same justification spike 007 recorded. **Files modified:** the spike drafts.
**Commit:** `b959e08`.

**2. [Rule 3 — blocking] The probe was rebuilt twice, and the second rebuild is a finding.**
`Show Alert` modals accept neither synthesized taps nor hardware Return on this channel, so the
breadcrumb ladder wedged the run permanently at its first alert. Rather than abandon the run
observation, the probe was rebuilt with **no blocking UI**, and both variants were kept — the
instrument a simulator needs and the instrument a device needs are genuinely different.
`assert_probe_shape.py` asserts the two are **identical on all three Set Brightness sites**, so the
chip observed in one and the run observed in the other are observations of the same wiring.
**Commit:** `f24f871`.

**3. [Rule 2 — coherence of the record] `.planning/spikes/CONVENTIONS.md` was also corrected.**
Not in the plan's `files_modified`. It carried the same retired "the simulator cannot import" claim as
CLAUDE.md and the skill; leaving it standing would have left a contradicting instruction in the file
new spikes are written against — the precise failure this plan exists to prevent. Struck through
rather than deleted, per the project's standing record rule. No code. **Commit:** `3d4b618`.

**4. Two validator rules shaped the probe's comment text.** `validate_shortcut.py` requires a
two-comment preamble carrying the literal Playground prompt block, and rejects internal parameter
names anywhere in comment text. Neither was anticipated; both were fixed before signing and neither
changed an action parameter.

## Authentication Gates

None.

## Known Stubs

None. Every artifact is built, signed, imported and observed; every script is re-runnable and passes.

## Verification

| check | result |
|---|---|
| Gate A on all three artifacts (`--target-macos 26 --target-platform all`) | `Validation passed.`, exit 0 |
| Gate B, advisory, recorded verbatim, chained into nothing | exit 0 (no Notes action, so the permanent waiver has nothing to waive) |
| Signed probe non-empty, AEA1 magic | 23,991 bytes, `AEA1` |
| `assert_probe_shape.py` (both variants, cross-variant equality) | passed |
| `audit_silence_target_sourcing.py` (both forks) | passed — A2 holds |
| `python3 docs/phase9_self_check.py` | exit 0 — `site_audit: passed (30/30 sites audited, 19 coerced, 11 correctly not)` |
| `python3 docs/environmental_restore_check.py` | exit 0 |
| No path under `tools/`, `src/`, or `docs/*.py` in any of the three commits | confirmed against the plan base |

## Self-Check: PASSED

All artifacts verified present on disk; all three commits verified in `git log`.

## What the Device Session Must Now Carry

Stated precisely so it is not re-derived:

1. Run the **Breadcrumbs** variant on hardware and confirm the coerced leg sets brightness to **0.42**
   and the uncoerced control to **0.66** — **by observing the value**, not by observing the absence of
   an error. Per CAP-08, "no error" is fully consistent with a silently defaulted 50%.
2. Confirm `Get Device Details → Current Brightness` returns a usable, correctly typed value.
3. Everything inside §9's rung-2 ceiling — the physical dim/un-dim, `WFBrightness = 0.0`'s real
   appearance, the failure-mode trials.

Two questions have been removed from that session's plate (the import channel, and the volume-site
disposition), and one has been sharpened from "does the chip go red" — an instrument now known not to
work here — into "what value was actually applied".
