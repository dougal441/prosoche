# Phase 16: Dimming and Silence as distinct device-proven Circles — Pattern Map

**Mapped:** 2026-08-17
**Files analyzed:** 11 (4 generated/derived)
**Analogs found:** 10 / 11

## Reading this file

This project has no application source. The product is two generated Shortcuts plist XMLs
emitted by Python generators and pinned by standalone Python structural checkers. "Closest
analog" therefore means one of five things, and each row below says which:

- a **renderer helper** in `tools/build_state_engine.py` (returns action dicts);
- a **build guard** in the same file (raises `SystemExit`, run from `main()`);
- a **checker function** in a `docs/*.py` script (raises `AssertionError`, prints `passed`);
- an existing **UAT document** under `.planning/phases/`;
- an existing **archived spike/probe** under `.planning/spikes/`.

**One non-obvious fact the planner must know.** `tools/build_state_engine.py:15` sets
`SOURCE = Path("src/PROSOCHE-Dumb.xml")`, and `main()` does exactly one
`SOURCE.read_bytes()` (`:4394`) and one `SOURCE.write_bytes()` (`:4472`). The generator
**edits the XML in place**; it does not emit it from scratch. Consequently the Config
literal — including `safety.dim_target` and `safety.brightness_floor` — lives **only in
`src/PROSOCHE-Dumb.xml`** (measured at lines 162–166), not in any Python constant. There is
no `dim_target` string anywhere in `tools/` except the read at `:609`. Work item 4 is an XML
edit plus a rebuild, not a generator edit. Do not go looking for a Python literal to change.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `tools/build_state_engine.py` — persistence fix inside `dimming()` / `silence()` | renderer (generator) | transform → file-I/O ordering | `persist_contract()` `:575-593` and the MANUAL menu arms `:2007`, `:2013`, `:2017`, `:2028`, `:2035` | exact |
| `tools/build_state_engine.py` — `Test a Circle` arm `:2023-2027` | renderer (generator) | transform | `manual_emergency_restore()`'s sibling menu arms `:2007-2035` | exact |
| `tools/build_state_engine.py` — new capture-persistence build guard | build guard | static analysis over action list | `verify_restore_gates()` `:3551-3590` | exact |
| `tools/build_state_engine.py` — remove `changed_at` / `changed_by_session_id` writes | renderer (generator) | transform | `dimming()`/`silence()` themselves `:606-608`, `:628-630`; the removal precedent is Phase 12 `12-03`/`12-04` | exact |
| `tools/build_state_engine.py` — `SNAPSHOT_SEED` / `SNAPSHOT_SEEDED_EMPTY` `:2758-2778` | config/seed constant | transform (text edit into a token) | `seed_settings_snapshot()` + `_replace_in_token()` `:2796` | exact |
| `docs/phase9_self_check.py` — new negative control + re-derived counts | test (static self-check) | batch | `negative_control()` `:72-108` and `site_audit()` `:111-151` in the same file | exact |
| `docs/phase5_self_check.py:107-109` — drop two leaf names | test (static self-check) | batch | the loop it lives in, same file | exact |
| `docs/environmental_restore_check.py:257` — relax `> 0` → `>= 0` | test (static self-check) | batch | the adjacent assertion at `:259-260`, which stays | exact |
| `src/PROSOCHE-Dumb.xml` Config literal (`:163-164`) | config | — | the same block's `allow_volume_increase` / `ash_managed_color_filters` rows | exact |
| `.planning/phases/16-…/16-UAT.md` (new) | UAT document | request-response (human operator) | `.planning/phases/13-…/13-UAT.md` | exact |
| `.planning/spikes/010-…/` aimed coercion probe (new) | spike/probe | — | `.planning/spikes/007-unresolvable-picker-failure-mode/` + `.planning/spikes/CONVENTIONS.md` | role-match |
| `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md` (BD-02), `.claude/CLAUDE.md`, `.claude/skills/spike-findings-prosoche/references/{evidence-and-probes,environmental-primitives}.md` | documentation | — | their own existing section structure | n/a |

---

## Pattern Assignments

### `tools/build_state_engine.py` — persist the capture (work item 1)

**Analog A — how a branch saves the dictionary it owns: `persist_contract()` `:575-593`**

