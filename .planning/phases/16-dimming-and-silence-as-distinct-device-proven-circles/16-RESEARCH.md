# Phase 16: Dimming and Silence as distinct device-proven Circles — Research

**Researched:** 2026-08-17
**Domain:** iOS Shortcuts environmental primitives — capture / apply / persist / restore, operand type coercion, and the evidence ladder under a standing no-device blocker
**Confidence:** HIGH for every file-level finding (measured against the built artifact and the generator this session); HIGH for the new simulator-import channel (screenshot evidence); BLOCKED for every device-behaviour claim (`xcrun devicectl list devices` → `No devices found.`, re-verified this run)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

*(CONTEXT.md was auto-generated — `workflow.skip_discuss` is true — so it records no user-elicited
decisions. The following are carried from the ROADMAP goal and are explicitly **not** at Claude's
discretion.)*

- **DEV-06** (`changed_at` / `changed_by_session_id` written at many sites, read nowhere) is
  reserved to the user per `docs/BUILD-NOTES.md` §17. Surface it as a decision; do not resolve it
  unilaterally.
- **A second `CoercionItemClass`** must never be guessed. If `WFNumberContentItem` proves wrong at
  the direct Set-action parameter position, follow `09-RESEARCH.md`'s fresh-donor protocol instead.
- **Distinct-Circle allocation** is settled by BD-06 Decision 4 — do not re-cut it.

### Claude's Discretion

All other implementation choices are at Claude's discretion — the discuss phase was skipped per
user setting. Use the ROADMAP phase goal, success criteria, and codebase conventions to guide
decisions.

### Hard environmental constraint at plan time (from CONTEXT.md, re-verified this run)

> ## ⚠ THE REASON BELOW IS RETIRED — re-measured 2026-08-18 at plan 16-06 execution time
>
> **The original assertion is struck rather than deleted, so the correction has something to
> point at, and so the record of what was believed survives.** It was true at the start of the
> 2026-08-17 session; it was already false by the time `16-CONTEXT.md`'s own CORRECTION block
> was measured later that same day, and it is false now.
>
> **Measured 2026-08-18, verbatim:** the `State` column reads `unavailable` for a
> `dougal` / `8E45671C-9E4D-54C9-AC19-2EB65747337E` / iPhone 15 Pro (`iPhone16,1`), and from
> `--json-output`: **`tunnelState: unavailable`**, `pairingState: paired`,
> `transportType: none`, `osVersionNumber: 26.6`, `productType: iPhone16,1`.
>
> **The corrected reason is "paired device present, `tunnelState: unavailable`,
> `transportType: none`; no live session to drive" — NOT "no device exists".** It has moved
> twice: 2026-08-17's correction measured `tunnelState: disconnected` with `transport: wired`.
>
> **Branch on `tunnelState` read from the JSON, never on the `State` column**, which read
> `available (paired)` on 2026-08-17 while the tunnel was down. Two facts worth carrying:
> `iPhone16,1` is Apple-Intelligence-capable, so this hardware can exercise the Aware fork when a
> session is arranged; and iOS 26.6 is inside the declared `iOS 26.x` target, so an observation
> on it is same-major-version evidence rather than an extrapolation.
>
> **Points 1, 2 and 3 below are unaffected by the correction and remain in force.** The three
> other occurrences of the retired wording in this file (in the Confidence line at the top, in
> the evidence-channel table, and in the closing measurements block) are retired by this same
> note; they are left in place as that session's record.

~~`xcrun devicectl list devices` reports **No devices found** (checked 2026-08-17, this run).~~ The
same DIST-03 blocker recorded against Phases 4, 9, 10 and 12 is still in force — **for the
corrected reason above.** The device-proving
half of this phase **cannot be executed by an autonomous run.** Plans must:

1. Do all non-device work in full — static/structural proof, checker coverage, the UAT instrument
   itself, the decisions the ROADMAP reserves.
2. Record device-gated tests as BLOCKED with a real reason, never as passed or inferred.
   Precedent: Phase 10 DIST-03, Phase 12 `verification_deferred_human`.
3. Escalate no higher on the CLAUDE.md §9 evidence ladder than the open question requires — rung 1
   (file-level) and rung 2 (simulator) work should be exhausted here so the eventual device session
   is not spent on questions a free rung could have settled.

### Deferred Ideas (OUT OF SCOPE)

None — discuss phase skipped.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (verbatim from REQUIREMENTS.md) | Research Support |
|----|---------------------------------------------|------------------|
| CIRC-03 | Silence reduces media audio only when the original value can be captured and restored, otherwise degrades safely | **Finding 1** shows the captured original is never persisted, so "can be restored" is currently false in the shipped build. The fix and its verification are specified in *The Persistence Defect* and *Don't Hand-Roll*. |
| CIRC-05 | Dimming reduces brightness only when reversible, never to zero, otherwise degrades safely | Same as CIRC-03. "Never to zero" additionally intersects the BD-02 floor decision — evidence assembled in *BD-02 — the brightness floor decision*, **not decided here**. |
| SAFE-01 | Brightness is never set to zero | Config `safety.dim_target = 0.12`, `safety.brightness_floor = 0.10`, measured in the artifact this session; `docs/environmental_restore_check.py` asserts strictly-positive-and-at-or-above-floor. |
| SAFE-02 | Volume is never increased and no startling output is produced | Measured: all 15 `setvolume` sites carry `WFVolumeSetting = "Media"`; `safety.allow_volume_increase = false`; `silence()` skips when the captured volume is already ≤ target. Structurally pinned by `environmental_restore_check.py`. |
| SAFE-03 | Any environmental setting whose original value cannot be captured is left unchanged rather than changed unrestorably | The has-any-value + `> 0` capture gate is present and correct. **But Finding 1 means a successfully-captured original is still lost**, so the *change* survives the run and the *capture* does not — the exact inversion SAFE-03 forbids. |
| SAFE-05 | Emergency Restore clears cooldown, clears the active session, and restores recoverable brightness, volume, and colour settings | `manual_emergency_restore()` calls `restore_managed_settings("State")`, clears `cooldown_until`, clears `active_session.id`, then saves. Verified present. Its *effectiveness* is nullified by Finding 1 and it has never been tapped on a device. |
| DIST-03 | Both forks import onto a real iPhone and complete a first manual run | **BLOCKED — no device.** Unchanged. See *Environment Availability*. A new rung-2 import channel (below) does **not** discharge DIST-03: the simulator is not a real iPhone and cannot host Personal Automations. |
</phase_requirements>

## Summary

This phase was scoped as "run the eleven outstanding device tests." **The research says: do not run
them yet.** A rung-1, file-level inspection performed this session — costing no device time —
found that the brightness/volume capture written by `dimming()` and `silence()` **is never
persisted to `state.json` on any path**. The `State` dictionary is saved for the last time at
action index 521, and `universal_leaving()` — which contains every `primitive_dispatch()` rendering
that fires Dimming and Silence — begins at index 524. Every save after that point writes a
*different* dictionary, `Reloaded State`, loaded fresh from disk on a later branch. CLOSE's
`restore_managed_settings("Reloaded State")` and Emergency Restore's `restore_managed_settings("State")`
both read `settings_snapshot.*.original_value` out of the file, find the cleared sentinel, fail the
`> 0` gate, and skip the restore.

The consequence is exact and it is the failure the phase brief names in its own words: **the screen
dims and nothing in the product ever un-dims it.** Before Phase 9's coercion fix these Set actions
silently no-opped, so the defect was invisible; the merge that made them live also made this live.
Running `09-UAT.md` tests 2–12 against the current build would spend the project's scarcest input —
a device session — reproducing a defect a `plistlib` script already proves, and would end with the
user's phone dim and quiet with only iOS Settings as a way back.

Two other results reduce what the eventual device session has to carry. First, the open
`CoercionItemClass` question is **narrower than `09-RESEARCH.md` recorded**: decrypting all sixteen
donors plus five archived probes this session found `Donor 7.1` action 7 carrying a
`WFCoercionVariableAggrandizement` at a **non-conditional, direct action parameter**
(`getvariable.WFVariable`, `WFDateContentItem`) — device ground truth that the mechanism is not
conditional-only — and the golden corpus carries coercions at six further non-conditional parameter
keys, eight of them on **named-variable** (`Type: Variable`) descriptors, which is exactly the shape
the generator emits. What remains genuinely unwitnessed is one narrow pair: `WFNumberContentItem` at
a float-typed system-control parameter. Second, and contradicting spike 007's recorded finding,
**the booted simulator can be made to open the Shortcuts import sheet**:
`xcrun simctl openurl <udid> "file:///abs/path.shortcut"` produced the "Add Shortcut" sheet on the
iPhone 17 Pro / iOS 26.5 simulator this session (screenshot evidence). Spike 007's `file://` attempt
was blocked by the MCP simulator tool's scheme allowlist, not by simctl — a channel it never tried.

