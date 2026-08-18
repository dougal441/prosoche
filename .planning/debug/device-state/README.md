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

---

# Fresh-install session — 2026-08-18 21:45 onward (AEST)

## Environment, as measured

| Item | Measured value |
|---|---|
| Library | **Exactly one** shortcut matches "Nine Circles": `PROSOCHĒ — Nine Circles — Core`, no suffix. **The Aware fork is NOT installed** — so any Aware sub-observation in `16-UAT.md` is unrunnable this session. |
| OPEN automation | `When any of 2 apps are opened` → Text `OPEN` → Run `PROSOCHĒ — Nine Circles — Core`, **Input = Text**. Run Immediately, Notify When Run **off**. |
| CLOSE automation | `When any of 2 apps are closed` → Text `CLOSE` (**not** the `CLOSED` typo that blocked the earlier session) → same shortcut. |
| Tracked apps | **AliExpress** and **Instagram**. |
| Disk artifacts | Core `873fa3db…`, Aware `4b7c2cfb…` — both match the `16-UAT.md` header exactly. |
| `state.json` | Deleted 21:52; `PROSOCHE` folder confirmed empty before the first run. |

## F-8 — The bootstrap seed shape is a usable BUILD FINGERPRINT, and it proves this build is post-D-02

`16-UAT.md` states that which build is installed cannot be determined by inspection, because the
signer strips `WFWorkflowName` and there is no version string on device. **That is true of the
shortcut, and false of the state it writes.** The first run's fresh bootstrap produced:

```json
"settings_snapshot": {
  "brightness": {"original_value": "null"},
  "volume":     {"original_value": "null"}
}
```

**One leaf per group, both containers present, no `changed_at`, no `changed_by_session_id`.**
That is decision **D-02**'s shape and no earlier build can emit it. Compare the pre-install file
(F-6), which carries both removed leaves.

So `16-UAT.md` **Test 12's fresh-bootstrap sub-observation is PASSED**, and the same reading
independently answers the re-import precondition that file could otherwise only take on trust.
A one-line addition to that file's "How to confirm which build is installed" section is
warranted: *delete `state.json`, run once, read `settings_snapshot`.*

The rest of the seed matches `_state_template()` exactly — `schema_version: 4`, `exit_events: []`
(not the degraded single object of F-3), `recent_contracts: []`, all six `exit_stats` groups
zeroed with `samples: []`, `behavioural_day: "2026-08-18"` (correct local day at 21:58 AEST),
and — corroborating **F-4** — **zero top-level keys containing a dot**, because no dotted
`set_value` had yet run. Preserved as `state-2026-08-18T2158-fresh-bootstrap.json`.

Status read back: Fork Core, Profile **Purgatory**, Sequence **Classic**, Voice Yes, Circle 1,
Pressure 0. Classic orders the primitives `Pause, Black and White, Silence, Intention, Dim,
Eject, Mirror, Loud Mirror, Frozen` — so **Silence is Circle 3, Intention (the contract) is
Circle 4 and Dim is Circle 5**, all reachable from the manual `Test a Circle` menu.

## F-9 — FIRST RUN ONLY: the manual menu prompts twice for input the user should never see

**Observed, twice, deliberately.** On the **first** manual run against a freshly-bootstrapped
`state.json`, choosing **Status** produced, in order:

1. the Status alert (correct);
2. a **Notes-app note picker listing every note on the device**, headed only `Note`;
3. an **unlabelled free-text prompt** — an empty `Text` field with Cancel / Done and no prompt
   copy whatsoever;
4. the Notes app opened to the Control Room note.

Cancelling at step 3 ended the run. **On the second run of the identical menu path, with
`state.json` now present, Status showed its alert and ended cleanly — no picker, no text prompt,
no Notes launch.** So the behaviour is specific to the fresh-bootstrap run, not to Status.

**Why this matters more than a cosmetic wart.** It is the *first thing a new user sees*, and the
generator already carries a fix for a near-identical symptom: the comment at the Show Note gate
records *"Reported symptom: every manual menu choice ended by launching the Notes app"* and
narrows the Show Note to the `Open Control Room` case alone. That gate is intact and is **not**
what fired here — `Manual Show Note Requested` was never set on this run.

**Mechanism — narrowed, not settled.** The first run differs from the second in two ways that
move together, so this pair of observations cannot separate them:

