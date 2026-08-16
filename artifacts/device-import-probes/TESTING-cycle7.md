# Cycle 7 device protocol — OPEN-path bisection

**Artifact:** `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut`
**Build stamp:** `build 2026-08-14g` (verified present *inside the signed file* by decryption; `14f` verified absent)
**This is a MEASUREMENT, not a fix.** Nothing was fixed this cycle, deliberately. The build is byte-identical
to `14f` apart from ten alert actions and the stamp string — proven, not asserted (see "What changed" below).

---

## Why you are doing this

Cycle 6 settled the big question: the handoff works. Probe 5 echoed `RAW [OPEN] / NORMALISED [OPEN]`,
so PROSOCHĒ *does* receive `OPEN`. And repointing the same wrapper back at PROSOCHĒ still failed — so
nothing on the device side is at fault. The failing action is inside PROSOCHĒ, on the OPEN path, before
any of its screens appear.

iOS refuses to tell us *which* action. So this build makes PROSOCHĒ tell us itself: it shows a one-letter
alert at ten checkpoints along the OPEN path. **The last letter you see is the answer.** Everything before
that letter worked; the failure is between that letter and the next one.

There are 10 taps. Sorry. Each one is a single OK, and it buys us a span of tens of actions in one sitting.

---

## Step 0 — install and re-point (do not skip the re-point)

1. **Delete** the installed `PROSOCHĒ — Nine Circles — Dumb` from Shortcuts.
   (Importing over a same-named shortcut can leave a second copy and we would be testing the old one.)
2. **Import** the new `PROSOCHĒ — Nine Circles — Dumb.shortcut`.
3. **Re-point the automation.** Deleting a shortcut orphans a Personal Automation's Run Shortcut target.
   Open your **App Is Opened** automation and select `PROSOCHĒ — Nine Circles — Dumb` fresh in the
   Run Shortcut action, exactly as you did last cycle. Leave the Text `OPEN` action alone.

## Step 1 — confirm the build (10 seconds, and it re-checks symptoms 2 and 3)

Tap PROSOCHĒ manually in the Shortcuts app.

- The trace alert appears, then a menu. **The menu prompt must read `PROSOCHĒ · build 2026-08-14g`.**
  If it says `14f`, the old copy is still installed — go back to step 0.
- While you are here, if you want: **Change Sequence → Classic** should still work with no
  "No value provided" error, and **Open Control Room** should still write the note. Both were fixed in
  earlier cycles and this build did not touch them. Only tell me if one of them has *broken*.
- Otherwise just cancel out of the menu.

## Step 2 — the measurement

**Open one of your watched apps**, the way the automation normally fires.

You will see a series of alerts titled **PROSOCHĒ OPEN TRACE**, each showing a single letter:
`A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, `I`, `J`. Tap OK on each.

**Report the LAST letter you saw**, and whether anything came after it.

That is the whole test. Three possible shapes of answer:

| What you see | What to report |
|---|---|
| Some letters, then the automation error | the last letter (e.g. "got to F, then the error") |
| **No letters at all**, just the error | "no letters" — this is a genuinely important answer, not a failed test |
| All ten letters A→J, then a PROSOCHĒ menu | "all ten, then a menu asking Leaving / Continue" |

Please also say whether the error message was still the same
("…Please choose a value for each parameter in this action").

---

## What each letter means (so the result is unambiguous)

Each letter is shown *after* the work named beside it has finished. So the **last letter you see** tells us
the failure is somewhere in the span that follows it.

| Letter | Shown after | If this is your LAST letter, the failure is in… |
|---|---|---|
| — (none) | — | before the OPEN body even starts — the router or the shared setup. Would contradict cycle 6's probe result and would need its own investigation. |
| **A** | the OPEN branch was entered at all | the 54 actions that read state and config (18 × get-value/text/set-variable). Flat, no branching — a second round would localise to a single action easily. |
| **B** | every state read and every config read finished | the 20-action behavioural-day rollover block. **Contains 2 nested branches** — a second round needed to pick the arm. |
| **C** | the day rollover resolved | the 117-action cooldown block: the live-Ice redirect *and* the Ice-expiry restore (brightness/volume restore, return-to-home). **11 nested blocks, 4 deep — this span would need a second bisection round, and I would say so rather than pretend one pass localises it.** |
| **D** | no live cooldown, Ice-expiry restore finished | the 19-action duplicate-OPEN debounce. 3 nested blocks, 2 deep. |
| **E** | debounce resolved; this is a genuine open | the 108-action Heat pipeline: decay, base, reopen bands, previous-contract adjustment, floor and cap clamps. **11 nested blocks, 4 deep — also a second-round span.** |
| **F** | the whole Heat pipeline finished and Heat is clamped | 8 flat actions: opens-today math and three dictionary writes. Would localise almost immediately. |
| **G** | opens-today, last-open and last-app written | **33 actions containing `Random Number` — one of this cycle's two named suspects** (see below), plus session-ID assembly, Detect Dictionary, Gravity and Pressure. |
| **H** | Random Number, Session ID, Gravity and Pressure all done | **14 actions containing the nine-step `Repeat` scan — the other named suspect.** |
| **I** | the nine-step Circle threshold scan completed | the 53-action pending-exit block (2 repeat-each loops, 3 nested blocks). |
| **J** | Circle written, pending exit completed | only Save File and the Phase 6 leaving block remain — 3 actions before the first menu. |

**Honest caveat, stated up front:** three of these spans (C, E, I) contain nested branching several levels
deep. If your last letter is C, E or I, one pass has *not* localised us to a single action and I will ship a
second, finer bisection inside that span. Spans A, F, G, H and J are small or flat enough that the answer
would be effectively immediate.

---

## The two named suspects (why G and H are bracketed so tightly)

Your **Donor 3** was decrypted this cycle and it did most of its work by *clearing* suspects rather than
finding one. iOS's own serialisation matched ours exactly for the three things we most suspected — the
variable-vs-variable numeric If, and the Calculate action with the operation left at its default. Those are
now closed on device evidence.

But the donor also showed that iOS never writes a whole number the way we do. Where we emit a plain
integer, iOS writes either a decimal or a quoted string — in the donor, in all 19 reference shortcuts, and
without a single exception anywhere. Two actions in PROSOCHĒ carry that difference *and have never once
run on your device*: **Random Number** (in span G→H) and the **nine-step Repeat** (in span H→I).
Everywhere else that same pattern appears, it has already run successfully on your phone — the Control
Room refresh uses it twice and works — so those are cleared.

That makes them a ranked, testable prediction rather than a guess, and this build is designed to confirm or
kill it in one sitting: **if your last letter is G or H, the prediction is right. Any other letter kills it.**

Deliberately, **nothing was changed to "fix" this**. Three static conclusions have already been refuted on
your device this session; the measurement must not be contaminated by an untested change.

---

## What changed in this build (and what provably did not)

- **Added:** 10 alert actions on the OPEN path. Each carries a plain-text title and a plain-text message,
  references no variable, and contains no branching — it cannot fail for a reason of its own.
- **Changed:** the build stamp string, `14f` → `14g`, in two display-only places on the manual menu.
- **Everything else:** with the 10 alerts removed, this build is byte-for-byte identical to `14f` across all
  3,674 actions — verified by comparison, including every internal ID. Symptoms 2 and 3 (the `sequence`
  error and the empty Control Room note) are therefore preserved by construction, not by hope.

To strip the breadcrumbs later: `OPEN_BISECT = False` in `tools/build_state_engine.py`, then rebuild.
