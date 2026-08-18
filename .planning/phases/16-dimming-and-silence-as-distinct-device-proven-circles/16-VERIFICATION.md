---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
verified: 2026-08-18T10:40:00Z
status: human_needed
score: 73/81 must-haves verified
behavior_unverified: 8
overrides_applied: 0
re_verification: null
advisory_findings:
  - id: F-01
    severity: warning
    file: ".planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-VALIDATION.md"
    line: 152
    issue: >-
      Carries the RETIRED, false device measurement verbatim and un-struck:
      "`xcrun devicectl list devices` -> `No devices found.`, re-verified 2026-08-17 after the
      Phase 13 merge." That reading is false. Independently re-measured at HEAD: a paired
      iPhone 15 Pro (iPhone16,1) on iOS 26.6, pairingState paired, tunnelState unavailable,
      transportType None. Every OTHER carrier of this claim was corrected in this phase
      (16-RESEARCH.md retired in place, 16-CONTEXT.md superseded in place, STATE.md, MANIFEST.md,
      16-UAT.md all carry the corrected reason). 16-VALIDATION.md was never in any plan's
      correction scope and was missed.
      The project's own rule, restated in 16-CONTEXT.md, 16-UAT.md and STATE.md, is that
      recording a false device reason is forbidden "exactly as firmly as a false pass".
    fix: >-
      One-line correction: strike the "No devices found." wording and replace the blocked reason
      with "paired device present, tunnelState: unavailable, transportType: none; no live session
      to drive", matching 16-UAT.md's closing section.
    autonomous: true
  - id: F-02
    severity: info
    file: ".planning/REQUIREMENTS.md"
    line: 64
    issue: >-
      CIRC-03's parenthetical still reads "pins `WFVolumeSetting = \"Media\"` at all 14 sites".
      Measured at HEAD: 15 setvolume sites per fork (docs/phase9_self_check.py::site_audit
      asserts 15/15 with a written derivation). 16-CONTEXT.md flagged the "28 operand sites
      (14 + 14)" figure as stale; the same stale figure survives in this requirement line.
      Out of scope for plan 16-05, whose site list covered the retired brightness-floor clause
      only, so this is a pre-existing staleness the phase did not introduce.
    fix: "14 -> 15, with the derivation cited (4 restore call sites + 11 silence() renderings)."
    autonomous: true
deferred: []
behavior_unverified_items:
  - truth: "CIRC-05 precision: the value read by Get Device Details, persisted to state.json as text, and written back through Set Brightness round-trips without rounding or precision loss on real hardware."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Test 2 — read the capture value out of state.json, then Test 4 — compare the post-restore slider reading against the hand-recorded original."
    expected: "The restored brightness equals the pre-dim brightness with no visible step."
    why_human: "Only a real Get Device Details reading has a real precision; no static or simulator channel produces one."
  - truth: "Set Brightness at run time actually CONSUMES a Number-coerced named-variable operand rather than merely rendering its chip normally."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Test 1, legs A and B — observe the ACTUAL brightness applied, not merely the absence of an error."
    expected: "Leg A (coerced) applies the requested value; leg B (uncoerced control) diverges."
    why_human: "Plan 16-02 proved at rung 2 that the simulator CANNOT distinguish a resolved operand from an absent one — both produce the same capability error — and that CAP-08 makes an unresolved operand fail SILENTLY at 50%. A 'no error' result is fully consistent with a broken operand."
  - truth: "Get Device Details current-brightness returns a usable, correctly typed value on real hardware."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Test 2 — a real capture is visible in state.json."
    expected: "A plausible non-zero numeric value in settings_snapshot.brightness.original_value."
    why_human: "The simulator returns 0, measured plan 16-02, and is explicitly not promotable."
  - truth: "SAFE-01: the practical minimum brightness on real hardware is dim rather than a black or unusable screen, so a target of 0 is safe to ship."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Test 5 — dim to 0 and record whether the screen is legible, navigable, and what the Settings slider reads."
    expected: "Screen dim but legible and navigable."
    why_human: "Rests on ONE unrepeated user report. D-01 accepts it as a decision; the decision does not make it a measured device fact, and this build ships dim_target = 0 on the strength of it."
  - truth: "SAFE-03: on a device that already holds a state file seeded with the D-02-removed leaves, the leaves persist harmlessly and no run reads them, so no migration is required."
    verification: backstop
    reason: insufficient_spec
    test: "Run the new build against an existing on-device state.json that still carries changed_at / changed_by_session_id."
    expected: "No dotted-read hard error; the extra leaves are simply ignored."
    why_human: "A device-state claim; the no-reader guard proves the code side statically but cannot observe an existing file on a phone."
  - truth: "DIST-03: both forks import onto a real iPhone and complete a first manual run."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Test 12 — import both signed artifacts and complete a first manual run."
    expected: "Both import under their exact display names and bootstrap without error."
    why_human: "Personal Automations are user-created on device and cannot be exercised anywhere else, at any effort."
  - truth: "CIRC-03, CIRC-05, SAFE-03, SAFE-05: capture, apply and restore close on real hardware across all five failure modes, and Emergency Restore recovers from each."
    verification: backstop
    reason: insufficient_spec
    test: "16-UAT.md Tests 2-11, including the compound overlap-plus-force-quit-the-winner trial."
    expected: "Every path restores or leaves the user at a safe value. Never dark. Never silent forever. Never loud."
    why_human: "No automated or simulator substitute exists. Emergency Restore has still never been tapped on a device."
  - truth: "The phase GOAL itself: Dimming and Silence are DEVICE-VERIFIED Circles with reliable capture-and-restore."
    verification: backstop
    reason: insufficient_spec
    test: "The whole of 16-UAT.md, pinned to Core 9b0f2614... and Aware 1db5c1ef..."
    expected: "12 tests run, outcomes recorded, DIST-03 closed."
    why_human: "The goal's operative word is device-verified. Zero device tests have run. What this phase delivered is the structural precondition that makes the goal satisfiable at all, plus the instrument to prove it."