- `State Recovery Occurred` is set by the bootstrap, which un-gates the recovery `appendnote`
  (`src/PROSOCHE-Dumb.xml` index 4293, `entity = Control Room Note`). An `appendnote` whose
  entity does not resolve is exactly what would raise a note picker, and an unresolved `text`
  is exactly what would raise a bare text prompt.
- The Control Room Note was **created during that same run** (index 4148), so `Control Room Note`
  was bound from Create Note's output rather than from the found branch's Get Item From List.

Both parameters were checked in the artifact and are **well-formed** — `entity` is a proper
`WFTextTokenAttachment` variable reference and `text` is a proper `WFTextTokenString` with its
one attachment at `{114, 1}`. So this is not one of the nine parameter-defect axes; it is a
**variable-binding or entity-resolution** failure that only file-level analysis cannot see.

**The cheap discriminating experiment, not yet run:** delete `state.json` again *while leaving
the Note in place*, then run Status. Prompts returning implicates the recovery `appendnote`;
prompts staying away implicates the Create-Note binding. It was deliberately deferred so the
clean bootstrap could be spent on the phase 4/6/16 tests instead.

**Related observation, recorded but not diagnosed:** the device already held **two** notes named
`PROSOCHĒ — Control Room` (one from Friday) before this run, and the run created a **third**
note named `PROSOCHĒ`. The Find Notes filter is `Name contains "PROSOCHĒ"` with limit 1, so all
three match and which one wins is unspecified. A rename of the note, or a user with any note
whose title contains the word, silently redirects the Control Room.

---

# Device UAT results — 2026-08-18 22:04–22:30 AEST, over iPhone Mirroring

All timestamps below are **local wall clock**. Remember F-5: every epoch inside `state.json`
is `local + 10 h`, so the two never match directly.

## F-10 — Phase 4: the CLOSE pipeline and the session race hold on the new build

Seven OPEN/CLOSE cycles were driven across the two tracked apps. Every session recorded is
**arithmetically exact** and **uniquely identified**:

| started | ended | `duration_seconds` | `ended - started` | id unique |
|---|---|---:|---:|---|
| 22:04:45 | 22:05:47 | 62 | 62 | ✔ |
| 22:07:13 | 22:08:16 | 63 | 63 | ✔ |
| 22:09:08 | 22:09:12 | 4 | 4 | ✔ |
| 22:11:04 | 22:11:24 | 20 | 20 | ✔ |
| 22:11:40 | 22:11:51 | 11 | 11 | ✔ |

`last_close_at` tracked the newest `ended_at` exactly throughout, and `active_session.id`
returned to the cleared sentinel after every CLOSE.

**The race was genuinely exercised, and it held.** At 22:11:04 an OPEN on AliExpress displayed
its Circle-3 Leaving/Continue menu; at 22:11:21 the app was left while **that menu was still on
screen and unanswered**; CLOSE fired and completed at 22:11:24, writing a correct 20 s session
**concurrently with the still-running OPEN instance**; a second app then opened at 22:11:40 and
closed at 22:11:51. No phantom session, no duplicate id, no overlapping intervals, no
corruption. That concurrency — a CLOSE writing state while an OPEN instance is parked on a
modal — is the hardest part of SESS-04 and it is now device-observed.

**The honest limit on Test 3.** The canonical `open A, open B, close A, close B` interleaving in
which **OPEN-B lands before CLOSE-A** was *not* reproduced, and may not be reachable by hand on
this device: every route out of a foreground app — Spotlight, the App Switcher, Home — fires
`App Is Closed` *first*. So what was tested is the reachable ordering, which is the one real
users produce.

**A behavioural consequence worth recording separately: invoking Spotlight ends a session.**
The 22:09:08 → 22:09:12 session is 4 s long because pulling down Spotlight over the foreground
app fires `App Is Closed`. Sessions are therefore truncated by *any* excursion, including ones
the user experiences as staying in the app. Session-duration figures should be read with that
in mind.

## F-11 — Phase 4 / G-04-4b: the intervention now identifies itself. CONFIRMED

The Leaving/Continue menu renders with real explanatory copy:

> You just opened a tracked app. PROSOCHĒ is at Circle 3.
>
> Leaving: PROSOCHĒ suggests somewhere better to go and takes you there.
> Continue: you go into the app, after this Circle's intervention.

