# Architecture Research: PROSOCHĒ — Nine Circles

> **v1-ERA RESEARCH (2026-08-13) — read with the re-foundation in mind.** The project was
> re-founded 2026-08-19 on canonical strategy **v2.0** (the covenant model; decisions
> BD-09..BD-12 in `docs/CAPABILITY-DECISIONS.md`): contract coverage above the Circle ladder,
> four fixed bands, verdicts in both forks, the BD-09 slot table. `§N` citations below refer
> to canon **v1** (preserved at git tag `pre-covenant-overhaul`) and resolve via canon v2
> Appendix A. Toolchain, plist, and capability findings here remain valid; claims about the
> interaction model (combined sequence entries, Confession as a Circle-4 rung with no routing
> consequence, the `Limbo` profile name — now `Purgatory` — and the universal Leaving menu)
> are historical.


**Domain:** Single large stateful iOS 26 Shortcut — three invocation modes, persistent JSON state, escalating intervention state machine
**Researched:** 2026-08-13
**Confidence:** MEDIUM-HIGH (control-flow and variable-wiring claims are grounded in the Shortcuts Playground plugin docs on disk and are HIGH confidence; a handful of specific action capabilities — brightness/volume *read*, `Use Model` on-device selection, list-sort/median, remove-item — are not evidenced in the bundled docs and are flagged explicitly below as build-time capability-audit items, per the canonical strategy's own §31 instruction not to fabricate actions)

There is no runtime framework here in the conventional sense — "architecture" means the action-graph shape, the JSON state schema, and the routing/dispatch structure inside one (or two, per fork) `.shortcut` files. Everything below is written to be handed directly to a phase planner and to a Shortcuts-Playground build agent.

---

## 0. Grounding notes (what the toolchain can actually do)

Read from `~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/{CONTROL_FLOW,DATE_TIME,BEST_PRACTICES,VARIABLES,ACTIONS,APPINTENTS,AUTOMATION_TRIGGERS}.md`. The facts below directly shape every recommendation in this document:

| Fact | Source | Architectural consequence |
|---|---|---|
| `WFControlFlowMode`: 0=start, 1=middle, 2=end; nesting confirmed to depth 7 in production shortcuts | CONTROL_FLOW.md | A single flat monolithic action graph with deep If/Repeat/Menu nesting is a *proven* pattern, not a risk. |
| **"Otherwise If" is a macOS 27+ serialization.** Target is iOS 26.x. | CONTROL_FLOW.md §"Otherwise If (macOS 27+)"; PROJECT.md constraint "Platform: iOS 26.x" | **Do not use Otherwise-If chains for the OPEN/CLOSE/MANUAL router or the Circle-sequence lookups.** Use nested single-condition `If`/`Otherwise` blocks instead. This is a concrete, non-obvious finding — flag it to the build agent. |
| `WFCondition` codes are integers; 4=equals, 99=contains, 100/101=existence; every code needs explicit `WFInput` (no implicit input) | CONTROL_FLOW.md, BEST_PRACTICES.md | Routing compares (Q1) and primitive-membership checks (Q8, using `contains`) are both directly buildable with documented codes. |
| Multi-condition If (`WFConditions`/`WFContentPredicateTableTemplate`, Any/All) exists as a *separate* serialization from single-condition If — the two must never be mixed on one action | CONTROL_FLOW.md | Useful for the cooldown short-circuit (`cooldown_until has value` AND `now < cooldown_until`) as one block instead of nested Ifs. |
| No native epoch/UNIX format token in Format Date. Apple's documented pattern is Date(1970-01-01 UTC) → Adjust Date. `CurrentDate` magic token must never be fed directly into `Get Time Between Dates` — materialize it via a `Date` action first. | DATE_TIME.md | Directly drives the timestamp-representation decision in §2 below (epoch-seconds integers, computed once per run). |
| `is.workflow.actions.getcurrentapp` (Get Current App) exists as a first-party action | ACTIONS.md L227 | Usable for genuine-reopen detection (Q4), with the reliability-at-trigger-time caveat still flagged for capability audit. |
| `is.workflow.actions.file.createfolder`, `file.getfoldercontents` exist | ACTIONS.md | Bootstrap can explicitly create its own folder and check existence via folder listing rather than risking a hard error on `Get File` against a missing path (Q3). |
| `is.workflow.actions.number.random` exists; `is.workflow.actions.hash` exists; **no `Generate UUID` action is documented anywhere in ACTIONS.md/APPINTENTS.md** | ACTIONS.md | Session IDs must be synthesized from `{epoch}-{random}` (or hashed), not from a native UUID generator (Q5). |
| **No `Get Brightness` / `Get Volume` read action is documented anywhere in the 300+ identifier catalog.** Only `setbrightness` / `setvolume` (write) exist. `getdevicedetails` is a plausible but *unverified* read path. | ACTIONS.md L227, full identifier dump | This is the single most consequential finding for Q9/environmental safety. It directly supports — with concrete grounding, not speculation — the canonical strategy's own §21 fallback rule ("if original value cannot be read, do not make the intervention"). Architecture must treat brightness/volume restoration as **conditionally available**, not guaranteed. |
| **No `Sort List`, `Remove Item from List`, or `Median` action is documented.** `statistics` exists as a bare identifier with no parameter detail in these docs. | ACTIONS.md | Rolling-window array trimming must use a rebuild-via-`Repeat`+`Get Item from List` pattern, not a trim/remove primitive. Median computation for exit-learning must be flagged for capability audit (`statistics` action) with a mean-based fallback. |
| `askllm` (Use Model) documented parameters are only `WFAllowWebSearch` and `FollowUp`. **No model-source (On-Device / Private Cloud Compute / ChatGPT) parameter is documented in these files.** | ACTIONS.md L126 | This is the **#1 Sentient-build capability-audit item**: the build agent must inspect the live `Use Model` action configuration UI on-device to find and record the actual on-device-selection parameter/key before writing any Sentient XML. Do not assume a default. |
| `text.trimwhitespace`, `text.changecase` exist | ACTIONS.md | Input normalization (Q1) is a two-action, fully-documented operation. |
| `runworkflow` (Run Shortcut) exists and can call the shortcut itself or another shortcut by name | ACTIONS.md | Available if ever needed, but see Q1 — recommendation is to avoid it for internal routing. |
| Notes: `appendnote`, `filter.notes`, `shownote`, `com.apple.mobilenotes.SharingExtension` (Create Note), `com.apple.Notes.CreateNoteFromMarkdownLinkAction` all exist and are documented with parameter shapes | ACTIONS.md, APPINTENTS.md | Control Room Note lifecycle (create/find/append) is fully buildable with first-party actions. |
| `lockscreen` exists as a first-party action | ACTIONS.md | Confirms Circle IX's "native Lock Screen if available" language in §11 has a real candidate action to verify. |

---

## 1. Invocation routing

### Recommendation: monolith, not dispatcher + helper shortcuts

**Ship one signed `.shortcut` per fork** (this is also a hard PROJECT.md requirement: "Two signed, importable `.shortcut` files," not four or six). A dispatcher+helpers architecture would mean:

- Every helper is a **separate installed Shortcut** the user must import individually — this directly fights the "self-saucing," one-tap-import onboarding goal in §0/§18 of the canonical strategy, and multiplies install-failure surface (duplicate-name silent-skip behavior is a documented Shortcuts Playground gotcha — see BEST_PRACTICES.md "Signing & Install Naming").
- Every `Run Shortcut` (`runworkflow`) hop is a real, measurable process-launch — commonly cited in the hundreds of milliseconds — plus a dictionary-serialization boundary where type fidelity has historically been lossy in Shortcuts. This directly fights the OPEN-pipeline latency budget (Q4: the intervention must feel closer to instant than to a network request) for zero isolation benefit — nothing here needs sandboxing, a background daemon, or independent versioning.
- A helper-shortcut split does not reduce actual complexity; it just moves it behind an invisible boundary that is *harder* to debug (you cannot single-step across a `Run Shortcut` call the way you can scroll through one file).

**One exception exists but is not a helper-shortcut architecture choice**: the OPEN and CLOSE **Personal Automations** must call the shortcut by name via `Run Shortcut` — that one hop (automation → shortcut) is mandatory and unavoidable per §5.1/§5.2 of the canonical strategy; it is the *trigger mechanism*, not an internal helper call. Internally, from the moment the shortcut starts executing, there should be **zero further `Run Shortcut` hops**.

**Tradeoff, stated honestly:** this produces one large action graph — plausibly 300–600+ actions once nine primitives × three sequences × six exits × contracts × Control Room menu × (for Sentient) eight model hooks are all inlined. There is no documented hard action-count ceiling (§5.3 of the canonical strategy), so this is an authoring-ergonomics cost, not a correctness risk. Mitigate it with the same discipline Shortcuts Playground already mandates: rigorous `Comment` section headers at every logical boundary (BEST_PRACTICES.md requires this for any shortcut over ~20 actions), consistent variable-naming conventions per Circle/primitive, and treating OPEN/CLOSE/MANUAL as three mentally-separate "sub-programs" that happen to live in one physical file — a "dispatcher + helpers" *mental model*, flattened into a "monolith" *implementation* to avoid the install/latency cost of literal separate files.

### Concrete routing structure

```
[Shortcut starts — receives ExtensionInput from automation, or nothing from a manual tap]
  │
  ├─ Comment: "--- ROUTING: normalize and classify Shortcut Input ---"
  ├─ Set Variable "Raw Input" = Shortcut Input (ExtensionInput token; NOT the
  │    `is.workflow.actions.input` action — BEST_PRACTICES.md explicitly says
  │    never emit that action; reference input via the ExtensionInput attachment)
  ├─ Text: Trim Whitespace(Raw Input) → Change Case: Uppercase → Set Variable "Input Key"
  │
  ├─ If "Input Key" — Has Any Value (code 100)
  │    │
  │    ├─ [TRUE branch] nested If "Input Key" is "OPEN" (code 4)
  │    │     ├─ [TRUE] → OPEN BRANCH
  │    │     └─ Otherwise → nested If "Input Key" is "CLOSE" (code 4)
  │    │            ├─ [TRUE] → CLOSE BRANCH
  │    │            └─ Otherwise → FAIL-SAFE BRANCH (unrecognised, non-empty)
  │    │
  │    └─ [FALSE branch, code 101 semantics via Otherwise] → MANUAL BRANCH
  └─ End
```

Nested single-condition `If`/`Otherwise` blocks are used throughout, **not** the macOS-27-only Otherwise-If pattern (see §0 grounding table). Each nesting level gets its own `GroupingIdentifier`.

**Empty input → MANUAL branch.** A bare manual tap passes no `ExtensionInput` value, and — critically — the very first-ever run (fresh import, before either Personal Automation exists) is also empty input by construction. The MANUAL branch therefore *must* contain the bootstrap check (Q3) as its first action, before presenting the Control Room menu.

**Unrecognised non-empty input → fail-safe, not OPEN.** If the automations are ever mis-typed, edited, or a stray caller passes garbage, the shortcut must never silently treat it as a real tracked-app open (that would corrupt Heat/Pressure with a phantom event) and must never crash. The fail-safe branch performs **zero state mutation** — no load-mutate-persist at all — shows a single diagnostic (`Show Alert`: "PROSOCHĒ received unexpected input and took no action.") and exits. This is a deliberate, named design decision, not an oversight: unrecognised input is inert by construction.

**Normalization is deliberately minimal**: uppercase + trim, then exact string match. Because the OPEN/CLOSE strings are entirely under our control (we author the exact text the user is instructed to type into their own Personal Automations, per the Control Room Note setup instructions), heavier normalization (fuzzy matching, synonyms) would be solving a problem that doesn't exist and would only widen the fail-safe/OPEN boundary in a way that's harder to reason about.

---

## 2. State schema

### Timestamp format — decided first, because it constrains everything else

**All timestamps are stored as integer Unix epoch seconds (UTC).** Rationale, grounded directly in DATE_TIME.md: Shortcuts' `Format Date` has no epoch pattern token, and reconstructing a `Date` object from a stored ISO-8601 string on every single OPEN (for Heat-decay and rapid-return arithmetic) would require an extra detect/parse step on the hot path, with locale/timezone risk baked in. An integer epoch avoids all of that: Heat decay, rapid-return windows, cooldown checks, and session-duration are all plain `Math` subtraction/comparison on two integers — no date reconstruction needed at read time.

Construction pattern (once per run, cached in a variable, reused everywhere):
1. A literal `Date` action set to a fixed specified date `1970-01-01 00:00:00` (the anchor — built once, effectively a constant).
2. A `Date` action set to **Current Date**, materializing the current instant into an actual Date value (DATE_TIME.md is explicit that the `CurrentDate` magic token must never be fed directly into `Get Time Between Dates` — it must go through a `Date` action first).
3. `Get Time Between Dates` (from: anchor, to: current, unit: Seconds) → integer, stored as `Now Epoch`.

`behavioural_day` is the one exception: it is a **string** date key (`yyyy-MM-dd`, via `Format Date → Custom`), computed from `Now Epoch − 4h`, because it is used for string-equality rollover comparison and Note-dating, not arithmetic — ISO-8601 date strings sort and compare correctly as strings (per DATE_TIME.md's own guidance).

### Complete schema (schema_version 1)

```json
{
  "schema_version": 1,
  "fork": "Dumb",
  "profile": "Limbo",
  "sequence": "Classic",
  "voice_enabled": true,
  "ai_enabled": false,

  "behavioural_day": "2026-08-13",
  "opens_today": 0,
  "heat": 0,
  "gravity": 0,
  "pressure": 0,
  "circle": 1,

  "last_open_at": null,
  "last_close_at": null,
  "last_app": null,

  "active_session": null,

  "recent_sessions": [],
  "recent_contracts": [],
  "exit_stats": {
    "Capture":    { "count": 0, "sum_return_seconds": 0, "samples": [] },
    "Coordinate": { "count": 0, "sum_return_seconds": 0, "samples": [] },
    "Create":     { "count": 0, "sum_return_seconds": 0, "samples": [] },
    "Connect":    { "count": 0, "sum_return_seconds": 0, "samples": [] },
    "Consult":    { "count": 0, "sum_return_seconds": 0, "samples": [] },
    "Close":      { "count": 0, "sum_return_seconds": 0, "samples": [] }
  },

  "cooldown_until": null,
  "settings_snapshot": {},
  "profile_snapshot": {
    "goal": "",
    "phone_purpose": "",
    "reclaim_for": "",
    "deliberate_leisure_definition": "",
    "enabled_exits": ["Capture", "Coordinate", "Create", "Connect", "Consult", "Close"],
    "synced_at": null,
    "note_content_hash": null
  },
  "last_model_message": null
}
```

`active_session`, when non-null:

```json
{
  "id": "1786598421-4821",
  "start_at": 1786598421,
  "app": "Instagram",
  "intention": null,
  "duration_declared_minutes": null,
  "is_custom_duration": false,
  "circle_at_open": 4,
  "heat_at_open": 6,
  "pressure_at_open": 6,
  "exit_used": null
}
```

`recent_sessions[]` entry (append-only, newest first, cap 20):

```json
{
  "session_id": "1786598421-4821",
  "app": "Instagram",
  "opened_at": 1786598421,
  "closed_at": 1786598685,
  "duration_seconds": 264,
  "circle_at_open": 4,
  "heat_at_open": 6,
  "pressure_at_open": 6,
  "contract_declared": true,
  "intention": "reply to Maya",
  "duration_declared_minutes": 5,
  "overrun_seconds": 24,
  "contract_respected": true,
  "exit_used": "Coordinate",
  "outcome_recorded": false
}
```

`recent_contracts[]` entry (append-only, newest first, cap 10 — written at CLOSE, mirroring `recent_sessions`, never mutated in place):

```json
{
  "session_id": "1786598421-4821",
  "intention": "reply to Maya",
  "duration_declared_minutes": 5,
  "is_custom_duration": false,
  "created_at": 1786598421,
  "respected": true,
  "overrun_seconds": 24
}
```

`settings_snapshot` entry, keyed by setting name (`brightness` | `volume` | `color_filters`), at most 3 keys, never a rolling array:

```json
{
  "brightness": {
    "original_value": 0.62,
    "changed_at": 1786598430,
    "changed_by_session_id": "1786598421-4821"
  }
}
```

### Field-by-field table

| Field | Type | Default | Written by | Read by | Rolling bound |
|---|---|---|---|---|---|
| `schema_version` | int | `1` | bootstrap only | load-validity gate (every run) | scalar |
| `fork` | enum `Dumb\|Sentient` | baked per-file at bootstrap | bootstrap only | routing gates, Sentient hooks, Note header | scalar, effectively immutable |
| `profile` | enum `Paradise\|Limbo\|Inferno` | `Limbo` | bootstrap (import Q), Change Profile menu | Circle-threshold lookup (OPEN), Ice cooldown-duration lookup, Status | scalar |
| `sequence` | enum `Classic\|BlackMirror\|Ambient` | `Classic` | bootstrap, Change Sequence menu | primitive-combination lookup (OPEN) | scalar |
| `voice_enabled` | bool | `true` | bootstrap (import Q), Toggle Voice menu | Voice primitive gate | scalar |
| `ai_enabled` | bool | `true` in Sentient, `false`/absent-as-false in Dumb | bootstrap (import Q, Sentient only), Toggle On-Device AI menu | Sentient hook gates (Circles II–VIII) | scalar |
| `behavioural_day` | string `yyyy-MM-dd` | today's key at bootstrap | rollover check (every entry point) | rollover comparison | always-current scalar |
| `opens_today` | int | `0` | OPEN (increment), rollover reset, Reset Today menu | Gravity calc, Note | day-bound scalar |
| `heat` | int, floor 0 cap 30 | `0` | OPEN only | Pressure calc, Note | **continuous** scalar — never reset by day rollover or Reset Today; decays by elapsed time only |
| `gravity` | int, floor 0 cap 5 | `0` | OPEN (`floor(opens_today/6)`), rollover reset, Reset Today | Pressure calc | day-bound scalar |
| `pressure` | int, derived cache | `0` | OPEN (recompute) | Circle mapping, Note, Sentient prompt | scalar |
| `circle` | int 1–9, derived cache | `1` | OPEN (recompute) | dispatch, Note, cooldown trigger | scalar |
| `last_open_at` | int epoch\|null | `null` | OPEN | debounce check | scalar |
| `last_close_at` | int epoch\|null | `null` | CLOSE (owning close only) | OPEN rapid-return calc | scalar |
| `last_app` | string\|null | `null` | OPEN | debounce (same-app check), Sentient context | scalar |
| `active_session` | object\|null | `null` | OPEN creates skeleton; Confession fills intention/duration; exit selection fills `exit_used`; CLOSE nulls it (owning close only) | CLOSE (captures at entry), Sentient context, Status | single record |
| `recent_sessions` | array | `[]` | **CLOSE only**, single append per completed session (owning or superseded, §5 below) | OPEN (`[0]` for contract-fidelity Heat delta), Note ledger, Sentient context (last 3–5) | **cap 20**, FIFO |
| `recent_contracts` | array | `[]` | **CLOSE only**, append when a contract existed | Sentient contract-auditor context (§28), Note ledger | **cap 10**, FIFO |
| `exit_stats` | object of 6 fixed keys | zeroed skeleton | OPEN, lazily, when the previous session's outcome is first observable (see §7) | exit explore/exploit selection (OPEN), Note, Sentient context | each key's `samples` **capped 20**; `count`/`sum_return_seconds` are running scalars |
| `cooldown_until` | int epoch\|null | `null` | OPEN (on Circle IX entry), Emergency Restore (clears), cooldown-expiry path (clears) | OPEN cooldown short-circuit (every run) | scalar |
| `settings_snapshot` | object, ≤3 keys | `{}` | environmental primitives (first un-restored change only — never overwrite an existing `original_value`) | CLOSE (owning), Emergency Restore, cooldown-expiry restore | ≤3 keys, no growth |
| `profile_snapshot` | object | empty skeleton | **`Sync My Profile` menu action only** | Sentient context builder, Status | whole-object overwrite each sync, no growth |
| `last_model_message` | string\|null | `null` | Sentient Mirror/Voice hook, after a successful parsed model call | next Circle's anti-repetition check | scalar (single most-recent value) |

**Deliberately excluded from v1 / marked optional:** a `lifetime_stats` block of unbounded *scalar* counters (`opens_interrupted_total`, etc.) is schema-compatible and carries zero rolling-window risk if added later for the Phase B "Life Returned" work — but PROJECT.md places that quantification explicitly Out of Scope for this milestone, so it is not included in the required v1 schema. Do not add it speculatively.

**Resolved ambiguity — where do per-exit enable/disable flags live?** §9.2 of the canonical strategy assumes some exits can be disabled, but the Control Room manual menu list (§18) has no "toggle exits" item. The clean resolution: `enabled_exits` lives inside `profile_snapshot`, populated by `Sync My Profile` parsing the proforma question "When PROSOCHĒ stops an automatic open, what would I rather do? Choose several from the six exits" — the Note is the human authoring surface for this, JSON is the derived cache, exactly matching the Note/JSON boundary in Q10. Default (before first sync, or if unparseable): all six enabled.

---

## 3. State read/write discipline

Shortcuts has no transactions, no file locks, and (per §0 grounding) no documented `Get Brightness`/`Sort List`/`Remove Item` primitives — so "as close to transactional as possible" means disciplined single-writer patterns, not real ACID.

### Load

1. **Existence check before read, not a try/read-and-catch-error.** Use `Get Folder Contents` (`file.getfoldercontents`) on the PROSOCHĒ data folder and test (`Count` → `If > 0` / or a `contains "state.json"` check) rather than calling `Get File` directly against a path that might not exist. This is a defensive substitution specifically because a hard `Get File` error on a missing path is unverified/risky behavior to build around, whereas listing a folder and inspecting the result is a documented, always-safe read. **Flag for build-time capability audit**, per §31 of the canonical strategy: confirm this substitution is actually necessary once `Get File`'s missing-file behavior is observed on-device.
2. If the folder itself doesn't exist, or the file isn't in the listing → **missing-file path** → go straight to bootstrap (§ below), skip parse entirely.
3. If found: `Get File` → `Get Contents of File` (Text) → `Detect Dictionary` → `Get Dictionary Value` for `schema_version`.
4. **Validity gate**: `schema_version` has any value, is the expected version, AND `profile` has any value (a cheap two-field sanity check, not full schema validation — full validation would itself be a place for a corrupt file to keep failing). If the gate fails → **corrupt-file path** → bootstrap, but log to the Note (best-effort) that recovery happened, so it's visible rather than silent.
5. If the gate passes, proceed with the loaded dictionary as `State`.

### Mutate

Build the **entire** next-state dictionary in memory via chained `Set Dictionary Value` calls against a single `State` variable across the run. Never write to disk mid-computation. This is the core "as transactional as possible" discipline: the disk file only ever sees a *complete*, internally-consistent snapshot, never a partially-computed one.

### Persist

**One `Save File` (overwrite) call per logical checkpoint**, never per-field. The OPEN pipeline in particular uses exactly **two** checkpoints (see Q4) — not one, not per-field — deliberately: the first captures everything essential to Pressure/Circle continuity before anything user-facing happens (so a crash mid-intervention doesn't lose behavioral-engine state); the second captures the outcome of the intervention itself (intention, duration, exit chosen) once known. Assemble the whole `State` dictionary → feed directly into `Save File` (Shortcuts coerces a Dictionary to JSON text when consumed by a text-expecting action — treat as the expected behavior, flag for on-device confirmation) → overwrite the same fixed path/bookmark every time.

### Missing file, corrupt file, partial write, self-healing bootstrap

| Scenario | Detection | Recovery |
|---|---|---|
| Missing file (first run, or user deleted it) | Folder listing doesn't contain `state.json` (§ Load step 2) | Bootstrap: build the default-state literal (per fork), `Save File`, then check/recreate the Control Room Note (independent check, see below) |
| Corrupt/unparseable JSON | `Detect Dictionary` produces nothing usable, or the two-field validity gate fails | Same bootstrap path as missing file. **Never crash, never propagate the parse failure into arithmetic.** Best-effort Note line: "State file was corrupt or unreadable — safe defaults restored on {date}." |
| Partial write (device killed mid-`Save File`, extremely rare on iOS but not impossible) | Indistinguishable from "corrupt JSON" at read time — same detection, same recovery | This is exactly why bootstrap-on-corruption must be unconditional and silent-safe: there is no way to distinguish "corrupted by a bad write" from "corrupted by anything else," so the recovery path must be identical and always safe regardless of cause |
| Control Room Note deleted independently of JSON | `Find Notes` by exact title returns zero results | Recreate the Note skeleton (setup instructions + blank proforma). **This check is independent of the JSON validity check** — the two stores can fail independently, and the architecture must not assume they fail together |

**When to run the Note-existence check:** not on every OPEN/CLOSE (an extra `Find Notes` call on the hot path is unnecessary overhead when the fast path never needs the Note per §5.4/§7.3 of the canonical strategy). Instead: (a) always on the MANUAL branch (bootstrap/Control Room entry is the natural repair point), and (b) lazily, immediately before any `Append to Note` call from OPEN/CLOSE — i.e., the moment the Note is actually about to be written to, guard it, recreate if missing, then proceed. This ties the repair cost to the moment it's needed rather than paying it on every single tracked-app open.

---

## 4. The OPEN pipeline

**Critical reordering vs. the raw §19 numbered list**: the canonical strategy's own step order in §19 lists "log meaningful OPEN if appropriate" (17) *before* "execute current Circle behaviour" (18) — but the requirement stated for this research ("the intervention should be shown before non-essential Note logging") is the opposite order. This document resolves the conflict in favor of the explicit constraint: **JSON persistence is essential and stays early; Note logging is non-essential and moves to the end, after the intervention has already been shown.** This is a deliberate, named deviation from the literal numbering in §19, not an oversight.

```
OPEN BRANCH
├─ Comment: "--- OPEN: compute Now Epoch, load state ---"
├─ Compute Now Epoch, Now Date, Behavioural Day key (§2 pattern)
├─ Load & validate state (§3) — bootstrap inline if needed
│
├─ Comment: "--- DEBOUNCE (cheap, must run before any heavy compute) ---"
├─ If (Now Epoch − last_open_at < 2s) AND (last_app == current app*)
│    → Exit Shortcut immediately, no mutation, no persist
│      (* Get Current App result if available; if the app identity can't be
│         read reliably at trigger time — flagged capability item — fall back
│         to time-only debounce: Now Epoch − last_open_at < 2s alone)
│
├─ Comment: "--- COOLDOWN SHORT-CIRCUIT (Circle IX Ice re-entry) ---"
├─ If cooldown_until has value AND Now Epoch < cooldown_until   (multi-condition If, "All are true")
│    ├─ Increment a lightweight "blocked_during_cooldown" counter only
│    │    (heat is explicitly NOT touched — blocked attempts must not inflate Heat)
│    ├─ Show remaining cooldown (deterministic, no model, no arithmetic beyond subtraction)
│    ├─ Minimal persist (counter only)
│    └─ Exit Shortcut
│    (this must short-circuit BEFORE any Heat/Gravity/Pressure recomputation)
│
├─ Comment: "--- BEHAVIOURAL DAY ROLLOVER (Q6) ---"
├─ If Behavioural Day key ≠ stored behavioural_day
│    → opens_today = 0, gravity = 0, behavioural_day = new key
│      (heat, recent_sessions, exit_stats, cooldown_until, settings_snapshot
│       are explicitly NOT touched here)
│
├─ Comment: "--- HEAT / GRAVITY / PRESSURE / CIRCLE (deterministic engine) ---"
├─ Decay heat by elapsed time since max(last_open_at, last_close_at)
├─ opens_today += 1
├─ Rapid-return heat bonus (compare Now Epoch − last_close_at against 2min/10min)
├─ Contract-fidelity heat delta, read from recent_sessions[0] (previous session's
│    contract_respected / overrun_seconds — NOT a separate "pending" field)
├─ heat += 1 (base OPEN), clamp [0, 30]
├─ gravity = floor(opens_today / 6), clamp [0, 5]
├─ pressure = heat + gravity
├─ circle = resolve via profile threshold table (Q7)
├─ If circle == 9 → cooldown_until = Now Epoch + profile's cooldown_seconds (Q7 Config)
│
├─ Comment: "--- EXIT-LEARNING LAZY OUTCOME RECORDING (Q on exit_stats) ---"
├─ If recent_sessions[0].exit_used has value AND recent_sessions[0].outcome_recorded == false
│    → interval = Now Epoch − recent_sessions[0].closed_at
│    → exit_stats[that exit].count += 1, sum_return_seconds += interval,
│       append interval to samples (rebuild-trim to cap 20, § pattern below)
│    → mark recent_sessions[0].outcome_recorded = true
│    (this is how "time until next tracked OPEN" — of ANY tracked app, not
│     necessarily the same one — gets observed: reactively, at whatever the
│     next OPEN turns out to be, however far away)
│
├─ Comment: "--- SESSION CREATION ---"
├─ session_id = combine(Now Epoch, Random Number)   [no native UUID action — §0]
├─ active_session = { id, start_at: Now Epoch, app, intention: null,
│      duration_declared_minutes: null, circle_at_open: circle,
│      heat_at_open: heat, pressure_at_open: pressure, exit_used: null }
├─ last_open_at = Now Epoch, last_app = app
│
├─ Comment: "--- PERSIST A (essential — before anything user-facing) ---"
├─ Save File (overwrite) — full State dictionary as of this point
│
├─ Comment: "--- EXECUTE CIRCLE (primitive dispatch, Q7/Q8) — shown BEFORE logging ---"
├─ Resolve sequence[profile-independent, Circle] → combination string → dispatch
│    (Confession, if present, fills active_session.intention/duration locally;
│     exit selection, if the flow reaches an exit, fills active_session.exit_used)
│
├─ Comment: "--- PERSIST B (intervention outcome) ---"
├─ Save File (overwrite) — active_session now includes intention/duration/exit_used
│
├─ Comment: "--- NOTE LOGGING (non-essential, best-effort, guarded existence check) ---"
├─ If Circle change / contract / redirect is "meaningful" (per §17 filter — not every
│    internal calculation) → guard Note existence → Append to Note
└─ Exit
```

---

## 5. The CLOSE pipeline and race handling

**Design decision that resolves most of the ambiguity here: Heat, Gravity, Pressure, Circle, and `active_session` are GLOBAL across all tracked apps, not per-app.** The v16 schema has no per-app fields for these — there is exactly one `active_session` pointer at a time. This is why interleaved OPEN/CLOSE across two different tracked apps is a real hazard, and it's what makes the reconciliation protocol below tractable: there is one well-defined "who owns the pointer right now" question, not N independent per-app state machines.

### Session-ID reconciliation protocol

```
CLOSE BRANCH
├─ Compute Now Epoch
├─ Load & validate state (§3)
│
├─ If active_session is null
│    → Anomalous CLOSE with nothing active (e.g. CLOSE fired without a matching
│      OPEN — possible if a tracked app was already foreground when PROSOCHĒ was
│      first installed). Log-and-exit, no duration math, no crash.
│
├─ Comment: "--- CAPTURE (before any wait/reload) ---"
├─ captured_id = active_session.id
├─ captured_start = active_session.start_at
├─ captured_app, captured_intention, captured_duration_declared,
│    captured_circle_at_open, captured_heat_at_open, captured_pressure_at_open
├─ actual_duration = Now Epoch − captured_start   (purely local — never needs the reload)
│
├─ Comment: "--- OPTIONAL BRIEF WAIT (race mitigation window) ---"
├─ Wait ~300–500ms   (`delay` action) — gives a near-simultaneous OPEN
│    (e.g. rapid switch to a second tracked app) time to finish its own
│    session-creation + Persist A before this CLOSE reloads
│
├─ Comment: "--- RELOAD & COMPARE (compare-and-swap approximation) ---"
├─ Reload state fresh from disk
├─ current_id = (reloaded) active_session.id, or null if active_session is now null
│
├─ If current_id == captured_id   → OWNING CLOSE (normal, non-interleaved case)
│    ├─ Idempotency guard: if recent_sessions already contains an entry with
│    │    session_id == captured_id → skip append (duplicate CLOSE trigger,
│    │    e.g. iOS firing Is Closed twice), just exit
│    ├─ Compute overrun_seconds, contract_respected from actual_duration vs.
│    │    captured_duration_declared
│    ├─ Append full session record to recent_sessions (cap 20, rebuild-trim)
│    ├─ Append to recent_contracts if a contract was declared (cap 10)
│    ├─ Update exit_stats immediately if exit_used is a same-run same-app exit
│    │    (rare fast path; the common case is the lazy OPEN-time recording in §4)
│    ├─ active_session = null
│    ├─ last_close_at = Now Epoch
│    ├─ Restore settings_snapshot (this CLOSE genuinely ends the tracked-app
│    │    engagement — see Q9)
│    └─ Persist (single Save File)
│
└─ If current_id ≠ captured_id   → SUPERSEDED CLOSE (interleaved case)
     ├─ Idempotency guard: same duplicate-check as above, using captured_id
     ├─ Still append A's completed session record to recent_sessions using the
     │    LOCALLY CAPTURED fields (captured_id/start/app/etc.) — A's engagement
     │    genuinely happened and its duration is real, usable data, independent
     │    of whichever session (B) is now globally "active"
     ├─ Do NOT touch active_session (it belongs to B now)
     ├─ Do NOT restore settings_snapshot (B may still want Ash/Dimming/Silence
     │    active — restoring now would strip friction already correctly applied
     │    to B's session)
     ├─ Do NOT update last_close_at (it would incorrectly attribute B's ongoing
     │    engagement as "just closed")
     └─ Narrow persist: only the recent_sessions append, nothing else
```

**Honesty about the limitation**: this is a compare-and-write approximation, not a true compare-and-swap — there is still a narrow window between "reload" and "write" where another run could theoretically interleave again. The window is now small (a handful of actions, not the full Heat/Gravity computation), and the idempotency guard (de-dupe by `session_id` already present in `recent_sessions`) bounds the damage of any remaining race to "at most a duplicate write attempt that gets silently skipped," never corruption. Document this as an accepted limitation of building on a non-transactional file store, not a claim of full atomicity.

**Accepted downstream approximation**: because Heat/rapid-return signals are global, a superseded CLOSE's `last_close_at` is deliberately not updated — meaning a subsequent reopen of app A specifically will compute its rapid-return delta against B's close time, not A's own. This is consistent with the global-Heat design decision (Heat measures aggregate compulsive attention-switching across all tracked apps, not per-app cadence) and should be stated as intentional, not a bug, when documenting build notes.

---

## 6. Behavioural-day rollover

- **Computed**: at the top of every entry point (OPEN, CLOSE, MANUAL) — cheap (one date-key string compare), and running it redundantly in all three is safe because the reset logic is gated behind "did the key actually change since last stored," making it idempotent regardless of how many entry points execute it in a day.
- **Formula**: `behavioural_day = Format(Now Epoch − 4h, "yyyy-MM-dd")`.
- **Resets on rollover**: `opens_today → 0`, `gravity → 0`. (`pressure`/`circle` are then recomputed downstream from the new `heat + gravity`, in OPEN only — CLOSE and MANUAL don't need Pressure/Circle recomputation, just the `behavioural_day` stamp update for Note-dating consistency.)
- **Must NOT reset**: `heat` (decays continuously by elapsed time, independent of day boundaries — this is explicit in §10.2 of the canonical strategy and is the entire reason Heat and Gravity are modeled as two separate signals), `recent_sessions`, `recent_contracts`, `exit_stats`, `cooldown_until` (a cooldown spanning midnight must still be honored), `settings_snapshot`, `profile`/`sequence`/`fork`/`voice_enabled`/`ai_enabled`/`schema_version`/`profile_snapshot`, `last_open_at`/`last_close_at`/`last_app`.
- **Manual "Reset Today" menu action** performs exactly the same reset as rollover (`opens_today`, `gravity` → 0) and nothing more — it explicitly does **not** reset `heat`, for the same continuity reason. This is a named design decision: "Reset Today" resets *daily accumulation*, not the *compulsive-clustering* signal.

---

## 7. Pressure → Circle mapping

### Data structure: one static Config literal, shared verbatim by both forks

Both profile thresholds and sequence tables are **not** part of mutable `state.json` — they are a literal JSON blob authored directly into the action graph (a `Text` action holding the literal, parsed once per run via `Detect Dictionary` into a `Config` variable). This is a deliberate separation from `state.json`: thresholds/sequences are *product configuration*, not *user data* — they never need per-user persistence, only per-user *selection* (which key to use), and keeping them out of `state.json` means `Change Profile`/`Change Sequence` only ever write a short string, never risk corrupting a numeric table.

```json
{
  "thresholds": {
    "Paradise": [1, 4, 7, 10, 13, 16, 19, 22, 25],
    "Limbo":    [1, 3, 5, 7, 9, 11, 14, 17, 20],
    "Inferno":  [1, 2, 4, 6, 8, 10, 12, 14, 16]
  },
  "cooldown_seconds": { "Paradise": 60, "Limbo": 180, "Inferno": 300 },
  "sequences": {
    "Classic":     ["Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice"],
    "BlackMirror": ["Knock", "Confession", "Ash+Confession", "Mirror", "Silence+Mirror", "Dimming+Mirror", "Exile", "Voice", "Ice"],
    "Ambient":     ["Ash", "Silence", "Dimming", "Knock", "Confession", "Exile", "Mirror", "Voice", "Ice"]
  }
}
```

Because `Config` is identical in both forks (Q11), this table is authored **once** and copied verbatim, never hand-diverged.

### Resolving Pressure → Circle

Given `pressure` and the active profile's threshold array `T[1..9]` (ascending), Circle = the highest index `i` such that `pressure >= T[i]`, clamped to `[1, 9]`. No native "find index" action exists, so implement as a bounded linear scan (9 iterations is trivial cost, well within documented `Repeat Count` capability):

```
Set Variable "Circle" = 1
Repeat 9 times (Repeat Index)
  If pressure >= Get Item from List(thresholds[profile], Repeat Index)
    → Set Variable "Circle" = Repeat Index
End Repeat
```

Because thresholds ascend and the assignment always overwrites, the loop naturally lands on the *highest* satisfied threshold after 9 iterations — a simple, fully-documented-primitives-only implementation.

### Resolving Circle → primitive combination

`combination = sequences[sequence][circle]` (a string like `"Ash+Confession"`) → this string is what Q8's dispatch gates against directly; the runtime does not need to `Split Text` it into an array unless a primitive-by-primitive loop is preferred over the flat If-chain described in Q8.

---

## 8. Primitive dispatch

**The sequence table itself is the single source of truth for "which primitives fire at this Circle," and it is non-cumulative by construction.** Each Circle's entry in the `sequences` Config lists *exactly* the primitives for that Circle (e.g. Classic Circle 5 = `"Dimming"` alone, not `Knock+Ash+Silence+Confession+Dimming`). This directly satisfies "a stronger Circle does not necessarily replay every weaker prompt" (§32 acceptance criteria) — replay-avoidance is a data-modeling property, not something the dispatch logic has to separately enforce or remember.

### Structure

Nine Comment-delimited primitive blocks, each gated by a single `If` testing whether the resolved `combination` string **contains** that primitive's name (`WFCondition = 99`, per §0 grounding — all nine primitive names are visually disjoint substrings of each other, so `contains` is a safe test):

```
Comment: "--- PRIMITIVE: The Knock ---"
If combination contains "Knock"
  → deterministic Knock copy (Dumb + Sentient both have this — Knock has no
    Sentient hook per §14.4, Circle I is deterministic-only for latency)
End If

Comment: "--- PRIMITIVE: Ash ---"
If combination contains "Ash"
  → environmental grayscale attempt, wrapped in the settings-snapshot guard (Q9)
End If

... (Silence, Confession, Dimming, Exile, Mirror, Voice, Ice — same pattern)
```

Because a Circle's combination typically names only one or two primitives, this flat sequence of up-to-nine independent `If` checks is simpler and more debuggable than a nested loop over a split array, at negligible extra cost (9 cheap string-contains checks per OPEN).

**Sentient hooks live inside the Mirror/Confession/Voice (and related) primitive blocks as an additional inner `If`**, gated on `fork == "Sentient" AND ai_enabled == true AND circle` in the appropriate range (Circles II–VIII per §14.4) — see Q11 for the exact fallback shape. The primitive block's deterministic behavior is always present as the `Otherwise` branch of that inner If, meaning the primitive *always* does something safe and correct even when the model call is skipped, fails, or is disabled.

---

## 9. Settings snapshot / restoration

**This is the section most constrained by an actual capability gap, not just a design choice.** Per §0's grounding audit, the documented action catalog contains `setbrightness` and `setvolume` (write) but **no `Get Brightness` / `Get Volume` (read) action**. This is not a hypothetical risk — it is the most concrete, evidenced finding in this research, and it directly validates the canonical strategy's own §21 fallback instruction ("if the original value cannot be read, do not make the intervention").

### Design consequence

Every environmental primitive (Ash/grayscale, Dimming/brightness, Silence/volume) is wrapped:

```
If [attempt to read original value] — has any value
  → settings_snapshot[setting] = { original_value, changed_at: Now Epoch,
       changed_by_session_id: active_session.id }   (only if no un-restored
       snapshot already exists for this key — never overwrite a true original
       with a value captured mid-friction)
  → apply the change (setbrightness/setvolume/color filter action)
Otherwise
  → SKIP the stateful change entirely for this one primitive; the primitive's
    text/Mirror behavior (if any) still runs — a failed environmental read
    degrades one primitive to message-only, it does not fail the whole Circle
```

**Build-time capability audit required** (flagged explicitly, per §31's instruction not to fabricate actions): confirm whether `getdevicedetails` exposes a brightness reading (plausible but undocumented in these files), and whether any read path exists for volume or Color Filters state at all. If none exists for a given setting, that primitive should be architected from day one as **message-only** for that setting, not as a "try and hope" — i.e., the "Dimming" and "Silence" primitives may need to ship in v1 as Knock-style text-only friction (referencing the concept: *"The screen could be dimmer right now."*) rather than actual system-setting manipulation, until/unless a safe read path is confirmed. This should be treated as an expected, planned outcome, not a build failure.

### Restoration triggers

Four independent triggers, all performing the same operation (restore every key in `settings_snapshot` from its `original_value`, then clear the object to `{}`):

1. **Owning CLOSE** (Q5) — the normal path.
2. **Emergency Restore** manual menu action — always available, works regardless of `active_session` state.
3. **Cooldown-natural-expiry**, detected at the top of the next OPEN that observes `Now Epoch >= cooldown_until` — added specifically to close a gap the canonical strategy doesn't otherwise address: if the user is ejected into Ice and never generates a CLOSE event (e.g., they just leave the phone locked), a grayscale/dimmed state could otherwise persist indefinitely until manual Emergency Restore. Restoring at cooldown expiry is a reasonable and cheap addition since that's exactly the moment the friction has "served its purpose."
4. *(Explicitly NOT a trigger: superseded CLOSE, per Q5 — restoring there would strip friction that legitimately still belongs to the other tracked app's active session.)*

---

## 10. Note vs JSON boundary

| Goes in the Note | Goes in JSON | Never |
|---|---|---|
| READ THIS FIRST setup instructions (static, written once at bootstrap, never re-parsed) | Every field the fast OPEN/CLOSE path needs to read (§2's full schema) | A CSV, a second machine store of any kind |
| `MY PHONE, ON PURPOSE` proforma (human-editable, free text) | `profile_snapshot` — the *only* thing ever extracted from the Note back into JSON | The Note being parsed on the OPEN/CLOSE hot path |
| CURRENT SETTINGS / CURRENT STATE sections (write-only from the Shortcut's perspective — human-readable, never read back) | Everything mutable and hot-path-relevant | Full-Note regex/Match Text parsing anywhere except the manual `Sync My Profile` action |
| ATTENTION LEDGER (append-only meaningful events, never read back) | | |

**`Sync My Profile` mechanics** (manual menu action only, never automatic, never on OPEN/CLOSE):

1. `Find Notes` by exact title "PROSOCHĒ — Control Room" → guard existence (recreate if missing, per Q3).
2. Get Note contents.
3. Extract just the `MY PHONE, ON PURPOSE` section — bounded between that heading and the next `##` heading — via `Match Text` → `Get Group` (regex is acceptable here precisely *because* this is a manual, infrequent, non-hot-path action; the same technique would be too slow/fragile to run on every tracked-app open, which is exactly why it's gated to this one menu action).
4. Compact the extracted text into the small `profile_snapshot` fields (`goal`, `phone_purpose`, `reclaim_for`, `deliberate_leisure_definition`, `enabled_exits` — parsed from the "which exits" question).
5. `Set Dictionary Value` into `State.profile_snapshot`, stamp `synced_at = Now Epoch` and a `note_content_hash` (so a future "the Note changed, want to resync?" prompt has something cheap to compare against without re-parsing every time).
6. Single `Save File`.

This is the *only* code path in the entire shortcut that reads the Note's rich content back into JSON — everywhere else, the Note is write-only.

---

## 11. Dumb ↔ Sentient shared-source strategy

**Requirement conflict resolved explicitly**: PROJECT.md requires two distinct signed `.shortcut` files (not one universal file that self-detects capability), and separately, shipping Sentient-only action references (`askllm`/Use Model) into a build distributed to non-Apple-Intelligence hardware is architecturally unsafe — the action may simply not be usable/selectable on incompatible devices, and §5.7/§13 of the canonical strategy is explicit that Dumb must be "a coherent product... not a degraded afterthought," which rules out shipping it with dead Sentient action references. So: **two files, one canonical authoring relationship between them.**

### Practice: Dumb is the base; Sentient is a disciplined, versioned remix — never two independently hand-maintained files

1. **Dumb XML is the canonical source.** It contains the full deterministic skeleton: routing, bootstrap, state I/O, OPEN/CLOSE pipelines, all nine primitives in their deterministic form, contracts, exits, exit-learning, Control Room menu, Circle IX.
2. **Sentient hook insertion points are exactly the ones enumerated in §14.4 of the canonical strategy** — no more, no fewer:

   | Circle | Hook |
   |---|---|
   | I | none — deterministic only, latency-critical |
   | II | optional lightweight mirror, only if cached/fast enough; else deterministic |
   | III | model may choose among a small set of message *tones*, may not alter Pressure |
   | IV | intent classification + at most one clarifying question |
   | V | short observation using current contract + recent history |
   | VI | model may classify which exit best matches stated intent; explore/exploit engine still governs actual routing |
   | VII | full Contract Auditor + Mirror |
   | VIII | full Mirror + Voice |
   | IX | none — deterministic Ice only, never model-decided |

3. **Every hook is wrapped, never a replacement**: `If fork == "Sentient" AND ai_enabled AND [Use Model call succeeded AND output parses as valid ALLOW/CHALLENGE/DENY JSON] → use model result. Otherwise → run the exact same deterministic logic the Dumb build already has at that Circle.` This means the Sentient file *literally contains* the complete Dumb primitive logic for every hooked Circle, as the `Otherwise` branch — Sentient = Dumb + additive wraps, never an independent rewrite. This is what makes "falls back deterministically" concrete rather than aspirational.
4. **Maintenance practice**: keep a short, versioned build note (not shipped) — e.g. `SENTIENT-HOOKS.md` — listing the exact anchor `Comment` text at each of the eight insertion points above. Every time the Dumb baseline changes (bugfix, new deterministic behavior, a new primitive variant), re-apply the hook spec to regenerate Sentient via the `shortcuts-playground:remix` skill (which is explicitly built for "apply a natural-language diff to an existing XML source") rather than hand-patching two files in parallel. Dumb is source; Sentient is derived; the remix is the diff.
5. **#1 build-risk flag for this fork**: the `Use Model` action's documented parameters (`WFAllowWebSearch`, `FollowUp`) do not include a model-source selector. Before writing a single line of Sentient XML, the build agent must inspect the live `Use Model` action configuration UI on a real device/simulator and record the actual parameter/key used to force **On-Device** (never Private Cloud Compute, never ChatGPT — a hard constraint in PROJECT.md and §5.6/§14/§27). Do not guess this parameter.

---

## 12. Build order implications

Dependency-ordered, not effort-ordered — each phase is either a hard prerequisite for the next or deliberately proven in isolation before being wired into something more expensive to debug.

1. **Config literals + schema definition.** Thresholds/sequences/cooldowns (Q7) baked as a literal; the default-state JSON literal per fork (Q2). Nothing to test yet, just source-of-truth artifacts everything else depends on.
2. **Routing + input normalization (Q1) + bootstrap (Q3).** Provable standalone: manual run with no input, with input `"OPEN"`, with input `"CLOSE"` (via a temporary Ask-for-Input test harness or hardcoded literals during authoring) — confirm correct branch selection, confirm bootstrap creates JSON + Note correctly on first run, confirm repeated manual runs never clobber existing state. Everything else nests inside this skeleton.
3. **State load/validate/persist discipline (Q3), proven against corrupt-file and missing-file cases specifically** (delete/corrupt `state.json` by hand between test runs) — before any behavioral logic is written, since every subsequent phase reads and writes through this layer.
4. **OPEN pipeline arithmetic only** — Heat/Gravity/Pressure/Circle mapping, behavioural-day rollover (Q4, Q6, Q7) — with all nine primitives stubbed to `Show Alert` placeholders. This proves the numeric engine correct (§32's "all three profiles differ," "Gravity accumulates," "Heat decays," "rapid return increases Heat") in isolation, before compounding it with UI/friction/environmental-setting debugging on a real device at the same time.
5. **CLOSE pipeline + session-ID race protocol (Q5)** — proven via manual two-tracked-app rapid-switch testing on-device (§32's explicit acceptance case: "rapid switching between two tracked apps does not corrupt state").
6. **Nine primitives, deterministic/Dumb versions, replacing the Circle-4 stubs** — including the settings-snapshot/restoration wrapping (Q9), with the brightness/volume read-capability audit (§0/§9) resolved *before* this phase starts, since it determines whether Dimming/Silence ship as environmental or message-only in v1.
7. **Six exits + explore/exploit learning + `exit_stats`** (Q7's lazy-outcome-recording design in §4).
8. **Intention contracts (Confession)** wired into `active_session` and closing the contract-fidelity Heat feedback loop from step 4's placeholder formula into real data.
9. **Control Room manual menu** (Status / Sync My Profile / Change Profile / Change Sequence / Toggle Voice / Test a Circle / Reset Today / Emergency Restore) — depends on steps 2–8 all existing, since every menu action exercises or resets state those steps created.
10. **Circle IX Ice cooldown + Emergency Restore interplay** — depends on `settings_snapshot` (step 6) and `cooldown_until` (step 4).
11. **Freeze Dumb**: full §32 acceptance pass, validate, sign, import-test on-device.
12. **Fork Sentient**: apply the hook spec (Q11) at Circles II–VIII, resolve the `Use Model` on-device-selection parameter (the flagged capability item), add Toggle On-Device AI / Test Model menu items.
13. **Sentient acceptance pass**: validate, sign, import-test.
14. **Explicitly deferred** (per PROJECT.md Out of Scope for this milestone): Life Returned/value metrics, pay-after-value, Screen Time telemetry, NFC — none of the schema or architecture above blocks adding these later; `lifetime_stats` scalars could be started opportunistically in step 8 if desired, but are not required.

**Why this order and not another**: routing/bootstrap/state-discipline (1–3) must be unshakeable before *any* behavioral logic exists, because every later phase reads and writes through exactly that layer — a bug there corrupts everything built on top of it silently. OPEN arithmetic (4) is proven with cheap stub primitives before real primitives (6) are wired, so formula bugs and on-device brightness/grayscale/API bugs are never being debugged simultaneously. CLOSE/race-protocol (5) lands before exits/contracts (7–8) because contract fidelity is *defined in terms of* accurate session duration, which the race protocol is what makes trustworthy under real multi-app usage. Dumb (1–11) must fully pass acceptance before Sentient work starts (12) because every Sentient hook is an additive wrap around already-correct Dumb branches (Q11) — an unstable Dumb baseline would force the same rework twice, once in each file, defeating the entire shared-source strategy.

---

## Anti-Patterns

### Anti-Pattern 1: Helper-shortcut fan-out for internal control flow
**What people do:** split OPEN/CLOSE/Control-Room/primitives into separate installable Shortcuts connected via `Run Shortcut`.
**Why it's wrong:** multiplies install burden (contradicts one-tap self-saucing onboarding), adds per-hop process-launch latency on a path that needs to feel instant, adds a dictionary-serialization boundary with historically lossy type fidelity, and produces zero isolation benefit since nothing here needs sandboxing.
**Instead:** one monolithic action graph per fork, internally organized as clearly Comment-delimited virtual subroutines (Q1).

### Anti-Pattern 2: Storing timestamps as formatted date strings in `state.json`
**What people do:** persist `"2026-08-13T22:41:00Z"`-style strings for `last_open_at`/`last_close_at`/etc.
**Why it's wrong:** every arithmetic operation (decay, rapid-return window, cooldown check, session duration) then requires re-parsing the string back into a `Date` object before it can be compared or subtracted — extra actions on the hottest path in the whole shortcut, and Shortcuts has no reliable locale-independent string→Date parse action verified in these docs.
**Instead:** integer Unix epoch seconds for every timestamp field except `behavioural_day` (a lookup key, not an arithmetic operand) — see Q2.

### Anti-Pattern 3: Mutating array entries in place
**What people do:** create a `recent_contracts` entry at OPEN time (with `respected: null`), then try to find-and-update that same array element at CLOSE.
**Why it's wrong:** Shortcuts has no documented in-place array-element-update primitive and no `Remove Item from List` action (§0) — implementing "find element by id, replace it, keep the rest" requires an awkward rebuild-the-whole-array loop for what should be a trivial operation.
**Instead:** hold provisional fields (`intention`, `duration_declared_minutes`) in `active_session` only; append to `recent_sessions`/`recent_contracts` exactly once, at CLOSE, fully formed — pure append-only writes, never in-place mutation (Q2, Q4, Q5).

### Anti-Pattern 4: Assuming brightness/volume can always be read back
**What people do:** write `setbrightness`, later `setbrightness` back to "whatever it was," without first confirming a read path exists.
**Why it's wrong:** no `Get Brightness`/`Get Volume` action is documented in the available action catalog (§0) — building the restoration logic on an unverified assumption risks either silent failure or, worse, restoring to a wrong hardcoded fallback value, which directly violates the canonical strategy's own safety rule in §21.
**Instead:** wrap every environmental primitive in a read-succeeded gate; degrade to message-only when the read isn't available (Q9).

---

## Sources

- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` (this repo) — §5, §10–12, §14, §16–22, §30–32, §35 specifically informed this document.
- `.planning/PROJECT.md` (this repo) — Active requirements, Constraints, Out of Scope.
- Shortcuts Playground plugin docs (`~/.claude/plugins/marketplaces/shortcuts-playground/claude/skills/shortcuts-playground/`): `CONTROL_FLOW.md`, `DATE_TIME.md`, `BEST_PRACTICES.md`, `VARIABLES.md`, `ACTIONS.md`, `APPINTENTS.md`, `AUTOMATION_TRIGGERS.md` — read in full or via targeted grep during this research; all control-flow, condition-code, timestamp, and action-catalog claims above are grounded in these files as of the versions present on disk (Shortcuts Playground v1.2.1).

---
*Architecture research for: PROSOCHĒ — Nine Circles (single stateful iOS Shortcut, greenfield)*
*Researched: 2026-08-13*
