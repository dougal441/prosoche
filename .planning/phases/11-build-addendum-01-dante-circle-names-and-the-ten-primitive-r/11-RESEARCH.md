# Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster — Research

**Researched:** 2026-08-17
**Domain:** Codebase archaeology over a hand-authored iOS 26 Shortcuts plist mutated in place by a Python transformer. Mass rename across a Config literal, ten dispatch renderings, a `WFTextTokenString` Note body with absolute attachment offsets, eleven structural checkers, and two signed display names.
**Confidence:** HIGH for every code-level fact below — all measured this session against the working tree at `ae0226c`, with the command shown. LOW/UNVERIFIED items are labelled inline and say what evidence would settle them.

**Nothing in this phase is answerable from the internet.** Zero web lookups were performed and none are warranted: every fact the planner needs is in this repository, and the project's standing evidence hierarchy (`.claude/CLAUDE.md` §"Evidence hierarchy") ranks device donors, the golden corpus and the ToolKit catalog above inference — none of which a search engine supplies.

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Verbatim from `11-CONTEXT.md` `<decisions>`:

> ### Claude's Discretion
> All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.
>
> ### Binding constraints carried in from the project (not discretionary)
> - BD-06 in `docs/CAPABILITY-DECISIONS.md` is settled and binding — do not re-cut the naming/roster table.
> - `.claude/CLAUDE.md` "Generator authoring rules — the seven parameter-defect axes" apply to every plist edit.
> - Rebuild provenance gate: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running `tools/build_state_engine.py` or `tools/build_sentient.py`.
> - Validator invocation is `--target-macos 26 --target-platform all`.
> - A validator pass is not "done" — archive + sign + verify non-zero bytes is the definition of done.

### Claude's Discretion

All implementation choices, per the block above. The discretion is bounded by the five binding constraints and by BD-06's six decisions, transcribed in §1 below.

### Deferred Ideas (OUT OF SCOPE)

Verbatim from `11-CONTEXT.md` `<deferred>`:

> None — discuss phase skipped.

**Out of scope by intermediate-state instruction** (from the ROADMAP/CONTEXT phase boundary, not a "deferred idea" but functionally the same constraint):
- `Redirect`'s implementation — Phase 17. All three sequences hold `Eject` at Circle 6 this phase.
- The designed Voice primitive — Phase 15. Circle 8 gets an interim real branch here.
- Ash as a real Color Filters toggle — Phase 14. `ash()` stays the alert-only fallback; only its *name* changes here.
- Dimming/Silence device-proving — Phase 16.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (from `.planning/REQUIREMENTS.md`) | Research support |
|----|-------------|------------------|
| AUDIT-02 | "Grayscale / Color Filters capability is resolved to a go/no-go decision, and the Ash primitive has a documented fallback design if no safe action exists" | BD-06 marks AUDIT-02 as *extended*, not re-decided. This phase renames Ash→**Black and White** only; §4 gives the two source sites. `docs/phase5_self_check.py:78` still asserts `"AXToggleColorFiltersIntent" not in text` — that assertion stays green here and is Phase 14's to flip. |
| CIRC-02 | "Ash applies the audited visual-salience reduction, or its documented fallback if no safe action exists" | Same as above — rename-only. `ash()` at `tools/build_state_engine.py:486-490` is unchanged in behaviour. |
| CIRC-06 | "Exile immediately routes to an exit without a permission prompt, and returning remains possible as an affirmative act" | `exile()` at `:580-584` becomes the **Eject** branch. `Redirect` is named in the roster but must NOT appear in any sequence array this phase (§3). |
| CIRC-08 | "The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels" | Circle 8 currently dispatches **nothing** — measured orphan, §5. This phase gives it a real branch (`Loud Mirror` → interim `mirror_and_voice()`), which is what makes the dispatch-coverage guard a hard gate. |
| ROOM-01 | "The Note opens with READ THIS FIRST explaining what PROSOCHĒ is and how to create both automations" | Note body is action **3616** (Dumb) / **3684** (Sentient), a `WFTextTokenString` with two absolute attachment offsets. §6 gives the full edit hazard. |
| ROOM-02 | "The Note gives exact steps for Automation A (App / selected apps / Is Opened / run automatically / Run Shortcut / pass input `OPEN`)" | Both automation blocks name the Run Shortcut target `PROSOCHĒ — Nine Circles — Dumb` verbatim. A Dumb→Core rename **must** rewrite both, per `docs/BUILD-NOTES.md` §9. §7. |
| DIST-01 | "Both forks pass the Shortcuts Playground validator at the iOS 26 target" | Pipeline invariants, §10. |
| DIST-02 | "Both forks sign successfully into importable `.shortcut` files" | Signed display names are load-bearing and hardcoded in `docs/manifest_check.py`. §7. |
</phase_requirements>

---

## Summary

`src/PROSOCHE-Dumb.xml` is **not a generated file in the ordinary sense**. `tools/build_state_engine.py:15` sets `SOURCE = Path("src/PROSOCHE-Dumb.xml")` and `main()` reads that same file, replaces marker-bounded branch bodies, runs a series of `fix_*`/`normalise_*`/`verify_*` sweeps, and writes it back to the same path (`:3155`). Everything *outside* a marker-bounded region — the Config JSON literal, the bootstrap `state.json` template, the whole Control Room Note body, the Find-Notes predicate, the Create-Note title — lives **only in the XML** and has no Python source. Grep the generator before assuming it owns any string; the quick task `260817-au7` established exactly this rule and its SUMMARY records it as a pattern.

That single architectural fact reshapes the whole phase. The rename is **two different jobs, not one**: (a) Python-side edits to the eight dispatch-branch names and the condition code in `primitive_dispatch()`; (b) direct, guarded plist edits to the Config literal's three `sequences` arrays, the Note title's three occurrences, the Note body's copy, and the `"fork": "Dumb"` seed. Job (b) must go through a `plistlib` round-trip that recomputes `attachmentsByRange`, never string substitution — the Note body carries two attachments at absolute offsets `{5478, 1}` and `{5509, 1}` that almost any copy edit invalidates, and out-of-range attachment ranges can crash Shortcuts on import.

Three things are load-bearing and easy to get wrong. First, the 99→4 dispatch move is **not cleanup** — it is a correctness prerequisite for the new roster: under condition 99 ("contains"), the existing `Mirror` branch fires for the entry `Loud Mirror`, so the new Circle-8 name is undispatchable until the move happens. Second, the Apple Note rename to bare `PROSOCHĒ` leaves the Find-Notes predicate at `Operator: 99` ("Name contains"), which after the rename matches *any* note containing `PROSOCHĒ` — including a stale `PROSOCHĒ — Control Room` from a prior install, bound as "First Item" with a limit of 1. Third, `Limbo` is already a **profile** name in the artifact (12 occurrences, all profile) and BD-06 Decision 2 makes it Circle 1's name too — a real namespace collision that must be handled deliberately, not discovered on device.

**Primary recommendation:** land the phase as four separable units in this order — (1) generator-side rename + condition 99→4 + the new `Loud Mirror` branch, (2) the `verify_dispatch_coverage()` build guard plus the promotion of `docs/sequence_dispatch_check.py` from reporter to gate, (3) the plist-side Config/Note/state-seed edits via a guarded `plistlib` round-trip, (4) fork rename + rebuild/validate/sign/decrypt-verify/MANIFEST. Unit 2 before unit 3 so the guard is already hard when the sequence arrays move — which is precisely why BD-06 says to write it "during the rename, not after it."

---

## Project Constraints (from `.claude/CLAUDE.md`)

Extracted as actionable directives. The planner must verify compliance against each.