That is the fix G-04-4b asked for — it names the Circle and says what each choice does. The
gap's own complaint (*"encountered a 'Leaving / Continue' menu popup and could not tell what it
signified"*) no longer reproduces.

## F-12 — ⚠ Phase 4/6, NEW AND SERIOUS: an OPEN's intervention can be deferred by minutes

**Observed.** After the 22:11 sequence, three consecutive OPENs (22:12:46, 22:14:06 and one at
22:15) each advanced Heat, Pressure and Circle and wrote `state.json` normally — and displayed
**nothing at all**. No Leaving/Continue menu, no primitive. The app opened clean.

Then, at **22:16**, on returning to the Home screen, the menu for the **22:12:46** OPEN
surfaced — *"PROSOCHĒ is at Circle 5"* — roughly **three and a half minutes late**, with the
triggering app long since closed.

**Why this is severe rather than cosmetic.** The product's stated core value is that when the
user reaches for a tracked app, *"PROSOCHĒ interrupts strongly enough that the user makes an
actual choice"*. An interruption that arrives three minutes later, after the app has been used
and closed, is not that. It is worse than no interruption: it trains the user to dismiss a
prompt that no longer refers to anything they are doing. State still accumulates correctly, so
this is invisible in `state.json` — only a person watching the screen can see it.

**Mechanism — hypothesis, NOT established.** The most likely trigger is the 22:11:40 OPEN on the
Screen-Time-limited app: Apple's own *"You've reached your limit"* sheet took the foreground
while PROSOCHĒ's menu was pending, and from then on Shortcuts appeared to serialise its
interactive surfaces behind that un-dismissed run. That is a plausible reading of the ordering,
not a measurement, and it should be treated as the first thing a diagnosis tries to reproduce —
ideally against a tracked app with **no** Screen Time limit, to separate the two.

## F-13 — Phase 16: the capture → apply → restore → clear cycle is DEVICE-PROVEN for volume

This is the first time in this project that an environmental primitive has been shown to change
a real device and put it back. Every step was measured numerically rather than inferred, using a
two-action probe (`Get Device Details` → `Show Content`) built on the phone.

| step | `Current Volume` (measured) | `state.json` |
|---|---:|---|
| before Silence | `1` | no capture key present |
| after **Silence** (Circle 3) | **`0.10000000149`** | flat key `settings_snapshot.volume.original_value = 1` |
| after **Emergency Restore** | **`1`** | same flat key back to `"null"` |

So: the original was **captured**, **persisted to disk before the change**, the change was
**actually applied to the device**, and Emergency Restore **restored the exact original and
cleared the sentinel**. `16-UAT.md` Tests 2, 4 and 11 all pass — **for volume**.

**This also proves F-4 was load-bearing, in the way that mattered most.** The capture landed in
a **flat top-level key**; the nested `settings_snapshot` block read `"null"` the entire time. A
tester reading only the nested block — which is what `16-UAT.md` Test 2 as written would lead
you to do — would have recorded a false negative on the very test this phase exists to pass.

## F-14 — ⚠ Phase 16: brightness cannot be settled over iPhone Mirroring. Dimming fails SAFE

Running Circle 5 (Dim) produced, verbatim:

> **Dim** — Brightness could not be captured, so nothing was changed.

and `state.json` gained **no** brightness capture key. Three direct probe readings explain it
and bound it:

| property | reading on this iPhone 15 Pro, over Mirroring |
|---|---|
| `Current Brightness` | **`0`** |
| `Current Volume` | `1` (correct) |
| `Device Is Locked` | **`No`** |

The capture gate is a numeric `> 0` test, so a `0` reading fails it and Dimming correctly
**skips the change rather than applying an unrestorable one**. **The safety property therefore
holds, and is confirmed working on hardware** — `16-UAT.md` Test 3 (the has-any-value/`> 0`
guard correctly skips) **passes**, with a clear, honest user-facing message.

**What is NOT established, and must not be recorded as though it were.** Whether
`Current Brightness` returns a usable value on a phone *in the user's hand* is **still open**.
The `0` reading is not attributable to the device being locked — the probe says it is not — so
the leading explanation is that the physical display is off while the phone is mirrored. That
is untested. **Do not promote "brightness cannot be captured on iOS 26" to a capability
verdict from this session.**

