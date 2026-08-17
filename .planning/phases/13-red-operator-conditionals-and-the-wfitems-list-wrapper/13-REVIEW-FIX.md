---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
fixed_at: 2026-08-17T22:30:00Z
review_path: .planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-REVIEW.md
iteration: 1
findings_in_scope: 10
fixed: 9
skipped: 1
status: partial
---

# Phase 13: Code Review Fix Report

**Fixed at:** 2026-08-17
**Source review:** `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-REVIEW.md`
**Iteration:** 1

**Summary:**
- Findings in scope: 10 (CR-01, CR-02, CR-03, WR-01 … WR-07)
- Fixed: 9
- Skipped: 1 (CR-03 — deferred by decision, see below)

Info findings IN-01, IN-02 and IN-03 were out of scope (`fix_scope: critical_warning`) and are
untouched.

## End state — verified after the last commit

| Gate | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0** |
| Rebuild both generators, then `git status --porcelain` | **empty** — byte-idempotent |
| **Gate A** `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit **0** |
| **Gate A** `validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` | `Validation passed.`, exit **0** |
| **Gate B** (advisory, standalone per fork, in no `&&` chain and no definition of done) | exit **1**, exactly one `WFCreateNoteInput` waiver line each and nothing else |
| All twelve `docs/*.py` checkers | **exit 0** — none silenced, no assertion weakened |
| `artifacts/shortcuts/*.shortcut` | exactly the two canonical basenames, no suffix |

**Shipped artifacts (all six `MANIFEST.md` rows recomputed from disk in one pass):**

| Fork | Source | Bytes | SHA-256 |
|---|---|---:|---|
| Core | `src/PROSOCHE-Dumb.xml` | 2901248 | `c62706919f3fca4fc8f44f3361aeb0a60c85d22efa32b26b787f34f105353496` |
| Core | `PROSOCHĒ — Nine Circles — Core.shortcut` | 233802 | `b07497ba1a66506aaaa9c48134f463ceefeac7f4a656e86dad48b0a76414ac5b` |
| Aware | `src/PROSOCHE-Sentient.xml` | 2937929 | `709f53f88fef829a6e6af7187a656e8ea5a128f2a475656e44d18a2569f2d878` |
| Aware | `PROSOCHĒ — Nine Circles — Aware.shortcut` | 237842 | `212598cff4dd349316aee93c872fb2fd2862eee11f0278d8d02f69a89f447533` |

**The `WFItems` census moved, and the old figures are superseded everywhere.** Measured on the
sources *and* on the decrypted payload of both signed containers, identical per fork:

| Measure | before (13-04's build) | now |
|---|---:|---:|
| `is.workflow.actions.list` actions | 67 | 67 |
| `WFItems` rows, total | 666 | 666 |
| wrapped `{WFItemType: 0, WFValue: …}` | **660** | **616** |
| bare `<string>` rows | **6** | **50** |
| wrapped but attachment-free | **44** | **0** |
| dict rows missing `WFItemType` | 0 | 0 |
| per-action row counts | `[6] + [10]*66` | unchanged |

Per-array shapes now: `1 × (0 wrapped, 6 bare)` — the exit names; `22 × (10, 0)` — the baseline
family; `44 × (9, 1)` — the success and lapse families, which now ship the **mixed** array both
donors exhibit.

## Fixed Issues

### CR-01: `_list_row()` wraps 44 pure-literal rows in the variable-row wrapper

**Files modified:** `tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml`,
`src/PROSOCHE-Sentient.xml`, `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut`,
`artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut`,
`artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-220448.xml`,
`artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Aware-220500.xml`,
`artifacts/shortcuts/MANIFEST.md`
**Commit:** `365937e`
**Applied fix:** `_list_row()` now discriminates on **attachment-bearing-ness**, not Python
type: an attachment-free `WFTextTokenString` (a template with no `￼`, hence an empty
`attachmentsByRange`) goes out as the bare `<string>` both donors show. 44 rows per fork moved
from wrapped to bare — all of them at row position 8 (confirmed post-fix), the row
`getitemfromlist` selects at **Circle VIII** on both the success and lapse families.

**The whole ship chain was redone**, because changing the emitter invalidated plan 13-04's
re-sign and every MANIFEST row: provenance check exit 0 → both generators re-run → gate A clean
on both forks → gate B read standalone (one waiver each) → re-archived and re-signed under the
canonical names, both first attempt, neither signer quirk fired → both containers **decrypted**
through the AEA1 recipe and measured on the recovered plists → all six MANIFEST rows recomputed
from disk in one pass → twelve of twelve checkers green.

`WFItemType` values other than `0` remain deliberately unaudited; nothing here encodes or
documents another value.

---

### CR-02: BD-08's numeric-slot "confirmation" is refuted by the donor it cites

**Files modified:** `docs/CAPABILITY-DECISIONS.md`, `docs/BUILD-NOTES.md`
**Commit:** `26a6538`
**Applied fix:** BD-08's closing "confirmation, not a change request" paragraph is **retracted**
and replaced with the measured divergence. Re-measured independently for this fix: 90 (Core) /
97 (Aware) `WFNumberValue` parameters hold a Python `int` so `plistlib` emits `<integer>`, while
a fresh AEA1 decrypt of `.planning/debug/Donor 4.1.shortcut` reads
`<key>WFNumberValue</key><string>10</string>` beside `<key>WFCondition</key><integer>2</integer>`;
and 32 conditionals per fork hold a **dict** in `WFNumberValue` (eleven distinct variables,
enumerated in the record) that no donor covers at all. The slot is now marked **UNVERIFIED on
both axes**, with only the slot *choice* and the left-operand coercion left as settled.

**Option (b) of the review's two was taken deliberately** — record the divergence as an open
assumption (`docs/BUILD-NOTES.md` §28, new assumption **A5**; the section's "Four assumptions"
count corrected to five) rather than emit `str(number)`. Emitting the donor's string form would
move 90/97 live comparison operands on a build no device can run (`xcrun devicectl list devices`
reports none) and would close at best half the finding, since the 32 dict-valued sites stay
unevidenced either way. A5 names the cheapest device witnesses and the rung-4 donor that would
settle the variable case on its own.

---

### WR-01: `verify_list_item_wrappers()` cannot detect most of what its arming comment claims

**Files modified:** `tools/build_state_engine.py`, `tools/build_sentient.py`
**Commit:** `0b15e4b`
**Applied fix:** The guard now asserts the whole two-kind contract per row — a literal row is a
bare string; an attachment-bearing row is `{WFItemType, WFValue}` around a `WFTextTokenString`
whose `Value.attachmentsByRange` is **non-empty** (CR-01's inverse assertion) — and pins the
census `EXPECTED_LIST_ACTIONS / EXPECTED_WRAPPED_ROWS / EXPECTED_BARE_ROWS = 67 / 616 / 50`,
measured post-CR-01 and identical on both forks. `WFItemType`'s *value* stays unasserted.

**Sensitivity demonstrated against ten synthetic mutations**, all ten now raising `SystemExit`;
nine of them passed silently before:

| Mutation | before | now |
|---|---|---|
| all rows dropped (`WFItems: []`) | PASSED | census raise |
| a wrapped row flattened to a bare string | PASSED | census raise |
| one row simply deleted | PASSED | census raise |
| `{WFItemType: 0}` with `WFValue` missing | PASSED | per-row raise |
| `{WFItemType: 0, WFValue: "oops"}` | PASSED | per-row raise |
| List action with no `WFItems` key at all | PASSED | per-row raise |
| a row that is an `int` | PASSED | per-row raise |
| a double-wrapped row | PASSED | per-row raise |
| wrapped but attachment-free (the CR-01 shape) | PASSED | per-row raise |
| raw `WFTextTokenString` row (the original defect) | raised | raised |

Non-vacuity: the guard returns without raising on both shipped forks. The Aware arming comment
was corrected to describe real coverage. No new touch point in `tools/build_sentient.py` — the
guard was already in the `from build_state_engine import (…)` list and already invoked.

---

### WR-02: the Donor-5 "pin" cannot see a flattened operand

**Files modified:** `tools/build_state_engine.py`, `tools/build_sentient.py`
**Commit:** `f951248`
**Applied fix:** Added `EXPECTED_VARIABLE_TARGETS = 20` (measured, identical on both forks:
19 × condition 4 + 1 × condition 99) and a third raise asserting the census. The raise is
**appended last** deliberately: `docs/BUILD-NOTES.md` §28 records that the first raise masks the
second, and appending adds no new mask while leaving the recorded ordering untouched.

Sensitivity demonstrated: a variable-bearing target flattened to the literal `"Circle Next"`
**PASSED** before and now raises `… expected 20 …, found 19 …`; a raw literal promoted to a
variable-bearing envelope **PASSED** before and now raises `… found 21 …`. The Aware arming
comment now records that its "flattened" claim is backed by the census rather than by the shape
check.

---

### WR-03: `_list_row()` is neither total nor idempotent

**Files modified:** `tools/build_state_engine.py`
**Commit:** `0384e80`
**Applied fix:** The two-kind contract is asserted at the emitter, raising `SystemExit` (never a
bare `assert`) while the action list is still being built — long before any write. Demonstrated:
a literal `str` and a `WFTextTokenString` pass unchanged; `int`, `None`, an already-wrapped row
and a `WFTextTokenAttachment` envelope each raise. This closes the silent double-wrap that WR-01
showed the guard also could not see.

---

### WR-04: the pin raises `AttributeError`, not `SystemExit`, on a malformed target

**Files modified:** `tools/build_state_engine.py`
**Commit:** `9252e9b`
**Applied fix:** The pin now fails **closed**: a `Value` that is not a dict, or a `string` that
is not a `str`, falls through into `unpinned` and is reported with the offending action index.

Sensitivity demonstrated across four mutations, all four now `SystemExit … actions 158 (1
total)`: `Value` flattened to a plain `str` (was `AttributeError`), `Value.string` an `int` (was
`TypeError`), `Value.string` `None` (was `TypeError`), `attachmentsByRange` emptied (already
covered).

**Note:** the review's suggested patch still crashed with `TypeError` on a non-string `string`
(`"￼" not in (token_value.get("string") or "")` evaluates `in` against the int). The applied fix
tests `isinstance(token_string, str)` before the membership test.

---

### WR-05: `.claude/CLAUDE.md`'s axis preamble asserts device provenance that axis 8 does not have

**Files modified:** `.claude/CLAUDE.md`
**Commit:** `4c9fcce`
**Applied fix:** The preamble now attributes provenance **per axis** — axes 1–7 to the
2026-08-13/14 OPEN-path device session, axis 9 to the cycle-15 device error, and axis 8 to the
device-authored **donor decrypt**, explicitly flagged "structurally proven and NOT yet
device-observed in this project's own artifact" with a "do not cite axis 8 as device evidence"
instruction. The honest qualifiers elsewhere (`MANIFEST.md`, `docs/BUILD-NOTES.md` §28) are
untouched — the overclaim was weakened, never the qualifier that exposed it.

---

### WR-06: axis numbering conflicts between the docs and the code

**Files modified:** `tools/build_state_engine.py`, `tools/build_sentient.py`,
`docs/CAPABILITY-DECISIONS.md`
**Commit:** `4b61c52`
**Applied fix:** Four stale strings corrected in one pass, each recording what it used to say so
the renumbering does not itself become an unexplained drift:
`build_state_engine.py` "the EIGHTH defect class, alongside the seven parameter-defect axes" →
TENTH / NINE; `build_state_engine.py` "CYCLE 15 — the eighth axis" → "axis 9";
`docs/CAPABILITY-DECISIONS.md` BD-06 "an eighth class alongside the seven" → tenth / nine; and
`tools/build_sentient.py` "BD-06 Decision 5's eighth class" → TENTH — **a fourth site the review
did not list**, found by sweeping the class per the project's "fix whole classes, never
site-by-site" rule. `build_sentient.py`'s "Cycle 12, axis 7" was already correct and is
untouched.

---

### WR-07: the 660-row figure is described as "variable-bearing" in three documents

**Files modified:** `docs/BUILD-NOTES.md`, `artifacts/shortcuts/MANIFEST.md`,
`docs/CAPABILITY-DECISIONS.md`
**Commit:** `ec45453`
**Applied fix:** §28's family-2 table now reports **three** stages — phase start / after 13-01 /
after CR-01 — splitting the wrapped rows into attachment-bearing (616) and attachment-free
(44 → 0); reporting only "pre → post" is what hid CR-01 from a reader auditing the record.
MANIFEST's Phase 13 paragraph and closing ⚠ bullet now say "616 attachment-bearing rows wrapped,
50 bare" and name the correction. BD-08 keeps the measured 660 (the correct count of *unwrapped*
rows at phase start) but drops the "variable-bearing" label.

Assumption **A3** was **restated, not merely edited**: its original wording is preserved verbatim
because it is the reason the defect survived the plan, followed by what it missed — the claim is
stronger than "no donor exhibits it", since a donor exhibits the **opposite**. A3's status now:
the success and lapse families ship the donor-observed mixed array; the 22 all-wrapped baseline
arrays are the only residue still open, for the original weaker reason.

## Skipped Issues

### CR-03: `mirror_templates()` binds facts by placeholder ordinal — 9 Mirror templates display the wrong number

**File:** `tools/build_state_engine.py:733` (constants at `:80`, `:92`)
**Reason:** **Deferred by decision, not dropped.** Three grounds, all recorded in the todo:

1. **Pre-existing.** `mirror_templates()` predates Phase 13 and was not touched by it.
2. **A different defect class from the two this phase scoped.** Phase 13 scoped row framing and
   conditional operand shape; this is **fact binding**. The token envelope is perfectly
   well-formed and every `attachmentsByRange` offset is valid, so no guard in either family is
   even shaped to see it.
3. **A fix needs its own Mirror-wide re-verification.** It touches all thirty templates across
   three families, 22 call sites, 66 List actions and 616 row serializations, and invalidates
   the signed artifacts and all six MANIFEST rows again — a full re-sign plus decrypt cycle for
   a defect unrelated to the phase's hypothesis. Fixing it here would silently widen the phase.

**Original issue:** `facts[index]` uses the placeholder's *ordinal position*, not the fact the
prose names. The three-placeholder baselines line up and are correct; every one-placeholder
success/lapse template always binds `facts[0]` = `Circle Next`. At Circle IV on a success path
the user is told "Recorded pressure is 4" when 4 is the Circle. Nine templates affected —
SUCCESS rows 4, 5, 7, 9 and LAPSE rows 2, 3, 5, 7, 10 — **re-verified independently for the
todo**, not copied from the review.

**Captured at:** `.planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md`
(commit `d056f9a`). The todo is cold-runnable: mechanism, the full nine-row table with rendered
text plus both bound and intended variable, a self-contained repro script verified to print
exactly those nine lines, file anchors, two workable fix shapes, and completion criteria
including the full ship chain. It additionally records two things a reader would otherwise
re-derive: that the review's "word preceding each placeholder" suggestion **does not work as
stated** (measured — that word is `is` or `now` in all nine cases), and that row 10's
reachability is an **open sub-question** (ten templates per family, nine circles), so the count
may be eight rather than nine.

## Notes for the phase verifier

- **The ship gate was re-established, not merely re-claimed.** CR-01 changed the built XML, so
  plan 13-04's signed artifacts and MANIFEST rows were stale. Both forks were re-archived and
  re-signed and both containers were decrypted and measured; the census above is what shipped,
  not what the source claims.
- **The device verdict is unchanged: `BLOCKED`.** Nothing in this fix pass is device evidence.
  `13-UAT.md` stays `BLOCKED` and DIST-03 stays open. A user on any earlier signed build must
  **re-import** — the artifact is now `PROSOCHĒ — Nine Circles — Core.shortcut` at
  `b07497ba…`; anything else is the wrong build.
- **Two findings changed what the record claims rather than what ships** (CR-02, WR-05, WR-07),
  and all three did so by *weakening an overclaim*, never by deleting the qualifier that exposed
  it.
- **Every widened guard has a demonstrated failure mode.** WR-01 (ten mutations), WR-02 (two),
  WR-03 (four), WR-04 (four) — each demonstration paired with a non-vacuity run on the unmutated
  artifact. No guard was widened on assertion alone.

---

_Fixed: 2026-08-17_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
