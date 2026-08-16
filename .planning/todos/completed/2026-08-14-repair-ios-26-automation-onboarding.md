---
created: 2026-08-13T21:15:08.738Z
title: Repair iOS 26 automation onboarding
area: general
severity: major
files:
  - src/PROSOCHE-Dumb.xml:75263
  - src/PROSOCHE-Dumb.xml:75266
  - src/PROSOCHE-Dumb.xml:75278
  - src/PROSOCHE-Dumb.xml:75281
  - src/PROSOCHE-Sentient.xml:76505
  - src/PROSOCHE-Sentient.xml:76508
  - src/PROSOCHE-Sentient.xml:76520
  - src/PROSOCHE-Sentient.xml:76523
  - tools/build_state_engine.py
---

## Problem

The iOS 26 automation instructions embedded in both variants cannot produce the required OPEN and CLOSE automations as written.

The app-trigger screen is a shortcut picker, so selecting PROSOCHĒ there creates a no-input automation. The current step 10 is factually impossible: Run Shortcut's Input parameter accepts a variable, not literal text. Step 7 also uses the stale `Ask Before Running` label instead of iOS 26's `Run After Confirmation` / `Run Immediately` choice.

## Solution

Replace the affected automation steps with the verified wrapper flow:

1. On the app-trigger shortcut-picker screen, tap **Create New Shortcut**.
2. Add a **Text** action and enter exactly `OPEN` for Automation A or `CLOSE` for Automation B.
3. Add **Run Shortcut** immediately below Text and select the appropriate PROSOCHĒ variant.
4. Expand Run Shortcut and confirm Input is the preceding Text magic variable; if it is not auto-filled, use **Choose Variable** and select Text.
5. Save with the blue checkmark.

Automation B must otherwise mirror Automation A, using the Is Closed trigger and `CLOSE`. Replace the stale confirmation instruction with selecting **Run Immediately**. Update both Note bodies and every generator/documentation source that can recreate them; regenerate, validate, sign, and verify both variants when this todo is implemented.

## Corroboration — added 2026-08-15

**The wrapper flow prescribed above is now device-proven correct**, independently, by the
`open-routing-sequence-error` debug session (see `.planning/debug/HANDOFF.md`).

A purpose-built INPUT PROBE — a signed shortcut echoing its Shortcut Input verbatim — was
pointed at by an automation wrapper built exactly as steps 1–5 describe: a **Text** action
containing `OPEN`, then **Run Shortcut** with Input set to that Text magic variable. The
probe reported `RAW [OPEN]` and `NORMALISED [OPEN]`. The handoff works end to end.

Two further confirmations from that session:

- A screenshot of the user's own automation confirmed the two-action wrapper renders with
  the Shortcut reference and the Input magic variable both correctly bound — so the flow is
  reproducible by a user following these steps.
- **One automation covering all target apps is correct.** `CurrentApp` appears zero times in
  either fork, and Heat/Gravity/Pressure/Circle/`active_session` are global across apps.
  OPEN and CLOSE must remain two separate automations only because they pass different
  literals — not because of per-app handling.

This todo is therefore **unblocked and low-risk**: the replacement instructions are known
good, and the only work is propagating them into the generator and both Note bodies. It
was independent of the OPEN-path defects and remains so now that the
`open-routing-sequence-error` debug session has fully closed (2026-08-15, both symptoms
device-verified, see `.planning/debug/resolved/open-routing-sequence-error.md`) — nothing
about that closure changes this todo's own scope or status. Still unfixed; still the next
concrete unblocked task in this project's queue if no higher-priority item is picked
first.

## Correction — added 2026-08-16

The 2026-08-16 corroboration note below was **wrong about the specific cause** for this
user's CLOSE failure during Phase 4 UAT — retracting it. The user's CLOSE automation did
have a Text → Run Shortcut wrapper; the Text action's literal was typo'd as `CLOSED`
instead of `CLOSE`, so the router's exact-match against the literal `CLOSE` never fired and
it fell to the MANUAL branch — a user configuration mistake, not the no-input-automation
defect this todo is about. Once the user corrected the Text literal, CLOSE routed and
completed correctly (device-confirmed: `recent_sessions` populated with correct non-zero
durations, `active_session` cleared, `last_close_at` set). This todo's underlying defect
(the iOS 26 shortcut-picker producing a no-input automation when Note step 10 is followed
literally) is still real and still unverified either way by this session — it was simply
not what happened here. Scope/priority unchanged from the original entry.

## Closed — 2026-08-17 (quick task `260817-au7`)

Implemented. The Control Room Note's Automation A and Automation B sections in both forks
now carry the twelve-step `Create New Shortcut` wrapper flow. The impossible literal-text
step and the stale `Ask Before Running` label are gone from both. The exact-literal typo
warning sits at the point the literal is entered, naming `CLOSED` explicitly and stating
that the failure is silent. The "one automation covers every watched app" statement appears
once, before Automation A. `PROSOCHE_Nine_Circles_Canonical_Strategy.md` was corrected to
the same shape and `docs/BUILD-NOTES.md` §20 records the repair.

Both forks were rebuilt from one generator run, validated at
`--target-macos 26 --target-platform all`, signed under their exact display names, and
**decrypted out of their AEA1 containers** and re-asserted: one `WFTextTokenString` note
body per fork, both attachment ranges equal to the recomputed placeholder offsets
(`{4389, 1}`/`{4420, 1}` → `{5478, 1}`/`{5509, 1}` — the edit lengthened the text ahead of
them, so leaving them alone would have shipped out-of-bounds ranges), zero stale onboarding
strings, all seven replacement strings present. All eleven `docs/*.py` checks exit 0 and
`artifacts/shortcuts/MANIFEST.md` was refreshed.

**What is and is not proven.** The instructions are now correct **as written** — every step
names a control that exists on iOS 26 and a parameter that accepts what the step supplies.
The flow itself remains **device-unproven end to end in this form**. The INPUT PROBE run of
the `open-routing-sequence-error` session proved the *handoff mechanism* — a `Text` action
feeding `Run Shortcut`'s Input yields `RAW [OPEN]` / `NORMALISED [OPEN]` — and a screenshot
confirmed the wrapper renders correctly once built. Neither proves that a user following
*this specific rendered text* arrives at a working automation. Confirming that belongs with
the outstanding device UAT
(`.planning/todos/pending/2026-08-16-device-uat-nine-circles-and-sequence-switching.md`),
and `MANIFEST.md` carries a warning saying so.

**Carried forward, not fixed here.** Both forks' note bodies still name
`PROSOCHĒ — Nine Circles — Dumb` as the Run Shortcut target, so Sentient's inherited body
names the wrong fork. That is a pre-existing fork-naming defect independent of this todo
and belongs with Build Addendum 01.