**Primary recommendation:** plan this phase in four ordered strands — (A) prove and fix the
persistence defect at rung 1, with a build guard so it cannot return; (B) close the coercion
question as far as rungs 1–2 reach, and build a small aimed probe for the rest; (C) author one
cold-runnable device instrument that supersedes `09-UAT.md`, pinned to a rebuilt artifact's SHA-256
and batched with the adjacent device work; (D) assemble, but do not decide, DEV-06 and the BD-02
floor. Strands A, B and D complete autonomously. Strand C's *execution* is BLOCKED on DIST-03 and
must be recorded as such.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Capture the original (`Get Device Details`) | On-device Shortcuts runtime | — | Live read of device state; no build-time equivalent |
| **Persist the capture (`Save File` on `State`)** | **Generator (`tools/build_state_engine.py`)** | On-device runtime | The *ordering* of the save relative to the primitives is a pure build-time decision — this is where Finding 1 lives and where it must be fixed |
| Apply the change (`Set Brightness` / `Set Volume`) | On-device Shortcuts runtime | — | Direct OS side effect, safety-critical |
| Operand type coercion on the write | Generator (`normalise_numeric_operands`) | On-device UI (chip render) | Emitted at build time; **only** observable at runtime/UI — no file-level check can see it |
| Restore (owning CLOSE, live-Ice, cooldown expiry, Emergency Restore) | On-device Shortcuts runtime | State persistence | Reads `settings_snapshot` back out of `state.json` |
| Structural non-regression of the whole surface | Build tooling (`docs/environmental_restore_check.py`, `docs/phase9_self_check.py`) | — | Already in place; needs one new assertion (Strand A) |
| Failure-mode proof (force-quit, restart, missed CLOSE, overlap, lock) | Physical device + human operator | — | Rung 3–4 by definition; CLAUDE.md §9 "Rung 2's ceiling" names real-hardware environmental behaviour explicitly |
| Import + editor chip inspection | **Simulator (rung 2) — newly viable** | Physical device | See *The simulator import channel* — this moves off the device's plate |

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages. It touches only
`tools/build_state_engine.py`, `tools/build_sentient.py`, `docs/*.py` checkers, and the
already-vetted Shortcuts Playground toolchain (`~/.claude/plugins/cache/shortcuts-playground/1.2.1`).
Python usage is stdlib only (`plistlib`, `json`, `importlib`, `inspect`). No `npm`/`pip`/`cargo`
install appears anywhere in the phase's surface. `[VERIFIED: direct inspection of the generator and
checker imports]`

---

## Finding 1 — the capture is never persisted (P0, rung 1, settled this session)

### What the artifact actually does

Measured against `src/PROSOCHE-Dumb.xml` (4,346 actions) with `plistlib`, this session:

| Action index | What it is | Which dictionary |
|---:|---|---|
| 521 | `documentpicker.save` — `save_state()` at the end of the arithmetic block | **`State`** |
| 522 | comment: *"Circle 0 is the silent band: state has already been saved directly above…"* | — |
| 524 | `--- PHASE 6 UNIVERSAL LEAVING ---` begins | — |
| 985–1237 | `--- PHASE 5 PRIMITIVE DISPATCH ---` rendering 1 (Continue arm) | — |
| 1019 → 1027 | `Get Device Details "Current Volume"` → three `settings_snapshot.volume.*` writes | `State` |
| 1035 | `Set Volume` | — |
| 1085 | `documentpicker.save` | `Reloaded State` (the Intention/contract primitive's own arm) |
| 1105 → 1113 | `Get Device Details "Current Brightness"` → three `settings_snapshot.brightness.*` writes | `State` |
| 1122 | `Set Brightness` | — |
| 1241–1493 | `--- PHASE 5 PRIMITIVE DISPATCH ---` rendering 2 (Panic-Escape-removed arm) | same pattern |
| 1495 | `--- PHASE 6 UNIVERSAL LEAVING END ---` | — |
| 1575, 1580, 1594, 1599 | CLOSE's restore reads `settings_snapshot.brightness` / `.original_value` / `settings_snapshot.volume` / `.original_value` | **`Reloaded State`** |

Every `documentpicker.save` in the OPEN arm after index 521 writes `Reloaded State` — indices 728,
793, 881, 946 (exit recording), 1085 and 1341 (the contract primitive). `[VERIFIED: plistlib scan of
all 31 save sites, resolving each save's source through the preceding `setitemname`'s `WFInput`]`

### Why that breaks the loop

`dimming()` and `silence()` write via `set_value(...)`, whose default is `dictionary_name="State"`
(`tools/build_state_engine.py:299`). `save_state()` (`:392`) renames a **named variable** to
`state.json` and saves it — so `save_state("Reloaded State")` writes a dictionary that never
received the capture. In Shortcuts there is no shared mutable store: `State` and `Reloaded State`
are two independent per-run variables.

Therefore, in execution order on a real OPEN:

1. `save_state()` writes the file — snapshot leaves still hold the cleared sentinel.
2. `dimming()` reads `Current Brightness`, passes the `> 0` gate, writes `original_value` **into
   `State` only**, and applies `Set Brightness` at `Dim Target = 0.12`.
3. The run ends. Nothing writes `State` again.
4. CLOSE reloads the file into `Reloaded State`, reads `settings_snapshot.brightness.original_value`
   → sentinel → the `if_block("Restore Brightness", 2, number=0)` gate reads false → **restore
   skipped, silently and by design** ("skipping a restore leaves the current setting untouched,
   which is the fail-safe direction" — `restore_managed_settings()` docstring).
5. Emergency Restore, on a later run, reads `State` freshly bootstrapped from the same file →
   identical outcome.

The user is left at 12% brightness and 10% media volume with **no in-product path back**. On a
second OPEN, `dimming()`'s `if_block("Captured Brightness", 1, number=variable("Dim Target"))` sees
0.12 ≤ 0.12 and correctly declines to re-dim — so the true original is not merely unpersisted, it
is **unrecoverable after the first run**.

### The same defect on the MANUAL arm

`Test a Circle` (`manual_emergency_restore()`, generator `:1946–1949`) renders
`primitive_dispatch("Test Circle")` nine times and **calls no `save_state()` in any of those nine
menu cases**. The `State` saves in the MANUAL arm (indices 1650, 1659, 1668, 1681, 1690, 1699, 1718)
belong to the Change Profile / Change Sequence / Toggle Voice / Reset Today cases, which are
different branches of the same `Choose from Menu`; the saves at 1834, 2099, 2364, 2629, 2894, 3159,
3424, 3689, 3954 are the per-rendering contract primitive, all `Reloaded State`.

This matters for the *instrument*, not only the product: `Test a Circle → Circle 5 (Dim)` is the
obvious way to fire Dimming on a device without building Personal Automations, and as shipped it
would dim the tester's phone with no recorded capture at all.

### Why nothing caught it

- `verify_restore_gates()` asserts every snapshot-fed **write** is numerically gated. It says
  nothing about whether the capture reached disk.
- `verify_state_seed()` asserts every snapshot **read** has a bootstrap-seeded counterpart. Same
  blind spot.
- `docs/environmental_restore_check.py` pins symbols, site counts, `Media` scoping, the dim floor
  and the seed. It has no persistence assertion.
- `validate_shortcut.py` (both gates) sees only structure. Gate A passes clean; gate B reports
  exactly the one permanent `WFCreateNoteInput` waiver and nothing else — re-measured this session.
- The forks have never run this path on hardware, and before `2e2261e` the Set actions no-opped, so
  even a device run would have shown "nothing dimmed" rather than "nothing restored."

`[VERIFIED: code read of set_value/save_state/dimming/silence/close_pipeline/manual_emergency_restore
+ plistlib scan of the built artifact + full run of all three static checkers this session]`

### What the fix must respect (do not treat this as a one-line move)

The pre-primitive save is **deliberate**. The comment at `:1260–1263` states it: *"State is
persisted before any menu/Ask action. The wrapper owns all later interaction."* A menu or Ask can be
abandoned, backgrounded, or killed; a save placed after one may never run, which is precisely how
Heat/Gravity/Pressure/`active_session` would be lost. Simply relocating `save_state()` below
`universal_leaving()` trades a brightness bug for a state-loss bug and would also collide with
`verify_circle_zero_silence()`'s invariant that Circle 0 persists but shows nothing.

The shape that preserves both properties is a **second, narrow save immediately after a successful
capture**, inside the capture-succeeded arm of `dimming()`/`silence()`, before the `Set` action
runs — so the file records the original *before* the device is changed, which is the ordering SAFE-03
actually asks for and the same "safety by ordering, not detection" rule the project already relies
on for `Use Model` (there is no try/catch in Shortcuts). Costs and open points the plan must weigh,
not this research:

- Two extra `Save File` actions per `dimming()`/`silence()` rendering × 11 renderings × 2 primitives
  = up to 44 new save actions per fork, which moves `environmental_restore_check.py`'s derivation
  and every count in `phase9_self_check.py`.
- Ordering *within* the capture arm: capture → **save** → apply. Applying first and saving second
  reintroduces a window where the screen is dim and the file does not know it.
- `Test a Circle` needs the same treatment or an explicit decision that it must not fire the
  environmental primitives at all.
- Whatever is chosen needs a **new build guard** asserting "a `settings_snapshot.*.original_value`
  write is followed, on the same arm, by a `State` save before any `setbrightness`/`setvolume`" —
  plus a negative control proving the guard is load-bearing, exactly as `docs/phase9_self_check.py`
  does for the coercion table.

---

## Finding 2 — the `CoercionItemClass` question, narrowed at rung 1

### What the generator emits today

Measured in both forks: 15 `setbrightness` + 15 `setvolume` sites; 19 carry the coercion, 11 do not
(the `Silence Target` sites, `number()`-sourced and already Number-typed — correctly skipped). Both
`docs/phase9_self_check.py` and `docs/environmental_restore_check.py` pass. The emitted shape:

```xml
WFBrightness = { "Value": { "Type": "Variable",
                            "VariableName": "Restore Brightness",
                            "Aggrandizements": [ { "Type": "WFCoercionVariableAggrandizement",
                                                   "CoercionItemClass": "WFNumberContentItem" } ] },
                 "WFSerializationType": "WFTextTokenAttachment" }
