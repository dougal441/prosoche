# Phase 9: Dimming/Silence Stateful Restore (Experimental Fork) - Pattern Map

**Mapped:** 2026-08-16
**Files analyzed:** 2 (1 modified generator file, 1 new UAT.md)
**Analogs found:** 2 / 2 (both analogs found in-repo; the generator analog is in the same
file being modified — this is a table-driven single-file change, not a multi-file feature)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `tools/build_state_engine.py` (edit: `NUMERIC_OPERAND_FIELDS` table + verify build passes) | config/utility (build-time plist generator, table-driven audit) | transform (static analysis + code-generation pass over an in-memory action list) | Same file — `"is.workflow.actions.math"` / `"is.workflow.actions.getitemfromlist"` entries in the same `NUMERIC_OPERAND_FIELDS` dict, lines 2362-2365 | exact (same table, same file, same mechanism — this is literally two new dict entries) |
| `.planning/phases/09-.../09-UAT.md` (new) | test (manual device-proving checklist, not automated) | request-response (human checkpoint Q&A loop via `/gsd-verify-work`) | `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md` | exact (same project-native UAT.md structure: frontmatter, Current Test, Context, Tests, Summary) |

## Pattern Assignments

### `tools/build_state_engine.py` — add two `NUMERIC_OPERAND_FIELDS` entries (config/utility, transform)

**Analog:** the file's own existing table, `tools/build_state_engine.py` lines 2362-2528.

**The table itself** (lines 2362-2365) — this is the entire mechanical surface of the fix:
```python
NUMERIC_OPERAND_FIELDS = {
    "is.workflow.actions.math": ("WFInput", "WFMathOperand"),
    "is.workflow.actions.getitemfromlist": ("WFItemIndex",),
}
```
Planner's exact target (per RESEARCH.md's own Code Examples section, confirmed against live
code): add
```python
    "is.workflow.actions.setbrightness": ("WFBrightness",),
    "is.workflow.actions.setvolume": ("WFVolume",),
```
No other code changes are needed — everything downstream reads this table generically.

**How the table is consumed — `_numeric_operand_sites()`** (lines 2368-2384):
```python
def _numeric_operand_sites(item):
    identifier = item.get("WFWorkflowActionIdentifier")
    parameters = item.get("WFWorkflowActionParameters", {})
    if identifier == "is.workflow.actions.conditional":
        if parameters.get("WFControlFlowMode") == 0 and parameters.get("WFCondition") in NUMERIC_CONDITION_CODES:
            yield "WFInput", parameters.get("WFInput")
        return
    if identifier == "is.workflow.actions.getitemfromlist" and parameters.get("WFItemSpecifier") != "Item At Index":
        return
    for field in NUMERIC_OPERAND_FIELDS.get(identifier, ()):
        if field in parameters:
            yield field, parameters[field]
```
`setbrightness`/`setvolume` are neither of the two special-cased identifiers, so they will
fall straight through to the generic `NUMERIC_OPERAND_FIELDS.get(identifier, ())` branch —
confirming RESEARCH.md's claim that no special-casing is needed for the new entries.

**Descriptor unwrap — `_operand_descriptor()`** (lines 2387-2404): unwraps either the
conditional-style `{"Type":"Variable","Variable":{"Value": desc}}` shape or the direct
`variable()`/`output()` shape `{"Value": desc, "WFSerializationType": ...}`. Both
`set_brightness()`/`set_media_volume()` (below) feed their `source` argument through
`variable()`/`output()`-style helpers elsewhere in the file, so this unwrap logic applies
unchanged — no new branch needed for the Set-action position.

**Source-tracing — `_numeric_operand_report()`** (lines 2407-2468) walks every
`is.workflow.actions.setvariable` definition of a name back through
`NUMERIC_SOURCE_ACTIONS`/`<literal>`/`<builtin>` to decide if a variable is "already
Number-typed." This is why RESEARCH.md's own site-classification table (`Restore
Brightness`/`Dim Target` → Text-sourced → need coercion; `Silence Target` →
`number()`-sourced → likely already numeric) is derived mechanically by this function, not
guessed — nothing needs to change here for the new table entries; the generic pass already
covers whatever identifier produced the site.

**Normalisation — `normalise_numeric_operands()`** (lines 2475-2493):
```python
for _index, _field, descriptor, sources in _numeric_operand_report(actions):
    if descriptor is None or _already_numeric(sources):
        continue
    existing = descriptor.setdefault("Aggrandizements", [])
    if not any(a.get("Type") == "WFCoercionVariableAggrandizement" for a in existing):
        existing.insert(0, dict(NUMBER_COERCION))
