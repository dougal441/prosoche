# Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster - Pattern Map

**Mapped:** 2026-08-17
**Files analyzed:** 9 (2 created, 7 modified)
**Analogs found:** 9 / 9

All excerpts below were read this session at `ae0226c` and are quoted verbatim with `file:line`.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `tools/build_state_engine.py` — **new** `verify_dispatch_coverage(actions)` | build guard (validator) | transform → assert → SystemExit | `verify_pending_exit_seed()` `tools/build_state_engine.py:2172-2194` | exact |
| `tools/build_state_engine.py` — `primitive_dispatch()` tuple + condition 99→4 | generator (branch construction) | transform | `if_block("Previous Respected", 4, string="true")` `:614` | exact |
| `docs/note_identity_check.py` — **new** standalone checker | test / structural checker | file-I/O → assert → exit | `docs/sentient_audit_check.py` (24 lines, complete) | exact |
| `docs/sequence_dispatch_check.py` — reporter → gate | test / structural checker | file-I/O → assert → exit | `docs/manifest_check.py` `require()` + raise `AssertionError` | role-match |
| `src/PROSOCHE-Dumb.xml` action 7 — `sequences` arrays | config literal (plist) | plistlib round-trip | `docs/sequence_dispatch_check.py:95-103` `config_literal()` (reader) | role-match |
| `src/PROSOCHE-Dumb.xml` action 3616 — Note body `WFTextTokenString` | data / user-facing copy | plistlib round-trip + offset recompute | quick task `260817-au7` six-step method (`docs/BUILD-NOTES.md` §20) | exact |
| `tools/build_state_engine.py` — `universal_leaving()` Panic Escape gate | generator (control flow) | request-response (menu) | `if_block(..., number=...)` numeric gate + `verify_circle_zero_silence()` | role-match |
| `docs/manifest_check.py` `DISPLAY_NAMES` | config constant in a checker | table-driven assert | itself (edit in place) | n/a |
| `docs/sentient_core_check.py:9` | assertion | assert | itself (edit in place) | n/a |

---

## Pattern Assignments

### 1. `verify_dispatch_coverage(actions)` — new build guard in `tools/build_state_engine.py`

**Analog:** `verify_pending_exit_seed()` — the container/leaf precedent named by RESEARCH.

**The full `verify_*` family in `tools/build_state_engine.py`** (measured, `grep -n "^def verify_"`):

```
1353 verify_router_shape            2071 verify_state_seed        2688 verify_numeric_operands
1421 verify_circle_zero_silence     2172 verify_pending_exit_seed 2761 verify_string_envelopes
1848 verify_required_pickers        2309 verify_restore_gates     2816 verify_output_names
1875 verify_conditional_inputs      2351 verify_sentinel_gates    2832 verify_parameter_keys
1925 verify_conditional_action_string  2434 verify_compound_value_reads
```

`tools/build_sentient.py:12-25` imports nine of them by name from the engine module and re-runs
them at `:201-221` — a new guard should be added to **both** import list and call chain.

**The full analog** (`tools/build_state_engine.py:2172-2194`) — note the docstring form
("Fail the build unless …"), the `raise SystemExit(...)` failure convention (never `assert`,
never `print`+`exit`), and the long actionable message naming the historical defect:

```python
def verify_pending_exit_seed(actions):
    """Fail the build unless pending_exit is seeded exactly as a {type, timestamp} container.

    Same discipline as verify_state_seed(): the invariant seed_pending_exit() establishes
    is asserted separately so the two cannot silently drift.
    """
    _, inner = _state_template(actions)
    document = inner["string"].replace('"￼"', '"x"').replace("￼", "0")
    try:
        seed = json.loads(document)
    except json.JSONDecodeError as error:
        raise SystemExit(f"bootstrap state.json template is not valid JSON: {error}")
    pending = seed.get("pending_exit")
    if not isinstance(pending, dict) or any(pending.get(leaf) != value
                                            for leaf, value in PENDING_EXIT_SEED.items()):
        raise SystemExit(
            f"pending_exit is seeded as {pending!r}; it must be exactly {PENDING_EXIT_SEED!r} "
            "-- an absent or malformed seed reproduces the confirmed cycle-16 hard error "
            "(\"no value was found for dictionary key 'pending_exit'\"), and any other "
            "leaf value risks the same sentinel-vs-real-value confusion axis 7 already "
            "closed for settings_snapshot")
```