```

`[VERIFIED: plistlib dump of sites 186 and 205 in src/PROSOCHE-Dumb.xml]`

### New evidence found this session

All sixteen donors in `.planning/debug/` plus the five archived device-import probes were decrypted
(AEA1 round-trip, CLAUDE.md §8 recipe — 21/21 succeeded) and swept for
`WFCoercionVariableAggrandizement`:

| Source | Site | Class | Descriptor kind |
|---|---|---|---|
| **Donor 7.1 [7]** | **`is.workflow.actions.getvariable` / `WFVariable`** | `WFDateContentItem` | `ActionOutput` |
| Donor 4.1 [2] | `conditional` / `WFInput` | `WFNumberContentItem` | `ActionOutput` |
| Donor 6 [2], [8] | `conditional` / `WFInput` | `WFStringContentItem`, `WFNumberContentItem` | `ActionOutput` |
| Donor 6.1 [2], [8], [14] | `conditional` / `WFInput` | mixed | `ActionOutput` |
| Donor 7.1 [5] | `conditional` / `WFInput` | `WFDateContentItem` | `ActionOutput` |

**Donor 7.1 action 7 is the new fact.** It is a coercion at a **non-conditional, direct action
parameter**, written by iOS on the target iPhone, and it also confirms the ordering the generator
implements — the coercion aggrandizement comes **first**, followed by
`WFDateFormatVariableAggrandizement`. `09-RESEARCH.md` recorded that all donor evidence was
conditional-operand-only; that is no longer true. `[VERIFIED: decrypted donor, device ground truth]`

The golden corpus (19 shipped shortcuts) adds position- and descriptor-generality:

| Position | Instances |
|---|---|
| `gettext.WFTextActionText` | 13 |
| `adjustdate.WFAdjustOffsetPicker` | 2 |
| `addnewevent.WFCalendarItem{AllDay,Calendar,Location,Notes}` | 4 |
| `getvalueforkey.WFInput`, `alert.WFAlertActionMessage`, `list.WFItems`, `choosefromlist.WFChooseFromListActionPrompt`, `evernote.append.WFEvernoteNotesTitleSearch`, `conditional.WFInput` | 1 each |

Descriptor kinds across those coerced sites: **`Variable` 8, `ActionOutput` 16.** The eight
named-variable instances (`Process Input`, `Repeat Item`, `Feed Items`) are the closest available
analogue to production, where all 173 coerced descriptors are `Type: Variable`.
`[VERIFIED: plistlib sweep of the bundled golden-shortcuts corpus]`

### What is still genuinely unwitnessed

1. **No `WFNumberContentItem` anywhere in the golden corpus** — the class name rests entirely on
   Donors 4.1/6/6.1, all at conditional operands.
2. **No instance, in any donor or golden shortcut, of a coercion on a float-typed system-control
   parameter** (`WFBrightness`/`WFVolume`).
3. **Whether a Number-coerced operand is actually *consumed*** by `Set Brightness` at runtime — a
   correct chip render is necessary, not sufficient.

Honest verdict: the position-generality half of `09-RESEARCH.md`'s A1 assumption is now
**supported by device ground truth plus corpus evidence**; the specific `(WFBrightness,
WFNumberContentItem)` pair remains `[ASSUMED]`. Confidence moves from LOW/MEDIUM to MEDIUM-HIGH.
**This does not license skipping the check** — CLAUDE.md is explicit that operator/operand type
validity is invisible in the plist and only the UI reveals it.

### Gate B cannot help here

Re-measured this session: `--target-macos 27 --target-platform all` on `src/PROSOCHE-Dumb.xml`
reports exactly the one waived line (`WFCreateNoteInput` on
`com.apple.mobilenotes.SharingExtension`) and nothing else. `setbrightness`/`setvolume` are legacy
`is.workflow.actions.*` identifiers, so the v78 first-party parameter catalog does not cover them and
gate B applies no unknown-key check to them at all. A clean gate B is **not** evidence about these
sites. Gate A passes clean. `[VERIFIED: both validator invocations run this session]`

---

## Finding 3 — the simulator import channel (rung 2 is wider than spike 007 recorded)

`.planning/spikes/007-unresolvable-picker-failure-mode/README.md` records, and the
`spike-findings-prosoche` skill repeats as a standing constraint: *"The booted simulator cannot
import a signed `.shortcut` through any channel tried… rung 2 tests the build, not the import."*
Its `file://` row reads *"Blocked by the tool's scheme allowlist"* — that is the **MCP simulator
tool's** allowlist, not simctl's.

Measured this session, from Bash:

```bash
xcrun simctl openurl 79A84C29-DB62-40A2-AC3F-CCB5F8192F86 "file:///tmp/probe1.shortcut"
xcrun simctl io   79A84C29-DB62-40A2-AC3F-CCB5F8192F86 screenshot /tmp/sim1.png
```

The screenshot shows the Shortcuts **import sheet** — "probe1 / Shared 17 Aug 2026", the shortcut
card, `Cancel` / `Report`, and a live **`Add Shortcut`** button. The file used was the archived,
signed `artifacts/device-import-probes/PROSOCHĒ Probe 1 — Baseline.shortcut` (22,090 bytes).
`[VERIFIED: screenshot, iPhone 17 Pro, iOS 26.5 (23F77), 2026-08-17]`

**What is settled:** the import sheet renders for a signed artifact delivered by `file://` via
`simctl openurl`. **What is not:** completing the import requires one synthesized tap on
`Add Shortcut`. This research agent has no tap tool; the executor does (CLAUDE.md §9 lists
`mcp__Claude_Code_iOS_Simulator__control` with a `tap` action). A plan task should finish the loop
and, if it lands, correct both CLAUDE.md §9's rung-2 row and the skill's evidence-and-probes
reference — the recording duty applies.

**What rung 2 could then settle, at zero device cost:**

- Whether the `WFBrightness`/`WFVolume` chip renders red or normal in the editor — the exact hard
  gate `09-UAT.md` Test 1 is, against the *current* build rather than the Phase-9 build.
