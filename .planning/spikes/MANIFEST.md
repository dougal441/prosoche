# Spike Manifest

## Idea

Collapse PROSOCHĒ's two shipped forks (Dumb / Sentient) into a single shortcut that
detects, at runtime, whether the device is Apple-Intelligence-capable (On-Device model
present) and defaults the Sentient behaviour on/off accordingly — while still letting the
user override that default via the existing Control Room menu. Triggered by evidence in
`Donor 10.shortcut`, which shows `is.workflow.actions.getdevicedetails` accepting
`WFDeviceDetail = "Device Model"` as a literal picker value on a real device.

## Requirements

- `WFWorkflowImportQuestions` cannot carry a runtime-computed default — it resolves before
  any action executes. Any capability check and its default would have to happen at
  first-run (or every run) via `Get Device Details`, cached in `state.json`, not via an
  import question. **Moot as of spike 001 — see below.**
- **Device-model-based hardware capability detection is infeasible.** `Get Device Details`
  → `Device Model` returns the bare literal `"iPhone"` on every device — no model
  identifier, no marketing name, no way to distinguish Apple-Intelligence-capable hardware
  (iPhone 15 Pro+) from ineligible hardware. No other `WFDeviceDetail` case (12 confirmed
  total — see spike 001) offers a usable proxy either. This closes off "auto-detect →
  smart default" as a mechanism entirely, not just as a spike 001 sub-question.
- The single-shortcut merge must therefore rely on an explicit user-set toggle (Control
  Room menu item, e.g. "Enable Sentient Mode") rather than any runtime detection. This was
  ponytail's original lazy-alternative proposal, now the only remaining viable path.
- Use Model must never be invoked when the toggle is off — a safety/reliability gate, not
  just a UX default.
- The toggle cannot verify hardware eligibility (spike 001). Safety is achieved by
  **ordering**, not detection: the core deterministic escalation must run before any
  Sentient-branch logic, so a Use Model halt on ineligible hardware costs only the bonus
  mirror text, never the core intervention.
- `WFFileErrorIfNotFound = false` (Get File) is the real answer to "no file-exists check"
  — cleaner than the attempt-and-treat-as-absent fallback CLAUDE.md currently documents.
  Worth folding into CLAUDE.md §3 item 2.
- Save File triggers a one-time OS permission prompt ("Allow to save 1 dictionary to a
  file") on first write per installation — not previously documented. Single-tap, not a
  blocker, but a real-build onboarding UX consideration.
- Confirmed on real hardware (iPhone 15 Pro + iPhone SE): the ordering fail-safe holds.
  On ineligible hardware, Use Model fails with a graceful native error ("support for
  selected model is downloading") rather than corrupting state or crashing — and the core
  escalation step, placed first, had already completed by the time of that failure.

## Spikes

| # | Name | Type | Validates | Verdict | Tags |
|---|------|------|-----------|---------|------|
| 001 | device-model-literal | standard | Given a real iPhone, when Get Device Details queries "Device Model", then the exact literal string format (identifier vs marketing name) is known | INVALIDATED ✗ | shortcuts, device-detection |
| 002 | capability-gate | standard | Given a single merged shortcut with a manual opt-in toggle, when the core deterministic escalation runs before the optional Sentient (Use Model) step, then a Use Model failure never prevents the core intervention from firing | VALIDATED ✓ | shortcuts, device-detection, state-machine |
