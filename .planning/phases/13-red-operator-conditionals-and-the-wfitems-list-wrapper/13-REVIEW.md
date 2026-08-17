---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
reviewed: 2026-08-17T00:00:00Z
iteration: 2
depth: standard
files_reviewed: 8
files_reviewed_list:
  - tools/build_state_engine.py
  - tools/build_sentient.py
  - .claude/CLAUDE.md
  - docs/BUILD-NOTES.md
  - docs/CAPABILITY-DECISIONS.md
  - artifacts/shortcuts/MANIFEST.md
  - src/PROSOCHE-Dumb.xml
  - src/PROSOCHE-Sentient.xml
findings:
  critical: 0
  warning: 2
  info: 3
  total: 5
deferred_by_decision: 1
status: issues_found
---

# Phase 13: Code Review Report (iteration 2)

**Reviewed:** 2026-08-17
**Depth:** standard
**Files Reviewed:** 8
**Status:** issues_found — 0 critical, 2 warnings, 3 info, plus 1 finding deferred by decision with a cold-runnable todo

## Summary

Everything the fixer reports was re-derived independently against the live tree; nothing was
taken on its word. The two critical findings that were fixed are fixed correctly and minimally,
the widened guards are genuinely sensitive rather than wider on paper, and the ship chain is
intact.

**Re-measured from scratch:**

| Check | Result |
|---|---|
| CR-01 on the **decrypted signed containers** (both forks) | 67 List actions, 666 rows, **616 wrapped / 50 bare / 0 attachment-free wrapped / 0 missing `WFItemType`**, per-action counts `[6] + [10]*66` |
| Which rows moved | **exactly 44**, **all at row position 7** (row 8 / Circle VIII), each transform an exact unwrap of an attachment-free token into its own `string`; **zero** other action changed anywhere in the 4346-action artifact |
| New bare rows vs donor | 8 distinct texts: the 6 exit names + `MIRROR_SUCCESSES[7]` / `MIRROR_LAPSES[7]` at 22 sites each — bare `<string>`, exactly what Donors 4/4.1 write for a literal row; **0** bare rows contain a stray `U+FFFC` |
| Inverse mis-bucketing | `_list_row()` probed across 10 input kinds: attachment-bearing → wrapper, attachment-free → bare, and `int`/`None`/`list`/pre-wrapped/`WFTextTokenAttachment` all `SystemExit`. No legitimate attachment-bearing row can reach the bare branch |
| MANIFEST | all six rows match disk byte-for-byte (`c627069…`/`709f53f…` sources, `b07497ba…`/`212598cf…` signed, both new dated archives byte-identical to their sources) |
| Rebuild | byte-idempotent in a clean scratch tree; reproduces both shipped digests |
| Gate A | `Validation passed.` exit 0, both forks |
| Gate B | exit 1, **exactly one** `WFCreateNoteInput` waiver line each, nothing else |
| Checkers | 12/12 exit 0 |
| Arming | AST-verified: both guards imported **and** invoked in `build_sentient.py` (calls :365, :384) and both precede its writes (:406/:408); `verify_list_item_wrappers` at `build_state_engine.py:4448` precedes the single write at `:4472` |

**Guard sensitivity — probed, not assumed.** Baseline passes on the shipped artifact (non-vacuous),
and every mutation fires with a diagnostic message:

- `verify_list_item_wrappers`: dropped row → census raise (`615`); flattened wrapped row → census
  raise (`615/51`); missing `WFItemType` / missing `WFValue` / `WFValue` a plain string /
  double-wrapped / `int` row / no `WFItems` key / **wrapped-but-attachment-free (the CR-01 inverse)**
  / a legitimate literal re-wrapped → per-row raise; extra List action → census raise (`68`).
- `verify_conditional_action_string`: flattened variable target → census raise (`found 19`); a new
  variable-bearing target → census raise (`found 21`); `Value` a plain string and `Value.string` an
  `int` → **`SystemExit`, not `AttributeError`/`TypeError`**.

**On item 4 — the fixer is right and I was wrong.** My suggested WR-04 patch
(`"￼" not in (token_value.get("string") or "")`) still raises `TypeError` when `string` holds an
`int`, because `or ""` never fires on a truthy non-string; I reproduced it. The applied
`isinstance`-first form fails closed on both malformed shapes and reports them as `unpinned`
rather than dying.

**On item 5 — CR-02's disposition is honest, not an evasion.** I explicitly offered option (b).
BD-08's confirmation is retracted verbatim in place, the slot is marked `UNVERIFIED` on both axes
with the measured evidence (90/97 `<integer>` sites vs the donor's `<string>`, 32 dict-valued
sites over eleven named variables), and a new open assumption **A5** in `BUILD-NOTES.md` §28
carries a medium risk rating and names the cheapest device witnesses. The stated reason holds:
changing 90/97 live comparison operands on a build no device can run would settle nothing and
would close at best half the finding.

