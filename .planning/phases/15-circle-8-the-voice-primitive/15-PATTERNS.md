# Phase 15: Circle 8 — the Voice primitive - Pattern Map

**Mapped:** 2026-08-18
**Files analyzed:** 10 (2 generator, 1 checker, 1 probe, 2 generated XML, 4 docs/artifacts)
**Analogs found:** 8 / 10 (2 need no analog — they are regenerated or prose)

**Read this first.** This codebase has no controllers, services or components. The unit of
work is a **Python emitter function** that returns a list of Shortcuts plist action dicts,
plus a **`verify_*()` build guard** that fails the build on a structural defect. Those are
the two roles. Every "analog" below is one of them.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `tools/build_state_engine.py` → `_mirror_body()` / `mirror()` / `voice()` (split of `mirror_and_voice()`) | emitter (primitive) | transform (state → action list) | `tools/build_state_engine.py:935 mirror_and_voice()` (the function being split) and `:770 silence()` (gate-then-act shape) | exact |
| `tools/build_state_engine.py` → dispatch tuple + interim comment | config/registry | request-response (name → branch) | `tools/build_state_engine.py:975 primitive_dispatch()` — same lines, edited in place | exact |
| `tools/build_state_engine.py` → `seed_voice_enabled()` + `VOICE_ENABLED_KEY`/`_SEED`/`_ANCHOR` | template seeder | file-I/O (guarded round trip inside a `WFTextTokenString`) | `tools/build_state_engine.py:3324 seed_panic_escape()` + its three module constants at `:3317-3321` | exact |
| `tools/build_state_engine.py` → `verify_voice_enabled_seed()` | build guard (seed shape) | batch scan over `actions` | `tools/build_state_engine.py:3365 verify_panic_escape_seed()` + `:3343 _panic_escape_variables()` | exact |
| `tools/build_state_engine.py` → `verify_voice_gates()` (speech enclosed by both gates; zero `setvolume` in the branch span) | build guard (enclosure/span) | batch scan + control-flow stack walk | `tools/build_state_engine.py:3533 verify_panic_escape_isolation()` + `:1828 enclosing_groups()` | exact |
| `tools/build_state_engine.py` → `verify_speaktext_placement()` (11 sites, all in `Loud Mirror`, none in `Mirror`) | build guard (counting) | batch scan | `tools/build_state_engine.py:1977 verify_dispatch_coverage()` (per-branch resolution) + `:1870 verify_circle_zero_silence()` (surface counting) | exact |
| `tools/build_sentient.py` → import list | config | batch | `tools/build_sentient.py:14-42` — the alphabetised `from build_state_engine import (...)` block | exact |
| `docs/sequence_dispatch_check.py` → "no two entries are action-equal" assertion | standalone checker | file-I/O (read shipped plist) | `docs/sequence_dispatch_check.py:166 require()` + `:189 main()`; sibling `docs/phase5_self_check.py` | exact |
| Rung-2 discriminator probe (`build_mirror_picker_probe.py` + run via `sim_input.py`) | probe builder | file-I/O + transform | `.planning/spikes/010-.../drafts/build_coercion_probe.py` and `sim_input.py` | exact |
| `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` | generated artifact | — | **none — never hand-edited.** Rewritten in place by `main()` | n/a |
| `src/CONFIG-BLOCK.md`, `docs/BUILD-NOTES.md`, `artifacts/shortcuts/MANIFEST.md` | docs / provenance | — | existing sections in each | n/a |

## Pattern Assignments

### `tools/build_state_engine.py` — `_mirror_body()` / `mirror()` / `voice()`

**Analog:** `tools/build_state_engine.py:935 mirror_and_voice()` — the code being split.
Copy its shape verbatim; move the boundary, change nothing else.

**Core pattern to preserve (lines 935-961, read this session):**

