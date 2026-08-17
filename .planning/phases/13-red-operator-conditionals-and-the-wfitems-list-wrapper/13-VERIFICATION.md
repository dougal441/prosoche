---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
verified: 2026-08-17T23:55:00Z
status: human_needed
score: 25/27 must-haves verified
behavior_unverified: 2
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 23/27
  previous_verified: 2026-08-17T23:10:00Z
  closed_at_commit: 71863bf
  gaps_closed:
    - "13-UAT.md is cold-runnable, and the signed-artifact provenance record states what actually shipped"
    - "The refuted counts are closed as a CLASS across .planning/ and docs/"
  gaps_remaining: []
  regressions: []
  regression_checks:
    - "git diff ac4d3ec..71863bf -- tools/ src/ artifacts/ is EMPTY — no build input touched, no re-sign implied"
    - "Artifact census unchanged: 67 List actions / 666 rows / 616 wrapped / 50 bare / 0 attachment-free wrapped, both forks"
    - "Gate A clean on both source XMLs; 12/12 docs/*.py checkers exit 0; all six MANIFEST rows match disk"
gaps: []
deferred:
  - truth: "A wrapped WFItems row renders non-blank on device, and Item At Index over a wrapped List returns the intended row"
    addressed_in: "Phase 19"
    evidence: "ROADMAP Phase 19: 'Device UAT — nine Circles and sequence switching'; docs/BUILD-NOTES.md §28 assigns assumptions A3, A4 and A5 to Phase 19 UAT by name"
  - truth: "mirror_templates() binds facts by placeholder ordinal, so nine Mirror templates name the wrong fact"
    addressed_in: "todo (deferred by decision, CR-03)"
    evidence: ".planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md, commit d056f9a — pre-existing, outside both defect families, cold-runnable repro recorded"
  - truth: "WFNumberValue integer-vs-string encoding, and the 32 variable-valued sites no donor covers (A5 / CR-02)"
    addressed_in: "outstanding device UAT"
    evidence: "BD-08 verdict UNVERIFIED on both axes with a named owner; §28 assumption A5 names the cheapest device witnesses and the rung-4 donor that would settle the variable case"
behavior_unverified_items:
  - truth: "A wrapped WFItems row renders non-blank on device — the whole point of the family-2 fix"
    test: "Delete any prior install, import the shipped Core artifact (233802 B, SHA-256 b07497ba…, commit 365937e) on an iOS 26.x iPhone, run it manually and drive a Mirror"
    expected: "A non-empty, fact-bearing Mirror body. Note row 8 is now a BARE row, so a blank at Circle VIII would indict the literal path rather than the wrapper — record WHICH row was showing"
    why_human: "Row rendering is runtime behaviour. Neither validator gate, the ToolKit catalog, nor the AEA1 decrypt can see it — the decrypt recovers the same structurally-perfect plist. The simulator cannot import a signed .shortcut and lacks com.apple.mobilenotes. Device-gated; `xcrun devicectl list devices` re-run at this verification returns 'No devices found.' and DIST-03 is open."
  - truth: "Item At Index selection over a WRAPPED List returns the same row content it returned over an unwrapped List (declared `verification: backstop` in 13-01)"
    test: "On device, drive Mirrors at Circle 3, 7 and 9 and confirm the body matches the template for that Circle, not a neighbouring row"
    expected: "The selected row's rendered text corresponds to the Circle chosen"
    why_human: "No donor chains a wrapped List into getitemfromlist, so extraction semantics over a wrapped array are unobserved. The file-level half IS verified here (row count/order unchanged at [6]+[10]*66, WFItemSpecifier and WFItemIndex untouched, no arithmetic and no uid() introduced) — the runtime half is device-only and abstains rather than passing on structure."
