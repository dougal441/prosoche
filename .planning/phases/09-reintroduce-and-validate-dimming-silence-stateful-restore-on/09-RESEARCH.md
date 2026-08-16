# Phase 9: Dimming/Silence Stateful Restore (Experimental Fork) - Research

**Researched:** 2026-08-16
**Domain:** Shortcuts plist generator (Python) — numeric parameter type-coercion defect + on-device capture/restore safety proof
**Confidence:** HIGH for the code-level findings (direct inspection + decrypted donor), MEDIUM for the coercion fix's exact shape (no direct donor evidence), LOW/BLOCKED for anything requiring a physical iPhone (none connected this session)

## Summary

Phase 9 has two genuinely separate halves, and the plan must not conflate them. **Half one** is a
mechanical generator fix: two action identifiers (`is.workflow.actions.setbrightness`,
`is.workflow.actions.setvolume`) are invisible to the existing numeric-operand coercion audit
because they are simply absent from the `NUMERIC_OPERAND_FIELDS` table in
`tools/build_state_engine.py` — adding two entries closes the gap structurally, the same way four
earlier numeric-operand classes were closed in cycle 14. **Half two** is a safety proof that cannot
be completed in this session: whether the coercion this project's own established pattern predicts
(`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem`) is actually correct
for a Set-action float parameter (as opposed to a conditional operand or math operand, which is all
the existing donor evidence covers) is **unverified** — Donor 10 does not contain the needed
construct — and every device-proving success criterion (2 through 6) requires a real iPhone, of
which zero are connected to this machine right now (`xcrun devicectl`: "No devices found",
consistent with the open `DIST-03` blocker in STATE.md).

