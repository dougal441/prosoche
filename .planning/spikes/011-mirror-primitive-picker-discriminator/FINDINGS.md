# Spike 011 Findings: Mirror Primitive Picker Discriminator

**Pointer:** the blocker todo this spike discriminates for is
`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md` -- see its
2026-08-18 dated section, which records this spike's verdict and points back here.

## Verdict

VERDICT: not discriminated at rung 2

None of the three action identifiers unique to the Mirror primitive's span
(`is.workflow.actions.list`, `is.workflow.actions.getitemfromlist`,
`is.workflow.actions.speaktext`) raised the axis-4 unfilled-required-picker error
(*"Please choose a value for each parameter in this action."*) on the booted iOS
simulator, in the full probe or in either bisection variant. Every run completed to its
final breadcrumb (or, for the full probe, to `Return to Home Screen`) with no error text
of any kind.

This does **not** mean the generator is clean, and does **not** refute the device-observed
failure the blocker todo records three times across two independent installs. It means the
simulator did not reproduce the device failure -- which itself narrows the question toward
a device-only reproduction, and re-opens `15-RESEARCH.md` assumption A6 (see "What this
narrows" below).

## Simulator runtime and device, as measured during this run

```
$ xcrun simctl list runtimes
== Runtimes ==
iOS 26.5 (26.5 - 23F77) - com.apple.CoreSimulator.SimRuntime.iOS-26-5

$ xcrun simctl list devices booted
== Devices ==
-- iOS 26.5 --
    iPhone 17 Pro (79A84C29-DB62-40A2-AC3F-CCB5F8192F86) (Booted)
```

Device was `Shutdown` at task start; booted explicitly with
`xcrun simctl boot 79A84C29-DB62-40A2-AC3F-CCB5F8192F86` before any import.

## Exact commands run

```bash
# Pin the files under test BEFORE the first import (see drafts/under-test.sha256)
shasum -a 256 tools/build_state_engine.py tools/build_sentient.py \
  src/PROSOCHE-Dumb.xml src/PROSOCHE-Sentient.xml docs/BUILD-NOTES.md \
  > .planning/spikes/011-mirror-primitive-picker-discriminator/drafts/under-test.sha256

# Boot the device (it was Shutdown, not already booted)
xcrun simctl boot 79A84C29-DB62-40A2-AC3F-CCB5F8192F86

# Raise the simulator window (a simctl-booted sim has no window until this)
open -a Simulator

# FULL PROBE
cp ".../011-.../PROSOCHE Mirror Picker Discriminator.shortcut" /tmp/mirror-picker-probe.shortcut
xcrun simctl openurl 79A84C29-DB62-40A2-AC3F-CCB5F8192F86 "file:///tmp/mirror-picker-probe.shortcut"
# one synthesized tap on "Add Shortcut" (drafts/sim_input.py's tap(), reused verbatim)
# one synthesized tap on the editor's Play button
# per-breadcrumb: one synthesized tap on a non-interactive area (focus) + one hardware
# Return keypress (Show Result dismisses on Return; see "What did not work" below)

# BISECTION VARIANT 1 -- minus Leg 3 (speaktext removed)
# built + signed as "PROSOCHE Mirror Picker Discriminator Minus Leg 3" in the scratchpad
# (not committed -- see "Where the bisection variants live" below), same import/run/dismiss
# sequence

# BISECTION VARIANT 2 -- minus Legs 2 and 3 (getitemfromlist and speaktext removed)
# built + signed as "PROSOCHE Mirror Picker Discriminator Minus Leg 2", same sequence

# Re-verify the pin after all three runs
shasum -a 256 -c .planning/spikes/011-mirror-primitive-picker-discriminator/drafts/under-test.sha256
```

## Results per variant

| Variant | Legs present | Last breadcrumb reached | Error raised | Final state |
|---|---|---|---|---|
| Full probe | List, Get Item From List, Speak Text | **D** ("Speak Text leg done. Probe complete -- no error was raised.") | **none** | `Return to Home Screen` executed; landed on the Home Screen |
| Minus Leg 3 | List, Get Item From List | **C** ("Get Item From List leg done. LEG 3 REMOVED for this bisection variant.") | **none** | `Return to Home Screen` executed; landed on the Home Screen |
| Minus Leg 2 | List only | **B** ("List leg done. LEGS 2 AND 3 REMOVED for this bisection variant.") | **none** | `Return to Home Screen` executed; landed on the Home Screen |

No variant produced any error text, verbatim or otherwise. The Get Item From List action
in both the full probe and the minus-Leg-3 variant rendered as "Get **Item at Index**
'**Circle Next**' from **List**" -- a populated, non-red picker with a resolved index
operand -- immediately before its Set Variable "Mirror Text" step, both visibly completed
with no "Please choose a value" interstitial. The Speak Text action in the full probe
rendered as "Speak 'Mirror Text'" and executed without interruption; audio output was not
independently confirmed (out of scope for rung 2 -- see "Rung-2 ceiling" below).

## Where the bisection variants live, and why they are not new spike artifacts

Plan `15-02-PLAN.md` Task 2's own `<files>` list is exactly
`FINDINGS.md, README.md, drafts/under-test.sha256` -- it does not list new probe XML or
`.shortcut` files. The two bisection variants were therefore built and signed in the
session scratchpad (`build_bisect_variants.py`, reusing every transcribed byte shape from
the committed `drafts/build_mirror_picker_probe.py` via a read-only import -- no edit was
made to that file), run on the simulator from there, and are not part of this spike's
committed deliverables. Their **results** are what this document records; the artifacts
themselves are reproducible from the committed full-probe builder by construction (delete
the named legs, keeping the breadcrumbs, per the plan's own bisection instructions) and are
not preserved, consistent with the plan's Task 2 file scope.

## WHAT DID NOT WORK (transcribed into README.md's own section too)

- **Tapping the toolbar Play button and the Show Result "Done" button using a y-fraction
  estimated by eye from the displayed screenshot thumbnail (0.6) missed both controls
  entirely** and instead landed inside the first Comment action's body text, opening an
  inline text-selection context menu (a "Select / Select All / AutoFill" popup) and,
  separately, a keyboard-dismiss "X" affordance in the bottom-right corner. Cropping the
  screenshot to the bottom band and reading pixel coordinates directly from the crop (PIL
  `Image.crop`) gave the correct fraction (`Play` at fx approx 0.840, fy approx 0.936;
  `Done` at fx approx 0.728, fy approx 0.202) -- eyeballing proportions from a
  described/rendered thumbnail is not reliable enough for this UI; crop-and-measure is.
- **A single synthesized tap on the Show Result sheet's "Done" button did not reliably
  dismiss it** -- it failed across several attempts at the measured coordinate, even though
  the same coordinate calculation was confirmed correct by cropping. **A hardware Return
  keypress (`Quartz.CGEventCreateKeyboardEvent(None, 36, True/False)`) dismissed it
  reliably**, but only when preceded by a tap on a neutral, non-interactive area of the
  screen (the nav bar / top of the comment card) to ensure the simulator window held input
  focus. This refines spike 010's `sim_input.py` docstring claim that "a Show Result sheet
  dismisses on Return, first try" -- first try was true only after an explicit
  focus-establishing tap; without one, neither a tap on Done nor a bare Return reliably
  dismissed the sheet in this session.
- Tapping the toolbar Play button while a text field is focused (from the mis-tap above)
  is silently ignored -- the run does not start, and the toolbar continues to show a
  static Play triangle rather than switching to the black "stop" square. This is only
  visible by comparing the toolbar icon across screenshots, not from any error text.

## What this narrows (per `15-RESEARCH.md` assumption A6 and the plan's own routing)

The blocker todo's device observations are rung 3/4 (real iPhone, iPhone Mirroring,
reproduced three times across two independent installs). This spike's null result is
rung-2 evidence that the failure did not reproduce **at rung 2**, on **this simulator**,
**today**. Per `15-RESEARCH.md` assumption A6, if Circle 3's device run (the basis for
exonerating the `getdevicedetails` sites) was actually a no-op rather than a genuine silent
success, the suspect list could be wider than the three identifiers this probe tests -- in
which case a clean rung-2 result on these three is fully consistent with the real defect
sitting elsewhere, entirely outside this probe's three-identifier scope. This spike does
not resolve that ambiguity; it narrows the *instrument*, not the *defect*.

