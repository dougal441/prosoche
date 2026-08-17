# Sentient and Capability Gating

Building the optional Apple Intelligence branch so that it can never harm the deterministic core.

## Requirements

These are non-negotiable, and each was established by a spike rather than chosen on paper:

- **Use Model must never be invoked when the toggle is off** — a safety/reliability gate,
  not a UX default.
- **The core deterministic escalation must run before any Sentient-branch logic.** Safety is
  achieved by **ordering**, not detection.
- The single-shortcut merge relies on an **explicit user-set toggle**
  (`WFWorkflowImportQuestions`), never on runtime detection or recovery.
- The model never controls arithmetic, thresholds, timers, Circle IX, or any safety decision.

## How to Build It

### Step 1 — the Use Model action

```xml
<key>WFWorkflowActionIdentifier</key>
<string>is.workflow.actions.askllm</string>
<key>WFWorkflowActionParameters</key>
<dict>
    <key>UUID</key><string>…</string>
    <key>WFLLMModel</key><string>Apple Intelligence on Device</string>
</dict>
```

**`WFLLMModel = "Apple Intelligence on Device"`** — donor ground truth (spike 008,
`sources/008-use-model-picker-literal/UseModel-Shortcut.xml`). Not `"On-Device"`, not
`"On Device"`, not an integer. None of the three candidates the capability audit was weighing
was correct.

Of 526 distinct enum-picker types across the entire first-party surface, this was the **only**
one absent from `toolkit-v78-first-party-enum-cases.json` — and it is exactly the item
`.claude/CLAUDE.md` §3 item 15 flagged as the top unknown. **That §3 item 15 verdict, and its
summary-table row, should be promoted from "UNVERIFIED — do not guess" to VERIFIED (donor).**

Parameter notes:
- `WFLLMPrompt` — catalog type `str`, so it needs `WFTextTokenString` treatment (axis 2).
  The donor left it empty, so it confirms the model literal only, **not** the prompt envelope.
- `WFGenerativeResultType` — **absent in the donor**, i.e. left at default. The capability
  audit assumed the literal `"Text"` had to be written; omitting it appears to match the
  device byte-for-byte. Single-donor evidence — see the absence caveat in
  `authoring-parameters.md`.
- `WFAllowWebSearch`, `FollowUp` — OS27-gated. Omit for a target-26 build. The donor agrees.

### Step 2 — the ordering fail-safe

This is the entire safety design:

```
[core deterministic escalation]      ← unconditional, FIRST, no dependency on anything below
[if ai_enabled toggle is on]
    [Use Model …]                    ← may fail; failure halts the shortcut
    [consume the mirror text]
[end if]
```

**Ordering is a structural property** — the core runs first and depends on nothing below it,
so *any* downstream halt is contained by construction. Build it this way. What follows is
what has and has not actually been observed.

**Observed (spike 004, 2026-08-16):**

- *iPhone 15 Pro, toggle off:* core escalation fired, no Use Model attempt.
- *iPhone 15 Pro, toggle on:* core escalation fired **first**, then a one-time Save File
  permission prompt, then the Use Model result.
- *An iPhone SE, toggle on:* core escalation fired at action index 3 — the first executable
  step — then Use Model halted with a native, non-crashing error, *"Support for selected
  model is downloading."* The core had already completed. **The ordering held under a real
  failure.** That single observation stands.

**Not observed — do not claim these (verdict downgraded to PARTIAL, 2026-08-17):**

- **Behaviour on genuinely ineligible hardware.** The spike's draft XML omits `WFLLMModel`
  entirely, so **both runs exercised the undocumented default model source, not the pinned
  On-Device path PROSOCHĒ ships.** Separately, *"Support for selected model is downloading"*
  is a **provisioning-state** message, not an eligibility rejection — an iPhone 16e (A18,
  8 GB, capable) later ran the same shortcut successfully once its models had downloaded,
  which shows the message tracks download state. The SE run is equally consistent with
  ineligible hardware or with a device that had simply not provisioned. Nothing distinguishes
  them, and the SE's generation was never recorded.
- **That a Use Model failure is always a graceful halt** rather than a hang or partial write.

**The consequence that matters for the merge.** If the failure is about provisioning rather
than eligibility, **capable devices fail too, in an ordinary state**: models are a ~7 GB
download needing Wi-Fi and power and are absent on a fresh or freshly-reset device, and the
user can switch Apple Intelligence off in Settings. Under two forks that window is only
reachable by someone who deliberately installed the AI fork. Under one merged product it is
reachable by a new user on perfectly good hardware **during first run** — PROSOCHĒ's most
fragile moment. Scope the merge risk as "any user whose models haven't landed yet," not
"users who answer the toggle wrongly on old hardware."

