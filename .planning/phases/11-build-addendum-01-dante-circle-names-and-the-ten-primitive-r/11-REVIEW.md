---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
reviewed: 2026-08-17T00:00:00Z
depth: standard
files_reviewed: 16
files_reviewed_list:
  - tools/plist_text_edit.py
  - tools/build_state_engine.py
  - tools/build_sentient.py
  - docs/note_identity_check.py
  - docs/sequence_dispatch_check.py
  - docs/sentient_core_check.py
  - docs/manifest_check.py
  - docs/phase5_self_check.py
  - docs/phase7_self_check.py
  - docs/phase9_self_check.py
  - docs/environmental_restore_check.py
  - docs/state_engine_self_check.py
  - src/CONFIG-BLOCK.md
  - docs/BUILD-NOTES.md
  - docs/CAPABILITY-DECISIONS.md
  - artifacts/shortcuts/MANIFEST.md
findings:
  critical: 3
  warning: 15
  info: 0
  total: 18
status: issues_found
---

# Phase 11: Code Review Report

**Reviewed:** 2026-08-17
**Depth:** standard
**Files Reviewed:** 16
**Status:** issues_found

## Summary

The phase's own new guards are, on the whole, real guards. I ran negative controls against
`verify_dispatch_coverage()` (orphan entry, reverted condition-99 branch, unknown condition
code) and against `verify_panic_escape_seed()` (unseeded flag, condition-100 gate) — five of
six deliberate defects were caught with a correct message. `docs/sequence_dispatch_check.py`'s
promotion to a gate is genuine. `tools/build_state_engine.py` is byte-idempotent across two
runs (verified on an isolated copy). All twelve standing checkers pass, the working tree is
clean, and the Emergency Restore / Panic Escape separation (T-11-22) holds structurally: none
of the four Emergency Restore menus or case bodies is enclosed by any Panic Escape
conditional, in either fork.

That is where the good news stops. Three defects are shipping in the signed artifacts.

The most serious is not new to this phase but was re-certified by it: **`dimming()` and
`silence()` have unreachable bodies.** Both gate on the *container* `settings_snapshot.<x>`
with condition 100, with the entire capture-and-apply body in the OTHERWISE arm — and cycle
11's `seed_settings_snapshot()` made that container a permanent bootstrap invariant that
nothing ever removes. The gate is therefore permanently TRUE and both primitives take the
`Nothing` arm on every run. Two of BD-06's nine shipped interventions (`Dim`, `Silence`) are
silent no-ops on device, and this phase's `environmental_restore_check.py` / `phase9_self_check.py`
site tables and the MANIFEST's "15 / 15 / 22, 19 coerced" prose are auditing dead code.

Second, the new Panic Escape removal path references `is.workflow.actions.text.match`'s output
as `"Matched Text"`. The golden corpus is unanimous (15/15) on `"Matches"`, and this repo's own
`build_sentient.py` uses `"Matches"` for the identical action. `ACTION_OUTPUT_NAMES` does not
cover `text.match`, so `verify_output_names()` is blind to it. If the reference does not
resolve, the removal direction of Panic Escape is permanently dead and — by the branch's own
design — reports "Nothing was changed" rather than an error.

Third, the Aware fork's Use Model audit is inserted at the *first* `persist_contract()` marker
only. Phase 11 added a second OPEN-arm `primitive_dispatch()` rendering, so a user who removes
Panic Escape silently loses the entire Aware differentiator. `sentient_core_check.py`'s
`assert len(models) == 1` pins that defect rather than catching it.

Beyond those, the recurring theme is the one plan 11-04 already found once: **coupled literals
with no reconciliation.** The phase fixed the `schema_version` triple and then created or left
five more instances of the same shape, one of which (`PROFILE_NAMES` ↔ `thresholds.*` ↔ the
hand-authored bootstrap chain) has exactly the hard-error consequence BD-06-A1 itself names.

## Critical Issues

### CR-01: `dimming()` and `silence()` bodies are unreachable — the container existence gate can never read false

**File:** `tools/build_state_engine.py:576-595` (`dimming`), `tools/build_state_engine.py:598-618` (`silence`)
**Emitted at:** `src/PROSOCHE-Dumb.xml` actions 1027-1029 (Silence) and 1121-1123 (Dim), ×11 renderings each

**Issue:**

```python
a += read_value("settings_snapshot.brightness", variable("State"), "Brightness Snapshot")
snapshot_g, snapshot_if = if_block("Brightness Snapshot", 100)
a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
a += device_detail("Current Brightness", "Captured Brightness")   # <-- OTHERWISE arm
```

The gate is `settings_snapshot.brightness` **has any value** → do nothing; otherwise → capture
and dim. But `seed_settings_snapshot()` (`:2481`) seeds that key as a permanent three-leaf
sub-dictionary, and `clear_snapshot()` (`:443`) deliberately clears only the *leaf*
`.original_value`, never the container — the docstring calls that a "PERMANENT invariant" and
`verify_sentinel_gates()` explicitly licenses container gates at condition 100 on those
grounds. Nothing in either fork ever removes the container. A read of a present, non-empty
sub-dictionary passes `has any value` (this project's own donor-measured semantics: present
but empty is already TRUE; a dict is present and non-empty).