human_verification:
  - test: "Arrange a live iPhone session (tunnelState is currently `unavailable`, transportType `none`) and run 16-UAT.md end to end against the pinned build."
    expected: "All 12 outcome fields filled with observed values; DIST-03 closed or a real failure recorded."
    why_human: "Every device-behaviour claim in this phase is rung 3-4 on the CLAUDE.md §9 ladder. Rungs 1 and 2 are exhausted — plan 16-02 proved rung 2 CANNOT reach these questions."
  - test: "Batch the session per 16-UAT.md's batching table — 12-UAT Test 3, 13-UAT, 10-UAT, Phase 4 tests 1 and 3-6, Phase 8's real-iPhone import."
    expected: "One session discharges the standing device backlog rather than three sessions covering overlapping ground."
    why_human: "A connected iPhone session is the scarcest input this project has."
  - test: "Before testing, hand-restore any phone that has already run a post-coercion-fix build (iOS Settings -> Display & Brightness / Sounds & Haptics)."
    expected: "Phone at a normal brightness and volume before Test 1."
    why_human: "16-UAT.md's live-hazard section: such a device is dim and quiet right now with no capture on disk, and Emergency Restore cannot help it."
  - test: "Decide F-01 (below): correct the false `No devices found.` claim at 16-VALIDATION.md:152, or accept it as an untouched historical record."
    expected: "Either the one-line correction lands, or an explicit decision that phase artifacts are frozen once written."
    why_human: "The correction is trivially autonomous, but 16-05's own freeze rule declares `.planning/phases/` a historical record. Which rule wins here is a judgment call the user owns."
---

# Phase 16: Dimming and Silence as distinct device-proven Circles — Verification Report

**Phase Goal:** Prove Dimming and Silence work as **distinct, device-verified Circles with reliable capture-and-restore** — the outstanding half of Phase 9, which merged its code untested.
**Verified:** 2026-08-18
**Status:** `human_needed`
**Re-verification:** No — initial verification.

---

## The headline, stated plainly

**The phase goal is NOT achieved, and the phase does not claim it is.**

The goal's operative word is **device-verified**. Zero device tests ran. What Phase 16 actually
delivered is the *precondition* for the goal plus the *instrument* to prove it:

| The goal asked for | What landed | Rung |
|---|---|---|
| Device-proven capture-and-restore | A P0 fix that makes capture-and-restore **possible at all** — before it, no build could have satisfied SAFE-01 | 1 (file-level) |
| `09-UAT.md` tests 2–12 run on a phone | `16-UAT.md` authored, build-identity pinned, all 12 outcomes blank | not run |
| The coercion shape confirmed at a direct Set parameter | An aimed rung-2 probe that proved the question is **unreachable at rung 2** — and found CAP-08 | 2 (simulator) |

That is a real, substantial phase — but it is **structurally proven and behaviourally unproven**,
which is exactly the phrase the MANIFEST, STATE.md and 16-UAT.md all use for it. Nothing in the
tree overclaims. The verdict is `human_needed`, matching the Phase 10 (DIST-03) and Phase 12
(`verification_deferred_human`) precedent.

---

## Goal Achievement

### Observable Truths — by plan

81 truths declared across six plans' `must_haves`. 73 are statically decidable; 8 carry
`verification: backstop` and abstain per honest-verifier discipline.