unverified_prohibitions:
  - statement: "MUST NOT fabricate a parameter shape the donors do not settle — in particular MUST NOT encode any WFItemType value other than 0"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "Measured at HEAD: the only WFItemType value present in either fork is 0 (616 rows each). verify_list_item_wrappers() asserts the KEY's presence and never its value. _list_row(), BD-08, axis 8 and assumption A2 each state the non-0 values are deliberately unaudited."
    flag: "unverified-prohibition — human review recommended"
  - statement: "MUST NOT silence a build guard or a docs/*.py checker to make the suite green"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "git diff 698ab99..HEAD touches no docs/*.py file. Both guards were widened, not weakened: ten synthetic mutations probed here all raise SystemExit, and both return cleanly on the unmutated artifact. AST: zero ast.Assert nodes in either guard or in _list_row(); every raise is SystemExit."
    flag: "unverified-prohibition — human review recommended"
  - statement: "MUST NOT record a device-evidence verdict that was not observed on a device"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "`xcrun devicectl list devices` re-run at this verification returns 'No devices found.' 13-UAT.md carries status: blocked, blocked_on: DIST-03, and all eight outcome fields are blank. No simulator run or decrypt inference is entered as device evidence in §28 or the UAT."
    flag: "unverified-prohibition — human review recommended"
  - statement: "MUST NOT erase a refuted claim without leaving a tombstone"
    verdict: "no violation found (LLM-judge, NON-AUTHORITATIVE)"
    evidence: "The gap-2 fix is +23/-0 lines on .planning/debug/resolved/open-routing-sequence-error.md — a pure insertion. All nine historical assertions re-measured present at +23 offsets; nothing was rewritten or deleted."
    flag: "unverified-prohibition — human review recommended"
human_verification:
  - test: "Import the shipped Core artifact (233802 B / b07497ba…) and drive a Mirror; record whether the body is non-empty and which row rendered"
    expected: "Non-empty, fact-bearing Mirror body"
    why_human: "Row rendering is device-only runtime behaviour; no file-level channel can observe it"
  - test: "Drive Mirrors at Circle 3, 7 and 9 and record which template body appears at each"
    expected: "Body corresponds to the Circle chosen, not a neighbour"
    why_human: "No donor chains a wrapped List into getitemfromlist; extraction over a wrapped array is unobserved"
---

# Phase 13: Red-operator conditionals and the WFItems List wrapper — Verification Report