**Methodological consequence, which is the durable part.** `.claude/CLAUDE.md` §9's ladder gives
rung 3 (iPhone Mirroring) no stated ceiling; §9's *"Rung 2's ceiling"* section is the only place
a ceiling is written down. **Rung 3 has one too, and this session measured its first member:**
every brightness observation. The Dim/restore half of phase 16 needs rung 4 — the user, phone in
hand, unmirrored. Volume has no such restriction and is now settled.

## F-15 — ⚠ F-9 is broader than first recorded: it is the Note APPEND, not the first run

F-9 recorded the note picker plus unlabelled text prompt as first-run-only. **That was wrong,
and the correction sharpens it into something actionable.** The prompts recur on **every manual
menu choice that appends to the Control Room Note** — reproduced twice on **Emergency Restore**,
long after first run. Read-only **Status** stays clean, which is exactly the discriminator: it
displays the snapshot and never appends.

So the failing action is `is.workflow.actions.appendnote`, and it fails on **both** of its
parameters at once — Shortcuts asks the user to pick the note (`entity`) *and* then to type the
text (`text`). Both are **well-formed in the artifact** (`entity` a proper variable
`WFTextTokenAttachment`; `text` a proper `WFTextTokenString` with its single attachment at
`{114, 1}`), so this is not one of the nine parameter-defect axes — it is a runtime
variable-binding / entity-resolution failure, the class only a device can see.

**Aggravating factor already on record:** the device holds three notes whose names contain
`PROSOCHĒ` (two `PROSOCHĒ — Control Room`, one `PROSOCHĒ` created by this install), and the
find-or-create filter is `Name contains "PROSOCHĒ"` limit 1. Which one wins is unspecified.

## F-16 — Onboarding: the Save File grant does not generalise, and prompts recur mid-intervention

**Three separate Save File permission dialogs** were raised during ordinary use, each after
`Always Allow` had already been granted for the previous one:

1. *"…to save **1 dictionary** to a file?"* — first automated OPEN
2. *"…to save **2 dictionaries** to a file?"* — first automated CLOSE
3. *"…to save **1 dictionary and 1 number** to a file?"* — first Silence

The grant is evidently scoped to the **shape of the payload**, not to the shortcut, so a new
shape re-prompts. A separate notification-permission dialog also fired on the first CLOSE. All
of these appear **in the middle of an intervention**, on top of the tracked app, in the first
few minutes of a new install — precisely when the product is trying to establish that it is
calm and predictable.

## F-17 — `Test a Circle` exercises a primitive's UI but not its session-dependent state

Circle 4 (Intention) was driven from the manual menu: the free-text prompt
(*"What are you reaching for? (optional)"*) accepted `Watch stupid videos for ten minutes`
verbatim with no challenge, the boundary menu offered `2 / 5 / 10 / 15 / Custom`, and **Custom**
correctly raised its own numeric *"How many minutes?"* prompt. So the contract UI works, and
deliberate leisure is accepted rather than moralised at — `06-UAT.md` Tests 2, 3 and 4 are
satisfied **at the UI level**.

**But nothing persisted:** `active_session.intention` stayed `"null"` and
`declared_duration_seconds` stayed `0`, because there was no active session for
`persist_contract()` to own. That is correct behaviour, not a defect — and it means
**`Test a Circle` cannot settle any contract-persistence test.** Tests 5, 6, 8 and 9 need a real
OPEN that lands on Circle 4 with a live session.

---

# Phase 6 — exits and exit learning, 22:30–22:41 AEST

## F-18 — ⚠⚠ BLOCKER: `enabled_exits()` filters nothing, and offers disabled exits

**This is the most severe functional defect found in the session, and it is fully characterised.**

Choosing *Leaving → Choose another* presents the exit list. With the shipped profile — all six
exits enabled — the list contained **36 entries**: `Capture` ×6, `Coordinate` ×6, `Create` ×6,
`Connect` ×6, `Consult` ×6, `Close` ×6.

**The controlled experiment.** `profile_snapshot.enabled_exits` was edited on the device to
`["Capture", "Close"]` — four exits disabled — and the menu re-triggered. It then contained
**12 entries**: every one of the six canonical exits, **twice each**.

