# Device protocol — debug cycle 6 (`open-routing-sequence-error`, symptom 1)

**No PROSOCHĒ rebuild. No clean install. Do NOT delete or re-import PROSOCHĒ.**

Deleting and re-importing PROSOCHĒ would silently rewrite the very thing step 2 measures,
and the sitting would prove nothing. The PROSOCHĒ already on the phone (`build 2026-08-14f`)
is the artifact under test and must stay exactly where it is.

Artifact to import: `PROSOCHE Probe 5 - Input Echo.shortcut`
(signed, AEA1, 22 953 bytes; decrypted and verified to carry 7 actions,
`WFWorkflowHasShortcutInputVariables = true`,
`WFWorkflowInputContentItemClasses = ["WFStringContentItem"]` — the same input
declaration PROSOCHĒ uses, so it is a faithful test of the same handoff).

---

## Step 1 — INPUT PROBE (the decisive one)

1. Import `PROSOCHE Probe 5 - Input Echo.shortcut`.
2. Open the **OPEN** Personal Automation (`When any of 3 apps are opened`).
3. On its **Run Shortcut** action, tap the shortcut chip and choose
   **PROSOCHE Probe 5 - Input Echo** instead of PROSOCHĒ.
   Leave the `Input` field alone — it should keep the yellow Text magic variable.
4. Save. Open one of the watched apps.

**Report the alert verbatim — both bracket lines.**

| What you see | What it proves |
|---|---|
| `RAW [OPEN]` / `NORMALISED [OPEN]` | The handoff delivers input. The defect is inside PROSOCHĒ's OPEN pipeline. |
| `RAW []` / `NORMALISED []` | The handoff runs but delivers nothing. |
| Same `please choose a value` error, **no alert at all** | The failure is at or above the handoff — in the wrapper or the trigger — and has nothing to do with what PROSOCHĒ contains. Five cycles of plist theory would be aimed at the wrong layer. |

## Step 2 — REPOINT BACK (single-variable test of a stale stored reference)

Do this **after** step 1, whatever step 1 showed.

1. Open the same automation again.
2. On the **Run Shortcut** action, tap the chip and select
   **PROSOCHĒ — Nine Circles — Dumb** fresh from the list.
   Re-selecting is the point: it rewrites the stored reference. Do not just look at it.
3. Save. Open a watched app.

| What you see | What it proves |
|---|---|
| It now works (PROSOCHĒ UI appears) | The stored reference was stale. The chip rendered from a cached *name* while the underlying target still pointed at a deleted install. The plist was not the problem. |
| Same `please choose a value` error | A stale reference is refuted with stored-representation evidence rather than a UI reading, and the defect really is inside PROSOCHĒ's OPEN pipeline. |

## Step 3 — DONOR 3 (do this regardless of what steps 1 and 2 showed)

**Un-gated deliberately.** This was originally conditional on step 1 showing `[OPEN]`, but
you offered to build donors and this costs one round trip either way. Build it even if
steps 1–2 look conclusive: it settles five constructs that have **zero** verification
coverage from any source we have, and it is the strictly strongest evidence channel in this
project — device ground truth beats the ToolKit catalog, which has now been wrong or
incomplete on three separate axes this session.

Same trick that cracked the empty-note bug: let iOS serialise the constructs we cannot
verify, then read its output as ground truth.

**What each item settles — none of these are idle curiosity:**

| Item | Open question it closes | Why it cannot be answered otherwise |
|---|---|---|
| 3 (variable-vs-variable If) | How iOS serialises a variable as a numeric condition operand. **13 sites, first at action 167 — on the guaranteed-executed OPEN path.** | Every conditional in all 19 golden-corpus shortcuts uses a **literal** operand. Zero precedent anywhere. |
| 4 (Calculate, default `+`) | Whether iOS stores an explicit `WFMathOperation` for the default operation. **This is DEV-05**, currently open on 1-of-2 corpus evidence, weaker than was recorded. | A donor settles it outright instead of leaving it open. |
| 5 (Round) | `Round` parameter shape | **Zero** golden-corpus instances |
| 6 (Random Number) | `number.random` parameter shape | **Zero** golden-corpus instances |
| 7 (Repeat 9) | `repeat.count` shape | Control-flow family is **absent from the ToolKit catalog entirely** — 336 OPEN-body actions are structurally invisible to every catalog sweep run so far |

In **Shortcuts.app on the iPhone**, create a new shortcut named `Donor 3` containing,
in this order:

1. **Number** → `5`, then **Set Variable** → `A`
2. **Number** → `3`, then **Set Variable** → `B`
3. **If** → set the left side to variable `A`, condition **is greater than**, and then
   **tap the number field on the right and insert the variable `B`**.
   (Putting a *variable* — not a typed number — on the right is the whole point.)
   Put a **Show Alert** inside it. End If.
4. **Calculate** → `A` `+` `B` (leave the operation on its default `+`)
5. **Round** → round the calculation result **down** to the **Integer** place
6. **Random Number** → between `1` and `100`
7. **Repeat** `9` times, with a **Comment** inside

Then: Share → **Save to Files** (or AirDrop) → send the `.shortcut` to the Mac and drop it
in `.planning/debug/`. Signed is fine — signed `.shortcut` files can now be decrypted and
read here (that capability is what cracked symptom 3).

**Note:** do not attempt to export the Personal Automation itself — iOS does not allow it.
A regular shortcut is exportable; an automation is not. Nothing in this protocol requires
exporting the wrapper.

This settles, from the device itself rather than from a catalog: how iOS serialises a
variable in a numeric condition operand (zero golden-corpus coverage — every corpus
conditional uses a literal), whether `Calculate` stores an explicit operation for `+`,
and the parameter shapes of `Round` and `Random Number` (both have **zero** corpus
instances anywhere).
