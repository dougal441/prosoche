---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 03
subsystem: infra
tags: [shortcuts, plist, note-identity, attachment-offsets, dante, bd-06-a1, ios26]

# Dependency graph
requires:
  - phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-01
    provides: "tools/plist_text_edit.py (the guarded round trip every copy edit in this plan went through) and docs/note_identity_check.py (the twelfth checker, whose EXPECTED_TITLE constant made the three-site rename a one-line edit instead of a three-site hunt)"
  - phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-02
    provides: "the BD-06 roster live on exact-match dispatch, and the twelve-green baseline this plan started from"
provides:
  - "The Apple Note's user-facing title is the bare product name PROSOCHĒ at all three identity sites, in both forks, asserted against one constant"
  - "docs/CAPABILITY-DECISIONS.md BD-06-A2 — the declined Find-Notes operator change, its two reasons, and the donor export that would settle it"
  - "tools/build_state_engine.py CIRCLE_NAMES + circle_menu_title() — Dante's nine positional names as one source of truth, from which the Test-a-Circle submenu derives BOTH its items and its case titles"
  - "Two new stable Note sections: ## THE NINE CIRCLES and ## OPTIONAL HARDENING, both placed upstream of the machine-appended tail"
  - "BD-06-A1 applied in full: the middle profile is Purgatory everywhere, and Limbo names exactly one thing — Circle 1"
affects: [11-04 schema_version, 11-05, 11-06 Core/Aware rename, 15 Voice primitive, 17 Redirect primitive]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A menu's items and its case titles are derived from ONE expression, making drift unrepresentable rather than merely unlikely"
    - "A declined change is recorded as a first-class decision record naming the evidence that would reverse it, not left as a silent non-action"
    - "A rename whose key path is read with dot notation is swept by class in one commit, because a dotted read with a missing segment is a hard error in this runtime"
    - "A negative assertion over surviving occurrences ('every remaining X is role Y') rather than an absence assertion, when the word legitimately survives in another role"

key-files:
  created: []
  modified:
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - src/CONFIG-BLOCK.md
    - tools/build_state_engine.py
    - docs/note_identity_check.py
    - docs/state_engine_self_check.py
    - docs/CAPABILITY-DECISIONS.md
    - docs/BUILD-NOTES.md
    - artifacts/shortcuts/MANIFEST.md

key-decisions:
  - "The Find-Notes lookup operator was RETAINED at 99 ('contains') rather than tightened to 4. RESEARCH §6.2 recommended the move; 99 is BOOT-08's recorded decision and 4 is UNVERIFIED for a WFContentPredicateTableTemplate on the Notes Name property, so moving it would have been inference against a recorded decision. Mitigated in Note copy, pinned in the checker, recorded as BD-06-A2"
  - "## OPTIONAL HARDENING sits beside the target-app guidance rather than at the Note's tail, as the addendum literally says. manual_note_refresh() appends to the tail on every state-changing manual run, so a tail section is progressively buried under machine-appended duplicates"
  - "The Purgatory rename swept ALL THREE bare 'Limbo' Text actions including the generator-owned one, rather than the two the generator does not rewrite. Hunting two of three is the exact partial-rename shape this project's history records as its recurring defect"
  - "Signing and the MANIFEST row refresh were run at EVERY task boundary, not only at Task 3, because manifest_check goes red on every rebuild and both earlier tasks required twelve green at their commit"
  - "Task 3 did not re-sign: both builders left both sources byte-identical to what Task 2 signed"
  - "docs/BUILD-NOTES.md's five historical 'Limbo' references were NOT rewritten. The file is append-only; §23 states that every prior occurrence is a historical profile reference superseded by BD-06-A1"

requirements-completed: [ROOM-01, ROOM-02, DIST-01]