```python
    a += reload_state() + read_value("active_session.id", variable("Reloaded State"), "Contract Owner ID")
    owns_group, owns = if_block("Contract Owner ID", 4, string="captured-session-placeholder")
    ...
    a += [owns, set_value("active_session.intention", variable("Confession Intention"), "Reloaded State"),
          set_value("active_session.declared_duration_seconds", variable("Declared Duration Seconds"), "Reloaded State")]
    a += save_state("Reloaded State") + [otherwise(owns_group), action("is.workflow.actions.nothing"), end_if(owns_group)]
```

The load-bearing shape, and the one the fix must copy: **every `set_value(..., X)` in the arm
is followed by `save_state(X)` on that same arm, with the *same* dictionary name.** This is
RESEARCH.md Pattern 2 stated in code. `dimming()`/`silence()` write `set_value(...)` with
`set_value`'s default `dictionary_name="State"` (`:299`), so the new save must be
`save_state("State")` — the default — and must sit **inside** the `capture_g` arm.

**Analog B — the MANUAL menu arms, `manual_emergency_restore()` `:2007-2035`** (same idiom,
splatted rather than concatenated, and the direct model for the `Test a Circle` arm):

```python
        a += [menu(profile_menu, 1, title=profile), action("is.workflow.actions.gettext", UUID=text_id, WFTextActionText=profile),
              set_var("Manual Profile", output(text_id, "Text")), set_value("profile", variable("Manual Profile")),
              *number(1, "Manual Refresh Requested"), *save_state()]
```

`:2028` (Reset Today) and `:2035` (Emergency Restore) use the identical `*save_state()` tail.
**`Test a Circle` at `:2023-2027` is the one arm in that menu with no `save_state()`:**

```python
    a += [menu(group, 1, title="Test a Circle"), menu(test_menu, 0, prompt="Test a Circle", items=[circle_menu_title(number) for number in range(1, 10)])]
    for ...:
        a += [set_var("Circle Next", variable("Test Circle")), comment(...)] + primitive_dispatch("Test Circle")
```

That absence is the MANUAL half of Finding 1. Fix it the same way the other arms already do,
or decide explicitly that it must not fire the environmental primitives — CONTEXT/RESEARCH
require the decision either way.

**Site to change — `dimming()` `:596-615` (`silence()` `:618-638` is the exact mirror):**

```python
    capture_g, capture_if = if_block("Captured Brightness", 2, number=0)
    a += [capture_if, set_value("settings_snapshot.brightness.original_value", variable("Captured Brightness")),
          set_value("settings_snapshot.brightness.changed_at", variable("Now Epoch")),
          set_value("settings_snapshot.brightness.changed_by_session_id", variable("Session ID"))]
    a += config("safety.dim_target", "Dim Target")
    already_dim_g, already_dim_if = if_block("Captured Brightness", 1, number=variable("Dim Target"))
    a += [already_dim_if, action("is.workflow.actions.nothing"), otherwise(already_dim_g),
          set_brightness(variable("Dim Target")), end_if(already_dim_g), otherwise(capture_g),
          alert("Dim", "Brightness could not be captured, so nothing was changed."), end_if(capture_g),
          end_if(snapshot_g)]
```

Ordering constraint (RESEARCH Pattern 1): the `save_state()` goes **after** the
`set_value(...original_value...)` and **before** `set_brightness(...)` / `set_media_volume(...)`.
Note that `set_brightness` sits inside the nested `already_dim_g` otherwise-arm, so a save
placed immediately after the `set_value` block (before `config(...)`) satisfies the ordering
for both arms at once and costs one save per rendering rather than two.

**Do not touch** the `snapshot_g` container gate (`if_block(..., 100)`) or the `capture_g`
numeric `> 0` gate. RESEARCH's Security Domain V5 row is explicit: the fix adds a save, it
must not touch a gate.

**Anti-pattern, named in RESEARCH:** relocating the OPEN-path `save_state()` at `:1337` below
`universal_leaving()`. The comment at `:1335-1336` states why it is where it is, and
`verify_circle_zero_silence()` pins it.

---

### `tools/build_state_engine.py` — the new build guard (work item 2)

