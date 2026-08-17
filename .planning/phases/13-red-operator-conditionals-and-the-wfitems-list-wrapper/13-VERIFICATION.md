---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
verified: 2026-08-17T23:10:00Z
status: gaps_found
score: 23/27 must-haves verified
behavior_unverified: 2
overrides_applied: 0
gaps:
  - truth: "The refuted counts are closed as a CLASS: a whole-tree sweep of .planning/ and docs/ finds no surviving assertion of 14 defective conditional sites or 2 WFItems instances outside the two deliberate exemptions (the closed todo and this phase's own planning directory)"
    status: failed
    reason: "The declared sweep is clean over its six chosen literals (independently re-run: 0 survivors). But nine untombstoned assertions of the refuted 14-site count survive in a THIRD location that is neither exemption, because their wording does not match any of the six literals. The file is the closed debug session the phase goal names by name."
    artifacts:
      - path: ".planning/debug/resolved/open-routing-sequence-error.md"
        issue: "Lines 810, 931, 1037, 1044, 1197, 1203, 1270, 1277, 4667 assert 'THE 14 WFConditionalActionString SITES … ARE UNCHANGED / STILL UNRESOLVED' and 'WFConditionalActionString at 14 sites … UNRESOLVED'. No REFUTED or SUPERSEDED marker within ±12 lines of any of them. Phrasings are 'THE 14 WFConditionalActionString SITES' and 'at 14 sites', which the declared literals ('the 14 sites', '14 `WFConditionalActionString` sites') do not match."
    missing:
      - "Either a single dated REFUTED banner at the head of .planning/debug/resolved/open-routing-sequence-error.md (or per-site annotations) closing the 14-site count for that file"
      - "Or an explicit third exemption for .planning/debug/resolved/ recorded in docs/BUILD-NOTES.md §28 with its rationale, so the class-closure claim matches what was actually swept"
  - truth: "13-UAT.md is cold-runnable by someone with no memory of this phase, and the signed-artifact provenance record states what actually shipped"
    status: failed
    reason: "CR-01's re-ship changed both signed artifacts, both sources and both dated archives. artifacts/shortcuts/MANIFEST.md and 13-REVIEW-FIX.md were updated; 13-UAT.md and docs/BUILD-NOTES.md §28's plan-13-04 subsection were not. The UAT's mandatory re-import precondition and its SHA-256 self-check now name a build that does not exist on disk, so a cold reader following it would refuse to test the artifact that actually ships."
    artifacts:
      - path: ".planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-UAT.md"
        issue: "Header rows 18-20 name commit 737ce07 and artifacts 234830 bytes / fe1bafdf… (Core) and 239184 bytes / bd1264d5… (Aware). Disk holds 233802 / b07497ba… and 237842 / 212598cf…. Line 31 makes importing that exact build mandatory ('you must not test an install that predates it'); line 27 offers a SHA self-check that will now reject the correct build. Lines 48, 72, 103, 271, 331 still state the superseded 660-wrapped / 6-bare census."
      - path: "docs/BUILD-NOTES.md"
        issue: "§28's 'Gate B advisory read and signed-artifact provenance (plan 13-04)' subsection carries no supersession marker: it records source digests 99388cad…/d01154b3… as current (disk: c6270691…/709f53f8…), signed digests fe1bafdf…/bd1264d5… with sizes 234830/239184, archives Core-184943.xml/Aware-184954.xml (MANIFEST names the 2204xx pair), and a decrypt-verification table reading '660 wrapped / 6 bare' for the shipped containers (measured on the shipped containers here: 616 wrapped / 50 bare). Its closing Phase-19 instruction reads 'The artifact to import is … at SHA-256 fe1bafdf…; anything else is the wrong build.' §28's own three-stage table 400 lines earlier says what ships is 616/50, so the section contradicts itself. MANIFEST.md handles the identical supersession correctly and explicitly — the pattern exists, it was just not applied here."
    missing:
      - "Refresh 13-UAT.md's header (commit, both sizes, both SHA-256s) and its 660/6 census statements to the shipped build"
      - "Add a SUPERSEDED marker to docs/BUILD-NOTES.md §28's plan-13-04 subsection in the form MANIFEST.md already uses, and correct the Phase-19 re-import digest"
