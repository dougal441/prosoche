# Phase 1: Capability Audit & Config Foundation - Context

**Gathered:** 2026-08-13
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Every iOS action PROSOCHĒ depends on is resolved to VERIFIED / UNVERIFIED / NOT AVAILABLE with its exact identifier and parameter shape before any behavioural logic is authored, and the tunable static config exists as a single editable block.

## CRITICAL — This is a Shortcuts project, not a conventional codebase

There is no npm, no test runner, no server, no application framework. The deliverable of this project is two signed iOS `.shortcut` files plus their unsigned `.xml` plist source.

**Build toolchain — Shortcuts Playground plugin v1.2.1, installed at:**
`/Users/dougalhanson/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/`

- Reference docs: `skills/shortcuts-playground/*.md` — `SKILL.md`, `BEST_PRACTICES.md`, `ACTIONS.md`, `APPINTENTS.md`, `PLIST_FORMAT.md`, `VARIABLES.md`, `CONTROL_FLOW.md`, `DATE_TIME.md`, `PARAMETER_TYPES.md`, `AUTOMATION_TRIGGERS.md`, `TOOLKIT_SNAPSHOT.md`, `EXAMPLES.md`
- ToolKit identifier/parameter/enum snapshots: `skills/shortcuts-playground/data/`
- Golden reference shortcuts: `skills/shortcuts-playground/golden-shortcuts/`
- Validator: `bin/validate-shortcut <file.xml> --target-macos 26 --target-platform ios`
- Signer: `bin/sign-shortcut <file.xml> --name "<Shortcut Name>"`
- Self-test: `bin/shortcuts-playground-selftest`

**The `shortcuts-playground` skill and the `shortcut-builder` / `shortcut-remixer` agents are the correct tools for authoring plist XML.** Load the skill (`Skill(skill="shortcuts-playground:shortcuts-playground")`) rather than guessing plist structure.

**Target:** iOS 26.x. `Otherwise If` is macOS-27+ only — use nested `If`/`Otherwise` everywhere.

## What this phase produces

Documentation and a config block — **not** a working Shortcut. This phase is deliberately investigative. Its output is:

1. `docs/BUILD-NOTES.md` — the capability audit table and the deviation log (living document, appended to by every later phase).
2. A concrete decision for each of the four known blockers.
3. `src/config-block.md` (or equivalent) — the single editable tuning block specifying profile threshold tables, sequence orderings, Ice cooldown durations, Heat coefficients, and the exploration rate, in a form that can be transcribed directly into a Shortcuts dictionary in Phase 2.

Prefer plain repository files (`docs/`, `src/`) at the project root. Do not create an app scaffold, package manifest, or test harness.

</domain>

<decisions>
## Implementation Decisions

### Locked by the canonical strategy — do not revisit

- Target iOS 26.x, native Shortcuts only. No companion app, no Screen Time blocking APIs, no private APIs.
- One JSON machine-state file plus one Apple Note. **No CSV. No second machine store.**
- Sentient uses the Apple **On-Device** model only. Never Private Cloud Compute, never ChatGPT, never a web API.
- The model never controls arithmetic, thresholds, timers, exit selection, or Circle IX.
- No Focus modes, no NFC, no remote A/B infrastructure.
- PROSOCHĒ is bypassable and must never claim otherwise.

### The "do not fabricate" protocol — binding for this phase and all later phases

From canonical strategy §31: *"Do not fabricate an action because the strategy requests it."*

When an action cannot be verified in the Playground ToolKit snapshots:
1. Use the safest fallback.
2. Record the deviation in `docs/BUILD-NOTES.md` with what was wanted, what was verified, and what was substituted.
3. Keep the Shortcut runnable.

A capability marked UNVERIFIED is a correct and expected research outcome. An invented action identifier is a defect.

### The four known blockers — resolve each to a decision

Prior research (`.planning/research/STACK.md`, `PITFALLS.md`, `ARCHITECTURE.md`) converged on four blockers. Each needs an explicit recorded decision, not a deferral:

