# Pre-install device `state.json` forensics — 2026-08-18

**Artifact:** `state-2026-08-18T1931-stale-preinstall.json`, 4338 bytes, recovered
2026-08-18 21:45 AEST from the paired iPhone's `iCloud Drive/Shortcuts/PROSOCHE/state.json`
via the Mac's iCloud mirror, **before** the file was deleted and before the freshly-installed
build had ever been run.

**Why it is worth a document.** It is the only surviving record of a real device's accumulated
state, and it settles or advances several UAT items at evidence rung 1 that would otherwise
have cost device time. It is also the last state written by a *pre-phase-16* build, which
makes it the direct device-side confirmation of the P0 that phase 16 fixed.

**Provenance / rung.** This is rung-1 analysis (file-level) performed against a **rung-4
artifact** (a file the real device wrote). It carries the authority of the device for *what
the device wrote*, and no authority at all for anything the file does not contain.

---

## Which build wrote it

`settings_snapshot.{brightness,volume}` still carry `changed_at` and `changed_by_session_id`.
Decision **D-02** (plan 16-04) removed both leaves from the writes and the bootstrap seed, and
the current build's template carries `{"original_value": "null"}` alone. `exit_events` is also
a **single object**, not the `[]` the current template seeds (plan `seed_exit_events()`).

**Therefore this file was written by a build that predates phase 16.** Nothing in it can
confirm a phase-16 fix. Everything in it that looks like a phase-16 defect is the *old* defect,
observed on a device for the first time.

---

## F-1 — Session arithmetic is exact, 14 for 14 (Phase 4, Tests 1 and 6)

Every one of the 14 `recent_sessions` entries satisfies
`duration_seconds == ended_at - started_at` exactly. `last_close_at` (1787081517) equals the
newest entry's `ended_at` exactly. The nested `active_session` container is back to its cleared
sentinel after the last CLOSE.

The one contracted session recomputes correctly too: `declared=120`, `duration=21`,
`overrun_seconds = 21 - 120 = -99` ✔, `respected = (overrun <= 0) = true` ✔.

This is stronger evidence for Phase 4 Test 6 than a fresh device run would produce in one
sitting, because it is 14 independent samples spanning 11 hours.

**It does NOT cover:** the A/B session race (no two sessions overlap anywhere in the file), the
04:00 rollover (all sessions fall between 08:16 and 19:31 local on one behavioural day), or the
locked-screen CLOSE.

## F-2 — `recent_contracts` is never written, by any code path (Phase 6, Test 8)

`recent_contracts` is `[]` in the file, despite the file also containing a fully-evaluated
contract (declared 120 s, respected, −99 s overrun) in `recent_sessions`.

This is not a device fluke. `grep -c 'set_value("recent_contracts"' tools/build_state_engine.py`
returns **0**: the key is seeded `[]` by the bootstrap template and no generator path ever
appends to it. Contract outcomes are instead folded into the `recent_sessions` record as
`declared_duration_seconds` / `overrun_seconds` / `respected`.

**Phase 6 Test 8 as written — "state.json's `recent_contracts` holds the last ~10 per §16" —
cannot pass on any build.** Either the test is describing a design that was superseded by
folding contract data into `recent_sessions` (in which case §16 and the test need restating),
or the rolling contract window is genuinely unimplemented. That is a scope call, not a device
question, and it is recorded as a UAT issue rather than silently re-scoped.

Note the derived figure Test 8 also asks for — *contract fidelity* — is computable from
`recent_sessions` today, so the capability may be intact even though the named container is not.

## F-3 — `exit_events` degraded to a single overwritten object (Phase 6, Test 11)

The file holds:

```json
"exit_events": {"app": "tracked", "timestamp": 1787079710, "type": "Capture", "heat": 4, "circle": 3}
```

— one object, not a list, after at least one exit was recorded.

`seed_exit_events()`'s docstring records this exact scenario as **assumption A1**, explicitly
`[ASSUMED]` and flagged as settleable only at rung 2: *"whether that is a zero-iteration no-op
or a type error is [ASSUMED]"*.

**A1 is now settled at rung 4, in the direction the docstring hoped for.** With `exit_events`
unseeded, the flat read returned nothing, the append produced a single item, and the write
stored that item as a bare object. **No error, no crash — a silent shape degradation.** The
current build seeds `exit_events: []`, so this is fixed; but the pre-fix behaviour is now a
measurement rather than an assumption, and `seed_exit_events()`'s docstring should be updated
to say so.

Also note what the event object does **not** contain: any field for *time until the next
target-app OPEN*. Phase 6 Test 11 calls that "the load-bearing field". The return time is
instead accumulated into `exit_stats.<Exit>.sum_return_seconds` (1044 s for the one Capture
event) rather than stored per event. Whether per-event retention is required is a Test 11
question for the device run.

## F-4 — A dotted `Set Dictionary Value` writes a FLAT top-level key; a dotted read prefers it

The file carries **nine top-level keys containing literal dots**, side by side with nested
containers of the same names:

```
pending_exit.type                      active_session.id
pending_exit.timestamp                 active_session.started_at
exit_stats.Capture.count               active_session.intention
exit_stats.Capture.sum_return_seconds  active_session.declared_duration_seconds
exit_stats.Capture.samples
```

The generator writes every one of these through `set_value("active_session.id", …)` etc.,
**intending a nested write**. iOS instead creates a literal flat key.

