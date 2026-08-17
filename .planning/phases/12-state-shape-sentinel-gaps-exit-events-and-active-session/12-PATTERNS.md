# Phase 12: State-shape sentinel gaps — exit_events and active_session - Pattern Map

**Mapped:** 2026-08-17
**Granularity:** SYMBOL, not file. This phase creates no new files; it adds functions to
`tools/build_state_engine.py`, arms them in `tools/build_sentient.py`, and edits one
assertion literal in `docs/state_engine_self_check.py`.
**Symbols analyzed:** 12 new/modified
**Analogs found:** 12 / 12 (every one exists at HEAD and was re-read this session)

> **Anchor discipline.** Every line number below was re-measured this session against the
> working tree. They match `12-RESEARCH.md`'s citations exactly — no anchor has moved.
> Still: **anchor on the symbol name, never the line number.** Each seeder insertion shifts
> every line after it in the file.

## File Classification

| Symbol to create / modify | File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|---|
| `seed_exit_events()` NEW | `tools/build_state_engine.py` | seeder (template transform) | file-I/O → text transform | `seed_panic_escape()` `:2645` | exact (flat top-level scalar/array seed) |
| `seed_active_session()` NEW | `tools/build_state_engine.py` | seeder | file-I/O → text transform | `seed_pending_exit()` `:2570` | exact (container/leaf seed) |
| `verify_exit_events_seed()` NEW | `tools/build_state_engine.py` | build guard | transform (assert-only) | `verify_panic_escape_seed()` `:2664` | exact |
| `verify_active_session_seed()` NEW | `tools/build_state_engine.py` | build guard | transform (assert-only) | `verify_pending_exit_seed()` `:2597` | exact |
| `verify_state_seed()` MODIFY (generalise) | `tools/build_state_engine.py` | build guard | transform | itself `:2496` — a **deletion** at `:2523` | self |
| `KNOWN_SENTINEL_EXISTENCE_GATES` → `()` | `tools/build_state_engine.py` `:217` | config constant | — | the pending_exit removal recorded in its own comment `:196-206` | exact |
| `EXIT_EVENTS_SEED` / `ACTIVE_SESSION_SEED` / `*_ANCHOR` consts NEW | `tools/build_state_engine.py` | config constant | — | `PENDING_EXIT_SEED` / `PENDING_EXIT_ANCHOR` `:2566-2567`; `PANIC_ESCAPE_KEY/SEED/ANCHOR` `:2638-2642` | exact |
| `PENDING_EXIT_ANCHOR` MODIFY | `tools/build_state_engine.py` `:2567` | config constant | — | — (its literal `'"active_session": null,'` **is** the line this phase rewrites — Pitfall 2) | n/a |
| `record_exit_and_route()` gate conversion | `tools/build_state_engine.py` `:897` | generator pipeline fn | request-response (emits plist) | `complete_pending_exit()` `:1036-1038` | exact |
| `persist_contract()` (×11 renders), `close_pipeline()` (2 gates), `route_exit()` Create branch | `tools/build_state_engine.py` `:560`, `:1230`, `:840` | generator pipeline fn | request-response | same `complete_pending_exit()` `:1036-1038` idiom | exact |
| `open_pipeline()` container write → 3 leaf writes | `tools/build_state_engine.py` `:1183-1188` | generator pipeline fn | CRUD (write) | `persist_contract()` `:569-570` leaf writes | exact |
| `live_ice_redirect()` / `manual_emergency_restore()` clears | `:1812`, `:1893` | generator pipeline fn | CRUD (clear) | `complete_pending_exit()` leaf clear `:1058-1061` | exact |
| `main()` seeder + verifier registration | `tools/build_state_engine.py` `:3683-3688`, `:3718-3722` | orchestration | — | the existing call block, quoted below | exact |
| `build_sentient.py` import + arm | `tools/build_sentient.py` `:13-27`, `:296-303` | orchestration | — | its own `verify_state_seed(actions)` arming, quoted below | exact |
| `docs/state_engine_self_check.py:92` literal | `docs/*.py` | test/checker | — | the required-key tuple itself | n/a (one-literal edit) |
| `SCHEMA_VERSION` 3→4 | `tools/build_state_engine.py` `:3557-3562` | config constant | — | the 2→3 bump recorded in `fix_state_rebind()`'s docstring | exact |