1. **Grayscale / Color Filters** — absent from the bundled ToolKit catalogs entirely. Decide the Ash primitive's fate: substitute a different visual-salience reduction, require user opt-in to a PROSOCHĒ-managed configuration, or degrade Ash to a non-environmental variant. Record the decision and its rationale.
2. **Brightness read-back** — only the write action appears to exist. Since §21 forbids any stateful change that cannot be restored, decide Dimming's degraded form. Check whether `Get Device Details` exposes a usable brightness property before concluding.
3. **Volume read-back** — same treatment for Silence.
4. **`Use Model` On-Device literal** — the exact plist key/enum that pins On-Device is unknown. Attempt recovery from the ToolKit enum snapshots first. If it cannot be recovered from the local toolchain, record it as an explicit **user action item** (select On-Device in Shortcuts.app, export the unsigned XML, read the literal back) and state plainly how Phase 8 is gated on it. Do NOT guess an enum string.

Also confirm the Notes actions (Create Note, Append to Note, find/show a Note) resolve for the iOS target — the bundled catalog tags them macOS-only, which is likely a snapshot gap, but the whole Control Room onboarding depends on them.

### Claude's discretion

File layout, the exact shape of the build-notes table, and how the config block is expressed are at Claude's discretion. Keep both human-readable and directly transcribable into plist.

</decisions>

<code_context>
## Existing Code Insights

The repository currently contains only `PROSOCHE_Nine_Circles_Canonical_Strategy.md` and `.planning/`. This phase creates the first `docs/` and `src/` content.

Prior research to read before planning:
- `.planning/research/STACK.md` — capability audit table, exact validator/signer invocations, recovered `WFWorkflowImportQuestions` schema
- `.planning/research/ARCHITECTURE.md` — complete proposed JSON state schema, routing design, race protocol
- `.planning/research/PITFALLS.md` — the "do not fabricate" protocol, validator false-passes, authoring hazards
- `.planning/research/SUMMARY.md` — consolidated blockers and phase rationale
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` §5, §10-§12, §21, §22, §31

</code_context>

<specifics>
## Specific Ideas

### Config block must cover, at minimum

- **Profile threshold tables** (Pressure → Circle), from §10.5:
  - Paradise: 1, 4, 7, 10, 13, 16, 19, 22, 25
  - Limbo (default): 1, 3, 5, 7, 9, 11, 14, 17, 20
  - Inferno: 1, 2, 4, 6, 8, 10, 12, 14, 16
- **Heat coefficients**, from §10.2: base OPEN +1; reopen <2min additional +2; reopen <10min additional +1; prior session exceeded declared duration by >50% and >2min +2; prior contract respected −1; decay −1 per ~10 min away; floor 0; cap 30
- **Gravity**, from §10.3: `floor(opens_today / 6)`, cap 5
- **Behavioural day**: current date − 4 hours
- **Sequence orderings**, from §12: Classic (default), Black Mirror, Ambient — each a nine-entry ordering of the primitives, with combined entries where specified
- **Ice cooldown durations**, from §22: Paradise ~60s, Limbo ~3min, Inferno ~5min
- **Exit exploration rate** — configuration, not a hardcoded constant (§9.3)

All values are explicitly prototype parameters and must be trivially tunable.

### Capability audit must cover, at minimum (§31)

Get Current App · Get File · Save File / overwrite · Dictionary and JSON parsing · Get Dictionary Value · date arithmetic · Notes search/find · Create Note · Append to Note · show/open note · Ask for Input · Choose from Menu/List · Open App · Open URLs / web search · Maps search · Set Brightness · get current brightness · Set Volume · get current volume · Color Filters / grayscale · Speak Text · Lock Screen · Run Shortcut · Wait · Base64 if needed · Use Model / On-Device model · model structured output · Get App & Website Data (research only, not core v1).

For each: exact identifier, parameter shape, verdict, evidence path, and named fallback if not VERIFIED.

</specifics>

<deferred>
## Deferred Ideas

- Authoring any actual plist XML — begins in Phase 2.
- `Get App & Website Data` beyond recording its verdict — v2 measurement work.
- Any Sentient/`Use Model` authoring — Phase 8, gated on this phase's AUDIT-06 outcome.

</deferred>
