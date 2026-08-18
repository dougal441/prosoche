---
phase: 16
slug: dimming-and-silence-as-distinct-device-proven-circles
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-17
---

# Phase 16 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `16-RESEARCH.md` § Validation Architecture, with the SAFE-01 row amended
> for the user's locked D-01 decision (floor and target both 0).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Custom Python static self-checks — no third-party test framework |
| **Config file** | none; each check is a standalone script |
| **Quick run command** | `python3 tools/build_state_engine.py` (build guards are hard `SystemExit`s) |
| **Full suite command** | see below |
| **Estimated runtime** | ~25 seconds |

Full suite:

```bash
python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 docs/state_engine_self_check.py && python3 docs/phase9_self_check.py && python3 docs/environmental_restore_check.py && python3 docs/retired_clause_check.py && python3 docs/manifest_check.py && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all
```

**Two members of this chain are deliberately not green for part of the phase. Both are expected,
and neither is a number to adjust.**

- `docs/retired_clause_check.py` — **✅ LANDED 2026-08-18 (plan 16-05, wave 4). From wave 5 onward
  run the chain as written and expect this term GREEN; do not drop it.** The paragraph below is
  retained because it remains the correct instruction for anyone replaying waves 1–3.
  It **did not exist until plan 16-05 created it** (wave 4). Before
  that wave the command fails at that link with a missing-file error; drop that one term when
  running the suite mid-phase. It is listed here from now because from wave 4 onward it gates
  the retired-clause class on every future run — a checker that ran only in the plan that wrote
  it is a sweep, not a gate. It carries two invariants: no live file still asserts the retired
  brightness-floor clause, and `src/CONFIG-BLOCK.md`'s fenced Config JSON agrees with both built
  forks' Config literal on `brightness_floor` and `dim_target`. It also states, in its own source,
  that it **cannot** see non-lexical encodings — `docs/phase5_self_check.py:117` was one — so a
  green result is never proof the class is empty.
- `docs/manifest_check.py` is **deliberately RED** from plan 16-01's first rebuild until plan
  16-06 re-signs and refreshes the rows (constraint D-MANIFEST). Do not fix it by editing MANIFEST
  rows without re-signing.

**Gate B is advisory and must never be chained into a definition of done.** Run
`validate-shortcut <fork> --target-macos 27 --target-platform all` separately; expect exit 1
with exactly the one waived `WFCreateNoteInput` line per fork. Anything else is a real finding.

**Baseline measured 2026-08-17, post-Phase-13-merge, before any Phase 16 change:**
`environmental restore check: passed`, `phase9 self-check: passed` (30/30 sites, 19 coerced),
`manifest check: passed` (6 rows), gate A `Validation passed.` both forks, gate B one waived
line per fork.

---

## Sampling Rate

- **After every task commit:** `python3 tools/build_state_engine.py` — the build guards fire immediately.
- **After every plan wave:** the full suite above, both forks, plus `manifest_check.py` if artifacts moved.
- **Before `/gsd-verify-work`:** full static suite green.
- **Max feedback latency:** ~25 seconds.

**Phase gate:** full static suite green, rung-2 findings recorded, the device instrument
authored and SHA-pinned, DEV-06 and BD-02 resolved per the locked decisions — and every device
test recorded **BLOCKED with a real reason**, never inferred.

---

## Per-Task Verification Map

Task IDs are assigned by the planner; this map binds requirements to their verification
mechanism so the planner can attach the right `<automated>` verify to each task.

| Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|
| CIRC-03, CIRC-05, SAFE-03 | a captured original is **persisted** before the device is changed | static / build guard | new guard in `tools/build_state_engine.py`, run by the generator | ❌ W0 | ⬜ pending |
| CIRC-03, CIRC-05, SAFE-03 | the persistence guard is load-bearing | static negative control | new function in `docs/phase9_self_check.py`, mirroring `negative_control()` | ❌ W0 | ⬜ pending |
| SAFE-01 | `dim_target >= 0` and `dim_target >= brightness_floor` | static | `python3 docs/environmental_restore_check.py` | ✅ (assertion amended per D-01) | ⬜ pending |
| SAFE-02 | every volume write is `Media`; `allow_volume_increase` false | static | `python3 docs/environmental_restore_check.py` | ✅ | ⬜ pending |
| SAFE-05 | Emergency Restore restores, clears cooldown and the session | static presence ✅ / device effect ❌ | `docs/environmental_restore_check.py` asserts the call | partial | ⬜ pending |
| D-02 (DEV-06) | no `read_value` targets a removed snapshot leaf | static | new assertion alongside the seed-shape check | ❌ W0 | ⬜ pending |
| — | coercion split re-derived after the persistence fix moves sites | static | `python3 docs/phase9_self_check.py` | ✅ (needs new derivation) | ⬜ pending |
| — | the coercion chip renders normally on the rebuilt artifact | rung-2 simulator | simulator import + editor screenshot | ❌ W0 | ⬜ pending |
| CIRC-03, CIRC-05 | capture → apply → restore closes on hardware | manual device | `checkpoint:human-verify` — no automated equivalent | ❌ BLOCKED | ⬜ pending |
| DIST-03 | both forks import and complete a first manual run on a real iPhone | manual device | `checkpoint:human-verify` | ❌ BLOCKED | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] A build guard asserting capture-before-change **persistence** (covers CIRC-03, CIRC-05, SAFE-03)
- [ ] Its negative control in `docs/phase9_self_check.py`
- [ ] Re-derived site counts in `docs/environmental_restore_check.py` and `docs/phase9_self_check.py`
      after the fix moves them, each with a written derivation — **never edit a count to match**
