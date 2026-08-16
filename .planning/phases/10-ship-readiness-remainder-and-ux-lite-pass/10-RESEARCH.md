# Phase 10: Ship-readiness cleanup and UX-lite pass — Research

**Researched:** 2026-08-16
**Domain:** iOS 26 Shortcuts plist generation (single Python generator over a hand-authored plist), subtractive refactor + user-facing interaction pruning
**Confidence:** HIGH for code-level facts (all measured from the artifact in this session); MEDIUM for device-behaviour inferences; LOW where explicitly flagged as needing device evidence

---

## Summary

This phase is **not** a research-into-a-new-domain phase. Almost every question it raises is answerable by reading `tools/build_state_engine.py` (2,883 lines) and the artifact it emits, `src/PROSOCHE-Dumb.xml` (3,676 actions). This research therefore reads the code and reports line-level ground truth rather than surveying a technology space. Every count and index below was measured in this session by parsing the committed plist at `HEAD` (`2e85aa3`) — not recalled, not estimated.

Three findings change the shape of the plan materially:

1. **Two of the four Strand A chores are already done or half-done.** `.gitignore` exists and already covers `.DS_Store`/`__pycache__/`/`*.pyc` (item 2 — **DONE**, nothing to do). `MANIFEST.md`'s three **Dumb** rows are current and checksum-correct; its three **Sentient** rows are stale *and factually wrong* (they name a 2026-08-13 archive and 2,169,124-byte source; the real source is 2,250,377 bytes with a different hash). So item 3 is half-done, and the remaining half is a correctness fix, not a cosmetic refresh.

2. **The `--target-platform ios` instruction in the phase brief is a documented, re-measured landmine.** `docs/BUILD-NOTES.md` §13 DEV-01 records that this project deliberately validates with `--target-platform all`. I re-ran both invocations against the current artifact this session: `all` → `Validation passed.`; `ios` → rejects actions wholesale including `is.workflow.actions.comment` and `is.workflow.actions.conditional`. Any plan task that writes `--target-platform ios` into a `<verify>` field will produce noise, not signal.

3. **The spurious-UI complaints map onto three *distinct* code sites, only one of which is where the brief implies.** The note-picker fix (cycle 16) is **already applied** at the one and only `filter.notes` site — but the real "note opens when I didn't ask" defect is a *different* thing: `shownote` at action 3673 sits at depth 0 in the MANUAL arm and fires on **every** manual run regardless of menu choice. And the "menu on CLOSE" cannot be a CLOSE-arm menu, because the CLOSE arm contains **zero** menus — it must be the MANUAL menu reached by router fall-through, which is exactly the tradeoff `DEV-02` recorded in advance.

**Primary recommendation:** Plan Strand A as *four* tasks (MANIFEST Sentient-row correction; the brightness/volume cut; a Config-sequence repair that the cut forces and the todos do not mention; a requirements-amendment task), and Strand B as *three code tasks* (gate `shownote`; add `Setup Check`; reframe `Leaving / Continue`) plus one clearly-marked deferred UAT block. Use `--target-platform all`. Do not bump `schema_version`.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Menu / prompt emission and gating | Generator (`tools/build_state_engine.py`) | — | All OPEN-arm and MANUAL-menu structure is emitted by `manual_emergency_restore()`, `universal_leaving()`, `primitive_dispatch()`, `route_exit()` |
| Control Room note find / create / show | Hand-authored region of `src/PROSOCHE-Dumb.xml` (actions 3594–3673) | Generator *patch passes* (`fix_shownote_key()`, `fix_notes_filter_limit()`) | This block is **not** generated. The generator only patches it in place, idempotently |
| `state.json` shape (bootstrap seed) | Generator seed passes (`seed_settings_snapshot()`, `seed_pending_exit()`) over the hand-authored template at action 75 | Verify passes (`verify_state_seed()`, `verify_pending_exit_seed()`) | Template is a `WFTextTokenString`; edits must go through `_replace_in_token()` to shift attachment offsets |
| Tuning constants (thresholds, sequences, safety) | Hand-authored Config JSON at action 7 | — | Read at runtime via `config()`; **not** touched by any generator pass |
| Sentient fork | `tools/build_sentient.py` (reads Dumb, writes Sentient) | Imports 10 `verify_*` functions from `build_state_engine` | Hard import coupling — see Pitfall 3 |
| Validation / signing / archiving | Shortcuts Playground plugin wrappers on `PATH` | `/usr/bin/shortcuts` (signing only, macOS) | Repo has no `bin/`; wrappers resolve from the plugin cache |
| Device behaviour (runtime semantics, picker suppression) | The target iPhone — **currently unavailable** | Decrypted signed artifact (structure only) | `xcrun devicectl list devices` → `No devices found.` (re-confirmed this session) |

---

## Project Constraints (from CLAUDE.md)

Extracted as actionable directives the planner must honour:

| # | Directive | Impact on this phase |
|---|-----------|----------------------|
| C1 | Never fabricate an action identifier or parameter shape; use the safest fallback and record the deviation | Any new action (e.g. a gate conditional) must reuse a shape already proven in this artifact |
| C2 | Build-provenance guard: `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must pass before running either builder | **Verified PASS this session.** Must be the first step of any rebuild task |
| C3 | The seven parameter-defect axes (key name / string envelope / AttributedString / required picker / variable slot inverse / numeric coercion / state shape) | Every new emitted action is subject to all seven; the generator's own `verify_*` passes enforce them at build time |
| C4 | Verified runtime semantics: flat read of missing key → no value, no error; **dotted** read with a missing segment → HARD ERROR | Decisive for the `Setup Check` design — see Finding 3 |
| C5 | Operator/operand type validity is invisible in the plist; device inspection is a first-class evidence channel | Numeric gates on new variables must go through `normalise_numeric_operands()`, which runs automatically |
| C6 | Evidence hierarchy: donor shortcuts > golden corpus > ToolKit catalog > inference | Do not "improve" `filter.notes`/`shownote` beyond the Donor-8 shape already applied |
| C7 | Validator flags `--target-macos 26 --target-platform ios` | **Superseded in practice by DEV-01.** See Pitfall 1 — the plan must use `--target-platform all` |
| C8 | Signed `.shortcut` files ARE recoverable via `aea decrypt` + `aa extract` | This is the only non-device verification channel for "what actually shipped" |
| C9 | Fix whole classes, never site-by-site | The brightness/volume cut must remove *all* of `restore_managed_settings`/`dim()`/`silence()`/`settings_snapshot` and their guards together, not incrementally |
| C10 | Safety: no zero brightness, no unsafe volume, Emergency Restore always available | The cut removes the *mechanism* that could violate the first two; but it collides with requirement SAFE-05 — see Finding 2 |

---

## Phase Requirements

The ROADMAP assigns **no** requirement IDs (`Requirements: TBD`). However, this phase's work **invalidates or amends seven already-checked requirements**. The planner must treat these as in-scope even though they were not assigned:

| ID | Current text (abridged) | Effect of this phase | Recommended disposition |
|----|-------------------------|----------------------|-------------------------|
| **AUDIT-03** | Brightness read-back resolved; if no safe read path, Dimming degrades to a non-stateful variant | The cut *is* the degradation | Remains ✅ if Dimming survives as a non-stateful (message-only) primitive; ❌ if `dimming()` is deleted outright with no replacement |
| **AUDIT-04** | Same for Volume / Silence | Same | Same |
| **SESS-07** | CLOSE restores any environmental setting PROSOCHĒ itself changed | Becomes vacuously true (PROSOCHĒ changes nothing) | Amend text to state the vacuity explicitly, or the requirement silently becomes unfalsifiable |
| **CIRC-03** | Silence reduces media audio only when capture/restore possible, otherwise degrades safely | The cut is the "degrades safely" branch, permanently | Amend |
| **CIRC-05** | Dimming reduces brightness only when reversible, never zero, otherwise degrades safely | Same | Amend |
| **SAFE-01 / SAFE-02** | Brightness never zero / volume never increased | Vacuously true after the cut | Amend or note vacuity |
| **SAFE-05** | Emergency Restore clears cooldown, clears the active session, **and restores recoverable brightness, volume, and colour settings** | **Directly contradicted.** After the cut, Emergency Restore restores nothing environmental | Must be amended — this is the one hard requirement conflict in Strand A |
| **ROOM-10** | The manual menu offers Status, Open Control Room, Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Test a Circle, Reset Today, and Emergency Restore | Strand B adds a tenth item (`Setup Check`) | Amend the enumerated list |

`[VERIFIED: .planning/REQUIREMENTS.md lines 16–17, 58, 64, 66, 117, 123–128, read this session]`

---

## Finding 1 — Spurious-UI site inventory (Strand B)

All indices are **action indices in the current `src/PROSOCHE-Dumb.xml`** at `HEAD`. Router arm boundaries measured this session:

| Arm | Action range | Boundary evidence |
|-----|-------------|-------------------|
| Pre-router (config / clock / bootstrap / normalisation) | 0 – 91 | `Input Key` set at 89 |
| **OPEN** | 93 – 1212 | `If Input Key is OPEN` at 92, `Otherwise` at 1213 |
| **CLOSE** | 1216 – 1345 | `If Input Key is CLOSE` at 1215, `Otherwise` at 1346 |
| **MANUAL** | 1347 – 3673 | Occupies CLOSE's `Otherwise` arm; `End If` at 3674 / 3675 |

`[VERIFIED: plist parse, this session]`

### 1a. Every `choosefrommenu` (mode 0) site, with router branch

| # | Action | Arm | Generator source | Prompt | Items | Runtime trigger | Verdict |
|---|--------|-----|------------------|--------|-------|-----------------|---------|
| M1 | 171 | OPEN | `live_ice_redirect()` — `build_state_engine.py:1388–1398` | `Ice is active` | Return Home / Emergency Restore | Only when `cooldown_until > Now Epoch` (Circle IX active) | **KEEP** — self-explanatory, gated |
| M2 | **519** | OPEN | `universal_leaving()` — **`:895–905`** | `Circle ￼ opened. Leave now, or continue?` | **Leaving / Continue** | **EVERY genuine OPEN.** Emitted unconditionally at `open_pipeline():1105`, inside the genuine-open branch only (not duplicate, not cooldown) | **REFRAME** — see analysis below |
| M3 | 666 | OPEN | `select_exit()` — `:777` | `Leave now` | Take suggested exit / Choose another | Only after the user chose `Leaving` at M2 | KEEP — user-initiated |
| M4 | 726 | OPEN | `route_exit()` — `:790` | `Capture` | Notes / Voice Memos / Camera | Only when the owned exit is `Capture` | KEEP |
| M5 | 740 | OPEN | `route_exit()` — `:791` | `Coordinate` | Reminders / Calendar | Only when exit is `Coordinate` | KEEP |
| M6 | 803 | OPEN | `route_exit()` — `:832` | `Consult` | 6 items | Only when exit is `Consult` | KEEP |
| M7–M9 | 887, 901, 964 | OPEN | `route_exit()` **second rendering** | duplicates of M4–M6 | | `record_exit_and_route()` is called twice from `select_exit()` (`:778` and `:782`), so `route_exit()` is emitted twice | KEEP (structural duplication, not a UI defect) |
| M10 | 1054 | OPEN | `confession()` — `:503` | `Choose a boundary` | 2/5/10/15/Custom | Only when the dispatched primitive contains `Confession` | KEEP |
| M11 | **1350** | MANUAL | `manual_emergency_restore()` — **`:1419`** | `PROSOCHĒ` | 9 items | **Every manual run, and every mis-routed automation run** | **REFRAME** — this is the "menu on CLOSE" |
| M12 | 1363 | MANUAL | `:1429` | `Choose profile` | Paradise/Limbo/Inferno | Submenu of `Change Profile` | KEEP |
| M13 | 1394 | MANUAL | `:1435` | `Choose sequence` | Classic/BlackMirror/Ambient | Submenu of `Change Sequence` | KEEP |
| M14 | 1443 | MANUAL | `:1444` | `Test a Circle` | Circle 1–9 | Submenu of `Test a Circle` | KEEP |
| M15–M23 | 1521, 1753, 1985, 2217, 2449, 2681, 2913, 3145, 3377 | MANUAL | `confession()` via `primitive_dispatch("Test Circle")` × 9 | `Choose a boundary` | | Nine copies, one per Test-a-Circle branch | KEEP (structural) |

**Total: 23 menu-start sites; 148 `choosefrommenu` actions counting all modes.** `[VERIFIED: plist parse]`

**Critical negative result — the CLOSE arm contains NO menus at all.** Actions 1216–1345 contain exactly one `alert` (1289, `Contract` / overrun seconds, gated on `Declared Duration > 0`) and one `notification` (1334, unconditional CLOSE confirmation). There is no `choosefrommenu`, no `ask`, no `choosefromlist` anywhere in the CLOSE branch.

**Therefore the user's "menu surfacing on CLOSE" cannot be a CLOSE-arm menu.** The only code-visible explanation is **router fall-through**: an `Input Key` that is neither exactly `OPEN` nor exactly `CLOSE` lands in the MANUAL arm and shows M11. This is not an accident — `docs/BUILD-NOTES.md` §13 **DEV-02** records the tradeoff verbatim: *"a mis-typed automation now reaches the manual menu instead of an explicit rejection alert."* `[VERIFIED: docs/BUILD-NOTES.md §13, read this session]`

Candidate causes, ranked:
- **(a) The user's Automation B input is not exactly `CLOSE`** (trailing character, autocorrect, wrong action). Code-visible consequence, device-diagnosable in one look at the automation. **Most likely.**
- **(b) The Shortcut Input arrives as a non-string content item** so the `gettext → trimwhitespace → changecase` chain at 86–89 yields something other than `CLOSE`. **Needs device evidence** — cannot be established from the plist.
- **(c) The OPEN automation is also firing on close.** Outside this repo entirely.

**Planner constraint:** you cannot fix this by re-adding an absence gate. `verify_router_shape()` (`:1340–1357`) hard-fails the build if (i) a condition-100 `Input Key` gate reappears, (ii) the `Input Key` tests drift from exactly `[(4,"OPEN"), (4,"CLOSE")]`, or (iii) the MANUAL arm leaves the CLOSE `Otherwise` branch. Any Strand B change here must keep all three invariants. The safe, in-scope move is to make **M11's own prompt self-describing** (it currently reads only `PROSOCHĒ`, which tells a confused user nothing about why they are being asked).

### 1b. `Leaving / Continue` (M2) — why it appears "without the user understanding why"

`universal_leaving()` at `:895–905`:

```python
menu(group, 0, prompt=text_token([("Circle ", "Circle Next"),
                                   (" opened. Leave now, or continue?", None)]),
     items=["Leaving", "Continue"])
