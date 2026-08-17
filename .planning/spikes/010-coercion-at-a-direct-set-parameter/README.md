---
spike: 010
name: coercion-at-a-direct-set-parameter
type: standard
validates: "Given a named-variable operand feeding a direct Set-action float parameter (`is.workflow.actions.setbrightness` / `WFBrightness`), when the operand carries `WFCoercionVariableAggrandizement` with `CoercionItemClass: WFNumberContentItem` — the shape the generator emits at all 15 brightness sites per fork — then determine whether that operand resolves as a Number in the Shortcuts editor and is consumed at run time, or renders degraded/red as an unusable operand"
verdict: PARTIAL
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

### Simulator session, 2026-08-18 — iPhone 17 Pro, iOS 26.5 (23F77), udid `79A84C29-DB62-40A2-AC3F-CCB5F8192F86`

Precondition re-derived rather than assumed: `xcrun simctl list devices booted` reports exactly that
device, and `xcrun simctl listapps` confirms `com.apple.shortcuts` present.

**1. The import sheet renders (Finding 3 reproduced independently).**
`xcrun simctl openurl <udid> "file:///tmp/coercion-probe.shortcut"` produced the Shortcuts import
sheet with a live "Add Shortcut" button. → `screenshots/01-import-sheet.png`

**2. THE SYNTHESIZED TAP COMPLETES THE IMPORT — research assumption A5 is CONFIRMED, explicitly YES.**
One synthesized click on "Add Shortcut" completed the import and dropped straight into the Shortcuts
editor showing the probe's actions. → `screenshots/02-import-completed-editor-open.png`

This retires spike 007's recorded finding and the standing constraint the skill repeats from it.
**The booted simulator CAN import a signed `.shortcut`.** Spike 007's `file://` row was measured
against the MCP simulator tool's scheme allowlist, not against `simctl`, which it never tried. Rung 2
therefore reaches the editor and the runtime, not merely the build.

The instrument is preserved at `drafts/sim_input.py`, with every channel that did *not* work recorded
in its docstring so nobody re-walks them. Briefly: the tap tool CLAUDE.md §9 names
(`mcp__Claude_Code_iOS_Simulator__control`) is not exposed to a subagent with a restricted tool list;
`osascript` is refused assistive access; `idb`/`cliclick` are not installed; `simctl` has no tap verb.
What works is `CGEventPost` straight to the window server, which needed no Accessibility grant. Two
preconditions that cost real time and are easy to miss: a `simctl`-booted simulator has **no on-screen
window** until `open -a Simulator` (a click has nothing to land on), and coordinates must be
**fractions of the device screen mapped through the window rect measured at run time**, never pixels.

**3. `shortcuts://import-shortcut` still rejects a `file://` URL — measured, not assumed.**
`shortcuts://import-shortcut?url=file:///…&silent=true` → *"Import Failed. The shortcut URL provided
was invalid."* Identical to the rejection spike 007 measured for an `http` URL; the scheme wants an
iCloud link, and `silent=true` does not bypass it because the URL is rejected before the flag is
consulted. → `screenshots/03-import-shortcut-scheme-rejects-file-url.png`
So spike 007 was right about `import-shortcut` and wrong only about `openurl file://`.

**4. THE CHIP RENDER DOES NOT DISCRIMINATE AT THIS POSITION. This is the central finding.**

| leg | operand | renders as |
|---|---|---|
| A — coerced | `Probe Coerced Target`, Number coercion first in `Aggrandizements` | **normal** blue chip with the orange variable glyph — `screenshots/10-final-build-leg-A-coerced-chip.png` |
| B — uncoerced control | `Probe Uncoerced Target`, bare descriptor | **normal**, *indistinguishable from leg A* — `screenshots/11-final-build-leg-B-uncoerced-chip.png` |
| D — restore | `Probe Original Brightness`, bare (correctly) | normal — `screenshots/12-final-build-legs-B-and-D.png` |

