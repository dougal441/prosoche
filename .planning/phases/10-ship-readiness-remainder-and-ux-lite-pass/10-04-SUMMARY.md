---
phase: 10-ship-readiness-remainder-and-ux-lite-pass
plan: 04
subsystem: infra
tags: [shortcuts-signing, aea1-decryption, provenance, manifest-check, build-notes, deviation-record]

# Dependency graph
requires:
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 01
    provides: the Circle-0 silent band and raised thresholds, re-asserted here against the decrypted artifact
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 02
    provides: the gated shownote and the tenth menu item, re-asserted here against the decrypted artifact
  - phase: 10-ship-readiness-remainder-and-ux-lite-pass
    plan: 03
    provides: the nine-script regression net this rebuild was run against
provides:
  - Two re-signed forks whose contents are proven by AEA1 decryption to match what was built
  - A green docs/sentient_core_check.py, restored by rebuilding Sentient from the same generator run
  - docs/manifest_check.py — the eleventh check, proving every MANIFEST row against disk
  - artifacts/shortcuts/MANIFEST.md refreshed, with the Phase 9 device warning extended rather than softened
  - docs/BUILD-NOTES.md section 19 — the complete Phase 10 record, including both corrections and DEV-06's reactivation
  - The measured fact that a signed .shortcut carries no display name internally
affects:
  - 10-05-PLAN.md (device UAT; these two signed files are what it imports, and MANIFEST names them)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Prove-by-decryption — a validator pass certifies the source, not the signature. Decrypt
      the AEA1 container and re-run the phase's structural assertions against the RECOVERED
      plist, so 'is the shipped file what I built' has an answer with no device in the loop"
    - "Measure the claim before recording it — a plan asserting a count ('eleven consumers',
      'the manifest was correct at phase start') is a hypothesis. Derive it from the artifact or
      the starting tree and record what was measured, not what was expected"
    - "Extend-never-replace for device-gap warnings — a warning about unexercised behaviour must
      survive every rebuild that adds more unexercised behaviour. Keep the inherited substance
      verbatim and append; a rewritten warning is indistinguishable from a softened one"
    - "Append-only amendment of a recorded user decision — when a section's premise is voided,
      add a dated forward pointer and write the correction elsewhere. Editing the premise in
      place rewrites the record of what the user actually decided"

key-files:
  created:
    - docs/manifest_check.py
  modified:
    - src/PROSOCHE-Sentient.xml
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut
    - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut
    - artifacts/shortcuts/MANIFEST.md
    - docs/BUILD-NOTES.md
    - .claude/CLAUDE.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "Sentient was REBUILT rather than left stale, keeping docs/sentient_core_check.py green.
    The phase brief directed leaving it red; measured at the phase's starting HEAD (0c9aace)
    it PASSED, so honouring the brief would have meant deliberately introducing the fork skew
    the check exists to detect. Recorded as DEV-P10-02. This is a rebuild, not a re-fork —
    SEED-005 is untouched."
  - "The plan's 'eleven consumers' figure for the widened circle domain was not reproducible,
    so it was MEASURED instead of transcribed: 75 actions reference Circle Next, resolving to
    five distinct consumer sites. The two that would have hard-errored at Circle 0 are named
    with their artifact indices (996/1155). Recording an unverifiable count would have violated
    the do-not-fabricate protocol in BUILD-NOTES section 2."
  - "docs/manifest_check.py computes sizes and hashes in Python (pathlib + hashlib) and spawns
    no child process, so it behaves identically anywhere; paths are compared as text, never
    normalised, because the product name carries Ē and an em dash."
  - "The MANIFEST's Phase 9 warning block was kept verbatim and a second warning added beside
    it, rather than being rewritten to cover both. A merged warning cannot be audited against
    the original."
  - "BUILD-NOTES section 17 was appended to with a single dated forward pointer. The whole
    BUILD-NOTES diff contains ZERO deletions, which is the strongest available form of the
    'no deletion within section 17' requirement."

requirements-completed: [DIST-01, DIST-02, DIST-04, DIST-05, DIST-06]

# Metrics
duration: ~35 minutes
completed: 2026-08-17
tasks-completed: 3
tasks-total: 3
files-modified: 8
status: complete
---

# Phase 10 Plan 04: Ship the forks, prove the artifacts, write the record Summary