deferred:
  - truth: "A wrapped WFItems row renders non-blank on device, and Item At Index over a wrapped List returns the intended row"
    addressed_in: "Phase 19"
    evidence: "ROADMAP Phase 19: 'Device UAT — nine Circles and sequence switching — The intervention layer converts from structurally-proven to actually-working on real hardware'; docs/BUILD-NOTES.md §28 assigns assumptions A3, A4 and A5 to Phase 19 UAT by name"
  - truth: "mirror_templates() binds facts by placeholder ordinal, so nine Mirror templates name the wrong fact"
    addressed_in: "todo (deferred by decision, CR-03)"
    evidence: ".planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md, commit d056f9a — pre-existing, outside both of this phase's defect families, cold-runnable repro recorded"
behavior_unverified_items:
  - truth: "A wrapped WFItems row renders non-blank on device — the whole point of the family-2 fix"
    test: "Re-import the shipped Core artifact on an iOS 26.x iPhone, trigger a Mirror at any Circle, and read the alert body"
    expected: "A non-empty, fact-bearing Mirror body; an empty or whitespace-only body means the wrapper did not take effect"
    why_human: "Row rendering is runtime behaviour. Neither validator gate, the ToolKit catalog, nor the AEA1 decrypt can see it — the decrypt recovers the same structurally-perfect plist. The simulator cannot import a signed .shortcut and lacks com.apple.mobilenotes. Device-gated; DIST-03 is open and `xcrun devicectl list devices` reports 'No devices found.' (re-run here)."
  - truth: "Item At Index selection over a WRAPPED List returns the same row content it returned over an unwrapped List (declared `verification: backstop` in 13-01)"
    test: "On device, drive Mirrors at Circle 3, 7 and 9 and confirm the body matches the template for that Circle, not a neighbouring row"
    expected: "The selected row's rendered text corresponds to the Circle chosen"
    why_human: "No donor chains a wrapped List into getitemfromlist, so extraction semantics over a wrapped array are unobserved. The file-level half IS verified here (row count/order unchanged at [6]+[10]*66, WFItemSpecifier and WFItemIndex untouched, no arithmetic and no uid() introduced) — the runtime half is device-only and abstains rather than passing on structure."
unverified_prohibitions:
  - statement: "MUST NOT fabricate a parameter shape the donors do not settle — in particular MUST NOT encode any WFItemType value other than 0"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "Measured: the only WFItemType value present in either fork is 0 (616 rows each). verify_list_item_wrappers() asserts the KEY's presence and never its value (source read). _list_row(), BD-08, axis 8 and assumption A2 each state the non-0 values are deliberately unaudited."
    flag: "unverified-prohibition — human review recommended"
  - statement: "MUST NOT silence a build guard or a docs/*.py checker to make the suite green"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "git diff 698ab99..HEAD touches no docs/*.py file. Both guards were widened, not weakened: ten synthetic mutations probed here all raise SystemExit, and both guards return cleanly on the unmutated artifact. AST: zero ast.Assert nodes in either guard or in _list_row(); all raises are SystemExit."
    flag: "unverified-prohibition — human review recommended"
  - statement: "MUST NOT record a device-evidence verdict that was not observed on a device"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "`xcrun devicectl list devices` re-run here returns 'No devices found.' 13-UAT.md carries status: blocked, blocked_on: DIST-03, and every outcome field is blank. No simulator run or decrypt inference is entered as device evidence anywhere in §28 or the UAT."
    flag: "unverified-prohibition — human review recommended"
---

# Phase 13: Red-operator conditionals and the WFItems List wrapper — Verification Report