## Pattern Assignments

### `seed_active_session()` (seeder, container/leaf) — NEW

**Analog:** `seed_pending_exit()`, `tools/build_state_engine.py:2570-2594` (constants `:2566-2567`)

**Constants pattern** — `:2566-2567`:
```python
PENDING_EXIT_SEED = {"type": CLEARED_SENTINEL, "timestamp": CLEARED_SENTINEL}
PENDING_EXIT_ANCHOR = '"active_session": null,'
```

**Core pattern (verbatim)** — `:2587-2594`:
```python
    _, inner = _state_template(actions)
    if '"pending_exit"' in inner["string"]:
        return  # already seeded; verify_pending_exit_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PENDING_EXIT_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    leaves = ", ".join(f'"{leaf}": "{value}"' for leaf, value in PENDING_EXIT_SEED.items())
    _replace_in_token(inner, PENDING_EXIT_ANCHOR,
                      PENDING_EXIT_ANCHOR + f'\n{indent}"pending_exit": {{{leaves}}},')
```

Four things to copy exactly and one to change:
1. **Locate by `_state_template(actions)`** `:2438` — content-anchored on `'"schema_version"'`, never an index.
2. **Idempotency early-return on a substring test** of the whole template string (Pitfall 8). `seed_active_session()` must guard on an unambiguous token: `'"active_session": {'` — **not** `'"active_session"'`, which is already present as `"active_session": null,`.
3. **Derive `indent` from the anchor line**, never hard-code it.
4. **Every text edit goes through `_replace_in_token()`** `:2453` — it shifts all four `attachmentsByRange` offsets past the edit and re-asserts each still lands on `U+FFFC`.
5. **Change:** this seeder *replaces* the existing `"active_session": null,` line rather than inserting after an anchor. That is closer to `seed_settings_snapshot()`'s `SNAPSHOT_EMPTY` replace (`:2489-2493`) than to `seed_pending_exit()`'s insert-after. Use `seed_settings_snapshot()` for the replace mechanics and `seed_pending_exit()` for everything else:

**Replace-in-place mechanics (verbatim)** — `seed_settings_snapshot()` `:2489-2493`:
```python
    if SNAPSHOT_EMPTY not in inner["string"]:
        return  # already seeded; verify_state_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if SNAPSHOT_EMPTY in text)
    indent = line[:len(line) - len(line.lstrip())]
    _replace_in_token(inner, SNAPSHOT_EMPTY, _snapshot_seed_text(indent))
```

**Multi-leaf seed-text builder (verbatim)** — `_snapshot_seed_text()` `:2422-2428`, the pattern for
rendering the four `active_session` leaves (`id`, `started_at`, `declared_duration_seconds`,
`intention`) if the planner wants them on separate lines:
```python
def _snapshot_seed_text(indent: str) -> str:
    inner = ",\n".join(
        f'{indent}  "{group}": {{'
        + ", ".join(f'"{leaf}": "{CLEARED_SENTINEL}"' for leaf in leaves)
        + "}"
        for group, leaves in SNAPSHOT_SEED.items())
    return '"settings_snapshot": {\n' + inner + "\n" + indent + "},"
```

**⚠ Coupled edit — Pitfall 2.** `PENDING_EXIT_ANCHOR = '"active_session": null,'` (`:2567`) *is*
the literal this seeder destroys. `seed_pending_exit()` early-returns today so `next(...)` is never
reached — but on a template regenerated without `pending_exit` it raises a bare `StopIteration`, not
`SystemExit`. **Re-point `PENDING_EXIT_ANCHOR` in the same commit.** Verified this session that
`SNAPSHOT_EMPTY` (`:2419`) and `PANIC_ESCAPE_ANCHOR = '"ai_enabled": false,'` (`:2642`) are *not*
touched by this phase.

---

### `seed_exit_events()` (seeder, flat array) — NEW

**Analog:** `seed_panic_escape()`, `tools/build_state_engine.py:2645-2661` — the flat top-level
insert-after-anchor form, which is the correct shape for `exit_events` (Research Pattern 2), plus
`exit_selection_counter: 0`.

