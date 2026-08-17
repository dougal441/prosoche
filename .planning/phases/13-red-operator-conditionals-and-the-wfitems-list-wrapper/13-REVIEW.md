---
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
reviewed: 2026-08-17T00:00:00Z
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
  critical: 3
  warning: 7
  info: 3
  total: 13
status: issues_found
---

# Phase 13: Code Review Report

**Reviewed:** 2026-08-17
**Depth:** standard
**Files Reviewed:** 8
**Status:** issues_found

## Summary

The phase's mechanical claims hold up under independent measurement. I re-decrypted Donors 4,
4.1 and 5 and both shipped signed containers, rebuilt both forks from the two generators in a
clean scratch tree, and re-ran all twelve `docs/*.py` checkers:

- The rebuild is **byte-idempotent** and reproduces the exact shipped digests
  (`99388cad…` Core, `d01154b3…` Aware).
- All six `MANIFEST.md` hash/size rows verify against disk.
- Decrypted signed payloads carry 67 List actions / 660 wrapped rows / 6 bare rows / 0 dict
  rows missing `WFItemType`, per fork — exactly as documented.
- The conditional inventory (192/195 slots, 20/20 variable-bearing, 19×code 4 + 1×code 99,
  172/175 literals) reproduces exactly.
- `verify_list_item_wrappers` is armed at **both** required touch points in
  `tools/build_sentient.py` (import list :23, invocation :368) and raises before every write in
  both builders.
- All twelve `docs/*.py` checkers exit 0.

What the phase did **not** establish is the part that matters. The row-wrapper fix discriminates
on **Python type** (`isinstance(item, str)`), not on whether the row actually bears an
attachment — so 44 of the 660 "wrapped" rows are pure literals with an empty
`attachmentsByRange`, shipped in a wrapper shape that **no donor exhibits** and that the phase's
own axis-8 rule explicitly says a literal must not carry. Separately, `BD-08`'s bonus finding
records a *confirmation* that its own cited donor refutes: `if_block()` emits `WFNumberValue` as
a plist `<integer>` at 90/97 sites where Donor 4.1 writes a `<string>`, and at 32 further sites
emits a variable attachment dict that no donor covers at all. Both new guards are also narrower
than the comments beside them claim: neither can see a **dropped** or **flattened** row/operand,
which is precisely the fork-regression scenario the per-fork arming comments say they catch.

One pre-existing, user-visible correctness bug is also reported: `mirror_templates()` binds
facts by placeholder ordinal, so nine Mirror templates announce "pressure is X" or "heat is X"
while displaying the **Circle** number.

## Critical Issues

### CR-01: `_list_row()` wraps 44 pure-literal rows in the variable-row wrapper — an unevidenced shape, shipped

**File:** `tools/build_state_engine.py:682` (and its call site `:688-689`)

**Issue:** The discriminator is `isinstance(item, str)`. Everything that is not a Python `str`
gets the wrapper — including a `WFTextTokenString` built by `text_token()` from a template that
contains **no** `￼` placeholder and therefore has an **empty** `attachmentsByRange`. That is a
literal row by content, encoded as a variable row.

The function's own docstring states the opposite rule it implements:

> THE TWO-KIND RULE. … a LITERAL row is a bare string, and an ATTACHMENT-BEARING row is the
> wrapper dict