**On item 8 — the fixer is right that I missed a fourth site.** My WR-06 grep pattern did not
include the literal `eighth class`, so `build_sentient.py:396` escaped it. The sweep is now
complete: all four sites carry renumbering notes and no stale "seven parameter-defect axes" or
"eighth axis" claim survives anywhere in `tools/`, `docs/` or `.claude/CLAUDE.md`.

**What remains** is a single, narrow class: **two documents still describe the guard and the
row-wrapping rule as they were *before* CR-01 and WR-01**. One of them is `.claude/CLAUDE.md`
axis 8, which is the file a future agent loads by default, and the stale sentence there is the
exact instruction that produced CR-01.

## Warnings

### WR-01: `.claude/CLAUDE.md` axis 8 still carries the refuted discriminator rule

**File:** `.claude/CLAUDE.md:435-437`

**Issue:** The fixer updated axis 8's **provenance preamble** (WR-05) and the axis **numbering**
(WR-06), but not axis 8's body. It still reads:

> Build guard: `verify_list_item_wrappers()` in `tools/build_state_engine.py`, armed on both
> forks, **asserting only that the `WFItemType` key is present** and never which value it holds.
> **Wrap only rows that are already dicts** — sweeping every row corrupts the legitimate
> bare-string literals.

Both halves are now wrong, and the second is the more serious:

1. "asserting only that the `WFItemType` key is present" — the guard now asserts the whole
   two-kind contract per row (bare-string kind, wrapper kind, `WFValue` must be a
   `WFTextTokenString`, and the **inverse** rule that a wrapped row must be attachment-bearing)
   **plus** the census `67 / 616 / 50`. A reader taking axis 8 at its word would think the CR-01
   inverse assertion and the census pin do not exist, and could "simplify" the guard back to the
   one-line test.
2. "**Wrap only rows that are already dicts**" — this is precisely the rule CR-01 refuted. It is
   the `isinstance(item, str)` discriminator restated as an instruction, and following it
   re-creates the 44 attachment-free wrappers verbatim. The corrected rule, already stated
   correctly in `BD-08`, `MANIFEST.md` and the `_list_row()` docstring, is **wrap only rows that
   are attachment-bearing**.

This is the last site in the repository where the refuted rule survives — I swept `tools/`,
`docs/` and `MANIFEST.md`, and every other occurrence of `isinstance(item, str)` / "Python type"
is explicitly framed as the corrected-in-place history.

**Fix:** replace the two sentences with the post-CR-01 rule and the real guard scope, e.g.:

```markdown
   Wrap only rows that are ATTACHMENT-BEARING — the discriminator is the token's content, not
   its Python type. A `WFTextTokenString` with an EMPTY `attachmentsByRange` is a literal row
   and goes out bare; wrapping it shipped 44 rows per fork in a shape no donor exhibits
   (phase 13 code review, CR-01). Build guard: `verify_list_item_wrappers()`, armed on both
   forks, asserting the whole two-kind contract per row — including the inverse rule that a
   wrapped row's `WFValue.Value.attachmentsByRange` must be non-empty — plus the measured
   census (67 List actions / 616 wrapped / 50 bare). Only `WFItemType`'s VALUE stays
   unasserted, because no donor exercises a non-text row.
```

---

### WR-02: `BUILD-NOTES.md` §28's guard table still describes the pre-fix guard, with stale coordinates

**File:** `docs/BUILD-NOTES.md:2490`

**Issue:** §28's prose, tables and assumptions were thoroughly rewritten (three-stage census
table, the "660 was not variable-bearing" correction, A3 restated, A5 added) — but the
**"The two guards" table row** was not, and it is the section's canonical "what does this guard
assert" reference:

> `verify_list_item_wrappers()` | … | **No `WFItems` row is a dict lacking a `WFItemType` key —
> the key's presence only, never its value** | … strictly above the single `SOURCE.write_bytes()`
> **(AST: call line 4248 < write line 4272)** | both forks

Two defects in one row:

1. The *Asserts* column describes only the pre-WR-01 test. The same table's neighbouring row for
   `verify_conditional_action_string()` was likewise not updated for the third raise
   (`EXPECTED_VARIABLE_TARGETS`), so §28 now under-reports both guards while §28's own body
   over-explains them.
2. The line numbers are stale by 200. Measured at HEAD by AST: the call is
   `tools/build_state_engine.py:4448` and the write is `:4472`. The **ordering** claim is true and
   I re-verified it; the coordinates are not. `.claude/CLAUDE.md` §1 already states the rule this
   breaks — "Anchor on the symbol, not the line."

