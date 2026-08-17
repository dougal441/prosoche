---
phase: 11
slug: build-addendum-01-dante-circle-names-and-the-ten-primitive-r
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-17
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `11-RESEARCH.md` §Validation Architecture (all values measured, not estimated).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | **No test framework.** Eleven bespoke structural checkers in `docs/*.py`, each a standalone `python3` script that raises `AssertionError`/`SystemExit` and prints a one-line pass message |
| **Config file** | none — by design |
| **Quick run command** | `python3 docs/sequence_dispatch_check.py && python3 docs/state_engine_self_check.py` |
| **Full suite command** | `for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check manifest_check; do python3 docs/$f.py \|\| echo "FAIL $f"; done` |
| **Estimated runtime** | ~2 s quick / ~30 s full |

**Baseline measured at `ae0226c`: all eleven exit 0**, and `git status --short` is empty after a full
rebuild (the builders are idempotent). **Any redness during this phase is a regression this phase
caused.**

---

## Sampling Rate

- **After every task commit:** `python3 tools/build_state_engine.py && python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py` (~10 s)
- **After every plan wave:** all eleven checks + both validator invocations
- **Before `/gsd-verify-work`:** all eleven green + both validators + both forks signed + both decrypt-verified + `MANIFEST.md` refreshed + `manifest_check` green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 11-01-T1 | 11-01 | 1 | CIRC-02, DIST-01, DIST-02 | T-11-01, T-11-02 | offset recompute on every token-string edit | tracer | one primitive asserted end to end: `config_literal(actions)["sequences"]` carries the new name ×3 and zero retired entries, then decrypt-verified in both signed artifacts | ❌ W0 — `tools/plist_text_edit.py` | ⬜ pending |
| 11-01-T2 | 11-01 | 1 | ROOM-01 | T-11-01 | attachment-offset invariant armed | structural | `python3 docs/note_identity_check.py` — three title sites plus offset equality across all 775/779 token strings, per fork | ❌ W0 — new twelfth checker | ⬜ pending |
| 11-02-T1 | 11-02 | 2 | CIRC-08, CIRC-06 | T-11-07 | build fails closed on an undispatched entry | build guard | `verify_dispatch_coverage(actions)` observed raising on the live Circle-8 orphan before being armed | ❌ W0 — new `verify_*` | ⬜ pending |
| 11-02-T2 | 11-02 | 2 | CIRC-02, CIRC-06, CIRC-08, AUDIT-02 | T-11-08, T-11-10, T-11-11 | exact-match dispatch, no substring collision | structural | per fork: nine slots, nine distinct components, `Eject` at index 5, `Redirect` absent, `WFCondition` set `== {4}`, `verify_dispatch_coverage` clean | ❌ W0 — folded into the coverage guard; `docs/phase5_self_check.py:65-67` rewritten | ⬜ pending |
| 11-02-T3 | 11-02 | 2 | CIRC-08 | T-11-07 | gate, not report | structural | `python3 docs/sequence_dispatch_check.py` exits non-zero on a synthesised orphan; `KNOWN_ORPHANS` parses as an empty dict | ⚠️ exists, promoted from reporter | ⬜ pending |
| 11-03-T1 | 11-03 | 3 | ROOM-01 | T-11-13, T-11-14 | lookup operator pinned with its rationale | structural | `python3 docs/note_identity_check.py` with `EXPECTED_TITLE` moved; three sites agree per fork; offsets clean | ⚠️ exists (from 11-01), constant re-pointed | ⬜ pending |
| 11-03-T2 | 11-03 | 3 | ROOM-01 | T-11-15, T-11-16 | menu items and case titles share one source | structural | `CIRCLE_NAMES` equals the nine canonical names; Test-a-Circle `WFMenuItems` equals its ordered case titles per fork; hardening section present | ❌ W0 — new `CIRCLE_NAMES` | ⬜ pending |
| 11-03-T3 | 11-03 | 3 | DIST-01, DIST-02 | T-11-18 | deviations recorded append-only | tool | `validate-shortcut src/PROSOCHE-*.xml --target-macos 26 --target-platform all`; decrypt-verify both containers | ✅ | ⬜ pending |
| 11-04-T1 | 11-04 | 4 | AUDIT-02, DIST-02 | T-11-19 | one-way door confirmed by a human | checkpoint | blocking `checkpoint:decision`; never auto-approved | ✅ n/a | ⬜ pending |
| 11-04-T2 | 11-04 | 4 | DIST-02 | T-11-20 | decision recorded with its cost | structural | `git diff --numstat -- docs/CAPABILITY-DECISIONS.md` shows deletion count `0`; record names the option, `fix_state_rebind` and `DIST-03` | ✅ | ⬜ pending |
| 11-05-T1 | 11-05 | 5 | AUDIT-02, CIRC-06 | T-11-22, T-11-23, T-11-24, T-11-25 | Emergency Restore never gated; numeric flat gate | structural | per fork: exactly one Leaving/Continue menu, Emergency Restore present, `panic_escape_enabled` seeded flat, every Panic-Escape conditional `WFCondition == 2`; both site-count tables at measured values | ❌ W0 — new state key and gate | ⬜ pending |
| 11-05-T2 | 11-05 | 5 | AUDIT-02 | T-11-26, T-11-27, T-11-28 | removal needs two deliberate acts and is reversible | structural | every `choosefrommenu` group's `WFMenuItems` equals its ordered case titles per fork; `docs/phase7_self_check.py` `MENU` updated; `docs/router_ui_census.py` clean | ⚠️ exists, `MENU` list needs update | ⬜ pending |
| 11-05-T3 | 11-05 | 5 | DIST-01 | T-11-23 | site-count deltas explained, not transcribed | tool | both validators; decrypt-verify carries `panic_escape_enabled` and an undiminished Emergency Restore surface | ✅ | ⬜ pending |
| 11-06-T1 | 11-06 | 6 | ROOM-02, DIST-02 | T-11-29, T-11-30, T-11-31 | filename is the sole carrier of the display name | structural | both root `WFWorkflowName` values and `DISPLAY_NAMES` carry the two new names; the Note names Core in both automation steps | ⚠️ exists, `docs/manifest_check.py` and `docs/sentient_core_check.py:9` need update | ⬜ pending |
| 11-06-T2 | 11-06 | 6 | ROOM-02 | T-11-32, T-11-33 | additivity proved through a fork-normalised equality | structural | `python3 docs/sentient_core_check.py`; Aware note names Aware ×2 and Core ×0; `fix_fork_strings` proven to fail on a count mismatch | ❌ W0 — new `fix_fork_strings` | ⬜ pending |
| 11-06-T3 | 11-06 | 6 | DIST-01, DIST-02 | T-11-29, T-11-34, T-11-35 | shipped payload asserted, not inferred | structural | `python3 docs/manifest_check.py` against six relabelled rows; both containers decrypt and carry `Loud Mirror`, `PANIC ESCAPE`, `THE NINE CIRCLES` | ⚠️ exists, `DISPLAY_NAMES` + six row labels updated | ⬜ pending |
| (all) | all | 1–6 | cross-cutting | — | builder idempotence | structural | `docs/phase5_self_check.py` / `phase6_self_check.py` — each runs the builder twice and compares digests; `git status --short` clean after a second run | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Task IDs are assigned by the planner; the rows above fix the requirement→command mapping the plans must satisfy.*