| # | Directive | Applies to this phase because |
|---|---|---|
| C1 | Every iOS action identifier and parameter shape must be verified before use; never fabricate an action | No new action identifiers are needed — the phase adds no new action types, only reuses `mirror_and_voice()`. Low exposure. |
| C2 | **Provenance gate:** `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running either builder | Both builders run. Measured **PASS (exit 0)** at `ae0226c` this session. |
| C3 | Validator: `--target-macos 26 --target-platform all`. Never `27`/`latest`, never `ios` (DEV-01) | Both forks validate. |
| C4 | A validator pass is not done — archive + sign + verify non-zero bytes | §10. |
| C5 | **Seven parameter-defect axes.** Axis 2/3 (string-typed params need `WFTextTokenString`), axis 5 (variable slots take the inverse envelope), axis 6 (non-text params fed by a variable need an explicit coercion aggrandizement) | The dispatch conditionals use `WFConditionalActionString` as a **plain literal string** with **no** coercion — measured, all 80 sites (§5). Condition 4 is a string comparator so axis 6 does not apply. The Note body is a string-typed param and axis 2/3 governs its edit. |
| C6 | Signed filename must equal the display name exactly — no suffix | A Dumb→Core rename changes both signed basenames and `docs/manifest_check.py`'s hardcoded list. §7. |
| C7 | Fix whole classes, never site-by-site | The rename touches 3 sequence arrays × 9 slots, 8 dispatch branch names × 10 renderings, 2 forks. A per-site approach costs a device round trip per site. |
| C8 | Signed `.shortcut` files ARE recoverable via `aea decrypt` + `aa extract` — use it to verify what shipped | The decrypt-verify step is the only non-device "what shipped" channel. §10. |
| C9 | Operator/operand type validity is invisible in the plist — inspecting on device is a first-class evidence channel | The 99→4 move is a *code* change on a text-typed operand; both codes are string comparators so no red-operator risk. UNVERIFIED on device, but no type change occurs. |
| C10 | GSD workflow enforcement — no direct repo edits outside a GSD command | Planner's concern, not research. |

---

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale |
|---|---|---|---|
| Dispatch branch names + condition code | **Generator (Python)** — `primitive_dispatch()` | — | Emitted by a loop at `tools/build_state_engine.py:658-666`; changing the tuple changes all 10 renderings at once. |
| `sequences` arrays (three, nine slots each) | **Plist literal** — `src/PROSOCHE-Dumb.xml` action 7 | Doc mirror in `src/CONFIG-BLOCK.md:45-49` | No Python source exists. `grep -n "sequences" tools/*.py` returns only the *reader* (`:653`), never a writer. |
| Note display title (3 occurrences) | **Plist literal** — actions 3602, 3616, 3619 | — | Same: no Python source. |
| Note body copy | **Plist literal** — action 3616, a `WFTextTokenString` | — | Established by quick task `260817-au7`. |
| `"fork": "Dumb"` | **Plist literal** — bootstrap `state.json` template, action 75 | — | Sentient does *not* flip it — measured: Sentient's Note body still reads `- Fork: Dumb`. |
| Shortcut display name (`WFWorkflowName`) | **Plist root key** (Dumb) / **Generator** (Sentient, `tools/build_sentient.py:181`) | — | Asymmetric — Dumb's is in the XML, Sentient's is written by the builder. |
| Signed artifact filename | **Build pipeline** (`sign-shortcut --name`) + `docs/manifest_check.py:DISPLAY_NAMES` | `artifacts/shortcuts/MANIFEST.md` | The signer strips `WFWorkflowName`; the display name lives in the filename and nowhere else. |
| Dispatch-coverage invariant | **Generator build guard** (`verify_*` chain in `main()`) | `docs/sequence_dispatch_check.py` as the reporting eleventh check | BD-06 Decision 5 calls it "an eighth class alongside the seven parameter-defect axes" — the seven live as `verify_*` functions inside `main()`, so that is the guard's correct home. |
| Panic Escape removability | **Plist Note copy** (user-editable setting) + **generator** (`universal_leaving()` gate, MANUAL-arm confirmation) | `state.json` seed | The user "manually edits the setting in the Note", so the read path is the MANUAL arm's Note parse, never OPEN. §8. |

---

## 1. BD-06, transcribed verbatim — do not re-derive

Source: `docs/CAPABILITY-DECISIONS.md` lines 288–435. `[VERIFIED: read in full this session]`

### Decision 1 — Dante names are *positional*, not intervention names

> Circle 1 is **Limbo** and Circle 9 is **Treachery** regardless of which intervention fires there. The Dante name labels the *depth*; the sequence table decides the *intervention*.
>
> **Rationale — this is forced, not preferred.** PROSOCHĒ ships three sequences (`Classic` / `BlackMirror` / `Ambient`, `src/CONFIG-BLOCK.md`) which deliberately order the interventions differently at the same Circle numbers. A fixed name↔intervention binding therefore cannot survive a sequence switch: under `Ambient`, Circle 1 is Black and White, not Pause. Since Pressure resolves to a Circle *number* and the sequence array resolves that number to an intervention, the only stable thing a Dante name can attach to is the number.
>
> Addendum 01 §5's table is consequently read as **the `Classic` sequence expressed in renamed intervention terms**.

### Decision 2 — the names keep Dante's canonical order

| Circle | Name |
|---|---|
| 1 | Limbo |
| 2 | Lust |
| 3 | Gluttony |
| 4 | Greed |
| 5 | Wrath |
| 6 | Heresy |
| 7 | Violence |
| 8 | Fraud |
| 9 | Treachery |

> **Circle 9 is Treachery — Cocytus, a frozen lake — and Circle 9's intervention is Ice/Frozen in all three sequences.** Circle 1 is Limbo, the circle with no torment, and Circle 1 is a bare factual knock. Circle 7 is Violence, which in Dante includes violence against the self, and Circle 7 is the Mirror.

### Decision 3 — the roster is ten primitives; each sequence uses nine

> Nothing is dropped from the product. `sequences` is already per-sequence and there has never been a rule that every primitive appears in every ordering — with ten primitives, each nine-slot sequence simply selects nine.

| Internal primitive | Shipped name | Status entering this decision |
|---|---|---|
| Knock | **Pause** | built |
| Ash | **Black and White** | alert-only; real Color Filters to be built |
| Silence | **Silence** | built; restore device-unproven |
| Confession | **Intention** | built |
| Dimming | **Dim** | built; restore device-unproven |
| Exile (straight) | **Eject** | built (bare Home Screen) |
| Exile (routed) | **Redirect** | new — lands the user in a deterministically selected exit |
| Mirror | **Mirror** | built |
| Voice | **Loud Mirror** | dispatches nothing; to be built |
| Ice | **Frozen** | built |

> `Eject` is this decision's own coinage; Addendum 01 §5 supplies every other name, and its `Redirect` is taken as the *routed* Exile, which is what the word describes.

### Decision 4 — slot allocation (**the table; do not re-cut**)

| Circle | Name | Classic | BlackMirror | Ambient |
|---|---|---|---|---|
| 1 | Limbo | Pause | Pause | Black and White |
| 2 | Lust | Black and White | Intention | Silence |
| 3 | Gluttony | Silence | Black and White | Dim |
| 4 | Greed | Intention | Mirror | Pause |
| 5 | Wrath | Dim | Silence | Intention |
| 6 | Heresy | Redirect | Eject | Redirect |
| 7 | Violence | Mirror | Dim | Mirror |
| 8 | Fraud | Loud Mirror | Loud Mirror | Loud Mirror |
| 9 | Treachery | Frozen | Frozen | Frozen |

> `Classic` and `Ambient` take **Redirect**; `BlackMirror` takes **Eject** — the colder, unnegotiable ejection suits that sequence, and it gives every primitive at least one home. Each column preserves its source ordering's identity: `Classic` is the reference escalation from `src/CONFIG-BLOCK.md`, `Ambient` still leads with the three environmental primitives, `BlackMirror` still surfaces the Mirror early (Circle 4).
>
> **Verification against Addendum 01 §5.** The addendum's table reads Limbo=Pause, Lust=Black and White, Gluttony=Silence, Greed=Intention, Wrath=Dim, Heresy=Redirect, Violence=Mirror, Fraud=Loud Mirror, Treachery=Frozen. That is the `Classic` column above, entry for entry.

### Decision 5 — combined entries abolished; dispatch becomes an exact match

> `BlackMirror` previously carried three combined entries — `Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror`. All three are gone: every slot in the table above names exactly one primitive.
>
> `primitive_dispatch()` currently matches the sequence entry with **condition code 99 ("contains")** solely to make the combined entries work. That choice is precisely why Circle 8 shipped dead… With no combined entries left, dispatch moves to **condition code 4 ("string is")** — an exact match, under which an unmatched entry is a build-time failure rather than a silent runtime no-op.
>
> **Binding build guard.** Every distinct primitive name appearing in any `sequences` array in `src/CONFIG-BLOCK.md` must have exactly one matching dispatch branch in the generated actions, and every dispatch branch must be named by at least one sequence entry. This is an eighth class alongside the seven parameter-defect axes in `.claude/CLAUDE.md`, and it is invisible to the validator, the ToolKit catalog, and the signed-artifact decrypt. It is written **during the rename**, not after it.

### Decision 6 — the routed Exile lands the user directly

> `Redirect` ejects *into* the deterministically selected exit without offering a "Take suggested exit / Choose another" menu first… The exit is still recorded through `record_exit_and_route()`… Selection remains deterministic — `select_exit()` unchanged, rotate-then-exploit with a counter-modulo epsilon step. No `is.workflow.actions.number.random`, no shuffle, nowhere in the exit path.

**Phase 11 scope note:** Decision 6 is Phase 17's to build. This phase only reserves the name.

---

## 2. The generator is an in-place transformer, not a from-scratch builder

`[VERIFIED: read tools/build_state_engine.py:15, :3086-3155 this session]`

```
SOURCE = Path("src/PROSOCHE-Dumb.xml")            # :15 — input AND output

def main():                                        # :3086
    data = plistlib.loads(SOURCE.read_bytes())     # exactly one parse
    actions = data["WFWorkflowActions"]
    pinned = plistlib.dumps(actions[:5], ...)      # actions 0-4 are FROZEN
    replace_branch_body(actions, "--- OPEN STATE ENGINE ---", ..., open_pipeline())
    replace_branch_body(actions, "--- CLOSE SESSION PIPELINE ---", ..., close_pipeline())
    install_cooldown_branches(actions)
    insert_or_replace_after(actions, "--- CONTROL ROOM: confirm", MANUAL_MARKER, ...)
    insert_or_replace_after(actions, "Check whether this run had to rebuild ...", ...)
    restructure_router(actions)
    normalize_setters / normalize_open_apps / seed_settings_snapshot / seed_pending_exit
    fix_state_rebind / fix_date_format_key / fix_shownote_key / fix_notes_filter_limit
    gate_control_room_shownote
    <comment-before-control-flow insertion pass>
    normalise_string_envelopes / normalise_output_names / normalise_numeric_operands
    verify_parameter_keys / verify_string_envelopes / verify_output_names
    verify_required_pickers / verify_conditional_inputs / verify_conditional_action_string
    verify_numeric_operands / verify_state_seed / verify_pending_exit_seed
    verify_restore_gates / verify_sentinel_gates / verify_compound_value_reads
    verify_router_shape / verify_circle_zero_silence
    if plistlib.dumps(actions[:5], ...) != pinned: raise SystemExit("pinned actions 0-4 changed")
    SOURCE.write_bytes(...)                        # exactly one serialization/write
```

**What follows for the planner:**

1. **The generator is idempotent and reproduces hand edits byte-for-byte.** Measured: after running all eleven checks (two of which invoke both builders twice), `git status --short` was **empty**. Confirmed independently in the `260817-au7` SUMMARY: "after `tools/build_state_engine.py` ran, `src/PROSOCHE-Dumb.xml` was **unmodified in `git status`**".
2. **Actions 0–4 are pinned and immutable.** The Config literal is action **7**, so it is *not* pinned and *is* editable.
3. **Sentient is a fork of the built Dumb source.** `tools/build_sentient.py:27-28` — `SOURCE = src/PROSOCHE-Dumb.xml`, `TARGET = src/PROSOCHE-Sentient.xml`. Every Dumb-side plist edit propagates automatically; Sentient is never hand-edited. `:229` asserts `SOURCE.read_bytes() != original → "frozen Dumb source changed"`.
4. **`verify_*` is where a new hard build guard belongs** — that is where the seven parameter-defect axes are enforced, and BD-06 names its guard "an eighth class alongside" them.

**Anti-pattern to avoid:** searching `tools/*.py` for a user-facing string, finding nothing, and concluding the string does not exist. Measured example: `grep -n "PROSOCHĒ — Control Room" tools/*.py` returns exactly **one** hit — a *comment* at `:2915` — while the artifact carries three real occurrences.

---

## 3. Where each old primitive name lives — measured inventory

Counts from `git grep -cwn <NAME> -- 'tools/*.py' 'docs/*.py' 'src/CONFIG-BLOCK.md'`, run this session. Generated `src/*.xml` and `artifacts/` excluded (artifacts are historical records and are left alone, per `260817-au7`).

### 3.1 Source-file counts (word-boundary matched)

| Old name | `tools/build_state_engine.py` | `tools/build_sentient.py` | `docs/*.py` | `src/CONFIG-BLOCK.md` |
|---|---:|---:|---:|---:|
| Knock | 2 | 0 | `phase5_self_check` 1 | 5 |
| Ash | 3 | 0 | `phase5_self_check` 2, `sequence_dispatch_check` 1 | 7 |
| Silence | 7 | 0 | `environmental_restore_check` 3, `phase5_self_check` 2, `phase9_self_check` 2, `sequence_dispatch_check` 1 | 4 |
| Confession | 5 | 4 | `phase5_self_check` 2, `sequence_dispatch_check` 1 | 4 |
| Dimming | 3 | 0 | `environmental_restore_check` 2, `phase5_self_check` 1, `sequence_dispatch_check` 1 | 5 |
| Exile | 2 | 0 | `phase5_self_check` 1 | 3 |
| Mirror | 8 | 0 | `phase5_self_check` 2, `sequence_dispatch_check` 1 | 4 |
| Voice | 18 | 0 | `phase5_self_check` 1, `phase7_self_check` 1, `sequence_dispatch_check` 2 | 3 |
| Ice | 14 | 3 | `phase5_self_check` 3, `router_ui_census` 1 | 10 |

### 3.2 The only sites that are *dispatch-name* sites

**`tools/build_state_engine.py:658-660` — the single tuple that names all eight branches:**

```python
for name, implementation in (("Knock", knock), ("Ash", ash), ("Silence", silence),
                             ("Confession", confession), ("Dimming", dimming), ("Exile", exile),
                             ("Mirror", mirror_and_voice), ("Voice", mirror_and_voice), ("Ice", ice_start)):
    # Mirror is rendered once for a combined Silence+Mirror entry; Voice is a separate sequence name.
    if name == "Voice":
        continue
    group, check = if_block("Selected Primitive", 99, string=name)
```

This is the whole dispatch surface. Change the tuple + drop the `continue` + change `99` → `4`, and all 10 renderings follow.

**Everything else that mentions a primitive name in `build_state_engine.py` is a Python function name, a comment, an alert title, or a variable name — none of it is compared at runtime.** Enumerated:

| Line | Kind | Rename obligation |
|---|---|---|
| `:477` `def knock()` | function name | Optional (cosmetic). Renaming forces `:658` to match. |
| `:478` comment `"Knock is a brief…"` | comment | Recommended for readability |
| `:486` `def ash()`, `:487` comment | function/comment | Optional |
| `:490` `alert("Ash", "Pause. Put the phone down for one breath.")` | **user-visible alert title** | **Yes** — becomes `"Black and White"` |
| `:493` `def confession()`, `:496` comment | function/comment | Optional |
| `:501,:520,:528` `"Confession Intention"` | **internal variable name** | Cosmetic only. Note `docs/sentient_audit_check.py:14` asserts `"Intention" in raw` — already satisfied by `build_sentient.py:135`'s prompt label. Renaming the variable to `"Intention"` alone would break `build_sentient.py:135/155`, which reference `"Confession Intention"` by name. **Safest: leave the variable name alone.** |
| `:535` `def dimming()`, `:536` comment | function/comment | Optional |
| `:552` `alert("Dimming", "Brightness could not be captured…")` | **user-visible alert title** | **Yes** — becomes `"Dim"` |
| `:557` `def silence()`, `:558` comment | function/comment | Unchanged name |
| `:570-575` `"Silence Target"` variable, `alert("Silence", …)` | variable / alert | Unchanged name |
| `:580` `def exile()`, `:581` comment | function/comment | Optional → `eject` |
| `:604` `def mirror_and_voice()`, `:608` comment | function/comment | Optional |
| `:613-618` `"Mirror Text"` variable, `alert("Mirror", …)` | variable / alert | Mirror keeps its name |
| `:619-628` `voice_enabled`, `"Voice Enabled"`, `"Spoken This Run"` | **state key + variables** | **DO NOT RENAME.** `voice_enabled` is a `state.json` key read at `:619`, `:1607`, `:1633`; the manual menu item is `"Toggle Voice"` (`:1567`, `:1606`), asserted by `docs/phase7_self_check.py:15`. This is the *voice output* feature, not the *Voice primitive*. |
| `:632` `def ice_start()`, `:633` comment, `:637-640` `"Ice Profile"/"Ice Seconds"/"Ice Until"` | function/comment/variables | Optional → `frozen` |
| `:1511,:1540-1560` `LIVE_ICE_MARKER`, `"Ice is active"` menu prompt, `"Heat Before Ice Relief"` etc. | **structural markers + menu prompt** | `LIVE_ICE_MARKER` is a comment-text anchor used by `install_cooldown_branches`; **renaming it is a structural change** and `docs/phase5_self_check.py:69` asserts `"PHASE 5 LIVE ICE REDIRECT" in comments`. Recommend leaving markers alone; the user-visible `menu(prompt="Ice is active")` at `:1541` may become `"Frozen is active"`. |
| `:84` `"Voice Memos": "com.apple.VoiceMemos"`, `:790`, `:801` | **app identifier / exit menu item** | **DO NOT TOUCH.** Unrelated — the Capture exit's Voice Memos app. |

### 3.3 The `sequences` arrays — the only two places they exist

| Location | Content | How to edit |
|---|---|---|
| `src/PROSOCHE-Dumb.xml` **action 7**, `is.workflow.actions.gettext` → `WFTextActionText` (a **plain `str`**, not a token envelope — the whole Config literal) | the live arrays | `plistlib` round-trip; JSON must stay parseable (`detect.dictionary` consumes it) |
| `src/CONFIG-BLOCK.md:45-49` (+ prose at `:82`, `:84`, `:86`, `:107-109`) | documentation mirror | text edit |
| `src/PROSOCHE-Sentient.xml` | inherited from the built Dumb source | **never edit by hand** |

Measured current arrays (`plistlib` dump of action 7 this session):

```json
"sequences": {
  "Classic":     ["Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice"],
  "BlackMirror": ["Knock", "Confession", "Ash+Confession", "Mirror", "Silence+Mirror", "Dimming+Mirror", "Exile", "Voice", "Ice"],
  "Ambient":     ["Ash", "Silence", "Dimming", "Knock", "Confession", "Exile", "Mirror", "Voice", "Ice"]
}
```

Target arrays under BD-06 Decision 4 **with the Phase-11 intermediate state applied** (Circle 6 holds `Eject` in all three until Phase 17):

```json
"sequences": {
  "Classic":     ["Pause", "Black and White", "Silence", "Intention", "Dim", "Eject", "Mirror", "Loud Mirror", "Frozen"],
  "BlackMirror": ["Pause", "Intention", "Black and White", "Mirror", "Silence", "Eject", "Dim", "Loud Mirror", "Frozen"],
  "Ambient":     ["Black and White", "Silence", "Dim", "Pause", "Intention", "Eject", "Mirror", "Loud Mirror", "Frozen"]
}
```

Distinct names across all three = **nine**: Pause, Black and White, Silence, Intention, Dim, Eject, Mirror, Loud Mirror, Frozen. `Redirect` deliberately absent — the coverage guard requires every branch be named by ≥1 sequence, so emitting a `Redirect` branch this phase would fail the guard it also introduces.

### 3.4 Pre-existing drift worth recording

`src/CONFIG-BLOCK.md:36-38` still shows the **old** thresholds (`Paradise: [1,4,7,…25]`) while `src/PROSOCHE-Dumb.xml` action 7 carries the Phase-10 raised curve (`[4,7,…28]`). `docs/state_engine_self_check.py:10-17` carries the *current* values with the comment "This table is a duplicate of the Config literal at `src/PROSOCHE-Dumb.xml` action 7 and must be changed in the same commit as it." The doc mirror was missed. `[VERIFIED: three-way diff run this session]` Not this phase's bug, but the planner is already editing `CONFIG-BLOCK.md`'s `sequences` block and can fix it in the same pass.

---

## 4. The condition-99 → condition-4 move: every site, measured

`[VERIFIED: plistlib walk of src/PROSOCHE-Dumb.xml this session]`

```
total dispatch branches: 80
  code=99  tested='Ash'          x10
  code=99  tested='Confession'   x10
  code=99  tested='Dimming'      x10
  code=99  tested='Exile'        x10
  code=99  tested='Ice'          x10
  code=99  tested='Knock'        x10
  code=99  tested='Mirror'       x10
  code=99  tested='Silence'      x10
distinct WFInput serialization types: {None}      # the Type/Variable descriptor form
any Aggrandizements:                {False}
WFConditionalActionString types:    {'str'}       # plain literals, no token() envelope
```

**Operand shape is already correct for condition 4 and needs no change.** `Selected Primitive` is set from a `gettext` output (`tools/build_state_engine.py:655-657`) so it is text-typed; condition 4 ("string is") is a string comparator; `NUMERIC_CONDITION_CODES = {0,1,2,3,1003}` at `:2509` does not include 4 or 99, so `normalise_numeric_operands()` is not involved. Axis 6 (coercion aggrandizement) does not apply. `verify_conditional_action_string()` (`:1925`) only rejects a **bare `￼`** comparison target — a real literal passes. `if_block(..., 4, string=<literal>)` is the established idiom, already used at `:614` (`"Previous Respected", 4, string="true"`) and in the router's OPEN/CLOSE tests.

**Where an exact-match move breaks things — three sites, all in the Config literal:**

| Combined entry | Sequence / Circle | Under 99 | Under 4 | Fix |
|---|---|---|---|---|
| `Ash+Confession` | BlackMirror C3 | fires Ash **and** Confession branches | fires **nothing** | BD-06: → `Black and White` |
| `Silence+Mirror` | BlackMirror C5 | fires Silence **and** Mirror | fires **nothing** | BD-06: → `Silence` |
| `Dimming+Mirror` | BlackMirror C6 | fires Dimming **and** Mirror | fires **nothing** | BD-06: → `Dim` at C7; `Eject` at C6 |

**The finding that makes the move mandatory, not optional.** Under condition 99 the test is *"does `Selected Primitive` contain `<branch name>`"*. The entry `"Loud Mirror"` **contains** `"Mirror"`. So with the new roster and the old code, Circle 8 would fire the **Mirror** branch as well as its own — a silent double-dispatch. `"Loud Mirror"` is undispatchable-as-distinct until dispatch is exact. Conversely no *new* name is a substring of another under exact matching (`Dim` vs `Dimming` disappears with the rename; `Pause`, `Black and White`, `Silence`, `Intention`, `Eject`, `Mirror`, `Loud Mirror`, `Frozen` are pairwise non-equal). `[VERIFIED: substring cross-product checked by hand against the nine target names]`

**Also note:** `docs/phase5_self_check.py:66-68` currently asserts the presence of `"Ash+Confession"` and `"Silence+Mirror"` as literal strings in the artifact text. That assertion **must** be updated in the same commit or the build goes red the moment the arrays change.

---

## 5. The dispatch-coverage guard — current state, verified

### 5.1 STATE.md's claim, verified against the file

`.planning/STATE.md:173` claims:

> docs/sequence_dispatch_check.py never filters on a condition code; semantics are resolved per branch from the branch's own code, so BD-06's contains-to-exact move needs no edit

**Verdict: TRUE for the resolution logic, FALSE as a statement that the file needs no edit at all.** `[VERIFIED: read docs/sequence_dispatch_check.py in full, ran it]`

What is true:
- `collect_dispatch_branches()` (`:122-143`) performs **no** condition-code filtering — it collects every mode-0 conditional whose `WFInput` variable is `Selected Primitive`, whatever code it carries, and stores the code per record.
- `match_strategy(code)` (`:56-72`) maps `99 → "contains"`, `4 → "exact"`, anything else → `"unknown"` (reported, never guessed).
- `sequence_components()` (`:106-119`) splits on `+` unconditionally; a name with no `+` yields itself, so it reads today's combined entries and tomorrow's single names with no branch.

What is **not** true — the file needs three edits to become the guard BD-06 mandates:

| Edit | Why |
|---|---|
| It is a **reporter, not a gate** — its docstring says so in capitals and `main()` (`:150-201`) exits 0 in every case, including on an unexpected orphan | BD-06 requires a hard gate |
| `KNOWN_ORPHANS = {"Voice": ".planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md"}` (`:51-53`) | The Voice orphan is closed by this phase; the dict must be emptied |
| Its own docstring: *"A future phase may promote this script to a build guard once the primitive roster and the matching strategy have settled under BD-06."* (`:11-12`) | This **is** that phase — the docstring must be rewritten |

### 5.2 Measured current output

```
$ python3 docs/sequence_dispatch_check.py
dispatch surface: 80 branch(es) testing 'Selected Primitive', 8 distinct name(s); 9 distinct sequence component(s)

ORPHANS -- sequence entries that dispatch nothing:
  Voice: Classic (Circle 8), BlackMirror (Circle 8), Ambient (Circle 8) -- KNOWN OPEN DEFECT, owned by …

UNREACHABLE -- dispatch branches no sequence entry names:
  (none)

UNKNOWN MATCH SEMANTICS: (none)

sequence dispatch check: 1 orphan(s) (0 unexpected), 0 unreachable, 0 of unknown semantics -- reported, not gated
```

**Circle 8 is measurably dead in all three sequences.** That is the exact defect CIRC-08 names.

### 5.3 Concrete guard to model the new one on

BD-06 says the invariant is "an eighth class alongside the seven parameter-defect axes in `.claude/CLAUDE.md`". The seven axes are enforced by `verify_*(actions)` functions called from `main()` in `tools/build_state_engine.py`. **The new guard's correct home is therefore a `verify_dispatch_coverage(actions)` in the generator**, appended to that chain — with `docs/sequence_dispatch_check.py` promoted alongside it as the independent, read-only eleventh check.

The eleven existing `docs/*.py` checks, all measured **exit 0** at `ae0226c`:

| Script | Lines | Result | What it is good as a model for |
|---|---:|---|---|
| `state_engine_self_check.py` | 117 | 0 | Arithmetic reference table duplicated from the Config literal, with a "must change in the same commit" comment |
| `phase5_self_check.py` | 151 | 0 | Runs the builder twice for **idempotence**, then string/marker/ancestry assertions. Hardcodes the primitive-name list at `:66-68` |
| `phase6_self_check.py` | 120 | 0 | Same idempotence idiom; per-action route-shape assertions |
| `phase7_self_check.py` | 68 | 0 | Menu-item list assertion (`MENU`, `:15`) |
| `phase9_self_check.py` | 142 | 0 | Hard site counts + coercion counts per fork |
| `sentient_audit_check.py` | 24 | 0 | Marker-bounded block extraction + phrase assertions |
| `sentient_core_check.py` | 21 | 0 | `SENTIENT["WFWorkflowName"].endswith("Sentient")` — **breaks on the Aware rename** |
| `environmental_restore_check.py` | 278 | 0 | Imports the generator **as a module** to assert on real symbols; derives its expected counts in a comment |
| `router_ui_census.py` | 267 | 0 | Per-arm surface census; **explicitly refuses** to assert absolute counts |
| **`sequence_dispatch_check.py`** | 205 | 0 | **The direct ancestor of the new guard — reuse its parsing wholesale** |
| `manifest_check.py` | 153 | 0 | **Best structural model**: module docstring explaining *why*, `require()` helper, table-driven, raises `AssertionError` with an actionable message. Hardcodes `DISPLAY_NAMES` — **breaks on the Core/Aware rename** |

**Recommended guard shape** (composed from the two ancestors — do not invent a third idiom):

```python
def verify_dispatch_coverage(actions):
    """Fail the build if any sequence entry dispatches nothing, or any branch is unnamed.

    BD-06 Decision 5's eighth defect class.  Invisible to validate_shortcut.py, to the
    ToolKit catalog, and to the signed-artifact decrypt: an unmatched entry is a silent
    runtime no-op, which is how Circle 8 shipped dead for four phases.
    """
    # 1. locate the Config literal by content, never by index
    #    (docs/sequence_dispatch_check.py:95-103 -- gettext whose text contains '"config_version"')
    # 2. components = every distinct name in any sequences array, split on '+'
    # 3. branches  = every mode-0 conditional whose WFInput variable is "Selected Primitive",
    #    carrying its own WFCondition; resolve semantics per branch (match_strategy)
    # 4. orphan     = a component no branch resolves for       -> SystemExit
    #    unreachable = a branch no component resolves for      -> SystemExit
    #    unknown     = a branch whose code neither rule knows  -> SystemExit
    #    duplicate   = a component matched by >1 distinct branch name -> SystemExit
    #                  (BD-06: "exactly one dispatch branch")
```

Call it from `main()` after `verify_circle_zero_silence(actions)`, and — mirroring how `tools/build_sentient.py:12-25` imports the other `verify_*` functions — from `build_sentient.py`'s verify chain too.

**Note the "exactly one" clause.** BD-06 says *exactly one* dispatch branch per name; the current reporter only tests *at least one*. Under exact matching, `Mirror` and `Loud Mirror` are distinct so no name is double-matched — but the guard should assert the stronger property BD-06 actually states, because that is what would have caught a `Mirror`/`Loud Mirror` collision had the 99→4 move been forgotten.

### 5.4 Action-count impact of adding the ninth branch

Measured by calling the generator's own functions `[VERIFIED: python3 import of build_state_engine this session]`:

| Function | Actions emitted |
|---|---:|
| `knock()` | 2 |
| `ash()` | 2 |
| `confession()` | 50 |
| `dimming()` | 25 |
| `silence()` | 24 |
| `exile()` | 2 |
| `mirror_and_voice()` | 32 |
| `ice_start()` | 11 |
| **`primitive_dispatch()` total** | **199** |

Per-branch wrapper overhead = 5 (`comment` + `if` + `otherwise` + `nothing` + `end_if`). Adding `Loud Mirror → mirror_and_voice()` costs **5 + 32 = 37 actions per rendering × 10 renderings = ~370 actions**, taking the artifact from **3,718** to roughly **4,090** (the comment-insertion pass at `:3128-3138` adds a little more). File grows from ~2.26 MB toward ~2.5 MB; signed from ~194 KB toward ~210 KB. No documented limit is approached. `[VERIFIED for counts; the size projection is arithmetic, not measured]`

---

## 6. The Apple Note rename — three occurrences, located exactly

`[VERIFIED: plistlib walk of src/PROSOCHE-Dumb.xml this session; grep -c confirms 3 in each fork]`

| Action | Identifier | Parameter | Current value | Role | Target |
|---:|---|---|---|---|---|
| **3602** | `is.workflow.actions.filter.notes` | `WFContentItemFilter → …Templates[0]` — `{Operator: 99, Property: "Name", Values.String: WFTextTokenString}` | `PROSOCHĒ — Control Room` | **lookup predicate** — how PROSOCHĒ finds the note | `PROSOCHĒ` |
| **3616** | `is.workflow.actions.gettext` | `WFTextActionText` (a `WFTextTokenString`, 6,210 chars, 2 attachments) | body opens `# PROSOCHĒ — Control Room` | **note body copy** (H1 heading) | `# PROSOCHĒ` |
| **3619** | `com.apple.mobilenotes.SharingExtension` | `name` (plain `str`) | `PROSOCHĒ — Control Room` | **the actual display title** | `PROSOCHĒ` |

Sentient's mirrors sit at the same relative positions (body at **3684**); it inherits all three from the built Dumb source.

### 6.1 Display name vs internal name — settled by `e84ee77`

`[VERIFIED: git show e84ee77]` — commit message:

> docs: clarify the Note rename keeps 'Control Room' as its internal name
> The addendum renames the Apple Note from 'PROSOCHE -- Control Room' to 'PROSOCHE' for the **user-facing title only**; the codebase and docs continue to call it the Control Room.

So: **rename all three of the above** (they are all user-facing — the title, the heading a user reads, and the predicate that has to match the title), and **keep "Control Room" everywhere internal**:

| Internal "Control Room" site | Do not rename |
|---|---|
| `tools/build_state_engine.py:1567` menu item `"Open Control Room"` — asserted by `docs/phase7_self_check.py:15` | ✓ keep |
| `"Control Room Note"` variable (`:1646`, `:1687`, `:2873`, `:2905`) | ✓ keep |
| `MANUAL_MARKER`, `"--- PHASE 7 MANUAL CONTROL ROOM REFRESH ---"`, `"--- CONTROL ROOM: confirm"` anchors | ✓ keep — structural |
| `gate_control_room_shownote()`, `fix_shownote_key()`, `fix_notes_filter_limit()` names/docstrings | ✓ keep |
| `docs/router_ui_census.py` prose | ✓ keep |

### 6.2 **The predicate hazard — the highest-value finding in this section**

Action 3602's filter is `Operator: 99` = **"Name contains"**, with `WFContentItemLimitEnabled: True` and `WFContentItemLimitNumber: 1.0` (added by `fix_notes_filter_limit()`), consumed by a Get Item From List "First Item".

Today `contains "PROSOCHĒ — Control Room"` is specific enough. After the rename, `contains "PROSOCHĒ"` matches **any note whose name contains `PROSOCHĒ`** — including a leftover `PROSOCHĒ — Control Room` from an earlier install, and including a hypothetical `PROSOCHĒ (old)`. With a limit of 1 + First Item, PROSOCHĒ would silently bind to the wrong note and append its ledger there forever.

**Recommendation:** change the predicate `Operator` from `99` to `4` ("is") in the same edit. The filter templates in `BEST_PRACTICES.md` use the same operator vocabulary as conditionals, so `4` is "string is". `[CITED: .claude/CLAUDE.md §4 condition-code table — 4 = "string is", 99 = "contains"]` `[UNVERIFIED: whether `Operator: 4` is accepted in a `WFContentPredicateTableTemplate` for the Notes `Name` property specifically — the code table is documented for `WFCondition` on conditionals, and the project's filter evidence is Donor-8-matched for the limit key, not for the operator. Evidence that would settle it: a donor export of a Find Notes action configured with "Name — is" from the owner's iPhone, decrypted via the §8 AEA1 recipe. If a donor is not available, the conservative fallback is to leave `Operator: 99` and accept the collision risk, recording it as a deviation.]`

**Second-order collision:** both forks create a note with the same title. Today both use `PROSOCHĒ — Control Room`, so this is **pre-existing**, not introduced here — but the rename makes the title shorter and more collision-prone. Worth a line in `docs/BUILD-NOTES.md` either way.

### 6.3 **The `attachmentsByRange` hazard — recompute, never substitute**

Action 3616's `WFTextActionText` is a `WFTextTokenString`:

```
LEN 6210
attachmentsByRange = {'{5478, 1}': {'Type': 'Variable', 'VariableName': 'Import Descent'},
                      '{5509, 1}': {'Type': 'Variable', 'VariableName': 'Import Voice'}}
```

Both attachments sit near the **end** of the body. The rename edits are the H1 at offset 0 and the two Run-Shortcut target strings mid-document — **all upstream of both attachments**. Every one of them shifts the offsets.

`.claude/CLAUDE.md` §5 states the rule and its consequence: *"`attachmentsByRange` positions must exactly match `￼` character offsets in the final string… out-of-bounds ranges can crash Shortcuts on import."*

`260817-au7` established the exact working method and it should be copied verbatim:

1. Prove a **no-op** `plistlib.dumps(data, fmt=FMT_XML, sort_keys=False)` comes back byte-identical to the source **before** any edit — this licenses a structured edit and keeps the diff free of reformatting noise. (Measured then: 2,259,398 == 2,259,398.)
2. Assert the **old** offsets equal the old `￼` positions.
3. Apply the text replacement.
4. **Rebuild `attachmentsByRange` from the new `￼` offsets in document order.**
5. Assert the replacement text introduces **no new placeholder**.
6. `plutil -lint` the file.
7. Verify final offsets equal recomputed offsets in **both** forks after the Sentient rebuild.

### 6.4 The Note body's full current structure (for copy planning)

Headings in document order: `# PROSOCHĒ — Control Room` → `## READ THIS FIRST` → `### Automation A — OPEN` (12 steps) → `### Automation B — CLOSE` (12 steps) → `## Do not target these apps` → `## MY PHONE, ON PURPOSE` (5 `###` prompts — **this is the user-editable proforma**) → `## CURRENT SETTINGS` (`- Fork: Dumb`, `- Profile: ￼`, `- Sequence: Classic`, `- Voice: ￼`, `- AI: not used by this fork`, `- Enabled exits: …`) → `## CURRENT STATE` → `## ATTENTION LEDGER` → `## VALUE / LIFE RETURNED` → `## SUPPORT PROSOCHĒ`.

The addendum's optional hardening note goes **at the end** (after `## SUPPORT PROSOCHĒ`, or as a new final `##` section). Because it is downstream of both attachments, adding it alone would not move them — but the H1 and Automation edits will, so recompute regardless.

**Critical for the Panic Escape setting placement:** `manual_note_refresh()` (`tools/build_state_engine.py:1645-1646`) **appends** a fresh `## CURRENT SETTINGS / ## CURRENT STATE / ## ATTENTION LEDGER` block on every state-changing manual run (`appendnote`, `operation="append"`). The Note therefore **grows**, and any user-editable setting placed inside `## CURRENT SETTINGS` gets buried under machine-appended duplicates. See §8.

---

## 7. Dumb→Core and Sentient→Aware — every site, and the downstream consequences

### 7.1 The three classes, kept separate

**(A) SIGNED ARTIFACT DISPLAY FILENAMES — load-bearing, cannot be got wrong**

`artifacts/shortcuts/MANIFEST.md`, and `docs/manifest_check.py`'s own docstring, state the mechanism:

> a signed artifact carries **no** display name inside it. Measured this phase by decrypting both containers — the AEA1 auth-data plist holds only `SigningCertificateChain`, and the recovered `Shortcut.wflow` has had its `WFWorkflowName` key **stripped** by the signer… The display name therefore lives in the filename and nowhere else, so a `_signed`-suffixed file imports as a second, differently named library entry that the user's two Personal Automations do not reference — a silently dead install.

Current filenames (both exist on disk):
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` (193,819 B)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` (198,124 B)

**Enumerated downstream consequences of renaming these:**

| # | Consequence | Site | Severity |
|---|---|---|---|
| D1 | `docs/manifest_check.py:DISPLAY_NAMES` is a hardcoded two-element list; `SIGNED_BASENAMES` derives from it; the coverage loop derives the fork label via `name.rsplit("—",1)[-1].strip()` → `"Dumb"`/`"Sentient"` and requires a row label starting with it | `docs/manifest_check.py:44-48, :140-148` | **Build-red until updated** |
| D2 | `artifacts/shortcuts/MANIFEST.md`'s six row labels (`Dumb source`/`Dumb archive`/`Dumb signed`/`Sentient …`) and three of its paths | `artifacts/shortcuts/MANIFEST.md` | **manifest_check red** |
| D3 | The Control Room Note tells the user to pick the Run Shortcut target *named exactly* `PROSOCHĒ — Nine Circles — Dumb` — **twice** (Automation A step 10, Automation B step 10). `docs/BUILD-NOTES.md` §9 binds this: *"Any future rename of the shipped shortcut requires updating both of this Note's automation sections to match; the Note is written first here and the signer must agree with it, not the reverse."* | Note body action 3616 (both forks) | **Silently dead install** if missed |
| D4 | **Sentient's Note already names the wrong fork.** Measured: Sentient's body (action 3684) contains `PROSOCHĒ — Nine Circles — Dumb` ×2 and `Sentient` ×0, and reads `- Fork: Dumb`. Recorded as a Deferred Item in the `260817-au7` SUMMARY, explicitly assigned to *"`.planning/todos/pending/2026-08-14-apply-build-addendum-01.md`"* — **i.e. this phase**. Fixing it requires a Sentient-side note-body divergence, which the current architecture (Sentient = verbatim fork of Dumb) does **not** provide. | `build_sentient.py` has no note-body edit | **New design work** — see §7.2 |
| D5 | `sign-shortcut --name "…"` invocations in every plan/verify block | pipeline | mechanical |
| D6 | `README.md:5-6, :8` name both signed artifacts and both `src/` paths | `README.md` | doc |
| D7 | Every dated archive under `artifacts/shortcuts/2026-08-1*/` keeps the old name. Per `260817-au7`'s precedent these are **historical records and are left alone** | `artifacts/` | none — do not touch |
| D8 | A user who already imported the old-named shortcut keeps a stale library entry; their two Personal Automations still point at it | user's device | **Must be stated in the Note / release text** — the rename is a breaking change for existing installs |

**(B) INTERNAL IDENTIFIERS — safe to leave or rename, but they are asserted**

| Site | Value | Note |
|---|---|---|
| `src/PROSOCHE-Dumb.xml` root `WFWorkflowName` | `PROSOCHĒ — Nine Circles — Dumb` | Lives in the XML; only stripped at sign time, but it is what a user sees if they import the *unsigned* source |
| `tools/build_sentient.py:181` | `root["WFWorkflowName"] = "PROSOCHĒ — Nine Circles — Sentient"` | Generator-owned |
| `docs/sentient_core_check.py:9` | `assert SENTIENT["WFWorkflowName"].endswith("Sentient")` | **Breaks on rename** |
| Bootstrap `state.json` seed, action 75 | `"fork": "Dumb"` | User-visible via `## CURRENT SETTINGS → - Fork:` and the Status alert (`Snapshot Fork`, `:1633`, `:1645`, `:1654`) |
| File paths `src/PROSOCHE-Dumb.xml` / `-Sentient.xml` | 8 non-`.planning` code files: `tools/build_state_engine.py`, `tools/build_sentient.py`, and all six of `docs/{environmental_restore_check,phase5_self_check,phase6_self_check,phase7_self_check,router_ui_census,sentient_audit_check,sentient_core_check,sequence_dispatch_check,state_engine_self_check}.py` | **Recommendation: do NOT rename the `src/*.xml` filenames.** It is pure churn across 10 code files plus ~70 `.planning` documents, breaks every historical plan's reproducibility, and the addendum asks to rename the *products*, not the source files. Record the decision. |
| Python identifiers/comments containing `Dumb`/`Sentient` | `build_sentient.py` ×22, `build_state_engine.py` ×4, `docs/*.py` ×~20 | cosmetic |