- Whether `Set Brightness` accepts the coerced operand at run time, or reports *"Please choose a
  value for each parameter in this action."*
- Whether `Get Device Details → Current Brightness / Current Volume` returns a usable, correctly
  typed value in the simulator (informative, and specifically **not** promotable — see below).
- Free-riding: the still-unrun `App Picker Probe.shortcut` from spike 007, and the unaudited
  `CoercionItemClass` values for boolean/file/dictionary/entity operands that CLAUDE.md §9 already
  names as the standing rung-2 target.

**What rung 2 still may not close** (CLAUDE.md §9 "Rung 2's ceiling", unchanged by this finding):
real-hardware environmental behaviour — whether the screen physically dims and un-dims, and what
`WFBrightness = 0.0` actually looks like; Personal Automation triggers; the Control Room Note path
(`com.apple.mobilenotes` is absent from the simulator's 25 apps); Apple Intelligence. A simulator
observation is **never above `UNVERIFIED`** for anything on that list, per the evidence hierarchy.

---

## Architecture Patterns

### The capture / apply / persist / restore loop — as designed, and as built

```
                     ┌──────────────────── OPEN run ────────────────────┐
  state.json ──load──► State (dict)                                     │
                     │   arithmetic: Heat, Gravity, Pressure, Circle    │
                     │   active_session written                         │
                     │   ┌─────────────────────────────────┐            │
                     │   │  save_state()  → state.json     │ idx 521    │
                     │   └─────────────────────────────────┘            │
                     │   Circle 0 gate                                  │
                     │   universal_leaving()            ─── idx 524 ──► │
                     │     Leaving arm ──► select_exit ──► save(Reloaded State)
                     │     Continue arm ──► primitive_dispatch()        │
                     │        dimming():                                │
                     │          Get Device Details "Current Brightness" │
                     │          gate: has-any-value AND > 0             │
                     │          write settings_snapshot.brightness.* ──► State   ✗ never saved
                     │      ✗   [ MISSING: save State here ]            │
                     │          Set Brightness ← Dim Target (coerced)   │  device CHANGES
                     └──────────────────────────────────────────────────┘

                     ┌──────────────────── CLOSE run ───────────────────┐
  state.json ──load──► Reloaded State                                   │
                     │   ownership compare on active_session.id         │
                     │   restore_managed_settings("Reloaded State")     │
                     │     read settings_snapshot.brightness.original_value
                     │       → cleared sentinel  (the capture never arrived)
                     │     gate > 0 → FALSE → skip                      │  device STAYS dim
                     │   clear_snapshot(); save(Reloaded State)         │
                     └──────────────────────────────────────────────────┘

  Four restore triggers, all reading the same never-written leaves:
    owning CLOSE · live-Ice Emergency Restore · cooldown natural expiry · manual Emergency Restore
```

### Pattern 1 — capture, persist, then apply (the ordering SAFE-03 implies)

**What:** the file must record the original *before* the device is changed, not after.
**When to use:** every stateful environmental primitive, in this project and in any Shortcuts design
without try/catch.
**Why:** Shortcuts cannot catch a failure, and a run can be killed at any action boundary. If the
apply precedes the persist, there is a window — however short — in which the device is changed and
nothing on disk knows the original. Force-quit and device-restart land squarely in that window,
which is exactly what `09-UAT.md` tests 6 and 7 exist to probe. The current build makes that window
infinite.

### Pattern 2 — one dictionary per branch, saved on the branch that owns it

**What:** `State` (bootstrap-loaded) and `Reloaded State` (re-read after the CLOSE wait) are distinct
variables; `save_state(source)` writes exactly one of them.
**Anti-pattern to avoid:** assuming a `set_value(..., "State")` is visible to a later
`save_state("Reloaded State")`. It is not, and this is the mechanism of Finding 1. Any fix must save
**the same dictionary the capture was written into**.

### Pattern 3 — the coercion goes first in `Aggrandizements`

Donor 7.1 action 7 and golden `332c12a0` both order `WFCoercionVariableAggrandizement` before any
property/format aggrandizement, because the property is read from the coerced item.
`normalise_numeric_operands()` already does this (`existing.insert(0, ...)`). Do not disturb it.

### Anti-patterns

- **Relocating the OPEN-path `save_state()` below `universal_leaving()`** — trades a brightness bug
  for a state-loss bug and breaks the documented "persist before any menu/Ask" rule.
- **Implementing DEV-06 as a field-equality check** — `09-UAT.md`'s own first-principles write-up
  traces exactly how that blocks the legitimate last-CLOSE-restores-first-capture case. Still true.
- **Treating a clean gate B as evidence about `setbrightness`/`setvolume`** — those identifiers are
  not in the v78 parameter catalog; gate B checks nothing there.
- **Editing a checker's expected count to match a new build** without deriving the delta.
  `environmental_restore_check.py` says this in its own comments; Strand A will move those counts and
  must move them by exactly what the change explains.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Proving the coercion shape is right | A second, guessed `CoercionItemClass` | Rung-2 editor inspection, then `09-RESEARCH.md`'s fresh-donor protocol if red | CONTEXT.md locks this; CLAUDE.md's do-not-fabricate rule governs |
| Re-deriving site counts | A hand-maintained list of indices | `docs/phase9_self_check.py` + `docs/environmental_restore_check.py`, updated with a written derivation | Both already exist, both carry their derivations in comments, both passed this session |
| Proving a new build guard is load-bearing | A prose claim | The negative-control idiom in `docs/phase9_self_check.py::negative_control()` | Already written, already proven for the coercion table; copy its shape |
| Recovering what actually shipped | Trusting the unsigned XML plus an mtime | `aea decrypt` → `aa extract` → `plutil -convert xml1` (CLAUDE.md §8) | 21/21 artifacts round-tripped cleanly this session |
| A device-session script | A fresh ad-hoc checklist | `12-UAT.md`'s cold-runnable structure — build identity header with SHA-256, "why device-only", Setup, per-test Setup/Sequence/Expected/Failure-evidence/`outcome:` | It is this project's best instrument and is already device-ready in form |
| Firing a Circle on device | Building Personal Automations first | `Test a Circle` in the MANUAL menu | Reaches `primitive_dispatch()` with no automation — **but see Finding 1: it persists nothing** |

**Key insight:** everything this phase needs already exists as tooling. The only genuinely new
artifacts are one build guard, one persistence fix, one aimed probe, and one UAT instrument.

---

## Common Pitfalls

### Pitfall 1: Spending the device session on a defect a script already proves
**What goes wrong:** the plan opens with "run `09-UAT.md` tests 2–12," the tester dims their phone,
CLOSE does not restore, Emergency Restore does not restore, and the session ends with a known
result and a dim phone.
**Why it happens:** the ROADMAP wrote the deliverable as "run the eleven tests," and the persistence
defect was not known when it was written.
**How to avoid:** fix and re-verify Finding 1 first; rebuild and re-sign; pin the instrument to the
new SHA-256. Make the device session the *last* thing the phase asks for.
**Warning signs:** any plan task that runs `09-UAT.md` against `ea7a0f4`'s artifacts.

### Pitfall 2: Treating `09-UAT.md`'s single pass as still valid
**What goes wrong:** Test 1 (`result: pass`) is carried forward as settled.
**Why it happens:** `09-UAT.md` has **no build-identity header** — no commit, no SHA-256, no byte
count. Since it was written the forks were renamed Dumb→Core / Sentient→Aware (BD-06-A4), gained an
eleventh `primitive_dispatch()` rendering (14/14 → 15/15 sites), bumped `schema_version` twice
(2→3→4), and were re-signed at `ea7a0f4`. The pass was also a *spot check*, by its own recorded
reason, not a sweep.
**How to avoid:** supersede `09-UAT.md` with a pinned instrument; re-establish Test 1 at rung 2
against the rebuilt artifact.
**Warning signs:** a summary that says "1 of 12 passed" without naming which build.

### Pitfall 3: Editing a checker's count instead of deriving the delta
**What goes wrong:** the persistence fix adds save actions; `environmental_restore_check.py`'s
`EXPECTED_SITES` or `phase9_self_check.py`'s `expected_counts` go red; someone edits the number.
**How to avoid:** both files already demand a written derivation and explain why. Add one for the
new totals, in the same comment style, and state what a *larger* delta would mean.
**Warning signs:** a diff that changes a number with no adjacent comment change.

### Pitfall 4: Compound failure modes tested only as a list
**What goes wrong:** force-quit, restart, missed CLOSE and overlap are each exercised once;
overlap + force-quit-the-winner is never run, and that is the state Emergency Restore exists for.
**How to avoid:** carry `09-RESEARCH.md` Pitfall 4 forward verbatim into the new instrument — the
compound trial is a named test, not an optional extra.

### Pitfall 5: Splitting the "screen locked mid-session" case away from Phase 18
**What goes wrong:** the same device behaviour is investigated twice, in two phases, from two
angles.
**Why it happens:** `09-UAT.md`'s ugly-cases block lists it, and so does ROADMAP Phase 18, which
says explicitly *"the two should be investigated together rather than twice."*
**How to avoid:** the instrument should reference Phase 18's spikes (`001-device-is-locked-literal`,
`002-close-automation-vs-screen-lock` — the latter already VALIDATED that screen lock fires CLOSE)
and hand the lock case to Phase 18 rather than duplicating it.

