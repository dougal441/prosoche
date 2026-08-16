# Spike Manifest

## Idea

PROSOCHĒ's session model (`active_session`) is opened and closed entirely by two iOS
Personal Automations calling the shortcut with literal input `"OPEN"` / `"CLOSE"`
(`.planning/research/ARCHITECTURE.md` §4). The open question: when a user locks their
phone's screen while a tracked app is in the foreground, does the "App Is Closed"
Personal Automation actually fire — giving PROSOCHĒ the same `CLOSE` signal it gets when
the user switches to a different app — or does locking leave `active_session` open
indefinitely until the user reopens and then leaves the app some other way? This matters
because an un-terminated session distorts session-duration Contract fidelity and leaves
`settings_snapshot` (Dimming/Silence restores) un-restored until Emergency Restore or
cooldown-natural-expiry.

The spike also captures a side-finding: decrypting `Donor 10.shortcut` (a user-built
donor artifact dropped in `.planning/debug/`) confirms the exact `WFDeviceDetail` literal
`"Device Is Locked"` on `is.workflow.actions.getdevicedetails` (Get Device Details) with
**donor-shortcut ground truth**, not just catalog evidence — per this project's own
evidence hierarchy (`.claude/CLAUDE.md` "Evidence hierarchy"), donor shortcuts outrank
the ToolKit catalog. This gives future debugging cycles a defensive read: PROSOCHĒ can
check whether the screen is currently locked at any point in its OPEN/CLOSE pipeline.

## Requirements

- `Device Is Locked` is confirmed usable as a `WFDeviceDetail` literal on
  `is.workflow.actions.getdevicedetails` — donor-shortcut ground truth, promotable above
  catalog-only evidence in `docs/BUILD-NOTES.md` CAP table.
- The CLOSE pipeline's correctness under screen-lock is an open empirical question that
  requires on-device testing — no file-level or catalog analysis can answer it (this is
  Automation-trigger *behavior*, not action *availability*).

## Spikes

| # | Name | Type | Validates | Verdict | Tags |
|---|------|------|-----------|---------|------|
| 001 | device-is-locked-literal | standard | Given Donor 10's decrypted plist, when inspected for `WFDeviceDetail`, then the literal `"Device Is Locked"` is present as donor-confirmed ground truth | VALIDATED | device-details, capability-audit, evidence-hierarchy |
| 002 | close-automation-vs-screen-lock | standard | Given a tracked app in foreground, when the user locks the screen (vs. switches app), then determine whether the "App Is Closed" Personal Automation fires the same `CLOSE` signal in both cases | PENDING — probe built, validated, signed; awaiting on-device run | session-model, close-pipeline, personal-automations |