Therefore the true arm — `Nothing` — fires on every run, and the *entire* body sits in the
unreachable otherwise arm: the Get Device Details capture, the three `settings_snapshot.*`
writes, the `Dim Target` read, the Set Brightness / Set Volume write, **and** the
"Brightness could not be captured, so nothing was changed" fallback alert. Circles configured
to `Dim` or `Silence` produce nothing at all on device — no dim, no alert, no state write, no
error. Two of the nine shipped primitives are silent no-ops.

This is the same class `verify_dispatch_coverage()` was built to prevent, one level deeper:
the branch is reached, the body is dead. Note the polarity contrast with
`restore_managed_settings()` (`:464`), where the identical always-true container gate is
*harmless* because the work is in the TRUE arm and the leaf gate then decides.

Consequence for this phase's own artifacts: `docs/environmental_restore_check.py`'s
`EXPECTED_SITES = {15, 15, 22}`, `docs/phase9_self_check.py`'s 30-site / 19-coerced audit, and
MANIFEST.md's "Dimming and Silence writes now execute where they previously no-opped" all
certify code that cannot run.

**Fix:** Gate on the *leaf*, numerically, mirroring `restore_managed_settings()`'s own
established rule ("only a strictly positive reading counts as a real capture"), and invert the
polarity so the capture happens when no original is recorded:

```python
# dimming()
a += read_value("settings_snapshot.brightness.original_value", variable("State"),
                "Brightness Original")
# already captured (> 0) -> leave the existing unrestored snapshot alone
snapshot_g, snapshot_if = if_block("Brightness Original", 2, number=0)
a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
a += device_detail("Current Brightness", "Captured Brightness")
...
```

The leaf is seeded with the cleared sentinel `"null"`, which coerces to a false `> 0` test
(Donor 6.1), so the otherwise arm is reachable on a fresh install and closed once a real
original is captured. Apply the identical change to `silence()` for
`settings_snapshot.volume.original_value`.

Then add a build guard in the same commit — the existing `verify_sentinel_gates()` cannot see
this because the container is not sentinel-written. Assert that every `setbrightness` /
`setvolume` write is *reachable*: i.e. that no condition-100 gate whose variable is read from a
`settings_snapshot` **container** key encloses (in either arm) a `getdevicedetails` or a
`setbrightness`/`setvolume`. And correct the site tables in
`docs/environmental_restore_check.py` and `docs/phase9_self_check.py` only after the bodies are
live, not before.

---

### CR-02: the new Panic Escape branch reads `text.match` through a wrong `OutputName`, silently killing the removal direction

**File:** `tools/build_state_engine.py:2030-2032` (new this phase); same defect pre-existing at `tools/build_state_engine.py:1968` (Sync My Profile)

**Issue:**

```python
action("is.workflow.actions.text.match", UUID=match_id,
       WFMatchTextPattern=PANIC_ESCAPE_SECTION_PATTERN,
       text=output(note_id, "Text")),
action("is.workflow.actions.gettext", UUID=section_id,
       WFTextActionText=output(match_id, "Matched Text")),   # <-- wrong output name
```

Measured against the bundled golden corpus (19 shipped shortcuts, all
`ActionOutput` references resolved back to their producing identifier):

| producing action | `OutputName` observed | count |
|---|---|---:|
| `is.workflow.actions.text.match` | `Matches` | 15 |
| `is.workflow.actions.text.match.getgroup` | `Group from Matched Text` | 1 |
| `is.workflow.actions.text.match.getgroup` | `Text` | 7 |

`"Matched Text"` never appears for `text.match` in the corpus. This repo's own
`tools/build_sentient.py:153-159` uses `output(matches, "Matches")` for the same identifier —
so the artifact carries two contradictory names for one action. `ACTION_OUTPUT_NAMES`
(`:3256`) covers only `getrichtextfrommarkdown`, so `normalise_output_names()` /
`verify_output_names()` — the machinery built for exactly this defect class — cannot see it.

The consequence is worse here than at the Sync site because of how the branch is written. If
the reference does not resolve, `Panic Escape Section` is empty, the condition-99 "contains"
test against `- Panic Escape: OFF` is always false, and control falls to the otherwise arm,
whose own comment says: *"Anything else … can only ever restore, never remove."* The user then
sees `"The Note says ON and Panic Escape is already available. Nothing was changed."` — a
confident, wrong, unlogged success message. The entire removal feature this phase shipped is
dead with no error anywhere.

The Sync My Profile instance is equally silent: it would store an empty
`profile_snapshot.proforma` forever.

**Fix:** Use the corpus-attested name at both sites and add the entry to the recurrence guard
so a third site cannot repeat it:

```python
# tools/build_state_engine.py
ACTION_OUTPUT_NAMES = {
    "is.workflow.actions.getrichtextfrommarkdown": "Rich Text from Markdown",
    "is.workflow.actions.text.match": "Matches",   # golden corpus 15/15
}
```

`normalise_output_names()` then rewrites both sites automatically and `verify_output_names()`
fails the build on any regression. Note the residual shape question — `text.match`'s output is
a *list* of matches, so `gettext` over it stringifies a one-element list; if the on-device
round trip shows that is not the value wanted, use
`is.workflow.actions.getitemfromlist` with `WFItemSpecifier="First Item"` between them, exactly
as `build_sentient.py:159` already does.

---

### CR-03: in the Aware fork the Use Model audit only exists on the Panic-Escape-enabled path

**File:** `tools/build_sentient.py:265-271`; interaction with `tools/build_state_engine.py:1014-1020`

**Issue:**

```python
for index, item in enumerate(actions):
    value = item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")
    if value.startswith("Reload before writing a contract."):
        actions[index:index] = audit_block()
        break        # <-- first marker only
```

Before this phase there was one OPEN-arm `primitive_dispatch()` rendering, so "first marker"
and "the OPEN-arm marker" coincided. Plan 11-05 added a second OPEN-arm rendering (the
`panic_escape_enabled == 0` otherwise arm of `universal_leaving()`), rendered *after* the
Continue arm in document order. Measured on the shipped `src/PROSOCHE-Sentient.xml`:

```
dispatch renderings:  998, 1328, 1842, 2115, ... (11 total)
persist_contract:    1150, 1414, 1926, 2199, ... (11 total)
audit marker:        1084   <-- inside rendering #1 (Continue) only
askllm:              1108   <-- exactly one, same place
```

So an Aware user who removes Panic Escape reaches the `Intention` (Confession) primitive with
**no contract audit at all** — the entire reason the Aware fork exists disappears because of an
unrelated bypass setting, silently and with no fork-level difference the user can observe.

`docs/sentient_core_check.py:102-103` asserts `len(models) == 1`, which locks this in rather
than detecting it, and `build_sentient.py` does not run `verify_circle_zero_silence()` or any
per-rendering coverage guard that would notice.

**Fix:** Insert the audit into every OPEN-arm rendering, and assert the count rather than
pinning it to one. Locate the OPEN arm structurally (the same way
`verify_circle_zero_silence()` does), then:

```python
open_index, open_end = open_arm_bounds(actions)          # reuse the router-shape locator
targets = [i for i in range(open_index, open_end)
           if actions[i].get("WFWorkflowActionParameters", {})
              .get("WFCommentActionText", "").startswith("Reload before writing a contract.")]
if not targets:
    raise SystemExit("semantic Confession contract marker not found in the OPEN arm")
for index in reversed(targets):                          # reverse so earlier indexes stay valid
    actions[index:index] = audit_block()
```

`audit_block()` calls `uid(name)` with fixed literal keys, so multiple renderings would collide
on `GroupingIdentifier`/`UUID` — `uid()` must take a per-rendering discriminator
(`uid(f"{ordinal}/{name}")`) or the second rendering will reuse the first's grouping
identifiers, which `.claude/CLAUDE.md` §4 names as the top real-world failure mode. Then change
`docs/sentient_core_check.py:103` from `== 1` to the measured OPEN-arm rendering count, with a
comment deriving it.

If the intended decision is instead "audit only the Panic-Escape path", that is a product
decision that must be written down in `docs/CAPABILITY-DECISIONS.md` and surfaced in the Note,
because it makes an unrelated setting silently switch forks.

## Warnings

### WR-01: `verify_panic_escape_seed()`'s gate check is coupled to a magic variable name and silently passes when it drifts

**File:** `tools/build_state_engine.py:2702-2705`

**Issue:** The third assertion matches conditionals by
`VariableName == "Panic Escape Enabled"` — a bare literal that appears nowhere as a shared
constant (the emitter uses its own literal at `:991-992`). I demonstrated the gap: rename the
variable to `PE` *and* flip the gate to condition 100, and the guard passes clean. It also does
not cover the two `"Panic Escape Stored"` gates in `panic_escape_branch()` (`:2043`, `:2071`),
which decide whether the flag is written and are subject to the identical axis-7 trap.

**Fix:** Resolve the tested variable by provenance instead of by name — `_read_variable_keys()`
already maps variables to the literal key they were read from — and cover *every* variable read
from `panic_escape_enabled`:

```python
reads = _read_variable_keys(actions)
guarded = {name for name, keys in reads.items() if PANIC_ESCAPE_KEY in keys}
...
if name in guarded and parameters.get("WFCondition") not in NUMERIC_CONDITION_CODES:
    existence.append((index, parameters.get("WFCondition")))
```

Additionally assert `guarded` is non-empty, so a rename that orphans the gate entirely fails
rather than passes vacuously.