#### 16-01 — the P0: persist the capture before the device changes (11 truths + 1 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Persist precedes apply, and the persisting save targets `State` | ✓ VERIFIED | **Independently traced, not taken from the guard.** I walked both built XMLs myself: 30 `settings_snapshot.*.original_value` writes, 30 applies. **22 of the 30 captures form an exact `CAPTURE(State) -> SAVE(source=State) -> APPLY` triple** (Dumb indices 1023/1032/1033, 1107/1117/1118, 1275, 1359, 1764, 1848, 2025, 2109, 2286, 2370, 2547, 2631, 2808, 2892, 3069, 3153, 3330, 3414, 3591, 3675, 3852, 3936). The remaining 8 are `clear_snapshot` sentinel writes with no same-group apply in scope. |
| 2 | All 11 `primitive_dispatch()` renderings fixed at the generator, incl. the MANUAL `Test a Circle` arm | ✓ VERIFIED | 22 triples = 11 renderings x 2 primitives. Exactly one `save_state()` call in `dimming()` and one in `silence()`; the count follows from `primitive_dispatch()`, not from 11 edits. The emitted `dimming()` comment renders **11x in each fork** (measured). |
| 3 | CIRC-03 adjacency — captured volume == silence target -> already-quiet arm, no write, no persist | ✓ VERIFIED | `if_block("Captured Volume", 1, number=variable("Silence Target"))` — condition **1** is `<=`, so equality takes the already-quiet arm; that arm holds `nothing` and no `save_state()`. |
| 4 | CIRC-05 boundary — same on brightness | ✓ VERIFIED | `if_block("Captured Brightness", 1, number=variable("Dim Target"))`, identical shape. **Observation (not a defect):** with `dim_target` now `0` and the capture gate `> 0`, this arm is *unreachable at equality* for brightness — the outer gate catches a 0 reading first and routes to the alert branch. Fail-safe direction; recorded so a later reader is not surprised the arm never fires. |
| 5 | Ordering — no action ordering changes the device while state.json holds the sentinel | ✓ VERIFIED | The 22-triple trace above, plus `verify_capture_persistence()` run by me directly against both shipped XMLs: **PASS on both**. |
| 6 | Empty — read returns nothing -> gates skip both persist and apply, alert branch runs | ✓ VERIFIED | `if_block(..., 100)` container gate + `if_block(..., 2, number=0)` capture gate both present and byte-identical; `otherwise(capture_g)` carries `alert("Dim", "Brightness could not be captured, so nothing was changed.")`. |
| 7 | Encoding — persisted original and the operand it feeds resolve Number-typed | ✓ VERIFIED (static half) | `docs/phase9_self_check.py::site_audit` green: 15/15 brightness coerced, 4/15 volume coerced with a written derivation. **The runtime half is truth #8 of the backstop set.** |
| 8 | A build guard fails the build if an apply is reachable from an unpersisted capture | ✓ VERIFIED | `tools/build_state_engine.py::verify_capture_persistence()` (:3778) — per-group bookkeeping, resolves each save's SOURCE via `_save_source_dictionary()` so a `Reloaded State` save cannot clear a pending capture (the exact defect mechanism). Wired into `main()` at :4908 and imported by `build_sentient.py` at :18/:398. |
| 9 | The guard is proven load-bearing by a negative control | ✓ VERIFIED | `docs/phase9_self_check.py::capture_persistence_negative_control()` (:169) calls the **real** `bse.dimming()`/`bse.silence()` and the **real** production guard, strips exactly one save, asserts it raises, then asserts it is silent on real output. Not a re-implementation. Ran it: **PASS**. |
| 10 | The has-any-value (100) and numeric `> 0` (2) gates are byte-identical to pre-plan | ✓ VERIFIED | Both present in `dimming()`/`silence()`; `docs/environmental_restore_check.py` green, which pins them. |
| 11 | Every added save lands outside the CLOSE-owner conditional's non-owner arm, TRACED | ✓ VERIFIED | `docs/state_engine_self_check.py` **PASS** — it owns the span assertion and was not relaxed (no diff to the assertion). |
| B1 | CIRC-05 precision on real hardware | ⚠ ABSTAIN (`backstop`) | `insufficient_spec` — routed to human verification. |

