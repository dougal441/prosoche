---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 06
subsystem: distribution
tags: [rename, signed-artifacts, fork-divergence, breaking-change, manifest, note-copy]
requires:
  - "BD-06-A3 Decision 2 (plan 11-04) — the old-named signed artifacts are DELETED"
  - "schema_version 3 (plan 11-05) — inherited, NOT bumped again by this plan"
  - "tools/plist_text_edit.py (plan 11-01) — the guarded, offset-recomputing round trip"
provides:
  - "The two canonical display names: PROSOCHĒ — Nine Circles — Core / — Aware"
  - "fix_fork_strings(actions) — the first deliberate Sentient-side content divergence"
  - "A fork-normalised additivity proof in docs/sentient_core_check.py, with bounded counts"
  - "BD-06-A4 — the rename recorded as a breaking change for any existing install"
affects:
  - "Phase 11 verification — this is the phase's closing plan"
  - "Any future plan touching build_sentient.py — the fork divergence set is now enumerated in two places and both must move together"
tech-stack:
  added: []
  patterns:
    - "Bounded, counted normalisation instead of deleting an equality a deliberate divergence broke"
    - "Pair every normalisation with a positive assertion that the divergence is real, so the normalisation cannot mask the defect it undoes"
    - "Assert renamed strings against the DECRYPTED payload, never against src/"
key-files:
  created: []
  modified:
    - "src/PROSOCHE-Dumb.xml — root WFWorkflowName, the Note's two automation targets, the settings-block fork label, the bootstrap fork seed, and a new rename notice"
    - "src/PROSOCHE-Sentient.xml — regenerated, now carrying its own fork strings"
    - "tools/build_sentient.py — CORE_NAME / AWARE_NAME constants, fix_fork_strings(), wired before the guard chain"
    - "docs/sentient_core_check.py — fork suffix, fork-normalised equality, positive divergence assertion"
    - "docs/manifest_check.py — DISPLAY_NAMES"
    - "README.md — both artifact names plus the breaking-change statement"
    - "artifacts/shortcuts/MANIFEST.md — six rows relabelled and refreshed from disk"
    - "docs/BUILD-NOTES.md — §25 appended, 130 insertions / 0 deletions"
    - "docs/CAPABILITY-DECISIONS.md — BD-06-A4 appended, 66 insertions / 0 deletions"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Core,Aware}.shortcut — the two signed deliverables"
  deleted:
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Dumb,Sentient}.shortcut — per BD-06-A3 Decision 2, recoverable via git"
decisions:
  - "The src/*.xml source filenames are deliberately NOT renamed; recorded in BUILD-NOTES §25, MANIFEST and README so a later phase reads it as a decision"
  - "The broken fork equality was normalised, not deleted — a bounded inverse substitution with exact per-site counts, paired with a positive divergence assertion"
  - "Both length-neutral and length-changing renames went through the offset-recomputing round trip rather than reasoning about which was safe"
  - "The header comment and the Note's `- AI:` line were left alone and deferred, because fixing either widens the fork-divergence surface this plan enumerated in advance"
metrics:
  duration: ~75 min
  completed: 2026-08-17
  tasks: 3
  files: 12
status: complete
---

# Phase 11 Plan 06: Ship the two variants under their new names Summary

`Dumb` is now **Core** and `Sentient` is now **Aware** at every site where the name is
load-bearing, the Aware fork stopped telling its users to install the other fork's shortcut,
and the proof that Aware is an additive fork survived the first deliberate divergence between
them.

## What Was Done

### Task 1 — the rename, everywhere the name carries weight (commit `69cfd37`)

Three classes, kept separate as the research does.

**Signed display names.** `docs/manifest_check.py`'s `DISPLAY_NAMES` moved to the two new
names; `SIGNED_BASENAMES` and the fork-label derivation (`rsplit("—", 1)`) follow from it
automatically, which is what forced the six `MANIFEST.md` row labels to move in Task 3.

**Internal identifiers.** The root `WFWorkflowName` in `src/PROSOCHE-Dumb.xml`, the assignment
in `tools/build_sentient.py`, and `docs/sentient_core_check.py`'s suffix assertion.

