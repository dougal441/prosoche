---
phase: 14
slug: ash-as-real-color-filters-grayscale
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-08-18
revised: 2026-08-19
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source: `14-RESEARCH.md` § Validation Architecture (baseline measured 2026-08-18).

> **⚠ REGENERATED 2026-08-19 after the user's scope reset.** The previous Wave 0 list was
> written against the superseded snapshot design and **four of its eight entries no longer
> exist**: the `seed_settings_snapshot()` third recogniser pass, the `verify_capture_persistence()`
> widening, the `EXPECTED_SITES` bootstrap-seed-loop entry, and the spike-011 read-back probe.
> They are struck rather than deleted so the change has something to point at. Under decisions
> **D-14-A/B/C/D** there is no third `settings_snapshot` group, no capture, no ownership marker
> and no persist-before-apply ordering for this primitive, so the guards that assert those
> properties have nothing to assert over it.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | **None conventional.** No pytest, no test runner, no `tests/`, no `pyproject.toml`, no Makefile. Verification is: two idempotent generators, 13 hand-written `docs/*.py` structural checkers (each `main()` raising `AssertionError`/`SystemExit`), plus the external Playground validator and signer. This phase adds a 14th checker. |
| **Config file** | none — each checker is standalone, resolving `ROOT = Path(__file__).resolve().parents[1]` |
| **Quick run command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` |
| **Full suite command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && for f in docs/*.py; do echo "== $f"; python3 "$f" \|\| exit 1; done` |
| **Estimated runtime** | ~seconds. The in-build `verify_*` guards are the fastest and strictest signal. |
| **Baseline measured 2026-08-19** | Pinned counts confirmed at HEAD: `setbrightness = 15`, `setvolume = 15`, `getdevicedetails = 22` in **both** forks. `settings_snapshot` holds exactly `["brightness", "volume"]` in both. 238 text tokens per fork pass the plist round trip's offset assertion. |
| **Gate A** | Clean at HEAD, exit 0 — and **expected to go permanently red from plan 14-01 onward**. Its executable form after plan 14-02 is `python3 docs/gate_a_residue_check.py`. The raw invocation must never be `&&`-chained. |

---

## Sampling Rate