#### 16-02 — the aimed rung-2 coercion probe (7 truths + 2 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 12 | One aimed probe isolating exactly the direct-Set-parameter question | ✓ VERIFIED | `.planning/spikes/010-coercion-at-a-direct-set-parameter/` — README, 3 signed probes, 5 dated XMLs, 5 build/audit scripts, **14 screenshots**. |
| 13 | Built, gate-A validated, signed, simulator-tested BEFORE reaching the iPhone | ✓ VERIFIED | Screenshots `01-import-sheet` through `14-negative-control-...`; drafts + dated archive present. |
| 14 | Result recorded into BUILD-NOTES and the spike README — recorded, not consumed | ✓ VERIFIED | `docs/BUILD-NOTES.md` §29.3–§29.5. |
| 15 | Simulator import channel exercised end to end; CLAUDE.md §9 rung-2 row corrected/confirmed | ✓ VERIFIED | Screenshots 01–03 incl. the `shortcuts://` scheme rejection; `.claude/CLAUDE.md` §9 carries the measured simulator inventory. |
| 16 | The probe distinguishes Number- from Text-resolved at a direct Set parameter | ✓ VERIFIED — **as a negative result** | §29.4: the coerced leg and a *no-operand* negative control produced the **identical** error. **The channel cannot discriminate.** Recorded as the refutation, which is the honest and more valuable finding. |
| 17 | The 11 uncoerced `setvolume` sites dispositioned WITH the probe result + a name-scoped check | ✓ VERIFIED | `docs/phase9_self_check.py` :17/:33-34 — Silence Target is `number()`-sourced (already Number-typed), so all 11 stay deliberately uncoerced; coerced volume count stays 4. `audit_silence_target_sourcing.py` in the spike drafts. |
| 18 | Every simulator observation recorded UNVERIFIED inside the rung-2 ceiling | ✓ VERIFIED | §29.5 "What this probe did NOT settle" states the negative record in full, including that `Set Brightness` is **unreachable at rung 2** and the simulator brightness read of `0` is not promotable. |
| B2, B3 | Runtime consumption of the coerced operand; real-hardware device-details read | ⚠ ABSTAIN (`backstop`) | Routed to human verification. |

**CAP-08 is the most consequential new finding in this phase and it is a safety finding.**
`setbrightness.WFBrightness` is **OPTIONAL and defaults to 50%**. An unresolved operand does not
halt and does not report a parameter error — it silently applies 50% with no capture behind it.
Consequence correctly propagated: `docs/phase5_self_check.py` now asserts the operand is
**present**, and 16-UAT.md Test 1 demands the tester observe the **value applied**, not merely the
absence of an error.

#### 16-03 — D-01 code half (17 truths + 1 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 19 | `brightness_floor` and `dim_target` both `0` in both built forks | ✓ VERIFIED | `src/PROSOCHE-Dumb.xml:163-164`, `src/PROSOCHE-Sentient.xml:197-198` — `"brightness_floor": 0, "dim_target": 0`. |
| 20 | CIRC-05 boundary — floor binds exactly at equality | ✓ VERIFIED | `dim_target >= floor` holds at `0 >= 0`. |
| 21 | This plan carries the CODE half only | ✓ VERIFIED | `files_modified` is 5 code/checker files; no record carrier touched. |
| 22 | The six CODE sites C1–C6 | ✓ VERIFIED | C1 Config literal (both forks); C2 `docs/environmental_restore_check.py:283-285` now `dim_target >= 0`; C3 narrative comment :250-277; C4 module docstring; C5 `docs/phase5_self_check.py:120+` replaced with a CAP-08-derived presence assertion; C6 `dimming()`'s emitted comment. |
| 23 | C5 is the NON-LEXICAL member — no grep gate can be the whole answer | ✓ VERIFIED | Reproduced: a case-insensitive grep of the retired vocabulary over `docs/phase5_self_check.py` returns **0** matches; the site was reachable only by reading. Recorded in both the checker and the gate. |
| 24 | C6 is an EMITTED artifact string shipping 11x/fork; count is 0 after rebuild | ✓ VERIFIED | `grep -c` for the retired bound vocabulary in both forks: **0**. `grep -c "Dimming is reversible or message-only"`: **11** in each fork — the replacement ships at the same multiplicity. |
| 25 | The rebuilt C6 states the PROPERTY, not a softer bound | ✓ VERIFIED | Shipped text: *"the captured original is saved before any change and is always restored"* — names capture-and-restore, asserts no floor, band or minimum. |
| 26 | `silence()`'s parallel comment NOT edited | ✓ VERIFIED | Its SAFE-02 Media/never-increase clause is intact. |
| 27 | Supersession notes cite, never quote | ✓ VERIFIED | BD-02:44 elides the clause explicitly ("…floor clause elided…"); `environmental_restore_check.py` :257-261 cites where it lived. `docs/retired_clause_check.py` green over live files. |
| 28 | `dim_target >= floor` byte-identical; no other assertion weakened | ✓ VERIFIED | `:286-287` unchanged; `allow_volume_increase is False` assertion intact at :288. |
| 29–33 | SAFE-02 untouched (adjacency / empty / ordering, Media at every site, flag false) | ✓ VERIFIED | `docs/phase5_self_check.py` requires `WFVolumeSetting == "Media"` on **every** setvolume action; `environmental_restore_check.py` requires `allow_volume_increase is False`. Both green. |
| 34–36 | SAFE-05 Emergency Restore adjacency / empty / ordering | ✓ VERIFIED (structural) | `environmental_restore_check.py` asserts the `restore_managed_settings()` call inside `manual_emergency_restore()` and the restore-before-clear ordering; green. Device effect is backstop B7. |
| B4 | SAFE-01 — practical minimum is dim, not black | ⚠ ABSTAIN (`backstop`) | One unrepeated user report. Routed to human verification. **This is the truth that carries the most residual risk in the phase**: the build ships `dim_target = 0` on the strength of it. |