**(C) DOC PROSE**

`docs/BUILD-NOTES.md` (35 matches), `docs/CAPABILITY-DECISIONS.md` (13), `PROSOCHE_Nine_Circles_Canonical_Strategy.md` (65), `README.md` (4), `src/CONFIG-BLOCK.md` (1). Historical records (BUILD-NOTES deviation entries, CAPABILITY-DECISIONS BD records) should be **appended to, not rewritten** — that is this project's established convention (`docs/BUILD-NOTES.md` §20 is "a pure append; the diff contains zero deletions"). Forward-facing docs (`README.md`, the canonical strategy's product sections) do get updated.

### 7.2 The Sentient note-body divergence (D4) — a genuine architectural gap

`tools/build_sentient.py` currently makes exactly **three** kinds of change to the forked Dumb source: it inserts an audit block at a comment anchor (`:184-189`), it sets `WFWorkflowName` (`:181`), and it sets `WFWorkflowIcon` + an import question (`:179-182`). It does **not** touch the note body, the note title, or the `"fork"` seed.

To satisfy D4 (Aware's Note naming Aware, and `- Fork: Aware`) the planner must add a Sentient-side patch. Options:

1. **A `fix_fork_strings(actions)` in `build_sentient.py`** that rewrites the note-body `WFTextTokenString` and the `state.json` seed text, recomputing `attachmentsByRange`. Most direct; reuses `260817-au7`'s method; must run before the `verify_*` chain.
2. **Parameterise the note body in the generator** — move the whole 6,210-char body into `build_state_engine.py` as a template. Large, invasive, and contradicts the deliberate "the body is XML-authored" architecture.
3. **Leave D4 open**, recording it as a carried-forward deviation. Defensible only if the phase runs out of budget; it means Aware ships instructing users to select a shortcut that does not exist.

**Recommendation: option 1.** It is the smallest change that closes a defect explicitly assigned to this phase, and it is a strict superset of the existing `_replace_in_token`-style helpers already in `build_state_engine.py` (`fix_state_rebind` uses `_replace_in_token` at `:3055`).

---

## 8. Panic Escape = the `Leaving` option — current implementation and a removal mechanism

### 8.1 What `Leaving` is today

`tools/build_state_engine.py:895-914`:

```python
def universal_leaving():
    group = uid()
    a = [comment(EXIT_MARKER + "…"),
         menu(group, 0, prompt=text_token([("You just opened a tracked app. PROSOCHĒ is at Circle ", "Circle Next"),
                                           (".\n\nLeaving: PROSOCHĒ suggests somewhere better to go and takes you there.\n"
                                            "Continue: you go into the app, after this Circle's intervention.", None)]),
              items=["Leaving", "Continue"]), menu(group, 1, title="Leaving")]
    a += select_exit() + [menu(group, 1, title="Continue")] + primitive_dispatch() + [menu(group, 2), …]
    return a
```

One `choosefrommenu` (artifact action **520**), mode-0 with `WFMenuItems == ["Leaving", "Continue"]`, two mode-1 cases, one mode-2 end. The `Leaving` case body is `select_exit()`; the `Continue` case body is `primitive_dispatch()`. **`Leaving` is not a separate action — it is a menu case, so "removing" it means not offering the menu.**

Confirmed distinct from **Emergency Restore**, which is a MANUAL-arm menu item (`:1567`) plus the `["Return Home", "Emergency Restore"]` menu inside the live-Ice redirect (artifact action 171) — neither is touched.

### 8.2 The three guards that constrain any change here

| Guard | Assertion | Constraint imposed |
|---|---|---|
| `verify_circle_zero_silence()` property (b), `tools/build_state_engine.py:1481-1490` | `len([menus with WFMenuItems == ["Leaving","Continue"]]) == 1` **and** that menu is enclosed by a `Circle Next > 0` conditional | **Exactly one** such menu must survive, still inside the silent band |
| `verify_circle_zero_silence()` property (c), `:1490-1498` | every `sequences.`-prefixed dotted read **inside the OPEN arm** is enclosed by the same silent-band group as the menu | Any new OPEN-arm `primitive_dispatch()` rendering inherits this requirement |
| `docs/router_ui_census.py:234-245` | **every** counted surface (`choosefrommenu` mode-0, `ask`, `alert`, `notification`, `choosefromlist`, `speaktext`, `shownote`, `filter.notes`, `SharingExtension`) in the OPEN arm is enclosed by a silent-band group | **No new OPEN-arm surface may sit outside the band.** A Panic-Escape confirmation dialog in the OPEN arm would go red |

Plus the two hard site counts that a **duplicated** `primitive_dispatch()` on the OPEN path would break:

- `docs/environmental_restore_check.py:78` — `EXPECTED_SITES = {setbrightness: 14, setvolume: 14, getdevicedetails: 20}`, derived in a comment from *"primitive_dispatch() is rendered TEN times — once on the OPEN path and nine times by the Test-a-Circle submenu"*.
- `docs/phase9_self_check.py:97-104` — `{setbrightness: 14, setvolume: 14}` per fork, plus coercion counts `{setbrightness: 14, setvolume: 4}` with the comment `# Restore Brightness x4 + Dim Target x10`.

An eleventh rendering makes these 15/15/22 and 15/5. Both are *legitimate reasons to move the number* per their own comments — but they must be moved deliberately and in the same commit, and the derivation comments rewritten.

### 8.3 Two viable mechanisms

**Mechanism A — gate the whole menu (recommended)**

```
If Panic Escape Enabled > 0            # numeric read from state.json
    <existing Leaving/Continue menu block, unchanged>
Otherwise
    primitive_dispatch()               # eleventh rendering
End If
```

- Preserves exactly one `["Leaving","Continue"]` menu → guard (b) green.
- The new conditional must sit **inside** the silent-band group so both arms stay enclosed → guards (c) and the census stay green.
- **Costs an eleventh `primitive_dispatch()` rendering** → +199 actions and the two site-count tables must move to 15/15/22 and 15/5.

**Mechanism B — hoist dispatch out of the menu**

```
If Panic Escape Enabled > 0
    menu(Leaving/Continue)
      case Leaving  -> select_exit() ... then is.workflow.actions.exit
      case Continue -> Nothing
    end menu
End If
primitive_dispatch()                   # single rendering, unconditional
```

- Keeps the rendering count at ten → both site-count tables unchanged.
- Requires the `Leaving` path to terminate the run. `is.workflow.actions.exit` **is** already used in the artifact (asserted present by `docs/sentient_audit_check.py:22`), so the primitive exists. `[VERIFIED: identifier present and asserted]`
- **Riskier**: it restructures the OPEN arm's control flow, which `verify_circle_zero_silence`, `verify_router_shape` and `router_ui_census` all reason about; and `select_exit()`/`record_exit_and_route()` currently end by routing (open app / return home) — whether a following `exit` is needed or harmful is `[UNVERIFIED — evidence that would settle it: an on-device run, or a decrypt-inspect of the current Leaving path's tail]`.

**Recommendation: Mechanism A**, accepting the eleventh rendering and updating both count tables with a fresh derivation comment. It is the change that touches the least control-flow structure, and this project's whole guard suite is built around structural stability.

### 8.4 The "manually edit the setting in the Note + explicit confirmation" path

Addendum §3 requires three things: (1) the user manually edits a Panic Escape setting **in the Note**; (2) explicit confirmation; (3) the bypass is then removed.

**Measured constraints on the read path:**

- The Config literal (action 7) is a **build-time constant** parsed by `detect.dictionary`. It is not user-editable. The flag must live in `state.json` (bootstrap seed, action 75).
- The **only** existing Note→state read is `Sync My Profile` (`:1687`): `gettext(Control Room Note)` → `text.match(pattern="(?s)## MY PHONE, ON PURPOSE.*?(?=## CURRENT SETTINGS)")` → `set_value("profile_snapshot.proforma", Matched Text)`. It captures the proforma as **opaque text** and parses nothing out of it.
- OPEN and CLOSE **never** parse the Note — `docs/BUILD-NOTES.md` §10 makes this binding, on both cost and the C10 permission-prompt safety ground. The read must therefore happen on the **MANUAL** arm only.
- `manual_note_refresh()` **appends** a new `## CURRENT SETTINGS` block on every state-changing manual run, so the Note accumulates duplicates of that heading. A setting placed there would be shadowed.