- [ ] A static assertion that no `read_value` targets a leaf removed by D-02
- [ ] `16-UAT.md` — cold-runnable, build-identity-pinned, superseding `09-UAT.md`
- [ ] The aimed coercion probe (build → gate A → sign → **simulator-test** → archive under `.planning/spikes/`)
- [ ] Documentation corrections: `docs/BUILD-NOTES.md` §17 site count; CLAUDE.md §9 rung-2 row and
      the stale "provisional" Safety bullet; the skill's `evidence-and-probes.md` rung-2 table;
      `09-UAT.md` marked superseded; `docs/CAPABILITY-DECISIONS.md` BD-02 updated for D-01

*Framework install: none needed.*

---

## Security Domain

`security_enforcement` is true, ASVS level 1. Single-user, single-device, network-free iOS
automation (DIST-08), so most ASVS web categories do not apply.

| ASVS category | Applies | Standard control |
|---|---|---|
| V2 Authentication | No | No auth surface — no accounts, no network |
| V3 Session Management | Internal only | `active_session` / `Session ID` is a race-protection concept (SESS-03), not a web session |
| V4 Access Control | No | Single local user |
| V5 Input Validation | **Yes, narrowly** | The has-any-value + numeric `> 0` guards around every `Get Device Details` read are this project's input validation for an absent/untrusted external reading. **This phase must not weaken them** — the persistence fix adds a save; it must not touch a gate. |
| V6 Cryptography | No | AEA1 decryption is a build/debug tool, not a shipped feature |
| V7 Error Handling / Logging | Partially | Shortcuts has no try/catch; safety is achieved by **ordering** |

### Threat patterns for this stack

| Pattern | STRIDE-nearest | Mitigation |
|---|---|---|
| Device left dim/quiet after a crash, restart, or missed CLOSE | Denial of Service (of the device's own usability) | Emergency Restore (SAFE-05) — **currently ineffective**; the persistence fix is the actual mitigation |
| A capture written but never persisted | Tampering (integrity of the safety-critical snapshot) | **The live instance of this threat, not a hypothetical** — Finding 1 |
| A capture never taken because the read returned empty | Tampering | has-any-value + `> 0` guard, already correct — do not touch |
| Volume raised, or the ringer touched | DoS / startling output | `WFVolumeSetting = "Media"` at all 15 sites + `allow_volume_increase: false`, pinned structurally |
| A guessed coercion class shipped without confirmation | project-specific: do-not-fabricate | Rung-2 chip check, then the fresh-donor protocol — never a guess |

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| Capture → apply → restore closes on real hardware | CIRC-03, CIRC-05, SAFE-03 | `Get Device Details` returns a real hardware reading; no simulator or static analysis can produce one | `16-UAT.md` |
| The five failure modes (force-quit, restart, missed CLOSE, overlapping sessions, locked screen) | SAFE-03, SAFE-05 | Each requires interrupting a live run on hardware | `16-UAT.md` |
| Emergency Restore recovers from every failure mode found | SAFE-05 | Has never been tapped on a device | `16-UAT.md` |
| Both forks import and complete a first manual run | DIST-03 | Personal Automations are user-created on-device and cannot be exercised anywhere else | `16-UAT.md` |

**All four are BLOCKED on DIST-03.** They are recorded as blocked with the true reason; none may be
inferred, and none may be marked passed by this phase.

~~`xcrun devicectl list devices` → `No devices found.`, re-verified 2026-08-17 after the Phase 13
merge.~~ **SUPERSEDED — that sentence was false when written here and is struck rather than deleted,
so the correction stays auditable** (finding F-01, `16-VERIFICATION.md`). It was true at session
start on 2026-08-17 and was carried into this file after the device state had already changed.

The reason has been re-measured three times and moved each time. Measure it again rather than
trusting any value recorded here:

| Measured | `pairingState` | `tunnelState` | `transportType` |
|---|---|---|---|
| 2026-08-17, session start | — | *(no devices returned)* | — |
| 2026-08-17, planning | `paired` | `disconnected` | `wired` |
| 2026-08-18, plan 16-06 + orchestrator re-check | `paired` | `unavailable` | `none` |

Current true reason: **a paired `iPhone16,1` (iPhone 15 Pro) on iOS 26.6 is known to the host, but
there is no live tunnel and no transport — so there is no session to drive.** Not "no device exists".

Any future re-measurement MUST branch on `tunnelState` read from `--json-output`, **never** on the
`State` column, which prints `available (paired)` even with the tunnel down.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
