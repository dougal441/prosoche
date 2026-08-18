# Phase 14: Ash as real Color Filters grayscale - Pattern Map

**Mapped:** 2026-08-18
**Files analyzed:** 8 modified (0 created in `tools/`; 1 created in `docs/`)
**Analogs found:** 7 / 8

**Read this first.** This is not a conventional app codebase. There are no controllers, services
or components. The tiers are: **generator** (`tools/build_state_engine.py`, `tools/build_sentient.py`
— idempotent Python that emits Shortcuts plist XML), **build guard** (`verify_*` functions *inside*
the generator, which abort the build), **artifact checker** (standalone `docs/*.py` scripts that
prove the shipped XML from disk without trusting its producer), **preserved literal** (text living
inside the artifact, edited only through `tools/plist_text_edit.py`), and **record** (`docs/*.md`,
`src/CONFIG-BLOCK.md`).

The controlling insight for every assignment below: **this phase adds the third member of an
existing two-member family.** Brightness and volume already run end to end. Every analog is the
brightness or volume equivalent of the thing being added. The risk in this codebase is never the
new action — it is a *new mechanism*. Join the existing machine.

**All references anchor on symbol names. No line numbers appear in this document by design**
(`.claude/CLAUDE.md`: "Anchor on the symbol, not the line: these shift on every edit").

---

## File Classification

| File to modify | Role | Data flow | Closest analog | Match quality |
|---|---|---|---|---|
| `tools/build_state_engine.py` → new `set_color_filters()` emitter | action emitter | transform (Python → plist dict) | `set_brightness()` / `set_media_volume()` in the same file | **exact** — same family, adjacent definitions |
| `tools/build_state_engine.py` → `ash()` rewrite | primitive emitter | request-response (Circle → device) | `dimming()` / `silence()` in the same file | **exact** |
| `tools/build_state_engine.py` → `restore_managed_settings()` third block | restore emitter | CRUD (read snapshot → write device → clear leaf) | the volume block *inside the same function* | **exact — copy in structure, verbatim** |
| `tools/build_state_engine.py` → `seed_settings_snapshot()` third recogniser | bootstrap seeder | transform (in-place text edit of a preserved literal) | the `SNAPSHOT_SEEDED_D02` `while` pass in the same function | **exact** |
| `tools/build_state_engine.py` → 4 build guards + 2 constants | build guard | batch (walk the action list, raise `SystemExit`) | `ENVIRONMENTAL_IDENTIFIERS`, `verify_capture_persistence()`, `verify_parameter_keys()`, `verify_environmental_reachability()` — the existing bodies | **exact (widen, do not rewrite)** |
| `docs/phase5_self_check.py` → invert Color Filters assertion | artifact checker | batch | the assertion itself, plus the neighbouring `require()` idioms in the same `main()` | **exact** |
| `docs/environmental_restore_check.py` → `EXPECTED_SITES` + seed loop | artifact checker | batch | the brightness/volume rows in the same tables | **exact** |
| `src/PROSOCHE-Dumb.xml` Control Room Note disclosure + `src/CONFIG-BLOCK.md` | preserved literal + mirror | file-I/O (guarded plist round trip) | `tools/plist_text_edit.py`'s documented six-step method; `src/CONFIG-BLOCK.md`'s 2026-08-18 D-01 revision entry | **role-match** |
| **NEW** `docs/gate_a_residue_check.py` (D-14-01) | artifact checker (subprocess-parsing) | request-response (run external validator, parse stdout) | **none — see `## No Analog Found`** | **partial** |

---

## Pattern Assignments

### `set_color_filters()` — the new emitter (action emitter, transform)

**Analog:** `set_brightness()` / `set_media_volume()`, `tools/build_state_engine.py`.
Define the new function immediately beside them; that adjacency is what makes the family
legible to the next reader.

```python
# Source: tools/build_state_engine.py, set_brightness() / set_media_volume() — the exact shape
def set_brightness(source):
    return action("is.workflow.actions.setbrightness", WFBrightness=source,
                  ShowWhenRun=False)


def set_media_volume(source):
    return action("is.workflow.actions.setvolume", WFVolume=source,
                  WFVolumeSetting="Media", ShowWhenRun=False)
```

