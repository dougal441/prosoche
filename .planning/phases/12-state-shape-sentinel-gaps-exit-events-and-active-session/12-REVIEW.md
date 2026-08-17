---
phase: 12-state-shape-sentinel-gaps-exit-events-and-active-session
reviewed: 2026-08-17T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - artifacts/shortcuts/MANIFEST.md
  - docs/BUILD-NOTES.md
  - docs/state_engine_self_check.py
  - src/PROSOCHE-Dumb.xml
  - src/PROSOCHE-Sentient.xml
  - tools/build_sentient.py
  - tools/build_state_engine.py
findings:
  critical: 0
  warning: 2
  info: 1
  total: 3
status: issues_found
---

# Phase 12: Code Review Report

**Reviewed:** 2026-08-17
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

This phase closes three state-shape sentinel gaps in the plist generator
(`tools/build_state_engine.py`): `exit_events`/`exit_selection_counter`,
`active_session` (container → four-leaf sentinel container), and
`profile_snapshot.create_target_url`. I traced the actual commit range for phase 12
(`da10ad5^..HEAD`, since the `diff_base` supplied in config predates the file's
existence and diffs the whole file), reviewed each new/changed seeder, verifier, and
condition-code conversion against the axis-7 (GATE SEMANTICS) and axis-6 (STATE SHAPE)
discipline the codebase already established, and spot-checked the claims against the
emitted `src/PROSOCHE-Dumb.xml`/`-Sentient.xml` directly (via `plistlib`, not just
grep).

