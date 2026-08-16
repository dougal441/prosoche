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
  any action executes. The capability check and its default must happen at first-run (or
  every run) via `Get Device Details`, cached in `state.json`, not via an import question.
- Any override of the auto-detected default lives in the Control Room menu (Choose from
  Menu), not a second import question.
- Use Model must never be invoked when the device is not Apple-Intelligence-capable —
  this is a safety/reliability gate, not just a UX default.

## Spikes

| # | Name | Type | Validates | Verdict | Tags |
|---|------|------|-----------|---------|------|
| 001 | device-model-literal | standard | Given a real iPhone, when Get Device Details queries "Device Model", then the exact literal string format (identifier vs marketing name) is known | PARTIAL ⚠ | shortcuts, device-detection |
| 002 | capability-gate | standard | Given the confirmed Device Model literal, when built into a capability table + state.json cache + Control Room override, then the Use Model branch only fires on capable hardware and the override correctly flips the default | PENDING | shortcuts, device-detection, state-machine |
