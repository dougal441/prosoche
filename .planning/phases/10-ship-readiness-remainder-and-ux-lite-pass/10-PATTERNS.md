# Phase 10: Ship-readiness remainder and UX-lite pass — Pattern Map

**Mapped:** 2026-08-17
**Files analyzed:** 11 (2 created, 9 modified)
**Analogs found:** 11 / 11

**Scope note:** the brightness/volume cut is **CANCELLED** (ROADMAP Phase 10, user decision
2026-08-16 reaffirmed 2026-08-17). No pattern below removes `dimming()`, `silence()`,
`restore_managed_settings()`, `device_detail()`, `set_brightness()`, `set_media_volume()`,
`clear_snapshot()`, the `settings_snapshot` subtree, `seed_settings_snapshot()`,
`verify_state_seed()` or `verify_restore_gates()`. 10-RESEARCH.md Finding 2 and Pitfalls 2/3
are superseded — ignore them. No `docs/cut_check.py` is mapped.

**Structural note the planner must internalise:** this repo has no controllers/services/
components. There are exactly four kinds of file: (1) the generator
`tools/build_state_engine.py`, which *reads and rewrites `src/PROSOCHE-Dumb.xml` in place*;
(2) the derived generator `tools/build_sentient.py`; (3) standalone assert-based checker
scripts in `docs/`; (4) hand-authored regions of the plist itself (Config literal at action
7, Control Room block at 3594–3673). Every analog below is drawn from one of those four.

---

## File Classification

| New/Modified File | Change | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|---|
| `tools/build_state_engine.py` → new `gate_control_room_shownote()` pass | add | generator patch-pass (idempotent) | transform (in-place plist mutation) | `fix_notes_filter_limit()` / `fix_shownote_key()` (`:2652`, `:2690`) | exact |
| `tools/build_state_engine.py` → `manual_emergency_restore()` | modify | generator emitter (menu) | event-driven (menu branch) | its own `Status` branch, `:1425` | exact |
| `tools/build_state_engine.py` → `manual_note_refresh()` (Setup Check display) | modify | generator emitter (read-only display) | request-response (read → gate → alert) | its own `Manual Status Requested` branch, `:1467–1475` | exact |
| `tools/build_state_engine.py` → `manual_emergency_restore()` prompt (M11) | modify | copy | — | `menu(..., prompt="Choose profile", ...)` `:1429` | exact |
| `tools/build_state_engine.py` → `universal_leaving()` copy + Circle-0 gate | modify | generator emitter (menu) | event-driven | `if_block("Genuine Open", 2, number=0)` in `open_pipeline():1105` | role-match |
| `tools/build_state_engine.py` → OPEN notification removal | modify | generator emitter | — | `notification()` call at `open_pipeline():1101–1103` (delete the 3-line block) | exact |
| `tools/build_state_engine.py` → new `verify_*` guard(s) | add | build guard | batch validation | `verify_router_shape()` (`:1340`), `verify_pending_exit_seed()` (`:1963`) | exact |
| `src/PROSOCHE-Dumb.xml` action 7 (Config JSON) — threshold rise | modify | config literal | — | the existing `thresholds` object in the same `gettext` blob | exact |
| `docs/phase5_self_check.py` | repair | test script | batch assert | `docs/phase7_self_check.py` (green, same skeleton) | exact |
| `docs/phase6_self_check.py` | repair | test script | batch assert | `docs/phase7_self_check.py` | exact |
| `docs/router_ui_census.py` | create | test script | batch assert | `docs/phase7_self_check.py` (`require()` + plistlib parse) | exact |
| `docs/manifest_check.py` | create | test script | file-I/O + assert | `docs/phase7_self_check.py` skeleton + `shasum`/`stat` from 10-RESEARCH §5b | role-match |
| `docs/sequence_dispatch_check.py` | create | test script | batch assert (record, do not fail) | `docs/state_engine_self_check.py` (`structural_check()` reads the plist without rebuilding) | role-match |
| `artifacts/shortcuts/MANIFEST.md` | modify | doc/manifest | — | its own current (correct) Dumb rows | exact |
| `.planning/REQUIREMENTS.md` (ROOM-10, SAFE-05 resolution) | modify | doc | — | existing requirement rows | exact |

---

## Pattern Assignments

### 1. New idempotent generator pass — `gate_control_room_shownote()`

