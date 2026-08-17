---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 02
subsystem: infra
tags: [shortcuts, plist, dispatch, build-guard, bd-06, structural-checks, ios26]

# Dependency graph
requires:
  - phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-01
    provides: "tools/plist_text_edit.py (the guarded plist round trip used for the Config literal edit), docs/note_identity_check.py (the twelfth checker), the live name Pause, and the deliberately-preserved Circle-8 orphan this plan needed to prove its new guard has teeth"
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    provides: the eleven green structural checks and the raised threshold curve whose doc mirror this plan corrected
provides:
  - "tools/build_state_engine.py verify_dispatch_coverage(actions) — the eighth defect class as a hard build guard, armed in both builders, aborting before any write"
  - "docs/sequence_dispatch_check.py promoted from reporter to hard gate: empty KNOWN_ORPHANS, four raising failure classes including BD-06's exactly-one clause"
  - "BD-06 Decision 4's whole slot table live: nine shipped primitive names in all three sequences arrays and on ninety dispatch branches, in both forks"
  - "Exact-match dispatch: condition code 4 on every Selected Primitive conditional, replacing 99"
  - "Circle 8 dispatches a real branch for the first time — CIRC-08's dispatch half closed"
affects: [11-03 Note rename, 11-04, 11-05, 11-06 Core/Aware rename, 15 Voice primitive, 17 Redirect primitive]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A build guard is authored INERT, observed raising on a live defect, and only then armed — in the same commit as the change it guards"
    - "Whole-array replacement through the guarded round trip, never per-name substitution, when retired names are substrings of their neighbours"
    - "Match semantics resolved per branch from that branch's own condition code, never from a hardcoded constant, in both the guard and the checker"
    - "Structural negative assertions over the parsed Config literal, never text greps, when retired words legitimately survive elsewhere in the artifact"

key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - tools/build_sentient.py
    - docs/sequence_dispatch_check.py
    - docs/phase5_self_check.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - src/CONFIG-BLOCK.md
    - artifacts/shortcuts/MANIFEST.md

key-decisions:
  - "The guard was authored inert in Task 1 and observed raising on the live Circle-8 orphan before Task 2 armed it. A guard never seen to fail is not a guard, and this ordering was the plan's explicit non-collapsible invariant"
  - "The guard's unknown class covers a non-str WFConditionalActionString as well as an unrecognised condition code — a strict superset of the plan's specification, so no branch can ever be silently dropped from the coverage calculation"
  - "No Python function renamed. docs/environmental_restore_check.py imports generator functions BY NAME; the tuple carries the shipped name, the function the internal one"
  - "The ash() alert BODY was rewritten, not only its title: it opened with the word Pause, which BD-06 has just made Circle 1's primitive name, so the Black and White alert read as if the other intervention had fired"
  - "Signing and the MANIFEST refresh were pulled forward into Task 2 rather than left to Task 3, because manifest_check is one of the twelve checks Task 2's acceptance criteria require green, and it cannot be green until the signed artifacts match the rebuilt sources"
  - "Task 3 did not re-sign: its change is checker-only, both builders left both sources byte-identical, and re-signing would have churned two signature hashes and orphaned two dated archives for no content change"

patterns-established:
  - "Pattern 1: the coupled halves of a cross-cutting change (roster + comparator) land in ONE commit, with the guard already hard, so either half alone fails the build"
  - "Pattern 2: an interim stand-in is labelled interim in the generator comment, in the doc mirror and in the MANIFEST, each naming the phase that replaces it"
  - "Pattern 3: a promoted gate is proven to FAIL on synthesised damage before it is trusted to pass"

requirements-completed: [AUDIT-02, CIRC-02, CIRC-06, CIRC-08]

