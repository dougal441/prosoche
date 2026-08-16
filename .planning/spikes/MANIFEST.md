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

## Spikes

| # | Name | Type | Validates | Verdict | Tags |
|---|------|------|-----------|---------|------|
| 001 | device-model-literal | standard | Given a real iPhone, when Get Device Details queries "Device Model", then the exact literal string format (identifier vs marketing name) is known | INVALIDATED ✗ | shortcuts, device-detection |
| 002 | capability-gate | standard | ~~Given the confirmed Device Model literal, when built into a capability table + state.json cache + Control Room override, then the Use Model branch only fires on capable hardware~~ — **superseded, see pivot decision** | SUPERSEDED | shortcuts, device-detection, state-machine |
