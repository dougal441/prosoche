---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
plan: 03
subsystem: docs
tags: [documentation, recording-duty, refutation, tombstone, donor-evidence, capability-decisions, build-notes, roadmap, handoff, circ-07]

# Dependency graph
requires:
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-01"
    provides: "the WFItems row wrapper fix, verify_list_item_wrappers(), the measured 66/660 inventory and three verbatim SystemExit transcripts"
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-02"
    provides: "the Donor-5 pin, the 192/195 and 20/20 inventory, four verbatim SystemExit transcripts, the ordering-mask demonstration, and the three corrections handed explicitly to this plan"
provides:
  - ".claude/CLAUDE.md's numbered generator-authoring axis list extended from seven to nine, with axis 7 refined"
  - "docs/CAPABILITY-DECISIONS.md BD-07 -- the conditional TEXT-slot operand settled ALREADY CORRECT from Donor 5"
  - "docs/CAPABILITY-DECISIONS.md BD-08 -- the WFItems two-kind row rule from Donors 4 and 4.1, with its unaudited boundary"
  - "docs/BUILD-NOTES.md section 28 -- the Phase 13 recording duty: decrypts, measured inventory, refutation, verbatim guard evidence, the ordering mask, A1-A4"
  - "the refuted counts closed as a CLASS across .planning/ and docs/, proven by a whole-tree sweep over six literal phrasings"
  - "the pending todo closed into completed/ with a standalone tombstone"
affects: [13-04, Phase-19-device-UAT, every-later-generator-pass]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Tombstone-not-delete: a refuted claim keeps its original wording and gains a dated uppercase REFUTED/SUPERSEDED annotation beside it, because an unrecorded refutation gets re-litigated next cycle"
    - "Close a stale claim as a CLASS via a whole-tree sweep over literal phrasings with a +/-12-line tombstone window, never by enumerating remembered sites -- a section-scoped edit measurably leaves sites uncorrected"
    - "Deliberate sweep exemptions (.planning/todos/completed/, .planning/phases/13-*/) where the historical wording must survive in order to BE the tombstone"
    - "Marker casing as a load-bearing contract: the sweep window matches case-sensitively, so a lowercase 'refuted' beside a quoted original figure passes one assertion and fails the other -- fix by adding the uppercase marker at the named line, never by relaxing the window"
    - "A CONTAINER defect gets its own axis rather than being filed under the string-envelope axis, because a type-scoped sweep for a wrong envelope is structurally blind to a missing row framing"

key-files:
  created: []
  modified:
    - ".claude/CLAUDE.md"
    - "docs/CAPABILITY-DECISIONS.md"
    - "docs/BUILD-NOTES.md"
    - ".planning/ROADMAP.md"
    - ".planning/debug/HANDOFF.md"
    - ".planning/todos/completed/2026-08-15-fix-red-operator-and-list-wrapper-defects.md (moved from pending/ via git mv)"

key-decisions:
  - "The WFItems row wrapper is a NEW axis (8), not an instance of axis 2. At a defective site the envelope inside WFValue is already correct; what is missing is the row framing around it, so a type-scoped sweep for a wrong string envelope cannot see the class at all. 13-RESEARCH.md and 13-01-SUMMARY.md both insist on this and the axis body states it explicitly."
  - "The pending_exit container/leaf pattern EXTENDS axis 7 rather than becoming a tenth axis. It is the same 'state shape must exist before it is read' rule made concrete -- seeding is only half of it, never destroying what was seeded is the other half."
  - "Axis 9 names the four COMPOUND_STATE_KEYS members verbatim from the frozenset in source (recent_sessions, recent_contracts, exit_events, profile_snapshot.enabled_exits), NOT the four listed in 13-RESEARCH.md's doc-update table, which named exit_stats.<name>.samples in place of recent_contracts. The source is authoritative; the dynamically-keyed fifth instance is recorded beside the frozenset as the source itself records it."
  - "All three corrections wave 2 handed over are carried verbatim into the prose record: the '14 sites' figure is ZERO; if_block('Previous Respected', 4, ...) is NOT a member of the family because it passes a raw literal; and the raw-literal comparison-target question is unsettled BY DECISION, needing a rung-4 one-action donor, never to be written up as resolved."
  - "HANDOFF.md keeps every original sentence. Five dated annotations were ADDED beside them; nothing was rewritten. Rewriting history in a handoff record destroys the audit trail that makes the refutation credible in the first place."
  - "The refuted counts were closed by SWEEP, not by enumeration. Plan review had measured two sites outside any section-scoped edit; the sweep found eleven, including three in the todo that resolved via the git mv into the exempt completed/ directory."
  - "docs/manifest_check.py left RED, unchanged from waves 1 and 2. No MANIFEST row was edited and the checker was not weakened. Plan 13-04 owns the re-sign (constraint D-04)."
  - "CIRC-04 and ROOM-03 are recorded as regression-protection requirements with NO defect site in either family. No work was invented to make them look addressed -- the honest record is that phase5_self_check.py and note_identity_check.py stayed green through the rebuild."