coverage:
  - id: N1
    description: "The Note's user-facing title is the bare product name at all three sites that decide it — the Find-Notes predicate, the body H1, and the Create Note name parameter — in both forks"
    requirement: "ROOM-01"
    verification:
      - kind: integration
        ref: "docs/note_identity_check.py exit 0: 'three identity sites agree on PROSOCHĒ (Name operator 99)' for Dumb and Sentient"
        status: pass
      - kind: integration
        ref: "decrypted payload of both signed containers: predicate == title == 'PROSOCHĒ', H1 == '# PROSOCHĒ', Operator 99"
        status: pass
    human_judgment: false
  - id: N2
    description: "The internal Control Room name is unchanged everywhere it is not user-facing"
    requirement: "ROOM-01"
    verification:
      - kind: unit
        ref: "docs/phase7_self_check.py exit 0 (the 'Open Control Room' menu item); inspect.getsource() finds 'Control Room Note', 'Open Control Room' and 'gate_control_room_shownote' still present"
        status: pass
    human_judgment: false
  - id: N3
    description: "Attachment offsets survive every copy edit — all of which sat upstream of the Note body's two placeholders"
    requirement: "ROOM-01"
    verification:
      - kind: integration
        ref: "docs/note_identity_check.py: 1105 (Dumb) / 1109 (Sentient) token strings, 0 attachment-offset mismatches, checked document-wide not only at the edit sites"
        status: pass
      - kind: integration
        ref: "same invariant re-measured on both decrypted signed payloads: same counts, 0 mismatches; plutil -lint OK on both"
        status: pass
    human_judgment: false
  - id: N4
    description: "Dante's nine names are surfaced positionally from one generator constant, so menu items and case titles cannot drift apart"
    requirement: "ROOM-02"
    verification:
      - kind: unit
        ref: "CIRCLE_NAMES == the nine canonical names in Dante order; 'positional' appears within 400 chars of the constant; circle_menu_title referenced 4 times"
        status: pass
      - kind: integration
        ref: "per fork and per decrypted payload: WFMenuItems == the nine WFMenuItemTitle values, element for element and in order"
        status: pass
    human_judgment: false
  - id: N5
    description: "The Note explains that a user may add the Shortcuts app itself to their target-app list as optional extra protection"
    requirement: "ROOM-02"
    verification:
      - kind: integration
        ref: "'## OPTIONAL HARDENING' present in note-body copy in both forks and on 1 line of each decrypted payload, mentioning the Shortcuts app"
        status: pass
    human_judgment: false
  - id: N6
    description: "BD-06-A1's profile rename is COMPLETE, not partial — thresholds.Purgatory and cooldown_seconds.Purgatory resolve, the Limbo keys are absent, and every surviving Limbo is a Circle-1 name"
    requirement: "ROOM-02"
    verification:
      - kind: integration
        ref: "parsed Config literal per fork and per payload: thresholds/cooldown_seconds keyed by exactly {Paradise, Purgatory, Inferno}; Purgatory holds [3,5,7,9,11,13,16,19,22] and 180; Limbo absent from both"
        status: pass
      - kind: integration
        ref: "full document walk per fork and per payload: exactly 3 surviving 'Limbo' strings, every one a 'Circle 1 · Limbo' label containing exactly one occurrence"
        status: pass
      - kind: unit
        ref: "docs/state_engine_self_check.py exit 0 with its threshold key renamed and the array unchanged; src/CONFIG-BLOCK.md's fenced literal parses and mirrors the live one exactly"
        status: pass
    human_judgment: false
  - id: N7
    description: "Running either builder twice produces byte-identical output"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "second and third consecutive builds leave src/PROSOCHE-Dumb.xml at 1e5bf2bd… and Sentient at 567befdb…; git status --short clean of src/ after the Task-3 rebuild"
        status: pass
    human_judgment: false
  - id: N8
    description: "Both forks validate, sign under their canonical display names, decrypt-verify to contain the new sections, and the MANIFEST matches disk"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "validate-shortcut ×2 --target-macos 26 --target-platform all -> 'Validation passed.'; aea decrypt + aa extract + plutil -lint OK ×2; docs/manifest_check.py -> 6 rows verified against disk"
        status: pass
      - kind: integration
        ref: "dated archive SHA-256 equals its src/ counterpart for each fork; signed basenames are the exact canonical display names with no suffix"
        status: pass
    human_judgment: false
  - id: N9
    description: "The Find-Notes lookup binds to the intended Note on a device that also holds a Note left over under the old two-part title"
    verification: []
    human_judgment: true
    rationale: "DIST-03 is open — no iPhone is connected, and com.apple.mobilenotes is absent from the booted simulator, so this is not reachable below rung 3 of the evidence ladder. The operator is still 'contains', so a leftover Note DOES match the new predicate; the mitigation is a user instruction in the Note, not a mechanism. Recorded as BD-06-A2 with the donor export that would settle whether Operator 4 is even available for this filter template."
  - id: N10
    description: "A manual run interrupted between the Find-Notes lookup and the append, or two overlapping runs, can lose an append or duplicate a block"
    verification: []
    human_judgment: true
    rationale: "Authored as a backstop truth in the plan, and it abstains rather than passing. Shortcuts offers no transaction and no lock, so the guarantee is at-most-one-note-bound-per-run and nothing stronger. Nothing in this plan changes that, and nothing in this plan can prove it either way without a device."