### Step 3 — the toggle

`WFWorkflowImportQuestions`, worded as a capability question the user can actually answer:
*"Do you have an iPhone 15 Pro or later and want to enable Sentient mode?"*

Implement it as a **Text** action holding the literal default, targeted by one import
question — `WFWorkflowImportQuestions` is a literal-text-prefill mechanism, not a form
builder. Read and validate the value at bootstrap.

**The validator does not check `WFWorkflowImportQuestions` at all** — zero references to the
key in `validate_shortcut.py`. A malformed import question will not be caught by the Craig
Loop. Correctness here is entirely the build's responsibility.

## What to Avoid

- **Do not attempt hardware capability detection. It is architecturally impossible.**
  `Get Device Details` → `Device Model` returns the bare literal **`"iPhone"`** on every
  device — no model identifier, no marketing name. An iPhone 8 and an iPhone 16 Pro Max
  return the identical string. Verified on device (spike 003, iOS 26.6).
- **No other signal substitutes**, all checked and all dead ends:
  - `System Build Number` (`23G71`) is a pure OS-build id, identical across all hardware.
  - `System Version` (`26.6`) can't stand in — iOS 26 runs back to iPhone 11 / SE 2nd gen,
    and the large majority of that population is Apple-Intelligence-ineligible. The plain
    iPhone 15 / 15 Plus don't qualify (A16, 6 GB) despite the same generation and OS as the
    15 Pro, so capability doesn't even track by device generation, only by SKU/chip.
  - `Screen Width`/`Height` repeat across generations.
  - The real check, `SystemLanguageModel.default.availability`, is a Swift Foundation Models
    API for native app code — unreachable from Shortcuts, and ruled out anyway by the
    project's no-companion-app constraint.
  - No app-presence check exists in Shortcuts, so probing for an Apple-Intelligence-only
    system app as a proxy is not possible either.
- **Do not design any "attempt, catch failure, save a boolean" recovery. There is no
  try/catch in Shortcuts at all.** An action failure halts the entire shortcut; nothing after
  it runs. Confirmed via docs, via an observed halt on device, and directly by an Apple DTS
  engineer: *"there is currently no way to detect an error from an action."*
- **Do not put anything load-bearing after a Use Model call.** Whatever follows it will not
  run whenever the model is unavailable — which includes capable hardware mid-provisioning,
  not just ineligible hardware.
- **Do not assume `WFWorkflowImportQuestions` can carry a runtime-computed default.** It
  resolves before any action executes. Any capability check would have to happen at run time
  and be cached in `state.json` — and per spike 003 there is no such check to run.

## Constraints

- The toggle **cannot verify hardware eligibility**. It is a user assertion. Safety comes
  from ordering alone.
- **Save File triggers a one-time OS permission prompt** ("Allow to save 1 dictionary to a
  file") on first write per installation. Single tap, not a blocker, but a real first-run UX
  interruption the onboarding should anticipate. It can also re-prompt on every automation
  run and **cannot be granted while the screen is locked** — see
  `session-model-and-automations.md`.
- Apple Intelligence cannot be tested on the simulator. This path is rung 3+ only.

### Open — four device runs nobody has done

Spike 004 is **PARTIAL** until these land. The last two are the ones that decide the merge.

| Open question | Evidence needed |
|---|---|
| Does the **On-Device-pinned** `askllm` behave like the unpinned one? | Re-run the gate with `WFLLMModel = "Apple Intelligence on Device"` — the config that actually ships |
| Is a genuinely-ineligible-hardware failure a graceful halt, or a hang / partial write? | A run on a **known** ineligible device — iPhone 15 / 15 Plus (A16), iPhone 14 or earlier, or an iPhone SE 2nd/3rd gen — with the generation recorded |
| What happens on **capable hardware with models not yet downloaded**? | A capable device with Apple Intelligence freshly enabled, run before provisioning finishes |
| What happens with **Apple Intelligence switched off** on capable hardware? | Same device, AI toggled off in Settings |

For every re-run, record: device model, iOS version, whether Apple Intelligence is enabled,
and whether the model download had completed. The original run recorded none of these, which
is why its failure could never be attributed.

## Origin

Synthesized from spikes: 003, 004, 008
Source files: `sources/003-device-model-literal/`, `sources/004-capability-gate/`,
`sources/008-use-model-picker-literal/`
