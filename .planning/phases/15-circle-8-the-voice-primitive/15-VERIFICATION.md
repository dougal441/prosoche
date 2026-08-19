---
phase: 15-circle-8-the-voice-primitive
verified: 2026-08-18T11:57:32Z
status: human_needed
score: 15/15 must-haves structurally verified
behavior_unverified: 1
overrides_applied: 0
behavior_unverified_items:
  - truth: "CIRC-08 — 'The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels' actually happens when a user reaches Circle 8 on a real iPhone."
    test: "Run `Test a Circle → Circle 8 · Fraud` on the signed Core build (SHA-256 a5b2976a...) with voice enabled; separately with voice off; separately confirm Circle 7 stays silent."
    expected: "Alert renders and the identical text is spoken exactly once (voice on); alert renders and nothing speaks (voice off, and at Circle 7 regardless of voice setting)."
    why_human: "The Mirror primitive both mirror() and voice() are built on carries a device-reproduced axis-4 unfilled-required-picker defect (reproduced 3x across 2 installs) that plan 15-02's rung-2 simulator probe explicitly could not discriminate (verdict: 'not discriminated at rung 2', spike 011 FINDINGS.md). No file-level check, validator run, or simulator probe can settle whether Circle 8 fires audibly on hardware — only a device session can. `15-UAT.md` is the pre-authored, digest-pinned instrument for this; it is blocked on DIST-03 (no live device session)."
human_verification:
  - test: "15-UAT.md Test 1 — Circle 8 speaks (voice on)"
    expected: "Alert renders AND identical text is spoken exactly once. Failure signature: anything other than the known axis-4 'Please choose a value for each parameter in this action' error is a NEW defect."
    why_human: "Device-only; simulator probe (spike 011) was inconclusive by design and by result."
  - test: "15-UAT.md Test 2 — Circle 7 no longer speaks"
    expected: "Alert renders, nothing spoken, regardless of voice_enabled (D-02)."
    why_human: "Device-only; confirms the CIRC-14 escalation is experienced, not just structurally distinct."
  - test: "15-UAT.md Test 3 — Circle 8 degrades rather than skips (voice off)"
    expected: "Alert renders, nothing spoken — indistinguishable from Circle 7 at this setting (D-01's accepted cost)."
    why_human: "Device-only; also the direct regression test against the original 'Circle 8 does nothing' defect."
  - test: "15-UAT.md Test 4 — voice_enabled round-trips as a number"
    expected: "Status line reads 'Voice: 1'/'Voice: 0' consistently, never 'Yes'/'No', both before and after Toggle Voice; state.json holds a bare JSON number."
    why_human: "Requires reading Status and Quick-Looking state.json on the physical device; not observable from the repository."
---

# Phase 15: Circle 8 — the Voice primitive Verification Report

**Phase Goal:** Build Circle 8 as a real, structurally distinct escalation from Circle 7 — Mirror
(Circle 7) shows a fact-gated reflection, Loud Mirror / Voice (Circle 8) shows and speaks the same
reflection, gated by consent and a once-per-run guard, with no volume manipulation and no
regression to Circle 9 (Ice/Frozen) or to gate-A validation. Per the phase's own corrected ROADMAP
entry, this phase replaces Phase 11's interim Mirror-stand-in at Circle 8 with the designed
primitive — it does **not** need to (and did not need to) fix a silent dispatch, remove a
`KNOWN_ORPHAN_ENTRIES` exemption, or address the `Spoken This Run` suppression warning; all three
were already resolved by Phase 11 and are correctly treated as already-done in every plan in this
phase.

