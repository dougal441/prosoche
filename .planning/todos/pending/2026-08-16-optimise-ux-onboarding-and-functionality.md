---
created: 2026-08-16T00:00:00.000Z
title: Optimise and streamline the UX — onboarding and in-run functionality
area: ux
severity: major
files:
  - tools/build_state_engine.py
  - src/PROSOCHE-Dumb.xml
  - src/PROSOCHE-Sentient.xml
  - PROSOCHE_Build_Addendum_01.md
---

> **COVENANT OVERHAUL (2026-08-19):** PARTLY RESOLVED BY DESIGN: the announcement-menu tension is settled by BD-09 Decision 9 (pre-menu retired; leave affordance in-surface), and Circle-order tuning by BD-09 Decision 7. The surviving scope — funnel instrumentation, latency, copy voice, Note restructure — is Phase 24 (renumbered from 20).


## Problem

The MVP is device-verified as a *mechanism* (OPEN → Heat/Gravity/Pressure → Circle →
intervention fires, build `2026-08-15o`), but it has never been optimised as an
*experience*. Everything shipped so far was authored to satisfy the canonical strategy
and to survive the seven parameter-defect axes — not to be pleasant, fast, or obvious to
a first-time user. Three distinct problem surfaces:

**1. Onboarding is the weakest link and is known-broken.** The canonical strategy's
"self-saucing" promise (§18: import → one tap → Note → create two automations → it runs
itself) currently fails at the automation-creation step. The embedded instructions are
factually impossible as written on iOS 26 — this is already captured in
`2026-08-14-repair-ios-26-automation-onboarding.md` and must be fixed *first*; this todo
covers everything after that fix lands. Beyond correctness, the flow itself is long:
import questions → manual run → read a long Note → leave the app → build two Personal
Automations by hand → come back. Each step is a drop-off point, and drop-off before the
first OPEN means the product has literally never run for that user.

**2. In-run interaction cost is unmeasured.** Circle 1 fired with a `Leaving / Continue`
menu, but no pass has been made over *any* Circle's copy, tap-count, latency, or dismiss
path. Canonical strategy §6.4 (the `one sec` field study) is explicit that the single
strongest mechanism is **giving the user an easy option to dismiss the consumption
attempt** — stronger than the deliberation message. The current design risks
over-investing in message text and under-investing in the choice architecture. §30's
first-named failure mode is intervention fatigue, and §12's stated key failure is "the
intervention is so annoying that the user disables PROSOCHĒ" — a product failure even if
it blocks more opens.

**3. The Control Room is a wall of text doing four jobs at once** — setup guide,
manifesto proforma, settings display, and event ledger — with no separation of what the
user reads *once* from what they return to. Build Addendum 01 already renames it to
`PROSOCHĒ`; that rename is a natural moment to restructure rather than a second pass.

## Solution

Sequence matters — do not start this until the onboarding *correctness* todo is closed.

1. **Close the prerequisites first.**
   - `2026-08-14-repair-ios-26-automation-onboarding.md` (correctness — instructions that
     actually work on iOS 26).
   - `2026-08-15-ship-readiness-cleanup.md` (strip `BUILD_STAMP`, `ROUTER_TRACE`,
     `OPEN_BISECT` and the ten breadcrumb alerts — a user cannot evaluate UX through ten
     debug dialogs).
   - `2026-08-14-apply-build-addendum-01.md` (Core/Aware, Dante Circle names, Note rename)
     — this is itself a UX change, so land it before re-authoring copy against old names.

2. **Instrument the funnel before redesigning it.** Define the drop-off points explicitly
   (import → first manual run → Note read → Automation A created → Automation B created →
   first OPEN → first intervention completed) and decide what, if anything, `state.json`
   should record locally about how far setup got. This is the only honest way to know
   whether onboarding changes helped. Keep it local-only per §27.

3. **Reduce time-to-first-value.** Options to evaluate, not a prescription:
   - a `Setup Check` item in the manual menu that reports which of the two automations
     has ever fired (derivable from whether `OPEN`/`CLOSE` input has ever been seen), so
     the user gets confirmation instead of guessing;
   - deferring the `MY PHONE, ON PURPOSE` proforma out of the critical path — it is not
     needed until the first Mirror/Contract Circle, and asking for it at minute one
     competes with automation setup;
   - shortening the READ THIS FIRST block to the two automations plus the safety warning,
     moving rationale below.

4. **Do a full interaction-cost pass over all nine Circles.** For each: count taps,
   count actions on the path, measure perceived latency on device, and confirm the
   dismiss/leave option is present, obvious, and reachable in one tap at every Circle
   where the design allows it (per §6.4). Rewrite copy to §29's voice — concrete
   behavioural facts, no slogans, no exclamation marks, no emoji. Retire or rewrite any
   message that reads as a lecture.

5. **Restructure the Note around read-once vs. return-to.** Setup instructions collapse
   or move to the bottom once automations exist; settings and the ledger surface at the
   top. Coordinate with Addendum 01's rename rather than doing two passes.

6. **Re-verify on device.** Every change here touches the generator, so the same
   discipline applies: validate, sign, decrypt-verify what shipped, and run the funnel
   end to end on the target iPhone from a genuinely fresh import (delete `state.json` and
   the Note first — a returning-user run does not test onboarding).

## Related

- Canonical strategy §6.4 (dismissal is the strongest mechanism), §7 (onboarding layers),
  §12 (annoyance/disablement as the key failure), §17 (Note structure), §18 (first-run
  flow), §29 (voice), §30 (intervention fatigue).
- `2026-08-14-repair-ios-26-automation-onboarding.md` — hard prerequisite.
- `2026-08-14-apply-build-addendum-01.md` — naming/renames this todo's copy work depends on.
- `2026-08-15-ship-readiness-cleanup.md` — scaffolding must be stripped to evaluate UX.

## Device observations from the 2026-08-18/19 UAT — four small UX items

Recorded in passing during phase 4/6/9 verification on a fresh install of Core `873fa3db…`.
None was investigated; each is a starting point, not a diagnosis. Evidence throughout:
`.planning/debug/device-state/README.md`.

1. **Raw unrounded floats are shown to the user.** The Circle 1 `Pause` alert rendered
   *"Circle 1 · pressure 3.33333333333333 · heat 3"*. Fourteen decimal places of a behavioural
   quantity, in the product's calmest surface.
2. **The contract result is bare machine phrasing.** On CLOSE, a completed contract showed only
   *"Contract — Overrun seconds: 30"*, to a user who has just put an app down. Compare the care
   taken over the Leaving/Continue copy, which reads well (finding F-11).
3. **`Capture → Notes` lands on the Control Room note, not a blank one.** The route is
   `open_app("Notes")`, so iOS restores the last-viewed note — and the last note PROSOCHĒ itself
   opened is its own settings page. Correct per the implementation, but a user sent to "capture a
   thought" arrives at the app's configuration. Product decision, not a bug (finding F-21).
4. **Permission dialogs land mid-intervention on a new install.** Three distinct Save File
   prompts plus a notification prompt, all on top of the tracked app in the first minutes of use.
   Fully characterised — including the fix — in
   `.planning/todos/pending/2026-08-17-note-entity-chooser-on-clean-install.md`; cross-referenced
   here because the *experience* is an onboarding problem even though the *cause* is generator
   shape (finding F-16).
