# Project Research Summary

**Project:** PROSOCHĒ — Nine Circles
**Domain:** Native iOS 26 Shortcut — adaptive-friction digital-wellbeing intervention (no companion app, no blocking APIs)
**Researched:** 2026-08-13
**Confidence:** MEDIUM-HIGH

## Executive Summary

PROSOCHĒ is a single large stateful iOS Shortcut that intercepts app-opens via Personal Automations, computes an adaptive "Pressure" score from behavioural clustering (Heat + Gravity), and escalates the user through nine graduated friction Circles. All four research passes converge: the deterministic state-engine architecture is fully buildable with verified Shortcuts primitives, but the design's most distinctive primitives depend on iOS capabilities the bundled ToolKit catalogs cannot confirm exist, and one — Color Filters/grayscale — is confirmed absent entirely. Brightness/volume readback and the `Use Model` On-Device pinning literal are similarly unverified.

The recommended approach: build the deterministic Dumb engine first using only fully verified primitives, and treat unverified/blocked capabilities as design-time contingencies via a dedicated early capability-audit phase, not late discoveries. Ash should be redesigned or deferred; Dimming/Silence default to message-only unless a readback path is confirmed; the Sentient fork is gated on manually round-tripping the On-Device enum literal before any Sentient XML is written.

The strongest product-discipline finding: the one sec preregistered study found the option to dismiss was the strongest mechanism — stronger than time-delay friction and the deliberation message. The choice architecture is the product; the clever sentence is not. This should discipline both engineering effort allocation (Exits and Circle IX deserve equal rigor to the Mirror) and roadmap sequencing.

## Key Findings

### Recommended Stack
Shortcuts Playground plugin v1.2.1 (skill docs + validator + signer), the macOS-only `shortcuts` CLI for signing, Python 3.10+ for the validator. Validate at `--target-macos 26 --target-platform ios`. One `state.json` + one Apple Note — no CSV, no second machine store.

### Expected Features
**Must have:** idempotent bootstrap, deterministic state engine (Heat/Gravity/Pressure/profiles), session-ID race-proof OPEN/CLOSE reconciliation, nine primitives (min. Knock/Confession/Exile/Ice), Circle IX with guaranteed route-out, six exits with outcome recording, environmental safety floors + Emergency Restore, corrupt-state recovery.
**Should have:** three switchable sequences, epsilon-greedy exit-learning, contract fidelity metric, Sentient contract-auditor/tiering/longitudinal memory.
**Defer:** contextual exit learning, Screen Time telemetry, "Life Returned" quantification, NFC/Focus/companion app.

### Architecture Approach
One monolithic action graph per fork (not dispatcher+helpers — internal `Run Shortcut` hops add latency/lossy serialization for zero isolation benefit). Timestamps as integer Unix epoch seconds. In-memory mutation, two `Save File` checkpoints per OPEN. Nested If/Otherwise throughout (`Otherwise If` is macOS-27+ only, unusable on iOS 26.x target).

**Major components:** invocation router (OPEN/CLOSE/MANUAL, fail-safe on unrecognized input); state engine (Heat/Gravity/Pressure, race-proof session reconciliation); Circle dispatch + nine primitives (sequence-table-driven, capture-verified environmental guards); Control Room (Note + manual menu, the only onboarding path); Sentient layer (additive wraps at Circles II–VIII only, I and IX always deterministic).

### Critical Pitfalls
1. **Validator false-passes** — `WFTextTokenAttachment` on display strings renders blank at runtime; `markdown` vs `markdownContents` on Note creation produces an empty Control Room Note body (the Note *is* onboarding).
2. **GroupingIdentifier collisions at depth** — the #1 documented real-world mistake; PROSOCHĒ's nesting is deep by construction.
3. **JSON dictionary type coercion** — booleans coerce to 1/0, null coerces to empty, nested reads on null parents break.
4. **No numeric "equals" condition code** — Pressure→Circle mapping needs `≥` ladders, not equality.
5. **Session-ID race-proofing** — the single hardest build item; no platform locking primitive exists.

