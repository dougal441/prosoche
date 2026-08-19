---
phase: 14-ash-as-real-color-filters-grayscale
plan: 03
subsystem: user-facing-copy-and-distribution
tags: [accessibility, disclosure, color-filters, control-room-note, plist-round-trip, signing, manifest, uat, roadmap, audit-02, safe-02, safe-05, circ-02]

# Dependency graph
requires:
  - phase: 14-ash-as-real-color-filters-grayscale
    plan: "01"
    provides: "the emitted Color Filters primitive and the live safety.ash_managed_color_filters kill switch this plan discloses, and the 15-site AX census the manifest and capability record now carry"
  - phase: 14-ash-as-real-color-filters-grayscale
    plan: "02"
    provides: "docs/gate_a_residue_check.py as the gate-A obligation, DEV-08, and the handed-over finding that artifacts/shortcuts/MANIFEST.md still asserted a clean gate A"
  - phase: 16-environmental-capture-persistence
    provides: "docs/retired_clause_check.py's supersession-by-pointer model, and 16-UAT.md as the instrument this one batches with"
provides:
  - "the Control Room Note tells the user plainly that PROSOCHĒ turns Color Filters on and off, names the kill switch and its shipped default, and says where to change it"
  - "the Note's Emergency Restore promise covers colour alongside a dim screen and a lowered volume"
  - "src/CONFIG-BLOCK.md asserts one thing about this primitive instead of two contradictory ones, and has a field-reference row for the kill switch"
  - "docs/CAPABILITY-DECISIONS.md BD-01-R2 records the decision as SHIPPED, with the census and the three divergences from what it anticipated"
  - "two signed forks under their exact display names, decrypt-verified, matching refreshed manifest rows"
  - "the full static suite green for the first time this phase — fourteen checkers, manifest included"
  - "14-UAT.md — an honest, unrun device instrument with the force-quit test first"
  - "ROADMAP Phase 14 describes what shipped; backlog phase 999.3 retired"
affects: [phase-15-voice, phase-19-nine-circle-sweep, ship-gate, 16-UAT-session]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "supersession applied at the SITE as well as at the top: a dated provenance measurement is retained unedited and given an inline pointer, never rewritten to match a later reality"
    - "a disclosure states the SHIPPED DEFAULT of a mutable setting and never its current value — the guarded round trip forbids the placeholder a live value would need, and a static claim about a mutable value goes stale on the first edit"
    - "a device instrument ordered by VALUE rather than by code order, with the single highest-value observation first and every outcome blank"

key-files:
  created:
    - .planning/phases/14-ash-as-real-color-filters-grayscale/14-UAT.md
    - artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Core-113713.xml
    - artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Aware-113713.xml
  modified:
    - src/PROSOCHE-Dumb.xml
    - src/PROSOCHE-Sentient.xml
    - src/CONFIG-BLOCK.md
    - docs/CAPABILITY-DECISIONS.md
    - artifacts/shortcuts/MANIFEST.md
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut
    - .planning/ROADMAP.md

key-decisions:
  - "The five gate-A cells in MANIFEST.md were RETAINED UNEDITED with an inline supersession pointer rather than corrected in place. Each was a true measurement of the build it describes; rewriting a dated provenance measurement to match a later reality would corrupt the record twice over. The plan handed over four; the independent sweep found five."
  - "The disclosure names no Circle number. Which Circle fires Black and White depends on the chosen sequence — Classic 2, BlackMirror 3, Ambient 1 — so naming Circle 2 would have been false under two of the three sequences. The Note's own neighbouring paragraph already makes this point."
  - "The disclosure names no fork. build_sentient.py's fix_fork_strings() asserts EXACTLY 2 occurrences of the Core display name in the Note body; a third would have aborted the Aware build. Avoiding the fork name entirely was both safer and more accurate, since the same prose ships in both forks."
  - "The stated 238-text-token baseline is not reproducible under any counting basis measured here and was not adopted. What was preserved and asserted instead: the count is UNCHANGED by this plan's edit (249 -> 249 WFTextActionText tokens per fork, measured at the wave-1 base commit, at HEAD before the edit and after), and every one passes assert_offsets_match in both forks."
  - "The three ROADMAP plan-list checkboxes were ticked and then deliberately reverted in a follow-up commit: plan-progress state is the orchestrator's to write, and this plan's ROADMAP scope is the goal-block prose plus the 999.3 retirement."

