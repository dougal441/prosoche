# PROSOCHĒ — Config Block

**Cross-references:** This is one of three Phase 1 artifacts. The capability audit table, deviation log, user action items, and coverage check live at `docs/BUILD-NOTES.md`. The five blocker decisions (BD-01 through BD-05) that shape several of this file's values — most directly BD-01's note on the `Ash` sequence entry below — live at `docs/CAPABILITY-DECISIONS.md`.

## How to use this file

This literal is **product configuration, not user data**. It is never written to `state.json` — `state.json` holds the mutable per-run machine state (heat, gravity, pressure, circle, active_session, etc.), while this file holds the fixed tuning values that shape how that machine state is interpreted.

It is transcribed **verbatim** into a single Shortcuts `Text` action (`is.workflow.actions.gettext`) and parsed once per run via `Detect Dictionary` (`is.workflow.actions.detect.dictionary`, the same JSON-parsing action used for `state.json` — see CAP-3 in `docs/BUILD-NOTES.md`) into a `Config` variable. Every later action that needs a tunable value reads it from `Config` by key, rather than hard-coding a literal inline.

It is authored **once** and copied verbatim into both the Dumb and Sentient forks — never hand-diverged. If a value needs to change for one fork and not the other, that is an architectural decision (Rule 4 territory), not a config edit.

### The transcription recipe

1. **One Shortcuts `Text` action** (`is.workflow.actions.gettext`) holds the literal from `## Config JSON literal` below, transcribed character-for-character — the fenced block in this file is the transcription source, not a description of one. This action runs exactly once, near the top of the action graph, before routing.
2. **One `Detect Dictionary` action** (`is.workflow.actions.detect.dictionary`) immediately consumes that Text output and parses it into a dictionary, stored as a variable named `Config`. This happens once per run — the same pattern already used for `state.json` (see CAP-3 in `docs/BUILD-NOTES.md`).
3. Every later action that needs a tunable value reads it from `Config` via **`Get Dictionary Value`, using 1-based dot notation on the key path** — for example `thresholds.Purgatory` to fetch the middle profile's threshold array, or `heat.cap` to fetch the Heat cap. Never hard-code a literal number inline where a `Config` read is available; the whole point of this file is that a value changes in exactly one place.

**Two coercion hazards a Phase 2 or Phase 3 executor will otherwise hit** (see `.planning/research/PITFALLS.md` A4/A5):

- **`safety.allow_volume_increase` is a JSON boolean and will read back as numeric `1` or `0`, not the strings `true`/`false`.** Branch on the number (`Is Greater Than 0`), never on a string comparison to `"true"`.
- **Any value destined for an `If` comparison must pass through a `Text` action first.** A Dictionary Value compared directly inside an `If` can evaluate blank — a documented Shortcuts bug, not a hypothetical one. Route the Dictionary Value into a `Text` action, then compare the resulting Text variable.

## Config JSON literal

This is the complete literal: nine sibling top-level keys, transcribed once from canonical strategy and never restated elsewhere in this file. `sequences` below now carries **BD-06 Decision 4's slot table** in full, applied by phase 11 plan 02: all nine shipped primitive names are live, the three combined entries (`Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror`) are abolished, and every entry names exactly one primitive. `thresholds` carries the Phase 10 raised curve.

**Two entries here are deliberately INTERIM and are not BD-06's final table:**

- **Circle 6 holds `Eject` in all three sequences.** BD-06 gives Circle 6 to `Redirect` in `Classic` and `Ambient`, and to `Eject` only in `BlackMirror`. `Redirect` — the *routed* Exile, which lands the user in a deterministically selected exit — has no implementation until **Phase 17**, and `tools/build_state_engine.py`'s `verify_dispatch_coverage()` fails the build on any dispatch branch that no sequence names, so a `Redirect` branch cannot be emitted before a sequence can name it. **Phase 17 flips exactly two cells:** `Classic[5]` and `Ambient[5]`, `Eject` → `Redirect`.
- **Circle 8's `Loud Mirror` dispatches `mirror_and_voice()`,** the same implementation as Circle 7's `Mirror`. This is what closes the *dispatch* half of CIRC-08 — Circle 8 reached no branch at all for four phases — using an implementation that already carries the once-per-run and voice-enabled gates. **Phase 15** replaces it with the designed Voice primitive.