**Insertion point — the verify chain in `main()`** (`tools/build_state_engine.py:3130-3143`),
verbatim. Append `verify_dispatch_coverage(actions)` after the last line shown:

```python
    verify_parameter_keys(actions)
    verify_string_envelopes(actions)
    verify_output_names(actions)
    verify_required_pickers(actions)
    verify_conditional_inputs(actions)
    verify_conditional_action_string(actions)
    verify_numeric_operands(actions)
    verify_state_seed(actions)
    verify_pending_exit_seed(actions)
    verify_restore_gates(actions)
    verify_sentinel_gates(actions)
    verify_compound_value_reads(actions)
    verify_router_shape(actions)
    verify_circle_zero_silence(actions)
```

The chain runs **after** `normalise_*` and **before** the pinned-actions equality check and
the single `SOURCE.write_bytes(...)` at `:3155` — i.e. a raising guard aborts before any write.

**Failure convention (settled):** `raise SystemExit(<message>)` inside `build_state_engine.py`;
`raise AssertionError(<message>)` via a `require()` helper inside `docs/*.py`. Do not mix.

---

### 2. `docs/note_identity_check.py` — new standalone checker

**Analog A — the shortest complete checker, `docs/sentient_audit_check.py` (24 lines, end to end).**
Copy this shape: shebang, one-line docstring stating what is proved, `plistlib.loads(Path(...).read_bytes())["WFWorkflowActions"]`,
bare `assert` with a message operand, single `print(...)` on success, no `main()`, no `__main__` guard:

```python
#!/usr/bin/env python3
"""Focused evidence for the bounded Sentient audit protocol."""
import plistlib
import re
from pathlib import Path

a = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())["WFWorkflowActions"]
start = next(i for i, x in enumerate(a) if "--- SENTIENT CONTRACT AUDIT ---" in x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
end = next(i for i, x in enumerate(a[start + 1:], start + 1) if "--- SENTIENT CONTRACT AUDIT END ---" in x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
block = a[start:end + 1]
raw = str(block)
assert raw.count("is.workflow.actions.askllm") == 1
for phrase in ("ALLOW", "CHALLENGE", "DENY", ... , "Previous Respected"):
    assert phrase in raw, phrase
...
print("sentient audit check: compact prompt, one challenge, bounded fallback")
```

**Analog B — the richer message idiom for a check that must be actionable**
(`docs/manifest_check.py:63-65` helper, `:148-153` message):

```python
def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)
```

```python
    require(
        basename in SIGNED_BASENAMES,
        f"signed artifact {basename!r} is not one of the two canonical display names "
        f"{sorted(SIGNED_BASENAMES)} -- a suffixed name imports as a separate library "
        f"entry the Personal Automations do not reference (DIST-04)",
    )
```

**Analog C — how `docs/router_ui_census.py` reaches Note/UI surfaces**, if the planner prefers
extending it rather than adding a twelfth script. Identifier constants (`:40-42`):

```python
SHOWNOTE = "is.workflow.actions.shownote"
FIND_NOTES = "is.workflow.actions.filter.notes"
CREATE_NOTE = "com.apple.mobilenotes.SharingExtension"
```

and its per-arm counting pass (`:133-151`), which is identifier-keyed and mode-aware:

```python
def counted_identifier(item) -> str | None:
    """The counted identifier for this action, or None if it is not a user-facing surface."""
    identifier = item.get("WFWorkflowActionIdentifier")
    if identifier not in COUNTED:
        return None
    if identifier == MENU and _parameters(item).get("WFControlFlowMode") != 0:
        return None
    return identifier


def census(actions, arms) -> dict[str, dict[str, int]]:
    table = {arm: dict.fromkeys(COUNTED, 0) for arm in ARMS}
    for arm, (start, end) in arms.items():
        for index in range(start, end):
            identifier = counted_identifier(actions[index])
            if identifier:
                table[arm][identifier] += 1
    return table
```

Note `router_ui_census.py:191` uses a `def main()` + `if __name__ == "__main__": main()`; the
short checkers do not. Both idioms exist — pick Analog A's for a new small checker.

**What the new checker must assert (the three Note-identity sites, from RESEARCH §6):**
action **3602** `filter.notes` predicate `Values.String`, action **3616** `gettext`
`WFTextActionText` H1, action **3619** `SharingExtension` `name` — all three equal to the same
title string, in **both** forks (Sentient body at 3684). Locate by content, never index —
see the `config_literal()` pattern in §5 below.