**Constants (verbatim)** — `:2638-2642`:
```python
PANIC_ESCAPE_KEY = "panic_escape_enabled"
PANIC_ESCAPE_SEED = 1
# Anchored on the neighbouring boolean-ish settings line, never on a line number: the
# template is one long WFTextTokenString and every offset in it moves on any edit.
PANIC_ESCAPE_ANCHOR = '"ai_enabled": false,'
```

**Core pattern (verbatim)** — `:2655-2661`:
```python
    _, inner = _state_template(actions)
    if f'"{PANIC_ESCAPE_KEY}"' in inner["string"]:
        return  # already seeded; verify_panic_escape_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    _replace_in_token(inner, PANIC_ESCAPE_ANCHOR,
                      PANIC_ESCAPE_ANCHOR + f'\n{indent}"{PANIC_ESCAPE_KEY}": {PANIC_ESCAPE_SEED},')
```

`'"exit_events"'` is a collision-free guard token (Pitfall 8). The seeded value is `[]` — mirroring
`"recent_sessions": []` / `"recent_contracts": []`, its two siblings in `COMPOUND_STATE_KEYS`
(`:2931-2934`) — so `verify_compound_value_reads()` and the existing `get_value()` read at `:919`
stay untouched (Pitfall 5).

**Docstring convention to copy** — `seed_panic_escape()`'s docstring names the mechanism *and* the
failure it prevents, and cites `.claude/CLAUDE.md` §5 on out-of-bounds attachment ranges. Every
seeder in this file does this; a bare one-liner would be the odd one out.

---

### `verify_active_session_seed()` (build guard) — NEW

**Analog:** `verify_pending_exit_seed()`, `tools/build_state_engine.py:2597-2617` — **quoted in full**:
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

Four load-bearing conventions, all mandatory:
1. **The two-step placeholder substitution** `.replace('"￼"', '"x"').replace("￼", "0")` before
   `json.loads`. All three existing verifiers do exactly this; a raw parse raises (one placeholder
   is an unquoted boolean).
2. **`raise SystemExit`, never `assert`** — the message *is* the diagnostic.
3. **The message names the concrete failure it prevents**, with the device error text where one
   exists. `verify_active_session_seed()` should cite the SESS-07 / SAFE-01 consequence measured in
   RESEARCH: a hard error before `close_pipeline():1306` leaves brightness/volume un-restored.
4. **Assert against the seed constant**, so the seeder and the guard cannot silently agree on being
   wrong — stated in three separate docstrings as this project's convention.

**Additional assertions to copy from `verify_panic_escape_seed()`** `:2664-2705`, which goes beyond
seed-shape into read/gate shape — the model for asserting `active_session`'s gate conversion actually
landed:
```python
    dotted, existence = [], []
    for index, item in enumerate(actions):
        identifier = item.get("WFWorkflowActionIdentifier")
        parameters = item.get("WFWorkflowActionParameters", {})
        if identifier == "is.workflow.actions.getvalueforkey":
            key = _dictionary_key_string(parameters)
            if PANIC_ESCAPE_KEY in key and key != PANIC_ESCAPE_KEY:
                dotted.append((index, key))
        if identifier == "is.workflow.actions.conditional" and parameters.get("WFControlFlowMode") == 0:
            name = parameters.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")
            if name == "Panic Escape Enabled" and parameters.get("WFCondition") not in NUMERIC_CONDITION_CODES:
```
Its three-numbered-assertion docstring form (`(1) … (2) … (3) …`, each naming the failure it
prevents) is the docstring template for a multi-assertion verifier.

---

### `verify_exit_events_seed()` (build guard) — NEW

**Analog:** same `verify_pending_exit_seed()` skeleton; the assertion collapses to
`seed.get("exit_events") != []` (plus `exit_selection_counter == 0` if seeded). Message must cite
STATE-12 — "the versioned document must declare its rolling windows" — and the `recent_sessions` /
`recent_contracts` precedent, not a crash claim (RESEARCH downgrades that to `[ASSUMED]` A1).

---

### `verify_state_seed()` — MODIFY (the generalisation; highest-leverage change in the phase)