---

### WR-02: `MINIMUM_TOKEN_STRINGS = 775` is ~36% below the measured value, so the floor guard has 430 units of slack

**File:** `docs/note_identity_check.py:84`

**Issue:** The docstring says the floor was "Measured at the phase-11 baseline (`ae0226c`) and
re-measured on the decrypted payload of both signed containers." Measured now with the file's
own counting method: **1205 (Dumb) / 1209 (Sentient)**. MANIFEST.md:173-174 states the
pre-phase baseline was 1105/1109. 775 matches neither. The named defect — parameter-defect
axis 2, string-typed parameters converted to bare `WFTextTokenAttachment` — could hit 430 sites
and still pass.

**Fix:** Set the floor to the measured value and derive it in a comment the way
`environmental_restore_check.py`'s site table does:

```python
# Measured 2026-08-17 on both shipped forks: 1205 (Dumb) / 1209 (Sentient).
# The floor is the LOWER of the two so one constant serves both.
MINIMUM_TOKEN_STRINGS = 1205
```

---

### WR-03: the brightness-floor assertion in `phase5_self_check.py` is vacuous

**File:** `docs/phase5_self_check.py:117`

**Issue:**

```python
require(params.get("WFBrightness") not in (0, "0", 0.0), "brightness may reach zero")
```

`set_brightness()` (`build_state_engine.py:433`) always passes a `variable(...)` dict.
Measured: all 15 `WFBrightness` values in each fork are `dict`. The comparison can never be
true, so this line has never had the capacity to fail. It reads as a safety assertion and is
decoration.

**Fix:** Either delete it (BD-02's Phase 9 addendum removed the absolute floor anyway, so the
real invariant is capture-and-restore, which `environmental_restore_check.py` owns), or make it
test something real — that the write's operand is a variable read from `safety.dim_target` or
`settings_snapshot.*.original_value` and never a literal:

```python
value = params.get("WFBrightness")
require(isinstance(value, dict) and value.get("Value", {}).get("Type") == "Variable",
        "a Set Brightness write carries a literal target instead of a captured/config variable")
```

---

### WR-04: nothing reconciles `PROFILE_NAMES` with the Config key paths or the hand-authored bootstrap chain — five copies, hard-error consequence

**File:** `tools/build_state_engine.py:56`; `src/PROSOCHE-Dumb.xml` actions 2, 7, 55-65

**Issue:** `build_state_engine.py:53-55`'s own comment states the stakes exactly: *"a profile
name is a live Config key path (`thresholds.<profile>`, `cooldown_seconds.<profile>`), and a
dotted read with a missing segment is a HARD ERROR in this runtime, so a partial rename here is
a crash rather than a degradation."* There is no guard.

The profile vocabulary exists in five independent, unlinked places:

1. `PROFILE_NAMES` (`:56`) — drives the Change Profile submenu, which writes `profile` directly;
2. the Config literal's `thresholds` keys (action 7) — read as `thresholds.<profile>`;
3. the Config literal's `cooldown_seconds` keys — read as `cooldown_seconds.<profile>`;
4. the **hand-authored** import normalisation chain (actions 55-65: literals `Paradise`,
   `Inferno`, fallback gettext `Purgatory`) — the only thing that decides the first-run value;
5. the import-question default and its Text action (action 2).

Only (1) is generated. Renaming a profile in `PROFILE_NAMES` without editing (2)-(5) — or vice
versa — builds, signs, imports, and then hard-errors on the first OPEN with "could not evaluate
the key path". This is structurally the same defect `verify_dispatch_coverage()` exists to
catch on the sequences side, on a path with a worse failure mode.

**Fix:** Add `verify_profile_coverage()` beside `verify_dispatch_coverage()` and run it in both
builders:

```python
def verify_profile_coverage(actions):
    config = json.loads(<the Config literal, located as verify_dispatch_coverage does>)
    for table in ("thresholds", "cooldown_seconds"):
        keys = set(config.get(table, {}))
        if keys != set(PROFILE_NAMES):
            raise SystemExit(
                f"profile coverage: Config.{table} names {sorted(keys)} but PROFILE_NAMES is "
                f"{sorted(PROFILE_NAMES)} -- `{table}.<profile>` is a DOTTED read, so a name "
                "that no key matches is a hard 'could not evaluate the key path' error on the "
                "next OPEN, after active_session was already written")
    # every literal the bootstrap chain and the profile menu can ever write must be a key
    written = {p["WFTextActionText"] for p in (a.get("WFWorkflowActionParameters", {})
               for a in actions) if isinstance(p.get("WFTextActionText"), str)
               and p["WFTextActionText"] in set(PROFILE_NAMES) | keys}
    ...
```

The minimum useful version is the first half: `set(config["thresholds"]) ==
set(config["cooldown_seconds"]) == set(PROFILE_NAMES)`.

---

