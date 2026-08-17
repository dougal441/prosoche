---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 05
subsystem: records-and-guards
tags: [D-01, SAFE-01, CIRC-05, brightness-floor, supersession, frozen-canon, repo-gate, non-lexical-blind-spot]
status: complete
requires:
  - "16-03: the CODE half of D-01 — both forks ship brightness_floor 0 and dim_target 0, which is the right-hand side this plan's records and cross-check assert against"
  - "16-04: BUILD-NOTES §17 closed by that plan and deliberately not re-edited here"
  - "16-CONTEXT.md D-01 (LOCKED) and its 2026-08-18 revision block — the frozen canon, the split, the gate, the measured-not-exhaustive status"
  - "docs/sequence_dispatch_check.py::config_literal — the project-canonical Config reader, reused not reimplemented"
provides:
  - "docs/retired_clause_check.py — a standalone repo-scoped gate carrying two invariants, a two-tier commented allowlist and a stated blind spot"
  - "docs/CAPABILITY-DECISIONS.md BD-02 Supersession note — the explicit canonical-§21 supersession the three §21-citing sites depend on"
  - "src/CONFIG-BLOCK.md fenced Config JSON in agreement with both shipped forks, now pinned mechanically"
  - "SAFE-01 and CIRC-05 restated to the capture-and-durably-persist-then-restore property, as traceable amendments"
  - "a mechanical answer to the recurring question 'did we get them all this time' — for the lexical majority"
affects:
  - "16-VALIDATION.md's full-suite command now runs a gate that did not exist before wave 4"
  - "plan 16-06 carries the gate in its own verify chain"
  - "artifacts/shortcuts/MANIFEST.md still stale — docs/manifest_check.py RED by constraint D-MANIFEST until 16-06"
tech-stack:
  added: []
  patterns:
    - "citation-not-quotation for every supersession note — enforced mechanically, not by discipline"
    - "two invariants in one file, because they fail together"
    - "the allowlist IS the freeze, expressed in code"
    - "a guard states its own blind spot where a reader of the guard will find it"
    - "pin the agreement, not the values"
    - "locate by content, never by line number"
key-files:
  created:
    - docs/retired_clause_check.py
  modified:
    - src/CONFIG-BLOCK.md
    - docs/CAPABILITY-DECISIONS.md
    - docs/BUILD-NOTES.md
    - .planning/REQUIREMENTS.md
    - .planning/PROJECT.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
    - .claude/CLAUDE.md
    - .planning/todos/pending/2026-08-16-dimming-and-silence-as-distinct-circles.md
    - .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-VALIDATION.md
decisions:
  - "The §11 quotation in BD-02's Question is retained as a quotation of a frozen source with the floor sentence ELIDED and the elision marked — the only way to keep the citation without keeping the clause"
  - "Tier 2 of the allowlist is seeded EMPTY: after tasks 1 and 2 no live occurrence needed sparing"
  - "16-VALIDATION.md's registration was already discharged at plan time; a LANDED marker was added so a wave-5 reader does not drop the term, rather than re-registering it"
metrics:
  duration: ~50m
  completed: 2026-08-18
  tasks: 3
  commits: 3
  files: 10
requirements: [SAFE-01, CIRC-05]
---

# Phase 16 Plan 05: The RECORD half of D-01 — twenty-one sites, and the gate that reports the next one Summary

Every live documentation, requirement, roadmap and decision carrier that still asserted the
retired brightness-floor clause now states the property the build actually guarantees, and a
standalone checker reports every lexical survivor with file and line from now on — while saying
plainly, in its own source, that it cannot see the non-lexical residue and is therefore not proof
the class is empty.

## The site list is MEASURED and NOT PROVEN EXHAUSTIVE

Stated first because it is the finding that shaped the whole plan. This class was enumerated
**four times** before this plan and every enumeration claimed completeness: six sites, then eight,
then nine, then thirteen-or-more. Re-measuring during plan revision found **four more** (R13, R15,
R16, R20) appearing in no prior list — the fifth undercount, caught before execution.

**This summary makes no completeness claim either.** What it claims is narrower and checkable: the
21 measured sites are corrected, a repo-wide re-measurement at execution time found the same 18
lexical hits across the same 9 live files the plan predicted, and a gate now exists that makes a
sixth undercount **visible on every future run** rather than discoverable only by a sixth manual
pass.

