---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
verified: 2026-08-17T13:10:00Z
status: gaps_found
score: 13/18 must-haves verified
behavior_unverified: 2
overrides_applied: 0
gaps:
  - truth: "The nine primitives named by BD-06 Decision 3 each perform their intervention when dispatched"
    status: failed
    reason: >-
      `dimming()` and `silence()` gate on the settings_snapshot CONTAINER at condition 100
      (has any value) with the entire capture-and-apply body in the OTHERWISE arm. The
      container is seeded at bootstrap as a non-empty sub-dictionary and `clear_snapshot()`
      clears only the LEAF — its own docstring calls the container a "PERMANENT invariant".
      The gate is therefore permanently TRUE and both primitives take the `Nothing` arm on
      every run. Two of BD-06's nine shipped interventions (Dim, Silence) are silent no-ops.
      Pre-existing, but RE-CERTIFIED by this phase: 11-05 updated the site tables that audit
      this dead code, and MANIFEST.md:195 ships the claim "Dimming and Silence writes now
      execute where they previously no-opped."
    artifacts:
      - path: "tools/build_state_engine.py:576-595"
        issue: "dimming(): if_block('Brightness Snapshot', 100) on the container; body in the otherwise arm"
      - path: "tools/build_state_engine.py:598-618"
        issue: "silence(): same shape on settings_snapshot.volume"
      - path: "artifacts/shortcuts/MANIFEST.md:195"
        issue: "Asserts the writes execute; they cannot be reached"
      - path: "docs/environmental_restore_check.py:97"
        issue: "EXPECTED_SITES = {15, 15, 22} certifies unreachable Set Brightness / Set Volume sites"
    missing:
      - "Gate on the LEAF (settings_snapshot.<x>.original_value) numerically at condition 2 (> 0), mirroring restore_managed_settings(), and invert the polarity so capture happens when no original is recorded"
      - "A build guard asserting no condition-100 gate read from a settings_snapshot CONTAINER key encloses a getdevicedetails / setbrightness / setvolume in either arm"
      - "Correct the MANIFEST prose and the two site tables only after the bodies are live"

  - truth: "Removing Panic Escape requires two deliberate acts — editing the setting line in the Note by hand, then choosing the removal option in an explicit confirmation menu — and the same route restores it"
    status: failed
    reason: >-
      The new Panic Escape removal branch reads is.workflow.actions.text.match's output as
      OutputName "Matched Text". Re-measured independently against the bundled golden corpus:
      text.match resolves as "Matches" 15/15 times and "Matched Text" 0 times. This repo's own
      tools/build_sentient.py:156,159 uses "Matches" for the identical action, so the shipped
      artifact carries two contradictory names for one identifier. ACTION_OUTPUT_NAMES covers
      only getrichtextfrommarkdown, so verify_output_names() — the machinery built for exactly
      this defect class — is blind to it. If the reference does not resolve, `Panic Escape
      Section` is empty, the condition-99 contains test is always false, control falls to the
      otherwise arm, and the user is shown "The Note says ON and Panic Escape is already
      available. Nothing was changed." — a confident, wrong, unlogged success. The removal half
      of this phase's Addendum §3 deliverable is then dead with no error anywhere. INTRODUCED
      THIS PHASE (the pre-existing Sync My Profile site at :1968 shares the defect).
    artifacts:
      - path: "tools/build_state_engine.py:2031"
        issue: "output(match_id, 'Matched Text') — new this phase, on the removal path"
      - path: "tools/build_state_engine.py:1968"
        issue: "Same defect, pre-existing (Sync My Profile stores an empty profile_snapshot.proforma)"
      - path: "tools/build_state_engine.py:3256"
        issue: "ACTION_OUTPUT_NAMES omits is.workflow.actions.text.match, so the recurrence guard cannot see either site"
    missing:
      - "Use the corpus-attested 'Matches' at both sites"
      - "Add is.workflow.actions.text.match -> 'Matches' to ACTION_OUTPUT_NAMES so normalise_output_names()/verify_output_names() cover it and a third site cannot repeat it"
      - "Resolve the residual shape question: text.match returns a LIST, so gettext stringifies a one-element list — build_sentient.py:159 already inserts getitemfromlist/'First Item' for this"

  - truth: "docs/sentient_core_check.py still proves Aware is an additive fork of Core — the Use Model audit is present wherever the Aware fork differentiates itself"
    status: failed
    reason: >-
      Measured on the shipped src/PROSOCHE-Sentient.xml: 11 primitive_dispatch() renderings,
      11 contract markers (1150, 1414, 1926, ...), and exactly ONE askllm at action 1108 —
      inside rendering #1 only. build_sentient.py:265-271 inserts audit_block() at the FIRST
      marker and breaks. Before this phase, "first marker" and "the OPEN-arm marker" coincided.
      Plan 11-05 added a SECOND OPEN-arm rendering (the panic_escape_enabled == 0 otherwise arm
      of universal_leaving()), so an Aware user who removes Panic Escape reaches the Intention
      (Confession) primitive with no contract audit at all — the entire reason the Aware fork
      exists disappears because of an unrelated bypass setting. sentient_core_check.py:103's
      `assert len(models) == 1` pins the defect rather than catching it. AGGRAVATED THIS PHASE.
    artifacts:
      - path: "tools/build_sentient.py:265-271"
        issue: "`break` after the first marker; only rendering #1 receives audit_block()"
      - path: "docs/sentient_core_check.py:103"
        issue: "assert len(models) == 1 locks the single-audit state in"
    missing:
      - "Locate the OPEN arm structurally and insert the audit into EVERY OPEN-arm rendering, iterating in reverse so earlier indexes stay valid"
      - "Give uid() a per-rendering discriminator — audit_block() uses fixed literal keys, so a second rendering would collide on GroupingIdentifier/UUID, the top real-world failure mode per .claude/CLAUDE.md §4"
      - "Change the sentient_core_check assertion from == 1 to the measured OPEN-arm rendering count, with a derivation comment"
      - "OR: record 'audit only the Panic-Escape path' as a deliberate product decision in docs/CAPABILITY-DECISIONS.md and surface it in the Note, because it makes an unrelated setting silently switch forks"

  - truth: "The guards this phase's value rests on are real guards that fail closed"
    status: partial
    reason: >-
      Five of six negative controls I ran were caught correctly. One passes silently.
      verify_panic_escape_seed()'s third assertion matches conditionals by the bare literal
      VariableName == "Panic Escape Enabled", which appears nowhere as a shared constant — the
      emitter at :991-992 carries its own copy. Precise negative control (renaming ONLY the
      emitter's variable to "PE" and flipping the gate to condition 100, leaving the guard's
      literal at :2704 untouched): the build exits 0 and every standing checker stays green.
      The guard is vacuous under exactly the drift it exists to catch. It also does not cover
      the two "Panic Escape Stored" gates at :2043 and :2071.
    artifacts:
      - path: "tools/build_state_engine.py:2702-2705"
        issue: "Name-coupled assertion; passes vacuously when the emitted variable name drifts"
    missing:
      - "Resolve the tested variable by PROVENANCE using _read_variable_keys() (which already maps variables to the literal key they were read from) rather than by name"
      - "Cover every variable read from panic_escape_enabled, including the two 'Panic Escape Stored' gates"
      - "Assert the guarded set is non-empty so an orphaning rename fails rather than passes vacuously"

  - truth: "Each interim stand-in is named as interim in the generator's own comment text AND in docs/BUILD-NOTES.md, with the phase that replaces it (plan 11-02 prohibition)"
    status: partial
    reason: >-
      The substance is recorded, but not in the file the prohibition names. The Loud Mirror
      interim is documented in the generator at :704-709 ("DELIBERATE INTERIM", PHASE 15 named).
      The Circle-6 Eject interim is documented in src/CONFIG-BLOCK.md:30 (Phase 17 named, with
      the exact two cells it will flip). Neither is in docs/BUILD-NOTES.md — "Eject" appears
      there 0 times, and "Loud Mirror" appears only as a count in an evidence table (:2139).
    artifacts:
      - path: "docs/BUILD-NOTES.md"
        issue: "Neither interim is named as interim with its replacing phase"
    missing:
      - "Append both interims to docs/BUILD-NOTES.md with their replacing phases (15 and 17), or amend the prohibition to name CONFIG-BLOCK.md as the accepted location"