**What differs, and why the difference is load-bearing:**
- Both analogs take a `source` **variable**. The new emitter takes a **literal** `bool` — the
  donors emit a bare `<integer>`. Do not accept a variable; a variable-fed `state` would
  reintroduce axis 6 (coercion) for no benefit (RESEARCH, nine-axes table, axis 5).
- Both analogs emit `ShowWhenRun=False`. **The AX intent must not.** No donor carries it; it is
  a macOS catalog row parameter only. Copying it would be a fabricated shape.
- `action()`'s contract (same file) is plain kwargs into `WFWorkflowActionParameters`, and
  `plistlib.dumps` renders a Python `int` as `<integer>` — which is exactly the donor shape:

```python
# Source: tools/build_state_engine.py, action() — the whole helper
def action(identifier: str, **parameters):
    return {"WFWorkflowActionIdentifier": identifier,
            "WFWorkflowActionParameters": parameters}
```

Target shape (RESEARCH §Code Examples, donor-verbatim):

```python
COLOR_FILTERS = "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent"

def set_color_filters(on: bool):
    """Donor-verbatim. `operation` is the elided default and is never written."""
    return action(COLOR_FILTERS, state=1 if on else 0)
```

---

### `ash()` — the primitive (primitive emitter, request-response)

**Analogs, in priority order:** `dimming()` for the gate/persist/apply skeleton; `mirror_and_voice()`
for the numeric-boolean Config read; `ash()` itself for the fallback arm that must survive.

**Pattern A — the outstanding-marker gate is the LEAF, numerically** (phase 11 plan 11-08's
correction; the single most important shape to copy):

```python
# Source: tools/build_state_engine.py, dimming()
a += read_value("settings_snapshot.brightness.original_value", variable("State"),
                "Outstanding Brightness Original")
original_g, original_if = if_block("Outstanding Brightness Original", 2, number=0)
a += [original_if, action("is.workflow.actions.nothing"), otherwise(original_g)]
#     ^ TRUE arm = "a capture is already outstanding, do nothing"
#       the work goes in the OTHERWISE arm of a NUMERIC gate, which can genuinely read false
```

Never a condition-100 gate over the `settings_snapshot.color_filters` **container** with the apply
in the otherwise arm: `clear_snapshot()` makes the container a permanent invariant, so that gate
is permanently TRUE and the apply is dead code (44 unreachable actions per fork last time).

**Pattern B — persist the ownership marker BEFORE the device changes**, and only on the arm
that applies:

```python
# Source: tools/build_state_engine.py, dimming() — the applying arm, in order
a += [capture_if, set_value("settings_snapshot.brightness.original_value", variable("Captured Brightness"))]
...
# PHASE 16 (16-01): persist BEFORE the apply, and only on the arm that applies.
a += save_state()
a += [set_brightness(variable("Dim Target")), end_if(already_dim_g), ...]
```

`save_state()` and `set_value()` both take their **default** dictionary `State`. Naming
`"Reloaded State"` here persists a dictionary that never received the capture — that is
defect T-16-04 itself (`dimming()` docstring). For grayscale there is no "already grayscale"
detection path (no read-back), so the applying arm is the only arm and there is no
`device_detail()` capture step — the written value is a literal `1` ownership marker via
`number()`/`set_value()`, not a device reading.

**Pattern C — the numeric-boolean Config read for `safety.ash_managed_color_filters`:**

```python
# Source: tools/build_state_engine.py, mirror_and_voice() — the in-repo precedent
a += read_value("voice_enabled", variable("State"), "Voice Enabled")
voice_g, voice_if = if_block("Voice Enabled", 2, number=0)
```

The one-line `config()` helper is the `Config`-sourced form of the same read:

```python
# Source: tools/build_state_engine.py, config() — the whole helper
def config(key: str, name: str):
    return read_value(key, variable("Config"), name)
```