**Analog:** `verify_restore_gates()` `:3551-3590`. It is the closest guard by *shape* (walks
the action list, resolves enclosing conditional arms, collects offenders, raises once) and by
*subject* (the same two identifiers, the same snapshot keys).

```python
def verify_restore_gates(actions):
    """Fail the build if a brightness/volume write is not numerically gated.
    ...
    """
    reads, offenders = _read_variable_keys(actions), []
    for index, enclosing in enumerate(_enclosing_if_arms(actions)):
        item = actions[index]
        identifier = item.get("WFWorkflowActionIdentifier")
        if identifier not in {"is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"}:
            continue
        ...
        from_snapshot = any(key.split(".")[0] == SNAPSHOT_ROOT for key in reads.get(name, ()))
        if from_snapshot:
            if not any(_tested_variable(gate) == name for gate in numeric):
                offenders.append((index, f"writes {name!r}, read from {SNAPSHOT_ROOT}, with no "
                                         f"numeric gate on {name!r} above it"))
        elif not numeric:
            offenders.append((index, f"writes {name!r} with no numeric gate above it"))
    if offenders:
        raise SystemExit(
            "a brightness/volume write is not numerically gated -- ..."
            + "; ".join(f"action {i}: {why}" for i, why in offenders[:5])
            + f" ({len(offenders)} total)")
```

Copy verbatim: the docstring-states-the-defect-it-closes convention; `_enclosing_if_arms()`
for arm ancestry; `_read_variable_keys()` / `SNAPSHOT_ROOT` for key provenance; the
`offenders` accumulation; the single `raise SystemExit` with the first five offenders and a
total count. Do **not** raise per site — the project convention is "fix whole classes."

Supporting helpers already present and reusable, no new idiom needed:
`_sentinel_written_keys()` `:3466`, `_read_variable_keys()` `:3483`, `_enclosing_if_arms()`
`:3525`, `_tested_variable()` `:3544`. For save-site resolution, RESEARCH's own script is the
reference — a `documentpicker.save`'s dictionary comes from the `setitemname` immediately
above it, which is exactly what `save_state()` `:392-399` emits:

```python
def save_state(source_name="State"):
    """Save exactly the final full dictionary from this branch, once."""
    named_id = uid()
    return [
        action("is.workflow.actions.setitemname", UUID=named_id, WFName="state.json", WFInput=variable(source_name)),
        action("is.workflow.actions.documentpicker.save", WFInput=output(named_id, "Renamed Item"),
               WFAskWhereToSave=False, WFFileDestinationPath="PROSOCHE/state.json", WFSaveFileOverwrite=True),
    ]
```

Register the guard from `main()` alongside the other `verify_*` calls (`main()` `:4391`), and
check whether `tools/build_sentient.py` needs it in its module-scope import list — the
`cross_fork_check()` docstring in `docs/environmental_restore_check.py:276-283` explains that
Sentient imports a dozen `verify_*` names at module scope and a mismatch breaks the fork build
at import time.

---

### `docs/phase9_self_check.py` — the negative control (work item 2b)

**Analog:** `negative_control()` `:72-108` in the same file. The idiom is three-phase, and the
three phases are what make it load-bearing rather than decorative:

```python
def negative_control() -> None:
    actions = _synthetic_fixture()

    saved = {}
    for identifier in NEW_ENTRIES:
        if identifier in bse.NUMERIC_OPERAND_FIELDS:
            saved[identifier] = bse.NUMERIC_OPERAND_FIELDS.pop(identifier)
    try:
        # Pre-fix state: ... the guard must NOT raise ...
        try:
            bse.verify_numeric_operands(copy.deepcopy(actions))
        except SystemExit:
            raise AssertionError(
                "verify_numeric_operands() raised with the new table entries "
                "removed -- the negative control does not reproduce the "
                "pre-fix exemption bug, so it cannot prove the fix is "
                "load-bearing")
    finally:
        bse.NUMERIC_OPERAND_FIELDS.update(saved)

    # Post-fix state, still uncoerced: the guard must now raise.
    post_fix = copy.deepcopy(actions)
    raised = False
    try:
        bse.verify_numeric_operands(post_fix)
    except SystemExit:
        raised = True
    assert raised, (...)

    # Post-fix, post-normalise: the same fixture must now pass cleanly.
    bse.normalise_numeric_operands(post_fix)
    bse.verify_numeric_operands(post_fix)  # must not raise
    print("negative_control: passed")
```