deferred:
  - truth: "Redirect occupies Circle 6 in Classic and Ambient"
    addressed_in: "Phase 17"
    evidence: "ROADMAP Phase 11 'Intermediate state to respect': 'Redirect has no implementation until Phase 17, so all three sequences hold Eject at Circle 6 until then; Phase 17 flips Classic's and Ambient's cells.' Confirmed in src/CONFIG-BLOCK.md:30."
  - truth: "Circle 8 dispatches the designed Voice primitive rather than the Mirror"
    addressed_in: "Phase 15"
    evidence: "ROADMAP Phase 11: 'Circle 8 gets a real branch here (interim: the Mirror) so the guard can be a hard gate immediately; Phase 15 replaces it with the designed Voice.' Confirmed in tools/build_state_engine.py:704-709."
  - truth: "Both forks import onto a real iPhone and complete a first manual run"
    addressed_in: "DIST-03 (open requirement, Phase 8)"
    evidence: ".planning/REQUIREMENTS.md:161 '- [ ] DIST-03' — Pending. No iPhone is connected; every claim in this phase is file-level structural."

behavior_unverified_items:
  - truth: "A second manual run reuses the note it already found rather than creating a second one, and a deleted note is recreated with its full body on the next manual run (BOOT-08)"
    test: "Import a signed fork on an iPhone. Tap it, let it create the Note. Tap it a second time. Then delete the Note in the Notes app and tap a third time."
    expected: "No duplicate Note after run 2; state.json unchanged. After deletion, run 3 recreates the Note with its FULL body (including ## THE NINE CIRCLES, ## OPTIONAL HARDENING, ## PANIC ESCAPE), not a lesser placeholder."
    why_human: >-
      The Find-Notes lookup is bound with limit 1 + First Item, which is structurally provable
      from the plist and IS proven (docs/note_identity_check.py exits 0). Whether a real device
      re-binds and re-creates correctly is runtime-only. BD-06-A2 also widened what the
      shortened 'contains PROSOCHĒ' predicate can match, so a leftover 'PROSOCHĒ — Control Room'
      note from an earlier install could be bound permanently and silently.
  - truth: "If a manual run is interrupted between the Find-Notes lookup and the append, or two runs overlap, the Note can lose an append or gain a duplicated block — the guarantee is at-most-one-note-bound-per-run and nothing stronger"
    test: "On device, force-quit Shortcuts mid-manual-run between the Note lookup and the append; separately, trigger two manual runs in rapid succession."
    expected: "At most one note bound per run. A lost append or a duplicated block is the accepted, documented limit — not a regression."
    why_human: >-
      Declared verification: backstop in plan 11-03. Shortcuts offers no transaction and no
      lock, so this is a negative runtime property that no file-level analysis can confirm or
      refute. Abstaining rather than asserting.
