---
phase: 14-ash-as-real-color-filters-grayscale
verified: 2026-08-19T01:56:29Z
status: human_needed
score: 27/34 must-haves verified
behavior_unverified: 0
overrides_applied: 0
abstained_backstop: 7
requirements: [CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02]
human_verification:
  - test: "Open a tracked app until the Black and White Circle fires on a real iPhone."
    expected: "The whole screen goes greyscale. No alert, no notification, no menu, nothing to tap."
    why_human: "insufficient_spec / device-gated. `verification: backstop` in 14-01 and 14-03. This is the same class of environmental action as Set Brightness, which is MEASURED to fail outright on a simulator ('There was a problem setting the brightness'); a simulator reading is never promotable above UNVERIFIED per `.claude/CLAUDE.md` §9 'Rung 2's ceiling'. Structural coverage is complete; behavioural coverage is not obtainable from here. 14-UAT.md Test 2."
  - test: "Force-quit the tracked app AND the Shortcuts app mid-intervention so no CLOSE can fire, then run the shortcut by hand and choose Emergency Restore."
    expected: "Colour returns immediately, without opening Settings."
    why_human: "insufficient_spec / device-gated. `verification: backstop` in 14-01 and 14-03. THE SINGLE HIGHEST-VALUE OBSERVATION IN THE PHASE: with no snapshot, the unconditional off leg reached through the panic button is the only thing between a user and permanent greyscale. Emergency Restore has never been tapped on a device in any phase. 14-UAT.md Test 1."
  - test: "Leave the tracked app normally (CLOSE), and separately let Ice expire and take the live-Ice redirect."
    expected: "Colour returns on each of the three paths."
    why_human: "insufficient_spec / device-gated. `verification: backstop` (SAFE-05). The off leg is structurally present, ungated and first at all four call sites — verified in both decrypted signed forks — but whether the action executes is device-gated. 14-UAT.md Tests 3 and 4."
  - test: "Import both signed forks on an iOS 26 iPhone and run the Black and White Circle."
    expected: "No unavailable-action warning on import; no 'Please choose a value for each parameter' dialog at the action."
    why_human: "insufficient_spec / device-gated. `verification: backstop` (SAFE-01). Signing is measured unaffected by the unknown identifier and the action is donor-exact, but the identifier is absent from all three bundled ToolKit snapshots so no file-level check can speak to import or run behaviour. Note also that the emitted action carries no `UUID` key (finding F-3), a structural divergence from the donors that only a device run can clear. 14-UAT.md Test 6."
  - test: "Read the Control Room Note on a real device after the guarded round trip."
    expected: "The new Color Filters disclosure renders correctly, with no blank or garbled inline values."
    why_human: "insufficient_spec / device-gated. `verification: backstop` (SAFE-02). Offsets are re-verified structurally — 0 of 1115 (Core) / 1123 (Aware) whole-document token strings fail `assert_offsets_match` in the decrypted signed artifacts — but rendering is device-gated, and the Note path additionally needs `com.apple.mobilenotes`, which is absent from the booted simulator's 25 apps."
  - test: "Set safety.ash_managed_color_filters to false and fire the Circle."
    expected: "Color Filters are untouched and the Circle produces no visible output at all."
    why_human: "insufficient_spec / device-gated. The gate is structurally correct (numeric `> 0` over the Config read, otherwise arm is a bare Nothing — verified in the generator and at all 11 rendered sites), but the flag is the ONLY recourse a colour-blind, migraine or low-vision user has until the backlogged detection item ships, so it warrants a device observation rather than a structural one. 14-UAT.md Test 5."
  - test: "Judgement call for the maintainer, not a device test: accept that the enumerated gate-A residue is stable only until a future Shortcuts Playground plugin update, and that the spec-less edge probe returned unclassified/unresolved for all five of CIRC-02, SAFE-01, SAFE-02, SAFE-05 and AUDIT-02."
    expected: "Accepted as surfaced-not-dismissed, or a held-out check is written."
    why_human: "insufficient_spec. `verification: backstop`. The plugin snapshot lives outside this repository; `docs/gate_a_residue_check.py` turns a snapshot that gains the identifier into a loud failure rather than a silent drift, but the event itself is not observable from here. The five unclassified edges were deliberately surfaced by the planner rather than dismissed and no verifier evidence can resolve them."
---

# Phase 14: Ash as real Color Filters grayscale — Verification Report

**Phase Goal (binding: `14-CONTEXT.md` `<decisions>`, D-14-A/B/C/D + D-14-01 + D-14-03):**
Circle 2 emits a real Color Filters grayscale action instead of an alert; an unconditional off
leg reaches all four recovery paths; no snapshot, no capture, no ownership marker; the kill
switch goes live; gate A's permanent residue is formalised mechanically; the change is disclosed
in the Control Room Note.

**User's own words:** *"open target app, we've hit the circle, phone goes black and white. no
notifications, nothing. then when you leave the app, your phone turns colour back on. simple."*

**Verified:** 2026-08-19T01:56:29Z
**Status:** human_needed
**Re-verification:** No — initial verification

---

## Post-verification amendment — 2026-08-19 (orchestrator)

**Finding F-1 has been actioned. The verdict below is UNCHANGED: `human_needed`, 27/34.**