# Metrics
duration: 78min
completed: 2026-08-17
status: complete
---

# Phase 11 Plan 03: The Note rename, the Dante name surface, and Purgatory Summary

**The product's entire control surface got its real name, its nine depths were named for the first time from a single constant that makes menu drift unrepresentable, and a word that had quietly come to mean two things was reduced to meaning one — with the attachment-offset invariant armed through every edit and the one change that could not be verified declined and recorded rather than guessed.**

## Performance

- **Duration:** ~78 min
- **Tasks:** 3 (all `type="auto"`)
- **Files modified:** 9 source/doc files, plus 4 build artifacts and 4 new dated archives

## Accomplishments

- **The Apple Note is now titled `PROSOCHĒ`, at all three sites that decide its identity.** PROSOCHĒ finds its Note by *name*, and three separate strings spell that name: the `filter.notes` lookup predicate, the H1 a person reads, and the `SharingExtension` `name` parameter. If the predicate and the title ever disagree, PROSOCHĒ creates a Note it can never find again and appends the ledger to a fresh one on every state-changing run — silently, invisibly to every check. All three moved in one commit and are asserted against one `EXPECTED_TITLE` constant.
- **The internal name did not move.** `Open Control Room`, the `Control Room Note` variable, the structural comment anchors and the three `*_control_room_*` / notes-fixing function names are untouched, per commit `e84ee77`. `docs/phase7_self_check.py` is green.
- **Every attachment offset survived.** The Note body carries two `attachmentsByRange` keys at the tail; every edit in this plan — the H1, the stale-note paragraph, two whole new sections — sat *upstream* of both. All went through `tools/plist_text_edit.py`'s guarded round trip. **1,105 (Dumb) / 1,109 (Sentient) token strings, 0 mismatches**, measured document-wide in `src/` *and* re-measured on both decrypted signed payloads.
- **Dante's nine names exist, and the menu cannot drift.** `CIRCLE_NAMES` is one module-level tuple; `circle_menu_title()` is one expression; the Test-a-Circle submenu builds **both** its `WFMenuItems` array and every case's `WFMenuItemTitle` from it. Items equal case titles element-for-element by construction, not by review — which matters because a `choosefrommenu` whose titles drift from its items is the top documented real-world failure mode for that action. Eight of the nine names were measured absent from the artifact, so this *added* a surface rather than renaming one.
- **`Limbo` now means exactly one thing.** BD-06-A1 renamed the middle profile to `Purgatory`, making the three profiles the three canticles. The rename was total by necessity: a profile name is a live dotted Config key path, and a dotted read with a missing segment is a **hard error** in this runtime, so a half-done rename is a crash rather than a degradation. Verified per fork and per shipped payload that exactly three `Limbo` strings survive and every one is a `Circle 1 · Limbo` label.
- **The one change that could not be verified was declined, not guessed.** RESEARCH recommended tightening the lookup operator from `contains` to `is`. It was retained, mitigated in copy, pinned in the checker, and recorded as `BD-06-A2` naming the exact donor export that would settle it.

