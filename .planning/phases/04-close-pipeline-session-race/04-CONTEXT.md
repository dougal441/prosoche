# Phases 3+4 (merged): Deterministic State Engine & CLOSE Pipeline - Context

**Gathered:** 2026-08-13
**Status:** Ready for execution
**Mode:** Compressed — planner and plan-checker skipped by owner decision. The canonical strategy and `src/CONFIG-BLOCK.md` already specify every coefficient, threshold and step exactly; a planner would only re-derive them. Executor works from this context directly. Verifier still runs.

<domain>
## Phase Boundary

**Phase 3 (STATE-01..11):** Given any sequence of OPEN events and contract outcomes, the engine computes Heat, Gravity, Pressure and the resulting Circle exactly as specified — reproducible, and provably different across the three profiles.

**Phase 4 (SESS-01..07):** Session duration is measured accurately and safely even under rapid app switching or overlapping automation triggers, and CLOSE always leaves state consistent.

These are merged because both are pure state arithmetic on the same file and the same two stub anchors, with no gate between them.

## The two windows this closes

`.planning/WINDOWS.md` has two open stubs, both in `src/PROSOCHE-Dumb.xml`:
- **id 1** — OPEN branch anchor is Comment+Nothing only; Phase 3 fills the OPEN pipeline
- **id 2** — CLOSE branch anchor is Comment+Nothing only; Phase 4 fills the CLOSE pipeline

Mark both fixed when done: `gsd-tools windows fixed 1` / `gsd-tools windows fixed 2`.

## Toolchain

Plugin root: `/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/`
- **Validator:** `bin/validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` — must pass before every commit. `--target-platform all` is required (DEV-04).
- Load `Skill(skill="shortcuts-playground:shortcuts-playground")` before editing XML.
- A `PostToolUse` hook auto-validates and requires a bulleted wiring list in any Comment immediately preceding a control-flow start.

## Established patterns — reuse, do not reinvent

Proven in the existing 133-action graph:
- Nested `If`/`Otherwise` at depth with balanced GroupingIdentifiers (13 blocks). **Never `Otherwise If`** — macOS-27 only.
- State load via Get File (`WFFileErrorIfNotFound` off) → Detect Dictionary → validity gate. Already runs **above** the router, so OPEN and CLOSE both have state loaded before they branch.
- `WFTextTokenString` with `` placeholders on every display string; `WFTextTokenAttachment` only for data-flow params.
- Dictionary coercion hazards: booleans read back as 1/0, null reads as empty, a read on a null parent breaks. Route through Text per the recipe in `src/CONFIG-BLOCK.md`.
- Import questions are pinned at action indices 2 and 4 — **never insert an action above index 5**.

</domain>

<decisions>
## Implementation Decisions

### Every number comes from `src/CONFIG-BLOCK.md` — read it, do not hardcode

The config JSON is already embedded in the graph and parsed into a dictionary. Read values from it. Hardcoding a threshold defeats the entire point of the config block, which exists so these prototype parameters can be tuned without restructuring.

Canonical values (cross-check against the config block; the config block wins if they differ):

- **Behavioural day** = current time − 4 hours, formatted `yyyy-MM-dd` (§10.1)
- **Heat** (§10.2): base OPEN `+1`; reopen <2 min additional `+2`; reopen <10 min additional `+1`; previous session exceeded its declared duration by >50% **and** >2 min → `+2`; previous contract respected → `−1`; decay `−1` per ~10 min away; floor `0`; cap `30`
- **`heat.reopen_bonus_mode`** is `"exclusive"` — a 90-second reopen earns `+2` only, never `+2 +1`. Read the key and branch on it; do not hardcode either behaviour.
- **Gravity** (§10.3) = `floor(opens_today / 6)`, cap `5`
- **Pressure** (§10.4) = `heat + gravity`
- **Thresholds** (§10.5): Paradise `1,4,7,10,13,16,19,22,25` · Limbo `1,3,5,7,9,11,14,17,20` · Inferno `1,2,4,6,8,10,12,14,16`

### Circle resolution is an ordered ≥ scan, never an equality test

There is **no numeric-equals condition code** in Shortcuts (code `0` is "is less than", not "equals"). Resolve the Circle by scanning the active profile's nine thresholds and taking the highest index whose threshold is `≤ pressure`. Clamp to 1..9.

### Ordered Heat pipeline — order matters, clamp last

1. Decay by elapsed time since last interaction
2. Add base OPEN
3. Add rapid-reopen bonus (per `reopen_bonus_mode`)
4. Apply previous contract outcome (`+2` overrun / `−1` respected)
5. Clamp to floor/cap

### Behavioural-day rollover

Resets `opens_today` and (by recomputation) Gravity. Does **not** reset `heat`, `recent_sessions`, `recent_contracts`, or `exit_stats` — Heat decays continuously across the boundary rather than being zeroed.

### Debounce (STATE-11)

Duplicate OPEN events from a single user action must increment the open count once. Use a short elapsed-time threshold against `last_open_at`; if the gap is below it, treat the event as a duplicate and take no state-mutating action. Ponytail: this is one timestamp comparison, not an event-dedup system.

### The CLOSE race protocol (SESS-03, SESS-04) — the one genuinely hard part

The hazard: rapid switching between two tracked apps interleaves OPEN and CLOSE runs, so a CLOSE can arrive after a newer OPEN has already claimed the state.

