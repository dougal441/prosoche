---
phase: 9
slug: reintroduce-and-validate-dimming-silence-stateful-restore-on
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-16
---

# Phase 9 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Custom Python static self-checks (no third-party test framework) — `tools/build_state_engine.py`'s own build-guard assertions |
| **Config file** | none — each check is a standalone function invoked as part of the generator run |
| **Quick run command** | `python3 tools/build_state_engine.py` |
| **Full suite command** | `python3 tools/build_state_engine.py && python3 docs/state_engine_self_check.py && python3 docs/phase5_self_check.py && python3 .claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/scripts/validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && python3 .claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/skills/shortcuts-playground/scripts/validate_shortcut.py src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` |
| **Estimated runtime** | ~10-30 seconds (static checks only; device trials are manual, unbounded) |

---

## Sampling Rate

- **After every task commit (Plan A only):** `python3 tools/build_state_engine.py` — fast, catches the coercion regression immediately
- **After every plan wave:** Full suite command above, both forks
- **Before `/gsd-verify-work`:** Full static suite green AND every Plan B device checkpoint resolved (pass or documented fail)
- **Max feedback latency:** ~30s for the automated half; device checkpoints are inherently unbounded (human/device dependent) — see Manual-Only Verifications below

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 09-01-* | 01 (generator fix) | 1 | Criterion 1 | Fabricated-coercion-shape / Tampering | `verify_numeric_operands()` hard-fails if either new table entry's site resolves to a non-numeric source | static/build-guard | `python3 tools/build_state_engine.py` | ✅ (existing guard, needs 2 table entries) | ⬜ pending |
| 09-02-* | 02 (device proof) | 2 | Criteria 2-7 | Device-left-unrestorable / DoS-of-usability | Emergency Restore reachable and effective under every trialed failure mode | manual/checkpoint:human-verify | none — no simulator or headless Shortcuts runtime exists | ❌ W0 (needs `09-UAT.md`) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md` — device-proving test list for criteria 2-7, following the exact structure already used in `04-UAT.md`/`05-UAT.md`/`07-UAT.md` (Current Test / Context / Tests / Summary sections)
- [ ] A negative-control check that `verify_numeric_operands()` actually fails when the two new `NUMERIC_OPERAND_FIELDS` entries are removed (proves the guard is load-bearing, not accidentally-passing)
- [ ] Documentation correction task confirming `.planning/debug/HANDOFF.md` §8 and `.planning/ROADMAP.md` criterion 1 both read 28 sites, not 18 (already corrected pre-planning on 2026-08-16 — this task verifies no other doc still says "18")

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|--------------------|
| Coercion chip does not render red in Shortcuts.app's editor | Criterion 1 (shape correctness) | The coercion shape is invisible to the validator, the ToolKit catalog, and a decrypted signed artifact — only the on-device UI reveals whether it's correct (RESEARCH.md Pitfall 1) | Import the rebuilt shortcut on a real iPhone, open a Dimming/Silence/Restore action in the editor, visually confirm the `WFBrightness`/`WFVolume` parameter chip is not red |
| Device read of brightness/volume returns real, correctly-typed value | Criterion 2 | Requires live `Get Device Details` execution on hardware | Trigger OPEN on the real device, inspect resulting `state.json`/Control Room state for a populated `settings_snapshot` |
| Original value restored exactly on CLOSE | Criterion 3 | Requires live CLOSE trigger and before/after brightness+volume comparison on hardware | Note pre-session brightness/volume, trigger OPEN then CLOSE, confirm both values match exactly |
| Force-quit / device-restart / missed-CLOSE / overlapping-session recovery | Criterion 4 | Cannot be simulated — Shortcuts has no headless runtime | Execute each of the 4 independent trials plus 1 compound trial (overlap + force-quit of the winning session) per RESEARCH.md Pitfall 4; observe screen state after each |
| Emergency Restore recovers from every failure mode found | Criterion 5 | Same as above | After each failure-mode trial, invoke Emergency Restore and confirm brightness/volume return to the original captured value |
| Device's true `WFBrightness` minimum is dim, not black | Criterion 4 addendum (BD-02) | No documented minimum exists in any bundled catalog; must be observed | Set `WFBrightness = 0.0` via a test action on-device, visually confirm the result matches the user's prior report before adopting it as the new dim target |
| DEV-06 design verdict | Criterion 6 | A first-principles design decision informed by, but not fully resolved by, static code trace (RESEARCH.md's DEV-06 section) | Write out the full capture/restore state machine under overlap before deciding whether/how to implement; if implemented, verify against the overlapping-session device trial above |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies — Plan A yes; Plan B tasks are `checkpoint:human-verify` by nature, tracked via `09-UAT.md` per project convention, not a gap
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify — Plan A's static guard covers every task; Plan B is entirely manual by necessity and is scoped as its own wave
- [ ] Wave 0 covers all MISSING references — see Wave 0 Requirements above
- [ ] No watch-mode flags — n/a, no test framework with watch mode in use
- [ ] Feedback latency < 30s (automated half) — met; manual half is inherently unbounded and out of scope for this bound
- [ ] `nyquist_compliant: true` set in frontmatter — not yet; set once `09-UAT.md` exists and the negative-control check is added (Wave 0 items above)

**Approval:** pending