```python
def mirror_and_voice():
    baseline = mirror_templates(MIRROR_BASELINES)
    success = mirror_templates(MIRROR_SUCCESSES)
    lapse = mirror_templates(MIRROR_LAPSES)
    a = [comment("""Mirror selects from 30 fact-gated, local templates: ...""")]
    a += mirror_text(baseline, "Mirror Text")
    respected_g, respected_if = if_block("Previous Respected", 4, string="true")
    lapsed_g, lapsed_if = if_block("Previous Respected", 4, string="false")
    a += [respected_if] + mirror_text(success, "Mirror Text") + [otherwise(respected_g), lapsed_if]
    a += mirror_text(lapse, "Mirror Text") + [otherwise(lapsed_g), action("is.workflow.actions.nothing"),
          end_if(lapsed_g), end_if(respected_g), alert("Mirror", variable("Mirror Text"))]
    a += read_value("voice_enabled", variable("State"), "Voice Enabled")
    voice_g, voice_if = if_block("Voice Enabled", 2, number=0)
    spoken_g, spoken_if = if_block("Spoken This Run", 101)
    a += [voice_if, spoken_if, action("is.workflow.actions.speaktext", WFText=variable("Mirror Text"))]
    a += number(1, "Spoken This Run")
    a += [otherwise(spoken_g), action("is.workflow.actions.nothing"), end_if(spoken_g),
          otherwise(voice_g), action("is.workflow.actions.nothing"), end_if(voice_g)]
    return a
```

**Four invariants this excerpt encodes — carry every one into both halves:**

1. `if_block()` returns `(group, action)`; the group is threaded to `otherwise()` and
   `end_if()`. Every block closes with an explicit
   `otherwise(g), action("is.workflow.actions.nothing"), end_if(g)` — never an
   unterminated arm. This is what D-01's "degrade, don't skip" already looks like.
2. Templates come **only** from `mirror_text()`; never build a `list`/`getitemfromlist`
   pair inline (see the `_list_row()` docstring at `:844` for why).
3. Envelopes are never hand-written. `action(...)`, `variable(...)`, `if_block(...)`,
   `text_token(...)` plus the `normalise_string_envelopes` / `normalise_numeric_operands`
   passes in `main()` own axes 2/5/6.
4. `read_value()` for the scalar `voice_enabled` (Get Dictionary Value → **Get Text** →
   Set Variable). Axis 9: `read_value()` is correct here precisely because the value is a
   scalar headed into a comparison. `get_value()` is for the four `COMPOUND_STATE_KEYS`.

**Gate-then-act analog for `voice()`'s speech arm:** `silence()` at `:770` — same shape of
"read a value, numeric `> 0` gate, act in the true arm, `nothing` in the otherwise arm".

**Comment-block pattern (mandatory, structural).** `main()` inserts a generic control-flow
comment before any mode-0 flow action lacking one. Prefer authoring a **specific** bulleted
comment (as `mirror_and_voice()` does) so the generic filler is not inserted for you.

---

### `tools/build_state_engine.py` — the dispatch tuple and its interim comment

**Analog:** `tools/build_state_engine.py:975-1024 primitive_dispatch()` — edit in place.

**The line whose right-hand side changes (`:1016`):**

```python
    for name, implementation in (("Pause", knock), ("Black and White", ash), ("Silence", silence),
                                 ("Intention", confession), ("Dim", dimming), ("Eject", exile),
                                 ("Mirror", mirror_and_voice), ("Loud Mirror", mirror_and_voice),
                                 ("Frozen", ice_start)):
        group, check = if_block("Selected Primitive", 4, string=name)   # 4 = "string is", never 99
        a += [comment(f"Dispatch {name} only when the selected Config entry names it exactly: ..."), check]
        a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
```

→ `("Mirror", mirror), ("Loud Mirror", voice)`.

