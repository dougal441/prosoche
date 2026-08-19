---
created: 2026-08-18T07:35:00.000Z
title: Mirror primitive fails with an unfilled required picker — a third, unrecorded axis-4 instance
area: general
severity: blocker
status: pending — rung-2 discriminator (spike 011, plan 15-02) did not reproduce the failure; CIRC-08 remains device-unproven; localisation still requires a device breadcrumb build (see 2026-08-18 dated section below)
files:
  - tools/build_state_engine.py
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
---

> **COVENANT OVERHAUL (2026-08-19):** Owned by Phase 21. Note the Mirror moves to Circle 5 (Band C) in Phase 18, so this defect will sit on the re-engagement path — fixing it precedes any covenant device UAT.


## Problem

**Device-observed three times, across two independent installs.** Choosing
`Test a Circle → Circle 7 · Violence` — the position the `Classic` sequence maps to **Mirror** —
raises the runtime error:

> **Please choose a value for each parameter in this action.**

The primitive never runs. No alert with a title or body is ever presented.

`.claude/CLAUDE.md` Conventions rule 4 records that exact string as the signature of an
**unfilled required picker (enum) parameter**.

### Why this is definitely in the shipped artifact

Reproduced at 11:30 and 11:33 on 2026-08-17 (first install), and again on 2026-08-18 after the
device was **wiped, the Core artifact re-airdropped and reinstalled, and both automations
rebuilt**. The third reproduction is what rules out contamination from any editor interaction.

### Scope — this is the useful part, and it narrows the search enormously

The other Circles were probed on the fresh install:

| Circle | Result |
|---|---|
| 1 · Limbo | **fires correctly** — alert `PROSOCHĒ`, body `Circle 1 · pressure 0 · heat 0`, both numeric facts correctly substituted and matching clean state |
| 3 · Gluttony | runs to completion, **no visible alert, no error** — unclassified (consistent with a deliberately silent primitive, equally consistent with a silent no-op) |
| 7 · Violence | **FAILS** as above |
| 9 · Treachery | **fires** — device ejected to the Home Screen |

**Therefore the shared dispatch preamble is sound.** If it were broken, Circles 1 and 9 could not
fire. The unfilled parameter is on the **Mirror primitive specifically**. Circles 2, 4, 5, 6 and 8
remain unprobed.

### PROVEN: the defect follows the MIRROR PRIMITIVE, not the Circle index

**Device, 2026-08-18 07:54–07:56.** `Change Sequence` was used to switch from `Classic` to
`BlackMirror`, the sequence in which **Circle 4** — not Circle 7 — maps to Mirror. Then
`Test a Circle → Circle 4 · Greed` was run.

**It failed with the identical error.** So:

| sequence | Circle mapped to Mirror | that Circle's result |
|---|---|---|
| `Classic` | 7 · Violence | **fails** |
| `BlackMirror` | 4 · Greed | **fails** |

The failure **moved with the primitive** when the mapping changed. Combined with Circles 1 and 9
firing correctly under `Classic`, this rules out any index-based or per-Circle explanation and
confirms the unfilled picker is inside the **Mirror primitive's own action span**. That is the
tightest localisation available without a breadcrumb build, and it should be the starting point
for one.

### What it is NOT — both known axis-4 instances were checked and cleared

`.claude/CLAUDE.md` names `count.WFCountType` and `getitemfromlist.WFItemSpecifier` as the two
known instances. The signed container was decrypted and both were verified:

- **69** `is.workflow.actions.getitemfromlist` sites — **all** carry `WFItemSpecifier`.
- **1** `is.workflow.actions.count` site — carries `WFCountType`.
- Zero missing among them.

So this is a **third, previously unrecorded axis-4 instance**, and the conventions list in
`.claude/CLAUDE.md` should gain it once identified.

### Leading suspect — NOT proven, do not fix on this alone

Tapping the error's `Show` scrolls the editor to the offending action. Across a 4346-action list
the scroll animates and drifts, and the highlight could not be pinned in-session. On the first
attempt it settled on **`Get the Current Brightness`** → `Set variable Captured Brightness`.

That is suggestive because `.claude/CLAUDE.md` capability audit item 8 records **Get current
brightness** as **UNVERIFIED**: *"the exact `WFDeviceDetailsProperty` string is not documented in
this plugin's reference files"*, with an explicit instruction not to guess. The artifact carries
**22** `is.workflow.actions.getdevicedetails` sites using key `WFDeviceDetail` with the literals
`'Current Brightness'` (11) and `'Current Volume'` (11) — a key/literal pair that was guessed.
If iOS does not accept that key or literal, the picker reads as unfilled and produces exactly this
error.

**Against that reading:** the editor rendered the action as "Get the **Current Brightness**" with
the value shown, which is not obviously how an unset picker renders; and Mirror is not obviously a
brightness-touching primitive. Treat it as a lead, not a finding.

