---
phase: 14
slug: ash-as-real-color-filters-grayscale
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-18
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source: `14-RESEARCH.md` § Validation Architecture (baseline measured 2026-08-18).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | **None conventional.** No pytest, no test runner, no `tests/`, no `pyproject.toml`, no Makefile. Verification is: two idempotent generators, 13 hand-written `docs/*.py` structural checkers (each `main()` raising `AssertionError`/`SystemExit`), plus the external Playground validator and signer. |
| **Config file** | none — each checker is standalone, resolving `ROOT = Path(__file__).resolve().parents[1]` |
| **Quick run command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` |
| **Full suite command** | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && for f in docs/*.py; do echo "== $f"; python3 "$f" || exit 1; done` |
| **Estimated runtime** | ~seconds (in-build `verify_*` guards are the fastest and strictest signal) |
| **Baseline measured 2026-08-18** | `environmental_restore_check.py` pass; `sequence_dispatch_check.py` pass (0 orphans / 0 unreachable / 0 unknown / 0 duplicates); `phase9_self_check.py` pass (30/30 sites, 19 coerced, 11 correctly not); gate A on `src/PROSOCHE-Dumb.xml` → `Validation passed.` exit 0 |

---

## Sampling Rate

- **After every task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py`
- **After every plan wave:** full 13-checker loop, plus gate A on both forks
- **Before `/gsd-verify-work`:** full suite green (including the new gate-A residue checker), both forks re-signed, `docs/manifest_check.py` green
- **Max feedback latency:** < 30 seconds

---

## Per-Task Verification Map

| Req ID | Behavior | Test Type | Automated Command | File Exists | Status |
|--------|----------|-----------|-------------------|-------------|--------|
| CIRC-02 | The AX identifier is emitted at exactly 15 sites per fork, and the `UA*` twin at zero | structural | `python3 docs/phase5_self_check.py` | ✅ assertion must be **inverted** — W0 | ⬜ pending |
| CIRC-02 | `"Black and White"` still resolves to exactly one dispatch branch | structural | `python3 docs/sequence_dispatch_check.py` | ✅ passes unchanged | ⬜ pending |
| SAFE-01 | No grayscale apply is reachable from an unpersisted ownership marker | build guard | `python3 tools/build_state_engine.py` (`verify_capture_persistence`) | ✅ guard must be **widened** — W0 | ⬜ pending |
| SAFE-01 / CIRC-02 | No grayscale action sits in a permanently-true gate's dead arm | build guard | `python3 tools/build_state_engine.py` (`verify_environmental_reachability`) | ✅ `ENVIRONMENTAL_IDENTIFIERS` must gain the id — W0 | ⬜ pending |
| SAFE-01 | Bootstrap seeds `settings_snapshot.color_filters.original_value` to the sentinel | build guard | `python3 tools/build_state_engine.py` (`verify_state_seed`) | ✅ new seeder recogniser required — W0 | ⬜ pending |
| SAFE-05 | `restore_managed_settings()` still called by `manual_emergency_restore()` and `close_pipeline()`, and now restores three groups | structural | `python3 docs/environmental_restore_check.py` | ✅ `EXPECTED_SITES` + seed loop — W0 | ⬜ pending |
| SAFE-02 | Volume writes remain Media-scoped; counts unmoved at 15/15/22 | structural | `python3 docs/environmental_restore_check.py`, `python3 docs/phase9_self_check.py` | ✅ passes unchanged — **must stay unchanged** | ⬜ pending |
| AUDIT-02 | The record no longer asserts two contradictory things about Ash | grep + manual read | `grep -n "UAToggleColorFilters\|is a real system Color Filters" src/CONFIG-BLOCK.md` | ⚠️ prose — no mechanical assertion today | ⬜ pending |
| AUDIT-02 | **Gate A residue equals exactly the enumerated deviation** (D-14-01) | structural | new `docs/` residue checker | ❌ **W0 gap — does not exist** | ⬜ pending |
| all | Signed artifacts match the manifest rows | structural | `python3 docs/manifest_check.py` | ✅ passes after re-sign | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `docs/phase5_self_check.py` — invert the Color Filters assertion **asymmetrically**: assert `AX*` present with a count, assert `UA*` still absent. The `UA*` half is the guard against a future "fix" that swaps in the macOS twin to satisfy the validator.
- [ ] `tools/build_state_engine.py` `ENVIRONMENTAL_IDENTIFIERS` — add the AX identifier.
- [ ] `tools/build_state_engine.py` `verify_capture_persistence()` — replace the two-way `identifier.endswith("setbrightness")`-else-volume group derivation with an identifier→group mapping including the AX identifier. Unchanged, it would **mislabel** a third identifier.
- [ ] `tools/build_state_engine.py` — new in-place recogniser pass in `seed_settings_snapshot()` for the third snapshot group. `seed_settings_snapshot()` returns early on an already-seeded tree, so adding to `SNAPSHOT_SEED` alone changes nothing in the artifact and then fails `verify_state_seed()` — the exact wall D-02 hit in phase 16.
- [ ] `tools/build_state_engine.py` `VERIFIED_PARAMETER_KEYS` — add `{COLOR_FILTERS: {"state"}}` to opt the action into axis-1 protection.
- [ ] `docs/environmental_restore_check.py` — `EXPECTED_SITES` gains the AX identifier at 15; bootstrap-seed loop gains `"color_filters"`; `REQUIRED_SYMBOLS` gains any new guard symbol.
- [ ] **New gate-A residue checker** (D-14-01) — runs gate A on both forks, subtracts exactly the enumerated `Unknown AppIntent identifier` lines for the AX identifier, exits non-zero on anything else.
- [ ] `14-UAT.md` device instrument, authored whether or not DIST-03 is reachable.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The screen actually turns grey at Circle 2 | CIRC-02 | No simulator can execute the AX intent meaningfully; §9 rung-2 ceiling. Real hardware only. | `14-UAT.md` — reach Circle 2 on a tracked app, observe colour |
| Colour, brightness and volume all return after a force-quit mid-intervention followed by Emergency Restore | SAFE-01, SAFE-05 | The single highest-value test in the phase; exercises all three environmental primitives through one code path | `14-UAT.md`, run in the same sitting as `16-UAT.md`'s 12 outstanding tests |
| A user who opts out via `safety.ash_managed_color_filters=false` never has Color Filters touched | SAFE-02 | Requires observing a device setting the shortcut cannot read back | `14-UAT.md` — set flag false, reach Circle 2, confirm filters unchanged |
| Whether the `state` **response** parameter is consumable as a magic variable (D-14-02) | SAFE-02 | Untested lead from spike 005; determines whether Ash can preserve a pre-existing filter instead of merely disclosing that it overrides one | Rung-2 simulator probe first (no blocking UI — a `Show Alert` wedges the run permanently), then device if inconclusive |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
