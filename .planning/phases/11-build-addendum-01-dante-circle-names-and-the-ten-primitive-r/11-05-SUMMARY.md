---
phase: 11-build-addendum-01-dante-circle-names-and-the-ten-primitive-r
plan: 05
subsystem: state-engine
tags: [panic-escape, removable-bypass, schema-version, note-setting, site-counts, safety-separation]
requires:
  - "BD-06-A3 (plan 11-04) — the schema_version 2→3 disposition and the three-literal implementation surface"
  - "BD-06-A1 Amendment 3 — the user statement that there is no installed base"
  - "tools/plist_text_edit.py (plan 11-01) — the guarded WFTextTokenString round trip"
provides:
  - "panic_escape_enabled — a flat, top-level, numeric state field gating the Leaving bypass"
  - "verify_panic_escape_seed() — a build guard for the seed, the read shape and the gate code"
  - "A stable ## PANIC ESCAPE Note section and an eleventh MANUAL menu item, both directions"
  - "SCHEMA_VERSION / SCHEMA_VERSION_PREVIOUS / SCHEMA_VERSION_ACCEPTED — the three literals, named once"
  - "Measured site-count tables at eleven primitive_dispatch() renderings: 15/15/22, coerced 15/4"
affects:
  - "11-06 — inherits schema_version 3; must NOT bump it again for the fork rename"
  - "Any future plan adding a primitive_dispatch() rendering — both site tables move by exactly one rendering"
tech-stack:
  added: []
  patterns:
    - "Gate a whole menu rather than suppressing a case, to preserve an exactly-one-menu structural invariant"
    - "Flag-in-menu / work-in-refresh: a MANUAL menu case raises a request flag, the Note read runs later once Control Room Note is bound"
    - "Idempotent generator seeder + separate verifier for every bootstrap-template field"
key-files:
  created: []
  modified:
    - "tools/build_state_engine.py — universal_leaving() gate, seed_panic_escape(), verify_panic_escape_seed(), panic_escape_branch(), the eleventh menu item, the three schema literals"
    - "src/PROSOCHE-Dumb.xml — the flag seed, the ## PANIC ESCAPE Note section, the gated OPEN path, the new MANUAL branch"
    - "src/PROSOCHE-Sentient.xml — regenerated from the fresh Dumb source"
    - "docs/environmental_restore_check.py — EXPECTED_SITES 14/14/20 → 15/15/22, derivation rewritten"
    - "docs/phase9_self_check.py — expected_counts 14/14 → 15/15, expected_coerced 14/4 → 15/4, derivation rewritten"
    - "docs/phase7_self_check.py — the order-sensitive MENU list gained an eleventh item"
    - "artifacts/shortcuts/MANIFEST.md — six rows refreshed, new prose and a new warning block"
    - "docs/BUILD-NOTES.md — §24 appended, 220 insertions, 0 deletions"
    - "artifacts/shortcuts/PROSOCHĒ — Nine Circles — {Dumb,Sentient}.shortcut — re-signed"
    - "artifacts/shortcuts/2026-08-17/*-1201{24,36}.xml — the two pre-sign archives"
decisions:
  - "Mechanism A (gate the whole menu) over Mechanism B (hoist the dispatch out), accepting an eleventh rendering to avoid restructuring the OPEN arm"
  - "The flag is FLAT and top-level, and the gate is numeric > 0 — both forced by the verified runtime semantics, not chosen for style"
  - "Seeded via an idempotent generator pass rather than a one-time plist_text_edit hand edit, matching the two existing precedents for the same template"
  - "The Note read lives in manual_note_refresh(), not the menu case: Control Room Note is not bound until after the whole menu block"
  - "Site counts MEASURED after the rebuild; research's projected coerced-volume 5 was not transcribed — the artifact measures 4"
  - "Gate B (--target-macos 27) deliberately not run: advisory, permanently waivered, and this plan asserts target 27 appears nowhere in the commands run"
metrics:
  duration: ~90 min
  completed: 2026-08-17
  tasks: 3
  files: 12
status: complete
---

# Phase 11 Plan 05: Panic Escape made deliberately removable Summary

Panic Escape — the `Leaving` bypass offered before every intervention — is now gated on a flat
numeric state field, removable by two deliberate acts and restorable by the same route, with
Emergency Restore proven untouched on both decrypted payloads.

## What Was Done

### Task 1 — the flag, the gate, the schema bump, the site tables (commit `6abdf96`)