coverage:
  - id: D1
    description: "verify_dispatch_coverage() exists, locates the Config literal by content, resolves semantics per branch, distinguishes four failure classes, and was observed raising on the live Circle-8 orphan before being armed"
    requirement: "CIRC-08"
    verification:
      - kind: unit
        ref: "python3 -c \"...b.verify_dispatch_coverage(a)\" against the unmodified src/PROSOCHE-Dumb.xml -> SystemExit naming 'Voice' at Classic/BlackMirror/Ambient Circle 8"
        status: pass
      - kind: unit
        ref: "inspect.getsource(): 'config_version' present, no actions[<int>] index addressing, 6 raise SystemExit sites, no bare assert; 'verify_dispatch_coverage' absent from main() at the Task-1 commit"
        status: pass
    human_judgment: false
  - id: D2
    description: "BD-06 Decision 4's slot table is live in both forks: nine slots per sequence, component set exactly the nine shipped names, Eject at Circle 6 in all three, no '+' in any component, Redirect absent"
    requirement: "CIRC-02"
    verification:
      - kind: integration
        ref: "the plan's <automated> verify over both src/PROSOCHE-{Dumb,Sentient}.xml -> 'roster moved, dispatch exact, coverage clean in both forks'"
        status: pass
      - kind: integration
        ref: "decrypted payload of both signed containers carries the same three arrays; retired names Knock / Ash+Confession / Silence+Mirror / Dimming+Mirror on 0 lines each"
        status: pass
    human_judgment: false
  - id: D3
    description: "Dispatch is an exact match: ninety Selected Primitive conditionals, nine distinct names, condition-code set exactly {4} in both forks and in both decrypted payloads"
    requirement: "CIRC-08"
    verification:
      - kind: integration
        ref: "90 mode-0 Selected Primitive conditionals, 9 distinct WFConditionalActionString values, codes == {4}"
        status: pass
    human_judgment: false
  - id: D4
    description: "docs/sequence_dispatch_check.py gates instead of reporting, has an empty KNOWN_ORPHANS, tests BD-06's exactly-one clause, and exits non-zero on a synthesised orphan"
    requirement: "CIRC-08"
    verification:
      - kind: unit
        ref: "ast parse: KNOWN_ORPHANS is an empty Dict literal; 'reported, not gated' and 'THIS IS A REPORTING SCRIPT' absent; match_strategy and both code arms preserved; raise AssertionError present and raise SystemExit absent"
        status: pass
      - kind: unit
        ref: "negative proof: Ambient[8] 'Frozen' -> 'Glacier' on a temp copy -> exit 1 with the silent-runtime-no-op consequence message"
        status: pass
    human_judgment: false
  - id: D5
    description: "The ninth dispatch branch does not move the environmental site counts, because mirror_and_voice() emits no Set Brightness, Set Volume or Get Device Details"
    requirement: "CIRC-06"
    verification:
      - kind: integration
        ref: "docs/environmental_restore_check.py exit 0 with EXPECTED_SITES unedited at 14/14/20; docs/phase9_self_check.py exit 0 with its tables unedited; neither file appears in the plan's diff"
        status: pass
    human_judgment: false
  - id: D6
    description: "Both forks validate, sign under their exact canonical display names with no suffix, decrypt-verify, and the MANIFEST matches disk for all six rows"
    requirement: "AUDIT-02"
    verification:
      - kind: integration
        ref: "validate-shortcut x2 --target-macos 26 --target-platform all -> 'Validation passed.' exit 0; aea decrypt + aa extract + plutil -lint OK x2; docs/manifest_check.py -> 6 rows verified against disk"
        status: pass
    human_judgment: false
  - id: D7
    description: "All twelve structural checks exit 0 at the final commit boundary, and a second consecutive builder run leaves both sources byte-identical"
    verification:
      - kind: integration
        ref: "12/12 green; git status --short clean of src/*.xml after the Task-3 rebuild"
        status: pass
    human_judgment: false
  - id: D8
    description: "A Circle actually reaches its renamed branch under exact matching on a real iPhone"
    verification: []
    human_judgment: true
    rationale: "DIST-03 is open — no iPhone is connected. Every proof in this plan is file-level structural. This project's own debug history records that operator/operand type validity is invisible in the plist: a condition can be structurally valid, validate, sign, import, render red in the UI and fail at runtime. Condition 4 on a text-typed operand is the correct pairing by every available piece of evidence, and that is still not a behavioural observation."