**Analog:** itself, `tools/build_state_engine.py:2496-2557`. The change is a **deletion** at
`:2523-2526`. Current scan, verbatim:
```python
    read_keys = set()
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.getvalueforkey":
            continue
        key = item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey")
        # Composite keys are built from a token and cannot be resolved statically; none
        # of them is rooted at settings_snapshot, and that is asserted rather than assumed.
        if isinstance(key, str) and key.split(".")[0] == "settings_snapshot":
            read_keys.add(key)
        elif not isinstance(key, str) and "settings_snapshot" in str(key):
            raise SystemExit("a settings_snapshot read uses a composite key and cannot be verified")
```
Drop the `key.split(".")[0] == "settings_snapshot"` filter. The paired composite-key assertion
(`elif`) must then **tolerate** the legitimate `exit_stats.<token>` composites that
`complete_pending_exit()` `:1044,:1052-1057` builds with `text_token()` — today it only fires on
composites mentioning `settings_snapshot`, and an unguarded generalisation would fail the build on
those five legitimate sites.

The resolution loop and the error message below it (`:2527-2540`) are already whole-class and need
no change — note in particular that the message already states the governing semantic:

```python
    if missing:
        raise SystemExit(
            "bootstrap state.json does not establish every settings_snapshot key that is "
            "read (Get Dictionary Value on a missing key is a HARD RUNTIME ERROR, so a "
            "condition-100 guard cannot protect the read): "
            + ", ".join(sorted(set(missing))))
```
Widen the wording from "every settings_snapshot key" to "every state key" in the same edit.

The `wanted` sentinel-value assertion at `:2541-2557` is `settings_snapshot`-specific and stays as
is; the per-key seeds for the new keys are asserted by their own `verify_*_seed()` functions.

---

### `record_exit_and_route()` gate conversion (generator pipeline fn)

**Analog:** `complete_pending_exit()`, `tools/build_state_engine.py:1036-1038` — the exact idiom all
six `active_session` gate sites converge on:
```python
    a += read_value("pending_exit.type", variable("State"), "Pending Exit Type")
    pending_group, pending = if_block("Pending Exit Type", 5, string=CLEARED_SENTINEL)
    a += [pending] + read_value("pending_exit.timestamp", variable("State"), "Pending Exit Timestamp")
```

**Current shape to convert, verbatim** — `record_exit_and_route()` `:900-904`:
```python
    a += reload_state() + read_value("active_session", variable("Reloaded State"), "Exit Active Session")
    active_group, active = if_block("Exit Active Session", 100)
    a += [active] + read_value("active_session.id", variable("Reloaded State"), "Exit Owner ID")
    owner_group, owner = if_block("Exit Owner ID", 4, string="captured-session-placeholder")
    owner["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID")
```
Converted: the `.id` read *becomes* the gate — `if_block("Exit Owner ID", 5, string=CLEARED_SENTINEL)`
— the flat container read and its condition-100 conditional both disappear, and `Exit Owner ID` is
reused unchanged by the ownership comparison. One read, one conditional. **Every `end_if(active_group)` /
`otherwise(active_group)` pairing must be deleted with it** — the tail at `:947` closes both groups.

**Identical conversion, five more sites** (all measured this session, all the same before-shape):

| Site | Line | Variables | Note |
|---|---|---|---|
| `persist_contract()` | `:563-565` | `Contract Active Session` → `Contract Owner ID` | Renders **11×** via `primitive_dispatch()` — one edit, 22 emitted offenders removed |
| `close_pipeline()` entry gate | `:1236-1240` | `Entry Active Session` → `Captured Session ID`, `Captured Start` | Reads two leaves inside the arm; gate on `Captured Session ID` |
| `close_pipeline()` reload gate | `:1249-1251` | `Reloaded Active Session` → `Reloaded Session ID` | The ownership compare at `:1252-1254` is unchanged |
| `route_exit()` Create branch | `:873` | `Create Owner ID` | **Dotted read with no enclosing container gate at all** — add the leaf gate, don't remove one |
| `close_pipeline()` `.declared_duration_seconds` | `:1261` | `Declared Duration` | Inside the owner arm; seed makes it safe |