```
This is where the coercion aggrandizement is actually attached. It is 100% generic over
`NUMERIC_OPERAND_FIELDS` — no per-identifier logic needs to be added for
`setbrightness`/`setvolume`.

**Verification / build-guard — `verify_numeric_operands()`** (lines 2496-2527): raises
`SystemExit` with a diagnostic listing every offending `(action_index, field, sources)` if
any numeric-typed operand lacks the coercion. This is the "negative-control" check
RESEARCH.md's Wave-0-gap item asks the plan to exercise (temporarily removing the two new
table entries and confirming the guard fails loudly is a valid verification task using this
exact function).

**The two producer call sites the new table entries cover** (`tools/build_state_engine.py`
lines 433-440):
```python
def set_brightness(source):
    return action("is.workflow.actions.setbrightness", WFBrightness=source,
                  ShowWhenRun=False)


def set_media_volume(source):
    return action("is.workflow.actions.setvolume", WFVolume=source,
                  WFVolumeSetting="Media", ShowWhenRun=False)
```
`source` here is exactly the raw value shape `_numeric_operand_sites()`/`_operand_descriptor()`
expect (a `variable()`/`output()`-produced dict), confirming the new table entries need no
change to these two producer functions themselves — the fix is purely additive at the table.

**Where the pipeline is invoked end-to-end** (line ~2877 and ~2883, inside the generator's
main build function):
```python
normalise_numeric_operands(actions)
...
verify_numeric_operands(actions)
```
These two calls already run unconditionally on every build; adding the table entries is
sufficient to bring all 28 `setbrightness`/`setvolume` sites under both passes with zero
other code changes.

---

### `.planning/phases/09-.../09-UAT.md` (new) — device-proving checklist (test, request-response/manual-checkpoint)

**Analog:** `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`

**Frontmatter pattern** (lines 1-7):
```yaml
---
status: testing
phase: 05-nine-primitives-environmental-safety
source: [05-01-SUMMARY.md, 05-02-SUMMARY.md, 05-03-SUMMARY.md]
started: 2026-08-16T00:11:00.000Z
updated: 2026-08-16T00:11:00.000Z
---
```

**`## Current Test` section** — a single overwritten pointer to "where we are," not a log:
```markdown
## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Test a Circle harness itself works
expected: |
  Test a Circle (manual menu) fires without the sequence Set Dictionary Value error that
  broke it once already.
awaiting: user response
```

**`## Context` section** — free-form paragraphs establishing what's untested and why,
citing prior device history and cross-referencing canonical strategy sections. For Phase 9
this should reuse the exact language RESEARCH.md already supplies (28-site correction, the
coercion-shape unknown, the four+one restoration/failure-mode triggers, the safety-floor
addendum) rather than re-deriving it.

**`## Tests` section** — numbered subsections, each with `expected:` prose and a
`result: pending` placeholder, e.g.:
```markdown
### 5. Safety floors (pass/fail, not observations)
expected: no zero brightness, no unsafe/startling volume, nothing that strands
accessibility, across every primitive fired. Any violation is stop-the-line regardless of
how the rest of the run went.
result: pending
```
Phase 9's own tests map directly from RESEARCH.md's "Phase Requirements → Test Map" table
(criteria 2-7) — each row becomes one numbered `### N.` block with `expected:`/`result:`.

**`## Summary` section** — trailing tally block:
```markdown
## Summary

total: 13
passed: 0
issues: 0
```

---

## Shared Patterns

### Table-driven numeric-operand coercion (the single load-bearing pattern for Plan A)
**Source:** `tools/build_state_engine.py` `NUMERIC_OPERAND_FIELDS` (2362) →
`_numeric_operand_sites()` (2368) → `_numeric_operand_report()` (2407) →
`normalise_numeric_operands()` (2475) → `verify_numeric_operands()` (2496)
**Apply to:** the two new entries only — no other function in this pipeline needs editing.
```python
NUMBER_COERCION = {"Type": "WFCoercionVariableAggrandizement",
                    "CoercionItemClass": "WFNumberContentItem"}  # (name inferred from usage at line 2493; confirm exact literal at its definition site before use)
```
Note: `NUMBER_COERCION`'s definition itself was not re-read in this pass (already
established/used elsewhere in the file per RESEARCH.md's Donor-4.1 cross-reference) —
planner should grep `NUMBER_COERCION =` once before editing to confirm the literal dict
shape rather than re-typing it from this excerpt.

### UAT.md checkpoint structure
**Source:** `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md` (also
consistent with `04-UAT.md`/`07-UAT.md` per RESEARCH.md's own citation — not re-read here
since 05-UAT.md alone fully establishes the structure and stop-condition rule: "Wave 0 Gap"
items become `## Tests` entries).
**Apply to:** `09-UAT.md` (new file, to be created by the planner/executor, not by this
pattern-mapping pass).

## No Analog Found

None. Both files in scope have a same-project, high-quality analog (one in the same source
file, one a sibling phase's UAT.md).

## Metadata

**Analog search scope:** `tools/build_state_engine.py` (targeted grep + two non-overlapping
`Read` ranges: lines 425-495 and 2355-2535); `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`
(head + tail, non-overlapping)
**Files scanned:** 2 (both were also the analogs — no broader repo search was needed given
RESEARCH.md already pinpointed the exact in-file table and named the UAT.md precedents)
**Pattern extraction date:** 2026-08-16