**The flag.** `panic_escape_enabled` is seeded `1` **flat at the top level** of the bootstrap
`state.json` template. Both properties are forced by this project's device-verified runtime
semantics rather than chosen: a **dotted** read whose final segment is absent is a **hard
error**, so a nested field could not be gated at all on a `state.json` written before it
existed — the read would raise before any conditional saw it. A **flat** read of a missing key
returns nothing, no error.

**The gate.** `universal_leaving()` reads the flag and wraps its existing block in
`if_block("Panic Escape Enabled", 2, number=0)` — a numeric `> 0` test, never a condition-100
existence test. Condition 100 reads **TRUE** for the string `"null"` and for `""`, which are
exactly the states that must read as *removed*; `> 0` reads false for `0`, missing, `null` and
`""` under every device-measured coercion.

**Mechanism A, and why.** Only the enabled arm emits the menu, so
`verify_circle_zero_silence()` property (b) — **exactly one** `["Leaving","Continue"]` menu,
enclosed by the `Circle Next > 0` band — still holds. `universal_leaving()` is called from
inside that band, so **both** arms inherit the enclosure, which is what keeps property (c) and
`docs/router_ui_census.py` green for the otherwise arm's new dotted `sequences.` read. The
otherwise arm renders `primitive_dispatch()` **verbatim**, so no capture-and-restore gate is
skipped on the no-bypass path (T-11-23).

**The schema bump, all three literals in one commit.** BD-06-A3 Decision 1 implemented exactly:
`schema_version` 2 → 3 across the template seed, the **recognition tuple**, and the runtime
validity-gate literal. All three now derive from named constants (`SCHEMA_VERSION`,
`SCHEMA_VERSION_PREVIOUS`, `SCHEMA_VERSION_ACCEPTED`) so they cannot drift apart again, and the
pass now *asserts* the template carries an accepted version rather than assuming it. No
migration, dual-key alias or read-time normalisation was built — BD-06-A1 forbids all three by
name.

### Task 2 — the removal-and-restore path (commit `d40e8b4`)

**The Note.** A stable `## PANIC ESCAPE` section, inserted through `tools/plist_text_edit.py`'s
guarded round trip immediately before `## MY PHONE, ON PURPOSE`. That position is load-bearing:
`manual_note_refresh()` **appends** a fresh `## CURRENT SETTINGS` block on every state-changing
manual run, so a setting placed in an appended region would be shadowed by its own duplicates.
The section carries exactly one editable line, `- Panic Escape: ON`, and prose naming Emergency
Restore as unaffected **689 characters** after the heading.

**The menu item.** An eleventh MANUAL item, `Panic Escape`, emitted last so the case order
matches `WFMenuItems` element for element. `docs/phase7_self_check.py`'s order-sensitive `MENU`
list moved in the same commit.

**The branch.** Bounded `text.match` on the section, a condition-99 test against the exact
literal `- Panic Escape: OFF`, then a two-item confirmation in **each** direction. Only the
confirm case writes the flag, saves state and appends one ledger line naming the change, its
time, and Emergency Restore as unaffected. If the Note and the flag already agree, nothing is
written and nothing is recorded. A missing or reworded section yields an empty match, fails the
contains test, and takes the otherwise arm — so an unreadable Note can only ever **restore**,
never remove.

### Task 3 — rebuild, validate, sign, decrypt-verify, record (commit `8af570a`)

RESEARCH §10 sequence in order. Both forks validated clean under gate A, signed under their
canonical display names with an explicit `--name`, decrypt-verified through the AEA1 recipe,
`MANIFEST.md` refreshed from disk, and `docs/BUILD-NOTES.md` §24 appended.

## The Measured Site Counts

Requested explicitly by the plan's acceptance criteria. Every number below was **read off the
rebuilt artifact**, not transcribed from the research projection.

| Count | Before (10 renderings) | After (11 renderings) | Delta | What explains it |
|---|---:|---:|---:|---|
| Set Brightness | 14 | **15** | +1 | one more `dimming()` |
| Set Volume | 14 | **15** | +1 | one more `silence()` |
| Get Device Details | 20 | **22** | +2 | one `Current Brightness` + one `Current Volume` |
| Coerced Set Brightness | 14 | **15** | +1 | `Dim Target` is `read_value()`-sourced (Text), so every site needs the coercion |
| Coerced Set Volume | 4 | **4** | **0** | `Silence Target` is `number()`-sourced, already Number-typed, so all 11 stay uncoerced |