patterns-established:
  - "When a documentation task both WRITES refuted-count prose and NEGATIVE-GREPS for it, keep every refuted literal either inside an exempt path or tombstoned in the same breath -- the task is its own adversary"
  - "A placeholder for a later plan must be labelled and EMPTY, with an explicit statement that its contents are not guessed, so a reader cannot mistake absence for a finding"

requirements-recorded: [CIRC-07]
requirements-regression-protected: [CIRC-04, ROOM-03]

coverage:
  - id: D1
    description: "The numbered generator-authoring axis list in .claude/CLAUDE.md runs 1 through 9; axis 8 is the WFItems two-kind row rule stated as a CONTAINER defect distinct from axis 2, axis 9 is the compound-versus-scalar reader rule, and axis 7 is extended with the pending_exit container/leaf pattern"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "regex over the section body: items == ['1'..'9']; axis 8 contains WFItemType, WFValue, 'Donor 4', verify_list_item_wrappers and the word 'container'; axis 9 contains get_value, read_value, verify_compound_value_reads; axis 7 contains pending_exit"
        status: pass
    human_judgment: false
  - id: D2
    description: "The axis count is consistent at every site in the file -- 'seven parameter-defect axes' appears nowhere and 'nine parameter-defect axes' appears at both the list heading and the /ponytail row in section 9"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "line-scan asserting zero occurrences of the old phrase and >= 2 of the new. Measured: exactly the two known sites carried the count (heading :353, /ponytail row :258)"
        status: pass
    human_judgment: false
  - id: D3
    description: "docs/CAPABILITY-DECISIONS.md carries BD-07 and BD-08, each in the table of contents and as a full record, with their evidence tokens and their unsettled boundaries stated rather than resolved"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "count(BD-07) >= 2 and count(BD-08) >= 2; BD-07 body contains 'Donor 5', WFTextTokenString, WFTextTokenAttachment and REFUTED; BD-08 body contains WFItemType, 'Donor 4.1', WFNumberValue and 660"
        status: pass
    human_judgment: false
  - id: D4
    description: "docs/BUILD-NOTES.md gains a numbered Phase 13 section carrying the decrypts, the measured inventory, the refutation, both guards' verbatim SystemExit texts, the ordering mask, A1-A4, and the CIRC-04/ROOM-03 regression-protection statement"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "section 28 matched by ^## (\\d+)\\. with 'Phase 13' in the title; body contains Donor 5, Donor 4.1, verify_list_item_wrappers, verify_conditional_action_string, SystemExit, 660, CIRC-04, ROOM-03 and the refutation"
        status: pass
    human_judgment: false
  - id: D5
    description: "The ROADMAP Phase 13 Goal and Deliverables prose states the MEASURED figures with a dated correction note, and the edit is provably scoped rather than a rewrite"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "the Phase 13 section contains 66, 660 and 'Donor 5'; the Requirements and Depends on lines are byte-identical; the file still holds >= 20 '### Phase ' headings (measured 21)"
        status: pass
    human_judgment: false
  - id: D6
    description: "The refuted counts are closed as a CLASS: a whole-tree sweep of .planning/ and docs/ over six literal phrasings finds no untombstoned survivor outside the two deliberate exemptions"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "sweep over *.md under .planning/ and docs/, excluding .planning/todos/completed/ and .planning/phases/13-*/, requiring every hit to sit within twelve lines of an uppercase REFUTED or SUPERSEDED marker. Dry run before the task found 11 survivors; final run finds 0"
        status: pass
    human_judgment: false
  - id: D7
    description: "The pending todo is closed by moving it into completed/ with a standalone tombstone, and .planning/debug/HANDOFF.md carries a dated annotation at every asserting site with its original wording preserved"
    requirement: "CIRC-07"
    verification:
      - kind: integration
        ref: "pending/ path absent, completed/ path present and containing REFUTED, 660 and 'Phase 13'; HANDOFF.md carries a tombstone marker plus both measured figures; git mv preserved history (R status in git)"
        status: pass
    human_judgment: false
  - id: D8
    description: "No build input was modified and the checker baseline is exactly as waves 1-2 left it"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "git status --porcelain shows no path under tools/ or src/ at either commit point; 11 of 12 docs/*.py exit 0 and docs/manifest_check.py fails with the identical D-04 byte-count AssertionError inherited from 13-01"
        status: pass
    human_judgment: false
  - id: D9
    description: "The Mirror renders non-empty text and the variable-bearing conditionals render as valid non-red chips on a real iPhone"
    requirement: "CIRC-07"
    verification:
      - kind: backstop
        ref: "Device-only, inherited unchanged from 13-01 (assumption A4) and 13-02 (assumption A1). This plan writes no code and can neither advance nor regress it; it records both as OPEN with their risk, and adds the installed-base note requiring Phase 19 to test a RE-IMPORTED build"
        status: deferred
    human_judgment: true