Copy: the synthetic-fixture builder (`_synthetic_fixture()` `:53-69`, which uses the *real*
`bse.action`/`bse.set_var`/`bse.variable` helpers, never hand-rolled dicts); calling the
**real production guard** rather than a re-implementation; the `try/finally` restore of any
mutated module state; `print("<name>: passed")`. For this phase the fixture is a
capture-then-`setbrightness` sequence **with** and **without** an intervening
`save_state("State")`.

The module docstring `:1-36` is also the analog for how a count change is justified — see
PHASE 11's paragraph at `:23-35`, which explains *why* the totals moved and states the numbers
were MEASURED, not projected. `site_audit()`'s in-body derivation comment `:112-116` is the
per-assertion form:

```python
    # Derivation, measured after PHASE 11's eleventh primitive_dispatch() rendering
    # (see this module's docstring for why there are eleven):
    #   setbrightness = 4 restore_managed_settings() call sites + 11 dimming() renderings
    #   setvolume     = 4 restore_managed_settings() call sites + 11 silence() renderings
    # A delta larger than the rendering count explains is a regression, not a table update.
```

RESEARCH Pitfall 3 is exactly this: any number that moves gets an adjacent comment change in
the same commit, stating what a *larger* delta would mean. The persistence fix adds save
actions and will move totals in both `phase9_self_check.py` and
`environmental_restore_check.py`.

---

### Removing `changed_at` / `changed_by_session_id` (work item 3)

Three coordinated sites, all measured:

**(a) The writes** — `dimming()` `:607-608` and `silence()` `:629-630`, quoted above.

**(b) The seed shape** — `tools/build_state_engine.py:2758-2778`:

```python
SNAPSHOT_SEED = {
    "brightness": ("original_value", "changed_at", "changed_by_session_id"),
    "volume": ("original_value", "changed_at", "changed_by_session_id"),
}
SNAPSHOT_EMPTY = '"settings_snapshot": {},'


def _snapshot_seed_text(indent: str) -> str:
    inner = ",\n".join(
        f'{indent}  "{group}": {{'
        + ", ".join(f'"{leaf}": "{CLEARED_SENTINEL}"' for leaf in leaves)
        + "}"
        for group, leaves in SNAPSHOT_SEED.items())
    return '"settings_snapshot": {\n' + inner + "\n" + indent + "},"


SNAPSHOT_SEEDED_EMPTY = '"original_value": "", "changed_at": "", "changed_by_session_id": ""'
```

`SNAPSHOT_SEEDED_EMPTY` is a **build-j convergence recogniser**, not a seed — its comment
`:2774-2777` says so. Removing leaves from `SNAPSHOT_SEED` changes what gets written;
changing `SNAPSHOT_SEEDED_EMPTY` changes what old text is recognised and corrected in place.
They are not the same edit and must be reasoned about separately. The rewrite goes through
`_replace_in_token()` `:2796-2804`, whose docstring warns that `attachmentsByRange` offsets
must shift with the text — do not hand-edit the template string.

**(c) The checker assertion** — `docs/phase5_self_check.py:107-109`:

```python
    for key in ("settings_snapshot.brightness.original_value", "settings_snapshot.volume.original_value",
                "changed_at", "changed_by_session_id", "cooldown_until"):
        require(key in text, f"missing state safety key: {key}")
```

Drop the two bare leaf names, keep the two dotted `original_value` keys and `cooldown_until`.

**(d) The explanatory comment** — `clear_snapshot()` `:472-474` currently reads:

```python
    changed_at / changed_by_session_id are deliberately left: they are written at 20 sites
    and READ AT NONE in either fork (the ownership check does not exist -- DEV-06, deferred
    to the user as a design change), so stale values there have no consumer.
```

That paragraph becomes false the moment D-02 lands. Rewrite it in place, in the same
docstring, recording that DEV-06 was decided (removal) rather than deleting the history.