**⚠ V3 (ASVS) constraint.** The ownership check `if_block(…, 4, string=token("Session ID"))` at all
four owner sites is what prevents a superseded CLOSE from writing state. It is **not** the gate being
converted, and this phase must not weaken it. Note the two-line `WFConditionalActionString` idiom
(`= "￼"` then `= token(...)`) that `persist_contract():566-567` and `close_pipeline():1253-1254`
both use — preserve it verbatim where it exists.

---

### `open_pipeline()` container write → three leaf writes

**Analog for the target shape:** `persist_contract()` `:569-570` — leaf writes under a permanent container:
```python
    a += [owns, set_value("active_session.intention", variable("Confession Intention"), "Reloaded State"),
          set_value("active_session.declared_duration_seconds", variable("Declared Duration Seconds"), "Reloaded State")]
```

**Current shape to replace, verbatim** — `open_pipeline()` `:1183-1188`:
```python
    session_text = text_token([('{"id":"', "Session ID"), ('","started_at":', "Now Epoch"), (',"declared_duration_seconds":0}', None)])
    session_json = uid()
    a += [action("is.workflow.actions.gettext", UUID=session_json, WFTextActionText=session_text),
          action("is.workflow.actions.detect.dictionary", UUID=uid(), WFInput=output(session_json, "Text"))]
    # Detect Dictionary output cannot safely be re-derived from action position: name it immediately.
    a += [set_var("Active Session Next", output(a[-1]["WFWorkflowActionParameters"]["UUID"], "Dictionary")), set_value("active_session", variable("Active Session Next"))]
```
Rewritten as three `set_value("active_session.<leaf>", …)` calls this **removes** the
`gettext` + `detect.dictionary` + `set_var` trio — a net reduction in action count, no new
identifiers, and it eliminates the last wholesale container replacement. `normalize_setters()`
`:2105` supplies the required full-dictionary rebind for each new setter automatically
(`docs/state_engine_self_check.py:96-101` asserts that rebind exists for *every* setter).

---

### `live_ice_redirect()` / `manual_emergency_restore()` clears

**Analog:** `complete_pending_exit()`'s leaf clear, `tools/build_state_engine.py:1058-1061` —
including the comment, which states the rule:
```python
          # Clear the LEAF, never the container -- clear_snapshot()'s own established
          # rule. .timestamp is deliberately left stale: it is read nowhere outside this
          # same branch, which this very clear makes unreachable on the next OPEN.
          set_value("pending_exit.type", cleared_value()),
```

**Three current container clears to convert** (all `set_value("active_session", cleared_value())`):
`close_pipeline():1301` (`"Reloaded State"`), `live_ice_redirect():1812`, `manual_emergency_restore():1893`.
Each becomes `set_value("active_session.id", cleared_value(), …)`. The clear must write the
**sentinel**, never `""` — `restore_managed_settings()`'s docstring `:467-479` records that code 5
was verified and rejected for the snapshot leaves precisely because `is not "null"` is TRUE for `""`.

---

### `main()` registration (orchestration)

**Analog:** `tools/build_state_engine.py:3683-3688` — verbatim, including the ordering comment
that makes it load-bearing (Pitfall 3):
```python
    seed_settings_snapshot(actions)
    seed_pending_exit(actions)
    # Must run BEFORE fix_state_rebind(): the rebind pass also edits the same template
    # token, and seeding a new field is the reason the schema_version bump below exists.
    seed_panic_escape(actions)
    fix_state_rebind(actions)
```
Both new seeders go **before** `fix_state_rebind(actions)`.

**Verify chain, verbatim** — `:3718-3723`:
```python
    verify_state_seed(actions)
    verify_pending_exit_seed(actions)
    verify_panic_escape_seed(actions)
    verify_restore_gates(actions)
    verify_sentinel_gates(actions)
    verify_compound_value_reads(actions)
```
The two new verifiers slot in alongside `verify_pending_exit_seed` / `verify_panic_escape_seed`.
Every guard raises `SystemExit` **before** the single `SOURCE.write_bytes()`.

---

### `tools/build_sentient.py` — import + arm

