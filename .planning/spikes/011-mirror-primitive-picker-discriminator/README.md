---
spike: 011
name: mirror-primitive-picker-discriminator
type: standard
validates: "Given the alert-free three-leg probe (List / Get Item From List / Speak Text, Circle 8's own index, MIRROR_SUCCESSES transcribed verbatim), when imported and run on the booted iOS simulator with a bisection, then determine which of the three action identifiers unique to the Mirror primitive's span raises \"Please choose a value for each parameter in this action\" -- the device-reproduced axis-4 unfilled-picker failure recorded in `.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`"
verdict: TBD
related: [010, 007]
tags: [axis-4, unfilled-picker, mirror, voice, list, getitemfromlist, speaktext, simulator, rung-2, probe, evidence-hierarchy, bisection]
---

# Spike 011: Mirror Primitive Picker Discriminator

## What This Validates

**One question, and only one:**

> Which of `is.workflow.actions.list`, `is.workflow.actions.getitemfromlist`, or
> `is.workflow.actions.speaktext` -- the three action identifiers unique to the Mirror
> primitive's own span, per `15-RESEARCH.md` Pitfall 4's exoneration of everything Circles
> 1, 3 and 9 exercised on device -- raises the device-reproduced axis-4 unfilled-picker
> error, or does none of them at rung 2?

Nothing else. Not whether Circle 8 speaks audibly. Not whether `voice_enabled` coerces
correctly (that is Q1, closed by decision D-05's writer normalisation in plan 15-03,
independent of this question). Not real-hardware speech playback. Those are different
questions on different rungs.

### Why the question is still open

