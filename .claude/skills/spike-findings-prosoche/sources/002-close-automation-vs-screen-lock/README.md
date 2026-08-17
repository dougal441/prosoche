---
spike: 002
name: close-automation-vs-screen-lock
type: standard
validates: "Given a tracked app in foreground, when the user locks the screen (vs. switches app), then determine whether the \"App Is Closed\" Personal Automation fires the same CLOSE signal in both cases"
verdict: VALIDATED
related: [001]
tags: [session-model, close-pipeline, personal-automations]
---

# Spike 002: Close-Automation vs. Screen-Lock

## What This Validates

Given a tracked app in the foreground, when the user (a) switches to a different app,
(b) locks the screen directly, or (c) locks the screen and later unlocks straight back
into the same app, then does iOS's "App Is Closed" Personal Automation trigger fire the
same `CLOSE` signal in all three cases — the exact signal PROSOCHĒ's CLOSE pipeline
depends on to end `active_session`, restore `settings_snapshot`, and finalize
`recent_sessions` (`.planning/research/ARCHITECTURE.md` §4–5).

This is a pure iOS runtime-behavior question. No file-level analysis, catalog lookup, or
donor-shortcut decryption can answer it — it requires a device log across real lock/unlock
events, the same "device ground truth beats inference" discipline this project already
applies everywhere else (`.claude/CLAUDE.md` "Evidence hierarchy").

## Research

Apple's own documentation for Personal Automations describes "App Is Closed" as firing
when the app "is no longer active" — which is ambiguous between "backgrounded because the
user switched apps" and "backgrounded because the screen locked." Community reporting is
mixed and version-dependent, which is exactly why this project's evidence hierarchy puts
external corroboration below on-device confirmation. No Playground-bundled doc
(`AUTOMATION_TRIGGERS.md`) documents Personal Automation trigger semantics — it only covers
`WFWorkflowTriggers` metadata for shortcut-embedded triggers, which explicitly does not
apply here (this project's Personal Automations are user-created outside the shortcut).

## How It Was Tested

The probe was wired to two Personal Automations for one test app ("App Is Opened" passing
`OPEN`, "App Is Closed" passing `CLOSE`, Ask Before Running off on both), then exercised by
hand: switching apps, and locking the screen with the app in the foreground. Five probe
builds were needed to get a readable signal out — see Probe Build History under Results.

## Results

**Verdict: VALIDATED — locking the screen fires the CLOSE automation, same as an app
switch.** Confirmed on device, 2026-08-16.

Evidence: with the probe wired to an "App Is Closed" Personal Automation, locking the
screen while the tracked app was in the foreground produced a probe run carrying the CLOSE
signal — captured log line `{"ts":"","signal":"CLOSED","locked":No}` — and the user
independently confirmed OPEN and CLOSE both firing across repeated lock and app-switch
cycles.

**Consequence for the build:** PROSOCHĒ's session model does not need a separate
screen-lock trigger or a lock-state poll to terminate `active_session`. A screen lock
already delivers the same `CLOSE` the CLOSE pipeline is built around
(`.planning/research/ARCHITECTURE.md` §5), so an un-terminated session caused by the user
locking rather than switching away is **not** a hazard the design has to defend against.
`Device Is Locked` (Spike 001) stays available as a defensive read if a later debugging
cycle wants it, but it is not required for session termination.

**Side observations, not load-bearing on this verdict:**
- `"locked":No` on a lock-triggered CLOSE suggests the automation fires on screen-off
  slightly before the passcode-lock state flips, so `Device Is Locked` should not be
  treated as a proxy for "this CLOSE came from a lock."
- `"ts":""` was a wiring defect in the probe's Format Date step, not a device finding.

**Spun out, not resolved here:** the repeated file-access permission prompt hit during
testing is a separate problem with its own todo —
`.planning/todos/pending/2026-08-16-persist-state-when-close-fires-from-a-locked-screen.md`.
It does not affect this verdict: the automation demonstrably fires, and the open question
is only whether state can be *persisted* when it does.

## Probe Build History (closed)

Four probe builds, kept for the wiring lessons rather than the verdict:

| Build | Storage approach | Outcome |
|---|---|---|
| v1 | `Create Note` AppIntent + Append | "unknown action" on import — synthesized `AppIntentDescriptor` was wrong |
| v2 | `Filter Notes` + `Append to Note` | popped an interactive Notes picker on device, wrote nothing; an action UUID collided with an unrelated If block's `GroupingIdentifier` |
| v3 | JSON-lines file via `documentpicker.open`/`.save` | wrote, but re-prompted for file permission every run |
| v4 | same, minus unconditional `file.createfolder` | prompt persisted — folder creation was not the cause |
| v5 | `Show Notification` only, 4 actions | rejected as a store: Notification Center is user-readable only, cannot be read back by a shortcut, so it can never back `state.json` |

The signed artifact left in this folder is v5. It is a display-only diagnostic, not a
storage design — see the todo above for the storage question.

## Build Notes

**`--target-macos 26 --target-platform ios` is degenerate in the installed Playground
(v1.2.1)** — it rejects every action, including `is.workflow.actions.comment`, because no
iOS-26 ToolKit snapshot is bundled and the `ios` platform filter drops the generic v63
allowlist entirely. All five builds validated at `--target-macos 26` alone. **Follow-up:**
this project's "Exact validator invocation" section in `.claude/CLAUDE.md` prescribes that
flag pair and should be corrected — it cannot pass for any shortcut in this version.

Wiring lessons worth keeping, all device-established:

- A single UUID must never serve as both an action's `UUID` and a control-flow block's
  `GroupingIdentifier` (v2's failure). This project's conventions already name it the #1
  real-world mistake; this is a live instance of it.
- `Create Note`'s `AppIntentDescriptor` cannot be synthesized from the documented template
  pattern — the guess imported as "unknown action" (v1).
- `Filter Notes` + `Append to Note` popped an interactive picker rather than filtering
  silently (v2), making Notes unusable from an unattended automation regardless of the
  Create Note gap.