**Precedent for a coordinated state-shape change:** Phase 12 did exactly this twice —
`.planning/phases/12-state-shape-sentinel-gaps-exit-events-and-active-session/12-03-PLAN.md`
(`active_session`) and `12-04-PLAN.md` (`exit_events`), with SUMMARYs beside each. The
resulting generator shape is visible today as the paired
`seed_active_session()` `:3271` / `verify_active_session_seed()` `:3311` and
`seed_exit_events()` `:3148` / `verify_exit_events_seed()` `:3185`. **The pairing is the
pattern:** a seeder and a verifier that move together, plus `persist_contract()`'s docstring
`:576-584` as the model for recording *what Phase 12 removed and why the removal was safe*.

**The regression check D-02 names**, stated in CONTEXT: "no `read_value` targets a removed
leaf." `_read_variable_keys()` `:3483` already builds exactly that index — reuse it rather
than grepping.

---

### `docs/environmental_restore_check.py:255-262` — the floor relaxation (work item 4)

```python
    config = _config_literal(actions)
    safety = config.get("safety")
    require(isinstance(safety, dict), "the Config literal has no safety block")
    dim_target = safety.get("dim_target")
    floor = safety.get("brightness_floor")
    require(isinstance(dim_target, (int, float)) and dim_target > 0,          # :257  -> >= 0
            f"safety.dim_target is {dim_target!r}; the dim target must be strictly positive")
    require(isinstance(floor, (int, float)) and dim_target >= floor,          # :259  UNCHANGED
            f"safety.dim_target {dim_target!r} is below safety.brightness_floor {floor!r}")
    require(safety.get("allow_volume_increase") is False,
            "safety.allow_volume_increase is not false; SAFE-02 forbids ever raising volume")
```

Change `:257` only, and update its message text and the block comment above it (`:244-251`,
which already narrates the BD-02 addendum and is the right place to record that the addendum
is now settled on main). D-01 forbids weakening anything else in this file.

**A second, adjacent assertion the planner must not miss** —
`docs/phase5_self_check.py:116-117`:

```python
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.setbrightness":
            require(params.get("WFBrightness") not in (0, "0", 0.0), "brightness may reach zero")
```

This asserts over the **action parameter**, not the Config literal. Every shipped
`WFBrightness` is a variable descriptor dict, not a scalar, so it does not fire today — but it
encodes the same retired "never zero" clause and should be reviewed in the same commit so the
two checkers cannot disagree about what D-01 decided.

**The Config literal itself** lives in `src/PROSOCHE-Dumb.xml:162-166`:

```json
  "safety": {
    "brightness_floor": 0.10,
    "dim_target": 0.12,
    "allow_volume_increase": false,
    "ash_managed_color_filters": true
  }
```

Edit there, then rebuild both forks (`tools/build_state_engine.py` reads and rewrites this
same file in place; `tools/build_sentient.py` forks the built Dumb source).

---

### `.planning/phases/16-…/16-UAT.md` (work item 5)

**Analog:** `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-UAT.md`
— the most recent and the better shape. `09-UAT.md` is the file being superseded, not a model.

Copy its structure section for section:

```markdown
---
status: blocked
phase: 13-red-operator-conditionals-and-the-wfitems-list-wrapper
source: [13-01-SUMMARY.md, 13-02-SUMMARY.md, 13-03-SUMMARY.md, 13-04-PLAN.md]
blocked_on: DIST-03
started: 2026-08-17
updated: 2026-08-17
---

# Phase 13 — Device UAT: does a wrapped `WFItems` row actually render?

## Header — what is under test

| Field | Value |
|---|---|
| Commit artifacts were signed at | `365937e` — **the CR-01 re-ship**, which supersedes plan 13-04 task 1's `737ce07` |
| Fork 1 | **Core** — `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — 233802 bytes — SHA-256 `b07497ba…` |
| Manifest row | `artifacts/shortcuts/MANIFEST.md`, the six "Core"/"Aware" rows — ... `python3 docs/manifest_check.py` proves every row against disk |
| Personal Automations | **Not required for Tests 1–4.** Every test below is reachable from the shortcut's own manual menu ... |