F-1 asked for a correction to `14-03-SUMMARY.md`'s claim that the 238-text-token baseline was
unreproducible. That correction landed in `91feb59`. The orchestrator independently reconfirmed
the finding on a second counting basis before amending: `WFTextActionText` action parameters in
the Core fork read **260** at `953ff1e` (the pre-wave-1 scope-reset commit) and **271** at both
`ca0bbea` and HEAD. The verifier's basis reads 238 → 249 across the same commits. Two different
bases, the same delta of **exactly +11 per fork** — `ash()`'s eleven config reads, one per
`primitive_dispatch()` rendering. The baseline was never unreproducible; it was taken at a
different commit from the one this plan measured.

**Why this section exists rather than a silent edit.** `query verification.status` derives
staleness from "a summary newer than the verification". Actioning F-1 necessarily rewrites a
SUMMARY, which necessarily stales this report — so the correction the verifier asked for cannot
be made without tripping the staleness rule. Nothing in the codebase, the generators, or either
signed artifact changed: the amendment is documentation-only, confined to a SUMMARY's narrative
about a measurement, and the 27 structural must-haves and 7 device-gated abstentions below all
stand exactly as verified. This note records that fact in the report itself rather than leaving a
`stale` reading that would imply the phase needs re-verifying when it needs a **phone**.

---

## Verdict in one line

**The build is structurally complete and correct, and behaviourally unproven.** Every claim that
a file, a count, a shape or a wiring can settle, I settled independently against the *decrypted
signed artifacts* rather than the source — and all of them hold. Nothing in this phase has run
on a phone, and by the honest-verifier protocol every `verification: backstop` truth abstains
rather than inheriting a pass from the structure underneath it. `human_needed` is the correct
and expected outcome here; it is not a failure.

---

## Goal Achievement

### Observable Truths — structural (independently measured, not read from SUMMARY.md)

Evidence marked **(signed)** was measured on the plists recovered from the two AEA1 containers
via `.claude/CLAUDE.md` §8's `aea decrypt` → `aa extract` recipe, not on `src/`.