### Was there a sixth undercount?

**No new site was found during execution** — the one honest caveat being that "no new site found"
is exactly what the four failed enumerations also reported. Two independent searches were run:

1. **The gate's own pattern families, repo-wide, historical paths excluded** — 18 hits across 9
   files, matching the plan's measured list exactly (R1 is a value drift not a lexical hit, R11
   shares R10's line, R17 was pre-discharged: 18 + 3 = 21).
2. **A deliberately WIDER scan** than the gate performs, for adjacent phrasings that could encode
   the bound without matching any family pattern: `0.10`, `0.12`, `lower bound`, `no lower than`,
   `not below`, `never below`, `minimum brightness`, `minimum value`, `safe band`, `prototype dim
   value`, `artificial floor`, `floor avoidance`, `must stay above`. Every hit resolved to one of
   three benign classes and none was a surviving assertion:
   - **Correct amendments describing the change** (the CONFIG-BLOCK change-log line naming the old
     values, `environmental_restore_check.py`'s "the lower bound this check used to place", the new
     BUILD-NOTES §30) — these narrate a retired value as history, which is the point.
   - **Unrelated subjects** — `heat.cap` "must stay above", `thresholds.Inferno`, a `time.sleep(0.12)`
     in a spike draft.
   - **SAFE-02, deliberately untouched** — `tools/build_state_engine.py:788`
     `number(0.10, "Silence Target")` is the **volume** target. D-01 is brightness-only.

**One targeted non-lexical probe was run**, because the known blind spot is precisely "the rule
re-encoded as a value": is the brightness write sourced from Config, or could a hardcoded literal
be a site no grep would reach? Measured — `tools/build_state_engine.py:732` is the only
`dim_target` reference in the generator and it reads `config("safety.dim_target", "Dim Target")`.
There is no hardcoded brightness literal. That was the highest-probability sixth site and it is
clean.

## The twenty-one sites and how each was handled

| # | Carrier | Handling |
|---|---|---|
| **R1** | `src/CONFIG-BLOCK.md` fenced Config JSON | `brightness_floor` `0.10 → 0`, `dim_target` `0.12 → 0`. Not a lexical hit — a **value drift**, and the one the gate's second invariant now pins mechanically. |
| **R2** | CONFIG-BLOCK `brightness_floor` table row | **All four assertions corrected**, not just the value: the default, the purpose text, the cited authority and the constraint cell's imperative prohibition. |
| **R3** | CONFIG-BLOCK `dim_target` table row | Value plus the constraint cell's band requirement. Now states the at-or-above-floor relationship the checker actually asserts. |
| **R4** | BD-02 Question, quoting canonical §11 | Floor sentence **elided with the elision marked**; citation retained. See "The §11 quotation" below. |
| **R5** | BD-02 Decision paragraph | Points at `safety.dim_target` and the new Supersession note. |
| **R6** | BD-02 Consequence-for-later-phases | Same. This paragraph names Phase 5's CIRC-05 build steps, so a stale line here is an instruction. |
| **R7** | BD-02 Phase 9 addendum | Its *provisional* and *fork-scoped* framing marked **superseded in place**; the finding itself retained; the retired quotation removed; the still-outstanding device claims restated explicitly so promotion is not read as device proof. |
| **R8** | `docs/BUILD-NOTES.md` CAP-16 Fallback cell | Corrected and pointed at BD-02. **This cell declared itself binding on Phase 5's CIRC-05 by requirement id** — a stale cell here is not a note, it is a live order. New **§30** appended recording the correction. |
| **R9** | `.planning/REQUIREMENTS.md` SAFE-01 | Restated to the real property, as a **traceable amendment** in the parenthetical form CIRC-03/CIRC-05/SAFE-05 already use for their Phase-10 amendments. |
| **R10** | REQUIREMENTS CIRC-05 statement clause | Restated: reversible *means* captured and durably persisted. |
| **R11** | REQUIREMENTS CIRC-05 trailing parenthetical | **The second correction on the same line.** Rewritten to describe the assertion 16-03 actually left behind. See below. |
| **R12** | `.planning/PROJECT.md` success criterion | Corrected to the property. |
| **R13** | `.planning/PROJECT.md` `## Constraints` Safety bullet | **NEW in this revision** — a *second* site in a file whose first was already listed. Corrected, and the bullet now says in its own text that it is the second of two. |
| **R14** | `.planning/ROADMAP.md` phase acceptance criterion | Asserted the clause **twice in one sentence**; both corrected. Volume and accessibility clauses untouched. |
| **R15** | ROADMAP Phase 9 criterion 4 | **NEW.** Was already substantively aligned; what it lacked was the main-line settlement. Amended visibly, meaning and 2026-08-16 date intact, band vocabulary removed. |
| **R16** | ROADMAP Phase 16 goal block | **NEW.** Said the correction "needs a decision on main". Now records D-01 as taken, with date and the plan that carried each half. |
| **R17** | ROADMAP plan-list tracking line | **Re-verified, not re-fixed** — see below. |
| **R18** | `.claude/CLAUDE.md` `## Constraints` Safety bullet | Settled on main **and** device-proof still outstanding — both facts, deliberately. |
| **R19** | `.claude/CLAUDE.md` capability-audit row 8 | A **second** site in a file already opened for R18. See below. |
| **R20** | `.planning/STATE.md` Phase 9 decision-log entry | **NEW.** Marked **superseded in place**, its three now-false claims named individually, with a new `[Phase 16]` D-01 entry added as the current record. Not deleted. |
| **R21** | pending todo | Recorded as settled with date and implementing plans; the rest of the todo (device work) explicitly still open. |

