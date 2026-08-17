---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 01
subsystem: infra
tags: [shortcuts, plist, plistlib, ios26, aea1, structural-checks, bd-06]

# Dependency graph
requires:
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    provides: the eleven green docs/*.py structural checks, the refreshed MANIFEST and the two canonically named signed artifacts this plan rebuilt on top of
  - phase: quick/260817-au7-ios26-automation-onboarding
    provides: the six-step guarded plist round-trip method, recorded as prose in docs/BUILD-NOTES.md §20 and re-implemented here as an executable module
provides:
  - "tools/plist_text_edit.py — the guarded plistlib round trip (seven public names) that every later plist edit in this phase must go through"
  - "docs/note_identity_check.py — the twelfth structural checker: three Note-identity sites plus the global attachment-offset invariant, per fork"
  - "The live primitive name `Pause` (was `Knock`) in all three sequences arrays, the generator dispatch tuple and all ten emitted dispatch branches"
  - "docs/BUILD-NOTES.md §21 — the round-trip method, the helper's API, the twelfth checker, and a 20-row structural evidence table"
  - "Both forks rebuilt, validated, re-signed under their current canonical display names, and decrypt-verified"
affects: [11-02 dispatch-coverage guard and the rest of the roster, 11-03 Note rename, 11-04, 11-05, 11-06 Core/Aware rename]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Guarded plistlib round trip: prove a no-op dumps() is byte-identical, assert old attachment offsets, replace with an expected_count guard, rebuild attachmentsByRange from the new U+FFFC offsets in document order, re-assert"
    - "Shipped name in the dispatch tuple, internal name on the Python function — the two are deliberately decoupled"
    - "Locate by content, never by index, with exactly-one-match required so a duplicate cannot hide"

key-files:
  created:
    - tools/plist_text_edit.py
    - docs/note_identity_check.py
  modified:
    - tools/build_state_engine.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - src/CONFIG-BLOCK.md
    - docs/phase5_self_check.py
    - docs/BUILD-NOTES.md
    - artifacts/shortcuts/MANIFEST.md

key-decisions:
  - "knock() keeps its Python identifier while the dispatch tuple carries the shipped name Pause — docs/environmental_restore_check.py imports generator functions by name, so renaming the function is a separate, unrelated breakage"
  - "The knock() comment body was rewritten to say Pause as well: it is emitted into the artifact ten times, so leaving it would have left the retired name in the shipped payload"
  - "docs/note_identity_check.py pins the Find Notes predicate Operator (99, 'contains') as an assertion rather than ignoring it, so plan 11-03's proposed move to 4 must be a deliberate edit to one constant"
  - "The pre-existing threshold drift at src/CONFIG-BLOCK.md:36-38 was deliberately NOT fixed — pre-existing and out of this plan's scope; logged to deferred-items.md"
  - "The Circle-8 Voice orphan and the condition-99 dispatch code were left exactly as found, because plan 11-02 Task 1 needs the orphan live to prove its new guard has teeth"

patterns-established:
  - "Pattern 1: every WFTextTokenString edit in this phase goes through tools/plist_text_edit.py, never string substitution on the XML"
  - "Pattern 2: a structural checker asserts the identity constant once and consumes it at every site, so a rename is a one-line edit"
  - "Pattern 3: a new checker is proven to FAIL on deliberately injected damage before it is trusted to pass"

requirements-completed: [CIRC-02, ROOM-01, DIST-01, DIST-02]

coverage:
  - id: D1
    description: "tools/plist_text_edit.py exposes the seven named public functions and its no-op round trip is byte-identical against src/PROSOCHE-Dumb.xml"
    requirement: "ROOM-01"
    verification:
      - kind: unit
        ref: "python3 -c \"import sys;sys.path.insert(0,'tools');import plist_text_edit as p;[getattr(p,n) for n in ('load','assert_noop_roundtrip','assert_offsets_match','replace_in_token','replace_in_plain','save','find_action')];d,b=p.load('src/PROSOCHE-Dumb.xml');p.assert_noop_roundtrip(d,b)\""
        status: pass
    human_judgment: false
  - id: D2
    description: "The BD-06 name Pause is live in the generator dispatch tuple, in all three Config sequences arrays, and on all ten emitted dispatch branches; the retired name is absent from both built forks"
    requirement: "CIRC-02"
    verification:
      - kind: integration
        ref: "python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 -c \"...config_literal(...)['sequences']; assert 'Knock' not in t; assert sum(v.count('Pause') for v in s.values())==3\" — the plan's <automated> verify"
        status: pass
      - kind: integration
        ref: "grep -c Knock src/PROSOCHE-Dumb.xml src/PROSOCHE-Sentient.xml -> 0, 0"
        status: pass
    human_judgment: false
  - id: D3
    description: "Both forks validate at --target-macos 26 --target-platform all, sign under their exact canonical display names with no suffix, and decrypt to payloads containing Pause and not the retired name"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "validate-shortcut src/PROSOCHE-{Dumb,Sentient}.xml --target-macos 26 --target-platform all -> 'Validation passed.' exit 0 x2"
        status: pass
      - kind: integration
        ref: "aea decrypt + aa extract + plutil -convert xml1 on both signed containers; plutil -lint OK x2; Knock 0 lines each, Pause 43 lines each, 3 sequences cells each"
        status: pass
    human_judgment: false
  - id: D4
    description: "artifacts/shortcuts/MANIFEST.md matches disk for all six rows, including the DIST-04 no-suffix filename assertion"
    requirement: "DIST-02"
    verification:
      - kind: integration
        ref: "python3 docs/manifest_check.py -> 'manifest check: passed (6 rows verified against disk)'"
        status: pass
    human_judgment: false
  - id: D5
    description: "docs/note_identity_check.py is green against the current Note title in both forks, and is proven to fail on a deliberately shifted attachmentsByRange key"
    requirement: "ROOM-01"
    verification:
      - kind: unit
        ref: "python3 docs/note_identity_check.py -> exit 0, 775 (Dumb) / 779 (Sentient) token strings, 0 offset mismatches"
        status: pass
      - kind: unit
        ref: "negative proof: shift {0, 1} -> {1, 1} on a temp copy -> exit 1 with the out-of-bounds-range consequence message"
        status: pass
    human_judgment: false
  - id: D6
    description: "All twelve docs/*.py structural checks exit 0 at the final commit boundary, and a second consecutive builder run leaves src/PROSOCHE-Dumb.xml byte-identical"
    verification:
      - kind: integration
        ref: "the eleven baseline checks plus docs/note_identity_check.py, all exit 0; shasum -a 256 src/PROSOCHE-Dumb.xml unchanged at efad0819... across two consecutive builds"
        status: pass
    human_judgment: false
  - id: D7
    description: "The renamed primitive actually dispatches on a real iPhone at Circle 1"
    verification: []
    human_judgment: true
    rationale: "DIST-03 is open — no iPhone is connected. Every proof in this plan is file-level structural: the validator, the decrypted payload and the twelve checkers can all pass on a plist that fails at runtime, which is the exact risk class this project's debug history records. Behavioural confirmation needs a device."

# Metrics
duration: 42min
completed: 2026-08-17
status: complete
---

# Phase 11 Plan 01: End-to-end "Knock becomes Pause" Summary

**One BD-06 primitive name driven from the generator's dispatch tuple to the decrypted payload of both signed artifacts, leaving behind `tools/plist_text_edit.py` (the guarded plist round trip, previously prose-only) and `docs/note_identity_check.py` (the twelfth structural checker).**

## Performance

- **Duration:** ~42 min
- **Started:** 2026-08-17T10:16Z
- **Completed:** 2026-08-17T10:58Z
- **Tasks:** 2 (1 tracer, 1 auto)
- **Files modified:** 9 (2 created, 7 modified) plus 4 build artifacts

## Accomplishments

- **The rename pipeline is proven end to end on one name.** `Knock` → `Pause` moved in the generator's dispatch tuple, in all three `sequences` arrays of the Config literal, through both builders, through eleven structural checks, through the validator, into both signed `.shortcut` files, and was read back out of both AEA1 containers by decryption. The retired name appears on **zero** lines of either built fork and of either recovered payload.
- **`tools/plist_text_edit.py` exists.** Quick task `260817-au7` proved the six-step guarded round trip and left it as prose in `docs/BUILD-NOTES.md` §20 with no script. It is now a standard-library-only module with the seven named public functions, each guard raising `SystemExit` with a message naming the consequence rather than the fact.
- **`docs/note_identity_check.py` is armed before any Note copy is edited.** It asserts the three Control Room Note identity sites against one `EXPECTED_TITLE` constant — the Find Notes predicate, the body H1, the Create Note `name` — each located by content with exactly one required, and it walks both whole documents asserting that every `attachmentsByRange` key lands on a real `U+FFFC` placeholder: **775** token strings in Dumb, **779** in Sentient, **zero** mismatches. It is proven to fail on a deliberately shifted key.
- **Both forks re-signed under their current canonical display names** with an explicit `--name`, so the two signed basenames still carry no suffix and `docs/manifest_check.py`'s DIST-04 assertion stays green. The Core/Aware rename is plan 11-06's, not this plan's.
- **`docs/BUILD-NOTES.md` §21 appended** — 113 insertions, **0 deletions** against the phase baseline `f4e47f9` — recording the method, the helper's API, the twelfth checker, and a 20-row evidence table in which every single row is labelled **structural**.

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): End-to-end "Knock becomes Pause" — one primitive, generator to signed artifact** — `3a30b15` (feat)
2. **Task 2: Arm the Note-identity and attachment-offset invariants as the twelfth checker** — `7d7d7f1` (test)

## Files Created/Modified

- `tools/plist_text_edit.py` — **created.** Guarded plistlib round trip: `load`, `assert_noop_roundtrip`, `assert_offsets_match`, `replace_in_token`, `replace_in_plain`, `save`, `find_action`.
- `docs/note_identity_check.py` — **created.** The twelfth structural check: three Note-identity sites plus the global attachment-offset invariant, both forks.
- `tools/build_state_engine.py` — dispatch tuple's first branch name is now `Pause`; `knock()`'s emitted comment body renamed to match; two comments record the shipped-vs-internal name mapping.
- `src/PROSOCHE-Dumb.xml` — three `sequences` cells rewritten through the helper (`Classic[0]`, `BlackMirror[0]`, `Ambient[3]`), then regenerated.
- `src/PROSOCHE-Sentient.xml` — regenerated from the fresh Dumb source; never hand-edited.
- `src/CONFIG-BLOCK.md` — the three array cells, two `Field reference` rows, two now-false "unchanged from plan 01-01" claims, and a dated change-log entry.
- `docs/phase5_self_check.py` — the hardcoded required-name tuple's first element, so the artifact and the checker cannot disagree about which name is live.
- `docs/BUILD-NOTES.md` — new §21, pure append.
- `artifacts/shortcuts/MANIFEST.md` — all six rows refreshed from disk, the decrypt-verification paragraph rewritten around the tracer, and a new structural-only warning added above the DIST-03 note.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Dumb,Sentient}.shortcut` — re-signed (193,836 B / 198,150 B).
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — {Dumb,Sentient}-1038*.xml` — new dated pre-sign archives, byte-identical to their `src/` counterparts.

## Decisions Made

- **The Python function `knock()` is deliberately unrenamed.** `docs/environmental_restore_check.py:55-56` imports generator functions by name; renaming any of them is a separate, unrelated breakage. The tuple carries the shipped name, the function carries the internal one, and both sites now say so in a comment.
- **The Find Notes `Operator` is asserted, not ignored.** RESEARCH §6.2 proposes moving it from `99` ("contains") to `4` ("string is") when the title shortens, because a shortened title under `contains` would also match a leftover Note from an earlier install and bind PROSOCHĒ's ledger to the wrong note forever. Pinning the current value makes that move visible instead of incidental.
- **A floor of 775 token strings is asserted, not just the offsets.** A *drop* in the count is the signature of string-typed parameters being converted to bare `WFTextTokenAttachment` values — parameter-defect axis 2, which validates and imports cleanly and then resolves to empty text.
- **`find_action` requires exactly one match, not the first.** Taking `[0]` would hide precisely the duplicate-site defect these checks exist to expose.
- **The Circle-8 `Voice` orphan and the condition-99 dispatch code were left untouched.** Plan 11-02 Task 1 depends on the orphan still being live to prove its new coverage guard has teeth, and the 99→4 move is coupled to abolishing the combined entries, which is 11-02 Task 2's work.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 — Missing Critical] The `knock()` comment body was renamed as well as the tuple**

- **Found during:** Task 1 (tracer)
- **Issue:** The plan's step 2 named only the dispatch tuple, but the plan's own acceptance criterion required `grep -c 'Knock'` to return **0** in both decrypted payloads. Measured, the retired name occupied 33 lines of the built Dumb fork: 3 in the Config literal, and 10 each from the `Dispatch {name}` comment, the `WFConditionalActionString`, and the `knock()` docstring-style comment body `"""Knock is a brief factual interruption:`. Renaming only the tuple would have cleared 23 of 33 and left 10 occurrences of the retired name in the shipped artifact.
- **Fix:** Renamed the emitted comment text to `Pause is a brief factual interruption:` while leaving `def knock()` untouched. RESEARCH §3.2's own site table already classes this line as "Recommended for readability".
- **Files modified:** `tools/build_state_engine.py`
- **Verification:** `grep -c "Knock"` returns 0 for both built forks and both decrypted payloads.
- **Committed in:** `3a30b15` (Task 1 commit)

**2. [Rule 1 — Bug] Two now-false provenance claims in `src/CONFIG-BLOCK.md`**

- **Found during:** Task 1 (tracer), step 4
- **Issue:** Line 26 asserted the `sequences` block was "carried over byte-identical from plan 01-01 — unchanged, unreordered", and line 82 repeated "unchanged from plan 01-01". Editing three cells made both statements false in the same file that carries them.
- **Fix:** Both rewritten to name the one BD-06 rename and the three cells it touched; a dated change-log entry added recording that the live literal is in the artifact and this file is its mirror, not its source.
- **Files modified:** `src/CONFIG-BLOCK.md`
- **Verification:** Read back; the file no longer claims an unchanged array it does not have.
- **Committed in:** `3a30b15` (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (1 missing critical, 1 bug)
**Impact on plan:** Both were required for the plan's own stated acceptance criteria and for the truthfulness of a file the plan edits. No scope creep — no additional primitive, Circle, sequence cell or checker was touched.

### Deferred, deliberately not fixed

- **`src/CONFIG-BLOCK.md:36-38` threshold drift.** The doc mirror still shows the pre-Phase-10 curve (`Paradise: [1,4,7,…25]`) while the live literal carries the raised one. RESEARCH §3.4 flags it and notes it is "not this phase's bug". It is pre-existing, unrelated to the rename, and outside this task's change surface, so it was logged to `.planning/phases/11-.../deferred-items.md` rather than fixed here.

## Issues Encountered

None that required problem-solving. The two known `sign-shortcut` quirks (`The file doesn't exist.` / `isn't in the correct format.`) did not occur; both signings succeeded first time. `timeout` was never invoked, `--target-macos 27` was never used, and `--target-platform ios` was never used.

## Verification Evidence

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before each builder run |
| No-op `plistlib` round trip before any edit | 2,260,491 in == 2,260,491 out |
| `tools/build_state_engine.py` / `tools/build_sentient.py` | exit **0** / exit **0** |
| Idempotence | second consecutive build leaves `src/PROSOCHE-Dumb.xml` at `efad0819…`; `git status --short` clean |
| Retired name, built sources | `Knock`: 0 lines Dumb, 0 lines Sentient |
| New name, built sources | `Pause`: 43 lines each; exactly 3 `sequences` cells |
| Attachment invariant, `src/` | 775 (Dumb) / 779 (Sentient) token strings, **0** mismatches |
| `plutil -lint src/PROSOCHE-Dumb.xml` | OK |
| Validator ×2, `--target-macos 26 --target-platform all` | `Validation passed.` exit 0, exit 0 |
| Signed artifacts | 193,836 B / 198,150 B, canonical names, no suffix |
| Dated archive SHA-256 == `src/` counterpart | `efad0819…` == `efad0819…`; `8d9c6105…` == `8d9c6105…` |
| Decrypt-verify, both containers | `plutil -lint` OK ×2; `Knock` 0 lines each; `Pause` 43 lines each; 3 `sequences` cells each; 775/779 token strings, 0 mismatches |
| Eleven baseline `docs/*.py` checks | all exit **0** |
| `docs/note_identity_check.py` | exit **0**; exit **1** on a deliberately shifted `attachmentsByRange` key |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk |

**Every row above is structural.** `DIST-03` — device verification — remains **open**: no iPhone is connected, nothing in this plan has been observed running, and no claim to the contrary appears in any artifact this plan wrote.

## Flagged assumptions owned by this plan

Carried forward verbatim from the plan's spec-less probe ledger; both remain **unresolved and not machine-proven — review manually**.

- **CIRC-02 (unclassified).** This phase changes the primitive's **name only**; `ash()` keeps its alert-only fallback verbatim and `docs/phase5_self_check.py`'s assertion that no Color Filters intent is emitted stays green. *Assumed: a rename with no behaviour change satisfies CIRC-02 for this phase.*
- **DIST-01 (unclassified).** A green `--target-macos 26 --target-platform all` run is asserted by exit code and exact invocation, but the validator's coverage of this project's action set is a known-imperfect instrument (`docs/BUILD-NOTES.md` §13 DEV-01). *Assumed: it is the strongest available structural signal and is not a behavioural guarantee.*

## Known Stubs

None. Nothing in this plan is a placeholder: `Pause` is a real, final BD-06 name; both new modules are complete and exercised; the Circle-8 `Voice` orphan is a pre-existing, already-tracked defect deliberately left in place for plan 11-02, not a stub introduced here.

## Threat Flags

None. This plan adds no network endpoint, no auth path, no file-access pattern and no schema change at a trust boundary. `tools/plist_text_edit.py` and `docs/note_identity_check.py` use only the Python standard library and no package was installed, so T-11-SC (package-manager installs) was never triggered.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **Plan 11-02 has both instruments it needs.** `tools/plist_text_edit.py` is the edit mechanism for the remaining sequence-array moves; `docs/note_identity_check.py` has the offset invariant armed across both whole documents before any further copy is edited.
- **The Circle-8 `Voice` orphan is intact**, which 11-02 Task 1 depends on to prove its new `verify_dispatch_coverage()` guard actually fails when it should.
- **Plan 11-03's Note rename is now a one-line edit** to `EXPECTED_TITLE`, with the predicate `Operator` pinned so the `contains` → `is` decision has to be made explicitly.
- **Blocker, unchanged:** DIST-03 is open. Everything this phase produces is structural until a device is available.

---
*Phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r*
*Completed: 2026-08-17*