Neither is a settled decision. Both are recorded here so a later reader cannot mistake an interim stand-in for the designed behaviour.

```json
{
  "config_version": 1,
  "behavioural_day": {
    "offset_seconds": -14400,
    "key_format": "yyyy-MM-dd"
  },
  "thresholds": {
    "Paradise": [4, 7, 10, 13, 16, 19, 22, 25, 28],
    "Purgatory": [3, 5, 7, 9, 11, 13, 16, 19, 22],
    "Inferno": [2, 3, 5, 7, 9, 11, 13, 15, 17]
  },
  "cooldown_seconds": {
    "Paradise": 60,
    "Purgatory": 180,
    "Inferno": 300
  },
  "sequences": {
    "Classic": ["Pause", "Black and White", "Silence", "Intention", "Dim", "Eject", "Mirror", "Loud Mirror", "Frozen"],
    "BlackMirror": ["Pause", "Intention", "Black and White", "Mirror", "Silence", "Eject", "Dim", "Loud Mirror", "Frozen"],
    "Ambient": ["Black and White", "Silence", "Dim", "Pause", "Intention", "Eject", "Mirror", "Loud Mirror", "Frozen"]
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
    "allow_volume_increase": false,
    "ash_managed_color_filters": true
  }
}
```

Transcribed from canonical strategy: `behavioural_day.offset_seconds` from §10.1; `thresholds.*` from §10.5, **raised in Phase 10** (this mirror was missed at the time and was corrected by plan 11-02 — `docs/state_engine_self_check.py:10-17` carries the same table and must change in the same commit as the literal); `cooldown_seconds.*` from §22; `sequences.*` from §12 — `Classic` from §12.1, `BlackMirror` from §12.2, `Ambient` from §12.3, with **BD-06 Decision 4's naming and slot table applied over all three**, subject to the two interim entries noted above; `heat.*` from §10.2's suggested initial rule; `gravity.*` from §10.3.

**Note — the primitive named `Ash` in the two notes below now ships as `Black and White`.** BD-06 Decision 3 renamed it; plan 11-02 applied the rename to the sequence arrays and to the dispatch surface and changed **nothing** about its behaviour. `ash()` keeps its Python identifier, its alert-only fallback is verbatim, and `docs/phase5_self_check.py`'s assertion that no Color Filters intent is emitted stays green. The `safety.ash_managed_color_filters` key keeps its name because it is a `state.json`-adjacent Config key, not a display name.

**Note — SUPERSEDED by BD-01-R (2026-08-13).** Ash *is* a real system Color Filters change on iOS: `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` with `operation = turn` and an explicit `state`, applied On and restored Off. `safety.ash_managed_color_filters` (default `true`) is the canonical-§21 opt-in — when `false`, Ash falls back to BD-01's non-environmental visual pause. Phase 5 reads this flag and branches. The paragraph below is retained for history; its claim that Ash is non-environmental no longer holds.

**Note — binding (historical, superseded above):** BD-01 (see `docs/CAPABILITY-DECISIONS.md`) redefines what the **Ash** primitive *does* on the iOS build (a non-environmental, self-contained low-salience visual pause rather than a system Color Filters toggle) — it does **not** delete Ash from these sequence orderings. All three arrays above keep their nine entries and keep the primitive where canonical strategy §12 places it (`Classic` position 2, `BlackMirror` position 3, `Ambient` position 1). The combined `Ash+Confession` entry this note originally described was abolished by BD-06 Decision 5 in plan 11-02: `BlackMirror` position 3 now names `Black and White` alone, and `Intention` — the renamed Confession — moved to position 2. This keeps the sequence table the single source of truth for which primitive fires at each Circle, and localises the grayscale deviation to one decision record (BD-01) instead of touching this file's structure.

