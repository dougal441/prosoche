---
name: spike-findings-prosoche
description: Implementation blueprint from PROSOCHĒ spike experiments — donor-confirmed parameter literals, the three-class picker rule, the evidence ladder, Sentient gating, session-model behaviour, and environmental-primitive recipes. Load when authoring or debugging Shortcuts plists for this project, choosing a literal or identifier, deciding what evidence a question needs, or building the Ash/Dimming/Silence or Use Model paths.
---

<context>
## Project: PROSOCHĒ — Nine Circles

PROSOCHĒ is a free, open-source iPhone Shortcut that restores the missing interval between
the impulse to open a habit-forming app and the act of consuming it. It watches user-selected
apps through native iOS Personal Automations (App Is Opened / Is Closed), accumulates
behavioural **Pressure** from clustered and repeated openings, and escalates the user through
nine progressively stronger friction "Circles." It ships as two forks from one engine —
**Dumb** (fully deterministic) and **Sentient** (same engine plus Apple's On-Device model as
an attention mirror). iOS 26.x, native Shortcuts only, no companion app, no private APIs.

Spike sessions wrapped: 2026-08-16, 2026-08-17
</context>

<requirements>
## Requirements

Non-negotiable design decisions that emerged from spiking. Every reference honours these.

**Authoring**
- Never fabricate a literal. If it cannot be sourced from a donor, the enum-cases catalog, or
  an `.intentdefinition`, it is not known — use the safest fallback and record the deviation.
- Never write an entity identifier into a plist. Find the entity at runtime.
- An `.intentdefinition` tells you what parameters *exist* and what a picker's cases are
  *called*. Only a donor tells you what gets *written*.

**Sentient**
- Use Model must never be invoked when the toggle is off — a safety gate, not a UX default.
- The core deterministic escalation must run **before** any Sentient-branch logic. Safety is
  achieved by ordering, not detection, because Shortcuts has no try/catch.
- The fork choice rests on an explicit user toggle. Hardware capability detection is
  architecturally impossible on iOS 26 Shortcuts and must not be attempted.
- The model never controls arithmetic, thresholds, timers, Circle IX, or any safety decision.

**Safety**
- Every environmental change must be captured before it is applied and reliably restored.
  Capture-and-restore reliability is the safety mechanism, not avoidance of the extreme.
- Where no read-back exists, the remedy is the opt-in guard, not inference.

**Evidence**
- Never climb the evidence ladder higher than the open question requires, and never skip a
  rung that would have caught a defect in the probe itself.
- A probe's result is recorded, not consumed — into `docs/BUILD-NOTES.md` and
  `docs/CAPABILITY-DECISIONS.md`.
</requirements>

<findings_index>
## Feature Areas

| Area | Reference | Key Finding |
|------|-----------|-------------|
| Authoring parameters | `references/authoring-parameters.md` | Three-class rule (synthesizable / runtime-derivable / hand-selection-only) predicts from the catalog alone whether a parameter can be written offline. **PROSOCHĒ has zero hand-selection blockers across all 51 emitted actions.** |
| Evidence and probes | `references/evidence-and-probes.md` | The four-rung ladder, the AEA1 donor round-trip, and the correct validator invocation. **Rung 2 tests the build, not the import — the simulator cannot import a signed `.shortcut`.** |
| Sentient and capability gating | `references/sentient-and-capability-gating.md` | `WFLLMModel = "Apple Intelligence on Device"` (donor). Hardware detection is impossible; ordering is the only fail-safe. **Its ineligible-hardware behaviour is unproven** — the failure window is provisioning, not eligibility, so it reaches capable devices at first run. |
| Session model and automations | `references/session-model-and-automations.md` | **Screen lock fires CLOSE**, same as an app switch — no extra trigger or poll needed. Open hazard: file-permission prompts cannot be granted while locked. |
| Environmental primitives | `references/environmental-primitives.md` | Ash is real on iOS under `AXToggleColorFiltersIntent`; both legs donor-confirmed (`state` `1`/`0`, omit `operation`). Still no accessibility read-back. |