### Pitfall 6: Not batching the device session
**What goes wrong:** three separate device sessions are requested for overlapping ground.
**Why it happens:** four artifacts each own part of it — `12-UAT.md` Test 3 is already the SESS-07
brightness/volume restore test; Phase 19 sweeps all nine Circles including Dim (Classic Circle 5)
and Silence (Classic Circle 3); Phase 18 owns the lock case; this phase owns the failure modes.
**How to avoid:** state the batching explicitly in the instrument's header and in STATE.md's standing
device backlog, which already groups these as "best run in one session."

### Pitfall 7: Running the device session before Phase 13
**What goes wrong:** a blank alert or a red operator during the trials is attributed to Dimming.
**Why it happens:** ROADMAP Phase 13 (14 red-operator `WFConditionalActionString` sites, 2 blank
`WFItems` List sites) is unplanned and explicitly says *"Fixing them first means a blank Circle in
testing is a real finding rather than a known artifact."*
**How to avoid:** note the dependency in the instrument; if the session happens first, pre-record
the known artifacts so they are not misattributed.

---

## Runtime State Inventory

This is not a rename phase, but it changes what a *live* device holds, so the categories are
answered explicitly.

| Category | Items Found | Action Required |
|---|---|---|
| Stored data | `state.json` in the Shortcuts iCloud folder (`PROSOCHE/state.json`), `schema_version` 4. `settings_snapshot.{brightness,volume}.{original_value,changed_at,changed_by_session_id}` are seeded by `seed_settings_snapshot()` and, per Finding 1, **never written by a real run** — so no device carries a stale capture from a *successful* dim. | If the persistence fix lands, no migration is needed: the leaves already exist in the seed. Deleting `state.json` before the device session remains the cleanest baseline (12-UAT.md Setup step 2 precedent). |
| Live device settings (the real "runtime state" here) | **Any device that has already run a post-`2e2261e` build and reached Dimming or Silence is dim (0.12) and quiet (0.10) right now, with no capture on disk.** | Restore by hand via iOS Settings — Emergency Restore cannot help, by Finding 1. The instrument's Setup must say this in plain words before any trial. |
| Live service config | None. No n8n, no cloud service, no external dashboard. PROSOCHĒ has no network surface (`DIST-08`). | None. |
| OS-registered state | The two user-created Personal Automations (App Is Opened / Is Closed) bound to a fork **by exact display name** (`PROSOCHĒ — Nine Circles — Core` / `— Aware`). Not in git; live only on the device. | If the phase re-signs the forks under the same names, the automations keep working; a rename would break them (BD-06-A4 precedent). Do not rename. |
| Secrets / env vars | None — no secrets anywhere in this project. | None. |
| Build artifacts | `src/PROSOCHE-{Dumb,Sentient}.xml` (generated) and `artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Core,Aware}.shortcut`, with six SHA-256/byte rows in `artifacts/shortcuts/MANIFEST.md` proven by `docs/manifest_check.py` (**passed this session**). | Any generator change requires: rebuild both forks in one pass (Sentient is a fork of the built Dumb source), re-sign, refresh MANIFEST.md, re-run `manifest_check.py`, and re-pin the instrument's SHA-256. |

---

## Code Examples

### The site audit, re-run against the current build (reusable verification)

```python
import plistlib, pathlib
for fork in ("Dumb", "Sentient"):
    acts = plistlib.loads(pathlib.Path(f"src/PROSOCHE-{fork}.xml").read_bytes())["WFWorkflowActions"]
    counts, coerced = {}, {}
    for a in acts:
        ident = a.get("WFWorkflowActionIdentifier")
        if ident not in ("is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"):
            continue
        counts[ident] = counts.get(ident, 0) + 1
        field = "WFBrightness" if "brightness" in ident else "WFVolume"
        desc = a["WFWorkflowActionParameters"].get(field, {})
        desc = desc.get("Value") if isinstance(desc, dict) else None
        hit = isinstance(desc, dict) and any(
            x.get("Type") == "WFCoercionVariableAggrandizement"
            and x.get("CoercionItemClass") == "WFNumberContentItem"
            for x in desc.get("Aggrandizements", []))
        coerced[ident] = coerced.get(ident, 0) + (1 if hit else 0)
    print(fork, counts, coerced)
# measured 2026-08-17, both forks:
#   {'...setbrightness': 15, '...setvolume': 15}  {'...setbrightness': 15, '...setvolume': 4}
```

### The persistence proof (the script the plan should keep as a regression check)

```python
import plistlib, pathlib
acts = plistlib.loads(pathlib.Path("src/PROSOCHE-Dumb.xml").read_bytes())["WFWorkflowActions"]

def save_source(i):                       # a save's dictionary comes from the setitemname above it
    for j in range(i - 1, i - 4, -1):
        if acts[j].get("WFWorkflowActionIdentifier") == "is.workflow.actions.setitemname":
            v = acts[j]["WFWorkflowActionParameters"].get("WFInput", {}).get("Value", {})
            return v.get("VariableName")
    return None

saves = [(i, save_source(i)) for i, a in enumerate(acts)
         if a.get("WFWorkflowActionIdentifier") == "is.workflow.actions.documentpicker.save"]
# OPEN arm (93..1503) measured 2026-08-17:
#   221 State | 521 State | 728 793 881 946 1085 1341 Reloaded State
# universal_leaving() starts at 524 -> no State save exists after any settings_snapshot write.
```

### The donor/corpus coercion sweep (how Finding 2 was established)

```python
def coercions(actions):
    def walk(node, ident, key, out):
        if isinstance(node, dict):
            ag = node.get("Aggrandizements")
            if isinstance(ag, list) and any(
                    isinstance(a, dict) and a.get("Type") == "WFCoercionVariableAggrandizement"
                    for a in ag):
                out.append((ident, key, node.get("Type"),
                            [a.get("CoercionItemClass") for a in ag
                             if a.get("Type") == "WFCoercionVariableAggrandizement"]))
            for k, v in node.items():
                walk(v, ident, key or k, out)
        elif isinstance(node, list):
            for v in node:
                walk(v, ident, key, out)
    out = []
    for a in actions:
        for k, v in a.get("WFWorkflowActionParameters", {}).items():
            walk(v, a.get("WFWorkflowActionIdentifier"), k, out)
    return out
```

### The simulator import channel

```bash
UDID=79A84C29-DB62-40A2-AC3F-CCB5F8192F86
cp "artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut" /tmp/core.shortcut
xcrun simctl openurl "$UDID" "file:///tmp/core.shortcut"     # → Shortcuts import sheet appears
xcrun simctl io   "$UDID" screenshot /tmp/sim.png            # → shows the "Add Shortcut" button
# remaining step: one synthesized tap on "Add Shortcut" (executor's simulator-control tool)
xcrun simctl terminate "$UDID" com.apple.shortcuts           # dismiss without importing
```

---

## The device instrument — what it must look like so the session is not wasted

`09-UAT.md` should be **superseded, not edited**, for three reasons: it carries no build identity,
it names the pre-rename forks, and its test list predates Finding 1. The replacement should follow
`12-UAT.md`'s structure exactly:

1. **Build-identity header** — commit, both fork display names, byte counts and SHA-256 for each
   signed artifact, the MANIFEST row they come from, and the one-line re-verification recipe. A
   later run must be able to prove it is testing the build the file was written against.
2. **A "why device-only" section** naming, per test, which rung it needs and why nothing cheaper
   settles it — and, new this phase, which tests were **already settled at rung 1 or 2** so they are
   not re-run on hardware.