| #  | Truth | Status | Evidence |
|----|-------|--------|----------|
| 1 | `ash()` emits the AX action with `state = 1` and NOTHING else — no alert, no notification, no menu (CIRC-02, D-14-A/D-14-C) | ✓ VERIFIED | **(signed)** 11 apply sites per fork, **one distinct shape across all 11**: `comment → getvalueforkey → gettext → setvariable → comment → conditional → AXToggleColorFiltersIntent → conditional → nothing → conditional`. No `showalert`, `notification` or `choosefrommenu` in the block. Generator `ash()` (`tools/build_state_engine.py:678-750`) contains no `alert(` call. |
| 2 | `safety.ash_managed_color_filters` is live, read through a numeric `> 0` gate; false → bare Nothing (CIRC-02, D-14-D) | ✓ VERIFIED | `a += config("safety.ash_managed_color_filters", ...)` then `if_block(..., 2, number=0)`; otherwise arm is `action("is.workflow.actions.nothing")`. **(signed)** 11 `getvalueforkey WFDictionaryKey=safety.ash_managed_color_filters` sites per fork. String-compare hazard explicitly commented against. |
| 3 | One unconditional `state = 0` inside `restore_managed_settings()` reaches all four call sites (SAFE-05, D-14-B) | ✓ VERIFIED | Single `a += [set_color_filters(False)]` at `:649`. Call sites measured: `close_pipeline()` `:1785`, `live_ice_redirect()` `:2293`, `ice_expiry()` `:2305`, `manual_emergency_restore()` `:2377`. **(signed)** exactly 4 off sites per fork, at indices 176 / 226 / 1585 / 4168 in Core. |
| 4 | The off leg is emitted FIRST, above the brightness block (SAFE-05) | ✓ VERIFIED | **(signed)** at every one of the 4 off sites the action sits immediately after the restore comment and immediately before `getvalueforkey → gettext → setvariable` (the `settings_snapshot.brightness` read). **No conditional intervenes** — the leg is genuinely ungated: no snapshot read, no numeric test, no ownership compare. |
| 5 | No snapshot leaf, no ownership marker, no `save_state()` in `ash()`; `settings_snapshot` stays at exactly TWO groups (SAFE-01, D-14-A) | ✓ VERIFIED | `SNAPSHOT_SEED = {"brightness": (...), "volume": (...)}` — two entries. **(signed)** the shipped bootstrap literal reads `"settings_snapshot": {"brightness": {"original_value": "null"}, "volume": {"original_value": "null"}}` in both forks. `ash()` calls neither `save_state()` nor `set_value()`. |
| 6 | Guard registration decided per guard from what each guard asserts, with the reasoning in the source (SAFE-01) | ✓ VERIFIED | `COLOR_FILTERS` appears in `VERIFIED_PARAMETER_KEYS` (`:2710`, mapped to `{"state"}` only, which makes an `operation` write a build failure) and in `ENVIRONMENTAL_IDENTIFIERS` (`:4738`, annotated as a *recurrence* guard that is deliberately silent today). It appears in **neither** `verify_capture_persistence()` nor `verify_restore_gates()`. A `DELIBERATE_NON_REGISTRATIONS` block at `:4741+` records the general rule. |
| 7 | The AX site count is DERIVED from the built artifact, equal in both forks, arithmetic beside the census (CIRC-02) | ✓ VERIFIED | **(signed)** 15 per fork, Core and Aware identical. Arithmetic (11 dispatch renderings + 4 restore call sites) written out in three independent places: `docs/environmental_restore_check.py:196-218`, `docs/gate_a_residue_check.py` census block, `docs/phase5_self_check.py:47`. Not the superseded 15/fork-under-snapshot figure — the derivation, not just the number, is stated. |
| 8 | `setbrightness = 15`, `setvolume = 15`, `getdevicedetails = 22` UNMOVED (SAFE-02) | ✓ VERIFIED | **(signed)** all three exact in both forks. Also exact in `src/`. |
| 9 | `docs/phase5_self_check.py`'s Color Filters assertion inverted ASYMMETRICALLY — `AX*` present at a count, `UA*` twin still absent (CIRC-02) | ✓ VERIFIED | `:163` asserts `AX` count == 15; `:167` asserts `UA_COLOR_FILTERS_MACOS_TWIN not in text`. The teeth-bearing half survives, with the reason commented at `:150-156`. |
| 10 | `.claude/CLAUDE.md`'s gate-A clause amended from "must pass clean, exit 0" to "residue must equal exactly the enumerated waiver" (AUDIT-02, D-14-01 item 1) | ✓ VERIFIED | Heading now reads *"Gate A — mandatory, residue must equal exactly the enumerated waiver"*; body expects **exit 1 with exactly 30 lines per fork**; mirrors gate B's existing table structure rather than inventing one. |
| 11 | The amendment is narrow in three stated ways | ✓ VERIFIED | Enumerated as items 1–3 in the amended clause: scoped to one identifier by full string; line count derived from site count (15 × 2 = 30); catalog gap recorded at `docs/BUILD-NOTES.md` §5 `DEV-08` where a red gate sends a reader. |
| 12 | The waiver is MECHANICAL, and fails on a residue that has SHRUNK as well as grown (AUDIT-02, D-14-01 item 2) | ✓ VERIFIED — **and independently proven to have teeth** | `docs/gate_a_residue_check.py` exits 0 at HEAD. I ran two negative controls against scratch copies: (a) delete one AX action → `AssertionError: the permitted residue is 28 line(s), expected exactly 30 … A SMALLER residue means emitted AX sites DISAPPEARED`; (b) swap one site to the `UA*` macOS twin → `AssertionError: gate A reported 1 line(s) OUTSIDE the enumerated waiver`. Both directions fire. A `classifier_control()` with 2 must-permit and 6 must-not-permit rows runs on every invocation. |
| 13 | The waiver enumerates BOTH validator line families (AUDIT-02) | ✓ VERIFIED | `FAMILIES` holds `Unknown AppIntent identifier` and `AppIntent action missing AppIntentDescriptor`, each regex demanding the full identifier string. Both tabulated in `.claude/CLAUDE.md`. |
| 14 | Gate A joins gate B in never exiting zero, consequence stated, checker named by path (AUDIT-02) | ✓ VERIFIED | Companion note in the gate-B section states it explicitly and names `python3 docs/gate_a_residue_check.py` as the replacement obligation. **No raw-validator `&&` chain was introduced anywhere** — `git diff 0a3b017 HEAD \| grep '^+' \| grep 'validate-shortcut.*&&'` returns nothing. |
| 15 | The deviation recorded in the build notes with a reproduction command, positioned before the temptation (AUDIT-02, D-14-01 item 3) | ✓ VERIFIED | `docs/BUILD-NOTES.md:269` §5 `DEV-08`, plus the deviation-table row at `:466` which explicitly says **"Never resolve this by substituting `UAToggleColorFiltersIntent`"**. |
| 16 | Gate B untouched; the two validator anti-pattern rules keep their teeth (AUDIT-02) | ✓ VERIFIED | Gate B section unchanged in substance (one-line `WFCreateNoteInput` waiver, advisory, false-acceptance limit). Anti-pattern rows survive at `.claude/CLAUDE.md:363` and `:364`. |
| 17 | Dated historical records not edited; supersession by pointer; superseded wording cited, not restated (AUDIT-02) | ✓ VERIFIED | See finding **F-4**. `artifacts/shortcuts/MANIFEST.md` retains **five** historical gate-A cells unedited, each carrying an inline `gate-A status superseded` pointer — I opened all five (`:68, :284, :332, :371, :391`) and confirmed each. `src/CONFIG-BLOCK.md:95` retains the twice-superseded BD-01 paragraph with a pointer. |
| 18 | The Control Room Note states PLAINLY that PROSOCHĒ turns Color Filters on and off (SAFE-02, D-14-D) | ✓ VERIFIED | **(signed)** present in **both** forks, in the `### One of them changes your screen` block. Plain language, no jargon: *"PROSOCHĒ turns your phone's Color Filters on and the screen goes black and white until you leave the app. There is nothing to read and nothing to tap."* |
| 19 | The Note names where the kill switch lives and its shipped default, without asserting a current value (SAFE-02) | ✓ VERIFIED | **(signed)** *"the setting named ash_managed_color_filters, on its own line inside the Text action near the top of this shortcut… **It ships turned on.** …find that line, and change true to false."* Shipped-default claim, not a current-value claim. |
| 20 | The Note's Emergency Restore promise gains colour (SAFE-05) | ✓ VERIFIED | **(signed)** *"If a run has left your screen dim, your media volume down, or your screen in black and white, Emergency Restore is what puts them back."* Extended, not replaced. |
| 21 | `src/CONFIG-BLOCK.md` stops asserting two contradictory things about Ash; the historical paragraph is RETAINED with a pointer (AUDIT-02) | ✓ VERIFIED | Corrected at **five** sites (four planned + one found by an independent sweep — the header cross-reference naming BD-01 instead of BD-01-R2): `:3`, `:91`, `:93`, `:139` (new `## Field reference` row for the kill switch), and the changelog entry at `:164`. Historical BD-01 paragraph retained at `:95`. `docs/CAPABILITY-DECISIONS.md` BD-01-R2 exists at `:225`. |
| 22 | The Note and Config literals were edited through the guarded plist round trip; offsets survive (AUDIT-02) | ✓ VERIFIED | See finding **F-1** for the count question. **(signed)** I ran `plist_text_edit.assert_offsets_match` over **every** `WFTextTokenString` in both recovered payloads: **0 failures of 1115 (Core) / 1123 (Aware)**. `docs/note_identity_check.py` exits 0. |
| 23 | `src/CONFIG-BLOCK.md` is the MIRROR; both it and the live literal updated in the same commit | ✓ VERIFIED | `029d856` touches `src/CONFIG-BLOCK.md`, `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` together. `docs/retired_clause_check.py` (which mechanically asserts mirror↔fork agreement) exits 0. |
| 24 | Both forks re-signed under exact display names, manifest rows refreshed with real bytes and hashes, `manifest_check.py` green (CIRC-02) | ✓ VERIFIED | Filenames are `PROSOCHĒ — Nine Circles — Core.shortcut` / `— Aware.shortcut`, **no suffix**. SHA-256 on disk matches the values recorded in `14-UAT.md` byte-for-byte (`c359bbe2…` / `bd269b0c…`). `docs/manifest_check.py`: *"passed (6 rows verified against disk)"*. **Decrypted action lists are identical to `src/` action-for-action in both forks** — so the signed artifact is the build, not a stale carry-over. |
| 25 | The ROADMAP's Phase 14 prose is corrected (CIRC-02) | ✓ VERIFIED | The goal block now describes the unconditional single-insertion design, states *"There is no snapshot, no capture, no marker of who changed it and no persist-before-apply ordering"*, cites the superseded paragraph by where it lived, and carries a `What shipped (2026-08-19)` block. The `⚠ SCOPE RESET` banner is retained as the record. |
| 26 | Backlog phase 999.3 is retired (AUDIT-02, D-14-03) | ✓ VERIFIED | `.planning/ROADMAP.md:236` — *"RETIRED 2026-08-19 (was BACKLOG)"* with a six-row step-accounting table (steps 1/2/4/5/6 complete, 3 n/a) and closing evidence. |
| 27 | The kill switch's shipped value is unchanged (`true`); this plan changed no behaviour | ✓ VERIFIED | **(signed)** `"ash_managed_color_filters": true` in the Config literal of both forks. `src/CONFIG-BLOCK.md:164` records *"the fenced literal above is byte-identical to what it held before this plan"*. |

