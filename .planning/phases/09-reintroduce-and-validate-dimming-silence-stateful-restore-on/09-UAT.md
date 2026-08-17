---
status: testing
phase: 09-reintroduce-and-validate-dimming-silence-stateful-restore-on
source: [09-01-SUMMARY.md]
started: 2026-08-16T10:05:40.000Z
updated: 2026-08-16T10:05:40.000Z
---

> # ⚠ SUPERSEDED — 2026-08-18, by Phase 16
>
> **This file is superseded by
> `.planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-UAT.md`.**
> Run that instrument instead. Nothing below is edited: the tests, the `result:` fields and the
> DEV-06 write-up are preserved exactly as they stood, because a record of what was believed and
> attempted is worth more than the space it costs. **Supersede, do not edit** — that is the only
> change made to this file.
>
> ## Why it is superseded — three reasons, none of them cosmetic
>
> 1. **It carries no build-identity header.** There is no commit, no byte count and no SHA-256
>    anywhere in it, so there is no way to know which artifact it was written against or to prove
>    a later run is testing the same one. `16-UAT.md` pins both forks by commit, display name,
>    byte count and full SHA-256, each matched into `artifacts/shortcuts/MANIFEST.md`.
> 2. **It names the pre-rename forks.** The artifacts it describes were `Dumb` and `Sentient`.
>    They now ship as **`Core`** and **`Aware`** (phase 11 plan 06). A signed `.shortcut` carries
>    no display name inside it — the signer strips `WFWorkflowName` — so the filename is the sole
>    carrier, and the entries this file's instructions would have a tester look for no longer
>    exist in the library.
> 3. **Its test list predates the persistence finding.** Phase 16 found that the captured
>    original was written into a dictionary that is never saved, so it never reached
>    `state.json`: CLOSE and Emergency Restore reloaded the file, found the cleared sentinel,
>    failed the numeric `> 0` gate and skipped. **The screen dimmed and nothing in the product
>    un-dimmed it.** No test in this file looks at `state.json` for a capture, so running these
>    twelve tests as written would have found that defect only as a cascade of unexplained
>    restore failures. `16-UAT.md`'s Test 2 is the direct test for it and is the one that would
>    have caught it.
>
> Beyond those three, the artifact this file describes has since been renamed, gained an
> **eleventh** `primitive_dispatch()` rendering (phase 11), been re-signed several times, had
> its brightness floor and dim target moved to `0` (decision D-01), and had two dead snapshot
> leaves removed (decision D-02). It describes a build that no longer exists.
>
> ## ⚠ The single recorded pass does NOT carry forward
>
> **Test 1 below is recorded `result: pass`. That pass is NOT carried forward, and it is not
> weak evidence — it is no evidence.**
>
> Test 1 asked whether the coercion chip renders red at a `Set Brightness` / `Set Volume`
> parameter, and treated a non-red chip as a hard gate cleared. Plan **16-02** established at
> rung 2, with a deliberately-uncoerced control leg, that **the coerced and uncoerced legs render
> identically**. A conditional's operator picker is populated from the operand's static type, so
> a mismatch renders red there; **`Set Brightness` has no operator picker**, so there is nothing
> for a type mismatch to break. The instrument cannot discriminate at this position at all.
>
> Without that control leg, "the chip was not red" would have been recorded as a pass — and the
> pass would have been vacuous. It is exactly what happened here.
>
> The question was therefore **sharpened rather than answered**: from *"does the chip go red"* to
> *"what value was actually applied"* — which is the only form a device can settle, and the only
> form worth asking, because **CAP-08** measured `setbrightness.WFBrightness` to be **OPTIONAL
> with a 50% default**, so an unresolved operand fails silently rather than erroring.
> `16-UAT.md` Test 1 carries the replacement.
>
> **Everything else in this file remains `pending` and is inherited, re-scoped, by `16-UAT.md`.**
> The DEV-06 first-principles write-up in `## Context` below is still sound as *reasoning* and is
> carried forward as the prediction that `16-UAT.md` Test 9 exists to test — but decision **D-02**
> has since removed `changed_at` and `changed_by_session_id` outright, so the ownership-check
> question that write-up frames is now closed by removal rather than open by deferral.

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Coercion chip does not render red (hard gate before any behavioral trial)
expected: |
  Every inspected Dimming/Silence/Restore `Set Brightness`/`Set Volume` action's
  `WFBrightness`/`WFVolume` parameter chip renders normally (not red/invalid) in
  Shortcuts.app's editor. A red chip halts the sequence and routes to the fresh-donor
  protocol (`09-RESEARCH.md` "Recommended verification path") rather than continuing to
  Test 2.