**Which delta the additional rendering explains: all of them, and nothing more.** One extra
`primitive_dispatch()` rendering emits one `dimming()` and one `silence()`. `dimming()` emits
one Set Brightness plus one Get Device Details; `silence()` emits one Set Volume plus one Get
Device Details. That is exactly +1 / +1 / +2, and it is exactly what was measured — in `src/`
and again in both decrypted payloads. The composite split moved 28 → **30** sites, 18 → **19**
coerced.

Both tables and both derivation comments changed together, in the same commit, as required.

## Key Decisions

**Mechanism A over Mechanism B.** Hoisting the dispatch out of the menu would have kept the
count at ten renderings, but it restructures the OPEN arm's control flow — which
`verify_circle_zero_silence()`, `verify_router_shape()` and `router_ui_census.py` all reason
about — and whether a trailing `is.workflow.actions.exit` after `record_exit_and_route()`'s own
routing is needed or harmful was **unverified**. Mechanism A touches the least structure, and
this project's entire guard suite is built on structural stability. The cost, roughly 200
actions, was paid deliberately.

**The flag is FLAT, and the gate is numeric.** Restated here because it is the decision most
likely to be undone by someone tidying the state shape later. Nesting the field under a
`settings` object would look neater and would make the removal path **unimplementable**: the
dotted read raises before the gate can read false. This is now enforced, not merely documented
— `verify_panic_escape_seed()` fails the build on any dotted read of the flag or any
non-numeric gate on it.

**Copy discipline held in both directions.** Neither confirmation recommends an answer; each
states what the chosen option does. Neither implies Emergency Restore is being removed — both
name it as unaffected, as do both ledger lines and the Note section.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 — missing critical functionality] `verify_state_seed()` does not cover this field**

- **Found during:** Task 1, while wiring the seed
- **Issue:** The plan states that "`verify_state_seed()` asserts that every state read has a
  seeded counterpart, and an unseeded read would fail the build." Measured, it does not: its
  read-side scan is scoped to keys rooted at `settings_snapshot` (`key.split(".")[0] ==
  "settings_snapshot"`). An unseeded `panic_escape_enabled` would have passed the build cleanly
  and been **dead on every device** — the gate would read a key that is simply not there.
- **Fix:** added `verify_panic_escape_seed()`, wired into `main()` beside the two existing seed
  verifiers. It asserts the top-level numeric seed, forbids any dotted read of the flag, and
  forbids a condition-100/101 gate on it. The measurement is recorded in the function's own
  docstring so the next reader does not repeat the assumption.
- **Commit:** `6abdf96`

**2. [Rule 3 — blocking] The Note read cannot live in the menu case**

- **Found during:** Task 2
- **Issue:** The plan directs the branch body into the new MANUAL menu case, citing the
  `Sync My Profile` branch as the working precedent for the `gettext → text.match → set_value`
  chain. Measured: `Control Room Note` is bound by the Find Notes / Create Note pair at artifact
  indices 4282–4300, **after** the entire manual menu block (1664–4281). A `gettext` of that
  variable inside a menu case would reference an unbound variable at runtime — a failure no
  validator, catalog lookup or decrypt can see. And `Sync My Profile` does **not** do what the
  plan describes: its menu case only raises `Manual Sync Requested`; the parse runs later, in
  `manual_note_refresh()`.
- **Fix:** followed the real precedent. The menu case raises `Manual Panic Escape Requested`;
  `panic_escape_branch()` — called from `manual_note_refresh()`, where the Note is bound — does
  the read, the comparison, the confirmations and the writes. Still MANUAL-arm only, which is
  what the plan's constraint actually protects.
- **Commit:** `d40e8b4`

**3. [Deliberate deviation, recorded] The seed uses the generator, not `plist_text_edit.py`**

- **Found during:** Task 1
- **Issue:** The plan instructs the flag be added to `src/PROSOCHE-Dumb.xml` "using
  `tools/plist_text_edit.py`'s guarded round-trip". The same bootstrap template already has two
  precedents that do it from the **generator**, idempotently — `seed_settings_snapshot()` and
  `seed_pending_exit()` — each paired with a separate verifier so the two cannot drift.