## Implications for Roadmap

**Unmissable finding: a live on-device capability audit must be its own early phase, before any phase depends on the primitives, the Note, or the model.** Four independent hard blockers:

1. No verified iOS action for Color Filters/grayscale exists anywhere in the bundled catalogs. The Ash primitive as literally specified cannot be built — a fallback design is required.
2. No verified `getbrightness`/`getvolume` read action exists — only writes. Since the canonical strategy forbids any stateful change that cannot be restored, Dimming and Silence must degrade to message-only unless a read path is confirmed on-device.
3. `Use Model` On-Device pinning literal is unverified — no known plist key/enum forces On-Device over Private Cloud Compute or ChatGPT. This is a hard gating blocker for the entire Sentient fork; resolve via manually selecting On-Device in Shortcuts.app, exporting unsigned XML, and reading the literal back — before writing any Sentient action.
4. Notes actions are tagged macOS-only in the bundled schema catalog but are near-certainly real on iOS (long-standing standard actions; the gap is likely simulator-snapshot incompleteness). The entire Control Room/onboarding design depends on them — needs on-device confirmation early.

Also: `Otherwise If` is macOS-27+ only — use nested If/Otherwise for all routing and Circle lookup from the start. Two specific validator false-passes (`WFTextTokenAttachment` on display strings; `markdown` vs `markdownContents`) will silently break every user-facing message and the Control Room Note body unless treated as hard authoring rules from line one.

### Phase 1: Capability Audit & Config Foundation
**Rationale:** Every later phase depends on knowing which of the four blockers resolve favorably.
**Delivers:** Go/no-go table for Ash, Dimming/Silence readback, Notes-on-iOS, and the `Use Model` On-Device literal (via manual export round-trip); the static Config literal (thresholds, sequences, cooldowns).
**Addresses:** Environmental-safety table stakes; capability audit requirement.
**Avoids:** Fabricated action identifiers; unverifiable On-Device pinning.

### Phase 2: Routing, Bootstrap, State Discipline
**Rationale:** Every later phase reads/writes through this layer — must be provably correct in isolation first.
**Delivers:** Input routing with fail-safe unrecognized-input handling; idempotent bootstrap; load/validate/persist proven against corrupted/missing files.
**Uses:** Nested If/Otherwise; integer epoch timestamps; coercion-safe reads.

### Phase 3: Deterministic State Engine (Heat/Gravity/Pressure/Circle)
**Rationale:** Numeric core proven correct with stubbed primitives before compounding with on-device UI debugging.
**Delivers:** Behavioural-day rollover, Heat/Gravity/Pressure, Circle threshold mapping across all profiles.
**Avoids:** No numeric-equals code misuse; date/epoch mistakes; rollover-at-04:00 edge case; cooldown Heat-inflation.

### Phase 4: CLOSE Pipeline & Race Protocol
**Rationale:** Contract fidelity and exit-learning depend on trustworthy duration; must be stress-tested with rapid app-switching before primitives layer on top.
**Delivers:** Session-ID reconciliation (owning vs superseded CLOSE), real duration measurement, idempotency guards.

### Phase 5: Nine Primitives (Dumb, Deterministic)
**Rationale:** Depends on Phase 1's audit resolving Ash/Dimming/Silence fallback shapes, and Phase 3/4's stable engine.
**Delivers:** All nine primitives deterministic; environmental primitives wrapped in capture-verified/skip-if-unreadable guards; Circle IX with guaranteed route-out.

### Phase 6: Exits, Exit Learning, Contracts
**Rationale:** Per the one-sec finding, deserves resourcing equal to primitive/Mirror work, not late polish.
**Delivers:** Six exits with outcome recording; epsilon-greedy explore/exploit; contracts feeding Heat's fidelity term.
**Avoids:** Over-verbal design; redirecting into another phone app instead of genuinely off-phone.

### Phase 7: Control Room, Dumb Mirror Engine, Freeze & Ship Dumb
**Rationale:** Depends on steps 2–6 all existing.
**Delivers:** Manual menu; ≥30 fact-gated Mirror templates; full acceptance pass; validate, sign, on-device import test.

