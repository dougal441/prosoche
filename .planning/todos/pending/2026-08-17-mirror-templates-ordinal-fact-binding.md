---
created: 2026-08-17T22:30:00.000Z
title: mirror_templates() binds facts by placeholder ordinal — 9 Mirror templates announce the wrong number
area: general
severity: major
files:
  - tools/build_state_engine.py:733
  - tools/build_state_engine.py:80
  - tools/build_state_engine.py:92
---

## Problem

`mirror_templates()` decides **which fact each `￼` placeholder binds to** from the
placeholder's **position in the sentence**, not from what the sentence says. Nine of the thirty
Mirror templates therefore announce one quantity and display another. At Circle IV on a success
path the user reads **"Recorded pressure is 4"** when `4` is the *Circle*, not the pressure.

CIRC-07 requires "a precise behavioural reflection built only from recorded facts". This states
a recorded fact under the **wrong label**, which is worse than showing nothing: the number is
real, so nothing looks broken.

### The mechanism

`tools/build_state_engine.py`, `mirror_templates()`:

```python
def mirror_templates(templates):
    facts = ("Circle Next", "Pressure Next", "Heat Final")
    return tuple(text_token([(part, facts[index] if index < len(template.split("￼")) - 1 else None)
                             for index, part in enumerate(template.split("￼"))]) for template in templates)
```

`index` is the ordinal of the placeholder within the template. The ten `MIRROR_BASELINES`
templates each carry **three** placeholders in the order Circle, pressure, heat, so
`facts[0..2]` line up and the baseline family is **correct**. Every `MIRROR_SUCCESSES` and
`MIRROR_LAPSES` template carries **one** placeholder (or none), so `index` is always `0` and
the binding is always `facts[0]` = **`Circle Next`** — whatever the prose names.

### The nine affected templates

Measured by walking each built token's `attachmentsByRange` against the literal text preceding
each offset. Row numbers are 1-based, and `mirror_text()` selects with `Item At Index` on
`Circle Next`, so **row N is the template shown at Circle N**.

| Family | Row (Circle) | Rendered text | Bound variable | Should bind |
|---|---|---|---|---|
| SUCCESS | 4 | "The previous contract was kept. Recorded pressure is ￼." | `Circle Next` | `Pressure Next` |
| SUCCESS | 5 | "A kept boundary is part of this record; heat is ￼." | `Circle Next` | `Heat Final` |
| SUCCESS | 7 | "One prior boundary was kept; this run's pressure is ￼." | `Circle Next` | `Pressure Next` |
| SUCCESS | 9 | "The last contract was kept; the current heat is ￼." | `Circle Next` | `Heat Final` |
| LAPSE | 2 | "The record shows a prior overrun; current pressure is ￼." | `Circle Next` | `Pressure Next` |
| LAPSE | 3 | "One earlier boundary exceeded its time; heat is now ￼." | `Circle Next` | `Heat Final` |
| LAPSE | 5 | "The previous boundary was exceeded; pressure is ￼." | `Circle Next` | `Pressure Next` |
| LAPSE | 7 | "A prior contract exceeded its boundary; heat is ￼." | `Circle Next` | `Heat Final` |
| LAPSE | 10 | "A time boundary ran over earlier; pressure is now ￼." | `Circle Next` | `Pressure Next` |

The remaining SUCCESS/LAPSE templates are unaffected because they genuinely name the Circle, or
(SUCCESS row 8, LAPSE row 8) carry no placeholder at all.

**All ten `MIRROR_BASELINES` templates are correct** and must not be disturbed by any fix.

### Reproduce it cold

From a clean checkout, with no reference to any review or plan:

```bash
cd <repo root>
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from build_state_engine import MIRROR_BASELINES, MIRROR_SUCCESSES, MIRROR_LAPSES, mirror_templates
FACT_WORD = {"Circle Next": "circle", "Pressure Next": "pressure", "Heat Final": "heat"}
for name, family in (("BASELINE", MIRROR_BASELINES), ("SUCCESS", MIRROR_SUCCESSES), ("LAPSE", MIRROR_LAPSES)):
    for row, (template, token) in enumerate(zip(family, mirror_templates(family)), start=1):
        attachments = token["Value"]["attachmentsByRange"]
        text = token["Value"]["string"]
        for key, attachment in attachments.items():
            offset = int(key.strip("{} ").split(",")[0])
            # the fact the SENTENCE names, anywhere in the clause before the placeholder
            named = [w for w in FACT_WORD.values() if w in text[:offset].lower()]
            if named and FACT_WORD[attachment["VariableName"]] not in named[-1:]:
                print(f"{name} row {row}: says {named[-1]!r}, binds {attachment['VariableName']!r}")
                print(f"    {template}")
PY
```

