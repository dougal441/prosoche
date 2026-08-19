---
created: 2026-08-19T04:15:00.000Z
title: An OPEN's intervention can be deferred by minutes and surface after the app is closed — needs /gsd-debug
area: general
severity: major
files:
  - tools/build_state_engine.py
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
---

## Problem

**Device-observed, 2026-08-18, Core `873fa3db…`, fresh install.** Three consecutive OPENs on a
tracked app (22:12:46, 22:14:06, ~22:15) each advanced Heat, Gravity, Pressure and Circle and
wrote `state.json` normally — and **displayed nothing at all**. No Leaving/Continue menu, no
primitive. The app opened clean each time.

Then at **22:16**, on returning to the Home screen, the menu belonging to the **22:12:46** OPEN
appeared — *"PROSOCHĒ is at Circle 5"* — roughly **three and a half minutes late**, with the
triggering app long since closed.

## Why this is `major` rather than cosmetic

`PROJECT.md`'s stated core value is that when the user reaches for a tracked app,
*"PROSOCHĒ interrupts strongly enough that the user makes an actual choice"*. An interruption
that arrives three minutes later, after the app has been used and put down, is not that. It is
arguably worse than no interruption: it trains the user to dismiss a prompt that no longer refers
to anything they are doing, and it does so while the Circle keeps escalating.

**It is invisible in `state.json`.** Heat, Pressure, Circle, `active_session` and the session
record were all correct throughout. Only a person watching the screen can see it. No file-level
check, validator or decrypt can.

## Why this needs `/gsd-debug` and not a gap plan

**The mechanism is a hypothesis, and the behaviour is intermittent — both of which make a fix
plan premature.** Later the same session, OPENs displayed their menus promptly and in-context
again, repeatedly. So this is not a systematic "menus never show" defect; it is a state the
product falls into and climbs out of.

**Ranked hypothesis, explicitly not a localisation.** The best-supported reading is that the
22:11:40 OPEN — on the tracked app that carries a user **Screen Time limit** — had its menu
appear behind Apple's own *"You've reached your limit"* sheet and was never answered, and that
Shortcuts then serialised subsequent interactive surfaces behind that un-dismissed run. The
ordering fits; nothing measures it.

**First experiment, and it is cheap:** reproduce against a tracked app with **no** Screen Time
limit, to separate "a pending un-dismissed Shortcuts run blocks later ones" from "the Screen Time
sheet specifically causes it". If the deferral does not reproduce without a Screen Time limit,
the interaction is identified and the fix is scoped to it. If it does reproduce, the question
becomes whether the OPEN pipeline can detect and abandon a superseded interaction.

Do not chase this at the file level first: `.claude/CLAUDE.md` records that operator/operand
validity and control-flow behaviour are invisible in the plist, and this is a *timing and
foreground* question on top of that.

## Related, and worth checking in the same run

`universal_leaving()` is the OPEN path's sole entry to every primitive and is enclosed by the
silent-band conditional. Confirm the deferral is a **presentation** delay and not the pipeline
taking the Circle-0 branch and then re-running — the state trace suggests presentation, since the
Circle written to `state.json` matched the Circle the late menu announced.

## Evidence

`.planning/debug/device-state/README.md`, finding **F-12**, with the full timestamped trace and
the state readings for each of the three silent OPENs.
