---
phase: 16-dimming-and-silence-as-distinct-device-proven-circles
plan: 03
subsystem: shortcuts-generator
tags: [safety, D-01, brightness-floor, capture-restore, non-lexical-site, SAFE-01, SAFE-02, CIRC-05]
status: complete
requires:
  - "16-01: the capture is persisted to disk before the device is changed — the property this plan's replacement comment now states"
  - "16-02: CAP-08, setbrightness.WFBrightness is OPTIONAL and defaults to 50% — the basis of the C5 replacement assertion"
  - "16-CONTEXT.md D-01 (LOCKED) and its 2026-08-18 revision block"
provides:
  - "safety.brightness_floor = 0 and safety.dim_target = 0 in both shipped forks"
  - "a shipped dimming comment that states the capture-and-restore PROPERTY and asserts no bound"
  - "docs/environmental_restore_check.py: an at-or-above-0 dim-target assertion, reconciled with its own message, narrative comment and module docstring"
  - "docs/phase5_self_check.py: a WFBrightness-operand-present assertion derived from CAP-08, replacing the retired non-lexical value check"
affects:
  - "src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml rebuilt (0 action delta)"
  - "artifacts/shortcuts/MANIFEST.md still stale — docs/manifest_check.py RED by constraint D-MANIFEST until 16-06"
  - "plan 16-05's gate baseline: the record half of D-01 is untouched here, as required"
tech-stack:
  added: []
  patterns:
    - "citation-not-quotation for every supersession note"
    - "state the property, never a softer bound"
    - "locate by content, never by index"
    - "the non-lexical site is closed by reading, not by grepping"
key-files:
  created: []
  modified:
    - tools/build_state_engine.py
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - docs/environmental_restore_check.py
    - docs/phase5_self_check.py
decisions:
  - "The C5 replacement is CAP-08-derived: assert the WFBrightness operand is PRESENT, because an absent one silently applies an unrequested 50% with no capture"
  - "The dimming comment's first line is left byte-identical as the stable anchor for comment_index() and for the verify"
metrics:
  duration: ~35m
  completed: 2026-08-18
  tasks: 2
  commits: 2
  files: 5
requirements: [SAFE-01, SAFE-02, CIRC-05]
---

# Phase 16 Plan 03: The CODE half of D-01 — the floor and the target reach zero Summary

Both forks now ship a brightness floor of 0 and a dim target of 0, and the eleven-per-fork
user-visible comment actions that asserted a lower bound on the brightness write have been
replaced by a statement of the property the build actually guarantees — capture-and-restore.

## The six CODE sites and how each was handled

| Site | Carrier | Handling |
|---|---|---|
| **C1** | `src/PROSOCHE-Dumb.xml` Config literal, safety block | `brightness_floor` `0.10 → 0`, `dim_target` `0.12 → 0`. Located by content. The other two safety keys untouched. |
| **C2** | `docs/environmental_restore_check.py` dim-target assertion + its failure message | Relaxed `dim_target > 0` → `dim_target >= 0`; message rewritten so it and the assertion agree. |
| **C3** | the narrative comment above C2 | Rewritten: BD-02's Phase 9 addendum is now **settled on the main line** by D-01, not provisional and fork-scoped. |
| **C4** | that file's **module docstring** summary of C2 | Rewritten to describe what the checker asserts *after* this task. Relaxing C2 without this would have left a live false statement inside the guard. |
| **C5** | `docs/phase5_self_check.py` per-action brightness-parameter assertion | Replaced (see below). **The non-lexical site.** |
| **C6** | `tools/build_state_engine.py::dimming()`'s emitted Shortcuts `comment()` | Middle bullet rewritten to state the property; first line untouched; both forks rebuilt. **The only one of the six that ships.** |

## C6 — measured before/after counts of the retired clause

| Fork | Before | After |
|---|---:|---:|
| `src/PROSOCHE-Dumb.xml` | **11** | **0** |
| `src/PROSOCHE-Sentient.xml` | **11** | **0** |

Both measured with `grep -c`, not assumed. 11 matches the plan's 2026-08-17 measurement and
matches `primitive_dispatch()`'s eleven renderings per fork exactly. One generator string edit
removed 22 shipped comment actions' worth of a false safety claim.