# Metrics
duration: 20 min
completed: 2026-08-17
status: complete
---

# Phase 13 Plan 03: The single-pass recording duty Summary

**The evidence that unblocked this phase after three cycles is now durable outside the planning directory — the axis list runs 1 through 9 with the `WFItems` row wrapper recorded as its own container defect, `BD-07` and `BD-08` carry both donor findings with their unsettled boundaries intact, `docs/BUILD-NOTES.md` §28 holds the decrypts, the measured inventories, the verbatim guard transcripts and the ordering mask, and both refuted counts are closed as a class by a whole-tree sweep rather than by fixing the two sites anyone happened to remember.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2
- **Files modified:** 6 (five edited, one moved with `git mv`)

## Accomplishments

- **Extended the axis list to nine, and got the taxonomy right.** The `WFItems` row wrapper is axis **8** and is stated explicitly as a **container** defect — at a defective site the envelope inside `WFValue` is *already correct*, so a type-scoped sweep hunting a wrong string envelope is structurally blind to it. Filing it under axis 2 would have taught the next reader to look for the wrong thing. Axis **9** is the compound-versus-scalar reader rule. Axis **7** was *extended*, not duplicated, with the `pending_exit` container/leaf pattern, because that is the same rule made concrete rather than a tenth one.
- **Carried all three of wave 2's corrections into the prose record verbatim.** The "14 sites" figure is **zero**. `if_block("Previous Respected", 4, …)` is **not a member of the family** — it passes a raw Python literal and never a `token()`, so the ROADMAP's "concrete starting site" was a false lead and this is a *corrected attribution*, not a second defect. The raw-literal comparison-target question is **unsettled by decision**, needing a rung-4 one-action donor, and is written that way in three places.
- **Closed the refuted counts as a CLASS.** A dry run before the task found **eleven** untombstoned survivors: `ROADMAP.md:36` (the milestone checklist bullet, ~550 lines above the phase section and outside any section-scoped edit), `ROADMAP.md:591`, `ROADMAP.md:598`, five in `HANDOFF.md`, and three in the pending todo. All eleven are closed; the final sweep over six literal phrasings across `.planning/` and `docs/` returns **zero** survivors outside the two deliberate exemptions.
- **Preserved history everywhere it is load-bearing.** `HANDOFF.md` keeps every original sentence and gains five dated annotations beside them. The closed todo keeps its entire original text above a tombstone written to be read standalone by someone who never opens this phase's planning directory — which is the only thing that stops the counts coming back.
- **Wrote the unsettled items down as unsettled.** `WFItemType` beyond `0`, the cause of the 2026-08-14 red render, and the pure-literal comparison target each appear as explicitly open, with their risk, in BD-07/BD-08, in §28's assumptions block, and in the closed todo.
- **Recorded the screenshot's absence as a finding rather than a gap.** Absent from the worktree, the main checkout and git history — verified three ways — with a `U+2060` word joiner in its recorded filename, and the explicit statement that **no task in this phase depended on reading it** because both defects were established independently and more precisely without it.

## Task Commits

Each task was committed atomically:

1. **Task 1: extend the axis list to nine and record `BD-07`/`BD-08`** — `45104a8` (docs)
2. **Task 2: write the Phase 13 BUILD-NOTES record and close the refuted counts as a class** — `25ae8d4` (docs)