## Task Commits

1. **Task 1: Rename the Note at its three identity sites, offsets recomputed** — `a6de6ed` (feat)
2. **Task 2: Surface the nine Dante names, add optional hardening, rename the profile to Purgatory** — `e84af34` (feat)
3. **Task 3: Rebuild, validate, decrypt-verify and record the wave** — `5b18576` (docs)

## The Note, as it now reads

Heading order in the body, asserted in both forks and both decrypted payloads:

```
# PROSOCHĒ
## READ THIS FIRST            <- gained the stale-note instruction
### Automation A — OPEN
### Automation B — CLOSE
## Do not target these apps
## OPTIONAL HARDENING          <- new
## THE NINE CIRCLES            <- new
## MY PHONE, ON PURPOSE        <- the user-editable proforma
## CURRENT SETTINGS  /  ## CURRENT STATE  /  ## ATTENTION LEDGER
## VALUE / LIFE RETURNED  /  ## SUPPORT PROSOCHĒ
```

Both new sections sit **before** the proforma. `manual_note_refresh()` appends a fresh
settings/state/ledger block to the **tail** on every state-changing manual run, so anything
placed at the end is progressively buried under machine-appended duplicates.

## Files Created/Modified

- `tools/build_state_engine.py` — new `CIRCLE_NAMES` (nine names, canonical order, index 0 == Circle 1) and `PROFILE_NAMES` (the three canticles) constants with their rationale recorded at the constant; new `circle_menu_title()`; the Test-a-Circle submenu's items and case titles both derived from it; the profile menu's items and cases both derived from `PROFILE_NAMES`; `fix_notes_filter_limit()`'s docstring no longer quotes the old title as the live predicate.
- `docs/note_identity_check.py` — `EXPECTED_TITLE` is the bare product name; `EXPECTED_NAME_OPERATOR`'s comment rewritten from "RESEARCH proposes moving it" to the record of why it was **not** moved, naming BOOT-08 and BD-06-A2.
- `docs/state_engine_self_check.py` — `THRESHOLDS` key `Limbo` → `Purgatory` (array unchanged), and both `circle(...)` assertions follow.
- `src/PROSOCHE-Dumb.xml` — three identity sites, one new `## READ THIS FIRST` paragraph, two new body sections, three bare `Limbo` Text actions, the Config literal's two profile keys, the normalisation comment, and the import question's default and prompt. 2,667,477 → 2,669,198 bytes.
- `src/PROSOCHE-Sentient.xml` — regenerated from the fresh Dumb source; never hand-edited. 2,704,157 → 2,705,878 bytes.
- `src/CONFIG-BLOCK.md` — literal, two field-reference rows, the transcription-recipe example, and a dated change-log entry recording the rename and why it had to be total.
- `docs/CAPABILITY-DECISIONS.md` — **BD-06-A2** appended (154 insertions, **0** deletions).
- `docs/BUILD-NOTES.md` — **§23** appended (161 insertions, **0** deletions).
- `artifacts/shortcuts/MANIFEST.md` — six rows refreshed from disk at each signing; header and evidence paragraphs rewritten around this wave; a new warning banner covering the renamed Note, the retained `contains` operator and the `Purgatory` key-path change.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Dumb,Sentient}.shortcut` — re-signed (219,923 B / 224,186 B).
- `artifacts/shortcuts/2026-08-17/…-1122*.xml` and `…-11294*/…-1130*.xml` — four new dated pre-sign archives, each byte-identical to its `src/` counterpart.

## Decisions Made

- **The lookup operator stays at `contains`.** Two independent reasons, either sufficient: it is BOOT-08's recorded decision taken against the documented Find-Notes name-matching trap, and `Operator: 4` is UNVERIFIED for a `WFContentPredicateTableTemplate` on the Notes `Name` property — the condition-code table documents `4` for `WFCondition` on *conditionals*, and no donor, golden shortcut or catalog entry covers the filter-template case. Changing it would have been inference against a recorded decision.
- **The Purgatory rename swept all three bare `Limbo` Text actions, including the generator-owned one.** Two of the three are hand-held; the third is rewritten by the builder on the next run anyway. Renaming it here is redundant rather than wrong — and hunting two of three is precisely the partial-rename shape this project's debug history records as its recurring defect (147, 367, 25, 20 and 8 sites).
- **`docs/BUILD-NOTES.md`'s historical `Limbo` references were not rewritten.** BD-06-A1 lists the file in the rename scope, but the file is append-only and those five records were true when written. §23 states instead that every prior occurrence is a historical profile reference superseded by the amendment.
- **No disambiguation line was written anywhere.** BD-06-A1 eliminates `T-11-16` rather than mitigating it; there is nothing left to disambiguate. Asserted negatively per fork.
- **Circle 0's name, "The Indifferent", reached no user-facing surface.** It is in `docs/CAPABILITY-DECISIONS.md` BD-06-A1 and `docs/BUILD-NOTES.md` §23 and nowhere else. The Note's legend lists **nine** Circles, the Test-a-Circle menu offers nine, and `verify_circle_zero_silence()` is unmodified and green.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocking] Signing and the MANIFEST row refresh were run at every task boundary, not only at Task 3**

- **Found during:** Task 1, at the acceptance-criteria sweep
- **Issue:** `docs/manifest_check.py` recomputes every declared size and hash from disk, so it goes red on **every** rebuild until the MANIFEST is refreshed — which requires current signed artifacts. Tasks 1 and 2 both require all twelve checks green at their commit boundary, while the plan assigns signing to Task 3. The criterion was unsatisfiable as written. Wave 2 hit the identical conflict and resolved it the same way.
- **Fix:** Both forks validated, signed under their exact canonical display names with an explicit `--name`, and the six MANIFEST **rows** refreshed from disk at the end of Task 1 and again at the end of Task 2. The MANIFEST's *prose* was rewritten once, in Task 3, so the expensive part was not repeated. Task 3 then re-ran the full pipeline, found both sources byte-identical to what Task 2 signed, and did **not** re-sign.
- **Files modified:** `artifacts/shortcuts/MANIFEST.md`, both signed `.shortcut` files, four new dated archives
- **Verification:** `docs/manifest_check.py` — "passed (6 rows verified against disk)" at all three commit boundaries.
- **Committed in:** `a6de6ed`, `e84af34`

**2. [Rule 1 — Bug] `fix_notes_filter_limit()`'s docstring quoted the old title as the live predicate**

- **Found during:** Task 1
- **Issue:** `tools/build_state_engine.py:3103` stated the artifact's search predicate as `Name contains "PROSOCHĒ — Control Room"`. After the rename that sentence is simply false, and it is the one place in the generator that describes the lookup's shape to a future reader.
- **Fix:** Rewritten to name the current title, to record that it was shortened by plan 11-03, and to state that the Operator is still 99 and pinned by `docs/note_identity_check.py`. This is a factual correction to a docstring, **not** a rename of the internal Control Room name — the function name, the `Control Room Note` variable and every other internal reference are untouched.
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** the internal-name assertion (`'Control Room Note'`, `'Open Control Room'`, `'gate_control_room_shownote'` all present) passes; `docs/phase7_self_check.py` green.
- **Committed in:** `a6de6ed`

### Deliberate deviations from the plan text

**3. `## OPTIONAL HARDENING` is not at the Note's tail**

