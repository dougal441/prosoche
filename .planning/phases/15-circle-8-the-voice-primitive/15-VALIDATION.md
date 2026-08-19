---
phase: 15
slug: circle-8-the-voice-primitive
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-18
---

# Phase 15 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `15-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Build guards + standalone checker scripts. No pytest/unittest exists and none should be added — the invariants are properties of a generated plist, and every guard already runs inside the build. |
| **Config file** | none — each `docs/*_check.py` is an executable script with a `main()` and `require()`/`SystemExit` assertions |
| **Quick run command** | `python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py && python3 docs/state_engine_self_check.py` |
| **Full suite command** | `for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check note_identity_check manifest_check; do python3 docs/$f.py \|\| echo "FAIL $f"; done` |
| **Build-time guards** | 20+ `verify_*()` in `tools/build_state_engine.py`, re-run by `tools/build_sentient.py` — these fail the *build*, not a test run |
| **Estimated runtime** | quick < 5s; full suite ~30s plus two fork rebuilds |

---

## Sampling Rate

- **After every task commit:** `python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py` (< 5s; catches the dispatch-surface class, this phase's core risk)
- **After every plan wave:** rebuild both forks, then the twelve-checker full suite, then gate A on both forks
- **Before `/gsd-verify-work`:** full suite green + gate A clean on both forks + both forks signed + a new `MANIFEST.md` block with `docs/manifest_check.py` green
- **Max feedback latency:** 5 seconds (quick), ~120 seconds (wave)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | 0 | CIRC-08 | — | Exactly one `speaktext` per Voice branch, none in the Mirror branch (11 total, down from 22) | structural guard | new `verify_*()` in `tools/build_state_engine.py` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0 | CIRC-08 | — | Every `speaktext` site enclosed by both the `Voice Enabled > 0` group and the `Spoken This Run` condition-101 group | structural guard | new `verify_*()` reusing `enclosing_groups()`/`gate_groups()` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0 | CIRC-08 | — | `voice_enabled` seeded numeric; every reader uses `WFCondition 2 / WFNumberValue 0` | structural guard | new `verify_*()` sibling to `verify_state_seed()` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0 | CIRC-08 / SAFE-02 | T-15-01 | "never at unsafe levels" — zero `setvolume` reachable inside any `Loud Mirror` branch span | structural guard | new `verify_*()` | ❌ W0 | ⬜ pending |
| TBD | TBD | 0 | CIRC-14 | — | No two distinct sequence-entry names resolve to action-equal branch bodies | structural | assertion in `docs/sequence_dispatch_check.py` (or sibling) | ❌ W0 | ⬜ pending |
| TBD | TBD | 1+ | CIRC-14 | — | Circle 7 and Circle 8 dispatch different implementations | structural | `python3 docs/sequence_dispatch_check.py` | ⚠️ partial | ⬜ pending |
| TBD | TBD | 1+ | CIRC-14 | — | Nine shipped names and three sequences unchanged | structural | `python3 docs/phase5_self_check.py` | ✅ | ⬜ pending |
| TBD | TBD | 1+ | CIRC-08 | — | `speaktext.WFText` carries the `WFTextTokenString` envelope | structural | `verify_string_envelopes()` (build guard) | ✅ | ⬜ pending |
| TBD | TBD | 1+ | CIRC-09 | — | Circle 9 still dispatches `Frozen` in all three sequences, unchanged | structural | `python3 docs/phase5_self_check.py && python3 docs/sequence_dispatch_check.py` | ✅ | ⬜ pending |
| TBD | TBD | 1+ | DIST-01 | — | Gate A passes clean on both forks | structural | `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` (and Sentient) | ✅ | ⬜ pending |
| TBD | TBD | last | — | — | Shipped payload matches sources | structural | `python3 docs/manifest_check.py` (decrypt + assert), `Loud Mirror` counts re-derived | ⚠️ counts move | ⬜ pending |
| TBD | TBD | 1+ | — | — | No surface entered the Circle-0 silent band | structural | `verify_circle_zero_silence()` + `python3 docs/router_ui_census.py` | ✅ | ⬜ pending |
| TBD | TBD | 1+ | — | — | ≥30 distinct Mirror templates survive the split | structural | `python3 docs/phase7_self_check.py` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Guard: `speaktext` appears **only** inside `Loud Mirror` branches, exactly once per rendering (11 total) — covers CIRC-08 and CIRC-14 simultaneously
- [ ] Guard: every `speaktext` site is enclosed by both the `Voice Enabled > 0` group and the `Spoken This Run` condition-101 group — covers CIRC-08's two clauses
- [ ] Guard: `voice_enabled` is seeded as a number, and every conditional reading it uses `WFCondition 2 / WFNumberValue 0` — covers RESEARCH Pitfall 2
- [ ] Guard: zero `setvolume` reachable inside a `Loud Mirror` branch span — covers "never at unsafe levels" / SAFE-02
- [ ] Assertion in `docs/sequence_dispatch_check.py` (or a sibling) that no two distinct sequence-entry names resolve to action-equal branch bodies — the general form of the CIRC-14 defect
- [ ] The rung-2 discriminator probe for RESEARCH Open Question 2 (`list` / `getitemfromlist` / `speaktext` unfilled picker), with its result recorded in `docs/BUILD-NOTES.md`

All five new guards belong in `tools/build_state_engine.py` beside the existing `verify_*()` family and must be armed in `tools/build_sentient.py`'s import list, matching the established pattern. **Each must be demonstrated to fail on a synthesised defect** — the project's own standard (`verify_panic_escape_isolation()`, plan 11-10) is that a guard proven only in the passing direction is not proven.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Circle 8 actually speaks on a phone | CIRC-08 | Personal Automations and audio output cannot be exercised by the validator, and the simulator lacks the surface | `Test a Circle → Circle 8 · Fraud` via iPhone Mirroring; confirm the alert renders AND the same text is spoken exactly once |
| Circle 7 no longer speaks | CIRC-14 | Same — audible behaviour | `Test a Circle → Circle 7 · Violence` with `voice_enabled = 1`; confirm alert renders and nothing is spoken |
| Circle 8 with `voice_enabled = 0` degrades to a Mirror-equivalent alert (D-15-A) | CIRC-08, CIRC-14 | Requires toggling a user setting on device | Toggle Voice off in the Control Room, then `Test a Circle → Circle 8 · Fraud`; confirm an alert renders and nothing is spoken |
| Axis-4 unfilled-picker discrimination | CIRC-08 | Rung-2 simulator probe (alert-free) | Per `15-RESEARCH.md` § Code Examples, "The alert-free rung-2 discriminator probe" |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s (quick) / < 120s (wave)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