### R17 — re-verified as already discharged, and it was

Measured, not assumed: `grep -n "all six sites\|six sites" .planning/ROADMAP.md` returns **nothing**,
and the wave-4 plan-list line reads "21 measured record sites, the BD-02 §21 supersession note, and
the repo-scoped gate". It was **already correct on arrival**, discharged at plan time on 2026-08-18
during the six-plan rewrite. No edit was made to it. Recorded here as the plan required.

### R13 and R19 — the shape that caused two of the four prior undercounts

**Naming this explicitly, because that is how the next reader avoids repeating it.** Both are
*second* sites in files whose *first* site was already on an earlier list. `.planning/PROJECT.md`
carried the class in the success criteria **and** in `## Constraints`; `.claude/CLAUDE.md` carried
it in `## Constraints` **and** in capability-audit row 8's guidance cell.

**Opening a file is not the same as finishing it.** An enumeration that records "PROJECT.md — 1
site" and moves on is structurally unable to find the second one, and the file appears on the list,
so nothing looks missing. Task 2's verify now asserts each file's **two regions independently**
rather than asserting the file was touched.

### R11 — the correction inside the correction

CIRC-05's Phase-10 parenthetical closed by describing what `docs/environmental_restore_check.py`
guards, and that description asserted a strictness plan 16-03 removed. An amendment scoped to the
statement clause alone would have cited D-01 while **leaving a false assertion standing on the same
line** — and would have looked like a completed amendment in any diff.

Read from the checker as 16-03 left it rather than from what this plan predicted:

```
:283  require(isinstance(dim_target, (int, float)) and dim_target >= 0,
:286  require(isinstance(floor, (int, float)) and dim_target >= floor,
```

So the parenthetical now says: a number **at or above 0** and **at or above `brightness_floor`** —
and notes the CIRC-05 boundary, that with both shipped at `0` the floor binds **exactly, at
equality**, rather than never.

## The BD-02 Supersession note — the named deliverable

Three of the amended sites (R2, R8, R19) **keep citing canonical §21 as their authority**. Without
this note each reads as amended text pointing at an unamended source: the record would look
consistent while being incoherent. It records, as three separately-scoped statements:

1. BD-02's own historical band-and-floor text is superseded — cited, never restated, amended in
   place rather than deleted.
2. The Phase 9 addendum is promoted from provisional and fork-scoped to **settled on main**; what
   it observed is unchanged, only its status.
3. **Canonical strategy §21's floor clause is superseded on the main line by D-01. The canonical
   strategy is retained UNMODIFIED as the original design input and was not edited. BD-02 governs
   where the two disagree** — and the note names the three §21-citing sites by location, so the
   dependency is legible rather than implied.