## Files Created/Modified

- `.claude/CLAUDE.md` — heading and the §9 `/ponytail` row both moved to `nine parameter-defect axes`; axis 7 extended with the `pending_exit` container/leaf paragraph; axes 8 and 9 added.
- `docs/CAPABILITY-DECISIONS.md` — two table-of-contents rows plus `BD-07` (Donor 5, conditional operand, settled already-correct) and `BD-08` (Donors 4 / 4.1, `WFItems` row wrapper, with Donor 4.1's `WFNumberValue` bonus finding recorded as confirmation of `if_block()`, not a change request).
- `docs/BUILD-NOTES.md` — new `## 28. Phase 13 — the recording duty: three decrypts, a refutation, and two guards`, following §27's shape.
- `.planning/ROADMAP.md` — the Phase 13 milestone checklist bullet rewritten to the measured scope; the phase section's Goal, both family paragraphs and Deliverables rewritten with a dated correction note. Structural lines untouched.
- `.planning/debug/HANDOFF.md` — five dated `REFUTED` / `SUPERSEDED` annotations at `:155` (axis-6 tally), the donor table (Donor 5's never-analysed status), the two §6 SPUN OFF bullets (the `WFItems` count and the false-lead attribution), and the §9 todo filing entry. No original sentence deleted.
- `.planning/todos/pending/…` → `.planning/todos/completed/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` — moved with `git mv`, with a `## Closed — 2026-08-17, Phase 13` tombstone appended.

## Decisions Made

- **Axis 9's four `COMPOUND_STATE_KEYS` members were lifted from the source frozenset, not from the research document.** `13-RESEARCH.md`'s doc-update table listed `recent_sessions`, `exit_events`, `exit_stats.<name>.samples` and `profile_snapshot.enabled_exits`; the frozenset in `tools/build_state_engine.py` actually holds `recent_sessions`, **`recent_contracts`**, `exit_events` and `profile_snapshot.enabled_exits`, with `exit_stats.<name>.samples` recorded *beside* it as the dynamically-keyed fifth instance a literal-key scan cannot match. The plan's instruction was to lift it faithfully from the source rather than paraphrase, so the axis names the frozenset's four and records the fifth exactly as the source does. Transcribing the research table instead would have laundered a small error into ground truth (threat T-13-17).
- **The `pending_exit` pattern extends axis 7 instead of becoming axis 10.** Adding it as its own axis would have implied a defect class distinct from "state shape must exist before it is read", when it is that rule's second half: seeding is worthless if a later write replaces the container wholesale.
- **`BD-08` records Donor 4.1's numeric-RHS finding as confirmation, not a change request.** `if_block()` already implements all three cases (string RHS, numeric `WFNumberValue` serialized as a string, and existence-family carrying neither) correctly. Writing it as a finding to act on would have invented work.
- **Marker casing was treated as a contract, and the failure was fixed at the named line.** The sweep's ±12-line window matches case-sensitively while the BUILD-NOTES section assertion accepts either case. `BD-08` quoted the original `2 confirmed instances` wording with its `REFUTED` marker more than twelve lines above; the sweep named `docs/CAPABILITY-DECISIONS.md:967` and the fix was to add the uppercase marker **at that line**, not to widen the window.
- **CIRC-04 and ROOM-03 were recorded as having no defect site.** Both plan and research are explicit that inventing work to "address" them would be the dishonest outcome. §28 states the regression-protection position and names the two checkers that hold it.
- **`docs/manifest_check.py` left red, unchanged.** Its failure is the expected D-04 consequence of wave 1's rebuild. No MANIFEST row was edited and the checker was not weakened.

## Deviations from Plan

None — plan executed exactly as written. No deviation rule was invoked and no auto-fix was required.

Two observations worth recording precisely rather than smoothing over, because each *looks* like a discrepancy and is not:

- **Two verify-block failures occurred and both were content gaps in this plan's own output, not defects in the checks.** (1) §28 described the guard failures as "exited 1" and quoted their messages without ever writing the literal `SystemExit`; the plan's acceptance criteria require the verbatim `SystemExit` texts to be *labelled as such*, so the section now names the convention and the AST evidence behind it (zero `ast.Assert`, one raise in the new guard, exactly two in the extended one). (2) The marker-casing hazard fired exactly where the plan's `<phase_critical_context>` warned it would, in `BD-08`. Both were fixed by adding the missing content at the named location; neither check was relaxed.
- **Task 2's commit shows one file deletion.** `git diff --diff-filter=D` reports `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md`. This is the intentional `git mv` — the same filename is created under `completed/` in the same commit, and git recorded the pair as a rename with modification (`RM`). No content was lost.

## Issues Encountered

None beyond the two verify failures described above, both self-diagnosing and both resolved by writing the missing content rather than by weakening a check.

## Verification Results

| Check | Result |
|---|---|
| Worktree branch / base assertion before any edit | `worktree-agent-a64c5b743d19e705c`, base `3904534…` — both match |
| Axis list under the generator-authoring heading | items `1.` … `9.`, in order |
| Axis 8 tokens (`WFItemType`, `WFValue`, `Donor 4`, `verify_list_item_wrappers`, `container`) | all present |
| Axis 8 boundary statement (only `WFItemType` `0` donor-observed) | present |
| Axis 9 tokens (`get_value`, `read_value`, `verify_compound_value_reads`) | all present; four `COMPOUND_STATE_KEYS` members named verbatim from source |
| Axis 7 extension (`pending_exit`, seed-container / write-leaves / never-condition-100) | present |
| `seven parameter-defect axes` anywhere in `.claude/CLAUDE.md` | **0 occurrences** |
| `nine parameter-defect axes` occurrences | **2** — the list heading and the §9 `/ponytail` row |
| `BD-07` / `BD-08` occurrences in `docs/CAPABILITY-DECISIONS.md` | ≥ 2 each — table of contents + section heading |
| `BD-07` body tokens (`Donor 5`, `WFTextTokenString`, `WFTextTokenAttachment`, `REFUTED`) | all present; both open questions recorded as unsettled |
| `BD-08` body tokens (`WFItemType`, `Donor 4.1`, `WFNumberValue`, `660`) | all present |
| `docs/BUILD-NOTES.md` Phase 13 section | `## 28.` — matched as a numbered section |
| §28 tokens (`Donor 5`, `Donor 4.1`, both guard names, `SystemExit`, `660`, `CIRC-04`, `ROOM-03`) | all present |
| §28 placeholder for gate B / signed-artifact provenance | present, labelled, **empty**, with an explicit "not guessed here" statement |
| ROADMAP Phase 13 measured tokens (`66`, `660`, `Donor 5`) | all present |
| ROADMAP `**Requirements**: CIRC-04, CIRC-07, ROOM-03, DIST-01, DIST-02` | **byte-identical** |
| ROADMAP `**Depends on:** Phase 12` | **byte-identical** |
| ROADMAP `### Phase ` heading count | **21** (≥ 20 required) — the edit was scoped, not a rewrite |
| ROADMAP milestone checklist bullet for Phase 13 | carries the measured scope; neither refuted count survives |
| `HANDOFF.md` tombstone markers | 5 dated `REFUTED` / `SUPERSEDED` annotations; both measured figures present; **every original sentence preserved** |
| **Whole-tree sweep, before the task** (dry run) | **11 untombstoned survivors** — `ROADMAP.md:36/:591/:598`, `HANDOFF.md:155/:239/:291/:298/:468`, 3 in the pending todo |
| **Whole-tree sweep, after the task** | **0 survivors** over all six literal phrasings across `.planning/` and `docs/`, outside the two deliberate exemptions |
| Sweep exemptions honoured | `.planning/todos/completed/` and `.planning/phases/13-*/` — the historical wording survives there in order to BE the tombstone |
| Pending todo path | **absent** |
| Completed todo path | **present**, containing `REFUTED`, `660` and `Phase 13`; readable standalone |
| `git status --porcelain` under `tools/` or `src/` | **nothing** — no build input touched |
| `docs/*.py` — eleven checkers | **all PASS** (`environmental_restore`, `note_identity`, `phase5`, `phase6`, `phase7`, `phase9`, `router_ui_census`, `sentient_audit`, `sentient_core`, `sequence_dispatch`, `state_engine_self_check`) |
| `docs/manifest_check.py` | **EXPECTED RED (D-04)** — `AssertionError: row 'Core source': MANIFEST declares 2831992 bytes, src/PROSOCHE-Dumb.xml is 2916560 bytes` — byte-identical to the failure 13-01 and 13-02 recorded. Not silenced, no MANIFEST row edited, checker not weakened. Plan 13-04 owns it |
| Build / validator / signer runs in this plan | **none** — no generator, artifact or checker was touched |
| File deletions | one, intentional: the `git mv` of the todo, recorded by git as `RM` with the file present at its new path in the same commit |

## Known Stubs

None. No hardcoded empty value, placeholder string, TODO, FIXME or unwired component was introduced.

The one placeholder this plan writes is **deliberate and plan-mandated**: §28's clearly-labelled empty subsection for the gate B advisory read and signed-artifact provenance, which plan 13-04 owns. It is not a stub — it is labelled as owned elsewhere, it carries an explicit statement that its contents are **not guessed here**, and the section states plainly that no wave-3 plan ran a build, a validator gate or a signer, so nothing in §28 is evidence about the shipped artifacts.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or trust-boundary schema change. The register's `mitigate` dispositions are discharged as planned:

- **T-13-15 (Repudiation, the refuted counts across four records)** — every asserting record corrected in place or annotated with a dated tombstone naming the donor evidence; the closed todo is readable standalone; `HANDOFF.md` keeps its original sentences beside the annotations.
- **T-13-29 (Repudiation, an assertion at a site nobody enumerated)** — closed by a whole-tree sweep over six literal phrasings, which found **eleven** sites where plan review had measured two. Enumeration would have left nine open.
- **T-13-16 (Tampering, `.planning/ROADMAP.md`)** — scoped replacements only; the `**Requirements**:` and `**Depends on:**` lines are byte-identical and 21 `### Phase ` headings survive.
- **T-13-17 (Spoofing, transcribed figures)** — every figure comes from `13-01-SUMMARY.md`, `13-02-SUMMARY.md` or `13-RESEARCH.md`'s measured tables. The one place a source disagreed with the research document — `COMPOUND_STATE_KEYS`' membership — was resolved in favour of the source, as recorded above.
- **T-13-18 (Repudiation, unsettled written as settled)** — `WFItemType` beyond `0`, the 2026-08-14 red render's cause, and the pure-literal comparison target are each written as explicitly unaudited in `BD-07`/`BD-08`, §28's assumptions block, and the closed todo.
- **T-13-19 (Elevation of privilege, ingested prose as instruction)** — the donor XML, the ROADMAP prose and the todo text were transcribed as data. No text lifted from them was executed and no directive found inside a quoted record changed what this plan did.
- **T-13-20 / T-13-SC (accept)** — unchanged: everything recorded is generator structure, action indices and hashes of locally-built artifacts; no package-manager install was run and no dependency file was touched.

## User Setup Required

None.

## Next Phase Readiness

**Ready.** Plan **13-04** starts from exactly the baseline waves 1–2 handed it, untouched by this plan:

- Both source XMLs are unchanged at `99388cad…` (Core) and `d01154b3…` (Aware) and remain gate-A clean; no generator, artifact or checker was modified here.
- `docs/manifest_check.py` is red for exactly one known reason, with all six MANIFEST size/SHA-256 rows stale.
- `docs/BUILD-NOTES.md` §28 carries a labelled, empty subsection reserved for 13-04's gate B advisory read and signed-artifact provenance. Its contents are deliberately not guessed.

**Carried forward, not blockers.** Assumptions **A1–A4** remain open and are now recorded in `docs/` rather than only in planning prose. Two belong to **Phase 19 device UAT**: that the Mirror renders non-empty text over a wrapped List (A4), and that the variable-bearing conditional operands render as valid non-red chips (A1). Phase 19 must test a **re-imported** build — a user still running the previously signed artifact keeps the blank-row Mirror until they re-import, and testing a stale install would observe the old defect and misattribute it to a fix that did land.

## Self-Check: PASSED

- `.claude/CLAUDE.md` — FOUND
- `docs/CAPABILITY-DECISIONS.md` — FOUND
- `docs/BUILD-NOTES.md` — FOUND
- `.planning/ROADMAP.md` — FOUND
- `.planning/debug/HANDOFF.md` — FOUND
- `.planning/todos/completed/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` — FOUND
- `.planning/todos/pending/2026-08-15-fix-red-operator-and-list-wrapper-defects.md` — correctly ABSENT
- `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-03-SUMMARY.md` — FOUND
- Commit `45104a8` — FOUND in `git log`
- Commit `25ae8d4` — FOUND in `git log`
- No modification under `tools/` or `src/` at any commit point
- `.planning/STATE.md` untouched — the orchestrator owns that write

---
*Phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper*
*Completed: 2026-08-17*
