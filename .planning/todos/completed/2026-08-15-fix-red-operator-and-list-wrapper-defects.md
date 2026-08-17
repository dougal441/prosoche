---
created: 2026-08-15T21:05:00.000Z
title: Fix the WFConditionalActionString red-operator sites and the WFItems List wrapper
area: general
severity: major
files:
  - tools/build_state_engine.py
  - .planning/debug/Donor 5.shortcut
---

## Problem

Two known, unresolved defect families were carried forward, unchanged, through every
cycle of the closed `open-routing-sequence-error` debug session because both sit past
breadcrumb J and could not affect that session's OPEN-path device measurement. Both are
now safe to pick up, since the OPEN path itself is device-confirmed working.

**1. 14 `WFConditionalActionString` sites (the "Donor 5" family).** A variable is placed
directly into a conditional's TEXT-slot operand as a template (`WFConditionalActionString
= token(...)`), the same general family as the already-fixed `WFInput.Variable`
envelope defect but a structurally different slot (text template vs. variable slot), so
the evidence that settled `WFInput.Variable` does not transfer. Zero golden-corpus
coverage, zero catalog coverage (`is.workflow.actions.conditional` is entirely absent
from the bundled ToolKit catalog), zero device coverage as of session close. `Donor 5`
was captured specifically to settle this and is on disk
(`.planning/debug/Donor 5.shortcut`) but was never analysed.

A concrete, previously-unexamined site name is now available: reviewing
`.planning/debug/Screenshot 2026-08-14 at 11.55.12⁠pm.png` during this closure (it was
never referenced anywhere in the debug session or examined before) shows an `If`
action testing `Previous Respected` `is` — rendered fully RED, including the operator
picker — which corresponds directly to `if_block("Previous Respected", 4, ...)` at
`tools/build_state_engine.py:649-650` and `:1069`. This is very likely one of the 14
already-catalogued sites, not a new class, but gives a concrete starting point instead
of an abstract count.

**2. The `WFItems` List wrapper (2 confirmed instances).** iOS wraps a variable-bearing
List row as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; this artifact's List
actions omit the wrapper, so rows render blank. The same screenshot reviewed above shows
this directly: a `List` action rendering nine consecutive rows, ALL as empty "Text"
placeholders instead of their configured content — direct, on-device visual confirmation
of the defect described in `HANDOFF.md` §6 item 4. The correct shape was already
recovered from Donors 4/4.1 (`.planning/debug/Donor 4.shortcut`,
`.planning/debug/Donor 4.1.shortcut`) but has not yet been applied to the generator.

## Solution

1. Decrypt `Donor 5.shortcut` (per `.claude/CLAUDE.md` §8's `aea decrypt` + `aa extract`
   recipe) and inspect its `WFConditionalActionString` operand shape directly — this is
   the missing device-ground-truth evidence this session's evidence hierarchy requires
   before touching any of the 14 sites.
2. Cross-check the recovered shape against the concrete site found this closure
   (`if_block("Previous Respected", 4, ...)`, `tools/build_state_engine.py:649-650`,
   `:1069`) before generalising to all 14 — confirm it is genuinely the same family, per
   this project's own "fix whole classes, never site-by-site" discipline, then run a
   full-codebase sweep for every `WFConditionalActionString`-with-token site (14
   expected) rather than patching sites individually.
3. Apply the `WFItems` wrapper shape recovered from Donors 4/4.1 to both known List
   sites (re-locate by content — line numbers shift on regeneration — starting from the
   `Previous Respected`-adjacent region shown in the reviewed screenshot as one
   candidate).
4. Add build-time recurrence guards for both fixes, following this session's own
   established pattern (guard runs before the single serialize/write; sensitivity
   verified by running it against a synthetically-reverted pre-fix artifact).
5. Fold both newly-confirmed axes into `.claude/CLAUDE.md` § Conventions' numbered axis
   list once fixed and device-confirmed — `HANDOFF.md` §9 already flags this as a
   candidate follow-up (folding cycle 15's `read_value()`/`get_value()` distinction and
   cycle 16's `pending_exit` container/leaf pattern into the same list); do all three
   documentation updates together rather than in separate passes.
6. Regenerate, validate, sign, decrypt-verify, then device-test specifically the Test
   Circle menu path and any screen reachable via the fixed conditionals (both sites are
   past breadcrumb J and were never exercised by the closed OPEN-path session).
7. Propagate to `tools/build_sentient.py` / Sentient once that fork is re-run (see the
   sibling Sentient re-fork todo) — check whether the Sentient-only `If [Audit Token]
   contains` red-render (`HANDOFF.md` §6 item 6) is the same family before treating it
   as a separate investigation.

## Related

- `.planning/debug/resolved/open-routing-sequence-error.md` — cycles 8–13's own
  investigation of this family (UI evidence via `IMG_5624.jpg`–`IMG_5646.jpg`, the
  `WFCoercionVariableAggrandizement` fix for the sibling numeric-operand class).
- `.planning/debug/HANDOFF.md` §6 items 4 and 5 — this todo's origin.
- `.planning/debug/Screenshot 2026-08-14 at 11.55.12⁠pm.png` — reviewed for the first
  time during this closure; shows both defects directly on-device.

## Closed — 2026-08-17, Phase 13 (`13-red-operator-conditionals-and-the-wfitems-list-wrapper`)

**Everything above this line is preserved verbatim as history. Several of its central claims
are REFUTED, and this block records which, why, and by what evidence — because in this project
an unrecorded refutation gets re-litigated the next cycle.** This block is written to be read
standalone, by someone who never opens Phase 13's planning directory.

### What this todo asked for, and what actually happened

| Solution step | Outcome |
|---|---|
| 1. Decrypt `Donor 5.shortcut` and inspect the operand shape | **Done as written.** Decrypted with the `.claude/CLAUDE.md` §8 recipe, first attempt, 196-line plist — the first analysis it ever received since landing on disk in cycle 14. |
| 2. Cross-check the recovered shape against the concrete site before generalising | **Done — and it INVERTED the conclusion.** See "The refutations" below. The cross-check is what proved there was nothing to sweep. |
| 3. Apply the `WFItems` wrapper to "both known List sites" | **Done by class, at a scale this todo did not know about.** One emitter fix, 66 actions and 660 rows per fork. |
| 4. Add build-time recurrence guards for both, sensitivity-demonstrated | **Done.** `verify_list_item_wrappers()` (new, armed on both forks at both touch points) and a positive Donor-5 pin inside `verify_conditional_action_string()`. Both demonstrated against synthetically reverted artifacts; both raise `SystemExit` before the single `SOURCE.write_bytes()`. |
| 5. Fold the axes into `.claude/CLAUDE.md`, all three doc updates in one pass | **Done as written.** The numbered axis list now runs 1–9: the `WFItems` row wrapper added as a **container** axis (explicitly *not* an instance of the string-envelope axis), the `read_value()`/`get_value()` compound-versus-scalar rule added beside it, and axis 7 extended with the `pending_exit` container/leaf pattern. |
| 6. Regenerate, validate, sign, decrypt-verify, then device-test | **Partly done, partly owned elsewhere.** Both forks rebuilt and gate-A clean. Signing, decrypt-verification and the MANIFEST refresh are owned by plan 13-04. Device testing is owned by Phase 19 UAT. |
| 7. Propagate to `tools/build_sentient.py` / Sentient | **Done — through the rebuild, not as separate work.** The Aware fork forks the *built* Core XML, so the emitter fix propagated automatically; only the guard arming needed touching, and it was done at both of `build_sentient.py`'s touch points. |

### The refutations

**1. "14 `WFConditionalActionString` sites" is ZERO.** Donor 5 shows iOS **itself** authoring
the exact construct this todo suspected of being a defect: a variable in a conditional's
TEXT-slot operand as a `WFTextTokenString` — a single `￼` string plus an `attachmentsByRange`
keyed `{0, 1}` holding a **bare** `{Type, VariableName}` dict — alongside a `WFInput` carrying
the **opposite** `WFTextTokenAttachment` envelope, with `WFCondition` as an integer and **no**
coercion aggrandizement on either side. The generator's `token()` helper emits a key-for-key
identical shape and always has. Measured per fork: **192 (Core) / 195 (Aware)** mode-0
conditionals carry the slot, **20 / 20** are variable-bearing (19 at condition 4, 1 at 99),
172 / 175 are raw literals, and **0 / 0** are defective. **Step 1 of the Solution was right to
demand the decrypt first; step 2's cross-check is what inverted the conclusion; and step 2's
proposed follow-through — "run a full-codebase sweep for every
`WFConditionalActionString`-with-token site (14 expected)" — was NOT performed, deliberately.
Performing it would have replaced a device-confirmed shape with a guess**, which this project's
do-not-fabricate rule forbids outright. The deliverable inverted from a repair into a *pin*: a
positive build-time assertion that the shape is still there, so a future pass reading a stale
record cannot "fix" 20 correct sites.

**2. "2 confirmed instances" of the `WFItems` wrapper is 66 actions and 660 rows, per fork.**
Direct `plistlib` measurement of both artifacts: 67 `is.workflow.actions.list` actions per fork,
of which **1** was correct and **66** were defective, carrying **660** unwrapped
variable-bearing rows. This todo's figure **under-counted actions by 33× and rows by 330×**.
All 66 originate from a single emitter, `mirror_text()`, unrolled across the Circle dispatch —
so the fix is one per-row type branch, not 66 edits. The six legitimate bare-string rows emitted
by `list_items()` were left bare: Donor 4 shows literal rows stay bare, and wrapping them would
have been an unforced regression.

**3. The named concrete site was a FALSE LEAD.** `if_block("Previous Respected", 4, ...)`
passes a **raw Python literal** (`string="true"` / `string="false"`), never a `token()`. It has
no variable in its text slot at all and is therefore **not a member of the family**. Its left
operand is genuinely Text-typed (`getvalueforkey` → `gettext` → `setvariable`), and a Text left
operand with condition 4 is the *valid* operator/operand pairing. `Previous Respected` is set at
action index 368 and all 44 uses occur at index 375 or later, so there is no dangling reference
either. This todo's own hedge — "This is *very likely* one of the 14 already-catalogued sites"
— was a guess, and measurement falsifies it. This is a **corrected attribution**, not a second
defect.

**4. The screenshot this todo cites DOES NOT EXIST.**
`.planning/debug/Screenshot 2026-08-14 at 11.55.12 pm.png` is absent from the worktree, absent
from the main checkout, and absent from git history — verified three ways. Its recorded filename
also carries a `U+2060` word joiner, so this is not a path-quoting problem. **Nothing was lost:**
both defects were established independently and more precisely without it, and no Phase 13 task
depended on reading it. The "nine consecutive blank rows" it was described as showing is
consistent with a 10-row List action viewed with one row scrolled off.

### What is still OPEN, and must not be written up as settled

- **The cause of the red operator observed on 2026-08-14.** Not reproducible at HEAD, the build
  is not retained, and the screenshot does not exist. Owned by Phase 19 device UAT, where a red
  chip would be a *new* finding with a live artifact to inspect.
- **Whether a pure-literal comparison target should be a `WFTextTokenString`.** No donor covers
  the pure-literal case. The 172 / 175 raw literals are device-proven working and were left
  untouched **and unasserted**. This is **unsettled by decision, not resolved** — settling it
  needs a rung-4 one-action donor with a literal comparison.
- **`WFItemType` values other than `0`.** Only text rows are donor-observed. Deliberately
  unaudited; the guard asserts the key's presence, never its value.
- **Whether wrapping changes what `getitemfromlist` returns.** Device-only; owned by Phase 19
  UAT, which must test a **re-imported** build — a user still running the previously signed
  artifact keeps the blank-row Mirror until they re-import.

### Where the durable record lives

`docs/BUILD-NOTES.md` §28 (the decrypts, the full measured inventory, the refutation, both
guards' verbatim `SystemExit` texts and the ordering mask, and the open assumptions);
`docs/CAPABILITY-DECISIONS.md` `BD-07` (the conditional operand, settled already-correct) and
`BD-08` (the `WFItems` row wrapper); `.claude/CLAUDE.md` § Conventions, axes 7, 8 and 9.