It also records that the safety property is unchanged and was never the bound, and that the
**durable-persistence half became true in plan 16-01** — before it, no build could have satisfied
the restated requirement, which is what makes the restatement a correction rather than a weakening.
Scope is stated: **brightness only**; BD-03's volume position and BD-01's Ash position untouched.

### The §11 quotation

BD-02's Question quotes canonical §11 — a frozen source — and that quotation contained the retired
clause verbatim. Two rules collided: *quote frozen sources faithfully* and *never leave the retired
clause live in a file*. Resolved by **eliding the floor sentence and marking the elision**, with a
bracketed pointer saying what was elided, why, and where the authority now lives. The citation
survives; the clause does not. The gate would have reported the alternative.

## The BD-01/BD-02/BD-03 consistency note — re-read, and it SURVIVES

Re-read in full (`docs/CAPABILITY-DECISIONS.md:104`) as the plan required. **It still reads true
and was not edited.**

Why it survives: the note's claim is that all three decisions are **the same rule applied to three
different evidentiary outcomes** — BD-01 landed message-only because CAP-20 found no read-back path
at all; BD-02 and BD-03 landed stateful because CAP-17/CAP-19 found one. The rule it invokes is
§21's **read-before-write-and-restore** rule, and it closes by asserting that none of the three
authorises a stateful change whose original cannot be captured on the run it fires.

**D-01 changes a bound, not that rule.** It does not move BD-02 between the two ends the note
describes, it does not touch BD-01 or BD-03, and its own Supersession note reaffirms the
capture-and-restore property the consistency note turns on. The one nuance worth recording: the note
says all three are governed by "the identical canonical strategy §21 rule", and §21 is now
*partially* superseded — but what is superseded is the **floor clause**, not the read-and-restore
clause the note actually relies on. The note was left byte-identical rather than patched, because
patching an unbroken note to look updated is how a record acquires noise.

## The gate — `docs/retired_clause_check.py`

Two invariants in one file, because they fail together: both are a **record drifting from the build
it describes**.

**Invariant 1 — no live file still asserts the retired clause.** Walks the repo, reports **every**
survivor in one run with file, line, matched pattern and the offending text. Deliberately not the
first: this class was under-fixed four times by correcting what was visible and re-measuring
afterwards, and a gate that stopped at the first hit would cost one full pass per site and reproduce
that loop exactly.

**Invariant 2 — the record agrees with the build.** Parses `src/CONFIG-BLOCK.md`'s fenced Config
JSON and **both** forks' Config literal via `sequence_dispatch_check.config_literal` — the
project-canonical reader, reused rather than hand-rolled a fourth time — and asserts all three agree
on `brightness_floor` and `dim_target`. **It pins the agreement, not the values**, so it survives the
next legitimate tuning change instead of being edited (or deleted) by it. This is the assertion that
would have caught the CONFIG-BLOCK miss mechanically instead of by a fifth enumeration pass.

### Verbatim output — the two-occurrence control

The acceptance criterion is that the gate reports **every** survivor, not the first. Two occurrences
injected into two different files, one from Family A and one from Family B:

```
EXIT: 1
retired clause check: FAILED -- 2 live occurrence(s) of the retired brightness-floor clause survive, in 2 file(s):
  docs/_retired_clause_probe_a.md:1  [never set to zero]  Synthetic control A for docs/retired_clause_check.py: never set to zero.
  docs/_retired_clause_probe_b.md:3  [10-15]  the prototype dim value sits in the 10-15 band.
  Correct each one by CITING where the clause lived -- BD-02's original Decision paragraph, or canonical strategy Sec 21 -- and never by restating it. An amendment that quotes what it supersedes is itself a surviving occurrence and this gate reports it as one. If an occurrence is deliberate, add it to ALLOWED_SITES with a written reason.
```

Both named, with file, line **and which pattern matched**. Both probes removed; the gate returned to
green.

### Five controls, all run — a guard that cannot be made to fire is decoration