**Comment-hygiene duty, same commit.** The block at `:994-1010` currently reads *"'Loud
Mirror' … reuses mirror_and_voice() as a DELIBERATE INTERIM … PHASE 15 replaces it."* Plan
11-02's standing prohibition cuts both ways — delete the Loud Mirror paragraph, **keep** the
`Eject`/Phase 17 paragraph. Same duty at `src/CONFIG-BLOCK.md:31` and `docs/BUILD-NOTES.md`
§34 (§34's second stand-in stays).

**Naming constraint copied from the same comment block:** `docs/environmental_restore_check.py`
imports generator functions **by name**. Check that file before renaming
`mirror_and_voice` out of existence; if it is referenced there, update both.

---

### `tools/build_state_engine.py` — `seed_voice_enabled()` and its constants

**Analog:** `tools/build_state_engine.py:3317-3341` — `seed_panic_escape()` is the exact
precedent, including a numeric flag seeded flat at the top level.

**Constants pattern (`:3317-3321`):**

```python
PANIC_ESCAPE_KEY = "panic_escape_enabled"
PANIC_ESCAPE_SEED = 1
PANIC_ESCAPE_ANCHOR = '"ai_enabled": false,'
```

**Seeder pattern (`:3324-3341`):**

```python
def seed_panic_escape(actions):
    """... Idempotent: a second run finds the key already present and returns.
    _replace_in_token() does the guarded round trip -- it shifts every attachmentsByRange
    offset that sits after the edit and re-asserts that each one still lands on a U+FFFC
    placeholder ... An unshifted offset points into unrelated prose and .claude/CLAUDE.md §5
    records that an out-of-bounds range can crash Shortcuts on import."""
    _, inner = _state_template(actions)
    if f'"{PANIC_ESCAPE_KEY}"' in inner["string"]:
        return  # already seeded; verify_panic_escape_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    _replace_in_token(inner, PANIC_ESCAPE_ANCHOR,
                      PANIC_ESCAPE_ANCHOR + f'\n{indent}"{PANIC_ESCAPE_KEY}": {PANIC_ESCAPE_SEED},')
```

**How this maps to D-05.** `voice_enabled` is already *in* the template (fed by the
`Voice Normalised` variable), so the phase's edit is not an insertion but a **retarget**: the
two `gettext` actions that produce `"true"` / `"false"` become `"1"` / `"0"`. Address them by
**content**, never by index 66/67 — `next(item for item in actions if ...
WFTextActionText == "true")` is the direct analog of the `next(text for text in ...)` line
above. `_state_template()` at `:3058` anchors on `'"schema_version"'`, never an index; the
`schema_version` 4→5 bump goes through `_replace_in_token()` at both the template **and** the
version-check literal (see `:5389-5399` for the prior bump's own reasoning).

**Registration:** call it in `main()` in the seeder block (`seed_settings_snapshot` …
`seed_create_target_url`), **before** `fix_state_rebind(actions)` — the ordering comment at
`main()`'s `seed_panic_escape` call states why.

---

### `tools/build_state_engine.py` — the three new build guards

**Primary analog:** `tools/build_state_engine.py:3365 verify_panic_escape_seed()` and
`:3533 verify_panic_escape_isolation()`. These are the project's best guards and encode four
rules the new guards must copy.

**Rule 1 — resolve targets by PROVENANCE, never by a bare variable-name literal
(`:3343-3363`):**

```python
def _panic_escape_variables(actions):
    """Every named variable whose PROVENANCE resolves to the Panic Escape state key.
    ... a NAME is not a contract: the emitter and the guard sat forty lines apart in this
    same file and shared no constant, so renaming the emitter silently disconnected the guard
    ... Resolution runs through _read_variable_keys(), which walks read_value()'s emitted
    getvalueforkey -> gettext -> setvariable chain backwards, accepting BOTH the bare
    descriptor and the attachmentsByRange form normalise_string_envelopes() rewrites it into.
    """
    return {name for name, keys in _read_variable_keys(actions).items()
            if PANIC_ESCAPE_KEY in keys}
```

→ `verify_voice_enabled_seed()` and `verify_voice_gates()` must resolve the Voice-Enabled
variable set through `_read_variable_keys(actions)` against `VOICE_ENABLED_KEY`, not against
the literal `"Voice Enabled"`.

**Rule 2 — a guard that resolves nothing must FAIL, not pass vacuously (`:3600-3625`):**

```python
    guarded = _panic_escape_variables(actions)
    if not guarded:
        raise SystemExit(
            f"no variable resolves to {PANIC_ESCAPE_KEY!r} by provenance, so no Panic Escape "
            "group could be located and this guard would report Emergency Restore isolated "
            "without having tested anything -- see verify_panic_escape_seed()")
    groups = {item["WFWorkflowActionParameters"].get("GroupingIdentifier") ...}
    groups.discard(None)
    if not groups:
        raise SystemExit("... Zero groups is a failure for the same reason zero surfaces is: "
                         "a guard that reports clean because it resolved nothing is worse "
                         "than no guard")
```

→ Every new guard needs **two** non-empty assertions: the resolved variable/site set, and
the resolved group set. Zero `speaktext` sites is a failure, not a pass.

**Rule 3 — enclosure is computed structurally, not by index (`:1828-1846`):**

```python
def enclosing_groups(actions):
    """For each action, the list of control-flow GroupingIdentifiers enclosing it.
    One left-to-right pass maintaining a stack. A mode-2 endpoint pops before it is
    recorded ...; a mode-0 start pushes after it is recorded ..."""
    stack, out = [], []
    for index, item in enumerate(actions):
        parameters = item.get("WFWorkflowActionParameters", {})
        identifier = item.get("WFWorkflowActionIdentifier")
        mode = parameters.get("WFControlFlowMode")
        if identifier in CONTROL_FLOW_IDENTIFIERS and mode == 2 and stack:
            stack.pop()
        out.append(tuple(stack))
        if identifier in CONTROL_FLOW_IDENTIFIERS and mode == 0:
            stack.append(parameters.get("GroupingIdentifier"))
    return out
```

→ Use this for "every `speaktext` site is enclosed by both the `Voice Enabled > 0` group and
the `Spoken This Run` condition-101 group" and for "zero `setvolume` inside a `Loud Mirror`
branch span". `docs/router_ui_census.py` has the same helper if the check lands there instead.

**Rule 4 — never hardcode a condition code as a filter; resolve it per site
(`verify_dispatch_coverage()`, `:2043-2060`):**

```python
        code = parameters.get("WFCondition")
        tested = parameters.get("WFConditionalActionString")
        if not isinstance(tested, str):
            strategy = "unknown"
        elif code == 99:      # "contains"
            strategy = "contains"
        elif code == 4:       # "string is"
            strategy = "exact"
        else:
            strategy = "unknown"
```

…and `unknown` **raises**, it is not skipped. Copy that discipline: an unrecognised gate
shape is a failure, never an exclusion.

**Gate-shape matcher to copy for the `> 0` assertion (`:1849-1858`):**

```python
def _is_silent_band_conditional(item):
    """A mode-0 If testing `Circle Next > 0` -- the Circle-0 silent-band gate."""
    parameters = item.get("WFWorkflowActionParameters", {})
    return (item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
            and parameters.get("WFControlFlowMode") == 0
            and parameters.get("WFCondition") == 2
            and parameters.get("WFNumberValue") == 0
            and parameters.get("WFInput", {}).get("Variable", {})
                          .get("Value", {}).get("VariableName") == "Circle Next")
```

→ The Voice gate is the same shape (`WFCondition == 2`, `WFNumberValue == 0`) with a
provenance-resolved variable name instead of the literal.

**Error-message convention, non-negotiable.** Every `raise SystemExit` in this file states
(a) what was found, (b) what is required, (c) **the user-visible failure it prevents**, and
(d) what to change. Copy `verify_dispatch_coverage()`'s orphan message as the model.

**Registration in `main()` (`:5535-5560`):** guards run after the three `normalise_*` passes
and before the single `SOURCE.write_bytes(...)`. Place the new ones **beside their sibling**
with a comment saying why they are neighbours — the `verify_panic_escape_isolation()` and
`verify_environmental_reachability()` call sites both do exactly this.

**Negative-control duty (project standard, plan 11-10).** Each new guard must be demonstrated
to fail on a synthesised defect. `verify_panic_escape_isolation()`'s docstring records its own
measured mutation ("all three gates behind one set_var hop each -> both builders exit 0") —
write the equivalent sentence into each new guard's docstring.

---

### `tools/build_sentient.py` — arming the new guards

**Analog:** `tools/build_sentient.py:14-42` — one alphabetised import block.

```python
from build_state_engine import (
    flow_index,
    input_key_tests,
    normalise_numeric_operands,
    ...
    verify_dispatch_coverage,
    ...
    verify_string_envelopes,
)
```

Add the new `verify_*` names **in alphabetical position** and call them where the fork calls
the other twenty. A guard added to the Core builder and not to this list is armed on one fork
only — the exact silent-divergence risk Pitfall 6 names.

---

### `docs/sequence_dispatch_check.py` — the "no two entries are action-equal" assertion

**Analog:** the same file, `:166 require()` and `:189 main()`.

```python
def require(value: bool, message: str) -> None:
    ...  # exits non-zero with the message; the file's only assertion primitive
```

**Structural conventions from its module docstring (`:1-46`), all load-bearing:**

- *"Read-only: parses the built artifact with plistlib. No subprocess, no rebuild."*
- It never hardcodes a condition code as a filter (`match_strategy()` at `:72`).
- It splits entries on `+` unconditionally so a reintroduced combined entry **fails** rather
  than being mis-parsed.
- `KNOWN_ORPHANS = {}` at `:69` — the escape hatch is deliberately visible and deliberately
  empty. **Do not re-populate it.** Phase 11 already removed the `Voice` entry; there is no
  exemption left to remove, contra the ROADMAP.

The new assertion (branch bodies for two distinct entry names must not be action-equal) fits
as a fifth `require(...)` in `main()`, comparing per-branch action spans located the same way
`collect_dispatch_branches()` at `:138` locates them. `docs/phase5_self_check.py` is the
sibling to copy if it lands in a separate file instead.

---

### The rung-2 discriminator probe (D-04, Open Question Q2)

**Analogs:** `.planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/build_coercion_probe.py`
(the builder) and `.../drafts/sim_input.py` (the runner). Both are recorded instruments, not
throwaways — reuse `sim_input.py` verbatim.

**Builder conventions, from `build_coercion_probe.py:1-52`:**

- **Author the plist directly rather than delegating to `shortcut-builder`** when the spike's
  purpose is to *vary* a byte shape deliberately — an agent "corrects" the value under test.
  `.planning/spikes/CONVENTIONS.md` records this exception; cite it in the new probe's
  docstring as a deviation, exactly as spike 010 does.
- **Transcribe byte shapes from `tools/build_state_engine.py`**, citing the symbol each came
  from. Here: `mirror_text()` `:917`, `_list_row()` `:844`, and the `speaktext` line in
  `mirror_and_voice()`. Do not re-derive them.
- **Breadcrumbs A..D at base depth**, and they are **`Show Result`, never `Show Alert`** — a
  Show Alert modal wedges a simulator run permanently (C-8).
- **Distinct test literals per leg**, so a partial failure is attributable from the screen
  alone.
- Bisect by deleting legs (`speaktext`, then `getitemfromlist`) to isolate.

**Runner conventions, from `sim_input.py:1-55`:**

- `open -a Simulator` **first** — a `simctl`-booted sim has no window and a click lands on
  nothing.
- `xcrun simctl openurl <udid> "file:///abs/path.shortcut"` → the import sheet; one
  synthesized tap on **Add Shortcut** completes it.
- **Coordinates are fractions of the device screen mapped through the window rect measured at
  run time, never pixels.** `simulator_window()` re-measures every call and caches nothing.
- The docstring's "WHAT DID NOT WORK" list is the format to copy for the new probe's own dead
  ends.

**Recording duty:** the probe's result goes into `docs/BUILD-NOTES.md` (and
`docs/CAPABILITY-DECISIONS.md` if it settles a capability). A probe result is *recorded, not
consumed*.

---

### `src/PROSOCHE-Dumb.xml` / `src/PROSOCHE-Sentient.xml`

**No analog and no pattern — these are never authored.** `main()` parses once and serializes
once back to the same path. Any hand edit is overwritten or corrupts `attachmentsByRange`
offsets. If a Config-literal edit is genuinely needed, it goes through
`tools/plist_text_edit.py` / `_replace_in_token()`. `src/CONFIG-BLOCK.md` is a **mirror**, not
the source — `verify_dispatch_coverage()` reads the literal inside the XML.

## Shared Patterns

### Emitter helper vocabulary
**Source:** `tools/build_state_engine.py:106-600`
**Apply to:** every emitter change in this phase

`uid()` `:106` · `action()` `:157` · `variable()` `:185` · `text_token()` `:196` ·
`comment()` `:285` · `set_var()` `:289` · `get_value()` `:293` (compound) ·
`read_value()` `:333` (scalar) · `set_value()` `:344` · `if_block()` `:354` ·
`otherwise()` `:377` · `end_if()` `:381` · `number()` `:385` · `alert()` `:447` ·
`list_items()` `:461` · `save_state()` `:437`.

Never hand-write a plist dict. The three `normalise_*` passes in `main()` own axes 2/5/6 at
4300 sites and are the only thing that has ever got all three right.

### Control-flow block discipline
**Source:** `mirror_and_voice()` `:935`, `silence()` `:770`
**Apply to:** `mirror()`, `voice()`, every new guard's expectations

A fresh `uid()` per block; the group threaded to both `otherwise()` and `end_if()`; every
otherwise arm explicitly filled with `action("is.workflow.actions.nothing")`.
`verify_group_identifier_uniqueness()` `:4429` enforces the first clause.

### Guard docstring form
**Source:** `verify_dispatch_coverage()` `:1977`, `verify_panic_escape_seed()` `:3365`
**Apply to:** all three new guards

Structure: (1) one-line "Fail the build if …"; (2) **why this needs a guard at all** — what
makes the defect invisible to the validator, the catalog and the decrypt; (3) the numbered
assertions with the failure each prevents; (4) the negative control that proved the guard has
teeth; (5) any deliberate non-coverage, stated as deliberate.

### Anchor on symbols and content, never on indices
**Source:** `_state_template()` `:3058` (anchors on `'"schema_version"'`),
`seed_panic_escape()` `:3337`, `tools/build_sentient.py`'s `CONTRACT_MARKER` /
`IMPORT_ANCHOR_VARIABLE` comments
**Apply to:** the `voice_enabled` gettext retarget, every doc line reference

Action indices shift on every rebuild. `build_sentient.py`'s WR-11 note records what happened
when an import question was spliced at a hard-coded 6.

### Do-not-fabricate at the parameter level
**Source:** `_list_row()` docstring `:844-908`; `.claude/CLAUDE.md` C-1
**Apply to:** the `speaktext` call in `voice()`

Emit `WFText` only. `WFSpeakTextWait` / `Rate` / `Pitch` / `Language` / `Voice` are
catalog-real but **no donor shows their serialization** — omitting them is the safest
fallback, and the deviation is recorded. There is **no volume parameter**; "never at unsafe
levels" is satisfied by writing no volume at all in the Voice path.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `docs/BUILD-NOTES.md` §19.7 / §34 supersession notes, `src/CONFIG-BLOCK.md:31` | prose | — | Documentation edits; follow each file's existing section/changelog form |
| `artifacts/shortcuts/MANIFEST.md` new block | provenance record | — | Copy the most recent existing block's row shape; `docs/manifest_check.py` asserts it. Convention: a fork whose source is byte-identical is **not** re-signed, and that must be *measured* (`git status --short -- src/` empty after rebuild), not assumed |

## Metadata

**Analog search scope:** `tools/`, `docs/`, `src/`, `.planning/spikes/010-*/drafts/`
**Files scanned:** 6 read in targeted ranges (`build_state_engine.py`, `build_sentient.py`,
`sequence_dispatch_check.py`, `build_coercion_probe.py`, `sim_input.py`, plus the two phase
inputs); ~1,400 lines of generator source read directly
**Pattern extraction date:** 2026-08-18

**Line-number caveat.** `tools/build_state_engine.py` is 5,582 lines and every symbol above
shifts on edit. **Anchor on the symbol name, not the line** — the same rule `.claude/CLAUDE.md`
states for the gate-B waiver.