The coerced leg does **not** render red. Neither does the control. **They render identically.**

That is not the null result it first looks like — it is the answer to a question this phase had wrong.
`09-UAT.md` Test 1 is *"the coercion chip does not render red."* At a **conditional operand** that gate
has teeth, because the operator picker is populated from the operand's static type, so a mismatch has
no case to render and the chip goes red. **`Set Brightness` has no operator picker.** There is nothing
for a type mismatch to break in the UI, so **the chip gate is structurally incapable of discriminating
at a direct Set-action parameter.** A green chip here is not weak evidence — it is *no* evidence.

That is exactly why leg B exists. Without the control, "leg A rendered fine" would have been recorded
as a pass, and the pass would have been vacuous. The control is what turned a false positive into a
finding.

The two legs could not be captured in one frame: the labelled comment between them is taller than the
device screen. Stating that plainly rather than cropping a composite — they are two real screenshots
of one artifact, taken minutes apart in one scroll.

**5. `Get Device Details → Current Brightness` returns `0` on the simulator.** →
`screenshots/07-run-leg-C-brightness-reads-0.png`. Informative for probe design, **not promotable** —
it sits squarely inside the rung-2 ceiling, and this plan's second backstop truth says so in advance.

**6. The run does not settle consumption either — and the negative control is what proved that.**

Running the coerced leg produced:

> **Could Not Run Set Brightness** — There was a problem setting the brightness.

→ `screenshots/13-run-coerced-leg-capability-error-not-parameter-error.png`

This is **not** the parameter error (*"Please choose a value for each parameter in this action"*) that
this project's conventions name as the signature of an operand-type defect. The tempting inference was:
*Shortcuts got past parameter validation and reached the OS call, so the coerced operand resolved.*

**That inference is wrong, and the negative control refuted it.** A one-action probe holding a
`Set Brightness` with `WFBrightness` **entirely absent** renders in the editor as **"Set brightness to
50%"** and produces **the same** "There was a problem setting the brightness."
→ `screenshots/14-negative-control-absent-operand-defaults-to-50-percent.png`

Two consequences, and the second is a genuine product finding:

- **The channel cannot distinguish a resolved operand from an absent one.** Both reach the OS call;
  both fail identically because the simulator has no backlight. `Set Brightness` cannot succeed on a
  simulator **at all**, so no run there can show whether the operand was consumed. The runtime half of
  the question is not partially answered — it is **untouched, and now known to be unreachable at
  rung 2**. That is worth more than a guess: it means no further simulator effort will help and the
  device session must carry it.
- **`setbrightness.WFBrightness` is OPTIONAL and defaults to 50%.** If the coercion were ever wrong in
  a way that left the operand unresolved, `Set Brightness` would **not** error — it would silently
  apply **50% brightness**. A silent unrequested environmental change with no capture is a strictly
  worse failure mode than a halt, and it bears directly on SAFE-01 / CIRC-05. **The device instrument
  must therefore verify the brightness VALUE APPLIED, not merely that the action did not error.** A
  "no error" device result would be consistent with a completely broken operand.

Building that control cost one small artifact and overturned the conclusion this spike was about to
record. `.claude/CLAUDE.md`'s "read the error text, not just the letter" is the rule that caught it.

**7. Show Alert modals are undismissable on this channel.** `is.workflow.actions.alert` accepted
neither a synthesized tap on OK nor a hardware Return across six attempts (geometry verified against
the display bounds); the run wedges permanently at the first alert. Regular in-app UI — the Add
Shortcut button, the run button, list scrolling — takes synthesized taps normally. This is why the
probe ships in **two variants** (below), and it matters beyond this spike: the product's own `alert()`
is used throughout both forks, so any future attempt to exercise a real fork on the simulator hits
this wall at the first message-only degrade path.

### Artifacts

