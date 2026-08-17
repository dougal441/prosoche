---
phase: 12
slug: state-shape-sentinel-gaps-exit-events-and-active-session
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-17
---

# Phase 12 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source: `12-RESEARCH.md` §Validation Architecture (measured against the live tree, not inferred).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | **None** — 12 standalone scripts in `docs/`, using bare `assert` or a local `require()` helper. No `pytest.ini`, no `setup.cfg`, no `pyproject.toml`, no `tests/`, and zero `import pytest` / `import unittest` anywhere in `tools/` or `docs/`. The checker-script convention *is* the framework. |
| **Config file** | none — see Wave 0 |
| **Quick run command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 docs/state_engine_self_check.py && python3 docs/phase6_self_check.py` |
| **Full suite command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check note_identity_check manifest_check; do python3 docs/$f.py \|\| exit 1; done && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` |
| **Estimated runtime** | ~30–60 seconds (`phase6_self_check.py` invokes the builder twice to prove idempotency) |

**Build provenance gate (mandatory before any builder run):**
`git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` — abort the rebuild if it fails.

---

## Sampling Rate

- **After every task commit:** Run the **quick run command** above
- **After every plan wave:** Run the **full suite command** (12 checkers + gate A on both forks)
- **Before `/gsd-verify-work`:** Full suite green, gate A clean ×2, gate B showing **exactly** the one waived line ×2, both forks signed under the Core/Aware display names, `docs/manifest_check.py` green
- **Max feedback latency:** ~60 seconds

---

## Per-Task Verification Map

| Req | Behavior | Test Type | Automated Command | File Exists | Status |
|-----|----------|-----------|-------------------|-------------|--------|
| STATE-12 | `exit_events` (and `exit_selection_counter`) declared in the versioned bootstrap document | unit (build guard) | `python3 tools/build_state_engine.py` — new `verify_exit_events_seed()` raises on failure | ❌ W0 | ⬜ pending |
| STATE-12 | schema bumped 3→4 across all three coupled literals | unit | `python3 -c "import sys;sys.path.insert(0,'tools');import build_state_engine as B;assert B.SCHEMA_VERSION=='4' and B.SCHEMA_VERSION_PREVIOUS=='3' and B.SCHEMA_VERSION in B.SCHEMA_VERSION_ACCEPTED;print('ok')"` | ❌ W0 | ⬜ pending |
| SESS-07 | `active_session` is a permanent multi-leaf container; every read leaf resolves in the seed | unit (build guard) | `python3 tools/build_state_engine.py` — new `verify_active_session_seed()` raises on failure | ❌ W0 | ⬜ pending |
| SESS-07 / SAFE-01 | zero condition-100 gates and zero dotted reads over a sentinel-written key, with an **empty** exemption set | unit (build guard) | `python3 -c "import sys;sys.path.insert(0,'tools');import build_state_engine as B;assert B.KNOWN_SENTINEL_EXISTENCE_GATES==();print('ok')" && python3 tools/build_state_engine.py` | ✅ `verify_sentinel_gates()` exists; only the constant changes | ⬜ pending |
| SAFE-01 | brightness/volume writes remain numerically gated | unit (build guard) | `python3 tools/build_state_engine.py` (`verify_restore_gates()`) + `python3 docs/environmental_restore_check.py` + `python3 docs/phase9_self_check.py` | ✅ | ⬜ pending |
| EXIT-01 / EXIT-02 | the six exit routes and their state keys survive the refactor | unit | `python3 docs/phase6_self_check.py` | ✅ | ⬜ pending |
| All | every literal state read resolves in the bootstrap seed (**class-level guard**) | unit (build guard) | `python3 tools/build_state_engine.py` — generalised `verify_state_seed()` (delete the `settings_snapshot` filter) | ❌ W0 | ⬜ pending |
| All | builders are byte-idempotent | integration | `python3 docs/phase6_self_check.py` | ✅ | ⬜ pending |
| All | both forks structurally valid at the real target | integration | gate A ×2 (`--target-macos 26 --target-platform all`) | ✅ | ⬜ pending |
| SESS-07 / EXIT-* | a real "leave and confirm exit" against clean state completes and restores settings | manual (device, rung 3/4) | **none possible — no automated substitute exists** | ❌ `12-UAT.md` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `verify_exit_events_seed()` in `tools/build_state_engine.py` — covers STATE-12
- [ ] `verify_active_session_seed()` in `tools/build_state_engine.py` — covers SESS-07
- [ ] Generalised `verify_state_seed()` read-side scan (delete the `settings_snapshot` filter) — covers the whole class
- [ ] `docs/state_engine_self_check.py:92` literal updated `"active_session"` → `"active_session.id"` — **required, or the suite goes red with a bare `AssertionError`**
- [ ] Both new verifiers imported and armed in `tools/build_sentient.py` (its verifier set is currently a subset that does not even assert the `pending_exit` seed)
- [ ] `12-UAT.md` for the device exit-path test, with an explicit **blocked** branch (Phase 10 precedent: leave UAT blank rather than substitute a simulator run)
- Framework install: **none required**

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| A real "leave and confirm exit" against a clean `state.json` completes without a key-path error and restores brightness/volume | SESS-07, EXIT-01, EXIT-02, SAFE-01 | Personal Automation triggers cannot be exercised on a simulator, and the exit path was never exercised by the closed OPEN-path debug session (`.claude/CLAUDE.md` §9, "Rung 2's ceiling") | Fresh-install both forks; delete `state.json`; open a target app to start a session; leave and confirm an exit; confirm no "could not evaluate the key path" error and that brightness/volume return to captured values |
| The Control Room Note path survives the refactor | EXIT-01, EXIT-02 | `com.apple.mobilenotes` is absent from the booted simulator's app list — device-gated by measurement | Open Control Room after the exit; confirm the ledger entry appended and the Note renders |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