| Control | Result |
|---|---|
| Two occurrences, two files (above) | **both** reported in one run, exit 1 |
| Probes removed | returns to green, exit 0 |
| **Family C scoped hit** — `strictly positive` 6 lines from a `dim_target` mention | **FIRES** (`docs/_probe_c_near.md:7`) — the ±6 window earns its width |
| **Family C false positive** — `strictly positive epoch`, no dim-target anchor | **correctly silent**. A guard that cries wolf gets disabled |
| **Allowlist actually spares** — a probe planted under `.planning/phases/` | **not reported**, exit 0 |
| **Walk coverage** — probes in `.claude/`, `.planning/`, `.planning/todos/pending/` | all three **walked and reported** |
| **Todo asymmetry** — same probe under `.planning/todos/completed/` | **correctly spared** |
| **Invariant 2** — `dim_target` in the fenced JSON perturbed to `0.12` | **FIRES**, naming both sides of the disagreement; restored → green |

Invariant 2's firing output, verbatim:

```
retired clause check: FAILED -- Dumb: the built Config literal has safety.dim_target = 0 but
src/CONFIG-BLOCK.md's fenced JSON -- which that file calls the transcription source, not a
description of one -- says 0.12. The record and the build disagree about a safety value;
fix the record, or rebuild, but do not leave them apart
```

### The allowlist — explicit, commented, two tiers

Held as named constants where every entry carries its reason **on the same line**, not buried in a
walk condition. An unexplained exclusion is indistinguishable from a defect.

**Tier 1 — path prefixes, 8 entries.** The frozen canonical strategy; `.planning/phases/`;
`.planning/debug/resolved/`; `.planning/todos/completed/`; `.planning/research/`; `artifacts/`;
`.git/`; and the gate's own source (which necessarily holds the pattern list — without this entry it
reports itself and can never be green).

**The `.planning/phases/` breadth is stated honestly in its own comment**, as the plan required: it
is broad, it subsumes both the closed prior-phase directories **and this phase's own plans, contexts
and summaries** (which quote the retired clause precisely in order to describe its retirement), and
the tradeoff is named explicitly — *a genuinely live authority document must never be filed there,
because this gate will not read it.* The comment then lists what the gate **does** walk, so the
boundary is legible: `docs/`, `src/`, `.planning/{PROJECT,ROADMAP,REQUIREMENTS,STATE}.md`,
`.planning/todos/pending/` and `.claude/CLAUDE.md`.

One deliberate asymmetry is documented at its entry: `.planning/todos/completed/` is excluded but
`.planning/todos/pending/` is **not**, because a pending todo is live work — and one of them carried
a real site (R21).

**Tier 2 — anchored per-site entries: `(path, distinguishing substring, reason)`. SEEDED EMPTY.**
No live occurrence needed sparing after tasks 1 and 2. **Zero entries were added, so there is
nothing to list** — recorded here explicitly because "none" is the answer to the plan's question, not
an omission. Any future entry must anchor on **content, never a line number**: every anchor in this
phase shifted at least once, several twice (the plan's own `strictly positive epoch` anchor moved
`:2084 → :2244` between the window sweep and the gate being written).

### The stated blind spot

A boxed warning in the module docstring and a dedicated commented block name it plainly:

> **THIS CHECK CANNOT CATCH NON-LEXICAL ENCODINGS. A GREEN RESULT IS NOT PROOF THAT THE CLASS IS
> EMPTY.**

It cites `docs/phase5_self_check.py`'s former line 117 — which asserted the brightness parameter was
not zero, **the retired rule as a value comparison carrying none of the vocabulary** — with the
measurement that proves it: a case-insensitive grep of every pattern in the gate over that whole
file returned **zero** matches while the site was live. It was reachable only by reading the code;
plan 16-03 fixed it by hand. The comment also points at the replacement's own inline reasoning,
which records the same status from the other side, and at plan 16-05's `<measured_site_list>` as the
human-reasoned residue — noting that that list is measured and **not proven exhaustive**.

### Family C's ±6 window

Scoped to a dim-target mention within ±6 lines, with the measured false positive
(`tools/build_state_engine.py`'s strictly-positive-**epoch** comment — a UNIX timestamp, which
genuinely is strictly positive) **cited by name beside the scoping**, and the sweep recorded: ±2 and
±4 miss a real site whose nearest anchor is six lines away; ±6 is the smallest window that catches
every real site; the false positive stays excluded out to ±10, so there is a four-line margin either
side and the choice is not delicately balanced. The comment says to anchor that citation **by the
word `epoch`, never by line**, and records that it had already moved `:2084 → :2244`.

### Registration