**Analog:** `fix_notes_filter_limit()`, `tools/build_state_engine.py:2690–2722`
(and the sibling `fix_shownote_key():2652–2688`).

**Shape to copy** — scan-by-identifier, early-return idempotency, docstring stating the
reported symptom, the donor/device evidence, and the idempotency condition explicitly:

```python
def fix_notes_filter_limit(actions):
    """... Idempotent: a second run finds WFContentItemLimitEnabled already present and returns."""
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.filter.notes":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if "WFContentItemLimitEnabled" in parameters:
            return
        parameters["AppIntentDescriptor"] = dict(NOTES_FILTER_APP_INTENT)
        parameters["WFContentItemLimitEnabled"] = True
        parameters["WFContentItemLimitNumber"] = 1.0
        return
```

**Differences the new pass must carry:** it *inserts* actions rather than editing
parameters, so the idempotency probe is positional — "is `actions[index-1]` already a
mode-0 `conditional` with `WFCondition == 2`?" — exactly as sketched in 10-RESEARCH.md
Code Examples. Ordering in `main()`: **after** `fix_shownote_key()`, so the `shownote`
already carries `WFInput`.

**Control-flow construction must use the helpers, never hand-built dicts** (`:259–288`):

```python
group = uid()
params = {"GroupingIdentifier": group, "WFControlFlowMode": 0,
          "WFCondition": condition,
          "WFInput": {"Type": "Variable", "Variable": variable(value_name)}}
```

`if_block()` is the only sanctioned producer of a conditional input (axis 5 — variable slot
takes a bare `WFTextTokenAttachment`, the inverse of the string-envelope rule).
`verify_conditional_inputs()` (`:1666`) fails the build otherwise.

---

### 2. New menu item — `Setup Check` in `manual_emergency_restore()`

**Analog:** the `Status` item in the same function, `tools/build_state_engine.py:1417–1426`.