# Metrics
duration: 51min
completed: 2026-08-17
status: complete
---

# Phase 11 Plan 02: Dispatch coverage guard and the whole BD-06 roster Summary

**The dispatch surface became impossible to break silently, and then the entire nine-name roster moved onto it in one commit — closing a defect that had shipped dead for four phases and making its whole class a build-time failure, permanently.**

## Performance

- **Duration:** ~51 min
- **Started:** 2026-08-17T10:59Z
- **Completed:** 2026-08-17T11:50Z
- **Tasks:** 3 (all `type="auto"`)
- **Files modified:** 8 source/doc files plus 4 build artifacts and 2 new dated archives

## Accomplishments

- **The eighth defect class is now a build guard.** `verify_dispatch_coverage(actions)` locates the Config literal by content, resolves matching semantics per branch from that branch's own condition code, and raises on four distinct classes: **orphan**, **unreachable**, **unknown** and **duplicate**. It is armed in `tools/build_state_engine.py`'s `main()` and in `tools/build_sentient.py`'s import list and verify chain, so the invariant is enforced **per fork** rather than inferred for Sentient from Dumb. It runs before the single `SOURCE.write_bytes(...)`, so a failure aborts before any write.
- **It was proven to have teeth before anything depended on it.** Run against the unmodified artifact at Task 1's HEAD it raised, naming the live orphan by name and by every Circle position it occupied. The message is recorded verbatim below.
- **Circle 8 dispatches a real branch.** The `Voice` entry that named nothing is gone; `Loud Mirror` names a branch that is actually emitted, in all three sequences, in both forks, and it is present on **23 lines** of each decrypted signed payload. `docs/sequence_dispatch_check.py` now reports **0 orphans** where it previously reported the Circle-8 defect in all three sequences.
- **Dispatch is exact.** All **ninety** `Selected Primitive` conditionals carry condition code **4** ("string is"); the measured code set is exactly `{4}` in both forks and in both decrypted payloads. Under the old code 99 ("contains") the new entry `Loud Mirror` would *also* have fired the `Mirror` branch — a silent double dispatch — which is why the roster move and the comparator move had to be one commit.
- **The eleventh checker gates instead of reporting.** `docs/sequence_dispatch_check.py`'s `KNOWN_ORPHANS` is empty, its reporter-not-a-gate docstring is gone, and it raises `AssertionError` on any unexpected orphan, unreachable branch, unknown-semantics branch, or duplicate. It gained the **exactly-one** clause BD-06 states and the reporter never tested — counting distinct branch **names**, not action instances.
- **Both promotions were proven to fail before being trusted to pass.** The gate exits 1 on a copy of the Dumb source with one sequence cell replaced by a name no branch emits.

## Task Commits

Each task was committed atomically:

1. **Task 1: Author `verify_dispatch_coverage()` and prove it catches the live Circle-8 orphan** — `3ea4e8c` (feat)
2. **Task 2: Move the whole roster to BD-06's names — exact-match dispatch, nine slots, guard armed** — `5b11eab` (feat)
3. **Task 3: Promote `docs/sequence_dispatch_check.py` from reporter to hard gate** — `39718db` (test)

## The guard's first failure, recorded verbatim

Run against the unmodified `src/PROSOCHE-Dumb.xml` at Task 1's HEAD, before `main()` called it:

```
dispatch coverage: 1 sequence entr(y/ies) dispatch NOTHING -- 'Voice' at Classic (Circle 8),
BlackMirror (Circle 8), Ambient (Circle 8).  An undispatched entry is a silent runtime no-op:
the Circle produces no intervention, no error and no log, which is how Circle 8 shipped dead
for four phases.  It is invisible to validate_shortcut.py, to the ToolKit catalog and to the
signed-artifact decrypt, so this build guard is the only place it can be caught.  Either add
the branch to primitive_dispatch()'s name tuple or correct the name in the Config literal's
sequences array -- never relax this guard
```