### Phase 8: Sentient Fork
**Rationale:** Must not begin until Dumb is stable and on-device-verified, and gated on Phase 1's On-Device literal resolution.
**Delivers:** `Use Model` integration with resolved On-Device pinning, structured ALLOW/CHALLENGE/DENY with deterministic fallback, per-circle AI tiering, longitudinal memory context.
**Avoids:** Model latency breaking early Circles; silent fallback off On-Device; malformed-output defaulting to punishment; model fabricating facts.

### Phase Ordering Rationale
Routing/bootstrap/state-discipline must be unshakeable before any behavioral logic exists. The numeric engine is proven with stubs before real primitives wire in. CLOSE/race-protocol lands before exits/contracts because fidelity depends on accurate duration. Dumb must fully pass acceptance before Sentient starts, since every Sentient hook is an additive wrap. Capability audit comes first because four independent researchers converged on the same four blockers.

### Research Flags

Needs research during planning:
- **Phase 1:** The on-device round-trip technique for the `Use Model` literal needs live execution.
- **Phase 5:** Environmental primitive fallback shapes depend entirely on Phase 1's findings, may need mid-phase redesign.
- **Phase 8:** `Use Model` structured-output parameter shape and contract-auditor prompt engineering are light-evidence areas.

Standard patterns (skip dedicated research-phase):
- **Phase 2:** Control-flow/dictionary/file-action patterns are HIGH-confidence, richly documented.
- **Phase 3:** Date/epoch arithmetic and condition codes exhaustively documented.
- **Phase 4:** Built entirely from already-verified primitives — risk is design correctness, not undocumented capability.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH for toolchain/validator/signing; MEDIUM for some parameter shapes; explicit UNVERIFIED (not fabricated) for `Use Model` pinning and brightness/volume read |
| Features | HIGH — traced directly to canonical strategy; competitor benchmarking MEDIUM |
| Architecture | MEDIUM-HIGH — control-flow/wiring claims HIGH; several action capabilities explicitly flagged unevidenced rather than assumed |
| Pitfalls | HIGH for authoring pitfalls and action-availability (verified against plugin/ToolKit); MEDIUM for concurrency and behavioural pitfalls |

**Overall confidence:** MEDIUM-HIGH. Uncertainty is concentrated in four named capabilities (grayscale, brightness/volume readback, On-Device pinning, Notes-on-iOS confirmation) — not in architecture or general authoring approach.

### Gaps to Address
- **Ash (grayscale):** No viable native mechanism — a Phase 1 design decision (drop/substitute/defer), not a later research task.
- **Brightness/volume readback:** Confirm on-device whether `Get Device Details` exposes usable properties; else ship Dimming/Silence as message-only in v1.
- **`Use Model` On-Device literal:** Must be resolved via manual export round-trip before any Sentient XML is authored.
- **Notes actions on real iOS:** High confidence but formally unconfirmed for this snapshot — verify on first Dumb on-device import.
- **Get Current App reliability at automation trigger time:** Needs on-device confirmation; time-only-debounce fallback already designed.

## Sources

### Primary (HIGH confidence)
- Shortcuts Playground plugin v1.2.1 skill docs and bundled ToolKit identifier/parameter/enum catalogs — installed ground truth
- 19 golden-shortcut XML corpus
- `PROSOCHE_Nine_Circles_Canonical_Strategy.md` and `.planning/PROJECT.md` (this repo)

### Secondary (MEDIUM confidence)
- Apple Support "What's new in Shortcuts" — brightness/volume properties, exact keys unconfirmed
- MacStories/TechCrunch/AppleInsider on the iOS 26 `Use Model` picker — model-source existence only, no plist literal
- Competitor marketing/review pages (Opal, Brick, ScreenZen) for benchmarking

### Tertiary (LOW confidence)
- None tracked separately — all UNVERIFIED items are flagged inline as capability-audit requirements.

---
*Research completed: 2026-08-13*
*Ready for roadmap: yes*