patterns-established:
  - "Site-level supersession pointer: where a document stacks dated blocks and an older block's claim would read as current, add a short inline pointer at the claim rather than editing the claim or relying on the top block alone. A reader skimming an old block meets the correction where the false reading would form."
  - "Disclosure-by-default-not-by-value: state what a setting SHIPS as and where to change it. A preserved literal cannot carry a live value without a placeholder, and the round trip forbids introducing one."
  - "Device instrument ordered by consequence: the test that stands between a user and an unrecoverable state goes first, with its reasoning stated at the test rather than in a preamble."

requirements-completed: [AUDIT-02, SAFE-02, SAFE-05, CIRC-02]

coverage:
  - id: D1
    description: "The Control Room Note in BOTH forks names Color Filters, names the kill switch key and its shipped default, and retains an Emergency Restore sentence now covering colour"
    requirement: "SAFE-02"
    verification:
      - kind: integration
        ref: "plan 14-03 Task 1 verify — plistlib parse of both forks: 'color filters', 'ash_managed_color_filters' and 'emergency restore' all present in the located Note body; asserted on the parsed artifact, not by grepping raw XML"
        status: pass
      - kind: integration
        ref: "decrypt-verify of both signed containers — the recovered Shortcut.wflow Note body carries the disclosure and the kill-switch key in what actually shipped"
        status: pass
    human_judgment: false
  - id: D2
    description: "Every text token in both forks passes the round trip's offset assertion after the edit, and the replacement introduced no new placeholder"
    requirement: "SAFE-02"
    verification:
      - kind: unit
        ref: "tools/plist_text_edit.py replace_in_token() — asserts offsets before, asserts no U+FFFC in the replacement, rebuilds attachmentsByRange, asserts offsets after; attachments moved 8555/8586 -> 9679/9710"
        status: pass
      - kind: integration
        ref: "249 WFTextActionText tokens per fork pass assert_offsets_match in both forks; docs/note_identity_check.py exits 0 across 1115 (Core) / 1123 (Aware) whole-document token strings"
        status: pass
    human_judgment: false
  - id: D3
    description: "src/CONFIG-BLOCK.md asserts one thing about this primitive, has a field-reference row for the kill switch, retains the historical reversed-decision paragraph, and gained a dated changelog line"
    requirement: "AUDIT-02"
    verification:
      - kind: unit
        ref: "plan 14-03 Task 1 verify — kill switch present in the Field reference section, no surviving 'stays green' assertion, no macOS twin literal anywhere in the file"
        status: pass
      - kind: unit
        ref: "independent sweep of the file, ten search terms — one further asserting site found beyond the plan's inventory and corrected; terms and findings recorded below"
        status: pass
    human_judgment: false
  - id: D4
    description: "Both forks re-signed under their exact display names with no suffix, decrypt-verified against their sources, matching refreshed manifest rows"
    requirement: "CIRC-02"
    verification:
      - kind: integration
        ref: "python3 docs/manifest_check.py — exit 0, 6 rows verified against disk, including the DIST-04 display-name assertion"
        status: pass
      - kind: integration
        ref: "AEA1 decrypt of both signed containers — identifier sequence identical to source action-for-action (Core 4396, Aware 4530), 15 AX sites each, WFWorkflowName stripped by the signer"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every script in docs/ exits 0 — the residue checker and the manifest check included — and pinned counts are unmoved"
    requirement: "CIRC-02"
    verification:
      - kind: integration
        ref: "14 of 14 docs/*.py exit 0 at fe30bf1; setbrightness 15, setvolume 15, getdevicedetails 22 in both forks; AX census 15 per fork, 11 on + 4 off, equal across forks"
        status: pass
    human_judgment: false
  - id: D6
    description: "The screen actually goes black and white, colour actually comes back, and Emergency Restore actually recovers a force-quit mid-intervention"
    requirement: "SAFE-05"
    verification: []
    human_judgment: true
    rationale: "Device-gated by construction. The rung-2 ceiling excludes real-hardware environmental behaviour of this class, and the sibling Set Brightness action is measured to fail outright on a simulator. Instrument authored as 14-UAT.md with six tests, all blank; BLOCKED on DIST-03, re-measured this plan as paired / tunnelState unavailable / transportType none."
  - id: D7
    description: "A user actually reads the disclosure and acts on it before the Circle fires"
    requirement: "SAFE-02"
    verification: []
    human_judgment: true
    rationale: "Disclosure is the only mitigation available — there is no read-back for any accessibility setting on iOS — and its effectiveness is not measurable from here. The pre-existing-grayscale user is accepted and backlogged, not solved."