**Phase Goal (as corrected by this phase's own research):** Settle two defect families carried
unchanged through every cycle of the closed `open-routing-sequence-error` session — the
`WFConditionalActionString` conditional operand shape (measured as already correct → pin, do not
fix) and the `WFItems` List row wrapper (real, 33× larger than recorded → fix by class) — with
build-time recurrence guards for both, sensitivity demonstrated, and the newly-confirmed axes
folded into `.claude/CLAUDE.md` in one pass.

**Verified:** 2026-08-17
**Status:** gaps_found
**Re-verification:** No — initial verification (post code-review-fix state, HEAD `ac4d3ec`)

Every figure below was re-derived independently against HEAD with `plistlib`, `git`, the
validator, the AEA1 decrypt recipe and direct guard probes. No number is taken from a SUMMARY.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Every attachment-bearing List row is wrapped `{WFItemType: 0, WFValue: <WFTextTokenString>}`; zero raw `WFTextTokenString` rows in any `WFItems` array, both forks | ✓ VERIFIED | Measured both sources: 67 List actions, 666 rows, **616 wrapped / 50 bare / 0 other / 0 missing `WFItemType` / 0 wrapped-but-attachment-free**, identical per fork |
| 2 | Literal rows stay bare strings — the donor two-kind rule, not a blanket sweep | ✓ VERIFIED | 50 bare rows = 6 exit names + 44 attachment-free Mirror templates. Per-array shapes measured: `1×(0 wrapped, 6 bare)`, `22×(10,0)`, `44×(9,1)` — the 44 are the donor-observed **mixed** array |
| 3 | `verify_list_item_wrappers()` raises `SystemExit` (never `assert`) before the single write; message carries the prose cause, first five offenders as action/row pairs, and the total | ✓ VERIFIED | AST: 0 `ast.Assert`, 2 `SystemExit` raises. Call at `:4448` precedes the single `SOURCE.write_bytes()` at `:4472`. Message text read at source |
| 4 | The new guard is armed on BOTH forks at BOTH touch points | ✓ VERIFIED | AST over `tools/build_sentient.py`: `verify_list_item_wrappers` present in the `ImportFrom build_state_engine` names **and** as a bare `Expr(Call(Name))` statement. Same for `verify_conditional_action_string` |
| 5 | Both guards are sensitive to a synthetically reverted artifact, and non-vacuous on HEAD | ✓ VERIFIED | 10 mutations probed here, all 10 raise `SystemExit` (see Behavioural Spot-Checks). Both guards return cleanly on the unmutated HEAD action arrays |
| 6 | The rebuild is byte-idempotent | ✓ VERIFIED | Provenance ancestor check exit 0, then both generators re-run here: `git status --porcelain` empty, `shasum -c` OK on both sources |
| 7 | `_list_row()` is element-wise and total; per-action row counts are `[6] + [10]*66` | ✓ VERIFIED | Distribution measured `{6:1, 10:66}` per fork. Probes: `5`, `None`, an already-wrapped row and a `WFTextTokenAttachment` each raise `SystemExit`; a `str` passes through unchanged |
| 8 | Row offsets survive the wrapper unchanged (BMP-only strings; every `{p, 1}` key indexes a `U+FFFC`) | ✓ VERIFIED | 1056 attachment ranges checked per fork: 0 bad, 0 non-BMP rows. The wrapper nests the existing envelope by reference — no re-serialization |
| 9 | A wrapped row renders **non-blank on device** | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Structure present, wired and shipped; rendering is runtime-only. `xcrun devicectl list devices` → "No devices found." Device-gated, DIST-03 open |
| 10 | `Item At Index` over a WRAPPED List returns the same row content (declared `verification: backstop`) | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | File-level half verified (row count/order unchanged, `WFItemSpecifier`/`WFItemIndex` untouched, no `uid()` added). Runtime half unobserved by any donor — abstained, not passed |
| 11 | `verify_conditional_action_string()` carries a POSITIVE Donor-5 pin with its provenance docstring | ✓ VERIFIED | Source `:2499-2618`: asserts `WFTextTokenString` + `U+FFFC` in `Value.string` + non-empty `attachmentsByRange`; docstring cites `.planning/debug/Donor 5.shortcut` and states the pin repairs nothing |
| 12 | The pin passes non-vacuously: exactly 20 variable-bearing sites per fork, zero offenders | ✓ VERIFIED | Independently measured: Core 192 mode-0 slots / 20 variable-bearing / 172 literals; Aware 195 / 20 / 175. Condition split 19×code 4 + 1×code 99 in both. **0 offenders** — the ROADMAP's "14 defective sites" is refuted by my own measurement, not only by the SUMMARY's |
| 13 | No emission site was swept — `token()` and `if_block()` are unchanged, literal counts unchanged at 172 / 175 | ✓ VERIFIED | AST of both functions at `698ab99` vs HEAD: **identical**. Literal counts measured 172 / 175 |
| 14 | The raises are distinguishable, the ordering mask is recorded verbatim, and the chain was not reordered | ✓ VERIFIED | Three raises, each fired independently here against its own mutation with distinct text. §28 records the mask; the census raise is appended last by design |
| 15 | The Aware fork needed no new touch point for the extended guard, and that absence is recorded rather than inferred | ✓ VERIFIED | AST confirms both sites pre-exist; `tools/build_sentient.py:337-362` states the exception and its reason explicitly |
| 16 | `.claude/CLAUDE.md`'s numbered axis list runs 1–9, and the heading and `/ponytail` row name the same count | ✓ VERIFIED | Heading `:353` "the nine parameter-defect axes"; `/ponytail` row `:258` likewise; items 1–9 at `:375-453`; no site asserts seven or eight |
| 17 | Axis 8 states the two-kind rule, cites both donors by path, names the guard, and is stated as a CONTAINER defect distinct from axis 2 | ✓ VERIFIED | `:419-452`, including the post-CR-01 correction "Discriminate on attachment-bearing-ness, NOT on Python type" and the `WFItemType`-beyond-0 boundary |
| 18 | Axis 9 states the compound/scalar reader rule, names the four `COMPOUND_STATE_KEYS` members and the guard | ✓ VERIFIED | `:453-468`; the four names match `tools/build_state_engine.py:3650-3653` exactly, with the dynamic fifth recorded beside the frozenset |
| 19 | Axis 7 is extended with the `pending_exit` container/leaf pattern | ✓ VERIFIED | `:407-418` — seed the container as a permanent invariant, write/clear only leaves, gate on is-not-sentinel or `> 0`, never condition-100 over the container |
| 20 | `docs/CAPABILITY-DECISIONS.md` carries BD-07 and BD-08 with their unsettled boundaries intact | ✓ VERIFIED | BD-07 `:869`, BD-08 `:936`, both in the ToC. BD-08 carries the post-CR-01 census, the CR-01 correction, the `WFItemType`-unaudited boundary, and CR-02's explicit retraction of the numeric-slot "confirmation" |
| 21 | `docs/BUILD-NOTES.md` carries a Phase 13 section recording the three decrypts, both measured inventories, the refutation, the verbatim guard texts, the ordering mask and every open assumption | ✓ VERIFIED | §28 `:2365-2843`: decrypt table, three-stage family-2 table, refutation table, both guards' verbatim `SystemExit` texts, the mask subsection, and assumptions A1–A5. *(See gap 2 for the stale plan-13-04 subsection inside the same section.)* |
| 22 | The ROADMAP prose and milestone checklist state the measured figures, dated and attributed to donor evidence; HANDOFF is tombstoned at every asserting site; the todo is closed with a tombstone | ✓ VERIFIED | ROADMAP `:36` and `:574-612` (dated correction block). HANDOFF: `REFUTED` at `:255`, `:321`, `:339`, `:523` and `SUPERSEDED` at `:163` for the axis-6 tally — all five named sites, originals preserved. Todo now at `.planning/todos/completed/…` carrying its own tombstone |
| 23 | The refuted counts are closed as a CLASS across `.planning/` and `docs/` | ✗ FAILED | Declared six-literal sweep re-run here: **0 survivors** — that claim holds. A broader phrasing sweep finds **9 untombstoned assertions** of the 14-site count in `.planning/debug/resolved/open-routing-sequence-error.md`, a third location that is neither declared exemption. See gap 1 |
| 24 | Ship gate: canonical display names, six MANIFEST rows matching disk, 12/12 checkers, gate A clean, gate B one waiver per fork, decrypt-verified shipped shape | ✓ VERIFIED | All re-derived independently — see the tables below. Decrypted both containers: their `WFWorkflowActions` arrays are **byte-identical** to the corresponding source XML, and carry 616 wrapped / 50 bare per fork |
| 25 | `13-UAT.md` is cold-runnable, with an explicit BLOCKED branch leaving every result blank | ✗ FAILED | The BLOCKED branch and blank results hold (`status: blocked`, `blocked_on: DIST-03`). Cold-runnability does not: the header names a build that is not on disk and makes importing exactly it mandatory. See gap 2 |
| 26 | The device verdict is recorded as observed, not inferred | ✓ VERIFIED | `xcrun devicectl list devices` re-run here → "No devices found." UAT is BLOCKED with blank results; no simulator or decrypt inference is entered as device evidence |
| 27 | Interrupting or re-running the build/sign sequence cannot leave a half-written artifact | ✓ VERIFIED | Core: every `verify_*` precedes the single `SOURCE.write_bytes()` (AST + the failed-build digest evidence in §28). Aware: `tempfile.NamedTemporaryFile` + `os.replace` at `tools/build_sentient.py:405-408`. Re-run byte-idempotent (truth 6) |

**Score:** 23/27 truths verified (2 present, behavior-unverified; 2 failed)

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | A wrapped row renders non-blank, and `Item At Index` over a wrapped List returns the intended row | Phase 19 | ROADMAP Phase 19 goal; §28 assigns A3/A4/A5 to Phase 19 UAT by name |
| 2 | `mirror_templates()` ordinal fact binding (CR-03) | todo, deferred by decision | `.planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md` (`d056f9a`) — pre-existing, different defect class, cold-runnable repro |
| 3 | `WFNumberValue` integer-vs-string encoding and the 32 variable-valued sites (A5 / CR-02) | outstanding device UAT | BD-08 verdict `UNVERIFIED` on both axes with named owner; §28 A5 names the cheapest device witnesses |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `tools/build_state_engine.py` | `_list_row()`, wrapped `mirror_text()`, `verify_list_item_wrappers()`, extended `verify_conditional_action_string()` | ✓ VERIFIED | `_list_row` `:648-718` (total, content-discriminating), `mirror_text` `:721-730`, conditional guard `:2499-2618`, list guard `:2630-2726`; all three registered in `main()` `:4442-4460` |
| `tools/build_sentient.py` | Per-fork arming at both touch points | ✓ VERIFIED | Import `:23`, call `:384` (list guard); import `:19`, call `:365` (conditional guard). AST-confirmed |
| `src/PROSOCHE-Dumb.xml` | 67 List actions, 616 wrapped + 50 bare | ✓ VERIFIED | Measured exactly; gate A clean; 4346 actions |
| `src/PROSOCHE-Sentient.xml` | Same census after the fork | ✓ VERIFIED | Measured exactly; gate A clean; 4414 actions |
| `.claude/CLAUDE.md` | Axis list 1–9, axis 7 extended | ✓ VERIFIED | See truths 16–19 |
| `docs/CAPABILITY-DECISIONS.md` | BD-07, BD-08 | ✓ VERIFIED | See truth 20 |
| `docs/BUILD-NOTES.md` | §28 Phase 13 record | ⚠️ PARTIAL | Content complete (truth 21); the plan-13-04 provenance subsection records the superseded ship identity with no supersession marker — gap 2 |
| `artifacts/shortcuts/MANIFEST.md` | Six refreshed rows | ✓ VERIFIED | All six recomputed here and matching disk; the phase-13-04 paragraph is explicitly marked **SUPERSEDED** by the code-review re-sign |
| `artifacts/shortcuts/…Core.shortcut` / `…Aware.shortcut` | Canonical names, AEA1, decrypt-verified | ✓ VERIFIED | Both begin `AEA1`; exactly two `.shortcut` basenames, no suffix; both decrypt cleanly |
| `.planning/todos/completed/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` | Closed todo with tombstone | ✓ VERIFIED | Present in `completed/`, absent from `pending/`, tombstone at `:90` |
| `.planning/debug/HANDOFF.md` | Dated REFUTED annotations at five sites | ✓ VERIFIED | Four `REFUTED` + one `SUPERSEDED` (axis-6 tally), originals preserved |
| `13-UAT.md` | Cold-runnable, BLOCKED branch | ✗ STALE | Exists with the correct BLOCKED branch and blank results; build-identity block names a non-existent artifact — gap 2 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `mirror_text()` | `verify_list_item_wrappers()` in `main()`'s chain | Guard walks the emitted array before the single write | ✓ WIRED | AST: call `:4448` < write `:4472`; a reverted emitter aborts the build (probed) |
| Built `src/PROSOCHE-Dumb.xml` | `src/PROSOCHE-Sentient.xml` | Aware forks the BUILT Core source and re-asserts per fork | ✓ WIRED | Both guards imported and invoked in `build_sentient.py`; Aware census measured identical, not inherited on assertion |
| `token()` | The Donor-5 pin | Guard fails the build if the device-confirmed envelope is replaced | ✓ WIRED | Probed: swapping one operand to `WFTextTokenAttachment` raises; flattening one raises via the census |
| `.planning/debug/Donor 5.shortcut` | The guard's docstring | Cited by path so the refutation cannot be re-litigated from the guard alone | ✓ WIRED | `:2518` |
| `src/*.xml` | `artifacts/shortcuts/*.shortcut` | Sign, then AEA1 decrypt-verify what shipped | ✓ WIRED | Decrypted both: `WFWorkflowActions` SHA-256 identical to source (4346 / 4414 actions) |
| `artifacts/shortcuts/*` | `MANIFEST.md` | Rows recomputed from disk, asserted by `manifest_check.py` | ✓ WIRED | All six rows verified independently; checker exits 0 |
| `13-UAT.md` | `mirror_text()`'s wrapped List and its `getitemfromlist` consumer | The manual device test | ⚠️ PARTIAL | The test design is sound and cold-runnable in structure; its build-identity block points at a build that no longer exists |

### Data-Flow Trace (Level 4)

| Artifact | Data variable | Source | Produces real data | Status |
|----------|---------------|--------|--------------------|--------|
| `src/*.xml` `WFItems` arrays | 666 rows / action array | `mirror_text()` → `_list_row()` per row | Yes — 616 rows carry live `attachmentsByRange` tokens over real state variables | ✓ FLOWING |
| Signed `.shortcut` containers | `WFWorkflowActions` | `sign-shortcut` over the built source | Yes — decrypted arrays byte-identical to source | ✓ FLOWING |
| `MANIFEST.md` rows | size + SHA-256 | recomputed from disk | Yes — all six match | ✓ FLOWING |
| `13-UAT.md` header build identity | size + SHA-256 + commit | copied from a superseded MANIFEST revision | **No** — names artifacts absent from disk | ✗ HOLLOW |
| `docs/BUILD-NOTES.md` §28 plan-13-04 ship table | digests, sizes, archive names, decrypt census | the pre-CR-01 ship | **No** — superseded by the re-ship, unmarked | ✗ HOLLOW |

### Behavioural Spot-Checks

| Behaviour | Command | Result | Status |
|-----------|---------|--------|--------|
| Both generators run clean with all guards armed | `python3 tools/build_state_engine.py; python3 tools/build_sentient.py` | exit 0, 0 | ✓ PASS |
| Rebuild is byte-idempotent | `git status --porcelain` + `shasum -a 256 -c` after rebuild | empty; both OK | ✓ PASS |
| Gate A, Core | `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.` exit 0 | ✓ PASS |
| Gate A, Aware | same for `PROSOCHE-Sentient.xml` | `Validation passed.` exit 0 | ✓ PASS |
| Gate B advisory, both forks (standalone, not chained) | `validate-shortcut … --target-macos 27 --target-platform all` | exit 1, **exactly one** line each: the `com.apple.mobilenotes.SharingExtension` / `WFCreateNoteInput` waiver (index 4192 Core, 4260 Aware). Nothing else | ✓ PASS (permitted waiver only) |
| All twelve `docs/*.py` checkers | each run individually | 12/12 exit 0 | ✓ PASS |
| Signed containers decrypt and match source | AEA1 → `aea decrypt` → `aa extract` → `plutil` | Both recovered; action arrays byte-identical to source; census 616/50 | ✓ PASS |
| Guard probe: revert one row to a raw `WFTextTokenString` | direct call | `SystemExit`: two-kind rule violated | ✓ PASS |
| Guard probe: drop all rows in one List | direct call | `SystemExit`: census 67/606/50 | ✓ PASS |
| Guard probe: flatten one wrapped row to a bare string | direct call | `SystemExit`: census 67/615/51 | ✓ PASS |
| Guard probe: wrapped-but-attachment-free (the CR-01 shape) | direct call | `SystemExit`: "WRAPPED but ATTACHMENT-FREE … (CR-01)" | ✓ PASS |
| Guard probe: double-wrapped row | direct call | `SystemExit`: per-row raise | ✓ PASS |
| Guard probe: List action with no `WFItems` key | direct call | `SystemExit`: per-row raise | ✓ PASS |
| Pin probe: swap Donor-5 envelope for `WFTextTokenAttachment` | direct call | `SystemExit`: "LOST the device-confirmed Donor 5 … envelope … actions 158" | ✓ PASS |
| Pin probe: FLATTEN a variable-bearing target to a raw literal | direct call | `SystemExit`: "expected 20 …, found 19 — a target was FLATTENED" | ✓ PASS |
| Pin probe: bare `U+FFFC` placeholder (pre-existing raise) | direct call | `SystemExit`: legacy message, textually distinct | ✓ PASS |
| WR-04 probe: `Value` is a plain string | direct call | `SystemExit` (not `AttributeError`) | ✓ PASS |
| Non-vacuity control | both guards on unmutated HEAD | return without raising | ✓ PASS |
| `_list_row()` totality | `5`, `None`, already-wrapped, `WFTextTokenAttachment` | all four `SystemExit`; `str` passes through | ✓ PASS |
| Device reachability | `xcrun devicectl list devices` | `No devices found.` | ✓ PASS (BLOCKED confirmed) |

### Probe Execution

No `scripts/*/tests/probe-*.sh` exists in this repository and no plan declares one — this project's
equivalent instruments are the twelve `docs/*.py` checkers and the build-time guards, all executed
above. Step 7c: satisfied by that substitution, recorded rather than skipped.

### Requirements Coverage

| Requirement | Source plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| CIRC-07 | 13-01, 13-02 | The Mirror shows a precise behavioural reflection built only from recorded facts | ✓ SATISFIED (structurally) | 616 Mirror rows now carry the donor-confirmed row framing; 0 unwrapped rows ship. The rendered result is device-gated (truths 9–10). CR-03's ordinal fact-binding defect is a separate, deferred class with its own todo |
| CIRC-04 | 13-01, 13-03, 13-04 | Confession asks for a free-text intention and then a time boundary | ✓ SATISFIED (regression-protected) | No defect site in either family — the picker is a `choosefrommenu`, not a `list`. `docs/phase5_self_check.py` exits 0 against the shipped build; §28 states this explicitly rather than inventing work |
| ROOM-03 | 13-01, 13-03, 13-04 | The Note gives exact steps for Automation B | ✓ SATISFIED (regression-protected) | No defect site in either family. `docs/note_identity_check.py` exits 0 against the shipped build |
| DIST-01 | 13-01, 13-02, 13-04 | Both forks pass the validator at the iOS 26 target | ✓ SATISFIED | Gate A re-run here: `Validation passed.`, exit 0, both forks |
| DIST-02 | 13-04 | Both forks sign into importable `.shortcut` files | ✓ SATISFIED | Both signed under the exact canonical display names, `AEA1` magic, non-zero, and both round-trip through decrypt to the exact source action arrays |
| DIST-03 | (not claimed) | Both forks import onto a real iPhone and complete a first manual run | ⚠️ BLOCKED (out of phase scope) | Standing blocker; `REQUIREMENTS.md:161` still `[ ]`. Correctly left open |

No orphaned requirements: `REQUIREMENTS.md`'s traceability table maps no additional ID to Phase 13,
and all five declared IDs are accounted for above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/*.py`, `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`, `.claude/CLAUDE.md` | — | `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` | — | **None found.** The debt-marker gate is clean |
| `docs/BUILD-NOTES.md` | §28 plan-13-04 subsection | Stale figures presented as current, with the correct figures 400 lines above in the same section | ⚠️ Warning | Gap 2 — the section contradicts itself on what shipped |
| `.planning/phases/13-…/13-UAT.md` | 18–20, 31, 48, 72, 103, 271, 331 | Build identity and census pointing at a superseded artifact | 🛑 Blocker | Gap 2 — the next device UAT would refuse the correct build |
| `.planning/debug/HANDOFF.md` | ~323 | "660 unwrapped **variable-bearing** rows" — the wording WR-07 corrected elsewhere | ℹ️ Info | The count is right; only the label is the superseded one. WR-07 swept BUILD-NOTES, MANIFEST and BD-08 but not HANDOFF |

### Human Verification Required

Both items are device-gated and cannot be raised above UNVERIFIED without hardware. DIST-03 is the
standing blocker; `xcrun devicectl list devices` returns "No devices found."

#### 1. A wrapped `WFItems` row renders non-blank

**Test:** Delete any prior install, import the **currently shipped** `PROSOCHĒ — Nine Circles —
Core.shortcut` (233802 bytes, SHA-256 `b07497ba…` — *not* the digest `13-UAT.md` currently names),
run it manually and drive a Mirror.
**Expected:** A non-empty, fact-bearing alert body. An empty or whitespace-only body means the
wrapper did not take effect.
**Why human:** Row rendering is runtime behaviour. The validator, the ToolKit catalog and the AEA1
decrypt all recover the same structurally-perfect plist; the simulator cannot import a signed
`.shortcut`. This is the entire premise of the phase and remains unobserved.

#### 2. `Item At Index` over a wrapped List returns the intended row

**Test:** Drive Mirrors at Circle 3, 7 and 9 and record which template body appears at each.
**Expected:** The body corresponds to the Circle chosen, not a neighbour.
**Why human:** No donor chains a wrapped List into `getitemfromlist`. Declared `verification:
backstop` in 13-01 precisely because it cannot be settled at file level; abstained rather than
passed on structural evidence.

*(Note: item 1's instruction deliberately overrides `13-UAT.md`'s current header, which is gap 2.)*

### Gaps Summary

**The engineering is sound and independently confirmed.** Both defect families are settled exactly
as the corrected scope requires: family 1 measured as already correct (20/20 variable-bearing sites
matching Donor 5, **zero** offenders — re-measured here, not taken from the SUMMARY) and pinned
rather than swept, with `token()`/`if_block()` byte-identical to the phase-start commit; family 2
fixed by class at one emitter, with the post-CR-01 census (67 / 616 / 50) holding identically on
both source XMLs **and** on the decrypted payloads of both signed containers. Both guards are total,
raise `SystemExit` before any write, are armed on both forks at both touch points, and every one of
the ten mutations probed here trips them while the unmutated artifact passes. Gate A is clean, gate
B reports only its permanent waiver, 12/12 checkers are green, all six MANIFEST rows match disk, and
the rebuild is byte-idempotent. The documentation pass landed: the axis list runs 1–9 with the
container defect correctly filed as its own axis, BD-07 and BD-08 carry both donor findings with
their unaudited boundaries intact, and §28 records the decrypts, the inventories, the verbatim guard
transcripts and five open assumptions.

**Both gaps are the same shape: a record that CR-01's re-ship invalidated and that was not swept.**
CR-01 changed both signed artifacts, both sources and both archives. `MANIFEST.md` and
`13-REVIEW-FIX.md` were updated — `MANIFEST.md` even marks the superseded paragraph **SUPERSEDED**
explicitly, which is the pattern the fix needs. `13-UAT.md` and `docs/BUILD-NOTES.md` §28's
plan-13-04 subsection were not. The consequence is not cosmetic: `13-UAT.md` makes importing a
specific digest **mandatory** and offers a SHA self-check, so a cold reader in Phase 19 would either
be unable to find the named artifact or would reject the correct one — and §28's closing sentence
tells that same reader "anything else is the wrong build" while naming the wrong build. This is the
one deliverable whose whole purpose is to make Phase 19's blank-Mirror observation trustworthy.

The class-closure gap is the same failure mode the must-have was written to prevent, one level out:
the sweep was honest and its six literals return zero survivors, but nine assertions of the refuted
14-site count survive in `.planning/debug/resolved/open-routing-sequence-error.md` — the closed
session the phase goal names by name — because they are phrased "THE 14 WFConditionalActionString
SITES" and "at 14 sites" rather than any declared literal. Whether that file deserves the same
exemption as the closed todo is a judgment call for the developer; either closing it with one dated
banner or naming the exemption in the record would satisfy the must-have. Both gaps are documentation
edits. **Neither touches a build input, so neither invalidates the shipped artifacts or requires a
re-sign.**

**If either gap is judged acceptable as-is**, add to this file's frontmatter:

```yaml
overrides:
  - must_have: "The refuted counts are closed as a CLASS across .planning/ and docs/"
    reason: ".planning/debug/resolved/ is immutable closed-session history, exempt on the same grounds as the closed todo"
    accepted_by: "{name}"
    accepted_at: "{ISO timestamp}"
```

---

_Verified: 2026-08-17_
_Verifier: Claude (gsd-verifier)_