## Fast lookups

Donor-confirmed literals — full table in `references/authoring-parameters.md` Step 4:

| Where | Literal |
|---|---|
| `askllm.WFLLMModel` | `"Apple Intelligence on Device"` |
| `AXToggleColorFiltersIntent.state` | `1` = On, `0` = Off; omit `operation` |
| `getdevicedetails.WFDeviceDetail` | `Device Model` · `Current Brightness` · `Current Volume` · `Current Appearance` · `Device Is Locked` |
| Notes folder | `applenotes:folder/DefaultFolder-CloudKit` |
| `openapp.WFSelectedApp.TeamIdentifier` | `"0000000000"` (first-party) |

Validator invocation — the **two-gate rule** (stated in full in `.claude/CLAUDE.md` §1
`### Exact validator invocation`; measurements in `docs/BUILD-NOTES.md` §22):

```bash
validate-shortcut --target-macos 26 --target-platform all "X.xml"   # gate A: MANDATORY, expect exit 1 + the waiver
validate-shortcut --target-macos 27 --target-platform all "X.xml"   # gate B: ADVISORY, expect exit 1
python3 docs/gate_a_residue_check.py                                # the executable form of gate A
```

**Both gates carry a permanent waiver, so neither can exit zero, and neither raw command
belongs in a definition of done.** Amended 2026-08-19 (phase 14, D-14-01); the superseded
wording — which demanded a clean gate-A report — lived in the code block above and in the
paragraph that stood here, and is cited rather than restated.

- **Gate A is mandatory and its obligation is that the residue equal exactly the enumerated
  waiver.** Two line families, `Unknown AppIntent identifier` and the missing-
  `AppIntentDescriptor` line, both scoped to
  `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` alone —
  15 sites per fork × 2 families = 30 lines. A descriptor-less action emits both per
  instance, which is why a one-family waiver would be unsatisfiable. **Satisfy gate A by
  running `python3 docs/gate_a_residue_check.py`**, which fails on any other line and on any
  change to the count in either direction. Never widen the waiver and never substitute the
  `UA*` macOS twin.
- **Gate B is advisory** and carries a permanent one-line waiver per fork (`WFCreateNoteInput`
  on `com.apple.mobilenotes.SharingExtension`, device-donor ground truth that outranks the
  catalog). That single line is the expected result, not a build failure. Anything gate B
  reports *outside* the waiver is a real finding.

Gate B uses `--target-platform all`, not `ios`: the `ios` setting excludes every
`macOS 27`-tagged catalog entry, dropping all four Notes actions out of checking
(1105 enum-checked identifiers under `all` versus 455 under `ios`).

Never `--target-macos 26 --target-platform ios` — that pair rejects every action.

## Promotions still pending

Two spike findings that should be carried into `.claude/CLAUDE.md` and `docs/`:

1. **§3 item 15** — `WFLLMModel` from "UNVERIFIED — do not guess" to **VERIFIED (donor)**,
   plus the summary-table row.
2. **§9** — correct the rung-2 row: the simulator cannot import a signed `.shortcut`.

## Source Files

Original spike READMEs, decrypted donor XML, probe sources, and the corpus sweep script are
preserved in `sources/` for complete reference.
</findings_index>

<metadata>
## Processed Spikes

- 001-device-is-locked-literal (VALIDATED)
- 002-close-automation-vs-screen-lock (VALIDATED)
- 003-device-model-literal (INVALIDATED)
- 004-capability-gate (PARTIAL — downgraded 2026-08-17, was VALIDATED)
- 005-ios-color-filters-identifier (VALIDATED)
- 006-picker-serialisation-taxonomy (VALIDATED)
- 007-unresolvable-picker-failure-mode (PARTIAL)
- 008-use-model-picker-literal (VALIDATED)
- 009-prosoche-exposure-audit (VALIDATED)
</metadata>
