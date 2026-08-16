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

## Corroboration — added 2026-08-16

Confirmed the same defect affects the **CLOSE** automation, not just OPEN. During Phase 4
UAT (`.planning/phases/04-close-pipeline-session-race/04-UAT.md`, Tests 1/3/4/5/6), the
user's OPEN automation fired correctly (Circle 1 notification observed), but closing the
tracked app displayed the manual Control Room menu instead of running `close_pipeline()` —
a dropped `state.json` confirmed `active_session` was never cleared and `recent_sessions`
stayed empty. The user's CLOSE automation was a no-input automation, exactly the failure
mode this todo describes. This blocks device re-verification of the already-landed
G-04-1/G-04-3 CLOSE fixes (`04-02-SUMMARY.md`) until the CLOSE automation is rebuilt with
the Text("CLOSE") → Run Shortcut wrapper. Raises this todo's practical priority — it is now
blocking Phase 4 UAT completion, not just onboarding polish.