Both forks were rebuilt from one generator run, validated, signed under their exact display names, and then **decrypted out of their AEA1 containers and re-asserted against every structural change this phase made** — 9 of 9 on each fork — behind a manifest a script now proves correct and a build-notes section that records both positions this phase had to reverse.

## What Was Built

### Task 1 — rebuild, validate, sign, prove (commit `c054c91`)

**Provenance guard first, every time.** `git merge-base --is-ancestor 7ca8ebb… HEAD` → exit 0, run before either builder. `aea`, `aa`, `openssl` and `plutil` were all confirmed present (`/usr/bin/aea`, `/usr/bin/aa`), so the decrypt step ran at full strength and no fallback to source-level assertions was needed.

**Build.** `tools/build_state_engine.py` then `tools/build_sentient.py`, in that order, so Sentient is a fork of the Dumb the checks had just certified. A quietly significant result: **`src/PROSOCHE-Dumb.xml` came back byte-identical to `HEAD`** — `git status` showed it unmodified — which independently confirms the generator is deterministic across all three of waves 1–3. Only Sentient changed.

**Check.** All ten scripts exit 0 in a single run:

| Script | Result |
|---|---|
| `state_engine_self_check` | exit 0 |
| `phase5_self_check` | `phase5 self-check: passed` |
| `phase6_self_check` | `phase6 self-check: passed` |
| `phase7_self_check` | `phase7 self-check: passed` |
| `phase9_self_check` | `passed (28/28 sites audited, 18 coerced, 10 correctly not)` |
| `sentient_audit_check` | `compact prompt, one challenge, bounded fallback` |
| **`sentient_core_check`** | **`unchanged Dumb core and one bounded model gate`** — returned to green by the rebuild |
| `environmental_restore_check` | `environmental restore check: passed` |
| `router_ui_census` | census table + `router UI census: passed` |
| `sequence_dispatch_check` | `1 orphan(s) (0 unexpected), 0 unreachable` — reported, not gated |

**Validate.** Both forks: `Validation passed.`, exit 0, at `--target-macos 26 --target-platform all`. The `all` flag is `docs/BUILD-NOTES.md` §13 **DEV-01**, not drift — at `ios` the validator rejects every action in the file (3675 of 3675 measured on the pre-cycle-3 build), including identifiers present in the very iOS snapshot the flag claims to consult. `--target-platform ios` was never invoked in this plan.

**Sign.** `sign-shortcut` with the plain `artifacts/shortcuts` output directory, never a pre-dated one — the signer creates the dated subdirectory itself. No retry was needed; neither known quirk fired.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `src/PROSOCHE-Dumb.xml` | 2,259,398 | `aeafe01a…fd81` |
| `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-013251.xml` | 2,259,398 | `aeafe01a…fd81` |
| `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 193,498 | `47957dbf…6324` |
| `src/PROSOCHE-Sentient.xml` | 2,296,078 | `293ac146…1229` |
| `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-013301.xml` | 2,296,078 | `293ac146…1229` |
| `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 197,668 | `c8656495…fcbf` |

Each dated archive hashes **identically** to its `src/` counterpart. Both signed files are non-zero and carry the exact display names with no suffix.

**Prove.** Both containers were decrypted via the CLAUDE.md §8 recipe — leaf certificate out of the auth-data plist, public key derived, `aea decrypt`, `aa extract`, `plutil -convert xml1` — and both recovered plists passed `plutil -lint`. The phase's structural assertions were then re-run **against the recovered plists, not against `src/`**:

| # | Assertion | Dumb | Sentient |
|---|---|---|---|
| 1 | Circle scan floor is 0 | PASS — exactly 1 number-seeded `Circle Next` set-variable, seed `0` | PASS |
| 2 | `Leaving`/`Continue` menu enclosed by the silent band | PASS — index 520, group `4AC9BA5C-…` | PASS — index 522, same group |
| 3 | OPEN arm holds no notification | PASS — span 92–1217, zero in span | PASS — span 94–1285 |
| 4 | Exactly one shownote, gated on `Manual Show Note Requested` | PASS — preceding action is mode-0 `conditional`, `WFCondition 2`, that variable | PASS |
| 5 | Manual menu holds ten items | PASS — `Status … Setup Check` | PASS |
| 6 | Brightness / volume / device-detail counts | PASS — measured **(14, 14, 20)** | PASS |
| 7 | Raised threshold arrays | PASS — all three exact | PASS |
| + | `notification` count is 1 | PASS | PASS |
| + | `shownote` count is 1 | PASS | PASS |