That is `6 canonical × N enabled`, measured at two values of N (36 at N=6, 12 at N=2). It
identifies the mechanism exactly: `enabled_exits()`'s **nested Repeat With Each** appends the
outer `Canonical Exit` on *every* inner iteration, i.e. its inner conditional
(`Enabled Exit Candidate` *string is* `Canonical Exit`) evaluates **TRUE unconditionally**.

**The consequence is worse than the duplication.** `Coordinate`, `Create`, `Connect` and
`Consult` were all **disabled** and were all still offered — and **`Coordinate` was selected and
fully routed**, presenting its `Reminders / Calendar` sub-menu. So the filter is not weak, it is
a **complete no-op**: a disabled exit is offered, selectable and functional.

This directly violates the canonical requirement that exploration never selects an exit the user
has disabled. **`06-UAT.md` Test 12 FAILS**, Test 10's menu is wrong, and Tests 13–14 cannot be
meaningful while the selector's counter arithmetic runs over a `6N`-item list instead of an
`N`-item one.

**Why nothing caught it before now.** `.claude/CLAUDE.md` already records that the control-flow
identifiers (`conditional`, `repeat.*`) are **absent from the ToolKit catalog entirely**, so
catalog-driven sweeps are blind to them, and that operator/operand validity is invisible in the
plist. This defect is both: a conditional, inside a repeat, whose comparator resolves wrongly at
runtime. Only a device shows it. Note the generator sets `WFConditionalActionString` **twice** at
this site — first to a bare `"￼"`, then to `token("Canonical Exit")` — which is the same
two-step pattern whose *unfinished* form caused G-04-1/G-04-3; here the second assignment is
present, so the shape is not obviously wrong and needs a device-side comparison against a
known-good conditional.

## F-19 — Phase 6 Test 11: the load-bearing field is CORRECT

The exit → return-time cycle was measured end to end:

- `Capture` exit recorded at epoch `1787092241`, with `pending_exit.type = "Capture"` and
  `pending_exit.timestamp` set.
- Next tracked OPEN at epoch `1787092494`.
- `exit_stats.Capture.sum_return_seconds` → **253**, and `1787092494 − 1787092241 = 253` exactly.
- `exit_stats.Capture.count` → 1, and `pending_exit.type` correctly cleared back to `"null"`.

So **"time until the next target-app OPEN" — the field `06-UAT.md` Test 11 calls load-bearing —
is captured correctly.** Exit-outcome recording also carries app, timestamp, type, heat and
circle. (It does **not** carry the return time *per event*; that lives only in the aggregate.
Whether §9.1 requires per-event retention is still the open scope question from F-3.)

## F-20 — The single-item list collapse is GENERAL, and it self-heals at n = 2

Three independent containers were observed collapsing to a bare object at exactly one element,
and two were then observed recovering:

| container | at n = 1 | at n = 2 |
|---|---|---|
| `recent_sessions` | bare object | **proper 2-element array** ✔ |
| `exit_events` | bare object | **proper 2-element array** ✔ |
| `exit_stats.Capture.samples` | bare scalar `253` | not yet observed at n = 2 |

**This corrects the expectation behind `seed_exit_events()`.** That fix seeds `exit_events: []`
and the fresh bootstrap does carry `[]` — yet the very first exit still wrote a bare object. **So
seeding an empty array does not prevent the collapse**; it prevents only the *unseeded* read.
The collapse is a property of how a one-item Shortcuts list serialises into the dictionary, and
`seed_exit_events()`'s docstring should be corrected to say so rather than implying the shape is
now guaranteed.

Severity is genuinely low for the two containers that self-heal — every downstream consumer here
tolerated the n=1 object and produced a correct array at n=2. It is **not** dismissible for
`exit_stats.<Exit>.samples`, which is the one §16 trims as a rolling window and the one that
feeds exploit-phase averaging; that consumer has not yet been observed at n≥2.

## F-21 — Exit routing (Test 10), partial pass

| exit | observed |
|---|---|
| Capture | ✔ sub-menu `Notes / Voice Memos / Camera`; **Notes** selected and the Notes app opened |
| Coordinate | ✔ sub-menu `Reminders / Calendar`; **Calendar** selected and Calendar opened |
| Create / Connect / Consult / Close | not yet exercised this session |