3. **A safety preamble the tester reads before anything else**: brightness and volume will actually
   change; if the phone is left dim or quiet, iOS Settings is the recovery; do not begin if the
   phone is needed for anything else in the next N minutes.
4. **Setup** — fresh-install both forks from the pinned artifacts, delete `state.json`, re-point
   both Personal Automations by exact display name, and note the pre-session brightness and volume
   **by hand, in writing**, since the whole proof is a comparison against them.
5. **Tests**, each with Setup / Sequence / Expected observation / Failure evidence to capture /
   blank `outcome:` — covering: the chip gate re-established on the new build; a real capture that
   is **visible in `state.json`** (the direct test for Finding 1 and the one that would have caught
   it); the has-any-value skip; capture → apply → restore round trip; `WFBrightness = 0.0`
   observation for BD-02; force-quit; device restart; CLOSE never fires; two overlapping sessions;
   the compound overlap + force-quit-the-winner trial; Emergency Restore after each failure mode;
   and the DEV-06 prediction cross-check.
6. **Explicit batching note** — this session should also discharge `12-UAT.md` Test 3, and should be
   scheduled with Phase 19's nine-Circle sweep and Phase 18's lock investigation. Say so in the
   header so a future reader does not schedule three sessions.
7. **A `## Verdict` placeholder** with a stated shape: demonstrated-safe or retired, citing test
   numbers per claim.

**The aimed probe.** Separately from the full-product UAT, a small standalone probe is the right
instrument for the coercion question — the same "probes and donors" doctrine spike 007 used. It
should hold: a `Text` action → `Set Variable` → `Set Brightness` fed by that variable **with** the
coercion; the same **without**; a `Get Device Details → Current Brightness` → `Show Result`; and a
restore leg. Build it with the `shortcut-builder` agent per spike CONVENTIONS.md, gate A clean, gate
B expected-waiver-only, sign it, **and simulator-test it before it reaches the user's iPhone** —
that is a standing project policy, and Finding 3 now makes it actually possible. If the coerced leg
renders red, that is the fresh-donor trigger; do not guess a second class.

---

## DEV-06 — evidence assembled, decision NOT taken

`docs/BUILD-NOTES.md` §17 reserves this to the user and §19.8 confirms it is live again because the
brightness/volume cut was cancelled. **This section supplies evidence only.**

**Measured this session, per fork** (both forks identical):

| Leaf | Write sites |
|---|---:|
| `settings_snapshot.brightness.original_value` | 15 |
| `settings_snapshot.volume.original_value` | 15 |
| `settings_snapshot.brightness.changed_at` | 11 |
| `settings_snapshot.brightness.changed_by_session_id` | 11 |
| `settings_snapshot.volume.changed_at` | 11 |
| `settings_snapshot.volume.changed_by_session_id` | 11 |

So `changed_at` + `changed_by_session_id` = **44 write sites per fork**, of which **22 are
`changed_by_session_id`**. §17's "written at 20 sites" is **stale** — the same staleness class as
the 18-vs-28 correction `09-RESEARCH.md` had to make, caused by the same Test-a-Circle unroll plus
Phase 11's eleventh rendering. `[VERIFIED: plistlib key scan of both forks]`

**Ancestry, re-derived:** `Session ID` is assigned once, in `open_pipeline()` (`:1216`).
`universal_leaving()` is called at `:1269`, after it. Of the eleven `dimming()`/`silence()`
renderings, **two** are in `universal_leaving()` (the Continue arm and the panic-escape-removed arm)
and therefore have `Session ID` in scope; **nine** are the `Test a Circle` submenu in the MANUAL arm
(`:1949`), where `Session ID` was never assigned. Per leaf: 2 of 11 with ancestry. Per fork: **4 of
22 `changed_by_session_id` writes carry a real owner, 18 record an empty one.** §17's "2 of 20 …
other 18" is arithmetically superseded even though the "18" coincidentally survives.

**Still true, and load-bearing for the decision:** `09-UAT.md`'s first-principles write-up (a) — the
single-slot `active_session` plus SESS-03's race protocol means only the winning CLOSE ever reaches
the restore, and `dimming()`/`silence()` no-op when an unrestored snapshot already exists, so the
overlap case is already correct with **no** ownership check; and (b) — a naive equality check would
block exactly that legitimate case.

**New, and it changes the shape of the question:** Finding 1 means `changed_by_session_id` is
**written into a dictionary that is never saved**, so the field does not survive the run that wrote
it. Any future ownership check would be reading a leaf that, today, no run can populate. If the
persistence fix lands, the field becomes real for the first time — which is precisely when the
decision starts to have consequences.

**The four options §17 put to the user, restated unchanged:** implement the check / drop the unused
fields / leave as-is and decide before ship / explain the risk first. **Surface these. Do not pick
one.** §17 ship-checklist item 5 (the `Session ID` scope fix) remains conditional on item 4.

---

## BD-02 — the brightness floor decision for main, evidence NOT decided

**What BD-02 says as written:** capture → has-any-value guard → `Set Brightness` in a *10–15% band,
never zero*, with per-run degrade-to-message-only. Requirement AUDIT-03.

**What the Phase 9 addendum says (2026-08-16, experimental fork only):** the "never zero" clause was
written on the premise that `WFBrightness = 0.0` yields a literal black screen. A user on-device
observation corrects that — iOS's practical minimum is dim, not black. The safety property was
always capture-and-restore, not floor avoidance. The addendum therefore permits targeting the
device's true minimum **contingent on Phase 9 device-proving the capture/restore loop under real
failure modes** — a proof that has not happened. `.claude/CLAUDE.md` repeats the correction and
labels it "provisional, not confirmed."

**What is shipped right now:** `safety.dim_target = 0.12`, `safety.brightness_floor = 0.10`,
`allow_volume_increase = false`, `ash_managed_color_filters = true` — read out of the Config literal
in the built artifact this session. `docs/environmental_restore_check.py` deliberately asserts only
*strictly positive and ≥ floor*, explicitly **not** a pinned 0.10–0.15 band, so the checker does not
re-impose the clause the addendum removed. `[VERIFIED: artifact Config literal + checker source]`

**What is missing for a decision:**

- **No source in this repository states what `WFBrightness = 0.0` actually looks like on hardware.**
  The ToolKit catalog carries no min/max for a `float` parameter; `Donor 10` has no variable-fed
  brightness example and no `0.0` literal. The only evidence is one user report, recorded but not
  re-checked. `[ASSUMED]`
- Canonical strategy §21 and §32's "Safety" acceptance criteria still read "never zero brightness"
  verbatim. The addendum corrects them for brightness only, on one fork only. Both are legitimate
  project artifacts and they genuinely diverge — a decision has to say which governs on main.
- The addendum's own contingency is unmet: the capture/restore loop is not proven, and per Finding 1
  it is currently *broken*. Relaxing a floor while the restore does not work is strictly the wrong
  order.
- Volume's floor is explicitly **unchanged** by the addendum: never increase, no startling output.
  Note the design asymmetry — `dimming()` reads `safety.dim_target` from Config, while `silence()`
  hardcodes a literal `number(0.10, "Silence Target")`. Worth the plan's awareness; not a stated
  requirement to fix.