**The reciprocal finding is what makes the engine work.** `active_session.started_at` is
`1787081487` in the flat key and `"null"` in the nested container, and the newest
`recent_sessions` entry records `started_at: 1787081487` — a value CLOSE obtained through
`read_value("active_session.started_at", …)`. So a dotted **read resolves the exact flat key in
preference to traversing the nested path**.

Writes and reads therefore agree, and the whole state engine is self-consistent. This is a
new device-established runtime semantic and belongs in `.claude/CLAUDE.md`'s
*Verified iOS Shortcuts runtime semantics* table:

| construct | behaviour |
|---|---|
| dotted **write** (`set` `a.b`) | creates a literal flat top-level key `"a.b"`; the nested subtree is untouched |
| dotted **read** (`get` `a.b`) when a flat `"a.b"` key exists | returns the flat key's value; no traversal occurs |

**Two consequences worth stating plainly.**

1. **Axis 7's container seeding is still necessary, and for a subtler reason than recorded.**
   The seed is what the *first* read — before any flat write exists — falls back to. Without it
   that read traverses, hits a missing segment and hard-errors. So the rule holds; the mechanism
   in `.claude/CLAUDE.md` ("write and clear only its leaves") is describing an intent the runtime
   does not implement, because the "leaves" being written are flat keys, not leaves of the
   container. Once the flat key exists the nested container is dead weight, shadowed forever.
2. **The nested containers are silently stale, permanently.** `exit_stats.Capture.count` reads
   `1` (flat) and `0` (nested) in this very file. Anything that reads `exit_stats` *as a whole
   object* — rather than by dotted key — gets the bootstrap zeros. No such reader exists today;
   one added later would be wrong in a way nothing in the toolchain can see.

This finding was **not** previously recorded anywhere in `docs/BUILD-NOTES.md`,
`docs/CAPABILITY-DECISIONS.md` or the generator.

## F-5 — Stored epoch timestamps carry the device's UTC offset (`Now Epoch` anchor is timezone-naive)

`last_close_at` is `1787081517`. The file's own mtime is `1787045519`. The difference is
**35998 s ≈ exactly +10 h**, the paired device's AEST offset, and rendering the stored value as
*UTC* reproduces the local wall clock of the write (`2026-08-18 19:31:57`) to the second.

The mechanism is visible in the artifact's CLOCK block (`src/PROSOCHE-Dumb.xml`, actions 11–16):

```
Date  · WFDateActionMode = "Specified Date" · WFDateActionDate = "1970-01-01 00:00:00"  -> Epoch Anchor
Date  · WFDateActionMode = "Current Date"                                               -> Now Date
Get Time Between Dates · Seconds                                                        -> Now Epoch
```

`"1970-01-01 00:00:00"` is parsed in the **device's local time zone**, so the anchor sits
`offset` seconds before the true Unix epoch and every `Now Epoch` is `true_epoch + offset`.

**Severity: real, but low in ordinary use, with one genuine failure mode.**

- Harmless where it is used most: every stored timestamp shares the same offset, so all
  *differences* — session duration, elapsed-since, cooldown comparison, return-time samples —
  are exactly right. That is why F-1 recomputes 14/14.
- `behavioural_day` is unaffected: it is derived from `Now Date` via Adjust Date −4 h and Format
  Date, never from `Now Epoch`, so the day key is genuinely local and correct.
- **The failure mode is a change of offset while state is live**, i.e. a DST transition or the
  user travelling. The paired device's zone observes DST (AEST +10 → AEDT +11). Across that
  boundary the anchor moves an hour while already-stored timestamps do not, so a session opened
  before and closed after is off by 3600 s, and a `cooldown_until` written before it is
  evaluated an hour wrong. `duration_seconds` would be silently wrong, not erroneous.
- It also makes the file misleading to any human or tool reading it as a true epoch — which is
  precisely how this was found.

The fix is a timezone-anchored epoch anchor (or deriving `Now Epoch` from a formatted UTC
timestamp), and it is a one-action change in the CLOCK block. Not previously recorded.

## F-6 — Direct device confirmation of the phase-16 capture-persistence P0 (Phase 9/16)

`settings_snapshot` holds the cleared sentinel for both keys, and — decisively — **no flat
`settings_snapshot.brightness.original_value` key exists in the file at all.** Per F-4 a
persisted capture would necessarily have left one. So on this build the capture never reached
`state.json` by any path, exactly as `16-UAT.md` describes.

**This is confirmation of the defect, not of the fix.** It also carries a caveat that stops it
being over-read: this device's `circle` was `4`, and its `sequence` was `BlackMirror`, whose
Circle 4 is **Mirror**. Dim sits at Circle 7 and Silence at Circle 5 in that sequence, so
Dimming and Silence were most likely never reached — the empty snapshot is therefore *consistent
with* the P0 without independently proving a capture was attempted and lost.

The phone was at normal brightness and volume when recovered, so the `16-UAT.md` "live hazard"
did not apply to this device.

## F-7 — Not confirmable from this file

- Phase 4 Test 3 (A/B session race): no two sessions overlap; the race never occurred.
- Phase 4 Test 5 (04:00 rollover): all 14 sessions fall inside one behavioural day.
- Phase 4 Test 4 (locked-screen / app-switch CLOSE): the 8201 s session (08:16→10:33 local) is
  suggestive of a late-firing CLOSE but proves nothing about the trigger path.
- Phase 6 Tests 12/13 (explore/exploit): one exit ever recorded (`Capture`),
  `exit_selection_counter: 1`. Far below `exploit_min_observations`.