## ⚠ Re-import precondition — read this before anything else
## What this phase changed, in one paragraph
## Why device-only — no automated substitute exists
```

Elements that are load-bearing and must be reproduced:

- **YAML frontmatter** with `status: blocked` / `blocked_on: DIST-03` — this is how the project
  records a device-gated result honestly (Phase 10 DIST-03, Phase 12
  `verification_deferred_human` precedent).
- **Build-identity header** pinned to commit + display name + byte count + SHA-256 per fork,
  cross-referenced to `artifacts/shortcuts/MANIFEST.md` and provable by
  `python3 docs/manifest_check.py`. `09-UAT.md`'s lack of this is RESEARCH Pitfall 2.
- **A re-import precondition block** explaining why a stale install produces a false negative —
  directly transferable: a device still holding a pre-fix build has an unpersisted capture.
- **"Why device-only"**, per test, citing `.claude/CLAUDE.md` §9's "Rung 2's ceiling", and — new
  this phase — which tests were already settled at rung 1 or 2 so they are not re-run.
- **Per-test Setup / Sequence / Expected observation / Failure evidence / blank `outcome:`.**
- A `## Verdict` placeholder citing test numbers per claim.

Additions this phase's instrument needs that `13-UAT.md` does not have, per RESEARCH: a safety
preamble (brightness and volume *will* change; iOS Settings is the only recovery); a Setup step
recording pre-session brightness and volume by hand; the explicit batching note (12-UAT Test 3,
Phase 18's lock case, Phase 19's nine-Circle sweep); and the compound
overlap + force-quit-the-winner trial as a **named test**, not an optional extra.

---

### The aimed coercion probe (work item 6)

**Analog:** `.planning/spikes/007-unresolvable-picker-failure-mode/` — directory layout
(`README.md`, the signed `.shortcut` at top level, `drafts/` for the unsigned XML, a timestamped
archive directory) — governed by `.planning/spikes/CONVENTIONS.md`:

```markdown
- Each spike directory (`.planning/spikes/NNN-name/`) holds: `README.md` (frontmatter +
  findings), the signed `.shortcut` artifact when the spike produces one, the unsigned
  editable `.xml` source (in `drafts/`), and a timestamped archive copy.
- Delegate the actual build to the `shortcut-builder` agent in the background — write the
  README's frontmatter and "What This Validates"/"How to Run"/"What to Expect" sections
  yourself before delegating, so the spike's intent is pinned down independent of the build.
- Diagnostic/probe shortcuts ... kept fully standalone — no dependency on the production
  PROSOCHĒ shortcut or its `state.json`.
```

Also mandatory from CONVENTIONS: build via the `shortcuts-playground:shortcut-builder` agent
rather than hand-authoring plist XML; gate A clean; gate B advisory, expected-waiver-only.
Register the new spike in `.planning/spikes/MANIFEST.md`. Simulator-test before it would ever
reach the user's iPhone — standing policy (`.claude/CLAUDE.md` §9), now actually possible per
RESEARCH Finding 3's `xcrun simctl openurl file://…` channel.

Probe content, per RESEARCH: `Text` → `Set Variable` → `Set Brightness` fed by that variable
**with** the coercion; the same **without**; a `Get Device Details → Current Brightness` →
`Show Result`; and a restore leg. The emitted shapes to reproduce are the generator's own
`set_brightness()` `:448-450` / `set_media_volume()` `:453-455` plus
`normalise_numeric_operands()` `:3912`'s aggrandizement — **coercion first in the
`Aggrandizements` list** (RESEARCH Pattern 3; `existing.insert(0, ...)`).

---

## Shared Patterns

### Guard-and-negative-control pairing
**Source:** `tools/build_state_engine.py::verify_restore_gates` `:3551` +
`docs/phase9_self_check.py::negative_control` `:72`
**Apply to:** every new invariant this phase asserts.
A guard is not accepted on the strength of prose. It ships with a synthetic fixture that
reproduces the pre-fix defect (guard must NOT raise), then the post-fix state (guard MUST
raise), then post-normalise (must pass). The fixture is built from the real generator helpers.

### Docstring-states-the-defect
**Source:** `clear_snapshot()` `:458-476`, `restore_managed_settings()` `:479-505`,
`verify_restore_gates()` `:3552-3562`, `universal_leaving()` `:1058-1092`
**Apply to:** every generator function this phase touches.
Every non-obvious construct carries a docstring naming the defect it closes, the evidence
(donor, cycle, phase), the rejected alternative and *why* it was rejected, and the cost paid
deliberately. `restore_managed_settings()` is the strongest example — it documents a verified
construct (condition 5) that was then rejected, with the device measurement that rejected it.

