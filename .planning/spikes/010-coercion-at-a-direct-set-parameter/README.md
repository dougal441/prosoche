---
spike: 010
name: coercion-at-a-direct-set-parameter
type: standard
validates: "Given a named-variable operand feeding a direct Set-action float parameter (`is.workflow.actions.setbrightness` / `WFBrightness`), when the operand carries `WFCoercionVariableAggrandizement` with `CoercionItemClass: WFNumberContentItem` — the shape the generator emits at all 15 brightness sites per fork — then determine whether that operand resolves as a Number in the Shortcuts editor and is consumed at run time, or renders degraded/red as an unusable operand"
verdict: PENDING
related: [007, 006, 001]
tags: [coercion, operand-types, setbrightness, setvolume, simulator, rung-2, probe, evidence-hierarchy]
---

# Spike 010: Coercion at a Direct Set-Action Parameter

## What This Validates

**One question, and only one:**

> Is `WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` correct at a
> **direct Set-action float parameter** (`setbrightness.WFBrightness`), as opposed to the
> **conditional-operand** position that Donor 4.1 already confirms?

Nothing else. Not whether the screen physically dims. Not whether `Get Device Details` returns a
real hardware brightness. Not whether the capture survives to disk. Those are different questions
on different rungs, and this probe is deliberately not aimed at any of them.

### Why the question is still open after research narrowed it

`16-RESEARCH.md` Finding 2 narrowed it considerably and did not close it:

- **Position-generality is now device-evidenced.** `Donor 7.1` action 7 carries a coercion at a
  **non-conditional, direct action parameter** (`getvariable.WFVariable`, `WFDateContentItem`),
  written by iOS on the target iPhone. The mechanism is demonstrably not conditional-only.
- **Named-variable descriptors are corpus-evidenced.** The golden corpus carries eight coerced
  `Type: Variable` descriptors across six parameter keys — the exact descriptor kind the generator
  emits at all 173 coerced sites.
- **What remains genuinely unwitnessed is one narrow pair:** `WFNumberContentItem` at a
  **float-typed system-control parameter**. `WFNumberContentItem` appears **nowhere** in the golden
  corpus; it rests entirely on Donors 4.1 / 6 / 6.1, all at conditional operands. No donor and no
  golden shortcut carries a coercion on `WFBrightness` or `WFVolume`.

Confidence is MEDIUM-HIGH. That does **not** license skipping the check. `.claude/CLAUDE.md`
`## Conventions` is explicit: **operator/operand type validity is invisible in the plist.** A
numeric operand on a text-typed value renders red in the UI, is structurally valid in the file, and
fails at runtime. No file-level analysis can detect it — not the validator, not the ToolKit catalog,
not decrypting the signed artifact.

**Gate B cannot help either.** `setbrightness` and `setvolume` are legacy `is.workflow.actions.*`
identifiers, absent from the v78 first-party parameter catalog, so gate B applies no unknown-key
check to them at all. A clean gate B is **not** evidence about these sites
(`16-RESEARCH.md` Finding 2, "Gate B cannot help here").

### Why this is a rung-2 question and not a device question

`.claude/CLAUDE.md` §9's governing rule: *never climb higher than the open question requires.* The
chip-render question needs the Shortcuts **editor**, which needs an **import** — and
`16-RESEARCH.md` Finding 3 measured that `xcrun simctl openurl "file://…"` renders the import sheet
on the booted simulator. Spike 007's recorded "the simulator cannot import a signed `.shortcut`"
was measured against the **MCP tool's scheme allowlist**, not against `simctl`, which it never
tried. Closing this at rung 2 keeps the scarce device session for the questions only hardware can
answer.

### What a pass and a fail each mean, and what each triggers

| Outcome | Meaning | Triggers |
|---|---|---|
| **Coerced leg renders normally, uncoerced control leg renders differently, run accepts the operand** | The shape is right at this position, as far as a simulator can establish it | Record VALIDATED-at-rung-2. The generator's emission is **unchanged** — this plan records a verdict, it does not act on it. Real-hardware environmental behaviour stays UNVERIFIED. |
| **Coerced leg renders red / degraded, or the run reports "Please choose a value for each parameter in this action."** | `WFNumberContentItem` is wrong at this position | **INVALIDATED. STOP.** This is the fresh-donor trigger. Follow `09-RESEARCH.md`'s fresh-donor protocol: build a donor on the device with a variable-fed Set Brightness and decrypt it. **Do NOT guess a second `CoercionItemClass`** — locked by `16-CONTEXT.md` and by `.claude/CLAUDE.md`'s do-not-fabricate rule. |
| **The import cannot be completed, or the editor cannot be reached** | Rung 2 does not reach this question after all | Record PARTIAL. Research assumption A5 is refuted; the chip gate returns to the device's plate and spike 007's rung-2 claim stands as written, with the new measurement recorded beside it. |

