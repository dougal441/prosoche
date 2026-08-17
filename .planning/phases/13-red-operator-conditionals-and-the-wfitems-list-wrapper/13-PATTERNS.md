# Phase 13: Red-operator conditionals and the WFItems List wrapper - Pattern Map

**Mapped:** 2026-08-17
**Files analyzed:** 5 modified (0 created)
**Analogs found:** 5 / 5 (all in-file siblings)

This phase creates **no new files**. Every unit of work is an in-file addition to an existing
module, so every analog below is an *in-file sibling* — the nearest existing function, guard,
or registration site that the new code must imitate key-for-key.

## File Classification

| Modified File | Unit of work | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|---|
| `tools/build_state_engine.py` | new `verify_list_item_wrappers()` | build-time guard | transform (validate over emitted action array) | `verify_conditional_action_string()` `:2413-2446` | exact (same shape, same idiom, same failure class) |
| `tools/build_state_engine.py` | extend `verify_conditional_action_string()` | build-time guard | transform | itself, `:2430-2446` | exact (in-place extension) |
| `tools/build_state_engine.py` | guard registration | config/harness | sequential invocation chain | `main()` verify chain `:4160-4177` | exact |
| `tools/build_state_engine.py` | fix `mirror_text()` `:651` | emitter helper | transform (Python data → plist dict) | `list_items()` `:416-419` | exact (same `WFItems=list(items)` line, correct case) |
| `tools/build_sentient.py` | arm the new guard | config/harness | sequential invocation | import list `:13-33` **and** guard block `:294-357` | exact |
| `docs/*.py` | (optional companion checker) | post-hoc checker | file-I/O + transform | `docs/sequence_dispatch_check.py` | role-match |
| `.claude/CLAUDE.md`, `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md` | doc updates | docs | — | no code analog needed | n/a |

---

## Pattern Assignments

### 1. `verify_list_item_wrappers()` — new guard in `tools/build_state_engine.py`

**Analog:** `verify_conditional_action_string()` — `tools/build_state_engine.py:2413-2446`, quoted in full.
This is the closest sibling: same file, same "device-visible defect invisible to the validator"
motivation, same single-identifier filter + offender-collection + `SystemExit` shape.

```python
def verify_conditional_action_string(actions):
    """Fail the build if a conditional's comparison target is the abandoned bare placeholder.

    WFConditionalActionString is the RIGHT/comparison-target side of a conditional (WFInput,
    checked by verify_conditional_inputs() above, is the LEFT/compared-variable side). The
    generator's established idiom for a variable-backed comparison target is:
    if_block(..., string=<placeholder text>) immediately followed by a reassignment to a real
    token(<variable>) envelope. At least ten sites left that reassignment out and shipped the
    bare, un-enveloped single placeholder character ("￼") instead -- structurally valid,
    silently wrong at runtime (the comparison can never match a real value). This was the
    confirmed root cause of G-04-1 (session duration always 0) and G-04-3 (CLOSE never
    switches, permanent no-op); see .planning/debug/G-04-1-close-duration-zero.md and
    .planning/debug/G-04-3-session-race-not-switching.md. Neither verify_conditional_inputs()
    (WFInput side only) nor STRING_ENVELOPE_PARAMS (does not cover
    is.workflow.actions.conditional) catches this axis, so this is a dedicated guard against
    the exact same defect class shipping silently again.
    """
    offenders = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        # Otherwise (1) and End If (2) never carry a comparison target of their own.
        if parameters.get("WFControlFlowMode") != 0:
            continue
        if "WFConditionalActionString" not in parameters:
            continue
        if parameters["WFConditionalActionString"] == "￼":
            offenders.append(index)
    if offenders:
        raise SystemExit("conditional comparison targets hold the abandoned bare placeholder "
                         "character instead of a wired token() reference: actions "
                         + ", ".join(str(i) for i in offenders[:5])
                         + f" ({len(offenders)} total)")
```

**Conventions the new guard must copy, extracted from the above:**

