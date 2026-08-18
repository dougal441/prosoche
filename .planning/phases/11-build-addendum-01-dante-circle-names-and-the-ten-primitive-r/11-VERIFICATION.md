---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
verified: 2026-08-18T16:20:00Z
status: human_needed
score: 18/21 must-haves verified
behavior_unverified: 2
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_verified: 2026-08-17T13:10:00Z
  previous_score: 13/18
  note: >-
    The denominator changed and the change is deliberate. The 2026-08-17 report carried a
    21-row truth table but a frontmatter score of 13/18, which does not reconcile against
    its own table (rows 1-15 are all marked VERIFIED there). This pass scores the table
    itself, which is the auditable artifact: 21 truths, 18 verified, 2
    present-behaviour-unverified, 1 accepted partial. No truth was dropped, merged or
    reworded; the row numbering below is identical to the first pass so the two are
    diffable line for line.
  gaps_closed:
    - "CR-01 — dimming()/silence() bodies unreachable behind a permanently-true container gate"
    - "CR-02 — Panic Escape removal read text.match through the unattested OutputName 'Matched Text'"
    - "CR-03 — only 1 of 2 OPEN-arm dispatch renderings received the Aware fork's Use Model audit"
    - "WR-01 — verify_panic_escape_seed() passed vacuously under an emitter rename"
    - "WR-02 — neither interim stand-in was named as interim in docs/BUILD-NOTES.md"
  gaps_remaining: []
  regressions: []
  new_findings:
    - "16-UAT.md's build-identity pin is stale against the artifacts this phase re-signed (WARNING, fails safe, unrecorded)"

warnings:
  - finding: "16-UAT.md's build-identity pin no longer matches the shipped artifacts"
    severity: warning
    measured: >-
      16-UAT.md:53-54 pins Core `9b0f2614...2e7c` / 230232 bytes and Aware `1db5c1ef...d93b6`
      / 234623 bytes. The artifacts this phase re-signed measure Core
      `873fa3dbda7b1f3440bfc76997c2962198ddec2052096833787547b52f129f10` / 231148 bytes and
      Aware `4b7c2cfbddf0dccf47ef8e34209378faf14ca2d760dc089013d3b033ebd2ada0` / 238095
      bytes. MANIFEST.md's live table (:286, :289) carries the CURRENT digests and
      docs/manifest_check.py exits 0 against disk, so the manifest is right and only the UAT
      instrument is stale.
    why_it_matters: >-
      16-UAT.md is the ONLY device instrument for the capture-and-restore loop, and plan
      11-08 is the change that made that loop reachable at all. 11-08-SUMMARY.md:273 names
      those twelve tests as the device proof and states that this plan changes "what that
      UAT will now actually be testing" -- but did not re-pin it, and no phase-11 record
      notes that the pin is now stale.
    fails_safe: >-
      Yes. An operator running 16-UAT's identity check gets a mismatch and stops. Nothing is
      falsified and no claim is over-stated. This is an instrument-maintenance gap, not a
      correctness gap, which is why it is a WARNING and not a BLOCKER.
    human_decision_requested: >-
      Re-pin 16-UAT.md:53-54 to the current digests as part of phase 11's close, or record
      explicitly that the pin is superseded and name where the current one lives. Either is
      acceptable; leaving it silent is not.
  - finding: "ROADMAP.md's gap-closure paragraph names 09-UAT.md where every other record names 16-UAT.md"
    severity: warning
    measured: >-
      ROADMAP.md Phase 11 "Gap closure (waves 7-10)" defers GAP 1's device proof to
      "Phase 16 / DIST-03 / `09-UAT.md` tests 2-12". 11-08-PLAN.md:109/123/362/572,
      11-08-SUMMARY.md:273, MANIFEST.md:238 and docs/BUILD-NOTES.md:1222 all name
      16-UAT.md's twelve tests. 09-UAT.md exists but is the Phase 9 instrument.
    human_decision_requested: "One-line ROADMAP correction; no code impact."

deferred:
  - truth: "Redirect occupies Circle 6 in Classic and Ambient"
    addressed_in: "Phase 17"
    evidence: >-
      ROADMAP Phase 11 "Intermediate state to respect". Re-measured: the Config literal in
      BOTH forks holds `Eject` at index 5 of all three sequences and `Redirect` appears 0
      times in either XML. docs/BUILD-NOTES.md §34 now records this as an interim naming
      Phase 17 and the exact two cells that flip.
  - truth: "Circle 8 dispatches the designed Voice primitive rather than the Mirror"
    addressed_in: "Phase 15"
    evidence: >-
      ROADMAP Phase 11. `Loud Mirror` is one of the nine live dispatch branches (11
      renderings per fork, re-counted). docs/BUILD-NOTES.md §34 records it as an interim
      naming Phase 15.
  - truth: "Both forks import onto a real iPhone and complete a first manual run"
    addressed_in: "DIST-03 (open requirement, Phase 8)"
    evidence: >-
      .planning/REQUIREMENTS.md:161 `- [ ] DIST-03` and :331 Pending. 16-UAT.md's
      reachability probe measures `tunnelState: unavailable`, `transportType: none`. No
      iPhone is connected. Every claim in this report is file-level structural.