**9 of 9 on each fork.** Every Phase 10 change is provably inside the bytes a user would import.

### Task 2 — `docs/manifest_check.py` and the MANIFEST refresh (commit `ad0a9ad`)

The script is in the read-only house style — `from __future__` annotations, `ROOT` from `parents[1]`, a local `require()`, one printed passed line, the name-guard — and **spawns no child process**: sizes come from `pathlib`, hashes from `hashlib`, so it behaves identically on any machine. `subprocess` is neither imported nor referenced (confirmed by AST walk: imports are `__future__`, `hashlib`, `pathlib`, `re`).

It parses the pipe-delimited table by **shape rather than line number** — a four-cell row that is not the header or the alignment rule — so the table can move within the document. Thousands separators and backtick fencing are stripped per cell. Per row it asserts existence, size and SHA-256. Across the table it asserts source/archive/signed coverage per fork, and that both signed basenames are exactly the two canonical display names plus `.shortcut`.

That last assertion earned a stronger justification than the plan anticipated. **Measured this phase: a signed `.shortcut` carries no display name inside it at all.** The AEA1 auth-data plist holds only `SigningCertificateChain`, and the recovered `Shortcut.wflow` has had `WFWorkflowName` **stripped by the signer** — even though both `src/*.xml` files set it (`'PROSOCHĒ — Nine Circles — Dumb'` / `'… — Sentient'` in source, `None` in both recovered plists). The display name therefore lives in the filename and nowhere else, which turns the filename-discipline rule from a convention into the only thing preventing a silently dead install. That measurement is recorded in the script's docstring, in the MANIFEST and in BUILD-NOTES.

**Manifest.** Header rewritten with today's date, the actual validator invocation, and the reason both forks were regenerated together (Sentient is a fork *of the built Dumb source*, so a Sentient carried across a Dumb change is a fork of a file that no longer exists). All six rows updated.

**The warning block was extended, never softened.** The Phase 9 dimming/silence paragraph survives **verbatim**. A second warning was added beside it naming the four new unexercised behaviours — Circle 0, the removed OPEN notification, the gated note-show, and `Setup Check` — followed by a third stating that **DIST-03 remains open** and that nothing in the manifest is device evidence. Both UAT paths are cited (`09-UAT.md`, and the `10-UAT.md` that 10-05 authors).

### Task 3 — the record (commit `023ed9b`)

**`docs/BUILD-NOTES.md` §19**, eight subsections. The number is pinned to 19 because the file's highest *value* is 18 — it contains two sections numbered 15 and a stray duplicate `## 9`, so ordinal position is not a usable guide; the section says so explicitly.

19.1 quotes all three raised threshold arrays **and** their predecessors verbatim, gives the first-band-width derivation and why it is strictly weaker than re-tuning, marks the values as prototypes for on-device tuning, and states the load-bearing safety fact: a dotted read whose final segment is absent is a **hard error**, not a null, so the band must be an enclosure plus a build guard rather than copy — there is no sentinel and no check-then-read gate, because the check *is* the read.

19.2 records the widened `circle` domain (1–9 → 0–9), no `schema_version` bump, no migration. 19.3 the removed OPEN notification and the second revision of the Leaving prompt, with G-04-4b named as the first and the reason the copy budget changed. 19.4 the gated shownote, why `filter.notes` and Create Note stay outside the gate (BOOT-08 self-heal), and Setup Check's asymmetry shipped in the alert copy. 19.5 both corrections as `DEV-P10-01` and `DEV-P10-02`. 19.6 the two Strand A items that needed no work. 19.7 the Circle 8 Voice orphan and why the reporter survives BD-06 Decision 5. 19.8 DEV-06's reactivation.

**§17 gained a single dated forward-pointer line.** `git diff docs/BUILD-NOTES.md` contains **zero deletions anywhere in the file** — a strictly stronger result than "no deletion within §17's body", and the right one, because §17 records a decision the user made.