Protocol, in order:
1. Capture the active session ID and its start timestamp from the state loaded at entry
2. Brief `Wait` to let an interleaved OPEN land
3. **Reload** state from disk
4. Compare the reloaded active session ID against the captured one
5. If they differ, a newer OPEN owns the state — **abort without writing anything**
6. If they match, this CLOSE owns the session: compute duration, compare against the declared contract, record overrun, append to the rolling window, clear the active session, restore any environmental setting PROSOCHĒ changed, persist

Aborting must be a genuine no-write path. A CLOSE that loses the race and still writes is the corruption this protocol exists to prevent.

### Cooldown short-circuit (feeds CIRC-10/11 in Phase 5)

If `cooldown_until` is in the future when OPEN fires, the OPEN must not inflate Heat. Compute and persist the short-circuit here so Phase 5 only has to attach the Ice behaviour to it.

### What this phase does NOT do

No primitives fire. No Circle *behaviour* executes. The OPEN pipeline computes the Circle number and persists it; a Comment marks where Phase 5 attaches dispatch. Same for CLOSE and the environmental restore hook — record the intent, leave the wiring point.

### Claude's discretion

Action layout, variable naming (respect the register in `.planning/phases/02-routing-bootstrap-control-room/SKELETON.md` — do not collide), how the threshold scan is expressed, and how much is inlined versus set into named variables.

</decisions>

<code_context>
## Existing Code Insights

`src/PROSOCHE-Dumb.xml` — 133 actions, validates, signs. Structure:

- indices 0–4: header comments + the two import-question Text actions (**pinned — do not disturb**)
- config transcription, epoch/behavioural-day clock
- state load chain (Get File → Detect Dictionary → two-field validity gate → bootstrap → Save File), positioned **above** the router so all three modes share it
- router: outer `has any value` gate (`F646324A`) → `OPEN` (`FA045F2B`) → `CLOSE` (`A2F7247B`) → fail-safe alert
- OPEN branch anchor: Comment + Nothing (window 1)
- CLOSE branch anchor: Comment + Nothing (window 2)
- MANUAL branch: bootstrap check, Note guard, Show Note

Read before editing:
- `docs/BUILD-NOTES.md` — the action vocabulary (CAP-01..CAP-34 + CAP-S*), §8 revisions, §11 device evidence
- `src/CONFIG-BLOCK.md` — the config JSON, field reference, derived-value rules, transcription recipe
- `.planning/phases/02-routing-bootstrap-control-room/SKELETON.md` — S-01..S-16 decisions and the variable register
- `.planning/phases/02-routing-bootstrap-control-room/02-0*-SUMMARY.md` — what each wave built and its deviations

Relevant verified capabilities: CAP-04 Dictionary/Detect Dictionary · CAP-05 Get/Set Dictionary Value · CAP-06 date arithmetic (Adjust Date, Format Date, Get Time Between Dates) · CAP-24 Wait (`WFDelayTime`, a bare float) · CAP-S01 Set/Get Variable · CAP-S03 Number/Math · CAP-S04 If/Otherwise/End If · CAP-S05 Repeat · CAP-S06 Get Item from List.

**Math operator gotcha** (skill Key Rule 53): addition = OMIT `WFMathOperation`; subtraction = `-`; multiplication = `×` (U+00D7); division = `÷` (U+00F7). ASCII `*` and `/` silently render as `+`.

</code_context>

<specifics>
## Specific Ideas

### Requirements this must satisfy

**Phase 3:** STATE-01 behavioural day · STATE-02 rollover semantics · STATE-03 decay · STATE-04 OPEN + rapid-reopen · STATE-05 contract-outcome adjustment · STATE-06 clamp · STATE-07 Gravity · STATE-08 Pressure · STATE-09 Circle mapping via ordered comparison · STATE-10 three profiles demonstrably differ · STATE-11 duplicate-OPEN debounce

**Phase 4:** SESS-01 session ID + start timestamp · SESS-02 duration measured · SESS-03 abort when superseded · SESS-04 rapid switching does not corrupt · SESS-05 contract comparison + overrun · SESS-06 clear session, append to rolling window · SESS-07 restore environmental settings

### Verification shape

No device, no test runner. Verify by:
- The validator passing
- Structural assertions on the plist (the threshold scan exists, the abort path contains no Save File, the clamp is last in the Heat chain)
- **A reference implementation of the arithmetic**, written as a small self-checking Python script under `docs/` or `src/`, that encodes the same Heat/Gravity/Pressure/Circle rules and asserts the worked examples below. This is the ponytail-sanctioned "one runnable check" for non-trivial logic — it proves the specification is coherent and gives Phase 5 a reference oracle. It does **not** test the plist; say so plainly in the file.

Worked examples the reference implementation must assert:
- Limbo, pressure 0 → Circle 1; pressure 3 → Circle 2; pressure 20 → Circle 9; pressure 99 → Circle 9 (clamped)
- Paradise vs Limbo vs Inferno at pressure 8 → three different Circles
- `opens_today` 0→Gravity 0; 6→1; 30→5; 60→5 (capped)
- Heat: 25 minutes away then an OPEN → decay −2, base +1
- Heat clamps at 30 and never below 0

### Ponytail discipline for this phase

The engine is arithmetic, not architecture. No abstraction layer over the config dictionary, no generalised rule engine, no event-sourcing. Read values, compute in order, clamp, write once. The CLOSE race protocol is the only place that earns real care — and it earns it because losing that race silently corrupts user data.

</specifics>

<deferred>
## Deferred Ideas

- Circle *behaviour* (the nine primitives) — Phase 5
- Exits, exit learning, contracts UI — Phase 6
- Ice cooldown behaviour — Phase 5 (this phase only computes and persists the short-circuit)
- Attention Ledger writing — Phase 7
- Anything Sentient — Phase 8

</deferred>