**Verified:** 2026-08-18T11:57:32Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `primitive_dispatch()` dispatches `("Mirror", mirror)` and `("Loud Mirror", voice)` as two distinct functions; `mirror_and_voice()` is retired | ✓ VERIFIED | `grep -n "(\"Mirror\", mirror), (\"Loud Mirror\", voice)" tools/build_state_engine.py` → line 1065; `hasattr(m, 'mirror_and_voice')` → False (measured) |
| 2 | Circle 7 (`mirror()`) shows and never speaks, whatever `voice_enabled` holds (D-02, CIRC-14) | ✓ VERIFIED | `speaktext` count dropped 22→11 per fork (measured); `verify_speaktext_placement()` armed on both forks, asserts zero speech sites inside any `Mirror` branch span, measured failing on a reverted negative-control mutation (plan 15-01 SUMMARY) |
| 3 | Circle 8 (`voice()`) structurally shows AND speaks — 11 `speaktext` sites, all inside `Loud Mirror` branch spans | ✓ VERIFIED | Measured directly: `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` both carry exactly 11 `is.workflow.actions.speaktext` actions; `verify_speaktext_placement()` asserts placement structurally |
| 4 | Voice-off Circle 8 degrades to a Mirror-equivalent alert, never an empty Circle (D-01) | ✓ VERIFIED (structural) | `voice()`'s alert is emitted before the consent gate per plan 15-01's action text and `verify_voice_gates()`'s enclosure assertions; `otherwise` arm is `is.workflow.actions.nothing` — degradation costs zero actions |
| 5 | Circle 8's words are the same 30 fact-gated Mirror templates as Circle 7's — escalation is modality, not copy (D-03) | ✓ VERIFIED | `docs/phase7_self_check.py` exits 0 (≥30 templates); `_mirror_body()` is the single shared consumer of `mirror_text()` in both `mirror()` and `voice()` |
| 6 | `Spoken This Run` guard is byte-identical to what shipped before this phase — no reset, no second flag, no clear step (D-06) | ✓ VERIFIED | Measured: 11 `WFCondition==101` conditionals testing `Spoken This Run`, one per dispatch rendering, matching the 11 speech sites exactly — no reset/clear action added |
| 7 | Speech is unreachable outside both the consent gate (`voice_enabled > 0`) and the once-per-run gate — structurally, on every site, both forks (CIRC-08) | ✓ VERIFIED (structural) | `verify_voice_gates()` armed on both forks (`grep -c` → 2 each); measured failing on 3 negative-control mutations including the vacuous-resolution direction (plan 15-04 SUMMARY) |
| 8 | Nothing in the Voice path writes device volume — "never at unsafe levels" satisfied by absence (CIRC-08, SAFE-02) | ✓ VERIFIED | `verify_voice_path_volume_silence()` armed on both forks; measured: 0 `setvolume` sites inside any `Loud Mirror` branch span, 15 total unchanged, all Media-scoped |
| 9 | `voice_enabled` holds a JSON number on every write path — bootstrap and Toggle Voice agree by construction (D-05) | ✓ VERIFIED | Measured: the two `Voice Normalised` gettext values are `['0','1']`; `Contract Respected`'s unrelated gettext pair (`true`/`false`) is untouched |
| 10 | An existing `state.json` on the old boolean schema is rebuilt exactly once — `schema_version` 4→5 (D-05) | ✓ VERIFIED | Measured: `SCHEMA_VERSION=5`, `SCHEMA_VERSION_PREVIOUS=4`; `python3 tools/build_state_engine.py` run twice in succession, both exit 0 (idempotence) |
| 11 | Circle 9 still dispatches `Frozen` in all three sequences; `ice_start()` untouched (CIRC-09) | ✓ VERIFIED | `docs/phase5_self_check.py` exits 0; `src/CONFIG-BLOCK.md`'s three `sequences` arrays all end `..., "Frozen"]`; no `ice_start` reference in any Phase-15 diff |
| 12 | Two distinct sequence-entry names never resolve to action-equal dispatch branch bodies (CIRC-14, edge: adjacency/ordering) | ✓ VERIFIED | `docs/sequence_dispatch_check.py` exits 0, reports "0 action-equal pair(s)" of 99 branches / 9 distinct names; new `branch_bodies()`/`action_equal_pairs()`/fifth `require()` measured failing on a reverted mutation |
| 13 | Both forks pass validator gate A clean at `--target-macos 26 --target-platform all` (DIST-01) | ✓ VERIFIED | Ran directly: both `validate-shortcut` invocations print `Validation passed.`, exit 0 |
| 14 | Every Mirror template list carries ≥9 rows so `WFItemIndex = Circle Next` (1..9) stays in range (backstop) | ✓ VERIFIED (direct measurement) | Measured directly: `MIRROR_BASELINES`/`MIRROR_SUCCESSES`/`MIRROR_LAPSES` each hold exactly 10 rows |
| 15 | All 12 `docs/*.py` checkers exit 0, including `manifest_check.py`, and the signed artifacts are re-derived (not row-edited) | ✓ VERIFIED | Ran all 12 checkers directly — all exit 0; `shasum -a 256` on both signed `.shortcut` files matches the digests recorded in `MANIFEST.md` and `15-UAT.md`'s header exactly |
| 16 | **The behavioral core of CIRC-08 — Circle 8 actually speaks once, safely, on a real iPhone** | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | See `behavior_unverified_items` above. Structurally proven (truths 3, 7, 8); the underlying Mirror-primitive Shortcuts action span carries a device-reproduced axis-4 defect that plan 15-02's rung-2 simulator probe could not discriminate (spike 011: `not discriminated at rung 2`). Every phase artifact (MANIFEST.md, BUILD-NOTES §36, 15-UAT.md) states this plainly and refuses to infer a device pass from a green build. |