## How to Run

`PROSOCHE Coercion Probe.shortcut` (signed, in this folder; unsigned source and its build script in
`drafts/`). Fully standalone: it reads no `state.json`, references no production shortcut, and needs
no Personal Automation.

```bash
UDID=$(xcrun simctl list devices booted -j | python3 -c 'import json,sys;print(next(d["udid"] for v in json.load(sys.stdin)["devices"].values() for d in v))')
cp ".planning/spikes/010-coercion-at-a-direct-set-parameter/PROSOCHE Coercion Probe.shortcut" /tmp/coercion-probe.shortcut
xcrun simctl openurl "$UDID" "file:///tmp/coercion-probe.shortcut"   # → Shortcuts import sheet
xcrun simctl io "$UDID" screenshot /tmp/sim-import.png               # → shows "Add Shortcut"
# then one synthesized tap on "Add Shortcut" via the simulator-control tool
```

Four legs, each labelled on screen so an observer can attribute a failure to a specific leg:

| leg | what it holds | why |
|---|---|---|
| **A — COERCED** | `Text("0.42")` → `Set Variable "Probe Coerced Target"` → `Set Brightness` fed by that named variable **with** `WFCoercionVariableAggrandizement` / `WFNumberContentItem` as the **first** entry in `Aggrandizements` | the question under test — byte-identical to what `set_brightness(variable(...))` + `normalise_numeric_operands()` emit at all 15 production brightness sites |
| **B — UNCOERCED (control)** | the identical chain **without** the aggrandizement | so leg A is read against a **reference** rather than against expectation. Without B, "the chip looked fine" is an unfalsifiable claim |
| **C — READ** | `Get Device Details "Current Brightness"` → `Show Result` | makes the read's presence and apparent type observable. `Current Brightness` is **donor-confirmed** (spike 001, Donor 10) — not an invented literal |
| **D — RESTORE** | `Set Brightness` fed by leg C's captured value | running the probe cannot strand the display. Ordering, not detection — Shortcuts has no try/catch |

Every identifier and literal in the probe is already evidenced by this project. **No unevidenced
literal appears anywhere in it.** A probe that fails for a reason unrelated to the question it was
built to answer burns the round trip and teaches nothing, and this project has already lost cycles
to exactly that.

**Inspect the editor before running it.** The chip render is the primary observation; the run is the
secondary one. Both are recorded.

## What to Expect

**Expected, on the evidence:** leg A's chip renders normally. Donor 7.1 puts a coercion at a direct
action parameter on real hardware, and the golden corpus puts eight of them on named-variable
descriptors. The expected outcome shifted toward "not red" when Finding 2 landed. **That is a
prediction, not a result** — it is written down here precisely so a confirming observation cannot be
mistaken for a foregone conclusion, and so a refuting one is unmissable.

**Unknown, and genuinely so:** what leg B looks like. There is no prior observation of an
*uncoerced* float system-control operand in the editor. It may render red, or plainly, or
identically to leg A — and "identically to leg A" would be its own finding, because it would mean
the chip render does not discriminate and the run is the only signal that counts.

**Explicitly out of reach at rung 2** — `.claude/CLAUDE.md` §9's "Rung 2's ceiling", which this
probe does not and cannot breach:

- **Real-hardware environmental behaviour.** Whether the screen physically dims and un-dims, and
  what `WFBrightness = 0.0` actually looks like. A simulator observation is **never above
  `UNVERIFIED`** for anything on that list.
- **Whether `Get Device Details → Current Brightness` returns a usable, correctly typed value on
  real hardware.** A simulator reading is informative for probe design and is **not promotable**.
- **Personal Automation triggers**, the Control Room Note path (`com.apple.mobilenotes` is absent
  from the simulator), and Apple Intelligence. None are touched by this probe.

## Investigation Trail

### Build (2026-08-18)

`drafts/build_coercion_probe.py` emits the plist; `drafts/assert_probe_shape.py` proves the built
XML actually carries the shape under test. Both are re-runnable and both live in this spike, not in
`docs/` — this plan touches no checker.

**Deviation from CONVENTIONS.md, recorded — the plist was authored directly rather than by
dispatching `shortcuts-playground:shortcut-builder`.** Justification, and it is the same exception
CONVENTIONS.md already grants and spike 007 already used: *"when a donor already gives the exact
byte shape and the spike's purpose is to vary it deliberately, author the plist directly — an agent
will tend to 'correct' the very values under test."* **Leg B is an operand deliberately missing its
coercion.** That absence is the control. An agent that "fixed" it would leave the probe structurally
valid, still signable, still importable — and silently unable to discriminate, because leg A would
have nothing to be read against. The shape is not guessed either: every byte is transcribed from
`tools/build_state_engine.py` (`variable()` :140, `set_var()` :244, `device_detail()` :441,
`set_brightness()` :448, `NUMBER_COERCION` :3755, `normalise_numeric_operands()` :3912), which is
read-only use — this plan modifies nothing under `tools/`.

