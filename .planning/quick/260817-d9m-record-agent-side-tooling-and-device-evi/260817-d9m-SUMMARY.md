---
phase: quick-260817-d9m
plan: 01
subsystem: docs
status: complete
tags: [evidence-protocol, tooling, simulator, device-uat, generator-drift]
requires:
  - .claude/CLAUDE.md §8 (corrected AEA1 recovery, quick task 260814-kqm)
  - docs/BUILD-NOTES.md §14 (device evidence — reading a signed .shortcut back)
  - docs/BUILD-NOTES.md §13 DEV-01 (validator --target-platform correction)
provides:
  - .claude/CLAUDE.md §9 — four-rung evidence-escalation ladder and probe policy
  - .planning/research/STACK.md §9 — byte-identical copy in the generator source
  - docs/BUILD-NOTES.md §3 — simulator/probe citation classes and recording duty
affects:
  - every future agent's choice of evidence channel for an open runtime question
  - regeneration of the GSD stack block from .planning/research/STACK.md
tech-stack:
  added: []
  patterns:
    - "Evidence-escalation ladder: cheapest/weakest rung first, never climb past the question, never skip a rung that would have caught a defect in the probe"
    - "Section body authored once and inserted byte-identically into both the managed block and its generator source, gated by diff"
key-files:
  created: []
  modified:
    - .claude/CLAUDE.md
    - .planning/research/STACK.md
    - docs/BUILD-NOTES.md
decisions:
  - "§9's ladder extends the Conventions Evidence hierarchy by cross-reference rather than rewriting it — that list lives in a separate managed block sourced from .planning/spikes/CONVENTIONS.md"
  - "STACK.md Family-A (AEA1) drift fixed at all four sites; Family-B (--target-platform ios) drift deliberately deferred at all eight"
  - "docs/CAPABILITY-DECISIONS.md deliberately not edited — no probe result exists yet to record, and a placeholder BD entry would violate the do-not-fabricate posture"
metrics:
  duration: ~25 min
  tasks: 3
  files: 3
  completed: 2026-08-17
---

# Quick Task 260817-d9m: Record Agent-Side Tooling and Device-Evidence Channels Summary

Turned `## 9.` from a tooling inventory into a working evidence protocol — a four-rung
escalation ladder with an explicit rung-2 ceiling — written identically into `.claude/CLAUDE.md`
and its generator source, plus a repair of the known-false AEA1 drift in that generator and an
extension of BUILD-NOTES' binding citation rule so simulator and probe observations are both
citable and recordable.

## What Was Built

**`.claude/CLAUDE.md` §9 and `.planning/research/STACK.md` §9** (49 lines, byte-identical,
ordered §8 < §9 < `## Recommended Stack` in each):

- **Tool table** — `/ponytail` (sanctioned, but bounded: laziness never licenses skipping the
  seven parameter-defect axes or the do-not-fabricate protocol), the iOS Simulator
  (`mcp__Claude_Code_iOS_Simulator__control` plus `xcrun simctl`), and iPhone Mirroring.
- **Measured simulator inventory**, all three `xcrun simctl` commands named as evidence and
  re-verified during execution: one runtime, iOS 26.5 (26.5 - 23F77) — inside the project's
  declared "iOS 26.x" target; iPhone 17 Pro `79A84C29-DB62-40A2-AC3F-CCB5F8192F86` booted among
  five iPhones and five iPads; 25 apps, `com.apple.shortcuts` present, `com.apple.mobilenotes`
  absent.
- **The four-rung ladder** — file-level analysis / simulator probe / device probe over
  mirroring / user-run probe or donor export, each with what it settles and what it costs. Its
  governing rule cuts both ways: never climb higher than the open question requires, and never
  skip a rung that would have caught a defect in the probe itself.
- **Rung 2's ceiling**, enumerated with measured reasons — the Control Room Note path in full
  (no `com.apple.mobilenotes` on the simulator), Apple Intelligence (not AI-capable hardware),
  Personal Automation triggers (user-created on device), and real-hardware environmental
  capture-and-restore. A rung-2 pass may never raise a verdict on any of these.
