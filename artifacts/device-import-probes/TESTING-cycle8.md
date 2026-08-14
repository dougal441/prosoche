# Cycle 8 device protocol — the fix

**Artifact:** `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`
**Build stamp:** `build 2026-08-14h` (verified present *inside the signed file* by decryption; `14g` verified absent)
**This is a FIX, not a measurement.** Your letter `B` located it exactly.

---

## What you found

You reported **B**. That put the failure in a 20-action span — the behavioural-day rollover.

I read all 20 actions. Eighteen of them are action types that have already run successfully on your
phone, so they were not suspects. The remaining two were both `If` checks, and both had the same
defect: **the thing being tested was written as a piece of text rather than as a reference to a
variable.** Shortcuts could not resolve it, showed the `If`'s input field as empty, and refused to
run — which is exactly the "Please choose a value for each parameter in this action" message.

Three independent sources agree this was wrong, and agree on what right looks like:

- **Your own Donor 3.** The variable-vs-variable `If` you built on your iPhone writes it the correct way.
- **All 19 reference shortcuts.** 20 of 20 comparable `If` actions write it the correct way. None write it our way.
- **PROSOCHĒ itself.** 282 of its 307 `If` actions were already correct — including the router, which
  runs on every single execution and has never failed. Only 25 were wrong.

And the clincher: of those 25, only **two** sit anywhere near the start of the OPEN path — and they are
the first two the OPEN path reaches, two actions after breadcrumb **B**. That is exactly where you stopped.

The fix deletes 13 lines that were overwriting a correct value with a wrong one. It does not invent
anything new; it lets the correct value stand.

---

## The breadcrumbs are still in. That is deliberate.

I could have stripped them. I kept them because **I cannot promise this is the only remaining defect**,
and if there is another one further along, "same error again" would look like the fix failed when
actually we would have moved forward. With the letters still in, a second defect shows up as a
*later letter* — progress plus a location, in the same sitting.

They come out for good once the OPEN path completes end to end.

---

## Step 0 — install and re-point (still unskippable)

1. **Delete** the installed `PROSOCHĒ — Nine Circles — Dumb` from Shortcuts.
2. **Import** the new `PROSOCHĒ — Nine Circles — Dumb.shortcut`.
3. **Re-point the automation.** Deleting a shortcut orphans the Personal Automation's Run Shortcut
   target. Open your **App Is Opened** automation and select `PROSOCHĒ — Nine Circles — Dumb` fresh
   in the Run Shortcut action. Leave the Text `OPEN` action alone.

## Step 1 — confirm the build (10 seconds)

Tap PROSOCHĒ manually. The menu prompt must read **`PROSOCHĒ · build 2026-08-14h`**.
If it says `14g`, the old copy is still installed — go back to step 0.

## Step 2 — the run

**Open one of your watched apps.**

Report **the last letter you see**, and whether a menu appeared after it.

| What you see | What it means |
|---|---|
| **C or any later letter**, then the error | Fix worked. Span B→C is cleared. A different, later defect — report the letter and I localise it next round. |
| **All ten A→J, then a menu** asking `Leaving` / `Continue` | **The OPEN pipeline has completed end to end for the first time in this project's history.** |
| **B again** | My hypothesis was wrong. Genuinely possible, and worth knowing — say so plainly and I go back to the other 18 actions in that span individually. |

Please also confirm the error text is still the same, if you get one.

---

## Optional, and NOT part of this test — a small donor whenever you have two minutes

There is a second group of 14 `If` actions with a *related* but **not identical** question, on the
exit and Circle-9 contract paths. I deliberately did **not** change them, because the evidence that
settled the first group does not transfer, and guessing is what cost us cycles 1, 2 and 5. They all
sit past breadcrumb J, so they cannot affect the test above.

A donor settles it outright. In Shortcuts on your iPhone, build a throwaway shortcut with:

1. **Text** action containing `hello` → **Set Variable** `A`
2. **Text** action containing `hello` → **Set Variable** `B`
3. **If** — set the condition to `A` **is** `B`, choosing the **variable `B`** as the comparison value
   (tap the text field, then pick the variable from the bar, rather than typing text)
4. Anything inside, e.g. a **Show Alert**
5. **End If**

Then Share → **Copy** is not enough — use **Share → Save to Files** so I get the `.shortcut`, and drop
it in `.planning/debug/`. Name it `Donor 4.shortcut`.

That one file tells me whether those 14 sites are defective or fine, at zero device-testing cost.