| Convention | Concrete rule from `:2413-2446` |
|---|---|
| Signature | `def verify_<thing>(actions):` — module-level, one positional arg, the emitted action list. No return value. |
| Docstring | Opens `"""Fail the build if …"""`, then a prose block naming: what the slot is, *why* the shape is wrong at runtime, the requirement/defect ID it protects, the evidence source, and which existing guard does **not** already cover it. |
| Traversal | `for index, item in enumerate(actions):` → `continue`-guard on `WFWorkflowActionIdentifier` → `parameters = item.get("WFWorkflowActionParameters", {})` → further `continue`-guards. Never a comprehension. |
| Accumulator | `offenders = []`, appended with the action `index` (this phase's guard needs `(index, position)` tuples — a justified extension, since the defect is per-row not per-action). |
| Failure | `raise SystemExit(<message>)`, **never `assert`**. Message = prose cause + `", ".join(...)` of the **first 5** offenders + `f" ({len(offenders)} total)"`. |
| Placement | Module level, adjacent to the sibling guards (the `verify_*` cluster spans `:1518`-`:3795`). |

RESEARCH.md `## Code Examples` already contains a draft that conforms to this shape;
the planner can specify it verbatim.

---

### 2. Guard-registration site — `tools/build_state_engine.py:4157-4177`

**Analog:** the harness block itself, quoted verbatim. There is exactly one registration site.

```python
    normalise_string_envelopes(actions)
    normalise_output_names(actions)
    normalise_numeric_operands(actions)
    verify_parameter_keys(actions)
    verify_string_envelopes(actions)
    verify_output_names(actions)
    verify_required_pickers(actions)
    verify_conditional_inputs(actions)
    verify_conditional_action_string(actions)
    verify_numeric_operands(actions)
    verify_state_seed(actions)
    verify_pending_exit_seed(actions)
    verify_panic_escape_seed(actions)
    verify_exit_events_seed(actions)
    verify_active_session_seed(actions)
    verify_restore_gates(actions)
    verify_sentinel_gates(actions)
    verify_compound_value_reads(actions)
    verify_router_shape(actions)
    verify_circle_zero_silence(actions)
    verify_dispatch_coverage(actions)
```

**Rules extracted:**
- All `normalise_*` calls precede all `verify_*` calls.
- One bare call per line, no comment per call at this site (comments live in the docstrings).
- The whole chain sits **before** `SOURCE.write_bytes(...)` at `:4189` — so a raise aborts
  before any write. Confirm the new call lands above `:4187`'s pinned-actions check.
- Ordering matters for sensitivity demos: a guard registered *after* another that also fires
  will be masked (this is exactly what Phase 12-03 hit — see §7).

---

### 3. The two touch points in `tools/build_sentient.py`

Phase 12 regressed by editing only one. Both are quoted.

**Touch point A — import list, `tools/build_sentient.py:13-33`** (alphabetical within the
`verify_*` run; `normalise_*` first):

```python
from build_state_engine import (
    normalise_numeric_operands,
    normalise_output_names,
    normalise_string_envelopes,
    verify_active_session_seed,
    verify_compound_value_reads,
    verify_conditional_action_string,
    verify_conditional_inputs,
    verify_dispatch_coverage,
    verify_exit_events_seed,
    verify_numeric_operands,
    verify_output_names,
    verify_panic_escape_seed,
    verify_pending_exit_seed,
    verify_required_pickers,
    verify_restore_gates,
    verify_router_shape,
    verify_sentinel_gates,
    verify_state_seed,
    verify_string_envelopes,
)
```

Note: `verify_parameter_keys` and `verify_circle_zero_silence` are **not** imported — the
Sentient fork runs 19 of the 21, not all. Adding a guard here is a deliberate choice, not
automatic.

**Touch point B — invocation block, `tools/build_sentient.py:294-357`.** Unlike Dumb's bare
chain, every Sentient arming carries a **justification comment explaining why it is asserted
per-fork rather than inferred from Dumb**. Representative excerpt, `:299-317`:

```python
    # Sentient INHERITS the seeded bootstrap template from the built Dumb source rather
    # than re-seeding it, so the assertion is the whole point here: it proves the subtree
    # survived the fork, and it fails loudly if a future Sentient-only insertion ever adds
    # a settings_snapshot read that the shared bootstrap does not establish.
    verify_state_seed(actions)
    # PHASE 12 (12-01).  Sentient INHERITS the seeded bootstrap template from the built Dumb
    # source rather than re-seeding it, so the assertion is the whole point here: it proves
    # exit_events and exit_selection_counter survived the fork.  Asserted per fork, never
    # inferred from Dumb -- a fork that dropped the rolling window would leave STATE-12's
    # "bounded, versioned document" claim false on the Aware artifact with no error anywhere.
    verify_exit_events_seed(actions)
```

And `:318-341` is the canonical precedent for *this exact phase's* situation — arming a
previously-unarmed inherited guard, with a `#   verify_x -- why` bullet list:

```python
    # PHASE 12 (12-01, PD-3) -- four guards this fork inherited but never asserted.  Measured
    # before this phase: build_sentient.py imported 13 symbols and ran 13 guards, and none of
    # these four was among them -- so pending_exit, the very seed pattern 12-01 mirrors, was
    # not checked on the Aware fork at all.  The phase rule is "fix whole classes, never
    # site-by-site", and a verifier set that asserts the NEW seed but not the pattern it
    # copies is exactly the site-by-site posture that rule forbids.  ...
    verify_pending_exit_seed(actions)
    verify_panic_escape_seed(actions)
    verify_compound_value_reads(actions)
    verify_conditional_action_string(actions)
```

**Verification idiom for "did I hit both?"** — RESEARCH.md Pitfall 3 names it:
`grep -c verify_ tools/build_sentient.py` must increase by **2** (one import + one call) per
new guard.

---

### 4. `mirror_text()` (the defect) and the literal-vs-variable helpers

**The defect site — `tools/build_state_engine.py:648-656`, quoted in full:**

```python
def mirror_text(items, name: str):
    """Select one non-empty template from a fact-gated list using Circle 1..9."""
    list_id, item_id = uid(), uid()
    a = [action("is.workflow.actions.list", UUID=list_id, WFItems=list(items)),
         action("is.workflow.actions.getitemfromlist", UUID=item_id,
                WFItemSpecifier="Item At Index", WFItemIndex=variable("Circle Next"),
                WFInput=output(list_id, "List")),
         set_var(name, output(item_id, "Item from List"))]
    return a
```

**The must-not-touch sibling — `list_items()`, `tools/build_state_engine.py:416-419`:**

```python
def list_items(items, name: str):
    list_id = uid()
    return [action("is.workflow.actions.list", UUID=list_id, WFItems=list(items)),
            set_var(name, output(list_id, "List"))]
```

These two share the **identical** `WFItems=list(items)` expression. The difference is entirely
in what the caller passes: `list_items(EXIT_NAMES, …)` passes plain `str`, `mirror_text(...)`
passes `text_token(...)` dicts. **This is why a blanket sweep of the `WFItems=` expression
would corrupt `list_items()`** — the emitter cannot tell them apart; only the *row value's*
type can.

**Existing helpers that produce the two row kinds — `:134-161`, quoted:**

```python
def output(uuid_value: str, name: str):
    return {"Value": {"OutputUUID": uuid_value, "OutputName": name,
                      "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def token(name: str):
    return {"Value": {"string": "￼", "attachmentsByRange":
            {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}


def text_token(parts: list[tuple[str, str | None]]):
    string, attachments, cursor = "", {}, 0
    for literal, name in parts:
        string += literal
        cursor += len(literal)
        if name:
            attachments[f"{{{cursor}, 1}}"] = {"Type": "Variable", "VariableName": name}
            string += "￼"
            cursor += 1
    return {"Value": {"string": string, "attachmentsByRange": attachments},
            "WFSerializationType": "WFTextTokenString"}
```

**Requested pattern: "a nearby helper that already distinguishes literal from variable-bearing
content."** The closest is `text_token()` at `:151-161` — its `if name:` branch is the only
existing *per-item* literal/variable discriminator in this helper cluster. It discriminates on
a `None` name inside a parts tuple, **not** on `isinstance(x, str)`. There is **no existing
`isinstance`-based row/literal discriminator anywhere in the emitter helpers** — grep of
`build_state_engine.py` finds no `isinstance` in the `:134-660` helper region. So the
`_list_row()` helper RESEARCH.md Pattern 1 proposes is a **new idiom**, not a copy of an
existing one; the planner should say so rather than claim an analog.

The nearest structural precedent for that new idiom is `verify_conditional_action_string()`'s
own `if parameters["WFConditionalActionString"] == "￼"` — i.e. the project *does* already
branch on a plist value's concrete form elsewhere, just not in an emitter.

---

### 5. `verify_conditional_action_string()` — the extension target

Quoted in full under §1 above (`:2413-2446`). The extension is a **positive** assertion added
inside the existing loop, after the existing `if parameters["WFConditionalActionString"] == "￼"`
check. Concrete constraints the existing body imposes on the extension:

- The two `continue` guards (`WFControlFlowMode != 0`, `"WFConditionalActionString" not in
  parameters`) are already in place and must be reused, not duplicated.
- The existing negative check compares against the raw `"￼"` **string**; the new positive check
  operates on the `dict` case. They are disjoint by type, so both can live in one loop with
  `isinstance(value, dict)`.
- If a **second** offender list is introduced (recommended, so the two failure messages stay
  distinguishable), it needs its own `raise SystemExit(...)` following the same
  prose + first-5 + total format. Note that the first `raise` short-circuits the second —
  relevant to §7's sensitivity demo.
- The docstring must be extended with the Donor-5 provenance, matching the existing docstring's
  habit of citing evidence files by path.

RESEARCH.md `### Pinning the Donor-5-confirmed conditional shape` supplies the body.

---

### 6. `docs/*.py` checker — closest analog if a companion checker is added

**Analog:** `docs/sequence_dispatch_check.py:1-55`.

It is the only checker in `docs/` that is an explicit *deliberate duplicate of an in-generator
`verify_*` guard*, which is exactly the relationship a List-wrapper checker would have to
`verify_list_item_wrappers()`. Its docstring states the pattern (`:41-47`):

```
`tools/build_state_engine.py`'s `verify_dispatch_coverage()` enforces the same invariant
inside both builders, before any write.  The two are deliberate duplicates: the build guard
aborts a bad build, and this script proves the shipped artifact independently, from disk,
without importing the generator that produced it.

Read-only: parses the built artifact with plistlib.  No subprocess, no rebuild.
```

Conventions to copy: `#!/usr/bin/env python3`; a long module docstring opening with
**"THIS IS A GATE."** and a **"WHY A GATE AND NOT A REPORT"** section naming the silent runtime
consequence and why every file-level tool is blind to it; `from __future__ import annotations`;
`import plistlib` + `from pathlib import Path`; `ROOT = Path(__file__).resolve().parents[1]`;
standalone script exiting 0/1; **must not import the generator**.

RESEARCH.md `## Alternatives Considered` prefers the in-generator guard and calls a checker
optional ("Both is best — guard blocks, checker documents"). The planner should treat this
analog as available, not mandatory.

**Full checker inventory** (12 files, all currently green — the regression set):
`environmental_restore_check.py`, `manifest_check.py`, `note_identity_check.py`,
`phase5_self_check.py`, `phase6_self_check.py`, `phase7_self_check.py`, `phase9_self_check.py`,
`router_ui_census.py`, `sentient_audit_check.py`, `sentient_core_check.py`,
`sequence_dispatch_check.py`, `state_engine_self_check.py`.

---

### 7. Guard-sensitivity demonstration — established precedent EXISTS

**Precedent found.** Phase 12 established it across all three plans. Quoted verbatim.

**Precedent A — plan-side acceptance criterion, `.planning/phases/12-…/12-01-PLAN.md:239`:**

> Guard sensitivity: with the `seed_exit_events(actions)` call neutralised against a pre-seed
> template, `verify_exit_events_seed()` raises `SystemExit` and the message names STATE-12.
> The observed message text appears in the commit body.

**Precedent B — the canonical evidence-row format, `12-02-SUMMARY.md:165-166`:**

> | Guard sensitivity (direct call) | `verify_active_session_seed()` raised `SystemExit` against the pre-seed template's actions, naming `restore_managed_settings` and SESS-07 / SAFE-01 |
> | Guard sensitivity (full build) | seeder commented out + `src/PROSOCHE-Dumb.xml` reverted to `930b762` -> `python3 tools/build_state_engine.py` exited 1 with the identical message before `SOURCE.write_bytes()`; both files restored via `git checkout --`, rebuilt clean, Sentient digest byte-identical to the pre-demonstration build |

**Precedent C — the two-ways rule and *why*, `12-03-SUMMARY.md:159`:**

> `main()`'s verify chain calls `verify_active_session_seed()` before `verify_sentinel_gates()`,
> so a full-build revert fires the former's newly-armed assertion 3 first. A direct-call script
> (mirroring 12-02's own two-ways technique) was written to skip the earlier guard and isolate
> `verify_sentinel_gates()`'s own message.

**The established procedure, distilled:**
1. **Direct call** — build the action list (or load the reverted artifact), call the new
   verifier in isolation, capture the verbatim `SystemExit`. Fast, no working-tree churn.
2. **Full build** — synthetically revert the generator line (comment out / restore the old
   `WFItems=list(items)`), run `python3 tools/build_state_engine.py`, confirm **exit 1 with the
   identical message, before `SOURCE.write_bytes()`**.
3. **Restore** via `git checkout -- <files>`, rebuild clean, and prove **the rebuilt digest is
   byte-identical** to the pre-demonstration build.
4. Record the **verbatim message text** in the commit body **and** in the SUMMARY's
   verification table using the two-row format of Precedent B.

**Direct relevance to this phase:** §5's extended `verify_conditional_action_string()` will
have *two* raises in one function, the first masking the second — the same masking problem
12-03 solved with the direct-call isolation script. The planner should pre-specify the
direct-call path for the pinning assertion.

---

## Shared Patterns

### `SystemExit`, never `assert`
**Source:** all 21 `verify_*` in `tools/build_state_engine.py` (`:1518, :1586, :1689, :2336,
:2363, :2413, :2582, :2713, :2780, :2905, :3031, :3271, :3313, :3397, :3651, :3724, :3779, :3795`).
**Apply to:** every new or extended guard.
**Message format:** `<prose cause>` + `", ".join(first 5 offenders)` + `f" ({len(offenders)} total)"`.

### Guards run before the single write
**Source:** `tools/build_state_engine.py:4160-4189` — the whole chain precedes
`SOURCE.write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False))  # exactly one serialization/write`.
**Apply to:** the registration of `verify_list_item_wrappers()`.

### Per-fork assertion, never inference
**Source:** `tools/build_sentient.py:299-357` — every armed guard carries a comment explaining
why the Aware fork asserts it itself rather than trusting the Dumb build.
**Apply to:** the Sentient arming of the new guard.

### Determinism / byte-idempotency
**Source:** `docs/phase6_self_check.py`; RESEARCH.md Pitfall 6.
**Apply to:** the `mirror_text()` fix — it must introduce **no new `uid()` call** (the proposed
`_list_row()` introduces none), and a second build must be byte-identical.

---

## No Analog Found

| Item | Role | Data Flow | Reason |
|---|---|---|---|
| `_list_row(item)` — `isinstance(item, str)` row discriminator | emitter helper | transform | **No `isinstance`-based literal/variable discriminator exists anywhere in the emitter-helper region (`:134-660`).** `text_token()`'s `if name:` (`:157`) is the nearest *conceptual* relative but discriminates on a `None` field inside a parts tuple, not on a value's Python type. This is a genuinely new idiom; do not describe it as copying an existing one. Its shape is fixed by Donor 4 / 4.1 evidence (RESEARCH.md Pattern 1), not by a codebase precedent. |
| Per-row `(action_index, row_position)` offender tuples in a guard | guard | transform | Every existing guard collects a flat action `index`. `verify_list_item_wrappers()` needs row granularity. This is a justified extension of the accumulator convention, not a copy; the `SystemExit` message format still applies (`f"action {i} row {p}"`). |

## Metadata

**Analog search scope:** `tools/build_state_engine.py` (4193 lines, targeted reads at
`:134-161`, `:410-423`, `:640-684`, `:2413-2452`, `:4140-4194`; full `verify_*` symbol index by
grep), `tools/build_sentient.py` (`:12-35`, `:280-359`), `docs/*.py` (12 files, inventory +
`sequence_dispatch_check.py:1-55`), `.planning/phases/12-*/` (grep for the sensitivity precedent).
**Files scanned:** 16
**Pattern extraction date:** 2026-08-17
