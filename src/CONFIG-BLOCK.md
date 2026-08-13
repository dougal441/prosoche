# PROSOCHĒ — Config Block

## How to use this file

This literal is **product configuration, not user data**. It is never written to `state.json` — `state.json` holds the mutable per-run machine state (heat, gravity, pressure, circle, active_session, etc.), while this file holds the fixed tuning values that shape how that machine state is interpreted.

It is transcribed **verbatim** into a single Shortcuts `Text` action (`is.workflow.actions.gettext`) and parsed once per run via `Detect Dictionary` (`is.workflow.actions.detect.dictionary`, the same JSON-parsing action used for `state.json` — see CAP-3 in `docs/BUILD-NOTES.md`) into a `Config` variable. Every later action that needs a tunable value reads it from `Config` by key, rather than hard-coding a literal inline.

It is authored **once** and copied verbatim into both the Dumb and Sentient forks — never hand-diverged. If a value needs to change for one fork and not the other, that is an architectural decision (Rule 4 territory), not a config edit.

## Config JSON literal

Only the `sequences` key is populated in this plan. Plan 01-03 fills in the remaining top-level keys (profile threshold tables, Heat coefficients, Gravity, behavioural-day offset, Ice cooldown durations, exploration rate) around this object — the final literal is a single JSON object with `sequences` as one of several sibling top-level keys, not a standalone document.

```json
{
  "sequences": {
    "Classic": ["Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice"],
    "BlackMirror": ["Knock", "Confession", "Ash+Confession", "Mirror", "Silence+Mirror", "Dimming+Mirror", "Exile", "Voice", "Ice"],
    "Ambient": ["Ash", "Silence", "Dimming", "Knock", "Confession", "Exile", "Mirror", "Voice", "Ice"]
  }
}
```

Transcribed verbatim from canonical strategy §12 (Candidate Circle sequences), with no reordering and no omission: `Classic` from §12.1, `BlackMirror` from §12.2, `Ambient` from §12.3.

**Note — binding:** BD-01 (see `docs/CAPABILITY-DECISIONS.md`) redefines what the **Ash** primitive *does* on the iOS build (a non-environmental, self-contained low-salience visual pause rather than a system Color Filters toggle) — it does **not** delete Ash from these sequence orderings. All three arrays above keep their nine entries and keep `Ash` and the combined `Ash+Confession` entry exactly where canonical strategy §12 places them (`Classic` position 2, `BlackMirror` position 3 as `Ash+Confession`, `Ambient` position 1). This keeps the sequence table the single source of truth for which primitives fire at each Circle, and localises the grayscale deviation to one decision record (BD-01) instead of touching this file's structure.

## Field reference

_Owner: plan 01-03._

## Derived-value rules

_Owner: plan 01-03._

## Change log

_Owner: plan 01-03._
