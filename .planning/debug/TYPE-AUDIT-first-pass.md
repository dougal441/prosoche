# TYPE AUDIT — first pass (session-manager, build `2026-08-14k`, Dumb fork)

Responds to the user's generalisation: *"it looks like a lot of these issues might stem from Type
being wrong in many places... check Types across the board."*

**The rule under test:** every parameter whose declared type is not text, when fed by a variable
reference, requires an explicit `WFCoercionVariableAggrandizement` with the right
`CoercionItemClass`. A bare text template validates, imports, and fails at runtime.

## ⚠ KNOWN LIMITATION OF THIS PASS — read before using the numbers

The classifier inspected the **top-level** parameter shape only. It did **not** descend into the
nested `{"Type":"Variable","Variable":{...}}` wrapper used by conditional `WFInput`. Evidence it
is under-reporting: the "fully coerced" set came back **empty**, yet build `i` demonstrably
added 20 coercions to conditional operands and they are present in the artifact.

**So `coerced=0` in the table below means "none found at the top level", NOT "none exist".**
The BARE counts are still meaningful for parameters that use the flat shape — which includes
every date parameter below. A second pass must handle the nested shape before any fix is scoped.

## Confirmed bare — date family (matches the device error exactly)

| action | parameter | bare | sites |
|---|---|---|---|
| `gettimebetweendates` | `WFInput` | 5 | 15, 292, 317, 334, 490 |
| `gettimebetweendates` | `WFTimeUntilFromDate` | 5 | 15, 292, 317, 334, 490 |
| `adjustdate` | `WFDate` | 1 | 17 |
| `format.date` | `WFDate` | 1 | 19 |
| `format.date` | `WFDateFormatString` | 1 | 19 |

Action **292 is in span D→E (286–306)** — exactly where build `k` stopped with *"couldn't convert
from Text to Date"*. Independent confirmation of the coordinator's static finding.

## Ranked candidates — highest risk first

**RANK 1 — date parameters (5 actions, 13 sites).** Device-confirmed failing. Needs the Date
equivalent of `WFNumberContentItem`. **Do not guess the class** — CAP-06 requires donor or corpus
evidence. One donor covering Format Date + Adjust Date + Get Time Between Dates settles all three.

**RANK 2 — numeric parameters on non-conditional actions.** `math.WFInput` (42) /
`math.WFMathOperand` (28), `round.WFInput` (3), `getitemfromlist.WFItemIndex` (31),
`conditional.WFNumberValue` (30), `calculateexpression.Input` (2), `count.WFInput` (1). The
build-`i` fix coerced conditional *left operands* only. These are the same type question on
different targets. `math` sites at 275/319/323/325 are on the OPEN Heat path.

**RANK 3 — `setbrightness.WFBrightness` (14) / `setvolume.WFVolume` (14).** Numeric-typed, bare.
**Moot if the brightness/volume cut proceeds** — resolve by deletion, not coercion.

**RANK 4 — entity/file/dictionary references.** `appendnote.entity` (2), `shownote.target` (1),
`documentpicker.save.WFInput` (28), `setitemname.WFInput` (28), `detect.dictionary.WFInput` (21),
`setvalueforkey.WFDictionary` (147), `choosefromlist.WFInput` (1), `repeat.each.WFInput` (10).
Entirely unchecked. `shownote.target` is a live suspect for the Control Room note-picker fault —
if the target is not a resolved note entity, iOS may fall back to prompting.

**RANK 5 — text-typed, expected bare, listed for completeness.** `setvariable.WFInput` (692),
`gettext.WFTextActionText` (231), `getvalueforkey.WFInput` (222), `alert.WFAlertActionMessage`
(22), `speaktext.WFText` (10). These *should* be bare. Useful as the control group.

**RANK 6 — low priority, already known.** `conditional.WFConditionalActionString` (14 — Donor 5,
right-hand operands, picker driven by left input, may be residual); the `List`/`WFItems` wrapper.

## Donor requests

- **DONOR 7 — dates.** Build: Date → Format Date (custom pattern) → Adjust Date → Get Time
  Between Dates, each fed from a *variable*, not a literal. Settles the Date `CoercionItemClass`
  and the `WFDateFormat` vs `WFDateFormatStyle` vs `WFDateFormatString` question (action 19
  carries the literal word `Custom` where a UTS#35 pattern belongs).
- **DONOR 8 — entity/file refs.** Build: Find Notes → Show Note, and Set Name → Save File, fed
  from variables. Settles RANK 4 and probably the Control Room note-picker fault.

Two donors plausibly close RANK 1 and RANK 4 together.
