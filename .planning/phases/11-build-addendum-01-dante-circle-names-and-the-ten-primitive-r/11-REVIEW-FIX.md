---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
fixed_at: 2026-08-18T00:00:00Z
review_path: .planning/phases/11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-REVIEW.md
iteration: 3
findings_in_scope: 4
fixed: 4
skipped: 0
status: all_fixed
---

# Phase 11: Code Review Fix Report — iteration 3

**Fixed at:** 2026-08-18
**Source review:** `.planning/phases/11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r/11-REVIEW.md`
**Iteration:** 3
**Scope:** WR-20, WR-21, WR-22, IN-04

**Summary:**
- Findings in scope: 4
- Fixed: 4
- Skipped: 0

| Finding | Commit | Files |
|---|---|---|
| WR-20 | `7d963d1` | `tools/build_state_engine.py` |
| WR-21 | `353621f` | `docs/environmental_restore_check.py` |
| WR-22 | `65e47b4` | `docs/environmental_restore_check.py` |
| IN-04 | `6396a6e` | `tools/build_sentient.py`, `docs/sentient_audit_check.py` |

## Read this first — the honest statement about WR-20

**I did not close WR-20 by teaching the fixpoint about `gettext`.** The walk no longer
enumerates hop identifiers at all. But it is **not unconditionally general either**, and the
one place it deliberately stops is named, measured and reproduced below under
`## Residual`. Reporting it as an unqualified class fix would be the exact failure the brief
forbids.

What is now general: **every action that carries a reference to a variable or to another
action's output propagates the provenance of those references to whatever it publishes.**
`set_var` and `gettext` are two instances of that rule; so is `math`, so is `expression`, so
is `getitemfromlist`, so is an action nobody has emitted yet. There is no allowlist.

What is not: **three container-shaped identifiers are barriers** — `getvalueforkey` (which
*seeds* instead of inheriting), `setvalueforkey` and `dictionary`. A value routed through a
dictionary and read back out under a different key therefore still loses its provenance. I
built that control and it exits 0. See `## Residual`.

The barrier list is a **denylist**, not an allowlist, and that inversion is the load-bearing
property: an identifier nobody anticipated **propagates**, so an unanticipated hop now fails
**loud** (provenance carried further than needed, guards get stricter) rather than failing
**quiet** (the guard silently resolves nothing) — which is the defect class of WR-16, WR-20,
and half this phase.

## Definition of done — measured, not asserted

Measured in an isolated `git worktree` (`/tmp/sv-11-reviewfix-…`) branched from `main` at
`ab96bed`. The tracked tree was never mutated; every negative control ran on a
`git archive HEAD` copy under the scratchpad.

| Gate | Result |
|---|---|
| `python3 <each>` for all 13 `docs/*.py` | **13/13 exit 0** |
| `docs/retired_clause_check.py` | exit 0 here. The documented 4 gitignored `.planning/graphs/` + `graphify-out/` occurrences are absent from a `git worktree` checkout, so this measures 13/13 where the main tree measures 12/13. **That difference is the known, separately-tracked, not-mine item — not a fix.** |
| Gate A, `src/PROSOCHE-Dumb.xml` | `Validation passed.`, exit 0 |
| Gate A, `src/PROSOCHE-Sentient.xml` | `Validation passed.`, exit 0 |
| Gate B (advisory, non-blocking) | exactly **one** line per fork — the documented `com.apple.mobilenotes.SharingExtension` / `WFCreateNoteInput` waiver, at indices **4148** (Core) and **4282** (Aware), unchanged. No new finding. |
| Both builders after every fix | exit 0; `md5` identical across consecutive rebuilds |
| Shipped totals | Core **4304** / Aware **4438**; Aware **2** `askllm`, Core **0** |
| `git status --short src/` | **empty** |

**No re-sign was performed, and none was needed — stated explicitly rather than acted on
reflexively.** All four fixes are guard-only. After all four, both forks rebuild to
`a8d712b091aff9b1549ea7d236c4a15a` (Core) and `0dee5197e609ccbc8d59af388d06cede` (Aware),
byte-identical to the shipped sources, and `src/` is untouched. `artifacts/shortcuts/MANIFEST.md`
therefore needs no refresh: nothing it declares moved.

