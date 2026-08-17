# Phase 12: State-shape sentinel gaps — exit_events and active_session - Research

**Researched:** 2026-08-17
**Researched at commit:** `9275a4e` (clean tree)
**Domain:** Codebase-internal — the `tools/build_state_engine.py` generator, the bootstrap
`state.json` template inside `src/PROSOCHE-Dumb.xml`, and the `docs/*.py` structural checkers
**Confidence:** HIGH (every claim below is a measurement taken this session against the live
tree; nothing is quoted from training data, and no external source was consulted)

## Summary

This phase is not a research problem — it is a **measurement** problem, and the measurements
are now done. Every anchor named by the ROADMAP exists, and each one was located, read and
quoted. The container/leaf pattern the phase must mirror is real, is implemented twice
(`settings_snapshot`, `pending_exit`) and three times counting the flat/numeric variant
(`panic_escape_enabled`), and the enforcing guard (`verify_sentinel_gates()`) is written so
that **the fix mechanically dissolves its own exemption** — once `active_session` stops being
written wholesale with the sentinel, its dotted reads become legal and `KNOWN_SENTINEL_EXISTENCE_GATES`
can be emptied without weakening anything.

Three findings materially change the shape of the plan versus what the ROADMAP assumed.
**First**, the two keys are **not** symmetrical: `active_session` is a genuine 34-site
container/leaf defect, while `exit_events` is a one-line array seed with **no gate and no
dotted read at all** — its stated crash risk does not survive contact with the verified iOS
semantics. **Second**, the full-codebase sweep the ROADMAP asked for found a **third key in
the same defect class that nobody named**: `profile_snapshot.create_target_url` is a DOTTED
read of a leaf absent from the bootstrap seed, sitting on `route_exit()`'s Create branch —
i.e. on the exact exit path this phase is chartered to make survivable. **Third**, the
container/leaf refactor **breaks `docs/state_engine_self_check.py:92` by construction**,
because that checker asserts the literal string `"active_session"` appears among the
`setvalueforkey` keys, and the refactor removes every bare-key write.

**Primary recommendation:** Treat this as one class fix, not two key fixes. Seed
`active_session` as a four-leaf permanent container and `exit_events` as `[]` (plus
`exit_selection_counter: 0` and `profile_snapshot.create_target_url` for completeness), bump
`schema_version` 3→4 through all three coupled literals, convert the six generator sites that
gate on container existence to leaf-value gates, empty `KNOWN_SENTINEL_EXISTENCE_GATES`, and
— the highest-leverage change available — **generalise `verify_state_seed()`'s read-side scan
from `settings_snapshot`-rooted keys to every literal key read from `State`/`Reloaded State`**,
which turns this whole defect family into a build error instead of a device error, permanently.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Bootstrap `state.json` shape | Generator text-edit layer (`_state_template` + `_replace_in_token`) | — | The template is one `WFTextTokenString` inside action 75 of `src/PROSOCHE-Dumb.xml`; only the offset-shifting text editor may touch it |
| Seed establishment | `seed_*` transformer functions in `tools/build_state_engine.py` | — | Idempotent, content-anchored, run before the verify chain in `main()` |
| Seed assertion | `verify_*_seed` build guards | — | Deliberately separate from the seeder so the two cannot silently drift (project convention, stated in three docstrings) |
| Read/write/clear gates | Generator pipeline functions (`open_pipeline`, `close_pipeline`, `record_exit_and_route`, `persist_contract`, `live_ice_redirect`, `manual_emergency_restore`) | — | Gate semantics are an emitted-plist property; nothing at runtime can repair them |
| Cross-fork enforcement | `tools/build_sentient.py`'s import list + verify chain | `tools/build_state_engine.py` | Sentient inherits the seeded template from the built Dumb source but re-asserts per fork |
| Structural regression detection | `docs/*.py` checker suite (12 scripts) | — | The only "test suite" this project has; run as bare `python3 docs/<name>.py` |
| Runtime behaviour proof | Real iPhone (evidence rung 3–4) | iOS Simulator (rung 2) | Exit-recording path has **never** been device-exercised |

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Binding project constraints that are NOT discretionary (from `.claude/CLAUDE.md`):
- Build provenance gate: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running `tools/build_state_engine.py` or `tools/build_sentient.py`.
- Two-gate validation: gate A (`--target-macos 26 --target-platform all`) is mandatory and must pass clean; gate B (`--target-macos 27 --target-platform all`) is advisory with exactly one permitted waived line per fork.
- Never fabricate an action identifier, parameter key, or enum literal. If it cannot be verified, use the safest fallback and record the deviation.
- Signed artifacts must carry the exact display names `PROSOCHĒ — Nine Circles — Dumb.shortcut` / `— Sentient.shortcut`, no `_signed` suffix.

### Claude's Discretion

All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

### Deferred Ideas (OUT OF SCOPE)

None — discuss phase skipped.
</user_constraints>

> **⚠️ One locked decision is stale and the planner must not copy it forward verbatim.**
> The last bullet names `Dumb.shortcut` / `Sentient.shortcut`. Phase 11 plan 06 **renamed the
> shipped products**. Measured this session: `src/PROSOCHE-Dumb.xml` carries
> `WFWorkflowName = "PROSOCHĒ — Nine Circles — Core"` and `src/PROSOCHE-Sentient.xml` carries
> `"PROSOCHĒ — Nine Circles — Aware"`; `docs/manifest_check.py:44-48` hard-codes exactly those
> two as `DISPLAY_NAMES`, and `artifacts/shortcuts/` contains
> `PROSOCHĒ — Nine Circles — Core.shortcut` and `PROSOCHĒ — Nine Circles — Aware.shortcut`.
> The *rule* (exact display name, no suffix) is unchanged and still binding; only the two
> literals moved. `.claude/CLAUDE.md` was not updated with the rename and is the source of the
> stale text. [VERIFIED: `plistlib` read of both sources + `ls artifacts/shortcuts/` + `docs/manifest_check.py:44-48`]

<phase_requirements>
## Phase Requirements

| ID | Description (verbatim from REQUIREMENTS.md) | Research Support |
|----|-------------|------------------|
| STATE-12 | "State is persisted as a bounded, versioned JSON document with rolling windows for sessions, contracts, and per-exit aggregates — no unbounded arrays, no CSV" | `exit_events` is a rolling window (cap 20, `record_exit_and_route()` `:921-925`) that the *versioned document does not declare*. Seeding `"exit_events": []` is what makes the requirement literally true. The schema bump 3→4 is the "versioned" half. §"The exit_events gap" below. |
| SESS-07 | "CLOSE restores any environmental setting PROSOCHĒ itself changed during the session" | `restore_managed_settings("Reloaded State")` is reached **only inside** `close_pipeline()`'s `Reloaded Active Session` / `Reloaded Session ID` ownership arms (`:1250-1258`, restore at `:1306`). Both arms are `active_session`-gated, so an `active_session` shape defect is a *safety* defect: a hard error before `:1306` leaves brightness/volume un-restored. §"Why active_session is a SAFE-01/SESS-07 issue". |
| EXIT-01 | "Capture routes to an idea-externalising target (notes, voice memo, or camera)" | Capture is routed by `route_exit()` `:844`, reached only through `record_exit_and_route()`, which is gated by the `active_session` container test at `:901`. §"Site inventory". |
| EXIT-02 | "Coordinate routes to a planning target (reminders, calendar, or task list)" | Same gate, same function, `route_exit()` `:845`. Additionally the sibling Create route at `:865` carries the newly-found `profile_snapshot.create_target_url` dotted-read defect. |
| SAFE-01 | "Brightness is never set to zero" | Enforced by `verify_restore_gates()` `:2835-2874` (numeric `> 0` gate over every state-derived brightness/volume write). This phase must not disturb it, and the sweep confirms the settings_snapshot leaves it depends on are correctly seeded. §"Regression surface". |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

Extracted as actionable directives; the planner must verify compliance against each.