**Phase Goal (as corrected by this phase's own research):** Settle two defect families carried
unchanged through every cycle of the closed `open-routing-sequence-error` session — the
`WFConditionalActionString` conditional operand shape (measured as already correct → pin, do not
fix) and the `WFItems` List row wrapper (real, 33× larger than recorded → fix by class) — with
build-time recurrence guards for both, sensitivity demonstrated, and the newly-confirmed axes
folded into `.claude/CLAUDE.md` in one pass.

**Verified:** 2026-08-17 (re-verification at HEAD `71863bf`)
**Status:** human_needed
**Re-verification:** Yes — after gap closure. Previous: `gaps_found`, 23/27.

Every figure below was re-derived independently at HEAD with `plistlib`, `git`, the validator, the
AEA1 decrypt recipe and direct guard probes. No number is taken from a SUMMARY or from the closure
claim.

## Re-verification Result

| Gap (previous run) | Status now | How it was re-checked |
|---|---|---|
| **Gap 1** — `13-UAT.md` and `BUILD-NOTES.md` §28 described the superseded `737ce07` ship | ✓ CLOSED | UAT header now names `365937e` and `233802 B / b07497ba…`, `237842 B / 212598cf…` — **byte-for-byte the values I computed from disk**, so its own SHA self-check would now ACCEPT the shipped build. All five census sites read 616/50; the three surviving `737ce07`/660-6 references are each explicitly labelled superseded (`:33-36`, `:59-61`, `:84-85`). §28's plan-13-04 subsection gained the `SUPERSEDED` block at `:2789` in the exact form its MANIFEST sibling used, both signing rows are labelled *(superseded)*, and the Phase-19 re-import instruction at `:2868` now names `b07497ba…` with `fe1bafdf…` marked superseded |
| **Gap 2** — nine untombstoned assertions of the refuted 14-site count | ✓ CLOSED | My broader phrasing sweep re-run: **0 untombstoned survivors** under the now-three declared exemptions (it still finds all 9 under the previous two, confirming the sweep itself did not go blind). `.planning/debug/resolved/` is recorded as the third exemption at `docs/BUILD-NOTES.md:2486-2500` with all nine of my line numbers enumerated and the audit-trail rationale. A dated `REFUTED` banner sits at `:10-31` of the resolved file — **immediately after the frontmatter, above the pre-existing RESOLVED banner**, so a cold reader meets it before any cycle entry |
| Regression check | ✓ NONE | `git diff ac4d3ec..71863bf -- tools/ src/ artifacts/` is **empty**. Doc-only, as claimed |

**Nothing was lost to close gap 2.** The diff on the resolved file is **+23 / −0** — a pure
insertion. All nine historical assertions re-measured present at +23 offsets (833, 954, 1060, 1067,
1220, 1226, 1293, 1300, 4690); the file grew 5001 → 5024 lines. The banner states the count is zero
not 14, names Donor 5 and the 192/195 · 20/20 measurement, records the 33× family-2 under-count and
the corrected 616/50 census, retires `if_block("Previous Respected", 4, …)` as a non-member, and says
explicitly that the nine assertions below stand on purpose. §28 additionally records the lesson —
a literal-phrasing sweep closes only the phrasings it enumerates — which is the honest generalisation
of the finding rather than a patch over it.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Every attachment-bearing List row is wrapped `{WFItemType: 0, WFValue: <WFTextTokenString>}`; zero raw `WFTextTokenString` rows in any `WFItems` array, both forks | ✓ VERIFIED | Re-measured at HEAD: 67 List actions, 666 rows, **616 wrapped / 50 bare / 0 other / 0 missing `WFItemType` / 0 wrapped-but-attachment-free**, identical per fork |
| 2 | Literal rows stay bare strings — the donor two-kind rule, not a blanket sweep | ✓ VERIFIED | 50 bare = 6 exit names + 44 attachment-free templates. Per-array shapes `1×(0,6)`, `22×(10,0)`, `44×(9,1)` — the 44 are the donor-observed **mixed** array |
| 3 | `verify_list_item_wrappers()` raises `SystemExit` (never `assert`) before the single write; message carries cause, first five offenders as action/row pairs, and the total | ✓ VERIFIED | AST: 0 `ast.Assert`, 2 `SystemExit` raises; call `:4448` precedes the single `SOURCE.write_bytes()` `:4472` |
| 4 | The new guard is armed on BOTH forks at BOTH touch points | ✓ VERIFIED | AST over `build_sentient.py`: present in the `ImportFrom build_state_engine` names **and** as a bare `Expr(Call(Name))`. Same for `verify_conditional_action_string` |
| 5 | Both guards are sensitive to a synthetically reverted artifact, and non-vacuous on HEAD | ✓ VERIFIED | 10 mutations probed, all 10 raise `SystemExit`; both guards return cleanly unmutated |
| 6 | The rebuild is byte-idempotent | ✓ VERIFIED | Provenance ancestor check exit 0, both generators re-run: `git status --porcelain` empty, `shasum -c` OK |
| 7 | `_list_row()` is element-wise and total; per-action row counts `[6] + [10]*66` | ✓ VERIFIED | Distribution `{6:1, 10:66}` per fork. `5`, `None`, an already-wrapped row and a `WFTextTokenAttachment` each raise; a `str` passes through |
| 8 | Row offsets survive the wrapper unchanged (BMP-only; every `{p, 1}` indexes a `U+FFFC`) | ✓ VERIFIED | 1056 attachment ranges per fork: 0 bad, 0 non-BMP |
| 9 | A wrapped row renders **non-blank on device** | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Structure present, wired and shipped; rendering is runtime-only. `xcrun devicectl list devices` → "No devices found." Deliberately not promoted now that the doc gaps are closed |
| 10 | `Item At Index` over a WRAPPED List returns the same row content (`verification: backstop`) | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | File-level half verified; runtime half unobserved by any donor — abstained, not passed |
| 11 | `verify_conditional_action_string()` carries a POSITIVE Donor-5 pin with its provenance docstring | ✓ VERIFIED | `:2499-2618`; docstring cites `.planning/debug/Donor 5.shortcut` and states the pin repairs nothing |
| 12 | The pin passes non-vacuously: exactly 20 variable-bearing sites per fork, zero offenders | ✓ VERIFIED | Core 192 slots / 20 / 172 literals; Aware 195 / 20 / 175; split 19×code 4 + 1×code 99. **0 offenders** — the 14-site claim refuted by my own walk |
| 13 | No emission site was swept — `token()` and `if_block()` unchanged, literals 172 / 175 | ✓ VERIFIED | AST of both functions at `698ab99` vs HEAD: **identical** |
| 14 | The raises are distinguishable, the ordering mask is recorded verbatim, the chain was not reordered | ✓ VERIFIED | Three raises, each fired independently against its own mutation with distinct text; census raise appended last by design |
| 15 | The Aware fork needed no new touch point, and that absence is recorded rather than inferred | ✓ VERIFIED | AST confirms both sites pre-exist; `build_sentient.py:337-362` states the exception and its reason |
| 16 | `.claude/CLAUDE.md`'s axis list runs 1–9, heading and `/ponytail` row agreeing | ✓ VERIFIED | Heading `:353`, `/ponytail` `:258`, items `:375-453`; no site asserts seven or eight |
| 17 | Axis 8 states the two-kind rule, cites both donors by path, names the guard, and is a CONTAINER defect distinct from axis 2 | ✓ VERIFIED | `:419-452`, including the post-CR-01 "discriminate on attachment-bearing-ness" correction and the `WFItemType`-beyond-0 boundary |
| 18 | Axis 9 states the compound/scalar reader rule with the four `COMPOUND_STATE_KEYS` and its guard | ✓ VERIFIED | `:453-468`; the four names match `build_state_engine.py:3650-3653` exactly |
| 19 | Axis 7 is extended with the `pending_exit` container/leaf pattern | ✓ VERIFIED | `:407-418` |
| 20 | `docs/CAPABILITY-DECISIONS.md` carries BD-07 and BD-08 with their unsettled boundaries intact | ✓ VERIFIED | BD-07 `:869`, BD-08 `:936`, both in the ToC; BD-08 carries the post-CR-01 census and CR-02's retraction |
| 21 | `docs/BUILD-NOTES.md` carries a Phase 13 section with the decrypts, both inventories, the refutation, verbatim guard texts, the ordering mask and every open assumption | ✓ VERIFIED | §28 `:2365-2872`, now also carrying the third-exemption record and the sweep lesson |
| 22 | ROADMAP prose and milestone checklist state the measured figures, dated and attributed; HANDOFF tombstoned at every asserting site; the todo closed with a tombstone | ✓ VERIFIED | ROADMAP `:36`, `:574-612`; HANDOFF `REFUTED` at `:255`, `:321`, `:339`, `:523` + `SUPERSEDED` `:163`; todo in `completed/` with tombstone `:90` |
| 23 | The refuted counts are closed as a CLASS across `.planning/` and `docs/` | ✓ VERIFIED *(was FAILED)* | Broader phrasing sweep re-run: **0 untombstoned survivors** under the three declared exemptions. Third exemption recorded with rationale and my nine line numbers; dated `REFUTED` banner at the head of the resolved file, +23/−0 |
| 24 | Ship gate: canonical names, six MANIFEST rows matching disk, 12/12 checkers, gate A clean, gate B one waiver per fork, decrypt-verified shipped shape | ✓ VERIFIED | All re-derived — see tables below. Decrypted both containers: action arrays **byte-identical** to source, census 616/50 |
| 25 | `13-UAT.md` is cold-runnable, with an explicit BLOCKED branch leaving every result blank | ✓ VERIFIED *(was FAILED)* | Header values match disk exactly, so the self-check accepts the correct build; precondition names `365937e` and explains why `737ce07` must not be tested; all census sites 616/50 or explicitly marked superseded; `status: blocked`, `blocked_on: DIST-03`, all eight outcome fields blank |
| 26 | The device verdict is recorded as observed, not inferred | ✓ VERIFIED | `xcrun devicectl list devices` re-run → "No devices found." |
| 27 | Interrupting or re-running the build/sign sequence cannot leave a half-written artifact | ✓ VERIFIED | Core: every `verify_*` precedes the single write. Aware: `tempfile.NamedTemporaryFile` + `os.replace` at `build_sentient.py:405-408`. Re-run byte-idempotent |

**Score:** 25/27 truths verified (2 present, behavior-unverified; 0 failed)

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | Wrapped-row rendering and wrapped-List extraction | Phase 19 | ROADMAP Phase 19 goal; §28 assigns A3/A4/A5 to Phase 19 UAT by name |
| 2 | `mirror_templates()` ordinal fact binding (CR-03) | todo, deferred by decision | `.planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md` (`d056f9a`) |
| 3 | `WFNumberValue` encoding + the 32 variable-valued sites (A5 / CR-02) | outstanding device UAT | BD-08 `UNVERIFIED` on both axes with a named owner |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `tools/build_state_engine.py` | `_list_row()`, wrapped `mirror_text()`, both guards | ✓ VERIFIED | `:648-718`, `:721-730`, `:2499-2618`, `:2630-2726`; registered `:4442-4460`. Unchanged by the gap-closure commit |
| `tools/build_sentient.py` | Per-fork arming at both touch points | ✓ VERIFIED | Import `:23` / call `:384`; import `:19` / call `:365`. AST-confirmed |
| `src/PROSOCHE-Dumb.xml` | 67 List actions, 616 wrapped + 50 bare | ✓ VERIFIED | Measured; gate A clean; 4346 actions |
| `src/PROSOCHE-Sentient.xml` | Same census after the fork | ✓ VERIFIED | Measured; gate A clean; 4414 actions |
| `.claude/CLAUDE.md` | Axis list 1–9, axis 7 extended | ✓ VERIFIED | Truths 16–19 |
| `docs/CAPABILITY-DECISIONS.md` | BD-07, BD-08 | ✓ VERIFIED | Truth 20 |
| `docs/BUILD-NOTES.md` | §28 Phase 13 record, ship provenance current | ✓ VERIFIED | Truth 21 + the `SUPERSEDED` block at `:2789` and the corrected Phase-19 instruction at `:2868` |
| `artifacts/shortcuts/MANIFEST.md` | Six refreshed rows | ✓ VERIFIED | All six recomputed and matching disk; `manifest_check.py` exits 0 |
| `artifacts/shortcuts/…Core.shortcut` / `…Aware.shortcut` | Canonical names, AEA1, decrypt-verified | ✓ VERIFIED | Both `AEA1`, exactly two basenames, no suffix, both round-trip to the exact source action arrays |
| `.planning/todos/completed/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` | Closed todo with tombstone | ✓ VERIFIED | In `completed/`, absent from `pending/`, tombstone `:90` |
| `.planning/debug/HANDOFF.md` | Dated annotations at five sites | ✓ VERIFIED | Four `REFUTED` + one `SUPERSEDED`, originals preserved |
| `.planning/debug/resolved/open-routing-sequence-error.md` | Dated `REFUTED` banner ahead of the history | ✓ VERIFIED | `:10-31`, above the pre-existing RESOLVED banner; +23/−0, nothing lost |
| `13-UAT.md` | Cold-runnable, BLOCKED branch | ✓ VERIFIED | Truth 25 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `mirror_text()` | `verify_list_item_wrappers()` in `main()`'s chain | Guard walks the array before the single write | ✓ WIRED | Call `:4448` < write `:4472`; a reverted emitter aborts the build (probed) |
| Built `PROSOCHE-Dumb.xml` | `PROSOCHE-Sentient.xml` | Aware forks the BUILT source and re-asserts per fork | ✓ WIRED | Both guards imported and invoked; Aware census measured, not inherited on assertion |
| `token()` | The Donor-5 pin | Guard fails the build if the device-confirmed envelope is replaced | ✓ WIRED | Envelope swap and flatten both raise |
| `.planning/debug/Donor 5.shortcut` | The guard's docstring | Cited by path | ✓ WIRED | `:2518` |
| `src/*.xml` | `artifacts/shortcuts/*.shortcut` | Sign, then AEA1 decrypt-verify | ✓ WIRED | `WFWorkflowActions` SHA-256 identical to source (4346 / 4414 actions) |
| `artifacts/shortcuts/*` | `MANIFEST.md` | Rows recomputed from disk, asserted by `manifest_check.py` | ✓ WIRED | Six of six verified independently |
| `13-UAT.md` | `mirror_text()`'s wrapped List and its `getitemfromlist` consumer | The manual device test | ✓ WIRED | Build identity now matches disk, so the test can actually be run against the artifact it describes |
| `.planning/debug/resolved/…` banner | `BUILD-NOTES.md` §28 / BD-07 | Cold reader meets the refutation before the history, and is pointed at the full account | ✓ WIRED | Banner is the first prose in the file and names both destinations |

### Data-Flow Trace (Level 4)

| Artifact | Data variable | Source | Produces real data | Status |
|----------|---------------|--------|--------------------|--------|
| `src/*.xml` `WFItems` arrays | 666 rows / action array | `mirror_text()` → `_list_row()` per row | Yes — 616 rows carry live tokens over real state variables | ✓ FLOWING |
| Signed `.shortcut` containers | `WFWorkflowActions` | `sign-shortcut` over the built source | Yes — decrypted arrays byte-identical to source | ✓ FLOWING |
| `MANIFEST.md` rows | size + SHA-256 | recomputed from disk | Yes — all six match | ✓ FLOWING |
| `13-UAT.md` header build identity | size + SHA-256 + commit | the live artifacts at `365937e` | Yes — matches disk byte-for-byte | ✓ FLOWING *(was HOLLOW)* |
| `docs/BUILD-NOTES.md` §28 ship provenance | digests, sizes, census, Phase-19 instruction | marked SUPERSEDED, with live values named | Yes — the current values are stated and the historical ones are labelled | ✓ FLOWING *(was HOLLOW)* |

### Behavioural Spot-Checks

| Behaviour | Command | Result | Status |
|-----------|---------|--------|--------|
| No build input touched by the gap closure | `git diff ac4d3ec..71863bf -- tools/ src/ artifacts/` | empty | ✓ PASS |
| Artifact census unchanged | `plistlib` walk, both forks | 67 / 666 / 616 / 50 / 0 / 0 | ✓ PASS |
| Gate A, both forks | `validate-shortcut … --target-macos 26 --target-platform all` | `Validation passed.` exit 0 ×2 | ✓ PASS |
| Gate B advisory, both forks (standalone) | `… --target-macos 27 --target-platform all` | exit 1, exactly one `WFCreateNoteInput` waiver each | ✓ PASS (permitted waiver only) |
| All twelve `docs/*.py` checkers | each run individually | 12/12 exit 0 | ✓ PASS |
| MANIFEST six rows vs disk | `shasum -a 256` + grep per row | 6/6 MATCH | ✓ PASS |
| Signed containers decrypt and match source | AEA1 → `aea decrypt` → `aa extract` → `plutil` | action arrays byte-identical; census 616/50 | ✓ PASS |
| Rebuild byte-idempotent | both generators + `git status --porcelain` | empty, digests unchanged | ✓ PASS |
| Refuted-count sweep, three exemptions | broader phrasing sweep over `.planning/` + `docs/` | **0 untombstoned survivors** | ✓ PASS |
| Refuted-count sweep, two exemptions (control) | same sweep, third exemption removed | 9 survivors — the sweep still has teeth | ✓ PASS |
| Banner insertion is loss-free | `git diff --numstat` on the resolved file | `23 0` — pure insertion; 5001 → 5024 lines | ✓ PASS |
| Guard probes (10 mutations + 2 non-vacuity controls) | direct calls against HEAD action arrays | 10/10 `SystemExit`; both guards clean unmutated | ✓ PASS |
| `_list_row()` totality | `5`, `None`, already-wrapped, `WFTextTokenAttachment`, `str` | 4 rejections, 1 pass-through | ✓ PASS |
| Device reachability | `xcrun devicectl list devices` | `No devices found.` | ✓ PASS (BLOCKED confirmed) |

### Probe Execution

No `scripts/*/tests/probe-*.sh` exists in this repository and no plan declares one. This project's
equivalent instruments are the twelve `docs/*.py` checkers and the build-time guards, all executed
above — recorded as a substitution rather than a skip.

### Requirements Coverage

| Requirement | Source plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| CIRC-07 | 13-01, 13-02 | The Mirror shows a precise behavioural reflection built only from recorded facts | ✓ SATISFIED (structurally) | 616 Mirror rows carry the donor-confirmed framing; 0 unwrapped rows ship. Rendered result device-gated (truths 9–10). CR-03's ordinal fact-binding defect is a separate, deferred class with its own todo |
| CIRC-04 | 13-01, 13-03, 13-04 | Confession asks for a free-text intention and then a time boundary | ✓ SATISFIED (regression-protected) | No defect site in either family — the picker is a `choosefrommenu`, not a `list`. `docs/phase5_self_check.py` exits 0 against the shipped build; §28 says so explicitly rather than inventing work |
| ROOM-03 | 13-01, 13-03, 13-04 | The Note gives exact steps for Automation B | ✓ SATISFIED (regression-protected) | No defect site in either family. `docs/note_identity_check.py` exits 0 against the shipped build |
| DIST-01 | 13-01, 13-02, 13-04 | Both forks pass the validator at the iOS 26 target | ✓ SATISFIED | Gate A re-run: `Validation passed.`, exit 0, both forks |
| DIST-02 | 13-04 | Both forks sign into importable `.shortcut` files | ✓ SATISFIED | Both signed under the exact canonical display names, `AEA1` magic, non-zero, both round-trip to the exact source action arrays |
| DIST-03 | (not claimed) | Both forks import onto a real iPhone and complete a first manual run | ⚠️ BLOCKED (out of phase scope) | Standing blocker; `REQUIREMENTS.md:161` still `[ ]`. Correctly left open |

No orphaned requirements: `REQUIREMENTS.md`'s traceability table maps no additional ID to Phase 13,
and all five declared IDs are accounted for.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/*.py`, `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`, `.claude/CLAUDE.md`, `13-UAT.md` | — | `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` | — | **None found.** Debt-marker gate clean |
| `docs/BUILD-NOTES.md` | 2730 | "both sources still carry the wave-2 digests `99388cad…` / `d01154b3…`" — present tense, above the `SUPERSEDED` block at `:2789`; sources now carry `c6270691…` / `709f53f8…` | ℹ️ Info | Not a gap: the operative claim (byte-idempotence) is true and independently re-verified, these are *source* not signed-artifact digests, no one imports a source XML, and `MANIFEST.md` is authoritative and correct. Worth a one-line fix on the next doc pass, not a re-open |
| `.planning/debug/HANDOFF.md` | ~323 | "660 unwrapped **variable-bearing** rows" — the wording WR-07 corrected elsewhere | ℹ️ Info | The count is right; only the label is superseded. WR-07 swept BUILD-NOTES, MANIFEST and BD-08 but not HANDOFF |

### Human Verification Required

Both items are device-gated and cannot be raised above UNVERIFIED without hardware. DIST-03 is the
standing blocker; `xcrun devicectl list devices` returns "No devices found." **These two are the only
things between this phase and `passed`, and they are correctly not promoted on structural evidence.**

#### 1. A wrapped `WFItems` row renders non-blank

**Test:** Delete any prior install, import `PROSOCHĒ — Nine Circles — Core.shortcut` (233802 bytes,
SHA-256 `b07497ba…`, commit `365937e` — the values `13-UAT.md`'s header now names, verified against
disk), run it manually and drive a Mirror.
**Expected:** A non-empty, fact-bearing alert body. **Row 8 is now a bare row**, so a blank at Circle
VIII would indict the literal path rather than the wrapper — record *which* row was showing, not just
"blank".
**Why human:** Row rendering is runtime behaviour. The validator, the ToolKit catalog and the AEA1
decrypt all recover the same structurally-perfect plist; the simulator cannot import a signed
`.shortcut` and lacks `com.apple.mobilenotes`. This is the premise of the phase and remains unobserved.

#### 2. `Item At Index` over a wrapped List returns the intended row

**Test:** Drive Mirrors at Circle 3, 7 and 9 and record which template body appears at each.
**Expected:** The body corresponds to the Circle chosen, not a neighbour.
**Why human:** No donor chains a wrapped List into `getitemfromlist`. Declared `verification:
backstop` in 13-01 precisely because it cannot be settled at file level; abstained rather than passed.

`13-UAT.md` is the cold-runnable instrument for both, and now names the build that actually ships.

### Gaps Summary

**No gaps remain.** Both defect families are settled exactly as the corrected scope requires, and
both closure edits are doc-only — `git diff ac4d3ec..71863bf -- tools/ src/ artifacts/` is empty, so
nothing about the shipped artifacts changed and no re-sign is implied.

Family 1 re-measured independently: 192/195 slot-carrying mode-0 conditionals, 20/20 variable-bearing
matching Donor 5, **zero** offenders, with `token()` and `if_block()` AST-identical to phase-start
`698ab99` — the phase pinned a device-confirmed shape and swept nothing, which is the right call and
the opposite of the ROADMAP's original instruction. Family 2 fixed by class at one emitter, census
67 / 616 / 50 holding identically on both source XMLs *and* on the decrypted payloads of both signed
containers. Both guards are total, raise `SystemExit` before any write, are armed on both forks at
both touch points, and all ten probed mutations trip them while the unmutated artifact passes.

The two closures are each better than the minimum the gap required. Gap 1 was fixed at both sites
with the supersession marker its sibling record already used, and `13-UAT.md` gained a genuinely new
piece of test guidance — row 8 is now bare, so the tester is told to record *which* row rendered,
which converts an ambiguous blank into a diagnosis. Gap 2 was closed by declaring the exemption and
adding one banner rather than by rewriting nine historical records, preserving the audit trail the
refutation depends on (+23/−0, verified), and §28 records the generalisable lesson — a
literal-phrasing sweep closes only the phrasings it enumerates — rather than just patching the
instance.

**Status is `human_needed`, not `passed`, solely because the two device-gated truths remain
unobserved.** No device exists; promoting either on structural evidence is exactly the inversion this
project's evidence ladder forbids. The phase's own goal calls these "device-visible defects that no
file-level analysis can detect" — file-level analysis is therefore complete, and correct, and cannot
be the last word.

---

_Verified: 2026-08-17 (re-verification at `71863bf`)_
_Verifier: Claude (gsd-verifier)_
