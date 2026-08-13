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