**Menu-list + case pattern** (order of `choices` and order of `menu(group, 1, title=...)`
cases must match exactly — CONTROL_FLOW's top real-world failure mode):

```python
choices = ["Status", "Open Control Room", "Sync My Profile", "Change Profile",
           "Change Sequence", "Toggle Voice", "Test a Circle", "Reset Today",
           "Emergency Restore"]
a = [comment(MANUAL_MARKER + "\n\n- Manual control is the only path that ..."),
     menu(group, 0, prompt="PROSOCHĒ", items=choices)]
a += [menu(group, 1, title="Status"), *number(1, "Manual Status Requested")]
a += [menu(group, 1, title="Open Control Room"), action("is.workflow.actions.nothing")]
```

**Two edits land here:**
- `"Setup Check"` appended to `choices`, plus
  `a += [menu(group, 1, title="Setup Check"), *number(1, "Manual Setup Check Requested")]`.
- the `Open Control Room` case's `action("is.workflow.actions.nothing")` becomes
  `*number(1, "Manual Show Note Requested")` (this is the flag pass 1 gates on).

**Flag-variable idiom:** `number(v, name)` (`:290`) emits
`is.workflow.actions.number` + `set_var`, so the output is already Number-typed and
`_already_numeric()` makes `normalise_numeric_operands()` (`:2458`) leave it alone. The flag
is undefined on the other branches — identical, device-proven shape to
`Manual Status Requested`.

**Prompt reframe (M11):** the same `menu(group, 0, prompt=...)` line. The literal-string
prompt form is already used at `:1429` (`prompt="Choose profile"`) and `:1435`
(`prompt="Choose sequence"`) — a plain `str` is correct for `WFMenuPrompt`; do not switch to
`text_token()` unless a variable is interpolated.

---

### 3. `Setup Check` display branch — read → numeric gate → alert

**Analog:** the cycle-14 `Status` branch in `manual_note_refresh()`,
`tools/build_state_engine.py:1467–1475`.

```python
status_g, status_if = if_block("Manual Status Requested", 2, number=0)
a += [status_if, comment("Status is read-only:\n- Displays the current snapshot directly, via an alert.\n- Never appends to or otherwise writes the Note."),
      alert("Status", text_token([("Fork: ", "Snapshot Fork"), ("\nProfile: ", "Snapshot Profile"), ...])),
      otherwise(status_g), action("is.workflow.actions.nothing"), end_if(status_g)]
```

Four rules embedded in this excerpt that `Setup Check` must copy verbatim in shape:
1. Gate is `if_block(<flag>, 2, number=0)` — numeric "> 0", never condition 100.
2. Every arm is closed: `otherwise(...)`, `action("is.workflow.actions.nothing")`, `end_if(...)`.
3. Display goes through `alert()` (`:352`) with a `text_token([...])` message —
   `WFAlertActionMessage` is a display parameter, so it needs the `WFTextTokenString`
   envelope that `text_token()` produces (axis 2).
4. **Never `appendnote`.** Read-only branches do not write the Note.

**Reading the two flat keys** — analog `read_value()` usage in the same function (`:1462`)
and in `open_pipeline():961–963`:

```python
a += read_value("last_open_at", variable("State"), "Last Open")
a += read_value("last_close_at", variable("State"), "Last Close")
```

Both keys are **flat**, so a read cannot hard-error on a legacy `state.json` (CLAUDE.md
verified runtime semantics). Gate each with `if_block(name, 2, number=0)`. Do **not** use
`get_value()` — that is reserved for `COMPOUND_STATE_KEYS`.

---

### 4. Circle 0 silent band

**Analog for the gate:** the genuine-open gate in `open_pipeline():1105`:

```python
genuine_group, genuine = if_block("Genuine Open", 2, number=0)
a += [genuine]
...
a += save_state() + universal_leaving() + [end_if(genuine_group), end_if(cooldown_group)]
```

The silent band is the same shape one level in: state accumulation and `save_state()` stay
outside the gate; `universal_leaving()` (which itself contains the menu *and*
`primitive_dispatch()`) moves inside a `if_block("Circle Next", 2, number=0)`.

**Analog for the threshold rise:** the Config literal at `src/PROSOCHE-Dumb.xml` action 7 —
a plain-string `WFTextActionText` on `is.workflow.actions.gettext`, consumed by
`detect.dictionary` at action 8 and read at runtime via `config(key, name)` (`:950`):

```json
"thresholds": {
  "Paradise": [1, 4, 7, 10, 13, 16, 19, 22, 25],
  "Limbo":    [1, 3, 5, 7, 9, 11, 14, 17, 20],
  "Inferno":  [1, 2, 4, 6, 8, 10, 12, 14, 16]
}
```

Constraints carried by `src/CONFIG-BLOCK.md:101–103, 122`: arrays must stay strictly
ascending, must stay 9 entries, and index 9 must stay below `heat.cap + gravity.cap` (35) or
Circle 9 becomes unreachable. Shifting every entry up by the band width preserves band
widths and only delays entry — which is what the ROADMAP asks. Note the Circle scan
initialises `number(1, "Circle Next")` (`:1084`) and only ever *raises* it, so reaching
Circle 0 additionally requires changing that floor to 0.

**Also:** the scan's ascending-array invariant is asserted arithmetically in
`docs/state_engine_self_check.py`'s `THRESHOLDS` table (lines 8–24) — that table is a
duplicate of the Config literal and **must be updated in the same commit** or
`state_engine_self_check.py` goes red.

---

### 5. Remove the OPEN notification / reword `Leaving / Continue`

**Notification removal analog** — `open_pipeline():1099–1103`, delete the block whole
(comment + call), per CLAUDE.md "fix whole classes":

```python
# Permanent, unconditional OPEN confirmation, fired on every genuine open once
# Circle is written and any pending exit has completed (G-04-4b). ...
a += [notification("PROSOCHĒ", text_token([("Circle ", "Circle Next"),
                                            (" · pressure ", "Pressure Next"),
                                            (" · heat ", "Heat Final")]))]
```

**Copy reframe analog** — `universal_leaving():895–905`, the interpolated-prompt form:

```python
menu(group, 0, prompt=text_token([("Circle ", "Circle Next"),
                                  (" opened. Leave now, or continue?", None)]),
     items=["Leaving", "Continue"]), menu(group, 1, title="Leaving")
```

`text_token([(literal, varname|None), ...])` is the only sanctioned way to build an
interpolated display string — it computes `attachmentsByRange` offsets itself, which is why
hand-editing the string is forbidden. The `items=` labels are matched by
`menu(group, 1, title=...)` **by exact string**; if the item labels are reworded, both the
`items` list and every matching case title change together.

---

### 6. New build guard (`verify_*`) inside the generator

**Analog:** `verify_router_shape()` (`:1340–1357`) and `verify_pending_exit_seed()`
(`:1963`). Signature is `def verify_x(actions):` raising on violation, registered in
`main()` alongside the existing 15 passes.

**Hard constraint from the ROADMAP:** a sequence/dispatch checker must **record** the
known Circle-8 `"Voice"` orphan rather than fail on it, and must **not** hard-code condition
99 / substring matching as an invariant (BD-06 moves dispatch to condition-4 exact
matching). So this one belongs in `docs/sequence_dispatch_check.py` as a *reporting*
script, not as a build-failing `verify_*`.

---

### 7. Checker scripts in `docs/`

**Analog for all four (two repairs, two/three new):** `docs/phase7_self_check.py` — 47
lines, the smallest complete instance of the house pattern.

```python
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"

def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)

def main() -> None:
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "builder is not idempotent")
    actions = plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"]
    params = [item.get("WFWorkflowActionParameters", {}) for item in actions]
    ...
    print("phase7 self-check: passed")

if __name__ == "__main__":
    main()
```

House conventions visible here and to be copied: `from __future__ import annotations`;
`ROOT = parents[1]`; a local `require()` (not bare `assert`) for messages; the
double-build idempotency check; `plistlib.loads(...)["WFWorkflowActions"]`; a single
`print("<name>: passed")` at the end; `if __name__ == "__main__": main()`.

**For a read-only script that must NOT rebuild** (`router_ui_census.py`,
`sequence_dispatch_check.py`, `manifest_check.py`), copy
`docs/state_engine_self_check.py:41–50` instead — it opens the plist directly with no
`subprocess` rebuild:

```python
def structural_check():
    from pathlib import Path
    import plistlib
    actions = plistlib.loads(Path("src/PROSOCHE-Dumb.xml").read_bytes())["WFWorkflowActions"]
    ids = [action["WFWorkflowActionIdentifier"] for action in actions]
    comments = [action.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for action in actions]
```

**Menu-list assertion pattern** (`phase7_self_check.py:16, 31–33`) — the exact idiom
`router_ui_census.py` and the ROOM-10 check should reuse, and the line that **must** be
updated when `Setup Check` is added or `phase7_self_check.py` goes red:

```python
MENU = ["Status", "Open Control Room", ..., "Emergency Restore"]
menus = [value["WFMenuItems"] for value in params if value.get("WFMenuItems") == MENU]
require(len(menus) == 1, "manual menu is not the exact nine required items")
```

**Repair targets, characterised:**

| Script | Failure at HEAD | Offending line | Repair shape |
|---|---|---|---|
| `docs/phase5_self_check.py` | `StopIteration` | the condition-100 `Input Key` absence-gate lookup (comment at `:93` already records the gate "was removed") | Delete the lookup and its dependent assertions; replace with an assertion of the DEV-02 router shape (`Input Key` tests are exactly `[(4,"OPEN"), (4,"CLOSE")]`) mirroring `verify_router_shape()` (`build_state_engine.py:1340`) |
| `docs/phase6_self_check.py` | `AssertionError: Open App route shape` | `:68` — `require("WFSelectedApp" in params and "WFAppName" in params, ...)` | Drop `WFAppName`; `normalize_open_apps()` (`:2640`) deliberately re-emits only `WFAppIdentifier` + `WFSelectedApp` |
| `docs/sentient_core_check.py` | `AssertionError` | `assert sa[:6] + sa[8:marker] + sa[end+1:] == da` — Sentient is stale at `2026-08-14k` | **Leave red, documented.** Re-forking is SEED-005, out of phase scope |

**`manifest_check.py` data source** — the commands already canonical in 10-RESEARCH §5b:
`shasum -a 256 <file>` and `stat -f%z <file>`, compared against the parsed MANIFEST rows.
The three **Dumb** rows are currently correct; only the three **Sentient** rows are wrong.

---

### 8. `tools/build_sentient.py`

**No change required this phase.** Its 10 `verify_*` imports (`:12–25`) stay valid because
the cut is cancelled — `verify_restore_gates` and `verify_state_seed` are not being deleted.
The only obligation is the existing smoke test:
`python3 -c "import sys; sys.path.insert(0,'tools'); import build_sentient"`.

---

## Shared Patterns

### The seven parameter-defect axes (applies to every emitted action)
**Source:** `.claude/CLAUDE.md` § Conventions; enforced by `verify_parameter_keys()`
(`:2623`), `verify_string_envelopes()` (`:2552`), `verify_required_pickers()` (`:1639`),
`verify_conditional_inputs()` (`:1666`), `verify_numeric_operands()` (`:2479`).
**Apply to:** every new action in `manual_emergency_restore()`, `manual_note_refresh()`,
`universal_leaving()`, and `gate_control_room_shownote()`.

Rules 2 and 5 are **inverses** and are the single most likely new-code defect:

```python
# Rule 2/3 — a STRING/AttributedString parameter needs a WFTextTokenString:
alert("Status", text_token([("Fork: ", "Snapshot Fork")]))

# Rule 5 — a VARIABLE SLOT needs a bare WFTextTokenAttachment:
"WFInput": {"Type": "Variable", "Variable": variable(value_name)}
```

### Numeric gating (never existence gating)
**Source:** `if_block(name, 2, number=0)` — used at `:1443` (`Manual Voice`), `:1467`
(`Manual Status Requested`), `:1463` (`Manual Refresh Requested`), `restore_managed_settings():463,470`.
**Apply to:** every new flag and every `Setup Check` read.
A dotted read with a missing segment is a **hard error**, and a read-then-`has any value`
gate is unimplementable (CLAUDE.md runtime semantics). Condition 100/101 on new state is the
axis-7 trap `verify_sentinel_gates()` (`:2142`) exists to prevent.

### Never hand-edit `src/PROSOCHE-Dumb.xml` for generated regions
**Source:** `comment_index()` (`:1194`), `replace_marker_block()` (`:1202`),
`insert_or_replace_after()` (`:1238`), `flow_index()` (`:1247`).
**Apply to:** all Strand B code changes. Index arithmetic over `WFWorkflowActions` is
forbidden — every index in 10-RESEARCH.md shifts on the first rebuild. The only sanctioned
hand-edit is the **Config literal at action 7** (hand-authored, not generated, and outside
`main()`'s `pinned` byte-identity check on actions 0–4).

### Authored comment before every control-flow start
**Source:** `main():2841–2851` auto-inserts a generic `"Control-flow check: …"` comment
before any control-flow start lacking one.
**Apply to:** every new `if_block()`/`menu()` pair. Author the intent comment yourself so the
generic filler is not used and decrypt-diffs stay readable.

### Verify command line
**Source:** `docs/BUILD-NOTES.md` §13 DEV-01, re-measured in 10-RESEARCH §5a.
**Apply to:** every `<verify>` in every plan.

```bash
validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all
```

`--target-platform ios` (as written in CLAUDE.md) rejects the file wholesale, including
`is.workflow.actions.conditional`. Cite DEV-01 so it does not read as drift. Do not use
`timeout` — it is not installed.

### Self-check baseline is 3 green / 3 red
**Source:** 10-RESEARCH §5c.
**Apply to:** any `<verify>` that says "self-checks pass". Green today:
`state_engine_self_check.py`, `phase7_self_check.py`, `sentient_audit_check.py`. This phase
repairs `phase5` and `phase6`; `sentient_core_check.py` stays red with a recorded reason.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `docs/manifest_check.py` | test script | file-I/O | The `require()`/plistlib skeleton is an exact analog, but nothing in `docs/` currently shells out to `shasum`/`stat` or parses a markdown table. Take the table-parsing and hashing logic from 10-RESEARCH §5b step 7; keep the script skeleton from `phase7_self_check.py`. |
| Circle-0 "silent band" gate | generator emitter | event-driven | No existing gate suppresses *all* user-facing surfaces while still persisting state. The `Genuine Open` gate (`:1105`) is the closest structural analog (state saved outside, interaction inside) but its semantics differ. Compose from `if_block()` + the existing `universal_leaving()` call site rather than copying a whole block. |

---

## Metadata

**Analog search scope:** `tools/build_state_engine.py` (2,883 lines, targeted reads of
`:259–405`, `:895–908`, `:954–1110`, `:1415–1482`, `:2652–2724`), `tools/build_sentient.py`,
`docs/*.py` (all 7), `src/PROSOCHE-Dumb.xml` (actions 6–8 via plistlib),
`src/CONFIG-BLOCK.md`, `.planning/ROADMAP.md` Phase 10, `10-RESEARCH.md` (full).
**Files scanned:** 12
**Pattern extraction date:** 2026-08-17