The blocker todo (`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`)
records the failure reproduced three times across two independent installs, and proven to
follow the **Mirror primitive**, not the Circle index (switching `Classic` -> `BlackMirror`
moved the failure from Circle 7 to Circle 4, the position that sequence maps to Mirror).
`15-RESEARCH.md` Pitfall 4 narrows the suspect list from the todo's own "leading suspect"
(22 `getdevicedetails` sites, demoted because Circle 3's silent, error-free device run means
`silence()`'s capture path succeeded) down to exactly three identifiers, all unique to the
Mirror/Voice span: `is.workflow.actions.list`, `is.workflow.actions.getitemfromlist`, and
`is.workflow.actions.speaktext`.

### Why this is a rung-2 question and not a device question

`.claude/CLAUDE.md` #9's governing rule: *never climb higher than the open question
requires.* None of "Rung 2's ceiling" applies here -- no Notes app, no Apple Intelligence,
no Personal Automation trigger, no real-hardware brightness or volume. This is exactly the
class of question rung 2 (a simulator run the agent builds and runs itself) can settle, per
spike 010's corrected import channel: `open -a Simulator` first, then
`xcrun simctl openurl <udid> "file://…"`, then one synthesized tap on "Add Shortcut".

### What each outcome means and triggers (D-04's pre-agreed routing)

| Outcome | Meaning | Triggers |
|---|---|---|
| Last breadcrumb **A**, error raised | The defect is in Leg 1 (`is.workflow.actions.list`) -- axis 8's `WFItems` row wrapper becomes device-observed, not merely structurally proven | Task 3 routes on whether the fix is a one-line class fix (Branch A) or not (Branch B) |
| Last breadcrumb **B**, error raised | Leg 2 (`getitemfromlist`) -- the axis-4 picker candidate `15-RESEARCH.md` ranks most likely | Same two-branch routing |
| Last breadcrumb **C**, error raised | Leg 3 (`speaktext`) | Same two-branch routing |
| Breadcrumb **D** reached, no error | **The probe discriminated nothing.** Does not mean the generator is clean -- means the simulator did not reproduce the device failure, narrowing toward a device-only reproduction and re-opening `15-RESEARCH.md` assumption A6 | Task 3 Branch B: record `not discriminated at rung 2`, mark CIRC-08 device-unproven |

## How to Run

`PROSOCHE Mirror Picker Discriminator.shortcut` (signed, in this folder; unsigned source and
build script in `drafts/`). Fully standalone: reads no `state.json`, references no
production shortcut, needs no Personal Automation.

```bash
UDID=$(xcrun simctl list devices booted -j | python3 -c 'import json,sys;print(next(d["udid"] for v in json.load(sys.stdin)["devices"].values() for d in v))')
open -a Simulator   # a simctl-booted sim has NO window until this
cp ".planning/spikes/011-mirror-primitive-picker-discriminator/PROSOCHE Mirror Picker Discriminator.shortcut" /tmp/mirror-picker-probe.shortcut
xcrun simctl openurl "$UDID" "file:///tmp/mirror-picker-probe.shortcut"   # -> Shortcuts import sheet
# then one synthesized tap on "Add Shortcut" via drafts/sim_input.py's tap(), coordinates
# computed as fractions of the device screen mapped through the window rect measured at
# run time (see .planning/spikes/010-.../drafts/sim_input.py, reused verbatim)
```

Four legs plus breadcrumbs, all at control-flow base depth:

| leg | what it holds | why |
|---|---|---|
| **Set-up** | `Number 8` -> `Set Variable "Circle Next"` | Circle 8's own index, not a synthetic one -- the same variable name `mirror_text()` feeds `Get Item From List` with in production |
| **Leg 1 -- List** | `is.workflow.actions.list`, `WFItems` = `MIRROR_SUCCESSES` transcribed verbatim (10 rows: 9 attachment-bearing, 1 bare -- row 8, the exact row `_list_row()`'s own docstring names) | reproduces the real production row-wrapper shape, not a synthetic array |
| **Leg 2 -- Get Item From List** | `WFItemSpecifier = "Item At Index"`, `WFItemIndex` fed by `"Circle Next"` **with** the `WFCoercionVariableAggrandizement`/`WFNumberContentItem` coercion, `WFInput` wired to Leg 1's own output by `OutputUUID`/`OutputName` | byte-identical to `mirror_text()`'s own wiring |
| **Leg 3 -- Speak Text** | `WFText` carries `"Mirror Text"` in the single-`￼`-placeholder `WFTextTokenString` envelope, no other parameter | byte-identical to `voice()`'s own `speaktext` call |
| **Terminator** | `is.workflow.actions.returntohomescreen` | ends the run without a modal |

No `Show Alert` appears anywhere -- every breadcrumb is `is.workflow.actions.showresult`,
mechanically asserted absent by `drafts/assert_probe_shape.py`.

## What to Expect

**Expected, on the research:** if the failure reproduces at rung 2 at all, `15-RESEARCH.md`
ranks Leg 2 (`getitemfromlist`) most likely, because its picker (`WFItemSpecifier`) is a
known axis-4 class already. That is a prediction, not a result -- recorded here so a
confirming observation cannot be mistaken for a foregone conclusion.

**Genuinely unknown:** whether the failure reproduces on the simulator at all. The device
observations behind the blocker todo are rung 3/4; this probe is the first rung-2 attempt
at the same question, and `15-RESEARCH.md` assumption A6 flags that if Circle 3's device
run was actually a no-op rather than a genuine silent success, the suspect list could be
wider than these three identifiers -- in which case this probe returning clean is
consistent with the real defect sitting elsewhere.

**Explicitly out of reach at rung 2** -- `.claude/CLAUDE.md` #9's "Rung 2's ceiling":

- Whether Circle 8 is audible on real hardware, or at what volume.
- The Control Room Note path, Personal Automation triggers, Apple Intelligence -- none are
  touched by this probe.
- A simulator observation here is never promotable above `UNVERIFIED` for anything on that
  list, even a clean pass on every leg.

## Investigation Trail

### Build (2026-08-18)

`drafts/build_mirror_picker_probe.py` emits the plist; `drafts/assert_probe_shape.py` proves
the built XML actually carries the shape under test. Both are re-runnable and both live in
this spike, not in `tools/` or `docs/` -- Task 1 modifies no generator, no fork, no checker.

**Deviation from CONVENTIONS.md, recorded -- the plist was authored directly rather than by
dispatching `shortcuts-playground:shortcut-builder`.** Same exception spike 007 and spike
010 both used: *"when a spike's purpose is to reproduce a byte shape under test, an agent
'corrects' the very value under test."* Every byte here is transcribed from
`tools/build_state_engine.py` -- `_list_row()` (:844), `mirror_text()` (:917),
`mirror_templates()` (:929), `MIRROR_SUCCESSES` (:80-91), and the `speaktext` call inside
`voice()` (:1006) -- read-only use; this plan touches no generator file in Task 1.

**Why the real `MIRROR_SUCCESSES` array, not a synthetic ten-row list.** `_list_row()`'s own
docstring names `MIRROR_SUCCESSES[7]` / `MIRROR_LAPSES[7]` as "ROW 8" -- the exact site where
an earlier `isinstance`-based row discriminator shipped a double-wrapped row for four cycles
before Phase 13 caught it. Transcribing the real array means both row kinds (`_list_row()`
must discriminate bare-string vs. attachment-wrapped) are present in the same real
proportions the shipped artifact carries: 9 attachment-bearing rows, 1 bare row.

**Why the coercion on `WFItemIndex` is hardcoded rather than derived locally.** In this
probe, taken in isolation, `"Circle Next"` is fed only by `is.workflow.actions.number`
(already Number-typed), so a local run of the generator's own
`normalise_numeric_operands()` would skip the coercion. The real shipped artifact does not
skip it, because `"Circle Next"` is mixed-typed **artifact-wide** (the Test Circle harness
assigns it from both `read_value()` and `number()`), and the generator's own comment at
`:5037-5041` records that every `getitemfromlist.WFItemIndex` site referencing it -- this
one included -- carries the coercion. Reproducing the real artifact's shape rather than
what this probe's narrower local context would derive is exactly what "transcribe, do not
re-derive" means in practice.

### Gates

**Gate A -- mandatory, passed clean:**

```
$ validate-shortcut "drafts/PROSOCHE Mirror Picker Discriminator.xml" --target-macos 26 --target-platform all
Validation passed.
```

Gate B is advisory per `.claude/CLAUDE.md` #1 and is not part of this task's acceptance
criteria; not run for this probe.

### Shape assertion, from the built XML

```
probe shape asserted from the built XML:
  1 list, 1 getitemfromlist, 1 speaktext -- each exactly 1
  4 showresult breadcrumbs, 0 alert (must be 0)
  getitemfromlist: WFItemSpecifier 'Item At Index', WFItemIndex carries WFCoercionVariableAggrandizement/WFNumberContentItem
  speaktext: WFText is WFTextTokenString with non-empty attachmentsByRange, no other WFSpeakText* parameter
  WFItems: 1 bare-string row(s), 9 wrapped row(s) with non-empty attachmentsByRange
```

### Signed artifact

`PROSOCHE Mirror Picker Discriminator.shortcut` -- **24,485 bytes**, SHA-256
`3ec35f49ba2caf909c8194b505e7de4cd795be0b4acb5c67e894fc0f24d688e6`. Filename equals the
display name exactly, no suffix, per the signing-name discipline. Timestamped pre-sign
archive under `2026-08-18/`.

## WHAT DID NOT WORK

None yet -- this section is filled in during Task 2's run.

## Results

### Verdict: TBD

Task 2 runs the probe on the simulator and records the bisection and the verdict here.
