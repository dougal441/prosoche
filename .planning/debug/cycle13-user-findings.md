# Cycle 13 — device findings from build `k`, plus a generalised TYPE hypothesis

Recorded by the orchestrator while the debugger was session-limited. Static claims below
were verified directly against `src/PROSOCHE-Dumb.xml`; device claims are the user's
verbatim observations. The debugger should **verify rather than trust** and may overrule
with fuller context.

## 1. Build `k` reached letter D — first time past C

Verbatim: *"I just ran build k and got to letter D! and then hit the new conversion error
'get time between dates failed because shortcuts couldn't convert from Text to Date'"*

Notification text (`IMG_5639.jpg`):

> "When any of 3 apps are opened" encountered an error: Conversion Error
> Get Time Between Dates failed because Shortcuts couldn't convert from Text to Date.

**The cycle-12 fix worked.** The `settings_snapshot` reads at 177/196 now pass; execution
crossed D=286 and failed in the D→E span. The predicted outcome was "C with a different
error" — the actual result is strictly better than predicted.

**No screen darkening was reported**, so the numeric restore gates held.

## 2. ROOT CAUSE of the conversion error — VERIFIED STATICALLY

All five `is.workflow.actions.gettimebetweendates` actions pass **text templates** into
date-typed parameters, with **zero coercion aggrandizements**:

| action | WFInput | WFTimeUntilFromDate |
|---|---|---|
| 15 | `TEXT-TEMPLATE '￼'` | `TEXT-TEMPLATE '￼'` |
| 292 | `TEXT-TEMPLATE '￼'` | `TEXT-TEMPLATE '￼'` |
| 317 | `TEXT-TEMPLATE '￼'` | `TEXT-TEMPLATE '￼'` |
| 334 | `TEXT-TEMPLATE '￼'` | `TEXT-TEMPLATE '￼'` |
| 490 | `TEXT-TEMPLATE '￼'` | `TEXT-TEMPLATE '￼'` |

Action 292 sits in D→E (286–306) — the span where execution now stops.

This is **the same defect class as the numeric-operand axis (axis 6)**, on a different
target type. Axis 6 was fixed by attaching
`WFCoercionVariableAggrandizement / CoercionItemClass = WFNumberContentItem` to variable
references feeding numeric comparisons. Date-typed parameters need the equivalent
(`WFDateContentItem` or whatever the donor establishes) and never received it, because
the axis-6 sweep was scoped to numeric conditionals only.

## 3. The user's generalisation — TYPE IS WRONG IN MANY PLACES

Verbatim: *"it looks like a lot of these issues might stem from Type being wrong in many
places. can you note to check Types across the board are as they should be. for example
you've got Formatted Date as Type Text, not as Type Date."*

**This is correct and it is the highest-value item in this document.** Axis 6 was applied
only where a numeric comparison forced the issue. The general rule is broader:

> **Every parameter whose declared type is not text, when fed by a variable reference,
> requires an explicit coercion aggrandizement. A bare text template validates, imports,
> and fails at runtime — silently or with a conversion error.**

Required work: enumerate **every** parameter in both forks whose catalog type is not a
string/text type, check whether it is fed by a variable reference, and confirm the
reference carries the correct `CoercionItemClass`. Date is confirmed broken. Others to
check include (non-exhaustive): dates, numbers, booleans, files, dictionaries, app/entity
references, quantity fields.

Do not fix by guessing the coercion class per type — establish each from donor evidence or
corpus, per CAP-06. One donor can likely cover several types at once.

## 4. Second confirmed type defect — `format.date` action 19

Verbatim: *"Or you've Format a Date as Date Format Custom, then Format String entered
'Custom'."*

Verified — action 19 carries **both** of these:

```
WFDateFormatStyle  = 'Custom'
WFDateFormat       = 'Custom'      <- the literal word, not a UTS#35 pattern
WFDateFormatString = TEXT-TEMPLATE '￼'
WFDate             = TEXT-TEMPLATE '￼'
```