The `silence()` half is **positively** asserted intact: `never increase it` still occurs
**11 times in each fork** after the rebuild.

### The rebuilt comment, verbatim from the built artifact

```
Dimming is reversible or message-only:
- Capture Current Brightness once when no snapshot exists.
- Do not brighten an already dim screen; the captured original is saved before any change and is always restored.
- Keep an existing unrestored snapshot unchanged.
```

Judge it against the two directions the plan gates:

- **Negatively** — it contains none of the bound vocabulary. No `zero`, no `floor`, no
  `10-15`, no `lower bound`, no `no lower than` / `not below` / `never below`, no
  `minimum value` / `minimum brightness`, no `safe band`. The replacement does not relocate
  the limit to a lower number; there is no limit in it at all.
- **Positively** — it names **both halves of the property**: the original *is captured*, and
  it *is always restored*, with the ordering (saved *before any change*) that plan 16-01 made
  structurally real. The half of the old bullet that was still true — do not brighten an
  already dim screen, which describes the already-dim arm — is retained verbatim.

The first line, `Dimming is reversible or message-only:`, is byte-identical. `comment_index()`
locates comments by prefix and the verify anchors on it; the rebuilt comment is found at
**exactly 11 renderings per fork**, confirming both the anchor and the dispatch count held.

## C5 — the site no grep could have found

`docs/phase5_self_check.py:117` asserted `params.get("WFBrightness") not in (0, "0", 0.0)` with
the message `"brightness may reach zero"`. It encoded the retired rule **as a value check
carrying none of the retired vocabulary** — measured 2026-08-18, a case-insensitive grep for
every retired phrase over that whole file returns **zero hits** while the line was live.

**This site was reachable only by reading the code, not by searching it.** Plan 16-05's
repo-scoped gate is structurally incapable of seeing it, and names it as its known blind spot
so a green gate is never mistaken for proof the class is empty.

It was **replaced, not removed**, with the honest version of what it was reaching for:

```python
require("WFBrightness" in params,
        "a Set Brightness action ships with no WFBrightness operand; an absent "
        "operand silently applies a default brightness with no captured "
        "original to restore (CAP-08)")
```

Why this and not deletion — the assertion is true, load-bearing, and pins a hazard nothing
else in `docs/` covers. Per **CAP-08** (plan 16-02, simulator-measured) `WFBrightness` is
**OPTIONAL**: an absent operand does *not* raise the unfilled-parameter error, it silently
applies an unrequested 50% with no capture behind it. Verified against both rebuilt forks:
15/15 `setbrightness` sites carry a `WFBrightness` operand, all of them variable descriptors.
The complementary direction — that a variable-fed operand is numerically gated so the cleared
sentinel or an empty read never reaches the write — is already enforced from the generator
side by `verify_restore_gates()`. Together they cover the write without either one re-imposing
a bound on its **value**. The full reasoning, including the blind-spot status, is recorded
inline at the site.

## `git diff` evidence

### Exactly one assertion relaxed in `docs/environmental_restore_check.py`

The only changed `require(...)` condition line in the whole file:

```
-    require(isinstance(dim_target, (int, float)) and dim_target > 0,
+    require(isinstance(dim_target, (int, float)) and dim_target >= 0,
```

The full diff is four regions and no more: the module docstring (C4), the narrative comment
(C3), that one condition, and that one message. The media-scoping assertion, the
allow-volume-increase assertion, `REQUIRED_SYMBOLS`, `EXPECTED_SITES`, `ALLOWED_DEVICE_DETAILS`
and the bootstrap-seed assertions are untouched.

### The at-or-above-floor assertion is byte-identical

```
     require(isinstance(floor, (int, float)) and dim_target >= floor,
```

It appears in the diff **only as unchanged context**. It was not edited.

**And it still holds — at equality.** With `brightness_floor == dim_target == 0`, `0 >= 0` is
true. This is the CIRC-05 boundary the plan names: at the threshold the floor **binds exactly
rather than never**, and one step below the floor stays unreachable because the target *is* the
floor. A floor of 0 under an unchanged target of 0.12 would have been inert; moving both is what
makes the correction observable.