**User-visible copy — the highest-severity site.** The Control Room Note names the Run Shortcut
target verbatim in Automation A step 10 and Automation B step 10. **Missing either one is a
silently dead install**: the user builds an automation pointing at a shortcut that does not
exist. Both were rewritten through `tools/plist_text_edit.py`'s `replace_in_token`, with an
expected count of 2, alongside the settings-block fork label and the bootstrap `state.json`
fork seed. The Note's `## READ THIS FIRST` gained one paragraph naming the rename, the stale
library entry it leaves behind, and the fact that both Personal Automations must be re-pointed
by hand because nothing can do it for them.

**The seed extraction trap, avoided as briefed.** The bootstrap seed is a `WFTextTokenString`
**dict** carrying four attachments with real `U+FFFC` placeholders; the Config literal, a few
actions away, is a plain `str` with none. A plain-`str` filter finds the second and misses the
first entirely. Both the read (dual-envelope) and the write (`replace_in_token`) were done
accordingly.

### Task 2 — the Aware fork's own copy, and the reconciled equality (commit `1e0777c`)

**`fix_fork_strings(actions)`** in `tools/build_sentient.py`, called before the
`normalise_*`/`verify_*` chain so the rewritten token strings pass the same guards as
everything else. Three sites, each with an expected occurrence count: the Note's two Run
Shortcut targets, the Note's settings-block fork label, and the bootstrap fork seed. It does
not touch the Note **title**, which is identical in both forks on purpose and out of scope —
and is out of reach by construction, since the function only ever edits `WFTextActionText`
token strings while the title lives in the Create Note action's `name` parameter.

**The failure path was exercised, not asserted.** Reducing the display-name count from 2 to 1
made `python3 tools/build_sentient.py` exit **1** with:

> `fix_fork_strings could not rewrite the Note's two Run Shortcut targets: expected 1
> occurrence(s) of 'PROSOCHĒ — Nine Circles — Core' in this WFTextTokenString, found 2 — …`
> `CONSEQUENCE: this Aware build would ship a Control Room Note naming the Core shortcut. The
> signed filename is the only carrier of a shortcut's display name, so a user following that
> Note builds two Personal Automations pointing at a shortcut that does not exist under these
> names — a silently dead install for every Aware user, with no error on device and nothing any
> structural check downstream of here can see.`

The count was then restored and both forks rebuilt.

**`docs/sentient_core_check.py` reconciled.** Its `sa[:6] + sa[8:marker] + sa[end + 1:] == da`
whole-list equality is now false **by design**, and deleting it would have discarded the only
proof that nothing *else* diverged. It was replaced by a **fork-normalised** equality: a deep
copy of the Sentient action list has the inverse substitution applied, with an exact expected
count per site, recomputing every `attachmentsByRange` offset — `Aware` is one character longer
than `Core` and sits upstream of every attachment in both edited strings. A bounded, counted
normalisation cannot absorb an unrelated drift; a fourth divergent site would simply fail the
equality.

It is paired with a **positive** assertion: the Aware Note names the Aware display name at
least twice and the Core display name exactly zero times, and its fork seed reads `Aware`. That
is what stops the normalisation from masking the very defect it undoes. A header comment names
this plan and says the stricter form must not be restored.

### Task 3 — validate, sign, decrypt-verify, record (commit `bdd04cf`)

RESEARCH §10's sequence in order: provenance gate, both builders, twelve checks, validator gate
A on both forks, `sign-shortcut --name` per fork with `--mode anyone --output-dir
artifacts/shortcuts` and no pre-dated directory, then the AEA1 decrypt-verify on both
containers. Neither signer quirk fired. `--target-macos 27`, `--target-platform ios` and
`timeout` were never invoked.

The two old-named signed artifacts were **deleted**, applying BD-06-A3 Decision 2 rather than
re-deciding it. `MANIFEST.md`'s six rows were relabelled `Core`/`Aware`, repathed, and every
size and SHA-256 recomputed from disk. `docs/BUILD-NOTES.md` §25 and
`docs/CAPABILITY-DECISIONS.md` BD-06-A4 were appended, both with zero deletions.

## The Measurement That Governs Everything Here

