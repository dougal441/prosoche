---
created: 2026-08-13T12:04:27.110Z
title: Fix OPEN routing and Test Circle sequence error
area: general
severity: blocker
files:
  - tools/build_state_engine.py:1045
  - tools/build_state_engine.py:1067
  - src/PROSOCHE-Dumb.xml:27277
  - src/PROSOCHE-Dumb.xml:27283
  - src/PROSOCHE-Dumb.xml:28185
  - src/PROSOCHE-Sentient.xml:28519
  - src/PROSOCHE-Sentient.xml:28525
  - src/PROSOCHE-Sentient.xml:29427
---

## Problem

On-device testing of the manually created app-open automation does not enter the expected OPEN path. The automation wrapper has a Text action containing exactly `OPEN`, followed by Run Shortcut with its Input set to that Text magic variable. Opening a configured target app nevertheless displays the manual menu (`Status`, `Open Control Room`, `Sync My Profile`, and so on) instead of immediately firing the Circle 1 intervention.

A second failure is observable from that unexpected menu. Choosing **Test a Circle** displays nine buttons labelled Circle 1 through Circle 9, but selecting a Circle produces this error:

> No value provided. No value was provided to the Set Dictionary Value action for the key "sequence".

It is not yet known whether the OPEN misrouting and missing `sequence` value share one cause. Record them together because they were observed in the same first on-device automation test, but do not assume they are causally related.

## Solution

TBD after debugging. Reproduce and trace the received Shortcut Input through OPEN/MANUAL routing, then independently trace Test a Circle's state and `sequence` write. Fix each at its shared source, propagate to both variants, and leave a minimal regression check for OPEN routing and the Test Circle path.
