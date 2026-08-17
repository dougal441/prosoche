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
| Sentient and capability gating | `references/sentient-and-capability-gating.md` | `WFLLMModel = "Apple Intelligence on Device"` (donor). Hardware detection is impossible; ordering is the only fail-safe, and it is verified on real ineligible hardware. |
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

Validator invocation — **both must pass**:

```bash
validate-shortcut --target-macos 26 "X.xml"
validate-shortcut --target-macos 27 --target-platform ios "X.xml"
```

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
- 004-capability-gate (VALIDATED)
- 005-ios-color-filters-identifier (VALIDATED)
- 006-picker-serialisation-taxonomy (VALIDATED)
- 007-unresolvable-picker-failure-mode (PARTIAL)
- 008-use-model-picker-literal (VALIDATED)
- 009-prosoche-exposure-audit (VALIDATED)
</metadata>