**Recommended shape (all at Claude's discretion, but these constraints are hard):**

1. Add a **stable, never-appended** section to the Note body — e.g. `## PANIC ESCAPE` placed immediately before `## MY PHONE, ON PURPOSE` — containing a single editable line such as `- Panic Escape: ON` and prose explaining that changing it to `OFF` and then choosing the confirmation menu item removes the easy bypass permanently.
2. Add a new MANUAL menu item (or extend `Sync My Profile`) that: `text.match`es that one line → shows an explicit `Choose from Menu` confirmation (`["Keep Panic Escape", "Remove Panic Escape"]`) → writes `panic_escape_enabled = 0` into `state.json` → appends the change to the ledger.
3. Seed `"panic_escape_enabled": 1` in the bootstrap template (action 75) — **required**, because `verify_state_seed()` asserts every snapshot/state read has a seeded counterpart, and `.claude/CLAUDE.md`'s verified runtime semantics make a *flat* read of a missing key return nothing (safe) but leave the numeric gate ambiguous. Gate on a numeric `> 0` test, never a `has any value` gate on a dotted path (the documented-unimplementable pattern).
4. Gate `universal_leaving()`'s menu on that flag per Mechanism A.

**If a new MANUAL menu item is added**, `docs/phase7_self_check.py:15`'s hardcoded `MENU` list and the `choosefrommenu` case-order rule (case titles must match `WFMenuItems` exactly and in order — `.claude/CLAUDE.md` §4, "the top real-world failure mode") both apply. `tools/build_state_engine.py:1620-1624` already carries a comment about emitting the tenth item last for exactly this reason.

---

## 9. Dante names — where they would land, and the `Limbo` collision

`[VERIFIED: grep -o over src/PROSOCHE-Dumb.xml this session]`

| Name | Occurrences in the artifact | What they are |
|---|---:|---|
| Limbo | **12** | **all are the `profile` name** — `thresholds.Limbo`, `cooldown_seconds.Limbo`, the `["Paradise","Limbo","Inferno"]` menu (action 1368) and its case |
| Paradise | 9 | profile |
| Inferno | 10 | profile |
| Lust, Gluttony, Greed, Wrath, Heresy, Violence, Fraud, Treachery | **0** | absent entirely |

**Two findings:**

1. **No Dante Circle name is surfaced anywhere today.** The artifact says `Circle {N}` — in the Knock alert (`:481`), the Mirror templates (`MIRROR_BASELINES` etc., `:33-70`), the Leaving prompt (`:906`), the Status alert (`:1654`), the Note's `## CURRENT STATE` gloss, and the Test-a-Circle menu (`["Circle 1" … "Circle 9"]`, action 1448). Applying Addendum §1 therefore means **adding** a name surface, not renaming an existing one — the planner must decide *where*. Candidates, in ascending risk: the Test-a-Circle menu titles (but menu case titles must match `WFMenuItems` element-for-element and in order), the Pause alert, the Leaving prompt, the Status alert, the Mirror templates (30 strings with `￼` placeholders whose `attachmentsByRange` are computed by `text_token()` — safe, since they are generated, not hand-authored).
2. **`Limbo` is a live namespace collision.** It is currently the middle *profile*; BD-06 Decision 2 makes it Circle 1's *name*. A user on the `Limbo` profile whose Pressure reaches Circle 1 would read "Limbo" meaning two different things one line apart in the Status alert (`Profile: Limbo` / `Circle 1 — Limbo`). BD-06 does not address this. It is **not** a code defect — the two are separate dictionary namespaces and no string comparison crosses them — but it is a real product-copy problem and the planner should decide deliberately: disambiguate the copy (`Profile: Limbo (pace)` / `Circle 1 · Limbo`), rename the profile, or accept it and record the acceptance. **Do not discover this on device.**

---

## 10. Rebuild / validate / sign pipeline — invariants

`[VERIFIED: transcribed from .planning/phases/10-.../10-RESEARCH.md §5b, re-confirmed against 260817-au7's SUMMARY and re-path-checked this session]`

```bash
# 0. Provenance guard — MANDATORY. Measured PASS (exit 0) at ae0226c this session.
git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD

# 1. Regenerate Dumb (MUTATES src/PROSOCHE-Dumb.xml IN PLACE — input AND output)
python3 tools/build_state_engine.py

# 2. Regenerate Sentient FROM THE FRESH DUMB (never carry a stale Sentient forward)
python3 tools/build_sentient.py

# 3. All eleven structural checks — every one measured exit 0 at ae0226c
python3 docs/state_engine_self_check.py
python3 docs/phase5_self_check.py          # also asserts builder idempotence
python3 docs/phase6_self_check.py          # also asserts builder idempotence
python3 docs/phase7_self_check.py
python3 docs/phase9_self_check.py
python3 docs/sentient_audit_check.py
python3 docs/sentient_core_check.py
python3 docs/environmental_restore_check.py
python3 docs/router_ui_census.py
python3 docs/sequence_dispatch_check.py    # -> becomes a hard gate this phase
python3 docs/manifest_check.py             # goes RED on every rebuild until MANIFEST refreshed

# 4. Validate — `all`, NEVER `ios` (DEV-01), NEVER --target-macos 27
validate-shortcut src/PROSOCHE-Dumb.xml     --target-macos 26 --target-platform all
validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all

# 5. Archive + sign in ONE step. NEVER a pre-dated --output-dir (doubled-path defect).
sign-shortcut src/PROSOCHE-Dumb.xml --name "<CANONICAL DISPLAY NAME>" \
  --mode anyone --output-dir artifacts/shortcuts

# 6. Decrypt-verify what actually shipped — the only non-device "what shipped" channel
signed="artifacts/shortcuts/<CANONICAL DISPLAY NAME>.shortcut"
dir="$(mktemp -d)"
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed" "$dir/leaf.der"
openssl x509 -inform DER -in "$dir/leaf.der" -noout -pubkey > "$dir/pub.pem"
aea decrypt -i "$signed" -o "$dir/payload.aa" -sign-pub "$dir/pub.pem"
mkdir -p "$dir/unwrapped" && aa extract -i "$dir/payload.aa" -d "$dir/unwrapped"
plutil -convert xml1 -o "$dir/Shortcut.xml" "$dir/unwrapped/Shortcut.wflow"

# 7. Refresh MANIFEST rows from disk
shasum -a 256 src/PROSOCHE-Dumb.xml "$signed"
stat -f%z    src/PROSOCHE-Dumb.xml "$signed"
```

**Definition of done** (from `.claude/CLAUDE.md` §1 and `260817-au7`'s evidence table): validator `Validation passed.` exit 0 ×2; signed files **non-zero bytes**, basenames exactly the canonical display names with **no suffix**; dated archive SHA-256 **equal** to its `src/` counterpart; both signed containers decrypt and carry the intended strings; `plutil -lint OK` on both recovered plists; all eleven `docs/*.py` checks exit 0; `MANIFEST.md` refreshed and `manifest_check.py` green; `timeout` never invoked; `--target-platform ios` never invoked.

**`sign-shortcut` side effects to expect:** it writes the pre-sign unsigned XML to `artifacts/shortcuts/<today>/<name>-<HHMMSS>.xml` **and** signs to `artifacts/shortcuts/<name>.shortcut`. No manual promotion step exists or should be added.

**Known signer quirks, both auto-retried:** `Error: The file doesn't exist.` for a file that does exist (retry from a clean XML→`.shortcut` copy); `Error: … isn't in the correct format.` even when `validate-shortcut`/`plutil -lint` pass (retry after `plutil -convert binary1`).

---

## Runtime State Inventory

This is a rename phase. All five categories answered explicitly.

| Category | Items found | Action required |
|---|---|---|
| **Stored data** | **`state.json` on the user's device.** Two fields carry renamed values: `"fork": "Dumb"` (bootstrap seed, action 75) and `"sequence": "Classic"` (unchanged — sequence *names* are not renamed by BD-06). **`"circle"` stores an integer, not a name** — verified: `circle` is written from `Circle Next`, a number seeded at 0 (`verify_circle_zero_silence` property (a)). **No stored value is a primitive name.** However: a device's existing `state.json` is *reused* unless `schema_version` changes — `fix_state_rebind()` (`:3022-3084`) bumped it 1→2 for exactly this reason, and the version-check conditional literal is rewritten to match. If the Panic Escape flag or a renamed `fork` value must reach existing devices, **`schema_version` must be bumped 2→3** in both the template text and the check literal, or the rename never lands on an installed phone. **This is a data migration, distinct from the code edit, and it is easy to miss.** | Bump `schema_version` 2→3 (template + `version_check["WFConditionalActionString"]`) if any seed field changes |
| **Live service config** | **The user's two iOS Personal Automations.** They reference the shortcut by library name. A signed-filename rename (Dumb→Core) **breaks both automations silently** — they keep pointing at the old library entry, which still exists after importing the new one. There is no API to patch them; the user must re-select the target in Shortcuts.app. | State it explicitly in the Note and in release text (D8) |
| **OS-registered state** | **None.** No Task Scheduler / launchd / pm2 / systemd registration anywhere in this project — it is a Shortcuts-only, no-companion-app product. Verified by the absence of any such tooling in `tools/`, `docs/` and `README.md`. | none |
| **Secrets / env vars** | **None.** No SOPS, no `.env`, no CI secrets, no API keys — the product has no network dependency (`README.md:12`). Verified: no secret-management file exists in the repo. | none |
| **Build artifacts** | `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` (regenerated), the two canonical signed `.shortcut` files (re-signed), the dated archives under `artifacts/shortcuts/2026-08-*/` (**historical — left alone**, per `260817-au7`'s precedent), `artifacts/shortcuts/MANIFEST.md` (refreshed), `docs/__pycache__/` and `tools/__pycache__/` (harmless). If the signed filenames change, the **old-named signed files remain on disk** — decide deliberately whether to delete them or leave them as history; `manifest_check.py` only asserts the rows it is given, so an orphaned file is invisible to it. | Regenerate all; decide on old signed files |

**Canonical question — after every file in the repo is updated, what runtime systems still have the old string cached, stored or registered?** Answer, in priority order: (1) an installed user's `state.json` `"fork"` value, unreachable without a `schema_version` bump; (2) an installed user's two Personal Automations, unreachable by any mechanism at all; (3) an installed user's existing `PROSOCHĒ — Control Room` Apple Note, which the renamed `contains "PROSOCHĒ"` predicate would still match (§6.2).

---

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Editing a string inside a `WFTextTokenString` | `sed`/regex substitution on the XML | `plistlib` round-trip that recomputes `attachmentsByRange` from `￼` offsets, guarded by a byte-identical no-op dumps first | `.claude/CLAUDE.md` §5: out-of-bounds ranges *"can crash Shortcuts on import."* `260817-au7` proved the method |
| Renaming all ten dispatch renderings | Editing the built XML's 80 conditionals | Change the tuple + condition code at `tools/build_state_engine.py:658-664` and rebuild | The generator is idempotent and reproduces hand edits byte-for-byte; hand-editing 80 sites is 80 chances to diverge from the generator, which then silently rewrites them back |
| Detecting an undispatched sequence entry | A one-off grep or a manual cross-check | `verify_dispatch_coverage()` in the generator + the promoted `docs/sequence_dispatch_check.py` | BD-06: this class is *"invisible to the validator, the ToolKit catalog, and the signed-artifact decrypt."* It is why Circle 8 shipped dead |
| Parsing the sequence entry's condition semantics | Hardcoding `4` or `99` in the checker | `match_strategy(code)` — resolve per branch from the branch's own code | Already written and already correct (`docs/sequence_dispatch_check.py:56-72`); hardcoding is what made the checker fragile in the first place |
| Reading what actually shipped | Trusting the unsigned source + an mtime | `aea decrypt` + `aa extract` + `plutil -convert xml1` (`.claude/CLAUDE.md` §8) | The AEA1 archive is *signed*, not encrypted; it unlocks with the leaf cert's public key. It is the only non-device "what shipped" channel |
| A "does the setting exist" gate on a dotted path | `read dotted key → has any value` | A numeric `> 0` test, or restructure to a flat read | `.claude/CLAUDE.md`: a dotted read with any missing segment is a **hard error**, so the gate can never read false without the read having already thrown. Unimplementable |
| Verifying manifest freshness | Reading `MANIFEST.md` and believing it | `python3 docs/manifest_check.py` | It hashes and sizes every declared path from disk. It goes red on every rebuild until refreshed — *that is the feature* |

---

## Common Pitfalls

### Pitfall 1 — Editing the Note body as text and shipping out-of-bounds attachment ranges
**What goes wrong:** the body's two attachments live at absolute offsets `{5478, 1}` / `{5509, 1}`; the H1 and both Run-Shortcut strings sit upstream of them. A text edit shifts every offset.
**Why it happens:** the ranges are invisible in a naive read of the string; the plist still lints, still validates, still signs.
**How to avoid:** `plistlib` round-trip, guarded by the six-step `260817-au7` method (§6.3).
**Warning signs:** offsets unchanged after a length-changing edit; a `{n, 1}` key whose `n` exceeds `len(string)`; Shortcuts crashing or showing wrong variable text on import.

### Pitfall 2 — Assuming the generator owns a string it merely reads
**What goes wrong:** grepping `tools/*.py` for a user-facing string, finding nothing, and concluding it does not exist or is generated elsewhere.
**Why it happens:** the file is named like a builder but is a marker-anchored transformer.
**How to avoid:** grep the built XML with `plistlib`, not the Python, for every user-facing string. Measured example: the Note title returns 1 hit in `tools/` (a comment) and 3 real ones in the artifact.
**Warning signs:** a "rename" that leaves the shipped artifact unchanged after a clean rebuild.

### Pitfall 3 — Moving 99→4 without abolishing the combined entries first (or vice versa)
**What goes wrong:** flipping the code while `Ash+Confession` etc. remain leaves three Circles dispatching nothing. Abolishing the entries while leaving code 99 leaves `Loud Mirror` double-dispatching through the `Mirror` branch.
**Why it happens:** they look like two independent changes.
**How to avoid:** land both in one commit, with the coverage guard already hard so either half alone fails the build.
**Warning signs:** `sequence_dispatch_check` reporting orphans, or a Circle-8 device run that shows the Mirror alert twice.

### Pitfall 4 — Renaming the Note to `PROSOCHĒ` while leaving the predicate at "contains"
**What goes wrong:** the Find Notes predicate binds to a stale `PROSOCHĒ — Control Room` note (limit 1, First Item) and the ledger appends to the wrong document forever.
**Why it happens:** the predicate is an obscure nested `WFContentPredicateTableTemplate`, three levels down from the action.
**How to avoid:** change `Operator: 99` → `4` in the same edit — subject to the donor caveat in §6.2.
**Warning signs:** on a device with a pre-existing note, "Open Control Room" opens the old one.

### Pitfall 5 — Duplicating `primitive_dispatch()` and forgetting the two hard site-count tables
**What goes wrong:** `environmental_restore_check` (14/14/20) and `phase9_self_check` (14/14, coerced 14/4) both go red.
**Why it happens:** the counts are derived in comments from "primitive_dispatch() is rendered TEN times", so an eleventh rendering is a legitimate move — but only if the numbers and the derivation comments move with it.
**How to avoid:** if Mechanism A (§8.3) is chosen, update both tables to 15/15/22 and 15/5 and rewrite their derivation comments in the same commit.
**Warning signs:** `expected 14 … sites, found 15`.

### Pitfall 6 — Renaming `voice_enabled` / `Toggle Voice` while renaming the Voice primitive
**What goes wrong:** the *voice output* feature (`state.json` `voice_enabled`, the `Toggle Voice` manual menu item, `speaktext`) is unrelated to the *Voice primitive* (Circle 8). Renaming the former breaks `docs/phase7_self_check.py:15`'s `MENU` list, the Status/Note `Voice:` line, and the `Snapshot Voice` read chain.
**Why it happens:** both are spelled "Voice"; the generator has 18 `Voice` matches and only two are the primitive.
**How to avoid:** rename only `("Voice", …)` in the dispatch tuple (`:660`) and the three `"Voice"` entries in the sequence arrays. Leave `voice_enabled`, `"Voice Enabled"`, `"Manual Voice"`, `"Snapshot Voice"`, `"Toggle Voice"` and `"Voice Memos"` untouched.
**Warning signs:** `phase7_self_check` red, or the Capture exit losing Voice Memos.

### Pitfall 7 — Forgetting `schema_version` when a seed field changes
**What goes wrong:** an installed device's `state.json` passes the three-check validity gate and is reused forever; the new `"fork"` value and any Panic Escape flag never reach it.
**Why it happens:** the local file rebuilds every time in testing, masking it.
**How to avoid:** if any bootstrap-seed field changes, bump `"schema_version": 2` → `3` in the template **and** `version_check["WFConditionalActionString"]` (both in `fix_state_rebind()`, `:3022-3084`). `[NOTE: fix_state_rebind() currently hardcodes both the 1→2 replacement and the `("1","2")` acceptance tuple — a 2→3 bump requires editing that function, not just data.]`
**Warning signs:** device shows `Fork: Dumb` after installing the Core build.

### Pitfall 8 — Adding an OPEN-arm surface outside the silent band
**What goes wrong:** `router_ui_census.py:234-245` fails with *"OPEN-arm surface(s) outside the Circle-0 silent band."*
**Why it happens:** any new alert/menu/ask in `universal_leaving()`'s vicinity must be inside the `Circle Next > 0` group.
**How to avoid:** put the Panic Escape **confirmation** in the MANUAL arm, never the OPEN arm; put any new OPEN-arm conditional strictly inside the silent-band group.
**Warning signs:** the census's offender list naming your new action's nearest comment.

---

## Code Examples

All from this repository, this session.

### The dispatch loop — the one site to change
```python
# tools/build_state_engine.py:658-666 (CURRENT)
for name, implementation in (("Knock", knock), ("Ash", ash), ("Silence", silence),
                             ("Confession", confession), ("Dimming", dimming), ("Exile", exile),
                             ("Mirror", mirror_and_voice), ("Voice", mirror_and_voice), ("Ice", ice_start)):
    if name == "Voice":
        continue
    group, check = if_block("Selected Primitive", 99, string=name)
    a += [comment(f"Dispatch {name} only when the selected Config entry names it:\n"
                  "- Input uses Selected Primitive from the sequence lookup.\n"
                  "- The otherwise path leaves State unchanged."), check]
    a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
```

### The exact-match idiom already used elsewhere (condition 4, plain literal)
```python
# tools/build_state_engine.py:614
respected_g, respected_if = if_block("Previous Respected", 4, string="true")
```

### Locating the Config literal by content, never by index
```python
# docs/sequence_dispatch_check.py:95-103
def config_literal(actions) -> dict:
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if isinstance(value, str) and '"config_version"' in value:
            return json.loads(value)
    raise AssertionError("the Config JSON literal was not found in the artifact")
```

### Collecting dispatch branches without hardcoding a condition code
```python
# docs/sequence_dispatch_check.py:130-143
for index, item in enumerate(actions):
    if item.get("WFWorkflowActionIdentifier") != CONDITIONAL:
        continue
    parameters = item.get("WFWorkflowActionParameters", {})
    if parameters.get("WFControlFlowMode") != 0:
        continue
    name = parameters.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")
    if name != SELECTED_PRIMITIVE:
        continue
    code = parameters.get("WFCondition")
    branches.append({"index": index, "tested": parameters.get("WFConditionalActionString"),
                     "code": code, "strategy": match_strategy(code)})
```

### The guard-message idiom to copy (actionable, explains the consequence)
```python
# docs/manifest_check.py:148-153
require(
    basename in SIGNED_BASENAMES,
    f"signed artifact {basename!r} is not one of the two canonical display names "
    f"{sorted(SIGNED_BASENAMES)} -- a suffixed name imports as a separate library "
    f"entry the Personal Automations do not reference (DIST-04)",
)
```

---

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|---|---|---|---|---|
| `python3` | both builders, all eleven checks | ✓ | 3.13.9 (≥3.10 required for PEP 604) | — |
| `validate-shortcut` | DIST-01 | ✓ | Shortcuts Playground 1.2.1, at `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/bin/` | — |
| `sign-shortcut` | DIST-02 | ✓ | same plugin | — |
| `shortcuts` (macOS CLI) | the real signer behind `sign-shortcut` | ✓ | `/usr/bin/shortcuts` | none — macOS-only |
| `aea` | decrypt-verify | ✓ | `/usr/bin/aea` | — |
| `aa` | decrypt-verify | ✓ | `/usr/bin/aa` | — |
| `plutil` | lint + binary1 retry | ✓ | `/usr/bin/plutil` | — |
| `openssl` | leaf-cert pubkey extraction | ✓ (implied by the working `260817-au7` run) | system | — |
| Git ancestor `7ca8ebb…` | provenance gate | ✓ | **exit 0 measured at `ae0226c`** | none — abort the rebuild |
| Apple-Intelligence iPhone | not needed this phase | — | — | Phase 15/19 concern |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** none.

---

## Validation Architecture

### Test framework

| Property | Value |
|---|---|
| Framework | **No test framework.** Eleven bespoke structural checkers in `docs/*.py`, each a standalone `python3` script that raises `AssertionError`/`SystemExit` and prints a one-line pass message |
| Config file | none — by design |
| Quick run command | `python3 docs/sequence_dispatch_check.py && python3 docs/state_engine_self_check.py` (~2 s, no rebuild) |
| Full suite command | `for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check manifest_check; do python3 docs/$f.py \|\| echo "FAIL $f"; done` |

**Baseline measured this session at `ae0226c`: all eleven exit 0**, and `git status --short` is empty afterwards (the builders are idempotent). This is a materially better starting position than Phase 10's (three of six red) — **any redness during this phase is a regression this phase caused.**

### Phase requirements → test map

| Req | Behavior | Test type | Automated command | Exists? |
|---|---|---|---|---|
| CIRC-08 | Every sequence entry dispatches exactly one branch; every branch is named | structural | `python3 docs/sequence_dispatch_check.py` → `0 orphan(s), 0 unreachable, 0 unknown` **and exit non-zero on any of them** | ❌ Wave 0 — must be promoted from reporter to gate |
| CIRC-08 | The generator refuses to emit an uncovered dispatch surface | build guard | `python3 tools/build_state_engine.py` (fails via `verify_dispatch_coverage`) | ❌ Wave 0 — new `verify_*` |
| CIRC-02, AUDIT-02 | New primitive names present, old names absent | structural | extend `docs/phase5_self_check.py:66-68`'s name list to the nine target names; add a negative assertion that the six retired names are absent from the artifact text | ⚠️ exists, needs rewrite (it currently asserts the **old** names, including `Ash+Confession` / `Silence+Mirror`) |
| CIRC-06 | `Eject` occupies Circle 6 in all three sequences; `Redirect` occupies none | structural | assertion over `config_literal(actions)["sequences"]` | ❌ Wave 0 — fold into the coverage guard |
| ROOM-01, ROOM-02 | Note title is `PROSOCHĒ` at all three sites; no `— Control Room` remains in a user-facing string; attachment offsets equal recomputed `￼` offsets in **both** forks | structural | new `docs/note_identity_check.py`, or extend `router_ui_census.py` | ❌ Wave 0 |
| ROOM-02 | Both automation blocks name the new canonical display name | structural | string assertion on the decrypted body of both signed artifacts | ❌ Wave 0 — model on `260817-au7`'s decrypt assertions |
| DIST-01 | Validator passes at the iOS 26 target | tool | `validate-shortcut src/PROSOCHE-*.xml --target-macos 26 --target-platform all` | ✅ |
| DIST-02 | Signed files exist, non-zero, exact display names, hashes match MANIFEST | structural | `python3 docs/manifest_check.py` | ⚠️ exists, `DISPLAY_NAMES` must be updated |
| (cross-cutting) | Builder is idempotent after every change | structural | `docs/phase5_self_check.py` / `phase6_self_check.py` (each runs the builder twice and compares digests) | ✅ |

### Sampling rate

- **Per task commit:** `python3 tools/build_state_engine.py && python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py` (~10 s)
- **Per wave merge:** all eleven checks + both validators
- **Phase gate:** all eleven green + both validators + both signed + both decrypt-verified + `MANIFEST.md` refreshed + `manifest_check` green, before `/gsd-verify-work`

### Wave 0 gaps

- [ ] `verify_dispatch_coverage(actions)` in `tools/build_state_engine.py`, called from `main()` and from `build_sentient.py`'s verify chain — covers CIRC-08, CIRC-06
- [ ] Promote `docs/sequence_dispatch_check.py` to a hard gate: empty `KNOWN_ORPHANS`, non-zero exit on orphan/unreachable/unknown, rewrite the docstring (which currently states it is deliberately not a gate)
- [ ] Rewrite `docs/phase5_self_check.py:66-68`'s name list; add negative assertions for the six retired names
- [ ] Update `docs/manifest_check.py:DISPLAY_NAMES` and `docs/sentient_core_check.py:9` for the Core/Aware rename
- [ ] Update `docs/environmental_restore_check.py:78` and `docs/phase9_self_check.py:97-104` **only if** Mechanism A adds an eleventh `primitive_dispatch()` rendering
- [ ] A note-identity check (three title sites + attachment-offset equality in both forks)
- [ ] Update `docs/phase7_self_check.py:15`'s `MENU` list **only if** a Panic Escape menu item is added

---

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1`.

### Applicable ASVS categories

| ASVS category | Applies | Standard control |
|---|---|---|
| V2 Authentication | **no** | No accounts, no identity, no login anywhere in the product |
| V3 Session Management | **no** (in the ASVS sense) | `active_session` is a behavioural session, not an auth session; no token, no credential |
| V4 Access Control | **no** | Single-user, on-device, no multi-tenancy, no privilege boundary |
| V5 Input Validation | **yes** | The only external input is the Shortcut Input string, routed by **positive identification** (`Input Key == "OPEN"` / `== "CLOSE"`, condition 4) with everything else falling to MANUAL — `ROUTER_OVERVIEW`, `tools/build_state_engine.py:1294`, enforced by `verify_router_shape()`. The renamed sequence entries are compared with condition 4 exact match, which is the stricter of the two available modes |
| V6 Cryptography | **no** (nothing hand-rolled) | Signing is Apple's `shortcuts sign` / AEA1. This phase writes no crypto. Never hand-roll — `.claude/CLAUDE.md` §8 |
| V7 Error Handling & Logging | **partial** | The Attention Ledger is a local Apple Note. This phase adds no new logged field beyond an optional Panic Escape change record |
| V9 Communications | **no** | Zero network dependency (`README.md:12`); the Dumb/Core fork has no model call at all |
| V12 File Resources | **yes** | One `state.json` in the Shortcuts iCloud folder, one Apple Note. **§6.2's predicate widening is the one real V12 issue this phase introduces** — a "contains" match on a shortened title can bind writes to an unintended file |
| V14 Configuration | **yes** | Provenance ancestor gate before either builder; signed-filename discipline; `--target-platform all` |

### Known threat patterns for this stack

| Pattern | STRIDE | Standard mitigation |
|---|---|---|
| Note-title widening binds the ledger to a stale/foreign note | **Tampering / Information disclosure** | Exact-match predicate (`Operator: 4`) instead of `contains` — §6.2 |
| Signed filename drift → user's automations point at a dead entry | **Denial of service** (the product silently stops protecting) | `docs/manifest_check.py`'s DIST-04 assertion; update `DISPLAY_NAMES` |
| Silent dispatch no-op (Circle N shows nothing) | **Denial of service** | The dispatch-coverage build guard — the whole point of BD-06 Decision 5 |
| Removing Panic Escape strands a user with no bypass | **Denial of service / safety** | Emergency Restore stays **unconditionally** available (CONTEXT is explicit); removal requires a manual Note edit **plus** explicit confirmation; the change is recorded in the ledger |
| Out-of-bounds `attachmentsByRange` crashes Shortcuts on import | **Denial of service** | Recompute offsets; `plutil -lint`; decrypt-verify (§6.3) |
| A guessed plist literal silently routing somewhere unintended | **Spoofing / Information disclosure** | Not applicable this phase — no new literal is guessed. The standing rule (BD-04/BD-04-R) is unchanged |

**No new trust boundary, network endpoint, credential store, or file-access pattern is introduced by this phase.** The single security-relevant change is the Note-lookup predicate widening in §6.2.

---

## State of the Art

| Old position | Current position | When changed | Impact on this phase |
|---|---|---|---|
| "Ash is NOT AVAILABLE on iOS" (BD-01) | BD-01-R2: **VERIFIED — donor-confirmed**, `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`, `state` integer 1/0, `operation` elided | 2026-08-16 | Phase 14, not here. `docs/phase5_self_check.py:78` still asserts the intent is **absent** — leave that green |
| "`WFLLMModel` literal is UNRECOVERED" (BD-04) | BD-04-R2: **`Apple Intelligence on Device`**, device-export evidence, already written at `tools/build_sentient.py:29` | recorded 2026-08-17 | No action; do not disturb |
| `--target-platform ios` | `--target-platform all` (DEV-01 — `ios` rejects 3675/3675 actions) | 2026-08-14 | Binding |
| "a signed `.shortcut` cannot be read back as plaintext" | False — AEA1 is *signed*, not encrypted; `aea decrypt` + `aa extract` recovers it | 2026-08-13 | Decrypt-verify is a required step, not a nicety |
| `docs/sequence_dispatch_check.py` is deliberately a reporter | This phase is the "future phase" its own docstring names for promotion to a build guard | now | Wave 0 |
| Circle scan seeded at 1 | Seeded at **0** — the silent band | Phase 10 | Every OPEN-arm change must respect `verify_circle_zero_silence` |

**Deprecated / retired by this phase:**
- The three combined sequence entries `Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror` — and with them, the only reason condition 99 was ever used for dispatch.
- The `KNOWN_ORPHANS` escape hatch in `docs/sequence_dispatch_check.py`.

---

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | `Operator: 4` ("is") is accepted in a Notes `WFContentPredicateTableTemplate` for the `Name` property | §6.2 | The Find Notes action fails or silently matches nothing on device; bootstrap self-heal breaks. **Settled by:** a donor export of a "Name — is" Find Notes action, decrypted per `.claude/CLAUDE.md` §8. **Fallback:** leave `Operator: 99` and record the collision risk as a deviation |
| A2 | Adding a ninth dispatch branch (`Loud Mirror` → `mirror_and_voice()`) leaves `EXPECTED_SITES` at 14/14/20 | §5.4, §8.2 | Two checkers go red unexpectedly. **Settled by:** running `docs/environmental_restore_check.py` and `docs/phase9_self_check.py` immediately after the first rebuild. Reasoning is sound (`mirror_and_voice()` emits no brightness/volume/device-details action — verified by reading `:604-629`) but not yet executed |
| A3 | The projected artifact size (~4,090 actions, ~2.5 MB source, ~210 KB signed) stays within all practical limits | §5.4 | Validator or signer failure. **Settled by:** the first rebuild + sign. No documented limit exists in the Playground bundle (`.claude/CLAUDE.md` §6 lists only wiring-density and comment-density concerns), so risk is low |
| A4 | `verify_dispatch_coverage()` can run inside the generator's `main()` — i.e. the Config literal is present and parseable at the point the verify chain runs | §5.3 | The guard raises spuriously. Low risk: it is action 7, outside every marker-bounded replacement, and `docs/sequence_dispatch_check.py` already parses it from the finished artifact. **Settled by:** running it |
| A5 | Mechanism B's `Leaving` path would need `is.workflow.actions.exit` to terminate the run, and appending one there is safe | §8.3 | Only matters if Mechanism B is chosen against the recommendation. **Settled by:** an on-device run, or a decrypt-inspect of the current Leaving tail |
| A6 | Existing `artifacts/shortcuts/2026-08-*/` dated archives should be left untouched under the old names | §7.1 D7 | Cosmetic inconsistency only. Based on `260817-au7`'s explicit precedent ("historical records and were left alone") |

---

## Open Questions

1. **Where do the Dante names actually surface?**
   - What we know: zero Dante names exist in the artifact today (measured); all copy says `Circle {N}`.
   - What's unclear: Addendum §1 says "replace the existing Circle names" but there are none to replace, and BD-06 makes the names positional labels rather than functional identifiers.
   - **Recommendation:** surface them in the Test-a-Circle submenu titles, the Status alert, and the Note's `## CURRENT STATE` gloss. Do **not** put them in the 30 Mirror templates (30× the copy churn for no product gain). Menu titles must match `WFMenuItems` element-for-element and in order.

2. **`Limbo` as both a profile name and Circle 1's name.**
   - What we know: 12 `Limbo` occurrences, all profile; BD-06 Decision 2 assigns it to Circle 1.
   - What's unclear: BD-06 does not address the collision.
   - **Recommendation:** disambiguate in copy (`Profile: Limbo` vs `Circle 1 · Limbo`) rather than renaming either. Record the decision so a future phase does not "fix" it.

3. **Does the Panic Escape flag need a `schema_version` bump?**
   - What we know: `fix_state_rebind()` bumped 1→2 precisely so a stale device state would rebuild once; the version-check literal is hardcoded to `"2"` and the acceptance tuple to `("1","2")`.
   - What's unclear: whether this phase's seed changes must reach installed devices, or whether the phase is pre-release enough that it does not matter.
   - **Recommendation:** bump to 3 if `"fork"` or any new flag is seeded. Cheap; the alternative is a device that silently keeps the old fork label.

4. **Does the Sentient/Aware note-body divergence land here or defer again?**
   - What we know: `260817-au7` explicitly assigned it to "`2026-08-14-apply-build-addendum-01.md`" — this phase.
   - What's unclear: budget.
   - **Recommendation:** land it (§7.2 option 1). Deferring twice means Aware ships instructing users to select a shortcut that will not exist under the new names.

5. **Do the old-named signed artifacts stay on disk after the rename?**
   - What we know: `manifest_check.py` only asserts declared rows; an orphaned file is invisible to it.
   - **Recommendation:** delete them and state the breaking change in `MANIFEST.md`, so `artifacts/shortcuts/` never contains two plausible "current" imports.

---

## Sources

### Primary (HIGH confidence — read or executed this session)
- `docs/CAPABILITY-DECISIONS.md` — BD-06 read in full (lines 288–435) and transcribed verbatim; BD-01-R2, BD-04-R2 read for scope boundaries
- `PROSOCHE_Build_Addendum_01.md` — §1–§5 read in full
- `tools/build_state_engine.py` (3,159 lines) — `primitive_dispatch()`, `universal_leaving()`, all nine primitive functions, `verify_circle_zero_silence()`, `verify_conditional_action_string()`, `if_block()`, `fix_state_rebind()`, `main()` read directly
- `tools/build_sentient.py` (234 lines) — read in full
- All eleven `docs/*.py` checkers — read; **all executed, all exit 0**; per-file grep for name dependencies
- `src/PROSOCHE-Dumb.xml` / `src/PROSOCHE-Sentient.xml` — walked with `plistlib`: Config literal (action 7), state seed (action 75), Note predicate/body/title (3602/3616/3619 and 3684), all 80 dispatch conditionals, all `WFMenuItems` arrays, `WFWorkflowName`
- `src/CONFIG-BLOCK.md`, `artifacts/shortcuts/MANIFEST.md`, `README.md`, `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/ROADMAP.md` Phase 11 block
- `docs/BUILD-NOTES.md` §9, §10, §19; `.planning/phases/10-.../10-RESEARCH.md` §5b/§5c
- `.planning/quick/260817-au7-ios26-automation-onboarding/{PLAN,SUMMARY}.md` — the working precedent for editing the Note body
- `git show e84ee77` — the Note internal-name decision
- `git merge-base --is-ancestor 7ca8ebb… HEAD` → exit 0
- `.claude/CLAUDE.md` — seven parameter-defect axes, verified iOS runtime semantics, evidence hierarchy, §4 condition codes, §5 attachment rules, §8 AEA1 recovery

### Secondary (MEDIUM confidence)
- Shortcuts Playground 1.2.1 reference docs, cited **indirectly** via `.claude/CLAUDE.md`'s already-distilled tables (condition codes, display-vs-non-display parameter rule, `attachmentsByRange` semantics, menu case-order requirement). Not re-read this session — the CLAUDE.md distillation is the project's own operative record of them

### Tertiary (LOW confidence)
- **None.** No web search was performed and none is warranted for this phase.

---

## Metadata

**Confidence breakdown:**
- Code inventory (file:line, counts, action indices) — **HIGH**: every number was measured with the command shown, not estimated. Grep counts are word-boundary matched and exclude generated `src/*.xml` and historical `artifacts/`
- Architecture (in-place transformer; plist-only strings; Sentient-forks-Dumb) — **HIGH**: read from `main()` and `build_sentient.main()` directly, corroborated by `260817-au7`'s independent finding and by the empty `git status` after a full rebuild
- Guard behaviour and current baseline — **HIGH**: all eleven checkers executed, exit codes recorded
- The 99→4 substring analysis — **HIGH**: measured operand shapes plus a hand-checked substring cross-product over the nine target names
- Notes filter `Operator: 4` acceptance — **LOW**: flagged `[UNVERIFIED]`, with the donor test that would settle it named
- Panic Escape mechanism — **MEDIUM**: the three constraining guards are measured facts; the choice between Mechanism A and B is a design recommendation, and Mechanism B's `exit` behaviour is `[UNVERIFIED]`
- Size/action-count projections — **MEDIUM**: derived arithmetically from measured per-function action counts

**Research date:** 2026-08-17
**Valid until:** until the next commit that touches `tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml`, or any `docs/*.py` checker. Every action index in this document (7, 75, 520, 1448, 3602, 3616, 3619, 3684) is position-dependent and will shift the moment the artifact is rebuilt with new content — **locate by content, never by index**, exactly as `docs/sequence_dispatch_check.py:95-103` does.
