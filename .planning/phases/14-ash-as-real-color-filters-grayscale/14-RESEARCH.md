# Phase 14: Ash as real Color Filters grayscale - Research

**Researched:** 2026-08-18
**Domain:** iOS 26 Shortcuts plist authoring — a private AppIntent accessibility toggle, wired into an existing capture-and-restore machine
**Confidence:** HIGH on the action shape and the code surface; MEDIUM on the gate-A disposition (a decision, not a fact); LOW on device behaviour (never run on hardware)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

None recorded as locked decisions in `14-CONTEXT.md` — the discuss phase was skipped via `workflow.skip_discuss`.

The `<domain>` block of CONTEXT.md nonetheless carries decisions made elsewhere and restated there as binding. Copied verbatim:

> **The blocker that justified the cut is gone.** Spike 005
> (`.planning/spikes/005-ios-color-filters-identifier/`, VALIDATED, merged `4d80176`) settled
> it from decrypted device donors — tier-1 evidence. Identifier:
> `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` — an `AX*`
> intent, **not** the `UA*` macOS twin. `state` is a **bool-as-integer**: `1` = On, `0` = Off.
> `operation` is elided when Turn, so omit it. No `ShowWhenRun`. Both legs are donor-confirmed.

> **Expect the validator not to know the identifier** — it is absent from all three bundled
> ToolKit snapshots. Record the deviation rather than letting a validator complaint trigger a
> substitution back to `UA*`, which would ship a macOS action to an iPhone.

> **The restore leg is the deliverable, not the apply leg.** A grayscale that does not restore
> is strictly worse than no grayscale. Wire `state = 0` everywhere the other environmental
> primitives restore — CLOSE, Emergency Restore, Ice expiry, the live-Ice redirect — reusing
> `restore_managed_settings()`'s ownership pattern, and track it in `settings_snapshot`
> alongside brightness and volume so Emergency Restore has one uniform recovery surface.

> **User decision 2026-08-17: default ON, disclosed in onboarding.** Branch on
> `safety.ash_managed_color_filters` (already in Config, currently dead code): true → real
> toggle, false → BD-01's non-environmental pause.

> Also correct `src/CONFIG-BLOCK.md`'s BD-01-R note, which currently asserts Ash *is* already a
> real Color Filters change — make it true or make it honest, but do not leave both. Closes
> spike 005 step 5.

### Claude's Discretion

> All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

### Deferred Ideas (OUT OF SCOPE)

> None — discuss phase skipped.