**Note — `heat.reopen_bonus_mode` is a labelled prototype interpretation, not a canonical value.** Canonical strategy §10.2 states a reopen under 2 minutes earns an additional `+2` and a reopen under 10 minutes earns an additional `+1`, but it does not settle what happens at a reopen that satisfies both bands simultaneously — for example, a reopen at 90 seconds, which is both "under 2 minutes" and "under 10 minutes." The value `exclusive` means only the tightest matching band applies: a 90-second reopen earns `+2` only, never `+3`. This is a prototype interpretation chosen here, not a canonical value. The alternative value is `cumulative` (both bands would stack, so the same 90-second reopen would earn `+2` plus `+1` = `+3`). Phase 3 owns implementing STATE-04 (the rapid-reopen Heat bonus) against whichever value this key holds at build time — it must read `reopen_bonus_mode` and branch, not hardcode either behavior.

**Note — Pressure and Circle resolution.** Pressure is Heat plus Gravity (`pressure = heat + gravity`, §10.4). Resolving Pressure to a Circle uses the highest index from 1 to 9 whose threshold in the active profile's array is met or exceeded by Pressure, clamped to 1 through 9 — an ordered greater-than-or-equal scan, never an equality test, because no numeric-equals condition code exists in Shortcuts (`WFCondition` code `0` means "is less than," not "equals" — see `.planning/research/PITFALLS.md` A5). The `thresholds` arrays above are ascending by construction (each profile's nine values strictly increase left to right) and this ordering is load-bearing: the scan overwrites its running Circle value on every satisfied threshold, so it only lands correctly on the *highest* satisfied threshold because the array ascends. Reordering a threshold array would silently break Circle resolution.

## Field reference

`Provenance` is either a canonical strategy section reference, or one of two explicit labels used when the strategy leaves a value open: `PROTOTYPE DEFAULT` (the strategy requires the field to exist but states no number) or `PROTOTYPE INTERPRETATION` (the strategy states a rule but leaves its resolution ambiguous). This distinction is the discipline that stops an invented value from being mistaken for a canonical one — see T-01-03 in this plan's threat register.