**One observation that is NOT a defect, recorded so it is not re-raised as one.** Capture → Notes
landed on the **PROSOCHĒ Control Room note**, not a blank note. The route is
`open_app("Notes")` (`tools/build_state_engine.py:1148` and the `Capture` branch of
`route_exit()`), so iOS simply restored the last-viewed note — and the last note PROSOCHĒ itself
opened is its own Control Room. Correct per the implementation; worth a product decision, since
a user sent to "capture a thought" lands in the app's settings page.

## F-22 — Circle 6 (`Eject`) behaves correctly

Choosing *Continue* at Circle 6 returned the device to the Home Screen, which is `exile()`'s
designed behaviour. Circles 1 (`Pause`), 2 (`Black and White`), 3 (`Silence`), 4 (`Intention`),
5 (`Dim`) and 6 (`Eject`) have now all been observed firing on hardware this session — the first
time more than one Circle has ever run on a real device in this project.

**Circle 2 (`Black and White`) showed its alert but the screen did not turn grey.** Phase 14
territory, recorded here only because it was observed in passing and not investigated.

---

# F-23 — The 04:00 rollover test was armed, and the HOST blocked it

A background timer was set at 22:43 to wake the session at **03:50 AEST**, ten minutes before
the behavioural-day boundary, specifically to drive a session across it. The timer fired on
schedule. **The Mac had locked itself to the login window** (`CGSSessionScreenIsLocked` present,
confirmed), and **iPhone Mirroring cannot run behind the login window**. Entering the password is
not an action I can take, so the phone became undrivable roughly nine minutes before 04:00.

`state.json` stayed readable through the iCloud mirror throughout, and its last device write is
**22:50** — so nothing ran on the phone after the session ended, and **no rollover data exists to
inspect**. Nothing about the rollover was observed. This is a host failure, not a product
result, and it must not be read as evidence either way.

**Two ways to finish it, and the second is much cheaper than the first.**

1. **The literal test** — be at the phone shortly before 04:00, open a tracked app, stay in it
   past 04:00, close a few minutes later. Confirm the spanning session's `duration_seconds`
   equals `ended_at - started_at` with no double-count and no drop, and that the **first** open
   after 04:00 flips `behavioural_day` and resets `opens_today` to `0`.

2. **The same coverage at any hour, without staying up.** The rollover branch compares the
   **stored** `behavioural_day` against the one computed at OPEN; it does not read the clock for
   anything else. So editing `behavioural_day` in `state.json` to a past date and then opening a
   tracked app exercises the reset arm exactly — and closing afterwards exercises CLOSE with the
   day having just changed underneath the session. This was the intended fallback and there was
   no time to run it. It is a fixture, not a simulation of the clock, so it settles the reset
   arithmetic but not the wall-clock boundary itself; run (1) once as well before calling the
   rollover proven.

**To avoid the repeat:** `sudo pmset -a sleep 0 displaysleep 0` plus disabling "Require password
after screen saver begins" for the session, or simply run these tests on the phone directly.

---

# Cleanup owed on the user's device — please read

Two deliberate changes were left on the phone and are **not** product behaviour:

1. **A scratch shortcut named `Show Content`** was built by hand in the Shortcuts library. It is
   two actions — `Get Device Details` → `Show Content` — and exists only as the brightness/volume
   probe that produced F-13 and F-14. **Safe to delete.** It is worth keeping if the brightness
   question is going to be re-run at rung 4, because it is the instrument for it.
2. **`state.json` was edited three times as a test fixture**, and every edit is disclosed here
   rather than left to be discovered: `profile_snapshot.enabled_exits` was reduced to
   `["Capture","Close"]` for the F-18 experiment **and restored to all six**; and
   `heat`/`gravity`/`pressure`/`circle` were lowered twice to bring Pressure back into the
   Circle 4 band so the contract tests could run at all. The final on-device values are
   `heat 5, gravity 0.5, pressure 5.5, circle 3, opens_today 13` — **accumulated behavioural
   data on that file is therefore synthetic and should not be read as real usage.** Delete
   `state.json` before any run whose numbers are meant to mean something.

Every state file from the session is preserved beside this document:
`state-2026-08-18T1931-stale-preinstall.json` (the outgoing build's, pre-delete),
`…T2158-fresh-bootstrap.json`, `…T2222-after-emergency-restore.json`,
`…T2241-after-exit-tests.json`, `…T2250-session-end.json`.
