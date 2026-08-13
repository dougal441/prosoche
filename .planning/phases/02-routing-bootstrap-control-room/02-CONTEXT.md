# Phase 2: Routing, Bootstrap & Control Room Onboarding - Context

**Gathered:** 2026-08-13
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

A user can import the Shortcut, run it manually for the first time, and get a working `state.json` plus a fully instructive Control Room Note — and every subsequent invocation routes correctly and never corrupts or duplicates that foundation.

## CRITICAL — This is a Shortcuts project, not a conventional codebase

The deliverable is iOS Shortcuts plist XML. There is no npm, no test runner, no server, no application framework. **This is the phase where the first plist XML is authored.**

**Build toolchain — Shortcuts Playground plugin v1.2.1:**
`/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/`

- Reference docs: `skills/shortcuts-playground/*.md` — read `SKILL.md`, `PLIST_FORMAT.md`, `CONTROL_FLOW.md`, `VARIABLES.md`, `BEST_PRACTICES.md`, `PARAMETER_TYPES.md`, `DATE_TIME.md`, `AUTOMATION_TRIGGERS.md` before authoring
- ToolKit snapshots: `skills/shortcuts-playground/data/`
- Golden reference shortcuts: `skills/shortcuts-playground/golden-shortcuts/` — 19 working examples; imitate their structure
- Validator: `bin/validate-shortcut <file.xml> --target-macos 26 --target-platform ios`
- Signer: `bin/sign-shortcut <file.xml> --name "<name>"`

**Load `Skill(skill="shortcuts-playground:shortcuts-playground")` before authoring plist.** For substantial authoring work, the `shortcuts-playground:shortcut-builder` agent is the purpose-built specialist and handles validation/signing internally.

## Phase 1 outputs are binding inputs — read them first

- `docs/BUILD-NOTES.md` — 36 audited capabilities. **Every action identifier and parameter key you use must come from this table.** It also carries the do-not-fabricate protocol (§2), the evidence protocol (§3), the deviation log (§5), and user action items (§6).
- `docs/CAPABILITY-DECISIONS.md` — BD-01…BD-05. BD-05 authorises building the Control Room on the Notes actions now, gated by UA-01 (on-device confirmation), with a named file-based fallback.
- `src/CONFIG-BLOCK.md` — the config JSON to transcribe into the graph, plus a documented Text → Detect Dictionary → Get Dictionary Value transcription recipe and its two coercion hazards.

## Source file convention

Author the unsigned plist XML at `src/PROSOCHE-Dumb.xml`. This single file grows through Phases 2–7 and is forked to `src/PROSOCHE-Sentient.xml` in Phase 8. Keep it validating at every commit — a phase that leaves the XML invalid blocks every later phase.

</domain>

<decisions>
## Implementation Decisions

### Locked — from the canonical strategy and Phase 1

- **Monolithic graph.** One shortcut per fork. No internal `Run Shortcut` hops (research: added latency and lossy serialization for zero isolation benefit). The only `Run Shortcut` call is the mandatory one from each Personal Automation into this Shortcut.
- **Nested `If`/`Otherwise` only.** `Otherwise If` is macOS-27+ and unusable on the iOS 26 target. This applies to the router and to every later Circle lookup.
- **Three invocation modes** distinguished by Shortcut Input: absent/empty → MANUAL; `OPEN`; `CLOSE`. Unrecognised input must fail safe.
- **Timestamps** are integer Unix epoch seconds (UTC). `behavioural_day` is an ISO date-key string. Use the Date(1970 anchor) → `Get Time Between Dates` pattern from `DATE_TIME.md`.
- **One JSON state file, one Apple Note.** No CSV, no second machine store.
- **State is bounded and versioned** — rolling windows for sessions, contracts, and per-exit aggregates. No unbounded arrays.
- **PROSOCHĒ is bypassable** and the Note must say so plainly.

### Known authoring hazards — treat as hard rules, they are silent failures

From `.planning/research/PITFALLS.md` and `docs/BUILD-NOTES.md`:

1. **`markdownContents` vs `markdown`** on Note creation — the wrong key produces an **empty Control Room Note body**. Since the Note is the only onboarding path, this would silently break the entire product. Verify the created Note has a non-empty body.
2. **`WFTextTokenAttachment` on display strings** renders blank at runtime while the plist still validates. Every user-facing message is at risk.
3. **GroupingIdentifier collisions** in nested If/Repeat/Menu blocks — the most common real-world authoring mistake, and this graph is deeply nested by construction.
4. **Dictionary type coercion** — booleans coerce to 1/0, null coerces to empty, and reads on a null parent break. Route values through Text where the recipe in `src/CONFIG-BLOCK.md` says to.
5. **The validator can pass a broken shortcut.** Validation is necessary, not sufficient. Reason through the variable wiring manually.