### `silence()` is unchanged

`git diff 2ce0560..HEAD -- tools/build_state_engine.py` is **a single hunk at `def dimming():`**
— ten added Python comment lines and one changed emitted-comment bullet. `silence()` does not
appear in the diff at any hunk. Proved a second way by the verify's positive SAFE-02 check:
`never increase it` still occurs 11 times in each rebuilt fork.

## Verification

| Check | Result |
|---|---|
| `python3 tools/build_state_engine.py` | exit 0 |
| `python3 tools/build_sentient.py` | exit 0, `built src/PROSOCHE-Sentient.xml (67174d10…)` |
| Task 1 artifact script (both forks) | passed — floor 0, target 0, target ≥ floor at equality, 0 retired-clause occurrences, 11 dimming renderings, no bound vocabulary, both property words present, `allow_volume_increase` still `false` |
| `python3 docs/environmental_restore_check.py` | `environmental restore check: passed`, exit 0 |
| `python3 docs/phase5_self_check.py` | `phase5 self-check: passed`, exit 0 |
| `python3 docs/phase9_self_check.py` | exit 0 — `site_audit: passed (30/30 sites audited, 19 coerced, 11 correctly not)` |
| `python3 docs/state_engine_self_check.py` | exit 0 |
| Task 2 grep script | passed — C2 relaxed, C3/C4 reconciled, floor relationship untouched, C5 handled |
| **Gate A** `--target-macos 26 --target-platform all` | `Validation passed.` exit 0 on **both** forks |
| **Gate B** `--target-macos 27 --target-platform all` (advisory, chained into nothing) | exit 1 with **exactly the one permitted waived line** per fork — `WFCreateNoteInput` at index 4236 (Dumb) / 4304 (Sentient) |
| `python3 docs/manifest_check.py` | **RED as expected** (D-MANIFEST): `row 'Core source': MANIFEST declares 2901248 bytes, src/PROSOCHE-Dumb.xml is 2931030 bytes`. No MANIFEST row edited. |

### Counts: MEASURED non-movement

A `comment()` text edit and a JSON literal edit add and remove no action, so nothing should
move — and nothing did.

| Measure | Before (wave 1) | After |
|---|---:|---:|
| Dumb total actions | 4390 | **4390** |
| Sentient total actions | 4458 | **4458** |
| `setbrightness` / `setvolume` / `getdevicedetails` per fork | 15 / 15 / 22 | **15 / 15 / 22** |
| Gate B waived-line action index (Dumb / Sentient) | 4236 / 4304 | **4236 / 4304** |

**No number was edited in any checker**, so no derivation comment was owed. `EXPECTED_SITES`,
`expected_counts` and `expected_coerced` are untouched.

The XML diff across both forks is exactly six distinct lines and no others:

```
  22 -- Do not brighten an already dim screen and never set zero.
  22 +- Do not brighten an already dim screen; the captured original is saved before any change and is always restored.
   2 -    "dim_target": 0.12,
   2 -    "brightness_floor": 0.10,
   2 +    "dim_target": 0,
   2 +    "brightness_floor": 0,
```

## Citation, never quotation

