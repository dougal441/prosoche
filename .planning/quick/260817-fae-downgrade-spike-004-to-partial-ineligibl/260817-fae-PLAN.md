---
quick_id: 260817-fae
description: Downgrade spike 004 to PARTIAL — the ineligible-hardware leg was never tested
date: 2026-08-17
status: planned
---

# Quick Task 260817-fae: Downgrade Spike 004 to PARTIAL

## Why

Device report from the user, 2026-08-17: their **iPhone 16e** — the device spike 004
recorded as *"iPhone SE (not Apple-Intelligence-capable)"* — has now downloaded the Apple
Intelligence models and **successfully ran the Sentient result** from the Capability Gate
shortcut.

The iPhone 16e is A18 / 8 GB and **is** Apple-Intelligence-capable. So the leg spike 004
recorded as its ineligible-hardware test was never a test of ineligible hardware at all.
The observed error — *"Support for selected model is downloading"* — was the transient
provisioning state that spike 004's own **"Not fully verified"** caveat explicitly
anticipated and then declined to chase, on the grounds that the ordering fail-safe was
proven "regardless of which case it is." That reasoning does not survive: with the device
eligible, the fail-safe has never met a hardware-ineligibility failure.

## What changes

**Verdict: VALIDATED → PARTIAL.**

Survives:
- The toggle gates the Sentient branch correctly in both directions (iPhone 15 Pro, both answers).
- A real `Use Model` failure was observed **not** to pre-empt the core escalation — the core
  alert had already fired. That observation stands; only its attributed cause was wrong.
- The Save File one-time permission prompt finding is untouched.
- Spike 003's INVALIDATED verdict is untouched and independent — detection is impossible
  either way, so the *design* (toggle + ordering) does not change.

Does not survive:
- "the ordering-based fail-safe works as designed on real ineligible hardware, not just in
  theory" — unsupported. No genuinely ineligible device has ever run this shortcut.
- The claim that `Use Model` fails *gracefully* on ineligible hardware. A transient
  provisioning failure and a hard eligibility failure are not established to behave alike.

New open question: retest on a device with no on-device LLM. Genuinely ineligible hardware
is iPhone 15 / 15 Plus (A16, 6 GB), iPhone 14 or earlier, or a real iPhone SE 2nd/3rd gen.

## Tasks

### Task 1 — correct spike 004 and everything citing it

**Files:**
- `.planning/spikes/004-capability-gate/README.md` — frontmatter `verdict`, the device-leg
  section, "What this confirms", and a dated correction note
- `.planning/spikes/MANIFEST.md` — requirements bullet (~line 69) and the 004 spike-table row
- `.planning/ROADMAP.md` — ~line 931, "Spike 004 (VALIDATED, on real hardware)"
- `.planning/spikes/CONVENTIONS.md` — the no-try/catch bullet citing "real ineligible hardware"
- `.planning/spikes/WRAP-UP-SUMMARY.md` — verdict table and key findings
- `.claude/skills/spike-findings-prosoche/SKILL.md` — feature-area row, processed-spikes list
- `.claude/skills/spike-findings-prosoche/references/sentient-and-capability-gating.md` —
  Step 2 ordering evidence and Constraints
- `.claude/skills/spike-findings-prosoche/sources/004-capability-gate/README.md` — mirror

**Action:** Rewrite each citation so it states what was actually observed and attributes it
correctly. Do not delete the original observation — record the misattribution, because the
lesson (a spike's own caveat was right and the verdict overrode it) is the durable part.

**Verify:** No file outside `.claude/worktrees/` asserts the fail-safe was tested on
ineligible hardware. `grep -rn "ineligible hardware"` returns only correctly-qualified uses.

**Done:** Spike 004 reads PARTIAL everywhere, with the retest named as an open question.

**Scope guard:** main worktree only. Leave `.claude/worktrees/*` untouched — those are other
sessions' working copies.
