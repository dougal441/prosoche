# Spike Conventions

Patterns and stack choices established across spike sessions. New spikes follow these
unless the question requires otherwise.

## Stack

This project's spikes are iOS Shortcuts (`.shortcut` files), authored and signed via the
Shortcuts Playground toolchain (`.claude/CLAUDE.md`), not code. There is no runnable app
stack in the usual sense — "running" a spike means importing a signed `.shortcut` onto a
real iPhone and exercising it there. The build Mac cannot execute Shortcuts itself.

## Structure

- Each spike folder holds: `README.md` (frontmatter + findings), the signed
  `.shortcut` artifact when the spike produces one, and the unsigned editable `.xml`
  source alongside it.
- Diagnostic/probe shortcuts built for a spike are named descriptively (e.g. "Lock Signal
  Probe") and kept fully standalone — no dependency on the production PROSOCHĒ shortcut or
  its `state.json`.
- When a spike's evidence is a decrypted donor `.shortcut` (from `.planning/debug/`), the
  recovered XML is archived in the spike folder for reference.

## Patterns

- **Building the probe:** dispatch the `shortcuts-playground:shortcut-builder` agent
  rather than authoring plist XML by hand — it owns the full build→validate→sign loop and
  already carries this project's wiring-pitfall knowledge (`.claude/CLAUDE.md`
  "seven parameter-defect axes").
- **Verifying a device-behavior question:** decrypting/inspecting a plist only answers
  *structural* questions (does an action/parameter exist). *Behavioral* questions (does an
  automation trigger fire under condition X) require a real on-device log and a human
  checkpoint — these spikes end PENDING until the user reports back what the device log
  shows, per this project's own evidence hierarchy (donor/device ground truth outranks
  catalog or inference).
- **Silent automation probes:** any shortcut wired into a Personal Automation must have zero
  UI (no Show Result/Show Alert) — an automation that displays something interrupts the
  user on every trigger. Log to a Note instead.

## Tools & Libraries

- `shortcuts-playground:shortcut-builder` agent for build/validate/sign.
- `aea decrypt` + `aa extract` (per `.claude/CLAUDE.md` §8) to recover plist XML from any
  signed `.shortcut`, including donor artifacts and this project's own probe outputs.
- Validator note: `--target-macos 26 --target-platform ios` was found to be degenerate in
  the installed Playground v1.2.1 (rejects every action, no bundled iOS-26 snapshot) —
  use `--target-macos 26` alone, or `--target-macos 26 --target-platform all`, until the
  project's CLAUDE.md is corrected.
