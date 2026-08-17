---
spike: 008
name: use-model-picker-literal
type: standard
validates: "Given the unanalysed Use Model.shortcut donor, when decrypted, then the exact WFLLMModel On-Device literal becomes device ground truth"
verdict: VALIDATED
related: [004, 006]
tags: [capability-audit, evidence-hierarchy, donor, sentient, use-model, pickers]
---

# Spike 008: Use Model Picker Literal

## What This Validates

**Given** the unanalysed `Use Model.shortcut` donor in `.planning/debug/`, **when**
decrypted, **then** the exact `WFLLMModel` On-Device literal becomes device ground truth.

This closes what `.claude/CLAUDE.md` §3 item 15 calls *"the single most important
UNVERIFIED item for the Sentient fork,"* under a standing instruction that it **must not
be guessed**. Spike 006 independently arrived at the same item from the other direction:
of 526 distinct enum-picker types across the entire first-party surface,
`com_apple_shortcuts_wfask_llmmodel_parameter` is the **only one absent** from
`toolkit-v78-first-party-enum-cases.json`.

## Research

CLAUDE.md's audit had three candidate spellings in play and refused to pick between them:
`"On-Device"`, `"On Device"`, or an integer code. External reporting (MacStories,
Apple's iOS 26 notes) confirmed the picker offers three sources — On-Device, Private
Cloud Compute, Extension Model — but no source gave the plist literal. The prescribed
remedy was an on-device round trip: author in Shortcuts.app, pick the model by hand,
export, decrypt, read the literal back.

That round trip had **already been performed** — the donor has been sitting in
`.planning/debug/` since 2026-08-16, unanalysed.

## How to Run

```bash
python3 -c 'import plistlib;p=plistlib.load(open("UseModel-Shortcut.xml","rb"));print(p["WFWorkflowActions"])'
```

The decrypted plist is archived as `UseModel-Shortcut.xml` in this folder.

## Investigation Trail

Decrypted the donor via the AEA1 round trip (CLAUDE.md §8). It contains exactly one
action and nothing else — a clean, single-purpose probe:

```xml
<key>WFWorkflowActionIdentifier</key>
<string>is.workflow.actions.askllm</string>
<key>WFWorkflowActionParameters</key>
<dict>
    <key>UUID</key>
    <string>5CD39B14-6405-4285-A29F-1C8A5A0844D4</string>
    <key>WFLLMModel</key>
    <string>Apple Intelligence on Device</string>
</dict>
```

`WFWorkflowClientVersion` is `4711`, consistent with the rest of the donor set.

## Results

**VALIDATED — tier 1, device ground truth.**

```
WFLLMModel = "Apple Intelligence on Device"
```

Not `"On-Device"`, not `"On Device"`, not an integer. None of the three candidates
CLAUDE.md was weighing was correct — a direct vindication of the do-not-guess rule.
The prose spelling includes the product name and uses lowercase "on".

### Secondary findings

1. **`WFLLMPrompt` is absent.** The donor was authored with the model picked but the
   request field left empty — so this donor confirms the model literal only, and does
   *not* confirm the prompt's serialization envelope. Per the seven parameter-defect axes,
   `WFLLMPrompt` is catalog type `str` and therefore needs `WFTextTokenString` treatment
   (axis 2). Unconfirmed by donor; follow the axis rule.
2. **`WFGenerativeResultType` is absent** — left at default. Consistent with spike 005's
   rule that absence often means "left at default, and the default may be what you want."
   CLAUDE.md's audit assumed the literal `"Text"` had to be written; this donor suggests
   omitting it matches the device byte-for-byte. Note spike 005's caveat: absence in a
   single donor is not proof of a default value. Two donors would settle it.
3. **`WFAllowWebSearch` and `FollowUp` are absent**, as CLAUDE.md's OS27-gating guidance
   already prescribed for a target-26 build. The donor agrees.

### What this does *not* settle

Availability and runtime behaviour are untouched by this spike. This spike settles the
**literal**, so the Sentient branch can now be authored offline without a guessed picker
value — it does not relax the ordering requirement or the `ai_enabled` gate.

**Corrected 2026-08-17.** This section originally read that "spike 004 already established
the safety posture on real ineligible hardware." It did not — spike 004 was downgraded to
PARTIAL because its ineligible-hardware leg was never confirmed to be ineligible. What
spike 004 supports is narrower: a real `Use Model` failure did not pre-empt the core
escalation. Whether a failure is always a graceful halt, and how the pinned On-Device path
behaves when the model is unavailable, remain open.

**This spike sharpens that open question rather than closing it.** Spike 004's runs omitted
`WFLLMModel` entirely, so they exercised the undocumented default model source. The literal
recovered here — `"Apple Intelligence on Device"` — is the configuration PROSOCHĒ actually
ships, and it has **never been exercised on a device where the model was unavailable.**
Re-running spike 004's gate with this literal pinned is now the first of its four open
device runs.

### Promotion

CLAUDE.md §3 item 15's verdict should move from
**"UNVERIFIED — do not guess, confirm via device round-trip"** to
**VERIFIED (donor ground truth)**, and the summary-table row
"Use Model — On-Device model-source literal" updated to match. Spike 009 carries this
through to `docs/BUILD-NOTES.md` and `docs/CAPABILITY-DECISIONS.md`.