**A signed `.shortcut` carries no display name inside it — re-measured on this build, not
inherited from the record.** Both containers were decrypted, and neither recovered
`Shortcut.wflow` contains a `WFWorkflowName` key at all, though both `src/*.xml` files set one.
The signer strips it; the AEA1 auth data holds only `SigningCertificateChain`.

Everything else follows: the filename is the sole carrier, `--name` had to be passed explicitly
(the signer otherwise defaults to the input basename, here `PROSOCHE-Dumb`), no suffix of any
kind is permissible, and the rename is a **breaking change nothing on the device can repair** —
the user's two Personal Automations reference the library entry by that name and no API exists
to re-point them.

## Verification

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run |
| Twelve `docs/*.py` checks, baseline before any edit | **12/12 green** |
| Twelve `docs/*.py` checks, final | **12/12 green** |
| Builder idempotence | a second consecutive builder pair leaves both sources byte-identical (`12bbfe31…`, `ef431b5d…`); `git status --short -- src/PROSOCHE-Dumb.xml` empty after running only `build_sentient.py` |
| Root `WFWorkflowName` | `…— Core` / `…— Aware` |
| `docs/manifest_check.py` `DISPLAY_NAMES` | exactly the two new names |
| Core Note, **decrypted payload** | Core ×**2**, Aware ×**0**, `Dumb` ×**0**, `Sentient` ×**0** |
| Aware Note, **decrypted payload** | Aware ×**2**, Core ×**0**, `Dumb` ×**0**, `Sentient` ×**0** |
| Fork seeds, decrypted payloads | `"fork": "Core"` ×1 / `"fork": "Aware"` ×1 |
| `WFWorkflowName` in either recovered payload | **absent** — stripped by the signer |
| Phase deliverables in both payloads | `Loud Mirror` ×**25**, `PANIC ESCAPE` ×**5**, `THE NINE CIRCLES` ×**1** |
| `fix_fork_strings` failure path | count 2 → 1 ⇒ exit **1**, message names the dead-install consequence; restored |
| `docs/note_identity_check.py` | **0** attachment-offset mismatches; 1,205 (Core) / 1,209 (Aware) token strings |
| Validator gate A ×2 | `Validation passed.`, exit **0** |
| Signed artifacts | **234,370 B** / **238,668 B**, non-zero, basenames exactly the canonical display names, no suffix |
| `ls artifacts/shortcuts/*.shortcut` | exactly **2** files, both canonical |
| Dated archive SHA-256 == `src/` counterpart | `12bbfe31…` == `12bbfe31…`; `ef431b5d…` == `ef431b5d…` |
| Decrypt-verify | `plutil -lint` **OK** ×2 |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk |
| `docs/BUILD-NOTES.md` / `docs/CAPABILITY-DECISIONS.md` append-only | **130 / 0** and **66 / 0** for this plan's own edits |
| Appended text contains `breaking change`, `structural`, `DIST-03` | yes, in both files |
| `git status --short -- artifacts/shortcuts/2026-08-1{3,4,5,6}` | empty — the dated historical archives were not touched |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked |
| `git status --short` after the final commit | empty |

## Key Decisions

**The equality was normalised, not deleted.** The tempting alternatives were both wrong:
deleting the assertion discards the additivity proof entirely, and weakening it to "compare
only the actions I expect to be equal" is an assertion that cannot fail. A bounded inverse
substitution with exact per-site counts, plus a positive assertion that the divergence is real
and complete, keeps the original guarantee and adds one: the divergence is exactly the fork
strings and nothing else.

**Both renames went through the offset-recomputing round trip, including the safe one.**
`Dumb` → `Core` is length-neutral, so the bootstrap seed's four attachment offsets survive it
by luck. `Core` → `Aware` is one character longer and sits upstream of all four. Reasoning
about which edit happens to be safe is exactly the habit that ships an out-of-bounds range, so
neither edit was hand-substituted.

**The source filenames stay.** Ten code files and roughly seventy planning documents reference
them and every historical plan's reproducibility depends on them; the addendum renames the
products. Recorded in three places so it is legible as a decision, not an oversight.

## Deviations from Plan