**The Python logic is sound.** `verify_state_seed()`'s generalisation from a
`settings_snapshot`-only filter to a `STATE_READ_SOURCE_VARIABLES`-based scan is
correctly scoped by dictionary identity (`WFInput.Value.VariableName`), not key root,
and correctly excludes `Config`/`Previous Session` reads. The 100→5 condition-code
conversions at `persist_contract()`, `record_exit_and_route()`, `close_pipeline()`,
`route_exit()`'s Create branch, `live_ice_redirect()`, and `manual_emergency_restore()`
are internally consistent with the seeded sentinel invariant, and I confirmed by
direct plist inspection (not just source reading) that the emitted condition codes
match what the generator functions claim (e.g. action 1509's `Captured Session ID`
gate is condition 5 against `"null"`, exactly as `close_pipeline()`'s source says).
`docs/state_engine_self_check.py`'s updated `"active_session.id"` assertion was run
and passes against the current artifact.

**One real, if low-severity, generator bug was found**: `seed_active_session()`
double-indents the emitted `active_session` line in the bootstrap `state.json`
template (4 spaces instead of the sibling keys' 2), because it re-prepends the
anchor line's indent onto a replacement that keeps the anchor's original leading
whitespace in place — the exact class of mistake `seed_settings_snapshot()`,
its own cited "mechanics analog," avoids. This is cosmetically wrong but not a
runtime defect (JSON tolerates the extra whitespace; the resulting document is
correctly parsed by both the Python verifiers and, expectedly, by Shortcuts'
own JSON-consuming actions).

**One documentation-provenance defect**: `artifacts/shortcuts/MANIFEST.md` was
"refreshed" in commit `ea7a0f4` (12-05) but only its six hash/size table rows were
updated — the header, the "no control flow moved" claim, the `schema_version 2→3`
narrative, and every `⚠ This build additionally carries...` warning bullet are all
still describing the *previous* (phase 11 plan 06) rebuild. The file now silently
misrepresents what shipped: it claims schema_version 3 when the artifact it
describes is schema_version 4, and it omits any mention of the `active_session`
leaf-container conversion, `exit_events`, or `create_target_url` — exactly the kind
of change this document's own established convention (a dedicated `⚠` bullet per
phase, explicitly separating "structurally proven" from "device-observed") exists to
flag.

## Warnings

### WR-01: `seed_active_session()` double-indents the emitted bootstrap template line

**File:** `tools/build_state_engine.py:3007-3013` (function `seed_active_session()`)
**Emitted at:** `src/PROSOCHE-Dumb.xml:1476`, `src/PROSOCHE-Sentient.xml:1510`

**Issue:** `seed_active_session()` computes `indent` from the *original*
`'"active_session": null,'` line (which already carries 2 spaces of leading
whitespace, matching its siblings `"last_open_at"`, `"last_close_at"`,
`"last_app"`), then calls:

```python
_replace_in_token(inner, ACTIVE_SESSION_ANCHOR, f'{indent}"active_session": {{{leaves}}},')
```

`_replace_in_token()` only replaces the `ACTIVE_SESSION_ANCHOR` *substring*
(`'"active_session": null,'`) — it does not touch the 2 spaces of whitespace that
precede that substring in the file, which remain untouched. Prepending `indent`
again therefore doubles it. Confirmed in the emitted artifact:

```
  "last_app": null,
    "active_session": {"id": "null", "started_at": "null", "declared_duration_seconds": "null", "intention": "null"},
  "pending_exit": {"type": "null", "timestamp": "null"},
```

Note the 4-space indent on the `active_session` line versus 2 spaces on its
neighbours, in both `src/PROSOCHE-Dumb.xml:1476` and `src/PROSOCHE-Sentient.xml:1510`.

Contrast with `seed_settings_snapshot()` (`tools/build_state_engine.py:2544-2556`),
cited in `seed_active_session()`'s own docstring as "the mechanics analog": its
`_snapshot_seed_text(indent)` helper deliberately does **not** prepend `indent`
before the first line of its replacement (`'"settings_snapshot": {\n' + inner + ...`)
— because it correctly accounts for the fact that the pre-existing indentation
before the anchor is left in place by `_replace_in_token()`. `seed_active_session()`
does not follow that same rule despite citing it as the model.

**Impact:** Purely cosmetic. JSON whitespace between tokens is insignificant, so
`json.loads()` (used by every verifier in this file) and Shortcuts' own Detect
Dictionary / Get Dictionary Value actions parse the resulting `state.json` text
identically either way. No runtime behaviour changes. Flagged as a WARNING rather
than BLOCKER because there is no correctness or safety impact, but it is a genuine
logic defect in the seeder (it doesn't do what its own docstring and cited analog
claim), and it silently ships slightly malformed output that a future edit to this
region (or a future line-anchored assertion) could trip over.

**Fix:** Do not re-prepend `indent` when replacing a same-line anchor whose leading
whitespace is not part of the matched substring — mirror `_snapshot_seed_text()`'s
approach:

```python
def seed_active_session(actions):
    _, inner = _state_template(actions)
    if '"active_session": {' in inner["string"]:
        return
    leaves = ", ".join(f'"{leaf}": "{value}"' for leaf, value in ACTIVE_SESSION_SEED.items())
    _replace_in_token(inner, ACTIVE_SESSION_ANCHOR, f'"active_session": {{{leaves}}},')
```

(The `indent`/`line` lookup becomes unnecessary entirely, since the replacement no
longer needs to reproduce the anchor's own leading whitespace — it's already there.)

### WR-02: `MANIFEST.md`'s "refresh" updated only the hash table, leaving stale prose that misdescribes the shipped artifact

**File:** `artifacts/shortcuts/MANIFEST.md:1-22` (header and opening paragraph), and
the entire prose body through the closing `⚠` bullet list (lines ~194-278)

**Issue:** Commit `ea7a0f4` ("feat(12-05): sign both forks under live display names,
refresh MANIFEST") updated only the six table rows (`src`/`archive`/`signed` × 2
forks — size + SHA-256). It left every other line of the document unchanged:

- The header still reads "Rebuilt 2026-08-17 by phase 11 plan 06" — this is a phase
  12-05 rebuild, not a phase 11-06 one.
- "**This rebuild is a copy and identity change, not a structural one**: both sources
  grew by roughly 0.4 KB, entirely the renamed strings and the Note's new rename
  notice. No control flow moved, no action was added or removed..." — this claim is
  now false for the artifact the table actually describes. Phase 12 added new
  bootstrap state fields (`exit_events`, `exit_selection_counter`,
  `profile_snapshot.create_target_url`), converted `active_session` from a bare
  `null` to a four-leaf container, converted roughly a dozen condition-100 gates to
  condition-5 gates across `persist_contract()`, `record_exit_and_route()`,
  `close_pipeline()`, and `route_exit()`, and reduced `open_pipeline()`'s
  container-write action count. This is exactly the kind of change the "no control
  flow moved" sentence explicitly denies happened.
- "`schema_version` moved 2 → 3, across three coupled literals" — the artifact this
  table now describes carries `schema_version` 4 (phase 12-01's 3→4 bump,
  `tools/build_state_engine.py` `SCHEMA_VERSION = "4"`), not 3. The manifest's own
  narrative is one version behind what it's attesting to.
- The closing `⚠` bullet list — this document's own established convention for
  flagging "this build additionally carries X, none of which has run on a real
  iPhone" per rebuild (present for phases 9, 10, the automation-onboarding fix, the
  guarded-round-trip module, the Note rename, Panic Escape, and the Core/Aware
  rename) — has **no bullet for phase 12 at all**. A reader of this file has no way
  to learn from it that the artifact they're about to import carries the
  `active_session`/`exit_events`/`create_target_url` state-shape changes, or that
  those changes are (per `docs/BUILD-NOTES.md` §27) file-level-proven only and
  unobserved on a real device (`12-UAT.md` recorded `BLOCKED` — no device was
  available).