Build Addendum 01 §3 says the instruction goes "at the end of the Note". It was placed immediately after `## Do not target these apps` instead. `manual_note_refresh()` appends a fresh `## CURRENT SETTINGS` / `## CURRENT STATE` / `## ATTENTION LEDGER` block to the end on every state-changing manual run, so the Note grows monotonically and a tail section is progressively buried under machine-appended duplicates. A section a user is meant to read once and act on cannot live where the machine writes. It is also topically the same subject as the target-app guidance. **This deviation was anticipated and authorised by the plan**, which asked for it to be recorded here; it is also recorded in `docs/BUILD-NOTES.md` §23.3.

**4. `docs/BUILD-NOTES.md`'s three deleted lines against the phase baseline are not this plan's**

The plan's Task-3 acceptance criterion asks that `git diff --numstat f4e47f9 -- docs/BUILD-NOTES.md` show a deletion count of exactly `0`. It reports `408 3`. The three deletions belong to commit `e768b93`, the `260817-ewg` quick task that superseded a falsified `--target-platform ios` paragraph between the phase baseline and this wave — work this plan neither performed nor could avoid. **This plan's own change is `161 0`**, measured as `git diff --numstat HEAD -- docs/BUILD-NOTES.md` immediately before the Task-3 commit. The criterion's intent — that this plan appends and deletes nothing — is met in full.