**Fix:** restate the *Asserts* cells to match the shipped guards (whole two-kind contract + inverse
rule + census `67/616/50`; and for the conditional guard: bare-placeholder + Donor-5 envelope +
census `20`), and replace the parenthetical with a symbol-anchored claim:
"`verify_list_item_wrappers()` precedes the single `SOURCE.write_bytes()` in `main()` (AST-verified,
no line numbers cited)."

## Info

### IN-01: the census constants cannot express a per-fork divergence

**File:** `tools/build_state_engine.py:2625-2627` (`EXPECTED_LIST_ACTIONS` / `EXPECTED_WRAPPED_ROWS` / `EXPECTED_BARE_ROWS`), `:2496` (`EXPECTED_VARIABLE_TARGETS`)

**Issue:** All four constants are single module-level values shared by both builders, and today
that is correct — I measured `67/616/50` and `20` identically on Core and Aware, because Aware
forks the built Core source. But Sentient *does* insert its own actions (`audit_block()`), and the
day a Sentient-only List action or variable-bearing conditional is added, the pin fails on Aware
and the only available repair — editing the shared constant — immediately breaks Core. The failure
message is clear about *what* moved but offers no per-fork expression.

**Fix:** when that day comes, take the constants as a `(core, aware)` pair or pass an expected
census into the guard from each builder. No change needed now; recorded so the brittleness is a
known cost of a deliberately brittle pin rather than a surprise.

---

### IN-02: `build_sentient.py`'s atomic write still leaves the generated source mode `0600`

**File:** `tools/build_sentient.py:405-409`

**Issue:** Carried unfixed from iteration 1 (correctly out of the fixer's scope). `NamedTemporaryFile`
creates at `0600` and `os.replace` preserves it, so a freshly generated `src/PROSOCHE-Sentient.xml`
is `-rw-------` while `build_state_engine.py`'s `write_bytes()` respects umask. Re-confirmed in this
iteration's scratch rebuild. Git does not track the bit, so committed artifacts are unaffected.

**Fix:** `os.chmod()` the temp file before `os.replace`, or use the sibling's write path.

---

### IN-03: the provenance ancestor check is documented but still not enforced by either generator

**File:** `tools/build_state_engine.py:4391` (`main`), `tools/build_sentient.py:257` (`main`)

**Issue:** Carried unfixed from iteration 1. `.claude/CLAUDE.md` requires
`git merge-base --is-ancestor 7ca8ebb… HEAD` to pass before either generator runs and to abort the
rebuild if it fails. Neither `main()` checks it: I ran both generators to completion this iteration
in a scratch directory that is **not a git repository**, and both produced the shipped digests
without complaint. The rule holds only by operator discipline — which was in fact exercised
(`13-04` and the CR-01 re-sign both record exit 0).

**Fix:** make it the first statement of each `main()` and `raise SystemExit` on a non-zero return.

## Deferred by decision (not counted above)

### CR-03 (iteration 1): `mirror_templates()` binds facts by placeholder ordinal

**Status:** deliberately deferred, **not** fixed. Todo:
`.planning/todos/pending/2026-08-17-mirror-templates-ordinal-fact-binding.md`.

I verified the deferral loses nothing:

- The todo is **genuinely cold-runnable**. I ran its embedded reproduce script from a clean shell
  with no reference to any plan or review: it prints exactly nine lines, matching my original
  table row-for-row. Its file/line references resolve (`mirror_templates()` is at
  `tools/build_state_engine.py:733`).
- It carries the full finding — mechanism, the nine-row table with *should bind*, the CIRC-07
  framing, and the "worse than showing nothing: the number is real, so nothing looks broken"
  statement.
- It **adds** something I did not raise: row-10 reachability (each family holds ten templates,
  `CIRCLE_NAMES` holds nine, and `Item At Index` behaviour at `Circle Next = 0`, the silent band,
  is unmeasured), correctly recorded as an open sub-question that decides whether the count is
  nine or eight.
- Its completion criteria carry the full ship chain (provenance check, gate A, re-sign, all six
  MANIFEST rows, 12/12 checkers, `SystemExit` guard armed at both Sentient touch points and
  AST-proven, sensitivity demonstrated against a mutation).
- The fixer's correction of my suggested fix is **accurate and measured**: the word *immediately*
  preceding each placeholder is `is` or `now` in all nine cases, never the fact's name. The todo
  records two workable shapes instead (carry the fact explicitly, or resolve by scanning the whole
  preceding literal *with* a build-time assertion) — the second is what my own verification script
  used.

The three deferral grounds are sound: the defect is pre-existing, it is a fact-binding class that
neither of this phase's two families touches, and fixing it invalidates 616 row serializations plus
both signed artifacts and all six MANIFEST rows — a full re-sign cycle for a defect unrelated to the
phase hypothesis. It remains a real, user-visible correctness defect and should not be lost.

---

_Reviewed: 2026-08-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard · iteration 2_