Every supersession note this plan wrote — the narrative comment in
`environmental_restore_check.py`, its module docstring, the Python comment above `dimming()`'s
`comment()`, and the inline reasoning at the phase5 site — **cites where the retired clause
lived** (BD-02's original Decision paragraph in `docs/CAPABILITY-DECISIONS.md`, and the
canonical strategy's §21) and never reproduces its wording. A note that quotes what it
supersedes is itself a surviving occurrence, and plan 16-05's repo gate would report it.
The task-2 verify enforces this negatively: `strictly positive` no longer occurs anywhere in
`environmental_restore_check.py`, in any case, and `brightness may reach zero` no longer occurs
in `phase5_self_check.py`.

## Scope held

This plan carries the **CODE half only**. Nothing outside its five declared files was touched —
confirmed by `git status --short` being clean after each commit and by both commits' file lists.
Specifically **not** edited, all of them plan 16-05's or frozen:

- `src/CONFIG-BLOCK.md`, `docs/CAPABILITY-DECISIONS.md`, `docs/BUILD-NOTES.md`
- `.planning/REQUIREMENTS.md`, `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`
- `.claude/CLAUDE.md`
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` — **frozen by user decision**, a historical
  design input, never edited by any task in this phase
- `artifacts/shortcuts/MANIFEST.md` — D-MANIFEST, 16-06's

`STATE.md` and `ROADMAP.md` were not modified: this is a parallel worktree executor and the
orchestrator owns those writes.

## Threat mitigations applied

- **T-16-10** (DoS of device usability, high): mitigated as the threat register specifies —
  **not** by floor avoidance, which the evidence retired, but by capture-and-restore: the
  original is captured and persisted before the change (16-01) and restored by four independent
  triggers. The residual claim — that the practical minimum is dim rather than black — is a
  `backstop` truth, device-gated, and **is not asserted by this plan**.
- **T-16-11** (tampering with the environmental checker, high): exactly one assertion relaxed,
  proved by diff; the at-or-above-floor assertion byte-identical, proved by its absence from
  the diff.
- **T-16-12** (volume floor / Media scoping, high): untouched. `allow_volume_increase is False`
  and every `WFVolumeSetting == "Media"` are both still asserted by the environmental checker,
  which ran green in this plan's chain. `silence()`'s SAFE-02 comment additionally proved
  present 11× per fork.
- **T-16-13** (checkers and docstring disagreeing, medium): all four descriptions-of-assertions
  reconciled in one plan — the assertion, its message, its narrative comment, and the module
  docstring.
- **T-16-14** (spoofing a safety guarantee to the user, high): closed. 11 → 0 per fork, asserted
  against the **rebuilt** artifact, and the replacement is gated in both directions so the
  guarantee cannot be re-spoofed at a lower value.
- **T-16-15** (a green lexical gate mistaken for an empty class, medium): C5 fixed by hand with
  its blind-spot status recorded inline and in this summary.
- **T-16-SC** (low, accepted): no external package installed. Python usage is stdlib only
  (`plistlib`, `pathlib`, `json`, `sys`).

## Deviations from Plan

None. Both tasks executed exactly as written, no auto-fix rules were invoked, and no
architectural question arose. No file outside the plan's declared five was modified.

## Authentication Gates

None.

## Known Stubs

None. No stub, placeholder, TODO, skipped test or unrun `<verify>` was introduced. Both task
verify blocks were run in full and passed.

## Device-gated work NOT done here (recorded, not inferred)

This plan is entirely rung-1 (file-level) work and claims nothing about hardware. That a
brightness target of 0 renders as *dim rather than black or unusable* on a real iPhone is
SAFE-01's `backstop` truth — it rests on one unrepeated user report and is a device observation
this plan cannot make. It remains **BLOCKED on DIST-03**: paired device present,
`tunnelState: disconnected`, no live session to drive. It is 16-06's instrument to settle, and
per CAP-08 that instrument must observe the **value actually applied**, not merely the absence
of an error.

## Follow-up for later plans in this phase

- **16-05** owns the record half of D-01 and the repo-scoped gate. Its positive cross-check —
  that `src/CONFIG-BLOCK.md`'s fenced JSON and the built forks' Config literal agree on both
  keys — now has a settled right-hand side to check against: **both keys are 0.**
- **16-05**'s gate must carry its comment naming `docs/phase5_self_check.py`'s former line 117
  as the known non-lexical blind spot. That site is closed here, but the *class* it proves —
  rules encoded as value checks rather than sentences — is not lexically searchable.
- **16-06** re-signs and refreshes the six MANIFEST rows. `docs/manifest_check.py` stays RED
  until then; do not fix it by editing rows.

## Self-Check: PASSED

Files claimed modified, verified present on disk: `tools/build_state_engine.py`,
`src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`, `docs/environmental_restore_check.py`,
`docs/phase5_self_check.py`.

Commits claimed, verified in `git log`: `8e2a676` (task 1), `189d1c0` (task 2).

Build provenance guard verified before either generator ran:
`git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` → exit 0.