---

### 3. Promoting `docs/sequence_dispatch_check.py` from reporter to gate

**Docstring to rewrite** (`:1-31`, opening paragraph verbatim):

```python
"""Report which Config sequence entries dispatch nothing, and which branches nothing names.

THIS IS A REPORTING SCRIPT, NOT A GATE.  It exits 0 in every case, including when it finds
an orphan it has never seen before.  That is deliberate and is required by the ROADMAP:
Circle 8 already ships dead -- the `"Voice"` sequence entry names no emitted dispatch branch
and silently matches nothing, with no error anywhere -- and fixing it is a later phase's
work (`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`).  A checker
that failed on it would block this phase on a defect this phase was told not to fix.  So the
orphan is RECORDED, by name and by the Circle positions it occupies, and the run stays green.
A future phase may promote this script to a build guard once the primitive roster and the
matching strategy have settled under BD-06.
```

**`KNOWN_ORPHANS`** (`:48-53`) — must be emptied (`Voice` is closed by this phase):

```python
# Orphans that are known, accepted, and owned elsewhere.  Each maps to the todo that owns
# the fix.  An orphan NOT in this mapping is still reported and still exits 0, but it is
# marked as unexpected so it cannot hide among the accepted ones.
KNOWN_ORPHANS = {
    "Voice": ".planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md",
}
```

**`match_strategy(code)`** (`:56-72`) — **keep exactly as is**; it already resolves 99→contains
and 4→exact per branch, which is what survives the 99→4 move without edits:

```python
def match_strategy(code):
    """Resolve one conditional's own WFCondition into the matching rule IT uses.

    This is the code -> strategy resolver, and it is the only place in this file that looks
    at a condition code at all.  Both arms below dispatch on a code READ FROM A CONDITIONAL
    in the artifact; neither presumes which code the artifact will carry.  That is what lets
    this script keep working across BD-06 Decision 5's move from "contains" to "string is":
    when the generator changes, the conditionals change, and this function simply returns
    the other answer for them.

    Anything else is "unknown" -- reported, never guessed at.
    """
    if code == 99:  # "contains": the tested string need only appear inside the entry
        return "contains"
    if code == 4:   # "string is": the tested string must equal the entry exactly
        return "exact"
    return "unknown"
```

**The exit path to change** (`:195-201`, the tail of `main()`) — today it computes `unexpected`
and only prints; there is no `raise`, no `sys.exit`, so the process exits 0 unconditionally:

```python
    unexpected = [component for component in orphans if component not in KNOWN_ORPHANS]
    print(f"\nsequence dispatch check: {len(orphans)} orphan(s) "
          f"({len(unexpected)} unexpected), {len(unreachable)} unreachable, "
          f"{len(unknown)} of unknown semantics -- reported, not gated")


if __name__ == "__main__":
    main()
```

**Precise change:** after the final `print`, add a `require(...)`-style raise (Analog B above)
covering `unexpected`, `unreachable`, and `unknown`, and drop the trailing
`-- reported, not gated` from the summary line. Add the BD-06 "exactly one dispatch branch"
clause the reporter does not currently test (its orphan test is `any(...)` = *at least one*,
`:153-157`).

---

### 4. The dispatch branch construction site — `primitive_dispatch()`

`tools/build_state_engine.py:645-668`, verbatim. This is the whole dispatch surface; the tuple
at `:658-660`, the `continue` at `:661-662`, and the literal `99` at `:663` are the entire edit:

```python
    a = [comment(DISPATCH_MARKER + "\n\n- Select exactly one configured sequence entry for Circle after Leaving is offered.\n- Combined entries call only their named primitives.")]
    a += read_value("sequence", variable("State"), "Sequence")
    if circle_name is None:
        a += read_value("circle", variable("State"), "Dispatch Circle")
    else:
        a += [set_var("Dispatch Circle", variable(circle_name))]
    entry_id, entry_text_id = uid(), uid()
    a += [action("is.workflow.actions.getvalueforkey", UUID=entry_id,
                 WFDictionaryKey=text_token([("sequences.", "Sequence"), (".", None), ("", "Dispatch Circle")]),
                 WFInput=variable("Config")),
          action("is.workflow.actions.gettext", UUID=entry_text_id,
                 WFTextActionText=output(entry_id, "Dictionary Value")),
          set_var("Selected Primitive", output(entry_text_id, "Text"))]
    for name, implementation in (("Knock", knock), ("Ash", ash), ("Silence", silence),
                                 ("Confession", confession), ("Dimming", dimming), ("Exile", exile),
                                 ("Mirror", mirror_and_voice), ("Voice", mirror_and_voice), ("Ice", ice_start)):
        # Mirror is rendered once for a combined Silence+Mirror entry; Voice is a separate sequence name.
        if name == "Voice":
            continue
        group, check = if_block("Selected Primitive", 99, string=name)
        a += [comment(f"Dispatch {name} only when the selected Config entry names it:\n- Input uses Selected Primitive from the sequence lookup.\n- The otherwise path leaves State unchanged."), check]
        a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
    a += [comment("--- PHASE 5 PRIMITIVE DISPATCH END ---")]
    return a
```

**Operand shape to preserve:** `if_block(name, code, *, number=None, string=None)` — the
condition-4 form is already in use in the same file at `:614`, plain literal, no coercion:

```python
    respected_g, respected_if = if_block("Previous Respected", 4, string="true")
```

Also update the leading comment at `:645` — `"- Combined entries call only their named
primitives."` is false once combined entries are abolished.

---

### 5. The `sequences` arrays

**Only live location:** `src/PROSOCHE-Dumb.xml` **action 7**, an
`is.workflow.actions.gettext` whose `WFTextActionText` is a **plain `str`** holding the whole
Config JSON literal. No Python writes it — `grep -n "sequences" tools/*.py` returns only the
reader at `build_state_engine.py:653`.

**Current value, verbatim** (plistlib dump of action 7):

```json
"sequences": {
  "Classic":     ["Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice"],
  "BlackMirror": ["Knock", "Confession", "Ash+Confession", "Mirror", "Silence+Mirror", "Dimming+Mirror", "Exile", "Voice", "Ice"],
  "Ambient":     ["Ash", "Silence", "Dimming", "Knock", "Confession", "Exile", "Mirror", "Voice", "Ice"]
}
```

**Pattern for locating it — by content, never by index** (`docs/sequence_dispatch_check.py:95-103`):

```python
def config_literal(actions) -> dict:
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if isinstance(value, str) and '"config_version"' in value:
            return json.loads(value)
    raise AssertionError("the Config JSON literal was not found in the artifact")
```

Doc mirror to edit in the same commit: `src/CONFIG-BLOCK.md:45-49` (plus prose `:82,:84,:86,:107-109`),
and the pre-existing threshold drift at `src/CONFIG-BLOCK.md:36-38`.

---

### 6. `universal_leaving()` — the Panic Escape "deliberately removable" site

`tools/build_state_engine.py:895-914`, verbatim:

```python
def universal_leaving():
    group = uid()
    a = [comment(EXIT_MARKER + "\n\n- The session was saved before every interactive action.\n- Leaving is available before every primitive in every sequence and Circle.\n- Continue reaches exactly the selected primitive."),
         # G-04-4b, revision 1: named the active Circle and stated that this menu belongs to
         # the OPEN path, so it could no longer be mistaken for a CLOSE-path signal.
         # ...
         # "Circle Next" is already set (breadcrumb I, above) at every call site.
         menu(group, 0, prompt=text_token([("You just opened a tracked app. PROSOCHĒ is at Circle ", "Circle Next"),
                                            (".\n\nLeaving: PROSOCHĒ suggests somewhere better to go and takes you there.\n"
                                             "Continue: you go into the app, after this Circle's intervention.", None)]),
              items=["Leaving", "Continue"]), menu(group, 1, title="Leaving")]
    a += select_exit() + [menu(group, 1, title="Continue")] + primitive_dispatch() + [menu(group, 2), comment("--- PHASE 6 UNIVERSAL LEAVING END ---")]
    return a
```

**How `Leaving` is offered:** one `choosefrommenu` mode-0 with `items=["Leaving", "Continue"]`
(artifact action **520**), then `menu(group, 1, title="Leaving")` whose body is `select_exit()`,
then `menu(group, 1, title="Continue")` whose body is `primitive_dispatch()`, then `menu(group, 2)`.
**`Leaving` is a menu case, not an action** — removing it means not emitting the menu, which is
why RESEARCH §8.3 Mechanism A wraps the whole block in a numeric gate and renders
`primitive_dispatch()` a second time in the `otherwise` arm.