| Key path | Value | Meaning | Provenance | Tunable range |
|---|---|---|---|---|
| `config_version` | `1` | Schema version of this Config literal, bumped whenever a key is added, renamed, or removed | PROTOTYPE DEFAULT | Integer, increment by 1 per breaking change; never decrease |
| `behavioural_day.offset_seconds` | `-14400` | Behavioural Day = Current Date minus 4 hours, so the day rolls over at 04:00 not midnight | §10.1 | Must stay negative and between roughly `-3600` (1h) and `-21600` (6h) or the "close the midnight loophole" purpose is defeated |
| `behavioural_day.key_format` | `"yyyy-MM-dd"` | UTS#35 date-format pattern string consumed by the `Format Date → Custom` action to render the adjusted date as a comparable, sortable day key | §10.1 ("format as date key"), pattern is a UTS#35 format string | Must remain a format that sorts and compares correctly as a string (ISO-8601-style); do not switch to a locale-dependent pattern |
| `thresholds.Paradise` | `[4, 7, 10, 13, 16, 19, 22, 25, 28]` | Pressure thresholds for the slow-descent profile, index 1-9 | §10.5, raised in Phase 10 | Must stay strictly ascending; must stay below `heat.cap` + `gravity.cap` (35) at index 9 or Circle 9 becomes unreachable |
| `thresholds.Purgatory` | `[3, 5, 7, 9, 11, 13, 16, 19, 22]` | Pressure thresholds for the balanced (default) profile | §10.5, raised in Phase 10; key renamed from `Limbo` by BD-06-A1 | Same as `thresholds.Paradise` |
| `thresholds.Inferno` | `[2, 3, 5, 7, 9, 11, 13, 15, 17]` | Pressure thresholds for the fast-descent profile | §10.5, raised in Phase 10 | Same as `thresholds.Paradise`; keep the most aggressive of the three so `heat.cap` must stay above this array's highest value or the top Circles become unreachable in every profile |
| `cooldown_seconds.Paradise` | `60` | Ice (Circle IX) cooldown duration for the Paradise profile | §22 | Positive integer seconds; the strategy calls this "~60 sec," so treat single-digit-second changes as within the intended tolerance |
| `cooldown_seconds.Purgatory` | `180` | Ice cooldown duration for the Purgatory profile | §22; key renamed from `Limbo` by BD-06-A1 | Positive integer seconds, "~3 min" |
| `cooldown_seconds.Inferno` | `300` | Ice cooldown duration for the Inferno profile | §22 | Positive integer seconds, "~5 min" |
| `sequences.Classic` | 9-entry array, `Pause`…`Frozen` | The single primitive fired at each Circle 1-9 under the Classic ordering | §12.1, BD-06 Decision 4 | Must stay exactly 9 entries, each naming exactly one primitive with no `+`; every entry must exactly equal an emitted dispatch branch name, which `verify_dispatch_coverage()` fails the build over. Reordering changes which primitive fires at which Circle — a deliberate tuning act, not a casual edit |
| `sequences.BlackMirror` | 9-entry array, `Pause`…`Frozen` | The single primitive fired at each Circle 1-9 under the Black Mirror ordering | §12.2, BD-06 Decision 4 | Same as `sequences.Classic` |
| `sequences.Ambient` | 9-entry array, `Black and White`…`Frozen` | The single primitive fired at each Circle 1-9 under the Ambient ordering | §12.3, BD-06 Decision 4 | Same as `sequences.Classic` |
| `heat.open_base` | `1` | Heat added for every genuine new OPEN | §10.2 | Small positive integer; this is the baseline unit the other Heat deltas are scaled against |
| `heat.reopen_under_120s_bonus` | `2` | Additional Heat when the reopen happens under 2 minutes since the last close | §10.2 | Positive integer, should stay ≥ `heat.reopen_under_600s_bonus` since it is the tighter, more compulsive band |
| `heat.reopen_under_600s_bonus` | `1` | Additional Heat when the reopen happens under 10 minutes since the last close | §10.2 | Positive integer, should stay ≤ `heat.reopen_under_120s_bonus` |
| `heat.reopen_bonus_mode` | `"exclusive"` | Whether the two reopen bonuses above stack (`cumulative`) or only the tightest matching band applies (`exclusive`) when a reopen satisfies both bands | PROTOTYPE INTERPRETATION | Only `"exclusive"` or `"cumulative"` are valid; Phase 3 owns STATE-04 against whichever value is set |
| `heat.overrun_penalty` | `2` | Additional Heat when the previous session exceeded its declared duration by more than `overrun_ratio` and more than `overrun_min_seconds` | §10.2 | Positive integer |
| `heat.overrun_ratio` | `0.5` | Fractional overrun threshold (50%) used together with `overrun_min_seconds` to decide whether `overrun_penalty` applies | §10.2 | Decimal between 0 and 1; both this and `overrun_min_seconds` must be satisfied together (an AND, not an OR) per §10.2's "by >50% and >2min" wording |
| `heat.overrun_min_seconds` | `120` | Absolute-seconds overrun floor used together with `overrun_ratio` | §10.2 | Positive integer seconds ("2 minutes" in the strategy text) |
| `heat.contract_respected_relief` | `-1` | Heat change when the previous declared boundary was respected | §10.2 | Negative integer (a relief, not a penalty) |
| `heat.decay_amount` | `-1` | Heat change per `decay_interval_seconds` of elapsed time since the last genuine target-app interaction | §10.2 | Negative integer |
| `heat.decay_interval_seconds` | `600` | Elapsed-time unit (10 minutes) that `decay_amount` applies per | §10.2 | Positive integer seconds ("~10 minutes" in the strategy text) |
| `heat.ice_expiry_relief` | `-1` | Heat relief applied when Ice (Circle IX) cooldown naturally expires, per §22's "provide Heat relief" instruction | PROTOTYPE DEFAULT | Negative integer; the strategy requires *some* relief on Ice expiry but states no number — must be large enough that expiring Ice visibly lowers Pressure, not a token `-1`-and-forget value if testing shows it re-triggers Ice immediately |
| `heat.floor` | `0` | Minimum Heat value after all deltas are applied | §10.2 | Fixed at `0`; Heat is explicitly never negative |
| `heat.cap` | `30` | Maximum Heat value after all deltas are applied | §10.2 | Must stay above the highest threshold in the most aggressive profile (`thresholds.Inferno[8]` = 17) plus `gravity.cap` (5), or the top Circles become unreachable even at max Heat |
| `gravity.opens_per_point` | `6` | Divisor in `gravity = floor(opens_today / opens_per_point)` | §10.3 | Positive integer; smaller values make Gravity accumulate faster across a day |
| `gravity.cap` | `5` | Maximum Gravity value | §10.3 | Fixed at `5` per the strategy's own suggested rule |
| `exits.exploration_rate` | `0.2` | Epsilon in the epsilon-greedy exit-learning policy — the fraction of exit selections that explore a non-preferred enabled exit rather than exploit the historically strongest one | PROTOTYPE DEFAULT | Decimal between 0 and 1; §9.3 requires this be configuration, not a hardcoded constant, but states no number |
| `exits.exploit_min_observations` | `10` | Minimum number of recorded observations for an exit before the exploitation phase (rather than even rotation) begins preferring it | PROTOTYPE DEFAULT | Positive integer; too low risks exploiting on noise, too high delays learning noticeably |
| `safety.brightness_floor` | `0.10` | Minimum brightness PROSOCHĒ will ever set, so Dimming never reaches zero | §21 ("Never zero... Prefer ~10-15% as a prototype dim value") | Must never be lowered to zero; keep within the strategy's own "~10-15%" band |
| `safety.dim_target` | `0.12` | Target brightness value Dimming aims for within the safe band | §21 | Must stay ≥ `safety.brightness_floor` and within the "~10-15%" band |
| `safety.allow_volume_increase` | `false` | Whether Silence is ever permitted to raise volume (it is not) | §21 ("Never increase volume as punishment") | Must remain `false`; this is a hard safety rule, not a tuning knob |