So: `a += config("safety.ash_managed_color_filters", "Ash Managed Filters")` then
`if_block("Ash Managed Filters", 2, number=0)`. Never a string compare against `"true"` —
`safety.*` booleans read back numeric (`src/CONFIG-BLOCK.md` coercion hazard A4). The read is
gettext-fed, so `normalise_numeric_operands()` attaches the coercion automatically; do not
hand-write a `WFCoercionVariableAggrandizement`.

**Pattern D — the fallback arm, preserved verbatim in intent:**

```python
# Source: tools/build_state_engine.py, ash() as it ships today
alert("Black and White", "One breath away from the screen before you go on.")
```

**Pattern E — the emitted Shortcuts comment.** It ships 11× per fork and currently asserts
*"It changes no accessibility setting. Color Filters is deliberately excluded because the iOS
action is not validator-supported."* — false the moment this lands. The correction precedent is
`dimming()`'s 16-03 comment rewrite:

```python
# Source: tools/build_state_engine.py, dimming() — the comment-correction precedent
# The bullet now states the PROPERTY the build actually guarantees -- capture-and-restore --
# rather than a softer limit ...
# The FIRST line is the stable anchor: comment_index() locates comments by prefix and
# 16-03's verify anchors on it.  Do not edit it.
a = [comment("""Dimming is reversible or message-only:
- Capture Current Brightness once when no snapshot exists.
- Do not brighten an already dim screen; the captured original is saved before any change and is always restored.
- Keep an existing unrestored snapshot unchanged.""")]
```

Keep `ash()`'s comment first line (`Black and White is …`) stable; rewrite the bullets to state
the property the build guarantees, not a per-arm outcome.

---

### `restore_managed_settings()` — the third block (restore emitter, CRUD)

**Analog:** the **volume block inside the same function**. Copy it in structure, verbatim; the
brightness block is the identical shape one earlier.

```python
# Source: tools/build_state_engine.py, restore_managed_settings() — the per-group template
a += read_value("settings_snapshot.volume", variable(dictionary_name), "Restore Volume Snapshot")
snapshot_g, snapshot_if = if_block("Restore Volume Snapshot", 100)
a += [snapshot_if] + read_value("settings_snapshot.volume.original_value",
                                variable(dictionary_name), "Restore Volume")
volume_g, volume_if = if_block("Restore Volume", 2, number=0)
a += [volume_if, set_media_volume(variable("Restore Volume")), clear_snapshot("volume", dictionary_name),
      otherwise(volume_g), action("is.workflow.actions.nothing"), end_if(volume_g),
      otherwise(snapshot_g), action("is.workflow.actions.nothing"), end_if(snapshot_g)]
```

Rules carried by this excerpt:
- The **condition-100 container gate is correct here and only here** — the restore side puts its
  work in the TRUE arm, so a permanently-true container gate is harmless.
  `verify_environmental_reachability()` tests the ARM, not the gate. Do not "simplify" it away.
- `dictionary_name` must be threaded through unchanged into both the reads and `clear_snapshot()`
  (T-16-04, load-bearing).
- Clear via `clear_snapshot("color_filters", dictionary_name)` — never
  `set_value("settings_snapshot.color_filters", ...)`. `clear_snapshot()`'s docstring records the
  cycle-10 finding: replacing a container with a string hard-errors the next dotted read one run
  later.
- The grayscale write differs from both analogs in one way: its operand is the **literal**
  `set_color_filters(False)`, not `variable("Restore …")`. The leaf read is still needed — it is
  what decides *whether* to restore.

**Four call sites, reached for free** (measured in `tools/build_state_engine.py`):
`close_pipeline()` → `restore_managed_settings("Reloaded State")`; and three
`restore_managed_settings("State")` calls in `live_ice_redirect()`, `ice_expiry()` and
`manual_emergency_restore()`. Adding the block reaches all four at once — do **not** hand-place
grayscale restores.

---

### `seed_settings_snapshot()` — the third recogniser (bootstrap seeder, transform)

