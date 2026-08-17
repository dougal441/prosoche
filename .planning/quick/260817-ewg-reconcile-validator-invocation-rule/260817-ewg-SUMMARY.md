---
quick_id: 260817-ewg
phase: quick-260817-ewg
plan: 01
subsystem: build-tooling-documentation
status: complete
tags: [validator, shortcuts-playground, documentation-reconciliation, deviation-history]
requires: []
provides:
  - "two-gate validator rule, stated once in .claude/CLAUDE.md §1"
  - "docs/BUILD-NOTES.md §22 — measured evidence record with index-normalised waiver"
affects:
  - .claude/CLAUDE.md
  - docs/BUILD-NOTES.md
  - .planning/research/STACK.md
  - .planning/research/SUMMARY.md
  - .planning/spikes/CONVENTIONS.md
  - artifacts/shortcuts/MANIFEST.md
  - .claude/skills/spike-findings-prosoche/SKILL.md
  - .claude/skills/spike-findings-prosoche/references/evidence-and-probes.md
  - tools/build_state_engine.py
tech-stack:
  added: []
  patterns:
    - "one-home discipline: the rule in CLAUDE.md §1, the evidence in BUILD-NOTES §22, pointers everywhere else"
    - "advisory gate: a check whose expected output is a nonzero exit plus an enumerated permanent waiver, read by diff rather than by exit code"
key-files:
  created:
    - .planning/quick/260817-ewg-reconcile-validator-invocation-rule/260817-ewg-SUMMARY.md
  modified:
    - .claude/CLAUDE.md
    - docs/BUILD-NOTES.md
    - .planning/research/STACK.md
    - .planning/research/SUMMARY.md
    - .planning/spikes/CONVENTIONS.md
    - artifacts/shortcuts/MANIFEST.md
    - .claude/skills/spike-findings-prosoche/SKILL.md
    - .claude/skills/spike-findings-prosoche/references/evidence-and-probes.md
    - tools/build_state_engine.py
decisions:
  - "Gate B uses --target-platform all, not ios — measured: 1105 vs 455 enum-checked identifiers, 1 vs 5 errors per fork, and ios drops all four Notes actions from checking"
  - "Gate B is advisory and structurally cannot exit 0, so it is never chained into a definition of done"
  - "Archived spike READMEs (.claude/skills/.../sources/, .planning/spikes/00[234]/) are historical evidence records and were deliberately left carrying the old invocation"
metrics:
  duration: "~1h (resumed after predecessor's worktree was destroyed mid-run)"
  completed: 2026-08-17
  tasks: 3
  commits: 4
---

# Quick Task 260817-ewg: Reconcile the Validator Invocation Rule — Summary

Three project sources disagreed on how to invoke the Shortcuts Playground validator, in files
future agents treat as binding. They are now one rule, stated once, backed by measurements
recorded once — and the two most-reachable instruction sites carried a pass-expectation that
the reconciled rule makes unsatisfiable, which is fixed.

## 1. No shipped defect was found

**Gate A is clean on both forks.** `--target-macos 26 --target-platform all` returns
`Validation passed.`, exit 0, for `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml`.

**Gate B reports exactly one line per fork**, index-normalised:

```
1 - Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

That line is **pre-adjudicated device-donor ground truth**, not a new finding. `WFCreateNoteInput`
was read off the owner's own iPhone (`.planning/debug/"Donor - notes.shortcut"`, decrypted
2026-08-14 — `docs/BUILD-NOTES.md` §14), and this project's evidence hierarchy ranks a donor
above the catalog. The builder retains it deliberately; the catalog's `contents` entry is the
`macOS 27`-tagged, less authoritative source.

So gate B **added no new information about the current artifacts**. Its demonstrated value rests
entirely on the synthetic-mutation control recorded at BUILD-NOTES §22.4 — a scratch copy of the
Dumb fork with one `WFCountType` changed `Items` → `Bananas` passes gate A clean and is caught by
gate B. Both halves of that are stated plainly in §22.6 and neither is inflated.

## 2. The reconciled rule as implemented

**Gate A — mandatory, must pass clean:** `--target-macos 26 --target-platform all` →
`Validation passed.`, exit 0. Byte-identical to prior practice, so every existing plan, pending
todo, `docs/*.py` checker and in-flight Phase 11 acceptance criterion stays correct.

**Gate B — advisory, waivered, never blocking:** `--target-macos 27 --target-platform all` →
exit 1 with exactly the one waived line per fork. Anything outside the waiver is a real finding.
Because the waiver is permanent, gate B is structurally incapable of exiting 0 and therefore
cannot be `&&`-chained into a definition of done even by accident.

**The one-line mechanism — why `--target-macos` was always the controlling variable:**
`TOOLKIT_PARAMETER_CATALOG_MIN_MACOS_MAJOR = 27` in `validate_shortcut.py:265` means that below
target-macOS 27 the v78 parameter-key and enum-case catalogs are **not loaded at all, on any
platform setting** — so no amount of platform-flag tuning could ever have surfaced a parameter-key
or picker-literal defect at target 26.

`--target-macos 27 --target-platform all` strictly dominates `27 / ios`: 1105 enum-checked
identifiers versus 455, 14 emitted `(identifier, key)` pairs versus 13, one waived error per fork
versus five, and `ios` excludes every `macOS 27`-tagged catalog entry — which removes all four
Notes actions, the ones this project depends on most, from checking entirely.
`--target-macos 26 --target-platform ios` remains forbidden and vacuous: both snapshots are
filtered out, one by the platform gate and one by the version gate, leaving an empty allowlist
that rejects 3675 of 3675 actions.

The rule lives in `.claude/CLAUDE.md` §1 `### Exact validator invocation` and nowhere else. The
evidence lives in `docs/BUILD-NOTES.md` §22 and nowhere else. Seven other sites are now pointers
carrying the greppable token `two-gate rule`.

## 3. Citation correction: `1805` → symbol anchor

The plan and both dispatches cited `tools/build_state_engine.py:1805` for the deliberate
`WFCreateNoteInput` retention. **That line number is wrong.** Measured by the predecessor at its
HEAD: the donor-evidence comment was at `:1789-1794` and the enforced entry at `:1810`, inside
`STRING_ENVELOPE_PARAMS` — not `:1805`, and not in `VERIFIED_PARAMETER_KEYS`.

Re-measured at this run's HEAD after concurrent sessions had grown the file, those had already
moved again: comment `:1961-1966`, entry `:1982`, with `VERIFIED_PARAMETER_KEYS` starting `:1894`.

Both citation sites (CLAUDE.md §1's waiver table and BUILD-NOTES §22.5) therefore **anchor on the
symbol** — `STRING_ENVELOPE_PARAMS["com.apple.mobilenotes.SharingExtension"]`, with the
donor-evidence comment in the CYCLE 4 block immediately above it — and record the line numbers only
as a dated measurement with an explicit warning that they drift. A bare line number in a file under
concurrent edit is a citation with a short half-life; that is the failure this correction removes,
not just the arithmetic.

## 4. The "both must pass" incompatibility in the skill files

Scope addition, found by the predecessor and fixed here. `.claude/skills/spike-findings-prosoche/`
is auto-surfaced to **every agent working in this repo** — a more reachable instruction site than
CLAUDE.md §1. Both of its live files asserted:

- `SKILL.md:75` — "Validator invocation — **both must pass**"
- `references/evidence-and-probes.md:107` — "**Require both validator invocations to pass.**"

This is **not merely a stale flag string**. Under the reconciled rule gate B can *never* exit 0,
because its waiver is permanent. An agent following that instruction literally reads gate B's
single expected waiver line as a build failure — and then either blocks on a non-problem or, worse,
"fixes" a `WFCreateNoteInput` that device-donor evidence says must stay.

Both sites now state: **only gate A must pass**; gate B is advisory, cannot exit 0, carries a named
permanent waiver, and its one expected line is the correct result rather than a failure. Anything
gate B reports outside the waiver is a real finding. The flag string is corrected in the same pass
(`27 ios` → `27 all`, with the 1105-vs-455 reason), and the existing
`never --target-macos 26 --target-platform ios` warning is **kept at both sites** — it remains true.

`.claude/skills/spike-findings-prosoche/sources/**` was deliberately **not touched** and is asserted
unmodified. Those archived spike READMEs are historical evidence records, the same category as a
BUILD-NOTES deviation entry; several name the old invocation as a record of what that spike actually
ran, and rewriting them would falsify the archive.

## 5. Further site carrying the old rule, enumerated by neither the plan nor the dispatch

**`.planning/research/SUMMARY.md:19`** — the Recommended Stack paragraph prescribed
`Validate at --target-macos 26 --target-platform ios` as a live operational instruction. This is
the executive summary sitting directly above `STACK.md`, is read as guidance rather than as a
record, and was a ready-made source for a fifth re-derivation. Fixed and committed separately
(`e03ed76`), bringing the propagation-site count to **six live sites plus one code comment**, versus
the plan's four.

A repo-wide sweep found the old invocation surviving in exactly one other category, all
**deliberately left alone as historical records**:

| Path | Category |
|---|---|
| `.claude/skills/spike-findings-prosoche/sources/00{2,3,4,7}/README.md` | archived spike evidence — explicitly out of scope |
| `.planning/spikes/00{2,3,4}/README.md` | original spike READMEs, same category |
| `.planning/debug/resolved/open-routing-sequence-error.md` | closed debug record |
| `.planning/quick/260817-au7-*/SUMMARY.md`, `260817-d9m-*/{PLAN,SUMMARY}.md` | closed quick-task records |
| `.planning/quick/260817-ewg-*/260817-ewg-PLAN.md` | this task's own plan |

Not swept, by the same append-only reasoning that governs the BUILD-NOTES deviation history.

## Deviations from Plan

### Auto-fixed / scope-extended

**1. [Dispatch scope addition] Two live skill files brought under the plan's allowlist gate**
- **Found during:** Task 2
- **Issue:** `.claude/skills/spike-findings-prosoche/{SKILL.md, references/evidence-and-probes.md}`
  are auto-surfaced to every agent and both asserted a pass-expectation the reconciled rule makes
  unsatisfiable. Neither was in the plan's `files_modified`.
- **Fix:** Extended (not weakened) Task 2's changed-file allowlist gate to cover exactly these two
  paths, with additional assertions that neither still names `27 ios`, neither still demands both
  gates pass, both retain the `26/ios` prohibition, and `sources/` is unmodified.
- **Commit:** `7ccc7f9`

**2. [Rule 1 — Bug] Stale line citation `1805` corrected and made drift-proof**
- **Found during:** Task 1 restore
- **Issue:** The line number in the plan was wrong, and the predecessor's corrected numbers had
  already gone stale again under concurrent commits.
- **Fix:** Both citation sites anchor on the `STRING_ENVELOPE_PARAMS` symbol; line numbers recorded
  as a dated measurement with an explicit drift warning.
- **Commits:** `e768b93` (CLAUDE.md §1 and BUILD-NOTES §22.5)

**3. [Plan truth enforcement] `.planning/research/SUMMARY.md` added as a sixth propagation site**
- **Found during:** post-Task-3 sweep
- **Issue:** The plan's own must-have truth requires *every* live standing-instruction site naming a
  validator target to become a pointer. SUMMARY.md was one and was not enumerated.
- **Fix:** Converted to a pointer.
- **Commit:** `e03ed76`

**4. [Rule 1 — Bug] Duplicated paragraph during the §3 rewrite**
- **Found during:** Task 3
- **Issue:** The "A validator pass is necessary but not sufficient" paragraph was momentarily
  emitted twice while replacing the §3 rationale block.
- **Fix:** Duplicate removed in the same task, before commit. The original paragraph survives
  unchanged as the plan required.

### Execution-context deviation

This plan ran **unisolated, directly on `main`, by explicit user authorization**, after the
predecessor's worktree was destroyed mid-run by a concurrent session's cleanup sweep. Task 1's work
was restored from a verified patch, its gate re-run at the new HEAD (`TASK1-OK`), and committed
before any further work. Four other sessions were committing to `main` concurrently throughout.
Mitigations applied: every task committed atomically the instant it completed; all staging by
explicit path with `git diff --cached --name-only` confirmed before each commit; no
`git add -A`/`.`/`-a`, and no `checkout --`/`restore`/`clean`/`reset`/`stash`/`rebase`/`pull` at any
point. Two files modified by other sessions (`docs/CAPABILITY-DECISIONS.md`, a Phase 11 PLAN.md)
appeared in the working tree during Task 3 and were left completely alone and unstaged.

## Verification

| Check | Result |
|---|---|
| Gate A, both forks | `Validation passed.` exit 0 |
| Gate B, both forks, index-normalised | exactly `1 -` line, the recorded waiver, nothing else |
| `python3 docs/manifest_check.py` | passed (6 rows verified against disk) |
| `tools/build_state_engine.py` AST vs pre-task HEAD | AST-IDENTICAL — comment-only edit proven |
| `git diff --quiet -- src/` | clean, no shortcut artifact touched, nothing rebuilt or re-signed |
| `.claude/worktrees/`, spikes 006/007/008, `skills/.../sources/` | untouched, asserted |
| `.planning/phases/` | not written by this task |
| `grep -c 'corrected from' .claude/CLAUDE.md` | 0 (was 4) |
| `two-gate rule` token | present at all 7 propagation sites |
| DEV-01 original text | verbatim — `3675 of 3675` and `is.workflow.actions.conditional` both survive |

## Commits

| Task | Commit | Scope |
|---|---|---|
| 1 (restored) | `e768b93` | CLAUDE.md §1 canonical rule + BUILD-NOTES §22 evidence record |
| 2 | `7ccc7f9` | six sites → pointers, including the two skill files |
| — | `e03ed76` | research/SUMMARY.md, the unenumerated seventh site |
| 3 | `eb87f62` | BUILD-NOTES §3/§12/§13 DEV-01/§5 DEV-04 amendments + comment-only builder fix |

## Follow-ups (recorded, not acted on)

- **Fold gate B into the standard rebuild recipe once Phase 11 closes.** Phase 11's in-flight plans
  assert the 27 target appears nowhere in their commands, so gate B stays a manual advisory read
  until Phase 11 lands. Natural home afterwards: the same chain that runs the twelve `docs/*.py`
  checkers, reading gate B's output against the recorded waiver rather than `&&`-chaining it.
- **`VERIFIED_PARAMETER_KEYS` is now partly redundant with gate B.** Gate B checks parameter keys
  against the same v78 catalog the hand-maintained table was built from. Worth an audit of which
  entries the automated gate now covers. Not touched here — this task changed no build logic.

## Self-Check: PASSED

- `.planning/quick/260817-ewg-reconcile-validator-invocation-rule/260817-ewg-SUMMARY.md` — FOUND
- `.claude/CLAUDE.md` §1 two-gate rule — FOUND
- `docs/BUILD-NOTES.md` §22 — FOUND
- Commits `e768b93`, `7ccc7f9`, `e03ed76`, `eb87f62` — all FOUND in `git log`