### WR-05: `state_engine_self_check.THRESHOLDS` duplicates the Config literal with no assertion, and this pair has already drifted once

**File:** `docs/state_engine_self_check.py:15-19`

**Issue:** The comment says "This table is a duplicate of the Config literal at
`src/PROSOCHE-Dumb.xml` action 7 and must be changed in the same commit as it." Nothing
enforces it, and `src/CONFIG-BLOCK.md:164` records that this exact pair *did* silently drift
through Phase 10 ("the pre-existing `thresholds` drift, where this mirror still showed the
pre-Phase-10 curve"). Phase 11 edited the table again (`Limbo` → `Purgatory`) and still did not
add the reconciliation. `structural_check()` in the same file already parses the artifact, so
the data is one line away.

**Fix:** In `structural_check()`, parse the Config literal and assert equality:

```python
config = json.loads(next(p["WFTextActionText"] for p in
                         (a.get("WFWorkflowActionParameters", {}) for a in actions)
                         if isinstance(p.get("WFTextActionText"), str)
                         and '"config_version"' in p["WFTextActionText"]))
assert config["thresholds"] == THRESHOLDS, (
    f"THRESHOLDS mirror {THRESHOLDS} disagrees with the shipped Config literal "
    f"{config['thresholds']} -- this file's arithmetic then verifies a curve nothing ships")
```

---

### WR-06: three generator constants are coupled to hand-authored Note copy with no assertion

**File:** `tools/build_state_engine.py:1979` (`PANIC_ESCAPE_OFF_LINE`), `:1984` (`PANIC_ESCAPE_SECTION_PATTERN`), `:47-48` (`CIRCLE_NAMES`)

**Issue:** The Note body is a hand-authored `WFTextTokenString` in the artifact, edited through
`plist_text_edit.py`. Three separate generator constants depend on its exact wording, and
nothing checks any of them:

- `PANIC_ESCAPE_SECTION_PATTERN` requires `## PANIC ESCAPE` to exist and to be followed by
  `## MY PHONE, ON PURPOSE`. Reordering or renaming either heading yields an empty match, which
  the branch (by design, `:2039`) treats as "restore only, never remove" — the feature dies
  with no error.
- `PANIC_ESCAPE_OFF_LINE` (`- Panic Escape: OFF`) must be the exact mirror of the Note's live
  `- Panic Escape: ON` line, including the leading `- ` and the capitals. A copy edit to
  `— Panic Escape: OFF` or `Panic Escape — OFF` kills removal silently.
- `CIRCLE_NAMES` is described in its own comment as "ONE SOURCE OF TRUTH", but the Note carries
  a **fourth, hand-written copy** of the nine names (`- Circle 1 · Limbo` … `- Circle 9 ·
  Treachery`, Note offset 5149). Renaming a Circle in the tuple leaves the Note stale.

**Fix:** Extend `docs/note_identity_check.py` — it already locates the Note body by content and
already parses both forks — with three assertions:

```python
body = <the Note body string, already located>
require(body.count("## PANIC ESCAPE") == 1 and
        body.index("## PANIC ESCAPE") < body.index("## MY PHONE, ON PURPOSE"),
        "the PANIC ESCAPE section is missing or no longer precedes MY PHONE, ON PURPOSE -- "
        "the bounded text.match returns nothing and Panic Escape can then only ever restore")
require(re.search(r"^- Panic Escape: (ON|OFF)$", body, re.M),
        "the Note's Panic Escape setting line no longer matches the '- Panic Escape: <WORD>' "
        "shape PANIC_ESCAPE_OFF_LINE mirrors")
for n, name in enumerate(CIRCLE_NAMES, 1):          # import from the generator
    require(f"- Circle {n} · {name}" in body,
            f"the Note's Circle list is stale: it does not name Circle {n} as {name!r}")
```

---

### WR-07: `plist_text_edit.py` is declared the trusted path but the generator keeps a divergent private copy, and four of the module's six exports have no caller

**File:** `tools/plist_text_edit.py:71,81,156,179`; `tools/build_state_engine.py:2453-2478`

**Issue:** The module docstring presents a six-step method and says step 1 — "Prove a no-op
`plistlib.dumps` is byte-identical to the source → `assert_noop_roundtrip()`" — "licenses every
later structured edit." Grep across `tools/` and `docs/` shows the only importer is
`build_sentient.py:12`, and it imports only `find_action` and `replace_in_token`. `load()`,
`assert_noop_roundtrip()`, `replace_in_plain()` and `save()` have no caller anywhere. Step 1 of
the module's own method is never executed by any automated path.

Meanwhile `build_state_engine.py` keeps `_replace_in_token()` — a second, materially different
implementation used for all four bootstrap-template edits, including this phase's new
`seed_panic_escape()`:

| | `plist_text_edit.replace_in_token` | `build_state_engine._replace_in_token` |
|---|---|---|
| occurrences replaced | all, with an asserted count | **first only** (`string.find`) |
| offset strategy | rebuild from a rescan of placeholders | shift by `delta` where `offset > at` |
| pre-edit offset validation | yes (`assert_offsets_match`) | no |
| placeholder-count invariant | asserted | not asserted |

The shift predicate `offset > at` is also subtly wrong for an attachment landing inside the
replaced span (it would be shifted rather than rejected); no current call site hits that, but
the divergence means the "trusted path" claim is not true of the code that does the most
editing.

**Fix:** Delete `_replace_in_token()` and have `seed_settings_snapshot()`,
`seed_pending_exit()`, `seed_panic_escape()` and `fix_state_rebind()` call
`plist_text_edit.replace_in_token(inner, old, new, expected_count=1)`. Then either wire
`assert_noop_roundtrip()` into `main()` (`data, raw = plist_text_edit.load(SOURCE)` at the top,
`assert_noop_roundtrip(data, raw)` immediately after) or delete `load`/`assert_noop_roundtrip`/
`save`/`replace_in_plain` and correct the docstring so it stops describing steps no caller
runs.

---

### WR-08: `plist_text_edit` discards the length component of every range key and silently rewrites it to 1

**File:** `tools/plist_text_edit.py:61-68, 97-116, 151-152`

**Issue:** `_key_offset()` matches `{offset, length}` but returns only `group(1)`.
`assert_offsets_match()` compares offsets only. `replace_in_token()` then emits every key as
`f"{{{offset}, 1}}"`. So a key of `{5478, 3}` passes the "offsets match" assertion and is
silently rewritten to `{5478, 1}` — an edit the module never reports. The docstring at `:42`
asserts "which is why every `attachmentsByRange` key has length 1" but no code enforces it.
(Measured: all 1654 / 1664 keys in the shipped forks currently have length 1, so this is
latent, not live.)

**Fix:** Assert the invariant where it is claimed:

```python
def _key_range(key: str) -> tuple[int, int]:
    match = RANGE_KEY.match(key)
    if not match:
        raise SystemExit(...)
    offset, length = int(match.group(1)), int(match.group(2))
    if length != 1:
        raise SystemExit(
            f"attachmentsByRange key {key!r} has length {length}, not 1 -- a U+FFFC "
            "placeholder is exactly one character, so a longer range already spans unrelated "
            "prose and this module would silently rewrite it to 1")
    return offset, length
```

---

### WR-09: offsets are computed as Python code points, not UTF-16 units, with no assertion that the difference is nil

**File:** `tools/plist_text_edit.py:111, 145`; `docs/note_identity_check.py:146`

**Issue:** `enumerate(string)` yields code-point indices. `attachmentsByRange` keys are NSRange
offsets into an `NSAttributedString`, i.e. **UTF-16 code units**. For everything currently in
the artifact the two agree — I scanned both forks and found **zero** characters above U+FFFF
(`Ē` U+0112, `—` U+2014, `·` U+00B7, `⚠` U+26A0 are all BMP). But the module is explicitly
positioned as the sanctioned path for *future* Note copy edits, and a single emoji (U+1F600+)
placed upstream of an attachment would shift every subsequent iOS offset by one per astral
character while this code computes it unshifted — producing exactly the out-of-bounds range the
module exists to prevent.

**Fix:** Make the assumption explicit and enforced, so the failure is a build error rather than
a device crash:

```python
def _assert_bmp_only(string: str, where: str) -> None:
    astral = sorted({c for c in string if ord(c) > 0xFFFF})
    if astral:
        raise SystemExit(
            f"{where}: the string contains non-BMP character(s) {astral} -- this module "
            "computes offsets as Python code points, but attachmentsByRange keys are UTF-16 "
            "NSRange offsets, so every attachment after such a character would be off by one "
            "per astral character and an out-of-bounds range can crash Shortcuts on import")
```

Call it from `assert_offsets_match()` and from `replace_in_token()` on both the old and new
strings. Add the same scan to `note_identity_check.check_offsets()`.

---

### WR-10: `build_sentient.py` runs a hand-maintained subset of the generator's verify chain, omitting both guards added this phase

**File:** `tools/build_sentient.py:281-313`

**Issue:** The file's own comments justify running each guard per fork ("asserted per fork,
never inferred"). Six guards `build_state_engine.main()` runs are absent from the Aware chain:

- `verify_parameter_keys`
- `verify_conditional_action_string`
- `verify_pending_exit_seed`
- `verify_panic_escape_seed` — added this phase
- `verify_compound_value_reads`
- `verify_circle_zero_silence`

The last two matter most. Sentient *inserts actions into the OPEN arm* (`audit_block()`, which
adds conditionals, a `returntohomescreen` and an `exit`), so `verify_circle_zero_silence()`'s
four properties are precisely the ones a Sentient-only insertion could break, and the fork is
the only artifact where they are not asserted. `verify_panic_escape_seed()` is skipped even
though `verify_state_seed()` is run with the rationale "it proves the subtree survived the
fork" — and `verify_panic_escape_seed()`'s own docstring records that `verify_state_seed()`
does not cover the panic field.

There is also no mechanism preventing further drift: adding a guard to `main()` does not add it
here.

**Fix:** Export the chain as data from `build_state_engine.py` and have both builders consume
it, so a new guard is armed in both by construction:

```python
# build_state_engine.py
VERIFIERS = (verify_parameter_keys, verify_string_envelopes, verify_output_names,
             verify_required_pickers, verify_conditional_inputs,
             verify_conditional_action_string, verify_numeric_operands,
             verify_state_seed, verify_pending_exit_seed, verify_panic_escape_seed,
             verify_restore_gates, verify_sentinel_gates, verify_compound_value_reads,
             verify_router_shape, verify_circle_zero_silence, verify_dispatch_coverage)

def verify_all(actions):
    for check in VERIFIERS:
        check(actions)
```

If any single guard genuinely cannot apply to the fork, exclude it by name with a written
reason rather than by omission.

---

### WR-11: `build_sentient.py` addresses the import-preference insertion by a hard-coded action index

**File:** `tools/build_sentient.py:258-262`

**Issue:**

```python
actions[6:6] = [action("is.workflow.actions.gettext", UUID=import_id, WFTextActionText="yes"),
                set_var("Import AI", output(import_id, "Text"))]
root["WFWorkflowImportQuestions"].append({"ActionIndex": 6, ...})
```

`build_state_engine.py`'s module docstring states the rule: *"Anchors are found by their branch
comments, never by mutable action indexes."* This is the one place that breaks it, and it
breaks it twice — the splice position and the `ActionIndex` both hard-code 6.
`build_state_engine.main()` pins only actions 0-4 (`pinned = actions[:5]`) and
`phase5_self_check` pins `ids[:5]`, so actions 5 and 6 are *unpinned*. A future generator change
that inserts an action at index 5 would move the third import question onto an unrelated
parameter with no error from either builder; `sentient_core_check.py:109-110` would then catch
it, but only after the fork is built.

**Fix:** Locate the insertion point by content and derive the index:

```python
anchor = next(i for i, a in enumerate(actions)
              if a.get("WFWorkflowActionParameters", {}).get("WFVariableName") == "Import Voice")
at = anchor + 1
actions[at:at] = [...]
root["WFWorkflowImportQuestions"].append({"ActionIndex": at, ...})
```

and extend `build_state_engine.main()`'s pin from `actions[:5]` to cover the full frozen import
prologue.

---

### WR-12: seed helpers raise bare `StopIteration` / `IndexError` instead of the project's SystemExit-with-consequence convention

**File:** `tools/build_state_engine.py:2590` (`seed_pending_exit`), `:2658` (`seed_panic_escape`), `:2477` (`_replace_in_token`)

**Issue:** Both new-generation seeders locate their anchor line with an unguarded `next()`:

```python
line = next(text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text)
```

If `'"ai_enabled": false,'` ever moves or is reformatted, this raises a bare `StopIteration`
with no message — against the file's own stated failure convention ("every guard raises
`SystemExit` with a message naming the CONSEQUENCE"), and inside a generator expression, which
in some contexts is swallowed rather than propagated. `seed_settings_snapshot()` gets this right
(`:2489` returns early when the anchor is absent). Separately, `_replace_in_token()`'s
post-shift validation `inner["string"][offset] != "￼"` can raise `IndexError` when a shrinking
edit pushes an offset past the end of the new string.

**Fix:**

```python
line = next((text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text), None)
if line is None:
    raise SystemExit(
        f"the bootstrap template no longer contains the anchor {PANIC_ESCAPE_ANCHOR!r}, so "
        f"{PANIC_ESCAPE_KEY} cannot be seeded -- universal_leaving()'s gate would then read a "
        "key that is not there and the Panic Escape removal path is dead on every device")
```

and in `_replace_in_token()` bounds-check before indexing:

```python
if offset >= len(inner["string"]) or inner["string"][offset] != "￼":
    raise SystemExit(f"attachment offset {offset} is out of bounds or no longer points at a "
                     "placeholder -- an out-of-bounds range can crash Shortcuts on import")
```

---

### WR-13: MANIFEST.md's dispatch-branch count is stale by nine

**File:** `artifacts/shortcuts/MANIFEST.md:223-224`

**Issue:** "All nine shipped names are proven present in the generator tuple, in all three
`sequences` arrays, **on all ninety emitted dispatch branches** and in the decrypted payload of
both signed containers, and every one of those branches is proven to carry condition code 4."

Measured on the shipped artifacts: **99** branches per fork (9 names × 11 renderings), not 90.
The eleventh rendering is this phase's own Panic Escape change, described correctly elsewhere in
the same document (`docs/environmental_restore_check.py`'s table and BUILD-NOTES §24.3 both moved
to eleven). MANIFEST.md is described in `manifest_check.py`'s docstring as "the only
human-readable claim this repository makes about what shipped"; a wrong count in it is a false
provenance claim of exactly the kind that check exists to prevent, and `manifest_check.py`
validates only the table rows, not the prose.

**Fix:** Change "ninety" to "ninety-nine (nine names × eleven `primitive_dispatch()`
renderings)" and cross-check the same paragraph against BUILD-NOTES §24.3's rendering-count
derivation, which is correct.