---

## Wave 0 Requirements

- [ ] `verify_dispatch_coverage(actions)` in `tools/build_state_engine.py`, called from `main()` and from `build_sentient.py`'s verify chain — covers CIRC-08 and CIRC-06
- [ ] Promote `docs/sequence_dispatch_check.py` to a hard gate: empty `KNOWN_ORPHANS`, non-zero exit on orphan/unreachable/unknown, rewrite the docstring (which currently states it is deliberately not a gate)
- [ ] Rewrite `docs/phase5_self_check.py:66-68`'s name list; add negative assertions for the six retired names
- [ ] Update `docs/manifest_check.py:DISPLAY_NAMES` and `docs/sentient_core_check.py:9` for the Core/Aware rename
- [ ] Update `docs/environmental_restore_check.py:78` and `docs/phase9_self_check.py:97-104` **only if** the Panic Escape mechanism adds an eleventh `primitive_dispatch()` rendering
- [ ] A note-identity check (three title sites + attachment-offset equality in both forks)
- [ ] Update `docs/phase7_self_check.py:15`'s `MENU` list **only if** a Panic Escape menu item is added

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The renamed Note title renders as `PROSOCHĒ` in Apple Notes and the Find-Notes predicate still resolves it | ROOM-01 | Notes filter `Operator` semantics for `WFContentPredicateTableTemplate` are UNVERIFIED in the bundled catalog (research flagged LOW confidence) — only a device run settles whether an exact-match operator is valid there | Import the signed fork on an iOS 26.x iPhone, run manually, confirm the Control Room Note is found and not duplicated |
| Panic Escape removal path (edit setting in Note + explicit confirmation) actually suppresses the `Leaving` option | AUDIT-02 | Behavioural, requires a live OPEN with the setting toggled | Toggle the setting in the Note, trigger an OPEN, confirm `Leaving` is absent and Emergency Restore is still offered |
| Every renamed Circle dispatches its intended primitive on device | CIRC-02, CIRC-06, CIRC-08 | Red operators and blank text are device-visible only (`.claude/CLAUDE.md` — operator/operand validity is invisible in the plist) | Deferred to Phase 19's nine-Circle sweep; **blocked on DIST-03 (no connected iPhone)** |

**Standing blocker:** DIST-03 — no iPhone is connected. Every manual row above is blocked. This phase's
gate is therefore structural-only, and the phase must say so rather than infer device behaviour.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