`16-VALIDATION.md`'s full-suite command **already contained** `python3 docs/retired_clause_check.py`
— discharged at plan time, like R17. Rather than re-registering it, a **`✅ LANDED 2026-08-18`**
marker was added ahead of the existing expected-absent note, so a wave-5 reader runs the term instead
of dropping it, while the original instruction remains correct for anyone replaying waves 1–3. Plan
16-06 carries the gate in its own verify chain.

## Verification

| Check | Result |
|---|---|
| Task 1 verify script | passed — R1–R11 corrected, fenced JSON parsed **as JSON** (floor 0, target 0, `allow_volume_increase` still `false`), all four files cite D-01 and carry no retired vocabulary, BD-02 records the §21 supersession and the canon retained unmodified, no frozen path in the commit |
| Task 2 verify script | passed — R12–R21, both PROJECT.md regions, both CLAUDE.md regions asserted independently, R17 still discharged, no frozen path in the commit |
| Task 3 verify script | passed — gate green, allowlist tokens present, blind spot named, `config_literal` reused, fires on injection and names the file, returns to green, registered in the full suite |
| `python3 docs/retired_clause_check.py` | `retired clause check: passed -- 0 live lexical occurrences (8 allowlisted path prefixes, 0 anchored sites); src/CONFIG-BLOCK.md agrees with both built forks on brightness_floor=0, dim_target=0 [LEXICAL ONLY…]` |
| `python3 docs/environmental_restore_check.py` | `environmental restore check: passed` |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed` |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| `python3 docs/phase9_self_check.py` | exit 0 |
| `python3 docs/note_identity_check.py` | exit 0 |
| `python3 docs/manifest_check.py` | **RED as expected** — constraint D-MANIFEST, until 16-06 re-signs. **No MANIFEST row edited.** |

No rebuild was run and none was needed: this plan touches no generator and no artifact. Both fork
XMLs are byte-identical across all three commits.

## Prohibitions honoured

- **`PROSOCHE_Nine_Circles_Canonical_Strategy.md` was NOT modified.** It is frozen by user decision
  2026-08-18. Confirmed against all three commits' file lists. BD-02's Supersession note carries the
  correction instead — which is the whole reason that note exists — and the freeze is additionally
  encoded as the gate's first tier-1 allowlist entry, so it survives the memory of whoever decided it.
- **No closed prior-phase directory, no `.planning/debug/resolved/`, no `.planning/todos/completed/`,
  no `.planning/research/`, nothing under `artifacts/`** — asserted by both task verifies against
  `git show --name-only HEAD`, anchored first on one of the task's own declared files so the check
  cannot pass vacuously against an earlier commit.
- **Nothing under `tools/`, no `src/PROSOCHE-*.xml`, no pre-existing `docs/*.py` checker.** The only
  `docs/*.py` file written is the new gate.
- **No amendment or supersession note reproduces the retired clause.** Enforced mechanically: every
  touched file is grepped after the edit, and the gate itself now reports a quoted clause as a
  survivor.
- **No allowlist entry without a written reason** — tier 1 carries eight reasons, tier 2 is empty.
- **D-01 was not re-opened or re-litigated.** It is a LOCKED user decision; this plan implements its
  record half.
- **No MANIFEST row edited** (D-MANIFEST). `STATE.md`'s and `ROADMAP.md`'s *content* corrections
  (R14–R17, R20) were made because the plan declares them; **no progress, status or plan-count
  bookkeeping was touched** — the orchestrator owns those writes.

## Threat mitigations applied

- **T-16-22** (repudiation, a fifth silent undercount, high): mitigated as specified — a measured
  human-reasoned list **paired** with a repo-scoped gate, with neither presented as complete. The
  gate reports every survivor in one run and is proven able to fire by injected controls. Two
  independent execution-time re-measurements (the gate's families, and a deliberately wider adjacent
  vocabulary) plus one targeted non-lexical probe found no sixth site.
- **T-16-23** (spoofing of completeness, a green gate read as an empty class, high): the blind spot
  is a boxed warning in the docstring **and** a dedicated comment block, citing the measured
  zero-match instance. The passed line itself ends `[LEXICAL ONLY: this is not proof the class is
  empty]`, so even a reader who never opens the source is told.
- **T-16-24** (tampering with the frozen historical record, high): authored as prohibitions, enforced
  in both task verifies against the task's own commit, **and** encoded as the gate's tier-1
  allowlist with per-entry reasons.
- **T-16-25** (an amendment quoting the clause it retires, medium): every touched file grepped after
  amendment; the §11 quotation resolved by marked elision rather than by keeping the clause.
- **T-16-26** (CONFIG-BLOCK drifting from the shipped literal, medium): invariant 2, pinning the
  agreement rather than the values, demonstrated to fire on injected drift.
- **T-16-SC** (low, accepted): no external package installed. The gate is stdlib only (`json`,
  `plistlib`, `re`, `sys`, `pathlib`) plus one import of an existing project checker.

## Deviations from Plan

**None.** All three tasks executed as written; no auto-fix rule was invoked and no architectural
question arose. No file outside the plan's declared ten was modified.

Two items were **re-verified rather than re-fixed**, exactly as the plan directed: R17 (the ROADMAP
plan-list line) and the `16-VALIDATION.md` full-suite registration were both already discharged at
plan time. The only edit made to `16-VALIDATION.md` was adding a `LANDED` marker so a wave-5 reader
does not drop a term that is now green — a clarification, not a correction.

One judgement call worth recording as a decision rather than a deviation: **the BD-01/BD-02/BD-03
consistency note was left byte-identical.** The plan required it be re-read and confirmed, with a
halt if it did not survive. It survives (reasoning above), so it was not touched.

## Authentication Gates

None.

## Known Stubs

None. No stub, placeholder, TODO, skipped test or unrun `<verify>` was introduced. All three task
verify blocks were run in full and passed, and every control listed above was **run**, not asserted.

## Device-gated work NOT done here (recorded, not inferred)

This plan is entirely rung-1 (file-level) work and claims **nothing** about hardware. Records were
written with that boundary held explicitly, because the failure mode here is a settled *decision*
being read as a settled *device fact*:

- **SAFE-01's `backstop` truth** — that a brightness target of `0` renders as *dim rather than black
  or unusable* on a real iPhone — rests on **one unrepeated user report** and is a device observation
  this plan cannot make. Every site that mentions it describes the **property**, and none vouches for
  the hardware.
- **The capture-and-restore loop remains device-unproven.** Plan 16-01 made the capture persist
  before the device is changed, which is what makes the property satisfiable at all, but no run of it
  has happened on a phone. `.claude/CLAUDE.md`'s Safety bullet, BD-02's addendum and the pending todo
  each now state **both** facts — settled decision, outstanding device proof — deliberately, so
  promotion cannot be misread.

Both remain **BLOCKED on DIST-03**: paired device present, `tunnelState: disconnected`, no live
session to drive. 16-06's instrument settles them.

## Follow-up for later plans in this phase

- **16-06** re-signs and refreshes the MANIFEST rows; `docs/manifest_check.py` stays RED until then
  and must not be fixed by editing rows. It should carry `docs/retired_clause_check.py` in its verify
  chain — the gate is registered in `16-VALIDATION.md`'s full-suite command and is now **green**, so
  the term should be run, not dropped.
- **Any future plan that changes `safety.brightness_floor` or `safety.dim_target`** must change
  `src/CONFIG-BLOCK.md`'s fenced JSON in the same commit. Invariant 2 pins the agreement, not the
  values, so a legitimate tuning change needs no checker edit — only both sides moved together.
- **The gate is lexical.** A future rule encoded as a value check, a threshold or an inequality will
  not be seen. That is stated in the gate's own source and is not a defect to fix by widening the
  patterns; it is why the human-reasoned residue list exists.

## Self-Check: PASSED

Files claimed created, verified present on disk: `docs/retired_clause_check.py` (executes, exit 0).

Files claimed modified, verified present on disk: `src/CONFIG-BLOCK.md`,
`docs/CAPABILITY-DECISIONS.md`, `docs/BUILD-NOTES.md`, `.planning/REQUIREMENTS.md`,
`.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.claude/CLAUDE.md`,
`.planning/todos/pending/2026-08-16-dimming-and-silence-as-distinct-circles.md`,
`16-VALIDATION.md`.

Commits claimed, verified in `git log`: `30126e6` (task 1), `53856bb` (task 2), `708e2fd` (task 3).
No commit deleted a tracked file (`git diff --diff-filter=D` empty for each). Working tree clean
after each commit.