- **Fix:** used the generator precedent (`seed_panic_escape()`). The edit mechanism is
  equivalent: `_replace_in_token()` shifts every downstream attachment offset and re-asserts
  each still lands on a `U+FFFC` placeholder, which is the same guarded round trip
  `plist_text_edit.py` implements standalone, and `docs/note_identity_check.py` independently
  re-verifies every offset in both forks. The gain is that the invariant is re-established on
  every build rather than resting on a one-time hand edit. **The Note body edit did use
  `tools/plist_text_edit.py`, as instructed** — that body is hand-authored source the generator
  only reads.
- **Commit:** `6abdf96`

**4. [Rule 1 — factual correction] The projected coerced-volume count is wrong**

- **Found during:** Task 1, measuring after the rebuild
- **Issue:** `11-RESEARCH.md` §8.2 projects the post-change coerced pair as **15 / 5**. The
  projection contradicts `docs/phase9_self_check.py`'s own derivation comment, which already
  recorded `Silence Target x10 left uncoerced`. An eleventh rendering adds an eleventh
  **uncoerced** volume site, not a coerced one.
- **Fix:** the tables carry the measurement, **15 / 4**, and both derivation comments now state
  why the two halves move asymmetrically. The plan's `<flagged_assumptions>` named exactly this
  as the assumption to close by measurement rather than transcription; it is closed.
- **Commit:** `6abdf96`

### Not a deviation — gate B was correctly not run

`docs/BUILD-NOTES.md` §22 and `.claude/CLAUDE.md` §1 introduced a two-gate validator rule after
this plan was authored. Gate B (`--target-macos 27`) is **advisory, permanently waivered and
structurally incapable of exiting 0**, and CLAUDE.md states explicitly that a plan asserting
target 27 appears nowhere in its commands "remains fully satisfied by gate A alone". Gate A was
run on both forks and passed clean. Target 27 was not invoked.

## Verification

