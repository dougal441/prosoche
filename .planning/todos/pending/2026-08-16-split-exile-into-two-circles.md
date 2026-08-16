---
created: 2026-08-16T23:26:00.000Z
title: Split Exile into two Circles — straight-to-home and routed-exit
area: general
severity: major
files:
  - tools/build_state_engine.py:580
  - tools/build_state_engine.py:786
  - tools/build_state_engine.py:695
  - src/CONFIG-BLOCK.md:46
---

## Problem

**User decision, 2026-08-16: Exile becomes two Circles.** One is a bare ejection to the
Home Screen. The other lands the user in a real, chosen destination — a deepened version of
the six exit routes.

Exile today is one line:

```python
def exile():
    return [comment("""Exile is immediate and deterministic:
- Return to Home Screen does not ask a permission question.
- Phase 6 may replace this route with learned exits."""),
            action("is.workflow.actions.returntohomescreen")]
```

Its own comment anticipates this change. It never happened: Phase 6 built the exit
machinery as a *separate* path reached only by choosing "Leaving" from the pre-primitive
menu, and left Exile as the bare Home Screen call. So the product has two disconnected
ways out — a voluntary one that routes somewhere useful, and an involuntary one that dumps
you on a Home Screen full of the same apps.

The strategy's own objection to the bare version is in §30 and §36: ejecting someone to the
Home Screen without a destination is a machine for changing *which* app consumes the time.
That is explicitly not the goal.

**The six exit routes exist but are thin.** `route_exit()` (`tools/build_state_engine.py:786`):

| Exit | What it currently does |
|---|---|
| Capture | Menu → opens Notes, Voice Memos, or Camera |
| Coordinate | Menu → opens Reminders or Calendar |
| Create | Opens a user-supplied URL, asked once and remembered |
| Connect | Opens Contacts. No send, call, or message action exists anywhere — deliberate |
| Consult | Asks a query → Search Web / Search Maps / Notes / Reminders / Calendar / Back |
| Close | Return to Home Screen |

Every one of them is "open an app." None carries context across the boundary — Capture
opens Notes but does not start a note; Coordinate opens Reminders but does not create one;
Consult is the only route that carries anything (the query string). None has ever run on a
device, and `exit_events` is absent from the bootstrap `state.json` template, so the first
real exit against clean state will very likely hard-error
(`2026-08-15-close-state-shape-sentinel-gaps.md`).

**Selection method.** The user's framing is random vs predetermined. The existing selector
(`select_exit()`, `tools/build_state_engine.py:695`) is neither — it is deterministic and
learned: rotate by a persisted counter under 10 observations, then exploit the lowest
average return-time with a 20% exploration roll. Note there is no random-number action in
the exit path at all, deliberately: `.planning/STATE.md` records the decision that "exit
selection remains deterministic and Config-driven without model, random, or network
actions." **Introducing genuine randomness reverses a recorded decision** — do it
knowingly, or implement "random" as rotation/shuffle over enabled exits rather than a real
`number.random` call.

## Solution

1. **Name and define the two Circles.** Suggested split, to be confirmed:
   - **Exile (straight)** — the current behaviour. Immediate, no menu, no question, Home
     Screen. Its virtue is that it is instant and cannot be negotiated with.
   - **Exile (routed)** — ejects *into* a destination rather than to a void. Reuses
     `select_exit()` / `record_exit_and_route()` so the exit is recorded, the return-time
     sample is captured, and the learning loop applies — the involuntary path feeds the
     same evidence base as the voluntary one.
2. **Settle random vs predetermined explicitly**, and record it as a decision:
   - *predetermined* — user picks a fixed exit at onboarding or in the Control Room; Exile
     always lands there. Most defensible: the user chose their own landing pad while calm.
   - *random* — rotation or shuffle across enabled exits. Cheap, and it prevents the
     landing pad becoming its own habit.
   - *learned* — reuse the existing selector unchanged. Free, consistent with the recorded
     no-randomness decision, but means the involuntary Circle inherits explore/exploit
     behaviour the user did not ask for at that moment.
   Whichever wins, it needs a Config key (`exits.exile_selection_mode` or similar) rather
   than being hardcoded, per the Config Block's own rule.
3. **Deepen each of the six routes** — one design pass, then plan, then execute. For each,
   answer: what does it actually open, what context crosses the boundary, and what does the
   user see one second after landing? Concrete leads, all against verified actions:
   - **Capture** — create the note/reminder rather than opening the app, seeded with the
     Confession intention text if one exists this session.
   - **Coordinate** — same, via the Reminders schemas already catalogued in
     `PARAMETER_TYPES.md`.
   - **Create** — currently one saved URL for everyone. Consider a small user-defined set.
   - **Connect** — the §8 intent is routing feed-shaped seeking toward actual people.
     Opening Contacts cold is weak. The no-send constraint is deliberate and stays.
   - **Consult** — already the strongest; it carries the query. Use it as the model.
   - **Close** — the honest null option. Keep it; do not decorate it.
4. **Land `2026-08-15-close-state-shape-sentinel-gaps.md` first.** `exit_events` missing
   from the bootstrap template sits directly on `record_exit_and_route()`. Any device test
   of either Exile Circle will hit it. Hard prerequisite.
5. **Resolve the slot arithmetic.** Each sequence has exactly nine slots. With Ash rebuilt,
   Dimming and Silence distinct, and Exile split, the roster is: Knock, Ash, Silence,
   Confession, Dimming, Exile-straight, Exile-routed, Mirror, Voice, Ice — **ten primitives
   for nine positions**. Either a sequence drops one, or sequences stop being 1:1 with
   Circles, or the count changes. This is the single decision that blocks all three
   in-flight Circle todos; settle it once, here or in a dedicated design pass, and have the
   other todos defer to it.
6. **Rebuild under the provenance guard**, self-check, validate at `--target-macos 26
   --target-platform all`, sign, refresh `artifacts/shortcuts/MANIFEST.md`.

## Related

- Canonical strategy §8 (the six exits and what each is *for*), §8.5 (routing feed-shaped
  seeking to query-shaped seeking), §11 Primitive F (Exile), §30 and §36 (why bare ejection
  is not the goal), §16, §23, §27.
- **Hard prerequisite:** `2026-08-15-close-state-shape-sentinel-gaps.md` (`exit_events`
  absent from bootstrap).
- `.planning/phases/06-exits-exit-learning-contracts/06-UAT.md` — none of the six routes
  has ever run on device.
- `2026-08-16-dimming-and-silence-as-distinct-circles.md` and
  `2026-08-16-build-circle-8-voice-primitive.md` — the other two claimants on the nine
  slots; see step 5.
- `.planning/STATE.md` Decisions — "exit selection remains deterministic and Config-driven
  without model, random, or network actions." Step 2 may reverse this; do so explicitly.