**Analog:** the `SNAPSHOT_SEEDED_D02` pass inside the same function. RESEARCH Pitfall 1 is the
governing trap: adding to `SNAPSHOT_SEED` alone changes **nothing** in the artifact, because
`main()` re-parses its own previous output and the seeder returns early on an already-seeded tree.

```python
# Source: tools/build_state_engine.py, seed_settings_snapshot() — the whole body
_, inner = _state_template(actions)
current = ", ".join(f'"{leaf}": "{CLEARED_SENTINEL}"' for leaf in SNAPSHOT_SEED["brightness"])
while SNAPSHOT_SEEDED_EMPTY in inner["string"]:
    _replace_in_token(inner, SNAPSHOT_SEEDED_EMPTY, current)
while SNAPSHOT_SEEDED_D02 in inner["string"]:
    # A pre-D-02 tree ... Without this pass the removal would never reach the artifact at all:
    # the template is already seeded, so the SNAPSHOT_EMPTY branch below returns early.
    _replace_in_token(inner, SNAPSHOT_SEEDED_D02, current)
if SNAPSHOT_EMPTY not in inner["string"]:
    return  # already seeded; verify_state_seed() proves it is the right shape
line = next(text for text in inner["string"].splitlines() if SNAPSHOT_EMPTY in text)
indent = line[:len(line) - len(line.lstrip())]
_replace_in_token(inner, SNAPSHOT_EMPTY, _snapshot_seed_text(indent))
```

The new pass must:
- Be a `while … in inner["string"]` loop using `_replace_in_token()` (**never** a raw string
  replace) — the docstring states why: the template carries four attachments, one sits *after*
  the `settings_snapshot` line, and a stale offset can crash Shortcuts on import.
- Have its recogniser literal **derived from existing constants, not hand-typed** — the
  `SNAPSHOT_SEEDED_D02` definition is the derivation idiom:

```python
# Source: tools/build_state_engine.py
SNAPSHOT_SEEDED_D02 = ", ".join(
    f'"{leaf}": "{CLEARED_SENTINEL}"'
    for leaf in ("original_value",) + D02_REMOVED_SNAPSHOT_LEAVES)
```

- Recognise the **current two-group seeded shape** and rewrite it to the three-group shape. The
  seed constant itself gains a row alongside the two that exist:

```python
# Source: tools/build_state_engine.py
SNAPSHOT_SEED = {
    "brightness": ("original_value",),
    "volume": ("original_value",),
}
SNAPSHOT_EMPTY = '"settings_snapshot": {},'
```

Read the long comment block immediately above `SNAPSHOT_SEEDED_EMPTY` before writing the pass —
it records the full D-02 reasoning for exactly this move.

`verify_state_seed()` builds its `wanted` set *from* `SNAPSHOT_SEED`, so the constant and the
artifact must agree or the build fails — that failure is the symptom of skipping the recogniser.

---

### The four build guards + two constants (build guard, batch)

**Analog: the existing bodies. Widen them; do not rewrite them.**

**1. `ENVIRONMENTAL_IDENTIFIERS` — add the AX identifier.** Without it, a grayscale apply buried
in a dead arm ships silently.

```python
# Source: tools/build_state_engine.py
ENVIRONMENTAL_IDENTIFIERS = frozenset({
    "is.workflow.actions.setbrightness",
    "is.workflow.actions.setvolume",
    "is.workflow.actions.getdevicedetails",
})
```

`verify_environmental_reachability()` needs no other change — its walk is
`if identifier not in ENVIRONMENTAL_IDENTIFIERS: continue`, so membership is the whole opt-in.

**2. `verify_capture_persistence()` — the group derivation must become a mapping.** Today the
apply side matches `identifier in {setbrightness, setvolume}` and derives the group with a
two-way `identifier.endswith("setbrightness")` test, which would mislabel any third identifier as
`"volume"`. The **capture** side is already identifier-agnostic and needs nothing:

```python
# Source: tools/build_state_engine.py, verify_capture_persistence() — the capture side, unchanged
if identifier == "is.workflow.actions.setvalueforkey":
    key = parameters.get("WFDictionaryKey")
    if isinstance(key, str) and key.startswith(f"{SNAPSHOT_ROOT}.") \
            and key.endswith(".original_value"):
        target = (parameters.get("WFDictionary") or {}).get("Value", {})
        dictionary = target.get("VariableName")
        if isinstance(dictionary, str):
            pending[(key.split(".")[1], dictionary)] = enclosing
```

Note the bookkeeping key is `(<group>, <dictionary>)` — the group comes from the *state key*, so
introducing `settings_snapshot.color_filters.original_value` produces the group `"color_filters"`
for free. Only the apply-side identifier→group derivation needs the mapping.

**3. `verify_parameter_keys()` — add a `VERIFIED_PARAMETER_KEYS` entry.** The guard `continue`s on
any identifier absent from the mapping, so axis-1 protection is *opt-in*:

```python
# Source: tools/build_state_engine.py, verify_parameter_keys() — the skip that must be closed
allowed = VERIFIED_PARAMETER_KEYS.get(item.get("WFWorkflowActionIdentifier"))
if allowed is None:
    continue
unknown = set(item.get("WFWorkflowActionParameters", {})) - allowed - STRUCTURAL_KEYS
```

Add `COLOR_FILTERS: {"state"}`. `UUID` is already covered by
`STRUCTURAL_KEYS = {"UUID", "GroupingIdentifier", "WFControlFlowMode", "CustomOutputName"}`.
Follow the commenting convention of the `shownote` / `filter.notes` entries in that dict: a short
provenance note naming the donor above the entry.

**4. `verify_restore_gates()` — state explicitly that it contributes nothing.** Its operand is
read from `WFBrightness`/`WFVolume`; grayscale's operand is a literal, so its
`continue  # a literal target is not a state-derived write` branch applies. Record that in the
plan rather than assuming coverage.

**5. `COMPOUND_STATE_KEYS` — do NOT add `color_filters`.** The marker is a scalar headed for a
numeric comparison, which is `read_value()`'s correct case (axis 9).

**6. `tools/build_sentient.py`** — imports the guards by name from `build_state_engine`
(`verify_capture_persistence`, `verify_environmental_reachability`, `verify_parameter_keys`,
`verify_state_seed` are all already in the import list). No change unless a *new* guard symbol is
added; if one is, it must be added to that import list **and** to
`docs/environmental_restore_check.py`'s `REQUIRED_SYMBOLS`.

---

### `docs/phase5_self_check.py` — invert the assertion (artifact checker, batch)

**Analog:** the assertion itself, and the `require()` idiom throughout its `main()`.

```python
# Source: docs/phase5_self_check.py — the line that asserts the OPPOSITE of what ships
require("AXToggleColorFiltersIntent" not in text and "UAToggleColorFiltersIntent" not in text,
        "unsupported Color Filters action was emitted")
```

Invert **asymmetrically**: assert the `AX*` identifier **is** present with an expected count, and
that `UA*` is **still absent**. The second half keeps its teeth — it is the guard against a future
"fix" that swaps in the macOS twin to satisfy gate A. Do not delete the line.

The neighbouring loop is the count/presence idiom to follow, and its comment block is the
precedent for *how to document a deliberate inversion* (16-04 removed two keys from this exact
tuple and explained why in place):

```python
# Source: docs/phase5_self_check.py — the state-safety-key loop, immediately above
for key in ("settings_snapshot.brightness.original_value", "settings_snapshot.volume.original_value",
            "cooldown_until"):
    require(key in text, f"missing state safety key: {key}")
```

Add `settings_snapshot.color_filters.original_value` to that tuple in the same edit.

---

### `docs/environmental_restore_check.py` — three additive edits (artifact checker, batch)

**Analog:** the brightness/volume rows in its own tables.

```python
# Source: docs/environmental_restore_check.py
EXPECTED_SITES = {SET_BRIGHTNESS: 15, SET_VOLUME: 15, DEVICE_DETAILS: 22}
ALLOWED_DEVICE_DETAILS = {"Current Brightness", "Current Volume"}
```