## Derived-value rules

These values are computed at runtime, never stored directly as leaf keys above. Each rule is written precisely enough that Phase 3 implements it without reinterpreting canonical strategy. **None of these computations may be delegated to the model, per D-04** — the model never controls arithmetic, thresholds, timers, exit selection, or Circle IX.

**Behavioural day.** Take the current instant as a raw `Date` value (via a `Date` action set to Current Date — never feed the `CurrentDate` magic token directly into date arithmetic, per `.planning/research/PITFALLS.md` A6), adjust it by `behavioural_day.offset_seconds` using an explicit `Adjust Date` → `Subtract` operation, then format the adjusted value with `behavioural_day.key_format` via `Format Date → Custom` to produce the day key. Never do string-level date math on the raw string. This yields an approximate 04:00-to-03:59 day; its purpose is to close the midnight loophole (§10.1).

**Gravity.** `gravity = min(floor(opens_today / gravity.opens_per_point), gravity.cap)`. The division must be floored to an integer — a fractional Gravity value is a bug, not a feature. The `opens_today` operand must pass through a `Number` action first, because a JSON-sourced value arrives as dictionary text, and Math actions on unconverted dictionary text produce the same class of silent coercion error documented for cents-to-dollars division in `.planning/research/PITFALLS.md` A5.

**Pressure.** `pressure = heat + gravity`.

**Circle resolution.** The highest index from 1 to 9 whose threshold in the active profile's array (`thresholds[profile][i]`) is met or exceeded by Pressure, clamped to 1 through 9. Implemented as a bounded nine-iteration scan: initialize `Circle = 1`, then `Repeat 9 times` overwriting `Circle = Repeat Index` whenever `pressure >= thresholds[profile][Repeat Index]` — because the threshold arrays ascend by construction, the loop naturally lands on the highest satisfied threshold after all nine iterations. **Equality tests must not be used** for this comparison, because Shortcuts has no numeric-equals condition code — `WFCondition` code `0` means "is less than," not "equals" (`.planning/research/PITFALLS.md` A5).

**The Heat pipeline**, as an ordered list — order changes the result, so this sequence is load-bearing:

1. **Decay** Heat by `heat.decay_amount` per `heat.decay_interval_seconds` of elapsed time since the last genuine target-app interaction (`max(last_open_at, last_close_at)`).
2. **Add** `heat.open_base` for the new OPEN.
3. **Add** the rapid-reopen bonus (`heat.reopen_under_120s_bonus` / `heat.reopen_under_600s_bonus`), subject to `heat.reopen_bonus_mode` (`exclusive` = tightest matching band only; `cumulative` = both bands stack when both match).
4. **Add** `heat.overrun_penalty` if the previous session exceeded its declared duration by more than `heat.overrun_ratio` AND by more than `heat.overrun_min_seconds` (both conditions, per §10.2's "by >50% and >2min" wording — not an OR).
5. **Apply** `heat.contract_respected_relief` if the previous session's declared boundary was respected, read from `recent_sessions[0]` (never a separate "pending" field).
6. **Clamp** to `[heat.floor, heat.cap]` — the clamp is always last, after every addition and subtraction above has been applied.

## Change log

- **2026-08-17** — Phase 11 plan 03. **BD-06-A1: the middle profile is renamed `Limbo` → `Purgatory`.** `thresholds.Limbo` → `thresholds.Purgatory` and `cooldown_seconds.Limbo` → `cooldown_seconds.Purgatory`; both **values are unchanged** — `[3, 5, 7, 9, 11, 13, 16, 19, 22]` and `180` — only the keys moved. BD-06 had made `Limbo` the positional name of **Circle 1** while `Limbo` was already the middle profile, so one word named both a depth and a pace; renaming the profile dissolves the collision at the root and makes the three profiles the three canticles of the Commedia, **Paradise / Purgatory / Inferno**. Circle 1 keeps `Limbo`. The rename is **total by necessity, not by taste**: a profile name is a live dotted key path, and a dotted read with a missing segment is a **hard error** in this runtime, so a surviving `thresholds.Limbo` read against a `Purgatory` profile value would be a crash rather than a degradation. Swept in the same commit across the live literal, the profile menu, the import question and its default, the bootstrap normalisation fallback, `docs/state_engine_self_check.py`'s threshold table, and this file. **No migration, dual-key alias or read-time normalisation was built** — BD-06-A1 records that PROSOCHĒ is undeployed and old `state.json` files are explicitly not a consideration. The live literal was edited through `tools/plist_text_edit.py`'s guarded round trip and re-parsed with `json.loads`; this file is its mirror, not its source.
- **2026-08-17** — Phase 11 plan 02. **BD-06 Decision 4's whole slot table applied in one commit.** All three `sequences` arrays rewritten to the nine shipped names (`Pause`, `Black and White`, `Silence`, `Intention`, `Dim`, `Eject`, `Mirror`, `Loud Mirror`, `Frozen`); the three combined entries `Ash+Confession`, `Silence+Mirror` and `Dimming+Mirror` abolished per BD-06 Decision 5; `primitive_dispatch()` moved from condition code 99 ("contains") to 4 ("string is") across all ninety `Selected Primitive` conditionals, without which `Loud Mirror` would also fire the `Mirror` branch. `Redirect` deliberately appears nowhere — Phase 17 flips `Classic[5]` and `Ambient[5]` from `Eject` to `Redirect` once it exists. `tools/build_state_engine.py`'s new `verify_dispatch_coverage()` is armed in both builders and makes any future disagreement between this table and the dispatch surface a build failure. Also fixed in the same pass: the pre-existing `thresholds` drift, where this mirror still showed the pre-Phase-10 curve while the live literal and `docs/state_engine_self_check.py:10-17` both carried the raised one. The live literal in `src/PROSOCHE-Dumb.xml` was edited through `tools/plist_text_edit.py`'s guarded round trip; this file is its mirror, not its source.
- **2026-08-17** — Phase 11 plan 01 (tracer). The BD-06 primitive rename `Knock` → `Pause`, applied to the three `sequences` cells that named it (`Classic[0]`, `BlackMirror[0]`, `Ambient[3]`) and to the two `Field reference` rows that spelled the array bounds. One name only: the remaining BD-06 renames move in plan 11-02, together with the abolition of the three combined entries and the condition-99 → condition-4 dispatch move. The live literal in `src/PROSOCHE-Dumb.xml` action 7 was edited in the same commit through `tools/plist_text_edit.py`'s guarded round trip; this file is its mirror, not its source.
- **2026-08-13** — File created by plan 01-01 (`## How to use this file` skeleton and the `sequences` object). Completed by plan 01-03 (`config_version`, `behavioural_day`, `thresholds`, `cooldown_seconds`, `heat`, `gravity`, `exits`, `safety`; the field reference, derived-value rules, and transcription recipe). Any later edit to this file adds a new dated line here.
