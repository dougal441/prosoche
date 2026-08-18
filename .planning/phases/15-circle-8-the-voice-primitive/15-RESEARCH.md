# Phase 15: Circle 8 — the Voice primitive - Research

**Researched:** 2026-08-18
**Domain:** iOS Shortcuts plist generation (Python generator-patcher), primitive dispatch, `is.workflow.actions.speaktext`, state-flag typing
**Confidence:** HIGH on structure and catalog facts; MEDIUM on the two device-gated questions (voice-flag coercion, inherited axis-4 picker)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

None. CONTEXT.md records no locked decisions — the discuss phase was skipped via
`workflow.skip_discuss`.

### Claude's Discretion

> All implementation choices are at Claude's discretion — discuss phase was skipped per user
> setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide
> decisions.

### Deferred Ideas (OUT OF SCOPE)

> None — discuss phase skipped.

**Consequence for the planner.** The one genuine product decision this phase carries — what
Circle 8 does when `voice_enabled = 0` — was *not* put to the user. The ROADMAP itself calls
it "a real product decision, not an implementation detail." This research recommends a
default (below, Decision D-15-A) and the planner should surface it as a
`checkpoint:human-verify` rather than burying it in a task action.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CIRC-08 | The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels | §Standard Stack (`speaktext` parameter set, VERIFIED); §Pitfall 2 (the `voice_enabled` type split — the gate CIRC-08 hangs on); §Pitfall 3 (`Spoken This Run` is already sufficient under condition-4 dispatch); §Pitfall 5 ("never at unsafe levels" cannot be enforced through a `speaktext` parameter — there is none) |
| CIRC-09 | Ice applies a deterministic cooldown whose duration varies by profile, decided entirely without the model | No code change required. `ice_start()` is untouched and Circle 9 = `Frozen` in all three sequences. Satisfied by **regression**: `verify_dispatch_coverage()` + `docs/phase5_self_check.py` + `docs/sequence_dispatch_check.py` must stay green after the Circle-8 edit. In scope only because Phase 15 is the first phase in which an 8→9 escalation is materially distinct |
| CIRC-14 | A stronger Circle does not necessarily replay every weaker Circle's prompt | Currently **violated at 7→8**: both dispatch to the identical `mirror_and_voice()`, so Circle 8 replays Circle 7 verbatim. §Architecture Pattern 2 (the split) is what satisfies it |
| DIST-01 | Both forks pass the Shortcuts Playground validator at the iOS 26 target | §Environment Availability (gate A tooling present); §Standard Stack (`speaktext` present in the v63 snapshot that gate A consults, so no new identifier risk); the two-gate rule in `.claude/CLAUDE.md` §1 is the authority |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

Directives extracted from `.claude/CLAUDE.md` that bind this phase. The planner must not
produce a task that contradicts any of these.

| # | Directive | Where it bites in Phase 15 |
|---|---|---|
| C-1 | **Never fabricate an action or a literal.** If it cannot be verified, use the safest fallback, record the deviation, keep the Shortcut runnable | `WFSpeakTextWait` / `WFSpeakTextRate` / `WFSpeakTextPitch` / `WFSpeakTextLanguage` / `WFSpeakTextVoice` exist in the catalog but **no donor shows how Shortcuts serializes any of them**. Omit them; do not invent an encoding |
| C-2 | **Build provenance gate.** `git merge-base --is-ancestor 7ca8ebbfe467da38e594bdd41687c094a1f0c678 HEAD` must exit 0 before running either builder; abort otherwise | A `<precondition>` on the first build task. Measured 2026-08-18: **PASS** on the current HEAD |
| C-3 | **Two-gate validator rule.** Gate A `--target-macos 26 --target-platform all` is mandatory and must pass clean. Gate B `--target-macos 27 --target-platform all` is advisory, expects exit 1 with exactly one waived line per fork, and must **never** be chained into a definition of done | DIST-01's verification command is gate A only |
| C-4 | **Never** `--target-macos 26 --target-platform ios` | Rejects 3675 of 3675 actions |
| C-5 | **Nine parameter-defect axes.** Axes 1–7 device-established, axis 9 device-established, axis 8 structurally proven only | Axis 2 (`WFText` needs `WFTextTokenString`), axis 4 (required pickers — the inherited blocker), axis 5 (variable slots take the inverse envelope), axis 6 (numeric coercion; **booleans unaudited** — this is exactly the `voice_enabled` question) |
| C-6 | **Evidence hierarchy** and the four-rung **evidence ladder**. Never climb higher than the question requires; never skip a rung that would have caught a defect in the probe itself | The two open questions here are rung-2 (simulator) questions, not rung-3 device questions — see §Open Questions |
| C-7 | **Rung 2's ceiling.** A simulator pass may not raise a verdict on Notes, Apple Intelligence, Personal Automations, or brightness/volume | `speaktext` is none of those. A simulator probe **can** settle both open questions |
| C-8 | **`Show Alert` modals wedge a simulator run permanently.** Build simulator-bound probes with no blocking UI | A probe that reuses `mirror_and_voice()` verbatim will hang. Strip the alerts |
| C-9 | **Fix whole classes, never site-by-site** | Every `speaktext` change lands at 22 sites; every dispatch change lands at 11 renderings |
| C-10 | **Definition of done includes signing.** A valid XML draft without a signed `.shortcut` is not a stopping point; the signed filename must equal the display name (no `_signed` suffix) | `PROSOCHĒ — Nine Circles — Core` / `… — Aware` |
| C-11 | GSD workflow enforcement — file edits go through a GSD command | Structural, not phase-specific |

## Summary

Phase 15 is **materially smaller than its ROADMAP description**, and one of its dependencies
has already shipped. Phase 11 executed on 2026-08-18 and closed four of the phase's five
stated deliverables: the Circle-8 sequence entry was renamed `Voice` → `Loud Mirror` in all
three sequences, a real dispatch branch was emitted for it, `primitive_dispatch()` moved from
condition 99 ("contains") to condition 4 ("string is") per BD-06 Decision 5, and
`docs/sequence_dispatch_check.py`'s `KNOWN_ORPHANS` is now an **empty dict** with the checker
promoted from reporter to hard gate. `verify_dispatch_coverage()` is armed in both builders.
Circle 8 is therefore **already a live dispatch** — it is not silent, and the escalation
ladder does not go quiet. What remains is exactly one thing: the branch dispatches
`mirror_and_voice()`, the *same Python function* Circle 7's `Mirror` dispatches, which the
generator's own comment and `src/CONFIG-BLOCK.md` both label a deliberate interim to be
replaced here. That interim is what violates CIRC-14 (Circle 8 replays Circle 7 verbatim) and
what leaves CIRC-08's "The Voice" without an identity of its own.

Two inherited hazards dominate the risk, and both are on the exact code path this phase
rewrites. **First**, `voice_enabled` is written with two different JSON types by two different
writers: bootstrap emits the unquoted boolean `true`/`false` (traced to actions 66/67 →
`Voice Normalised` → the `state.json` template), while `Toggle Voice` emits the number `1`/`0`.
The gate CIRC-08 depends on is a numeric `> 0` comparison with a `WFNumberContentItem`
coercion, and `.claude/CLAUDE.md`'s own runtime-semantics table covers only `"null"` and `""`
— **boolean coercion is explicitly unaudited (axis 6)**. If `"true"` coerces to nothing, The
Voice is silent on every fresh install that answered `yes`, and CIRC-08 is unsatisfiable no
matter how well the primitive is written. **Second**, the Mirror primitive is the subject of
an open, device-reproduced `blocker` todo: `Test a Circle → the Circle mapped to Mirror`
fails with *"Please choose a value for each parameter in this action."* — an axis-4 unfilled
picker, reproduced three times across two independent installs, and proven to follow the
primitive rather than the Circle index. Because Circle 8 *is* the Mirror today, Circle 8
inherits that failure; whatever this phase ships at Circle 8 will not run on a phone until it
is fixed.

This research contributes a **new narrowing of that blocker** that costs nothing to act on.
Intersecting the three device-probed Circles against the generator's action inventory: Circle
1 (`knock` = comment + alert) fires; Circle 9 (`ice_start` = `read_value` / `config` / `math` /
`set_value` / `returntohomescreen`) fires; Circle 3 under `Classic` (`silence`) ran to
completion with **no error and no alert**, and `silence()` alerts *only* on its
capture-failure path — so the capture path succeeded and
`is.workflow.actions.getdevicedetails` with `WFDeviceDetail = "Current Volume"` and
`is.workflow.actions.setvolume` both executed cleanly. That demotes the todo's own "leading
suspect" (the 22 `getdevicedetails` sites) and leaves exactly **three** action identifiers
unique to `mirror_and_voice()`'s span: `is.workflow.actions.list`,
`is.workflow.actions.getitemfromlist`, and `is.workflow.actions.speaktext`. All three are
rung-2 questions — no Notes, no Apple Intelligence, no automations, no real hardware — so a
single alert-free simulator probe can discriminate them in one pass.

**Primary recommendation:** split `mirror_and_voice()` into `mirror()` (alert only) and
`voice()` (alert + speech, degrading to a Mirror-equivalent alert when `voice_enabled = 0`),
sharing `mirror_text()` and the 30 templates unchanged; **before** that, normalise
`voice_enabled` to the number `1`/`0` at every writer and bump `schema_version` 4→5; and land
an alert-free rung-2 probe that discriminates `list` / `getitemfromlist` / `speaktext` so the
Circle-8 branch this phase ships is one that can actually run.

## Architectural Responsibility Map

