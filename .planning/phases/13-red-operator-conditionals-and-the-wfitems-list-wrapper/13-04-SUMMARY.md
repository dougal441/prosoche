---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
plan: 04
subsystem: distribution
tags: [signing, provenance, manifest, aea1-decrypt, gate-a, gate-b, device-uat, blocked, dist-04, ship-gate]

# Dependency graph
requires:
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-01"
    provides: "the WFItems row wrapper fix and verify_list_item_wrappers(), which put 660 wrapped rows into both sources"
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-02"
    provides: "the Donor-5 pin inside verify_conditional_action_string(), which this plan ships unchanged"
  - phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
    plan: "13-03"
    provides: "the labelled empty BUILD-NOTES §28 subsection this plan fills, and the recorded wave-2 source digests"
provides:
  - "two re-signed distributable artifacts under the exact canonical display names, at SHA-256 fe1bafdf… (Core) and bd1264d5… (Aware)"
  - "two new dated pre-sign archive XMLs, each byte-identical to its src/ counterpart"
  - "six refreshed MANIFEST.md rows, all recomputed from disk, closing the deliberate D-04 red carried since 13-01"
  - "docs/BUILD-NOTES.md §28's gate B advisory read and signed-artifact provenance subsection, filled with measured evidence"
  - "13-UAT.md — six cold-runnable device tests with an explicit BLOCKED branch and every outcome blank"
affects: [Phase-19-device-UAT, DIST-03, any-later-re-sign]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Decrypt-verify the SHIPPED artifact, not the source: AEA1 auth-data leaf cert -> openssl pubkey -> aea decrypt -> aa extract -> plutil, then measure the recovered plist. The only channel that would catch a row altered between source and artifact"
    - "Refresh EVERY manifest row in one pass rather than only the rows believed to have moved — Phase 10 measured three of six wrong at once"
    - "Gate B is issued as a standalone command and its exit 1 recorded as expected; it appears in no && chain and in no verify block, because a permanent waiver makes it structurally incapable of being a gate"
    - "A device UAT's row-selection assertion must name the INTENDED row, not merely a non-empty one — a non-empty but wrong row passes a non-emptiness-only test and hides the regression"
    - "Byte-idempotence as provenance: a rebuild on an already-built tree leaving git status empty is what makes a published digest reproducible rather than run-specific"

key-files:
  created:
    - ".planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-UAT.md"
    - "artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-184943.xml"
    - "artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Aware-184954.xml"
  modified:
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut"
    - "artifacts/shortcuts/MANIFEST.md"
    - "docs/BUILD-NOTES.md"

key-decisions:
  - "Signed to the LIVE display names Core/Aware, not to .claude/CLAUDE.md §8's Dumb/Sentient examples. §8's rule is unchanged and its examples are stale — Phase 11 renamed the products and docs/manifest_check.py hard-codes the live names as DIST-04, so signing to the §8 example names would have failed that checker outright. Source filenames deliberately stay PROSOCHE-Dumb.xml / PROSOCHE-Sentient.xml."
  - "D-04 was closed by RE-SIGNING and recomputing every row from disk, never by editing byte counts to match a stale artifact. Editing the numbers would have made manifest_check.py green while making the provenance record lie — the exact failure the checker exists to prevent."
  - "All six MANIFEST rows were recomputed in one pass, including the two source rows whose digests were already known from 13-03. Refreshing only the rows believed to have moved is how Phase 10 ended up with three of six wrong."
  - "Gate B was run twice as two standalone commands and its exit 1 was recorded as the expected outcome. It appears in neither task's verify block and in no && chain, so nothing in this plan's definition of done depends on a command that can never exit 0."
  - "The decrypt-verify measured the RECOVERED plists, not src/. Both measured 67 List actions, 660 wrapped rows, 6 bare rows and 0 unwrapped rows, and both showed WFWorkflowName ABSENT — independently re-confirming that the filename is the sole carrier of the display name on this build, which is what makes the naming discipline load-bearing rather than cosmetic."
  - "MANIFEST.md's superseded paragraphs were kept and annotated rather than rewritten, following the file's own established convention, and the previous six row values were quoted into the header so a reader holding an older build can still identify it."
  - "13-UAT.md drives Tests 1-4 through the manual `Test a Circle` menu item rather than through accumulated Pressure. That removes the Pressure arithmetic as a confound from the row-rendering question and makes the file runnable without first hand-building the two Personal Automations; Test 5 exists precisely to cover the automation path the manual menu does not."
  - "13-UAT.md's Test 2 carries a per-Circle expected-template table rather than a non-emptiness assertion, and names three distinguishable failure shapes. `Test a Circle` copies the chosen Circle straight into the value the Mirror indexes with, so the mapping is exact and the A4 question becomes directly checkable instead of merely observable."
  - "Test 4 is framed as an OBSERVATION with no expected result. The 2026-08-14 red render is not reproducible at HEAD, its screenshot does not exist in the repository, and this phase deliberately changed nothing in that family — so a red chip would be a NEW finding with a live artifact, and its absence is not a pass of anything."
  - "The device verdict was recorded as observed and BLOCKED. `xcrun devicectl list devices` was actually run and returned `No devices found.`; every outcome field in 13-UAT.md is blank. No simulator run, decrypted-artifact inference or plausible-looking pass was entered as device evidence."

