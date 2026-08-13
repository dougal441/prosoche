# PROSOCHĒ — Config Block

## How to use this file

This literal is **product configuration, not user data**. It is never written to `state.json` — `state.json` holds the mutable per-run machine state (heat, gravity, pressure, circle, active_session, etc.), while this file holds the fixed tuning values that shape how that machine state is interpreted.

It is transcribed **verbatim** into a single Shortcuts `Text` action (`is.workflow.actions.gettext`) and parsed once per run via `Detect Dictionary` (`is.workflow.actions.detect.dictionary`, the same JSON-parsing action used for `state.json` — see CAP-3 in `docs/BUILD-NOTES.md`) into a `Config` variable. Every later action that needs a tunable value reads it from `Config` by key, rather than hard-coding a literal inline.

It is authored **once** and copied verbatim into both the Dumb and Sentient forks — never hand-diverged. If a value needs to change for one fork and not the other, that is an architectural decision (Rule 4 territory), not a config edit.

## Config JSON literal

This is the complete literal: nine sibling top-level keys, transcribed once from canonical strategy and never restated elsewhere in this file. `sequences` below is carried over byte-identical from plan 01-01 — unchanged, unreordered.

```json
{
  "config_version": 1,
  "behavioural_day": {
    "offset_seconds": -14400,
    "key_format": "yyyy-MM-dd"
  },
  "thresholds": {
    "Paradise": [1, 4, 7, 10, 13, 16, 19, 22, 25],
    "Limbo": [1, 3, 5, 7, 9, 11, 14, 17, 20],
    "Inferno": [1, 2, 4, 6, 8, 10, 12, 14, 16]
  },
  "cooldown_seconds": {
    "Paradise": 60,
    "Limbo": 180,
    "Inferno": 300
  },
  "sequences": {
    "Classic": ["Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice"],
    "BlackMirror": ["Knock", "Confession", "Ash+Confession", "Mirror", "Silence+Mirror", "Dimming+Mirror", "Exile", "Voice", "Ice"],
    "Ambient": ["Ash", "Silence", "Dimming", "Knock", "Confession", "Exile", "Mirror", "Voice", "Ice"]
  },
  "heat": {
    "open_base": 1,
    "reopen_under_120s_bonus": 2,
    "reopen_under_600s_bonus": 1,
    "reopen_bonus_mode": "exclusive",
    "overrun_penalty": 2,
    "overrun_ratio": 0.5,
    "overrun_min_seconds": 120,
    "contract_respected_relief": -1,
    "decay_amount": -1,
    "decay_interval_seconds": 600,
    "ice_expiry_relief": -1,
    "floor": 0,
    "cap": 30
  },
  "gravity": {
    "opens_per_point": 6,
    "cap": 5
  },
  "exits": {
    "exploration_rate": 0.2,
    "exploit_min_observations": 10
  },
  "safety": {
    "brightness_floor": 0.10,
    "dim_target": 0.12,
    "allow_volume_increase": false
  }
}
```

Transcribed verbatim from canonical strategy: `behavioural_day.offset_seconds` from §10.1; `thresholds.*` from §10.5 (`Classic` default profile is `Limbo`, per ARCHITECTURE.md §2); `cooldown_seconds.*` from §22; `sequences.*` from §12, unchanged from plan 01-01 — `Classic` from §12.1, `BlackMirror` from §12.2, `Ambient` from §12.3; `heat.*` from §10.2's suggested initial rule; `gravity.*` from §10.3.

**Note — binding:** BD-01 (see `docs/CAPABILITY-DECISIONS.md`) redefines what the **Ash** primitive *does* on the iOS build (a non-environmental, self-contained low-salience visual pause rather than a system Color Filters toggle) — it does **not** delete Ash from these sequence orderings. All three arrays above keep their nine entries and keep `Ash` and the combined `Ash+Confession` entry exactly where canonical strategy §12 places them (`Classic` position 2, `BlackMirror` position 3 as `Ash+Confession`, `Ambient` position 1). This keeps the sequence table the single source of truth for which primitives fire at each Circle, and localises the grayscale deviation to one decision record (BD-01) instead of touching this file's structure.

**Note — `heat.reopen_bonus_mode` is a labelled prototype interpretation, not a canonical value.** Canonical strategy §10.2 states a reopen under 2 minutes earns an additional `+2` and a reopen under 10 minutes earns an additional `+1`, but it does not settle what happens at a reopen that satisfies both bands simultaneously — for example, a reopen at 90 seconds, which is both "under 2 minutes" and "under 10 minutes." The value `exclusive` means only the tightest matching band applies: a 90-second reopen earns `+2` only, never `+3`. This is a prototype interpretation chosen here, not a canonical value. The alternative value is `cumulative` (both bands would stack, so the same 90-second reopen would earn `+2` plus `+1` = `+3`). Phase 3 owns implementing STATE-04 (the rapid-reopen Heat bonus) against whichever value this key holds at build time — it must read `reopen_bonus_mode` and branch, not hardcode either behavior.

**Note — Pressure and Circle resolution.** Pressure is Heat plus Gravity (`pressure = heat + gravity`, §10.4). Resolving Pressure to a Circle uses the highest index from 1 to 9 whose threshold in the active profile's array is met or exceeded by Pressure, clamped to 1 through 9 — an ordered greater-than-or-equal scan, never an equality test, because no numeric-equals condition code exists in Shortcuts (`WFCondition` code `0` means "is less than," not "equals" — see `.planning/research/PITFALLS.md` A5). The `thresholds` arrays above are ascending by construction (each profile's nine values strictly increase left to right) and this ordering is load-bearing: the scan overwrites its running Circle value on every satisfied threshold, so it only lands correctly on the *highest* satisfied threshold because the array ascends. Reordering a threshold array would silently break Circle resolution.

## Field reference

_Owner: plan 01-03._

## Derived-value rules

_Owner: plan 01-03._

## Change log

_Owner: plan 01-03._