**Hard constraints on any edit here** (all quoted in RESEARCH §8.2, re-check before planning):
`verify_circle_zero_silence()` `tools/build_state_engine.py:1481-1490` requires **exactly one**
`["Leaving","Continue"]` menu, enclosed by the `Circle Next > 0` silent band;
`docs/router_ui_census.py:234-245` requires every OPEN-arm surface inside that band; an eleventh
`primitive_dispatch()` rendering moves `docs/environmental_restore_check.py:78` and
`docs/phase9_self_check.py:97-104`.

---

### 7. The plist round-trip edit method — the analog for every Note-body string edit

Established by quick task `260817-au7` and recorded in `docs/BUILD-NOTES.md:1324-1385` (§20)
and `.planning/quick/260817-au7-ios26-automation-onboarding/SUMMARY.md:115-129`. **No script was
left behind — the method is prose plus a verification table; the planner must re-implement it.**

`SUMMARY.md:115-129`, verbatim:

> **`WFTextTokenString`** carrying two attachments — `Import Descent` at `{4389, 1}` and
> `Import Voice` at `{4420, 1}` — **both downstream of the edited region**. The replacement
> lengthened the string 5121 → 6210 characters, moving both placeholders to 5478 and 5509.
>
> A plain string substitution in the XML would have left the range keys reading 4389/4420 and
> shipped a plist with two ranges pointing into the middle of unrelated prose — the failure
> `VARIABLES.md` records as able to **crash Shortcuts on import**. The edit was therefore made
> through a plistlib round trip that rebuilds `attachmentsByRange` from the new placeholder
> offsets in document order, with a guard asserting the old offsets matched the old keys first,
> and a second asserting the replacement text introduces no new placeholder.
>
> Licensing that approach: a **no-op** `plistlib.dumps(data, fmt=FMT_XML, sort_keys=False)` was
> confirmed byte-identical to the 2,259,398-byte source before any edit was made, so the
> resulting diff is 17 insertions / 11 deletions of real content and nothing else.

**The six steps to copy verbatim** (RESEARCH §6.3, derived from the above):

1. Prove a no-op `plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False)` is byte-identical to the source.
2. Assert the **old** `attachmentsByRange` keys equal the old `￼` offsets.
3. Apply the text replacement.
4. Rebuild `attachmentsByRange` from the **new** `￼` offsets in document order.
5. Assert the replacement text introduces no new `￼`.
6. `plutil -lint` the file; then verify offsets in **both** forks after the Sentient rebuild.

**Evidence table to reproduce** (`SUMMARY.md:156-170`) — the planner should copy its row shape
into the phase's verification block: no-op round trip byte count, `plutil -lint OK`, provenance
guard exit 0, both builders exit 0 with Dumb byte-identical, stale-string count 0, new-string
count n/n, `attachmentsByRange` keys vs recomputed offsets per fork, validator ×2, signed sizes,
dated-archive SHA equality, `plutil -lint` on both recovered plists.

---

### 8. The two rename-broken assertions

**`docs/manifest_check.py:44-48`** — verbatim; `SIGNED_BASENAMES` derives from it, and
`:130` derives the fork label as `name.rsplit("—", 1)[-1].strip()`:

```python
# The two canonical display names, from which the only two acceptable signed basenames
# follow.  DIST-04: the signed filename must equal the intended library name exactly.
DISPLAY_NAMES = [
    "PROSOCHĒ — Nine Circles — Dumb",
    "PROSOCHĒ — Nine Circles — Sentient",
]
SIGNED_BASENAMES = {f"{name}.shortcut" for name in DISPLAY_NAMES}
```

```python
        fork = name.rsplit("—", 1)[-1].strip()  # "Dumb" / "Sentient"
        for kind in KINDS:
            require(
                any(label.startswith(fork) and kind in label.lower() for label in labels),
                f"MANIFEST has no {kind!r} row for the {fork} fork",
            )
```

A Dumb→Core / Sentient→Aware rename changes `DISPLAY_NAMES` **and** requires the six row labels
in `artifacts/shortcuts/MANIFEST.md` to start with `Core` / `Aware`.

**`docs/sentient_core_check.py:9`** — verbatim, in file context (`:1-9`):