patterns-established:
  - "When a plan both fills a placeholder AND owns the observation that placeholder describes, run the observation before writing the prose — the forward reference is the easy way to write something not yet true"
  - "A ship-gate plan states the artifact's SHA-256 inside the UAT header, so a later cold run can prove it is testing the build the file was written against"

requirements-recorded: [DIST-01, DIST-02, DIST-04]
requirements-regression-protected: [CIRC-04, ROOM-03]

coverage:
  - id: D1
    description: "Both forks rebuild from the provenance-checked source, are gate-A clean, and are signed under the exact canonical display names with no suffix of any kind"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "git merge-base --is-ancestor 7ca8ebbf… HEAD exit 0; both generators run; validate-shortcut --target-macos 26 --target-platform all prints `Validation passed.` on both sources; both signed files exist, are non-zero and begin with AEA1; no other .shortcut basename in artifacts/shortcuts/"
        status: pass
    human_judgment: false
  - id: D2
    description: "Gate B is read standalone per fork and reports exactly one waived line each — the com.apple.mobilenotes.SharingExtension / WFCreateNoteInput waiver — recorded verbatim and index-normalised"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "two standalone validate-shortcut --target-macos 27 --target-platform all runs, each exit 1 with exactly one finding line (Core index 4192, Aware index 4260); both recorded in BUILD-NOTES §28 verbatim plus an index-normalised form. Appears in no && chain and in no verify block"
        status: pass
    human_judgment: false
  - id: D3
    description: "What actually shipped carries the Phase 13 shape, proven by decryption rather than by inference"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "AEA1 leaf cert (779 DER bytes both forks) -> openssl pubkey -> aea decrypt (0) -> aa extract (0) -> plutil (0); recovered plists measure 67 List actions, 660 wrapped rows, 6 bare rows, 0 unwrapped dict rows, WFWorkflowName absent — per fork"
        status: pass
    human_judgment: false
  - id: D4
    description: "All six MANIFEST rows match disk and all twelve docs/*.py checkers exit 0, closing the D-04 red carried since plan 13-01"
    requirement: "DIST-02"
    verification:
      - kind: integration
        ref: "python3 docs/manifest_check.py -> `manifest check: passed (6 rows verified against disk)`; twelve-checker sweep reports `failed: none`; the verify block independently recomputes SHA-256 and size for all six paths and greps both out of MANIFEST.md"
        status: pass
    human_judgment: false
  - id: D5
    description: "CIRC-04 and ROOM-03 are proven unregressed against the artifact that actually ships"
    requirement: "CIRC-04, ROOM-03"
    verification:
      - kind: integration
        ref: "docs/phase5_self_check.py and docs/note_identity_check.py both exit 0 in the final twelve-checker sweep, run against the rebuilt sources the shipped artifacts were signed from. Neither requirement had a defect site in either family and no work was invented for them"
        status: pass
    human_judgment: false
  - id: D6
    description: "The build is byte-idempotent, so an interrupted-and-retried run converges on the same digests rather than a new set"
    requirement: "DIST-02"
    verification:
      - kind: integration
        ref: "both generators run on an already-built tree; git status --porcelain empty afterwards; both source digests equal the wave-2 values 99388cad… and d01154b3… recorded in 13-03-SUMMARY"
        status: pass
    human_judgment: false
  - id: D7
    description: "13-UAT.md exists, is cold-runnable, names the exact artifact and its SHA-256, carries a re-import precondition, six numbered tests and an explicit BLOCKED branch"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "the plan's verify script asserts BLOCKED, the exact Core basename, devicectl, Mirror/Circle/Leaving coverage, >= 4 numbered tests and the re-import precondition, plus the BUILD-NOTES cross-reference — all pass"
        status: pass
    human_judgment: false
  - id: D8
    description: "The device-reachability verdict is recorded as observed, with every outcome blank"
    requirement: "DIST-01"
    verification:
      - kind: integration
        ref: "xcrun devicectl list devices actually executed, returning `No devices found.`, transcribed verbatim into 13-UAT.md's reachability-probe block; all six Results rows and every inline outcome field left empty"
        status: pass
    human_judgment: false
  - id: D9
    description: "A Mirror renders non-empty text on device, and getitemfromlist returns the INTENDED row over a wrapped List"
    requirement: "CIRC-07"
    verification:
      - kind: backstop
        ref: "Device-only (assumptions A1 and A4). No iPhone was reachable — 13-UAT.md Tests 1, 2 and 6 are written to settle it and are recorded BLOCKED with blank outcomes. Deferred to the standing DIST-03 backlog and to Phase 19"
        status: deferred
    human_judgment: true