```python
# Source: docs/environmental_restore_check.py, artifact_check() — the bootstrap-seed loop
for group in ("brightness", "volume"):
    leaves = snapshot.get(group)
    require(isinstance(leaves, dict) and "original_value" in leaves,
            f"settings_snapshot.{group}.original_value is missing from the bootstrap "
            "seed, so a restore-side dotted read can hard-error on a fresh install")
```

Edits:
- `EXPECTED_SITES` gains a `COLOR_FILTERS: 15` row (11 apply + 4 restore — RESEARCH assumption A3;
  **re-measure against the built artifact, do not transcribe**).
- The seed loop gains `"color_filters"`.
- `REQUIRED_SYMBOLS` gains `set_color_filters` (and any new `verify_*` symbol —
  `CALLED_GUARDS = tuple(name for name in REQUIRED_SYMBOLS if name.startswith("verify_"))`, so the
  call-site check follows automatically).

**The three existing numbers must move by zero.** The file's own comment says why:
*"if they HAD moved, that would have been a finding to investigate rather than a table to update."*
`ALLOWED_DEVICE_DETAILS` is untouched — grayscale reads no device property.

---

### The preserved literals (preserved literal, file-I/O)

**Analog:** `tools/plist_text_edit.py`'s documented six-step guarded round trip. The Control Room
Note disclosure copy lives **inside** `src/PROSOCHE-Dumb.xml` as a `WFTextTokenString`, not as a
generator constant.

```python
# Source: tools/plist_text_edit.py, module docstring — the method, in order
#   1. assert_noop_roundtrip()  -- plistlib.dumps(data, fmt=FMT_XML, sort_keys=False) is
#                                  byte-identical to the source
#   2. assert_offsets_match()   -- OLD attachmentsByRange keys equal OLD placeholder offsets
#   3. replace_in_token()       -- apply the text replacement
#   4. replace_in_token()       -- rebuild attachmentsByRange from NEW offsets, document order
#   5. replace_in_token()       -- assert the replacement introduces no new placeholder
#   6. plutil -lint, then re-verify offsets in BOTH forks after the Sentient rebuild
```

Entry points: `from plist_text_edit import find_action, replace_in_token` — exactly as
`tools/build_sentient.py` already imports them. `docs/note_identity_check.py` is the standing
assertion afterwards (`MINIMUM_TOKEN_STRINGS` is a floor; additive prose cannot breach it).

**`src/CONFIG-BLOCK.md`** — two independent defects, and both halves of each must be corrected:
- The `BD-01-R` note asserts Ash *is already* a real Color Filters change **and** names the wrong
  `UA*` identifier with `operation = turn`.
- The `## Field reference` table has rows for `safety.brightness_floor`, `safety.dim_target` and
  `safety.allow_volume_increase` but **no row** for `safety.ash_managed_color_filters`.

The correction precedent is the file's own **2026-08-18 D-01 revision entry**, which is the model
for both the edit and its changelog line: it corrected *every asserting cell* (purpose, cited
authority, constraint) rather than only the value, kept the superseded §21 citation with a
supersession pointer rather than deleting it, and noted that the fenced block is
*"the transcription source, not a description of one"* — i.e. the live literal in
`src/PROSOCHE-Dumb.xml` is what ships and this file is the mirror. Update both in one commit.

---

## Shared Patterns

### The numeric `> 0` gate — the only sentinel-and-empty-safe test
**Source:** `restore_managed_settings()` docstring, `tools/build_state_engine.py`
**Apply to:** every gate this phase writes — the outstanding-marker gate, the Config flag gate,
the restore leaf gate.

```
"null" -> WFNumberContentItem -> > 0  ->  FALSE, no error   (Donor 6.1 test 2)
""     -> WFNumberContentItem -> > 0  ->  FALSE, no error   (Donor 6 action 8)
```

Condition code 5 (`is not "null"`) reads **TRUE for an empty value** and is rejected. Condition
100 (existence) is licensed **only** on the `settings_snapshot.<group>` container on the restore
side, where the work sits in the TRUE arm. Never condition 100 over a container with work in the
otherwise arm.