---

### WR-14: the two display names exist as three unlinked hardcoded copies, and one assertion is a suffix test

**File:** `tools/build_sentient.py:38-39`; `docs/manifest_check.py:51-54, 130`; `docs/sentient_core_check.py:33-34, 51`

**Issue:** `CORE_NAME`/`AWARE_NAME`, `DISPLAY_NAMES`, and `CORE`/`AWARE` are three independent
literal pairs with no import relationship and no cross-assertion. `manifest_check.py:130` still
carries the stale comment `# "Dumb" / "Sentient"` on a line that now yields `"Core"`/`"Aware"`.
`sentient_core_check.py:51` asserts only `SENTIENT["WFWorkflowName"].endswith("Aware")`, which
passes for any string ending in those five characters. Nothing at all asserts the **Core** fork's
root `WFWorkflowName` — it is hand-set in `src/PROSOCHE-Dumb.xml` and never verified, even
though MANIFEST.md:186-192 makes the filename/display-name equality the load-bearing anti-dead-
install rule.

The Note↔`CORE_NAME` coupling *is* guarded, indirectly and well, by `fix_fork_strings()`'s
`expected_count=2`.

**Fix:** Put the pair in one place — `tools/build_sentient.py` already owns them — and import it
in both checkers (`docs/` scripts already add `tools/` to `sys.path` via
`environmental_restore_check.load_module`). Then tighten:

```python
# sentient_core_check.py
assert SENTIENT["WFWorkflowName"] == AWARE, SENTIENT["WFWorkflowName"]
assert DUMB["WFWorkflowName"] == CORE, DUMB["WFWorkflowName"]
```

and update `manifest_check.py:130`'s comment to `# "Core" / "Aware"`.

---

### WR-15: T-11-22 — the phase's only `critical` threat — has no standing checker

**File:** `artifacts/shortcuts/MANIFEST.md:89-93`; no corresponding `docs/*.py`

**Issue:** The separation of Panic Escape from Emergency Restore is described in
`universal_leaving()`'s docstring (`build_state_engine.py:958-964`) as threat T-11-22, "the only
`critical` in this phase". Its verification is a hand-measurement recorded in MANIFEST prose:
"Re-measured on the decrypted payloads … two menus offer Emergency Restore and two case bodies
implement it in each fork, and **none of the four is enclosed by any Panic Escape
conditional**."

I reproduced that measurement and it holds today (Dumb actions 171/174/1665/4229, Sentient
173/176/1733/4297, zero Panic Escape enclosures). But a hand-measurement recorded in a markdown
file is not a guard: the next change to `universal_leaving()` or `panic_escape_branch()` will not
re-run it. Every other invariant of comparable weight in this repo (dispatch coverage, restore
gates, sentinel gates, router shape, silent band) has an executable guard.