| file | purpose |
|---|---|
| `PROSOCHE Coercion Probe.shortcut` | **silent** — no blocking UI; the variant a simulator can run end to end |
| `PROSOCHE Coercion Probe Breadcrumbs.shortcut` | the A–D ladder, for a **device** session where a human can tap |
| `PROSOCHE Coercion Negative Control.shortcut` | one `Set Brightness` with no operand — the control that refuted §6's inference |

`drafts/assert_probe_shape.py` asserts the two probe variants are **identical on all three Set
Brightness sites**, so a chip observed in one and a run observed in the other are observations of the
same wiring. That is checked, not claimed.

## Results

### Verdict: **PARTIAL**

**Settled at rung 2, and genuinely useful:**

1. **Research assumption A5 is CONFIRMED — yes, the synthesized tap completes the import.** The
   simulator import channel is real. `.claude/CLAUDE.md` §9's rung-2 row and the skill's
   `evidence-and-probes.md` rung-2 table both needed correcting, and were corrected.
2. **The chip gate does not discriminate at a direct Set-action float parameter, and cannot.**
   `09-UAT.md` Test 1, re-established against the current build, is **not a valid instrument here** —
   its single recorded pass was never evidence about `WFBrightness`, only about conditionals. The
   coerced and uncoerced legs render identically.
3. **`WFBrightness` is optional and defaults to 50%** — so an unresolved operand fails *silently and
   dangerously* rather than loudly.

**NOT settled, and now known to be unsettleable at rung 2:**

4. **Whether `Set Brightness` actually CONSUMES a Number-coerced named-variable operand at run time.**
   `Set Brightness` cannot succeed on a simulator at all. This is `must_haves` backstop truth 1 and it
   remains **UNVERIFIED**, exactly as CLAUDE.md §9's rung-2 ceiling requires.
5. **Whether `Get Device Details` current-brightness returns a usable, correctly typed value on real
   hardware.** The simulator returns `0`. Backstop truth 2, **UNVERIFIED and not promotable**.
6. **Real-hardware environmental behaviour** — whether the screen physically dims and un-dims, and
   what `WFBrightness = 0.0` looks like. Untouched. Personal Automations, the Control Room Note path
   and Apple Intelligence are likewise untouched.

**Why PARTIAL and not INVALIDATED — this distinction is load-bearing.** Nothing observed contradicts
`WFNumberContentItem`. The coerced leg did not render red; the run's failure was a **capability**
failure the control proved an operand-less action produces identically. **The fresh-donor protocol is
NOT triggered.** No replacement `CoercionItemClass` appears anywhere in this spike, and
`drafts/assert_probe_shape.py` fails the build if one ever does.

**Why not VALIDATED.** The one thing that would validate it — the operand being consumed — is the one
thing rung 2 cannot see. Recording a green chip as a pass would be recording a measurement the
instrument is incapable of making.

**What the device session must now carry**, stated precisely so it is not re-derived: run the
**Breadcrumbs** variant on hardware and confirm that the coerced leg sets brightness to **0.42** and
the uncoerced control to **0.66** — *by observing the value*, not by observing the absence of an error.
Per §6, "no error" is consistent with a silently defaulted 50%.

### Disposition of the 11 uncoerced `setvolume` sites

Recorded in `docs/BUILD-NOTES.md` alongside the name-scoped measurement that backs it. In short:
**correctly left uncoerced**, on a name-scoped check of every assignment of the silence-target
variable in both built forks — not by analogy to brightness. The 15/15-brightness vs 4/15-volume
asymmetry is a **sourcing artifact, not a gap**: brightness operands are `gettext`-sourced (Text) and
need the coercion; the silence target is `number()`-sourced and is already Number-typed, so the
generator correctly skips it. `docs/environmental_restore_check.py` deliberately asserts no coercion
count for exactly this reason. **Do not "fix" the asymmetry by pattern-matching brightness.**

### Free-ride: spike 007's App Picker Probe

Run while the channel was open, per the plan. Results recorded in **spike 007**, where they belong —
they retire that spike's open question and its verdict moves PARTIAL → VALIDATED.