**Structural score: 27/27 verified.**

### Observable Truths — `verification: backstop` (ABSTAINED, per the honest-verifier protocol)

These are the truths the planner deliberately tagged non-inferable/device-gated. Symbol
presence plus wiring is **not** explicit evidence for a backstop truth, so each is recorded as
`insufficient_spec` and routed to human verification rather than absorbed into the score.

| #  | Truth | Status | Reason |
|----|-------|--------|--------|
| B1 | The screen actually turns black and white when the Circle fires on a real iPhone (CIRC-02) | ⚠️ ABSTAINED `insufficient_spec` | Environmental action of the same class as `Set Brightness`, which is measured to fail outright on a simulator. `.claude/CLAUDE.md` §9 "Rung 2's ceiling". |
| B2 | Colour actually comes back at CLOSE, and through Emergency Restore after a force-quit (SAFE-05) | ⚠️ ABSTAINED `insufficient_spec` | The highest-value unrun observation in the phase. Emergency Restore has never been tapped on a device in any phase. |
| B3 | The AX action imports and runs on iOS 26 with no unfilled-parameter error (SAFE-01) | ⚠️ ABSTAINED `insufficient_spec` | Signing is measured unaffected; import and run are device-gated. Compounded by F-3 (no `UUID` key). |
| B4 | The edited Note literal renders correctly on a real device after the guarded round trip (SAFE-02) | ⚠️ ABSTAINED `insufficient_spec` | Offsets verified structurally; rendering is device-gated, and `com.apple.mobilenotes` is absent from the simulator. |
| B5 | A user actually reads the disclosure and acts on it before Circle 2 fires (SAFE-02) | ⚠️ ABSTAINED `insufficient_spec` | Disclosure is the only available mitigation and its effectiveness is not measurable from here. |
| B6 | The enumerated residue is stable across a future Shortcuts Playground plugin update (AUDIT-02) | ⚠️ ABSTAINED `insufficient_spec` | The bundled snapshots live outside this repository. The checker turns the event into a loud failure, but cannot predict it. |
| B7 | The five unclassified spec-less edges (CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02) | ⚠️ ABSTAINED `insufficient_spec` | Surfaced by the planner rather than dismissed. No verifier evidence resolves them. |