And the promoted checker, on a temp copy whose `Ambient[8]` reads `Glacier` instead of `Frozen` — **exit 1**:

```
AssertionError: 1 sequence entr(y/ies) dispatch NOTHING and are not a reviewed exception:
'Glacier' at Ambient (Circle 9).  An undispatched entry is a silent runtime no-op -- the
Circle produces no intervention, no error and no log -- and it is invisible to
validate_shortcut.py, to the ToolKit catalog and to the signed-artifact decrypt, which is how
Circle 8 shipped dead for four phases.  Add the branch to primitive_dispatch()'s name tuple
or correct the name in the Config literal; do not add it to KNOWN_ORPHANS to silence this
```

## The roster, as it now ships

| Circle | Dante name | Classic | BlackMirror | Ambient |
|---|---|---|---|---|
| 1 | Limbo | Pause | Pause | Black and White |
| 2 | Lust | Black and White | Intention | Silence |
| 3 | Gluttony | Silence | Black and White | Dim |
| 4 | Greed | Intention | Mirror | Pause |
| 5 | Wrath | Dim | Silence | Intention |
| 6 | Heresy | **Eject** *(interim)* | Eject | **Eject** *(interim)* |
| 7 | Violence | Mirror | Dim | Mirror |
| 8 | Fraud | **Loud Mirror** *(interim impl)* | **Loud Mirror** | **Loud Mirror** |
| 9 | Treachery | Frozen | Frozen | Frozen |

Nine slots per sequence, nine distinct names across all three, no `+` in any entry, `Redirect` absent.

## Files Created/Modified

- `tools/build_state_engine.py` — **+205 lines net.** New `verify_dispatch_coverage()` and the `SELECTED_PRIMITIVE` constant; `primitive_dispatch()`'s branch tuple replaced with BD-06's nine pairs, the `if name == "Voice": continue` skip deleted, condition `99` → `4`; three now-false comments rewritten; three user-visible strings moved (`alert("Ash", …)` → `alert("Black and White", …)` with a reworded body, `alert("Dimming", …)` → `alert("Dim", …)`, the live-Ice menu prompt → `"Frozen is active"`); guard armed in `main()`.
- `tools/build_sentient.py` — `verify_dispatch_coverage` added to the module-scope import list and to the verify chain, with a comment stating why the invariant is enforced per fork rather than inherited.
- `docs/sequence_dispatch_check.py` — **reporter → gate.** Docstring rewritten, `KNOWN_ORPHANS` emptied (dict and comment retained as a visible, deliberately-empty escape hatch), `require()` helper added, four raising classes on the exit path, new `resolving_names()` and duplicate test, `"reported, not gated"` dropped. `match_strategy()` untouched.
- `docs/phase5_self_check.py` — required-name tuple rewritten to the nine shipped names plus the three sequence names; new **structural** negative assertions over the parsed Config literal (nine slots per array, component set equals the nine, no `+`, no `Redirect`); imports `config_literal` from the existing checker rather than inventing a third parsing idiom.
- `src/PROSOCHE-Dumb.xml` — three `sequences` arrays rewritten whole-array through `tools/plist_text_edit.py`, then regenerated. 2,260,491 → 2,667,477 bytes.
- `src/PROSOCHE-Sentient.xml` — regenerated from the fresh Dumb source; never hand-edited. 2,297,171 → 2,704,157 bytes.
- `src/CONFIG-BLOCK.md` — the three arrays, the provenance paragraph, the two `Ash` notes, three `Field reference` rows and a dated change-log entry; both interim states recorded with the phase that replaces them; the pre-existing pre-Phase-10 `thresholds` drift corrected.
- `artifacts/shortcuts/MANIFEST.md` — all six rows refreshed from disk, the header and evidence paragraphs rewritten around this plan, a paragraph recording both checker promotions, and a new interim-states warning added.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Dumb,Sentient}.shortcut` — re-signed (218,979 B / 223,070 B).
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — {Dumb,Sentient}-1056*.xml` — new dated pre-sign archives, byte-identical to their `src/` counterparts.

