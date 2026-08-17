---
phase: 13
slug: red-operator-conditionals-and-the-wfitems-list-wrapper
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-17
---

# Phase 13 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Sourced from `13-RESEARCH.md` § Validation Architecture (measured this session, not inferred).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None conventional — this project uses **executable structural checkers** (`docs/*.py`) plus **in-generator guards** (`verify_*`, raised as `SystemExit` before any write) |
| **Config file** | none — each checker is a standalone script exiting 0/1 |
| **Quick run command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` (runs 21 + 17 guards inline) |
| **Full suite command** | build both forks + all 12 `docs/*.py` checkers + validator gate A on both source XMLs |
| **Estimated runtime** | ~60 seconds |

**Gate A (mandatory, must pass clean):**

```
validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all
validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all
```

**Gate B (advisory, never blocking):** `--target-macos 27 --target-platform all`, expect exit 1
with exactly one waived `com.apple.mobilenotes.SharingExtension` line per fork. Anything else is
a real finding.

**Build provenance precondition:** `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD`
must exit 0 before either generator runs.

---

## Sampling Rate

- **After every task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py`
- **After every plan wave:** full 12-checker sweep + gate A on both forks.
  **One deliberate exception:** `docs/manifest_check.py` is expected RED in waves 1–3, because
  rebuilding the forks stales the MANIFEST and the artifacts are only re-signed in 13-04. This is
  stated as constraint D-04 in every affected plan objective. Do **not** close it by editing
  MANIFEST rows without re-signing — 13-04 closes it properly. All other 11 checkers must stay
  green in every wave.
- **Before `/gsd-verify-work`:** full suite green, gate B showing exactly one waived line per
  fork, signed artifacts regenerated under the canonical display names, MANIFEST refreshed
- **Max feedback latency:** ~60 seconds

---

## Per-Task Verification Map

> Refreshed 2026-08-17 against the four final plans. Plan/wave/requirement columns now match the
> plans' own frontmatter: 13-01 wave 1 (CIRC-07, CIRC-04, ROOM-03, DIST-01) · 13-02 wave 2
> (CIRC-07, DIST-01) · 13-03 wave 3 (CIRC-07, CIRC-04, ROOM-03) · 13-04 wave 4 (DIST-01, DIST-02,
> CIRC-04, ROOM-03). CIRC-04 and ROOM-03 carry **regression-protection** duty in this phase, not
> new implementation work — neither has a defect site in either family.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 13-01-01 | 01 | 1 | CIRC-07 | T-13-* | Guard raises `SystemExit` with an actionable message before any write (V7) | structural guard | `python3 tools/build_state_engine.py` (new `verify_list_item_wrappers`) | ❌ W0 | ⬜ pending |
| 13-01-02 | 01 | 1 | CIRC-07 | T-13-* | Revert/restore leaves a byte-identical digest (V12) | sensitivity demo | direct-call + full-build revert on both generators, `git checkout --` restore | ❌ W0 | ⬜ pending |
| 13-01-* | 01 | 1 | CIRC-04, ROOM-03 (regression) | — | N/A | checker | `python3 docs/phase5_self_check.py`; `python3 docs/note_identity_check.py` | ✅ | ⬜ pending |
| 13-01-* | 01 | 1 | DIST-01 | — | N/A | validator | gate A on both source XMLs | ✅ | ⬜ pending |
| 13-02-01 | 02 | 2 | CIRC-07 | T-13-08 | N/A | source assertion | AST byte-equality of `token()` / `if_block()` bodies vs the phase-start blob | ✅ | ⬜ pending |
| 13-02-02 | 02 | 2 | CIRC-07, DIST-01 | — | Both raises reachable; ordering mask demonstrated, not assumed (V7) | structural guard | extended `verify_conditional_action_string` (positive Donor-5 pin) | ❌ W0 | ⬜ pending |
| 13-03-* | 03 | 3 | CIRC-07, CIRC-04, ROOM-03 | T-13-15 | N/A | source assertion | refuted counts absent from the whole of ROADMAP.md and HANDOFF.md; axis list updated | ✅ | ⬜ pending |
| 13-04-01 | 04 | 4 | DIST-01, DIST-02 | — | Canonical signed basenames, no `_signed` suffix (V12) | checker | `python3 docs/manifest_check.py` + AEA1 decrypt-verify of 660 wrapped rows | ✅ | ⬜ pending |
| 13-04-02 | 04 | 4 | CIRC-04, ROOM-03 | — | N/A | human-check + UAT | `13-UAT.md`, cold-runnable, explicit BLOCKED branch under DIST-03 | ❌ W0 | ⬜ pending |
| 13-0*-* | * | 1–4 | — (regression) | — | N/A | checker | `python3 docs/phase6_self_check.py` (byte-idempotent rebuild) | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `verify_list_item_wrappers()` in `tools/build_state_engine.py` — covers CIRC-07
- [ ] Register it in the Dumb guard harness at `tools/build_state_engine.py:4160-4177`
- [ ] Add it to `tools/build_sentient.py`'s import list **and** its guard block (two touch
      points — Phase 12 hit exactly this trap)
- [ ] Extend `verify_conditional_action_string()` with the positive Donor-5 assertion that
      *pins* the device-confirmed shape (guards the correct shape against a future "fix")
- [ ] Sensitivity demonstration for both guards against a synthetically reverted artifact — a
      guard that cannot fail proves nothing

*No new test framework is needed — the project's guard/checker mechanism covers everything.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Mirror List rows render non-empty text on device | CIRC-07 | §9 rung 2 ceiling — the simulator lacks `com.apple.mobilenotes` and cannot exercise the Control Room path; row rendering is a device-visible property no file-level analysis can confirm | Import the signed Core fork on a real iPhone, drive the Mirror primitive, confirm every List row shows text rather than an empty placeholder. Fold into Phase 19 device UAT. |
| `getitemfromlist` return value over a wrapped List | CIRC-07 | No donor chains a wrapped List into `getitemfromlist`; open question recorded in RESEARCH.md | Assert "Mirror renders non-empty text" in Phase 19 UAT and observe the selected row is the intended one. |

---

## Measured Baseline (HEAD, before the phase starts — all green)

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebbf… HEAD` | exit 0 — provenance OK |
| 12 × `docs/*.py` | all PASS |
| Gate A, Dumb | `Validation passed.` |
| Gate A, Sentient | `Validation passed.` |
| Gate B, Dumb | exactly 1 waived line |
| Gate B, Sentient | exactly 1 waived line |
| Wrapped-row prototype (660 rows), gate A | `Validation passed.` |

Everything is green *before* the phase starts, so any red during execution is caused by the phase.

---

## Validation Sign-Off

- [ ] All tasks have an automated verify or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] Both new guards demonstrated sensitive against a synthetically reverted artifact
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