| # | Directive | Where it bites in Phase 12 |
|---|-----------|----------------------------|
| C1 | Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` must exit 0 before either builder runs | **Measured PASS this session** (exit 0 at `9275a4e`). Re-run before each builder invocation. |
| C2 | Gate A `validate-shortcut <f> --target-macos 26 --target-platform all` mandatory, must print `Validation passed.` exit 0 | **Measured baseline this session: PASS on both forks.** |
| C3 | Gate B `--target-macos 27 --target-platform all` advisory; exactly one permitted waived line per fork; never chained into a definition of done | **Measured baseline this session: exit 1 on both forks with exactly the one waived `WFCreateNoteInput` line** (Dumb index 4302, Sentient index 4370). Any *other* line after this phase is a real finding. |
| C4 | Never pair `--target-platform ios` with `--target-macos 26` | Empty allowlist, 3675/3675 rejections. Never use. |
| C5 | Never fabricate an action identifier, parameter key or enum literal | This phase introduces **zero new identifiers and zero new parameter keys** — see §"Don't Hand-Roll". |
| C6 | Signed artifact basename = exact display name, no suffix | Current canonical names are **Core** / **Aware** (see the stale-decision box above). |
| C7 | Seven parameter-defect axes are asserted by build guards | New `set_value`/`read_value` calls inherit all seven automatically via the existing normalise/verify chain. Do **not** hand-author plist dicts. |
| C8 | Dotted read with any missing segment = HARD ERROR; flat read of missing key = returns nothing, no error | The single semantic fact this entire phase turns on. |
| C9 | Evidence hierarchy: device > simulator > golden corpus > `.intentdefinition` > ToolKit catalog > inference | The exit-recording path has **no** device evidence at any rung. |
| C10 | `/ponytail` laziness sanctioned, but never licenses skipping the seven axes or the do-not-fabricate protocol | Argues for the minimal template edit + guard generalisation, not a rewrite. |

## Standard Stack

No external packages. This is a pure-stdlib Python 3 generator plus two macOS-only CLI wrappers.

### Core
| Component | Version (measured) | Purpose | Why standard |
|-----------|--------------------|---------|--------------|
| Python | **3.13.9** (`python3 --version`) | Runs the generators and all 12 checkers | `validate_shortcut.py` needs ≥3.10 (PEP 604); 3.13.9 comfortably clears it |
| `plistlib` (stdlib) | — | The **only** sanctioned plist parse/serialise path | `main()` does exactly one parse and exactly one write; no third-party plist lib exists in this repo |
| `json` (stdlib) | — | Parses the bootstrap template after placeholder substitution | Used identically by all three existing `verify_*_seed()` functions |
| `validate-shortcut` | Shortcuts Playground 1.2.1 | Gates A and B | Present and executable at `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/bin/validate-shortcut` |
| `sign-shortcut` | Shortcuts Playground 1.2.1 | Produces the importable AEA1 archive | Same directory; macOS-only |

### Supporting
| Component | Purpose | When to use |
|-----------|---------|-------------|
| `tools/plist_text_edit.py` (197 lines) | Standalone six-step offset-shifting token editor | Only when editing a token *outside* `build_state_engine.py`; inside it, use `_replace_in_token()` |
| `aea decrypt` + `aa extract` | Recover the plist from a signed `.shortcut` | Post-sign verification that what shipped is what was built |
| `docs/manifest_check.py` | Hash/size-verifies every declared artifact against disk | After signing, before declaring done |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| One `seed_*` + one `verify_*_seed` per key (established pattern) | A single generic `STATE_SEED` registry driving one seeder and one verifier | Fewer functions, but it rewrites three working, device-evidenced guards and their docstrings — a large diff for no new coverage. **Recommend keeping the per-key pattern** and adding coverage via the generalised read-side scan instead (below). |
| Scoping the read-side scan to the two new keys | Generalising `verify_state_seed()`'s scan to **all** literal `State`/`Reloaded State` reads | The general form is *smaller code* (delete one `if key.split(".")[0] == "settings_snapshot"` filter) and catches `profile_snapshot.create_target_url`, which the scoped form misses. **Strongly recommended.** |
| Leaf-gating `active_session.id` | Keeping the container gate and adding a nested leaf gate | Two conditionals where one suffices, and `complete_pending_exit()` `:1036-1038` already proves the one-conditional form. |

**Installation:** none. No package is added, removed or upgraded by this phase.

## Package Legitimacy Audit

**Not applicable — this phase installs no external packages.** The entire change surface is
`tools/build_state_engine.py`, `tools/build_sentient.py`, `src/PROSOCHE-*.xml` (generated),
and `docs/*.py`. All imports in scope are Python standard library (`json`, `plistlib`,
`pathlib`, `hashlib`, `uuid`, `re`, `subprocess`, `tempfile`, `os`) — verified by reading the
import blocks of `tools/build_state_engine.py:1-14` and `tools/build_sentient.py:1-27`.

## Architecture Patterns

### System Architecture Diagram

```
                         ┌──────────────────────────────────────┐
   git provenance gate ─▶│  git merge-base --is-ancestor 7ca8ebb│──fail──▶ ABORT
   (C1)                  └────────────────┬─────────────────────┘
                                          │ exit 0
                                          ▼
  src/PROSOCHE-Dumb.xml ──plistlib.loads──▶  tools/build_state_engine.py  main()
  (4456 actions, incl.                       │
   the bootstrap template                    │  ① STRUCTURAL REPLACEMENT
   at action 75)                             │     replace_branch_body(OPEN → open_pipeline())
                                             │     replace_branch_body(CLOSE → close_pipeline())
                                             │     install_cooldown_branches / manual blocks
                                             │     restructure_router
                                             ▼
                                          ② SEEDING  ◀── PHASE 12 EDITS LAND HERE
                                             seed_settings_snapshot()   :2481
                                             seed_pending_exit()        :2570
                                          ▷  seed_exit_events()          NEW
                                          ▷  seed_active_session()       NEW
                                             seed_panic_escape()        :2645
                                             fix_state_rebind()         :3618  ← schema 3→4
                                             │      (all five mutate ONE WFTextTokenString
                                             │       through _replace_in_token(), which
                                             │       shifts every attachmentsByRange offset
                                             │       and re-asserts each lands on U+FFFC)
                                             ▼
                                          ③ NORMALISATION (7 axes, order-sensitive)
                                             normalize_setters → normalise_string_envelopes
                                             → normalise_output_names → normalise_numeric_operands
                                             ▼
                                          ④ VERIFY CHAIN (18 guards, any raises SystemExit
                                             BEFORE the single SOURCE.write_bytes())
                                             verify_state_seed          :2496 ◀ generalise
                                             verify_pending_exit_seed   :2597
                                          ▷  verify_exit_events_seed     NEW
                                          ▷  verify_active_session_seed  NEW
                                             verify_sentinel_gates      :2877 ◀ deferred set → ()
                                             verify_restore_gates / …
                                             ▼
                            ──── exactly one write ────▶ src/PROSOCHE-Dumb.xml
                                             │
                                             ▼
                    tools/build_sentient.py (reads the BUILT Dumb source, forks additively,
                    re-runs a 13-guard SUBSET per fork) ──▶ src/PROSOCHE-Sentient.xml
                                             │
                                             ▼
                    12 × python3 docs/<checker>.py   ──▶ pass/fail
                                             │
                                             ▼
                    gate A (mandatory) → gate B (advisory) → sign-shortcut --name
                                             │
                                             ▼
                    artifacts/shortcuts/ + MANIFEST.md + docs/manifest_check.py
                                             │
                                             ▼
                    DEVICE: a real "leave and confirm exit" on the iPhone (rung 3/4)
```

### Recommended change surface
```
tools/
├── build_state_engine.py   # 2 new seeders, 2 new verifiers, 1 generalised verifier,
│                           #  1 emptied constant, 6 gate conversions, 3 schema literals
└── build_sentient.py       # import + arm the 2 new verifiers (see Pitfall 6)
src/
├── PROSOCHE-Dumb.xml       # GENERATED — never hand-edit
└── PROSOCHE-Sentient.xml   # GENERATED — never hand-edit
docs/
├── state_engine_self_check.py  # :92 REQUIRED EDIT — breaks by construction (Pitfall 1)
└── phase6_self_check.py        # :56-57 verify still satisfied (substring, likely fine)
```

### Pattern 1: Container/leaf split — the exact template to mirror
**What:** A key that is (a) dotted-read and (b) cleared, must have its **container** seeded
once and never replaced wholesale; only **leaves** are written and cleared, and the "is it
set?" gate tests a **leaf value** (condition 5 vs `CLEARED_SENTINEL`), never container
existence (condition 100).

**When to use:** `active_session`. (**Not** `exit_events` — see Pattern 2.)

**The seeder, quoted verbatim** — `tools/build_state_engine.py:2566-2594`:
```python
PENDING_EXIT_SEED = {"type": CLEARED_SENTINEL, "timestamp": CLEARED_SENTINEL}
PENDING_EXIT_ANCHOR = '"active_session": null,'


def seed_pending_exit(actions):
    """Establish pending_exit as a permanent {type, timestamp} container in bootstrap.
    ...
    Idempotent: a second run finds "pending_exit" already in the template and returns;
    verify_pending_exit_seed() re-proves the shape either way.
    """
    _, inner = _state_template(actions)
    if '"pending_exit"' in inner["string"]:
        return  # already seeded; verify_pending_exit_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PENDING_EXIT_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    leaves = ", ".join(f'"{leaf}": "{value}"' for leaf, value in PENDING_EXIT_SEED.items())
    _replace_in_token(inner, PENDING_EXIT_ANCHOR,
                      PENDING_EXIT_ANCHOR + f'\n{indent}"pending_exit": {{{leaves}}},')
```

**The verifier, quoted verbatim** — `tools/build_state_engine.py:2597-2617`:
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

**The consumer-side gate this produces, quoted verbatim** — `complete_pending_exit()`
`tools/build_state_engine.py:1036-1038`, the exact shape `active_session`'s six gates must
converge on:
```python
    a += read_value("pending_exit.type", variable("State"), "Pending Exit Type")
    pending_group, pending = if_block("Pending Exit Type", 5, string=CLEARED_SENTINEL)
    a += [pending] + read_value("pending_exit.timestamp", variable("State"), "Pending Exit Timestamp")
```
Note the economy: **one** read, **one** conditional, and the read variable is reused later as
the `exit_stats.<type>` key rather than re-read. The current `active_session` sites use two
reads and two nested conditionals each; the converted form is *smaller*.

**And the clear, quoted verbatim** — `complete_pending_exit()` `:1058-1061`:
```python
          # Clear the LEAF, never the container -- clear_snapshot()'s own established
          # rule. .timestamp is deliberately left stale: it is read nowhere outside this
          # same branch, which this very clear makes unreachable on the next OPEN.
          set_value("pending_exit.type", cleared_value()),
```

### Pattern 2: Flat array seed — the correct pattern for `exit_events`
**What:** A compound (Array) state key that is read flat via `get_value()` and consumed by a
List action needs **only** an empty-array seed. No container/leaf split, no gate change.

**When to use:** `exit_events`, and its already-correct siblings.

**The precedent, quoted from the live template** (action 75 of `src/PROSOCHE-Dumb.xml`):
```json
  "recent_sessions": [],
  "recent_contracts": [],
```
Both are members of `COMPOUND_STATE_KEYS` (`:2931-2934`) alongside `exit_events`; both are
seeded `[]`; `exit_events` is the only one of the three that is not. The correct fix is one
line, anchored the same way the other seeders anchor.

### Pattern 3: The three coupled schema-version literals
**What:** Adding or changing a bootstrap field requires forcing every device to rebuild
`state.json` once, which is done by bumping `schema_version` — and the bump is **three**
literals that must move in the same commit.

**Quoted verbatim** — `tools/build_state_engine.py:3557-3562`:
```python
SCHEMA_VERSION = "3"
SCHEMA_VERSION_PREVIOUS = "2"
# The RECOGNITION tuple.  It must admit every literal this transformer has ever written --
# including the one it is about to write -- or the NEXT build fails to locate the
# conditional and aborts, one build downstream of the change that caused it.
SCHEMA_VERSION_ACCEPTED = ("1", "2", "3")
```
For Phase 12: `SCHEMA_VERSION = "4"`, `SCHEMA_VERSION_PREVIOUS = "3"`,
`SCHEMA_VERSION_ACCEPTED = ("1", "2", "3", "4")`.

**The runtime gate this drives**, measured in the built artifact: action **27** reads
`schema_version` from `State`; action **37** is a condition-100 has-value test; action **39**
is `WFCondition 4` against `WFConditionalActionString = "3"`. `fix_state_rebind()` rewrites
action 39's literal from `SCHEMA_VERSION_ACCEPTED` to `SCHEMA_VERSION`.

**Precedent that the bump is licensed:** `fix_state_rebind()`'s docstring, `:3595-3599`:
> "PHASE 11 (11-05) — the version moves 2 -> 3 … BD-06-A1 Amendment 3 records that **there is
> no installed base**, so the unrecoverable loss a bump normally carries (heat, gravity,
> pressure, the rolling windows, the session record, exit_stats[*].samples) costs nothing
> here. No migration, no dual-key alias and no read-time normalisation was built; BD-06-A1
> **forbids all three by name**."

The planner should re-confirm "no installed base" still holds before bumping — it was true at
Phase 11 and nothing since has shipped to a device (Phase 10 device UAT is recorded as blocked:
`xcrun devicectl list devices` returned "No devices found.", `.planning/STATE.md`).

### Anti-Patterns to Avoid
- **Clearing the container.** `set_value("active_session", cleared_value())` at three sites is
  literally cycle-10 finding 5 replayed. `clear_snapshot()`'s docstring `:443-459` documents
  the failure: "clearing `settings_snapshot.<key>` replaced the sub-DICTIONARY with a string,
  so the very next run's dotted read of `.original_value` ran against a string parent and
  hard-errored — the identical failure the bootstrap seed exists to prevent, reintroduced one
  run later and **presenting as a regression**."
- **Read-then-`has any value` on a dotted path.** Structurally unimplementable, stated at
  `:173-177`: "the read raises unless the final key exists, and if it exists the gate is true.
  There is NO state in which the gate reads false without the read having already raised."
- **Condition 5 where empty is possible.** `restore_managed_settings()`'s docstring `:467-479`
  records that code 5 was verified and then *rejected* for the snapshot leaves because
  `is not "null"` is TRUE for empty. Code 5 is correct for `active_session.id` **only because
  the seed guarantees non-empty**; if the planner ever seeds a leaf as `""` this reasoning
  collapses. Seed with `CLEARED_SENTINEL`, never `""`.
- **Hand-editing `src/PROSOCHE-*.xml`.** Both are generator outputs; `main()` writes each
  exactly once and `build_sentient.py` asserts `"frozen Dumb source changed"` if the Dumb
  source moved during its run.
- **Hand-computing `attachmentsByRange` offsets.** `_replace_in_token()` `:2453-2478` shifts
  every offset past the edit and re-asserts each still lands on `U+FFFC`. Four attachments live
  in this template, at offsets 57 / 105 / 182 / **1395** — the last one sits *after* every
  proposed insertion point, so every Phase 12 template edit moves it.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| Editing the bootstrap template text | `str.replace` on `inner["string"]` | `_replace_in_token(inner, old, new)` `:2453` | It shifts all four attachment offsets and re-asserts each lands on `U+FFFC`; an unshifted offset points into unrelated prose and `.claude/CLAUDE.md` §5 records that an out-of-bounds range **can crash Shortcuts on import** |
| Locating the template | An action index | `_state_template(actions)` `:2438` | Content-anchored on `'"schema_version"'`; indices move on every build |
| Parsing the template as JSON | `json.loads(inner["string"])` | `inner["string"].replace('"￼"', '"x"').replace("￼", "0")` first | The template is a text template with 4 placeholders, one of them an unquoted boolean; raw parse raises. All three existing verifiers do exactly this two-step substitution |
| Emitting a dictionary read | A hand-authored `getvalueforkey` dict | `read_value()` `:273` (scalar) or `get_value()` `:233` (compound Array) | `get_value` omits the `gettext` step; using `read_value` on a compound key stringifies the array and the downstream List consumer fails with "couldn't convert Text to Dictionary" — device-confirmed cycle 15. Enforced by `verify_compound_value_reads()` `:2960` |
| Emitting a dictionary write | A hand-authored `setvalueforkey` dict | `set_value()` `:284` | It uses `WFDictionaryValue` (not `WFInput`) and `normalize_setters()` `:2105` then auto-inserts the required full-dictionary rebind. `docs/state_engine_self_check.py:96-101` asserts that rebind exists for **every** setter |
| Emitting a conditional | A hand-authored `conditional` dict | `if_block()` `:294` | `WFInput.Variable` must be a `WFTextTokenAttachment`, never a `WFTextTokenString`; 13 hand-written overwrites of this parameter went unnoticed for seven debug cycles. Enforced by `verify_conditional_inputs()` |
| Numeric operand typing | A `Number` action before the compare | `normalise_numeric_operands()` (automatic) | Donor 4.1 measured that iOS attaches a `WFCoercionVariableAggrandizement` to the operand descriptor instead. Runs automatically over new sites |
| The cleared sentinel literal | The string `"null"` inline | `CLEARED_SENTINEL` `:192` / `cleared_value()` `:220` | `_sentinel_written_keys()` `:2750` recognises sentinel writes by matching `inner.get("string") == CLEARED_SENTINEL` with no attachments; a hand-built token with an attachment is invisible to the guard |

**Key insight:** every one of the seven parameter-defect axes is already asserted by a build
guard, and every guard operates on *emitted structure*, not on call sites. A Phase 12 change
expressed purely through `set_value` / `read_value` / `get_value` / `if_block` inherits all
seven for free. A change that hand-authors a plist dict inherits none of them.

## Runtime State Inventory

This phase is a refactor of persisted state shape, so this section is mandatory.

| Category | Items found | Action required |
|----------|-------------|------------------|
| **Stored data** | One file: `PROSOCHE/state.json` in the Shortcuts iCloud folder on the user's iPhone. Its shape is defined by the bootstrap template at action 75. `schema_version` is currently `3`. | **Code edit + forced rebuild.** No data migration is written — the project explicitly forbids one (`BD-06-A1`, quoted above). The bump to `4` makes the device's `schema_version == "3"` check fail once, taking the rebuild branch and discarding heat/gravity/pressure/rolling windows/exit_stats samples. Confirm "no installed base" before accepting that loss. |
| **Live service config** | **None.** No n8n, no Datadog, no Cloudflare, no external service of any kind. PROSOCHĒ is a single on-device Shortcut; `.claude/CLAUDE.md` states "no behavioural data leaves the device." Verified: zero HTTP/network actions in the generator (`is.workflow.actions.searchweb` / `searchmaps` / `openurl` are user-initiated app launches, not data egress). | None. |
| **OS-registered state** | **Two iOS Personal Automations** (App Is Opened → run the shortcut with input `OPEN`; App Is Closed → `CLOSE`). They are user-created on the device and reference the shortcut **by display name**. | **None for this phase** — Phase 12 changes no display name and no `WFWorkflowName`. But note: they must be re-pointed if a rename ever happens, and they are the only way the exit path can be device-tested from a genuine trigger. |
| **Secrets / env vars** | **None.** No API keys, no `.env`, no SOPS, no credentials anywhere in the repo. Verified by absence of any `os.environ` read in either generator. | None. |
| **Build artifacts / installed packages** | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` and `— Aware.shortcut`, plus five dated archive directories (`2026-08-13` … `2026-08-17`), all declared with size + SHA-256 in `artifacts/shortcuts/MANIFEST.md`. `docs/__pycache__` and `tools/__pycache__` exist (harmless). | **Re-sign both forks and refresh all six MANIFEST rows**, then `python3 docs/manifest_check.py` must exit 0. A stale row is a false provenance claim, and Phase 10 measured three of six already wrong once. |

**The canonical question — after every file in the repo is updated, what runtime systems still
hold the old shape?** Exactly one: the `state.json` on the user's iPhone. The schema bump is
the mechanism that invalidates it, and it is the only mechanism the project permits.

## The two keys are not symmetrical — measured

### `active_session`: a genuine 34-site container/leaf defect

**Bootstrap seed today** (measured by extracting action 75's `WFTextTokenString`):
```json
  "active_session": null,
```
A bare JSON `null` — present, unlike `pending_exit`'s former total absence, but **not a
dictionary**. Every `active_session.<leaf>` dotted read against a fresh state file therefore
runs against a non-dictionary parent.

**Measured blast radius.** I re-implemented `verify_sentinel_gates()`'s two rules with
`KNOWN_SENTINEL_EXISTENCE_GATES` emptied, and ran them against the live built artifact:

```
OFFENDERS IF active_session REMOVED FROM DEFERRED: 34
  15 × condition-100 existence gate over a sentinel-written 'active_session'
  19 × dotted read hanging beneath sentinel-written 'active_session'
```

Those 34 emitted actions come from only **six generator functions**, because
`primitive_dispatch()` renders 11× and `record_exit_and_route()` renders 2×:

| Generator function | Line(s) | Renderings | Emitted offenders | What it does |
|---|---|---:|---:|---|
| `persist_contract()` | `:563-570` | **11** | 22 | `read_value("active_session", …, "Contract Active Session")` → `if_block(…, 100)` → `read_value("active_session.id", …)` → writes `.intention` + `.declared_duration_seconds` |
| `record_exit_and_route()` | `:900-902` | **2** | 4 | `read_value("active_session", …, "Exit Active Session")` → `if_block(…, 100)` → `read_value("active_session.id", …, "Exit Owner ID")` |
| `route_exit()` (Create branch) | `:873` | **2** | 2 | `read_value("active_session.id", …, "Create Owner ID")` — a dotted read with **no** enclosing container gate at all |
| `close_pipeline()` | `:1236-1240`, `:1249-1251`, `:1261`, `:1301` | 1 | 6 | Two condition-100 gates + `.id` ×2, `.started_at`, `.declared_duration_seconds`; clears the container at `:1301` |
| `open_pipeline()` | `:1188` | 1 | 0 (write) | `set_value("active_session", variable("Active Session Next"))` — **wholesale container replacement** |
| `live_ice_redirect()` | `:1812` | 1 | 0 (clear) | `set_value("active_session", cleared_value())` |
| `manual_emergency_restore()` | `:1893` | 1 | 0 (clear) | `set_value("active_session", cleared_value())` |

**Variables bound from `active_session*`** (measured via `_read_variable_keys()`):
`Contract Active Session`, `Exit Active Session`, `Entry Active Session`,
`Reloaded Active Session` (all flat container reads, all condition-100 gated);
`Contract Owner ID`, `Create Owner ID`, `Exit Owner ID`, `Reloaded Session ID`,
`Captured Session ID` (all `.id`); `Captured Start` (`.started_at`);
`Declared Duration` (`.declared_duration_seconds`).

**Leaves that must be seeded** (union of every dotted read + every dotted write):
`id`, `started_at`, `declared_duration_seconds`, `intention`. The first three are read;
`intention` is written at 11 sites (`persist_contract()`) and read nowhere — seed it anyway,
mirroring `PENDING_EXIT_SEED`, which seeds `timestamp` even though its read is inside the
guarded arm.

**Why the guard self-heals.** `verify_sentinel_gates()`'s own docstring anticipates this
exactly — `:2740-2745`:
> "This enforces the CONTAINER vs LEAF split automatically rather than by convention: once
> `clear_snapshot()` writes the leaf instead of the container, `settings_snapshot.brightness`
> stops being sentinel-written and its condition-100 container gate becomes legal again, while
> the leaf beneath it must be numeric. Change the clear back to the container and the build fails."

After the refactor, `_sentinel_written_keys()` will contain `active_session.id` instead of
`active_session`; no read of `active_session.id.<anything>` exists, so rule 2 finds nothing,
and no condition-100 gate will remain over a variable read from `active_session.id`, so rule 1
finds nothing. `KNOWN_SENTINEL_EXISTENCE_GATES = ()` then holds honestly.

### `exit_events`: a one-line array seed, and a **lower** crash risk than the ROADMAP states

**Bootstrap seed today:** the key is **absent entirely** — confirmed by extracting action 75
and by JSON-resolving every literal read key against it.

**All sites, measured** (`grep -n "exit_events" tools docs`):

| Site | Line | Shape |
|---|---|---|
| `get_value("exit_events", variable("Reloaded State"), "Exit Events")` | `:919` | **flat** read, un-stringified (correct helper) |
| `repeat.each` over `variable("Exit Events")` | `:922` | List consumer |
| `set_value("exit_events", variable("Exit Events Next"), "Reloaded State")` | `:934` | flat write |
| `COMPOUND_STATE_KEYS` membership | `:2932` | guard registry |
| A comment recording the gap | `:908-916` | prose |

**There is no dotted read of `exit_events`, and no conditional gates it — at all.**

Per the device-verified semantics quoted at `:168-171`, **a flat read of a missing key returns
nothing with no error**. The generator's own comment at `:913-916` already says so:
> "A flat read of a missing key returns nothing (no error, per this session's verified iOS
> semantics), so this swap cannot regress the pre-fix behaviour."

So the ROADMAP's framing — "the first real exit against clean state will very likely
hard-error" — is **not supported by the measured evidence**. The honest statement is:

- `exit_events` **absent** → flat read returns nothing → `Repeat With Each` receives nothing.
- What that does is the **one genuinely open runtime question** in this phase: whether
  `is.workflow.actions.repeat.each` over an empty/absent input is a zero-iteration no-op or a
  type error. That is not settled by any document in this repo. `[ASSUMED]` — most likely a
  no-op, and the recorded exit-recording behaviour on the write side would then be correct on
  the very first exit anyway (`Exit Events Next` already carries the appended event).
- **Evidence rung that would settle it: rung 2 (simulator).** It needs no Notes app, no Apple
  Intelligence, no Personal Automation and no real hardware — it is pure control-flow/operand
  behaviour, which `.claude/CLAUDE.md` §9 names as exactly the rung-2 class.

**The seed is still the right change**, for three reasons that do not depend on the crash
question: (1) STATE-12 claims the persisted document declares its rolling windows, and this one
is undeclared; (2) `recent_sessions` and `recent_contracts`, its two siblings in
`COMPOUND_STATE_KEYS`, are both seeded `[]`, so the omission is an inconsistency with no
defender; (3) it costs one line and shifts one attachment offset that `_replace_in_token()`
handles.

## The third key nobody named — `profile_snapshot.create_target_url`

I ran the full sweep the ROADMAP asked for, but generalised beyond the two named keys: every
literal `WFDictionaryKey` read from `State` or `Reloaded State`, resolved against the seeded
template.

```
STATE-SOURCED LITERAL READS NOT PRESENT IN BOOTSTRAP SEED
key                                           source var               n  dotted?
active_session.declared_duration_seconds      Reloaded State           1  DOTTED
active_session.id                             Reloaded State          16  DOTTED
active_session.id                             State                    1  DOTTED
active_session.started_at                     State                    1  DOTTED
exit_events                                   Reloaded State           2  flat
exit_selection_counter                        Reloaded State           2  flat
exit_selection_counter                        State                    1  flat
profile_snapshot.create_target_url            Reloaded State           2  DOTTED
```

**`profile_snapshot.create_target_url` is a DOTTED read of a leaf that the bootstrap does not
establish** — `route_exit()` `:865`:
```python
    a += [create] + read_value("profile_snapshot.create_target_url", variable("Reloaded State"), "Create Target URL")
```
`profile_snapshot` **is** seeded (goal, phone_purpose, reclaim_for,
deliberate_leisure_definition, enabled_exits, synced_at, note_content_hash) but
`create_target_url` is **not**. Per the verified semantics — and per the generator's own
statement of the same failure at `:1223`, "reads `sequences.<Sequence>.<Dispatch Circle>` as a
DOTTED key, and at index 0 the final segment is absent, which iOS raises as a hard 'could not
evaluate the key path' error" — **a missing final segment raises**.

**This sits on the exit path.** `route_exit()` is called only from `record_exit_and_route()`
`:944`. Choosing the **Create** exit on a clean install would hard-error at the read, *after*
`exit_events`, `pending_exit.type/.timestamp` and `exit_selection_counter` have been written
and `save_state("Reloaded State")` has already run at `:944`. This is arguably the single
most likely first-exit crash in the whole phase surface, and it is **not** one of the two keys
the ROADMAP names.

**Recommendation:** include it. The phase's own governing rule is "fix whole classes, never
site-by-site," it is the same defect class on the same code path as the chartered keys, and the
fix is one seed line: `"create_target_url": null` inside the existing `profile_snapshot`
object. (Seeding it `null` rather than the sentinel is correct here: the consumer gate at
`:866` is `if_block("Create Target URL", 100)` — a has-any-value test that must read **false**
when unset, and JSON `null` read flat-then-dotted... — see Open Question 2, this is the one
place where the sentinel-vs-null choice interacts with an existing condition-100 gate and needs
a deliberate decision rather than a copy of the `pending_exit` shape.)

**`exit_selection_counter`** is also unseeded but is **flat** and already correctly guarded by
condition 101 at both consumers (`:752` and `:941`, each with a documented rationale comment
at `:753-762` explaining why code 5 vs `""` cannot work there). Seeding it `0` would be tidy
and would let those two 101-guards be simplified later, but it is **not** a defect and carries
no crash risk. **Recommend seeding it for STATE-12 completeness, leaving both 101 guards alone.**

**`profile_snapshot.proforma`** appears in the write-side sweep but is **write-only**
(`manual_note_refresh()` `:1968`, MANUAL arm) and read nowhere. Writing a leaf under an
existing container is safe. No action.

## Why `active_session` is a SAFE-01 / SESS-07 issue, not just tidiness

`restore_managed_settings("Reloaded State")` — the only path that restores brightness and
volume after a Dimming or Silence primitive — is emitted at `close_pipeline():1306`, **inside**
three nested `active_session`-derived arms:

```
if Entry Active Session has any value            (:1237, cond 100, reads "active_session")
  └─ if Reloaded Active Session has any value    (:1250, cond 100, reads "active_session")
       └─ if Reloaded Session ID is <Session ID> (:1252, cond 4,  reads "active_session.id")
            └─ … restore_managed_settings()      (:1306)
                 notification()                  (:1310)
                 save_state("Reloaded State")    (:1311)
```

Any hard error on the `.id` / `.started_at` / `.declared_duration_seconds` reads at `:1240`,
`:1251` or `:1261` aborts the run **before** `:1306`. The user is then left on a dimmed screen
or a silenced device with no restore, which is precisely the safety failure `.claude/CLAUDE.md`
calls out ("capture-and-restore reliability *is* the safety mechanism"). That is why SESS-07
and SAFE-01 are correctly listed on this phase and why the fix is not cosmetic.

The corresponding *sentinel-vs-empty* rule must be preserved: `restore_managed_settings()`'s
docstring `:467-479` records that code 5 was verified and **rejected** for the snapshot leaves
because `is not "null"` is TRUE for `""`. That reasoning is about `settings_snapshot` leaves,
which are gated numerically. It does **not** forbid code 5 for `active_session.id`, because the
seed guarantees the leaf is the non-empty sentinel and every real value is a
`session-<epoch>-<random>` string. Both remain correct simultaneously — but only while the seed
is `CLEARED_SENTINEL`, never `""`.

## Common Pitfalls

### Pitfall 1: `docs/state_engine_self_check.py:92` breaks by construction
**What goes wrong:** the container/leaf refactor removes every bare `"active_session"`
`setvalueforkey` key (one write at `:1188`, two clears at `:1812` / `:1893`), and that checker
asserts **exact list membership**:
```python
keys = [action["WFWorkflowActionParameters"]["WFDictionaryKey"] for _, action in setters]
for required in ("heat", "gravity", "pressure", "circle", "active_session", "recent_sessions", "last_close_at"):
    assert required in keys
```
**Why it happens:** `keys` is a list of literal key strings, so `"active_session" in keys` is
exact, not substring — `"active_session.id"` will **not** satisfy it.
**How to avoid:** update the tuple to `"active_session.id"` in the same commit, and — per the
project's own recorded convention ("Structurally-derived exemption: an assertion false at HEAD
for a by-construction reason gets a named helper located by the same structural handle the
generator uses, never an index or a silent skip", `.planning/STATE.md`) — add a comment naming
*why* the literal moved.
**Warning sign:** `python3 docs/state_engine_self_check.py` raises a bare `AssertionError` with
no message (it uses `assert`, not `require()`), so the failure is uninformative if you are not
expecting it.

### Pitfall 2: `PENDING_EXIT_ANCHOR` is the `active_session` seed line
`PENDING_EXIT_ANCHOR = '"active_session": null,'` (`:2567`). Changing the `active_session` seed
to a container changes that exact line. Today `seed_pending_exit()` early-returns because
`"pending_exit"` is already in the committed template, so the anchor lookup is never reached —
but the moment anyone regenerates from a template without `pending_exit`, `next(...)` raises a
bare **`StopIteration`** (not `SystemExit`, no message). **Update the anchor in the same
commit.** Same class of latent break applies to `SNAPSHOT_EMPTY` (`:2419`) and
`PANIC_ESCAPE_ANCHOR = '"ai_enabled": false,'` (`:2642`) — neither of those two lines is
touched by this phase, but verify that before assuming it.

### Pitfall 3: seeder ordering in `main()` is load-bearing
`main()` runs, in order: `seed_settings_snapshot` → `seed_pending_exit` → `seed_panic_escape`
→ `fix_state_rebind`. The comment at that call site is explicit:
> "Must run BEFORE `fix_state_rebind()`: the rebind pass also edits the same template token,
> and seeding a new field is the reason the schema_version bump below exists."

New seeders must be inserted **before** `fix_state_rebind(actions)`. New verifiers go in the
verify block, alongside `verify_pending_exit_seed` / `verify_panic_escape_seed`.

### Pitfall 4: `verify_state_seed()` will not cover the new keys unless you generalise it
Its read-side scan is filtered to `settings_snapshot`-rooted keys (`:2523`), and its own
docstring in `verify_panic_escape_seed()` records the consequence, measured 2026-08-17:
> "NOTE, measured 2026-08-17: `verify_state_seed()` does **NOT** cover this field. Its
> read-side scan is scoped to keys rooted at `settings_snapshot`, so it would not have noticed
> an unseeded `panic_escape_enabled`. This verifier is why the seed is guarded at all."

**The generalisation is a deletion, not an addition.** Removing the
`key.split(".")[0] == "settings_snapshot"` filter (and the paired composite-key assertion, which
must then tolerate the legitimate `exit_stats.<token>` composites) turns the existing missing-key
loop into a whole-class guard. Run against HEAD it reports the eight rows in the sweep table
above — which is exactly the set this phase closes. **This is the single highest-leverage line
in the phase.**

### Pitfall 5: `verify_compound_value_reads()` must stay satisfied
`exit_events` is already in `COMPOUND_STATE_KEYS` (`:2932`) and already read via `get_value()`.
If any refactor accidentally routes it through `read_value()`, the build fails with
"a compound (Array) state key is read via read_value()…". Leave `:919` alone.

### Pitfall 6: `build_sentient.py`'s verifier set is a **subset**, and already has a hole
Measured — `tools/build_sentient.py:13-27` imports exactly 13 symbols and its verify chain runs
13 guards. It does **not** import `verify_pending_exit_seed`, `verify_panic_escape_seed`,
`verify_compound_value_reads` or `verify_conditional_action_string`. So the pending_exit seed —
the very pattern this phase mirrors — is **not** asserted on the Aware fork today. The phase's
per-fork discipline (stated three times in `build_sentient.py`'s own comments: "enforced PER
FORK rather than inferred for Sentient from Dumb") argues for arming the two new verifiers on
both forks. Whether to also close the pre-existing gap for `verify_pending_exit_seed` /
`verify_panic_escape_seed` is a scope call for the planner — it is a two-line change and
strictly increases coverage, but it is not chartered by this phase.

### Pitfall 7: the schema bump is three literals and fails one build late
Move `SCHEMA_VERSION`, `SCHEMA_VERSION_PREVIOUS` and `SCHEMA_VERSION_ACCEPTED` together.
Missing the recognition tuple does not fail *this* build — it fails the **next** one with
"schema version check conditional not found", pointing at a missing conditional rather than at
the bump one build earlier. Documented verbatim at `:3604-3617`.

### Pitfall 8: idempotency is a checked property, and every seeder is written for it
`docs/phase6_self_check.py:45-49` runs the builder **twice** and requires byte-identical output:
```python
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = digest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == digest(), "builder output is not idempotent")
```
Every new seeder must guard with the same `if '"<key>"' in inner["string"]: return` early-exit
that `seed_pending_exit()` and `seed_panic_escape()` use. Note the guard is a **substring**
test on the whole template string — pick a guard token that cannot collide (e.g. `'"exit_events"'`
does not appear elsewhere; `'"id"'` obviously would, so guard `active_session`'s seeder on
something unambiguous like the full seeded line or `'"active_session": {'`).

### Pitfall 9: the exit path has **zero** device evidence at any rung
`grep`ping `docs/BUILD-NOTES.md` for exit-recording device evidence returns nothing relevant;
`.planning/STATE.md` records that Phase 10's device UAT was blocked ("`xcrun devicectl list
devices` returned 'No devices found.'", all ten tests left blank, DIST-03 still open). The
closed OPEN-path debug session reached breadcrumb J on the OPEN path only. **Treat the exit
path as new-risk surface, and expect the device task to be blocked** — the project's recorded
posture in that situation is to not fabricate a pass and to leave the UAT blank.

## Code Examples

All three verified patterns are quoted in full under **Architecture Patterns** above
(`seed_pending_exit` `:2570`, `verify_pending_exit_seed` `:2597`, the
`complete_pending_exit()` leaf gate `:1036-1038` and leaf clear `:1058-1061`). Two more the
planner will need:

### The current `record_exit_and_route()` gate, verbatim (`:900-902`) — the shape to convert
```python
    a += reload_state() + read_value("active_session", variable("Reloaded State"), "Exit Active Session")
    active_group, active = if_block("Exit Active Session", 100)
    a += [active] + read_value("active_session.id", variable("Reloaded State"), "Exit Owner ID")
```
Converted, it collapses to one read and one conditional, exactly matching
`complete_pending_exit()`'s idiom — the `.id` read *is* the gate, and `Exit Owner ID` is then
reused unchanged by the existing ownership comparison at `:903-904`:
```python
    owner_group, owner = if_block("Exit Owner ID", 4, string="captured-session-placeholder")
    owner["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID")
```

### The current `open_pipeline()` session write, verbatim (`:1183-1188`) — the wholesale replace
```python
    session_text = text_token([('{"id":"', "Session ID"), ('","started_at":', "Now Epoch"), (',"declared_duration_seconds":0}', None)])
    session_json = uid()
    a += [action("is.workflow.actions.gettext", UUID=session_json, WFTextActionText=session_text),
          action("is.workflow.actions.detect.dictionary", UUID=uid(), WFInput=output(session_json, "Text"))]
    # Detect Dictionary output cannot safely be re-derived from action position: name it immediately.
    a += [set_var("Active Session Next", output(a[-1]["WFWorkflowActionParameters"]["UUID"], "Dictionary")), set_value("active_session", variable("Active Session Next"))]
```
Rewritten as three leaf writes (`active_session.id`, `.started_at`,
`.declared_duration_seconds`), this **removes** the `gettext` + `detect.dictionary` +
`set_var` trio and adds two `set_value` calls — a net *reduction* in action count, no new
identifiers, and it eliminates the last wholesale container replacement. `normalize_setters()`
supplies the rebind for each new setter automatically.

## State of the Art

| Old approach | Current approach | When changed | Impact |
|---|---|---|---|
| Sentinel = `""` (empty) | `CLEARED_SENTINEL = "null"` | Cycle 12 | Empty passes `has any value` (Donor 6.1) and let an empty value reach Set Brightness — a black screen. Never seed `""`. |
| Clear the whole key | Clear the **leaf**, keep the container permanent | Cycle 10 finding 5 → cycle 16 | The pattern this phase applies for the third time |
| Existence gate (cond 100) over a sentinel-written key | Leaf-value gate (cond 5) or numeric `> 0` | Cycle 12 axis 7 | The gate-semantics half of this phase |
| `read_value()` for everything | `get_value()` for `COMPOUND_STATE_KEYS` | Cycle 15 | Already correct for `exit_events` at `:919` |
| `--target-platform ios` | `--target-platform all` at both gates | DEV-04, then quick task 260817-ewg | Gate A mandatory, gate B advisory-with-waiver |
| Product names Dumb / Sentient | **Core / Aware** | Phase 11 plan 06 | `.claude/CLAUDE.md` and `12-CONTEXT.md` still carry the old literals |

**Deprecated / outdated in this repo:**
- `elapsed()` / `gettimebetweendates` for stored epochs → replaced by `elapsed_since()` (cycle 14).
- The `WFAppName` term in `docs/phase6_self_check.py` → removed as stale in Phase 10-03.
- `KNOWN_SENTINEL_EXISTENCE_GATES` itself — this phase's charter is to make it `()`.

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|-------|---------|---------------|
| A1 | `is.workflow.actions.repeat.each` over an absent/empty input is a zero-iteration no-op, not a runtime type error | "exit_events: a one-line array seed" | If it errors, `exit_events` **is** a live first-exit crash after all and the seed is load-bearing rather than tidy. The seed fixes it either way, so this affects severity framing, not the fix. **Settle at rung 2 (simulator) if the planner wants the record.** |
| A2 | A dotted read whose *final* segment is missing raises identically to one whose *intermediate* segment is missing | "The third key" | If only intermediate segments raise, `profile_snapshot.create_target_url` is safe and its inclusion is optional tidying. Supported by `.claude/CLAUDE.md`'s "any missing segment" wording and by the generator's own `:1223` comment describing the final-segment case, so confidence is HIGH — but it is inference from two written records, not a fresh device measurement. |
| A3 | "No installed base" still holds, so a schema bump loses nothing | Pattern 3 | If a device does hold a real `state.json`, the bump silently discards heat/gravity/pressure/rolling windows/exit_stats samples with no migration (explicitly forbidden by BD-06-A1). **Planner must re-confirm before bumping.** |
| A4 | Seeding `active_session.id` with `CLEARED_SENTINEL` and gating condition 5 is safe, because no real session ID can equal the literal `"null"` | Pattern 1 | Session IDs are `session-<epoch>-<1..2147483647>` (`:1177-1182`), so collision is impossible. Very low risk. |
| A5 | `set_value` on a dotted key whose leaf does not yet exist creates the leaf (needed for `.intention`) | "Leaves that must be seeded" | Already relied on today at `:569` and `:876` in shipped builds; seeding all four leaves removes the dependency entirely. |

## Open Questions

1. **Does `Repeat With Each` over an absent input error?** (= A1.)
   - *What we know:* a flat read of a missing key returns nothing, no error (device-verified).
   - *What's unclear:* what `repeat.each` does with that nothing.
   - *Recommendation:* seed `exit_events` regardless; optionally settle at rung 2 with a small
     probe shortcut and record the result in `docs/BUILD-NOTES.md`. Do not spend a device
     session on it.

2. **Sentinel or JSON `null` for `profile_snapshot.create_target_url`?**
   - *What we know:* its consumer gate at `:866` is `if_block("Create Target URL", 100)` — a
     has-any-value test that must read **false** when the user has not yet supplied a URL. The
     sentinel `"null"` is present and non-empty, so a condition-100 gate over it reads **TRUE**
     — exactly the axis-7 trap. JSON `null` read through `read_value()`'s `gettext` chain is
     the untested case here.
   - *What's unclear:* whether `read_value()` of a JSON-`null` leaf yields no-value (gate false,
     correct) or the text `"null"` (gate true, wrong — it would then `openurl` the string
     "null"). `.claude/CLAUDE.md` documents `"null"`→Number→`>0` as false, but says nothing
     about `null`→Text→has-any-value.
   - *Recommendation:* **do not seed this leaf with the sentinel.** Either (a) seed it JSON
     `null` and convert the gate at `:866` to the same numeric/`is not sentinel` discipline the
     rest of the file uses, or (b) leave `create_target_url` out of this phase entirely and
     raise it as its own todo. Option (a) is in-class and small; option (b) is the safest if the
     planner wants Phase 12 tightly scoped. **Either is defensible; guessing the gate semantics
     is not.**

3. **Should the pre-existing Sentient verifier gap be closed here?** (Pitfall 6.)
   - *Recommendation:* arm the two **new** verifiers on both forks (in-scope, required for the
     "per fork, never inferred" convention). Adding `verify_pending_exit_seed` and
     `verify_panic_escape_seed` to Sentient is a strict improvement but is out of charter —
     surface it as a follow-up todo unless the planner wants it.

4. **Can the exit path actually be device-tested?**
   - *What we know:* Phase 10's device UAT was blocked with no iPhone connected; DIST-03 is open.
   - *Recommendation:* plan the device task, plan the blocked branch explicitly, and do not
     substitute a simulator run or a decrypted-artifact inference for a device observation —
     that is the recorded precedent from Phase 10.

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` | both generators, all 12 checkers | ✓ | 3.13.9 | — |
| `git` + provenance ancestor `7ca8ebb…` | C1 build gate | ✓ | `git merge-base --is-ancestor` exits **0** at `9275a4e` | none — abort if it fails |
| `validate-shortcut` | gates A and B | ✓ | Playground 1.2.1 | none |
| `sign-shortcut` | signed artifacts | ✓ | Playground 1.2.1 | none |
| macOS `shortcuts` CLI | invoked by `sign-shortcut` | ✓ (implied — signing succeeded in Phase 11 on this machine) | — | none |
| `aea` / `aa` | decrypt-verify what shipped | ✓ (used successfully in Phase 11) | — | skip decrypt-verify, record deviation |
| iOS Simulator (iOS 26.5, iPhone 17 Pro `79A84C29-…` booted) | optional rung-2 probe for Open Question 1 | ✓ per `.claude/CLAUDE.md` §9 (not re-measured this session) | 26.5 (23F77) | skip the probe |
| Real iPhone via iPhone Mirroring | exit-path UAT (rung 3/4) | ✗ at last measurement | — | **No fallback.** Plan the blocked branch; leave UAT blank rather than fabricating a pass |
| pytest / unittest | — | n/a | — | The project has **no** Python test framework; checkers are bare scripts |

**Missing dependencies with no fallback:** a connected iPhone for the exit-path device test.
**Missing dependencies with fallback:** none others.

## Validation Architecture

### Test framework
| Property | Value |
|----------|-------|
| Framework | **None** — 12 standalone scripts in `docs/`, using bare `assert` or a local `require()` helper. Confirmed: no `pytest.ini`, no `setup.cfg`, no `pyproject.toml`, no `tests/`, and zero `import pytest` / `import unittest` anywhere in `tools/` or `docs/` |
| Config file | none — see Wave 0 |
| Quick run command | `python3 docs/state_engine_self_check.py && python3 docs/phase6_self_check.py` (~seconds; note `phase6_self_check.py` itself invokes the builder **twice** to prove idempotency) |
| Full suite command | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check note_identity_check manifest_check; do python3 docs/$f.py \|\| exit 1; done && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` — copied verbatim from the phase-11 plans' `<automated>` blocks, which is this project's canonical chain |

### Phase requirements → test map
| Req ID | Behavior | Test type | Automated command | File exists? |
|--------|----------|-----------|-------------------|-------------|
| STATE-12 | `exit_events` (and `exit_selection_counter`) are declared in the versioned bootstrap document | unit (build guard) | `python3 -c "import sys;sys.path.insert(0,'tools');import plistlib,pathlib,json,build_state_engine as B;a=plistlib.loads(pathlib.Path('src/PROSOCHE-Dumb.xml').read_bytes())['WFWorkflowActions'];_,i=B._state_template(a);s=json.loads(i['string'].replace('\"￼\"','\"x\"').replace('￼','0'));assert s['exit_events']==[];print('ok')"` | ❌ Wave 0 — new `verify_exit_events_seed()` |
| STATE-12 | schema bumped 3→4 across all three coupled literals | unit | `python3 -c "import sys;sys.path.insert(0,'tools');import build_state_engine as B;assert B.SCHEMA_VERSION=='4' and B.SCHEMA_VERSION_PREVIOUS=='3' and B.SCHEMA_VERSION in B.SCHEMA_VERSION_ACCEPTED;print('ok')"` | ❌ Wave 0 |
| SESS-07 | `active_session` is a permanent four-leaf container; every read leaf resolves in the seed | unit (build guard) | `python3 tools/build_state_engine.py` (new `verify_active_session_seed()` raises on failure) | ❌ Wave 0 |
| SESS-07 / SAFE-01 | zero condition-100 gates and zero dotted reads stand over a sentinel-written key, with an **empty** exemption set | unit (build guard) | `python3 -c "import sys;sys.path.insert(0,'tools');import build_state_engine as B;assert B.KNOWN_SENTINEL_EXISTENCE_GATES==();print('ok')" && python3 tools/build_state_engine.py` (`verify_sentinel_gates()` now runs unexempted) | ✅ `verify_sentinel_gates()` `:2877` exists; only the constant changes |
| SAFE-01 | brightness/volume writes remain numerically gated | unit (build guard) | `python3 tools/build_state_engine.py` (`verify_restore_gates()` `:2835`) + `python3 docs/environmental_restore_check.py` + `python3 docs/phase9_self_check.py` | ✅ exists |
| EXIT-01 / EXIT-02 | the six exit routes and their state keys survive the refactor | unit | `python3 docs/phase6_self_check.py` | ✅ exists (`:56-57` key list; verify still satisfied after the refactor) |
| All | every literal state read resolves in the bootstrap seed (**the class-level guard**) | unit (build guard) | `python3 tools/build_state_engine.py` (generalised `verify_state_seed()`) | ❌ Wave 0 — generalisation |
| All | builders are byte-idempotent | integration | `python3 docs/phase6_self_check.py` (builds twice, digests, compares) | ✅ exists |
| All | both forks structurally valid at the real target | integration | gate A ×2 | ✅ exists |
| SESS-07 / EXIT-* | a real "leave and confirm exit" against clean state completes and restores settings | manual (device, rung 3/4) | — none possible; **no automated substitute exists** | ❌ device UAT doc |

### Sampling rate
- **Per task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 docs/state_engine_self_check.py && python3 docs/phase6_self_check.py`
- **Per wave merge:** the full 12-checker chain + gate A on both forks
- **Phase gate:** full suite green, gate A clean ×2, gate B showing **exactly** the one waived
  line ×2, both forks signed under the Core/Aware names, `docs/manifest_check.py` green, then
  `/gsd-verify-work`

### Wave 0 gaps
- [ ] `verify_exit_events_seed()` in `tools/build_state_engine.py` — covers STATE-12
- [ ] `verify_active_session_seed()` in `tools/build_state_engine.py` — covers SESS-07
- [ ] Generalised `verify_state_seed()` read-side scan (delete the `settings_snapshot` filter) — covers the whole class
- [ ] `docs/state_engine_self_check.py:92` literal updated `"active_session"` → `"active_session.id"` — **required or the suite goes red**
- [ ] Both new verifiers imported and armed in `tools/build_sentient.py`
- [ ] A `12-UAT.md` for the device exit-path test, with an explicit blocked branch
- Framework install: **none** — the checker-script convention is the framework

## Security Domain

`security_enforcement` is `true`, `security_asvs_level` 1. This is an offline, single-device
iOS Shortcut with no network, no server, no auth and no secrets, so most ASVS categories are
structurally inapplicable — stated explicitly rather than left blank.

### Applicable ASVS categories

| ASVS category | Applies | Standard control |
|---------------|---------|------------------|
| V2 Authentication | **no** | No accounts, no login, no identity. |
| V3 Session management | **partially — locally** | `active_session` is not a security session; it is a behavioural ownership token. But its ownership check (`Reloaded Session ID` is `Session ID`) is what prevents a superseded CLOSE from writing state. Preserve `if_block(…, 4, string=token("Session ID"))` at all four owner sites; this phase must not weaken it. |
| V4 Access control | **no** | Single user, single device, no privilege boundary. |
| V5 Input validation | **yes** | Two inputs cross a trust boundary: (1) `state.json`, validated by the three-check gate at actions 27/37/39 (`schema_version` present, equals `SCHEMA_VERSION`, `profile` non-empty) with rebuild-on-failure; (2) the user-hand-edited Control Room Note, parsed on the MANUAL arm only. This phase strengthens (1) by making the declared shape complete. |
| V6 Cryptography | **no (delegated)** | Signing is Apple's `shortcuts sign` / AEA1. Nothing hand-rolled. |
| V7 Error handling & logging | **yes** | Shortcuts has no try/catch. The *only* defence against a hard error is making the read impossible to fail — which is exactly what this phase does. |
| V12 File handling | **yes** | One fixed path `PROSOCHE/state.json`, `WFAskWhereToSave=False`, `WFSaveFileOverwrite=True`, `WFFileErrorIfNotFound=False`. No user-controlled path. Unchanged by this phase. |

### Known threat patterns for this stack

| Pattern | STRIDE | Standard mitigation |
|---------|--------|---------------------|
| Un-restored environmental change after a mid-run hard error | Denial of service (user stranded dim/silent) | Make every read on the path to `restore_managed_settings()` unable to raise — **this phase**. Plus `manual_emergency_restore()` and `live_ice_redirect()`, which are never gated on any Note-editable setting |
| Sentinel-vs-real-value confusion at a gate | Tampering (state corruption) | `verify_sentinel_gates()` with an **empty** exemption set — this phase's charter |
| State-shape drift between generator and template | Tampering | Separate `seed_*` / `verify_*_seed` pairs so the two cannot silently agree on being wrong |
| Malformed/stale `state.json` accepted as valid | Tampering | The three-check validity gate + schema bump forcing exactly one rebuild |
| A signed artifact shipping under a wrong filename (silently dead install) | Denial of service | `sign-shortcut --name` with the exact display name + `docs/manifest_check.py`'s DIST-04 assertion |
| Fabricated action identifier or enum literal | Tampering | `verify_parameter_keys()` + the do-not-fabricate protocol. **This phase introduces none.** |

## Sources

### Primary (HIGH confidence — measured this session at `9275a4e`)
- `tools/build_state_engine.py` (3742 lines) — read in full at the relevant ranges; every quoted block copied verbatim with line numbers
- `tools/build_sentient.py` (326 lines) — import list `:13-27` and verify chain `:285-313`
- `src/PROSOCHE-Dumb.xml` / `src/PROSOCHE-Sentient.xml` — parsed with `plistlib`; 4456 / 4524 actions; bootstrap template extracted from action 75 including its four `attachmentsByRange` offsets
- Executable probe: `verify_sentinel_gates()` re-run with an emptied exemption set → **34 offenders**, itemised
- Executable probe: every literal `WFDictionaryKey` read from `State`/`Reloaded State` JSON-resolved against the seeded template → **8 unresolved key/source rows**
- `docs/state_engine_self_check.py`, `docs/phase6_self_check.py`, `docs/manifest_check.py`, `docs/environmental_restore_check.py`, `docs/phase9_self_check.py`, `docs/router_ui_census.py` — read at the assertion sites
- `validate-shortcut` gate A and gate B run on both forks → baselines recorded above
- `git merge-base --is-ancestor 7ca8ebb… HEAD` → exit 0
- `.planning/todos/pending/2026-08-15-close-state-shape-sentinel-gaps.md` — the phase's origin document, read in full
- `.planning/REQUIREMENTS.md` — the five requirement texts quoted verbatim
- `.planning/STATE.md` — decisions log, including the Phase 10 device-UAT block and the no-fabrication precedent
- `.planning/phases/11-*/11-05-PLAN.md`, `11-06-PLAN.md`, `11-PATTERNS.md` — the canonical `<automated>` command chains and the analog-mapping convention

### Secondary (MEDIUM confidence)
- `.claude/CLAUDE.md` — the two-gate rule, the seven parameter-defect axes, the verified runtime semantics table, the evidence ladder. Authoritative for this project, but **measured stale** on the product display names.
- `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md` — grepped, not read end-to-end.

### Tertiary (LOW confidence)
- None. **No web search, no Context7, no external documentation was consulted** — this phase's
  entire unknown surface is inside this repository, and every question the network could have
  answered was answerable by running the code instead.

## Metadata

**Confidence breakdown:**
- Standard stack: **HIGH** — no external dependency exists; toolchain presence and versions measured
- Architecture / pattern to mirror: **HIGH** — the analog is quoted verbatim and has shipped twice
- Site inventory: **HIGH** — enumerated by executing the project's own guard logic, not by grep alone
- Pitfalls: **HIGH** for 1–8 (each derived from a read of the failing assertion or the ordering
  comment); **MEDIUM** for 9 (device availability may have changed since Phase 10)
- `exit_events` severity framing: **MEDIUM** — the fix is certain, the crash claim is not (A1)
- `profile_snapshot.create_target_url` as a defect: **HIGH** that it is unseeded and dotted-read;
  **MEDIUM** on the exact runtime consequence (A2)

**Research date:** 2026-08-17
**Valid until:** 30 days for the pattern/architecture findings; **invalidated immediately by any
commit touching `tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml` or `docs/*.py`** — every
line number and every count above is pinned to `9275a4e`.