### Container is a permanent invariant; only leaves are written and cleared
**Source:** `clear_snapshot()` docstring
**Apply to:** the seeder, the marker write, and the restore clear.
Seed `settings_snapshot.color_filters` at bootstrap and never overwrite it; write and clear only
`.original_value`. Replacing the container with a string hard-errors the next dotted read one run
later — cycle-10 finding 5. Do **not** introduce a `changed_by`-style leaf;
`verify_no_removed_snapshot_leaf_reads()` exists to keep D-02's removal safe.

### Guard docstrings state the CONSEQUENCE and the correct response
**Source:** `verify_environmental_reachability()`, `verify_capture_persistence()`
Every guard in this codebase ends with an *"IF THIS FIRES, a future reader should conclude …"*
paragraph naming the user-visible failure and the correct fix — explicitly *"never to relax the
guard or exempt the site."* Any new or widened guard must carry the same, and any deliberate
inversion (`docs/phase5_self_check.py`) must carry an in-place comment explaining why, following
the 16-04 removal note already in that file.

### Failure convention
**Source:** the `verify_*` family and `tools/plist_text_edit.py`
Build guards raise `SystemExit` with a message naming the consequence. `docs/*.py` checkers use a
local `require(value, message) -> None` raising `AssertionError`, resolve
`ROOT = Path(__file__).resolve().parents[1]`, and end with `print("<name>: passed")` in `main()`
under `if __name__ == "__main__":`.

---

## No Analog Found

| File | Role | Data flow | Reason |
|---|---|---|---|
| **NEW** `docs/gate_a_residue_check.py` (D-14-01 item 2) | artifact checker | request-response — run an external command, parse its stdout, exit non-zero on unexpected content | **No existing checker does this.** Measured: only `docs/phase5_self_check.py`, `docs/phase6_self_check.py` and `docs/phase7_self_check.py` call `subprocess.run`, and all three do the identical thing — `subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)` to prove builder idempotence. **None captures output. None parses output. None tolerates a non-zero exit.** `docs/environmental_restore_check.py`'s docstring states its posture explicitly: *"Read-only … It never shells out."* |

**What the planner must know about this gap.** The new checker needs three behaviours with no
in-repo precedent: (a) invoke the Playground `validate-shortcut` wrapper, (b) capture stdout/stderr
and accept exit 1 as the expected case, (c) subtract an enumerated waiver set and fail on residue.
Compose it from two partial sources rather than inventing wholesale:

- **Structure, naming, `ROOT`, `require()`, `main()`, the `print("… passed")` tail, and the
  subprocess call form** — copy from `docs/phase6_self_check.py` (the smallest, cleanest
  subprocess-using checker at 120 lines), adding `capture_output=True, text=True` and dropping
  `check=True`.
- **The waiver-enumeration discipline** — the model is `.claude/CLAUDE.md`'s existing **gate B**
  waiver table, which normalises indices to `N` so a future run can diff against it. The new
  checker must do mechanically what that table does by convention: enumerate exactly the permitted
  `Unknown AppIntent identifier` lines for the AX identifier, subtract them, and exit non-zero on
  anything else.

This is a genuinely new file with a partial template, and it should be scoped as its own task —
as should D-14-01's item 1, the `.claude/CLAUDE.md` gate-A constitutional edit, which CONTEXT.md
requires to be a separately named task and not a side effect.

Two further deliverables are new-file work with adjacent-phase precedent rather than a code analog:
`14-UAT.md` (model: the phase-16 UAT instrument, designed to be run in the same device sitting) and
the `docs/BUILD-NOTES.md` deviation-log entry (model: the existing deviation-log rows, which each
carry a reproduction command).

---

## Metadata

**Analog search scope:** `tools/` (3 files), `docs/` (13 checkers), `src/CONFIG-BLOCK.md`,
`.planning/spikes/005-ios-color-filters-identifier/`
**Files scanned:** 17 read or grepped; 5 read in depth for excerpt extraction
**Pattern extraction date:** 2026-08-18