| Check | Result |
|---|---|
| Provenance gate `git merge-base --is-ancestor 7ca8ebb… HEAD` | exit **0**, before every builder run |
| Twelve `docs/*.py` checks, baseline before any edit | **12/12 green** |
| Twelve `docs/*.py` checks, final | **12/12 green** |
| Builder idempotence | second and third consecutive runs leave `src/PROSOCHE-Dumb.xml` byte-identical (`4ce1eb4e…`, then `7ddd94b7…` after Task 2); `git status --short` empty after a post-commit rebuild |
| Exactly one `["Leaving","Continue"]` menu | **1** per fork, in `src/` and both payloads |
| Emergency Restore surfaces | **2** menus + **2** case bodies per fork, **none enclosed by a Panic Escape conditional**, measured on both decrypted payloads |
| `Emergency Restore` literal occurrences | **7** at the phase baseline → **14** per fork; increased, never reduced |
| Flag seeded flat, top level, `== 1` | read back from the template JSON in both forks |
| Panic Escape gate condition codes | all **2** (greater than); **0** condition-100/101 gates |
| Dotted reads of the flag | **0** |
| Both write directions | **2** `setvalueforkey` writes in **2** distinct control-flow groups, per fork |
| Manual menu | **11** items; every `choosefrommenu` group's `WFMenuItems` == its ordered case titles, both forks |
| Note section order | `## PANIC ESCAPE` precedes `## MY PHONE, ON PURPOSE`; `Emergency Restore` **689** chars after the heading |
| Note-parsing actions in the OPEN / CLOSE arms | **0** in both forks (Sentient's one OPEN-arm `text.match` is the pre-existing `(ALLOW\|CHALLENGE\|DENY)` model-token parse) |
| Attachment invariant | **1,205** (Dumb) / **1,209** (Sentient) token strings, **0** offset mismatches, in `src/` and both payloads |
| Note-body attachment offsets after the 1,157-char insert | 6982 / 7013 → **8139 / 8170**, exactly the inserted length |
| Site counts | **15 / 15 / 22**, coerced **15 / 4**, in `src/` and both payloads |
| `schema_version` | template **3**, runtime gate literal **"3"**, both present in both payloads |
| Validator gate A ×2 | `Validation passed.`, exit **0** |
| Signed artifacts | **233,976 B** / **238,171 B**, canonical basenames, no suffix, non-zero |
| Dated archive SHA-256 == `src/` counterpart | `7ddd94b7…` == `7ddd94b7…`; `c04f7364…` == `c04f7364…` |
| Decrypt-verify | `plutil -lint` **OK** ×2; `## PANIC ESCAPE` ×5, `panic_escape_enabled` ×7 per payload |
| `docs/manifest_check.py` after the refresh | passed, 6 rows verified against disk |
| `docs/BUILD-NOTES.md` append-only | **220 insertions, 0 deletions** for this plan's own edit; the 3 deletions a baseline-relative diff reports against `f4e47f9` belong entirely to prior in-phase commits (408/3 at HEAD beforehand). 220+408=628 ✓, 0+3=3 ✓ |
| `--target-macos 27`, `--target-platform ios`, `timeout` | never invoked |

## What This Does NOT Establish

**DIST-03 is open. No iPhone is connected and no device has run either build.** Every row above
is structural. In particular, none of the following is observed:

- that a user editing the setting line and confirming actually removes the bypass;
- that the restore direction actually restores it;
- that the bounded `text.match` binds to the intended section on a real Note carrying appended
  `## CURRENT SETTINGS` blocks;
- that the numeric `> 0` gate resolves as intended against a Text-coerced operand on device —
  `.claude/CLAUDE.md` records that operator/operand type validity is **invisible in the plist**
  and can only be settled by inspecting the imported shortcut;
- that a device holding `"schema_version": "2"` takes the rebuild branch on its next run.

Structural proof is not behavioural proof, and nothing here is described as device-verified.

## Known Stubs

None. Every surface this plan added is wired to a real read and a real write: the flag is
seeded, read, gated, written in both directions and asserted; the Note section is real copy
bound to a real `text.match`; both confirmation menus have real case bodies; both ledger lines
are real `appendnote` calls. No placeholder text, no empty default flowing to a UI, no TODO.

## Threat Flags

None. This plan introduces no network endpoint, no auth path and no new file-access pattern.
It does introduce one **schema change at a trust boundary**, and it is not new surface: it is
`T-11-19`'s `schema_version` bump, decided and costed in BD-06-A3 and implemented here exactly
as recorded.

Register dispositions from the plan's own `<threat_model>`:

| Threat | Disposition | How it was discharged |
|---|---|---|
| `T-11-22` — bypass removed **and** Emergency Restore unreachable | **mitigated** | Emergency Restore is not represented by the flag, not enclosed by any conditional added here, and remains a manual item plus one of two cool-down options. Asserted per fork in `src/` **and re-asserted on both decrypted payloads**; occurrences rose 7 → 14, never fell |
| `T-11-23` — an environmental primitive reached without its capture-and-restore gate | **mitigated** | the otherwise arm renders `primitive_dispatch()` verbatim; `verify_restore_gates()` and `verify_sentinel_gates()` green per fork; both site tables at measured values with every delta explained by exactly one rendering |
| `T-11-24` — the gate reading false for the wrong reason | **mitigated** | flat top-level key, seeded, numeric `> 0`; `verify_panic_escape_seed()` now fails the build on a dotted read or a non-numeric gate |
| `T-11-25` — a new OPEN-arm surface outside the silent band | **mitigated** | the confirmation lives in the MANUAL arm; the new conditional sits inside the band so both arms inherit the enclosure; `verify_circle_zero_silence()` and `router_ui_census.py` green |
| `T-11-26` — removal by accident | **mitigated** | two deliberate acts, neither sufficient alone; the restore direction uses the same two acts |
| `T-11-27` — nudging copy | **mitigated** | neither prompt recommends an answer; the section, both prompts and both ledger lines name Emergency Restore as unaffected |
| `T-11-28` — menu items drifting out of order | **mitigated** | every `choosefrommenu` group's items proven equal to its ordered case titles in both forks; `phase7_self_check.py`'s list moved in the same commit |
| `T-11-SC` — package-manager installs | **not triggered** | no install command was run; no third-party import added |

## Self-Check: PASSED

- `.planning/phases/11-…/11-05-SUMMARY.md` — this file — **FOUND**
- `tools/build_state_engine.py`, `src/PROSOCHE-Dumb.xml`, `src/PROSOCHE-Sentient.xml`,
  `docs/environmental_restore_check.py`, `docs/phase9_self_check.py`,
  `docs/phase7_self_check.py`, `artifacts/shortcuts/MANIFEST.md`, `docs/BUILD-NOTES.md` — all
  **FOUND**, all present in `git diff --name-only 98b213b HEAD`
- Both signed `.shortcut` files and both dated archives — **FOUND**, non-zero, hashes recorded
- Commits `6abdf96`, `d40e8b4`, `8af570a` — all **FOUND** in `git log`
- Twelve structural checks green at the final commit — **VERIFIED**
- `git status --short` empty after the final commit — **VERIFIED**