A critical correction to the phase's own framing surfaced during this research: **the actual
current site count is 28 (14 `setbrightness` + 14 `setvolume`), not 18** as recorded in
`docs/BUILD-NOTES.md` §8 and repeated in the originating todo and ROADMAP.md Phase 9 criterion 1.
Direct inspection of the already-built `src/PROSOCHE-Dumb.xml`/`src/PROSOCHE-Sentient.xml` (both
generated from the current, device-confirmed `848d00e` lineage) confirms 14+14 per fork, with zero
existing coercion aggrandizements on any of them. The discrepancy is explained below (§ "Site count
correction") — it is not a sign of a broken audit, it is the todo's own historical snapshot going
stale as later cycles (specifically the "Test a Circle" 9-way unroll) added call sites after
HANDOFF.md §8 was written.

**Primary recommendation:** Treat this phase as two plans. Plan A is a pure generator change (add
two `NUMERIC_OPERAND_FIELDS` entries, regenerate, run the existing static self-checks, confirm the
build guard now fails loudly if the coercion is ever missing) that can be fully completed and
verified without a device. Plan B is a device-proving checkpoint sequence (import → on-device
visual type-check → capture/restore/force-quit/restart/overlap trials → verdict) that must be
handed to the user as a `checkpoint:human-verify` sequence, because this machine has no iPhone
attached this session and the Playground toolchain has no execution/runtime simulator.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Numeric operand coercion (generator fix) | Build tool (`tools/build_state_engine.py`, Python) | — | Pure static plist-generation concern; no device involvement |
| Brightness/volume capture (`Get Device Details`) | On-device Shortcuts runtime | State persistence (`state.json`) | Runtime read of live device state, captured into the JSON store |
| Brightness/volume apply (`Set Brightness`/`Set Volume`) | On-device Shortcuts runtime | — | Direct OS-level side effect, safety-critical |
| Restore-on-CLOSE / Emergency Restore / cooldown-expiry | On-device Shortcuts runtime | State persistence | Reads `settings_snapshot` back out of `state.json` and reapplies |
| Ownership verification (DEV-06) | On-device Shortcuts runtime (session-ID comparison) | State persistence | Currently unimplemented; any implementation is pure state-comparison logic, no new device capability needed |
| Failure-mode proof (force-quit, restart, missed CLOSE, overlap) | Physical device + human operator | — | Cannot be simulated from the build machine; Shortcuts has no headless runtime |

## Package Legitimacy Audit

Not applicable. This phase touches only the existing Python generator
(`tools/build_state_engine.py`) and the Shortcuts Playground toolchain already vetted for this
project. No new package installs.

## Site count correction — 28, not 18

`docs/BUILD-NOTES.md` §8 (cycle-14 nested-descent pass) recorded:

| field | offenders |
|---|---:|
| `setbrightness.WFBrightness` | 14 |
| `setvolume.WFVolume` | 4 |

Direct inspection of the current build (`git log` confirms `848d00e` — "close OPEN-routing debug
session — device-verified end to end" — is the tip the todo says to branch from, and it is
unchanged on this branch) shows both fields at **14 each**:

```
python3 -c "import plistlib; ..." on src/PROSOCHE-Dumb.xml and src/PROSOCHE-Sentient.xml
  setbrightness: 14 sites, 0 already coerced
  setvolume:     14 sites, 0 already coerced
```
`[VERIFIED: direct plist inspection]`

**Why the count changed.** `set_brightness()`/`set_media_volume()` (both defined once,
`tools/build_state_engine.py` lines 433–440) are called from exactly two producer functions:

- `dimming()` (line 570) and `silence()` (line 592), each invoked once per call to
  `primitive_dispatch()` (line 679).
- `restore_managed_settings()` (line 464), called at 4 fixed sites: the CLOSE owner branch
  (line 1216), the live-Ice Emergency-Restore menu (line 1450), cooldown-natural-expiry
  (`ice_expiry()`, line 1459), and the manual-menu Emergency Restore item (line 1506). These four
  map exactly onto BD-02/BD-03's documented "four restoration triggers." `[VERIFIED: code + BD-02 cross-reference]`

`primitive_dispatch()` itself is called from two places, but one of them is inside a **Python
`for test_circle in range(1, 10):` loop** in `manual_emergency_restore()` (line 1501) that builds
the "Test a Circle" menu — one full dispatch chain per Circle 1–9, unrolled at *generator* build
time, not a runtime Shortcuts Repeat. That is 1 (real dispatch, line 919) + 9 (Test-a-Circle loop)
= 10 calls to `primitive_dispatch()`, each emitting one `dimming()` (1 `setbrightness`) and one
`silence()` (1 `setvolume`) call. 10 + 4 (restore sites) = **14 setbrightness, 14 setvolume, 28
total**. `[VERIFIED: code trace + XML site-by-site confirmation — variable names "Dim Target"/"Silence Target" appear exactly 10 times each, "Restore Brightness"/"Restore Volume" exactly 4 times each]`

The HANDOFF.md snapshot's "4 setvolume" figure predates whichever cycle added Silence to the
Test-a-Circle dispatch path (or fixed a bug that had been suppressing it) — this is a documentation
staleness issue, not a code regression. **The plan must audit against the current 28, not the
historical 18**, and should correct `docs/BUILD-NOTES.md` §8 and the ROADMAP.md/todo's "18" figures
as part of its own record-keeping.

## The fix mechanism — table-driven, already proven for 4 sibling axes

`tools/build_state_engine.py`'s numeric-operand audit is fully table-driven and already handles
four other numeric-typed field classes identically:

```python
# line ~2362
NUMERIC_OPERAND_FIELDS = {
    "is.workflow.actions.math": ("WFInput", "WFMathOperand"),
    "is.workflow.actions.getitemfromlist": ("WFItemIndex",),
}
```

`_numeric_operand_sites()` (line ~2368) special-cases `conditional` and `getitemfromlist`, then
falls through to a generic `NUMERIC_OPERAND_FIELDS.get(identifier, ())` lookup for everything else.
`setbrightness`/`setvolume` are neither special-cased identifier, so **the fix is exactly two
dictionary entries**:

```python
NUMERIC_OPERAND_FIELDS = {
    "is.workflow.actions.math": ("WFInput", "WFMathOperand"),
    "is.workflow.actions.getitemfromlist": ("WFItemIndex",),
    "is.workflow.actions.setbrightness": ("WFBrightness",),
    "is.workflow.actions.setvolume": ("WFVolume",),
}
```

Both `normalise_numeric_operands()` (applies the coercion) and `verify_numeric_operands()` (the
paired build-guard assertion) consume this table generically via the shared
`_numeric_operand_report()` — no other code changes are needed to wire the fix into both the
generator and its own self-verification. `[VERIFIED: code inspection]`

**This also structurally satisfies ROADMAP.md criterion 1's "the numeric-audit build guard no
longer exempts them"** — before this change, `verify_numeric_operands()` silently skips these 28
sites because `_numeric_operand_sites()` never yields them; after, any of the 28 that resolve to a
non-numeric source will hard-fail the build with the existing, already-worded error message ("a
brightness/volume write is not numerically gated..." — actually a *different*, already-passing
guard; see next section for why these are not the same check).

### Two audits, don't conflate them

`tools/build_state_engine.py` already contains **two different, already-passing** guards near
these sites, and Phase 9 must not confuse either with the coercion fix it needs to add:

1. **`verify_restore_gates()`** (line 2119) — asserts every `setbrightness`/`setvolume` write is
   wrapped in a numeric `> 0` gate on the source variable, closing the "empty snapshot leaf passes
   `has any value` and reaches Set Brightness with nothing" defect (cycle 14j). **Already fixed,
   already enforced, not in scope for Phase 9.**
2. **The missing coercion (this phase's actual target)** — even with a numeric gate correctly
   above it, the *operand itself* (`WFBrightness`/`WFVolume`'s value descriptor) is untyped as far
   as iOS's UI is concerned unless it carries `WFCoercionVariableAggrandizement`. This is invisible
   to `verify_restore_gates()`, invisible to the validator, invisible to the ToolKit catalog, and
   invisible to a decrypted signed artifact's raw bytes — the only channel that reveals it is
   opening the built shortcut in Shortcuts.app on a real device and looking at whether the
   parameter chip renders red. `.claude/CLAUDE.md` and `docs/BUILD-NOTES.md` §15 both name this
   explicitly as the fifth defect axis found in the project's own debug history.

### Which of the 28 sites actually need the coercion (not all, mechanically)

The audit is source-tracing, not site-counting: a variable is already treated as "Number-typed"
if every `Set Variable` that can define it traces back to a `NUMERIC_SOURCE_ACTIONS` member
(`is.workflow.actions.number`, `.math`, `.getdevicedetails`, etc. — line ~2326). Tracing the
current 28 sites' source variables:

| Variable name | Set via | Numeric source? | Needs coercion? |
|---|---|---|---|
| `Restore Brightness` / `Restore Volume` (4 sites each) | `read_value()` → `is.workflow.actions.gettext` | No (Text) | **Yes** |
| `Dim Target` (10 sites) | `config("safety.dim_target", …)` → `read_value()` → `gettext` | No (Text) | **Yes** |
| `Silence Target` (10 sites) | `number(0.10, "Silence Target")` → `is.workflow.actions.number` | Yes | Likely **no**, if this name is never redefined elsewhere via a Text path |

`[VERIFIED: code trace of read_value()/config()/number() definitions]`. This means the fix will
almost certainly not add an aggrandizement to all 28 sites uniformly — `normalise_numeric_operands()`
will correctly skip the `Silence Target` sites as already-numeric. **Do not treat "coercion added to
all 28" as the success signal; treat "verify_numeric_operands() passes with the new table entries"
as the success signal**, and manually re-check the `Silence Target` sites specifically, because the
project's own "one Text definition anywhere poisons every numeric use of that name" rule
(demonstrated for `Circle Next` in `docs/BUILD-NOTES.md`) means a single stray Text-typed
redefinition of `Silence Target` anywhere in either fork would flip this classification. A grep for
`"Silence Target"` set-variable sites should be part of the plan's own verification task, not
assumed from this research alone.

## Donor 10 evidence — does NOT cover the needed construct (report honestly, not guessed)

`.planning/debug/Donor 10.shortcut` was decrypted this session using the `.claude/CLAUDE.md` §8
recipe (`aea decrypt` → `aa extract` → `plutil -convert xml1`), successfully. Its full action list:

```
1. setbrightness   — WFWorkflowActionParameters: {}   (unconfigured / no value set)
2. setvolume       — WFWorkflowActionParameters: {}   (unconfigured / no value set)
3. setvolume       — WFVolume: 0.796875 (literal), WFVolumeSetting: "Ringtone"
4. getdevicedetails — WFDeviceDetail: "Device Model"
5. getdevicedetails — WFDeviceDetail: "Current Brightness"
6. getdevicedetails — WFDeviceDetail: "Current Volume"
7. getdevicedetails — WFDeviceDetail: "Current Appearance"
8. getdevicedetails — WFDeviceDetail: "Device Is Locked"
```

`[VERIFIED: decrypted donor, device ground truth per project evidence hierarchy]`

**What this confirms, usefully:**
- `is.workflow.actions.setbrightness`/`.setvolume` and their `WFBrightness`/`WFVolume` keys are
  real, importable, device-authored action identifiers (corroborates CAP-16/CAP-18's existing
  VERIFIED status — nothing new here).
- A **literal** float value for `WFVolume` serializes as a bare `<real>0.796875</real>` — no
  envelope, no `Value`/`WFSerializationType` wrapper. This is the expected shape for a literal
  (matches every other numeric literal already in this codebase, e.g. `number(0.10, ...)`,
  `WFVolume: 0.796875`) and is not itself in question.
- `Current Brightness`/`Current Volume` are confirmed again as literal `WFDeviceDetail` enum
  cases, on device, independent of the catalog — reinforces CAP-17/CAP-19 with a second evidence
  source.

**What it does NOT confirm — the actual gap:** none of the three `setbrightness`/`setvolume`
actions in Donor 10 has a **variable-fed** operand. Two are entirely unconfigured (empty parameter
dict — the user added the action but never picked a value in the UI), and the one configured
instance uses a hand-typed literal, not a variable reference. **There is no example anywhere in
this donor of a Number-typed variable wired into `WFBrightness` or `WFVolume`, so the exact
`CoercionItemClass` (or whether a coercion is required at all in this parameter position) cannot be
read off this evidence.** This is a genuine, honestly-reported gap, not an oversight — it matches
exactly the scenario `.claude/CLAUDE.md` §"What NOT to use" row 1 warns against papering over.

**The only evidence for what coercion shape *might* apply is analogy**, not direct proof:
`WFBrightness`/`WFVolume` are catalog-confirmed (`toolkit-v78-first-party-parameter-keys.json`)
`float`-typed action parameters — the same declared type class as `math.WFMathOperand`,
`math.WFInput`, and `getitemfromlist.WFItemIndex`, all three of which were already fixed with
`WFCoercionVariableAggrandizement` / `CoercionItemClass: WFNumberContentItem` (the Donor 4.1 /
CAP-07 pattern, cross-validated against 24 corpus instances and one direct device round-trip). But
those three are all either a **conditional operand** or a **math/list-index operand** — not a
**direct Set-action parameter** — and `.claude/CLAUDE.md`'s own instructions for this phase state
explicitly this must not be assumed to transfer without verification. `[ASSUMED — by analogy to
the Donor-4.1 pattern, NOT Donor-10-verified]`.

### Recommended verification path (matches the project's own established playbook)

The project has already solved this exact category of problem once (CAP-07, `docs/BUILD-NOTES.md`
§15–16) using a technique the plan should reuse rather than reinvent:

1. Apply the coercion by analogy (`NUMBER_COERCION` = `WFCoercionVariableAggrandizement` /
   `WFNumberContentItem`) as the working hypothesis and regenerate both forks.
2. **On-device visual check** (the established "eyeball is a first-class evidence channel"
   technique): import the rebuilt shortcut on a real iPhone, open the Dimming/Silence/Restore
   actions in Shortcuts.app's editor, and confirm the `WFBrightness`/`WFVolume` parameter chip
   does **not** render red/invalid. A red chip is definitive proof the coercion shape is wrong
   for this parameter position; a normal chip plus a successful run is evidence (not absolute
   proof, but consistent with how CAP-07 itself was confirmed) that it is right.
3. If red: request a **fresh donor** built the same way Donor 4.1 was — in Shortcuts.app on the
   target iPhone, wire a Number variable into a Set Brightness action, save, export, decrypt with
   the §8 recipe — and read the literal `CoercionItemClass` (or absence of one) back, exactly as
   was done for the conditional-operand case. This is a fast, known-working, ~15-minute loop on
   this project's own evidence, not a research dead end.

This verification path belongs in Plan B (device-proving), not Plan A (generator fix) — Plan A can
ship the analogy-based fix and self-check-clean; Plan B is what actually confirms it.

## DEV-06 (restore-ownership check) — re-evaluate, don't blindly re-enable

`docs/BUILD-NOTES.md` §17 records `changed_at`/`changed_by_session_id` are written at 20 sites and
**read nowhere** — the ownership check that would use them to verify a CLOSE only restores a
change it actually owns is unimplemented. The user's 2026-08-14 decision was "leave as-is for now,
decide before ship" — main line's ship-readiness cleanup resolves this by deleting the whole
stateful design; Phase 9 is explicitly where this decision comes back live (ROADMAP.md criterion 6).

**Important finding for the planner: a naive implementation of the ownership check could make the
already-correct overlapping-session behavior worse, not better.** Trace through the existing,
already-working mechanism:

- `active_session` is a single slot (not a stack). SESS-03's session-race protocol (Phase 4,
  confirmed via `04-01-SUMMARY.md`: "CLOSE reloads state and aborts without mutating it if a newer
  OPEN owns the active session") already guarantees **only the winning (last) OPEN's CLOSE ever
  reaches the restore step** — a superseded/loser CLOSE takes a Nothing-only branch and never calls
  `restore_managed_settings()` at all.
- `dimming()`/`silence()` only capture into `settings_snapshot` when **no** unrestored snapshot
  already exists (`Brightness Snapshot`/`Volume Snapshot` has-any-value gate, condition 100). So in
  a genuinely overlapping pair (session A opens and dims, session B opens before A closes),
  session B's `dimming()` call is a complete no-op — it neither re-captures nor re-dims.
- Consequently the single winning CLOSE (session B's) is the only one that ever restores, and it
  correctly restores **session A's** captured original — which is the only true original that
  exists. This is already correct today, with **no** ownership check.

If `changed_by_session_id` is checked naively (restore only if it equals the closing session's own
ID), this exact legitimate case — B's CLOSE restoring what A captured — would be **blocked**,
because B never captured anything, so the field it wrote (see below) is empty for B and never
matches B's own session ID either way. The residual risk DEV-06 actually names is narrower than "no
ownership check exists at all" — it is specifically about a **different**, not-yet-articulated
failure mode (the entry itself only says "requires two overlapping runs where one restores what the
other captured," without specifying why that's unsafe given the above). **The plan should treat
DEV-06 as a design question to re-derive from first principles on this fork, not a checkbox to flip
on** — implementing it incorrectly could introduce a new "stuck dim, no path back except Emergency
Restore" failure mode that this phase's own success criterion 4 explicitly forbids.

Also carried forward and still true: only **2 of the 20** `changed_by_session_id` writes share
ancestry with the genuine-OPEN branch where `Session ID` is actually assigned; the other 18 record
an empty owner. **If DEV-06 is implemented, this scope defect becomes a hard prerequisite
(`docs/BUILD-NOTES.md` §17 SHIP CHECKLIST items 4→5), not an independent fix.**

## Existing CLOSE/restoration wiring — already matches BD-02/BD-03's design

Phase 4 (`04-01-SUMMARY.md`) already built the hook Phase 9 extends, not duplicates:
`restore_managed_settings("Reloaded State")` is called exactly once, inside the CLOSE
session-ownership-match branch (`tools/build_state_engine.py` line 1216), preceded by the comment
"Only the matching CLOSE owner restores captured settings. A superseded CLOSE reaches no restore or
Save File action." `[VERIFIED: code + Phase 4 SUMMARY cross-reference]`. The other three
restoration triggers BD-02/BD-03 specify are also already wired and match exactly:

| Trigger | Call site | Line |
|---|---|---|
| Owning CLOSE | `open_pipeline`'s CLOSE handler (session-ID match) | 1216 |
| Live-Ice Emergency Restore | `live_ice_redirect()` menu | 1450 |
| Cooldown-natural-expiry | `ice_expiry()` | 1459 |
| Manual-menu Emergency Restore | `manual_emergency_restore()` | 1506 |

Phase 9 does not need to build new restoration call sites — the four-trigger structure is already
in place and already validator-clean. Its job is (a) the coercion fix at all 28 write sites feeding
these four call sites plus the primitive-dispatch call sites, and (b) proving the whole loop on
device.

## State shape / bootstrap seeding — already solid, not in scope

`settings_snapshot`'s bootstrap seeding (`seed_settings_snapshot()`, `verify_state_seed()`, lines
~1866–1920) is a previously-closed defect axis (cycle 11, STATE SHAPE) with its own build-guard
assertion tying every `settings_snapshot.*` read to a bootstrap-seeded counterpart. This is solid,
already enforced, and out of scope for Phase 9 — do not re-litigate it. The one thing worth noting:
every leaf is seeded with the cleared sentinel (empty), never a fabricated number — "no capture
recorded → skip restore" fails safe by construction, consistent with SAFE-03.

## Common Pitfalls

### Pitfall 1: Assuming the CAP-07/Donor-4.1 coercion shape transfers without confirmation
**What goes wrong:** The generator ships `WFCoercionVariableAggrandizement` /
`CoercionItemClass: WFNumberContentItem` on `WFBrightness`/`WFVolume` sites, it validates and
signs cleanly (coercion aggrandizements are invisible to the bundled validator and ToolKit
catalog), and the team declares victory without ever importing on a real device.
**Why it happens:** Every other visible signal (validator pass, sign success, plist structural
correctness) looks identical whether the coercion shape is right or wrong — this is explicitly the
one defect class the project's own evidence hierarchy says only an on-device UI check can catch.
**How to avoid:** Make the on-device visual chip-color check (§ above) a named, non-skippable task
in the plan, not an optional nice-to-have.
**Warning signs:** A shipped build where the coercion was added but the phase's own success
criteria 2–7 were marked complete without ever importing on a physical iPhone.

### Pitfall 2: Treating "18" as the audit target instead of "28"
**What goes wrong:** A verification pass counts exactly 18 fixed sites, declares Success
Criterion 1 met, and misses the 10 sites contributed by the Test-a-Circle unroll.
**Why it happens:** `docs/BUILD-NOTES.md` §8 and the originating todo both say 18; that number is
now stale.
**How to avoid:** Verify against `verify_numeric_operands()` passing cleanly (which is
self-auditing across every site the table now covers), not against a fixed count. Additionally
re-run the direct plist-inspection script used in this research (grep for
`is.workflow.actions.setbrightness`/`.setvolume`, check `Aggrandizements` on each) as an
independent cross-check.
**Warning signs:** Any success-criteria checklist that references "18" as a literal target count.

### Pitfall 3: Implementing DEV-06's ownership check as a blind field-equality check
**What goes wrong:** `changed_by_session_id == active_session.id` (or similar) is added as a gate
in front of `restore_managed_settings()`; this silently blocks the legitimate
last-CLOSE-restores-first-capture case described above, converting a working restore path into a
stuck-dim/stuck-quiet failure that only Emergency Restore can clear.
**Why it happens:** The literal field names ("ownership check") suggest a simple equality test is
the obvious implementation, without tracing through what the single-slot `active_session` +
SESS-03 race protocol already guarantees.
**How to avoid:** Model the actual failure DEV-06 is protecting against explicitly (write it down
as a concrete before/after state sequence) before writing any gating code, and test the
overlapping-session device scenario both with and without the change.
**Warning signs:** A test where a legitimate single-overlap capture/restore that used to succeed
now leaves the device dim/quiet after the ownership check lands.

### Pitfall 4: Testing failure modes only in the order listed, missing interaction effects
**What goes wrong:** Force-quit, restart, missed-CLOSE, and overlapping-session are tested as four
independent scenarios; a compound case (e.g., overlapping session + force-quit of the *winning*
session before its CLOSE fires) is never exercised, and it is exactly this compound case that
would leave `settings_snapshot` populated with no CLOSE ever reaching it — the case Emergency
Restore exists for, per canonical strategy §21.
**Why it happens:** The four failure modes read as an enumerable checklist; their combinations do
not.
**How to avoid:** After the four independent trials pass, run at least one compound trial
(overlap + force-quit) before declaring the verdict.
**Warning signs:** A "works safely" verdict written after only the four independent trials.

## Runtime State Inventory

Not applicable in the rename/refactor sense — this phase adds a coercion aggrandizement to
existing action parameters and (conditionally) new ownership-check logic; it does not rename or
migrate any stored key, service configuration, or OS-registered state. `state.json`'s
`settings_snapshot` shape is unchanged by this phase (already fully seeded per the section above).
One item worth flagging as a genuine runtime-state consideration, not a rename: **any iPhone that
already has a build from before Phase 9 installed will have live, unrestored
`settings_snapshot.brightness`/`.volume` entries if a prior test run left brightness/volume dimmed
without a matching restore** (plausible given Circles 2–9 have never fired on device per
05-UAT.md). The plan's first device-import step should include an Emergency Restore tap before
beginning new trials, to start from a clean baseline rather than inheriting stale captured state
from an earlier, pre-Phase-9 test.

## Common Pitfalls — Safety Floors

Per the corrected `docs/CAPABILITY-DECISIONS.md` BD-02 addendum and `.claude/CLAUDE.md`'s
[Phase 9] note (both dated 2026-08-16, same day): the "never zero, 10-15% band" language in
canonical strategy §21 is corrected for **brightness only**, on this fork only, **contingent on**
this phase's own device proof. Concretely:

- `safety.dim_target` currently = `0.12`, `safety.brightness_floor` = `0.10` (`.planning/phases/01-capability-audit-config-foundation/01-03-PLAN.md`). These are the values shipped today.
- The addendum permits targeting "the device's true minimum" instead — but **no source in this
  repository states what that numeric `WFBrightness` float value actually is.** This is not
  documented anywhere in the bundled ToolKit catalog (there is no minimum/maximum metadata for a
  `float`-typed parameter) and was not covered by Donor 10. `[gap — must be established by device
  test, not assumed]`. The natural way to establish it: on-device, try `WFBrightness = 0.0` via
  Set Brightness and observe the actual resulting screen brightness (per the user's own report
  that iOS's practical floor is dim, not black) — this is itself one of Plan B's device tasks, not
  a value the plan should hardcode from research.
- Volume's floor language is explicitly **unchanged** by the addendum: never increase, no
  startling output. The current `silence()` implementation already writes a hardcoded literal
  `0.10` Silence Target (not routed through `Config`, unlike Dimming's `safety.dim_target`) — this
  is a minor design asymmetry worth the plan's awareness but not a stated requirement to fix.
- Regardless of what numeric floor is ultimately chosen, `SAFE-01`/`SAFE-02`/§21/§32's "Safety"
  acceptance-criteria section (`no zero brightness` / `no unsafe volume` language, still present
  verbatim in canonical strategy §21 and §32 even though the *addendum* relaxes brightness's
  floor for this fork) must be read as **corrected by the addendum for brightness specifically**,
  not silently ignored — the plan's verdict section should explicitly state which floor value it
  tested and why, since this is the one place canonical strategy text and the project's own
  same-day correction genuinely diverge, and both are legitimate project artifacts.

## Code Examples

### The two-line generator fix (Plan A's actual deliverable)

```python
# tools/build_state_engine.py, near line 2362
NUMERIC_OPERAND_FIELDS = {
    "is.workflow.actions.math": ("WFInput", "WFMathOperand"),
    "is.workflow.actions.getitemfromlist": ("WFItemIndex",),
    "is.workflow.actions.setbrightness": ("WFBrightness",),   # NEW
    "is.workflow.actions.setvolume": ("WFVolume",),           # NEW
}
```
`[VERIFIED: existing code structure, table-driven — this is the minimal correct change]`

### The Donor-4.1 coercion shape being applied by analogy (unverified for this exact position)

```json
"WFBrightness": {"Type": "Variable", "Variable": {
    "Value": {"Type": "Variable", "VariableName": "Restore Brightness",
              "Aggrandizements": [{"Type": "WFCoercionVariableAggrandizement",
                                   "CoercionItemClass": "WFNumberContentItem"}]},
    "WFSerializationType": "WFTextTokenAttachment"}}
```
`[ASSUMED — by analogy to Donor 4.1's conditional-operand shape; NOT confirmed for a direct
Set-action float parameter by any donor in this repository]`

### Site-audit script used to establish the 28-site count (reusable for the plan's own verification)

```python
import plistlib
for fork in ["Dumb", "Sentient"]:
    with open(f"src/PROSOCHE-{fork}.xml", "rb") as f:
        data = plistlib.load(f)
    counts, coerced = {}, {}
    for a in data["WFWorkflowActions"]:
        ident = a.get("WFWorkflowActionIdentifier")
        if ident in ("is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"):
            counts[ident] = counts.get(ident, 0) + 1
            field = "WFBrightness" if "brightness" in ident else "WFVolume"
            val = a["WFWorkflowActionParameters"].get(field)
            desc = val.get("Value") if isinstance(val, dict) else None
            has = isinstance(desc, dict) and any(
                x.get("Type") == "WFCoercionVariableAggrandizement"
                for x in desc.get("Aggrandizements", []))
            coerced[ident] = coerced.get(ident, 0) + (1 if has else 0)
    print(fork, counts, "coerced:", coerced)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Dimming/Silence treated as MVP-cut candidates, coercion deferred | Two-plan split: mechanical generator fix + device-proving safety verdict | This research, 2026-08-16 | Prevents the plan from treating "add coercion" and "prove it's safe" as one task with one completion signal |
| "18 deferred sites" (HANDOFF.md §8, cycle 14) | 28 sites (10 more from the Test-a-Circle 9-way unroll) | Between cycle 14 and build `848d00e` | Any audit/plan referencing "18" needs correction |
| DEV-06 framed as "implement the ownership check" | DEV-06 must be re-derived from first principles; naive implementation risks a regression | This research | Plan should not treat DEV-06 as a checkbox |

**Deprecated/outdated:** `docs/BUILD-NOTES.md` §8's 18-site table and any plan text that treats
Donor 10 as having settled the coercion-shape question — both need correction as part of this
phase's own documentation deliverables.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `CoercionItemClass: WFNumberContentItem` is the correct coercion for `setbrightness.WFBrightness`/`setvolume.WFVolume` when fed by a variable | Donor 10 evidence / Code Examples | If wrong, the fix either does nothing (chip stays red, action still fails at runtime) or is itself a new, unverified construct shipped without device confirmation — directly against `.claude/CLAUDE.md`'s do-not-fabricate rule |
| A2 | `Silence Target`'s 10 sites are already Number-typed (via `number()`) and need no coercion, having checked no Text-typed redefinition of that name exists elsewhere | Which of the 28 sites actually need coercion | If a stray Text-typed `Silence Target` definition exists elsewhere in either fork, these 10 sites would also need coercion and the audit table would need re-verification, not assumption from this research |
| A3 | The device's true minimum `WFBrightness` value is not documented anywhere and must be established by direct device test (trying `0.0`) | Common Pitfalls — Safety Floors | If the plan hardcodes a guessed floor instead of testing it, the "corrected floor" claim in BD-02's addendum remains unconfirmed as this phase's own success criterion 4 requires |
| A4 | DEV-06's residual risk is broader/different than the two-overlapping-sessions case this research traced through (BUILD-NOTES §17 does not fully specify the failure it protects against) | DEV-06 section | If the actual risk DEV-06 was written to address is something this research's trace missed, a "do not naively implement" recommendation could leave a real gap unaddressed — the plan should re-derive from first principles, not skip DEV-06 entirely on the strength of this research alone |

## Open Questions

1. **What is `WFBrightness`'s actual minimum float and does `0.0` produce the "dim, not black" result the user reported?**
   - What we know: BD-02's addendum reports a user on-device observation that the practical floor is dim, not literal black.
   - What's unclear: The exact `WFBrightness` value tested, and whether `0.0` specifically (vs. some very small non-zero value) is what was observed.
   - Recommendation: Make this an explicit device-test task in Plan B before finalizing the new dim target; do not assume `0.0` is safe without observing it.

2. **Does the analogy-based coercion (`WFNumberContentItem`) actually clear the red-chip check on `setbrightness`/`setvolume`?**
   - What we know: The identical coercion shape is confirmed correct for conditional operands, math operands, and list-index operands (all catalog-typed the same as `WFBrightness`/`WFVolume`: `float`/numeric).
   - What's unclear: Whether a **direct Set-action parameter** position behaves identically to a **comparison/computation operand** position — Donor 10 doesn't cover this.
   - Recommendation: On-device visual check first (fast); fresh donor request only if the visual check is inconclusive or shows red.

3. **What is DEV-06's actual, fully-specified failure mode?**
   - What we know: `docs/BUILD-NOTES.md` §17 states the risk narrowly ("requires two overlapping runs where one restores what the other captured") without stating why that's unsafe, and this research's trace of the existing single-slot `active_session` + SESS-03 mechanism suggests the described case is already handled correctly.
   - What's unclear: Whether there's a scenario BUILD-NOTES didn't fully write out (e.g., three-way overlap, or a capture/restore/capture-again cycle within one still-open session) that DEV-06 is actually meant to guard against.
   - Recommendation: The plan should include a design task — write out the full state-machine of capture/restore under overlap before deciding whether/how to implement DEV-06, rather than treating BUILD-NOTES §17 as a complete specification.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Generator, self-checks, donor decryption scripts | ✓ | 3.13.9 | — |
| `shortcuts` CLI (macOS) | Signing | ✓ | present (build 518.33 host) | — |
| `aea` / `aa` (AEA1 decrypt/extract) | Donor decryption | ✓ | present | — |
| macOS host OS | Signing, Playground toolchain | ✓ | macOS 26.5.2 (build 25F84) | — |
| Physical iPhone (Apple-Intelligence-capable, iOS 26.x) | ALL device-proving success criteria (2–7) | ✗ | — | None — `xcrun devicectl list devices` reports "No devices found" this session, matching the open STATE.md `DIST-03` blocker. No simulator/headless Shortcuts runtime exists for any project on this machine. |

**Missing dependencies with no fallback:**
- A connected, unlocked iPhone. Every success criterion from 2 onward (device read/write proof,
  restore-on-CLOSE proof, all four failure-mode trials, Emergency Restore recovery proof, the final
  verdict) requires physical device access and a human operator tapping through Shortcuts.app and
  the Control Room menu. The plan must express these as `checkpoint:human-verify` tasks, following
  the same pattern already used for `04-UAT.md`/`05-UAT.md`/`07-UAT.md` in this project (conducted
  via `/gsd-verify-work`, not autonomously).

**Missing dependencies with fallback:**
- None. There is no simulator or automated-execution fallback for Shortcuts.app behavior; this is
  an inherent, already-acknowledged constraint of the whole project (`TOOLKIT_SNAPSHOT.md`: "the
  validator only checks structural/plist correctness").

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Custom Python static self-checks (no third-party test framework) |
| Config file | none — each check is a standalone script/function |
| Quick run command | `python3 tools/build_state_engine.py` (runs the generator, which calls `verify_numeric_operands()`, `verify_restore_gates()`, `verify_state_seed()`, and the other build guards as hard `SystemExit` assertions — a non-zero exit means a defect was caught) |
| Full suite command | `python3 tools/build_state_engine.py && python3 docs/state_engine_self_check.py && python3 docs/phase5_self_check.py && python3 .../validate_shortcut.py src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && python3 .../validate_shortcut.py src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` |

### Phase Requirements → Test Map

No phase requirement IDs have been assigned yet (ROADMAP.md Phase 9: "Requirements: TBD"). This
table maps ROADMAP.md's seven success criteria instead, pending ID assignment during planning.

| Criterion | Behavior | Test Type | Automated Command | File Exists? |
|-----------|----------|-----------|-------------------|-------------|
| 1 | All 28 (not 18) sites carry the coercion aggrandizement; build guard no longer exempts them | static/build-guard | `python3 tools/build_state_engine.py` (must exit 0, and must fail loudly with the new table entries removed, as a negative-control check) | ✅ (existing guard, needs table entries) |
| 2 | Device read of brightness/volume returns real, correctly-typed value; has-any-value guard correctly skips on empty read | manual device | checkpoint:human-verify — no automated equivalent | ❌ Wave 0 (needs a UAT.md test entry) |
| 3 | Original value restored exactly on CLOSE | manual device | checkpoint:human-verify | ❌ Wave 0 |
| 4 | Force-quit / restart / missed-CLOSE / overlapping-session trials each restore or fail safe | manual device | checkpoint:human-verify (4 distinct trials + 1 compound trial per Pitfall 4) | ❌ Wave 0 |
| 5 | Emergency Restore recovers from every failure mode found | manual device | checkpoint:human-verify | ❌ Wave 0 |
| 6 | DEV-06 re-evaluated live on this fork | design + manual device | N/A — a design/decision deliverable, not a device test per se | ❌ Wave 0 |
| 7 | Written verdict exists | documentation | N/A | ❌ Wave 0 (the verdict document itself) |

### Sampling Rate
- **Per task commit (Plan A only):** `python3 tools/build_state_engine.py` (fast, catches the
  coercion regression immediately)
- **Per wave merge:** Full suite command above, both forks
- **Phase gate:** Full static suite green AND every Plan B checkpoint resolved (pass or documented
  fail) before `/gsd-verify-work` / the phase's written verdict

### Wave 0 Gaps
- [ ] `.planning/phases/09-.../09-UAT.md` — the device-proving test list for criteria 2–7, following the exact structure already used in `04-UAT.md`/`05-UAT.md`/`07-UAT.md` (Current Test / Context / Tests / Summary sections)
- [ ] A negative-control check that `verify_numeric_operands()` actually fails when the two new table entries are removed (proves the guard is load-bearing, not accidentally-passing)
- [ ] Documentation correction task: `docs/BUILD-NOTES.md` §8's 18-site table and any other "18" references need updating to 28, with an explanation note (this phase should carry that correction, since it's the phase that discovered the discrepancy)

*Framework install: none needed — the existing self-check scripts and validator are already in place.*

## Security Domain

### Applicable ASVS Categories

This project is a native iOS Shortcuts automation with no network surface (`DIST-08`: core
functionality has no external network dependency) and no authentication/session concept in the web
sense — most ASVS web-application categories do not apply. The one meaningfully applicable
category is around safe handling of a local, unauthenticated JSON data store and device-state
mutation, which this project already treats as its own first-class "Environmental state safety"
domain (canonical strategy §21) rather than a generic ASVS mapping.

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No auth surface — single-user, single-device, no network |
| V3 Session Management | Partially — internal only | `active_session`/`Session ID` is an internal race-protection concept (SESS-03), not a web session; already covered by Phase 4's existing race protocol, not a new Phase 9 concern |
| V4 Access Control | No | Single local user, no multi-tenant concept |
| V5 Input Validation | Yes, narrowly | The has-any-value + numeric-sanity guards already wrapping every `Get Device Details` read (BD-02/BD-03) are this project's equivalent of input validation for untrusted/absent external readings; Phase 9 must not weaken these guards while adding the coercion fix |
| V6 Cryptography | No | No cryptographic operations in scope (AEA1 decryption is a build-tool/debugging concern, not a shipped-shortcut feature) |

### Known Threat Patterns for this stack

Not classic STRIDE web threats — this project's own domain-specific safety framing (canonical
strategy §21, §32 "Safety" acceptance criteria) is the correct threat model here. Reframed in
STRIDE terms for completeness:

| Pattern | STRIDE-nearest | Standard Mitigation (already project-specified) |
|---------|--------|---------------------|
| Device left stuck at an unsafe/unrestorable brightness or volume after a crash/restart/missed-CLOSE | Denial of Service (of the device's own usability) | Emergency Restore (SAFE-05/SAFE-06), always reachable including during Ice; this phase's own success criterion 5 |
| A capture never written because the read silently returned empty/wrong-typed | Tampering (data integrity of the safety-critical snapshot) | has-any-value + numeric-sanity guard before every write (BD-02/BD-03, already implemented) |
| An overlapping session's restore reverting the wrong original, or blocking a legitimate restore | Tampering / Repudiation (which session's capture is authoritative) | The DEV-06 design question above — must be resolved carefully, not by a naive equality check |
| A fabricated/guessed coercion shape shipped without device confirmation | (project-specific: "do not fabricate an action/parameter shape") | The Donor-10-then-device-eyeball verification path documented above |

## Sources

### Primary (HIGH confidence)
- Direct code inspection: `tools/build_state_engine.py` (functions `set_brightness`,
  `set_media_volume`, `dimming`, `silence`, `restore_managed_settings`, `primitive_dispatch`,
  `manual_emergency_restore`, `NUMERIC_OPERAND_FIELDS`, `_numeric_operand_sites`,
  `normalise_numeric_operands`, `verify_numeric_operands`, `verify_restore_gates`,
  `seed_settings_snapshot`, `verify_state_seed`) — read in full, HIGH confidence
- Direct plist inspection: `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml` (current
  device-confirmed build `848d00e`) via `plistlib` — site counts and coercion-absence confirmed
  programmatically
- Decrypted `.planning/debug/Donor 10.shortcut` (this session, via `.claude/CLAUDE.md` §8 recipe:
  `aea decrypt` → `aa extract` → `plutil -convert xml1`) — device ground truth, project's own
  top-tier evidence source
- `docs/BUILD-NOTES.md` §8 (cycle-14 type audit table), §15–16 (CAP-07/Donor-4.1 coercion pattern
  and its rationale), §17 (DEV-06)
- `docs/CAPABILITY-DECISIONS.md` BD-02, BD-03, and BD-02's 2026-08-16 addendum
- `.claude/CLAUDE.md` (this project's authored conventions document, including the corrected
  Safety line and the seven generator-authoring-rule axes)
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` §21 (Environmental state safety), §32 (Agent
  acceptance criteria)
- `.planning/phases/04-close-pipeline-session-race/04-01-SUMMARY.md`
- `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`
- `.planning/phases/01-capability-audit-config-foundation/01-03-PLAN.md` (Config `safety.*` values)
- `PLUGIN_DATA/toolkit-v78-first-party-parameter-keys.json` — `is.workflow.actions.setbrightness`/`.setvolume` parameter schema (confirms `float` type, cross-platform tag)
- `git log` on `tools/build_state_engine.py`/`src/*.xml` — confirms current branch tip matches the "device-confirmed Dumb build" lineage the todo requires
- `xcrun devicectl list devices` (this session) — confirms zero connected iPhones, corroborating STATE.md's open `DIST-03` blocker

### Secondary (MEDIUM confidence)
- Analogy between `WFBrightness`/`WFVolume`'s catalog-declared `float` type and the already-fixed
  `math`/`getitemfromlist`/`conditional` numeric operand classes — reasonable, project-precedented,
  but explicitly not donor-verified for this exact parameter position

### Tertiary (LOW confidence)
- None knowingly used beyond what's marked `[ASSUMED]` above

## Metadata

**Confidence breakdown:**
- Site-count correction (28 vs 18): HIGH — direct, reproducible code + plist inspection
- Generator fix mechanism (table entries): HIGH — existing table-driven architecture, minimal change
- Coercion shape correctness for this exact parameter position: MEDIUM/LOW — analogy only, Donor 10 doesn't cover it, requires device confirmation
- DEV-06 re-evaluation: MEDIUM — traced from existing code + BUILD-NOTES, but BUILD-NOTES §17 itself under-specifies the exact risk it's protecting against
- Device-proving criteria (2-7): BLOCKED this session — no device connected; all findings here are about what the plan must ask a human to do, not about device outcomes themselves

**Research date:** 2026-08-16
**Valid until:** Re-verify before use if `tools/build_state_engine.py` receives further commits after `62012fc`, or if a new donor/device round-trip changes the coercion-shape finding — this is fast-moving, actively-debugged code, treat as valid for ~7 days or until the next commit to `tools/build_state_engine.py`, whichever is sooner.