- **Probes vs. donors** — a donor is evidence the user already happens to have; a probe is
  evidence we deliberately manufacture, so it can be aimed at precisely the open question.
  Illustrated with a verified-open rung-2 target: the unaudited `CoercionItemClass` values for
  boolean, file, dictionary and entity-reference operands (`## Conventions` rule 6).
- **Two standing policies** — probes are simulator-tested before they reach the user's iPhone;
  once mirroring is live the agent drives the device itself rather than issuing a list of taps
  (request-first is unchanged).
- **The recording duty** — a probe result goes into `docs/BUILD-NOTES.md` and, where it settles
  a capability question, `docs/CAPABILITY-DECISIONS.md`.

**`.planning/research/STACK.md` §8** brought into agreement with the corrected `.claude/CLAUDE.md`
§8, written in the register of a capability this project has exercised rather than a caveat.

**`docs/BUILD-NOTES.md` §3** gained a 15-line subsection between the binding citation rule and
the runnable lookup snippet, admitting the two new evidence classes, ranking them (below §11/§14
device evidence, above ToolKit-catalog inference), stating the ceiling as a rule, and carrying
the recording duty. It restates no measured fact, so it cannot drift out of step with §9.

## Task Commits

| Task | Name | Commit | Files |
| ---- | ---- | ------ | ----- |
| 1 | Author §9 as an evidence protocol, insert into both files | `bcea9ae` | `.claude/CLAUDE.md`, `.planning/research/STACK.md` (98 insertions, 0 deletions) |
| 2 | Sync STACK.md's AEA1 drift (Family A only) | `1c9350f` | `.planning/research/STACK.md` (16 insertions, 4 deletions) |
| 3 | Admit simulator and probe evidence in BUILD-NOTES §3 | `5e0a895` | `docs/BUILD-NOTES.md` (15 insertions, 0 deletions) |

## Verification

All three task gates ran as written and passed. No gate was weakened or rewritten.

| Gate | Result |
| ---- | ------ |
| Exactly one §9 heading in each file | 1 and 1 |
| §9 body byte-identical across both files | `diff` clean |
| §9 length within 45-90 lines | 49 |
| Closed `speaktext`/DEV-C3-03 example absent from §9 | 0 matches (section-scoped; the legitimate §3 Speak Text capability row is untouched) |
| Section order §8 < §9 < `## Recommended Stack` | CLAUDE.md 187 < 207 < 256; STACK.md 243 < 265 < 314 |
| Numbered run 1..9 unbroken | confirmed in both files |
| STACK.md §8 retitled | 1 match |
| `aea decrypt` / `aa extract` present in STACK.md | 3 / 3 |
| Three disproven AEA1 literals removed | 0 / 0 / 0 |
| Family-B `--target-platform ios` sites unchanged | exactly 8 |
| BUILD-NOTES subsection between the two §3 headings | gap 19 lines (> 6 required) |
| BUILD-NOTES cross-references CLAUDE.md §9 and names CAPABILITY-DECISIONS | both present |
| Changed-file allowlist | only the three target files |
| `src/`, `tools/`, `artifacts/`, `assets/` untouched | 0 |
| CLAUDE.md and BUILD-NOTES additive-only | 0 removed lines each |

The three `xcrun simctl` commands in `<measured_facts>` were re-run during execution and
reproduced the planning values exactly. No measured fact was replaced by inference.

`docs/CAPABILITY-DECISIONS.md` and `.planning/spikes/CONVENTIONS.md` were not touched.

## Open Observations for the User

### 1. Deferred — STACK.md Family-B drift (8 sites still recommend `--target-platform ios`)

`docs/BUILD-NOTES.md` §13 DEV-01 withdrew `--target-platform ios` in favour of `all`, and
`.claude/CLAUDE.md` already carries the correction. The generator source does not. Deferred
deliberately to keep this task atomic — five sections is broader than one quick task should
absorb — and the Task 2 gate pins the count at exactly 8 so over-reaching would have failed as
loudly as under-reaching.