**Score:** 15/15 structurally-verifiable truths verified. 1 truth (the core behavioral claim of
CIRC-08) is present-and-wired but not behaviorally exercised — this is not a gap in this phase's
work, it is an honestly-recorded, pre-existing, device-gated blocker (`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`) that this phase discriminated at rung 2 (per its own D-04 decision) but explicitly could not close, and said so everywhere a reader would look.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `tools/build_state_engine.py :: _mirror_body()`, `mirror()`, `voice()` | Shared-body split of the retired `mirror_and_voice()` | ✓ VERIFIED | All three callable, `mirror_and_voice` absent (measured) |
| `tools/build_state_engine.py :: verify_speaktext_placement()` | Placement guard | ✓ VERIFIED | Present, called in `main()`, armed on Sentient fork |
| `tools/build_state_engine.py :: verify_voice_gates()` | Two-gate enclosure guard | ✓ VERIFIED | Present, called, armed on Sentient fork |
| `tools/build_state_engine.py :: verify_voice_path_volume_silence()` | Volume-silence guard | ✓ VERIFIED | Present, called, armed on Sentient fork |
| `tools/build_state_engine.py :: verify_voice_enabled_seed()` | Type/seed guard | ✓ VERIFIED | Present, called, armed on Sentient fork |
| `docs/sequence_dispatch_check.py :: branch_bodies()` + fifth `require()` | Action-equality checker assertion | ✓ VERIFIED | `python3 docs/sequence_dispatch_check.py` reports "0 action-equal pair(s)", exits 0 |
| `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` (regenerated) | Both forks rebuilt with all changes | ✓ VERIFIED | Rebuilt, gate A clean, measured action counts match |
| `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Core,Aware}.shortcut` (re-signed) | Signed, correctly named, non-`_signed`-suffixed | ✓ VERIFIED | Both present, filenames exact, `manifest_check.py` passes, digests match header |
| `docs/BUILD-NOTES.md §36` | Full recording duty for the phase | ✓ VERIFIED | Present, contains D-01..D-06, four declined alternatives, probe verdict with evidence rung, CIRC-08 device status stated plainly |
| `.planning/phases/15-circle-8-the-voice-primitive/15-UAT.md` | Cold-runnable, digest-pinned device instrument | ✓ VERIFIED | Present, pinned to both signed SHA-256 digests (confirmed matching disk), records nothing as passed, `status: blocked` (honest) |
| `.planning/spikes/011-mirror-primitive-picker-discriminator/FINDINGS.md` | Rung-2 discrimination verdict | ✓ VERIFIED | Present, verdict `not discriminated at rung 2`, evidence-rung analysis included |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `primitive_dispatch()` tuple | `mirror()` / `voice()` | direct function reference | ✓ WIRED | `("Mirror", mirror), ("Loud Mirror", voice)` at line 1065 |
| `_mirror_body()` | `mirror_text()` → 30 templates | single shared consumer | ✓ WIRED | Both `mirror()` and `voice()` call `_mirror_body()`; no duplicate template selection found |
| `verify_speaktext_placement()` | `enclosing_groups()` | branch-span computation | ✓ WIRED | Confirmed via docstring and source read; structural, not index-based |
| `verify_voice_gates()` | `_voice_enabled_variables()` | provenance resolution | ✓ WIRED | Confirmed via source and docstring — no hardcoded variable-name literal for the consent role |
| `docs/sequence_dispatch_check.py` | built artifact (plistlib, read-only) | `branch_bodies()` / `action_equal_pairs()` | ✓ WIRED | Checker runs read-only against `src/*.xml`, no subprocess/rebuild; exits 0 |
| `voice_enabled` bootstrap writer | `Toggle Voice` writer | shared numeric literal shape | ✓ WIRED | Both now write `1`/`0`; `verify_voice_enabled_seed()` holds the shape at build time |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Both forks validate at gate A | `validate-shortcut src/PROSOCHE-{Dumb,Sentient}.xml --target-macos 26 --target-platform all` | `Validation passed.` (both) | ✓ PASS |
| Speech site count matches claim | direct plistlib parse of both `src/*.xml` | 11/11 `speaktext`, 15/15 `setvolume` | ✓ PASS |
| All 12 project checkers | `python3 docs/*.py` (12 named checkers) | all exit 0 | ✓ PASS |
| Signed artifact digests match claimed | `shasum -a 256` on both `.shortcut` files | matches `MANIFEST.md` and `15-UAT.md` header exactly | ✓ PASS |
| Circle 8 audibly speaks on a real iPhone | `15-UAT.md` Test 1 | not run — blocked on DIST-03 | ? SKIP (routed to human verification) |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| CIRC-08 | 15-01, 15-02, 15-03, 15-04, 15-05 | Voice speaks the Mirror at most once per run, only when enabled, never at unsafe levels | ⚠ STRUCTURALLY SATISFIED / DEVICE-UNPROVEN | All structural gates verified (truths 7, 8, 9, 10); the runtime behavior itself is device-gated per spike 011's inconclusive rung-2 verdict — human verification required |
| CIRC-09 | 15-01 (regression only) | Ice applies a deterministic cooldown, decided without the model | ✓ SATISFIED | Regression-only scope, as the plan itself flags; `phase5_self_check.py` confirms Circle 9 = Frozen unchanged in all sequences |
| CIRC-14 | 15-01, 15-04 | A stronger Circle does not necessarily replay every weaker Circle's prompt | ✓ SATISFIED | Structurally distinct branches (11 speech sites all in Loud Mirror); action-equality checker proves no two entries collapse to one behaviour. Note: with `voice_enabled=0`, Circles 7/8 are experientially indistinguishable — this is D-01's accepted, recorded cost, not a CIRC-14 failure (satisfied by construction) |
| DIST-01 | 15-01, 15-03, 15-04, 15-05 | Both forks pass the Shortcuts Playground validator at the iOS 26 target | ✓ SATISFIED | Gate A verified directly on both forks; gate B correctly treated as advisory/waivered throughout, never chained into any definition of done |