## Fixed Issues

### WR-20: the transitive-provenance fix follows one edge only

**Files modified:** `tools/build_state_engine.py`
**Commit:** `7d963d1`

**Applied fix.** `_read_variable_keys()` is now a thin projection over a new
`_variable_provenance()`, which runs one fixpoint over the **emitted data-flow graph**:

- `_reference_descriptors()` walks the **whole** `WFWorkflowActionParameters` tree — not a
  named slot — collecting every `Type: "Variable"` / `Type: "ActionOutput"` descriptor
  wherever it sits: bare `WFTextTokenAttachment`, a `WFTextTokenString`'s
  `attachmentsByRange`, `if_block()`'s nested `WFInput.Variable` wrapper, a `WFItems` row
  wrapper (axis 8), a dictionary field value. Descent continues *through* a matched
  descriptor because `if_block()` nests one inside another. Enumerating slots is the failure
  WR-20 measured one level up; this enumerates none.
- Nodes are action outputs (keyed by the action's own `UUID`) and named variables. A
  `getvalueforkey` **seeds** its literal key; every non-barrier action **inherits** the union
  of its references. `setvariable` publishes to a variable name as well as a UUID.
- Provenance is carried as `(key, stringified)` pairs. `gettext` / `text` flip
  `stringified`, which is what preserves axis 9's `read_value()`-vs-`get_value()` distinction
  — see the false-positive note below.
- Termination is unchanged in kind: sets grow monotonically over a finite vocabulary
  (literal keys × {stringified, not}). Converges in **3** iterations on both forks.
- Incidental, inside the code being rewritten: a nameless `setvariable` can no longer create a
  `None`-keyed entry (`isinstance(..., str)` guard). That is the latent **IN-06** shape, which
  was not in scope; I am recording it as a side effect rather than claiming IN-06 closed,
  since IN-06's second half (`_tested_variable()`) is untouched.

**Verified by the adversary, not by the change.** CR-01 rebuilt **verbatim** —
`dimming()` re-gated onto the `settings_snapshot.brightness` **container** at condition 100
with the whole capture-and-apply body back in the `otherwise` arm — behind each hop shape.
Each row is a full build of a mutated generator copy, `before` = `git archive HEAD` (the
iteration-2 code), `after` = the same tree with only this commit applied:

| Control | before | after |
|---|---|---|
| **J0** no hop (baseline) | build **exit 1** | build **exit 1** |
| **J1** one **`gettext`** hop | build **exit 0** ← WR-20 | build **exit 1** |
| **J2** one **`set_var`** hop | build **exit 1** | build **exit 1** (WR-16 preserved) |
| **J3** two-hop **`set_var` → `gettext`** | build **exit 0** | build **exit 1** |
| **J4** two-hop **`gettext` → `set_var`** | build **exit 0** | build **exit 1** |

The `after` message in all five is `verify_environmental_reachability()`'s own dead-arm text:
*"an environmental read or write sits in the never-taken arm of a permanently-true
settings_snapshot container gate…"*.

Same shape re-run on the Panic Escape **bypass** gate (`universal_leaving()`, flipped to
condition 100), which is the gate deciding whether the user is offered the Leaving/Continue
menu at all:

| Control | before | after |
|---|---|---|
| **I1** one `gettext` hop | core **exit 0**, 12/13 checkers green | core **exit 1** |
| **I2** one `set_var` hop | core exit 1 | core exit 1 |
| **I3** `set_var` → `gettext` | core **exit 0**, 12/13 green | core **exit 1** |

`after` message: *"a Panic Escape gate uses a non-numeric condition code action 531: 'PE Gate'
at condition 100 — the variable is read from 'panic_escape_enabled'…"*.

**One correction to the acceptance wording, stated rather than glossed.** The brief asked for
`docs/environmental_restore_check.py` to exit 1 in every case. It exits **0**, and that is the
*stronger* outcome, not a miss: the build now refuses to write the defective artifact, so
`src/` still holds the good fork and the checker has nothing to find. That checker parses the
built artifact and asserts the guards exist and are called; it never runs
`verify_environmental_reachability()` itself, so it structurally cannot see a defect the build
gate has already stopped. The chain that actually holds is: **guard call present ⇒ the build
fails** (measured above) **and guard call removed or commented out ⇒
`environmental_restore_check.py` fails** (measured under WR-21/WR-22 below). Neither half
alone is the property; the composition is.

**Zero false positives, re-measured on the shipped tree.**

| | Core | Aware |
|---|---:|---:|
| `variable → variable` copies (iteration 2's figure) | **40** | **42** |
| propagation edges the new walk follows | **1431** | **1478** |
| resolved variables | 72 → **104** | 73 → **107** |
| key assignments | 72 → **146** | 73 → **157** |
| **`settings_snapshot`-provenance variables** | 6 → **6** (added: none) | 6 → **6** (added: none) |
| **`panic_escape_enabled` variables** | `{Panic Escape Enabled, Panic Escape Stored}` — unchanged | unchanged |

So the walk now follows ~36× more edges while the two safety-critical provenance sets are
**bit-identical to before**. The widening it does produce is genuine data flow
(`Heat After Contract` really is derived from `heat`, `heat.open_base`, `heat.decay_amount`…).

**One false positive the generalisation *did* create, and how it was closed rather than
suppressed.** Because the walk now also resolves `get_value()`'s two-action form — which the
old chain walk could not see at all — `verify_compound_value_reads()` would have fired on
`Recent Sessions`, `Exit Events` and `Profile Enabled Exits`, i.e. on **three correct
`get_value()` call sites**. That guard's subject is axis 9's *Get Text stringification*, not
the read. It now consumes `_stringified_variable_keys()` instead, and the split takes it back
to **zero offenders** on both forks. Measured: unsplit would be
`['Exit Events', 'Profile Enabled Exits', 'Recent Sessions']`; split is `[]`.

---

### WR-21: `call_site_check()`'s substring test is satisfied by a commented-out call

**Files modified:** `docs/environmental_restore_check.py`
**Commit:** `353621f`

**Applied fix.** New `called_names(function)` parses `inspect.getsource(function)` with
`ast` and returns the set of plain `ast.Name` call targets; `call_site_check()` tests
membership in that set instead of `f"{name}(" in body`. `ast` and `textwrap` are stdlib and
this file already imported `inspect`. The docstring's honesty is kept and narrowed to what is
still true of *any* static read: a call behind a never-taken branch, or reached through an
alias or `getattr`, still reads as present.

**Negative control** — both guard calls (`verify_environmental_reachability`,
`verify_panic_escape_isolation`) in **both** builders, definitions untouched:

| Mutation | before | after |
|---|---|---|
| `# verify_…(actions)  # TEMPORARILY DISABLED` | builds exit 0, `env_check` **exit 0**, **13/13** green | builds exit 0, `env_check` **exit 1**, 12/13 |
| call replaced by `pass` (deletion) | `env_check` exit 1, 12/13 | `env_check` exit 1, 12/13 (no regression) |

`after` message: *"build_state_engine.py's main() no longer CALLS
verify_environmental_reachability() — the function still exists, so the REQUIRED_SYMBOLS check
above stays green while the guard is disarmed…"*.

---

### WR-22: `CALLED_GUARDS` is a hand-copied subset with nothing reconciling it

**Files modified:** `docs/environmental_restore_check.py`
**Commit:** `65e47b4`

**Applied fix.** Two parts, both as the review specified.

1. **Derived, never copied:**
   `CALLED_GUARDS = tuple(name for name in REQUIRED_SYMBOLS if name.startswith("verify_"))`.
   The comment records *why* — this is the archive's own recurring class (WR-04, WR-05,
   WR-06, WR-14: coupled literals with nothing reconciling them), reintroduced by the fix for
   a finding about vacuous guards.
2. **`verify_panic_escape_seed` added to `REQUIRED_SYMBOLS`**, beside
   `verify_panic_escape_isolation`, with the written reason the review argued for: the two are
   one guard pair, and this one holds half of the WR-19 fix.

The derivation is self-demonstrating: adding the sixth name to `REQUIRED_SYMBOLS` **only**
moved `CALLED_GUARDS` from 5 entries to 6 with no second edit. Confirmed by evaluation:
`('verify_state_seed', 'verify_restore_gates', 'verify_capture_persistence',
'verify_environmental_reachability', 'verify_panic_escape_isolation',
'verify_panic_escape_seed')`.

**Negative control** — `verify_panic_escape_seed(actions)` removed from `main()` in **both**
builders:

| Mutation | before | after |
|---|---|---|
| deleted (→ `pass`) | builds exit 0, **13/13 green** | `env_check` **exit 1**, 12/13 |
| commented out | builds exit 0, **13/13 green** | `env_check` **exit 1**, 12/13 |

That is the "half of the WR-19 fix is protected by nothing" measurement, closed.

---

### IN-04: `WR-18`'s builder assertion is tautological with respect to marker derivation

**Files modified:** `tools/build_sentient.py`, `docs/sentient_audit_check.py`
**Commit:** `6396a6e`

**Decided on the merits, then applied.** The review offered a fix and left the checker
question open. Both halves are answered:

1. **The builder assertion is now independent.** The inline OPEN-arm derivation was factored
   into one module-level `open_arm_contract_markers(actions)`, called **twice over two
   different inputs**: on the already-spliced Aware list to find the *insertion points*, and
   on a **fresh parse of the untouched Core bytes** (`plistlib.loads(original)`) to find the
   *expectation*. The assertion is now
   `if not expected or inserted != expected or len(markers) != expected`. This is the review's
   own preferred shape — the builder gains independence and the codebase gains **no third
   derivation**, because both call sites share one body.
2. **`docs/sentient_audit_check.py` does NOT get a Core-derived expectation — declined, on a
   rationale that now holds.** With the builder assertion independent *and* firing before
   disk, and `sentient_core_check.py` keeping the same expectation post-hoc on the shipped
   artifact, a third instance in `sentient_audit_check.py` would assert exactly what
   `sentient_core_check.py` already asserts, on the same artifact, at the same moment, and
   give the derivation a third place to drift. The reason — **and the retraction of the wrong
   one** — is now written into that file's own docstring, where a reader looking for it will
   find it, rather than only in a process artifact.

**Correction to the record (this file, iteration 1) — quoted before it is refuted.**
Iteration 1's `11-REVIEW-FIX.md` said, at its WR-18 entry:

> *"`docs/sentient_audit_check.py` was deliberately **not** given a Core-derived expectation. The
> review offered that as an alternative to correcting the SUMMARY; correcting the SUMMARY was the
> mandated half, and the builder assertion is strictly stronger than a second standalone checker
> because it fires before the artifact reaches disk. Duplicating `sentient_core_check.py`'s
> derivation into a third file would have added a second place for that derivation to drift."*

The **outcome** was right and is retained. The **"strictly stronger"** clause was wrong, and
iteration 2 measured it rather than arguing it. The builder assertion was stronger in
**timing** and weaker in **independence**, and independence was the half that mattered. The
last sentence ("a third place to drift") was and remains correct — it is why the fix was to
make the builder independent rather than to add a third checker. This paragraph is the
correction; the wording above is preserved rather than deleted, per this project's own
history-corrected-not-deleted convention.

**Negative controls** — the two defect classes, distinguished:

| Defect | before | after |
|---|---|---|
| **insertion loop** (`markers[:1]` — WR-18's own control) | build exit 1, artifact unchanged | build exit 1, artifact unchanged (no regression) |
| **derivation** (`markers` truncated after collection; `open_test`/`open_end` intact) | build **exit 0**, artifact **CHANGED** → **4372** actions written to disk, `sentient_audit_check.py` **exit 0** (passes the defect), only `sentient_core_check.py` exit 1 | build **exit 1**, artifact **unchanged at 4438**, nothing written |

`after` message: *"the Core fork's OPEN arm has 2 dispatch rendering(s); this build collected 1
marker(s) and emitted 1 Use Model action(s)."* — it now names all three quantities, so a reader
can tell which one moved.

## Residual — what WR-20's fix still does not follow

Named precisely, because a partial fix reported as a class fix is the failure this project
forbids. Each of these was checked, not assumed.

### R-1 — provenance does not survive a round trip THROUGH a dictionary. **MEASURED, OPEN.**

`getvalueforkey`, `setvalueforkey` and `dictionary` are deliberate barriers. Writing a value
into a dictionary key and reading it back out under **that** key restarts provenance at the new
key, so the original key is lost.

Reproduced on an isolated copy of the fixed tree — the Panic Escape flag copied into an
already-seeded `State` key and read back, then gated at condition 100:

```
set_value("last_app", variable("Panic Escape Enabled"))
read_value("last_app", variable("State"), "PE Gate")
if_block("PE Gate", 100)
```
```
python3 tools/build_state_engine.py -> EXIT 0
python3 tools/build_sentient.py     -> EXIT 0
12 of 13 checkers                   -> EXIT 0
```

(The thirteenth is `manifest_check.py`, failing only on a declared byte-size mismatch from the
two extra actions — it does not see the defect. Same footnote iteration 2 recorded for its own
Control I.) An earlier variant using an *unseeded* scratch key exits 1, but by
`verify_state_seed()` complaining about the unseeded key — a different guard catching a
different thing, which is luck, not coverage.

**Why the barrier is there and not simply removed.** With those three identifiers propagating,
the map explodes from **146 to 2325** key assignments on Core: `State` absorbs the provenance of
everything ever written into it and hands it to every subsequent read. That is conflation, not
provenance, and it would make `verify_restore_gates`, `verify_sentinel_gates` and
`verify_environmental_reachability` fire on essentially everything.

**What would actually close it:** container-key-aware provenance — track
`(container variable, key) → value provenance` through `setvalueforkey`, so a write of a
snapshot-derived value into `State["last_app"]` makes the later read of `State["last_app"]`
inherit it, without `State` itself becoming a provenance sink. That is a larger change than
this pass, and **I am recording it as open rather than shipping it half-done.**

### R-2 — `_tested_variable()` reads one gate shape. **CHECKED, not reachable today.**

The provenance walk is now general; the *gate* side is not. `_tested_variable()` reads only
`WFInput.Variable.Value`, so a multi-condition `If` (the `WFConditions` /
`WFContentPredicateTableTemplate` Any/All serialization documented in `.claude/CLAUDE.md` §4)
would not be recognised as a gate at all — provenance would resolve perfectly and no gate would
be found to hold it to. Measured: **0** occurrences of `WFConditions` in
`tools/build_state_engine.py` and **0** multi-condition conditionals in either shipped fork, so
this is latent, not live. It is the same defect *shape* one layer over, and it is exactly what
a fourth iteration would find.

### R-3 — a reference expressed as anything but a `Type`-bearing descriptor. **Not seen.**

`_reference_descriptors()` matches on `Type: "Variable"` / `Type: "ActionOutput"`. A parameter
that names a variable as a raw string, or any future envelope without a `Type` key, is
invisible. Every reference the generator emits today goes through `variable()` / `output()` /
`token()` / `text_token()`, all of which carry `Type`.

### R-4 — static reads remain static (WR-21's own disclosure).

`called_names()` closes deletion and commenting-out. A guard call moved behind a never-taken
branch, or reached through an alias or `getattr`, still reads as present. Recorded in the
docstring rather than papered over; a runtime trace was again rejected because this file is
documented read-only and must never rebuild an artifact.

## Skipped Issues

None.

## Explicitly out of scope, and confirmed untouched

- **IN-05** (raise ordering in `verify_panic_escape_seed`) and **IN-06** (`None`-keyed
  provenance) — not in this pass's scope. IN-06's `_read_variable_keys()` half is closed
  incidentally by the rewrite (recorded above); its `_tested_variable()` half is not.
- The duplicate action `UUID` `792D1640-…` on both forks — `deferred-items.md`, separately
  tracked. Unchanged (byte-identical forks).
- Gate B's single waived line per fork — advisory, never blocking; re-measured as still exactly
  one per fork, at unchanged indices.
- `docs/retired_clause_check.py`'s 4 gitignored `.planning/graphs/` + `graphify-out/`
  occurrences — pre-existing, separately tracked, absent from a worktree checkout.
- Every finding below `# ARCHIVE — waves 1–6 review`.

## Device evidence

**None.** Everything above is **rung 1** — file-level analysis of the generators, the two built
plists and the checkers. The negative controls are builds of mutated generator copies and are
therefore still rung 1. No simulator and no phone was involved. `DIST-03` is open and nothing
here touches it.

---

_Fixed: 2026-08-18_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 3_