By contrast, `docs/BUILD-NOTES.md` §26-27 (touched by this same phase) *does* record
all of this accurately, including the explicit device-unobserved status. The defect
is specifically that `MANIFEST.md` — the document `docs/manifest_check.py` treats as
the canonical distribution record, and the one this project's own conventions single
out as carrying provenance warnings — was only partially updated, and the
inconsistency is invisible to any automated check (`manifest_check.py` verifies only
the hash/size table, not the prose).

**Impact:** No functional or security impact — this is a documentation file, not
shipped code. But `.claude/CLAUDE.md` places explicit, repeated weight on this
project's build-provenance discipline (the two-gate rule, the evidence ladder, the
recording duty, "a probe's result is recorded, not consumed") specifically because
this is a safety-relevant behavioural-intervention shortcut. A manifest that
misstates its own artifact's schema version and omits the most recent phase's
changes from its warning-bullet convention undermines exactly the guarantee that
convention exists to provide.

**Fix:** Add a phase-12 paragraph and `⚠` bullet to `MANIFEST.md` following this
document's own established pattern (see the phase 10/11 bullets it already
contains as templates) — cover: `schema_version` 3→4, the `active_session`
container→leaf conversion, `exit_events`/`exit_selection_counter`, and
`create_target_url`, each stated as structurally proven / device-unobserved,
consistent with `docs/BUILD-NOTES.md` §26-27 and the `12-UAT.md` `BLOCKED` verdict.
Update the header date/phase attribution and correct the "schema_version moved 2→3"
and "no control flow moved" sentences, which are now factually wrong about the
artifact the table describes.

## Info

### IN-01: Diff-base scoping note (not a code defect)

The `diff_base` supplied in this review's config (`b21ad362f5a0b034d4a5b8a3b4363d5b92271099^`)
predates the commit that first introduced `tools/build_state_engine.py`,
`tools/build_sentient.py`, and `docs/state_engine_self_check.py` as tracked files at
their current paths (`git diff` against it renders the entire ~4,200-line generator as
"new file"). I did not review the files as if entirely new; I instead located phase
12's actual commit range (`da10ad5^..HEAD`, spanning plans 12-01 through 12-05) via
`git log` and reviewed that diff plus the surrounding unchanged context needed to
verify correctness. No action needed — flagging only so the workflow's diff-base
selection can be revisited for future phase-12-shaped reviews if this recurs.

---

_Reviewed: 2026-08-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
