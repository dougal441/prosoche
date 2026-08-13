---
created: 2026-08-13T11:57:50.992Z
title: Apply Addendum 01 and repair automation onboarding
area: general
severity: blocker
files:
  - PROSOCHE_Build_Addendum_01.md
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

The next correction pass has two named scopes that must be worked through together:

1. Apply `PROSOCHE_Build_Addendum_01.md` across the authoritative build source, both product variants, the PROSOCHĒ Note, documentation, requirements, generated XML, and signed deliverables. The addendum changes the Circle names and intervention mapping, renames Dumb/Core and Sentient/Aware, makes Panic Escape deliberately removable with confirmation and optional Shortcuts-app hardening guidance, and renames the Apple Note from `PROSOCHĒ — Control Room` to `PROSOCHĒ`.
2. Repair the iOS 26 automation instructions embedded in both variants. The current app-trigger screen is a shortcut picker, so selecting PROSOCHĒ there creates a no-input automation. The current step 10 is also impossible as written: Run Shortcut's Input parameter accepts a variable, not literal text. Step 7 uses the stale `Ask Before Running` label instead of iOS 26's `Run After Confirmation` / `Run Immediately` choice. These errors block a user following the Note from creating functional OPEN and CLOSE automations.

The correction must be made in the authoritative source rather than patched only in generated artifacts, then propagated consistently to both forks.

## Solution

Work through Addendum 01 in full, preserving its exact requested names and mapping.

Replace the affected automation steps with the verified wrapper flow:

1. On the app-trigger shortcut-picker screen, tap **Create New Shortcut**.
2. Add a **Text** action and enter exactly `OPEN` for Automation A or `CLOSE` for Automation B.
3. Add **Run Shortcut** immediately below Text and select the appropriate PROSOCHĒ variant.
4. Expand Run Shortcut and confirm Input is the preceding Text magic variable; if it is not auto-filled, use **Choose Variable** and select Text.
5. Save with the blue checkmark.

Automation B must otherwise mirror Automation A, using the Is Closed trigger and `CLOSE`. Replace the stale confirmation instruction with selecting **Run Immediately**. Update both Note bodies and every generator/documentation source that can recreate them; regenerate, validate, sign, and verify both variants when this todo is implemented.