**Score: 27/34 truths verified; 7 abstained as `insufficient_spec` (all `verification: backstop`).**

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `tools/build_state_engine.py` | `set_color_filters()`, rewritten `ash()`, off leg in `restore_managed_settings()`, guard registrations | ✓ VERIFIED | `:514` emitter, `:678-750` `ash()`, `:649` off leg, `:2710` + `:4738` guards. All wired and rendered. |
| `docs/phase5_self_check.py` | Asymmetric Color Filters assertion | ✓ VERIFIED | Exits 0. `EXPECTED_COLOR_FILTER_SITES = 15`; twin-absence assertion retained. |
| `docs/environmental_restore_check.py` | Fourth census row with derivation | ✓ VERIFIED | Exits 0. `EXPECTED_SITES[COLOR_FILTERS] = 15` with a 25-line derivation comment that explicitly flags the *different shape* from the three rows above it. |
| `docs/gate_a_residue_check.py` | New; mechanical two-family waiver, bidirectional | ✓ VERIFIED | 330 lines. Exits 0. Both negative controls fire (see truth 12). |
| `.claude/CLAUDE.md` | Amended gate-A clause | ✓ VERIFIED | Clause + Recommended-Stack row `:348` both amended; gate B and both anti-pattern rows intact. |
| `docs/BUILD-NOTES.md` | `DEV-08` deviation entry | ✓ VERIFIED | §5 `DEV-08` at `:269`, deviation-table row at `:466`, validate line at `:128` amended by pointer. |
| `.claude/skills/spike-findings-prosoche/{SKILL.md, references/evidence-and-probes.md}` | Gate-A obligation updated | ✓ VERIFIED | Both name `python3 docs/gate_a_residue_check.py`. |
| `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` | Generated, not hand-edited | ✓ VERIFIED | 4396 / 4530 actions. Byte-identical to the decrypted signed payloads' action lists. Regenerated after the provenance ancestor check (`git merge-base --is-ancestor 7ca8ebb… HEAD` → exit 0, re-run and confirmed). |
| `src/CONFIG-BLOCK.md` | Contradiction removed, history retained | ✓ VERIFIED | Five sites corrected; historical paragraph retained with pointer. |
| `docs/CAPABILITY-DECISIONS.md` | BD-01-R2 | ✓ VERIFIED | `:225`, resting on three decrypted donors. |
| `artifacts/shortcuts/MANIFEST.md` | Six rows refreshed; historical gate-A cells superseded by pointer | ✓ VERIFIED | Top block owns the table; five historical cells pointered. |
| `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Core,Aware}.shortcut` | Re-signed, exact display names | ✓ VERIFIED | 235369 / 241805 bytes; SHA-256 matches `14-UAT.md`; both decrypt cleanly. |
| `.planning/ROADMAP.md` | Goal prose corrected; 999.3 retired | ✓ VERIFIED | Both survive at HEAD after the `fe30bf1` revert. |
| `14-UAT.md` | Authored; every outcome blank; blocked | ✓ VERIFIED | `status: blocked`, `blocked_on: DIST-03`. Six tests, thirteen `outcome:` fields, **all empty**; results table entirely blank with an explicit *"Every cell above is blank because no device test has been run."* |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `ash()` | every `primitive_dispatch()` rendering | The `"Black and White"` dispatch tuple (`:1152`) | ✓ WIRED | 11 renderings, **one distinct action shape across all 11** — a site-by-site edit would have produced more than one. |
| off leg in `restore_managed_settings()` | `close_pipeline()`, `manual_emergency_restore()`, `ice_expiry()`, `live_ice_redirect()` | One insertion, four call sites | ✓ WIRED | All four measured in the generator and in both signed artifacts. No restore path is missing it. |
| `safety.ash_managed_color_filters` (Config literal) | numeric `> 0` gate in `ash()` | `config()` + `if_block(..., 2, number=0)` | ✓ WIRED | Key present in the shipped Config literal; read at 11 sites; gate is numeric, not a string compare. |
| AX identifier | `VERIFIED_PARAMETER_KEYS` | `verify_parameter_keys()` | ✓ WIRED | Mapped to `{"state"}` — an `operation` write is now a build failure rather than a shipped fabrication. |
| derived AX census | `docs/environmental_restore_check.py` `EXPECTED_SITES` | census row | ✓ WIRED | Present with derivation; a silent loss of sites turns the checker red. |
| Note kill-switch disclosure | the Config read emitted by `ash()` | user-facing prose | ✓ WIRED | The Note names the exact key `ash_managed_color_filters` that the emitted `getvalueforkey` reads. |
| signed filename | the user's existing Personal Automations | library display name | ✓ WIRED | No suffix, no rename. |

---

## Data-Flow Trace (Level 4)

| Artifact | Data | Source | Real data? | Status |
|----------|------|--------|-----------|--------|
| `set_color_filters()` | `state` | Python literal `1 if on else 0` | Yes — bare plist `int`, type-confirmed in both signed payloads | ✓ FLOWING |
| `ash()` gate | `Ash Managed Color Filters` | `getvalueforkey` over the live Config dictionary, not a constant | Yes | ✓ FLOWING |
| Note disclosure | prose | preserved literal inside the artifact, edited through `plist_text_edit` | Yes — present in both decrypted payloads | ✓ FLOWING |
| `gate_a_residue_check.py` | validator output | shells out to the real validator | Yes — measured 30 permitted lines per fork | ✓ FLOWING |

---

## Behavioural Spot-Checks