`.claude/CLAUDE.md` axis 8 ("A **literal** row is emitted as a bare string directly in the
`WFItems` array … It takes **no** wrapper") and `docs/CAPABILITY-DECISIONS.md` BD-08 say the same.

Measured, both in `src/*.xml` and in the **decrypted payload of both shipped signed
containers**: 660 wrapped rows per fork, of which **44 carry an empty `attachmentsByRange`**.
Donor ground truth (I re-decrypted `.planning/debug/Donor 4.shortcut` and `Donor 4.1.shortcut`)
shows literal rows written as bare `<string>` elements — `"Circle"`, `"follows"` — never as
`{WFItemType, WFValue}`.

Two things make this more than cosmetic:

1. This is exactly the class the project's do-not-fabricate rule forbids. The whole phase exists
   because an unevidenced row framing renders blank on device. Shipping a *second* unevidenced
   row framing at 44 sites re-opens the same risk from the other direction, and no guard,
   validator gate or decrypt can see it.
2. The affected rows are not randomly placed. `mirror_text()` selects with `Item At Index` on
   `Circle Next` (1-based), and the two attachment-free templates are
   `MIRROR_SUCCESSES[7]` / `MIRROR_LAPSES[7]` — **row 8**. So the shape no donor supports is the
   one selected at **Circle VIII** on both the success and the lapse family. If iOS mishandles
   it, the observed symptom is a blank Mirror at a high circle, which is indistinguishable from
   the defect this phase claims to have fixed.

`docs/BUILD-NOTES.md` §28 assumption **A3** notices the adjacent fact ("an all-wrapped array is a
configuration no donor exhibits") but frames it as a *mix* question and rates it low risk. It
does not record that 44 rows are literal-by-content, so the reader is not told that the shipped
encoding contradicts axis 8's stated rule.

**Fix:** discriminate on attachment-bearing-ness, not on Python type, and emit a bare string for
an attachment-free token — the exact shape both donors show:

```python
def _list_row(item):
    if isinstance(item, str):
        return item
    body = item.get("Value", {}) if isinstance(item, dict) else {}
    # An attachment-free token is a LITERAL row: donors write those as bare <string>.
    if isinstance(body, dict) and isinstance(body.get("string"), str) and not body.get("attachmentsByRange"):
        return body["string"]
    return {"WFItemType": 0, "WFValue": item}
```

Then extend `verify_list_item_wrappers()` with the inverse assertion (a wrapped row's
`WFValue.Value.attachmentsByRange` must be non-empty), re-archive and re-sign, and correct the
"660 variable-bearing rows" wording in `MANIFEST.md`, `BUILD-NOTES.md` §28 and BD-08.

---

### CR-02: BD-08's numeric-slot "confirmation" is refuted by the donor it cites

**File:** `docs/CAPABILITY-DECISIONS.md` — BD-08, "Bonus finding — Donor 4.1 settles the numeric-conditional right-hand slot"; behaviour lives in `tools/build_state_engine.py:309-330` (`if_block`)

**Issue:** BD-08 closes with:

> `if_block()` already implements all three cases correctly via its optional `number=` /
> `string=` keywords — recorded here as **confirmation, not a change request**.

Measurement contradicts it on two counts:

1. **Serialization type.** BD-08 itself records that Donor 4.1 writes `WFNumberValue` as a
   `<string>` (`"10"`), "not an `<integer>`". `if_block()` assigns the raw Python value, so
   `plistlib` emits `<integer>`. Measured in the shipped sources: **90 (Core) / 97 (Aware)**
   `WFNumberValue` parameters are `int`. The generator therefore diverges from the donor on the
   exact axis BD-08 says it confirms. (Re-verified against my own decrypt of Donor 4.1:
   `'WFNumberValue': ('str', '10')`.)
2. **A fourth, unevidenced case.** **32** conditionals per fork hold a *dict* in `WFNumberValue`
   — a bare `WFTextTokenAttachment` variable reference, e.g. `Now Epoch`, `Heat Floor`,
   `Overrun Minimum`, from call sites such as `:1184`, `:1235`, `:1293`. No donor covers a
   variable in `WFNumberValue`, and BD-08's "three cases" framing does not mention it, so the
   record silently implies coverage it does not have. Given this project's history with unfilled
   or non-literal comparison slots ("Please choose a value for each parameter in this action"),
   this is the highest-value unaudited operand shape currently shipping.

Recording a false confirmation is worse than recording nothing: `docs/CAPABILITY-DECISIONS.md`
is a decision record future agents treat as settled, and the evidence hierarchy makes a donor
claim authoritative.

**Fix:** replace the "confirmation, not a change request" paragraph with the measured divergence
— `<integer>` vs donor `<string>` at 90/97 sites, plus 32 dict-valued sites — and mark the
numeric right-hand slot **UNVERIFIED for both the integer encoding and the variable case**.
Either (a) emit the donor's string form:

```python
if number is not None:
    params["WFNumberValue"] = str(number) if isinstance(number, (int, float)) else number
```

and re-measure, or (b) leave the artifact untouched and record the divergence as an open
assumption owned by device UAT. Do not leave it recorded as confirmed.

---

### CR-03: `mirror_templates()` binds facts by placeholder ordinal — 9 Mirror templates display the wrong number

**File:** `tools/build_state_engine.py:697-700` (constants at `:80-103`)

**Issue:** (Pre-existing, not introduced this phase, but it is user-visible incorrect behaviour
in a reviewed file and it lives in the code this phase touched.)

```python
facts = ("Circle Next", "Pressure Next", "Heat Final")
... facts[index] if index < len(template.split("￼")) - 1 else None
```

`index` is the **position of the placeholder in the template**, not the fact the prose names. A
three-placeholder baseline works. A **one**-placeholder template always binds `facts[0]` =
`Circle Next`, whatever the sentence says. Measured against the built artifact (action 1146 in
`src/PROSOCHE-Dumb.xml`), nine templates are affected:

| Family | Row (Circle) | Rendered text | Bound variable |
|---|---|---|---|
| SUCCESS | 4 | "…Recorded pressure is ￼." | `Circle Next` |
| SUCCESS | 5 | "…heat is ￼." | `Circle Next` |
| SUCCESS | 7 | "…this run's pressure is ￼." | `Circle Next` |
| SUCCESS | 9 | "…the current heat is ￼." | `Circle Next` |
| LAPSE | 2 | "…current pressure is ￼." | `Circle Next` |
| LAPSE | 3 | "…heat is now ￼." | `Circle Next` |
| LAPSE | 5 | "…pressure is ￼." | `Circle Next` |
| LAPSE | 7 | "…heat is ￼." | `Circle Next` |
| LAPSE | 10 | "…pressure is now ￼." | `Circle Next` |

At Circle IV on a success path the user is told "Recorded pressure is 4" when 4 is the Circle.
CIRC-07 requires "a precise behavioural reflection built only from recorded facts"; this states
a recorded fact under the wrong label, and it is invisible to every existing guard because the
token envelope is perfectly well-formed.

**Fix:** name the fact per template rather than deriving it from ordinal position — e.g. carry
`(template, facts_tuple)` pairs, or map on the word preceding each placeholder:

```python
FACT_BY_LABEL = {"circle": "Circle Next", "pressure": "Pressure Next", "heat": "Heat Final"}
```

and assert at build time that every placeholder resolved to a label found in its own preceding
literal, so a future template edit cannot silently re-introduce the mismatch.

## Warnings

### WR-01: `verify_list_item_wrappers()` cannot detect most of what its arming comment claims

**File:** `tools/build_state_engine.py:2565-2582`; claim at `tools/build_sentient.py:359-368`

**Issue:** The Sentient arming comment says "a fork that **dropped**, re-serialized or unwrapped
a row would ship a BLANK Mirror … Asserted per fork". The guard only tests
`isinstance(row, dict) and "WFItemType" not in row`. I probed it directly against the shipped
module; every one of these **passes silently**:

| Mutation | Guard result |
|---|---|
| all rows dropped (`WFItems: []`) | PASSED |
| a wrapped row flattened to a bare string | PASSED |
| `{"WFItemType": 0}` with `WFValue` **missing** | PASSED |
| `{"WFItemType": 0, "WFValue": "oops"}` | PASSED |
| List action with **no** `WFItems` key at all | PASSED |
| a row that is an `int` | PASSED |
| a **double-wrapped** row | PASSED |

So the guard covers exactly one regression direction (raw dict row) and none of the drop /
flatten / malformed-payload directions the comment advertises.

**Fix:** assert the whole row-shape contract, and pin the counts the phase measured:

```python
if isinstance(row, str):
    continue
if not isinstance(row, dict) or "WFItemType" not in row or not isinstance(row.get("WFValue"), dict):
    offenders.append((index, position))
    continue
body = row["WFValue"].get("Value", {})
if row["WFValue"].get("WFSerializationType") != "WFTextTokenString" or not body.get("attachmentsByRange"):
    offenders.append((index, position))
```

plus a total-count assertion (`660 wrapped + 6 bare` for Core after CR-01 is fixed) so a dropped
row cannot pass. Then correct the arming comment to describe real coverage.

---

### WR-02: the Donor-5 "pin" cannot see a flattened operand — the failure its comment names

**File:** `tools/build_state_engine.py:2519-2524`; claim at `tools/build_sentient.py:340-354`

**Issue:** The pin only runs `if isinstance(value, dict)`. The arming comment says it protects
against "a fork that **flattened** or re-enveloped one of those operands". Flattening produces a
plain `str`, which the pin skips entirely — and the guard has no notion of *which* 20 sites are
supposed to be variable-bearing, so a flattened site is indistinguishable from one of the 172
legitimate literals. Probed: a variable-bearing target replaced with the literal `"Circle Next"`
**passes**.

**Fix:** pin the census, not just the shape — the phase already measured it:

```python
EXPECTED_VARIABLE_TARGETS = 20  # Donor 5 family; see BD-07
...
if len(variable_bearing) != EXPECTED_VARIABLE_TARGETS:
    raise SystemExit(f"variable-bearing comparison targets: expected "
                     f"{EXPECTED_VARIABLE_TARGETS}, found {len(variable_bearing)} -- a target "
                     "was flattened to a literal or a new one appeared unreviewed")
```

Otherwise narrow the comment to "re-enveloped" and drop the flatten claim.

---

### WR-03: `_list_row()` is neither total nor idempotent

**File:** `tools/build_state_engine.py:682`

**Issue:** `item if isinstance(item, str) else {...}` accepts anything. Probed:

- `_list_row(5)` → `{"WFItemType": 0, "WFValue": 5}` — a fabricated row shape for a value type
  the docstring explicitly says is unaudited, emitted with **no** error.
- `_list_row(already_wrapped)` → `{"WFItemType": 0, "WFValue": {"WFItemType": 0, …}}` — silent
  double-wrap, which WR-01 shows the guard also cannot see. That combination is exactly the
  "sweeping every row corrupts the legitimate rows" hazard `.claude/CLAUDE.md` axis 8 warns
  about, with nothing standing between it and a signed artifact.

**Fix:** make the contract explicit at the emitter:

```python
if isinstance(item, str):
    return item
if not (isinstance(item, dict) and item.get("WFSerializationType") == "WFTextTokenString"):
    raise SystemExit(f"mirror_text() row is neither a literal str nor a WFTextTokenString: {item!r}")
```

---

### WR-04: the pin raises `AttributeError`, not `SystemExit`, on a malformed target

**File:** `tools/build_state_engine.py:2520-2523`

**Issue:** `token_value = value.get("Value", {})` then `token_value.get("string", "")`. If a
future change makes `Value` a plain string (a plausible flatten-in-place regression), the guard
dies with `AttributeError: 'str' object has no attribute 'get'` instead of the project-mandated
`SystemExit` with a diagnostic message. Reproduced. The same shape would `TypeError` if `string`
held a non-string. Failure still precedes the write, so nothing corrupt ships — but the operator
gets a traceback naming the guard rather than the offending action index.

**Fix:**

```python
token_value = value.get("Value")
if (value.get("WFSerializationType") != "WFTextTokenString"
        or not isinstance(token_value, dict)
        or "￼" not in (token_value.get("string") or "")
        or not token_value.get("attachmentsByRange")):
    unpinned.append(index)
```

---

### WR-05: `.claude/CLAUDE.md`'s axis preamble now asserts device provenance that axis 8 does not have

**File:** `.claude/CLAUDE.md:353-358`

**Issue:** The heading became "the **nine** parameter-defect axes" but the preamble underneath is
unchanged:

> Every rule below was established by on-device failure during the 2026-08-13/14 OPEN-path debug
> session and is asserted by a build guard…

Axis 8 (`WFItems` wrapper) was established by a **donor decrypt on 2026-08-17** and is recorded
everywhere else in this same commit as "**Structurally proven, device-unobserved**"
(`MANIFEST.md`, `BUILD-NOTES.md` §28). Axis 9 came from cycle 15, not that session. The preamble
therefore promotes a file-level inference to on-device evidence in the one document future
agents read as authority — the precise inversion the evidence hierarchy exists to prevent.

**Fix:** rewrite the preamble to attribute provenance per axis, e.g. "Axes 1–7 were established
by on-device failure during the 2026-08-13/14 OPEN-path debug session; axis 9 by device error at
cycle 15; **axis 8 by device-authored donor decrypt (Donors 4/4.1) and is not yet device-observed
in this artifact**."

---

### WR-06: axis numbering now conflicts between the docs and the code

**File:** `tools/build_state_engine.py:1714`, `tools/build_state_engine.py:3493`, `docs/CAPABILITY-DECISIONS.md:413`

**Issue:** `.claude/CLAUDE.md` renumbered to nine axes (8 = `WFItems` wrapper, 9 = compound
value), but the code and BD-06 still say:

- `:1714` — "BD-06 Decision 5 -- the **EIGHTH** defect class, alongside the **seven**
  parameter-defect axes"
- `:3493` — "CYCLE 15 -- the **eighth axis**, STRUCTURED VALUE (compound state fields)"
- `docs/CAPABILITY-DECISIONS.md:413` — "eighth class alongside the **seven** parameter-defect axes"

Three different things are now called "the eighth". A future debugger grepping "axis 8" lands on
the wrong defect class. `tools/build_sentient.py:369` ("Cycle 12, axis 7") is still correct, which
makes the drift harder to spot, not easier.

**Fix:** update the three stale strings in the same pass that renumbered `.claude/CLAUDE.md`;
compound becomes "axis 9", BD-06's dispatch class becomes "the tenth defect class, alongside the
nine parameter-defect axes".

---

### WR-07: the 660-row figure is described as "variable-bearing" in three documents

**File:** `docs/BUILD-NOTES.md` §28 ("Unwrapped **variable-bearing** rows | 660 → 0"); `artifacts/shortcuts/MANIFEST.md` ("Every **non-literal** List row is now framed"); `docs/CAPABILITY-DECISIONS.md` BD-08 ("660 unwrapped **variable-bearing** rows")

**Issue:** 44 of the 660 have an empty `attachmentsByRange` — they are literal rows (see CR-01).
The inventory tables are numerically right and semantically wrong, and the wording is what makes
CR-01 invisible to a reader auditing the record rather than the artifact.

**Fix:** restate as "660 rows wrapped (616 attachment-bearing, 44 attachment-free literals —
see CR-01)", or fix CR-01 first and restate as "616 wrapped + 50 bare".

## Info

### IN-01: `docs/BUILD-NOTES.md` §28 cites line numbers that no longer resolve

**File:** `docs/BUILD-NOTES.md` §28, guard-registration table

**Issue:** "(AST: call line 4248 < write line 4272)". At HEAD the call is
`tools/build_state_engine.py:4301` and the write is `:4325`. The *ordering* claim is true and I
re-verified it; the coordinates are stale by 24 lines. `.claude/CLAUDE.md` §1 already states the
rule this breaks: "Anchor on the symbol, not the line."

**Fix:** cite the symbols (`verify_list_item_wrappers()` precedes the single
`SOURCE.write_bytes()` in `main()`) and drop the line numbers.

---

### IN-02: `build_sentient.py`'s atomic write leaves the generated source mode `0600`

**File:** `tools/build_sentient.py:387-390`

**Issue:** `tempfile.NamedTemporaryFile` creates at `0600`; `os.replace` preserves it, so a fresh
`src/PROSOCHE-Sentient.xml` lands at `-rw-------` while `build_state_engine.py`'s
`SOURCE.write_bytes()` respects umask (`-rw-r--r--`). Confirmed in a clean scratch build. Git does
not track the bit, so the committed artifact is unaffected — this only bites a build consumed
directly from the working tree by another user or process. (Pre-existing.)

**Fix:** `os.chmod(temporary, 0o644 & ~current_umask)` before `os.replace`, or write through the
same `write_bytes` path the sibling generator uses.

---

### IN-03: the provenance ancestor check is documented but not enforced by either generator

**File:** `tools/build_state_engine.py:4244`, `tools/build_sentient.py:257`

**Issue:** `.claude/CLAUDE.md` requires `git merge-base --is-ancestor 7ca8ebb… HEAD` to pass
before either generator runs, and "abort the rebuild if it fails". Neither `main()` checks it. I
ran both generators to completion in a scratch directory that is **not a git repository at all**;
both produced the shipped digests without complaint. The rule currently depends entirely on the
operator remembering it. (Pre-existing; `13-04` did run it manually and recorded exit 0.)

**Fix:** add the check as the first statement of each `main()` —
`subprocess.run(["git","merge-base","--is-ancestor",ANCESTOR,"HEAD"])`, `raise SystemExit` on a
non-zero return — so it is a build gate rather than a convention.

---

_Reviewed: 2026-08-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
