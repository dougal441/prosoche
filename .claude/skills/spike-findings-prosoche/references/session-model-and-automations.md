# Session Model and Automations

How OPEN/CLOSE actually behaves on the device, and what the session model must and must not defend against.

## Requirements

- The OPEN → Heat/Gravity/Pressure → Circle → intervention loop must work reliably on a real
  iPhone **without corrupting state**. If everything else fails, this must hold.
- Any shortcut wired into a Personal Automation must have **zero UI**.
- Personal Automations are **user-created by design** — they are not, and cannot be, part of
  the shipped artifact.

## How to Build It

### Screen lock terminates a session — no extra machinery needed

**Locking the screen fires the CLOSE automation, exactly as an app switch does.** Confirmed
on device 2026-08-16 (spike 002): with the probe wired to an "App Is Closed" Personal
Automation, locking the screen while the tracked app was foregrounded produced a probe run
carrying the CLOSE signal — logged as `{"ts":"","signal":"CLOSED","locked":No}` — and the
user independently confirmed OPEN and CLOSE both firing across repeated lock and app-switch
cycles.

**Consequence:** the session model needs **no** separate screen-lock trigger and **no**
lock-state poll to terminate `active_session`. An un-terminated session caused by locking
rather than switching away is not a hazard the design has to defend against.

### `Device Is Locked` is available as a defensive read

`is.workflow.actions.getdevicedetails` with `WFDeviceDetail = "Device Is Locked"` is
donor-confirmed (spike 001, Donor 10). Six `WFDeviceDetail` literals are confirmed on that
donor: `Device Model`, `Current Brightness`, `Current Volume`, `Current Appearance`,
`Device Is Locked`, plus Device Name / System Version / System Build Number from spike 003.

`Get Device Details` is a single-parameter, zero-wiring-hazard action — the
`WFTextTokenString`/`WFTextTokenAttachment` distinction applies only to what consumes its
output downstream.

**But do not use it as a proxy for "this CLOSE came from a lock."** On a lock-triggered
CLOSE the probe logged `"locked":No` — the automation fires on screen-off slightly *before*
the passcode-lock state flips.

### The tracked-app identity question

Personal Automations pass the triggering app's identity to the automation. Rather than
depending on `Get Current App` inside the invoked shortcut, **trust the automation's own app
filter** — if the shortcut was invoked by the OPEN automation at all, the app *is* the
configured target.

PROSOCHĒ never writes a third-party bundle id into a plist. `tools/build_state_engine.py:82`
defines a closed `APPS` set of six **first-party** apps (Notes, Voice Memos, Camera,
Reminders, Calendar, Contacts) matching `Donor - apps` exactly; tracked apps are chosen by
the user inside the Personal Automation and never appear in generated output.

## What to Avoid

- **Notes is not usable from an unattended automation via the naive path.** Spike 002 v2
  wired `Filter Notes` + `Append to Note` and it **popped an interactive Notes picker on
  device and wrote nothing**. The working pattern is the one Donor 8 proves — see
  `authoring-parameters.md` Step 2 — with the found note bound to a variable and consumed
  through `WFInput`. Note that `shownote` reads its note from `WFInput`; `target` is not a
  parameter the action defines and is silently ignored.
- **Show Notification cannot back a store.** Spike 002 v5 established this: Notification
  Center is user-readable only and cannot be read back by a shortcut, so it can never
  substitute for `state.json`.
- **Do not put any UI in an automation-triggered shortcut.** Log to a Note.
- **Do not reuse a UUID as both an action `UUID` and a `GroupingIdentifier`** — spike 002 v2
  hit this live.

## Constraints

- **iCloud file access re-prompts for permission on essentially every automation run**
  ("Always Allow" does not stick), and **cannot be granted at all while the screen is
  locked.** This is the one genuinely open hazard in the session model: the automation
  demonstrably fires on lock, but whether state can be *persisted* when it does is
  unresolved. Tracked at
  `.planning/todos/pending/2026-08-16-persist-state-when-close-fires-from-a-locked-screen.md`.
  Spike 002 tried and rejected four storage approaches (Create Note + Append; Filter + Append;
  JSON-lines file; the same minus `file.createfolder`) — the prompt persisted in all file
  variants, and folder creation was not the cause.
- **Personal Automation triggers cannot be exercised on a simulator at any effort.** Every
  question about them is rung 3+.
- Spike 001 does **not** resolve whether `Device Is Locked` reads accurately *during* an
  automation's brief execution window — a locked screen and a running background automation
  are not mutually exclusive states.

## Origin

Synthesized from spikes: 001, 002
Source files: `sources/001-device-is-locked-literal/`, `sources/002-close-automation-vs-screen-lock/`