**Analog:** its own import block `:13-27` (alphabetically sorted, one symbol per line) and its
arming site, verbatim `:296-303`:
```python
    # Sentient INHERITS the seeded bootstrap template from the built Dumb source rather
    # than re-seeding it, so the assertion is the whole point here: it proves the subtree
    # survived the fork, and it fails loudly if a future Sentient-only insertion ever adds
    # a settings_snapshot read that the shared bootstrap does not establish.
    verify_state_seed(actions)
    # Cycle 12, axis 7 -- GATE SEMANTICS.  Sentient inherits the restore block and every
    # sentinel write from Dumb, so these assert the fork did not lose them; and because
    # Sentient adds its own conditionals, they also cover any Sentient-only gate that a
    # future insertion puts over a sentinel-written key.  A brightness/volume write reached
    # with an empty value is a black screen, so this is asserted per fork, never inferred.
    verify_restore_gates(actions)
    verify_sentinel_gates(actions)
```
**Copy the "inherits, therefore assert per fork" comment idiom** — it is stated three times in this
file and is the stated justification for the whole subset. **Confirmed this session:** the import
list contains exactly 13 symbols and does **not** include `verify_pending_exit_seed`,
`verify_panic_escape_seed`, `verify_compound_value_reads` or `verify_conditional_action_string`
(Pitfall 6). Arm the two new verifiers on both forks; closing the pre-existing gap is a scope call.

---

### `docs/state_engine_self_check.py:92` — required literal edit