**5. The plan's original acceptance criterion asserting the profile menu still reads `['Paradise','Limbo','Inferno']` was withdrawn**

Superseded by BD-06-A1, a user decision taken the same day. The menu now reads `['Paradise','Purgatory','Inferno']`, and threat `T-11-16` is **eliminated** rather than mitigated. Recorded here because the plan file carries both the withdrawn text and the amendment, and a future reader should not mistake the withdrawal for an oversight.

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug), 3 recorded deliberate deviations
**Impact on plan:** No scope creep. No additional primitive, Circle, sequence cell, checker or generator function was touched beyond what the plan and BD-06-A1 name. No Rule-4 architectural decision arose.

## Issues Encountered

None that required problem-solving. Both signings succeeded first time on both occasions; neither documented `sign-shortcut` quirk occurred. `timeout` was never invoked, `--target-macos 27` was never used, and `--target-platform ios` was never used. No `git clean`, `git stash` or destructive reset was run at any point.

Two of the plan's `<automated>` verify commands were adjusted where they were self-defeating rather than where the artifact was wrong: the plan's `git diff --numstat f4e47f9` criterion (deviation 4 above), and an over-strict text grep asserting the old two-part title survives *nowhere* — it necessarily survives at exactly one site, quoted inside the stale-note instruction that exists to warn about it. That site is asserted individually instead, and every other occurrence is proven absent by a full document walk.