- **After every task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py`
- **After every plan wave:** every script in `docs/` — expected green except `manifest_check.py`, which is deliberately red in waves 1–2 and closed in plan 14-03
- **Before `/gsd-verify-work`:** full suite green including `docs/gate_a_residue_check.py` **and** `docs/manifest_check.py`, both forks re-signed and decrypt-verified
- **Max feedback latency:** < 30 seconds

---

## Per-Task Verification Map

| Req ID | Behavior | Test Type | Automated Command | File Exists | Status |
|--------|----------|-----------|-------------------|-------------|--------|
| CIRC-02 | The AX identifier is emitted at the derived count in both forks; the macOS twin at zero | structural | `python3 docs/phase5_self_check.py` | ✅ assertion **inverted asymmetrically** — W0 | ⬜ pending |
| CIRC-02 | Every AX action carries only the structural UUID and a bare integer state of zero or one | structural | `plistlib` parse of both forks (plan 14-01 T1 verify) | ✅ inline | ⬜ pending |
| CIRC-02 | `ash()` emits no alert, notification or menu | structural | generator source scan (plan 14-01 T1 verify) | ✅ inline | ⬜ pending |
| CIRC-02 | `"Black and White"` still resolves to exactly one dispatch branch | structural | `python3 docs/sequence_dispatch_check.py` | ✅ passes unchanged | ⬜ pending |
| SAFE-01 | An accidental extra parameter on the AX action fails the build | build guard | `python3 tools/build_state_engine.py` (`verify_parameter_keys`) | ✅ `VERIFIED_PARAMETER_KEYS` gains the id — W0 | ⬜ pending |
| SAFE-01 / CIRC-02 | No grayscale action sits in a permanently-true snapshot gate's dead arm | build guard | `python3 tools/build_state_engine.py` (`verify_environmental_reachability`) | ✅ `ENVIRONMENTAL_IDENTIFIERS` gains the id — W0 | ⬜ pending |
| SAFE-01 | `settings_snapshot` still holds exactly two groups; the seed constants are untouched | structural | template parse of both forks (plan 14-01 T2 verify) | ✅ inline | ⬜ pending |
| SAFE-05 | The off leg reaches all four `restore_managed_settings()` call sites and is unconditional | structural | `python3 docs/environmental_restore_check.py` (census row) | ✅ `EXPECTED_SITES` gains a colour row — W0 | ⬜ pending |
| SAFE-05 | `restore_managed_settings()` is still called by `manual_emergency_restore()` and `close_pipeline()` | structural | `python3 docs/environmental_restore_check.py` | ✅ passes unchanged | ⬜ pending |
| SAFE-02 | Volume writes remain Media-scoped; counts unmoved at 15/15/22 and the 15/4 coercion split | structural | `python3 docs/environmental_restore_check.py`, `python3 docs/phase9_self_check.py` | ✅ passes unchanged — **must stay unchanged** | ⬜ pending |
| SAFE-02 | The Control Room Note discloses the Color Filters change and names the kill switch | structural | Note-body parse of both forks (plan 14-03 T1 verify) | ✅ inline | ⬜ pending |
| SAFE-02 | Every text token still passes the plist round trip's offset assertion after the prose edits | structural | `plist_text_edit.assert_offsets_match` over both forks | ✅ inline (238 tokens/fork at baseline) | ⬜ pending |
| AUDIT-02 | Gate A's residue equals exactly the enumerated waiver, in **both** directions | structural | `python3 docs/gate_a_residue_check.py` | ❌ **W0 gap — does not exist** | ⬜ pending |
| AUDIT-02 | No live carrier still asserts the retired gate-A obligation | structural | line-scanning regex over the three live carriers (plan 14-02 T1 verify) | ✅ inline | ⬜ pending |
| AUDIT-02 | The config mirror asserts one thing about this primitive, and has a kill-switch field row | structural | `src/CONFIG-BLOCK.md` scan (plan 14-03 T1 verify) | ✅ inline | ⬜ pending |
| AUDIT-02 | New prose is clear of the retired-clause families | structural | `python3 docs/retired_clause_check.py` | ✅ passes unchanged | ⬜ pending |
| all | Signed artifacts match the manifest rows and their exact display names | structural | `python3 docs/manifest_check.py` | ✅ **expected red** in waves 1–2; closed in 14-03 | ⬜ pending |
| all | `14-UAT.md` records zero passes and is build-identity pinned | structural | UAT scan (plan 14-03 T3 verify) | ❌ **W0 gap — does not exist** | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

**Live — these must exist before the assertions above can run:**

- [ ] `docs/phase5_self_check.py` — invert the Color Filters assertion **asymmetrically**: the `AX*` identifier asserted present at a named derived count, the `UA*` macOS twin asserted still absent. The twin half is the teeth — it is the guard against a future "fix" that substitutes the macOS action to satisfy a red validator. Do not delete the line; deleting removes the twin protection too. *(plan 14-01 T3)*
- [ ] `tools/build_state_engine.py` `VERIFIED_PARAMETER_KEYS` — map the AX identifier to its single donor-evidenced parameter. `verify_parameter_keys()` **skips unmapped identifiers entirely**, so without this the action ships with zero axis-1 protection. *(plan 14-01 T2)*
- [ ] `tools/build_state_engine.py` `ENVIRONMENTAL_IDENTIFIERS` — add the AX identifier as a **recurrence guard**. Silent today (the apply gates on a Config read, and permanence is derived only from `settings_snapshot`-rooted keys); loud the moment somebody puts the apply behind a snapshot container gate's otherwise arm. *(plan 14-01 T2)*
- [ ] `docs/environmental_restore_check.py` — a colour identifier constant and an `EXPECTED_SITES` row at the derived count, plus the new emitter and the primitive in `REQUIRED_SYMBOLS`. Without a census row the checker stays green while covering nothing new. *(plan 14-01 T3)*
- [ ] **`docs/gate_a_residue_check.py`** — new. Runs gate A on both forks, permits exactly the two enumerated line families for the one identifier, and exits non-zero on anything else **including a residue that has shrunk**, because a shrinking residue means emitted sites disappeared. *(plan 14-02 T2)*
- [ ] **`14-UAT.md`** — the device instrument, authored whether or not a device session is reachable. Nothing in this phase is device-proven by construction. *(plan 14-03 T3)*

**Struck — these belonged to the superseded snapshot design and are NOT to be built:**

- ~~`tools/build_state_engine.py` — a third in-place recogniser pass in `seed_settings_snapshot()` for a `color_filters` snapshot group.~~ **There is no third group** (D-14-A). `SNAPSHOT_SEED`, `seed_settings_snapshot()`, `clear_snapshot()` and `verify_state_seed()` are untouched. A task proposing this has reinstated the superseded design.
- ~~`tools/build_state_engine.py` `verify_capture_persistence()` — replace the two-way group derivation with an identifier→group mapping including the AX identifier.~~ **Deliberate non-registration.** Its pending map is keyed by a snapshot capture this primitive never writes, so the assertion could never fire in either direction. A guard registered where it cannot fire is a false certification.
- ~~`docs/environmental_restore_check.py` — the bootstrap-seed group loop gains `"color_filters"`.~~ **Deliberate non-registration.** There is no colour group to seed; adding one would fail against a template that correctly does not carry it.
- ~~Spike 011 — probe the `state` response parameter for accessibility read-back.~~ **Cut by D-14-D.** No detection is built; the pre-existing-grayscale case is accepted, backlogged at `.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`, and compensated by the kill switch plus the onboarding disclosure.

**Also deliberately not registered** (recorded so the set is not "completed" by analogy):
`verify_restore_gates()` — it resolves its operand from the brightness/volume parameter keys this
action does not carry, so the site is skipped before any assertion; and `COMPOUND_STATE_KEYS` —
nothing compound is read.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| **Force-quit mid-intervention, then Emergency Restore, and colour comes back** | SAFE-05, CIRC-02 | **The single highest-value test in the phase.** With no snapshot, an unconditional off leg reached through the panic button is the only thing between a user and being stuck in grayscale. Emergency Restore has never been tapped on a device. | `14-UAT.md` test 1 — run in the same sitting as `16-UAT.md` |
| The screen actually turns black and white when the Circle fires | CIRC-02 | Real-hardware environmental behaviour. §9's rung-2 ceiling excludes it; the sibling brightness action is measured to fail outright on a simulator. | `14-UAT.md` — reach the Circle on a tracked app, observe colour |
| Colour returns on leaving the app, and through Ice expiry and the live-Ice redirect | SAFE-05 | Same class; also needs Personal Automations, which are user-created on the device and cannot be exercised on a simulator at any effort. | `14-UAT.md` |
| The kill switch set off leaves Color Filters untouched and the Circle fires a blank | SAFE-02, D-14-D | Requires observing a device setting the Shortcut cannot read back. | `14-UAT.md` — set the flag false, reach the Circle, confirm filters unchanged |
| The AX action imports and runs without an unfilled-parameter error | SAFE-01 | Signing is measured unaffected by the unknown identifier, but import and run behaviour is device-gated. | `14-UAT.md` |
| The edited Note literal renders correctly after the guarded round trip | AUDIT-02 | Offsets are re-verified structurally in both forks; the rendering itself is device-gated, and an out-of-bounds range can crash Shortcuts on import. | `14-UAT.md` |

**Every one of these is device-gated. No simulator result may be promoted above `UNVERIFIED` for
any of them**, and no device outcome may be inferred from a structural check, a decrypted
artifact or a simulator run. An unrun test stays blank.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify — all 9 tasks carry one
- [x] Wave 0 covers all MISSING references (2 genuinely missing: the residue checker, `14-UAT.md`)
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