# Metrics
duration: 51min
completed: 2026-08-19
status: complete
---

# Phase 14 Plan 03: Ash as real Color Filters grayscale Summary

**The build started telling the user what it does to their phone: the Control Room Note now says
in plain words that PROSOCHĒ turns Color Filters on and off, names the one switch that stops it,
and promises Emergency Restore will bring colour back — and both forks were re-signed so that
promise ships.**

## Performance

- **Duration:** ~51 min
- **Tasks:** 3 of 3
- **Files modified:** 11 (3 created, 8 modified)
- **Commits:** 4

## Accomplishments

- **The disclosure is a deliverable, and it landed where a user will meet it.** It sits inside
  `## THE NINE CIRCLES`, immediately after the paragraph explaining that the sequence decides
  which interruption fires at which depth — not in a footnote and not at import. It says exactly
  three things: the screen goes black and white; PROSOCHĒ turns it back off when you leave and
  whenever Emergency Restore runs; and if you use Color Filters yourself, here is the switch,
  here is what it ships as, and here is where to change it.
- **The Emergency Restore promise stopped being incomplete the moment this phase shipped.** The
  sentence that promised to put back a dim screen and a lowered media volume now covers colour
  too. Extended, not replaced.
- **`src/CONFIG-BLOCK.md` stopped asserting two contradictory things about the same primitive.**
  One note said the alert-only body was verbatim and the checker's no-Color-Filters assertion
  stayed green; the note directly below it said the primitive was already a real Color Filters
  change. Both were corrected in **every** asserting cell.
- **The manifest was closed by re-signing, and its five stale gate-A cells were handled without
  falsifying a single dated measurement.** Each is retained exactly as written, with an inline
  pointer to the new top block. The plan handed over four; the sweep found five.
- **The full static suite is green for the first time this phase** — fourteen checkers, the
  manifest check and the residue checker included.
- **The device instrument is honest about never having run**, and its first test is the one that
  matters most: force-quit mid-intervention, then Emergency Restore, then look at the screen.

## Task Commits

1. **Task 1: disclose the Color Filters change in the Note; stop the config mirror contradicting itself** — `029d856` (docs)
2. **Task 2: re-sign both forks under their exact display names, close the manifest** — `49926a7` (chore)
3. **Task 3: author `14-UAT.md`, retire backlog 999.3, correct the ROADMAP's superseded Phase 14 prose** — `25981c7` (docs)
4. **Correction: leave the Phase 14 plan checkboxes to the orchestrator** — `fe30bf1` (fix)

## The independent config-mirror sweep — terms, scope, and findings

**Stated plainly: a starting set given a mechanical assertion by the plan's verify, not a claim of
completeness.** The plan's four-site inventory was checked first, then the whole file was swept
independently.

**Search terms** (one `grep -n -i` over `src/CONFIG-BLOCK.md`, all case-insensitive):
`ash` · `color filter` · `grayscale` · `greyscale` · `black and white` · `colorfilter` ·
`visual pause` · `alert-only` · `phase5_self_check` · `BD-01`

**What the sweep found, beyond the plan's four:**

| Site | Verdict |
|---|---|
| **Header cross-reference** — "most directly BD-01's note on the `Ash` sequence entry below" | **A genuine fifth asserting site, and corrected.** It asserts *which decision governs* this file's `Ash`-related values. BD-01 and BD-01-R are both superseded; **BD-01-R2** governs. Corrected in the same pass. |
| The `sequences` intro paragraph, the three `sequences` arrays, and the `sequences.Ambient` field-reference row | **Not carriers.** They name `Black and White` as a slot value. Nothing about behaviour is asserted, and all are correct. |
| Changelog lines dated 2026-08-17 and 2026-08-18 | **Historical and retained.** The 16-05 line's statement that `ash_managed_color_filters` was untouched by D-01 is true of that plan and stays true. |
| The historical BD-01 paragraph ("Note — binding (historical, superseded above)") | **Retained deliberately** with its pointer, per this file's own convention for a reversed decision. Verified still present after the edit. |

**The four inventoried sites, and what each carried:**