## Verification Evidence

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run |
| No-op `plistlib` round trip before each guarded edit | 2,667,477 == 2,667,477; 2,667,711 == 2,667,711 |
| `tools/build_state_engine.py` / `tools/build_sentient.py` | exit **0**, three times each |
| Idempotence | second and third consecutive builds leave both sources byte-identical (`1e5bf2bd…` / `567befdb…`) |
| Twelve `docs/*.py` checks | all exit **0**, at **all three** commit boundaries |
| Note identity, both forks | three sites agree on `'PROSOCHĒ'`, Name operator **99** |
| `EXPECTED_TITLE` / operator pin | `EXPECTED_TITLE = "PROSOCHĒ"` ×1; `Operator` and `BOOT-08` both present in the checker |
| Internal name preserved | `docs/phase7_self_check.py` exit 0; `Control Room Note`, `Open Control Room`, `gate_control_room_shownote` all still in the generator |
| Attachment invariant, `src/` | **1,105** (Dumb) / **1,109** (Sentient) token strings, **0** offset mismatches, document-wide |
| Attachment invariant, decrypted payloads | same counts, **0** mismatches |
| Old two-part title | exactly **1** surviving site per fork — the `## READ THIS FIRST` stale-note instruction that quotes it |
| `CIRCLE_NAMES` | exactly the nine canonical names in Dante order; "positional" recorded within 400 chars of the constant |
| Test-a-Circle submenu | `WFMenuItems` == the nine `WFMenuItemTitle` values, element for element, both forks **and** both payloads |
| Note-body heading order | do-not-target < OPTIONAL HARDENING < THE NINE CIRCLES < MY PHONE, both forks and both payloads |
| Profile menu | `['Paradise', 'Purgatory', 'Inferno']`, exactly one per fork and per payload |
| Config literal keys | `thresholds` and `cooldown_seconds` keyed by exactly the three canticles; `Purgatory` holds `[3,5,7,9,11,13,16,19,22]` and `180`; `Limbo` absent from both |
| Import question | `DefaultValue` == `Purgatory`; prompt names Purgatory and not Limbo |
| Bootstrap normalisation | falls back to `Purgatory`; no `Limbo` in the comment |
| Surviving `Limbo` | exactly **3** sites per fork and per payload, every one a `Circle 1 · Limbo` label |
| Disambiguation line | **absent**, asserted negatively per fork |
| `src/CONFIG-BLOCK.md` | fenced literal parses; keyed by the three canticles; mirrors the live Config literal exactly; no `Limbo` key row |
| `docs/router_ui_census.py` | exit **0**, no OPEN-arm surface outside the silent band |
| Validator (gate A) ×2, `--target-macos 26 --target-platform all` | `Validation passed.`, exit 0 |
| Signed artifacts | 219,923 B / 224,186 B, canonical basenames, **no suffix** |
| Dated archive SHA-256 == `src/` counterpart | `1e5bf2bd…` == `1e5bf2bd…`; `567befdb…` == `567befdb…` |
| Decrypt-verify, both containers | `plutil -lint` **OK** ×2; `THE NINE CIRCLES` **1** line each; `OPTIONAL HARDENING` **1** line each |
| `docs/manifest_check.py` | passed, 6 rows verified against disk, at all three commit boundaries |
| `docs/CAPABILITY-DECISIONS.md` vs `f4e47f9` | `154 0` — pure append |
| `docs/BUILD-NOTES.md` vs `HEAD` at Task 3 | `161 0` — pure append |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked |

**Every row above is structural.** `DIST-03` — device verification — remains **open**: no iPhone is connected, nothing in this plan has been observed running, and no claim to the contrary appears in any artifact this plan wrote.

## Flagged assumptions owned by this plan

- **The retained `contains` operator (BD-06-A2).** The shortened title genuinely widens what the lookup can match, and the mitigation is a *user instruction in the Note*, not a mechanism. **Assumed: a user who reads `## READ THIS FIRST` and deletes or renames an old-titled Note avoids the wrong-Note binding.** That assumption is unfalsifiable without a device holding both Notes. The evidence that would let us replace the instruction with a mechanism is named precisely in BD-06-A2.
- **Both forks still create a Note with the same title.** Pre-existing, not introduced here, but sharper now that the title is shorter. A user who installs both forks has one Note and two writers. **Assumed: giving the forks distinct Note titles belongs with the Dumb→Core / Sentient→Aware rename in plan 11-06, not with a copy change.**
- **BD-06-A1's accepted breakage.** A device holding `profile: "Limbo"` hard-errors on `thresholds.Purgatory` at its next OPEN. **Assumed, on the user's explicit statement: PROSOCHĒ is undeployed and the only installs are the owner's own testing, so there is no population this can harm.** Recorded in the MANIFEST's warning banner so that a reader who does hold such a device is told to re-run setup rather than this build.

## Known Stubs

None introduced by this plan. The two interim states carried forward from plan 11-02 — `Loud Mirror` dispatching `mirror_and_voice()` (Phase 15 replaces it) and `Eject` holding Circle 6 in all three sequences (Phase 17 flips two cells) — are unchanged, still labelled interim in the generator, `src/CONFIG-BLOCK.md` and `artifacts/shortcuts/MANIFEST.md`, and are not this plan's to resolve.

## Threat Flags

None. This plan adds no network endpoint, no auth path and no new file-access pattern. No package was installed and no third-party import was added — every new line uses the Python standard library, so **T-11-SC** was never triggered.