Two problems:
1. `WFDateFormat = 'Custom'` holds the literal string `Custom` where a format pattern
   belongs. The UI renders it as the Format String, which is exactly what the user saw.
   `DATE_TIME.md` documents the custom pattern belonging in `WFDateFormatString`.
   Establish which key iOS actually reads and remove or correct the other.
2. `WFDate` is a text template with no coercion — same defect as §2.

`IMG_5641.jpg` / `IMG_5642.jpg` show the Date Format and Time Format pickers
(None/Short/Medium/Long/RFC 2822/ISO 8601/Relative/How Long Ago/Custom), confirming
`Custom` is a legitimate *style* enum case — so the style value is fine; the pattern field
is the defect.

`IMG_5640.jpg` shows a correctly-typed variable for contrast: `Time Between Dates` with
**Type: Date** selected, Date Format Medium / Time Format Short. That is what a
correctly-coerced date reference looks like in the UI.

## 5. Scaffolding still present — should be removed

Verbatim: *"am I meant to still be getting this input key:[] empty ref:[] ? we don't need
that anymore."*

Correct — `ROUTER_TRACE` has served its purpose. The router restructure is device-verified
and the trace is now pure noise on every manual run. Set `ROUTER_TRACE = False`. Keep
`BUILD_STAMP` (still needed to confirm which build is installed) and `OPEN_BISECT` (still
localising defects) for now.

## 6. Control Room UX defect — genuine, and user-facing

Verbatim: *"in the manual arm, when we click menu and open control room, I get a menu of
list of all my notes, then if I click the control room note I get an open text box, which
if I enter words into, this appends to the bottom of the control room note. weird
behaviour and this will confuse people."*

Two distinct faults in one flow:
1. **A note picker is shown instead of opening the Control Room note directly.** The
   shortcut should resolve the note itself (Find Notes filtered by name, per the design)
   and open it — the user should never choose from all their notes.
2. **An editable text box appears and its content is appended to the note.** Opening the
   Control Room should be read-only. An append-on-open path is a data-integrity risk as
   well as confusing: a stray tap writes into the ledger.

This is on the MANUAL arm, so it does not block OPEN, but it is squarely an MVP concern —
the Control Room is the user's primary surface.

## 7. Further screenshots — lower confidence, worth checking

- `IMG_5644.jpg` — `If [Audit Token] contains` with the operator rendered **red**.
  Condition 99 (`contains`) on an operand whose type does not offer it. Same axis-5 class
  (operator/operand-type validity) as the numeric operators, on a string operator this
  time. Needs the same treatment: establish the operand's type and coerce or change the
  condition.
- `IMG_5645.jpg` — another **10-row empty `List`**, in the Mirror templates section
  ("Mirror selects from 30 fact-gated, local templates"). Consistent with the known
  `WFItems` wrapper defect: iOS wraps variable-bearing rows as
  `{"WFItemType": 0, "WFValue": <WFTextTokenString>}` and ours omits the wrapper. This is
  a second instance, so the fix is a class fix, not a single site.
- `Screenshot 2026-08-14 at 11.55.12 pm.png` — not yet examined.

## 8. Status of the three original symptoms

| symptom | status |
|---|---|
| 2 — `sequence` / Set Dictionary Value | **CLOSED**, device-verified |
| 3 — empty Control Room note body | **CLOSED**, device-verified (but see §6 — the *open* flow is separately broken) |
| 1 — OPEN path | **OPEN** — now failing at D→E on the date-coercion defect |

## 9. Recommended sequencing

1. **The type audit (§3)** — this is the user's explicit ask and subsumes §2, §4 and
   probably §7's first item. Produce a ranked list of every mistyped parameter feed
   **before** building, so scope decisions go to the user.
2. Establish the date coercion class from a donor, then fix §2 and §4 together.
3. `ROUTER_TRACE = False` (§5) — trivial, do it in the same build.
4. Control Room open flow (§6) — MVP-critical, MANUAL arm, independent of OPEN.
5. `WFItems` wrapper class fix (§7).

Deferred and still open from earlier cycles: brightness/volume cut from MVP; stale-state
`State` rebind; Donor 5's 14 `WFConditionalActionString` sites; DEV-06 ownership design.