Also checked and cleared: `openapp` (18 sites, all with `WFAppIdentifier` + `WFSelectedApp`),
`setvolume` (15, all with `WFVolume` + `WFVolumeSetting`), `setbrightness` (15, all with
`WFBrightness`), `speaktext` (22, all with `WFText`).

## Solution

TBD — **localise before fixing.**

1. **Breadcrumb the Mirror primitive.** Flag-gated alerts at each action in the Mirror dispatch,
   one device run, to identify the offending action precisely. This is the instrument
   `.claude/CLAUDE.md` already prescribes and it costs one round trip.
2. Once identified, **fix the whole class, not the site** — every prior defect in this project was
   systematic (147, 367, 25, 20 and 8 sites). If it is `getdevicedetails`, all 22 sites are
   implicated, and the fix must settle the correct `WFDeviceDetail` key/literal from donor
   evidence rather than another guess.
3. Add a **build guard** asserting the newly-identified required picker is present, sibling to the
   existing guards, so this cannot ship again.
4. Record the third axis-4 instance in `.claude/CLAUDE.md` Conventions rule 4.

## Impact on outstanding UAT

- `07-UAT.md` Test 7 — recorded **fail**.
- `13-UAT.md` Tests 1 and 2 — **cannot be answered on this build at all.** Mirror is exactly the
  primitive under test, so the alert never renders and there is no body to judge empty or
  populated. The `WFItems` wrapper question is **gated behind this fix, not refuted by it**.
- `05-UAT.md` (nine primitives) depends on `Test a Circle` as its harness, so it is gated too.

## Evidence

- Device: iPhone Mirroring, 2026-08-17 11:30 / 11:33 and 2026-08-18 07:10, screenshots in-session.
- Artifact: `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut`, SHA-256
  `b07497ba1a66506aaaa9c48134f463ceefeac7f4a656e86dad48b0a76414ac5b`, decrypted and
  parameter-dumped for every candidate action family named above.

## 2026-08-18 — Phase 15 plan 15-02, spike 011: rung-2 discrimination attempted, did not reproduce

**Spike:** `.planning/spikes/011-mirror-primitive-picker-discriminator/` (README.md,
FINDINGS.md). This section and that spike each point at the other, per this phase's own
recording duty — neither can be found without the other.

`15-RESEARCH.md` Pitfall 4 narrowed this todo's suspect list from this todo's own "leading
suspect" — the 22 `getdevicedetails` sites, based on an un-pinned edit-view scroll landing
on "Get the Current Brightness" — down to exactly three identifiers unique to the Mirror
primitive's own span: `is.workflow.actions.list`, `is.workflow.actions.getitemfromlist`,
`is.workflow.actions.speaktext`. The reasoning: Circle 3 (`silence()`, which uses
`getdevicedetails`) ran silently and error-free on a fresh device install, and `silence()`
alerts only on its capture-failure path — so the capture path (and `getdevicedetails`)
must have succeeded. **This todo's own "leading suspect" is demoted on that reasoning,
carried here from the research rather than re-derived.**

Plan 15-02 built an alert-free, three-leg simulator probe reproducing the real Mirror
primitive's byte shapes verbatim (the actual `MIRROR_SUCCESSES` array, `_list_row()`'s
row-wrapper discrimination, `mirror_text()`'s `Get Item From List` wiring, and `voice()`'s
`speaktext` call) and ran it, with a bisection, on the booted iOS 26.5 simulator.

**VERDICT: not discriminated at rung 2.** None of the three suspects raised the
unfilled-picker error in the full probe or in either bisection variant (minus Leg 3, minus
Legs 2+3) — every run completed cleanly to `Return to Home Screen`. Full bisection
evidence, commands and screenshots are in `FINDINGS.md`.

**This is Branch B of D-04's routing rule** (`15-02-PLAN.md` Task 3): the verdict does not
name an identifier, so no fix is attempted here. **CIRC-08 remains device-unproven for
Phase 15** — a green build, a clean gate A, and this spike's clean rung-2 bisection do not
mean Circle 8 (or Circle 7's Mirror) fires on a phone. The original device-reproduced
failure this todo records stands unexplained.

**What this means for next steps, carried forward rather than acted on here:** because the
rung-2 probe did not reproduce the failure, and per `15-RESEARCH.md` assumption A6 the
demotion of `getdevicedetails` itself rests on a soft link (Circle 3's silent run being
read as success rather than no-op), the suspect list this todo should investigate next is
**wider than the three identifiers this spike tested**, not narrower. This todo's own
original Solution step 1 — "Breadcrumb the Mirror primitive" with a **device** build — is
now the most direct path to localisation and remains the right next instrument; a rung-2
probe has been tried and could not close the question, so the next attempt should go
directly to rung 3 (a real device) rather than repeating rung 2.

This todo remains **pending**. Its scope is not widened — no fix was attempted or is
recorded as attempted.