**Leg A is not an approximation of the production shape; it is that shape.** The generator's own
docstring at `:500` describes `restore_managed_settings()`'s
`set_brightness(variable("Restore Brightness"))`: *"The operand is gettext-fed, so
`normalise_numeric_operands()` attaches Donor 4.1's `WFCoercionVariableAggrandizement`
automatically."* Leg A is a Get Text → Set Variable → Set Brightness chain with the coercion
attached first — the same wiring at the same position, on the highest-stakes production site there
is (the restore leg, the one the whole safety property rests on). The Text source is load-bearing:
a `number()`-fed operand is already Number-typed, `normalise_numeric_operands()` would skip it, and
a probe built that way would test nothing at all.

**Two validator rules shaped the comment text, neither of them anticipated.** `validate_shortcut.py`
requires a two-comment preamble whose second comment carries the literal Playground prompt block
(`:2552-2569`), and separately **rejects internal parameter names anywhere in comment text**,
demanding Shortcuts UI wording. So the on-device comments name actions the way the editor shows them
("the Number coercion", "Set Brightness") and the exact plist keys live here and in the build
script's docstrings — which is where a reader who needs them is looking anyway. Both corrections
were made before signing; neither changed a single action parameter.

### Ordering: capture runs first, and that is a safety property

The four legs the plan specifies are all present, sequenced **C → A → B → D**. The device read runs
**before** either write. Reading after the writes would capture `0.42` — the probe's own test value —
so the "restore" leg would restore the probe's mistake rather than the user's original. Shortcuts has
no try/catch, so safety here comes from ordering rather than detection (CONVENTIONS.md; research
Pattern 1, *capture → persist → apply*). This is the same rule the product itself is being fixed to
obey.

Leg A writes `0.42` and leg B writes `0.66` — **deliberately different literals**. A shared value
would make "the uncoerced leg silently no-opped" and "both legs worked" indistinguishable on screen,
which is precisely the discrimination the control leg exists to provide. Both are mid-range and safe;
neither darkens the display.

### Gates

**Gate A — mandatory, passed clean:**

```
$ validate-shortcut "drafts/PROSOCHE Coercion Probe.xml" --target-macos 26 --target-platform all
Validation passed.
exit=0
```

**Gate B — advisory, recorded verbatim, chained into nothing:**

```
$ validate-shortcut "drafts/PROSOCHE Coercion Probe.xml" --target-macos 27 --target-platform all
Validation passed.
exit=0
```

Gate B exits **0** here, which is not the per-fork norm and is worth stating so nobody reads it as a
stronger result than it is. The project's permanent gate-B waiver is a **Notes** waiver
(`WFCreateNoteInput` on `com.apple.mobilenotes.SharingExtension`); this probe contains no Notes
action, so there is nothing for it to waive. **A clean gate B is still not evidence about this
probe's question.** `setbrightness` is a legacy `is.workflow.actions.*` identifier, absent from the
v78 first-party parameter catalog, so gate B applies no unknown-key check to it at all
(`16-RESEARCH.md` Finding 2, "Gate B cannot help here"). Gate B passing means the probe contains no
*catalogued* parameter error. It says nothing whatsoever about the coercion.

### Shape assertion, from the built XML

`drafts/assert_probe_shape.py` parses the built plist — not the build script, not the diff — and
asserts: three Set Brightness sites; leg A's coercion **first** in `Aggrandizements` with class
`WFNumberContentItem`; leg B bare; leg D bare (correctly, since Get Device Details is already
Number-typed and the generator skips such operands); both test operands Get-Text-sourced; and no
reference to `state.json`, either production fork display name, or any automation input. It also
fails if **any** `CoercionItemClass` other than `WFNumberContentItem` appears anywhere — a mechanical
guard on the one prohibition this spike must not violate.

```
probe shape asserted from the built XML (20 actions):
  leg A  coerced   -- WFCoercionVariableAggrandizement/WFNumberContentItem, FIRST in Aggrandizements
  leg B  control   -- bare descriptor, no Aggrandizements
  leg D  restore   -- bare descriptor (Get Device Details is already Number-typed)
  both test operands are Get Text -> Set Variable sourced
  no reference to the state file, either production fork, or any automation input
```

### Signed artifact

`PROSOCHE Coercion Probe.shortcut` — **23,990 bytes**, first four bytes `AEA1`. Filename equals the
display name exactly, no suffix, per the signing-name discipline. ASCII-only by design so the
`simctl openurl file://` path needs no escaping. Timestamped pre-sign archive under `2026-08-18/`.

## Results

*(filled in during task 2 — verdict, screenshots, and the disposition of the 11 uncoerced
`setvolume` sites)*