#### 16-04 — D-02 dead-state removal (9 truths + 1 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 37 | `changed_at` / `changed_by_session_id` written at **zero** sites in either fork | ✓ VERIFIED | `grep -c` over both fork XMLs: **0** and **0**. |
| 38 | One generator-level change across all three coordinated sites | ✓ VERIFIED | Capture-arm writes removed (:728, :784 comments mark the sites); `SNAPSHOT_SEED` :2926 now `original_value` only; `docs/phase5_self_check.py:107-114` assertion tuple updated with its reason. |
| 39 | A static assertion proves no read targets a removed leaf | ✓ VERIFIED | `verify_no_removed_snapshot_leaf_reads()` (:3867) + `_is_removed_snapshot_leaf()` (:3853), scoped to `settings_snapshot`-rooted or bare-leaf keys so a foreign `changed_at` is not falsely flagged. Ran it directly against both shipped XMLs: **PASS on both**. |
| 40 | The seed still establishes the container and both group sub-dicts, and seeds `original_value` | ✓ VERIFIED | `SNAPSHOT_SEED = {"brightness": ("original_value",), "volume": ("original_value",)}`; `environmental_restore_check.py:245-249` independently requires `settings_snapshot.<group>.original_value` in the bootstrap seed, citing the cycle-10 hard-error class. |
| 41 | The build-j recogniser and the seed shape reasoned about separately | ✓ VERIFIED | :2942-2970 — an unusually good piece of work. `SNAPSHOT_SEEDED_EMPTY` is **deliberately left at three leaves** because build-j wrote three; a second recogniser `SNAPSHOT_SEEDED_D02` is derived from the same two constants so it cannot drift. The reasoning is recorded, not guessed. |
| 42–43 | SAFE-03 empty branch and the two gates byte-identical | ✓ VERIFIED | Alert branch present; both gates unchanged. |
| 44 | BUILD-NOTES §17 site count corrected; DEV-06 recorded DECIDED | ✓ VERIFIED | §17 Addendum (2026-08-18): *"DEV-06 is CLOSED. Decided by the user: **REMOVAL**."* |
| 45 | The explanatory comment rewritten in place, not deleted | ✓ VERIFIED | :519-520 retains the original deferral text verbatim inside its own supersession note. |
| B5 | SAFE-03 — existing on-device state file with the removed leaves | ⚠ ABSTAIN (`backstop`) | Routed to human verification. |

#### 16-05 — D-01 record half + the repo gate (15 truths + 1 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 46 | The RECORD half lands here, split by user decision | ✓ VERIFIED | Plan/ROADMAP both record the split and its rationale. |
| 47 | The canonical strategy and the historical record are FROZEN | ✓ VERIFIED | `git status` clean; `PROSOCHE_Nine_Circles_Canonical_Strategy.md` untouched; the gate's Tier-1 allowlist encodes the freeze **with a reason on every entry** (:124-141). |
| 48 | BD-02 records the §21 supersession EXPLICITLY | ✓ VERIFIED | `docs/CAPABILITY-DECISIONS.md` — Supersession note reached from BD-02 :44, :54, :58, :60, :62; :62 retires the *provisional* and *fork-scoped* framing by name. |
| 49–50 | SAFE-01 and CIRC-05 restated to the real property, as traceable amendments; CIRC-05's TWO corrections on one line | ✓ VERIFIED | `.planning/REQUIREMENTS.md:123` (SAFE-01) and `:66` (CIRC-05) both amended, both citing D-01 and BD-02, and CIRC-05 explicitly names that it carried two independent assertions and corrects both. |
| 51–53 | The site list is MEASURED and explicitly NOT exhaustive; R1–R21 located by content; R13/R15/R16/R20 were the fifth undercount | ✓ VERIFIED | Spot-checked 9 of 21 independently: R1/R2/R3 `src/CONFIG-BLOCK.md:81-82,136,137`; R4–R7 BD-02; R8 BUILD-NOTES CAP-16 :204; R9/R10/R11 REQUIREMENTS; R12/R13 `.planning/PROJECT.md:38,81` (both corrected, the second naming itself as the second site); R18 `.claude/CLAUDE.md` Safety bullet (corrected on disk — the stale text in a session-start cache is not the file); R20 `.planning/STATE.md:168-169`. |
| 54 | R17 discharged at plan time; executor re-verifies | ✓ VERIFIED | ROADMAP plan list matches the six-plan split. |
| 55 | Cite, never quote | ✓ VERIFIED | Gate green over all live files. |
| 56–58 | The gate exists, carries a commented allowlist, states it CANNOT catch non-lexical encodings, and names `phase5_self_check.py:117` as the known blind spot | ✓ VERIFIED | `docs/retired_clause_check.py` — BLIND SPOT block at :58-75 with the *measurement* that proved it, not an argument. Output line itself carries `[LEXICAL ONLY: this is not proof the class is empty]`. |
| 59 | The gate's SECOND invariant — CONFIG-BLOCK vs. both forks | ✓ VERIFIED | Ran it: `src/CONFIG-BLOCK.md agrees with both built forks on brightness_floor=0, dim_target=0`. |
| 60 | Registered in 16-VALIDATION's suite and 16-06's verify chain | ✓ VERIFIED | 16-VALIDATION.md:32 + the landed-marker note at :38. |
| B6 | SAFE-01 backstop (duplicate of B4) | ⚠ ABSTAIN (`backstop`) | Routed to human verification. |