behavior_unverified_items:
  - truth: "The nine primitives named by BD-06 Decision 3 each PERFORM their intervention when dispatched"
    test: >-
      On an iPhone, drive a Circle whose sequence entry is Dim, and separately one that is
      Silence. Observe the screen actually dims and the media volume actually drops; then
      complete the session and observe both are restored to the value captured before the
      change. Repeat with a force-quit between the apply and the CLOSE.
    expected: >-
      The device changes, state.json holds the captured original BEFORE the change, and the
      original is restored. A failure to restore leaves the user dim or quiet with only iOS
      Settings as recovery.
    why_human: >-
      GAP 1's STRUCTURAL half is closed and verified below -- 0 environmental actions per
      fork remain in a dead arm, negative-controlled. The BEHAVIOURAL half cannot be reached
      from here. .claude/CLAUDE.md §9 "Rung 2's ceiling" is explicit: `Set Brightness`
      cannot succeed on a simulator at all (it returns "There was a problem setting the
      brightness") and `Get Device Details -> Current Brightness` reads `0` there, so a
      simulator reading is never promotable above UNVERIFIED. This phase made 44
      environmental actions per fork reachable FOR THE FIRST TIME; none has ever executed.
      Instrument: 16-UAT.md's twelve tests, all BLOCKED on DIST-03 -- see the stale-pin
      warning above before running them.
  - truth: >-
      Removing Panic Escape requires two deliberate acts -- editing the setting line in the
      Note by hand, then choosing the removal option in an explicit confirmation menu -- and
      the same route restores it
    test: >-
      On an iPhone, edit the `## PANIC ESCAPE` line in the real Apple Note to OFF, run the
      shortcut manually, confirm the removal in the menu, then open a tracked app and check
      the Leaving/Continue menu no longer appears. Reverse it by editing the line back to ON
      and confirming again.
    expected: >-
      The Note edit is detected, the confirmation menu appears, panic_escape_enabled flips,
      and the reverse route restores it. Critically: no path shows "Nothing was changed."
      when the Note in fact says otherwise.
    why_human: >-
      The unattested output name is fixed and verified below. The consumption shape was
      SETTLED at rung 2 (docs/BUILD-NOTES.md §31, booted iOS 26.5 simulator, both candidate
      shapes byte-identical, the load-bearing condition-99 contains test reading TRUE) --
      and that settlement is correctly bounded there to a single-match fixture and to
      nothing about a device. The end-to-end path reads from a real Apple Note, and
      `com.apple.mobilenotes` is absent from the booted simulator's 25 apps, which puts the
      whole Note path inside rung 2's ceiling. Structurally proven; behaviourally untouched.
  - truth: >-
      A second manual run reuses the note it already found rather than creating a second
      one, and a deleted note is recreated with its full body on the next manual run
      (BOOT-08)
    test: >-
      Import a signed fork on an iPhone. Tap it, let it create the Note. Tap it a second
      time. Then delete the Note in the Notes app and tap a third time.
    expected: >-
      No duplicate Note after run 2; state.json unchanged. After deletion, run 3 recreates
      the Note with its FULL body (including `## THE NINE CIRCLES`, `## OPTIONAL HARDENING`,
      `## PANIC ESCAPE`), not a lesser placeholder.
    why_human: >-
      Carried forward unchanged from the first pass. The limit-1 + First Item binding is
      structurally provable and IS proven (docs/note_identity_check.py exit 0, re-run).
      BD-06-A2 widened what the shortened `contains PROSOCHĒ` predicate can match, so a
      leftover `PROSOCHĒ — Control Room` note from an earlier install could be bound
      permanently and silently.
  - truth: >-
      If a manual run is interrupted between the Find-Notes lookup and the append, or two
      runs overlap, the Note can lose an append or gain a duplicated block -- the guarantee
      is at-most-one-note-bound-per-run and nothing stronger
    test: >-
      On device, force-quit Shortcuts mid-manual-run between the Note lookup and the append;
      separately, trigger two manual runs in rapid succession.
    expected: >-
      At most one note bound per run. A lost append or a duplicated block is the accepted,
      documented limit -- not a regression.
    why_human: >-
      Carried forward unchanged. Declared `verification: backstop` in plan 11-03. Shortcuts
      offers no transaction and no lock, so this is a negative runtime property that no
      file-level analysis can confirm or refute. Abstaining rather than asserting.
  - truth: "Aware's Use Model audit runs on Apple-Intelligence-capable hardware, on every OPEN-arm rendering"
    test: >-
      On an iPhone 15 Pro or later, import the Aware fork, reach the Intention (Confession)
      primitive via the normal OPEN path, and again via the panic_escape_enabled == 0 path.
      Observe a contract audit on BOTH.
    expected: >-
      Both renderings produce a model response inside the eight-second gate, using the
      pinned on-device source, with the deterministic fallback taking over if not.
    why_human: >-
      NEW THIS PASS. Plan 11-09 added the second audit block; it is verified present, in the
      OPEN arm, pinned and collision-free below. But .claude/CLAUDE.md §9's rung-2 ceiling
      names Apple Intelligence explicitly: the simulator is not AI-capable hardware. Per
      11-09-SUMMARY.md:306, no Use Model call in either audit block "has EVER run on
      Apple-Intelligence-capable hardware -- it has not, in this plan or any before it."
      16-UAT.md:reachability-probe records the paired device as `iPhone16,1`, which IS
      AI-capable, so this becomes answerable the moment DIST-03 opens.

human_verification:
  - test: "Drive Dim and Silence on a real iPhone and observe capture-and-restore"
    expected: "The device changes, the original is on disk before the change, and it is restored"
    why_human: "Set Brightness cannot execute on a simulator at all — rung 2's ceiling, .claude/CLAUDE.md §9"
  - test: "Remove and restore Panic Escape via a real Apple Note edit plus confirmation"
    expected: "Both directions work; no false 'Nothing was changed.'"
    why_human: "com.apple.mobilenotes is absent from the simulator — the whole Note path is rung 3+"
  - test: "Reach Intention on the Aware fork via both OPEN-arm renderings"
    expected: "A contract audit on each; on-device model source honoured"
    why_human: "Apple Intelligence is inside rung 2's ceiling"
  - test: "Note binding and re-creation (BOOT-08)"
    expected: "No duplicate after run 2; full body recreated after deletion"
    why_human: "Runtime re-binding is not derivable from the plist"
  - test: "Note append atomicity under interruption"
    expected: "At-most-one-note-bound-per-run and nothing stronger"
    why_human: "Negative runtime property; declared verification: backstop"
  - test: "Decide the disposition of 16-UAT.md's stale build-identity pin"
    expected: "Re-pinned to the current digests, or explicitly recorded as superseded"
    why_human: "A maintenance decision about the phase's own device instrument, not a code fact"
---

# Phase 11: Build Addendum 01 — Dante Circle names and the ten-primitive roster — Verification Report

**Phase Goal:** Apply `PROSOCHE_Build_Addendum_01.md` in full, once, against the roster settled
in BD-06 (`docs/CAPABILITY-DECISIONS.md`) — so the rename lands a single time rather than being
re-cut after each of the four in-flight Circle phases.

**Verified:** 2026-08-18
**Status:** human_needed
**Re-verification:** Yes — after gap closure waves 7–10 plus a code review and two fix passes.
The 2026-08-17 first pass is preserved below in full as `## First pass — the record and its
disposition`; nothing it found has been overwritten or softened.

## Standing evidence constraint

**DIST-03 is open. No iPhone is connected.** Re-measured this pass from 16-UAT.md's own
reachability probe: a paired `iPhone16,1` exists, `tunnelState: unavailable`,
`transportType: none`. Every check below is file-level structural (rung 1) except where a rung-2
simulator settlement is cited by name, and no rung-2 result is promoted past the ceiling
`.claude/CLAUDE.md` §9 sets for it. Where this report says VERIFIED it means *the artifact
provably has this shape*, never *the device provably does this*.

**Every number below was re-taken by this verifier from the working tree.** None is transcribed
from a SUMMARY, from `11-REVIEW.md`, or from the orchestrator's dispatch baseline — the baseline
was re-derived independently and agreed.

## Baseline re-measurement

| Measurement | Result |
|---|---|
| `git status --short` (whole tree) | empty |
| Gate A, both forks (`--target-macos 26 --target-platform all`) | `Validation passed.` exit 0 |
| Gate B, both forks (`--target-macos 27 --target-platform all`) | exactly one `WFCreateNoteInput` waiver line per fork, nothing else |
| `docs/*.py` checkers | 12 of 13 exit 0 |
| `docs/retired_clause_check.py` | exit 1 on 4 occurrences, all inside gitignored `graphify-out/` and `.planning/graphs/` — confirmed via `git check-ignore -v`. Pre-existing, separately tracked, absent from a worktree checkout |
| Isolated-copy rebuild (`git archive HEAD` → both builders) | Core `a8d712b091aff9b1549ea7d236c4a15a`, Aware `0dee5197e609ccbc8d59af388d06cede` — byte-identical to the shipped sources |
| Action totals | Core **4304**, Aware **4438** |
| `askllm` | Core **0**, Aware **2** |
| Signed artifacts decrypted (AEA1 → `aea decrypt` → `aa extract`) | Core signed 4304 actions `== src` **True**; Aware signed 4438 actions `== src` **True** |

Both signed containers are current against the sources this phase ships. That is structural
proof that the right bytes shipped and nothing more.

## Gap closure — the five gaps, re-measured

### GAP 1 (CR-01) — `dimming()` / `silence()` unreachable → **CLOSED**

**What the artifact now does.** `tools/build_state_engine.py:735-737` reads the **leaf**
`settings_snapshot.brightness.original_value` and gates it at condition **2** (`> 0`) with a bare
`Nothing` in the TRUE arm and the whole capture-and-apply body in the OTHERWISE arm — the exact
shape and the exact rule `restore_managed_settings()` already used, so capture and restore now
agree on what counts as an outstanding original. Traced in the shipped plist at Core actions
1096–1123: leaf read → `Outstanding Brightness Original` → condition 2 → otherwise → Get Device
Details → capture gate → `set_value` → **save (1116-1117)** → **Set Brightness (1118)**. The
persist-before-apply ordering plan 16-01 established is preserved and is now on a live path.

**Why the gate can read false.** The bootstrap template seeds
`settings_snapshot.{brightness,volume}.original_value` as `"null"` (`CLEARED_SENTINEL`), and
`.claude/CLAUDE.md`'s verified runtime semantics record that `"null"` coerced to
`WFNumberContentItem` is **false, no error**. The dotted read is safe because the container is a
permanent bootstrap invariant (axis 7), and the leaf is present-but-sentinel rather than absent.

**Negative control (run by this verifier, isolated copy).** Reverting the gate to the original
defect shape — container key `settings_snapshot.brightness`, condition **100** — makes the build
exit **1** with a message that names the consequence and enumerates the dead actions:

> `an environmental read or write sits in the never-taken arm of a permanently-true
> settings_snapshot container gate … action 1103: getdevicedetails; action 1118: setbrightness;
> … (22 total)`

**Record corrected, not edited away.** `artifacts/shortcuts/MANIFEST.md:77-125` now states the
defect, quantifies it (**44 environmental actions per fork** previously in the dead arm — 22 Get
Device Details, 11 Set Brightness, 11 Set Volume), states **0 remain**, and explicitly retracts
three older claims a reader might otherwise trust — including the Phase-9-era *"Dimming and
Silence writes now execute where they previously no-opped"* that the first pass flagged as a
false capability statement attached to a distributable artifact. MANIFEST also narrows its own
new claim (IN-01) rather than over-reaching: it discloses that the already-dim short-circuit
inside `dimming()` is itself inert while `dim_target` is `0`, and says why it is retained.

### GAP 2 (CR-02) — the unattested `text.match` OutputName → **CLOSED**

**In the shipped artifacts.** Every `ActionOutput` token resolved back to its producing
identifier: Core carries **2** `text.match` references, Aware **8**, and **all ten** read
`"Matches"`. `"Matched Text"` appears **0 times** in either fork.

**The guard is a normaliser, which is stronger than a detector.**
`ACTION_OUTPUT_NAMES["is.workflow.actions.text.match"] = "Matches"` feeds
`normalise_output_names()`, which repoints every magic-variable reference at the producing
action's real output name. Negative control: injecting `output(match_id, "Matched Text")` at a
consumption site and rebuilding produces a **byte-identical** artifact (`a8d712b0…`). Drift at a
consumption site cannot ship. *Observed limit, recorded not as a gap:* deleting the
`ACTION_OUTPUT_NAMES` row itself is not detected (it also rebuilds byte-identically, because the
source already emits the attested name literally). That is strictly narrower than the original
defect and would require two simultaneous edits to matter.

**Evidence-tier discipline is correct.** `docs/BUILD-NOTES.md` §31 records the consumption-shape
question as **SETTLED at rung 2** on the booted iOS 26.5 simulator, with the verbatim probe
payload, and then bounds it explicitly: the fixture yields exactly one match, the multi-match
case is untested, *"this is a simulator observation and is never promotable above UNVERIFIED for
anything in §9's Rung 2's ceiling list … It says nothing about device behaviour; DIST-03 remains
open."* The section also **retracts** the false "could not be installed" claim the plan first
shipped, names the real cause (the probe skipped the generator's own normalisation pipeline and
so measured itself), and earns a reusable rule from it. This is the behaviour the project's
evidence hierarchy asks for, done unprompted.

### GAP 3 (CR-03) — the Aware fork's Use Model audit on one rendering of two → **CLOSED**

Measured independently, not read from the checker:

| Measurement | Result |
|---|---|
| Core OPEN conditional (`WFCondition` 4, string `OPEN`) | index **92**, `GroupingIdentifier` `FA045F2B…` |
| Core OPEN **arm** bound (mode-1 otherwise) | index **1493** |
| Contract markers inside the OPEN arm | **2** |
| Contract markers fork-wide (arm + the nine Test-a-Circle renderings) | 11 — so the arm bound, not the End-If, is what excludes the MANUAL arm |
| Aware `askllm` actions | **2**, at 1095 and 1413 |
| Both inside Aware's OPEN arm proper (94 → 1627) | **yes** |
| `WFLLMModel` on each | `Apple Intelligence on Device` |
| Audit spans | (1071, 1136) and (1389, 1454) — disjoint, in order |
| UUID overlap between spans | **none** |
| `GroupingIdentifier` overlap between spans | **none** — the `uid()` discriminator the first pass asked for is real |

`docs/sentient_core_check.py:146-160` no longer asserts a literal; it **derives**
`expected_audits` from the Core fork's own OPEN-arm marker count and asserts equality in both
directions, with the consequence of each direction spelled out.

**Two negative controls.** Restoring the `break` in `build_sentient.py`'s insertion loop makes
the **builder** exit 1 (*"the Core fork's OPEN arm has 2 dispatch rendering(s); this build
collected 2 marker(s) and emitted 1 Use Model action(s)"*) and the artifact is never written.
Independently, deleting one `askllm` from a copy of the shipped Aware artifact makes the
**standalone checker** exit 1 with the same derivation. The defect is caught at the write and at
the audit.

### GAP 4 (WR-01) — `verify_panic_escape_seed()` vacuous under rename → **CLOSED**

The guarded set is now resolved **by provenance**, not by a bare name literal. Measured by
importing the generator and running its own helpers against the shipped Core artifact:

- `_panic_escape_variables()` → `{'Panic Escape Enabled', 'Panic Escape Stored'}`
- gates over that provenance: **3** — action 529 (`Panic Escape Enabled`, cond 2), 4248 and 4268
  (`Panic Escape Stored`, cond 2). The first pass's literal covered **one** of these three.
- the set is asserted non-empty, so an orphaning rename fails rather than passing.

**The first pass's exact negative control now fails closed.** Renaming *only* the emitter's
variable to `PE` and flipping its gate to condition 100 — leaving every guard literal untouched —
made the build exit **1**:

> `a Panic Escape gate uses a non-numeric condition code action 529: 'PE' at condition 100 — the
> variable is read from 'panic_escape_enabled', and an existence test reads TRUE for the string
> "null" and for an empty string …`

**Beyond the gap: the phase's only `critical` threat now has an executable guard.** Plan 11-10
added `verify_panic_escape_isolation()` for **T-11-22** — Emergency Restore must never be
enclosed by a Panic Escape conditional. The first pass verified this by hand-measurement; it is
now a build gate, and 11-08's reachability fix is exactly what made the stranding state
materially reachable. Negative-controlled in both directions by this verifier:

| Control | Result |
|---|---|
| Baseline on the shipped artifact | passes; 4 Emergency Restore surfaces (171, 174, 1619, 4075), 0 enclosed |
| Inject a well-formed `Emergency Restore` menu **inside** the Panic Escape group span | exit 1, naming both the `WFMenuItems` surface and the case title and the enclosing group |
| Delete **every** Emergency Restore surface | exit 1 — *"SAFE-05's safety hatch has been removed"*, rather than reporting the remaining zero as un-enclosed |

*Observation, not a finding:* a mutation that moves the group's End-If past a surface without
re-nesting the intervening blocks is not reported, because `enclosing_groups()` is a stack walk
and the mutation produces improperly-nested control flow. The generator emits properly nested
blocks by construction and `verify_group_identifier_uniqueness()` covers the endpoint-ownership
axis, so this is not live.

### GAP 5 (WR-02) — interims not named in `docs/BUILD-NOTES.md` → **CLOSED**

`docs/BUILD-NOTES.md` **§34** records both interims, with a three-record cross-reference table so
each of the generator comment, the config mirror and the build note names the other two. `Loud
Mirror` → **replaced by Phase 15**, with the ROADMAP semantics quoted. `Eject` at Circle 6 →
**replaced by Phase 17**, naming the exact cells that flip and noting `BlackMirror[5]` does not
move. The section closes by stating that neither interim has ever run on a phone and that
naming Phase 15/17 is a statement about the ROADMAP, not a device fact.

## Goal Achievement

### Observable Truths

Row numbering is identical to the 2026-08-17 pass so the two reports diff line for line.

| # | Truth | First pass | Now | Evidence |
|---|-------|-----------|-----|----------|
| 1 | Intervention rename per Addendum §5 reaches both signed artifacts | ✓ | ✓ VERIFIED | Re-counted per fork: `Pause` ×36, `Loud Mirror` ×25, `Black and White` ×47, `Frozen` ×26; retired `Knock` ×0, `Ash` ×0. Signed payloads action-array-equal to source, both forks |
| 2 | BD-06 Decision 4's slot table applied to all three sequences, in the Phase-11 intermediate state | ✓ | ✓ VERIFIED | Config literal parsed from both plists. Classic / BlackMirror / Ambient each 9 names; `Eject` at index 5 in all three; `Redirect` ×0 |
| 3 | Dispatch is exact-match; every sequence entry resolves to exactly one branch and every branch is named | ✓ | ✓ VERIFIED | **99** `Selected Primitive` conditionals per fork, **all condition code 4**, 0 at 99. 9 branch names × 11 renderings each. Bijection holds |
| 4 | The dispatch-coverage build guard is a hard gate written in this phase | ✓ | ✓ VERIFIED | `docs/sequence_dispatch_check.py` exit 0; first pass's three negative controls stand un-regressed |
| 5 | Circle 8 dispatches a real branch in all three sequences (interim) | ✓ | ✓ VERIFIED | `Loud Mirror` live, 11 renderings. Interim now labelled in all three required places — see truth 20 |
| 6 | The Apple Note's user-facing title is the bare product name at all three identity sites | ✓ | ✓ VERIFIED | `docs/note_identity_check.py` exit 0, both forks |
| 7 | Dante's nine names are surfaced positionally from one generator constant | ✓ | ✓ VERIFIED | Re-measured: `WFMenuItems` and the mode-1 case titles are `['Circle 1 · Limbo' … 'Circle 9 · Treachery']`, **equal element-for-element in order** |
| 8 | The Note explains the optional Shortcuts-app hardening | ✓ | ✓ VERIFIED | `## OPTIONAL HARDENING` present in both fork bodies |
| 9 | BD-06-A1's profile rename Limbo→Purgatory landed completely | ✓ | ✓ VERIFIED | Both forks: `thresholds` and `cooldown_seconds` keys are `[Paradise, Purgatory, Inferno]`. No `Limbo` profile key survives; all 3 remaining `Limbo` occurrences per fork are Circle-1 positional names |
| 10 | The schema_version disposition is recorded, and the bump applied | ✓ | ✓ VERIFIED | Bootstrap template carries `"schema_version": 4` (bumped again by Phase 16 since the first pass); no migration or dual-key alias built |
| 11 | Panic Escape is gated on a first-class flat state field, read numerically | ✓ | ✓ VERIFIED | `panic_escape_enabled` seeded top-level as `1`; flat read; **all three** gates at condition 2, now provenance-resolved rather than name-matched |
| 12 | Emergency Restore is reachable on every path and is enclosed by no Panic Escape conditional (T-11-22 — the phase's only `critical`) | ✓ | ✓ VERIFIED **and upgraded** | 4 surfaces per fork, **0 enclosed**. No longer a hand-measurement: `verify_panic_escape_isolation()` is a build gate, negative-controlled in both directions by this verifier |
| 13 | Both variants ship under their new canonical names with no suffix | ✓ | ✓ VERIFIED | `docs/manifest_check.py` exit 0; six rows SHA-256-verified against disk |
| 14 | Each fork's Note names its own variant as the Run Shortcut target | ✓ | ✓ VERIFIED | `docs/sentient_core_check.py` exit 0 — own ×2, other ×0, both forks |
| 15 | Both builders are idempotent, all structural checks pass, and both forks validate at the iOS 26 target | ✓ | ✓ VERIFIED | Isolated-copy rebuild reproduces both shipped sources byte-for-byte. 12/13 checkers exit 0 (13th is the gitignored-graphify pre-existing). Gate A clean both forks. `git status` clean |
| 16 | The nine primitives named by BD-06 Decision 3 each **perform** their intervention when dispatched | ✗ FAILED | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | **GAP 1 closed structurally** — 0 of 44 environmental actions per fork remain in a dead arm, guard negative-controlled. But "perform" is device behaviour and `Set Brightness` cannot execute on a simulator at all (rung 2's ceiling). Not verified, and deliberately not manufactured |
| 17 | Removing Panic Escape requires a manual Note edit plus explicit confirmation, and the same route restores it | ✗ FAILED | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | **GAP 2 closed** — `Matches` at all 10 references, 0 `Matched Text`; consumption shape settled at rung 2 and correctly bounded. But the end-to-end path reads a real Apple Note, and `com.apple.mobilenotes` is absent from the simulator |
| 18 | `docs/sentient_core_check.py` proves Aware is an additive fork of Core on every path | ✗ FAILED | ✓ VERIFIED | **GAP 3 closed.** 2 OPEN-arm renderings, 2 audits, 2 `askllm`, both on-device-pinned, disjoint spans, no identifier collision. Derived assertion; negative-controlled at builder and checker |
| 19 | The guards this phase's value rests on are real guards that fail closed | ⚠️ PARTIAL | ✓ VERIFIED | **GAP 4 closed.** The first pass's own precise negative control now exits 1. Guarded set 1 → 3 gates, provenance-resolved, asserted non-empty. Two further guards added and negative-controlled here (`verify_environmental_reachability`, `verify_panic_escape_isolation`) |
| 20 | Each interim stand-in is named as interim in the generator AND in `docs/BUILD-NOTES.md` | ⚠️ PARTIAL | ✓ VERIFIED | **GAP 5 closed.** BUILD-NOTES §34, both interims, replacing phases named, three cross-referencing records |
| 21 | Aware's status display and note settings block report its own fork label | ⚠️ PARTIAL | ⚠️ PARTIAL (accepted) | Unchanged and unchanged deliberately. The load-bearing `- Fork:` line is correct. Two non-load-bearing sites still say the other fork — confirmed this pass: `WFWorkflowActions[0]`'s header comment reads `(Dumb fork)` on both forks, and the Aware Note's `- AI: not used by this fork`. Both self-reported in `deferred-items.md` with the reason each fix is design work rather than a string edit. Neither is an automation target, state key or lookup predicate |

**Score:** **18/21** truths verified. **2** present-but-behaviour-unverified (rows 16, 17).
**1** accepted partial (row 21, documented deferral).

Rows 16 and 17 are the honest cost of DIST-03 and are **not** regressions: both moved from
FAILED to present-and-wired. What they did not move to is *proven on a phone*, and this report
declines to promote a structural fix into a behavioural claim.

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|--------------|----------|
| 1 | `Redirect` occupies Circle 6 in Classic and Ambient | Phase 17 | Config literal re-parsed: `Eject` at index 5 ×3, `Redirect` ×0. BUILD-NOTES §34 names the two cells |
| 2 | Circle 8 dispatches the designed Voice primitive | Phase 15 | `Loud Mirror` live ×11. BUILD-NOTES §34 |
| 3 | Device import + first manual run | DIST-03 (open) | REQUIREMENTS.md:161/:331 Pending; 16-UAT reachability probe `tunnelState: unavailable` |

### Key Link Verification

| From | To | Via | First pass | Now |
|------|-----|-----|-----------|-----|
| `primitive_dispatch()` name tuple | 99 `Selected Primitive` conditionals | `if_block(…, 4, string=name)` | ✓ WIRED | ✓ WIRED — 9 × 11, all code 4 |
| Dispatch branches | `sequences` arrays in the Config literal | `verify_dispatch_coverage()` | ✓ WIRED | ✓ WIRED |
| `src/PROSOCHE-Dumb.xml` | `src/PROSOCHE-Sentient.xml` | `tools/build_sentient.py` | ✓ WIRED | ✓ WIRED — isolated rebuild byte-identical |
| `CIRCLE_NAMES` | Test-a-Circle `WFMenuItems` → case titles | `circle_label()` | ✓ WIRED | ✓ WIRED — equal in order |
| Create Note `name` | Find-Notes lookup predicate | `note_identity_check` | ✓ WIRED | ✓ WIRED |
| `DISPLAY_NAMES` | MANIFEST rows → files on disk | `manifest_check.py` | ✓ WIRED | ✓ WIRED |
| `## PANIC ESCAPE` Note line | text-match read → confirmation menu → `panic_escape_enabled` | `text.match` → `getitemfromlist[First Item]` | ✗ NOT WIRED | ✓ **WIRED** — `Matches` ×10, `Matched Text` ×0; first-item chain at both sites |
| OPEN-arm dispatch renderings | Aware `audit_block()` | derived marker insertion in `build_sentient.py` | ✗ PARTIAL | ✓ **WIRED** — 2 of 2, negative-controlled |
| `settings_snapshot.<x>` leaf gate | Set Brightness / Set Volume writes | numeric `> 0` on the captured original | ✗ NOT WIRED | ✓ **WIRED** — traced 1096→1118, save at 1116-1117 precedes the apply |
| Captured original | `state.json` (persisted before the device changes) | `save_state()` inside the applying arm | — | ✓ WIRED — `verify_capture_persistence()` still armed and the ordering is now on a live path |
| 16-UAT.md build-identity pin | the shipped signed artifacts | SHA-256 in 16-UAT.md:53-54 | — | ⚠️ **STALE** — see Warnings |

### Behavioural Spot-Checks

| Behaviour | Command | Result | Status |
|-----------|---------|--------|--------|
| Structural checkers pass | `python3 docs/<each>.py` | 12/13 exit 0 | ✓ PASS |
| Both forks validate at the iOS 26 target | gate A, both forks | `Validation passed.`, exit 0 | ✓ PASS |
| Gate B advisory shape unchanged | gate B, both forks | exactly one `WFCreateNoteInput` waiver each | ✓ PASS |
| Builders idempotent and reproduce the shipped sources | `git archive HEAD` → isolated rebuild → md5 | `a8d712b0…` / `0dee5197…`, identical | ✓ PASS |
| Signed artifacts decrypt and match source | `aea decrypt` → `aa extract` → plistlib | 4304 / 4438, `==` **True** both forks | ✓ PASS |
| Environmental dead-arm reverted | patch `dimming()` back to container/cond-100, rebuild | build exit 1, 22 actions named | ✓ PASS (guard fires) |
| Panic-escape emitter renamed + gate flipped to 100 | patch emitter only, leave guards | build exit 1, correct message | ✓ PASS (first pass's WR-01 control now caught) |
| Single-audit `break` restored | patch `build_sentient.py` insertion loop | build exit 1, artifact not written | ✓ PASS |
| One `askllm` deleted from the shipped Aware artifact | run `sentient_core_check.py` on the mutant | exit 1, derived expectation | ✓ PASS |
| Emergency Restore surface enclosed by a Panic Escape group | inject a well-formed menu inside the span | exit 1, both surfaces named | ✓ PASS |
| Every Emergency Restore surface deleted | strip all 4 surfaces | exit 1, "safety hatch has been removed" | ✓ PASS |
| `ACTION_OUTPUT_NAMES` normalisation is self-healing | inject `"Matched Text"` at a consumption site, rebuild | artifact byte-identical | ✓ PASS |
| `ACTION_OUTPUT_NAMES` row deleted | remove the entry, rebuild | artifact byte-identical, build exit 0 | ℹ️ INFO — not detected; strictly narrower than the original defect |
| `text.match` OutputNames in the shipped forks | resolve every `ActionOutput` to its producer | `Matches` ×10, `Matched Text` ×0 | ✓ PASS |
| Panic-escape provenance coverage | `_panic_escape_variables()` + gate scan | 2 variables, 3 gates, all condition 2 | ✓ PASS |
| Emergency Restore enclosure (baseline) | enclosure walk, both forks | 4 surfaces, 0 enclosed | ✓ PASS |
| Duplicate action UUIDs, Aware | whole-artifact UUID count | 1 — `792D1640-…`, the documented deferral | ℹ️ INFO (tracked in `deferred-items.md`) |
| 16-UAT pin vs disk | `shasum -a 256` on both signed artifacts | mismatch on both | ✗ FAIL → Warning |

**Device behaviour: not tested — DIST-03 open, no iPhone connected.** No spot-check above starts
a service, mutates repository state, or touches a device. Every negative control was run in a
`git archive HEAD` copy under the scratchpad; the working tree was verified clean before and
after.

### Requirements Coverage

All eight declared IDs are claimed by at least one plan and all eight resolve to evidence.
Cross-referenced against `.planning/REQUIREMENTS.md`.

| Requirement | Source plans | Description | Status | Evidence |
|-------------|--------------|-------------|--------|----------|
| AUDIT-02 | 11-02, 11-04, 11-05 | Grayscale / Color Filters resolved to go/no-go with a documented Ash fallback | ✓ SATISFIED | `Black and White` is a live dispatch branch, 11 renderings per fork; BD-06-A3 recorded; fallback design in CAPABILITY-DECISIONS.md |
| CIRC-02 | 11-01, 11-02 | Ash applies the audited visual-salience reduction or its documented fallback | ✓ SATISFIED | Renamed to `Black and White`; dispatches at condition 4 in all three sequences |
| CIRC-06 | 11-02, 11-05, 11-08, 11-10 | Exile immediately routes to an exit without a permission prompt | ✓ SATISFIED | `Eject` at Circle 6 in all three sequences, resolving to `exile()` (`returntohomescreen`, no prompt). Routed `Redirect` deferred to Phase 17 per ROADMAP |
| CIRC-08 | 11-02, 11-08, 11-10 | The Voice speaks the Mirror at most once per run, only when voice is enabled, never at unsafe levels | ✓ SATISFIED (interim) | `Loud Mirror` → `mirror_and_voice()` with the once-per-run and voice-enabled gates. Designed primitive deferred to Phase 15; **now labelled interim in the generator, CONFIG-BLOCK.md and BUILD-NOTES §34** |
| ROOM-01 | 11-01, 11-03 | The Note opens with READ THIS FIRST explaining PROSOCHĒ and both automations | ✓ SATISFIED | `## READ THIS FIRST` asserted by `note_identity_check.py` (exit 0); `## THE NINE CIRCLES` and `## OPTIONAL HARDENING` present |
| ROOM-02 | 11-03, 11-06 | The Note gives exact steps for Automation A | ✓ SATISFIED | Each fork's Note names its own Run Shortcut target ×2, the other ×0 (`sentient_core_check.py` exit 0) |
| DIST-01 | 11-01, 11-03, 11-05, 11-06, 11-07, 11-08, 11-09, 11-10 | Both forks pass the validator at the iOS 26 target | ✓ SATISFIED | Gate A re-run this pass: `Validation passed.`, exit 0, both forks |
| DIST-02 | 11-01, 11-04, 11-06, 11-07, 11-08, 11-09 | Both forks sign successfully into importable `.shortcut` files | ✓ SATISFIED (structural) | Both signed artifacts present, non-zero, decrypt cleanly and match source exactly; `manifest_check.py` exit 0. **"Importable" here is structural — DIST-03 is the device half and is open** |

**Orphaned requirements: none.** `.planning/REQUIREMENTS.md` maps no additional ID to Phase 11
that no plan claims.

**Adjacent, not declared:** DIST-04 (forks named unambiguously and distinguishable at import) is
asserted by `docs/manifest_check.py` and passes; the Core/Aware rename satisfies it.

**Requirement-status honesty note.** REQUIREMENTS.md marks DIST-02 `- [x]` while DIST-03 is
`- [ ]`. That split is correct and is the reason DIST-02 can be SATISFIED above without this
report claiming anything about a phone.

### Anti-Patterns Found

Scanned the fourteen non-generated source and doc files this phase modified.

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | `TBD` / `FIXME` / `XXX` debt markers | — | **None found.** Clean across all phase-modified files |
| — | — | `TODO` / `HACK` / `PLACEHOLDER` | — | **None found** |
| `.planning/phases/16-*/16-UAT.md` | 53-54 | Stale build-identity pin against re-signed artifacts | ⚠️ Warning | The phase's own named device instrument cannot be run as written; fails safe |
| `.planning/ROADMAP.md` | Phase 11 gap-closure paragraph | Names `09-UAT.md` where every other record names `16-UAT.md` | ⚠️ Warning | Doc drift only |
| `tools/build_state_engine.py` | `ACTION_OUTPUT_NAMES` | Guard-table row whose own deletion is undetected | ℹ️ Info | Requires two simultaneous edits to matter; strictly narrower than the closed defect |
| `src/PROSOCHE-*.xml` | action 0 | Aware's header comment still reads `(Dumb fork)` | ℹ️ Info | Non-load-bearing; recorded in `deferred-items.md` with the reason |
| both forks | — | Duplicate action UUID `792D1640-…` | ℹ️ Info | Pre-existing, both forks, documented in `deferred-items.md` with a proposed fix shape |

The three residual findings the fixer left open — **R-1** (provenance does not survive a round
trip through a dictionary), **R-2** (`_tested_variable()` reads one gate shape), **R-3**, **R-4** —
were checked against the shipped build rather than accepted on the record. R-1 is real and
correctly described, and it is **latent, not live**: every Panic Escape gate in the shipped
artifact reads directly from `State` with no dictionary round trip, which is why
`_panic_escape_variables()` resolves all three. R-2 is likewise latent — 0 `WFConditions`
multi-condition conditionals exist in either fork. Naming these rather than shipping a half fix
described as a class fix is the correct call and this verifier endorses it.

### Human Verification Required

Six items. Five are device-gated by DIST-03; one is a maintenance decision.

#### 1. Dim and Silence actually intervene, and restore

**Test:** On an iPhone, drive a Circle whose entry is `Dim`, and separately one that is
`Silence`. Watch the screen dim and the media volume drop. Complete the session and watch both
restore. Repeat with a force-quit between the apply and the CLOSE.
**Expected:** The device changes; `state.json` holds the captured original *before* the change;
the original is restored.
**Why human:** `.claude/CLAUDE.md` §9 — `Set Brightness` cannot succeed on a simulator at all,
and `Get Device Details → Current Brightness` reads `0` there, so a simulator reading is never
promotable above UNVERIFIED. **This phase made 44 environmental actions per fork reachable for
the first time; not one of them has ever executed anywhere.** Instrument: `16-UAT.md`'s twelve
tests — resolve the stale pin first.

#### 2. Panic Escape removal and restoration, end to end

**Test:** Edit the `## PANIC ESCAPE` line in the real Apple Note to OFF, run manually, confirm
in the menu, then open a tracked app. Reverse it.
**Expected:** Both directions work. Critically, no path reports *"Nothing was changed."* when the
Note says otherwise.
**Why human:** `com.apple.mobilenotes` is absent from the booted simulator, so the whole Note
path is rung 3+. The rung-2 settlement covers the `text.match` consumption shape against a
synthetic fixture and explicitly nothing more.

#### 3. Aware's contract audit on both OPEN-arm renderings

**Test:** On an iPhone 15 Pro or later, reach Intention via the normal OPEN path and again via
the `panic_escape_enabled == 0` path.
**Expected:** A contract audit on both; on-device model source honoured; the deterministic
fallback takes over if the eight-second gate expires.
**Why human:** Apple Intelligence is inside rung 2's ceiling. No Use Model call in either audit
block has ever run on capable hardware, in this plan or any before it. The paired device is
`iPhone16,1`, which *is* capable — this becomes answerable the moment DIST-03 opens.

#### 4. Note binding and re-creation (BOOT-08)

Carried forward unchanged from the first pass. See `behavior_unverified_items`.

#### 5. Note append atomicity under interruption

Carried forward unchanged; declared `verification: backstop`. See `behavior_unverified_items`.

#### 6. Disposition of `16-UAT.md`'s stale build-identity pin

**Decision needed:** re-pin `16-UAT.md:53-54` to Core
`873fa3dbda7b1f3440bfc76997c2962198ddec2052096833787547b52f129f10` / 231148 bytes and Aware
`4b7c2cfbddf0dccf47ef8e34209378faf14ca2d760dc089013d3b033ebd2ada0` / 238095 bytes; or record
explicitly that the pin is superseded and where the current one lives. **Not** a code change and
**not** a blocker — but leaving it silent would mean the phase's own named device instrument
points at a build that no longer exists, with nothing saying so.

## Verdict

**The five gaps are closed, and closed properly rather than papered over.** Each was
independently re-measured, and each of the four that has a guard behind it was negative-controlled
by this verifier against the exact defect shape it was written to catch — including the first
pass's own precise WR-01 control, which now exits 1 where it previously exited 0 with every
checker green. Two of the closures went further than the gap required: T-11-22, the phase's only
`critical`, moved from a hand-measurement recorded in prose to an executable build gate that
fails closed in both directions; and the Aware audit assertion moved from a literal `== 1` that
*pinned* the defect to a count *derived* from the Core fork's own OPEN arm.

**No regressions.** All fifteen truths the first pass verified were re-taken from the working
tree and all fifteen hold. The forks rebuild byte-identically from a clean `git archive HEAD`,
both signed containers decrypt to exactly the shipped sources, gate A is clean, gate B's waiver
is still exactly one line per fork, and the working tree is clean.

**The record is honest about what it does not know, and that is the strongest signal here.**
`BUILD-NOTES` §31 retracts a false claim the phase itself shipped and says why the first probe
taught nothing. MANIFEST retracts three older capability claims and then *narrows its own new
one* rather than over-reaching. Every wave-7–10 summary opens its device section with "nothing in
this plan is device-verified, and nothing claims to be" and then enumerates what is specifically
**not** claimed. `11-REVIEW-FIX.md` names R-1 as measured-and-open rather than shipping a half
fix as a class fix. `deferred-items.md` names a duplicate UUID nothing currently detects and
states plainly that its harmlessness was not investigated. This is the evidence hierarchy being
applied against the phase's own interests, repeatedly.

**Why this is `human_needed` and not `passed`.** The phase's central behavioural change — making
Dim and Silence reach the device at all — is precisely the class `.claude/CLAUDE.md` §9 puts
beyond a simulator's ceiling, and DIST-03 is open. Truths 16 and 17 are present, wired and
guarded; they are not proven, and promoting the structural fix into a behavioural pass would be
exactly the inversion this project forbids. Prior phases returned the same verdict for the same
reason, and doing so again is the accurate answer rather than a failure.

**Recommendation.** Nothing here blocks Phase 12. Before anyone takes a phone to `16-UAT.md`,
re-pin its two digests — that file is now the only instrument standing between a live
capture-and-restore loop and a user left on a screen they cannot read.

---

## First pass — the record and its disposition

Preserved verbatim in substance from `11-VERIFICATION.md` as written 2026-08-17T13:10:00Z, so
what was found then remains auditable independently of what was fixed since.

**Status then:** `gaps_found`. **Score then:** 13/18. **Truths failed:** 3 (rows 16, 17, 18).
**Partials:** 3 (rows 19, 20, 21).

| First-pass finding | Its disposition now |
|---|---|
| **CR-01** — `dimming()`/`silence()` bodies unreachable behind a permanently-true `settings_snapshot` container gate at condition 100; MANIFEST:195 advertised the writes as live; `EXPECTED_SITES` certified dead code | **CLOSED** by 11-08. Leaf-gated at condition 2, body reachable, `verify_environmental_reachability()` armed on both builders with no exemption set and negative-controlled here. MANIFEST corrected *and* retracts its own earlier claim rather than editing it away. The site tables now certify live code |
| **CR-02** — the Panic Escape removal path read `text.match` as `"Matched Text"` (corpus 15/0 against it); failure mode was a confident, wrong, unlogged *"Nothing was changed."* | **CLOSED** by 11-07. `Matches` at all ten references across both forks, 0 `Matched Text`; the identifier is in `ACTION_OUTPUT_NAMES` so `normalise_output_names()` now self-heals any future drift at a consumption site; the residual consumption-shape question was then settled at rung 2 with correct bounding and an explicit retraction |
| **CR-03** — 11 renderings, 11 markers, exactly 1 `askllm`; removing Panic Escape silently turned Aware into Core; `assert len(models) == 1` pinned the defect | **CLOSED** by 11-09. The OPEN arm is bounded structurally at the mode-1 otherwise (2 markers, not 11), Aware carries 2 audits inside it, both pinned on-device, spans disjoint, no UUID or `GroupingIdentifier` collision. The assertion is derived from Core and negative-controlled at both the builder and the checker |
| **WR-01** — `verify_panic_escape_seed()` matched a bare literal and passed vacuously under an emitter rename; covered 1 of 3 gates | **CLOSED** by 11-10. Provenance-resolved via `_read_variable_keys()`, guarded set asserted non-empty, 3 of 3 gates covered, and the first pass's exact negative control now fails the build. `verify_panic_escape_isolation()` added on top for T-11-22 |
| **WR-02** — neither interim named as interim in `docs/BUILD-NOTES.md`, which the 11-02 prohibition names | **CLOSED**. BUILD-NOTES §34, both interims, Phase 15 and Phase 17 named, three mutually-referencing records, and an explicit statement that neither has run on a phone |
| **Row 21** — two non-load-bearing Aware fork labels still read the other fork | **UNCHANGED, accepted.** Self-reported in `deferred-items.md` with the reason each is design work rather than a string edit. Confirmed still present this pass |
| **`note_identity_check.py:84`** — `MINIMUM_TOKEN_STRINGS = 775` against a measured 1205/1209 | Still slack; still a floor guard rather than an equality guard. Not re-raised as a gap — it was a first-pass warning and its disposition is unchanged |
| **Two behaviour-unverified items** (BOOT-08 note binding; note append atomicity) | **CARRIED FORWARD unchanged**, joined by three more this pass (rows 16, 17, and the Aware model path) |

The first pass's closing judgment — *"Tasks completed; the rename goal achieved; the addendum
goal not"* — is now superseded on its second clause. Addendum §3, the half that did not land, has
landed: the removal path reads an attested output name through a confirmed chain, and its guard
can see a third site if one ever appears.

---

_Verified: 2026-08-18T16:20:00Z_
_Verifier: Claude (gsd-verifier), re-verification after gap-closure waves 7–10_
_Evidence tier: rung 1 throughout, plus one cited rung-2 settlement that is not promoted. No device evidence. DIST-03 open._