The plan's own threat register closes as follows, all structurally:

| Threat ID | Disposition | Evidence at this commit |
|---|---|---|
| T-11-13 (lookup binding to a stale or foreign Note) | mitigated | operator retained per BOOT-08 rather than changed on inference; `## READ THIS FIRST` instructs deletion/rename; BD-06-A2 records the deviation and the donor test; `docs/note_identity_check.py` pins the operator |
| T-11-14 (out-of-bounds `attachmentsByRange`) | mitigated | every edit through the guarded round trip; 1,105/1,109 token strings with 0 mismatches in `src/` **and** in both decrypted payloads; `plutil -lint` OK on both |
| T-11-15 (submenu items and case titles drifting apart) | mitigated | both derived from `circle_menu_title()`; the two lists compared directly per fork and per payload |
| T-11-16 (`Limbo` meaning two things) | **eliminated** | the profile is `Purgatory`; `Limbo` survives on 3 sites per fork, all Circle-1 labels; no disambiguation line written, asserted negatively |
| T-11-16b (partial rename leaving a live `thresholds.Limbo`) | mitigated | swept by class in one commit; both the presence of every `Purgatory` key and the absence of every `Limbo` profile key asserted per fork and per payload; `docs/state_engine_self_check.py` green |
| T-11-17 (hardening making Shortcuts harder to reach) | accepted | the instruction is explicitly optional, never automated, and states that it locks nothing and is reversible by the same route; Emergency Restore remains reachable from the MANUAL arm independently |
| T-11-18 (a deviation taken silently) | mitigated | both deviations appended to `docs/CAPABILITY-DECISIONS.md` (154/0) and `docs/BUILD-NOTES.md` (161/0), with zero deletions in either |
| T-11-SC (package-manager installs) | accepted | none triggered; no install of any kind |

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **`11-04` is unblocked and lighter than planned.** BD-06-A1 answers its `schema_version` 2→3 question outright: there is no accumulated device record to discard, so a bump is free and no migration is to be built. `11-04` remains a recording task with no blocking one-way gate.
- **`11-06` inherits a sharpened decision.** Both forks still create a Note with the same title, and that title is now shorter. If the forks are to have distinct Note titles, the Dumb→Core / Sentient→Aware rename is where it belongs — and `docs/note_identity_check.py` currently asserts a single `EXPECTED_TITLE` across both forks, which is the constant that would have to become per-fork.
- **The name surface is now extensible in one place.** Any future plan wanting a Dante name in the Status alert, the Mirror templates or the Leaving prompt reads `CIRCLE_NAMES`; nothing needs to be re-derived and nothing can drift from the menu.
- **Blocker, unchanged: DIST-03 is open.** The device questions this plan specifically raises: does the `contains` lookup bind to the intended Note on a device that also holds a Note titled `PROSOCHĒ — Control Room`, and does `Operator: 4` even exist as an option for a Find Notes `Name` filter in the iOS Shortcuts UI? The second is answerable by a single donor export and would close BD-06-A2.

## Self-Check: PASSED

- `src/PROSOCHE-Dumb.xml` (2,669,198 B) / `src/PROSOCHE-Sentient.xml` (2,705,878 B) — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` (219,923 B) — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` (224,186 B) — FOUND
- `docs/CAPABILITY-DECISIONS.md` BD-06-A2 — FOUND
- `docs/BUILD-NOTES.md` §23 — FOUND
- `tools/build_state_engine.py` `CIRCLE_NAMES` / `circle_menu_title` — importable and callable — FOUND
- Commit `a6de6ed` (Task 1, feat) — FOUND in `git log`
- Commit `e84af34` (Task 2, feat) — FOUND in `git log`
- Commit `5b18576` (Task 3, docs) — FOUND in `git log`
- All twelve `docs/*.py` checks re-run green after the final task commit; working tree clean of source and artifact changes.

---
*Phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r*
*Completed: 2026-08-17*