```

- It fires on **every genuine OPEN**, before any primitive, at every Circle 1–9. `open_pipeline():1105` — `a += save_state() + universal_leaving() + [...]`.
- It is **not** the intervention. The intervention is whatever `primitive_dispatch()` runs behind the `Continue` case. So at Circle 1 (Knock), the user sees the menu *then* an alert — two dialogs for one open.
- The generator comment at `:898–900` says this prompt was already once revised (`G-04-4b`) specifically so it "can no longer be mistaken for a CLOSE-path signal". It is still ambiguous: "Leave now, or continue?" does not say *leave what*, *continue to what*, or *why now*.
- The canonical strategy §6.4 argument (easy dismissal is the strongest mechanism) is what this menu implements — so **deleting it would be a product regression**, not a UX win. The scoped fix is copy plus, optionally, a Circle gate.

**Verdict: REFRAME (copy), do not delete.** A Circle-gated variant (e.g. offer the menu only from Circle ≥ 2) is a *design* change; flag it for the user rather than assuming it.

### 1c. Note-opening sites (`filter.notes` / `shownote` / Create Note)

There is exactly **one** of each. All three live in the **hand-authored** region of `src/PROSOCHE-Dumb.xml`, not in the generator.

| Action | Identifier | Fix status | Verdict |
|--------|-----------|-----------|---------|
| **3594** | `is.workflow.actions.filter.notes` | **cycle-16 fix IS APPLIED** — carries `AppIntentDescriptor{NoteEntity}`, `WFContentItemLimitEnabled=True`, `WFContentItemLimitNumber=1.0`, exactly the Donor-8 shape | **KEEP as-is.** Do not re-patch. `fix_notes_filter_limit()` (`:2688–2719`) is idempotent and returns early |
| **3611** | `com.apple.mobilenotes.SharingExtension` | `WFCreateNoteInput` correctly enveloped as `WFTextTokenString`; `name = "PROSOCHĒ — Control Room"` | KEEP |
| **3673** | `is.workflow.actions.shownote` | **cycle-14 fix IS APPLIED** — `WFInput = $Control Room Note` (not the old `target` key) | **GATE — this is the real spurious-note defect** |

**The `shownote` defect the brief did not name.** Action 3673 sits at **depth 0** within the MANUAL arm — i.e. outside every conditional. The hand-authored comment immediately above it (action 3672) states the intent explicitly:

> *"Whether or not that line was added, the setup note is always shown next below — a failed or skipped best-effort line here must never stop the note from being shown."*

Consequence: choosing **Status**, **Toggle Voice**, **Reset Today**, **Change Profile**, **Test a Circle**, or **Emergency Restore** all end by launching the Notes app and opening the Control Room note. Only one of the nine menu items ("Open Control Room") actually asks for that — and that branch is literally `action("is.workflow.actions.nothing")` (`:1426`), relying entirely on this unconditional tail.

This exactly matches "no note-list picker appearing when a Note is opened" in spirit, though it is a different mechanism than the cycle-16 picker fix. **The planner should treat the cycle-16 picker fix as done-and-verified-in-source and treat the ungated `shownote` as the actual Strand B work.**

**Recommended shape (reuses an established in-artifact pattern, satisfies C1):**
1. In `manual_emergency_restore()`, change the `Open Control Room` case at `:1426` from `nothing` to `*number(1, "Manual Show Note Requested")` — mirroring the existing `Manual Status Requested` / `Manual Refresh Requested` / `Manual Sync Requested` flags at `:1425`, `:1427`.
2. Add a new **idempotent** generator pass (precedent: `fix_shownote_key()`, `fix_notes_filter_limit()`) that wraps action 3673 — and optionally the 3669–3671 recovery-append block — in `if_block("Manual Show Note Requested", 2, number=0)` / `end_if(...)`.
3. Ordering: it must run in `main()` **after** `fix_shownote_key()` so it locates a `shownote` already carrying `WFInput`, and its idempotency check should be "is the action immediately preceding `shownote` already the matching If?".

Type-safety note: `"Manual Show Note Requested"` will be **undefined** on eight of nine menu branches. This is the *identical* shape as `Manual Status Requested` (defined only in the `Status` branch, tested at 3648 with condition 2 vs `WFNumberValue=0`) and is device-proven working. Because `number()` produces an `is.workflow.actions.number` output, `_already_numeric()` returns True and `normalise_numeric_operands()` correctly leaves it alone. `[VERIFIED: build_state_engine.py:2300–2321, 2452–2475; plist actions 3648–3653]`

### 1d. Every `ask` / `alert` / other dialog, by arm

| Arm | `ask` | `alert` | `notification` | `choosefromlist` | `speaktext` | Note actions |
|-----|------:|--------:|---------------:|-----------------:|------------:|-------------:|
| OPEN | 6 | 8 | 1 | 1 | 1 | 0 |
| CLOSE | 0 | 1 | 1 | 0 | 0 | 0 |
| MANUAL | 18 | 55 | 0 | 0 | 9 | 3 |
| **Total** | **24** | **64** | **2** | **1** | **10** | **3** |

`[VERIFIED: plist parse]`

**OPEN-arm `ask` sites** (all gated behind an exit route or a primitive — none is unconditional):

| Action | Prompt | Type | Gate | Verdict |
|--------|--------|------|------|---------|
| 770, 931 | `Where should Create open?` | URL | Only if exit = `Create` **and** no saved `profile_snapshot.create_target_url` | KEEP |
| 800, 961 | `What are you trying to find?` | Text | Only if exit = `Consult` | KEEP |
| 1051 | `What are you reaching for? (optional)` | Text | Only if dispatched primitive contains `Confession` | KEEP |
| 1068 | `How many minutes?` | Number | Only after choosing `Custom` at M10 | KEEP |

**OPEN-arm `alert` sites:**

| Action | Title / message | Gate | Verdict |
|--------|-----------------|------|---------|
| 792, 953 | `Create` / "No target was saved or opened." | Create-exit failure path | KEEP (error feedback) |
| **1002** | `PROSOCHĒ` / "Circle ￼ · pressure ￼ · heat ￼" | The **Knock** primitive (`knock()`, `:477–483`) | **REVIEW — duplicates the unconditional notification at 515.** `open_pipeline():1101–1103` fires a `notification` with byte-identical phrasing on *every* genuine OPEN. At Circle 1 (Knock) the user therefore gets: notification (515) → menu (519) → alert (1002). Three surfaces for one open |
| 1009 | `Ash` / "Pause. Put the phone down for one breath." | Ash primitive | KEEP |
| 1042 | `Silence` / "Volume could not be captured…" | Silence capture-failure path | **REMOVED by the Strand A cut** |
| 1102 | `Boundary` / "Choose a positive number of minutes." | Confession validation failure | KEEP |
| 1137 | `Dimming` / "Brightness could not be captured…" | Dimming capture-failure path | **REMOVED by the Strand A cut** |
| 1171 | `Mirror` / `$Mirror Text` | Mirror primitive | KEEP |

The **55 MANUAL alerts** are almost entirely structural: `Test a Circle` × 9 each renders the full `primitive_dispatch()`, so `Knock`/`Ash`/`Mirror`/`Boundary`/`Silence`/`Dimming` alerts each appear nine times. Only **one** MANUAL alert is a real distinct site: **3650**, the read-only `Status` display. `[VERIFIED: plist parse]`

### 1e. Consolidated verdict table (what the planner should turn into tasks)

| Site → Action | Function → line | Arm | Verdict | Blocking evidence needed? |
|---|---|---|---|---|
| `shownote` → **3673** | hand-authored; patched by `fix_shownote_key():2650` | MANUAL | **GATE** behind `Manual Show Note Requested` | No — source-verifiable |
| MANUAL menu prompt → **1350** | `manual_emergency_restore():1419` | MANUAL | **REFRAME** — prompt must say what this menu is and why the run reached it | No |
| `Leaving / Continue` → **519** | `universal_leaving():901` | OPEN | **REFRAME** copy; Circle-gating is a design question for the user | No for copy; yes for gating decision |
| Knock alert → **1002** vs notification → **515** | `knock():481` vs `open_pipeline():1101` | OPEN | **DEDUPLICATE** — pick one surface | No |
| `filter.notes` → **3594** | `fix_notes_filter_limit():2688` | MANUAL | **KEEP** — fix already applied, Donor-8-matched | Device confirmation of *behaviour* only (deferred UAT) |
| `Silence`/`Dimming` failure alerts → 1042, 1137 | `silence():575`, `dimming():552` | OPEN | **REMOVED** by Strand A cut | No |
| Router fall-through causing MANUAL menu on close | `restructure_router():1293`, guarded by `verify_router_shape():1340` | — | **DIAGNOSE, do not restructure** | **YES — device evidence required** |

---

## Finding 2 — The brightness/volume cut surface (Strand A item 5)

### 2a. The true count: **28**, not 18

| Measure | Value | Method |
|---|---|---|
| `is.workflow.actions.setbrightness` actions | **14** | plist parse |
| `is.workflow.actions.setvolume` actions | **14** | plist parse |
| **Total** | **28** | |
| Of which carry a **variable** operand | **28** (100%) | operand descriptor inspection |
| Of which carry a `WFCoercionVariableAggrandizement` | **0** | |
| Of which are therefore **uncoerced** | **28** | |
| `is.workflow.actions.getdevicedetails` actions (all in `dim()`/`silence()`) | **20** | plist parse |

`[VERIFIED: plist parse of src/PROSOCHE-Dumb.xml @ 2e85aa3, this session]`

**Which figure is right: 28.** Derivation that reconciles it exactly:

- `restore_managed_settings()` emits 1 `set_brightness` + 1 `set_media_volume` per call, and is called **4 times**: `close_pipeline():1185`, `live_ice_redirect():1394`, `ice_expiry():1403`, `manual_emergency_restore():1450` → **4 + 4 = 8**.
- `dimming()` emits 1 `set_brightness`; `silence()` emits 1 `set_media_volume`. Both are rendered inside `primitive_dispatch()`, which is called **10 times**: once from `universal_leaving():904` (OPEN) and nine times from the `Test a Circle` loop (`:1448`) → **10 + 10 = 20**.
- 8 + 20 = **28**. ✔

The **18** in `2026-08-15-ship-readiness-cleanup.md` traces to the generator's own cycle-14 comment (`build_state_engine.py:2330`, "plus 18 setbrightness/setvolume"). That was a count taken at cycle 14 against a different build and is **stale**. The sibling experimental branch's figure of **28** is correct today. `[VERIFIED: measured; the 18 figure CITED from build_state_engine.py:2330]`

### 2b. Complete removal surface — every symbol the cut must touch

Removing anything less leaves a dangling reference or a build-guard failure.

**Emitter functions (delete):**

| Symbol | Lines | Notes |
|---|---|---|
| `set_brightness()` | `:398–400` | Helper |
| `set_media_volume()` | `:403–405` | Helper |
| `device_detail()` | `:391–395` | **Used only by `dim()`/`silence()`** — verify no other caller before deleting |
| `clear_snapshot()` | `:408–426` | |
| `restore_managed_settings()` | `:429–474` | |
| `dimming()` | `:535–554` | |
| `silence()` | `:557–577` | |

**Call sites (remove the call *and* its surrounding comment/marker):**

| Caller | Line | What must happen |
|---|---|---|
| `close_pipeline()` | `:1184–1185` | Remove `RESTORE_MARKER` comment, the call, and the `--- PHASE 5 RESTORE MANAGED SETTINGS END ---` comment. **Note:** `RESTORE_MARKER` (`:21`) becomes an unused constant |
| `live_ice_redirect()` | `:1394` | Emergency Restore during Ice keeps only cooldown/session clearing |
| `ice_expiry()` | `:1403` | |
| `manual_emergency_restore()` | `:1450` | The `Emergency Restore` menu branch keeps only cooldown/session clearing → **contradicts SAFE-05** |
| `primitive_dispatch()` | `:658–660` | The dispatch tuple lists `("Silence", silence)` and `("Dimming", dimming)`. **See Finding 2c — this is the trap** |

**Config reads that become dead:**

| Read | Line | Config key |
|---|---|---|
| `dimming()` | `:548` | `safety.dim_target` |
| — | — | `safety.brightness_floor`, `safety.allow_volume_increase` become unreferenced Config JSON (action 7) |

**State-shape machinery (all of it becomes dead and must go together, per C9):**

| Symbol | Lines |
|---|---|
| `SNAPSHOT_SEED`, `SNAPSHOT_EMPTY`, `SNAPSHOT_SEEDED_EMPTY`, `SNAPSHOT_ROOT` | `:1781–1801`, `:2012` |
| `_snapshot_seed_text()` | `:1788–1794` |
| `seed_settings_snapshot()` | `:1847–1859`; called at `main():2833` |
| `verify_state_seed()` | `:1862–1923`; called at `main():2862` |
| `verify_restore_gates()` | `:2100–2139`; called at `main():2864` |
| The cycle-11/12 block comments | `:1752–1780`, `:1986–2012` — should be *rewritten as history*, not silently deleted (they encode axis-6/axis-7 lessons that still apply to `pending_exit`) |

**Do NOT delete** (still needed by `pending_exit` and by `active_session`): `CLEARED_SENTINEL`, `cleared_value()`, `_state_template()`, `_replace_in_token()`, `_sentinel_written_keys()`, `_read_variable_keys()`, `_enclosing_if_arms()`, `_tested_variable()`, `verify_sentinel_gates()`, `EXISTENCE_CONDITION_CODES`, `NUMERIC_CONDITION_CODES`, `NUMBER_COERCION`. `verify_sentinel_gates()` currently references `SNAPSHOT_ROOT` only indirectly — check `:2172` uses `parent.split(".")[0]`, which is generic; safe.

### 2c. **The trap the todos do not mention: Config sequences still name `Silence` and `Dimming`**

The runtime Config JSON (hand-authored, action 7) defines:

```json
"sequences": {
  "Classic":     ["Knock","Ash","Silence","Confession","Dimming","Exile","Mirror","Voice","Ice"],
  "BlackMirror": ["Knock","Confession","Ash+Confession","Mirror","Silence+Mirror","Dimming+Mirror","Exile","Voice","Ice"],
  "Ambient":     ["Ash","Silence","Dimming","Knock","Confession","Exile","Mirror","Voice","Ice"]
}
```

`primitive_dispatch()` matches with **condition 99 ("contains")** — `if_block("Selected Primitive", 99, string=name)` at `:664`. So if `dim()`/`silence()` and their dispatch arms are deleted with no replacement:

| Profile | Circle | Entry | Post-cut behaviour |
|---|---:|---|---|
| **Classic** (the default for `Limbo`, the default profile) | 3 | `Silence` | **No primitive fires. Silent no-op** |
| **Classic** | 5 | `Dimming` | **No primitive fires. Silent no-op** |
| BlackMirror | 5 | `Silence+Mirror` | Mirror still fires (contains "Mirror") — degraded but non-empty |
| BlackMirror | 6 | `Dimming+Mirror` | Mirror still fires — degraded but non-empty |
| **Ambient** | 2 | `Silence` | **Silent no-op** |
| **Ambient** | 3 | `Dimming` | **Silent no-op** |

Four Circles across the two most-used profiles would produce **no intervention at all** beyond the `Leaving / Continue` menu. That is a functional regression that no automated guard in the generator would catch (`primitive_dispatch` builds arms from a Python tuple; an unmatched Config string is simply never selected).

**The cut must be paired with one of:**
- **(A) Non-stateful replacements** — keep `dimming()`/`silence()` as message-only primitives (alert copy only, no `getdevicedetails`, no `setbrightness`/`setvolume`, no `settings_snapshot`). This is what AUDIT-03/AUDIT-04/CIRC-03/CIRC-05 literally specify ("degrades to a non-stateful variant"), keeps all four requirements green, and requires **no Config edit**. **Recommended.**
- **(B) Config sequence rewrite** — replace the six `Silence`/`Dimming` entries with surviving primitive names. Requires editing the hand-authored Config JSON at action 7, and changes the designed escalation curve.

Option A is strictly less invasive, preserves more requirements, and is the reading the requirements themselves already anticipate. `[VERIFIED: config JSON parsed from action 7; primitive_dispatch:658–666]`

### 2d. Runtime state / migration concern

| Question | Answer |
|---|---|
| Does anything read a `settings_snapshot` key at runtime after the cut? | **No** — the only readers are `restore_managed_settings()`, `dimming()`, `silence()`, all removed |
| What happens to an on-device `state.json` that still contains `settings_snapshot`? | **Nothing.** The keys become inert dead data. A flat read of an unused key is never performed; nothing enumerates the dictionary |
| Should `settings_snapshot` be removed from the bootstrap template? | Optional. Removing it is cosmetically cleaner but requires an `_replace_in_token()` edit with attachment-offset shifting (`:1819–1844`) — a real risk for zero functional gain. **Recommendation: leave the seed in place**, or remove it only with `verify_pending_exit_seed()`-style assertion coverage |
| Should `schema_version` be bumped to force a device rebuild? | **NO.** `fix_state_rebind()` (`:2750–2810`) bumps 1→2 specifically to force a one-time rebuild. Bumping to 3 would wipe every device's accumulated `heat`, `opens_today`, `exit_stats`, `recent_sessions`, and the user's synced `profile_snapshot.proforma`. Dead keys do not justify destroying learned state |

### 2e. Hard coupling: `tools/build_sentient.py` will break

`build_sentient.py:12–25` imports **`verify_restore_gates`** and **`verify_state_seed`** by name from `build_state_engine`, and calls them at `:216` and `:210`. Deleting either function makes `build_sentient.py` fail at **import time**.

The Strand A cut must therefore either (i) also edit `build_sentient.py` to drop those two imports and calls, or (ii) keep both functions as no-op stubs (ugly, and violates C9's "fix whole classes"). **(i) is correct.** `[VERIFIED: tools/build_sentient.py read this session]`

---

## Finding 3 — `Setup Check` feasibility (Strand B)

### 3a. What `state.json` already records

Bootstrap template (action 75) seeds these flat top-level keys as **JSON `null`**:

```json
"last_open_at": null,
"last_close_at": null,
"last_app": null,
"active_session": null,
```

Write sites:

| Key | Written at | Condition |
|---|---|---|
| `last_open_at` | `open_pipeline():1056` — `set_value("last_open_at", variable("Now Epoch"))` | Only inside the **genuine-open** branch: not on a cooldown short-circuit, not on a sub-2-second duplicate |
| `last_close_at` | `close_pipeline():1179` — `set_value("last_close_at", variable("Now Epoch"), "Reloaded State")` | Only when this CLOSE still **owns** the session (session-ID match after the 0.5 s delay) |

`[VERIFIED: build_state_engine.py:1056, 1179; bootstrap template parsed from action 75]`

### 3b. The two viable designs

**Design A — derive from existing keys, add nothing (zero new state).**

Gate `last_open_at` and `last_close_at` with a **numeric `> 0`** test (`if_block(name, 2, number=0)`), exactly as `restore_managed_settings()` gates its snapshot leaves.

Why numeric and not existence:
- Both keys are **flat** (single segment), so per C4 a read can never hard-error regardless of whether the key is present, absent, or null. ✔
- A numeric `> 0` is false for `"null"`, for `""`, and for a genuine JSON `null` under every plausible coercion — all three device-measured or device-implied (`"null" → WFNumberContentItem → >0 → FALSE, no error`, Donor 6.1 test 2; `"" → >0 → FALSE`, Donor 6 action 8). `[CITED: build_state_engine.py:443–444, quoting Donor 6.1 / Donor 6 device measurements]`
- A **condition-100 existence** gate is the wrong tool: it is exactly the axis-7 GATE-SEMANTICS trap the project already closed twice, and `verify_sentinel_gates()` exists specifically to prevent it.
- Every value ever written is a strictly positive epoch (`Now Epoch`), so `> 0` is true iff a genuine OPEN / owning CLOSE has ever been recorded.

**Honest limitation the planner must record:** this answers *"has a genuine OPEN / owning CLOSE ever been recorded"*, which is **sufficient but not necessary** for *"has Automation A/B ever fired"*. A CLOSE that fired but was superseded by a newer OPEN writes nothing; an OPEN inside a Circle-IX cooldown writes nothing. So Design A can produce a false "never fired" in edge cases. It cannot produce a false "has fired".

**Design B — two new flat sentinel keys (minimal, strictly correct).**

Add `"open_seen": 0` and `"close_seen": 0` to the bootstrap template, and write `set_value("open_seen", <1>)` as the **first** statement of the OPEN arm and `set_value("close_seen", <1>)` as the first statement of the CLOSE arm — before any gate, cooldown, debounce, or ownership check. Then `Setup Check` reads both flat keys with a numeric `> 0` gate.

Costs:
- Requires a bootstrap-template text edit via `_replace_in_token()` (offset-shifting), plus a `verify_*_seed()` guard to mirror `verify_pending_exit_seed()`'s discipline.
- Adds a `save_state()` concern: writing the flag needs to survive to disk. On the OPEN path the existing `save_state()` at `:1105` is *inside* the genuine branch, so a duplicate/cooldown OPEN would set the variable but not persist it. Making `open_seen` genuinely unconditional means adding a save on the non-genuine paths too — which is **more** than "minimal".
- **Legacy-file safety is fine**: a flat read of a key missing from an older `state.json` returns nothing (C4), so a numeric `> 0` reads false. **No `schema_version` bump is needed.**

### 3c. Recommendation

**Ship Design A.** It requires zero new state keys, zero bootstrap-template edits, zero new build guards, and zero migration surface. It reuses a device-proven gate shape. Present its edge-case limitation honestly in the `Setup Check` copy itself — e.g. *"Automation A: seen (last open recorded <time>)"* / *"Automation A: not seen yet"*, rather than an absolute claim. If the user rejects the edge cases, Design B is the escalation and should be a separate follow-up, not a lite-round item.

Implementation shape, reusing patterns already in the file:
1. Add `"Setup Check"` to the `choices` list at `manual_emergency_restore():1417`.
2. Add a menu case: `menu(group, 1, title="Setup Check"), *number(1, "Manual Setup Check Requested")`.
3. In `manual_note_refresh()`, add a display branch next to the existing Status branch (`:1472–1475`): read `last_open_at`/`last_close_at`, build two text verdicts via `if_block(..., 2, number=0)`, and show one `alert()` — reusing the **read-only, never-writes-the-Note** discipline already established for `Status` by the cycle-14 checkpoint decision (`:1467–1471`).
4. Update `ROOM-10` in `REQUIREMENTS.md` to list ten items.

**Explicitly out of scope (deferred to the heavy round):** any `state.json` funnel record (`import → first manual run → Note read → Automation A created → …`). That is item 2 of the source todo and is named in the ROADMAP's own Deferred list.

---

## Finding 4 — What is actually in the first-run path today (Strand B, onboarding)

Traced action-by-action. **User-visible** steps only:

| Step | Where | What the user sees |
|---|---|---|
| 1 | `WFWorkflowImportQuestions[0]` → action 2 | *"Choose your descent: Paradise, Limbo, or Inferno. If you are not sure, choose Limbo."* — free-text prefill, default `Limbo` |
| 2 | `WFWorkflowImportQuestions[1]` → action 4 | *"May PROSOCHĒ speak to you at the highest circles? Answer yes or no."* — free-text prefill, default `yes` |
| 3 | actions 6–84 | **Nothing visible.** Config load, clock, state-file read, folder create, normalisation, bootstrap write. Zero alerts, zero prompts |
| 4 | actions 85–92 → 1347 | **Nothing visible.** Router normalises absent input → falls through to MANUAL |
| 5 | **action 1350** | **A nine-item menu titled only `PROSOCHĒ`**, with no explanation, shown *before* the user has ever seen the Control Room note |
| 6 | user must pick one of 9 | Every item does something. There is no "just show me the instructions" item other than `Open Control Room`, which is a `nothing` no-op |
| 7 | actions 3594–3613 | Note found or created (5,121-char, 102-line markdown body, action 3608) |
| 8 | action 3673 | Notes app opens the Control Room note — **unconditionally, whatever was chosen at step 5** |
| 9 | outside the app | User reads `## READ THIS FIRST`, then two 10-step Automation build procedures, and builds them by hand in Shortcuts |

