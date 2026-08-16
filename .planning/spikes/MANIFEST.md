# Spike Manifest

## Ideas

### Session-model correctness under screen lock (spikes 001–002)

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

### Merge Dumb/Sentient forks into one shortcut (spikes 003–004)

Collapse PROSOCHĒ's two shipped forks (Dumb / Sentient) into a single shortcut, using the
same decrypted `Donor 10.shortcut` as the trigger — it shows
`is.workflow.actions.getdevicedetails` accepting `WFDeviceDetail = "Device Model"` as a
literal picker value on a real device, raising the question of whether hardware
capability could be auto-detected to drive the fork choice.

## Requirements

**From the screen-lock spikes:**

- `Device Is Locked` is confirmed usable as a `WFDeviceDetail` literal on
  `is.workflow.actions.getdevicedetails` — donor-shortcut ground truth, promotable above
  catalog-only evidence in `docs/BUILD-NOTES.md` CAP table.
- The CLOSE pipeline's correctness under screen-lock is an open empirical question that
  requires on-device testing — no file-level or catalog analysis can answer it (this is
  Automation-trigger *behavior*, not action *availability*).

**From the fork-merge spikes:**

- `WFWorkflowImportQuestions` cannot carry a runtime-computed default — it resolves before
  any action executes. Any capability check and its default would have to happen at
  first-run (or every run) via `Get Device Details`, cached in `state.json`, not via an
  import question. **Moot as of spike 003 — see below.**
- **Device-model-based hardware capability detection is infeasible.** `Get Device Details`
  → `Device Model` returns the bare literal `"iPhone"` on every device — no model
  identifier, no marketing name, no way to distinguish Apple-Intelligence-capable hardware
  (iPhone 15 Pro+) from ineligible hardware. No other `WFDeviceDetail` case (12 confirmed
  total — see spike 003) offers a usable proxy either. This closes off "auto-detect →
  smart default" as a mechanism entirely, not just as a spike 003 sub-question.
- **No try/catch exists in Shortcuts at all** — an action failure halts the entire
  shortcut, so "attempt on-device model, catch failure, save a boolean" cannot be built
  either (confirmed both via docs/web research and, separately, on real ineligible
  hardware — see spike 004).
- The single-shortcut merge must therefore rely on an explicit user-set toggle
  (`WFWorkflowImportQuestions`, "Do you have an iPhone 15 Pro or later and want to enable
  Sentient mode?") rather than any runtime detection or recovery.
- Use Model must never be invoked when the toggle is off — a safety/reliability gate, not
  just a UX default.
- The toggle cannot verify hardware eligibility. Safety is achieved by **ordering**, not
  detection: the core deterministic escalation must run before any Sentient-branch logic,
  so a Use Model halt on ineligible hardware costs only the bonus mirror text, never the
  core intervention. **Confirmed on real hardware** (iPhone 15 Pro + iPhone SE): on
  ineligible hardware, Use Model fails with a graceful native error ("support for selected
  model is downloading") rather than corrupting state or crashing, and the core escalation
  step, placed first, had already completed by the time of that failure.
- `WFFileErrorIfNotFound = false` (Get File) is the real answer to "no file-exists check"
  — cleaner than the attempt-and-treat-as-absent fallback CLAUDE.md currently documents.
  Worth folding into CLAUDE.md §3 item 2.
- Save File triggers a one-time OS permission prompt ("Allow to save 1 dictionary to a
  file") on first write per installation — not previously documented. Single-tap, not a
  blocker, but a real-build onboarding UX consideration.

## Spikes

| # | Name | Type | Validates | Verdict | Tags |
|---|------|------|-----------|---------|------|
| 001 | device-is-locked-literal | standard | Given Donor 10's decrypted plist, when inspected for `WFDeviceDetail`, then the literal `"Device Is Locked"` is present as donor-confirmed ground truth | VALIDATED | device-details, capability-audit, evidence-hierarchy |
| 002 | close-automation-vs-screen-lock | standard | Given a tracked app in foreground, when the user locks the screen (vs. switches app), then determine whether the "App Is Closed" Personal Automation fires the same `CLOSE` signal in both cases | VALIDATED — yes, screen lock fires CLOSE | session-model, close-pipeline, personal-automations |
| 003 | device-model-literal | standard | Given a real iPhone, when Get Device Details queries "Device Model", then the exact literal string format (identifier vs marketing name) is known | INVALIDATED ✗ | shortcuts, device-detection |
| 004 | capability-gate | standard | Given a single merged shortcut with a manual opt-in toggle, when the core deterministic escalation runs before the optional Sentient (Use Model) step, then a Use Model failure never prevents the core intervention from firing | VALIDATED ✓ | shortcuts, device-detection, state-machine |

## Spun-Out Work

- **Persisting state when CLOSE fires from a locked screen** —
  `.planning/todos/pending/2026-08-16-persist-state-when-close-fires-from-a-locked-screen.md`.
  Surfaced during spike 002: iCloud file access re-prompts for permission on every
  automation run ("Always Allow" does not stick), and cannot be granted at all while the
  screen is locked. Separate from this spike's verdict — the automation fires; whether
  state can be *saved* when it does is the open question.