Nine lines, all binding `Circle Next`.

## Why this was deferred out of Phase 13 rather than fixed

Recorded so the deferral is a decision rather than an omission.

1. **It is pre-existing.** `mirror_templates()` predates Phase 13 and was not touched by it.
   Phase 13 changed `_list_row()` (row framing) and `verify_conditional_action_string()`
   (conditional operand shape); this defect is in neither family.
2. **It is a different defect class.** Phase 13 scoped exactly two families — the `WFItems` row
   framing and the conditional operand envelope. This is a **fact-binding** defect: the token
   envelope is perfectly well-formed, every `attachmentsByRange` offset is valid, and every
   existing build guard passes. Nothing in the phase's guard set is even shaped to see it.
3. **Fixing it needs its own Mirror-wide re-verification.** Any fix touches all thirty
   templates in three families across 22 call sites and 66 built List actions, changes 616 row
   serializations, and invalidates the signed artifacts and all six `MANIFEST.md` rows again.
   That is a re-sign cycle plus a fresh decrypt-verification — the same chain Phase 13 already
   ran twice — for a defect with no relationship to the phase's hypothesis.

Recorded at review time as **CR-03**, outcome `skipped`, in
`.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-REVIEW-FIX.md`.

## What a fix has to do

The review's first suggestion — "map on the word **immediately preceding** each placeholder" —
**does not work as stated**, and that is measured, not assumed: the word immediately before the
placeholder is `is` or `now` in all nine cases, never the fact's name. The label sits earlier in
the clause. Two workable shapes:

- **Carry the fact explicitly.** Replace each bare template string with a `(template, facts)`
  pair, so `MIRROR_SUCCESSES[3]` becomes
  `("The previous contract was kept. Recorded pressure is ￼.", ("Pressure Next",))`. Verbose,
  but the binding stops being derivable and therefore stops being derivable *wrongly*. The
  baseline family keeps `("Circle Next", "Pressure Next", "Heat Final")` unchanged.
- **Resolve by label with a build-time assertion.** Keep a
  `FACT_BY_LABEL = {"circle": "Circle Next", "pressure": "Pressure Next", "heat": "Heat Final"}`
  and search the whole literal preceding each placeholder (last match wins), then **assert at
  build time that every placeholder resolved to exactly one label found in its own preceding
  literal**. Without that assertion this is the same class of derivation that produced the bug.

Either way, add a build guard so a future template edit cannot silently re-introduce the
mismatch, raising `SystemExit` (never a bare `assert`) before any file write, armed in
`tools/build_sentient.py` at **both** touch points — the `from build_state_engine import (...)`
list **and** the guard invocation block — and prove the arming by AST, not by `grep -c verify_`.

## Open sub-question, not a claim

`mirror_text()` selects with `Item At Index` on `Circle Next`, which is 1-based, and each family
holds **ten** templates while `CIRCLE_NAMES` holds **nine** circles. Whether row 10 is reachable
at all (and what `Item At Index` does when `Circle Next` is `0`, the silent band) was **not**
measured here. `LAPSE` row 10 is in the table above on the assumption that it is reachable; if
it is not, the affected count is eight, not nine. Settle this before writing the fix — it also
decides whether the tenth template is dead weight in all three families.

## Completion criteria

- [ ] All nine templates bind the fact their prose names; all ten baselines unchanged.
- [ ] Row 10 reachability settled and recorded either way.
- [ ] A build guard makes the mismatch unrepresentable, armed on **both** forks (AST-proven),
      with its sensitivity demonstrated against a synthetic mutation rather than asserted.
- [ ] Provenance ancestor check exits 0; both generators re-run; **gate A**
      (`--target-macos 26 --target-platform all`) prints `Validation passed.` on both forks.
- [ ] Both forks re-archived and re-signed under the canonical basenames
      `PROSOCHĒ — Nine Circles — Core.shortcut` / `— Aware.shortcut`, no suffix; all six
      `artifacts/shortcuts/MANIFEST.md` rows recomputed from disk in one pass.
- [ ] All twelve `docs/*.py` checkers exit 0, none silenced and no assertion weakened.
- [ ] `docs/BUILD-NOTES.md` records the measured before/after, per the recording duty.