## Rung-2 ceiling -- what this result is and is not evidence for

Per `.claude/CLAUDE.md` #9, **a simulator observation is never promotable above
`UNVERIFIED` for anything on rung 2's ceiling list.** This spike's result sits partly
inside and partly outside that boundary:

- **Inside rung 2's reach, and settled here:** whether the three action identifiers'
  *structural* wiring (the picker literal, the coercion aggrandizement, the row-wrapper
  shape, the string envelope) raises an unfilled-parameter error on import and run. It does
  not, on this simulator, on this device model, on this iOS 26.5 build. That is a genuine
  rung-2 finding, not merely a non-finding.
- **Outside rung 2's reach, and NOT settled here, even though every leg "ran":** whether
  `Speak Text` actually produces audible speech on real hardware (spike 010 established
  that a structurally-identical, catalog-correct action -- `Set Brightness` -- can accept
  its operand at the editor level and still fail the underlying OS call on the simulator,
  with no distinguishing error text). This probe's clean run says the picker parameters
  resolved and the action was dispatched without a structural halt; it says nothing about
  whether Circle 8 is audible on a phone. The Control Room Note path, Personal Automation
  triggers, and Apple Intelligence remain untouched by this probe and are not implicated
  either way.

**CIRC-08 remains device-unproven for Phase 15.** A green build, a clean gate A, and this
spike's clean rung-2 bisection do not mean Circle 8 fires audibly on a phone -- the original
device-reproduced axis-4 failure stands unexplained by this spike, and the routing in
`15-02-PLAN.md` Task 3 records that explicitly.

## What this spike does establish

1. The exact byte shapes `mirror_text()`, `_list_row()` and `voice()`'s `speaktext` call
   emit -- reproduced verbatim here, including the real `MIRROR_SUCCESSES` array and its
   one bare-string row -- do not, by themselves, trip the axis-4 unfilled-picker error on
   the iOS 26.5 simulator. If the device failure is caused by something in this exact
   byte shape, it is not visible at rung 2, on this simulator, with this iOS version.
2. `is.workflow.actions.list`'s `WFItems` row-wrapper shape (axis 8, previously
   structurally-proven-only per `.claude/CLAUDE.md`) imports and resolves into a normal,
   editable list on the simulator with both row kinds present (9 attachment-bearing rows,
   1 bare row) -- no row rendered as an unexpected blank or malformed entry in the editor.
   This is a simulator observation, not a device one, and is recorded as such.
3. The bisection is complete and mechanically sound: three variants, each one leg removed
   from the last, each reaching a strictly earlier breadcrumb than the full probe by
   construction, each observed independently on the simulator.