# Metrics
duration: 25 min
completed: 2026-08-17
status: complete
---

# Phase 13 Plan 04: Ship the wrapper fix and record what only a device can answer Summary

**Both forks are re-signed under their exact live display names and the wrapped rows are proven to have *shipped* — 67 List actions, 660 wrapped rows, 6 bare rows and 0 unwrapped rows measured in the plists recovered by decrypting the `.shortcut` containers themselves, not inferred from the source — all six MANIFEST rows now match disk so the D-04 red carried deliberately since plan 13-01 is closed with all twelve checkers green, and the two questions only an iPhone can answer are written down as a cold-runnable UAT that is recorded BLOCKED with every outcome blank because `xcrun devicectl list devices` really was run and really did report no device.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2
- **Files created:** 3 (`13-UAT.md`, two dated pre-sign archives)
- **Files modified:** 4 (two signed artifacts, `MANIFEST.md`, `BUILD-NOTES.md`)

## Accomplishments

- **Shipped the fix, and proved it shipped.** Both containers were decrypted through the full AEA1 workflow — leaf certificate out of `SigningCertificateChain` (779 DER bytes each), `openssl x509` public key, `aea decrypt`, `aa extract`, `plutil` — and the **recovered** plists measured 67 `is.workflow.actions.list` actions, **660** rows wrapped as `{WFItemType: 0, WFValue: …}`, **6** bare-string rows and **0** dict rows missing `WFItemType`, per fork. This is the only check that would catch a row altered between source and artifact, and it is what licenses the claim that the wrapper *shipped* rather than merely *built*.
- **Signed to the right names, which is the difference between a build and a dead install.** `PROSOCHĒ — Nine Circles — Core.shortcut` (234830 bytes) and `PROSOCHĒ — Nine Circles — Aware.shortcut` (239184 bytes), no suffix, nothing else in `artifacts/shortcuts/`. Both recovered plists were also checked for `WFWorkflowName` and **neither has one** — independently re-confirming on this build that the signer strips it and the filename is the sole carrier of the display name.
- **Closed D-04 properly.** Every one of the six MANIFEST rows was recomputed from disk in a single pass — including the two source rows whose digests were already known — because Phase 10 measured three of six wrong at once. `docs/manifest_check.py` reports `passed (6 rows verified against disk)` and the full twelve-checker sweep reports `failed: none`.
- **Read gate B, and it surfaced nothing.** This was the run most likely to catch a parameter-key or picker-literal regression, since the phase moved 660 row serializations and gate B is the only channel that checks those at all. Both forks reported **exactly one** line — the permanent `WFCreateNoteInput` waiver — and nothing else.
- **Wrote the device questions down so they can be answered later without this context.** `13-UAT.md` carries six tests, an exact-artifact re-import precondition, and a per-Circle expected-template table that makes the A4 question (does `getitemfromlist` return the *intended* row over a wrapped List?) directly checkable rather than merely observable.
- **Recorded BLOCKED honestly.** The probe was run, not assumed. Every outcome field is blank.

## Task Commits

Each task was committed atomically:

1. **Task 1: rebuild, gate A, gate B advisory read, sign, decrypt-verify, refresh every MANIFEST row** — `737ce07` (chore)
2. **Task 2: author the cold-runnable `13-UAT.md` and record the device verdict** — `91e2b8b` (docs)