**The assertion that breaks by construction, verbatim** `:91-93`:
```python
    keys = [action["WFWorkflowActionParameters"]["WFDictionaryKey"] for _, action in setters]
    for required in ("heat", "gravity", "pressure", "circle", "active_session", "recent_sessions", "last_close_at"):
        assert required in keys
```
`keys` holds literal key strings, so membership is exact — `"active_session.id"` will **not** satisfy
`"active_session"`. Update the tuple in the same commit and add a comment naming why the literal
moved (`.planning/STATE.md`'s structurally-derived-exemption convention). Failure mode is a bare
`AssertionError` with no message — this file uses `assert`, not `require()`.

---

### `SCHEMA_VERSION` 3→4

**Analog:** the constant block itself, `tools/build_state_engine.py:3557-3562`, verbatim:
```python
SCHEMA_VERSION = "3"
SCHEMA_VERSION_PREVIOUS = "2"
# The RECOGNITION tuple.  It must admit every literal this transformer has ever written --
# including the one it is about to write -- or the NEXT build fails to locate the
# conditional and aborts, one build downstream of the change that caused it.
SCHEMA_VERSION_ACCEPTED = ("1", "2", "3")
```
Three literals, one commit (Pitfall 7 — missing the recognition tuple fails the *next* build, not
this one). `fix_state_rebind()`'s docstring `:3595-3599` is the precedent that the bump is licensed
("there is no installed base") — **re-confirm that before bumping** (Assumption A3).

## Shared Patterns

### Never hand-author a plist dict — use the four emitters
**Source:** `read_value()` `:273`, `get_value()` `:233`, `set_value()` `:284`, `if_block()` `:294`
**Apply to:** every emitted action this phase adds or moves.
A change expressed purely through these four inherits all seven parameter-defect axes for free via
the normalise/verify chain. A hand-authored dict inherits none of them. In particular:
`set_value()` uses `WFDictionaryValue` (not `WFInput`); `if_block()` gets the
`WFTextTokenAttachment`-not-`WFTextTokenString` variable slot right; `get_value()` omits the
`gettext` step that would stringify a compound Array.

### Template edits go through `_replace_in_token()` — never `str.replace`
**Source:** `tools/build_state_engine.py:2453-2478`
**Apply to:** both new seeders.
```python
    string = inner["string"]
    at = string.find(old)
    if at < 0:
        raise SystemExit(f"state template does not contain {old!r}")
    delta = len(new) - len(old)
    inner["string"] = string[:at] + new + string[at + len(old):]
    shifted = {}
    for key, attachment in inner.get("attachmentsByRange", {}).items():
        offset, length = (int(part) for part in key.strip("{}").split(","))
        if offset > at:
            offset += delta
        shifted[f"{{{offset}, {length}}}"] = attachment
    inner["attachmentsByRange"] = shifted
    for key in inner["attachmentsByRange"]:
        offset, _ = (int(part) for part in key.strip("{}").split(","))
        if inner["string"][offset] != "￼":
            raise SystemExit(f"attachment offset {offset} no longer points at a placeholder")
```
Four attachments live in this template (offsets 57 / 105 / 182 / 1395); the last sits after every
proposed insertion point, so **every** Phase 12 template edit moves it.

### The seeder / verifier separation is a convention, stated in three docstrings
**Source:** `verify_pending_exit_seed()` `:2600-2601`, `verify_state_seed()` `:2502-2504`,
`verify_panic_escape_seed()` `:2677-2679`
**Apply to:** both new pairs. Never fold the assertion into the seeder — "the two cannot silently
drift" is the entire reason the guard exists.

### Idempotency is a checked property
**Source:** `docs/phase6_self_check.py:45-49` builds twice and requires byte-identical output.
**Apply to:** both new seeders — each needs the substring early-return, with a collision-free guard
token (`'"exit_events"'` ✓, `'"active_session": {'` ✓, `'"id"'` ✗).

### Sentinel vs empty — never seed `""`
**Source:** `verify_state_seed()` `:2545-2557` and `verify_restore_gates()` `:2836-2846`
```python
        if node != CLEARED_SENTINEL:
            raise SystemExit(f"{key} is seeded as {node!r}; it must be the cleared sentinel "
                             f"{CLEARED_SENTINEL!r} -- an EMPTY seed passes `has any value` "
                             "(Donor 6.1) and a fabricated number could restore a setting the "
                             "user never had")
```
Condition 5 is correct for `active_session.id` **only because** the seed guarantees a non-empty
sentinel. Seed one leaf as `""` and that reasoning collapses.

### `verify_sentinel_gates()` self-heals — do not weaken it
**Source:** `tools/build_state_engine.py:2877-2917`; the constant it reads, `:217`.
The guard's two rules run against `_sentinel_written_keys()` `:2750`. After the refactor
`active_session.id` is sentinel-written instead of `active_session`; no read of
`active_session.id.<anything>` exists (rule 2 clean) and no condition-100 gate stands over a variable
read from `active_session.id` (rule 1 clean). `KNOWN_SENTINEL_EXISTENCE_GATES = ()` then holds
honestly. **Update the docstring `:2883-2886`** — it currently says "only active_session remains,
deliberately" — and the 24-line note at `:193-216`, which will be describing a closed defect.

## No Analog Found

| Symbol | Role | Data Flow | Reason |
|---|---|---|---|
| `profile_snapshot.create_target_url` seed + its `:866` gate | seeder + gate | CRUD | The seed line itself has an analog (`seed_settings_snapshot`), but the **sentinel-vs-JSON-`null` choice** does not: this is the one place where the choice interacts with an existing condition-100 gate (`route_exit():866`) that must read **false** when unset. The sentinel is present and non-empty → gate reads TRUE → `openurl` on the string "null". Whether `read_value()` of a JSON-`null` leaf yields no-value or the text `"null"` is **not settled by any document in this repo**. Research Open Question 2: seed `null` **and** convert the gate to the sentinel/numeric discipline, **or** defer the key to its own todo. Do not guess. |
| `12-UAT.md` device exit-path test | test doc | manual | The exit-recording path has **zero** device evidence at any rung; Phase 10's UAT was blocked. Plan the blocked branch explicitly. The Phase 10 precedent for a blocked UAT is the analog for the *document*, not for any code. |
| rung-2 simulator probe for `repeat.each` over absent input | probe shortcut | — | Assumption A1. No probe-shortcut analog exists in this repo. Optional; the seed fixes it either way. |

## Metadata

**Analog search scope:** `tools/build_state_engine.py` (3742 lines, targeted non-overlapping reads at
`:190-230`, `:556-575`, `:860-950`, `:1020-1069`, `:1180-1192`, `:1230-1265`, `:1296-1312`,
`:1806-1816`, `:1886-1896`, `:2415-2705`, `:2825-2975`, `:3676-3730`), `tools/build_sentient.py`,
`docs/state_engine_self_check.py`
**Symbol index built by:** `grep -n "^def \|^CONST"` over `tools/build_state_engine.py`
**Anchor re-verification:** all 12 analog anchors confirmed at the line numbers `12-RESEARCH.md`
cites; **zero corrections needed**
**Pattern extraction date:** 2026-08-17