### 1. [Rule 3 — blocking] Task 2's "all twelve checks exit 0" could not hold at Task 2

- **Found during:** Task 2, running the check suite before commit
- **Issue:** `docs/manifest_check.py` hashes every declared path from disk, so it goes **red on
  every rebuild** until `MANIFEST.md` is refreshed — RESEARCH §10 states this explicitly
  (*"goes RED on every rebuild until MANIFEST refreshed"*). The manifest refresh is Task 3's
  work, by the plan's own sequencing, so Task 2's criterion is unsatisfiable at Task 2 without
  duplicating Task 3.
- **Fix:** none needed in code. Task 2 landed at **11/12**, with `manifest_check` the sole red
  and its failure message naming exactly the expected byte-count drift. Task 3's refresh
  returned it to 12/12, which is asserted in the table above at both the baseline and the final
  commit. No check was disabled, skipped or weakened.
- **Commit:** `1e0777c` (state), `bdd04cf` (resolution)

### 2. [Recorded, not a fix] The `docs/BUILD-NOTES.md` baseline-relative deletion count is 3, not 0

- **Found during:** Task 3, running the acceptance assertion
- **Issue:** The criterion asks for a deletion count of exactly `0` in
  `git diff --numstat f4e47f9 -- docs/BUILD-NOTES.md`. It measures **758 / 3**.
- **Why it is not this plan's deletion:** plan 11-05's SUMMARY already recorded the same three
  deletions, measured before this plan began (408/3 at its HEAD). Against **this plan's own
  base commit** (`62dc68b`) the file measures **130 insertions / 0 deletions** — a pure append,
  which is what the criterion is protecting. `docs/CAPABILITY-DECISIONS.md` measures 0
  deletions on both baselines.
- **Commit:** `bdd04cf`

### 3. [Scope boundary] Two pre-existing copy defects left alone and logged

Both are recorded in `deferred-items.md` with the reason:

- `WFWorkflowActions[0]`'s comment still opens `PROSOCHE - Nine Circles (Dumb fork).` in both
  forks. Generator-authored and inherited verbatim, so it has always been wrong in the
  Sentient/Aware build too. Fixing it properly means adding a **fourth** site to
  `fix_fork_strings()` and a fourth entry to `FORK_STRINGS` — a widening of a divergence set
  this plan enumerated in advance.
- The Note's static `- AI: not used by this fork` line. That literal also lives in
  `manual_note_refresh()`'s **shared** snapshot template, which re-appends the block on every
  state-changing manual run, so editing only the Note body leaves the two disagreeing after the
  first manual run. The fix is a fork-aware snapshot template — new design work. The adjacent
  `- Fork:` line **was** fixed, because that one is load-bearing state.

### Not a deviation — gate B was correctly not run

`.claude/CLAUDE.md` §1's two-gate rule post-dates this plan's authoring. Gate B
(`--target-macos 27`) is advisory, permanently waivered and structurally incapable of exiting
0; CLAUDE.md states that a plan asserting target 27 appears nowhere in its commands "remains
fully satisfied by gate A alone". Gate A was run on both forks and passed clean.

## Requirements

| ID | Status | Evidence |
|---|---|---|
| DIST-01 | structurally satisfied | Both forks build, validate under gate A, sign under exact canonical basenames, and decrypt-verify |
| DIST-02 | structurally satisfied | `docs/manifest_check.py` hashes and sizes every declared path from disk, so a partially written, stale or half-signed artifact is detected at build time whatever order the signing steps ran in — green against six refreshed rows |
| ROOM-02 | **unresolved, as the plan owns it** | This plan changed only the Run Shortcut *target name* inside the already-authored automation steps, and asserts the new name appears in both steps of both forks in the decrypted payloads. The steps' end-to-end correctness was rewritten by quick task `260817-au7` and remains device-unproven, blocked on DIST-03. **Assumed, not machine-proven — review manually.** |

## What This Does NOT Establish

**DIST-03 is open. No iPhone is connected and no device has run either renamed build.** Every
row above is structural. In particular, none of the following is observed:

- that either renamed shortcut imports on a device at all;
- that a user following the renamed automation steps arrives at a working automation;
- that an existing install behaves as described — that the old entry survives, that the
  automations keep pointing at it, and that re-pointing them by hand restores the loop. That the
  rename breaks an existing install is a **reasoned consequence** of the stripped-
  `WFWorkflowName` measurement plus the absence of any automation-editing API, not an
  observation of a device failing;
- that the Aware fork's Note, now diverged from Core's, renders as intended in Notes.

Structural proof is not behavioural proof, and nothing here is described as device-verified.

## Known Stubs

None. Every string this plan changed is a real, reachable site: both automation targets are
asserted present in both decrypted payloads, both fork seeds are read back from the shipped
template JSON, `fix_fork_strings()` is wired into `main()` and proven to fail on a count
mismatch, and the reconciled equality is exercised by a green `sentient_core_check` on every
run. No placeholder text, no empty default flowing to a UI, no TODO.

## Threat Flags

None. This plan introduces no network endpoint, no auth path, no new file-access pattern and
no schema change — `schema_version` stays at **3**, inherited from plan 11-05 and deliberately
not bumped again.

Register dispositions from the plan's own `<threat_model>`:

| Threat | Disposition | How it was discharged |
|---|---|---|
| `T-11-29` — a signed filename that is not exactly the canonical display name | **mitigated** | `sign-shortcut --name` with the exact display name, no pre-dated output directory; `manifest_check`'s DIST-04 assertion green; `artifacts/shortcuts/` holds exactly two `.shortcut` files and both basenames are canonical |
| `T-11-30` — a Note naming a shortcut that does not exist | **mitigated** | Both automation steps rewritten per fork with expected occurrence counts; `fix_fork_strings()` proven to raise on a mismatch; asserted against the **decrypted payload** of each signed artifact, not against `src/` |
| `T-11-31` — an existing user's automations pointing at a stale entry | **mitigated; residual risk accepted and recorded** | Stated in the Note's `## READ THIS FIRST`, in `README.md`, in `MANIFEST.md`'s ⚠ block, in BUILD-NOTES §25 and in BD-06-A4. No mechanism can re-point an automation; BD-06-A4 records that explicitly rather than implying a remedy |
| `T-11-32` — the fork-additivity proof weakened to accommodate the divergence | **mitigated** | The equality was fork-normalised with bounded per-site counts rather than removed, and paired with a positive assertion (Aware ≥2, Core ==0, Aware fork seed) so the normalisation cannot mask a genuine drift |
| `T-11-33` — out-of-bounds `attachmentsByRange` after the rewrites | **mitigated** | Every rewrite went through the offset-recomputing helper, including the length-neutral one; `note_identity_check` reports 0 mismatches across 1,205 / 1,209 token strings; `plutil -lint` OK on both recovered plists |
| `T-11-34` — two plausible "current" signed imports side by side | **mitigated** | BD-06-A3 Decision 2 applied exactly: both old-named files deleted, stated in the manifest, and the allowed basename set asserted |
| `T-11-35` — history rewritten to read as though the old names never existed | **mitigated** | Both doc updates measured append-only against this plan's base (130/0 and 66/0); the dated archives under `artifacts/shortcuts/2026-08-*` untouched and still carrying the old names |
| `T-11-SC` — package-manager installs | **not triggered** | No install command was run; no third-party import added |

## Self-Check: PASSED

- `.planning/phases/11-…/11-06-SUMMARY.md` — this file — **FOUND**
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` (234,370 B) and
  `… — Aware.shortcut` (238,668 B) — **FOUND**, non-zero, both decrypt-verified
- `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`, `tools/build_sentient.py`,
  `docs/sentient_core_check.py`, `docs/manifest_check.py`, `README.md`,
  `artifacts/shortcuts/MANIFEST.md`, `docs/BUILD-NOTES.md`,
  `docs/CAPABILITY-DECISIONS.md` — all **FOUND** and all present in
  `git diff --name-only 62dc68b HEAD`
- Both old-named signed artifacts — **CONFIRMED ABSENT** from the working tree and recoverable
  via `git show 62dc68b:…`
- Commits `69cfd37`, `1e0777c`, `bdd04cf` — all **FOUND** in `git log`
- Twelve structural checks green at the final commit — **VERIFIED**