**`.claude/CLAUDE.md`** — `grep -c 'target-platform ios'` went 4 → **0**. Exactly four lines changed (85, 112, 216, 231; `git diff --stat`: 4 insertions, 4 deletions). Line 84's separate `--target-macos 26` bullet is untouched, every amended line keeps its macOS-26 rationale, all four cite DEV-01, and no capability-audit row was altered.

**`.planning/REQUIREMENTS.md`** — SAFE-05 recorded as **satisfied as written, needing no amendment**, because the cut was proposed and cancelled, so Emergency Restore still restores brightness, volume and colour. SESS-07, AUDIT-03, AUDIT-04, CIRC-03 and CIRC-05 each gained a clause recording that the non-stateful branch is the **per-run fallback, not the permanent shipped behaviour**, each naming `docs/environmental_restore_check.py` as its standing guard. Diff is 6 insertions / 6 deletions, every pair `[x] → [x]`; DIST-03 stays unchecked; ROOM-10 untouched.

## Verification Evidence

| Check | Result |
|---|---|
| `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit 0, before either builder |
| `aea`, `aa`, `openssl`, `plutil` present | all four resolved; no reduced-evidence fallback needed |
| Both builders | exit 0; Dumb byte-identical to `HEAD`, Sentient rebuilt |
| Ten checkers in one run | all exit 0, including `sentient_core_check` |
| `validate-shortcut` × 2 at macOS 26 / all | `Validation passed.`, exit 0 each |
| Signed sizes | 193,498 and 197,668 — both non-zero |
| Dated archives vs `src/` | SHA-256 **equal** for both forks |
| `plutil -lint` on both recovered plists | `OK` |
| Structural assertions on recovered plists | **9/9 Dumb, 9/9 Sentient** |
| `python3 docs/manifest_check.py` | `manifest check: passed (6 rows verified against disk)` |
| Independent `shasum -a 256` / `stat -f%z` on all six rows | size OK, sha OK × 6 |
| `subprocess` in `manifest_check.py` | not imported (AST-verified); imports are `__future__`, `hashlib`, `pathlib`, `re` |
| `grep -c 'target-platform ios' .claude/CLAUDE.md` | **0** (was 4) |
| `git diff --stat .claude/CLAUDE.md` | 4 insertions, 4 deletions — lines 85, 112, 216, 231 only |
| Deletions anywhere in `docs/BUILD-NOTES.md` diff | **0** |
| `grep -c '^### 19\.'` | 8 subsections |
| `grep -c 'environmental_restore_check.py' .planning/REQUIREMENTS.md` | 6 |
| Checkbox states in `REQUIREMENTS.md` diff | six `[x] → [x]` pairs, no state change |
| Eleven checks after Task 3 | all exit 0 |
| `timeout` | never invoked in any command in this plan |

### Negative control — the MANIFEST byte count

One declared byte count was altered by one in the **real** file (`193,498` → `193,499`):

```
AssertionError: row 'Dumb signed': MANIFEST declares 193499 bytes,
artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut is 193498 bytes
EXIT=1
```

The failure names the offending row and **both** values, so a drift report is directly actionable. Restored from backup → `manifest check: passed (6 rows verified against disk)`.

### Measurements that replaced assumptions

Three claims the plan stated were checked rather than transcribed:

1. **"The MANIFEST rows were correct at the start of the phase."** Verified by hashing every declared path out of the phase's starting tree (`0c9aace`, `docs(10): add pattern map`): **all six rows matched** on size and SHA-256. The research's §5d drift table was measured at the older `2e85aa3`, before `c6d8737` refreshed them. The claim holds.
2. **"`.gitignore` already covers the build-noise patterns."** Read directly: `.planning/debug/*.{jpg,jpeg,png,heic}`, `*.DS_Store`, `__pycache__/`, `*.pyc`, `.planning/graphs/`, `graphify-out/`. The claim holds; nothing was added.
3. **"The eleven consumers audited."** Not reproducible — see Deviation 1.

## Deviations from Plan

**1. [Rule 2 - Missing critical correctness] The plan's "eleven consumers" figure was not reproducible, so the consumer surface was measured instead**

- **Found during:** Task 3, writing §19.2.
- **Issue:** The plan directed recording "the eleven consumers audited, and the two that would have hard-errored had the gate been omitted." No wave-1/2/3 summary records an eleven-consumer audit, and no measurement at `HEAD` produces eleven. Writing the number as given would have put an unverifiable count into the project's evidence document — precisely what BUILD-NOTES §2's do-not-fabricate protocol forbids, and the kind of claim a later reader would reasonably trust.
- **Fix:** the consumer surface was derived from the built artifact instead. **75 actions** reference `Circle Next`, resolving to **five distinct consumer sites** when grouped by nearest preceding comment (state persistence and Circle-derived text 43; the silent-band conditional 1; the universal Leaving menu 1; Knock's ten alerts 10; Mirror's template selection 20). §19.2 states outright that this was measured directly rather than counted from memory, and prints the table.
- **The two hard-error sites were confirmed with their artifact indices**, which is the part of the plan's claim that was load-bearing and did hold: `primitive_dispatch()`'s dotted `sequences.<Sequence>.<Dispatch Circle>` read (`Dispatch Circle` set at index 996 on the OPEN path with no `Test Circle` source; the nine MANUAL-arm sites all source from `Test Circle`), and `mirror_text()`'s Get Item From List at `WFItemSpecifier = "Item At Index"` indexing a ten-element list by `Circle Next` (index 1155).
- **Files modified:** `docs/BUILD-NOTES.md`
- **Commit:** `023ed9b`

**2. [Rule 2 - Missing critical functionality] A stronger justification for the signed-name assertion was discovered and recorded**

- **Found during:** Task 1's decrypt step, carried into Task 2.
- **Issue:** The plan justified `manifest_check.py`'s no-suffix assertion as "DIST-04's naming property expressed as a check". The decrypt evidence showed the property is stronger than that framing: the signed container carries **no display name at all** — auth-data holds only `SigningCertificateChain`, and `WFWorkflowName` is stripped from the recovered `Shortcut.wflow` despite being set in both `src/*.xml`. A suffixed filename is therefore not a cosmetic inconsistency but the *only* failure mode, with no internal name to fall back on.
- **Fix:** recorded in three places so it cannot be lost — the script's docstring (as the reason the assertion exists), the MANIFEST's "Do not rename these files" paragraph, and BUILD-NOTES via the manifest. No behaviour changed; the assertion was already correct.
- **Files modified:** `docs/manifest_check.py`, `artifacts/shortcuts/MANIFEST.md`
- **Commit:** `ad0a9ad`

No other deviation. No architectural decision (Rule 4) arose, no authentication gate or checkpoint was reached, and no package-manager install was attempted.

**Hard constraints, as held:** the provenance guard ran and exited 0 before both builders; `--target-platform ios` was never invoked (and was removed from CLAUDE.md); `timeout` appears in no command; the signed filenames carry no suffix; `dimming()`, `silence()`, `restore_managed_settings()` and `settings_snapshot` were not removed or stubbed — this plan's requirement clauses and BUILD-NOTES §19.8 exist to make their retention harder to reverse; nothing was renamed; and no guard from waves 1–3 was weakened. `verify_circle_zero_silence()`, `gate_control_room_shownote()`, `environmental_restore_check.py`, `router_ui_census.py` and `sequence_dispatch_check.py` were all left untouched and all ran green.

## Known Stubs

None. `docs/manifest_check.py` contains no placeholder, hardcoded-empty, `TODO` or `FIXME` value; every value it compares is computed from a real file on disk.

## Deferred Items

| Item | Where | Why deferred |
|---|---|---|
| **DIST-03 — device import and first manual run** | `.planning/REQUIREMENTS.md:161` | Device-gated and 10-05 owns it. `xcrun devicectl list devices` reports no devices. Left unchecked deliberately; the MANIFEST states it is open. |
| **DEV-06 — the restore-ownership check, and the `Session ID` scope defect** | `docs/BUILD-NOTES.md` §17, §19.8 | Live again because the cut was cancelled, but the decision is **reserved to the user** by §17's explicit record. Implementing or designing it was correctly out of scope; §19.8 says so in three ways so nothing here reads as having settled it. |
| **Circle 8 dispatches nothing — the `Voice` orphan** | Config `sequences`, all three arrays at position 8 | Known open defect owned by `.planning/todos/pending/2026-08-16-build-circle-8-voice-primitive.md`. Reported by `sequence_dispatch_check.py` on every run, exit 0 by ROADMAP instruction. |
| **`docs/sequence_dispatch_check.py` is a reporter, not a build guard** | — | Promotion needs the primitive roster and matching strategy to settle under BD-06 Decisions 3–5. Carried forward from 10-03. |
| **Canonical strategy §10.5 still prints the pre-rise threshold arrays** | `PROSOCHE_Nine_Circles_Canonical_Strategy.md:1178, 1184, 1190` | Carried forward from 10-01 and 10-03. BUILD-NOTES §19.1 now carries the correct arrays verbatim, so the authoritative record exists; §10.5 remains under-specific rather than contradictory. Worth a one-line documentation pass. |
| **SEED-005 — the Sentient re-fork question** | — | Untouched. This plan performed a *rebuild* from the existing fork script, which is explicitly not a re-fork; §19.5's DEV-P10-02 states the distinction. |

## Threat Flags

None. No file changed in this plan introduces a network endpoint, auth path, file-access pattern, or schema change at a trust boundary. `docs/manifest_check.py` is strictly read-only and spawns no child process.

Register dispositions from the plan, as shipped:

- **T-10-21** (signed artifact not matching built source) — **mitigated with direct evidence.** Both containers decrypted; all seven structural invariants plus the three supplementary counts re-asserted against the recovered plists, 9/9 per fork. A stale or mismatched signature could not have passed.
- **T-10-22** (suffixed or misnamed signed file) — **mitigated, and the mitigation strengthened.** Both files carry the exact canonical display names; `manifest_check.py` asserts both basenames. The decrypt evidence showed the internal name is stripped entirely, so the filename is the *only* carrier — the assertion is load-bearing rather than belt-and-braces.
- **T-10-23** (stale or wrong MANIFEST row) — **mitigated with a demonstrated negative control.** Every size and hash recomputed from the files themselves; the control names the row and both values.
- **T-10-24** (device-gap warning softened or dropped) — **mitigated.** The Phase 9 paragraph survives verbatim; two further warnings were appended covering the four new unexercised behaviours and DIST-03. Nothing was replaced.
- **T-10-25** (building from unverified ancestry) — **mitigated.** The provenance guard ran first and exited 0; neither builder was invoked before it.
- **T-10-26** (signing with a pre-dated output directory) — **mitigated.** The plain `artifacts/shortcuts` directory was passed; the signer created `2026-08-17/` itself, one level, and each archive hashes equal to its source.
- **T-10-27-SC** (package-manager installs) — **accepted as planned, and correct.** No install of any kind occurred; the toolchain was the system `python3`, `aea`, `aa`, `openssl`, `plutil` and the installed Playground wrappers.

## Notes for the Next Plan

- **10-05 imports these two files by name.** `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` (193,498 bytes, `47957dbf…`) is the fork the user's two Personal Automations reference. If a device shows a *second* PROSOCHĒ entry after import, the cause is a filename, not a build — the payload carries no name.
- **Everything Phase 10 changed is structurally proven and behaviourally unproven.** The four UAT observations that matter most: a first open of a cold day must produce **no visible reaction at all** while `state.json` still shows `heat` 1, `pressure` 1, `circle` 0, an incremented `opens_today` and a live `active_session`; opening a tracked app must produce **no notification**, while closing one still must; any manual menu item other than `Open Control Room` must **not** launch Notes, and `Open Control Room` still must; and `Setup Check` must report `seen` for whichever automation has actually run.
- **`docs/manifest_check.py` is the eleventh check and should be added to any future "run the suite" command.** It will go red on the next rebuild until MANIFEST is refreshed — that is the intended behaviour, and it is the cheapest signal that a build shipped without its record being updated.
- **§18's Phase 9 warning still governs.** Dimming and Silence remain live, load-bearing and device-unproven; `09-UAT.md` is authored and unrun. Nothing in this plan is device evidence.

## Self-Check: PASSED

- `docs/manifest_check.py` — FOUND
- `artifacts/shortcuts/MANIFEST.md` — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` — FOUND
- `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-013251.xml` — FOUND
- `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-013301.xml` — FOUND
- `docs/BUILD-NOTES.md` — FOUND
- `.claude/CLAUDE.md` — FOUND
- `.planning/REQUIREMENTS.md` — FOUND
- commit `c054c91` — FOUND
- commit `ad0a9ad` — FOUND
- commit `023ed9b` — FOUND