## Decisions Made

- **The guard was authored inert and observed failing before it was armed.** This was the plan's explicit non-collapsible ordering, and it earned its keep: the message quoted above is the only direct evidence that the guard's orphan class fires on the real defect rather than on a hypothetical one.
- **The guard's `unknown` class is a strict superset of the plan's specification.** The plan defined it as "a branch whose condition code neither rule knows." A branch whose `WFConditionalActionString` is not a plain `str` is equally unresolvable, and silently skipping it would let an unrecognised dispatch scheme look like a clean surface. Both causes now raise the same message, which names both.
- **Whole-array replacement, never per-name substitution.** `"Ash"` is a substring of `"Ash+Confession"` and `"Dimming"` of `"Dimming+Mirror"`; a per-name pass would have produced exactly the partial rename `tools/plist_text_edit.py`'s `expected_count` guard exists to refuse. Three guarded edits, one per sequence, each asserting exactly one occurrence, followed by a `json.loads` of the whole literal.
- **No Python function was renamed.** `docs/environmental_restore_check.py:49-60` names `dimming` and `silence` by Python identifier in `REQUIRED_SYMBOLS`. The tuple carries the shipped name; the function carries the internal one.
- **The voice-output feature was left entirely alone.** `voice_enabled`, `"Voice Enabled"`, `"Manual Voice"`, `"Snapshot Voice"`, the `Toggle Voice` manual menu item and the `Voice Memos` app identifier are the *voice output* feature, not the *Voice primitive*. Asserted explicitly by an acceptance check.
- **Task 3 did not re-sign.** Its change is checker-only; both builders left both sources byte-identical, so the artifacts signed in Task 2 already provably match the generator at this commit. Re-signing would have churned two signature hashes and orphaned two dated archives for no content change.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 — Missing Critical] The guard's `unknown` class extended to cover a non-literal comparison target**

- **Found during:** Task 1
- **Issue:** The plan specified `unknown` as "a branch whose condition code neither rule knows." But `collect_dispatch_branches()`'s ancestor in `docs/sequence_dispatch_check.py` silently skips a branch whose `WFConditionalActionString` is not a `str`, and a guard that did the same would exclude that branch from both the orphan and the unreachable calculations — the precise silent-drop this guard exists to prevent.
- **Fix:** A non-`str` comparison target resolves to `strategy = "unknown"` alongside an unrecognised code, and the raise message names both causes.
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** `s.count('raise SystemExit') >= 4` still holds (6 sites); the check is green on both forks.
- **Committed in:** `3ea4e8c`

**2. [Rule 2 — Missing Critical] The `ash()` alert body was rewritten, not only its title**

- **Found during:** Task 2
- **Issue:** The plan named this and it was load-bearing: the body read `"Pause. Put the phone down for one breath."` — opening with the word that BD-06 has just made **Circle 1's primitive name**. Renaming only the title would have left the Circle-2 Black and White alert reading as though the Circle-1 intervention had fired. It is emitted ten times into the artifact.
- **Fix:** Body replaced with `"One breath away from the screen before you go on."`, with a comment recording why.
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** Present in both built forks and both decrypted payloads.
- **Committed in:** `5b11eab`

**3. [Rule 3 — Blocking] Signing and the MANIFEST refresh pulled forward from Task 3 into Task 2**

- **Found during:** Task 2, at the acceptance-criteria sweep
- **Issue:** Task 2's acceptance criteria require all twelve checks to exit 0, but `docs/manifest_check.py` recomputes every declared size and hash from disk and therefore goes red on **every** rebuild until the MANIFEST is refreshed — which requires the signed artifacts to be current. Task 3 nominally owned signing, so the criterion was unsatisfiable at Task 2's commit boundary as written.
- **Fix:** Both forks validated, signed under their exact canonical display names with an explicit `--name`, decrypt-verified, and all six MANIFEST rows refreshed from disk inside Task 2. Task 3 then re-ran the full pipeline and found both sources byte-identical, so it did not re-sign.
- **Files modified:** `artifacts/shortcuts/MANIFEST.md`, both signed `.shortcut` files, two new dated archives
- **Verification:** `docs/manifest_check.py` — "passed (6 rows verified against disk)" at both the Task-2 and Task-3 commit boundaries.
- **Committed in:** `5b11eab`