### Claude's discretion

Action-graph layout, comment discipline, variable naming, how the config block is embedded, and how the Note body is assembled are at Claude's discretion — subject to the hazards above.

</decisions>

<code_context>
## Existing Code Insights

The repository contains `docs/BUILD-NOTES.md`, `docs/CAPABILITY-DECISIONS.md`, `src/CONFIG-BLOCK.md`, the canonical strategy, and `.planning/`. **No plist XML exists yet — this phase creates the first.**

Relevant verified capabilities from `docs/BUILD-NOTES.md` (use the table for exact parameter shapes):
- CAP-02 Get File, CAP-03 Save File with overwrite — plus DEV-02, which records that no file-existence-check action exists; the substitute is Get File with `WFFileErrorIfNotFound` off, piped through Detect Dictionary
- CAP-04 Dictionary / Detect Dictionary, CAP-05 Get/Set Dictionary Value
- CAP-07 Find Notes, CAP-08 Create Note, CAP-09 Append to Note, CAP-10 Open Note
- CAP-11 Ask for Input, CAP-12 Choose from Menu/List
- CAP-S01 Set/Get Variable, CAP-S02 Text, CAP-S04 If/Otherwise/End If, CAP-S07 Show Alert/Result/Notification

</code_context>

<specifics>
## Specific Ideas

### The Control Room Note body (canonical §17, §18) — required sections

- `# PROSOCHĒ — CONTROL ROOM`
- `## READ THIS FIRST` — what PROSOCHĒ is; that it is bypassable and cannot install its own automations
- **Automation A — OPEN**: Trigger: App → select target apps → `Is Opened` → run automatically → Run Shortcut `PROSOCHĒ — Nine Circles` → pass input `OPEN`
- **Automation B — CLOSE**: same target apps → `Is Closed` → run automatically → Run Shortcut → pass input `CLOSE`
- Safety warning: do not target Phone, Maps, Wallet, authenticators, password managers, or other essential apps
- `## MY PHONE, ON PURPOSE` — the editable proforma with all six prompts from §7.2 (what is my phone genuinely for; which apps take more attention than I intend; what do I want the reclaimed attention for; when PROSOCHĒ stops an automatic open what would I rather do; what does deliberate leisure look like for me; optional sentence to my future self)
- `## CURRENT SETTINGS` — fork, profile, sequence, voice, AI, enabled exits
- `## CURRENT STATE` — human-readable snapshot placeholder (populated in Phase 7)
- `## ATTENTION LEDGER` — readable event log (entries begin in later phases)
- `## VALUE / LIFE RETURNED` — reserved
- `## SUPPORT PROSOCHĒ` — reserved

Tone: calm, clean, unsentimental. No emoji, no exclamation marks.

### Import questions (canonical §7.1, `WFWorkflowImportQuestions`)

- Choose your descent: Paradise / Limbo / Inferno — default **Limbo**
- May PROSOCHĒ speak to you at the highest circles? yes/no
- (Sentient fork only, Phase 8) Use on-device intelligence? yes/no

`.planning/research/STACK.md` records the recovered `WFWorkflowImportQuestions` schema, reconstructed from populated instances in the golden-shortcut corpus.

### First-run bootstrap sequence (canonical §18)

1. Check for existing state; if present, do not re-bootstrap
2. Create the PROSOCHĒ directory in the Shortcuts-accessible file location
3. Create `state.json` seeded from the import-question answers and the config block
4. Create the Control Room Note with the full body above
5. Show/open the Control Room Note

### Self-healing requirements

- Missing `state.json` → bootstrap, from **any** invocation mode including OPEN and CLOSE
- Corrupt/unparseable `state.json` → safe recovery, not failure and not silent wrong behaviour
- Deleted Control Room Note → detected and recreated without crashing the run
- Later manual runs → never overwrite state, never create a second Note

### Definition of done for this phase

`src/PROSOCHE-Dumb.xml` exists, passes `validate-shortcut --target-macos 26 --target-platform ios`, and contains the router, the bootstrap, the embedded config, and the full Control Room Note body.

</specifics>

<deferred>
## Deferred Ideas

- Heat / Gravity / Pressure arithmetic and Circle mapping — Phase 3
- CLOSE session measurement and the race protocol — Phase 4
- The nine primitives — Phase 5
- Exits, exit learning, contracts — Phase 6
- The manual Control Room menu, the dynamic state snapshot, the Attention Ledger writer, and the Mirror templates — Phase 7
- Signing and on-device import testing — Phase 7 (Dumb) and Phase 8 (both forks)
- Anything Sentient or `Use Model` — Phase 8, gated by UA-02

</deferred>