```python
#!/usr/bin/env python3
"""Structural proof that Sentient is an additive fork of Dumb."""
import plistlib
from pathlib import Path

DUMB = plistlib.loads(Path("src/PROSOCHE-Dumb.xml").read_bytes())
SENTIENT = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())
da, sa = DUMB["WFWorkflowActions"], SENTIENT["WFWorkflowActions"]
assert SENTIENT["WFWorkflowName"].endswith("Sentient")
```

Paired with `tools/build_sentient.py:181` (`root["WFWorkflowName"] = "PROSOCHĒ — Nine Circles — Sentient"`),
which is the writer. Note this check also asserts `sa[:6] + sa[8:marker] + sa[end+1:] == da` at
`:20` — any Sentient-side note-body divergence (RESEARCH §7.2 option 1) **breaks that equality**
and must be accounted for in the same commit.

**Third rename-broken assertion, not in the brief but adjacent** —
`docs/phase5_self_check.py:65-67`, which hardcodes the old primitive names and the two combined
entries and goes red the moment the sequence arrays move:

```python
    for name in ("Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice",
                 "Ash+Confession", "Silence+Mirror", "Classic", "BlackMirror", "Ambient"):
        require(name in text, f"missing sequence or primitive: {name}")
```

---

## Shared Patterns

### Failure convention
**Generator (`tools/*.py`):** `raise SystemExit(<long actionable message>)`.
**Checkers (`docs/*.py`):** `require(cond, msg)` → `raise AssertionError(msg)`, or a bare
`assert cond, msg` in the short checkers. Messages state the **consequence**, not just the fact —
model on `docs/manifest_check.py:148-153` and `tools/build_state_engine.py:2188-2194`.

### Locate by content, never by index
`config_literal()` (`docs/sequence_dispatch_check.py:95-103`) and the comment-marker
`next(i for i, x in enumerate(a) if "--- MARKER ---" in ...)` idiom
(`docs/sentient_audit_check.py:8-9`, `tools/build_state_engine.py:3092-3097`).
Applies to: the Config literal, the three Note-identity sites, the new checker's anchors.

### Never hardcode a condition code as a filter
`match_strategy(code)` (`docs/sequence_dispatch_check.py:56-72`). Resolve semantics from the
branch's own `WFCondition`. Applies to `verify_dispatch_coverage()` too.

### Any `WFTextTokenString` edit goes through the six-step round trip
§7 above. Applies to: Note body 3616/3684, the bootstrap `state.json` template (action 75),
and any Sentient-side `fix_fork_strings()`.

### Idempotence is the acceptance test for a generator change
`docs/phase5_self_check.py` and `docs/phase6_self_check.py` run the builder twice and assert
byte equality; `260817-au7` confirmed a hand edit to the XML comes back unmodified in
`git status` after a rebuild. Any plist-side edit in this phase must survive that.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `tools/build_sentient.py` — proposed `fix_fork_strings(actions)` | generator patch | plistlib round-trip on a forked artifact | `build_sentient.py` makes only three kinds of change today (`:179-189`: icon+import question, `WFWorkflowName`, audit-block insertion) and touches **no** note body, note title or `"fork"` seed. The nearest in-repo shape is `_replace_in_token` used by `fix_state_rebind()` (`tools/build_state_engine.py:3055`) — a partial analog, in the wrong file, and it collides with `docs/sentient_core_check.py:20`'s `sa[:6] + sa[8:marker] + sa[end+1:] == da` equality. Treat as new design work (RESEARCH §7.2). |
| Dante Circle-name surface (`Limbo` … `Treachery`) | user-facing copy | — | Measured zero occurrences of eight of the nine names in the artifact; no existing name surface to copy. `Limbo` ×12, all the *profile*. New surface, planner's choice of site (RESEARCH §9). |

## Metadata

**Analog search scope:** `tools/*.py` (2 files), `docs/*.py` (11 checkers), `src/PROSOCHE-Dumb.xml`
(action 7, 520, 3602/3616/3619), `src/CONFIG-BLOCK.md`, `docs/BUILD-NOTES.md` §20,
`.planning/quick/260817-au7-ios26-automation-onboarding/{PLAN,SUMMARY}.md`, `artifacts/shortcuts/MANIFEST.md`
**Files scanned:** 18
**Pattern extraction date:** 2026-08-17 (working tree at `ae0226c`)
