---
quick_id: 260817-fae
description: Downgrade spike 004 to PARTIAL — the ineligible-hardware leg was never tested
date: 2026-08-17
status: complete
---

# Quick Task 260817-fae — Summary

## Trigger

The project owner reported that their **iPhone 16e**, with Apple Intelligence models
downloaded, ran the Capability Gate shortcut and returned the Sentient result successfully.
The 16e is A18 / 8 GB and **is** Apple-Intelligence-capable, so the device spike 004 recorded
as its ineligible-hardware test was not established to be ineligible at all.

## Work found already done

A concurrent session had already downgraded and reassessed the primary artifacts before this
task started (uncommitted in the working tree):

- `.planning/spikes/004-capability-gate/README.md` — frontmatter `verdict: PARTIAL`, a
  downgrade banner, and a full **Reassessment (2026-08-17)** section with sourced research
- `.planning/spikes/MANIFEST.md` — requirements bullet and the 004 spike-table row
- `.planning/ROADMAP.md` — the Phase 21 spike-004 bullet

That reassessment is stronger than this task's original plan and was left intact. It found
two problems the plan had not:

1. **The runs never used the shipped configuration.** Spike 004's draft XML omits
   `WFLLMModel` entirely, so both device runs exercised the undocumented *default* model
   source, not the pinned On-Device path `src/PROSOCHE-Sentient.xml` ships.
2. **The failure class is wider than "ineligible hardware," which changes the merge risk.**
   *"Support for selected model is downloading"* is a provisioning message. Models are a
   ~7 GB download absent on a fresh device, and users can switch Apple Intelligence off. So
   **capable hardware fails too** — and under one merged product that window is hit by a new
   user during first run, PROSOCHĒ's most fragile moment. The merge risk was scoped as "users
   who answer the toggle wrongly on old hardware"; it is actually "any user whose models
   haven't landed yet."

## Work done here (the gaps)

| File | Change |
|---|---|
| `.claude/skills/.../references/sentient-and-capability-gating.md` | Rewrote Step 2 into *observed* vs *not observed*; framed ordering as a structural property to build by; added the merge-risk consequence; replaced the stale caveat with the four open device runs; corrected the try/catch line to cite Apple DTS |
| `.claude/skills/.../SKILL.md` | Feature-area row and processed-spikes list |
| `.planning/spikes/008-use-model-picker-literal/README.md` | Removed its citation of the false claim; sharpened it — the recovered literal is the config that has **never** been exercised with the model unavailable |
| `.planning/spikes/CONVENTIONS.md` | No-try/catch bullet no longer cites "real ineligible hardware"; cites the Apple DTS statement |
| `.planning/spikes/WRAP-UP-SUMMARY.md` | Verdict-table row and the key-findings paragraph |
| `.planning/spikes/004-capability-gate/README.md` | Inline correction markers in the superseded `## Results` section (kept verbatim — the misattribution is the lesson) |
| `.claude/skills/.../sources/004-*/README.md`, `sources/008-*/README.md` | Re-synced from the corrected originals |

The skill reference was the priority: it auto-loads into future build conversations and was
asserting the false claim as proven guidance.

## Verification

`grep -rn "real ineligible hardware"` across `.planning/spikes`, `.planning/ROADMAP.md` and
the skill (excluding `.claude/worktrees/`) returns only occurrences **inside correction
text**. Spike 004 reads PARTIAL consistently across MANIFEST, WRAP-UP-SUMMARY, SKILL.md and
its own frontmatter.

## Scope

Main worktree only. `.claude/worktrees/*` left untouched — those are other sessions' copies
and carry their own stale versions.

## What this does not change

The **design** is unaffected. Spike 003's INVALIDATED verdict stands independently, so
detection remains impossible and toggle-plus-ordering remains the only available shape. What
changed is the strength of the evidence behind it, and the size of the failure window.

## Follow-on

Four device runs are now open, tracked in the spike and in the skill reference. The two that
decide the merge — capable hardware mid-provisioning, and Apple Intelligence switched off —
have never been tested. Every re-run must record device model, iOS version, whether Apple
Intelligence is enabled, and whether the model download completed; the original run recorded
none of these, which is why its failure could never be attributed.
