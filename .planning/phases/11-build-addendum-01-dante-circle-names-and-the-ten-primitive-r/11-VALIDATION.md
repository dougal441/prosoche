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
| 11-XX-XX | TBD | 0 | CIRC-08 | — | N/A | structural | `python3 docs/sequence_dispatch_check.py` exits non-zero on any orphan/unreachable/unknown | ❌ W0 — promote reporter to gate | ⬜ pending |
| 11-XX-XX | TBD | 0 | CIRC-08, CIRC-06 | — | N/A | build guard | `python3 tools/build_state_engine.py` fails via `verify_dispatch_coverage` | ❌ W0 — new `verify_*` | ⬜ pending |
| 11-XX-XX | TBD | 1 | CIRC-02, AUDIT-02 | — | N/A | structural | `python3 docs/phase5_self_check.py` — new names asserted present, six retired names asserted absent | ⚠️ exists, needs rewrite (`docs/phase5_self_check.py:66-68`) | ⬜ pending |
| 11-XX-XX | TBD | 1 | CIRC-06 | — | N/A | structural | assertion over `config_literal(actions)["sequences"]`: `Eject` at Circle 6 in all three, `Redirect` in none | ❌ W0 — folded into coverage guard | ⬜ pending |
| 11-XX-XX | TBD | 2 | ROOM-01, ROOM-02 | — | N/A | structural | `python3 docs/note_identity_check.py` — three title sites, no user-facing `— Control Room`, attachment offsets equal recomputed `￼` offsets in **both** forks | ❌ W0 | ⬜ pending |
| 11-XX-XX | TBD | 2 | ROOM-02 | — | N/A | structural | string assertion on the decrypted body of both signed artifacts (model on `260817-au7`) | ❌ W0 | ⬜ pending |
| 11-XX-XX | TBD | 3 | DIST-01 | — | N/A | tool | `validate-shortcut src/PROSOCHE-*.xml --target-macos 26 --target-platform all` | ✅ | ⬜ pending |
| 11-XX-XX | TBD | 3 | DIST-02 | — | N/A | structural | `python3 docs/manifest_check.py` (DISPLAY_NAMES updated for Core/Aware) | ⚠️ exists, needs update | ⬜ pending |
| 11-XX-XX | TBD | all | cross-cutting | — | N/A | structural | `docs/phase5_self_check.py` / `phase6_self_check.py` — each runs the builder twice and compares digests (idempotence) | ✅ | ⬜ pending |

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