**Surface these to the user as a decision with three shapes** — adopt the addendum on main; keep the
10–15% band on main and retire the addendum; or defer until the capture/restore loop is
device-proven (the conservative reading of the addendum's own contingency). **Do not decide it
here.**

---

## State of the Art

| Old position | Current position | When it changed | Impact |
|---|---|---|---|
| "28 sites (14+14), 0 coerced" (`09-RESEARCH.md`) | **30 sites (15+15), 19 coerced, 11 correctly not** | Phase 11 plan 11-05 added an eleventh `primitive_dispatch()` rendering | Any count in a plan must come from the checkers, not from `09-RESEARCH.md` |
| Coercion evidence is conditional-operand-only | **Donor 7.1 shows a coercion at a direct, non-conditional action parameter; the golden corpus shows eight named-variable instances across six parameter keys** | This research, 2026-08-17 | The A1 assumption narrows to one unwitnessed pair; the device gate stays, its expected outcome shifts toward "not red" |
| "The simulator cannot import a signed `.shortcut` through any channel" (spike 007) | **`xcrun simctl openurl file://…` renders the import sheet** | This research, 2026-08-17 | Rung 2 regains editor/runtime inspection; CLAUDE.md §9 and the skill's rung-2 row both need correcting |
| DEV-06 spans "20 sites" (§17) | **44 sites per fork; 4 of 22 `changed_by_session_id` writes carry a real owner** | Phase 11's eleventh rendering | §17's numbers are stale; the decision is unchanged and still the user's |
| The capture/restore loop is "built and merged, untested" | **Built, merged, and structurally incapable of restoring — the capture never reaches disk** | This research, 2026-08-17 | Reorders the phase: fix before instrument, instrument before device |

**Deprecated / outdated:** `09-UAT.md` in its entirety (no build identity, pre-rename fork names,
test list predates Finding 1); `docs/BUILD-NOTES.md` §17's "20 sites"; the ROADMAP Phase 16 text's
"28 sites (14/14)"; spike 007's and the skill's rung-2 import claim.

---

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | `CoercionItemClass: WFNumberContentItem` is correct for `setbrightness.WFBrightness` / `setvolume.WFVolume` fed by a named variable | Finding 2 | If wrong the write no-ops or the chip renders red. Position-generality is now donor- and corpus-evidenced; the specific class-at-this-parameter pair is not. **Do not guess a replacement** — fresh-donor protocol. |
| A2 | The `Silence Target` sites are genuinely Number-sourced and need no coercion | Finding 2 | If a Text-typed redefinition of that name exists anywhere in either fork, 11 more sites need coercion. `phase9_self_check.py`'s `site_audit()` currently pins 4-of-15 and passes, which is evidence but not a name-scoped grep. |
| A3 | The device's practical `WFBrightness` minimum is dim, not black | BD-02 section | One unrepeated user report. If wrong, adopting the addendum on main could produce an unusable screen. This is a decision input, and it is not confirmed. |
| A4 | A second `Save File` per capture arm is the right shape for the persistence fix | Finding 1 | An alternative (e.g. one save at the end of `primitive_dispatch()`, or restructuring which dictionary the primitives write) may be cheaper or safer. The research establishes the **defect**; the **fix shape** is a design decision for the plan. |
| A5 | Tapping "Add Shortcut" completes the simulator import | Finding 3 | The sheet is proven; the tap is not. If the tap fails or the import is rejected, rung 2 reverts to build-only and the chip gate returns to the device's plate. |
| A6 | The two `universal_leaving()` renderings are the only ones with `Session ID` in scope | DEV-06 section | Derived from generator call ordering (`:1216` before `:1269`), not from a runtime observation. If a third path assigns `Session ID`, the 4-of-22 figure moves. |

---

## Open Questions

1. **Does the coerced operand actually drive `Set Brightness` at run time?**
   - Known: the shape validates, signs, and matches the donor/corpus aggrandizement family.
   - Unclear: whether iOS *consumes* it at a float system-control parameter.
   - Recommendation: rung-2 probe first (chip render + a live run in the simulator); device only if
     rung 2 is inconclusive or red.

2. **What does `WFBrightness = 0.0` look like on real hardware?**
   - Known: one user report says dim, not black.
   - Unclear: everything else, including whether the report was `0.0` specifically or a small
     non-zero value.
   - Recommendation: a named device test, and an explicit input to the BD-02 decision. Never a
     hard-coded floor change ahead of the observation.

3. **What fix shape for Finding 1?**
   - Known: the defect, its mechanism, and why the naive relocation is wrong.
   - Unclear: save-per-capture-arm vs. a single post-dispatch save vs. restructuring the primitives
     to write `Reloaded State`; and what `Test a Circle` should do.
   - Recommendation: a short design task at the head of the plan, written down as a before/after
     action-order trace, then one guard that pins whichever shape is chosen.

4. **Does `Get Device Details → Current Brightness` return a usable value in the simulator?**
   - Known: the literal is donor-confirmed; the simulator has no physical display.
   - Unclear: whether the read returns a plausible number, an empty value, or a fixed constant.
   - Recommendation: observe at rung 2 — a null read there is a useful *probe-design* signal (it
     exercises the has-any-value skip path for free) but is **never promotable** above `UNVERIFIED`
     for the device, per CLAUDE.md §9's ceiling.

5. **Is `dimming()`'s `already dim → do nothing` arm reachable in a way that strands the user?**
   - Known: `if_block("Captured Brightness", 1, number=variable("Dim Target"))` skips the write when
     the captured value is ≤ target — but the capture has **already been written to `State`** by that
     point.
   - Unclear: with the persistence fix in place, whether that ordering could persist a snapshot for a
     change that never happened, so a later restore "restores" a value that was never altered.
   - Recommendation: trace it in the plan; benign today only because nothing persists.

---

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|---|---|---|---|---|
| Python 3 | generator, checkers, donor decryption | ✓ | 3.13.x | — |
| `shortcuts` CLI | signing | ✓ | present (`run`/`list`/`view`/`sign`; **no import verb**) | — |
| `aea` / `aa` | AEA1 donor round-trip | ✓ | present — 21/21 artifacts decrypted this session | — |
| Shortcuts Playground v1.2.1 | validate + sign | ✓ | gate A clean, gate B expected-waiver-only, both re-run this session | — |
| iOS Simulator | rung-2 probe | ✓ | one runtime, **iOS 26.5 (23F77)**; iPhone 17 Pro `79A84C29-…` **Booted**; `com.apple.shortcuts` present | — |
| Simulator import channel | rung-2 editor/runtime inspection | ✓ (sheet) / ✗ (tap) | `simctl openurl file://` renders the sheet; completing it needs a tap tool this research agent lacks | Executor's simulator-control tool; else defer to device |
| `com.apple.mobilenotes` on the simulator | Control Room Note path | ✗ | absent from the simulator's 25 apps | None — rung 3+ |
| Apple Intelligence on the simulator | Aware fork's `Use Model` | ✗ | not AI-capable hardware | None — rung 3+. Out of scope for this phase. |
| **Physical iPhone, iOS 26.x** | every failure-mode trial, Emergency Restore, Personal Automations, real brightness/volume behaviour | **✗** | `xcrun devicectl list devices` → `No devices found.` (2026-08-17, this run) | **None.** DIST-03 remains open. |

**Missing dependencies with no fallback:** a connected iPhone. Every trial in the "ugly cases" block,
the Emergency Restore tap, and DIST-03 itself require it and a human operator.

**Missing dependencies with fallback:** the chip gate, the coercion runtime question, and import
success now have a rung-2 fallback (Finding 3) — pending the tap.

---

## Validation Architecture

### Test framework

| Property | Value |
|---|---|
| Framework | Custom Python static self-checks — no third-party test framework |
| Config file | none; each check is a standalone script |
| Quick run | `python3 tools/build_state_engine.py` (build guards are hard `SystemExit`s) |
| Full suite | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && python3 docs/state_engine_self_check.py && python3 docs/phase9_self_check.py && python3 docs/environmental_restore_check.py && python3 docs/manifest_check.py && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all && validate-shortcut src/PROSOCHE-Sentient.xml --target-macos 26 --target-platform all` |
| Gate B | `validate-shortcut <fork> --target-macos 27 --target-platform all` — **advisory**, expect exit 1 with exactly the one `WFCreateNoteInput` line. Never chain into a definition of done. |

Baseline measured this session, before any Phase 16 change: `environmental restore check: passed`,
`phase9 self-check: passed` (30/30 sites, 19 coerced), `manifest check: passed` (6 rows), gate A
`Validation passed.`, gate B one waived line.

### Requirements → test map

| Req | Behaviour | Test type | Automated command | Exists? |
|---|---|---|---|---|
| CIRC-03 / CIRC-05 | a captured original is **persisted** before the device is changed | static / build guard | new guard in `tools/build_state_engine.py`, run by the generator | ❌ Wave 0 |
| CIRC-03 / CIRC-05 | the guard is load-bearing | static negative control | new function in `docs/phase9_self_check.py`, mirroring `negative_control()` | ❌ Wave 0 |
| CIRC-03 / CIRC-05 | capture → apply → restore closes on hardware | manual device | `checkpoint:human-verify` — no automated equivalent | ❌ Wave 0 (instrument) |
| SAFE-01 | `dim_target > 0` and ≥ `brightness_floor` | static | `python3 docs/environmental_restore_check.py` | ✅ |
| SAFE-02 | every volume write is `Media`; `allow_volume_increase` false | static | `python3 docs/environmental_restore_check.py` | ✅ |
| SAFE-03 | no change without a capture, and the capture survives the run | static + device | new guard (above) + instrument | ❌ Wave 0 |
| SAFE-05 | Emergency Restore restores, clears cooldown and the session | static presence ✅ / device effect ❌ | `environmental_restore_check.py` asserts the call; only a device proves the effect | partial |
| DIST-03 | both forks import and complete a first manual run on a real iPhone | manual device | `checkpoint:human-verify` | ❌ BLOCKED |
| — | coercion split unchanged after the persistence fix | static | `python3 docs/phase9_self_check.py` (counts re-derived) | ✅ (needs new derivation) |
| — | chip renders normally on the rebuilt artifact | rung-2 simulator | simulator import + editor screenshot | ❌ Wave 0 |

### Sampling rate

- **Per task commit:** `python3 tools/build_state_engine.py` — the guards fire immediately.
- **Per wave merge:** the full suite above, both forks, plus `manifest_check.py` if artifacts moved.
- **Phase gate:** full static suite green, rung-2 findings recorded, instrument authored and pinned,
  DEV-06 and BD-02 surfaced — and the device tests recorded **BLOCKED with a real reason**, never
  inferred.

### Wave 0 gaps

- [ ] A build guard asserting capture-before-change **persistence** (covers CIRC-03, CIRC-05, SAFE-03)
- [ ] Its negative control in `docs/phase9_self_check.py`
- [ ] Re-derived site counts in `docs/environmental_restore_check.py` and `docs/phase9_self_check.py`
      after the fix moves them, each with a written derivation
- [ ] `16-UAT.md` — cold-runnable, build-identity-pinned, superseding `09-UAT.md`
- [ ] The aimed coercion probe (build → gate A → sign → **simulator-test** → archive under
      `.planning/spikes/` per CONVENTIONS.md)
- [ ] Documentation corrections: `docs/BUILD-NOTES.md` §17's site count; CLAUDE.md §9's rung-2 row;
      the skill's `evidence-and-probes.md` rung-2 table; `09-UAT.md` marked superseded

*Framework install: none needed.*

---

## Security Domain

`security_enforcement` is true in `.planning/config.json`, ASVS level 1. This is a single-user,
single-device, network-free iOS automation (`DIST-08`), so most ASVS web categories do not apply.

| ASVS category | Applies | Standard control |
|---|---|---|
| V2 Authentication | No | No auth surface — no accounts, no network |
| V3 Session Management | Internal only | `active_session` / `Session ID` is a race-protection concept (SESS-03), not a web session. Unchanged by this phase, but DEV-06 sits adjacent to it. |
| V4 Access Control | No | Single local user |
| V5 Input Validation | **Yes, narrowly** | The has-any-value + numeric `> 0` guards around every `Get Device Details` read are this project's input validation for an untrusted/absent external reading. **This phase must not weaken them** — Finding 1's fix adds a save, it must not touch a gate. |
| V6 Cryptography | No | AEA1 decryption is a build/debug tool, not a shipped feature |
| V7 Error Handling / Logging | Partially | Shortcuts has no try/catch; safety is achieved by **ordering**. That is the whole substance of Pattern 1. |

### Threat patterns for this stack

| Pattern | STRIDE-nearest | Mitigation |
|---|---|---|
| Device left dim/quiet after a crash, restart, or missed CLOSE | Denial of Service (of the device's own usability) | Emergency Restore (SAFE-05) — **currently ineffective by Finding 1**; the persistence fix is the actual mitigation |
| A capture written but never persisted | Tampering (integrity of the safety-critical snapshot) | **Finding 1 — this is the live instance of this threat, not a hypothetical** |
| A capture never taken because the read returned empty | Tampering | has-any-value + `> 0` guard, already correct |
| Volume raised, or the ringer touched | Denial of Service / startling output | `WFVolumeSetting = "Media"` at all 15 sites + `allow_volume_increase: false`, pinned structurally |
| An overlapping session restoring the wrong original, or a check blocking a legitimate restore | Tampering / Repudiation | DEV-06 — user's decision; a naive equality check is the documented wrong answer |
| A guessed coercion class shipped without confirmation | project-specific: do-not-fabricate | Rung-2 chip check, then the fresh-donor protocol |

---

## Sources

### Primary (HIGH confidence)

- Direct code read: `tools/build_state_engine.py` — `set_value`, `read_value`, `save_state`,
  `device_detail`, `set_brightness`, `set_media_volume`, `clear_snapshot`,
  `restore_managed_settings`, `dimming`, `silence`, `primitive_dispatch`, `universal_leaving`,
  `open_pipeline`, `close_pipeline`, `manual_emergency_restore`, `NUMERIC_OPERAND_FIELDS`,
  `_numeric_operand_report`, `normalise_numeric_operands`, `verify_numeric_operands`
- Direct artifact inspection via `plistlib`: `src/PROSOCHE-Dumb.xml` (4,346 actions) and
  `src/PROSOCHE-Sentient.xml` (4,414) — site counts, coercion split, save-source resolution,
  marker-comment map, Config literal, `settings_snapshot` write census
- **Decrypted this session:** all 16 donors in `.planning/debug/` and 5 archived probes in
  `artifacts/device-import-probes/` — 21/21 clean AEA1 round-trips. Donor 7.1's non-conditional
  coercion is device ground truth (evidence-hierarchy tier 1)
- Bundled golden-shortcut corpus (19 XMLs) — coercion position and descriptor-kind sweep
- **Measured this session:** `xcrun devicectl list devices` → `No devices found.`;
  `xcrun simctl list runtimes/devices` → iOS 26.5 (23F77), iPhone 17 Pro booted;
  `xcrun simctl openurl file://…` → Shortcuts import sheet (screenshot)
- Static checkers run clean this session: `docs/environmental_restore_check.py`,
  `docs/phase9_self_check.py`, `docs/manifest_check.py`
- Validator, both gates, run this session against `src/PROSOCHE-Dumb.xml`
- `docs/BUILD-NOTES.md` §17 (DEV-06), §19.8 (DEV-06 live again), §22 (gate baselines)
- `docs/CAPABILITY-DECISIONS.md` BD-02 + its Phase 9 addendum, BD-03, BD-06 Decision 4/5, BD-06-A4
- `.planning/phases/09-…/09-RESEARCH.md`, `09-UAT.md`; `.planning/phases/12-…/12-UAT.md`
- `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/ROADMAP.md` Phases 13–19
- `.claude/CLAUDE.md` §1, §8, §9, `## Conventions`; `Skill("spike-findings-prosoche")` references
  `evidence-and-probes.md` and `environmental-primitives.md`
- `.planning/spikes/007-unresolvable-picker-failure-mode/README.md`, `CONVENTIONS.md`, `MANIFEST.md`

### Secondary (MEDIUM confidence)

- The analogy from the golden corpus's non-conditional coercion positions to `WFBrightness` /
  `WFVolume` — corpus is evidence tier 3, and no corpus instance uses `WFNumberContentItem`
- The derivation that exactly two `dimming()`/`silence()` renderings carry `Session ID` — from
  generator call ordering, not a runtime observation

### Tertiary (LOW confidence)

- The user's single on-device report that `WFBrightness = 0.0` is dim rather than black — recorded
  in BD-02's addendum, never re-checked, and marked `[ASSUMED]` throughout

---

## Metadata

**Confidence breakdown**

- Finding 1 (capture never persisted): **HIGH** — three independent reads agree (generator source,
  artifact action ordering, save-source resolution across all 31 save sites)
- Site counts and coercion split: **HIGH** — measured, and both checkers pass against the same numbers
- Finding 2 (coercion position-generality): **HIGH** for the donor and corpus facts; **MEDIUM** for
  the transfer to `WFBrightness`/`WFVolume`; the specific pair stays `[ASSUMED]`
- Finding 3 (simulator import sheet): **HIGH** for the sheet; **UNVERIFIED** for completing the import
- DEV-06 counts and ancestry: **HIGH** for the counts, **MEDIUM** for the ancestry derivation
- BD-02 floor: **LOW** — one unrepeated user report; assembled as decision input only
- Every device-behaviour claim: **BLOCKED** — no device connected; nothing inferred, nothing fabricated

**Research date:** 2026-08-17
**Valid until:** re-verify if `tools/build_state_engine.py` receives further commits, if Phases 13–15
land (each moves the site counts and the artifact SHA-256), or if a device session produces new
ground truth. Treat as valid ~7 days or until the next commit to the generator, whichever is sooner.