One enhancement is explicitly named as **not a gate** by BD-01-R2 and spike 005's Open Questions, and should be treated as out of scope unless the planner deliberately adopts it: the `state` **response** parameter read-back probe (`operation = toggle` to reveal prior state by inversion). It is unverified, post-operation, and costs a visible flicker.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (from REQUIREMENTS.md) | Research Support |
|----|-------------|------------------|
| CIRC-02 | "Ash applies the audited visual-salience reduction, or its documented fallback if no safe action exists" | The audited action now exists and is donor-confirmed on both legs — §Standard Stack, §Code Examples. Both the real toggle and the fallback ship, selected by `safety.ash_managed_color_filters`. |
| SAFE-01 | "Brightness is changed only when its original value has been captured **and durably persisted** before the change, and is always restored" | The ordering rule generalises to grayscale: write the ownership marker to `settings_snapshot`, `save_state()`, *then* apply. `verify_capture_persistence()` is the guard that pins it and it is currently blind to the new action — §Architecture Patterns, Pattern 3. |
| SAFE-02 | "Volume is never increased and no startling output is produced" | Untouched by this phase — but the guard that enforces it (`artifact_check()`'s `WFVolumeSetting == "Media"` sweep and `EXPECTED_SITES`) sits in the file this phase must edit, so the phase must not disturb it. §Common Pitfalls, Pitfall 6. |
| SAFE-05 | "Emergency Restore clears cooldown, clears the active session, and restores recoverable brightness, volume, **and colour settings**" | The requirement text **already promises colour** and the build has never delivered it. Wiring the restore leg through `restore_managed_settings()` makes the requirement true as written — §Architecture Patterns, Pattern 2. |
| AUDIT-02 | "Grayscale / Color Filters capability is resolved to a go/no-go decision, and the Ash primitive has a documented fallback design if no safe action exists" | Resolved GO by BD-01-R2 (`docs/CAPABILITY-DECISIONS.md`) and CAP-20 (`docs/BUILD-NOTES.md`), both already VERIFIED. This phase closes the residual documentation defect in `src/CONFIG-BLOCK.md` — §Don't Hand-Roll and §State of the Art. |
</phase_requirements>

## Summary

Everything this phase needs to *write* is already settled by tier-1 device evidence. Spike 005 decrypted three donors exported from the owner's iPhone and pinned the identifier, both parameter values, and the elision rule. There is no open capability question on the write path. The action is two lines of plist: an identifier and `state` as a bare `<integer>`. Authoring it is the smallest part of the work.

The work is everything the action must be *wired into*. PROSOCHĒ has a mature, heavily-guarded capture-and-restore machine for two environmental primitives (brightness, volume) built across phases 5, 9, 11 and 16, and its guards are keyed by identifier and by group name. A third primitive that does not join those keys is not merely unguarded — it is **invisible to the guards while the site tables go on certifying the build as safe**, which is precisely the failure `verify_environmental_reachability()`'s docstring was written to describe. Four build guards, one bootstrap seeder, and three `docs/` checkers all need to learn about grayscale, and one of them (`docs/phase5_self_check.py`) currently asserts the *opposite* — that `AXToggleColorFiltersIntent` never appears in the artifact — so the build's own self-check will go red the moment the primitive ships. That inversion is a required, deliberate edit, not an incident.

Two structural traps are worth naming before planning starts. First, `seed_settings_snapshot()` **returns early on every already-seeded tree**, so adding a `color_filters` group to `SNAPSHOT_SEED` changes nothing in the artifact and then makes `verify_state_seed()` fail — the identical shape D-02 hit in phase 16, and it needs its own in-place recogniser. Second, gate A **cannot pass clean** with this identifier present: measured, the validator emits `Unknown AppIntent identifier` once per site and has no allowlist, waiver flag, or environment override. Signing, however, is unaffected — measured, a signed `.shortcut` is produced from a plist carrying the unknown identifier with no descriptor at all. So the artifact remains shippable; what changes is the project's own definition of gate A.

**Primary recommendation:** Emit the donor shape byte-exactly (identifier + `state` integer, nothing else), reuse `settings_snapshot.color_filters.original_value` as a numeric **ownership marker** (`1` = PROSOCHĒ owns an outstanding filter, sentinel = nothing outstanding) so every existing gate idiom applies unchanged, teach the four build guards and three checkers the new identifier and group in the same commit, add a recogniser-based seeder pass for the new snapshot group, and convert gate A from "must pass clean" to "residue must equal exactly the enumerated waiver" with a mechanical check — not a remembered one.

## Architectural Responsibility Map

There is no client/server split here. The tiers are the project's own build pipeline layers, and misassigning between them is this codebase's documented recurring defect (a rule stated in a document that no build guard asserts).

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Emitting the AX Color Filters apply/restore actions | Generator (`tools/build_state_engine.py`) | — | Every action in the artifact is emitted, never hand-edited; `src/PROSOCHE-Dumb.xml` is generated output. |
| Propagating the change to the second fork | Generator (`tools/build_sentient.py`) | — | Aware forks the *built* Core source additively; the change arrives for free, but the guard imports must still resolve. |
| Selecting real toggle vs. fallback pause | Config literal (`safety.ash_managed_color_filters`) read at runtime | Generator emits the branch | §21's opt-in remedy is a user-editable value, not a build-time constant. The generator emits both arms. |
| Ownership tracking / crash safety | `state.json` via `settings_snapshot` | Bootstrap seeder | Only a persisted marker survives a force-quit; only a seeded container prevents a dotted-read hard error. |
| Preventing a dead arm / unpersisted apply / ungated write | Build guards in the generator (`verify_*`) | `docs/*.py` checkers, independently, from disk | The project deliberately duplicates: build guard aborts a bad build, checker proves the shipped artifact without importing its producer. |
| Proving the identifier is authorised | Human record (`docs/BUILD-NOTES.md` CAP-20, `docs/CAPABILITY-DECISIONS.md` BD-01-R2) | Validator gate A **cannot** do this — it has never heard of the identifier | The catalog gap is real. Do not let a tool that lacks the fact overrule the donor that has it. |
| Disclosure of the accessibility change | Control Room Note copy (preserved plist literal, edited via `tools/plist_text_edit.py`) | `src/CONFIG-BLOCK.md` field reference | There is no read-back, so consent is obtained by disclosure, not detection. |

## Standard Stack

There is nothing to install. The "stack" is the set of already-present, already-audited identifiers and helpers this phase composes.

### Core

| Library / identifier | Version | Purpose | Why standard |
|---------|---------|---------|--------------|
| `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` | iOS 26 | The apply and restore legs of Ash | Donor-confirmed on three device-exported shortcuts `[VERIFIED: .planning/spikes/005-ios-color-filters-identifier/{SetColourFilters,Donor9,Donor9.1}-Shortcut.xml, read verbatim this session]` |
| `tools/build_state_engine.py` → `ash()` | HEAD | The primitive to replace | Currently an `alert()` only `[VERIFIED: read this session]` |
| `tools/build_state_engine.py` → `restore_managed_settings()` | HEAD | The restore expansion, rendered at 4 call sites | The project's single restore idiom; SAFE-05/SESS-07 are asserted against it by name `[VERIFIED: docs/environmental_restore_check.py source_check()]` |
| `tools/build_state_engine.py` → `clear_snapshot()` | HEAD | Clears the captured LEAF, never the container | Container/leaf split is a hard invariant; violating it reintroduces cycle-10's hard error `[VERIFIED: clear_snapshot() docstring]` |
| `tools/build_state_engine.py` → `config()` | HEAD | `read_value(key, variable("Config"), name)` — reads the opt-in flag | One-line helper; `voice_enabled` is the exact numeric-boolean precedent in `mirror_and_voice()` `[VERIFIED: read this session]` |
| `tools/build_state_engine.py` → `if_block(name, 2, number=0)` | HEAD | The numeric `> 0` gate | The only gate family that excludes BOTH the `"null"` sentinel and an empty value `[VERIFIED: restore_managed_settings() docstring, Donor 6 / 6.1]` |
| `tools/build_state_engine.py` → `number()`, `set_value()`, `save_state()` | HEAD | Write the ownership marker and persist it before the apply | `dimming()` / `silence()` are the exact precedent `[VERIFIED: read this session]` |

### Supporting

| Symbol | Purpose | When to use |
|--------|---------|-------------|
| `SNAPSHOT_SEED`, `SNAPSHOT_EMPTY`, `SNAPSHOT_SEEDED_EMPTY`, `SNAPSHOT_SEEDED_D02`, `_snapshot_seed_text()` | Bootstrap `state.json` template seeding | A new snapshot group needs an entry **and** a new recogniser — see Pitfall 1 |
| `ENVIRONMENTAL_IDENTIFIERS` (frozenset) | Feeds `verify_environmental_reachability()` | Must gain the AX identifier or a dead-arm grayscale is invisible |
| `VERIFIED_PARAMETER_KEYS` / `STRUCTURAL_KEYS` / `verify_parameter_keys()` | Axis-1 key-name guard | Identifiers absent from the mapping are **skipped entirely** — adding an entry is opt-in armour |
| `tools/plist_text_edit.py` (`find_action`, `replace_in_token`) | Guarded round-trip edit of a preserved plist text literal | The Control Room Note body and the Config literal are preserved literals, not generated — edit only through this |
| `docs/environmental_restore_check.py` → `EXPECTED_SITES`, `REQUIRED_SYMBOLS`, `CALLED_GUARDS` | Independent artifact-side proof | Must gain a grayscale row and, if a new guard is written, a symbol entry |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `AXToggleColorFiltersIntent` | `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | **Never.** That is the macOS twin. It is in the ToolKit snapshots, so it would silence gate A — which is exactly the trap CONTEXT.md warns about: a green validator obtained by shipping a macOS action to an iPhone. `[VERIFIED: BD-01-R2, CAP-20]` |
| `state` omitted (donor 9's untouched second action) | — | An absent `state` is the untouched default in the UI; it is not a directive. Emitting nothing applies nothing. `[VERIFIED: Donor 9 action 2 vs Donor 9.1, same UUID]` |
| `state = 2` for Off | — | **Never.** Apple's `.intentdefinition` declares `off` = case index 2; Shortcuts does not use those indices. Shipping 2 leaves the user stuck in grayscale. `[VERIFIED: Donor 9.1 emits <integer>0</integer>]` |
| `operation = "turn"` | omit `operation` | Both the On and Off donors emit **no** `operation` key. `turn` is the elided default and no donor has ever written that literal. Omitting is both donor-verified and fabrication-free. `[VERIFIED: all three donors]` |
| `ShowWhenRun` | — | Does not exist on the iOS intent; it is a macOS catalog row parameter only. `[VERIFIED: BD-01-R2]` |
| A synthesised `AppIntentDescriptor` to quiet gate A | Emit the donor shape unchanged | Measured this session: adding a descriptor removes one of gate A's two error lines per site but **not** the `Unknown AppIntent identifier` line. Since it cannot make gate A clean, its only effect is to insert a fabricated `BundleIdentifier`/`AppIntentIdentifier`/`TeamIdentifier` that no donor supplies, into a plist iOS itself writes without one. **Do not add it.** `[VERIFIED: probe /tmp/axtest/t2.xml, this session]` |
| A new leaf name (`settings_snapshot.color_filters.managed`) | Reuse `original_value` | See Open Question 1. `original_value` is semantically imprecise for a value that was never read back — but every existing guard keys on that exact leaf name (`clear_snapshot()`, `verify_capture_persistence()`, `verify_state_seed()`, `_is_removed_snapshot_leaf()`). A new name means generalising four guards; reuse means one honest docstring. **Recommend reuse.** |

**Installation:** none. No package, no dependency, no registry.

**Version verification:** not applicable — this phase adds no external package to any ecosystem.

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages in any ecosystem. Every symbol it touches is either already in this repository (`tools/`, `docs/`, `src/`) or is an Apple-supplied Shortcuts action identifier verified against device-exported donors. The `package-legitimacy` seam has no ecosystem to query.

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
                      Personal Automation                    Manual tap
                     (App Is Opened / Closed)                    │
                              │                                  │
                        "OPEN" / "CLOSE" text                    │
                              ▼                                  ▼
                   ┌──────────────────────────────────────────────────┐
                   │  ROUTER  (Input Key == "OPEN" / "CLOSE" / else)   │
                   └───────┬───────────────┬──────────────────┬───────┘
                           │               │                  │
                       OPEN arm        CLOSE arm           MANUAL arm
                           │               │                  │
              ┌────────────┴────┐          │        ┌─────────┴──────────┐
              │ cooldown live?  │          │        │ Test a Circle (×9) │
              ├── yes ──────────┤          │        │ Emergency Restore  │
              │  live_ice_      │          │        └────┬───────────┬───┘
              │  redirect() ────┼─── R     │             │           │
              ├── no (expired) ─┤          │             │           └── R
              │  ice_expiry() ──┼─── R     │             │
              └─────────────────┘          │             │
                           │               │             │
                  Heat → Pressure → Circle │             │
                           │               │             │
                  Circle Next > 0 ?  ──no──┼─────────────┼──► silent, nothing shown
                           │ yes           │             │
                   universal_leaving()     │             │
                    (Leaving | Continue)   │             │
                           │               │             │
                           ▼               │             ▼
                 ┌──────────────────────────────────────────────┐
                 │  primitive_dispatch()   × 11 renderings/fork │
                 │  reads Config sequences.<Seq>.<Circle>       │
                 │  "Black and White" ─────────────► ash()      │
                 └──────────────────┬───────────────────────────┘
                                    │
                    ┌───────────────▼─────────────────────────────┐
                    │ ash()   [THIS PHASE]                        │
                    │  1. read settings_snapshot.color_filters    │
                    │       .original_value  (LEAF, numeric > 0)  │
                    │     > 0 → outstanding, do nothing           │
                    │  2. read Config safety.ash_managed_color_   │
                    │       filters   (numeric > 0)               │
                    │     0 → alert() fallback pause, no device   │
                    │           change (BD-01 behaviour)          │
                    │  3. set_value(marker = 1)                   │
                    │  4. save_state()          ◄── ORDERING RULE │
                    │  5. AX ...ColorFiltersIntent  state = 1     │
                    └─────────────────────────────────────────────┘
                                    │
                        state.json now records "we own it"
                                    │
   R = restore_managed_settings(), rendered at FOUR call sites:
       close_pipeline("Reloaded State"), live_ice_redirect("State"),
       ice_expiry("State"), manual_emergency_restore("State")
                                    │
                    ┌───────────────▼─────────────────────────────┐
                    │ restore_managed_settings()   [+1 block]     │
                    │  brightness: container gate → leaf > 0      │
                    │              → setbrightness, clear leaf    │
                    │  volume:     same shape → setvolume, clear  │
                    │  colour:     same shape → AX state = 0,     │
                    │              clear leaf         [THIS PHASE]│
                    └─────────────────────────────────────────────┘
```

### Recommended Project Structure

No new files. Every change lands in files that already exist:

```
tools/
├── build_state_engine.py     # ash(), restore_managed_settings(), SNAPSHOT_SEED,
│                             #   ENVIRONMENTAL_IDENTIFIERS, verify_capture_persistence(),
│                             #   VERIFIED_PARAMETER_KEYS, + one new seeder recogniser
└── build_sentient.py         # imports only — no change unless a new guard is added
src/
├── PROSOCHE-Dumb.xml         # GENERATED (Core). Never hand-edit except via plist_text_edit
├── PROSOCHE-Sentient.xml     # GENERATED (Aware), forked from the built Core
└── CONFIG-BLOCK.md           # mirror of the Config literal + the false BD-01-R note
docs/
├── phase5_self_check.py      # carries the assertion that must be INVERTED
├── environmental_restore_check.py  # EXPECTED_SITES, REQUIRED_SYMBOLS, bootstrap seed loop
├── phase9_self_check.py      # site_audit() — unaffected, verify it stays 30/30
├── BUILD-NOTES.md            # CAP-20 already VERIFIED; deviation log gains a gate-A entry
└── CAPABILITY-DECISIONS.md   # BD-01-R2 already correct; may gain an "implemented" note
artifacts/shortcuts/MANIFEST.md  # re-signed rows
```

### Pattern 1: The primitive's own gate is the LEAF, numerically — never the container

This is phase 11 plan 11-08's correction and it is the single most important shape to copy. `dimming()` and `silence()` originally opened on a **condition-100 existence gate over the `settings_snapshot.<group>` container** with all their work in the OTHERWISE arm. Because `clear_snapshot()` writes the leaf and never the container, that container is a permanent bootstrap invariant, the gate is permanently TRUE, and the otherwise arm was **dead code — 44 unreachable actions per fork**, while `EXPECTED_SITES` went on certifying them as shipped.

```python
# Source: tools/build_state_engine.py, dimming() — the shape to copy, verbatim in structure
a += read_value("settings_snapshot.brightness.original_value", variable("State"),
                "Outstanding Brightness Original")
original_g, original_if = if_block("Outstanding Brightness Original", 2, number=0)
a += [original_if, action("is.workflow.actions.nothing"), otherwise(original_g)]
#     ^ TRUE arm = "a capture is already outstanding, do nothing"
#       work goes in the OTHERWISE arm of a NUMERIC gate — which can genuinely read false
```

### Pattern 2: One restore expansion, four call sites, and the group ordering is free

`restore_managed_settings(dictionary_name)` emits two structurally identical blocks today. Adding a third is additive and lands at all four call sites at once — `close_pipeline("Reloaded State")`, `live_ice_redirect("State")`, `ice_expiry("State")`, `manual_emergency_restore("State")`. The `dictionary_name` parameter is load-bearing (T-16-04) and must be threaded through unchanged.

```python
# Source: tools/build_state_engine.py, restore_managed_settings() — the per-group template
a += read_value("settings_snapshot.volume", variable(dictionary_name), "Restore Volume Snapshot")
snapshot_g, snapshot_if = if_block("Restore Volume Snapshot", 100)
a += [snapshot_if] + read_value("settings_snapshot.volume.original_value",
                                variable(dictionary_name), "Restore Volume")
volume_g, volume_if = if_block("Restore Volume", 2, number=0)
a += [volume_if, set_media_volume(variable("Restore Volume")), clear_snapshot("volume", dictionary_name),
      otherwise(volume_g), action("is.workflow.actions.nothing"), end_if(volume_g),
      otherwise(snapshot_g), action("is.workflow.actions.nothing"), end_if(snapshot_g)]
```

The container gate at condition 100 is **correct here and only here**: the restore side puts its work in the TRUE arm, so a permanently-true container gate is harmless. `verify_environmental_reachability()` tests the ARM, not the gate, which is why the restore side is correct by construction rather than by exemption. Copy the shape exactly; do not "simplify" the container gate away.

### Pattern 3: Persist the ownership marker BEFORE the device changes

Shortcuts has no try/catch. Safety here is achieved by ordering, not detection. `dimming()` and `silence()` each emit `save_state()` **inside the applying arm only**, immediately before the write. The rejected alternative — saving on the outer capture arm — is recorded in `dimming()`'s docstring: it also runs on the already-dim path, so it would record a snapshot for a change that never happened and a later CLOSE would drive the device to it.

For grayscale the same rule holds with one simplification: there is no "already grayscale" path to detect (no read-back), so the applying arm is the only arm.

### Anti-Patterns to Avoid

- **A condition-100 existence gate over `settings_snapshot.color_filters`, with the apply in the otherwise arm.** Permanently true; the apply becomes dead code. Caught by `verify_environmental_reachability()` **only if the AX identifier is added to `ENVIRONMENTAL_IDENTIFIERS`** — otherwise it ships silently.
- **Writing `state` through a `WFTextTokenString` envelope.** `state` is a plain plist `<integer>`, not a string parameter. Axes 2/3 do not apply; applying them would be a fabricated shape.
- **Substituting the `UA*` identifier to make gate A green.** Ships a macOS action to an iPhone.
- **Emitting the AX action with no `state` key at all.** Donor 9's second action proves that is the *untouched* default, not a directive.
- **Adding `color_filters` to `SNAPSHOT_SEED` and assuming the artifact follows.** It will not — see Pitfall 1.
- **Editing `docs/environmental_restore_check.py`'s `EXPECTED_SITES` numbers to "make the check pass"** if brightness/volume counts move. Those numbers moving is a regression signal, not a table to update. This phase should move them by **zero**.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| "Has PROSOCHĒ already changed this setting?" | A new ownership-tracking field, dictionary or convention | `settings_snapshot.<group>.original_value` + the numeric `> 0` gate | Four restore call sites, one seeder, four build guards and two checkers are already keyed to that exact shape. A parallel mechanism doubles the surface and halves the guard coverage. |
| Restoring the filter on CLOSE / Ice expiry / live-Ice / Emergency Restore | Four hand-placed restore calls | One block inside `restore_managed_settings()` | The expansion already reaches all four sites; hand-placing invites the "restored at three of four" defect that has no symptom until a user is stuck grey. |
| Clearing the marker after restore | `set_value("settings_snapshot.color_filters", ...)` | `clear_snapshot("color_filters", dictionary_name)` | Replacing the container with a string makes the next dotted read hard-error one run later — cycle-10 finding 5, recorded in `clear_snapshot()`'s docstring. |
| Reading a JSON boolean from Config | A string compare against `"true"` | `read_value(...)` + `if_block(name, 2, number=0)` | `safety.*` booleans read back as numeric `1`/`0`, not the strings. `src/CONFIG-BLOCK.md` names this as coercion hazard A4 and `mirror_and_voice()`'s `voice_enabled` is the in-repo precedent. |
| Numeric coercion on the Config read | A hand-written `WFCoercionVariableAggrandizement` | Let `normalise_numeric_operands()` attach it | The read is gettext-fed, so the pass attaches Donor 4.1's coercion automatically and adds no new shape to the artifact. |
| Detecting the user's pre-existing Color Filters state | A toggle-probe, an inference, or a default assumption | Disclosure + `safety.ash_managed_color_filters` | No `Get*`/`Query*` intent exists across all 35 intents in `AccessibilityUtilities.framework`. §21's remedy is opt-out-by-disclosure, and that is a settled user decision. |
| Making gate A green | Any change to the emitted action | A recorded, mechanically-checked deviation | The identifier is genuinely absent from all three snapshots. Every way of silencing the validator either fabricates a shape or ships the wrong action. |

**Key insight:** in this codebase the risky move is never the new action — it is the *new mechanism*. Every parallel path this repo has grown (a second restore idiom, a second ownership convention, a second row framing) has produced a defect invisible to every existing guard. Join the existing machine.

## Runtime State Inventory

This is not a rename or migration phase, but it **does** change the persisted `state.json` shape, which triggers the same class of question. Answered explicitly:

| Category | Items found | Action required |
|----------|-------------|------------------|
| Stored data | `state.json` gains `settings_snapshot.color_filters.original_value`. The bootstrap template is a preserved text literal inside the artifact, not a file on disk in this repo. **Any device carrying an older `state.json` will not have the key**, and a dotted read of a missing segment is a **hard runtime error**. | Generator change: a new in-place recogniser in `seed_settings_snapshot()` (see Pitfall 1). Data migration on device: **none needed** — BD-06-A1 records that PROSOCHĒ is undeployed and old `state.json` files are explicitly not a consideration; and `fix_state_rebind()` / the bootstrap path rebuilds the file. Confirm this reasoning holds rather than assuming it. |
| Live service config | None — PROSOCHĒ has no server, no external service, no cloud component. Verified by the project constraint "no behavioural data leaves the device" and by there being no network action in the artifact. | None |
| OS-registered state | The user's two Personal Automations reference the shortcut **by library display name** (`PROSOCHĒ — Nine Circles — Core` / `— Aware`). This phase does not rename either fork, so the automations are unaffected. | None — but the re-signed `.shortcut` must keep the exact display name with no suffix (DIST-04, asserted by `docs/manifest_check.py`). |
| OS-registered state (accessibility) | **iOS Color Filters itself is OS-registered state that survives the run, the app, and a reboot.** This is the whole reason the restore leg is the deliverable. A missed restore is not a stale record — it is a user whose phone is grey until they find Settings → Accessibility. | The restore leg at all four call sites, plus Emergency Restore reachable at all times (`verify_panic_escape_isolation()` already pins that). |
| Secrets / env vars | None. No secrets, no env vars, no `.env`. | None |
| Build artifacts | `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` are regenerated; `artifacts/shortcuts/<date>/*.xml` archives and the two signed `.shortcut` files are re-produced, and `artifacts/shortcuts/MANIFEST.md` carries their sizes and SHA-256 hashes. | Rebuild both forks, re-sign both, update MANIFEST rows, and run `python3 docs/manifest_check.py` — it asserts path, byte count and hash per row. |

## Common Pitfalls

### Pitfall 1: Adding a `SNAPSHOT_SEED` group silently changes nothing, then fails the build

**What goes wrong:** the planner adds `"color_filters": ("original_value",)` to `SNAPSHOT_SEED`, rebuilds, and `verify_state_seed()` raises `bootstrap state.json does not establish every state key that is read`.

**Why it happens:** `seed_settings_snapshot()` ends with `if SNAPSHOT_EMPTY not in inner["string"]: return`. `main()` re-parses its own previous output as `SOURCE`, so on every tree built since the seed first landed the template is **already seeded**, `SNAPSHOT_EMPTY` (`"settings_snapshot": {},`) is absent, and the seeder returns early. `_snapshot_seed_text()` — the only consumer of `SNAPSHOT_SEED` on the write side — never runs. Meanwhile `verify_state_seed()` builds its `wanted` set *from `SNAPSHOT_SEED`*, so the constant and the artifact disagree and the guard correctly reports it.

**How to avoid:** add a third in-place recogniser pass alongside the two that already exist (`SNAPSHOT_SEEDED_EMPTY` for build-j trees, `SNAPSHOT_SEEDED_D02` for pre-D-02 trees). Phase 16's D-02 hit this exact wall and the reasoning is recorded in full in the comment block above `SNAPSHOT_SEEDED_EMPTY` — read it before writing the new pass. The recogniser must be **derived from existing constants, not hand-typed**, and `_replace_in_token()` must be used so `attachmentsByRange` offsets are shifted (the template carries four attachments and one sits after the `settings_snapshot` line; a stale offset can crash Shortcuts on import).

**Warning signs:** the build passes but a `grep '"color_filters"' src/PROSOCHE-Dumb.xml` returns only the new action sites and not the bootstrap template.

### Pitfall 2: `docs/phase5_self_check.py` asserts the opposite of what this phase ships

**What goes wrong:** the build succeeds, then `python3 docs/phase5_self_check.py` raises `unsupported Color Filters action was emitted`.

**Why it happens:** the file carries, verbatim:

```python
require("AXToggleColorFiltersIntent" not in text and "UAToggleColorFiltersIntent" not in text,
        "unsupported Color Filters action was emitted")
```

That assertion was correct when written — BD-01 had ruled the capability NOT AVAILABLE. BD-01-R2 superseded that from donor evidence.

**How to avoid:** invert it deliberately and asymmetrically in the same commit as the generator change: assert the `AX*` identifier **is** present (with an expected count), and that the `UA*` identifier is **still absent**. The second half is the one that keeps its teeth — it is the guard against a future "fix" that swaps in the macOS twin to satisfy gate A. Do not simply delete the line; deleting it removes the `UA*` protection too.

### Pitfall 3: The build guards are keyed by identifier and will not see grayscale

Four guards are scoped to `{"is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"}` or to `ENVIRONMENTAL_IDENTIFIERS`. Measured this session by reading each:

| Guard | Current scope | What happens to grayscale if unchanged |
|-------|---------------|-----------------------------------------|
| `verify_environmental_reachability()` | `ENVIRONMENTAL_IDENTIFIERS` frozenset | A grayscale apply buried in a permanently-true container gate's otherwise arm ships **silently**. |
| `verify_capture_persistence()` | applies matched by `identifier in {setbrightness, setvolume}`, group derived by `identifier.endswith("setbrightness")` | The marker write raises a pending flag that **no apply ever consumes**, so an apply-before-persist ordering error is invisible. The group derivation is also a two-way `if/else` that would mislabel any third identifier as `"volume"` — it must become a mapping. |
| `verify_restore_gates()` | same two identifiers, operand read from `WFBrightness`/`WFVolume` | Grayscale's operand is a **literal** `0`/`1`, so even after widening, the guard's `continue  # a literal target is not a state-derived write` branch applies and it contributes nothing. State this explicitly rather than assuming coverage. |
| `verify_parameter_keys()` | `VERIFIED_PARAMETER_KEYS.get(identifier)`; **returns `None` → `continue`** | Axis-1 protection is simply absent for the new identifier. Adding `{"state"}` (plus `"operation"` only if ever emitted, which it should not be) opts the action in. `UUID` is already covered by `STRUCTURAL_KEYS`. |

**How to avoid:** treat "which guards key on an identifier set" as a checklist item in the plan, not as something to discover during verification.

### Pitfall 4: `docs/environmental_restore_check.py` will pass while covering nothing new

`EXPECTED_SITES` counts exactly three identifiers, `ALLOWED_DEVICE_DETAILS` allows exactly two device properties, and the bootstrap-seed assertion loops over `("brightness", "volume")`. None of these fails when grayscale is added — they simply do not look. A green run after this phase, with the file unedited, is a false reassurance of exactly the kind its own docstring warns about ("the site tables go on certifying those actions"). The file must gain: a grayscale entry in `EXPECTED_SITES`, `"color_filters"` in the bootstrap-seed group loop, and — if a new build guard is written — its name in `REQUIRED_SYMBOLS` (which feeds `CALLED_GUARDS` by comprehension, so the call-site check follows automatically).

### Pitfall 5: Gate A cannot pass clean, and there is no waiver mechanism

**Measured this session, not inferred.** A minimal probe carrying the AX identifier produced, at `--target-macos 26 --target-platform all`:

```
- AppIntent action missing AppIntentDescriptor at index 1: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent
- Unknown AppIntent identifier at index 1: com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent
```

exit 1. Both errors are emitted **once per action instance** (confirmed with a two-instance probe). Adding an `AppIntentDescriptor` with an `AppIntentIdentifier` removes the first line and leaves the second. There is **no** allowlist flag, `--ignore`, waiver file, or environment override: `validate_shortcut.py` accepts exactly two options beyond the path (`--target-macos`, `--target-platform`), and its allowed-id set is built from `skill_dir/data/toolkit-v*-tool-ids.json` plus `ACTIONS.md` / `APPINTENTS.md` / `THIRD_PARTY_ACTIONS.md`, where `skill_dir = Path(__file__).resolve().parents[1]` — a fixed path inside the plugin cache, not repo-controllable and overwritten by plugin updates.

**Signing is unaffected.** Measured: `sign-shortcut probe.xml --name AXProbe` on a plist carrying the unknown identifier and **no** descriptor produced a 21,698-byte signed `.shortcut` and exited cleanly. The artifact remains shippable; only the validator's verdict changes.

**How to avoid the wrong fix:** do not chase a clean gate A. See Open Question 2 for the disposition options and the recommendation.

### Pitfall 6: A count that must not move, and one that must

`docs/phase9_self_check.py`'s `site_audit()` and `docs/environmental_restore_check.py`'s `EXPECTED_SITES` both pin `setbrightness = 15`, `setvolume = 15`, `getdevicedetails = 22` per fork, and the coercion split `15 / 4`. This phase must move **none of them**. If they move, something unintended was emitted — investigate rather than updating the table. Conversely, the new AX count **is** expected to be **15 per fork**: 11 apply sites (one per `primitive_dispatch()` rendering — 9 Test-a-Circle submenu cases plus 2 in `universal_leaving()`) plus 4 restore sites (one per `restore_managed_settings()` call site). That the number matches the other two exactly is a derivation, not a coincidence, and is worth writing into the site-derivation comment.

### Pitfall 7: `docs/retired_clause_check.py` scans the whole repo for retired brightness prose

Any new prose this phase writes — the Control Room Note disclosure, the `src/CONFIG-BLOCK.md` correction, the BUILD-NOTES deviation entry — is swept. The patterns are narrow (`10-15` as a standalone token near a brightness/dim word or a `%`; `strictly positive` within ±6 lines of `dim_target`), so ordinary Color Filters prose will not trip them. Low risk, but run the checker before declaring done rather than after.

### Pitfall 8: The Control Room Note and the Config literal are preserved literals

Both live inside the artifact as preserved `is.workflow.actions.gettext` text tokens, not as generator string constants. The Note body is located by content (`## READ THIS FIRST`) by `docs/note_identity_check.py`, and `src/CONFIG-BLOCK.md`'s own header says the fenced block is "the transcription source, not a description of one" — i.e. `CONFIG-BLOCK.md` is the **mirror**, and the live literal in `src/PROSOCHE-Dumb.xml` is the thing that ships. Edit the live literal through `tools/plist_text_edit.py`'s guarded round trip, re-parse with `json.loads`, and update the mirror in the same commit. `docs/note_identity_check.py`'s `MINIMUM_TOKEN_STRINGS = 1104` floor is a lower bound and additive prose cannot breach it.

## Code Examples

### The apply leg — donor-verbatim

```xml
<!-- Source: .planning/spikes/005-ios-color-filters-identifier/SetColourFilters-Shortcut.xml
     Device-authored on the owner's iPhone, decrypted via the AEA1 round-trip. Complete
     action; no other parameter is present. -->
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key>
        <string>05477FE4-67CE-42DD-8421-44EE444E3CE8</string>
        <key>state</key>
        <integer>1</integer>
    </dict>
</dict>
```

### The restore leg — donor-verbatim

```xml
<!-- Source: .planning/spikes/005-ios-color-filters-identifier/Donor9.1-Shortcut.xml
     Same UUID as Donor 9's untouched second action, reconfigured to Off, so the On/Off
     pairing is exact. `state` is a bool-as-integer; `operation` is absent on BOTH legs. -->
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key>
        <string>FA4D2410-A0DB-4706-BE8F-8942A7E4D658</string>
        <key>state</key>
        <integer>0</integer>
    </dict>
</dict>
```

### What the generator's `action()` helper produces

```python
# Source: tools/build_state_engine.py, action() — plain kwargs into WFWorkflowActionParameters.
# A Python int becomes a plist <integer> under plistlib.dumps, which is exactly the donor shape.
COLOR_FILTERS = "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent"

def set_color_filters(on: bool):
    """Donor-verbatim. `operation` is the elided default and is never written."""
    return action(COLOR_FILTERS, state=1 if on else 0)
```

### The Config read — the numeric-boolean idiom already in the repo

```python
# Source: tools/build_state_engine.py, mirror_and_voice() — the precedent for reading a
# JSON boolean back out of a parsed dictionary. safety.* booleans arrive as numeric 1/0,
# never as the strings "true"/"false" (src/CONFIG-BLOCK.md, coercion hazard A4).
a += read_value("voice_enabled", variable("State"), "Voice Enabled")
voice_g, voice_if = if_block("Voice Enabled", 2, number=0)
```

For this phase the source is `Config`, not `State`, so the one-line helper applies:

```python
a += config("safety.ash_managed_color_filters", "Ash Managed Filters")
managed_g, managed_if = if_block("Ash Managed Filters", 2, number=0)
```

### The fallback arm that must survive

```python
# Source: tools/build_state_engine.py, ash() as it ships today. Under
# safety.ash_managed_color_filters == false this alert is the BD-01 non-environmental
# pause and must remain reachable, verbatim in intent.
alert("Black and White", "One breath away from the screen before you go on.")
```

Note the emitted Shortcuts comment above it currently asserts *"It changes no accessibility setting. Color Filters is deliberately excluded because the iOS action is not validator-supported."* That comment **ships to the user's device 11 times per fork** and becomes false the moment this phase lands. Phase 16 hit the identical class with `dimming()`'s brightness-floor bullet; the correction there is the precedent — restate the property the build actually guarantees, per arm.

## State of the Art

| Old approach | Current approach | When changed | Impact |
|--------------|------------------|--------------|--------|
| CAP-20 `NOT AVAILABLE`; BD-01 redefines Ash as a non-environmental pause | BD-01-R reverses from catalog *reasoning* + owner assertion | 2026-08-13 | Conclusion right, recipe wrong in three ways |
| BD-01-R's recipe: `UA*` identifier, `operation = turn`, `ShowWhenRun = Off` | BD-01-R2: `AX*` identifier, `state` bool-as-integer, `operation` omitted, no `ShowWhenRun` | 2026-08-16 (spike 005, merged `4d80176`) | CAP-20 VERIFIED. **BD-01-R got exactly one thing wrong — the identifier.** Its parameter model was right and spike 005's two intermediate "corrections" of it were both wrong. |
| `state = 2` for Off (asserted from Apple's `.intentdefinition`) | `state = 0` | Donor 9.1, same spike | Would have shipped a restore leg that leaves users stuck in grayscale |
| `dimming()`/`silence()` gated on the snapshot **container** at condition 100 | Gated on the `.original_value` **leaf**, numerically | Phase 11, plan 11-08 | 44 dead actions per fork became reachable; `verify_environmental_reachability()` armed |
| Capture written into a dictionary that was never saved | `save_state()` inside the applying arm, before the write | Phase 16, plan 16-01 | SAFE-01's "durably persisted" half became satisfiable at all; `verify_capture_persistence()` armed |
| `snapshot.<group>.changed_at` / `.changed_by_session_id` | Removed (D-02) | Phase 16, plan 16-04 | Written at 44 sites, read at none. **Do not reintroduce a `changed_by` leaf for grayscale** — `verify_no_removed_snapshot_leaf_reads()` exists specifically to keep that removal safe. |

**Deprecated / outdated in the live record — this phase's documentation debt:**

- `src/CONFIG-BLOCK.md`, the note beginning *"**Note — SUPERSEDED by BD-01-R (2026-08-13).**"* asserts both that Ash *is* a real Color Filters change (false in the artifact today) **and** the wrong `UA*` identifier with `operation = turn` (superseded by BD-01-R2). Both halves need correcting, not just the first.
- `src/CONFIG-BLOCK.md`'s `## Field reference` table has rows for `safety.brightness_floor`, `safety.dim_target` and `safety.allow_volume_increase` but **no row for `safety.ash_managed_color_filters`**, despite the key being live in the fenced literal. Adding it is part of making the record honest.
- The Shortcuts comment inside `ash()` (see §Code Examples) is a user-visible false assertion once this ships.
- `docs/phase5_self_check.py`'s Color Filters exclusion assertion (Pitfall 2).

## Environment Availability

| Dependency | Required by | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` ≥ 3.10 | Both builders, all 13 `docs/*.py` checkers, the validator | ✓ | system python3 (validator's own version gate passes) | — |
| Shortcuts Playground plugin | `validate-shortcut`, `sign-shortcut` | ✓ | 1.2.1 at `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/` | — |
| `shortcuts` CLI (macOS) | Signing | ✓ | measured: signed a probe successfully this session | — |
| Bundled ToolKit snapshot containing `AXToggleColorFiltersIntent` | Gate A passing clean | ✗ | absent from all three (v63, v78, v78-ios27) | **No fallback that preserves correctness.** See Open Question 2. |
| Read-back intent for any accessibility setting | §21 "do not clobber pre-existing state" by detection | ✗ | none across 35 intents in `AccessibilityUtilities.framework` | Opt-in flag + onboarding disclosure (settled user decision) |
| A connected iPhone (DIST-03) | Proving the toggle and the restore actually work | Uncertain | STATE.md records DIST-03 **LIFTED** as of the 2026-08-17/18 UAT session (Mirroring reachable); an earlier `16-06` measurement recorded `tunnelState: unavailable` | Ship structurally proven, author a UAT file, branch on the measured `tunnelState` at execution time — never on the `State` column |
| iOS Simulator | Rung-2 probe of the toggle | ✓ (iOS 26.5, iPhone 17 Pro booted) | 26.5 (23F77) | **Ceiling applies.** A simulator observation of an accessibility toggle is not promotable above `UNVERIFIED`; `Set Brightness` already fails outright there, and Color Filters is real-hardware environmental behaviour of the same class. |

**Missing dependencies with no fallback:** the ToolKit snapshot entry. This is a genuine catalog gap, not a project error, and it is the single reason gate A's disposition is a decision this phase must make.

**Missing dependencies with fallback:** accessibility read-back — fallback is disclosure plus `safety.ash_managed_color_filters`, already decided.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | **None conventional.** No pytest, no test runner, no `tests/` directory, no `pyproject.toml`, no Makefile. Verification is: two idempotent generators, 13 hand-written `docs/*.py` structural checkers (each `main()` raising `AssertionError` or `SystemExit`), plus the external Playground validator and signer. |
| Config file | none — each checker is a standalone script resolving `ROOT = Path(__file__).resolve().parents[1]` |
| Quick run command | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` (in-build `verify_*` guards run here; ~seconds) |
| Full suite command | `python3 tools/build_state_engine.py && python3 tools/build_sentient.py && for f in docs/*.py; do echo "== $f"; python3 "$f" || exit 1; done` |
| Baseline measured this session | `docs/environmental_restore_check.py` → passed; `docs/sequence_dispatch_check.py` → passed (0 orphans / 0 unreachable / 0 unknown / 0 duplicates); `docs/phase9_self_check.py` → passed (30/30 sites, 19 coerced, 11 correctly not); gate A on `src/PROSOCHE-Dumb.xml` → `Validation passed.` exit 0 |

### Phase Requirements → Test Map

| Req ID | Behavior | Test type | Automated command | File exists? |
|--------|----------|-----------|-------------------|-------------|
| CIRC-02 | The AX identifier is emitted at exactly 15 sites per fork, and the `UA*` twin at zero | structural | `python3 docs/phase5_self_check.py` | ✅ (assertion must be **inverted** — Wave 0) |
| CIRC-02 | `"Black and White"` still resolves to exactly one dispatch branch | structural | `python3 docs/sequence_dispatch_check.py` | ✅ passes unchanged |
| SAFE-01 | No grayscale apply is reachable from an unpersisted ownership marker | build guard | `python3 tools/build_state_engine.py` (`verify_capture_persistence`) | ✅ (guard must be **widened** — Wave 0) |
| SAFE-01 / CIRC-02 | No grayscale action sits in a permanently-true gate's dead arm | build guard | `python3 tools/build_state_engine.py` (`verify_environmental_reachability`) | ✅ (`ENVIRONMENTAL_IDENTIFIERS` must gain the id — Wave 0) |
| SAFE-01 | The bootstrap template seeds `settings_snapshot.color_filters.original_value` to the sentinel | build guard | `python3 tools/build_state_engine.py` (`verify_state_seed`) | ✅ (new seeder recogniser required — Wave 0) |
| SAFE-05 | `restore_managed_settings()` is still called by `manual_emergency_restore()` and `close_pipeline()`, and now restores three groups | structural | `python3 docs/environmental_restore_check.py` | ✅ (`EXPECTED_SITES` + seed loop — Wave 0) |
| SAFE-02 | Volume writes remain Media-scoped and counts unmoved at 15/15/22 | structural | `python3 docs/environmental_restore_check.py`, `python3 docs/phase9_self_check.py` | ✅ passes unchanged — **must stay unchanged** |
| AUDIT-02 | The record no longer asserts two contradictory things about Ash | manual read + grep | `grep -n "UAToggleColorFilters\|is a real system Color Filters" src/CONFIG-BLOCK.md` | ⚠️ prose — no mechanical assertion exists; consider a one-line addition to an existing checker |
| all | Signed artifacts match the manifest rows | structural | `python3 docs/manifest_check.py` | ✅ passes after re-sign |
| all | Gate A residue is exactly the enumerated deviation | **none today** | — | ❌ **Wave 0 gap** — see Open Question 2 |

### Sampling Rate

- **Per task commit:** `python3 tools/build_state_engine.py && python3 tools/build_sentient.py` — the in-build `verify_*` guards are the fastest signal and the strictest.
- **Per wave merge:** the full 13-checker loop, plus gate A on both forks.
- **Phase gate:** full suite green (with the gate-A residue check, if adopted), both forks re-signed, `docs/manifest_check.py` green, then `/gsd-verify-work`.

### Wave 0 Gaps

- [ ] `docs/phase5_self_check.py` — invert the Color Filters assertion (assert `AX*` present with a count; assert `UA*` still absent). Covers CIRC-02.
- [ ] `tools/build_state_engine.py` `ENVIRONMENTAL_IDENTIFIERS` — add the AX identifier. Covers CIRC-02/SAFE-01.
- [ ] `tools/build_state_engine.py` `verify_capture_persistence()` — replace the two-way `identifier.endswith("setbrightness")` group derivation with an identifier→group mapping including the AX identifier. Covers SAFE-01.
- [ ] `tools/build_state_engine.py` — new in-place recogniser pass in `seed_settings_snapshot()` for the third snapshot group. Covers SAFE-01/SAFE-05.
- [ ] `tools/build_state_engine.py` `VERIFIED_PARAMETER_KEYS` — add `{COLOR_FILTERS: {"state"}}` to opt the action into axis-1 protection.
- [ ] `docs/environmental_restore_check.py` — `EXPECTED_SITES` gains the AX identifier at 15; bootstrap-seed loop gains `"color_filters"`; `REQUIRED_SYMBOLS` gains any new guard symbol.
- [ ] **Gate-A residue check** — no mechanism exists today to assert "the validator's only complaints are the N enumerated ones". Recommended as a new `docs/` checker; see Open Question 2.
- [ ] A `14-UAT.md` device instrument, authored whether or not DIST-03 is reachable: nothing in this phase is device-proven by construction.

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1`. This is a local, offline iOS Shortcut: no network, no server, no auth, no session tokens, no persistence beyond one JSON file in the user's own iCloud Shortcuts folder and one Apple Note. Most ASVS categories are structurally inapplicable, and saying so explicitly is more useful than inventing coverage.

### Applicable ASVS Categories

| ASVS category | Applies | Standard control |
|---------------|---------|-----------------|
| V2 Authentication | no | No accounts, no credentials, no remote identity. The device passcode is the only authentication boundary and it is Apple's. |
| V3 Session Management | **partly, by analogy** | PROSOCHĒ has an `active_session` with an ownership compare (condition 4 against the Session ID token) that prevents a superseded CLOSE from restoring. The grayscale restore rides that same gate at `close_pipeline()`. Do not introduce a restore path outside it. |
| V4 Access Control | no | Single-user, single-device, no privilege boundary. |
| V5 Input Validation | **yes** | The untrusted inputs are (a) `state.json`, which the user can hand-edit or which can be left corrupt by a crash, and (b) the Shortcut Input string from the automation. The control is the numeric `> 0` gate: it is the only test that rejects **both** the `"null"` sentinel and an empty value, and it is device-measured (Donor 6 / 6.1). Grayscale must use it, not a string test. |
| V6 Cryptography | no | No crypto is performed. Signing uses Apple's own `shortcuts sign` (AEA1); nothing is hand-rolled. |
| V7 Error Handling & Logging | **yes, adversely** | Shortcuts has **no try/catch**. Safety is achieved by ordering and by gating, never by catching. This is why "persist then apply" is a security control and not a style preference. |
| V12 Files & Resources | **yes** | `state.json` is read with `WFFileErrorIfNotFound=False` and every dotted read must resolve against a seeded template, because a missing segment is a hard runtime error that aborts the run — potentially *before* a restore. |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard mitigation |
|---------|--------|---------------------|
| Apply grayscale, then crash/force-quit before the marker reaches disk → user stuck grey with no record | Denial of Service (against the user's own device) | Ordering: write marker → `save_state()` → apply. Pinned by `verify_capture_persistence()` **after** it is widened. |
| Restore leg placed in a dead arm → grayscale applies and never restores | Denial of Service | `verify_environmental_reachability()`, **after** `ENVIRONMENTAL_IDENTIFIERS` gains the identifier. |
| Sentinel or empty value passed into a gate as truthy → restore fires when nothing is outstanding, or fails to fire when something is | Tampering (via a hand-edited `state.json`) | Numeric `> 0` only. Never condition 100, never condition 5. |
| Dotted read of an unseeded `settings_snapshot.color_filters` → hard error aborts the run before `restore_managed_settings()` | Denial of Service | Bootstrap seeding + `verify_state_seed()`. This is exactly the mechanism that stranded users dimmed in Phase 12. |
| A future "fix" swaps `AX*` → `UA*` to satisfy the validator → a macOS action ships to an iPhone and Ash silently does nothing | Spoofing (a green check that certifies nothing) | Keep the `UA*`-absent half of `docs/phase5_self_check.py`'s assertion; record the deviation in `docs/BUILD-NOTES.md` where a future reader will find it. |
| Clobbering a user's own Color Filters setting (colour-blindness, migraine, low vision) | Tampering with assistive configuration | No read-back exists. Mitigation is disclosure + `safety.ash_managed_color_filters` opt-out, plus Emergency Restore always reachable (`verify_panic_escape_isolation()`). **This is an accessibility harm, and it is the reason the disclosure copy is a deliverable rather than a nicety.** |

## Project Constraints (from CLAUDE.md)

Directives extracted from `.claude/CLAUDE.md` that bind this phase. The planner should verify each plan against them.

1. **Native Shortcuts only, iOS 26.x** — no companion app, no private APIs. (The AX intent is a *private Apple intent* exposed through Shortcuts, not a private API call; it is authored as an ordinary action identifier and is donor-confirmed as user-authorable in Shortcuts.app.)
2. **Do-not-fabricate.** "Every iOS action identifier and parameter shape must be verified before use — if it cannot be verified, use the safest fallback, record the deviation, and keep the Shortcut runnable. Never fabricate an action because the strategy asks for it." Binds directly against synthesising an `AppIntentDescriptor`.
3. **Build provenance gate.** Before running either builder: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must succeed; abort the rebuild if it fails.
4. **Safety.** Every environmental change must be captured **and durably persisted** before it is applied and reliably restored; any setting whose original cannot be captured is left unchanged. Emergency Restore always available. **Colour Filters has no capture path at all**, which is why the ownership marker (rather than an original value) plus the opt-in flag is the compliant reading — record it as a deviation from the literal "capture the original" wording.
5. **Two-gate validator rule.** Gate A (`--target-macos 26 --target-platform all`) mandatory and must pass clean; gate B (`--target-macos 27 --target-platform all`) advisory, waivered at exactly one line per fork, never chained into a definition of done. **This phase forces an amendment to gate A's clause** — see Open Question 2.
6. **Definition of done includes signing.** "A valid XML draft without a signed `.shortcut` is not a useful stopping point." Signed filenames must equal the display names exactly, with no suffix.
7. **The nine parameter-defect axes** — see the dedicated analysis below.
8. **Evidence hierarchy.** Device donor > simulator observation > golden corpus > `.intentdefinition` > ToolKit catalog > inference. Spike 005's whole lesson is that the `.intentdefinition` was ranked too high; do not repeat it.
9. **Evidence ladder.** Never climb higher than the question requires; never skip a rung that would catch a defect in the probe itself. Rung 2's ceiling explicitly excludes real-hardware environmental behaviour.
10. **`$gsd-*` workflow enforcement** — no direct repo edits outside a GSD workflow.
11. **`/ponytail`** — prefer the minimal change; laziness never licenses skipping the nine axes or the do-not-fabricate protocol.

### The nine parameter-defect axes, applied to `AXToggleColorFiltersIntent`

Answering the brief's question 8 explicitly, axis by axis:

| Axis | Applies? | Ruling for this action |
|------|----------|------------------------|
| 1 — key names match the catalog exactly | **YES** | The catalog has no entry, so the *donor* is the authority: the only keys are `UUID` and `state`. `verify_parameter_keys()` currently **skips** unknown identifiers, so add `{COLOR_FILTERS: {"state"}}` to `VERIFIED_PARAMETER_KEYS` to arm the guard. `UUID` is already in `STRUCTURAL_KEYS`. |
| 2 — `str`-typed parameters need `WFTextTokenString` | **NO** | `state` is a bare plist `<integer>` in all three donors. Wrapping it in a text envelope would be a fabricated shape. This is the direct answer to "which axis governs its envelope": **none of the string axes do** — a literal integer parameter has no envelope. |
| 3 — `AttributedString` parameters need the same | **NO** | No `AttributedString` parameter exists on this intent. |
| 4 — required enum pickers must hold a literal case | **NO, and this is the subtle one** | Per the three-class picker rule, `operation` is the enum-picker-shaped parameter — and the donors prove Shortcuts *elides* it when the operation is Turn. `state` is declared `enumType=State` but Shortcuts renders a `State`-typed enum as an **On/Off switch** serialising a boolean, not as a picker. So there is no unfilled-picker hazard here and no picker literal to author. **Do not** add `operation` "for completeness" — that would write a literal (`turn`) no donor has ever emitted. |
| 5 — variable slots take the opposite envelope | **NO** | Both legs use literal constants. No variable is fed to this action in the recommended design, and none should be: a variable-fed `state` would reintroduce axis 6 for no benefit. |
| 6 — non-text parameters fed by a variable need an explicit coercion | **NO for the action; YES for the gates around it** | The action's operand is literal. But the `Config` read of `safety.ash_managed_color_filters` and the `settings_snapshot` leaf read are both gettext-fed and feed **numeric** conditionals — `normalise_numeric_operands()` attaches Donor 4.1's `WFCoercionVariableAggrandizement`/`WFNumberContentItem` automatically, and `verify_numeric_operands()` proves it. `CoercionItemClass` for booleans remains **unaudited** and must not be guessed; the design avoids the question entirely by treating the flag as a number, which *is* audited. |
| 7 — state shape must exist before it is read | **YES — the highest-risk axis for this phase** | `settings_snapshot.color_filters.original_value` is a dotted read; a missing segment is a hard runtime error. Seed the **container** as a permanent invariant, write and clear only the **leaf**. See Pitfall 1 for why adding to `SNAPSHOT_SEED` alone is insufficient. |
| 8 — `WFItems` row wrapper | **NO** | No `is.workflow.actions.list` is involved. |
| 9 — compound value read via `get_value()` not `read_value()` | **NO** | The marker is a scalar destined for a numeric comparison, which is exactly `read_value()`'s correct case. Do **not** add `color_filters` to `COMPOUND_STATE_KEYS`. |

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|-------|---------|---------------|
| A1 | Writing `1` to `settings_snapshot.color_filters.original_value` as an **ownership marker** (rather than a captured original) is an acceptable reading of SAFE-01's "capture the original" wording, given no read-back exists | Architecture Patterns; Don't Hand-Roll | If the user rejects it, the alternative is a differently-named leaf and generalising four guards — a materially larger change. Flag at planning, not at execution. |
| A2 | Old on-device `state.json` files need no migration for the new snapshot group, because BD-06-A1 records PROSOCHĒ as undeployed | Runtime State Inventory | A user with a pre-existing `state.json` would hit a hard error on the first dotted read of the new key — the exact class that stranded users in Phase 12. Verify BD-06-A1's scope before relying on it. |
| A3 | The AX action's site count will be exactly 15 per fork (11 apply + 4 restore) | Pitfall 6; Validation Architecture | Derived from the current 11 `primitive_dispatch()` renderings and 4 restore call sites, both measured — but it moves if the plan puts the apply anywhere else. Re-measure against the built artifact; do not transcribe. |
| A4 | Adding actions cannot breach `docs/note_identity_check.py`'s `MINIMUM_TOKEN_STRINGS = 1104` floor | Pitfall 8 | It is a *minimum*, so only a removal of token strings could breach it. Low risk; confirm by running the checker. |
| A5 | `shortcuts sign` succeeding on the probe implies it will succeed on the full fork carrying 15 AX sites | Environment Availability | The probe was 2 actions; the forks are ~4,200. Signing is content-agnostic in every prior build, but confirm on the first real rebuild rather than assuming. |
| A6 | The simulator cannot settle whether Color Filters actually toggles | Environment Availability | If a simulator *could* exercise it, one rung-2 pass would be far cheaper than a device session. Spike 010 measured `Set Brightness` failing outright on the simulator and `Get Device Details → Current Brightness` reading `0`; Color Filters is the same class of real-hardware environmental behaviour, but this specific action has **not** been probed there. A cheap rung-2 probe is worth ten minutes before requesting a device session. |
| A7 | DIST-03 is currently lifted (an iPhone is reachable via Mirroring) | Environment Availability; Open Question 3 | STATE.md's header says lifted as of the 2026-08-17/18 session; a Phase 16 entry recorded `tunnelState: unavailable`. **Branch on `tunnelState` read from `xcrun devicectl list devices --json-output` at execution time, never on the `State` column** — the column read `available (paired)` while the tunnel was down. |

## Open Questions (RESOLVED)

> All five were resolved before planning. Resolving authority is named on each. Nothing below
> is still open; this heading is retained so the reasoning that produced each answer stays
> readable next to the answer.

1. **Leaf naming: reuse `original_value`, or introduce an honest name?** — **RESOLVED: reuse, per the recommendation.** Authority: `14-CONTEXT.md` "Claude's Discretion" clause accepting this recommendation as written. Implemented in plan 14-01.
   - *What we know:* `clear_snapshot()`, `verify_capture_persistence()` (`key.endswith(".original_value")`), `verify_state_seed()` (`wanted` built from `SNAPSHOT_SEED`) and `_is_removed_snapshot_leaf()` all key on that exact leaf name. Reusing it costs zero guard changes on the naming axis; renaming costs four.
   - *What's unclear:* whether the semantic imprecision — the value is not an original, it is an ownership flag — is acceptable in a codebase that has repeatedly paid for names that overstate what they hold (`changed_by_session_id` written 44× and read 0×; `snapshot_g` documented as validating a reading it was evaluated before).
   - *Recommendation:* **reuse `original_value`**, and pay for it in the docstring — one paragraph in `clear_snapshot()` or a new `COLOUR_MARKER` constant stating plainly that for this group the leaf holds an ownership marker and never a captured original, because no read-back exists. Naming honesty is achieved by the record; guard coverage cannot be achieved by a comment.

2. **Gate A's disposition — the phase's one genuinely open decision.** — **RESOLVED: option (a).** Authority: user decision 2026-08-18, recorded as locked decision **D-14-01** in `14-CONTEXT.md`. Implemented in plan 14-04. One widening was forced during planning and is recorded there as a flagged assumption: the waiver must enumerate BOTH validator line families, because a descriptor-less action emits a missing-descriptor line per instance and D-14-01 itself forbids synthesising a descriptor, so a one-family waiver would be permanently unsatisfiable.
   - *What we know (measured, HIGH confidence):* gate A emits `Unknown AppIntent identifier` once per AX site and there is no allowlist, flag, env var, or repo-controllable data path. With no `AppIntentDescriptor` it emits a second line per site (≈30 lines/fork at 15 sites); with a fabricated descriptor, ≈15. Signing is unaffected and the artifact ships either way. `.claude/CLAUDE.md` currently says gate A "must pass clean, exit 0" and that a plan may not chain a permanently-failing gate into a definition of done.
   - *What's unclear:* which of three dispositions the user wants.
     - **(a)** Amend `.claude/CLAUDE.md`'s gate-A clause to "residue must equal exactly the enumerated waiver", mirroring gate B's existing treatment, and add a repo-local `docs/` checker that runs gate A on both forks, subtracts exactly the enumerated `Unknown AppIntent identifier` lines for the AX identifier, and **exits non-zero on anything else**. Cost: one new checker + a constitutional edit. Benefit: gate A keeps teeth for every other action, and the waiver is mechanical rather than remembered — the project's own stated preference after `retired_clause_check.py`.
     - **(b)** Emit a synthesised `AppIntentDescriptor` to halve the residue. **Not recommended:** it does not make gate A clean, and it fabricates three field values no donor supplies, into a plist iOS itself writes without one.
     - **(c)** Vendor a patched copy of the plugin's `data/toolkit-*.json` and point at it. **Not viable:** `skill_dir = Path(__file__).resolve().parents[1]` is fixed relative to the validator script; there is no override, and editing the plugin cache is outside the repo and lost on plugin update.
   - *Recommendation:* **(a)**, and make the constitutional edit an explicit, named task in the plan rather than a side effect. Also record the deviation in `docs/BUILD-NOTES.md`'s deviation log with the reproduction command, so a future reader hitting a red gate A finds the reason before reaching for the `UA*` identifier.

3. **Can a rung-2 simulator probe say anything about the toggle at all?** — **RESOLVED: yes, build it, and run it in this phase.** Authority: user decision 2026-08-18, recorded as locked decision **D-14-02** in `14-CONTEXT.md`. Implemented as plan 14-02 (spike 011), scoped so it cannot block the phase.
   - *What we know:* the booted simulator is iOS 26.5 and can import a signed `.shortcut` via `xcrun simctl openurl <udid> "file:///abs/path.shortcut"` + one synthesised tap (spike 010 retired spike 007's narrowing). `Set Brightness` fails outright on the simulator; `Get Device Details → Current Brightness` reads `0`.
   - *What's unclear:* whether `AXToggleColorFiltersIntent` **imports and runs without erroring** on the simulator. That is a different, weaker question than "does the screen go grey" — but it is a genuinely useful one, because it would catch an import failure or an unfilled-parameter error before a device session is spent.
   - *Recommendation:* build a no-blocking-UI probe (no `Show Alert` — the run wedges permanently), import it, run it, and record only what was observed. Do **not** promote any simulator result above `UNVERIFIED` for the grayscale behaviour itself.

4. **Is the phase "done" without a device pass?** — **RESOLVED: no, and the phase says so rather than pretending otherwise.** Authority: `14-CONTEXT.md` "Claude's Discretion" clause accepting this recommendation as written. `14-UAT.md` is authored regardless of DIST-03's state (plan 14-06), designed to run in the same sitting as `16-UAT.md`, and every device-gated truth across all six plans carries `verification: backstop` so an unconfirmable truth abstains to `human_needed` rather than passing silently.
   - *What we know:* Phase 16 shipped structurally proven and behaviourally unproven, and STATE.md says so plainly. Everything in this phase is in the same position by construction. CONTEXT.md notes that routing grayscale through `restore_managed_settings()` means **one device pass can prove all three environmental primitives** — which makes `16-UAT.md`'s twelve outstanding tests and a new `14-UAT.md` a single session rather than two.
   - *Recommendation:* author `14-UAT.md` regardless of DIST-03's state, and design it to be run **in the same sitting as `16-UAT.md`**. The highest-value single test is not "does the screen go grey" — it is **"force-quit mid-intervention, then run Emergency Restore, and confirm colour, brightness and volume all come back."**

5. **Does the emitted Shortcuts comment inside `ash()` need per-arm text?** — **RESOLVED: no — state the property the build guarantees, and keep the first line stable.** Authority: `14-CONTEXT.md` "Claude's Discretion" clause accepting this recommendation as written. Implemented in plan 14-01.
   - *What we know:* the comment ships 11× per fork and currently asserts Ash changes no accessibility setting. Under the opt-in flag, that assertion is true on one arm and false on the other, and the comment sits above the branch.
   - *Recommendation:* state the *property the build guarantees* rather than a per-arm outcome — "PROSOCHĒ turns Color Filters on only when you have allowed it, and always turns them back off" — following plan 16-03's precedent for `dimming()`'s retired bullet. Keep the comment's **first line stable**: `comment_index()` locates comments by prefix and other passes anchor on it.

## Sources

### Primary (HIGH confidence)

- `.planning/spikes/005-ios-color-filters-identifier/README.md` + `SetColourFilters-Shortcut.xml`, `Donor9-Shortcut.xml`, `Donor9.1-Shortcut.xml`, `AXToggleColorFilters-intentdefinition.txt` — read verbatim this session. Device-authored donors, decrypted via the AEA1 round trip. Tier 1.
- `tools/build_state_engine.py` — `ash()`, `dimming()`, `silence()`, `restore_managed_settings()`, `clear_snapshot()`, `primitive_dispatch()`, `config()`, `close_pipeline()`, `live_ice_redirect()`, `ice_expiry()`, `manual_emergency_restore()`, `seed_settings_snapshot()`, `verify_state_seed()`, `verify_capture_persistence()`, `verify_restore_gates()`, `verify_sentinel_gates()`, `verify_environmental_reachability()`, `verify_parameter_keys()`, `verify_circle_zero_silence()`, `main()`, and the constants `SNAPSHOT_SEED` / `SNAPSHOT_EMPTY` / `SNAPSHOT_SEEDED_*` / `ENVIRONMENTAL_IDENTIFIERS` / `VERIFIED_PARAMETER_KEYS` / `NUMERIC_OPERAND_FIELDS` / `CLEARED_SENTINEL` — all read this session.
- `tools/build_sentient.py` — import list and `main()`, read this session.
- `docs/phase5_self_check.py`, `docs/environmental_restore_check.py`, `docs/sequence_dispatch_check.py`, `docs/phase9_self_check.py`, `docs/manifest_check.py`, `docs/note_identity_check.py`, `docs/retired_clause_check.py`, `docs/router_ui_census.py`, `docs/sentient_core_check.py` — read this session.
- `src/CONFIG-BLOCK.md` — read in full this session; `safety.ash_managed_color_filters` confirmed present in the fenced literal and absent from the field-reference table.
- `src/PROSOCHE-Dumb.xml` — parsed with `plistlib` this session: import questions, the sole `com.apple.*` action and its `AppIntentDescriptor`, the Control Room Note body headings, and `WFWorkflowName` = `PROSOCHĒ — Nine Circles — Core`.
- `docs/CAPABILITY-DECISIONS.md` BD-01-R2 and `docs/BUILD-NOTES.md` CAP-20 — read this session.
- `.claude/skills/spike-findings-prosoche/references/environmental-primitives.md` and `references/authoring-parameters.md` — read this session.
- **Measured probes, this session:**
  - Gate A on a minimal AX plist → `Unknown AppIntent identifier` + `AppIntent action missing AppIntentDescriptor`, exit 1. Reproduce: `/tmp/axtest/t.xml`.
  - Gate A with a synthesised `AppIntentDescriptor` and two instances → descriptor error gone, one `Unknown AppIntent identifier` line **per instance**. Reproduce: `/tmp/axtest/t2.xml`.
  - Gate A on `src/PROSOCHE-Dumb.xml` → `Validation passed.` exit 0 (the baseline this phase changes).
  - `sign-shortcut /tmp/axtest/probe.xml --name AXProbe` → 21,698-byte signed `.shortcut`, clean exit. Signing is blind to the unknown identifier.
  - `validate_shortcut.py` source: only two CLI options beyond the path; `skill_dir = Path(__file__).resolve().parents[1]`; allowed ids from `data/toolkit-v*-tool-ids.json` ∪ `ACTIONS.md` ∪ `APPINTENTS.md` ∪ `THIRD_PARTY_ACTIONS.md`.
  - `docs/environmental_restore_check.py`, `docs/sequence_dispatch_check.py`, `docs/phase9_self_check.py` → all passed at HEAD.
- `.claude/CLAUDE.md` — project constraints, the nine axes, the evidence hierarchy and ladder, the two-gate rule.
- `.planning/REQUIREMENTS.md` (CIRC-02, SAFE-01, SAFE-02, SAFE-05, AUDIT-02), `.planning/ROADMAP.md` §Phase 14, `.planning/STATE.md`, `.planning/todos/pending/2026-08-16-build-ash-as-real-color-filters-grayscale.md`.

### Secondary (MEDIUM confidence)

- `~/.claude/plugins/.../APPINTENTS.md` line ~116 — documents the private `AX*` / public `UA*` accessibility-intent split for sibling toggles, and states the rule the donor satisfies.
- `.planning/STATE.md` on DIST-03's current state — the header says lifted; a Phase 16 entry records `tunnelState: unavailable`. Re-measure at execution time.

### Tertiary (LOW confidence)

- None. No WebSearch was performed and none was needed: every question this phase asks is answered by local device evidence or by reading this repository.

## Metadata

**Confidence breakdown:**
- Standard stack (identifier + both parameter legs): **HIGH** — three device donors read verbatim this session; zero inference.
- Architecture (where the change lands, which guards must move): **HIGH** — every symbol read directly, every call site enumerated, baseline checkers run green.
- Gate A behaviour: **HIGH** as a measurement, **MEDIUM** as a plan — the measurement is exact; the disposition is an open decision (Open Question 2).
- Pitfalls: **HIGH** — each derives from a documented, previously-shipped defect in this repo (cycle-10 container/leaf, 11-08 dead arm, 16-01 unpersisted capture, 16-04 D-02 seeder early-return).
- Device behaviour of the toggle and its restore: **LOW** — never executed on hardware, and the simulator is at or beyond its stated ceiling for this class of action.

**Research date:** 2026-08-18
**Valid until:** 2026-09-17 (30 days). Earlier if the Shortcuts Playground plugin updates — its bundled snapshots are the only thing between gate A and a clean run, and a future snapshot containing the AX identifier would retire Open Question 2 entirely.