#### 16-06 — rebuild, re-sign, instrument, checkpoint (14 truths + 2 backstop)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 61 | Both forks rebuilt, re-signed under their exact display names, 6 manifest rows refreshed and proven against disk | ✓ VERIFIED | `PROSOCHĒ — Nine Circles — Core.shortcut` 230232 B, `…— Aware.shortcut` 234623 B. I re-ran `shasum -a 256` myself: **both digests match the manifest rows exactly.** No `_signed` suffix; names unchanged. |
| 62 | Full static suite green at phase end, incl. the manifest check | ✓ VERIFIED | **I ran all 13 `docs/*.py` checkers: 13/13 PASS**, including `manifest_check.py` (6 rows, D-MANIFEST closed) and `retired_clause_check.py`. Gate A `Validation passed.` on **both** forks. |
| 63 | 16-UAT.md exists, is cold-runnable, pinned by commit + display name + byte count + SHA-256 per fork | ✓ VERIFIED | Header table carries all four per fork plus a one-line re-verification recipe. |
| 64 | Closed-loop proof FIRST, then the five failure modes | ✓ VERIFIED | Test 1 coercion, Test 2 capture visible in state.json ("the single most valuable test"), Test 3 skip-on-empty, Test 4 CLOSE restores — then 5-11. |
| 65 | The compound overlap-plus-force-quit-the-winner trial is a NAMED test | ✓ VERIFIED | Present with its own outcome fields. |
| 66 | Screen-locked case handed to Phase 18 by reference | ✓ VERIFIED | Stated in the batching table and body. |
| 67 | Explicit batching note naming the other outstanding device work | ✓ VERIFIED | Batching table incl. 12-UAT Test 3 with the reason it is the same observation. |
| 68 | Safety preamble the tester reads first | ✓ VERIFIED | Three numbered warnings + a live-hazard block stating that an already-dimmed phone must be hand-restored via iOS Settings and that Emergency Restore cannot help it. |
| 69 | 09-UAT.md marked superseded, its one pass NOT carried forward | ✓ VERIFIED | 09-UAT.md header is a superseded banner; STATE.md :289 records why the coercion-chip pass does not carry forward — plan 16-02 measured the chip cannot discriminate at this position at all. |
| 70 | SAFE-05 has a named Emergency Restore test after every failure mode, and the instrument records it has never been tapped | ✓ VERIFIED | Present. |
| 71 | DIST-03 re-measured at execution time, real output recorded verbatim | ✓ VERIFIED — **and independently re-measured by me** | My reading at HEAD: `dougal / iPhone16,1 / tunnelState **unavailable** / pairingState paired / transportType **None** / osVersion 26.6`. **Identical to what 16-06 recorded.** Nothing fabricated, nothing inferred. |
| 72 | COVERAGE.md records a reasoned no-external-API declaration | ✓ VERIFIED | Declaration with a per-dependency table and an explicit "why the detector fired anyway" section. Not a fabricated matrix. |
| 73 | The build-identity pin is TWO DISTINCT full 64-char SHA-256 digests, both in the manifest | ✓ VERIFIED | `9b0f2614…2e7c` (Core) and `1db5c1ef…d93b6` (Aware) — 64 hex chars each, distinct, both present in MANIFEST.md and both matching disk. The stated trap (a looser 16+ hex check being satisfied by the commit SHA) is genuinely avoided. |
| 74 | `retired_clause_check.py` runs in this plan's verify chain | ✓ VERIFIED | Registered and green. |
| B7, B8 | DIST-03 import + first manual run; capture/apply/restore on hardware across five failure modes | ⚠ ABSTAIN (`backstop`) | Routed to human verification. |