| Behaviour | Command | Result | Status |
|-----------|---------|--------|--------|
| All repo checkers green | `for f in docs/*.py; do python3 "$f"; done` | 14/14 exit 0 | ✓ PASS |
| Gate-A waiver fires on a GROWN residue | `gate_a_residue_check` with the `UA*` twin swapped in at one site | `AssertionError: … 1 line(s) OUTSIDE the enumerated waiver` | ✓ PASS |
| Gate-A waiver fires on a SHRUNK residue | `gate_a_residue_check` with one AX action deleted | `AssertionError: … 28 line(s), expected exactly 30 … A SMALLER residue means emitted AX sites DISAPPEARED` | ✓ PASS |
| Shipped artifacts decrypt and match source | `aea decrypt` → `aa extract` → `plutil`, then compare `WFWorkflowActions` | `True` for both forks | ✓ PASS |
| Every shipped text token's offsets are sound | `plist_text_edit.assert_offsets_match` over both payloads | 0 failures / 1115 Core, 0 / 1123 Aware | ✓ PASS |
| Build provenance | `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0 | ✓ PASS |
| The screen actually goes greyscale | — | — | ? SKIP — device-gated (B1) |
| Colour actually returns | — | — | ? SKIP — device-gated (B2) |

**No simulator run was attempted, deliberately.** `.claude/CLAUDE.md` §9 measures `Set Brightness`
as failing outright on a simulator and puts real-hardware environmental behaviour above rung 2's
ceiling; a simulator observation of this action would be worth nothing and would risk being
mistaken for evidence.

---

## Probe Execution

No `scripts/*/tests/probe-*.sh` exists in this repository and no plan declares one. The
project's equivalent instruments are the `docs/*.py` checkers, all executed above.

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| CIRC-02 | 14-01, 14-03 | Ash applies the audited visual-salience reduction, or its documented fallback | ✓ SATISFIED structurally / ? device-gated behaviourally | 15 AX sites per fork; alert deleted; kill switch as the documented fallback. Behaviour is B1. |
| SAFE-01 | 14-01 | Environmental change captured and durably persisted before applied, and always restored | ✓ SATISFIED, with the reading recorded as a deviation | The capture clause is **structurally inapplicable** to a two-valued setting; the executor recorded this ruling in `ash()`'s docstring and in 14-01-SUMMARY as flagged assumption A1, and deliberately did **not** number it `D-14-xx` to avoid claiming user authority. The compliant substitute is the unconditional off leg reachable from the panic button. Sound and correctly labelled. Behaviour is B3. |
| SAFE-02 | 14-01, 14-03 | Volume never increased, no startling output | ✓ SATISFIED | `setvolume = 15` unmoved, every write `WFVolumeSetting = "Media"` (asserted by `environmental_restore_check`). The assistive-configuration half is carried by the Note disclosure. |
| SAFE-05 | 14-01, 14-03 | Emergency Restore restores brightness, volume **and colour** | ✓ SATISFIED structurally / ? device-gated behaviourally | Colour is now genuinely in the restore path, at all four sites, first and ungated. Requirement text at `.planning/REQUIREMENTS.md:127` explicitly names colour. Behaviour is B2. |
| AUDIT-02 | 14-02, 14-03 | Grayscale capability resolved to a go/no-go decision with a documented fallback | ✓ SATISFIED | BD-01-R2, DEV-08, the amended gate-A clause, the mechanical residue checker, the CONFIG-BLOCK correction, 999.3 retirement. |

**Orphaned requirements: none.** `.planning/REQUIREMENTS.md` maps no additional IDs to Phase 14
(it contains no "Phase 14" mapping at all), so no requirement was expected of this phase and
left unclaimed. The traceability table's `Phase 1`/`Phase 5` rows are the *original* satisfaction
points and are pre-existing, not a phase-14 gap.

---

## Prohibitions

Every prohibition in all three plans is a plain string (no `{statement, verification}` tiering),
and every one is mechanically checkable. All were checked; **none is flagged**.

| Prohibition | Status | Evidence |
|-------------|--------|----------|
| MUST NOT emit `state = 2` for Off | ✓ HELD | **(signed)** states are exactly `{0: 4, 1: 11}`. Nothing outside `{0, 1}`. |
| MUST NOT emit the `UA*` macOS twin, MUST NOT delete the checker half asserting its absence | ✓ HELD | **(signed)** 0 `UniversalAccess` actions in either fork. `phase5_self_check.py:167` assertion intact. |
| MUST NOT write `operation` on either leg | ✓ HELD | **(signed)** parameter keys are exactly `('state',)` at all 15 sites in both forks. `VERIFIED_PARAMETER_KEYS[COLOR_FILTERS] = {"state"}` now makes an `operation` write a build failure. |
| MUST NOT wrap the integer in a text-token envelope | ✓ HELD | **(signed)** `type(state)` is `int` at all 30 sites across both forks. |
| MUST NOT use the Toggle form | ✓ HELD | No `operation: "toggle"` anywhere. |
| MUST NOT synthesise an `AppIntentDescriptor` | ✓ HELD | The validator still reports the missing-descriptor family 15× per fork — direct proof none was synthesised. |
| MUST NOT add a third `settings_snapshot` group or touch `SNAPSHOT_SEED` / `seed_settings_snapshot()` / `clear_snapshot()` / `verify_state_seed()` | ✓ HELD | Two groups in `SNAPSHOT_SEED` and in both shipped bootstrap literals. The superseded snapshot design was **not** reinstated. |
| MUST NOT add an ownership marker, changed-by leaf or `save_state()` to `ash()` | ✓ HELD | `ash()` is 17 lines of body; none present. |
| MUST NOT gate the off leg on anything | ✓ HELD | **(signed)** no conditional between the restore comment and the off action at any of the 4 sites. |
| MUST NOT add an alert, notification, menu or acknowledgement to `ash()` | ✓ HELD | One shape across all 11 apply sites; no such action in it. |
| MUST NOT register the identifier in `verify_capture_persistence()` / `verify_restore_gates()` | ✓ HELD | `COLOR_FILTERS` occurs at only 5 places in the generator; neither function is one. |
| MUST NOT change the three pinned counts or the 15/4 coercion split | ✓ HELD | 15 / 15 / 22 exact. |
| MUST NOT hand-edit the two `src/*.xml` | ✓ HELD | Signed payload action lists are identical to `src/`; both regenerated after the provenance check. |
| MUST NOT carry forward the superseded per-fork AX figure | ✓ HELD | Derived, and the derivation (not just the number) is written into three checkers. |
| MUST NOT run either generator without the provenance ancestor check | ✓ HELD | Ancestor check re-run here: exit 0. Recorded in the MANIFEST and both summaries. |
| MUST NOT weaken gate B or the two anti-pattern rules | ✓ HELD | Both rows intact at `.claude/CLAUDE.md:363-364`; gate B section substantively unchanged. |
| MUST NOT let the residue checker pass on a shrunk residue | ✓ HELD | Negative control run by this verifier — it fails. |
| MUST NOT edit dated historical records; supersede by pointer; cite rather than restate | ✓ HELD | Five MANIFEST cells retained unedited with pointers; CONFIG-BLOCK's historical paragraph retained; superseded wording cited by where it lived throughout. |
| MUST NOT chain the raw validator into any `&&` success condition | ✓ HELD | No such line added anywhere in the phase diff. |
| MUST NOT rename either fork or add a suffix | ✓ HELD | Exact display names, no suffix. |
| MUST NOT edit manifest rows without re-signing | ✓ HELD | `manifest_check.py` green against real bytes and hashes on disk. |
| MUST NOT record any device test as passed, or infer a device outcome from a structural check | ✓ HELD | **This is the prohibition most at risk in a phase this structurally clean, and it held.** All 13 `outcome:` fields blank, results table blank, `status: blocked`, and an explicit *"Do not record 'no error appeared' as a pass."* |
| MUST NOT assert a current value for the kill switch in the Note | ✓ HELD | *"It ships turned on"* — a shipped-default claim. |
| MUST NOT change the kill switch's shipped value | ✓ HELD | `true`, unchanged. |
| MUST NOT weaken the Note's Emergency Restore promise | ✓ HELD | Extended with colour, not replaced. |
| MUST NOT delete the historical reversed-decision paragraph in the config mirror | ✓ HELD | Retained at `src/CONFIG-BLOCK.md:95`. |

---

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | — | — | **None.** `git diff 0a3b017 HEAD \| grep '^+' \| grep -E 'TBD\|FIXME\|XXX'` returns nothing: **no new debt marker was introduced by this phase.** The `TBD` occurrences in `.planning/ROADMAP.md` are pre-existing plan-list placeholders for Phases 15–19 and are untouched here. No `TODO`, `HACK` or `PLACEHOLDER` in any modified `.py`. |

---

## Findings

### F-1 — WARNING (documentation accuracy): the "238 text tokens" baseline WAS reproducible; the summary says it was not

`14-03-SUMMARY.md` records the brief's 238-token-per-fork baseline as *"not reproducible under
any counting basis measured here"* and adopts 249 instead. **The 238 figure is exactly
reproducible**, under the very counting basis the executor itself adopted — `WFTextActionText`
parameters serialized as `WFTextTokenString`:

| Commit | What it is | Core | Aware |
|---|---|---:|---:|
| `953ff1e` | the phase-14 scope-reset commit — **pre-wave-1** | **238** | **238** |
| `ca0bbea` | plan 14-01's `feat` commit | 249 | 249 |
| `029d856` | plan 14-03's Note-disclosure commit | 249 | 249 |
| `9714e66` | plan 14-03 complete | 249 | 249 |

The delta is **exactly +11 per fork**, which is exactly the 11 `primitive_dispatch()` renderings
of `ash()`'s new `config()` read, each contributing one `Get Text` token string. 238 was the
*pre-14-01* baseline; the executor measured from a base that was already post-14-01.

**The invariant that actually matters held, and I confirmed it independently:** the count is
unchanged across 14-03's edit (249 → 249), and every token in both *signed* artifacts passes
`assert_offsets_match` (0 failures of 1115 Core / 1123 Aware). So this is a wrong *label* on a
correct measurement, erring toward under-claiming rather than over-claiming — the honest
direction. **Recommended correction, non-blocking:** the record should read "238 was the
pre-14-01 baseline; the +11 delta is `ash()`'s config read", not "unreproducible". An
unexplained delta invites a future reader to treat 249 as arbitrary.

### F-2 — no finding: the accepted risk is recorded as ACCEPTED, nowhere as mitigated

I checked every artifact that touches the pre-existing-Color-Filters user. None implies the risk
is handled:

- `src/CONFIG-BLOCK.md:139` — *"**accepted and backlogged, not mitigated**"*, verbatim.
- `14-UAT.md` safety preamble — *"This is accepted and backlogged, not mitigated"*, plus an
  instruction that a tester who is such a user must record and restore their own configuration
  **by hand**, because *"The product will not do it for them."*
- The shipped Control Room Note, in both forks — *"iOS gives PROSOCHĒ no way to read what your
  Color Filters setting was, so it cannot put your own setting back afterwards. It turns them
  off."*
- Backlog item present at
  `.planning/todos/pending/2026-08-19-ash-void-circle-when-user-already-uses-grayscale.md`.

The Note's honesty here is notable: it states the harm before it states the remedy.

### F-3 — INFO (self-reported discrepancy 1, resolved): no `UUID` key on the emitted AX action

The emitted action carries `state` only. The executor's house-style defence **is verified
against the generator**: `action()` (`:157`) emits identifier + parameters and nothing else, and
`set_brightness` / `set_media_volume` (`:492-499`) likewise omit `UUID`; `UUID=` is passed
explicitly only at sites whose output a later action references (~60 such sites). No action
references the Color Filters output. So the omission is consistent, deliberate and correct by
this codebase's own convention.

Stated honestly, though: all three donors **do** carry a `UUID`, and this is a structural key
not covered by donor evidence in the omitted direction. It is a real (small) unproven surface,
and it rides on backstop truth **B3** — the device import-and-run test — rather than being
independently closed. Not a blocker; do not read it as fully settled either.

### F-4 — no finding (self-reported discrepancy 3, resolved): five MANIFEST gate-A cells left intact is HONEST, not merely defensible

Wave 2 predicted four; the executor found five and left each intact with a supersession pointer.
This is honest rather than technically defensible, for three checkable reasons:

1. The top block **states the count out loud** — *"Five sentences in the blocks below record that
   one fork or both passed gate A clean"* — so a reader is not left to discover them.
2. I opened all five (`:68`, `:284`, `:332`, `:371`, `:391`) and each carries an inline
   *"gate-A status superseded, see the 2026-08-19 block at the top of this file"* pointer. None
   is a bare stale claim.
3. Each **was** a true measurement of the build it describes, and the project's own recorded
   convention — reaffirmed in `14-02`'s prohibitions and in `src/CONFIG-BLOCK.md`'s header — is
   that rewriting a dated provenance measurement corrupts the record. Rewriting them would have
   been the *dishonest* option.

The top block also explicitly asserts it *"owns the table's six rows"*, so there is no ambiguity
about which measurement describes the shipped artifacts.

### F-5 — no finding (self-reported discrepancy 5, resolved): the ROADMAP checkbox revert is clean

`fe30bf1` changes exactly three lines of `.planning/ROADMAP.md`, all `[x]` → `[ ]` on the plan
list. Both plan-mandated edits survive at HEAD and I verified each directly: the goal-prose
correction (Phase 14 goal block now describes the shipped unconditional design) and the 999.3
retirement (`:236`). Orchestrator-owned state was correctly handed back.

### F-6 — no finding (self-reported discrepancy 4, resolved): the disclosure's two omissions are both load-bearing

- **No Circle number.** Verified against the shipped Config literal: `Black and White` sits at
  position **2** under `Classic`, **3** under `BlackMirror`, **1** under `Ambient`. Naming a
  number would have been false for two of three sequences. The Note instead says *"Which Circle
  it lands on depends on the sequence you chose, so it is not always the same depth."*
- **No fork name.** Verified in `tools/build_sentient.py`'s `fix_fork_strings()`: it asserts
  **exactly 2** occurrences of the Core display name in the Note body (the two Run Shortcut
  targets) and aborts the Aware build on a third. A disclosure naming the fork would have broken
  the Aware build. The constraint is real, not a rationalisation.

---

## Human Verification Required

Seven items, all `insufficient_spec` abstentions on `verification: backstop` truths. Full
detail in the frontmatter `human_verification` block. In priority order:

1. **Force-quit mid-intervention → Emergency Restore returns colour.** The highest-value unrun
   observation in the phase, and the one that answers a debt older than it: Emergency Restore has
   never been tapped on a device.
2. **The screen actually goes black and white, silently, when the Circle fires.**
3. **Colour returns on CLOSE, on Ice expiry and on the live-Ice redirect.**
4. **Both forks import and the action runs with no unfilled-parameter dialog** (carries F-3).
5. **The kill switch set to `false` leaves Color Filters untouched and the Circle fires a blank.**
6. **The edited Note literal renders correctly on device.**
7. **Maintainer judgement:** accept the plugin-snapshot-stability and unclassified-edge
   backstops as surfaced-not-dismissed, or commission held-out checks.

All seven are already authored as `14-UAT.md`'s six tests plus its device-availability block.
`14-UAT.md` is `status: blocked`, `blocked_on: DIST-03`, and DIST-03 was measured at execution
time as `tunnelState: unavailable`, `transportType: none`. **No new instrument is needed — this
phase needs a phone.**

---

## Gaps Summary

**No gaps.** Nothing is missing, stubbed, unwired, hollow or contradicted. Every structural
must-have across all three plans holds when measured against the *decrypted signed artifacts*
rather than the source, every prohibition holds, all 14 checkers exit 0, the new gate-A residue
checker fails correctly in both directions under negative controls I ran myself, and no new debt
marker was introduced.

The phase is `human_needed` for exactly one reason, and it is the right one: **seven truths were
tagged `verification: backstop` by the planner because they are device-gated or non-inferable,
and no explicit evidence exists for any of them.** Per the honest-verifier protocol, symbol
presence plus wiring is not explicit evidence for a backstop truth, so each abstains rather than
inheriting a pass from the (excellent) structure beneath it. Promoting any of them on the
strength of the structural work would be precisely the confident false-pass the protocol exists
to prevent.

One recommended non-blocking correction: **F-1**, the "238 tokens unreproducible" note, which is
a wrong label on a correct measurement and should be replaced with the actual explanation
(238 = pre-14-01 baseline; +11 = `ash()`'s config read).

---

_Verified: 2026-08-19T01:56:29Z_
_Verifier: Claude (gsd-verifier)_