**Fix:** Add `verify_panic_escape_isolation()` to the shared `VERIFIERS` tuple — the enclosure
machinery already exists (`enclosing_groups()`, `:1487`):

```python
def verify_panic_escape_isolation(actions):
    panic = {p["GroupingIdentifier"] for p in (a.get("WFWorkflowActionParameters", {}) for a in actions)
             if p.get("WFControlFlowMode") == 0
             and _tested_variable(p) in ("Panic Escape Enabled", "Panic Escape Stored",
                                         "Manual Panic Escape Requested")}
    enclosure = enclosing_groups(actions)
    sites = [i for i, a in enumerate(actions)
             if a.get("WFWorkflowActionParameters", {}).get("WFMenuItemTitle") == "Emergency Restore"
             or "Emergency Restore" in (a.get("WFWorkflowActionParameters", {}).get("WFMenuItems") or [])]
    if not sites:
        raise SystemExit("no Emergency Restore surface found at all -- the safety hatch is gone")
    caught = [i for i in sites if set(enclosure[i]) & panic]
    if caught:
        raise SystemExit(
            f"Emergency Restore is enclosed by a Panic Escape conditional at actions {caught} -- "
            "T-11-22: a user who removed the bypass and cannot reach Emergency Restore is "
            "stranded inside an intervention with a dimmed screen or a silenced device")
```

Also note the interaction BD-06-A2 does not record: shortening the Note title to the bare
product name widened the `contains` lookup, so a wrong-Note binding is now more likely — and a
wrong Note has no `## PANIC ESCAPE` section, which makes the new removal path silently
unavailable (the same otherwise-arm behaviour as CR-02). Worth adding to BD-06-A2's recorded
consequences.

---

_Reviewed: 2026-08-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