`[VERIFIED: plist parse and WFWorkflowImportQuestions read this session]`

**Redundancies / ordering defects this trace exposes — all in scope for "tighten the first-run path":**

| # | Issue | Fix shape |
|---|---|---|
| O1 | The menu (step 5) precedes the note (step 8). A first-run user is asked to choose from nine unexplained options before receiving any instructions | Reorder, or make the MANUAL menu prompt self-describing, or add a first-run-aware default |
| O2 | `Open Control Room` is a no-op (`:1426`) whose effect is delivered by an unconditional tail | Directly resolved by the Finding-1c `shownote` gate — the two changes are the same edit |
| O3 | The `PROSOCHĒ` menu prompt carries no context at all | One-line prompt rewrite at `:1419` |
| O4 | Nothing distinguishes a first run from a return visit — the same nine items every time | A `Setup Check` item (Finding 3) partially addresses this; a genuine first-run branch is heavier |
| O5 | The import questions are free text with no validation feedback; a typo silently becomes `Limbo` (`:58–63` normalisation) | Out of scope this round (Note copy, not mechanism) — but worth recording |

**Explicitly OUT of scope this round (deferred, per the source todo's "Scope split — 2026-08-16"):**
- Deferring the `MY PHONE, ON PURPOSE` proforma out of the critical path (note body lines 48–76).
- Shortening the `READ THIS FIRST` block to the two automations plus the safety warning.
- The §29 voice copy rewrite across all nine Circles.
- The read-once-vs-return-to Note restructure (coordinated with Build Addendum 01's rename).
- Funnel instrumentation in `state.json`.
- Full fresh-import end-to-end funnel re-verification.

**The plan must not pull these forward.** They are named in both the ROADMAP phase text and the todo's Deferred section.

---

## Finding 5 — The rebuild / validate / sign / verify loop

### 5a. Environment (all re-verified this session)

| Tool | Path | Status |
|---|---|---|
| `validate-shortcut` | `~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/bin/validate-shortcut` (on `PATH`) | ✓ |
| `sign-shortcut` | same directory (on `PATH`) | ✓ |
| `/usr/bin/shortcuts` | macOS built-in | ✓ |
| `aea`, `aa` (AEA1 recovery) | macOS built-in | assumed present (used successfully in prior cycles) |
| `python3` | system | ✓ (3.10+, PEP 604 syntax in the validator works) |
| `xcrun devicectl list devices` | — | **`No devices found.`** — DIST-03 blocker live |
| `timeout(1)` | — | **NOT available** on this machine (zsh/macOS). Do not put `timeout` in plan commands |

### 5b. Canonical command order

```bash
# 0. Provenance guard — MANDATORY, per .claude/CLAUDE.md. Verified PASS at HEAD this session.
git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD

# 1. Regenerate Dumb (MUTATES src/PROSOCHE-Dumb.xml IN PLACE — it is both input and output)
python3 tools/build_state_engine.py

# 2. Regenerate Sentient from the fresh Dumb (only if Sentient is in scope this phase)
python3 tools/build_sentient.py

# 3. Structural self-checks (see 5c for the CURRENT BASELINE — three of six already fail)
python3 docs/state_engine_self_check.py
python3 docs/phase7_self_check.py
python3 docs/sentient_audit_check.py

# 4. Validate — NOTE THE FLAG. Use `all`, NOT `ios`. See Pitfall 1.
validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all

# 5. Archive + sign, in ONE step, with the EXACT invocation (never a pre-dated --output-dir)
sign-shortcut src/PROSOCHE-Dumb.xml --name "PROSOCHĒ — Nine Circles — Dumb" \
  --mode anyone --output-dir artifacts/shortcuts

# 6. Decrypt-verify what actually shipped (the only non-device "what shipped" channel)
signed="artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut"
dir="$(mktemp -d)"
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed" "$dir/leaf.der"
openssl x509 -inform DER -in "$dir/leaf.der" -noout -pubkey > "$dir/pub.pem"
aea decrypt -i "$signed" -o "$dir/payload.aa" -sign-pub "$dir/pub.pem"
mkdir -p "$dir/unwrapped" && aa extract -i "$dir/payload.aa" -d "$dir/unwrapped"
plutil -convert xml1 -o "$dir/Shortcut.xml" "$dir/unwrapped/Shortcut.wflow"

# 7. Refresh MANIFEST rows
shasum -a 256 src/PROSOCHE-Dumb.xml "$signed"
stat -f%z src/PROSOCHE-Dumb.xml "$signed"
```

`[VERIFIED: HANDOFF.md canonical invocation banner; docs/BUILD-NOTES.md §3; .claude/CLAUDE.md §8; commands re-run or path-checked this session]`

**`sign-shortcut` side effects the planner must expect:** it writes the pre-sign unsigned XML to `artifacts/shortcuts/<today>/<name>-<HHMMSS>.xml` (one dated level) **and** signs to the canonical `artifacts/shortcuts/<name>.shortcut`. No manual promotion step exists or should be added. Passing an already-dated `--output-dir` produces the doubled-path defect recorded in HANDOFF.md's Process Note.

### 5c. **Current self-check baseline — three of six already FAIL at `HEAD`**

Measured this session, before any Phase 10 change:

| Script | Status at `HEAD` | Cause |
|---|---|---|
| `docs/state_engine_self_check.py` | **PASS** | — |
| `docs/phase7_self_check.py` | **PASS** | — |
| `docs/sentient_audit_check.py` | **PASS** | — |
| `docs/phase5_self_check.py` | **FAIL** (`StopIteration`) | Looks for a condition-100 `Input Key` gate. That gate was **deliberately removed** by the cycle-3 router restructure (DEV-02). The check is obsolete, not a regression |
| `docs/phase6_self_check.py` | **FAIL** (`AssertionError: Open App route shape`) | Requires `WFAppName` in `openapp` params; `normalize_open_apps()` (`:2638–2647`) clears params and re-emits only `WFAppIdentifier` + `WFSelectedApp`. Check is stale |
| `docs/sentient_core_check.py` | **FAIL** (`AssertionError`) | Sentient is stale — built at `2026-08-14k`, before cycles 14–16 and before the notification work. `src/PROSOCHE-Sentient.xml` contains **0** `is.workflow.actions.notification` actions vs Dumb's 2 |

**This is a plan-shaping fact.** If a task's `<verify>` says "all self-checks pass", it fails for three pre-existing reasons unrelated to this phase. The planner must either (a) scope `<verify>` to the three green scripts, or (b) add explicit repair tasks for `phase5_self_check.py` / `phase6_self_check.py` (both are one-line staleness fixes), or (c) accept and record them as known-red. **Recommendation: (b) for the two stale scripts — they are cheap and their redness masks real regressions — and leave `sentient_core_check` red with a documented reason, since re-forking Sentient is SEED-005 / a separate todo.**

### 5d. MANIFEST.md — measured drift

| Row | MANIFEST says | Actual (measured) | Status |
|---|---|---|---|
| Dumb source | 2,231,608 / `1cc64598…` | 2,231,608 / `1cc64598…` | ✔ current |
| Dumb archive `2026-08-16/…-220924.xml` | 2,231,608 / `1cc64598…` | 2,231,608 / `1cc64598…` | ✔ current |
| Dumb signed | 189,792 / `89418e28…` | 189,792 / `89418e28…` | ✔ current |
| **Sentient source** | 2,169,124 / `9d547896…` | **2,250,377 / `c3c63771…`** | ✘ **wrong** |
| **Sentient archive** | `2026-08-13/…-191155.xml` | source actually matches `2026-08-14/…-232448.xml` | ✘ **wrong** |
| **Sentient signed** | 187,660 / `73b91f9e…` | **192,965 / `75fdd78c…`** | ✘ **wrong** |
| Header | *"Built 2026-08-13 with … `--target-platform all`"* | Dumb rebuilt 2026-08-16 | ✘ stale date; flag `all` is correct per DEV-01 |

Archive directories present: `2026-08-13/` (6 files), `2026-08-14/` (22), `2026-08-15/` (1), `2026-08-16/` (3). The todo's "add the 2026-08-14/15 archive entries" is best read as "make the table describe the current canonical artifacts and note the archive lineage" — enumerating all 32 archives would be noise.

---

## Finding 6 — Device-verification blockers and how to structure around them

`xcrun devicectl list devices` → **`No devices found.`** (re-run this session). DIST-03 is live.

### 6a. Criterion-by-criterion triage

| Acceptance criterion | Needs a device? | Non-device substitute available |
|---|---|---|
| `.gitignore` covers `.DS_Store`/`__pycache__`/`*.pyc` | **No** | `cat .gitignore` — **already satisfied** |
| MANIFEST rows match reality | **No** | `shasum -a 256` + `stat -f%z` |
| `restore_managed_settings`/`dim()`/`silence()`/`settings_snapshot` removed | **No** | `grep` the generator; count `setbrightness`/`setvolume` in the rebuilt plist must be **0** |
| No dangling references after the cut | **No** | `python3 tools/build_state_engine.py` runs the 15 `verify_*` passes; `python3 -c "import tools.build_sentient"` catches the import break |
| Config sequences no longer name a deleted primitive | **No** | Parse Config JSON at action 7, cross-check against `primitive_dispatch()`'s tuple |
| `shownote` is gated behind `Open Control Room` | **No (structure)** / **Yes (behaviour)** | Structure: assert action-3673's immediate predecessor is the matching `conditional` mode-0 in the rebuilt plist, and re-assert after decrypting the signed artifact |
| `Setup Check` item present and reads the right keys | **No (structure)** / **Yes (copy correctness on device)** | Assert the menu item string and the `getvalueforkey` keys in the rebuilt plist |
| Menu/prompt copy reads correctly | **No** | String assertions against the rebuilt plist |
| **Control Room "Open Control Room" shows no note picker** | **YES — hard blocker** | None. This is a *behavioural* claim about an iOS interactive fallback. The plist-level fix is verified present (Donor-8-matched); its *effect* is not |
| **No menu appears on CLOSE** | **YES — hard blocker** | Partial: the CLOSE arm provably contains zero menus. But diagnosing *why* the user saw one requires inspecting their Automation B on device |
| OPEN-path regression after the cut + menu changes | **YES** | Partial: validator + 15 build guards + decrypt-diff against `2026-08-15o` |
| `Leaving / Continue` copy comprehension | **YES (judgement)** | None — it's a human comprehension claim |

### 6b. Recommended plan structure

**Do not let the phase stall on the device.** Structure it as:

1. **Wave 1 — fully source-verifiable** (Strand A items 2/3/5 + the Config repair + the Strand B code changes). Every `<verify>` is a `grep`, a plist assertion, a self-check, or the validator. These can complete and commit today.
2. **Wave 2 — build + sign + decrypt-verify.** Structural assertions re-run against the *decrypted signed artifact*, not just `src/`. This is the strongest non-device evidence channel (C8) and catches "the signed file isn't what I built".
3. **Wave 3 — a single `checkpoint:human-verify` task holding ALL device-dependent criteria**, explicitly marked deferred-on-DIST-03, with the precedent already set by `.planning/phases/08-sentient-fork-dual-distribution/08-03-PLAN.md` Task 2 and `.planning/quick/260816-ukb-…/260816-ukb-SUMMARY.md`. That precedent's wording is the model: *record the blocker honestly, leave the criterion unchecked, never substitute a Mac import or fabricated evidence.*

The phase can **seal** with Wave 3 explicitly outstanding, exactly as the breadcrumb-strip quick task sealed on 2026-08-16.

Recommended deferred-UAT bundle (one task, five checks):
- Tap `Open Control Room` → the resolved note opens and **no note list appears**.
- Tap `Status` / `Toggle Voice` → the Notes app does **not** open (regression check for the `shownote` gate).
- Tap `Setup Check` after zero opens → both automations report "not seen"; after one real OPEN → Automation A reports seen.
- Trigger Automation B (CLOSE) → **no menu appears**; if one does, screenshot the automation's Run Shortcut input field.
- Trigger Automation A (OPEN) → Circle/Pressure/Heat notification, then `Leaving / Continue`, then the Circle-1 primitive — i.e. the `2026-08-15o` OPEN-path result reproduces after the cut.

---

## Finding 7 — Regression risk

### 7a. What is actually at risk

Three edits land in the **same control-flow region** within one build:
1. The breadcrumb strip (already landed at `154b998`/`2e85aa3`, **on-device regression confirmation still outstanding**).
2. The brightness/volume cut — removes 28 actions plus ~4 `restore_managed_settings()` expansions plus 20 `getdevicedetails`, changing action indices throughout OPEN, CLOSE, and MANUAL.
3. Strand B's menu/gate changes — inserts a conditional pair into the MANUAL tail and adds a menu case.

**Index-fragility is the dominant risk class.** The generator is explicitly designed against it (`comment_index()` matches on comment-text prefixes, `flow_index()` on `GroupingIdentifier`, `_state_template()` by content). But two things are **not** index-immune:
- `_replace_in_token()` (`:1819–1844`) shifts `attachmentsByRange` offsets on template text edits and raises if an offset stops pointing at a placeholder. Any bootstrap-template edit (Design B for `Setup Check`, or removing the `settings_snapshot` seed) goes through this. **Its own guard is good** — it raises rather than corrupting.
- `main()`'s `pinned` check (`:2818`, `:2877`) asserts actions 0–4 are byte-identical after the run. Adding an import question would trip this.

### 7b. Non-device evidence that genuinely substitutes

| Evidence | Catches |
|---|---|
| `python3 tools/build_state_engine.py` (runs 15 `verify_*` passes) | All seven parameter-defect axes, router shape, sentinel gates, compound reads, numeric coercion, state seed |
| `validate-shortcut … --target-platform all` | Structural/plist correctness, unknown identifiers, empty strings |
| `python3 -c "import tools.build_sentient"` | The `verify_restore_gates`/`verify_state_seed` import break (Finding 2e) |
| Decrypt-diff of the new signed artifact against the `2026-08-15o` archive | Confirms the OPEN critical path's *structure* (breadcrumb-free, Circle scan, `complete_pending_exit()`, notification, `universal_leaving()`) survived the cut |
| Plist assertion: `count(setbrightness) == 0 and count(setvolume) == 0 and count(getdevicedetails) == 0` | Cut completeness |
| Plist assertion: every `sequences.*` entry contains at least one name in `primitive_dispatch()`'s tuple | The Finding-2c silent-no-op trap. **This does not exist today — it is worth adding as a new build guard** |
| Router-arm menu census (0 menus in CLOSE, N in OPEN, M in MANUAL) | Strand B regressions |

### 7c. What non-device evidence does **not** catch

Per C5 and the project's own record: operator/operand type validity, interactive-fallback behaviour (the note picker), iOS's actual reading of `WFMenuPrompt` composition, whether `speaktext`'s `WFText` key works (DEV-C3-03 still open), and whether the `Leaving / Continue` reframe reads well to a person. These belong in Wave 3.

### 7d. Interaction risk: Strand A × Strand B

Low-to-moderate, and mitigable by ordering:
- Strand A **removes** two dispatch arms and four `restore_managed_settings()` expansions; Strand B **adds** one conditional pair in the MANUAL tail and one menu case in `manual_emergency_restore()`.
- They touch overlapping *functions* (`manual_emergency_restore()` for both) but non-overlapping *statements*.
- **Recommended ordering: Strand A first, then Strand B.** Strand A shrinks the MANUAL arm (removing `restore_managed_settings()` from the `Emergency Restore` branch), so Strand B's insertion lands in a smaller, already-verified structure. Doing them in one rebuild is fine; doing them in one *commit* is not — separate commits keep the decrypt-diff meaningful.

---

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Locating a generated region to replace | Index arithmetic over `WFWorkflowActions` | `comment_index()` / `replace_marker_block()` / `insert_or_replace_after()` (`:1194–1244`) | Every index shifts when the cut removes ~200 actions |
| Locating a control-flow endpoint | Scanning for the Nth `conditional` | `flow_index(actions, group, mode)` (`:1247`) | `GroupingIdentifier` is the only stable handle |
| Editing the bootstrap `state.json` template | String replace on the plist | `_state_template()` + `_replace_in_token()` (`:1804`, `:1819`) | Raw replace corrupts `attachmentsByRange` offsets; BEST_PRACTICES warns out-of-bounds ranges can crash Shortcuts on import |
| Patching a hand-authored action | Hand-editing `src/PROSOCHE-Dumb.xml` | A new **idempotent** pass in `main()`, modelled on `fix_shownote_key()` / `fix_notes_filter_limit()` | The generator rewrites `src/` in place on every run; a hand edit outside a marker survives, but the intent is invisible and untested |
| Number-typing a new operand | Hand-writing `Aggrandizements` | `normalise_numeric_operands()` (`:2456`) runs automatically | Donor-4.1 shape, applied structurally; hand-writing it re-opens axis 6 |
| Wrapping a variable in a conditional input slot | `token()` / `text_token()` | `if_block()` (`:259`) — which uses `variable()` | Rules 2 and 5 are inverses; `verify_conditional_inputs()` will fail the build |
| Deciding whether a new dialog is safe | Reasoning from the ToolKit catalog | `VERIFIED_PARAMETER_KEYS` + `STRING_ENVELOPE_PARAMS` + `REQUIRED_PICKER_PARAMS` (`:1508`, `:1587`, `:1626`) | These encode device/donor ground truth the catalog lacks |
| Verifying "what shipped" | Trusting `src/` + mtime | AEA1 decrypt recipe (§5b step 6) | Established practice in this project |

**Key insight:** this generator has spent 16 debug cycles building a guard for every class of defect it has ever shipped. Any new code should route through those guards rather than around them; the fastest way to introduce an eighth defect axis is to hand-author something the guards cannot see.

---

## Common Pitfalls

### Pitfall 1 — Writing `--target-platform ios` into a verify command
**What goes wrong:** the validator rejects the whole file. Re-measured this session against the current artifact: `--target-platform all` → `Validation passed.`; `--target-platform ios` → rejects actions wholesale, *including* `is.workflow.actions.comment` and `is.workflow.actions.conditional`, which are present in the bundled snapshot.
**Why:** the bundled iOS snapshot is demonstrably incomplete; `is.workflow.actions.conditional` is absent from **both** the iOS-27 and v63 snapshots. `docs/BUILD-NOTES.md` §13 DEV-01 records this as a deliberate, measured deviation from `.claude/CLAUDE.md`.
**Avoid:** use `--target-macos 26 --target-platform all` everywhere. Cite DEV-01 in the plan so it does not look like drift.
`[VERIFIED: both invocations run this session]`

### Pitfall 2 — Cutting `dim()`/`silence()` without touching Config
**What goes wrong:** Classic Circles 3 and 5 and Ambient Circles 2 and 3 become silent no-ops. No build guard catches it. See Finding 2c.
**Avoid:** prefer non-stateful replacements (Option A); if deleting outright, edit the Config JSON at action 7 and add a build guard cross-checking `sequences.*` against `primitive_dispatch()`'s tuple.

### Pitfall 3 — Deleting `verify_restore_gates` / `verify_state_seed` without editing `build_sentient.py`
**What goes wrong:** `tools/build_sentient.py` fails at **import** (`:12–25`), so the Sentient fork cannot be built at all.
**Avoid:** edit both files in the same commit; verify with `python3 -c "import sys; sys.path.insert(0,'tools'); import build_sentient"`.

### Pitfall 4 — Bumping `schema_version` to 3
**What goes wrong:** every device takes the rebuild branch and loses `heat`, `opens_today`, `gravity`, `exit_stats`, `recent_sessions`, and the synced `profile_snapshot.proforma`.
**Why it looks tempting:** `fix_state_rebind()` (`:2750`) did exactly this for 1→2, for a *correctness* reason (old files lacked the settings_snapshot/sentinel fixes).
**Avoid:** the cut leaves only inert dead keys. A flat read of an unused key is never performed. Do not bump.

### Pitfall 5 — Assuming the cycle-16 note-picker fix still needs applying
**What goes wrong:** re-patching or "improving" action 3594, breaking a Donor-8-matched shape.
**Reality:** `AppIntentDescriptor` + `WFContentItemLimitEnabled=True` + `WFContentItemLimitNumber=1.0` are all present in the committed artifact. `fix_notes_filter_limit()` is idempotent and returns early. **The only outstanding work on this item is device confirmation.**

### Pitfall 6 — Treating "menu on CLOSE" as a CLOSE-arm bug
**What goes wrong:** editing the CLOSE arm, which contains no menus, or re-adding an absence gate, which `verify_router_shape()` hard-fails.
**Reality:** it is router fall-through into MANUAL, the exact tradeoff DEV-02 recorded. Fix the MANUAL prompt's clarity; diagnose the automation input on device.

### Pitfall 7 — Adding a menu without a preceding comment
**What goes wrong:** `main()` (`:2841–2851`) auto-inserts a generic `"Control-flow check: …"` comment before any control-flow start lacking one. Harmless, but it silently pads the artifact and makes decrypt-diffs noisier than expected.
**Avoid:** author the intent comment yourself so the generic filler is not used.

### Pitfall 8 — Using `timeout` in a plan command
`timeout(1)` is not installed on this machine (`command not found: timeout`, zsh). Verified this session.

### Pitfall 9 — Assuming self-checks are green
Three of six fail at `HEAD` for pre-existing reasons. See Finding 5c. A `<verify>` that runs all six will always fail.

---

## Code Examples

### Gating an existing hand-authored action behind a menu flag (Finding 1c)

Pattern already proven in-artifact by `Manual Status Requested` (menu case `:1425`; gate at plist action 3648). New menu case, in `manual_emergency_restore()`:

```python
# Replace the existing no-op at :1426
a += [menu(group, 1, title="Open Control Room"), *number(1, "Manual Show Note Requested")]
```

New idempotent pass, modelled on `fix_notes_filter_limit()` (`:2688`), called from `main()` **after** `fix_shownote_key()`:

```python
def gate_control_room_shownote(actions):
    """Show the Control Room Note only when the user asked for it.

    Action <shownote> sits at depth 0 in the MANUAL arm, so every manual run --
    Status, Toggle Voice, Reset Today, Test a Circle -- ends by launching Notes.
    Only the 'Open Control Room' menu item asks for that, and its branch is a
    bare Nothing that relies on this unconditional tail.
    Idempotent: returns once the shownote is already preceded by its gate.
    """
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.shownote":
            continue
        prior = actions[index - 1].get("WFWorkflowActionParameters", {}) if index else {}
        if prior.get("WFControlFlowMode") == 0 and prior.get("WFCondition") == 2:
            return  # already gated
        group, gate = if_block("Manual Show Note Requested", 2, number=0)
        actions[index:index + 1] = [gate, item, otherwise(group),
                                    action("is.workflow.actions.nothing"), end_if(group)]
        return
```

Notes: `if_block()` produces the correct `WFInput.Variable` attachment envelope (rule 5); `normalise_numeric_operands()` leaves the operand alone because `number()`'s output is already Number-typed; `main()`'s auto-comment pass will insert a control-flow comment before the gate unless one is authored.

### Reading a flat epoch key with a safe numeric gate (Finding 3, Design A)

Existing precedent — `restore_managed_settings()` (`:463`, `:470`):

```python
a += read_value("last_open_at", variable("State"), "Setup Last Open")
seen_g, seen_if = if_block("Setup Last Open", 2, number=0)   # numeric "> 0"
a += [seen_if, *number(1, "Automation A Seen"),
      otherwise(seen_g), *number(0, "Automation A Seen"), end_if(seen_g)]
```

Both operands are safe under every measured coercion: `"null" → Number → > 0 → FALSE, no error` (Donor 6.1 test 2) and `"" → Number → > 0 → FALSE` (Donor 6 action 8). The key is **flat**, so the read cannot hard-error even if absent from a legacy `state.json` (C4).
`[CITED: build_state_engine.py:443–444, quoting device donor measurements]`

### Reporting via the read-only alert path (Finding 3)

Precedent — the cycle-14 `Status` branch in `manual_note_refresh()` (`:1472–1475`). Reuse `alert()` with a `text_token([...])` message; **never** `appendnote` (Status/Setup Check must not write the Note).

---

## Runtime State Inventory

This phase is a refactor/subtraction pass, so this section is mandatory.

| Category | Items found | Action required |
|---|---|---|
| **Stored data** | `state.json` at `PROSOCHE/state.json` in Shortcuts' iCloud folder. After the cut, `settings_snapshot.{brightness,volume}.{original_value,changed_at,changed_by_session_id}` (6 leaves) become dead keys on any device that already has a file | **None.** Dead keys are inert; no reader remains; a flat read of an unused key is never performed. **Code edit only, no data migration.** Do **not** bump `schema_version` to force a rebuild — it would destroy `heat`, `opens_today`, `exit_stats`, `recent_sessions`, and the synced proforma |
| **Live service config** | The two **Personal Automations** (App Is Opened / Is Closed) live in the Shortcuts app on the user's iPhone, not in git. They reference the shortcut **by display name** `PROSOCHĒ — Nine Circles — Dumb` and pass the literal text `OPEN` / `CLOSE` | **None this phase** — the display name is unchanged (Build Addendum 01's rename is a *different*, deferred todo). But the router-fall-through diagnosis (Finding 1a) requires *inspecting* Automation B's Run Shortcut input on device |
| **OS-registered state** | The imported `.shortcut` in the user's Shortcuts library. A re-import replaces it by name; a `_signed`-suffixed name would create a duplicate | **None** provided `sign-shortcut --name "PROSOCHĒ — Nine Circles — Dumb"` is used exactly. Any device still running `2026-08-15o` will need a re-import to see these changes |
| **Secrets / env vars** | **None — verified.** No `.env`, no SOPS, no CI secrets; the project has no network surface at all (privacy constraint: nothing leaves the device) | None |
| **Build artifacts / installed packages** | `src/PROSOCHE-Dumb.xml` (regenerated in place), `src/PROSOCHE-Sentient.xml` (stale at `2026-08-14k`), both canonical `.shortcut` files, 32 dated archive XMLs, `MANIFEST.md` rows. No `__pycache__` is tracked (`.gitignore` covers it) | **Rebuild + re-sign Dumb; refresh MANIFEST.** Sentient: decide explicitly whether to re-fork (it is SEED-005 / a separate todo) or leave stale and document it — but **`build_sentient.py` must still import cleanly** after the cut (Finding 2e) |

---

## Environment Availability

| Dependency | Required by | Available | Version / result | Fallback |
|---|---|---|---|---|
| `python3` | Both builders, all self-checks, validator | ✓ | 3.10+ (PEP 604 works) | — |
| `validate-shortcut` | Validation gate | ✓ | plugin v1.2.1, on `PATH` | — |
| `sign-shortcut` | Archive + sign | ✓ | plugin v1.2.1, on `PATH` | — |
| `/usr/bin/shortcuts` | Real signer behind the wrapper | ✓ | macOS built-in | — |
| `openssl`, `plutil`, `shasum`, `stat` | AEA1 decrypt-verify + MANIFEST | ✓ | macOS built-in | — |
| `aea`, `aa` | AEA1 decrypt-verify | assumed ✓ | used successfully in prior cycles | If absent: structural verification limited to `src/` |
| `git` | Provenance guard | ✓ | guard **PASSES** at `HEAD` | — |
| `timeout(1)` | — | ✗ | `command not found` | Do not use it in plan commands |
| **Target iPhone (iOS 26)** | Behavioural UAT | **✗** | `xcrun devicectl list devices` → `No devices found.` | **Wave-3 deferred UAT block** — see Finding 6b |

**Missing dependencies with no fallback:** the target iPhone. Four acceptance criteria genuinely require it (note-picker behaviour, no-menu-on-CLOSE, OPEN-path regression, `Leaving / Continue` comprehension).
**Missing dependencies with fallback:** `timeout` (omit); `aea`/`aa` (fall back to `src/`-level assertions if unavailable).

---

## Validation Architecture

`workflow.nyquist_validation` is `true` in `.planning/config.json`, so this section applies.

### Test framework

| Property | Value |
|---|---|
| Framework | **None (no pytest/unittest).** Verification is a set of standalone assert-based Python scripts in `docs/` plus the generator's own 15 in-process `verify_*` passes |
| Config file | none — see Wave 0 |
| Quick run command | `python3 docs/state_engine_self_check.py && python3 docs/phase7_self_check.py` (~1 s) |
| Full suite command | `python3 tools/build_state_engine.py && python3 docs/state_engine_self_check.py && python3 docs/phase7_self_check.py && python3 docs/sentient_audit_check.py && validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` |

### Phase requirements → test map

| Item | Behaviour | Test type | Automated command | File exists? |
|---|---|---|---|---|
| Strand A / `.gitignore` | Ignores build noise | smoke | `grep -qE '__pycache__|\.DS_Store|\*\.pyc' .gitignore` | ✅ (already satisfied) |
| Strand A / MANIFEST | Rows match artifacts | unit | new `docs/manifest_check.py` — parse table, recompute `shasum`/`stat`, assert equality | ❌ **Wave 0** |
| Strand A / cut complete | Zero brightness/volume/device-detail actions | unit | new `docs/cut_check.py` — assert counts of `setbrightness`, `setvolume`, `getdevicedetails` are all `0`; assert `settings_snapshot` absent from every literal `WFDictionaryKey` | ❌ **Wave 0** |
| Strand A / no dangling refs | Both builders still run | smoke | `python3 tools/build_state_engine.py && python3 -c "import sys;sys.path.insert(0,'tools');import build_sentient"` | ✅ |
| Strand A / Config integrity | Every `sequences.*` entry names a live primitive | unit | new `docs/sequence_dispatch_check.py` — cross-check Config JSON at action 7 against the dispatch tuple | ❌ **Wave 0** (**and it does not exist today for any reason** — this is the Finding-2c guard) |
| Strand B / `shownote` gated | `shownote` is preceded by a mode-0 conditional on `Manual Show Note Requested` | unit | extend `docs/phase7_self_check.py` | ✅ (extend) |
| Strand B / `Setup Check` present | Menu items list contains `Setup Check`; a `getvalueforkey` for `last_open_at` and `last_close_at` exists in the MANUAL arm | unit | extend `docs/phase7_self_check.py` | ✅ (extend) |
| Strand B / no menus in CLOSE | CLOSE arm contains zero `choosefrommenu` | unit | new `docs/router_ui_census.py` — assert per-arm UI-action counts | ❌ **Wave 0** (high value: it is the regression guard for the whole of Strand B) |
| Both / plist validity | Structural correctness | smoke | `validate-shortcut … --target-platform all` | ✅ |
| Both / what shipped | Signed artifact matches the built source | integration | AEA1 decrypt → re-run the unit assertions against `Shortcut.xml` | ✅ (recipe) |
| Behavioural | Device UAT | manual-only | — | **Deferred (DIST-03)** |

### Sampling rate

- **Per task commit:** `python3 tools/build_state_engine.py && python3 docs/state_engine_self_check.py && python3 docs/phase7_self_check.py`
- **Per wave merge:** full suite above + the new Wave-0 check scripts + `validate-shortcut`
- **Phase gate:** full suite green + signed artifact decrypt-verified, **before** `/gsd-verify-work`; Wave-3 device UAT explicitly outstanding

### Wave 0 gaps

- [ ] `docs/router_ui_census.py` — per-arm census of `choosefrommenu`/`ask`/`alert`/`shownote`/`filter.notes`; the regression guard for Strand B
- [ ] `docs/cut_check.py` — asserts the brightness/volume cut is complete and no `settings_snapshot` key is read
- [ ] `docs/sequence_dispatch_check.py` — Config `sequences.*` × `primitive_dispatch()` cross-check (Finding 2c)
- [ ] `docs/manifest_check.py` — MANIFEST rows vs real sizes/hashes
- [ ] Repair `docs/phase5_self_check.py` (obsolete condition-100 `Input Key` lookup, dead since DEV-02) and `docs/phase6_self_check.py` (`WFAppName` assertion contradicted by `normalize_open_apps()`) — both currently **red** and masking real regressions

*(No framework install is needed — these are plain `python3` scripts matching the five that already exist.)*

---

## Security Domain

`workflow.security_enforcement` is `true`, ASVS level 1.

### Applicable ASVS categories

| ASVS category | Applies | Standard control |
|---|---|---|
| V2 Authentication | **no** | No accounts, no auth surface |
| V3 Session management | **no** (in the ASVS sense) | `active_session` is a local behavioural record, not a security session; ownership is a race guard, not an authz check |
| V4 Access control | **no** | Single-user, on-device, no privilege boundary |
| V5 Input validation | **yes** | Import answers are normalised via an If-chain to a closed set (`Paradise`/`Inferno`/else `Limbo`, `:55–65`; `yes`/else `false`, `:69–73`). The `Create` exit accepts a **user-supplied URL** (`ask` type `URL`, actions 770/931) persisted to `profile_snapshot.create_target_url` and later opened via `openurl` — this is the one genuine untrusted-input path, and **this phase does not change it** |
| V6 Cryptography | **no** (in-app) | The only crypto is Apple's AEA1 signing, handled entirely by `shortcuts sign` |
| V7 Error handling / logging | **partial** | The Control Room Note is an append-only local ledger; it records behavioural facts, never credentials. `manual_note_refresh()` (`:1465`) writes fork/profile/sequence/voice/circle/pressure/cooldown/exits — no secrets |
| V12 File handling | **yes** | Fixed path `PROSOCHE/state.json`, `WFAskWhereToSave=False`, `WFSaveFileOverwrite=True`; no user-supplied path anywhere |
| V13 API / SSRF | **no** | **No network surface at all.** No `HTTP`/`downloadurl` action exists in either fork — verified: the artifact contains zero networking identifiers |

### Known threat patterns for this stack

| Pattern | STRIDE | Standard mitigation | Status in this phase |
|---|---|---|---|
| Unsafe environmental change with no restore path (black screen, startling audio) | Denial of Service (self-inflicted) | Never write a setting whose original cannot be captured and restored; numeric-gate every write (`verify_restore_gates()`) | **This phase REMOVES the entire mechanism.** Strictly risk-reducing. But it also removes the guard — record the trade in the deviation log |
| Accessibility stranding (a user locked out by a setting PROSOCHĒ changed) | DoS | Emergency Restore always reachable, including during Ice | **SAFE-05 is weakened** by the cut: Emergency Restore keeps clearing cooldown and the active session, but no longer restores anything environmental. After the cut there is nothing environmental to restore, so the *property* holds while the *requirement text* does not. **Amend the requirement; do not silently leave it checked** |
| Open redirect via the persisted `Create` URL | Tampering | The URL is user-authored, local-only, never shared | Unchanged this phase |
| Data exfiltration | Information disclosure | No network actions exist; the Note and `state.json` are local | Unchanged; `Setup Check` must report **local** facts only, never anything new |
| Silent state corruption via a dotted read of a missing key | DoS | Container/leaf split + bootstrap seeding + `verify_sentinel_gates()` | `Setup Check` **must use flat reads only** (Design A does) |

**Security verdict for this phase: net risk-reducing.** The only security-relevant deliverable is the **SAFE-05 requirement amendment**, which must not be skipped.

---

## State of the Art

| Old approach (in this repo) | Current approach | When changed | Impact on this phase |
|---|---|---|---|
| Router gated MANUAL on "Input Key has any value" | Positive identification: `OPEN` / `CLOSE` / else MANUAL, guarded by `verify_router_shape()` | cycle 3, DEV-02 | A mis-typed automation now lands in the MANUAL menu — **this is the "menu on CLOSE" report** |
| `shownote` carried a `target` key | `WFInput`, Donor-8-matched, `fix_shownote_key()` | cycle 14 | Applied; the remaining defect is that `shownote` is *ungated*, not mis-keyed |
| `filter.notes` had no result bound | `AppIntentDescriptor` + `WFContentItemLimitEnabled` + `WFContentItemLimitNumber=1` | cycle 16 | **Applied.** Only device confirmation is outstanding |
| `pending_exit` absent from bootstrap | Permanent `{type, timestamp}` container + leaf writes + condition-5 gates | cycle 16 | The pattern to copy if any new state key is added |
| `read_value()` used for compound arrays | `get_value()` for `COMPOUND_STATE_KEYS`, guarded | cycle 15 | Relevant if `Setup Check` ever reads a list (it should not) |
| `BUILD_STAMP` / `ROUTER_TRACE` / `OPEN_BISECT` breadcrumbs | Stripped; replaced by two permanent `notification()` confirmations (OPEN and CLOSE) | 2026-08-16, `2e85aa3` | Strand A item 1 is **DONE**; its on-device regression check is still outstanding |
| `--target-platform ios` per CLAUDE.md | `--target-platform all` per DEV-01 | cycle 3, re-measured today | **Use `all`** |

**Deprecated / stale in-repo:**
- `docs/phase5_self_check.py` — asserts a router shape deleted by DEV-02.
- `docs/phase6_self_check.py` — asserts an `openapp` shape contradicted by `normalize_open_apps()`.
- `src/PROSOCHE-Sentient.xml` — built at `2026-08-14k`; missing cycles 14–16 and both notifications. Re-fork is SEED-005 / a separate todo.
- `RESTORE_MARKER` (`:21`) — becomes unused after the cut.
- Config `safety.dim_target` / `safety.brightness_floor` / `safety.allow_volume_increase` — become dead after the cut. `safety.ash_managed_color_filters` is *already* dead (Ash is the validator-clean message-only fallback).

---

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|---|---|---|
| A1 | A genuine JSON `null` read via `getvalueforkey` behaves like an absent value for a numeric `> 0` gate | Finding 3 | **Low.** The recommended numeric gate is safe under *both* readings (present-null and absent both yield `> 0 == false`). Only an existence gate would be at risk — which is why it is not recommended |
| A2 | The user's "menu on CLOSE" is router fall-through from a non-`CLOSE` `Input Key` | Finding 1a | **Medium.** If the real cause is (b) or (c), the copy fix is cosmetic and the real defect persists. **Requires device evidence to settle** |
| A3 | `aea` / `aa` are present on this machine | §5b, Environment | Low — used successfully in prior cycles; if absent, decrypt-verify degrades to `src/`-level assertions |
| A4 | Removing `settings_snapshot` readers leaves on-device `state.json` files safe without migration | Finding 2d | Low — nothing enumerates the dictionary; only literal-key reads occur, all of which are being removed |
| A5 | `device_detail()` has no caller outside `dim()`/`silence()` | Finding 2b | Low — grep shows two call sites (`:543`, `:565`), and the built artifact's 20 `getdevicedetails` actions equal 2 × 10 dispatch renderings exactly. **Planner should still re-grep before deleting** |
| A6 | Non-stateful `dimming()`/`silence()` replacements keep AUDIT-03/04 and CIRC-03/05 green | Finding 2c, Phase Requirements | Medium — this is an interpretation of requirement text ("degrades to a non-stateful variant"), not a measured fact. **Worth user confirmation before it becomes a locked decision** |
| A7 | The 18 vs 28 discrepancy is a stale count, not two different measurement targets | Finding 2a | Low — 28 is derived and reconciled exactly (8 restore + 20 primitive). The 18 is CITED from a cycle-14 comment about *uncoerced operand* sites at that time |

---

## Open Questions

1. **Should `Leaving / Continue` be Circle-gated, or only reworded?**
   - Known: it fires on every genuine OPEN at every Circle; canonical strategy §6.4 says easy dismissal is the strongest mechanism, so deleting it is a regression.
   - Unclear: whether the user's complaint is "I don't understand it" (copy) or "it's too often" (frequency).
   - Recommendation: **reword this round** (in scope); flag frequency/Circle-gating as a design question for the user. The nine-Circle interaction-cost pass is explicitly deferred.

2. **Non-stateful replacements vs. Config sequence rewrite for `Silence`/`Dimming`?**
   - Known: doing neither leaves four Circles as silent no-ops (Finding 2c).
   - Recommendation: non-stateful replacements (Option A) — fewer requirement casualties, no Config edit.
   - This is a **decision the plan must record explicitly**, not infer.

3. **Is Sentient in scope?**
   - Known: `build_sentient.py` **must** be edited for the cut (import break), but *rebuilding* Sentient is SEED-005 / `2026-08-15-fork-sentient-post-openpath-fix.md`.
   - Recommendation: edit `build_sentient.py` (mandatory), do **not** rebuild Sentient (out of scope), and correct the MANIFEST Sentient rows to describe what actually exists today rather than deleting them.

4. **Duplicate OPEN surfaces (notification 515 + Knock alert 1002)?**
   - Known: identical phrasing, both on the OPEN path, at Circle 1 both fire.
   - Unclear: the notification was added deliberately (`G-04-4b`) as a permanent confirmation after the breadcrumbs were stripped.
   - Recommendation: in scope as spurious-UI ("no prompt whose purpose is not evident"). Suggested resolution: keep the notification (non-blocking, permanent), and change `knock()`'s alert copy so it is not a verbatim duplicate — or gate the notification off at Circle 1 specifically. **Confirm with the user.**

5. **Should the two currently-red stale self-checks be repaired here?**
   - Recommendation: yes — they are one-line fixes and their redness prevents the suite from being a usable gate for the rest of this phase.

---

## Sources

### Primary (HIGH confidence — measured in this session)
- `tools/build_state_engine.py` (2,883 lines) — read in full; all line numbers cited are from `HEAD` (`2e85aa3`)
- `src/PROSOCHE-Dumb.xml` — parsed with `plistlib`; 3,676 actions; all indices, counts, arm boundaries, prompts, and parameter shapes measured directly
- `src/PROSOCHE-Sentient.xml` — parsed; 3,752 actions; 0 `notification` actions (staleness evidence)
- `tools/build_sentient.py` — read; import coupling confirmed
- `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform {all,ios}` — **both run this session**; `all` passes, `ios` rejects wholesale
- `python3 docs/{state_engine,phase5,phase6,phase7}_self_check.py`, `docs/sentient_{core,audit}_check.py` — **all six run this session**; 3 PASS / 3 FAIL
- `git merge-base --is-ancestor 7ca8ebb… HEAD` — **PASS**
- `xcrun devicectl list devices` — **`No devices found.`**
- `shasum -a 256` / `stat -f%z` on all six MANIFEST-referenced artifacts

### Secondary (HIGH–MEDIUM — project records)
- `.claude/CLAUDE.md` — capability audit, seven parameter-defect axes, verified runtime semantics, evidence hierarchy, AEA1 recipe
- `docs/BUILD-NOTES.md` §3 (validator/signer invocations), §13 (DEV-01, DEV-02, DEV-C3-03)
- `.planning/debug/HANDOFF.md` — canonical sign invocation, cycle-16 findings, Sentient staleness
- `.planning/debug/resolved/open-routing-sequence-error.md` — Finding 2 (`filter.notes`) locally verified, not device-confirmed
- `.planning/REQUIREMENTS.md` — AUDIT-03/04, SESS-07, CIRC-03/05, ROOM-10, SAFE-01/02/05/06
- `.planning/todos/pending/2026-08-15-ship-readiness-cleanup.md`, `.planning/todos/pending/2026-08-16-optimise-ux-onboarding-and-functionality.md` (incl. the 2026-08-16 scope split)
- `.planning/ROADMAP.md` Phase 10; `.planning/STATE.md`; `.planning/config.json`
- `.planning/quick/260816-ukb-…/{PLAN,SUMMARY}.md` — the deferred-UAT precedent to copy

### Tertiary (LOW — not used for any load-bearing claim)
- None. No web search was required or performed; every claim in this document is grounded in the repository or in a command run against it.

---

## Metadata

**Confidence breakdown:**

| Area | Level | Reason |
|---|---|---|
| Spurious-UI site inventory (Finding 1) | **HIGH** | Every index, prompt, and arm boundary measured by parsing the committed plist |
| Brightness/volume cut surface (Finding 2) | **HIGH** | Removal surface grepped; the 28 count derived and reconciled exactly (8 + 20) |
| Config-sequence trap (Finding 2c) | **HIGH** | Config JSON parsed; `primitive_dispatch()`'s condition-99 matching read directly |
| `Setup Check` feasibility (Finding 3) | **MEDIUM–HIGH** | Write sites and seed values verified; the recommended numeric gate is safe under both readings of JSON `null` (A1) |
| Onboarding trace (Finding 4) | **HIGH** | Traced action-by-action through the pre-router block and MANUAL arm |
| Build/validate/sign loop (Finding 5) | **HIGH** | Validator run both ways, self-checks run, provenance guard run, hashes recomputed |
| Device-blocker triage (Finding 6) | **HIGH** for what needs a device; **MEDIUM** for the router fall-through diagnosis (A2) |
| Regression risk (Finding 7) | **MEDIUM** | Structural risks enumerated from the code; interaction risk is a judgement |
| Requirement impact | **HIGH** | Requirement texts read verbatim; SAFE-05's conflict is textual, not inferred |

**Research date:** 2026-08-16
**Valid until:** 2026-08-23 — or immediately invalidated by any run of `tools/build_state_engine.py`, since every action index in this document is measured against `src/PROSOCHE-Dumb.xml` at `2e85aa3`. **Re-measure indices after the first rebuild; function/line references in `build_state_engine.py` remain stable.**