**Score: 73/81 truths verified. 8 abstained (`verification: backstop`, device-gated).**
No truth FAILED.

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `tools/build_state_engine.py` | Persistence guard + no-reader guard + D-01/D-02 generator changes | ✓ VERIFIED | Both guards present, substantive, wired into `main()`, imported by the Sentient fork. |
| `tools/build_sentient.py` | Imports and calls both guards | ✓ VERIFIED | :18 import, :398 call. |
| `src/PROSOCHE-Dumb.xml` | 4302 actions; floor/target 0; 0 removed leaves; 22 persist triples | ✓ VERIFIED | Measured directly. |
| `src/PROSOCHE-Sentient.xml` | 4370 actions; same invariants | ✓ VERIFIED | Measured directly. |
| `docs/phase9_self_check.py` | Negative control + re-derived site counts | ✓ VERIFIED | Runs the real guard; 15/15 and 4/15 with written derivations. |
| `docs/environmental_restore_check.py` | `dim_target >= 0` and `>= floor` | ✓ VERIFIED | Exactly the single named relaxation; nothing else weakened. |
| `docs/phase5_self_check.py` | CAP-08 presence assertion replacing the value check | ✓ VERIFIED | Replacement is stronger than what it replaced. |
| `docs/retired_clause_check.py` | Repo gate with allowlist + blind-spot statement + config cross-check | ✓ VERIFIED | Green; both invariants live. |
| `artifacts/shortcuts/MANIFEST.md` | 6 refreshed rows | ✓ VERIFIED | `manifest_check.py` green; digests re-verified by hand. |
| Two signed `.shortcut` files | Exact display names | ✓ VERIFIED | 230232 / 234623 bytes, names unchanged. |
| `16-UAT.md` | Cold-runnable, SHA-pinned, all outcomes blank | ✓ VERIFIED | 53 KB instrument; every `outcome:` field blank. |
| `COVERAGE.md` | Reasoned declaration | ✓ VERIFIED | — |
| `.planning/spikes/010-…/` | Probe + 14 screenshots + drafts | ✓ VERIFIED | — |

## Key Link Verification

| From | To | Via | Status |
|---|---|---|---|
| capture arm | `save_state("State")` | must sit between write and apply | ✓ WIRED — 22/22 triples |
| `verify_capture_persistence` | `main()` verify list | :4908 | ✓ WIRED |
| `verify_capture_persistence` | `build_sentient.py` module import | :18 / :398 | ✓ WIRED |
| negative control | the REAL production guard | `bse.verify_capture_persistence` | ✓ WIRED — not a re-implementation |
| `dimming()`'s `comment()` | 11 renderings per fork | `primitive_dispatch()` | ✓ WIRED — 11/11 both forks |
| `src/CONFIG-BLOCK.md` | built forks' Config literal | `retired_clause_check.py` 2nd invariant | ✓ WIRED |
| `retired_clause_check.py` | 16-VALIDATION suite + 16-06 chain | registration | ✓ WIRED |
| signed artifact | MANIFEST row | 16-UAT.md pinned SHA-256 | ✓ WIRED — hand-verified |

## Behavioural Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Persistence guard holds on shipped artifacts | `verify_capture_persistence()` on both parsed XMLs | no raise | ✓ PASS |
| No-reader guard holds | `verify_no_removed_snapshot_leaf_reads()` on both | no raise | ✓ PASS |
| Guard is load-bearing | `python3 docs/phase9_self_check.py` (runs the negative control) | `phase9 self-check: passed` | ✓ PASS |
| All 13 checkers | each `docs/*.py` | 13/13 | ✓ PASS |
| Gate A both forks | `validate-shortcut … --target-macos 26 --target-platform all` | `Validation passed.` x2 | ✓ PASS |
| Artifact digests | `shasum -a 256` vs MANIFEST | exact match x2 | ✓ PASS |
| Device state | `xcrun devicectl list devices --json-output` | `tunnelState: unavailable`, `transportType: None`, paired, 26.6 | ✓ PASS (matches record) |
| Capture→save→apply ordering | independent plist walk | 22 triples, 0 violations | ✓ PASS |
| Device behaviour (any) | — | — | ? SKIP — rung 3-4, no live session |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|---|---|---|---|
| CIRC-03 | Silence reduces media audio only when the original can be captured and restored | ⚠ PARTIAL — static ✓, device ✗ | Persist-before-apply proven at 11 renderings; Media scoping pinned at all 15 sites. Hardware close-of-loop backstop B8. |
| CIRC-05 | Dimming reduces brightness only when reversible — captured **and durably persisted** first | ⚠ PARTIAL — static ✓, device ✗ | Same. The requirement text itself was amended this phase to include durable persistence — before 16-01 **no build could have satisfied it**. |
| SAFE-01 | Brightness changed only when captured and persisted; always restored | ⚠ PARTIAL | Amended and structurally pinned. The `dim_target = 0` safety rests on backstop B4. |
| SAFE-02 | Volume never increased, no startling output | ✓ SATISFIED (static) | Media at every site + `allow_volume_increase: false`, both pinned; D-01 explicitly brightness-only and the volume clause verified untouched. |
| SAFE-03 | Any setting whose original cannot be captured is left unchanged | ✓ SATISFIED (static) | Both gates byte-identical; alert branch present. Device-state edge is backstop B5. |
| SAFE-05 | Emergency Restore clears cooldown, session, and restores brightness/volume/colour | ⚠ PARTIAL | **This phase is what makes SAFE-05 achievable at all** — before 16-01 Emergency Restore was structurally incapable of restoring. Never tapped on a device. |
| DIST-03 | Both forks import onto a real iPhone and complete a first manual run | ✗ **NOT SATISFIED** | Correctly recorded unchecked (`- [ ]`) in REQUIREMENTS.md. Backstop B7. |