| # | Stale assertion | Correction |
|---|---|---|
| C1 | the primitive's "alert-only fallback is verbatim", and `docs/phase5_self_check.py`'s no-Color-Filters assertion "stays green" | Both cited by where they lived, not restated. The alert is **deleted** (D-14-C); the checker assertion was **inverted** by plan 14-01, which now asserts the `AX*` identifier present at a derived count while keeping the twin-absent half as a trap guard. |
| C2 | the primitive *is already* a real Color Filters change | It was true of **no build** when written on 2026-08-13, and became true at plan 14-01 for a different reason. Recorded as such rather than left to come right quietly. |
| C3 | the macOS twin identifier and an elided-default `operation` literal | Both **removed from the file entirely** and cited by where they lived (this note's pre-2026-08-19 text, and BD-01-R). The twin literal now appears nowhere in `src/CONFIG-BLOCK.md`. A pointer to `DEV-08` and `docs/gate_a_residue_check.py` was added so a reader meeting a red gate A finds the authority before the temptation. |
| C4 | no `## Field reference` row for the kill switch, despite the key being live in the fenced literal above | Row added: what it does at `true` and at `false`, the numeric `> 0` coercion hazard, the §21 authority via BD-01-R2, and the statement that it is the **only** recourse a Color Filters user has, with the backlog item named and labelled accepted-not-mitigated. |

**Changelog:** one dated `2026-08-19` line added in the file's existing style, at the top of
`## Change log`.

## The Note edits, and the guarded round trip that made them safe

Both edits went through `tools/plist_text_edit.py`: `load` → `assert_noop_roundtrip` →
`find_action` (by content, on `## READ THIS FIRST`) → `replace_in_token` × 2 with explicit
occurrence counts → `assert_offsets_match` → `save`. Then `build_state_engine.py` and
`build_sentient.py` were re-run so the second fork carries the edit rather than skewing from it.

| Measurement | Before | After |
|---|---:|---:|
| Note body length (characters) | 9,287 | 10,411 |
| Attachments in the Note body | 2 | 2 |
| Attachment offsets | `{8555, 1}`, `{8586, 1}` | `{9679, 1}`, `{9710, 1}` |
| `WFTextActionText` token strings per fork | 249 | 249 |
| Whole-document token strings (`note_identity_check`) | — | 1115 Core / 1123 Aware |

**Both attachments sit downstream of the insertion point** (they are the `Profile` and `Voice`
values in `## CURRENT SETTINGS`), so both offsets moved by exactly the inserted length. That is
precisely the class of damage a plain text substitution on the XML would have shipped silently —
structurally valid all the way to the device, invisible to the validator, the catalog and a
decrypt, and capable of crashing Shortcuts on import.

**No new placeholder was introduced.** `replace_in_token()` asserts this, and it is why the
disclosure states the kill switch's **shipped default** rather than its current value: a live
value would need an attachment, and a preserved literal has no attachment to bind a new one to.

**Two constraints on the prose that were discovered rather than assumed:**

1. **The disclosure names no Circle number.** `Black and White` sits at Circle 2 under `Classic`,
   Circle 3 under `BlackMirror` and Circle 1 under `Ambient`. Naming Circle 2 would have been
   false for two of the three sequences.
2. **The disclosure names no fork.** `build_sentient.py`'s `fix_fork_strings()` asserts
   **exactly 2** occurrences of `PROSOCHĒ — Nine Circles — Core` in the Note body, and would have
   aborted the Aware build on a third. The prose says "open the shortcut in the Shortcuts app"
   instead, which is also more accurate, since the same paragraph ships in both forks.

## Decrypt-verify — measured on the recovered plists, not on `src/`

Both signed containers were opened through the AEA1 recipe in `.claude/CLAUDE.md` §8
(`SigningCertificateChain` leaf → public key → `aea decrypt` → `aa extract` → `Shortcut.wflow`):

| Measurement | Core | Aware |
|---|---:|---:|
| Recovered actions | 4396 | 4530 |
| Source actions | 4396 | 4530 |
| Identifier sequence identical to source, action-for-action | ✅ | ✅ |
| `AXToggleColorFiltersIntent` sites in the recovered payload | 15 | 15 |
| Note body names `ash_managed_color_filters` | ✅ | ✅ |
| Note body names Color Filters | ✅ | ✅ |
| `WFWorkflowName` present in the recovered payload | **No** | **No** |

The last row is a re-measurement, not an inherited claim: both `src/*.xml` set `WFWorkflowName`
and the signer strips it, so **the filename is the sole carrier of the display name**. That is
why `sign-shortcut --name` was passed the exact display name for each fork and why no suffix was
added. Both signings succeeded on the first attempt; neither of the signer's two known quirks
was triggered.

## The refreshed manifest rows

| Row | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Core source | `src/PROSOCHE-Dumb.xml` | 2915855 | `e15ae8bc5a4da5a93141be620ac70000bf4aa1a896a9980939b8b4002c198d28` |
| Core archive | `artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Core-113713.xml` | 2915855 | `e15ae8bc5a4da5a93141be620ac70000bf4aa1a896a9980939b8b4002c198d28` |
| Core signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` | 235369 | `c359bbe2f801f899ac21237000d589df5be9e7e575a825306c5333055a76658e` |
| Aware source | `src/PROSOCHE-Sentient.xml` | 2987938 | `bcb2b37e97d563d3e3a407a1a4c6a75777101606000cff8990b2049aa7fe93cb` |
| Aware archive | `artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Aware-113713.xml` | 2987938 | `bcb2b37e97d563d3e3a407a1a4c6a75777101606000cff8990b2049aa7fe93cb` |
| Aware signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` | 241805 | `bd269b0cd3ae496811ec4482ab965cdb0288f2ec127d9d7350c344d36ec575d2` |

**Closed by re-signing, never by editing rows to match.** The rebuild is byte-idempotent — after
the provenance ancestor check passed (exit 0), both generators were re-run and
`git status --short -- src/` was empty, so these digests are reproducible rather than
run-specific. The superseded phase-16 rows are retained in the file so a build already on a
device stays identifiable. The standing structurally-proven / behaviourally-unproven warning was
carried forward and **strengthened**: the build now changes an accessibility setting, and no run
of it has happened on a phone.

## The five gate-A cells wave 2 handed over

Wave 2 recorded four; the sweep found five. **None was rewritten.** Each is a true measurement of
the build it describes — at the time those artifacts were signed, gate A genuinely did report
clean — and rewriting a dated provenance measurement to match a later reality would corrupt the
record twice over, exactly as `docs/retired_clause_check.py`'s tier-1 allowlist reasons about
`artifacts/`.

| Block | Claim | Treatment |
|---|---|---|
| Phase 11 wave 10 (2026-08-18) | "Both forks still pass gate A" | inline pointer: *true of the 11-10 build; gate-A status superseded* |
| Phase 16 (2026-08-18) | "`Validation passed.` exit 0 on both forks before signing" | inline pointer |
| Phase 13 CR-01 (2026-08-17) | "which passes clean on both forks" | inline pointer |
| Phase 13 CR-01 detail | "**gate A** `Validation passed.` exit 0 on both forks" | inline pointer |
| Phase 13 plan 04 (already marked SUPERSEDED) | "Both forks passed **gate A** … exit 0" | inline pointer |

The correction itself lives in a new top block, which states unmissably that gate A exits 1 by
construction, that `docs/gate_a_residue_check.py` is the obligation, and that reaching for the
macOS twin is the wrong fix.

## Gate readings, recorded and chained into nothing

**Gate A** — the obligation, discharged by the checker, **exit 0**:

```
gate A residue check: passed -- residue equals exactly the enumerated waiver on 2 fork(s)
(Core (src/PROSOCHE-Dumb.xml): 30 permitted; Aware (src/PROSOCHE-Sentient.xml): 30 permitted);
2 line families scoped to com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent;
8 classifier control rows.
```

**Gate B** — advisory, read standalone per fork, **exit 1** on both, index-normalised:

| Line family | Core | Aware |
|---|---:|---:|
| `Unknown AppIntent identifier at index N: …AXToggleColorFiltersIntent` | 15 | 15 |
| `AppIntent action missing AppIntentDescriptor at index N: …AXToggleColorFiltersIntent` | 15 | 15 |
| `Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput` | 1 (N=4240) | 1 (N=4374) |

**Nothing outside the two permanent waivers appeared on either fork.** Gate B at target 27 loads
the parameter catalogs on top of the identifier baseline, which is why it reports the union.

## Device availability at UAT-authoring time

Measured 2026-08-19, branching on `tunnelState` read from `xcrun devicectl list devices
--json-output` and **never** on the `State` column:

| Field | Value |
|---|---|
| `deviceProperties.name` | `dougal` |
| `hardwareProperties.marketingName` / `productType` | iPhone 15 Pro / `iPhone16,1` |
| `deviceProperties.osVersionNumber` | `26.6` |
| `connectionProperties.pairingState` | `paired` |
| **`connectionProperties.tunnelState`** | **`unavailable`** |
| `connectionProperties.transportType` | `null` (none) |
| `connectionProperties.lastConnectionDate` | `2026-08-18T21:18:00.000Z` |
| `State` column | `unavailable` — recorded only to show it agrees today; it is not the signal |

**Resolved to the blocked branch**, reason unchanged from plan 16-06's measurement: a known,
paired device with no live tunnel and no active transport — no session to drive. This is *not*
"no devices found", and recording that phrasing would be recording something false. `DIST-03`
stays open; all six tests in `14-UAT.md` stay blank.

## The final full-suite result — every checker that ran

All fourteen at `fe30bf1`, each `exit=0`:

`environmental_restore_check` · `gate_a_residue_check` · **`manifest_check`** ·
`note_identity_check` · `phase5_self_check` · `phase6_self_check` · `phase7_self_check` ·
`phase9_self_check` · `retired_clause_check` · `router_ui_census` · `sentient_audit_check` ·
`sentient_core_check` · `sequence_dispatch_check` · `state_engine_self_check`

`manifest_check` is bolded because it entered this plan **red** and is closed here, by
re-signing. Pinned counts are unmoved — `setbrightness` 15, `setvolume` 15, `getdevicedetails`
22 in both forks — and the AX census is 15 per fork (11 on, 4 off), equal across forks and
non-zero.

## Decisions Made

- **Site-level supersession over wholesale correction in `MANIFEST.md`.** The file already stacks
  dated blocks and already relies on the topmost block winning. Adding a short inline pointer at
  each stale claim means a reader skimming an old block meets the correction exactly where the
  false reading would form, without any dated measurement being rewritten.
- **The macOS twin literal was removed from `src/CONFIG-BLOCK.md` entirely** rather than kept
  under a supersession pointer. The plan's verify permits either; removal is stronger, and the
  twin is still named-and-rejected on the four surfaces wave 2 established, which is where a
  reader hitting a red gate A actually looks.
- **The disclosure states the shipped default, never a current value.** This is a prohibition in
  the plan and also a mechanical consequence: `replace_in_token()` refuses a replacement carrying
  a `￼` placeholder, and a live value would need one.
- **`14-UAT.md` is six tests, not twelve.** Everything the phase changed sits on one primitive
  with two legs and one kill switch. Padding the instrument would have made a scarce device
  session longer without answering anything more.
- **The ROADMAP's scope-reset banner was retained rather than deleted** once its correction was
  applied, and re-headed `APPLIED`. It is the record of what was reset and when.

## Deviations from Plan

### Auto-fixed Issues

None. No bug, missing critical functionality or blocking issue was encountered; nothing required
a Rule 1–3 fix.

### Recorded divergences (not auto-fixes)

**1. The stated 238-text-token baseline was not reproducible and was not adopted.** The plan's
preamble gives "238 text tokens per fork" as the wave-1 baseline to preserve. Measured under
every basis available here, the figure is **249** `WFTextActionText` token strings per fork —
at the wave-1 base commit `80e0240`, at `HEAD` before this plan's edit, and after it — or
**1104/1112** whole-document `WFTextTokenString` values, which is `note_identity_check.py`'s own
basis and its recorded floor. Neither yields 238. **The invariant that actually matters was
preserved and asserted:** the count is unchanged across the edit and every token passes
`assert_offsets_match` in both forks. The 238 figure is recorded here as unreproduced rather than
silently rounded to.

**2. One further stale site in `src/CONFIG-BLOCK.md` beyond the plan's inventory of four.** The
plan's flagged assumption **C2** anticipated exactly this and instructed a sweep; the sweep found
the header cross-reference naming BD-01 as governing. Corrected in the same pass, and the sweep's
terms and full findings are recorded above.

**3. Five gate-A cells in `MANIFEST.md`, not the four wave 2 handed over.** All five handled
identically.

**4. Three ROADMAP plan-list checkboxes ticked, then reverted.** Task 3 ticked them while
correcting the goal prose. Plan-progress state is the orchestrator's to write, and this plan's
ROADMAP scope is the goal-block prose plus the 999.3 retirement. Reverted in `fe30bf1`; both
plan-mandated edits are untouched.

---

**Total deviations:** 0 auto-fixed. 4 recorded divergences, all within scope.
**Impact on plan:** None. No prohibition was touched: no plain text substitution was made on
either XML, no new placeholder was introduced into a preserved literal, no current value is
asserted for the kill switch, the kill switch's shipped value is unchanged (`true`), the
Emergency Restore promise was extended rather than replaced, the historical reversed-decision
paragraph survives, no superseded wording is quoted inside a supersession note, neither fork was
renamed and no signed filename carries a suffix, no manifest row was edited without re-signing,
no device test is recorded as passed, `tools/` and `docs/*.py` are untouched
(`git status --short` shows no change under either), and the provenance ancestor check passed
before every generator run.

## Issues Encountered

- **None outstanding.** `docs/manifest_check.py` entered this plan red by design (waves 1–2
  rebuilt the artifacts without re-signing) and is closed here. The full suite is green.

## What this plan does NOT establish

Stated plainly, because every item is device-gated and the plan's own must-haves carry them as
backstops:

- **That the screen turns black and white on a real iPhone**, or that colour comes back on any
  of the four recovery paths. `14-UAT.md` Tests 1–4, all blank.
- **That Emergency Restore recovers a force-quit mid-intervention.** It has still never been
  tapped on a device, in any phase. This is `14-UAT.md` Test 1 and the single highest-value
  observation in the phase.
- **That the edited Note literal renders correctly on a device.** Offsets are re-verified
  structurally in both forks and in both decrypted payloads; the rendering itself is
  device-gated.
- **That the kill switch does anything at run time.** Its gate is structurally present and
  numerically correct for a JSON boolean; resolution on device is `14-UAT.md` Test 5.
- **That a user reads the disclosure and acts on it.** Disclosure is the only mitigation
  available and its effectiveness is not measurable from here.
- **The pre-existing-grayscale user.** No detection is built (D-14-D). T-14-14 is **accepted,
  backlogged and disclosed — not mitigated**.

## Known Stubs

None. No placeholder, TODO or unwired data path was introduced. Every blank `outcome:` field in
`14-UAT.md` is a deliberate unrun-test marker, not a stub: the plan's verify **fails** on any
recorded pass, and a filled outcome without a device session would be a fabricated result.

## Threat Flags

None. No new network endpoint, auth path, file-access pattern or schema change at a trust
boundary was introduced. This plan changed prose, re-signed two artifacts and authored one
planning document.

## User Setup Required

None for this plan. **One user action is now outstanding for the phase:** a connected iPhone
session to run `14-UAT.md`, best scheduled together with `16-UAT.md`'s twelve outstanding tests —
they share their entire setup, and one Emergency Restore tap answers a test in each.

## Self-Check: PASSED

Files asserted present:

- `.planning/phases/14-ash-as-real-color-filters-grayscale/14-UAT.md` — FOUND (six tests, all outcomes blank; contains `force-quit`, `Emergency Restore`, `DIST-03`, `tunnelState`, `16-UAT`, and the SHA-256 build pin)
- `src/PROSOCHE-Dumb.xml` — FOUND (Note names Color Filters and `ash_managed_color_filters`; 15 AX sites)
- `src/PROSOCHE-Sentient.xml` — FOUND (same)
- `src/CONFIG-BLOCK.md` — FOUND (kill-switch field-reference row present; no `stays green`; no macOS twin literal; historical BD-01 paragraph retained; dated 2026-08-19 changelog line)
- `docs/CAPABILITY-DECISIONS.md` — FOUND (BD-01-R2 `IMPLEMENTED` note with the 15-site census)
- `artifacts/shortcuts/MANIFEST.md` — FOUND (2026-08-19 top block; six refreshed rows)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` — FOUND (235369 bytes, non-zero, exact display name, no suffix)
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` — FOUND (241805 bytes, non-zero, exact display name, no suffix)
- `artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Core-113713.xml` — FOUND
- `artifacts/shortcuts/2026-08-19/PROSOCHĒ — Nine Circles — Aware-113713.xml` — FOUND
- `.planning/ROADMAP.md` — FOUND (Phase 14 goal prose corrected; backlog 999.3 retired)

Commits asserted present: `029d856`, `49926a7`, `25981c7`, `fe30bf1` — all FOUND in `git log`.