awaiting: user response

## Context

Phase 5's device UAT (`05-UAT.md`) never exercised Circles 2-9 — exactly one Circle has
ever fired on a real device (Circle 1, once, on build `2026-08-15o`). Dimming, Silence,
and the restore mechanism have therefore never executed on real hardware, even before this
phase's coercion fix. This UAT is the first device evidence either primitive has ever
produced.

The coercion shape applied by `09-01-PLAN.md`
(`WFCoercionVariableAggrandizement`/`CoercionItemClass: WFNumberContentItem`) is
analogy-based: it is the same shape already device-confirmed for the Donor-4.1
conditional-operand pattern (CAP-07), but the decrypted `Donor 10.shortcut` — this
project's only device evidence for `setbrightness`/`setvolume` at all — does not contain a
variable-fed `WFBrightness`/`WFVolume` example, only unconfigured actions and one hand-typed
literal. Whether the same coercion shape is correct at a **direct Set-action parameter**
position (as opposed to a conditional or math operand) is genuinely unconfirmed. Test 1 is
therefore a hard gate, not a formality — a red chip means the fix is wrong at this exact
position and must not be treated as shippable.

Any prior test build (pre-Phase-9, or an earlier session's partial run) may have left
`settings_snapshot` dimmed/quiet without a matching restore, since Circles 2-9 have never
completed a full cycle on this device before. Test 2 (Emergency Restore, tapped before any
new trial begins) exists to establish a clean baseline rather than let stale captured state
from an earlier run contaminate this UAT's results.

#### DEV-06 (restore-ownership check) — first-principles design decision

`docs/BUILD-NOTES.md` §17 records that `changed_at`/`changed_by_session_id` are written at
20 sites and read nowhere — no ownership check currently gates
`restore_managed_settings()`. This section is the first-principles re-derivation
`09-RESEARCH.md` requires, not a restatement of BUILD-NOTES §17 alone.

**(a) Why the CURRENT no-ownership-check design is already correct for the two-session
overlap case.** `active_session` is a single slot, not a stack. Phase 4's SESS-03
session-race protocol (confirmed in `04-01-SUMMARY.md`) guarantees that only the winning
(last) OPEN's CLOSE ever reaches the restore step — a superseded/loser CLOSE reloads state,
finds it no longer owns `active_session`, and takes a Nothing-only branch that never calls
`restore_managed_settings()`. Separately, `dimming()`/`silence()` only capture into
`settings_snapshot` when no unrestored snapshot already exists (the condition-100
has-any-value gate on `Brightness Snapshot`/`Volume Snapshot`). So in a genuine overlap
(session A opens and dims, session B opens before A closes), session B's `dimming()` call
is a complete no-op — it neither re-captures A's original nor re-dims. The single winning
CLOSE (B's) is therefore the only CLOSE that ever restores, and it correctly restores
session A's captured original — the one true original that exists. This already works
today, with no ownership check of any kind.

**(b) The specific regression a naive equality check would introduce.** A gate of the form
`changed_by_session_id == closing session's own ID` would block exactly the legitimate case
just traced: B's `changed_by_session_id` write is empty (B never captured anything, since
its `dimming()`/`silence()` calls were no-ops per (a)), so it never matches B's own session
ID either. A naive equality check has no session ID that satisfies it, so the restore that
correctly happens today would be blocked, converting a working restore into a stuck-dim /
stuck-quiet failure recoverable only via Emergency Restore — precisely the outcome success
criterion 4 forbids.

**(c) The explicit decision this plan tests rather than assumes.** Do NOT implement a naive
ownership check. Ship the current no-ownership-check design as-is. Use device Tests 9
(genuine overlap) and 10 (overlap plus force-quit of the winning session before its CLOSE
fires) to look for any residual failure mode the trace in (a) did not anticipate, and record
whichever finding actually occurs — held or gap-found — in the `## Verdict` section (Test
12 is the explicit cross-check of this prediction against what Tests 9-10 actually show).

**(d) If a real gap is found and an ownership check is later implemented.** The Session ID
scope defect already on record (`docs/BUILD-NOTES.md` §17: only 2 of the 20
`changed_by_session_id` writes share ancestry with the genuine-OPEN branch where `Session
ID` is actually assigned; the other 18 record an empty owner) becomes a hard prerequisite
for that future work, not an independent fix that can be scoped separately from it.

## Tests

### 1. Coercion chip does not render red (hard gate)
expected: no `WFBrightness`/`WFVolume` parameter chip renders red/invalid on any inspected
Dimming, Silence, or Restore action in Shortcuts.app's editor — checked before any
behavioral trial begins. If red: stop, do not proceed to Test 2, follow the fresh-donor
protocol in `09-RESEARCH.md` "Recommended verification path" instead.
result: pass
reason: "User spot-checked rather than all ~3,500 actions in the shortcut — reasonable given only the 28 Phase-9 coercion sites are actually in question. Not a red chip on any inspected instance."

### 2. Clean baseline via Emergency Restore
expected: tapping Emergency Restore once, before any new trial, returns the device to a
known-clean state regardless of what any earlier (pre-Phase-9) test run may have left
captured/dimmed/quiet.
result: pending

### 3. Capture read is real, non-empty, and correctly typed
expected: an OPEN that dims/silences produces a real, non-empty, correctly-typed
`settings_snapshot.brightness`/`.volume.original_value` in `state.json` — the device read
of Current Brightness/Current Volume via Get Device Details actually returns usable data,
not an empty or wrongly-typed value.
result: pending

### 4. Observed floor of WFBrightness = 0.0
expected: forcing `WFBrightness = 0.0` on this device and observing the actual resulting
screen brightness either confirms or refutes the "dim, not black" prior report. The
observed value (not an assumption) is what any new dim-target decision must be based on.
result: pending

### 5. Capture -> apply -> restore round trip
expected: noting pre-session brightness/volume by hand, running OPEN then CLOSE, and
confirming both brightness and volume return to exactly their pre-session values (recomputed
by hand, not inferred from "no error dialog").
result: pending

### 6. Force-quit mid-session before CLOSE fires
expected: force-quitting the target app mid-session, before CLOSE fires, does not leave the
device permanently dim/quiet with no path back — either a later mechanism restores it, or
Emergency Restore (checked in Test 11) recovers it.
result: pending

### 7. Device restart mid-session before CLOSE fires
expected: restarting the device mid-session, before CLOSE fires, does not leave the device
permanently dim/quiet with no path back.
result: pending

### 8. CLOSE never fires at all
expected: a session where CLOSE never fires (no matching automation trigger) does not leave
the device permanently dim/quiet with no path back.
result: pending

### 9. Two overlapping sessions
expected: session A opens and dims, session B opens before A closes; B's CLOSE restores A's
captured original correctly — matching the DEV-06 write-up's (a) prediction above.
result: pending

### 10. Compound trial — overlap plus force-quit of the winning session
expected: per `09-RESEARCH.md` Pitfall 4, reproduce Test 9's overlap, then force-quit the
WINNING session (B) before its CLOSE fires. Confirm this does not leave `settings_snapshot`
populated with no CLOSE ever able to reach it, and that Emergency Restore (Test 11) still
recovers cleanly from this specific compound state.
result: pending

### 11. Emergency Restore recovers from every failure-mode trial
expected: after each of Tests 6-10, invoking Emergency Restore returns brightness/volume to
the originally captured value; if nothing was captured for that trial, confirm no error and
no state corruption.
result: pending

### 12. DEV-06 prediction cross-check
expected: Tests 9 and 10's actual results are checked against the DEV-06 write-up's (a)
prediction above, and this test's `result:` states plainly whether the current
no-ownership-check design held under device evidence, or a real gap was found.
result: pending

## Summary

total: 12
passed: 1
issues: 0
skipped: 0

## Verdict

_Placeholder — filled in by this plan's Task 3 after all twelve tests resolve (pass, issue,
or skipped), per `09-02-PLAN.md`'s acceptance criteria: a clear "demonstrated safe" or
"retired" judgement, citing specific test numbers for each claim._