---

# Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster — Verification Report

**Phase Goal:** Apply `PROSOCHE_Build_Addendum_01.md` in full, once, against the roster settled
in BD-06 (`docs/CAPABILITY-DECISIONS.md`) — so the rename lands a single time rather than being
re-cut after each of the four in-flight Circle phases.

**Verified:** 2026-08-17
**Status:** gaps_found
**Re-verification:** No — initial verification

## Standing evidence constraint

**DIST-03 is open. No iPhone is connected.** Every check below is file-level structural. Where
this report says VERIFIED it means *the artifact provably has this shape*, never *the device
provably does this*. The signed artifacts were decrypted (AEA1 → `aea decrypt` → `aa extract`)
and compared to source, but a decrypted artifact is still a file — no device behaviour is
inferred from it anywhere in this report.

Every number below was re-taken by this verifier. None is transcribed from a SUMMARY.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Intervention rename per Addendum §5 reaches both signed artifacts | ✓ VERIFIED | Decrypted payloads action-array-equal to source (Core 4456, Aware 4524, `==` True). `Pause` ×36, `Loud Mirror` ×25, `Black and White` ×47, `Frozen` ×26; retired `Knock` ×0, `Ash` ×0 |
| 2 | BD-06 Decision 4's slot table applied to all three sequences, in the Phase-11 intermediate state | ✓ VERIFIED | Config literal parsed from both plists: Classic/BlackMirror/Ambient each 9 shipped names; `Eject` at Circle 6 in all three; `Redirect` absent |
| 3 | Dispatch is exact-match; every sequence entry resolves to exactly one branch and every branch is named | ✓ VERIFIED | Measured 99 `Selected Primitive` conditionals, **all condition code 4**, 0 at code 99. 9 branch names × 11 renderings. Bijection with the 9 distinct sequence entries |
| 4 | The dispatch-coverage build guard is a hard gate written in this phase | ✓ VERIFIED | Negative-controlled: orphaned one Config sequence entry → `verify_dispatch_coverage()` exit 1 AND `docs/sequence_dispatch_check.py` exit 1, both with correct messages. Condition 99 revert → caught (duplicate). Unknown code 8 → caught |
| 5 | Circle 8 dispatches a real branch in all three sequences (interim) | ✓ VERIFIED | `Loud Mirror` is one of the 9 emitted branch names; the orphan that made Circle 8 ship dead is gone. Interim labelling: see truth 18 |
| 6 | The Apple Note's user-facing title is the bare product name at all three identity sites; internal "Control Room" kept | ✓ VERIFIED | `docs/note_identity_check.py` exit 0 for both forks. `Control Room` ×26 internally; the one `PROSOCHĒ — Control Room` literal remaining is the deliberate stale-note migration warning (BD-06-A2) |
| 7 | Dante's nine names are surfaced positionally from one generator constant | ✓ VERIFIED | `CIRCLE_NAMES` at :47; `WFMenuItems` == `["Circle 1 · Limbo" … "Circle 9 · Treachery"]` and case titles == items element-for-element, in order |
| 8 | The Note explains the optional Shortcuts-app hardening | ✓ VERIFIED | `## OPTIONAL HARDENING` present in both fork bodies with the full explanation and the Emergency-Restore reassurance |
| 9 | BD-06-A1's profile rename Limbo→Purgatory landed completely (a partial rename is a hard error, not a degradation) | ✓ VERIFIED | Config literal in **both** forks: `thresholds` keys `[Paradise, Purgatory, Inferno]`, `cooldown_seconds` keys `[Paradise, Purgatory, Inferno]`. **No `Limbo` profile key survives.** All 3 remaining `Limbo` occurrences per XML are Circle-1 positional names (`Circle 1 · Limbo` ×2 + note legend ×1). `PROFILE_NAMES = ("Paradise","Purgatory","Inferno")` |
| 10 | The schema_version disposition is recorded, and the bump applied | ✓ VERIFIED | BD-06-A3 present in CAPABILITY-DECISIONS.md citing BD-06-A1 as the discharging input; bootstrap template carries `"schema_version": 3`; no migration, dual-key alias or read-time normalisation built |
| 11 | Panic Escape is gated on a first-class flat state field, read numerically | ✓ VERIFIED | `panic_escape_enabled` seeded top-level as `1`; `read_value(..., "Panic Escape Enabled")` flat; gate `if_block(..., 2, number=0)` (> 0), never condition 100. Negative controls: unseeded flag → caught; gate flipped to 100 alone → caught |
| 12 | Emergency Restore is reachable on every path and is enclosed by no Panic Escape conditional (T-11-22, the phase's only `critical`) | ✓ VERIFIED | Enclosure walk over both forks: 5 Panic-Escape-gated groups, 4 real Emergency Restore menu surfaces per fork (2 `WFMenuItems`, 2 case titles), **0 enclosed**. Confirms the review |
| 13 | Both variants ship under their new canonical names with no suffix | ✓ VERIFIED | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` and `… — Aware.shortcut`; `docs/manifest_check.py` exit 0, 6 rows verified against disk |
| 14 | Each fork's Note names its own variant as the Run Shortcut target | ✓ VERIFIED | Core: own ×2, other ×0. Aware: own ×2, other ×0 |
| 15 | Both builders are idempotent, all twelve structural checks pass, and both forks validate at the iOS 26 target | ✓ VERIFIED | Isolated-copy rebuild reproduces the shipped sources byte-for-byte and is stable across two runs (md5 identical ×3). 12/12 checkers exit 0. `validate-shortcut --target-macos 26 --target-platform all` → "Validation passed" for both. `git status --short` clean. Attachment-offset invariant: **0 mismatches** over 1205 (Core) / 1209 (Aware) `WFTextTokenString` tokens |
| 16 | The nine primitives named by BD-06 Decision 3 each perform their intervention when dispatched | ✗ FAILED | **CR-01.** `dimming()`/`silence()` bodies unreachable — container gate at condition 100 is permanently TRUE, body sits in the never-taken OTHERWISE arm. See Gaps |
| 17 | Removing Panic Escape requires a manual Note edit plus explicit confirmation, and the same route restores it | ✗ FAILED | **CR-02.** The removal path reads `text.match` as `"Matched Text"`; corpus is 15/15 on `"Matches"` and the repo's own other site uses `"Matches"`. Failure mode is a false success message. See Gaps |
| 18 | `docs/sentient_core_check.py` proves Aware is an additive fork of Core on every path | ✗ FAILED | **CR-03.** 11 OPEN-arm dispatch renderings, 11 contract markers, exactly 1 `askllm` (action 1108, rendering #1 only). Removing Panic Escape silently turns Aware into Core. See Gaps |
| 19 | The guards this phase's value rests on fail closed | ⚠️ PARTIAL | 5/6 negative controls caught. `verify_panic_escape_seed()` passes vacuously under an emitter rename (WR-01 confirmed). See Gaps |
| 20 | Each interim stand-in is named as interim in the generator AND in docs/BUILD-NOTES.md | ⚠️ PARTIAL | Substance recorded (generator :704-709 → Phase 15; CONFIG-BLOCK.md:30 → Phase 17) but not in BUILD-NOTES.md, which the prohibition names. See Gaps |
| 21 | Aware's status display and note settings block report its own fork label | ⚠️ PARTIAL | The load-bearing `- Fork:` line was fixed. Two non-load-bearing sites still say the other fork — self-reported in `deferred-items.md`: the `WFWorkflowActions[0]` header comment ("Dumb fork") and the Aware Note's `- AI: not used by this fork`. Neither is an automation target, state key or lookup predicate |

**Score:** 13/18 truths verified (2 present, behaviour-unverified; 3 partial folded into gaps).

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|--------------|----------|
| 1 | `Redirect` occupies Circle 6 in Classic and Ambient | Phase 17 | ROADMAP Phase 11 "Intermediate state to respect"; CONFIG-BLOCK.md:30 names the exact two cells |
| 2 | Circle 8 dispatches the designed Voice primitive | Phase 15 | ROADMAP Phase 11; generator :704-709 |
| 3 | Device import + first manual run | DIST-03 (open) | REQUIREMENTS.md:161 Pending |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| `primitive_dispatch()` name tuple | `WFConditionalActionString` on 99 conditionals | `if_block("Selected Primitive", 4, string=name)` | ✓ WIRED | 9 names × 11 renderings, all code 4 |
| Dispatch branches | `sequences` arrays in the Config literal | `verify_dispatch_coverage()` | ✓ WIRED | Exact bijection; negative-controlled in both directions |
| `src/PROSOCHE-Dumb.xml` | `src/PROSOCHE-Sentient.xml` | `tools/build_sentient.py` | ✓ WIRED | Sentient rebuild reproduces the shipped file byte-for-byte |
| `CIRCLE_NAMES` | Test-a-Circle `WFMenuItems` → case titles | `circle_label()` | ✓ WIRED | Items == case titles, element-for-element, in order |
| Create Note `name` | Find-Notes lookup predicate | `EXPECTED_TITLE` in note_identity_check | ✓ WIRED | Both resolve to the bare product name; checker exit 0 |
| `DISPLAY_NAMES` | MANIFEST row labels → files on disk | `docs/manifest_check.py` | ✓ WIRED | 6 rows, SHA-256 + byte size verified against disk |
| `## PANIC ESCAPE` Note line | MANUAL-arm text-match read → confirmation menu → `panic_escape_enabled` | `text.match` → `gettext` | ✗ NOT WIRED | **CR-02** — the `gettext` reads `OutputName "Matched Text"`, which no corpus evidence supports |
| OPEN-arm dispatch renderings | Aware `audit_block()` | first-marker insertion in build_sentient.py | ✗ PARTIAL | **CR-03** — 1 of 2 OPEN-arm renderings receives the audit |
| `settings_snapshot.<x>` gate | Set Brightness / Set Volume writes | container gate at condition 100 | ✗ NOT WIRED | **CR-01** — writes sit in the unreachable OTHERWISE arm |

### Behavioural Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Twelve structural checkers pass | `python3 docs/<each>.py` | 12/12 exit 0 | ✓ PASS |
| Both forks validate at iOS 26 target | `validate-shortcut … --target-macos 26 --target-platform all` | "Validation passed", exit 0, both | ✓ PASS |
| Engine idempotent + reproduces shipped source | two rebuilds in an isolated copy, md5 | shipped == run1 == run2, both forks | ✓ PASS |
| Signed artifacts decrypt and match source | `aea decrypt` → `aa extract` → `plutil` | action arrays `==` True, both forks | ✓ PASS |
| Dispatch orphan is caught | patch Config entry → run engine + gate | both exit 1, correct messages | ✓ PASS |
| Condition 99 revert is caught | patch `if_block(…, 4` → `99` | exit 1, "matches MORE THAN ONE distinct dispatch branch" | ✓ PASS |
| Unknown condition code is caught | patch to code 8 | exit 1, "unresolvable matching semantics" | ✓ PASS |
| Unseeded panic-escape flag is caught | strip key from template + neuter seeder | exit 1, correct message | ✓ PASS |
| Panic-escape gate flipped to 100 is caught | patch gate only | exit 1, correct message | ✓ PASS |
| Panic-escape gate flipped to 100 **with emitter renamed** | rename emitter var only, leave guard literal | **exit 0, all checkers green** | ✗ FAIL (WR-01) |
| `text.match` OutputName in golden corpus | resolve all ActionOutput refs across 19 shipped XMLs | `Matches` ×15, `Matched Text` ×0 | ✗ FAIL (CR-02) |
| Aware Use Model audit coverage | count askllm vs OPEN-arm renderings | 1 askllm vs 11 renderings, rendering #1 only | ✗ FAIL (CR-03) |
| Emergency Restore enclosure | enclosure walk over both forks | 4 surfaces each, 0 enclosed by a Panic Escape group | ✓ PASS |
| Environmental site counts | count identifiers in shipped plist | 15 setbrightness / 15 setvolume / 22 getdevicedetails — matches `EXPECTED_SITES` | ✓ PASS (but see CR-01: these audit dead code) |

Device behaviour: **not tested — DIST-03 open, no iPhone connected.** No spot-check above starts a service, mutates state, or touches a device.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| AUDIT-02 | 11-02, 11-04, 11-05 | Grayscale / Color Filters resolved to go/no-go with a documented Ash fallback | ✓ SATISFIED | `Black and White` is a live dispatch branch (11 renderings); BD-06-A3 recorded; fallback design carried in CAPABILITY-DECISIONS.md |
| CIRC-02 | 11-01, 11-02 | Ash applies the audited visual-salience reduction or its documented fallback | ✓ SATISFIED | Renamed to `Black and White`, dispatches at condition 4 in all three sequences |
| CIRC-06 | 11-02, 11-05 | Exile immediately routes to an exit without a permission prompt | ✓ SATISFIED | `Eject` occupies Circle 6 in all three sequences and resolves to `exile()` (`returntohomescreen`, no prompt). Routed `Redirect` deferred to Phase 17 per ROADMAP |
| CIRC-08 | 11-02 | The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels | ✓ SATISFIED (interim) | `Loud Mirror` resolves to `mirror_and_voice()`, which carries the once-per-run and voice-enabled gates. Designed primitive deferred to Phase 15, labelled DELIBERATE INTERIM in the generator |
| ROOM-01 | 11-01, 11-03 | The Note opens with READ THIS FIRST explaining PROSOCHĒ and both automations | ✓ SATISFIED | `## READ THIS FIRST` anchor asserted by note_identity_check.py (exit 0); `## THE NINE CIRCLES` and `## OPTIONAL HARDENING` added |
| ROOM-02 | 11-03, 11-06 | The Note gives exact steps for Automation A | ✓ SATISFIED | Each fork's Note names its own Run Shortcut target ×2, the other ×0 |
| DIST-01 | 11-01, 11-03, 11-05, 11-06 | Both forks pass the validator at the iOS 26 target | ✓ SATISFIED | Re-run by this verifier: "Validation passed", both forks |
| DIST-02 | 11-01, 11-04, 11-06 | Both forks sign successfully into importable `.shortcut` files | ✓ SATISFIED | Both signed artifacts present, non-zero, decrypt cleanly, manifest_check exit 0. **"Importable" is structural — DIST-03 is the device half and is open** |

**Orphaned requirements:** none. All eight ROADMAP requirement IDs appear in at least one plan's
`requirements` field, and all eight resolve to implementation evidence.

**Adjacent:** DIST-04 (forks named unambiguously and distinguishable at import) is not in the
phase's declared list but is asserted by `docs/manifest_check.py` and passes — the Core/Aware
rename satisfies it.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tools/build_state_engine.py` | 576-595, 598-618 | Unreachable body behind an always-true container gate | 🛑 Blocker | Dim and Silence are silent no-ops (CR-01) |
| `tools/build_state_engine.py` | 2031 | Unattested `OutputName` on a load-bearing read | 🛑 Blocker | Panic Escape removal dead with a false success message (CR-02) |
| `tools/build_sentient.py` | 265-271 | `break` after first marker; assumes one OPEN-arm rendering | 🛑 Blocker | Aware silently becomes Core on the Panic-Escape-removed path (CR-03) |
| `tools/build_state_engine.py` | 2702-2705 | Guard coupled to a bare literal with no shared constant | ⚠️ Warning | Guard passes vacuously under rename (WR-01) |
| `docs/note_identity_check.py` | 84 | `MINIMUM_TOKEN_STRINGS = 775` vs measured 1205/1209 | ⚠️ Warning | 430 units of slack on the axis-2 floor guard (WR-02 confirmed by independent count) |
| `artifacts/shortcuts/MANIFEST.md` | 195 | Asserts behaviour that cannot occur | ⚠️ Warning | Ships a false capability claim alongside the artifacts |
| `docs/BUILD-NOTES.md` | — | Neither interim recorded where the prohibition requires | ⚠️ Warning | Interim state auditable only from two other files |

No `TBD` / `FIXME` / `XXX` debt markers were found in the files this phase modified.

### Human Verification Required

Both items below are recorded in `behavior_unverified_items` and gate on DIST-03.

#### 1. Note binding and re-creation (BOOT-08)

**Test:** Import a signed fork on an iPhone. Tap it and let it create the Note. Tap a second
time. Then delete the Note in the Notes app and tap a third time.
**Expected:** No duplicate Note after run 2, `state.json` unchanged; after deletion, run 3
recreates the Note with its full body — including the new `## THE NINE CIRCLES`,
`## OPTIONAL HARDENING` and `## PANIC ESCAPE` sections.
**Why human:** The limit-1 + First Item binding is structurally proven and green. Whether a
device re-binds and re-creates correctly is runtime-only. BD-06-A2 also widened the `contains
"PROSOCHĒ"` predicate when the title shortened, so a leftover `PROSOCHĒ — Control Room` note
could be bound permanently and silently.

#### 2. Note append atomicity under interruption (declared `verification: backstop`)

**Test:** Force-quit Shortcuts mid-manual-run between the Note lookup and the append; separately,
trigger two manual runs in rapid succession.
**Expected:** At-most-one-note-bound-per-run and nothing stronger. A lost append or duplicated
block is the accepted documented limit, not a regression.
**Why human:** Shortcuts offers no transaction and no lock. This is a negative runtime property;
no file-level analysis can confirm or refute it. Abstaining rather than asserting.

## Gaps Summary

**The rename itself landed, and landed once.** That is the part of the goal this phase most
needed to get right, and it is genuinely done: BD-06 Decision 4's slot table is in all three
sequences, dispatch moved to exact match across all 99 conditionals with a real bijection, the
Note title moved at all three identity sites, both variants ship as Core and Aware under exact
canonical filenames, and BD-06-A1's mid-phase profile rename — the one whose partial application
would be a *hard error* rather than a degradation — is total: `thresholds.Purgatory` and
`cooldown_seconds.Purgatory` resolve in both forks, no `Limbo` profile key survives anywhere,
and every remaining `Limbo` is a Circle-1 positional name. The new build guard is a real guard;
I orphaned a sequence entry and both the build-time guard and the promoted standalone gate
failed closed with correct messages. The safety-critical separation (T-11-22) holds: zero of the
four Emergency Restore surfaces in either fork is enclosed by a Panic Escape conditional.

**But the goal was to apply the addendum *in full*, and §3 is the half that did not land.**
Panic Escape's removal direction — the feature plan 11-05 exists to deliver — depends on reading
a `text.match` output through an `OutputName` that appears 0 times in 15 corpus observations,
while this very repository uses the attested name for the same identifier 40 lines away in
another file. The project's own evidence hierarchy ranks the golden corpus second and inference
last; this site is inference, and it contradicts both the corpus and the repo. Its failure mode
is the worst available: not an error, but the message *"Nothing was changed."* And because that
same plan added a second OPEN-arm dispatch rendering, it silently halved the Aware fork's
differentiator — a user who removes Panic Escape gets no Use Model audit at all, which
`sentient_core_check.py` pins with `assert len(models) == 1` rather than detects.

**A third defect is older, but this phase re-certified it.** `dimming()` and `silence()` gate on
a container that `clear_snapshot()`'s own docstring designates a permanent bootstrap invariant,
with the whole capture-and-apply body in the arm that can never be taken. Two of BD-06's nine
shipped interventions do nothing. Phase 11 did not cause this, but it updated the site tables
that count those unreachable actions and shipped a MANIFEST that tells a distributor
"Dimming and Silence writes now execute where they previously no-opped." Auditing dead code and
advertising it as live is worse than leaving it unaudited.

**And one guard is theatre.** `verify_panic_escape_seed()` matches on a bare variable-name
literal. I renamed only the emitter's variable and flipped its gate to the exact existence test
the guard exists to forbid; the build exited 0 and all twelve checkers stayed green. Five of six
negative controls caught their defect — the reviewer's tally is correct and I confirm it rather
than dispute it — but the sixth guards the feature this phase introduced.

**Verdict.** Tasks completed; the rename goal achieved; the addendum goal not. Three of the four
gaps sit on paths that produce *no error* when they fail, which is precisely the defect class
BD-06 Decision 5 and this phase's own coverage guard were written to eliminate — the guard was
built for the dispatch layer and the same class immediately reappeared one level down, in output
names, in insertion points, and in gate polarity. Recommend closing CR-02 and CR-03 before
Phase 12, since both were introduced or aggravated here; CR-01 and WR-01 may be scheduled, but
CR-01's MANIFEST claim should be corrected immediately regardless, because it is a false
capability statement attached to a distributable artifact.

Nothing in this phase is device-verified. DIST-03 remains open.

---

_Verified: 2026-08-17T13:10:00Z_
_Verifier: Claude (gsd-verifier)_