PROSOCHĒ has no network tiers. The meaningful tiers are the build pipeline's stages, and
mis-assigning a responsibility between them is this project's real analogue of putting auth
in the browser.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Circle 8's behaviour (what the user experiences) | **Generator** (`tools/build_state_engine.py`, the `voice()`/`mirror()` functions) | — | Behaviour is emitted actions; there is no runtime that could decide it |
| Which primitive Circle 8 names | **Config literal** (the `sequences` JSON inside `src/PROSOCHE-Dumb.xml`, mirrored in `src/CONFIG-BLOCK.md`) | Generator (must emit a matching branch) | BD-06 Decision 4 owns the slot table; the generator only supplies receivers |
| Name↔branch agreement | **Build guard** (`verify_dispatch_coverage()`) | Checker (`docs/sequence_dispatch_check.py`) | A Config entry with no receiver is invisible to the validator, the catalog and the decrypt — only a guard sees it |
| `voice_enabled` value and type | **State file** (`state.json`), written by bootstrap and by `Toggle Voice` | Generator (both writers are generated) | This is the tier the type split lives in, and why fixing it needs a schema bump, not just a code edit |
| "At most once per run" | **Run-scoped Shortcuts variable** (`Spoken This Run`) | Dispatch structure (exactly one branch per run) | Shortcuts variables do not persist across runs, which is precisely what makes this the right tier |
| "Never at unsafe levels" | **Absence of any volume write in the Voice path** | `SAFE-02` / `silence()`'s Media-only scoping | `speaktext` exposes no volume parameter — see §Pitfall 5 |
| Identifier / parameter-key legality | **Validator gate A** | ToolKit v63 snapshot | Structural only; it sees nothing about runtime behaviour |
| Does the action actually run on a phone | **Device (rung 3/4)** | Simulator (rung 2) for everything not on rung 2's ceiling list | The axis-4 blocker lives here and nowhere else |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `tools/build_state_engine.py` | in-repo, 5582 lines | The Core (Dumb) generator-patcher; owns `primitive_dispatch()`, `mirror_and_voice()`, `mirror_text()`, and all 20+ build guards | The only place a primitive can be defined `[VERIFIED: read in this session]` |
| `tools/build_sentient.py` | in-repo, 663 lines | Additive Aware (Sentient) fork; consumes `src/PROSOCHE-Dumb.xml`, re-runs 20 imported guards | SENT-15 — the Aware fork adds nothing to the deterministic engine, so a Circle-8 change flows through automatically `[VERIFIED: import list read]` |
| `is.workflow.actions.speaktext` | iOS 26 target | The Voice's only mechanism | Present in **all three** bundled ToolKit snapshots — v63 (the snapshot gate A consults at `--target-macos 26`), v78 macOS 27, and the v78 **iOS 27 Simulator** capture `[VERIFIED: toolkit-v63-tool-ids.json, toolkit-v78-ios27-tool-ids.json, queried this session]` |
| `validate-shortcut` | Playground 1.2.1 | Gate A, DIST-01 | `.claude/CLAUDE.md` §1 `[VERIFIED: binary present on PATH]` |
| `sign-shortcut` + `/usr/bin/shortcuts` | macOS built-in | DIST-02, C-10 | Signing is macOS-only; no substitute `[VERIFIED: both present]` |
| Python | 3.13.9 | Runs the generators and all twelve `docs/*_check.py` | Validator needs ≥3.10 (PEP 604) `[VERIFIED: python3 --version]` |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tools/plist_text_edit.py` | in-repo | Guarded round-trip text edit inside a `WFTextTokenString`, recomputing `attachmentsByRange` offsets | Required if the phase edits the live Config JSON literal or the `state.json` template — **never hand-edit either** `[VERIFIED: used by seed_* and by CONFIG-BLOCK.md's own changelog]` |
| `docs/sequence_dispatch_check.py` | in-repo, 296 lines | Orphan / unreachable / unknown / duplicate detection over the shipped Config vs. the shipped branches | Hard gate since Phase 11; `KNOWN_ORPHANS = {}` `[VERIFIED: read]` |
| `docs/phase5_self_check.py` | in-repo | Asserts the nine shipped primitive names and the three sequence names | Will fail if a branch is renamed without updating the Config `[VERIFIED: read, lines 22 / 78]` |
| `docs/phase7_self_check.py` | in-repo | Asserts ≥30 distinct Mirror templates (DUMB-02) | Constrains any refactor of `MIRROR_BASELINES` / `MIRROR_SUCCESSES` / `MIRROR_LAPSES` (10 each) `[VERIFIED: line 67, counts measured]` |
| `docs/router_ui_census.py` | in-repo | Counts user-facing surfaces per router arm; `speaktext` is in `COUNTED` | Its printed census moves when speech sites move; its **assertions** do not pin `speaktext`, only Notes/notification/menu counts `[VERIFIED: read lines 44–52, 190–225]` |
| `xcrun simctl` + iOS 26.5 runtime | Xcode on this Mac | Rung-2 probe execution | The only runtime that can answer this phase's two open questions without a device session `[VERIFIED: runtime present]` |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Splitting into `mirror()` + `voice()` | Give `mirror_and_voice()` a `mode` parameter | The ROADMAP offers both. **Prefer the split.** A mode flag keeps one function whose body is two interleaved behaviours behind conditionals a reader must simulate; the split makes the 7-vs-8 difference readable at the call site — which is exactly the property whose absence let `Voice` dispatch nothing for four phases. The split also keeps each function's rendered action count independently measurable |
| Reusing the 30 Mirror templates at Circle 8 | A separate escalated template set | **Reuse.** Canonical strategy §11 Primitive H is explicit: *"The Mirror becomes spoken once."* Distinct copy is a new product surface, is not requested by any requirement, and would put `docs/phase7_self_check.py`'s ≥30 assertion and DUMB-02/DUMB-03's fact-gating in play for no gain |
| Bumping `schema_version` 4→5 for the `voice_enabled` type fix | A dual-type read (accept both `true` and `1`) | **Bump.** BD-06-A3 and BD-06-A4 both record the developer's position that PROSOCHĒ has no installed base worth preserving, and BD-06-A3 explicitly rejected a dual-key alias for exactly the reason that applies here: it permanently encodes the inconsistency the fix exists to dissolve |
| Setting `WFSpeakTextWait` to make Circle 8 block until the utterance ends | Omit it | **Omit.** The parameter is real (catalog-confirmed) but **no donor shows how Shortcuts serializes a `speaktext` bool**, and this project has already been burned once by assuming a bool encoding (spike 005: the schema said `on`=1/`off`=2, Shortcuts writes a plain bool). C-1 applies. Record the deviation |

**Installation:** none. This phase adds no external dependency of any kind, in any ecosystem.

**Version verification:** not applicable — no package is installed. The only third-party
component is the already-installed Shortcuts Playground plugin v1.2.1.

## Package Legitimacy Audit

**Not applicable — this phase installs no external packages.** Every tool it uses is either
already in the repository (`tools/*.py`, `docs/*.py`), shipped with macOS (`shortcuts`, `aea`,
`aa`, `xcrun`), or part of the already-installed Shortcuts Playground plugin. There is no npm,
PyPI or crates surface to audit, and no `checkpoint:human-verify` install gate is required.

**Packages removed due to [SLOP] verdict:** none.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

```
                              ┌──────────────────────────────────────┐
   src/PROSOCHE-Dumb.xml ─────►│  tools/build_state_engine.py         │
   (previous build, parsed     │  main(): parse once, patch, verify,  │
    exactly once)              │  serialize once, write back to SAME  │
                              │  file  ← IN-PLACE, self-mutating      │
                              └───────────────┬──────────────────────┘
                                              │
        ┌─────────────────────────────────────┼──────────────────────────────┐
        │ replace_branch_body("--- OPEN STATE ENGINE ---", open_pipeline())   │
        │ insert_or_replace_after(MANUAL_MARKER, manual_emergency_restore())  │
        │ seed_*(actions)  ← edit the state.json TEMPLATE token in place      │
        └─────────────────────────────────────┬──────────────────────────────┘
                                              │
                                    primitive_dispatch()
                                    rendered ELEVEN times
                                              │
        ┌─────────────────────┬───────────────┴──────────────┬──────────────────┐
        │ OPEN arm ×2         │                              │ MANUAL arm ×9    │
        │ (Panic Escape on /  │                              │ (Test a Circle,  │
        │  Panic Escape off — │                              │  one per Circle) │
        │  MUTUALLY EXCLUSIVE)│                              │                  │
        └─────────────────────┴──────────────────────────────┴──────────────────┘
                                              │
                     read Config.sequences.<Sequence>.<Dispatch Circle>
                             → Get Text → "Selected Primitive"
                                              │
                     nine `if Selected Primitive is <name>` branches
                       (condition 4 = EXACT; never 99 = contains)
                                              │
     ┌──────┬──────┬──────┬──────┬──────┬──────┬────────┬────────────┬────────┐
     │Pause │Black │Silen │Inten │ Dim  │Eject │ Mirror │Loud Mirror │Frozen  │
     │knock │ ash  │silen │confe │dimmi │exile │mirror_ │  mirror_   │ice_    │
     │      │      │ce    │ssion │ng    │      │and_    │  and_voice │start   │
     │      │      │      │      │      │      │voice   │  ◄── THIS  │        │
     └──────┴──────┴──────┴──────┴──────┴──────┴────────┴─────┬──────┴────────┘
                                                              │ PHASE 15
                                                              ▼
                         ┌───────────────────────────────────────────────┐
                         │ voice()                                       │
                         │  mirror_text(baseline/success/lapse)          │
                         │      → is.workflow.actions.list               │
                         │      → getitemfromlist "Item At Index"        │
                         │        (WFItemIndex = Circle Next, coerced)   │
                         │  → alert("The Voice", Mirror Text)            │
                         │  → read_value("voice_enabled") → "> 0"        │
                         │       ├── true  → Spoken This Run has no value │
                         │       │            → speaktext(WFText=…)       │
                         │       │            → Spoken This Run = 1       │
                         │       └── false → D-15-A: alert only          │
                         └───────────────────────────────────────────────┘
                                              │
        ┌─────────────────────────────────────┴────────────────────────────────┐
        │ 20+ verify_*() build guards run AFTER every patch, before the write   │
        │  verify_dispatch_coverage · verify_required_pickers ·                 │
        │  verify_string_envelopes · verify_numeric_operands ·                  │
        │  verify_circle_zero_silence · verify_list_item_wrappers · …           │
        └─────────────────────────────────────┬────────────────────────────────┘
                                              │
   src/PROSOCHE-Dumb.xml (rewritten) ─────────┴──► tools/build_sentient.py
                                                    → src/PROSOCHE-Sentient.xml
                                                        (re-runs 20 imported guards)
                                              │
                          validate-shortcut --target-macos 26 --target-platform all
                                              │
                             sign-shortcut → artifacts/shortcuts/*.shortcut
                                              │
                              docs/manifest_check.py (decrypt + assert payload)
```

### Component Responsibilities

| File / symbol | Responsibility in this phase |
|---|---|
| `tools/build_state_engine.py:935 mirror_and_voice()` | The function to split. 32 actions per rendering; rendered **twice** per `primitive_dispatch()` (Mirror + Loud Mirror), ×11 renderings = **704 actions**, ~16% of the 4304-action Core artifact `[VERIFIED: measured this session]` |
| `tools/build_state_engine.py:917 mirror_text()` | Shared template selector. 3 actions per call, called 3× per Mirror rendering. **Both** new functions must keep using it — it is the only place the 30 templates are consumed |
| `tools/build_state_engine.py:975 primitive_dispatch()` | The name→function tuple at line 1016. The `("Loud Mirror", mirror_and_voice)` entry is the one line whose right-hand side changes |
| `tools/build_state_engine.py:1016` comment block above the tuple | **Must be updated in the same commit.** Plan 11-02's standing prohibition requires an interim to be named as interim in the generator's *own* comment text; leaving a comment that says "PHASE 15 replaces it" after Phase 15 has replaced it is a fresh instance of the same defect |
| `src/CONFIG-BLOCK.md:31` | Mirror doc of the live Config literal. Its second bullet says Circle 8 dispatches `mirror_and_voice()` and that Phase 15 replaces it — same update duty |
| `src/PROSOCHE-Dumb.xml` Config JSON literal | The **live** `sequences` arrays. `"Loud Mirror"` stays; the entry name does **not** change. If it ever did, it must go through `tools/plist_text_edit.py`, never a hand edit |
| `docs/sequence_dispatch_check.py` | Already a hard gate with `KNOWN_ORPHANS = {}`. **No exemption to remove — Phase 11 did that.** Must stay green |
| `docs/phase7_self_check.py:67` | ≥30 distinct Mirror templates. Constrains any template refactor |
| `docs/router_ui_census.py` | Prints `speaktext` counts per arm; assertions do not pin them |

### Recommended Structure

```
tools/build_state_engine.py
├── mirror_text(items, name)          # UNCHANGED — shared selector
├── _mirror_body()                    # NEW (optional): the three fact-gated
│                                     #   mirror_text() calls + the Previous
│                                     #   Respected If/Otherwise, returning
│                                     #   actions that leave "Mirror Text" set
├── mirror()                          # NEW: _mirror_body() + alert("Mirror", …)
│                                     #   NO speech. Circle 7 only.
└── voice()                           # NEW: _mirror_body() + alert(…) +
                                      #   voice_enabled gate + Spoken This Run
                                      #   gate + speaktext.  Circle 8 only.
```

Keeping `_mirror_body()` factored is what makes "sharing the template selector" (the
ROADMAP's own words) literal rather than aspirational, and it keeps the 30-template surface
single-sourced for DUMB-02/DUMB-03.

### Pattern 1: exactly one primitive executes per run — and this is structural, not lucky

**What:** `primitive_dispatch()` renders eleven times, but at most one rendering *executes*,
and within it at most one branch matches.

**Why it holds `[VERIFIED: tools/build_state_engine.py:1332, 1338, 2237 read this session]`:**

- The two OPEN-arm renderings (line 1332 inside the `Continue` menu case, line 1338 in the
  `otherwise` arm) are the two **mutually exclusive** arms of the
  `Panic Escape Enabled > 0` conditional. They cannot both run.
- The nine MANUAL-arm renderings are nine cases of one `choosefrommenu`; exactly one case
  runs per manual invocation, and the MANUAL arm is disjoint from the OPEN arm.
- Within a rendering, dispatch is condition **4** ("string is"), not 99 ("contains"), so
  `"Loud Mirror"` matches the Loud Mirror branch and *only* that branch. Under 99 it would
  also have fired `Mirror` — a silent double dispatch, and precisely why BD-06 Decision 5
  moved the code.

**Consequence, and it retires a ROADMAP warning:** the ROADMAP says *"if Circle 8 is reached
in a run where Mirror already spoke, the guard currently suppresses the second utterance."*
**That cannot happen.** Mirror and Loud Mirror are never both reached in one run. The
`Spoken This Run` guard is not an obstacle to Circle 8; it is CIRC-08's "at most once per
run" clause implemented correctly, and it should be **kept** in `voice()` as
defence-in-depth (Shortcuts variables are run-scoped, so it resets naturally every run).

### Pattern 2: the Mirror/Voice split, and what makes it an escalation

**What:** Circle 7 shows; Circle 8 speaks.

**Canonical grounding `[CITED: PROSOCHE_Nine_Circles_Canonical_Strategy.md]`:**

- §11 Primitive G — The Mirror: *"Show a precise behavioural reflection."*
- §11 Primitive H — The Voice: *"The Mirror becomes spoken once. Never shout. Never
  manipulate sound to unsafe levels."*
- §14.3 Circle VII: *"Full Contract Auditor / Mirror."*
- §14.4 Circle VIII: *"Full Mirror + Voice."*

Read together these give one unambiguous design: **the same reflection, escalated by being
spoken.** Not different words. Not more words. The escalation is the modality.

**Therefore:**

| | Circle 7 · Violence · `Mirror` | Circle 8 · Fraud · `Loud Mirror` |
|---|---|---|
| Template source | the 30 fact-gated templates | **the same 30** |
| Visual | `alert("Mirror", Mirror Text)` | `alert(…, Mirror Text)` |
| Speech | **none** | `speaktext(WFText = Mirror Text)` when enabled |
| `voice_enabled` role | irrelevant | the gate |

This is a **behaviour change at Circle 7**: today Circle 7 speaks whenever `voice_enabled`
is on. Removing that is what makes Circle 8 an escalation at all, and it is what satisfies
CIRC-14. It is also faithful to §11 — Primitive G's description contains no speech.

**Decision D-15-A (recommended, needs user confirmation).** When `voice_enabled = 0`,
Circle 8 **degrades to a Mirror-equivalent alert; it never skips.**

Rationale, in force order:

1. **Skipping recreates the exact defect this phase exists to close.** A Circle that renders
   the menu, takes `Continue`, and does nothing is the bug — the fact that the cause would be
   a user setting rather than a dispatch miss does not change what the user experiences.
2. `voice_enabled` is described to the user at import as *"May PROSOCHĒ speak to you at the
   highest circles?"* `[VERIFIED: WFWorkflowImportQuestions, read from src/PROSOCHE-Dumb.xml]`
   — that is consent to be **spoken to**, not consent to **have Circle 8**.
3. CIRC-14 permits a stronger Circle to differ from a weaker one; it does not permit a
   Circle to be empty.
4. Degrading costs nothing structurally: the alert is already emitted before the gate, so
   the `otherwise` arm is `is.workflow.actions.nothing` — literally the current shape.

**What D-15-A costs, stated honestly:** with voice off, Circles 7 and 8 become
indistinguishable to the user again — CIRC-14 is satisfied by construction but not
*experienced*. Making them differ with voice off would require new copy, which no
requirement asks for. Record the tradeoff; do not paper over it.

### Pattern 3: string envelope vs. variable slot, at the two positions this phase touches

**What:** axes 2 and 5 are inverses, and `voice()` sits at both positions in adjacent lines.

**Example `[VERIFIED: decrypted/parsed from src/PROSOCHE-Dumb.xml, action 1163 and 1160]`:**

```xml
<!-- STRING position: speaktext.WFText is catalog type `str` -> WFTextTokenString -->
<key>WFText</key>
<dict>
  <key>Value</key>
  <dict>
    <key>string</key><string>￼</string>
    <key>attachmentsByRange</key>
    <dict><key>{0, 1}</key>
      <dict><key>Type</key><string>Variable</string>
            <key>VariableName</key><string>Mirror Text</string></dict>
    </dict>
  </dict>
  <key>WFSerializationType</key><string>WFTextTokenString</string>
</dict>

<!-- VARIABLE SLOT position: conditional.WFInput.Variable -> bare WFTextTokenAttachment,
     plus the numeric coercion for a numeric condition code -->
<key>WFInput</key>
<dict>
  <key>Type</key><string>Variable</string>
  <key>Variable</key>
  <dict>
    <key>Value</key>
    <dict><key>Type</key><string>Variable</string>
          <key>VariableName</key><string>Voice Enabled</string>
          <key>Aggrandizements</key>
          <array><dict>
            <key>Type</key><string>WFCoercionVariableAggrandizement</string>
            <key>CoercionItemClass</key><string>WFNumberContentItem</string>
          </dict></array>
    </dict>
    <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
  </dict>
</dict>
```

**In practice the generator does both for you** — `STRING_ENVELOPE_PARAMS` already registers
`is.workflow.actions.speaktext: {"WFText"}` (line 2618) and `normalise_numeric_operands()`
attaches the coercion. New code must call `action(...)`, `if_block(...)` and `variable(...)`
and let the normalisation passes run. **Do not hand-write either envelope.**

### Anti-Patterns to Avoid

- **Hand-editing `src/PROSOCHE-Dumb.xml`.** `main()` parses once and serializes once,
  rewriting the same file. Any hand edit is either overwritten or corrupts
  `attachmentsByRange` offsets — which `VARIABLES.md` warns can crash Shortcuts on import.
  Use `tools/plist_text_edit.py`.
- **Editing `src/CONFIG-BLOCK.md` and thinking the Config changed.** It is a *mirror* of the
  live JSON literal, stated as such in its own changelog. `verify_dispatch_coverage()` reads
  the **literal**, not the mirror.
- **Adding an exemption to `KNOWN_ORPHANS`.** It is `{}` and the checker's own error text
  forbids re-populating it: *"do not add it to KNOWN_ORPHANS to…"*.
- **Introducing a second `speaktext` outside the Voice path.** `docs/router_ui_census.py`
  counts it as a user-facing surface, and `verify_circle_zero_silence()` forbids any surface
  reachable from a Circle-0 OPEN.
- **Reintroducing a combined sequence entry (`"Mirror+Voice"`).** BD-06 Decision 5 abolished
  them; `verify_dispatch_coverage()` splits on `+` unconditionally specifically so it
  **fails** on one rather than mis-parsing it.
- **Testing the new primitive by importing the whole 4300-action artifact into the
  simulator.** It is full of `Show Alert` modals, and per C-8 the first one wedges the run
  permanently. Probe with a purpose-built, alert-free shortcut.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Text-to-speech | Anything else | `is.workflow.actions.speaktext` | It is the only speech action on iOS Shortcuts, and it is already wired with the correct `WFText` key (DEV-03, BUILD-NOTES §13 correction) |
| "Speak at most once" | A `state.json` counter | The run-scoped Shortcuts variable `Spoken This Run` + condition 101 | Shortcuts variables reset every run by definition. A persisted counter would need clearing, and a clear that fails leaves the user permanently mute |
| Template selection | A new list/index construct in `voice()` | `mirror_text()` | 3 actions, already carries the `WFItemSpecifier="Item At Index"` literal (axis 4) and the `WFItems` row-wrapper discipline (axis 8) |
| Dispatch-name/branch agreement | A hand-written assertion or a MANIFEST count | `verify_dispatch_coverage()` | Already armed in both builders; resolves matching semantics **per branch** from that branch's own `WFCondition`, so it stays correct across a condition-code change |
| Number/string envelopes | Hand-written plist dicts | `action()`, `if_block()`, `variable()`, `text_token()` + the `normalise_*` passes | Axes 2/5/6 are inverses at adjacent positions; the passes are the only thing that has ever got all three right at 4300 sites |
| Checking what actually shipped | Trusting the unsigned XML plus an mtime | `aea decrypt` → `aa extract` → `plutil` (`.claude/CLAUDE.md` §8), or `docs/manifest_check.py` | The signed container is recoverable, and the project's own convention is to assert the payload rather than infer it |

**Key insight:** every defect this project has shipped was **systematic** — 147, 367, 25, 20
and 8 sites. The generator is not incidental scaffolding; it is the only mechanism that can
apply a fix at all 11 renderings and 22 speech sites at once. A one-site fix here is
guaranteed to be a partial fix.

## Runtime State Inventory

Phase 15 is a refactor **and** — if the recommended `voice_enabled` normalisation lands — a
state-shape change. This inventory is therefore required.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| **Stored data** | `state.json` key `voice_enabled`, currently written as JSON boolean `true`/`false` by bootstrap and as number `1`/`0` by `Toggle Voice`. Every existing install on the developer's device holds one of the two forms `[VERIFIED: template token + actions 66/67/69–73 parsed from src/PROSOCHE-Dumb.xml; device UAT 07-UAT.md Test 6]` | **Both**: a code edit (make bootstrap write `1`/`0`) **and** a data migration (existing files hold `true`). Precedent BD-06-A3 handles this by bumping `schema_version` so the old file fails the validity gate and is rebuilt — currently `4`, so `5`. There is **no** in-place migrator in this codebase and building one is not warranted |
| **Live service config** | **None.** PROSOCHĒ has no external service. The two Personal Automations are user-created on the device and reference the shortcut by *display name* only — a Circle-8 change does not touch them `[VERIFIED: ROOM-02/ROOM-03, and the automations were re-verified correct in the 2026-08-17/18 device session]` |
| **OS-registered state** | **None.** No Task Scheduler, launchd, pm2 or systemd surface exists — the product is a single Shortcut plus two Personal Automations. Confirmed by the absence of any such reference across `tools/`, `docs/` and `.claude/CLAUDE.md` | — |
| **Secrets / env vars** | **None.** DIST-08: core functionality has no external network dependency, and no secret, token or env var appears anywhere in the build or the artifact | — |
| **Build artifacts** | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` (SHA-256 `b07497ba…`, the hash the device UAT ran against) and `… — Aware.shortcut`; `src/PROSOCHE-Dumb.xml` and `src/PROSOCHE-Sentient.xml` are **rewritten in place** by the builders; `artifacts/shortcuts/MANIFEST.md` carries six hash/size rows asserted by `docs/manifest_check.py` `[VERIFIED: MANIFEST.md read]` | Rebuild both forks, re-sign both, add a new MANIFEST block with fresh hashes, and re-run `docs/manifest_check.py`. Per MANIFEST convention, a fork whose source is byte-identical is **not** re-signed — and that must be *measured* (`git status --short -- src/` empty after rebuild), not assumed |
| **Anything already installed on the phone** | The Core artifact currently on the device is `b07497ba…`. After this phase it is stale, and because `schema_version` bumps, the existing `state.json` becomes invalid and is rebuilt on first run | The device UAT instrument must re-install; any prior Circle-8 observation against `b07497ba…` does not carry forward |

## Common Pitfalls

### Pitfall 1: assuming the ROADMAP description still describes the code

**What goes wrong:** the plan re-does work Phase 11 already shipped, or worse, "restores" a
`KNOWN_ORPHAN_ENTRIES` exemption in order to remove it.

**Why it happens:** the ROADMAP entry and the todo
(`.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`) were both written
2026-08-16, **before** Phase 11 executed on 2026-08-18.

**Measured status of every ROADMAP deliverable** `[VERIFIED: source read this session]`:

| ROADMAP claim | Reality |
|---|---|
| `primitive_dispatch()` explicitly `continue`s past `Voice` | **False.** No `continue` exists; the tuple at line 1016 contains `("Loud Mirror", mirror_and_voice)` |
| dispatch comparison is condition 99 ("contains") | **False.** Condition 4, changed by plan 11-02 |
| the sequence entry is `"Voice"` | **False.** All three sequences carry `"Loud Mirror"` at Circle 8 |
| Voice renders 0 dispatch branches | **False.** It renders one branch per rendering, ×11 |
| `sequence_dispatch_check.py` reports the orphan and exits 0 | **False.** It is a hard gate; `KNOWN_ORPHANS = {}` |
| `Spoken This Run` suppresses Circle 8's utterance after Mirror spoke | **False.** Exactly one branch runs per run — see Pattern 1 |
| Circle 8 dispatches the Mirror as a deliberate interim | **True** — the one thing left to do |

**How to avoid:** treat `tools/build_state_engine.py:975–1024`, `src/CONFIG-BLOCK.md:31`, and
`docs/BUILD-NOTES.md` §34 as ground truth; treat the ROADMAP entry as a historical statement
of intent. The plan should say so explicitly so the verifier does not later read the ROADMAP
and mark the phase incomplete.

**Warning signs:** any task whose action text contains the string `"Voice"` as a sequence
entry name, or `KNOWN_ORPHAN_ENTRIES` (a symbol that does not exist — the real one is
`KNOWN_ORPHANS`).

### Pitfall 2: `voice_enabled` is written with two different JSON types — and this is the gate CIRC-08 hangs on

**What goes wrong:** The Voice never speaks on a fresh install that answered `yes`, and the
failure is completely silent — no error, no alert, the Circle simply shows its text.

**Why it happens `[VERIFIED: traced end-to-end this session]`:**

| Writer | What lands in `state.json` |
|---|---|
| Bootstrap (actions 66–73 → `Voice Normalised` → template token at action 75) | `"voice_enabled": true` — **unquoted JSON boolean** |
| `Toggle Voice` (line 2227) | `"voice_enabled": 1` — **JSON number**, via `number(1, …)` |

Both readers use `read_value()` (Get Dictionary Value → **Get Text** → Set Variable) and then
`if_block(name, 2, number=0)` — a `> 0` comparison whose operand carries
`WFCoercionVariableAggrandizement / WFNumberContentItem` (confirmed present in the shipped
artifact at actions 1160 and 1201). So the runtime question is: **what does the text `"true"`
coerce to under `WFNumberContentItem`?**

`.claude/CLAUDE.md`'s device-verified runtime-semantics table answers this for `"null"` and
`""` (both → false, no error) and says nothing about `"true"`. Axis 6 states the gap plainly:
*"Booleans, files, dictionaries and entity references are unaudited."*

**The one piece of device evidence is indirect and points the other way.** `07-UAT.md` Test 6
records that on a clean bootstrap (`Voice: Yes`, i.e. boolean `true`), the **first**
`Toggle Voice` wrote `voice_enabled: 0` — which requires its `Manual Voice > 0` test to have
evaluated **true**. That is consistent with `"true"` coercing to something positive. But it
is a single observation with a live alternative explanation (the state may not have been at a
pristine bootstrap), and the same test recorded a *confirmed* symptom of the type split:
Status degraded from `Voice: Yes` to `Voice: 1` after the first toggle, because the renderer
maps booleans to Yes/No and passes numbers through raw.

**How to avoid:**

1. **Normalise the writer.** Bootstrap should emit `1`/`0`, not `true`/`false` — replacing the
   two `gettext` actions at indices 66/67. One edit, both writers agree, the Status renderer
   stops degrading, and the `> 0` gate is fed a number by construction rather than by
   coercion. This also removes `voice_enabled` from axis 6's unaudited-boolean class entirely,
   which is strictly better than establishing what `"true"` coerces to.
2. **Bump `schema_version` 4 → 5** in the template *and* in the version-check literal, so an
   existing file carrying `true` fails the validity gate and is rebuilt. Precedent:
   BD-06-A3 (2→3) and its explicit rejection of a dual-key alias.
3. **Add a build guard** asserting the seeded `voice_enabled` is numeric and that every
   conditional reading it uses the `> 0` shape — sibling to `verify_state_seed()`.
4. Note that `panic_escape_enabled` is already seeded as the number `1` in the same template,
   so this makes the two flags consistent rather than inventing a new convention.

**Warning signs:** a `Test a Circle → Circle 8` run that shows the alert and stays silent
while Status reads `Voice: Yes`.

### Pitfall 3: treating the `Spoken This Run` guard as an obstacle

**What goes wrong:** the plan adds a reset, a second flag, or a "clear before Circle 8" step
to work around a suppression that cannot occur — adding actions at ×11 for nothing, and
weakening the guard that implements CIRC-08's "at most once per run".

**Why it happens:** the ROADMAP says the guard suppresses the second utterance. That was true
under condition 99, where `"Loud Mirror"` also matched the `Mirror` branch. Condition 4 (plan
11-02) removed the double dispatch.

**How to avoid:** keep the guard verbatim in `voice()`. Do not add a reset. Shortcuts
variables are run-scoped; `Spoken This Run` has no value at the start of every run by
construction, which is exactly the semantics CIRC-08 asks for.

### Pitfall 4: shipping a Circle 8 that cannot run, because the Mirror it is built on cannot run

**What goes wrong:** the phase completes, all guards are green, gate A passes, both forks
sign — and Circle 8 raises *"Please choose a value for each parameter in this action."* on
the first device run, exactly as Circle 7 does today.

**Why it happens:** the open `blocker` todo
`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md` records the axis-4
failure **reproduced three times across two independent installs**, and **proven to follow
the primitive rather than the Circle index** (switching `Classic`→`BlackMirror` moved the
failure from Circle 7 to Circle 4, the position BlackMirror maps to Mirror). Circle 8
currently *is* that primitive. Nothing in this phase's scope removes the defect; a naïve
split copies it into both halves.

**New narrowing this research contributes.** Intersect the device-probed Circles against the
generator's per-primitive action inventory:

| Circle probed (fresh install, `Classic`) | Primitive | Action identifiers exercised | Result |
|---|---|---|---|
| 1 · Limbo | `knock` | `comment`, `alert` | **fires** |
| 3 · Gluttony | `silence` | `getvalueforkey`, `gettext`, `setvariable`, `conditional`, `getdevicedetails` (`WFDeviceDetail = "Current Volume"`), `number`, `setvalueforkey`, `setvolume`, `nothing`, save chain | **ran to completion, no error, no alert** |
| 7 · Violence | `mirror_and_voice` | + `list`, `getitemfromlist`, `speaktext` | **FAILS** |
| 9 · Treachery | `ice_start` | `getvalueforkey`, `gettext`, `setvariable`, `math`, `setvalueforkey`, `returntohomescreen` | **fires** |

`silence()` emits an alert on **exactly one** path — its capture-failure `otherwise` arm
(*"Volume could not be captured, so nothing was changed."*). Circle 3 showing **no** alert
therefore means the capture path *succeeded*: `getdevicedetails` returned a positive reading
and `setvolume` applied. And the outer "already-outstanding" gate cannot have short-circuited
it on a fresh install, because the seed is `CLEARED_SENTINEL = "null"` and `.claude/CLAUDE.md`
records `"null"` coerced to `WFNumberContentItem` as **false**.

**Conclusion:** the todo's own "leading suspect" — the 22 `getdevicedetails` /
`WFDeviceDetail` sites — is **demoted**, and the offending action is one of the three
identifiers unique to `mirror_and_voice()`'s span:

1. `is.workflow.actions.list` — carries **no parameters at all** in the v78 catalog, so
   `WFItems` is uncatalogued; the axis-8 row-wrapper class lives here and is *structurally
   proven but never device-observed*
2. `is.workflow.actions.getitemfromlist` — `WFItemSpecifier` is the enum (`"Item At Index"`
   is a correct case id, catalog-confirmed) and `WFItemIndex` is a variable-fed `int`
3. `is.workflow.actions.speaktext` — reachable **only** when the `voice_enabled` gate passes,
   which couples this question to Pitfall 2

Confidence: **MEDIUM.** The device observations are rung-3/4; the intersection is rung-1
inference over them. It is a narrowing, not a finding, and it must not be fixed on alone —
`.claude/CLAUDE.md` is explicit: *"do not fix on this suspicion alone"* and *"Breadcrumb the
Mirror primitive."*

**How to avoid:** the plan must contain an explicit, early **discriminator task** — see
§Open Questions Q2 — and must not treat the Circle-8 split as verifiable on device until it
resolves. If the phase chooses not to own the fix (defensible: the todo is filed as its own
`blocker` and touches Circle 7 equally), the plan must say so **and** record that CIRC-08
remains device-unproven, rather than letting a green build imply otherwise.

**Warning signs:** a verification step that says "Circle 8 fires on device" with no
accompanying evidence that the Mirror picker defect was settled first.

### Pitfall 5: reading "never at unsafe levels" as something `speaktext` can enforce

**What goes wrong:** the plan adds a volume parameter to `speaktext`, or — far worse — adds a
`setvolume` before the utterance so the user can hear it.

**Why it happens:** CIRC-08 and canonical §11 Primitive H both say "never at unsafe levels",
which sounds like a parameter.

**The catalog is unambiguous `[VERIFIED: toolkit-v78-first-party-parameter-keys.json, queried
this session]`.** `is.workflow.actions.speaktext` has exactly six parameters —
`WFSpeakTextWait` (bool), `WFSpeakTextRate` (float), `WFSpeakTextPitch` (float),
`WFSpeakTextLanguage` (str), `WFSpeakTextVoice` (str), `WFText` (str) — all tagged available
on **both** `iOS 27 Simulator` and `macOS 27`. **There is no volume parameter.** Speech plays
at the device's current output level.

**How to avoid:** "never at unsafe levels" is satisfied by **not writing volume at all** in
the Voice path. That is SAFE-02 ("Volume is never increased and no startling output is
produced") and it is already how the artifact behaves — the only `setvolume` sites belong to
`silence()` and `restore_managed_settings()`, all Media-scoped (15 of 15 sites carry
`WFVolumeSetting = "Media"`, re-measured 2026-08-18).

**The real product consequence, which should be recorded rather than fixed:** because
`silence()` can leave Media volume at 10% and `settings_snapshot` persists until a CLOSE
restores it, a user can reach Circle 8 with the phone near-silent, and The Voice will be
inaudible. **PROSOCHĒ must not raise the volume to compensate** — that is exactly the
"startling output" SAFE-02 forbids. This is the strongest independent argument for D-15-A's
always-show-the-alert behaviour: the alert is the only channel guaranteed to reach the user.

### Pitfall 6: forgetting the ×11 multiplier and the second fork

**What goes wrong:** an innocuous-looking addition to `voice()` adds hundreds of actions, or
the Aware fork silently diverges.

**Measured `[VERIFIED: computed this session]`:** `mirror_and_voice()` = **32 actions**,
rendered twice per `primitive_dispatch()` (Mirror + Loud Mirror), and `primitive_dispatch()`
renders **eleven** times → **704 actions**, ~16% of the Core artifact's 4304. One `speaktext`
per rendering per branch gives the **22** sites present today. For scale: `knock()` = 2
actions, `silence()` = 24, `ice_start()` = 11, one whole `primitive_dispatch()` rendering =
229.

**How to avoid:** budget every added action as ×11 (×22 if it lands in both halves of the
split). Run `tools/build_sentient.py` after `tools/build_state_engine.py` in the same task —
it consumes the Core XML and re-runs 20 imported guards, so a Core change that breaks an
invariant surfaces there too.

### Pitfall 7: leaving a stale "this is an interim" comment behind

**What goes wrong:** the code ships the designed primitive while three separate documents
still tell a reader it is a placeholder Phase 15 will replace.

**Where the interim is currently declared `[VERIFIED: all three read]`:**
`tools/build_state_engine.py:994–998` (the comment above the dispatch tuple),
`src/CONFIG-BLOCK.md:31` (second bullet under the Config JSON literal heading), and
`docs/BUILD-NOTES.md` §34 (the "two interim stand-ins in force" record).

**How to avoid:** the plan must update all three in the same commit as the code. Plan 11-02's
standing prohibition — an interim must be named as interim in the generator's *own* comment
text — cuts both ways: when it stops being an interim, the comment must stop saying so. Note
that §34's *second* interim (`Eject` at Circle 6, owned by Phase 17) stays.

## Code Examples

### The current interim, verbatim — the code being replaced

```python
# tools/build_state_engine.py:935 — VERIFIED, read this session
def mirror_and_voice():
    baseline = mirror_templates(MIRROR_BASELINES)
    success  = mirror_templates(MIRROR_SUCCESSES)
    lapse    = mirror_templates(MIRROR_LAPSES)
    a = [comment("""Mirror selects from 30 fact-gated, local templates: ...""")]
    a += mirror_text(baseline, "Mirror Text")
    respected_g, respected_if = if_block("Previous Respected", 4, string="true")
    lapsed_g,    lapsed_if    = if_block("Previous Respected", 4, string="false")
    a += [respected_if] + mirror_text(success, "Mirror Text") + [otherwise(respected_g), lapsed_if]
    a += mirror_text(lapse, "Mirror Text") + [otherwise(lapsed_g),
          action("is.workflow.actions.nothing"), end_if(lapsed_g), end_if(respected_g),
          alert("Mirror", variable("Mirror Text"))]
    a += read_value("voice_enabled", variable("State"), "Voice Enabled")
    voice_g,  voice_if  = if_block("Voice Enabled", 2, number=0)
    spoken_g, spoken_if = if_block("Spoken This Run", 101)
    a += [voice_if, spoken_if,
          action("is.workflow.actions.speaktext", WFText=variable("Mirror Text"))]
    a += number(1, "Spoken This Run")
    a += [otherwise(spoken_g), action("is.workflow.actions.nothing"), end_if(spoken_g),
          otherwise(voice_g),  action("is.workflow.actions.nothing"), end_if(voice_g)]
    return a
```

Note the shape the split must preserve: `if_block` returns `(group, action)`, every block is
closed with an explicit `otherwise` + `is.workflow.actions.nothing` + `end_if`, and every
`GroupingIdentifier` is a fresh `uid()`.

### The dispatch tuple — the one line whose right-hand side changes

```python
# tools/build_state_engine.py:1015-1017 — VERIFIED
for name, implementation in (("Pause", knock), ("Black and White", ash), ("Silence", silence),
                             ("Intention", confession), ("Dim", dimming), ("Eject", exile),
                             ("Mirror", mirror_and_voice), ("Loud Mirror", mirror_and_voice),
                             ("Frozen", ice_start)):
    group, check = if_block("Selected Primitive", 4, string=name)   # 4 = "string is", never 99
    a += [comment(f"Dispatch {name} only when the selected Config entry names it exactly: ..."), check]
    a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
```

After the split: `("Mirror", mirror), ("Loud Mirror", voice)`.

### The `voice_enabled` seed chain — the source of the type split

```python
# Parsed from src/PROSOCHE-Dumb.xml — VERIFIED, actions 66-75
# 66  gettext  WFTextActionText = "true"
# 67  gettext  WFTextActionText = "false"
# 69  conditional  WFCondition 4, WFConditionalActionString "yes", input = Import Voice
# 70    setvariable  Voice Normalised = <66>       # the yes branch
# 72    setvariable  Voice Normalised = <67>       # the otherwise branch
# 75  gettext  the state.json template, containing:  "voice_enabled": ￼,
#             with attachment {105,1} -> Variable "Voice Normalised"
#
# -> a fresh install writes the UNQUOTED JSON BOOLEAN  true / false
#
# vs. tools/build_state_engine.py:2227 (Toggle Voice), which writes the NUMBER 1 / 0.
```

The recommended fix is two literals: `"true"` → `"1"`, `"false"` → `"0"`, plus the
`schema_version` bump. Both `gettext` actions are addressable by content, not index —
follow `seed_panic_escape()`'s pattern rather than hardcoding 66/67.

### The verified `speaktext` parameter set

```json
// toolkit-v78-first-party-parameter-keys.json -> tools["is.workflow.actions.speaktext"]
// VERIFIED: queried this session. platforms: ["iOS 27 Simulator", "macOS 27"]
// Also present in toolkit-v63-tool-ids.json — the snapshot gate A consults at --target-macos 26
{
  "displayName": "Speak Text",
  "parameters": [
    {"key": "WFSpeakTextWait",     "typePythonName": "bool",  "name": "Wait Until Finished"},
    {"key": "WFSpeakTextRate",     "typePythonName": "float", "name": "Rate"},
    {"key": "WFSpeakTextPitch",    "typePythonName": "float", "name": "Pitch"},
    {"key": "WFSpeakTextLanguage", "typePythonName": "str",   "name": "Language"},
    {"key": "WFSpeakTextVoice",    "typePythonName": "str",   "name": "Voice"},
    {"key": "WFText",              "typePythonName": "str",   "name": "Text"}
  ]
}
// NO volume parameter exists.  None of the six is flagged required.
// Emit WFText only; omit the other five (C-1 — no donor shows their serialization).
```

### The alert-free rung-2 discriminator probe (shape, not a finished file)

```
Probe: "Mirror Picker Discriminator"          # NO Show Alert anywhere — C-8
  [1] Number 8                        -> Set Variable "Circle Next"
  [2] List (10 rows, WFItems)         -> Get Item From List
        WFItemSpecifier "Item At Index"
        WFItemIndex = Circle Next  (WFNumberContentItem coercion)
                                      -> Set Variable "Mirror Text"
  [3] Speak Text  WFText = Mirror Text (WFTextTokenString envelope)
  [4] Return to Home Screen           # terminates without a modal

Run:  open -a Simulator
      xcrun simctl openurl <udid> "file:///abs/path/Probe.shortcut"
      # one synthesized tap on "Add Shortcut", then run it
Read: which action, if any, raises "Please choose a value for each parameter in this action."
```

Bisect by deleting `[3]`, then `[2]`, to isolate. Coordinates must be **fractions of the
device screen mapped through the window rect measured at run time**, never pixels
(`.claude/CLAUDE.md` §9). Instrument: `.planning/spikes/010-.../drafts/sim_input.py`.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Sequence entry `"Voice"`, no branch | Entry `"Loud Mirror"`, real branch | Phase 11 plan 11-02, 2026-08-17/18 | The ROADMAP's premise is stale — see Pitfall 1 |
| Dispatch condition 99 ("contains") | Condition **4** ("string is"), all 90 `Selected Primitive` conditionals | BD-06 Decision 5, plan 11-02 | Removes the double dispatch that made `Spoken This Run` a hazard |
| Combined entries `Ash+Confession`, `Silence+Mirror`, `Dimming+Mirror` | Abolished; every slot names exactly one primitive | BD-06 Decision 5 | `verify_dispatch_coverage()` splits on `+` specifically so it **fails** on a reintroduction |
| `sequence_dispatch_check.py` as a reporter (exit 0) with a `Voice` exemption | Hard gate, `KNOWN_ORPHANS = {}` | Phase 11 plan 11-02 (11-VALIDATION.md 11-02-T3) | Nothing to remove; keep it green |
| Circle names as intervention names | **Positional** Dante names (1 Limbo … 9 Treachery); the sequence table decides the intervention | BD-06 Decisions 1–2 | Circle 8 is "Fraud"; its intervention is `Loud Mirror` in all three sequences |
| `speaktext` "lists no parameters at all" (BUILD-NOTES §13) | Six parameters, `WFText` confirmed as the text key | DEV-03 / CAP-21, 2026-08-13 | The current 22 sites are already correct |
| Rung 2 cannot import a signed `.shortcut` (spike 007) | It **can**, via `open -a Simulator` + `xcrun simctl openurl file://…` + one tap | Spike 010, 2026-08-18 | This is what makes Q1 and Q2 rung-2 questions rather than device sessions |
| DIST-03 blocked (no device reachable) | **Lifted** — iPhone reachable via Mirroring, both automations verified | Device session 2026-08-17/18 | Device UAT is available for this phase if a rung-3 question genuinely remains |

**Deprecated / outdated in this repository:**

- `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` — steps 2 (partially),
  3 (entirely: combined entries are gone) and 5 (entirely: `verify_dispatch_coverage()` is
  built and armed) are **done**. Step 1 (decide the semantics) and the residue of step 2 are
  what remain. The todo should be rewritten or closed-with-carryover by this phase.
- `docs/BUILD-NOTES.md` §19.7 "The Circle 8 Voice orphan — a known open defect, reported not
  blocked" — describes a state that no longer exists.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Canonical §11 Primitive H + §14.4 mean *the same reflection, escalated by being spoken* — not different copy at Circle 8 | Pattern 2 | If the intent was distinct escalated copy, Circle 8 needs a new template set, DUMB-02/DUMB-03 come into play, and the phase roughly doubles. The canon text is quoted verbatim and reads unambiguously, but it is terse |
| A2 | D-15-A: `voice_enabled = 0` degrades Circle 8 to a Mirror-equivalent alert rather than skipping | Pattern 2 | This is the phase's one genuine product decision and the discuss phase was skipped. If the user wants skip-entirely, Circle 8 becomes silent for voice-off users — reintroducing the very symptom the phase closes. **Must be confirmed** |
| A3 | Removing speech from Circle 7 is desired, not a regression | Pattern 2 | Users on voice=on lose speech at Circle 7. It is what makes 8 an escalation and what satisfies CIRC-14, but it is a visible behaviour change |
| A4 | `schema_version` may be bumped 4→5 with no migrator, invalidating existing `state.json` | Pitfall 2, Runtime State Inventory | Precedent BD-06-A3/A4 rests on a recorded developer statement that PROSOCHĒ has no installed base worth preserving. If that has changed, a migrator is needed |
| A5 | The text `"true"` coerced to `WFNumberContentItem` may evaluate false | Pitfall 2 | If false, CIRC-08 is unsatisfiable on fresh installs today. If true, the normalisation is hygiene rather than a fix. **Either way the normalisation is correct** — which is why the recommendation does not depend on resolving A5 |
| A6 | Circle 3's silent, error-free device run means `silence()` executed its capture path | Pitfall 4 | If Circle 3 was actually a no-op, `getdevicedetails` is **not** exonerated and the axis-4 suspect list is wider. The `CLEARED_SENTINEL = "null"` chain makes the no-op reading unlikely but the UAT explicitly left it open |
| A7 | `is.workflow.actions.list` cannot be the axis-4 site because it has no picker | Pitfall 4 | The v78 catalog lists **zero** parameters for `list` — which is a catalog *gap* (it certainly takes `WFItems`), not proof of no picker. Do not let this shrink the probe below three legs |
| A8 | Omitting `WFSpeakTextWait` leaves Shortcuts' own default, which does not raise an unfilled-parameter error | Pitfall 5, Alternatives | It is omitted today at 22 sites and the shipped artifact validates and signs; whether the *runtime* accepts it is only established once speech is observed running. Setting it would require a donor for the bool encoding |
| A9 | Phase 14 (Ash) has not executed, so `ash()` is still alert-only and Circle 3-under-`Ambient` reasoning is unaffected | Pitfall 4 | `.planning/phases/14-*/` is empty. If 14 lands first, re-derive the Circle-3 exoneration against the new `ash()` |

## Open Questions (RESOLVED)

All five questions below were closed during planning by locked decisions D-04 and D-05 and by
the plan set that implements them. **The questions' original text is unmodified** — each
carries an appended `**RESOLVED**` bullet naming what closed it and where the closure lives, so
the record shows both what was open and what settled it. A question closed by a *decision* is
not the same as a question closed by *evidence*: Q2 and Q3 are closed as far as the phase's
scope goes, and the underlying device fact they concern stays open until plan 15-02 measures it.

1. **Does `voice_enabled = true` (JSON boolean, read through Get Text, coerced to
   `WFNumberContentItem`) satisfy `> 0`?**
   - *What we know:* the coercion aggrandizement is present in the shipped artifact;
     `"null"` and `""` are device-established as false; booleans are explicitly unaudited
     (axis 6); one indirect device observation (07-UAT Test 6) suggests it evaluates true.
   - *What's unclear:* the direct answer, and therefore whether The Voice is silent today on
     every fresh install.
   - *Recommendation:* **do not spend a device session on this.** Normalise the writer to
     `1`/`0` — that makes the question moot regardless of the answer, and is the smaller
     change. If the answer is wanted for the record, it is a **rung-2** question: a two-action
     probe (`Set Variable = "true"` → conditional `> 0` → `Return to Home Screen` vs. an
     ejecting alternative) settles it with no Notes, no AI, no automations and no hardware
     dependency.
   - **RESOLVED — by decision D-05, implemented in plan 15-03.** The recommendation was taken:
     `voice_enabled` is normalised to numeric `1`/`0` at *both* writers (bootstrap and Control
     Room `Toggle Voice`) with a `schema_version` bump 4 → 5, which makes the coercion question
     moot rather than answering it. **The underlying device fact — whether a JSON boolean
     coerced to `WFNumberContentItem` satisfies `> 0` — remains unmeasured and stays unaudited
     under nine-axes rule 6.** No device session was spent on it, by design.

2. **Which of `list` / `getitemfromlist` / `speaktext` carries the axis-4 unfilled picker?**
   - *What we know:* the failure is device-reproduced ×3 across 2 installs, follows the
     Mirror primitive rather than the Circle index, and this research narrows it to three
     identifiers by exonerating everything Circles 1/3/9 exercised.
   - *What's unclear:* which one — and, if it is `speaktext`, whether it is reachable at all
     (that depends on Q1).
   - *Recommendation:* a **rung-2** alert-free discriminator probe (§Code Examples). One
     simulator run. This is precisely the ladder rule: do not climb to a device session for a
     question rung 2 can answer, and do not hand the device a probe that fails for an
     unrelated reason.
   - *Scope note for the planner:* the fix itself may belong to the standalone `blocker`
     todo rather than to Phase 15. **The discrimination belongs here** — Phase 15 is
     rewriting the span, and doing it blind guarantees a rework.
   - **RESOLVED — by decision D-04, implemented in plan 15-02.** The recommendation was taken
     verbatim: plan 15-02 builds the alert-free three-leg discriminator (Task 1) and runs it on
     the simulator with a bisection (Task 2), at rung 2, with no device session. **This closes
     the question of *how* the answer is obtained, not the answer itself** — the verdict does
     not exist until 15-02 Task 2 runs, and `not discriminated at rung 2` is a first-class
     outcome of that run, enumerated in the plan's acceptance criteria alongside the three
     positive ones.

3. **Should the phase own the axis-4 fix, or discriminate and hand off?**
   - *What we know:* the defect affects Circle 7 equally; the todo is filed at `blocker`
     severity with its own solution plan; `.claude/CLAUDE.md` requires fixing whole classes.
   - *What's unclear:* whether the fix, once localised, is a one-line class fix (in which
     case owning it is cheap) or a `WFItems`/donor question (in which case it is its own
     phase).
   - *Recommendation:* structure the plan so the discriminator runs **early**, then branch:
     one-line class fix → absorb it; anything larger → record it and mark CIRC-08
     device-unproven rather than silently implying otherwise.
   - **RESOLVED — by D-04's two-branch routing rule, implemented in plan 15-02 Task 3.**
     Discriminate-and-branch was chosen over owning the fix unconditionally. Branch A absorbs a
     one-line class fix (a single missing required picker at a single emitter, applied
     everywhere by the generator's own construction, plus a `verify_required_pickers()`
     expectation so it cannot recur); Branch B records the narrowing into the blocker todo
     `.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md` and states in
     writing that **CIRC-08 remains device-unproven for Phase 15**. There is no third branch.
     Branch A is additionally gated on plan 15-01 being committed, because it edits
     `tools/build_state_engine.py`, which 15-01 owns.

4. **Does `Test a Circle` reach `voice()` with a usable `Circle Next`?**
   - *What we know:* line 2237 sets `Circle Next` from `Test Circle` before
     `primitive_dispatch("Test Circle")`, and `mirror_text()` indexes the 10-row lists with
     `WFItemIndex = Circle Next`. Circle 8 → index 8 of 10, in range.
   - *What's unclear:* nothing structurally — flagged only so the plan's verification uses
     `Test a Circle → Circle 8 · Fraud` as the harness rather than trying to accumulate real
     Pressure to Circle 8 (which STATE.md records as ~30 tests' worth of prerequisite work).
   - *Recommendation:* use the Test-a-Circle harness. It never writes Pressure (ROOM-12).
   - **RESOLVED — by the harness choice recorded in plan 15-05's UAT instrument.** The
     recommendation was taken: every Circle-8 and Circle-7 test in `15-UAT.md` is driven from
     `Test a Circle → Circle 8 · Fraud` and `Test a Circle → Circle 7 · Violence` rather than
     by accumulating real Pressure, which STATE.md prices at roughly thirty tests' worth of
     prerequisite work. No plan attempts the Pressure route.

5. **Should `docs/BUILD-NOTES.md` gain a new section for this phase's decisions?**
   - *What we know:* the project's convention is that a probe's result is *recorded, not
     consumed*, into BUILD-NOTES and CAPABILITY-DECISIONS.
   - *Recommendation:* yes — D-15-A, the Circle-7 speech removal, and the Q2 discriminator
     result all need a home. §19.7 and §34's first stand-in both need superseding notes.
   - **RESOLVED — yes; `docs/BUILD-NOTES.md` §36 is authored in plan 15-05 Task 2.** It carries
     D-01 through D-06, the declined alternatives, the omitted-`WFSpeakText*` deviation, the
     15-02 probe verdict *with its evidence rung*, and CIRC-08's device status. The two
     supersessions are split by ownership so one file's edits do not straddle two waves:
     §34's Circle-8 stand-in is discharged in plan 15-01 Task 3, and §19.7 is superseded in
     15-05 Task 2. §34's Circle-6 `Eject` subsection is left in force — that stand-in is
     Phase 17's.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | generators, twelve `docs/*_check.py`, validator | ✓ | 3.13.9 | — |
| `validate-shortcut` | DIST-01 gate A | ✓ | Playground 1.2.1 | — |
| `sign-shortcut` | DIST-02, C-10 | ✓ | Playground 1.2.1 | — |
| `/usr/bin/shortcuts` | the real signer | ✓ | macOS built-in | — |
| `aea` + `aa` | AEA1 decrypt, `docs/manifest_check.py` | ✓ | `/usr/bin` | — |
| Build provenance ancestor `7ca8ebb…` | C-2 | ✓ | `merge-base --is-ancestor` exits 0 | none — **abort the rebuild** if it ever fails |
| iOS Simulator runtime | rung-2 probe (Q1, Q2) | ✓ | iOS 26.5 (23F77) — inside the declared iOS 26.x target | Rung 3 device session via iPhone Mirroring (more costly) |
| `xcrun simctl` + `open -a Simulator` | probe import channel (spike 010) | ✓ | Xcode toolchain | Rung 3 |
| Real iPhone via Mirroring | rung-3/4 verification of Circle 8 firing | ⚠ on request | — | Record CIRC-08 as device-unproven; DIST-03 is lifted so this is *available*, not blocked |
| Apple Intelligence hardware | — | n/a | — | Not needed; Circle 8 is deterministic and the Aware fork adds nothing to it (SENT-15) |
| Network | — | not required | — | DIST-08: no external network dependency |

**Missing dependencies with no fallback:** none.

**Missing dependencies with fallback:** a live iPhone Mirroring session is not standing —
the user sets it up on request. Every question this research identifies is answerable at
rung 2, so the plan should reach rung 3 only for final CIRC-08 confirmation.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | **Build guards + standalone checker scripts.** No pytest/unittest exists and none should be added — the invariants are properties of a generated plist, and every guard already runs inside the build |
| Config file | none — each `docs/*_check.py` is an executable script with a `main()` and `require()`/`SystemExit` assertions |
| Quick run command | `python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py && python3 docs/state_engine_self_check.py` |
| Full suite command | `for f in state_engine_self_check phase5_self_check phase6_self_check phase7_self_check phase9_self_check sentient_audit_check sentient_core_check environmental_restore_check router_ui_census sequence_dispatch_check note_identity_check manifest_check; do python3 docs/$f.py \|\| echo "FAIL $f"; done` |
| Build-time guards | 20+ `verify_*()` in `tools/build_state_engine.py`, re-run by `tools/build_sentient.py` — these fail the *build*, not a test run |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CIRC-14 | Circle 7 and Circle 8 dispatch **different** implementations | structural | `python3 docs/sequence_dispatch_check.py` (name↔branch bijection) + a new assertion that the `Mirror` and `Loud Mirror` branch bodies are not action-equal | ⚠️ checker exists; **the "not identical" assertion is a Wave 0 gap** |
| CIRC-14 | The nine shipped names and three sequences are unchanged | structural | `python3 docs/phase5_self_check.py` | ✅ |
| CIRC-08 | Exactly one `speaktext` per Voice branch, none in the Mirror branch | structural | new guard: count `speaktext` per dispatch branch across all 11 renderings — expect 11 total (down from 22) | ❌ Wave 0 |
| CIRC-08 | `speaktext.WFText` carries the `WFTextTokenString` envelope | structural | `verify_string_envelopes()` (build guard, already registers `speaktext: {"WFText"}`) | ✅ |
| CIRC-08 | The speech is gated on `voice_enabled > 0` **and** `Spoken This Run` has no value | structural | new guard asserting both conditionals enclose every `speaktext` site (reuse `enclosing_groups()` / `gate_groups()` from `docs/router_ui_census.py`) | ❌ Wave 0 |
| CIRC-08 | `voice_enabled` is seeded numeric and every reader uses the `> 0` shape | structural | new guard sibling to `verify_state_seed()` | ❌ Wave 0 |
| CIRC-08 | "never at unsafe levels" — no volume write is reachable from the Voice path | structural | new guard: zero `setvolume` inside any `Loud Mirror` branch span | ❌ Wave 0 |
| CIRC-08 | Circle 8 actually speaks on a phone | manual-only | `Test a Circle → Circle 8 · Fraud` via iPhone Mirroring | ⚠️ device UAT — gated on Q2 |
| CIRC-09 | Circle 9 still dispatches `Frozen` in all three sequences, unchanged | structural | `python3 docs/phase5_self_check.py && python3 docs/sequence_dispatch_check.py` | ✅ |
| DIST-01 | Gate A passes clean on both forks | structural | `validate-shortcut src/PROSOCHE-Dumb.xml --target-macos 26 --target-platform all` and the same for `src/PROSOCHE-Sentient.xml`; both print `Validation passed.` and exit 0 | ✅ |
| — | Shipped payload matches the sources | structural | `python3 docs/manifest_check.py` (decrypt + assert), with `Loud Mirror` count re-derived | ⚠️ exists; expected counts move |
| — | No surface entered the Circle-0 silent band | structural | `verify_circle_zero_silence()` (build guard) + `python3 docs/router_ui_census.py` | ✅ |
| — | ≥30 distinct Mirror templates survive the split | structural | `python3 docs/phase7_self_check.py` | ✅ |

### Sampling Rate

- **Per task commit:** `python3 docs/sequence_dispatch_check.py && python3 docs/phase5_self_check.py`
  (< 5s; catches the dispatch-surface class, which is this phase's core risk)
- **Per wave merge:** rebuild both forks, then the twelve-checker full suite, then gate A on
  both forks
- **Phase gate:** full suite green + gate A clean on both forks + both forks signed + a new
  `MANIFEST.md` block with `docs/manifest_check.py` green, before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] Guard: `speaktext` appears **only** inside `Loud Mirror` branches, exactly once per
      rendering (11 total) — covers CIRC-08 and CIRC-14 simultaneously
- [ ] Guard: every `speaktext` site is enclosed by both the `Voice Enabled > 0` group and the
      `Spoken This Run` condition-101 group — covers CIRC-08's two clauses
- [ ] Guard: `voice_enabled` is seeded as a number, and every conditional reading it uses
      `WFCondition 2 / WFNumberValue 0` — covers Pitfall 2
- [ ] Guard: zero `setvolume` reachable inside a `Loud Mirror` branch span — covers "never at
      unsafe levels" / SAFE-02
- [ ] Assertion in `docs/sequence_dispatch_check.py` (or a sibling) that no two distinct
      sequence-entry names resolve to action-equal branch bodies — the general form of the
      CIRC-14 defect, and the one that would have caught this phase's own bug class
- [ ] The rung-2 discriminator probe for Q2, with its result recorded in
      `docs/BUILD-NOTES.md`

All five new guards belong in `tools/build_state_engine.py` beside the existing `verify_*()`
family and must be armed in `tools/build_sentient.py`'s import list, matching the established
pattern. Each must be demonstrated to **fail on a synthesised defect** — the project's own
standard (`verify_panic_escape_isolation()`, plan 11-10) is that a guard proven only in the
passing direction is not proven.

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1`.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | **no** | No accounts, no login, no credentials anywhere in the product |
| V3 Session Management | **no** (in the ASVS sense) | PROSOCHĒ's "session" is a behavioural app-usage interval in `state.json`, not an auth session. Its integrity is covered by SESS-03's newer-OPEN ownership check, not by ASVS V3 |
| V4 Access Control | **no** | Single-user, on-device, no privilege boundary. Every surface is reachable by the one user by design (EXIT-07) |
| V5 Input Validation | **yes** | The only input this phase reads is `state.json`'s `voice_enabled`. Control: type-normalise at the writer (`1`/`0`) and gate numerically at the reader — which is exactly Pitfall 2's fix. Corrupt/unparseable state is already handled by BOOT-07's recovery path |
| V6 Cryptography | **no** | No crypto in the product. Artifact signing uses Apple's `shortcuts sign`; the AEA1 container is Apple's. Nothing is hand-rolled |
| V7 Error Handling & Logging | **partial** | Shortcuts has no try/catch, so the project's control is **ordering, not detection**. Relevant here: the `speaktext` failure mode is a modal error attributed to the outermost caller, never naming the action |
| V12 Files & Resources | **no change** | This phase adds no file read or write |
| V14 Configuration | **yes** | `schema_version` is the configuration-integrity control. Bumping it (Pitfall 2) is what prevents a stale-typed `state.json` from being silently accepted |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A sequence entry that names no branch — the Circle does nothing, silently | **Denial of Service** (of the product's own function) | `verify_dispatch_coverage()` + `docs/sequence_dispatch_check.py` as a hard gate. Already armed |
| Two entries resolving to the same behaviour, so an escalation is not one | Denial of Service | The proposed "no two entries are action-equal" assertion (Wave 0) |
| A type-confused state flag silently disabling a safety-or-consent gate | **Tampering** / Information Disclosure (of the consent boundary) | Normalise `voice_enabled` at the writer; bump `schema_version`; guard the read shape |
| Speech emitted when the user withheld consent | **Repudiation** of a consent boundary | The `voice_enabled > 0` gate must enclose **every** `speaktext` site — asserted by a guard, never by inspection |
| Startling audio output | Denial of Service / user harm | SAFE-02. `speaktext` exposes no volume parameter; the control is that the Voice path writes no volume at all |
| An unbuilt artifact shipped from an unknown ancestor | **Spoofing** of build provenance | C-2's `git merge-base --is-ancestor` precondition, which **aborts** rather than warns |
| A signed container that does not match the source it claims | Spoofing / Tampering | `docs/manifest_check.py` decrypts and asserts the payload; MANIFEST's own convention requires "no hash moved" to be measured, not assumed |

## Sources

### Primary (HIGH confidence)

- `tools/build_state_engine.py` — read in full at lines 185–450, 900–1080, 1273–1345,
  1871–2100, 2181–2270, 2540–2680, 4780–4880, 5480–5582; `mirror_and_voice()` /
  `primitive_dispatch()` / `silence()` / `knock()` / `ash()` / `ice_start()` executed to
  measure action counts
- `tools/build_sentient.py` — import list and header, lines 1–70
- `src/PROSOCHE-Dumb.xml` — parsed with `plistlib`; actions 0–75 dumped, `speaktext` and
  `voice_enabled` conditional sites located, `WFWorkflowImportQuestions` read
- `src/PROSOCHE-Sentient.xml` — action and `speaktext` counts
- `docs/sequence_dispatch_check.py`, `docs/phase5_self_check.py`, `docs/phase7_self_check.py`,
  `docs/router_ui_census.py`, `docs/environmental_restore_check.py`
- `src/CONFIG-BLOCK.md` — the three `sequences` arrays and the Phase 11 changelog entry
- `docs/CAPABILITY-DECISIONS.md` — BD-06 Decisions 1–5, the slot table, BD-06-A1/A3/A4
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` — §7.1 (import questions), §11 Primitives G/H/I,
  §14.3/§14.4 (Circle VII/VIII)
- `PROSOCHE_Build_Addendum_01.md` — §5 Fraud → Loud Mirror
- ToolKit snapshots, queried directly with Python:
  `toolkit-v78-first-party-parameter-keys.json` (`speaktext`, `list`, `getitemfromlist`,
  `alert`), `toolkit-v78-first-party-enum-cases.json` (`getitemfromlist_wfitem_specifier`),
  `toolkit-v63-tool-ids.json`, `toolkit-v78-ios27-tool-ids.json`
- `.claude/CLAUDE.md` — §1 (two-gate rule), §3 items 11/15, §4, §5, §8, §9 (evidence ladder,
  rung-2 ceiling, spike 010's import channel), Conventions (nine axes, runtime semantics,
  evidence hierarchy)
- `.claude/skills/spike-findings-prosoche/` — SKILL.md and `references/authoring-parameters.md`
  (three-class rule, donor-confirmed literals, the seven axes)
- Environment probes run this session: `python3 --version`, `command -v` for
  `validate-shortcut` / `sign-shortcut` / `shortcuts` / `aea` / `aa`,
  `xcrun simctl list devices`, `git merge-base --is-ancestor`

### Secondary (MEDIUM confidence)

- `.planning/phases/07-control-room-dumb-freeze/07-UAT.md` Tests 5, 6, 7, 7b, 7c — the device
  observations this research intersects. Device evidence is rung 3/4 (HIGH); the
  **intersection** drawn from it in Pitfall 4 is rung-1 inference (MEDIUM)
- `.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md` — the axis-4 blocker
- `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md` — largely superseded
- `.planning/STATE.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`
- `.planning/phases/11-*/11-VALIDATION.md` — the validation-architecture pattern reused here
- `artifacts/shortcuts/MANIFEST.md`, `docs/BUILD-NOTES.md` §13, §19.7, §22, §34, CAP-21

### Tertiary (LOW confidence)

- None. No WebSearch was performed: every question this phase raises is answerable from the
  repository, the bundled ToolKit snapshots, or the project's own device records, and the
  project's evidence hierarchy ranks all three above general web sources.

## Metadata

**Confidence breakdown:**

- **Standard stack: HIGH** — every identifier and parameter key was queried directly from the
  bundled ToolKit snapshots this session, and every generator symbol was read in source. No
  package is installed, so there is no registry risk.
- **Architecture: HIGH** — the ×11 rendering count, the mutual exclusivity of the two OPEN-arm
  dispatch sites, the 32-action size of `mirror_and_voice()`, and the 22 `speaktext` sites are
  all **measured**, not inferred.
- **Pitfalls 1, 3, 5, 6, 7: HIGH** — each rests on source read this session plus catalog
  queries.
- **Pitfall 2 (`voice_enabled` typing): HIGH on the defect, MEDIUM on the consequence** — the
  two-writer type split is traced end-to-end through the shipped artifact. What `"true"`
  coerces to is genuinely open (A5), which is why the recommendation is framed so it does not
  depend on the answer.
- **Pitfall 4 (axis-4 narrowing): MEDIUM** — a sound intersection over rung-3 device
  observations, with one soft link (A6) explicitly acknowledged. Actionable as a probe
  target; **not** actionable as a fix.
- **Product decision D-15-A: MEDIUM** — well-grounded in canon and in the requirement set, but
  the discuss phase was skipped and it is a real product choice (A2).

**Research date:** 2026-08-18
**Valid until:** 2026-09-17 (30 days) for the catalog and toolchain facts, which are stable.
**Re-derive sooner if** Phase 14 executes (changes `ash()`, and with it the Circle-3 reasoning
in Pitfall 4), if the axis-4 blocker todo is closed by other work, or if any device session
adds an observation to `07-UAT.md` Test 7.