**Current line numbers in `.planning/research/STACK.md`** (re-measured after this task's
insertions; the plan's pre-insertion numbers were 70, 74, 77, 80, 127, 262, 269, 294):

| Line | Section | Site |
|---|---|---|
| 70 | §1 exact validator invocation | flag line in the fenced invocation |
| 74 | §1 | full `validate-shortcut` example command |
| 77 | §1 | "Recommended target flags for this project" |
| 80 | §1 | the `--target-platform ios` rationale bullet |
| 127 | §2 practical rule | "validate with `--target-platform ios`" |
| 323 | Recommended Stack table | Validator target row |
| 330 | Build sequencing step 4 | Craig Loop invocation |
| 355 | What NOT to use | the "Use instead" cell |

**Why it matters:** until this lands, a regeneration of the GSD stack block from STACK.md would
reintroduce a validator invocation the project measured as rejecting 3675 of 3675 actions on a
known-good file. Worth its own quick task.

### 2. Left un-amended by decision — the `### Evidence hierarchy` under `## Conventions`

That four-item list still ranks **donor > golden corpus > ToolKit catalog > inference**, naming
neither probes nor the simulator. It is in genuine tension with the new four-rung ladder: §9
places a simulator probe at rung 2 and a donor export at rung 4, while the hierarchy ranks
donors first outright.

§9 cross-references and extends it rather than rewriting it, because it lives in a **separate
managed block** sourced from **`.planning/spikes/CONVENTIONS.md`** — not `.planning/research/`.
Amending it means a fourth file and a second generator source to keep in sync, for a tension one
cross-reference line resolves.

Flagging the path in case you want the hierarchy itself rewritten. Note the two are reconcilable
as written: the hierarchy ranks *authority when sources disagree*, the ladder ranks *cost and
reach when a question is open* — a donor is legitimately the most authoritative and among the
most expensive to obtain. If you want that stated explicitly rather than left implicit, that is
the edit to make.

### 3. `docs/CAPABILITY-DECISIONS.md` untouched

Both §9 and BUILD-NOTES §3 **name** it as the destination for a probe result that settles a
capability question, but no probe result exists yet. Its 498 lines are a ledger of settled
`BD-NN` decision records with no protocol or how-to-record section, so a rule about recording has
no natural home there — and creating an empty placeholder BD entry would violate the project's
own do-not-fabricate posture. The file gets touched by the task that produces a real result.

## Deviations from Plan

**Two, both procedural, neither changing any deliverable.**

1. **Task 3 committed one file, not three plus artifacts.** The plan's Task 3 said "commit all
   three files plus this quick task's own artifacts in one commit." The orchestrator's execution
   constraints override this: commit each task atomically, and leave the GSD docs artifacts
   (SUMMARY.md, STATE.md, PLAN.md) to the orchestrator. So the three deliverable files landed
   across three atomic task commits and no GSD artifact was committed here. All content required
   by the plan is committed.

2. **Verify gates were run as discrete commands rather than the single chained one-liners.**
   The worktree sandbox refuses compound shell commands it cannot statically prove stay inside
   the worktree. Every assertion in every gate was executed and checked individually — the
   results table above is the full set, with the same literals, counts and thresholds the plan
   specified. Nothing was skipped or relaxed.

**No Rule 1-4 deviations.** No bugs found, no missing critical functionality, no blocking issues,
no architectural decisions required. The plan's `<probe_examples_correction>` was honoured — the
closed `speaktext`/DEV-C3-03 example was not used, and the substituted `CoercionItemClass` target
was confirmed still open in `## Conventions` rule 6 before citing it.

## Known Stubs

None. This task produced prose protocol only — no code, no placeholder values, no unwired data
paths.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern, or schema change at a trust
boundary. The plan's threat register anticipated the two real risks here — tampering with
existing CLAUDE.md content (T-d9m-01) and a simulator pass being used to close a device-gated
question (T-d9m-02) — and both mitigations were verified: the additive-only gate reported zero
removed lines, and rung 2's ceiling is stated in §9 and repeated in rule form in BUILD-NOTES §3.

## Self-Check: PASSED

Files verified present on disk: `.claude/CLAUDE.md` (§9 at line 207), `.planning/research/STACK.md`
(§9 at line 265, §8 retitled at 243), `docs/BUILD-NOTES.md` (new subsection at line 66-84).

Commits verified in `git log`: `bcea9ae`, `1c9350f`, `5e0a895` — all present on
`worktree-agent-ad0c9bfcbfed47530`, working tree clean after the third.