## Files Created/Modified

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — re-signed; 234830 bytes; SHA-256 `fe1bafdf53f872a3e149734456899d1be0987706551d7b8fa7b50f81b8a913b7`.
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — re-signed; 239184 bytes; SHA-256 `bd1264d502891c9afeeccb66134dceaf66288a1da890133498605538aa75ba19`.
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-184943.xml` and `— Aware-184954.xml` — new dated pre-sign archives, each byte-identical to its `src/` counterpart.
- `artifacts/shortcuts/MANIFEST.md` — all six rows refreshed; header rewritten to name the phase 13 plan 04 re-sign as the table's provenance, with the previous six values quoted so a reader holding an older build can still identify it; a phase 13 narrative paragraph and a closing `⚠` bullet added; the superseded phase 12 WR-01 paragraph annotated rather than deleted.
- `docs/BUILD-NOTES.md` — §28's `PLACEHOLDER` subsection replaced by the measured record: provenance and byte-idempotence, the pre-signing checker baseline, gate A results, both gate B outputs verbatim plus an index-normalised form, the signed-artifact table, the stale-§8-examples note, the decrypt-verification table, the MANIFEST statement, the device verdict, and the Phase 19 re-import note.
- `.planning/phases/13-…/13-UAT.md` — new; six tests, BLOCKED.

## Decisions Made

- **Signed to `Core`/`Aware`, not to `.claude/CLAUDE.md` §8's `Dumb`/`Sentient` examples.** §8's filename-discipline *rule* is unchanged and was followed exactly; its *example names* predate Phase 11's product rename. `docs/manifest_check.py` hard-codes the live names as `DIST-04`, so signing to the §8 example names would have failed that checker outright. The source filenames deliberately stay `PROSOCHE-Dumb.xml` / `PROSOCHE-Sentient.xml`; the addendum renamed the products, not the sources. This is recorded in §28 so the next reader does not have to rediscover it.
- **D-04 was closed by re-signing, never by editing byte counts to match.** Editing the numbers would have turned `manifest_check.py` green while making the provenance record lie — precisely the failure the checker exists to prevent, and precisely what plan 13-03 declined to do when it left the red in place.
- **All six rows were recomputed, not just the four that obviously moved.** The two source rows' digests were already known from 13-03's record and were still recomputed from disk. Trusting a known-good row is how three of six ended up wrong in Phase 10.
- **Gate B was issued as two standalone commands and its exit 1 recorded as expected.** It appears in neither task's `<verify>` block and in no `&&` chain. Because its waiver is permanent it can never exit 0, so treating it as a gate would either block every build or train the reader to ignore its output.
- **The decrypt-verify measured the recovered plists, not `src/`.** Verifying the source and then trusting the signer would have left the one gap the whole step exists to close.
- **`13-UAT.md` drives Tests 1–4 through the manual `Test a Circle` menu item.** That item copies the chosen Circle straight into the value the Mirror indexes with, so it removes Pressure arithmetic as a confound from a question that is purely about row rendering, and it makes the file runnable without first hand-building the two Personal Automations. Test 5 exists specifically because the manual menu does not exercise the automation path a real user takes.
- **Test 2 asserts the *intended* row, with a per-Circle template table and three named failure shapes.** A non-empty but wrong row would pass a non-emptiness-only test and hide the A4 regression completely; the plan is explicit that non-emptiness alone is not sufficient, and the ten baseline templates are distinct enough that the mapping is checkable by eye. The three shapes — right wording with a wrong substituted number, wrong wording entirely, and a consistent off-by-one — mean different things and are recorded separately so a failure report is diagnostic rather than just negative.
- **Test 4 has no expected result, by design.** The 2026-08-14 red render is not reproducible at HEAD, its screenshot exists nowhere in the repository or in git history, and this phase changed nothing in that family. A red chip would be a *new* finding with a live artifact to inspect — worth more than a clean run — and its absence is not a pass of anything.
- **The device verdict was observed, not assumed.** `xcrun devicectl list devices` was executed and returned `No devices found.`, transcribed verbatim. Every outcome field is blank.

## Deviations from Plan

**None.** No deviation rule was invoked and no auto-fix was required. The plan executed as written, both `<verify>` blocks passed on their first run, and neither known signer quirk fired — both `shortcuts sign` invocations succeeded on the first attempt, so `sign-shortcut`'s two auto-retries were never exercised.

Three observations worth recording precisely, because each *looks* like a discrepancy and is not:

- **The rebuild produced no diff.** `tools/build_state_engine.py` and `tools/build_sentient.py` both ran, and `git status --porcelain` was empty afterwards — the sources still carry the wave-2 digests `99388cad…` and `d01154b3…`. That is the byte-idempotence the plan's write-atomicity truth asks for (T-13-26), not a skipped build.
- **Gate B's `First failing action: index 0 (is.workflow.actions.comment)` line is not a second finding.** It is the validator's own framing of where it stopped, printed above the findings list on every gate B run. Exactly one finding line was reported per fork.
- **The phase 12 dated archives were left in place.** `artifacts/shortcuts/2026-08-17/` now holds both this run's archives and the earlier ones from the same date. `MANIFEST.md` no longer references the older two, and nothing deletes them; multiple dated archives per day is the established shape of that directory. No file was deleted in either commit (`git diff --diff-filter=D` is empty for both).

## Issues Encountered

None.

One thing was corrected *during* authoring rather than after: the `MANIFEST.md` phase 13 paragraph was first drafted with a sentence asserting that `13-UAT.md` recorded BLOCKED — a forward reference to a file task 2 had not yet created and to a probe that had not yet been run. It was rewritten to state the probe result directly, and the probe was run before either statement was committed. The same hazard was caught a second time in `docs/BUILD-NOTES.md` §28, where the device paragraph was trimmed to the observed probe result at task 1 and the `13-UAT.md` cross-reference added only in task 2, once the file existed. Writing "it is recorded BLOCKED" before running the probe is exactly the fabrication this plan's central prohibition forbids, and it is easy to do by accident when one plan owns both the record and the observation.

## Verification Results

| Check | Result |
|---|---|
| Worktree branch / base assertion before any edit | `worktree-agent-a2ee93e1f27ae9148`, base `6c49f993…` — both match |
| `git merge-base --is-ancestor 7ca8ebbf… HEAD` | exit **0** |
| `tools/build_state_engine.py`, `tools/build_sentient.py` | both ran; `git status --porcelain` empty afterwards — **byte-idempotent** |
| Source digests after rebuild | `99388cad…` (Core), `d01154b3…` (Aware) — equal to the wave-2 values |
| Eleven non-manifest checkers **before** signing | all **PASS** |
| `docs/manifest_check.py` before signing | **EXPECTED RED (D-04)** — `MANIFEST declares 2831992 bytes, src/PROSOCHE-Dumb.xml is 2916560 bytes`, byte-identical to 13-01/02/03's record |
| Gate A, Core | `Validation passed.`, exit **0** |
| Gate A, Aware | `Validation passed.`, exit **0** |
| Gate B, Core (standalone) | exit 1, **exactly one** finding line — `com.apple.mobilenotes.SharingExtension` at index **4192**, `WFCreateNoteInput` |
| Gate B, Aware (standalone) | exit 1, **exactly one** finding line — same waiver at index **4260** |
| Gate B in any `&&` chain or verify block | **none** — issued as two standalone commands |
| Signer quirks | **neither fired**; both `shortcuts sign` runs succeeded first attempt |
| Signed artifacts | `— Core.shortcut` 234830 bytes `fe1bafdf…`; `— Aware.shortcut` 239184 bytes `bd1264d5…`; both begin `AEA1` |
| Other `.shortcut` basenames in `artifacts/shortcuts/` | **none** — no suffix leaked in |
| AEA1 recovery | leaf 779 DER bytes both forks; `aea decrypt` 0, `aa extract` 0, `plutil -convert xml1` 0, both forks |
| Recovered plist — Core | 4346 actions, **67** List actions, 666 rows: **660 wrapped**, **6 bare**, **0** unwrapped dicts |
| Recovered plist — Aware | 4414 actions, **67** List actions, 666 rows: **660 wrapped**, **6 bare**, **0** unwrapped dicts |
| `WFWorkflowName` in either recovered plist | **absent** — filename is the sole carrier, re-confirmed |
| Source XMLs at moment of signing | 660 wrapped rows, 0 unwrapped, both forks |
| Dated archives | byte-identical to their `src/` counterparts (size and SHA-256 match exactly) |
| `docs/manifest_check.py` after refresh | **PASS** — `manifest check: passed (6 rows verified against disk)` |
| Twelve-checker sweep, final | `failed: none` — **all twelve green**, D-04 closed |
| `docs/phase5_self_check.py` (CIRC-04) / `docs/note_identity_check.py` (ROOM-03) | both **PASS** in the final sweep, against the artifact that ships |
| Task 1 verify block | **PASS** — `signed, named, decrypt-shape-checked and manifested` |
| Task 2 verify block | **PASS** — `13-UAT.md authored and the device verdict recorded` |
| `xcrun devicectl list devices` | `No devices found.` — recorded verbatim |
| `13-UAT.md` outcome fields | **all blank**, six tests marked BLOCKED |
| File deletions in either commit | **none** (`git diff --diff-filter=D --name-only` empty for both) |
| `.planning/STATE.md` / `.planning/ROADMAP.md` | **untouched** — the orchestrator owns those writes |

## Known Stubs

None. No hardcoded empty value, placeholder string, TODO, FIXME or unwired component was introduced. The `PLACEHOLDER` subsection plan 13-03 deliberately left in `docs/BUILD-NOTES.md` §28 was **filled and its heading renamed** — it no longer reads `PLACEHOLDER` and no longer carries the "not guessed here" disclaimer, because its contents are now measured.

`13-UAT.md`'s blank outcome fields are **not** stubs. They are the deliberate, plan-mandated, project-precedented representation of an unobserved device result, and filling them with anything would be the prohibited outcome rather than the complete one.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or trust-boundary schema change. The register's `mitigate` dispositions are discharged:

- **T-13-21 (DoS, signed artifact filenames)** — signed with `sign-shortcut --name` at the exact canonical display names; `docs/manifest_check.py`'s DIST-04 assertion passes; the verify block independently confirms no other `.shortcut` basename exists in `artifacts/shortcuts/`.
- **T-13-22 (Repudiation, MANIFEST)** — all six rows recomputed in one pass; the verify block independently recomputes SHA-256 and byte size for all six paths and greps both out of the MANIFEST text.
- **T-13-23 (Tampering, what the signer emitted)** — both containers decrypted and the recovered plists measured at 660 wrapped / 0 unwrapped rows. `aea` and `aa` were both available at `/usr/bin`, so no tooling deviation was recorded.
- **T-13-24 (Repudiation, device UAT results)** — the probe was run and its verbatim output recorded; every outcome is blank; the standing-note section states explicitly what may not be substituted.
- **T-13-25 (Tampering, rebuild provenance)** — the ancestor check exited 0 before either generator ran and heads the automated verify chain.
- **T-13-26 (Tampering, partial write)** — discharged by measurement rather than by inspection: the rebuild on an already-built tree left `git status` empty and both digests unchanged, so a re-run after an interruption converges rather than diverging.
- **T-13-27 (Repudiation, gate B treated as a gate)** — run standalone twice, absent from every `&&` chain and from both verify blocks, recorded verbatim and index-normalised.
- **T-13-28 / T-13-SC (accept)** — unchanged. No package-manager install was run and no dependency file was touched; the toolchain is the Python standard library plus already-installed macOS and Shortcuts Playground tooling.

## User Setup Required

**To use these builds:** delete any previously installed `PROSOCHĒ — Nine Circles — Core` / `— Aware` from the Shortcuts app, then import the two artifacts named above. A signed `.shortcut` carries no display name internally, so two builds of the same name cannot be told apart in the library once both are installed — and a device holding any earlier build keeps the blank-row Mirror until it re-imports. Re-point both Personal Automations at the newly imported entry by hand; no mechanism in iOS can do it for you.

## Next Phase Readiness

**Ready, and the phase's ship gate is closed.** Both forks are installable under the names the user's Personal Automations reference, what shipped is proven by decryption to carry the fix, the MANIFEST is a true provenance claim again, and all twelve checkers are green.

**Carried forward, not blockers.** `DIST-03` remains **open** and is the only thing standing between this phase and a device verdict. `13-UAT.md` Tests 1, 2 and 6 are the assertions that settle assumptions **A1** and **A4** and they are written to be run cold at any later date. **Phase 19 must test a re-imported build** — the artifact to import is `PROSOCHĒ — Nine Circles — Core.shortcut` at SHA-256 `fe1bafdf…`; anything else is the wrong build and would observe the old defect while attributing it to a fix that did land.

## Self-Check: PASSED

- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-184943.xml` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Aware-184954.xml` — FOUND
- `artifacts/shortcuts/MANIFEST.md` — FOUND
- `docs/BUILD-NOTES.md` — FOUND
- `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-UAT.md` — FOUND
- `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-04-SUMMARY.md` — FOUND
- Commit `737ce07` — FOUND in `git log`
- Commit `91e2b8b` — FOUND in `git log`
- `.planning/STATE.md` and `.planning/ROADMAP.md` untouched — the orchestrator owns those writes

---
*Phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper*
*Completed: 2026-08-17*