**Note on REQUIREMENTS.md:** the requirements-coverage table in `.planning/REQUIREMENTS.md` maps
CIRC-08/09/14 to "Phase 5" and DIST-01 to "Phase 8" as "Complete" — these are stale mappings to the
original design phases and were not updated by Phase 15 (out of scope for any of its five plans'
`files_modified`). This is a pre-existing documentation staleness issue, not a Phase 15 gap.

### Anti-Patterns Found

None. Scanned all Phase-15-modified files (`tools/build_state_engine.py`, `tools/build_sentient.py`,
`docs/sequence_dispatch_check.py`, `src/CONFIG-BLOCK.md`, `docs/BUILD-NOTES.md`) for `TBD`/`FIXME`/`XXX`
debt markers — zero found. No placeholder returns, no stub handlers, no hardcoded empty data feeding
a user-facing surface were found in the diff.

### Human Verification Required

Device UAT is required to close CIRC-08's behavioral claim. `15-UAT.md` is the pre-authored,
digest-pinned instrument (blocked on DIST-03 — no live device session available to this agent).

1. **Circle 8 speaks (15-UAT.md Test 1)**
   **Test:** `Test a Circle → Circle 8 · Fraud` on signed Core (SHA-256 `a5b2976a…`), voice enabled.
   **Expected:** Alert renders and identical text is spoken exactly once.
   **Why human:** Device-only; the underlying Mirror-primitive action span carries a
   device-reproduced axis-4 unfilled-picker defect that a rung-2 simulator probe (spike 011)
   explicitly could not reproduce or discriminate.