No orphaned requirements: all seven declared requirements appear across the six plans' `requirements` fields.

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| — | — | `TBD` / `FIXME` / `XXX` in any modified file | — | **None found.** |
| — | — | `TODO` / `HACK` / `PLACEHOLDER` | ℹ Info | Only `PLACEHOLDER = "￼"` — the U+FFFC attachment constant in two pre-existing checkers. Not a debt marker. |
| — | — | Fabricated device result | — | **None found.** All 12 `outcome:` fields blank; every UAT precedent honoured. |

## Findings beyond the device blocker

Two, both record-integrity rather than code. Neither fails a declared must-have; both are
autonomously fixable and are surfaced rather than folded into the device deferral.

### F-01 (WARNING) — a retired, FALSE device measurement survives in `16-VALIDATION.md:152`

```
**All four are BLOCKED on DIST-03** — `xcrun devicectl list devices` → `No devices found.`,
re-verified 2026-08-17 after the Phase 13 merge.
```

That reading is **false**, and the phase knows it is false everywhere else. `16-CONTEXT.md`,
`16-RESEARCH.md`, `STATE.md`, `MANIFEST.md` and `16-UAT.md` all carry the corrected reason —
*paired device present, no live tunnel* — and three of them say in terms that recording
"No devices found" "would be recording something false, which this project forbids exactly as
firmly as a false pass". `16-VALIDATION.md` appeared in plan 16-05's `files_modified` and was
edited there (the `retired_clause_check.py` registration at :38), so the file was open; the
DIST-03 correction was scoped by 16-06 to `16-RESEARCH.md` only and this carrier was missed.
This is the same failure shape the phase itself documented five times over: *opening a file is
not the same as finishing it.*

Counter-consideration, which is why this is routed to a human rather than called a gap:
plan 16-05's freeze rule declares `.planning/phases/` a historical record that must not be
rewritten, and `retired_clause_check.py`'s allowlist encodes that freeze. A reader could
legitimately hold that this line is frozen history. But it is not marked as history — it is
stated in the present tense as a re-verified measurement, unlike every other superseded claim in
this phase, all of which were struck in place rather than left standing. **Recommendation: strike
it in place, exactly as `16-RESEARCH.md:58` and `16-CONTEXT.md:254` were struck.**

### F-02 (INFO) — a stale site count in `.planning/REQUIREMENTS.md:64`

CIRC-03 still says `WFVolumeSetting = "Media"` is pinned "at all **14** sites". Measured: **15**
per fork. `16-CONTEXT.md` already flagged the parent "28 operand sites (14 + 14)" figure as stale
("it is 30 (15 + 15) per fork as shipped") — the same stale figure survives here. Out of plan
16-05's declared scope, so pre-existing rather than introduced.

## Gaps Summary

**There are no gaps in the sense of work that was planned, claimed, and not done.** Every
artifact the six SUMMARYs describe exists, is substantive, is wired, and holds under independent
re-measurement. The P0 — the phase's most consequential claim — is genuinely closed: I traced all
22 capture→persist→apply triples in the shipped plists myself rather than trusting the guard, and
then ran the guard and its negative control as an independent second channel.

**What is missing is a device.** The goal says *device-verified*; the evidence ladder says that
question lives at rung 3–4; rungs 1 and 2 are exhausted, and plan 16-02 went further and *proved*
rung 2 cannot reach it (`Set Brightness` cannot execute on a simulator at all, and the error
channel cannot discriminate a resolved operand from an absent one). There is nothing further an
autonomous run can extract from this phase.

Two residual risks a human should hold in mind when the session is arranged:

1. **CAP-08 makes silent failure the default failure mode.** An unresolved `WFBrightness` applies
   50% with no capture behind it and no error. Test 1 must observe the **value applied**.
2. **`dim_target = 0` ships on one unrepeated user report.** D-01 is a settled *decision*; it is
   not a settled *device fact*, and the tree is careful to say so in five places. Test 5 is what
   converts it.

---

_Verified: 2026-08-18_
_Verifier: Claude (gsd-verifier)_