### Comments that own a number
**Source:** `docs/phase9_self_check.py:112-116`, `docs/environmental_restore_check.py:264-273`,
`universal_leaving()` `:1089-1092`
**Apply to:** every count that the persistence fix moves.
A number in a checker carries an adjacent derivation stating how it was arrived at, that it was
MEASURED not projected, and what a larger delta would mean. RESEARCH Pitfall 3: a diff that
changes a number with no adjacent comment change is the warning sign.

### `require()` over bare `assert`
**Source:** `docs/phase5_self_check.py:29-31`, `docs/environmental_restore_check.py`

```python
def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
```

`phase9_self_check.py` uses bare `assert` with a long message instead. Both idioms are live;
match whichever file you are editing rather than introducing a third.

### Locate by content, never by index
**Source:** `_state_template()` `:2781-2793`, `docs/phase5_self_check.py::marker_index` `:34-38`,
`docs/phase5_self_check.py:12` (`from sequence_dispatch_check import config_literal`)

```python
def _state_template(actions):
    """The bootstrap state.json template action, located by content, never by index."""
```

Every action index in CONTEXT.md and RESEARCH.md (521, 524, 1012, 728, …) is a *measurement*,
not an anchor. The persistence fix will move all of them. No new code may key off an index.

### Reuse the existing reader rather than inventing a third idiom
**Source:** `docs/phase5_self_check.py:10-12` comment
Before writing a new helper to find the Config literal, the snapshot seed, or a save's source
dictionary, check whether `config_literal()` (`sequence_dispatch_check`), `_config_literal()`
(`environmental_restore_check`), `_state_template_string()`, `_read_variable_keys()` or
`_sentinel_written_keys()` already does it.

### The full static suite is the definition of done
**Source:** `16-RESEARCH.md` "Validation Architecture"

```bash
python3 tools/build_state_engine.py && python3 tools/build_sentient.py \
  && python3 docs/state_engine_self_check.py && python3 docs/phase9_self_check.py \
  && python3 docs/environmental_restore_check.py && python3 docs/manifest_check.py \
  && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all \
  && validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all
```

Add `docs/phase5_self_check.py` — this phase edits it. Gate B
(`--target-macos 27 --target-platform all`) is advisory, expects exit 1 with exactly the one
`WFCreateNoteInput` waiver, and must never be `&&`-chained.

### Rebuild ripple
**Source:** `16-RESEARCH.md` Runtime State Inventory, `docs/manifest_check.py`
Any generator or Config change requires: rebuild both forks in one pass (Sentient forks the
built Dumb source), re-sign under the **exact existing display names** (`PROSOCHĒ — Nine
Circles — Core` / `— Aware` — a rename breaks the user's Personal Automations, BD-06-A4
precedent), refresh `artifacts/shortcuts/MANIFEST.md`'s six rows, re-run
`python3 docs/manifest_check.py`, and re-pin `16-UAT.md`'s SHA-256 header.
Provenance guard first: `git merge-base --is-ancestor 7ca8ebb HEAD`.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| A build guard that reasons about **save ordering across an arm** | build guard | static analysis | Every existing guard reasons about a single action's parameters or its enclosing conditional arms. None traces "does a `documentpicker.save` of dictionary X occur between action A and action B on the same arm." `verify_restore_gates()` supplies the walk-and-collect skeleton and `_enclosing_if_arms()` supplies the ancestry, but the save-source resolution is new — model it on RESEARCH.md's "The persistence proof" snippet (`save_source(i)` looks back up to 3 actions for a `setitemname` and reads its `WFInput.Value.VariableName`), which matches `save_state()`'s emitted shape exactly. |

---

## Metadata

**Analog search scope:** `tools/` (2 generators + 1 helper), `docs/` (12 checkers),
`src/PROSOCHE-Dumb.xml` (Config literal), `.planning/phases/09|12|13-*/`, `.planning/spikes/`
**Files scanned:** 12 read in full or in targeted ranges; 24 phase directories and 9 spike
directories enumerated
**Pattern extraction date:** 2026-08-17