**4. [Rule 1 — Bug] `heat.cap`'s tuning note in `src/CONFIG-BLOCK.md` cited a stale threshold**

- **Found during:** Task 2, step D
- **Issue:** The plan directed the fix of the `thresholds` drift at `:36-38`. The `heat.cap` field-reference row derives its constraint from `thresholds.Inferno[8]` and stated that value as `16` — the pre-Phase-10 number. Correcting the array while leaving the derived note would have left the file internally inconsistent in the same pass that was fixing it.
- **Fix:** Updated to `17`, the measured live value.
- **Files modified:** `src/CONFIG-BLOCK.md`
- **Verification:** Cross-checked against the live Config literal parsed from the artifact.
- **Committed in:** `5b11eab`

---

**Total deviations:** 4 auto-fixed (2 missing critical, 1 blocking, 1 bug)
**Impact on plan:** All four were required either for the plan's own stated acceptance criteria or for the truthfulness of a file the plan edits. No scope creep — no additional primitive, Circle, sequence cell, checker or generator function was touched, and no Rule-4 architectural decision arose.

### Deliberately not done

- **`Redirect` was not emitted.** BD-06 Decision 4 gives Circle 6 to `Redirect` in `Classic` and `Ambient`, but its implementation is Phase 17's, and an emitted branch that no sequence names is exactly what the new `unreachable` rule fails the build over. All three sequences hold `Eject` at Circle 6 as the declared intermediate state.
- **`schema_version` was not bumped.** No bootstrap-seed field changed: `sequences` lives in the Config literal, not in the `state.json` template, and `"circle"` stores an integer rather than a primitive name (RESEARCH's Runtime State Inventory, verified). No installed device's stored state carries a retired primitive name.

## Issues Encountered

None that required problem-solving. Both signings succeeded first time; neither known `sign-shortcut` quirk occurred. `timeout` was never invoked, `--target-macos 27` was never used, and `--target-platform ios` was never used. No `git clean`, `git stash` or destructive reset was run at any point.

## Verification Evidence

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before each builder run |
| Guard observed raising on the live orphan, before arming | `SystemExit`, naming `'Voice'` at all three Circle-8 positions |
| Guard inert at the Task-1 commit | `'verify_dispatch_coverage' not in inspect.getsource(main)` |
| Guard shape | `config_version` present; no `actions[<int>]` index addressing; **6** `raise SystemExit`; no bare `assert` |
| No-op `plistlib` round trip before the Config edit | 2,260,491 in == 2,260,491 out |
| `tools/build_state_engine.py` / `tools/build_sentient.py` | exit **0** / exit **0**, three times each |
| Idempotence | second and third consecutive builds leave both sources byte-identical; `git status --short` clean of `src/*.xml` |
| Dispatch surface | **90** `Selected Primitive` mode-0 conditionals, **9** distinct names |
| Condition codes | set is exactly `{4}` in both forks and both decrypted payloads; **0** carry 99 |
| Sequence shape, both forks | 3 sequences × 9 slots; component set == the nine shipped names; `Eject` at index 5 in all three; no `+`; no `Redirect` |
| `verify_dispatch_coverage` on both built forks | passes |
| Retired names in both built forks | `Knock` 0, `Ash+Confession` 0, `Silence+Mirror` 0, `Dimming+Mirror` 0 |
| Generator function identifiers | `knock`, `ash`, `confession`, `dimming`, `silence`, `exile`, `mirror_and_voice`, `ice_start` all still importable |
| Voice-output feature | `voice_enabled`, `Toggle Voice`, `Voice Memos` all still present |
| Environmental site counts | `docs/environmental_restore_check.py` exit **0** with `EXPECTED_SITES` unedited at **14 / 14 / 20**; `docs/phase9_self_check.py` exit **0** with its tables unedited |
| Promoted gate, clean run | `0 orphan(s) (0 unexpected), 0 unreachable, 0 of unknown semantics, 0 duplicate(s)` → `passed` |
| Promoted gate, synthesised orphan | exit **1**, `AssertionError` naming `'Glacier'` at Ambient (Circle 9) |
| Promoted gate, structural | `KNOWN_ORPHANS` parses as an empty dict; `reported, not gated` and `THIS IS A REPORTING SCRIPT` absent; `match_strategy` and both code arms preserved; `raise AssertionError` present, `raise SystemExit` absent |
| Twelve `docs/*.py` checks | all exit **0**, at both the Task-2 and Task-3 commit boundaries |
| Validator ×2, `--target-macos 26 --target-platform all` | `Validation passed.` exit 0, exit 0 |
| Signed artifacts | 218,979 B / 223,070 B, canonical names, no suffix |
| Dated archive SHA-256 == `src/` counterpart | `c92ccb30…` == `c92ccb30…`; `2b83f791…` == `2b83f791…` |
| Decrypt-verify, both containers | `plutil -lint` **OK** ×2; `Loud Mirror` **23** lines each; condition codes `{4}`; sequences as intended; **1,105** (Dumb) / **1,109** (Sentient) token strings, **0** attachment-offset mismatches |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk |

**Every row above is structural.** `DIST-03` — device verification — remains **open**: no iPhone is connected, nothing in this plan has been observed running, and no claim to the contrary appears in any artifact this plan wrote.

## Flagged assumptions owned by this plan

Carried forward from the plan's spec-less probe ledger. All three remain **unresolved and not machine-proven — review manually**.

- **AUDIT-02 (unclassified, unresolved).** BD-06 marks AUDIT-02 as *extended*, not re-decided. This plan renamed the primitive to `Black and White` and changed nothing about its behaviour: `ash()`'s body is verbatim apart from its alert title and message copy, and `docs/phase5_self_check.py`'s assertion that no Color Filters intent is emitted stays green. Flipping that assertion is Phase 14's. **Assumed: renaming a documented fallback does not re-open the go/no-go decision.**
- **CIRC-06 (unclassified, unresolved).** `exile()` became the `Eject` branch with its body untouched — one comment plus `is.workflow.actions.returntohomescreen`. **Assumed: the straight-ejection half of CIRC-06 is satisfied by the rename, and the routed half (`Redirect`) is Phase 17's, not a gap in this phase.**
- **CIRC-08 (unclassified, unresolved).** This plan closed the *dispatch* half — Circle 8 now reaches a real branch in all three sequences — by reusing `mirror_and_voice()`, which already carries the once-per-run and voice-enabled gates. The designed Voice primitive is Phase 15's. **Assumed: an interim branch that satisfies the gates but is not the designed primitive is the correct Phase-11 state, and it is labelled interim in the generator, in `src/CONFIG-BLOCK.md` and in `artifacts/shortcuts/MANIFEST.md`.**

## Known Stubs

Two entries in this build are **interim stand-ins, deliberately and visibly so**. Neither is a placeholder in the sense of unwired or non-functional code — both dispatch real, tested implementations — but neither is the designed final behaviour, and each is labelled as interim in the generator's own comment text, in `src/CONFIG-BLOCK.md` and in `artifacts/shortcuts/MANIFEST.md`, naming the phase that replaces it.

| Interim | Site | Why it is here | Replaced by |
|---|---|---|---|
| `Loud Mirror` dispatches `mirror_and_voice()` — the same implementation as Circle 7's `Mirror` | `tools/build_state_engine.py` `primitive_dispatch()` branch tuple | Circle 8 named no branch at all for four phases. An entry with no branch cannot coexist with a hard coverage guard, and `mirror_and_voice()` already carries CIRC-08's once-per-run and voice-enabled gates | **Phase 15** — the designed Voice primitive |
| `Eject` holds Circle 6 in all three sequences | the Config literal's `sequences` arrays, `Classic[5]` and `Ambient[5]` | BD-06 gives those two cells to `Redirect`, whose implementation is Phase 17's. Emitting a `Redirect` branch that no sequence names would fail the `unreachable` rule this plan arms | **Phase 17** — flips exactly those two cells |

Neither prevents the plan's goal from being achieved: the plan's goal was that every sequence entry dispatch exactly one real branch, and both of these do.

## Threat Flags

None. This plan adds no network endpoint, no auth path, no file-access pattern and no schema change at a trust boundary. No package was installed and no third-party import was added — every new line uses the Python standard library, so **T-11-SC** (package-manager installs) was never triggered.

The plan's own threat register is closed as follows, all structurally:

| Threat ID | Disposition | Evidence at this commit |
|---|---|---|
| T-11-07 (undispatched entry) | mitigated | `verify_dispatch_coverage()` armed in both builders and proven to raise; `docs/sequence_dispatch_check.py` gates and is proven to exit 1 |
| T-11-08 (`Mirror` / `Loud Mirror` collision under 99) | mitigated | condition-code set exactly `{4}` on all ninety conditionals in both forks; the guard's duplicate rule is live |
| T-11-09 (`Redirect` emitted early) | mitigated | `Redirect` absent from every sequence and from the branch tuple; the `unreachable` rule would fail the build |
| T-11-10 (renamed environmental branch bypassing its restore gate) | mitigated | `dimming()` and `silence()` bodies untouched; `verify_restore_gates()` and `verify_sentinel_gates()` green per fork; site counts unmoved at 14/14/20 |
| T-11-11 (Config literal ceasing to be parseable JSON) | mitigated | edit made through `tools/plist_text_edit.py`'s guarded round trip; `json.loads` re-parsed the literal in the edit script and in the verify command, in both forks |
| T-11-12 (interim read later as designed) | mitigated | both interim states labelled in the generator comment, `src/CONFIG-BLOCK.md` and `artifacts/shortcuts/MANIFEST.md`, each naming Phase 15 / Phase 17 |

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **The dispatch surface is now self-defending.** Any future plan that renames a primitive, adds a Circle, or reorders a sequence will fail the build unless both halves move together, in both forks. Plans 11-03 through 11-06 inherit that.
- **Phase 15 has a precise handoff:** replace `("Loud Mirror", mirror_and_voice)` in `primitive_dispatch()`'s tuple with the designed Voice primitive. The name, the sequence cells and the guard are already in place; only the implementation changes.
- **Phase 17 has a two-cell handoff:** add `("Redirect", <impl>)` to the tuple and flip `Classic[5]` and `Ambient[5]` from `Eject` to `Redirect` in the Config literal — in the **same commit**, because either half alone now fails the coverage guard.
- **Blocker, unchanged:** DIST-03 is open. Everything this phase produces is structural until a device is available. The device question this plan specifically raises: does condition 4 on the `Selected Primitive` operand render black rather than red in the Shortcuts UI, and does a Circle actually reach its branch? Operator/operand type validity is invisible in the plist by this project's own measured record.

## Self-Check: PASSED

- `tools/build_state_engine.py` — `verify_dispatch_coverage` importable and callable — FOUND
- `docs/sequence_dispatch_check.py` — gates, `KNOWN_ORPHANS` empty — FOUND
- `src/PROSOCHE-Dumb.xml` (2,667,477 B) / `src/PROSOCHE-Sentient.xml` (2,704,157 B) — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` (218,979 B) — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` (223,070 B) — FOUND
- Commit `3ea4e8c` (Task 1, feat) — FOUND in `git log`
- Commit `5b11eab` (Task 2, feat) — FOUND in `git log`
- Commit `39718db` (Task 3, test) — FOUND in `git log`
- All twelve `docs/*.py` checks re-run green after the final task commit; working tree clean of source and artifact changes.

---
*Phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r*
*Completed: 2026-08-17*