2. **Circle 7 no longer speaks (15-UAT.md Test 2)**
   **Test:** `Test a Circle → Circle 7 · Violence`, voice enabled.
   **Expected:** Alert renders, nothing spoken (D-02's intended, recorded behaviour change).
   **Why human:** Device-only; confirms the escalation is experienced, not just structurally present.

3. **Circle 8 degrades rather than skips, voice off (15-UAT.md Test 3)**
   **Test:** Toggle Voice off, then `Test a Circle → Circle 8 · Fraud`.
   **Expected:** Alert renders, nothing spoken — indistinguishable from Circle 7 at this setting.
   **Why human:** Device-only; direct regression test against the original "Circle 8 does nothing" defect.

4. **Consent flag round-trips as a number (15-UAT.md Test 4)**
   **Test:** Read `Status` before and after one `Toggle Voice`; Quick Look `state.json`.
   **Expected:** `Voice: 1`/`Voice: 0` consistently, never `Yes`/`No`; `voice_enabled` is a bare JSON number.
   **Why human:** Requires reading device UI and a Quick Look file preview; not observable from the repo.

### Gaps Summary

No structural gaps found. Every truth, artifact, key link, and requirement this phase's own plans
committed to is present, wired, and — where mechanically checkable — independently re-measured
against the actual codebase rather than trusted from SUMMARY.md prose (rebuilt XML action counts,
re-ran all 12 checkers, re-ran gate A on both forks, recomputed both signed artifacts' SHA-256
digests, confirmed all cited commit hashes exist, read guard docstrings for the claimed negative
controls).

The single open item is not a gap this phase failed to close — it is the phase's own honestly
recorded limit. CIRC-08's actual runtime behavior on a real iPhone cannot be established by any
means available to this verifier (or, per `15-02-SUMMARY.md`'s own rung-2 probe, by any means
available short of a real device session). The phase's own artifacts (`15-CONTEXT.md` D-04,
`15-02-PLAN.md`, `spike 011/FINDINGS.md`, `docs/BUILD-NOTES.md §36`, `artifacts/shortcuts/MANIFEST.md`,
`15-UAT.md`) all state this plainly, consistently, and in the same place as the claims they qualify —
exactly what the phase's own `<what_to_verify_hardest>` instruction 6 asked this verifier to check
for. No artifact anywhere implies Circle 8 is known to work on a device. This verifier concurs.

**Recommended next action:** schedule the batched device session `15-UAT.md` itself names
(`16-UAT.md`, `12-UAT.md` Test 3, `13-UAT.md`, `10-UAT.md`, Phase 19's sweep) — this is a
pre-existing, cross-phase DIST-03 blocker, not something Phase 15 could have closed alone. Until
then, this phase's status is honestly `human_needed`, not `passed`.

---

*Verified: 2026-08-18T11:57:32Z*
*Verifier: Claude (gsd-verifier)*
