---
quick_id: 260817-ewg
phase: quick-260817-ewg
plan: 01
type: execute
wave: 1
depends_on: []
autonomous: true
requirements: [QUICK-260817-ewg]
files_modified:
  - .claude/CLAUDE.md
  - docs/BUILD-NOTES.md
  - .planning/research/STACK.md
  - .planning/spikes/CONVENTIONS.md
  - artifacts/shortcuts/MANIFEST.md
  - tools/build_state_engine.py

must_haves:
  truths:
    - "Reading `.claude/CLAUDE.md` §1 alone yields the complete two-gate rule AND the mechanism behind it, with no need to consult any other file."
    - "Every live standing-instruction site that names a validator target points at CLAUDE.md §1 instead of restating a rule of its own."
    - "The mandatory gate command is byte-identical to what it was before this task, so no in-flight Phase 11 plan, no pending todo, and no `docs/*.py` checker breaks."
    - "`docs/BUILD-NOTES.md` carries the 2026-08-17 measurements, the exact index-normalised waiver line, the reproduction commands, and the synthetic-mutation control."
    - "`docs/BUILD-NOTES.md` §13 DEV-01's original text survives verbatim; the correction is appended, never overwritten."
    - "`tools/build_state_engine.py` parses to an identical AST before and after — the change is comment-only."
  artifacts:
    - ".claude/CLAUDE.md §1 `### Exact validator invocation` — the single canonical home of the rule and the mechanism"
    - "docs/BUILD-NOTES.md §22 — the dated rung-1 evidence record with the waiver list"
    - "docs/BUILD-NOTES.md §13 DEV-01 amendment (append-only)"
    - ".planning/research/STACK.md, .planning/spikes/CONVENTIONS.md, artifacts/shortcuts/MANIFEST.md — pointer-only, no independent rule"
  key_links:
    - "CLAUDE.md §1 ↔ BUILD-NOTES §22: the rule and the measurements that justify it must cite each other, or the next agent re-derives the rule a fifth time."
    - "STACK.md ↔ CLAUDE.md §1: STACK.md is the generator source for CLAUDE.md's Technology Stack section. If STACK.md keeps the old rule, a regeneration silently reinstates the bug this task exists to remove."
    - "Gate B's advisory status ↔ Phase 11's in-flight acceptance criteria: Phase 11 plans 03/05 assert that `--target-macos 27` appears nowhere in the commands they run. Gate B must be defined as advisory-only so it never becomes a command an in-flight plan is obliged to run."
---

<objective>
Three project sources disagree on how to invoke the Shortcuts Playground validator, in files
future agents treat as binding. Reconcile them into one rule, stated once, backed by
measurements recorded once.

Purpose: this is the fourth time the validator invocation has been re-derived. Each previous
derivation was written into a different file and none cited the others, so each new agent
found a contradiction and resolved it locally. Fixing the rule without fixing the
one-home-for-the-explanation problem guarantees a fifth round.

Output: `.claude/CLAUDE.md` §1 becomes the single home of the rule and its mechanism;
`docs/BUILD-NOTES.md` §22 becomes the single home of the evidence; four other sites become
pointers; one code comment that this task falsifies is corrected.

**This plan is documentation reconciliation only.** It changes no build logic, rebuilds no
fork, re-signs nothing, and does not touch `src/`.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@.claude/CLAUDE.md
@docs/BUILD-NOTES.md
@.planning/research/STACK.md
@.planning/spikes/CONVENTIONS.md
@artifacts/shortcuts/MANIFEST.md
</context>

<the_finding>

## What was measured, and what it changes

All figures below were measured during planning against the working tree at commit `0119405`
using plugin `1.2.1`. **Record them as measured. You may re-run any of them to confirm — the
commands are given — but do not replace a measured number with an inferred one.**

### 1. The mechanism (read from the validator source, not inferred)

`skills/shortcuts-playground/scripts/validate_shortcut.py` in plugin `1.2.1`:

- `:864-889` `resolve_target_platform` — `all` / `any` / `latest` all normalise to Python
  `None`; `ios`/`ipados`/`iphone`/`ipad` → `"ios"`; everything else → `"macos"`.
- `:892-1019` — bundled ToolKit snapshots are filtered by two independent gates: a minimum
  target-macOS-major check and a platform-label check. `toolkit-v63` is macOS-labelled;
  `toolkit-v78-ios27` is a v78/27 capture. So `--target-macos 26 --target-platform ios`
  admits **no snapshot at all**.
- `:265` `TOOLKIT_PARAMETER_CATALOG_MIN_MACOS_MAJOR = 27`, consumed at `:1086`, `:1162` and
  `:1223`. **Below target-macOS 27 the parameter-key catalog and the enum-case catalog are
  not loaded at all**, on any platform setting.
- `:1039-1046` `_catalog_platforms_match_target` — returns `True` immediately when the target
  platform is `None` (i.e. `all`).
- `:1048-1055` `_catalog_platform_name_matches_target` — `ios` matches only platform names
  beginning `iOS`. Every catalog entry tagged `macOS 27`-only is therefore **excluded from
  parameter-key and enum-case checking** under `--target-platform ios`.
- `:1144-1211` `load_toolkit_parameter_enum_cases`; applied at `:2311-2314`.

### 2. The four invocations, measured

| Invocation | Dumb | Sentient |
|---|---|---|
| `--target-macos 26 --target-platform all` | `Validation passed.` **exit 0** | `Validation passed.` **exit 0** |
| `--target-macos 27 --target-platform all` | **exit 1**, exactly **1** error | **exit 1**, exactly **1** error |
| `--target-macos 27 --target-platform ios` | **exit 1**, exactly **5** errors | **exit 1**, exactly **5** errors |
| `--target-macos 26 --target-platform ios` | rejects essentially every action (empty allowlist) | not re-run |

### 3. Enum-case coverage, measured directly from the loader

`load_toolkit_parameter_enum_cases(skill_dir, macos_major, platform)` returns this many
enum-checked identifiers:

| target | identifiers |
|---|---:|
| macOS 26, any platform | **0** |
| macOS 27, platform `all` (→ `None`) | **1105** |
| macOS 27, platform `macos` | **886** |
| macOS 27, platform `ios` | **455** |

Of the picker parameters **the forks actually emit**, `27 all` enum-checks **14**
`(identifier, key)` pairs and `27 ios` enum-checks **13** — `ios` loses
`is.workflow.actions.appendnote` / `operation`, because that action's catalog entry is
`macOS 27`-tagged. Both forks give identical sets.

### 4. Synthetic-mutation control — proof the second gate has teeth

A scratch copy of the Dumb fork with a single `is.workflow.actions.count` `WFCountType`
changed from `Items` to `Bananas`:

- `--target-macos 26 --target-platform all` → **`Validation passed.`** — blind.
- `--target-macos 27 --target-platform all` → **caught it**:
  `Invalid ToolKit enum value for is.workflow.actions.count.WFCountType at index 574: 'Bananas'. ToolKit v78 allows: 'Characters', 'Items', 'Lines', 'Sentences', 'Words'.`

`src/` was never modified; the mutation lived only in the scratch directory.

### 5. What this means — and where it departs from the task brief

The task brief proposed adopting `--target-macos 27 --target-platform ios` as the advisory
second gate, waivered against a five-row Notes identifier list. **The measurements above say
that is the wrong second gate**, and the brief explicitly invited an evidence-led departure.

`--target-macos 27 --target-platform all` **strictly dominates** it on this project's
artifacts:

- It loads 1105 enum-checked identifiers instead of 455 — a superset, +659.
- It runs parameter-key and enum-case checks on **all four Notes actions**, which the `ios`
  variant skips entirely (their catalog entries are `macOS 27`-tagged, so
  `_catalog_platform_name_matches_target` excludes them).
- It produces **zero** of the five spurious identifier rejections, because it never applies
  the platform-label filter that generates them.
- Its waiver is **one line, not five** — and that line is a *parameter-key* observation with
  device-donor ground truth behind it, which is a far better-grounded waiver than five
  identifier rows waived on a provenance-tag argument.

The `ios` half of the spikes' prescription actively subtracts coverage on exactly the actions
this project depends on most. The spikes were right that a second `--target-macos 27` gate is
the valuable one; they were wrong about the platform flag, and wrong for a reason they had no
way to see without reading the loader.

### 6. The headline — stated plainly

**The empirical check did not reveal a shipped defect.** Both forks pass the mandatory gate
clean. The second gate surfaces exactly one line per fork, and that line is a known,
already-adjudicated, deliberately-retained deviation, not a new finding:

```
- Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.
```

`WFCreateNoteInput` is **device-donor ground truth** from the owner's own iPhone
(`.planning/debug/"Donor - notes.shortcut"`, decrypted 2026-08-14 — `docs/BUILD-NOTES.md`
§14 line 623 and §14 line 654), and the project's evidence hierarchy ranks a donor above the
catalog. `tools/build_state_engine.py:1805` already allowlists it deliberately. The catalog's
`name`/`contents` entry is the `macOS 27`-tagged, less authoritative source.

So: no new information about *these* artifacts. But gate B's value is no longer prospective
hand-waving — §4 above is a measured demonstration that it catches a class of defect gate A
passes clean. Say both things honestly in the record; do not oversell either.

### 7. Do not create a collision with in-flight Phase 11

STATE.md has Phase 11 **executing**. `.planning/phases/11-*/11-03-PLAN.md:303` and
`11-05-PLAN.md:331` both carry an acceptance criterion asserting that `--target-macos 27` and
the iOS platform flag appear nowhere in the commands they run; `11-RESEARCH.md:756` says the
same. **Do not edit any Phase 11 artifact.**

The reconciliation avoids the collision by construction: **gate A is unchanged, and gate B is
advisory — a diagnostic read, never a build gate.** Because gate B carries a permanent waiver
it can never exit 0, so it could not be `&&`-chained into a definition of done even if
someone wanted to. CLAUDE.md §1 must state this explicitly so a Phase 11 executor reading the
new rule does not think their own plan is now wrong. Nothing downstream — no pending todo, no
`docs/*.py` checker, no Phase 11 criterion — changes.

### 8. Concurrent work — handling, stated explicitly

`.planning/spikes/006-picker-serialisation-taxonomy/`, `007-*` and `008-*` are **untracked and
uncommitted**, being written by another session right now. **Handling chosen: option (ii) —
reference without dependency.** No claim in this plan rests on them; every figure above was
measured directly here, including the enum-coverage counts that 006 would otherwise have been
cited for. Mention them in the record only as adjacent concurrent work deliberately not
cited. **Do not read from, write to, or cite 006/007/008.** Also do not touch anything under
`.claude/worktrees/` — those are other sessions' checkouts with their own stale copies of
these same files.

</the_finding>

<the_reconciled_rule>

## The rule to record

**Gate A — mandatory, must pass clean.**
`validate-shortcut <file.xml> --target-macos 26 --target-platform all` → `Validation passed.`,
exit 0. This is the **identifier / availability baseline at the project's real target**.
Unchanged from current practice. Every existing plan, todo and checker that names a validator
command names this one and stays correct.

**Gate B — advisory, waivered, never blocking.**
`validate-shortcut <file.xml> --target-macos 27 --target-platform all` → exit 1 with
**exactly one** error line per fork, the `WFCreateNoteInput` line above. This is the
**parameter-key and picker-literal check**. Gate A performs zero of these checks, measured.

**The waiver, index-normalised so a future run can diff against it:**

| Waived line (indices normalised to `N`) | Count per fork | Why waived |
|---|---:|---|
| `Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension at index N: WFCreateNoteInput. ToolKit v78 expects: OpenWhenRun, contents, folder, interpretAsMarkdown, name.` | 1 | Device-donor ground truth outranks the `macOS 27`-tagged catalog entry — `docs/BUILD-NOTES.md` §14; allowlisted at `tools/build_state_engine.py:1805` |

Real indices at the time of measurement: Dumb `3619`, Sentient `3687`. They shift on rebuild,
which is why the waiver is recorded index-normalised.

**Anything gate B reports outside that waiver is a real finding and must be investigated
before the affected artifact ships.**

**Gate B's own limit — why A stays mandatory.** At `--target-macos 27` the validator may
*accept* an OS27-only parameter key that iOS 26 does not offer. Gate B can therefore produce
false acceptances; it is a supplement to gate A, never a replacement.

**Why the earlier rule went wrong.** The failure was never "`ios` is wrong for an iPhone
project." `--target-platform` selects which bundled ToolKit snapshot the validator consults;
it changes nothing in the plist and nothing about where the shortcut runs. The failure was
the **pairing** of the iOS platform flag with `--target-macos 26`: `toolkit-v63` is
macOS-labelled and gets filtered out by the platform gate, the only iOS snapshot is a v78/27
capture and gets filtered out by the version gate, and the result is an empty allowlist that
rejects everything. The controlling variable is `--target-macos`, not `--target-platform`.

</the_reconciled_rule>

<tasks>

<task type="tracer" tdd="false">
  <name>Task 1: State the rule once in CLAUDE.md §1, record its evidence once in BUILD-NOTES §22</name>
  <files>.claude/CLAUDE.md, docs/BUILD-NOTES.md</files>
  <read_first>
    `.claude/CLAUDE.md` lines 81-90 (`### Exact validator invocation`, currently three bullets).
    `docs/BUILD-NOTES.md` lines 37-84 (§3 evidence protocol and its citation rule) and lines
    1406-1515 (§21, currently the last section — append after it).
    `.claude/CLAUDE.md` lines 207-255 (§9, the evidence-escalation ladder — gate results are
    rung 1, file-level).
  </read_first>
  <action>
    This is the thin end-to-end slice: after this task a reader gets the correct rule from one
    place and can verify it from one other place. Everything else in this plan is expansion.

    First, rewrite `.claude/CLAUDE.md` §1 `### Exact validator invocation` as the single
    canonical home. It must carry, in this order and in full: (a) what each flag actually
    controls — the platform flag selects which bundled ToolKit snapshot is consulted and has
    no bearing on the plist or on where the shortcut runs, while the macOS-major flag gates
    both the snapshot minimum-version filter and, separately, whether the v78 parameter-key
    and enum-case catalogs load at all; (b) gate A as the mandatory identifier/availability
    baseline with its exact command and expected `Validation passed.` exit 0; (c) gate B as
    the advisory parameter-key and picker-literal check with its exact command, its expected
    exit 1, and the one-line index-normalised waiver reproduced verbatim from
    this plan's "The rule to record" section; (d) the explicit statement that gate B is advisory — it can never
    exit 0 because its waiver is permanent, so it must never be chained into a definition of
    done, and a plan authored before today that asserts the 27 target appears nowhere in its
    commands remains satisfied by gate A alone; (e) gate B's false-acceptance limit at target
    27, which is why gate A stays mandatory; (f) the root cause — the pairing of the iOS
    platform flag with the 26 macOS target yields an empty allowlist — stated as the
    mechanism, not as a verdict on either flag alone; (g) why the second gate does not use the
    iOS platform flag, with the measured 1105-vs-455 identifier counts and the 14-vs-13
    emitted-pair counts, naming that the iOS setting excludes every `macOS 27`-tagged catalog
    entry and so skips all four Notes actions; (h) a one-line pointer to the new
    `docs/BUILD-NOTES.md` §22 for the measurements and the reproduction commands.

    Keep the existing first bullet about the plugin default targeting the build machine — it
    is still true and still useful.

    Second, append a new `## 22.` section to `docs/BUILD-NOTES.md` after §21. Date it
    2026-08-17 and attribute it to quick task `260817-ewg`. It records, as rung-1 file-level
    evidence per §9 and satisfying §3's binding citation rule: the six `validate_shortcut.py`
    line citations from this plan's "What was measured" section §1 with the plugin path; the four-invocation results
    table from §2 with exit codes; the enum-coverage table from §3; the emitted-pair counts;
    the synthetic-mutation control from §4 including both the mutation and both gate outcomes;
    the exact index-normalised waiver table; the normalisation command a future run diffs
    against, which is the validator piped through `grep '^- '`, then
    `sed -E 's/ at index [0-9]+:/ at index N:/'`, then `sort`, then `uniq -c`; and the real
    indices measured (Dumb 3619, Sentient 3687) with a note that they shift on rebuild.

    State the headline plainly in §22 and do not soften it: no shipped defect was found. State
    equally plainly that gate B added no new information about the current forks — its one line
    is pre-adjudicated — and that its demonstrated value rests on the synthetic-mutation
    control, not on a finding in these artifacts. Note that spikes 006/007/008 were untracked
    at the time and are deliberately not cited, and that no claim here depends on them.

    §22 records measurements and cites the rule; it must not restate the rule. The rule lives
    in CLAUDE.md §1 only. Follow the precedent §3 line 83 already set for the §9 tooling
    inventory: one home, a pointer from the other, nothing measured restated in two places.

    Do not touch `src/`. Do not touch any Phase 11 artifact. Do not touch spikes 006/007/008
    or anything under `.claude/worktrees/`.
  </action>
  <verify>
    <automated>set -e
PLUG=~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1
# Gate A still passes clean on both forks, unchanged.
for f in src/PROSOCHE-Dumb.xml src/PROSOCHE-Sentient.xml; do
  "$PLUG/bin/validate-shortcut" "$f" --target-macos 26 --target-platform all | grep -q "Validation passed."
done
# Gate B reports exactly the one recorded waiver line on both forks.
for f in src/PROSOCHE-Dumb.xml src/PROSOCHE-Sentient.xml; do
  n=$("$PLUG/bin/validate-shortcut" "$f" --target-macos 27 --target-platform all 2>&1 | grep -c '^- ')
  test "$n" -eq 1
  "$PLUG/bin/validate-shortcut" "$f" --target-macos 27 --target-platform all 2>&1 \
    | grep -q "Unknown AppIntent parameter key(s) for com.apple.mobilenotes.SharingExtension"
done
# src/ untouched by this task.
git diff --quiet -- src/
# CLAUDE.md §1 carries both gate commands and the waiver identifier.
grep -q -- "--target-macos 26 --target-platform all" .claude/CLAUDE.md
grep -q -- "--target-macos 27 --target-platform all" .claude/CLAUDE.md
grep -q "WFCreateNoteInput" .claude/CLAUDE.md
# BUILD-NOTES has a new section 22 that cites the validator source and the waiver.
grep -q "^## 22\." docs/BUILD-NOTES.md
grep -q "validate_shortcut.py" docs/BUILD-NOTES.md
grep -q "TOOLKIT_PARAMETER_CATALOG_MIN_MACOS_MAJOR" docs/BUILD-NOTES.md
grep -q "Bananas" docs/BUILD-NOTES.md
echo TASK1-OK</automated>
  </verify>
  <done>
    `.claude/CLAUDE.md` §1 states the two-gate rule, the mechanism, the waiver, gate B's
    advisory status and its false-acceptance limit, and points at BUILD-NOTES §22 — and a
    reader needs no other file to apply it correctly. `docs/BUILD-NOTES.md` §22 records every
    measurement with its citation and does not restate the rule. Gate A's command and result
    are unchanged. `src/` is untouched.
  </done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: Convert every remaining rule-asserting site into a pointer</name>
  <files>.claude/CLAUDE.md, .planning/research/STACK.md, .planning/spikes/CONVENTIONS.md, artifacts/shortcuts/MANIFEST.md</files>
  <read_first>
    `.claude/CLAUDE.md` lines 108-112 (§2 `### How a shortcut declares iOS-only vs macOS
    actions`), line 265 (Recommended Stack `Validator target` row), line 280 (the `What NOT to
    use` row about the 27/latest target).
    `.planning/research/STACK.md` lines 66-82, 123-128, 320-332, 353-357 — the eight sites
    naming an iOS platform target are at lines 70, 74, 77, 80, 127, 323, 330 and 355.
    `.planning/spikes/CONVENTIONS.md` lines 36-44.
    `artifacts/shortcuts/MANIFEST.md` lines 3-9.
  </read_first>
  <action>
    Every site here currently states a rule of its own. After this task each states the
    operational command it needs and defers the reasoning to CLAUDE.md §1. Use a consistent,
    greppable pointer phrase at every site so the link is mechanically checkable. The required
    token is the literal phrase `two-gate rule`, which must appear at every propagated site
    alongside a reference to `.claude/CLAUDE.md` §1. It is currently absent from all five files,
    measured, so grepping for it is a real gate rather than a tautology — do not substitute a
    synonym at any site, or the check silently passes on four files instead of five.

    In `.claude/CLAUDE.md`: rewrite the §2 practical-rule bullet at line 112 to name both gates
    by pointer and keep its still-true second half about manual import-testing on a real
    iPhone, since the validator cannot execute a Shortcut. Rewrite the Recommended Stack
    `Validator target` row at line 265 to name gate A as mandatory and gate B as advisory, with
    the pointer as its Why cell. The `What NOT to use` row at line 280 is now actively wrong as
    an absolute prohibition, because the 27 target is exactly what gate B requires — rewrite it
    to prohibit the two things that are genuinely wrong: using the 27 target as the sole or
    mandatory gate, given its false-acceptance risk on OS27-only keys; and pairing the iOS
    platform flag with the 26 macOS target, which yields the empty allowlist. Four clauses
    across §1, §2 and these two rows currently attribute the current rule to a correction of an
    earlier one; that framing is what made this a standing contradiction rather than a settled
    rule, so remove it from all four and let §1's mechanism carry the explanation. The
    deviation history is preserved in BUILD-NOTES, which is where it belongs.

    In `.planning/research/STACK.md`: this file is the generator source for CLAUDE.md's
    Technology Stack section, so leaving it stale means a regeneration silently reinstates the
    bug. Do **not** sweep the eight sites to the platform-`all` string — that reproduces the
    original error in the opposite direction, replacing one under-argued absolute with another.
    Each site gets the two-gate treatment appropriate to its context: the two command blocks at
    lines 70 and 74 become both gate commands; the recommendation and rationale at lines 77-80
    become the two-gate rule with the pointer, and the rationale bullet at line 80 asserting the
    iOS setting is required to admit iOS-only rows is the false premise at the root of this
    whole tangle and must be replaced by the measured mechanism, not merely re-flagged; the
    practical rule at line 127 mirrors CLAUDE.md §2; the table row at line 323 mirrors the
    Recommended Stack row; the Craig Loop step at line 330 names gate A as the loop's gate and
    gate B as a post-loop advisory read; the table row at line 355 mirrors the `What NOT to use`
    row.

    In `.planning/spikes/CONVENTIONS.md`: the toolchain-correction bullet at lines 36-44 has the
    best mechanism description anywhere in the repo and was right that a second gate at the 27
    target is the valuable one — keep both of those. Correct its prescription: the second gate
    uses the platform-`all` setting, not the iOS one, and give the measured reason — the iOS
    setting excludes every `macOS 27`-tagged catalog entry, which drops all four Notes actions
    out of parameter-key and enum-case checking and adds five spurious identifier rejections.
    Reframe it from a lone contrarian note into a pointer at CLAUDE.md §1, so it reads as the
    origin of the settled rule rather than as a dissent from it.

    In `artifacts/shortcuts/MANIFEST.md`: lines 6-9 currently assert the platform-`all` target
    as deliberate and attribute it to the DEV-01 deviation. Replace with the two-gate framing —
    these artifacts were built and validated under gate A, and gate B was read against them
    with the one recorded waiver and nothing else. Add the pointer. Change nothing else in the
    file: no hash, no byte count, no warning block, no row. `docs/manifest_check.py` recomputes
    the table from the files themselves and asserts nothing about this prose, but it must still
    pass afterwards.

    Do not touch `src/`, any Phase 11 artifact, spikes 006/007/008, or `.claude/worktrees/`.
  </action>
  <verify>
    <automated>set -e
# Every propagated site carries the canonical pointer token (absent from all 5 before this task).
for f in .claude/CLAUDE.md .planning/research/STACK.md .planning/spikes/CONVENTIONS.md artifacts/shortcuts/MANIFEST.md; do
  grep -q 'two-gate rule' "$f" || { echo "MISSING POINTER: $f"; exit 1; }
done
# The stale attribution framing is gone from the standing-instruction file (was 4 occurrences).
test "$(grep -c 'corrected from' .claude/CLAUDE.md)" -eq 0
# STACK.md and CLAUDE.md now agree on gate A and gate B.
for f in .claude/CLAUDE.md .planning/research/STACK.md; do
  grep -q -- "--target-macos 26 --target-platform all" "$f"
  grep -q -- "--target-macos 27 --target-platform all" "$f"
done
# MANIFEST prose changed but its asserted table did not.
python3 docs/manifest_check.py
git diff --quiet -- src/
# Nothing outside the permitted set was edited.
test -z "$(git status --porcelain -- .planning/phases/ .claude/worktrees/ .planning/spikes/006-picker-serialisation-taxonomy .planning/spikes/007-unresolvable-picker-failure-mode .planning/spikes/008-use-model-picker-literal)"
echo TASK2-OK</automated>
  </verify>
  <done>
    All four files defer their reasoning to CLAUDE.md §1 and none states an independent rule.
    STACK.md's eight sites carry the two-gate rule rather than a swept platform flag, so a
    regeneration of CLAUDE.md's Technology Stack section reproduces the reconciled rule.
    CONVENTIONS.md's prescription is corrected and reframed as the rule's origin. MANIFEST.md's
    prose is updated and `docs/manifest_check.py` still exits 0.
  </done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: Supersede the deviation history append-only, and fix the one comment this task falsifies</name>
  <files>docs/BUILD-NOTES.md, tools/build_state_engine.py</files>
  <read_first>
    `docs/BUILD-NOTES.md` lines 126-142 (§3 `### Validator and signer invocations`), line 574
    (§12's sentence about the plan's literal platform-iOS command), lines 578-586 (§13 DEV-01),
    and lines 249-256 (§5 DEV-04, which records the same measurement from the Phase 2 side).
    `tools/build_state_engine.py` lines 1715-1740 (the `VERIFIED_PARAMETER_KEYS` header
    comment).
  </read_first>
  <action>
    This project keeps its deviation history. **Supersede or amend; never delete.** Every
    original sentence in DEV-01 must survive verbatim.

    In `docs/BUILD-NOTES.md` §3: the command block at line 131 shows a single validate command
    with the iOS platform flag. Replace it with both gate commands, leave the sign command
    alongside it unchanged, and replace the rationale paragraph at line 140 with a pointer to
    CLAUDE.md §1. That paragraph's closing claim — that the iOS platform setting is required to
    admit iOS-only rows and reject macOS-only rows — is the false premise this task retires, so
    say so in one sentence and cite §22, rather than silently dropping it. Keep the
    "necessary but not sufficient" paragraph at line 142 unchanged; it is still true and now
    doubly so.

    In §12, line 574 refers to the plan's literal platform-iOS command reporting every
    pre-existing core action as a false negative. Amend in place with a short dated note: that
    observation was of the 26-plus-iOS pairing, the reconciled rule keeps §12's operative
    command as gate A unchanged, and §22 supersedes the generalisation. Do not rewrite the
    Phase 5 findings around it.

    In §13 DEV-01: leave lines 580-586 exactly as they are and append a dated amendment
    subsection beneath them. It must state, without hedging, which parts of DEV-01 hold and
    which do not. Holds: the 26-plus-iOS pairing is vacuous, its 3675-of-3675 measurement is
    correct, and building on gate A was the right call. Does not hold: the generalisation that
    the iOS platform flag as such carries zero signal — the controlling variable is the macOS
    target, not the platform flag; and the closing expectation that this only becomes
    re-evaluable when a future plugin release ships a corrected iOS snapshot — no new plugin
    was needed, only a corrected pairing. Record that gate B at the 27 target with the
    platform-`all` setting is now adopted as advisory, that it found no defect in the shipped
    forks, and that the synthetic-mutation control in §22 is what establishes it has teeth.
    Cross-reference §5 DEV-04, which recorded the same measurement from the Phase 2 side and is
    amended by the same reasoning.

    In `tools/build_state_engine.py`: the header comment above `VERIFIED_PARAMETER_KEYS` claims
    this build-time guard is the only gate standing between a renamed key and a runtime failure,
    because the bundled validator never loads the parameter catalog at the 26 macOS target. The
    first half stays true — gate A genuinely loads no catalog. The "only gate" claim is
    falsified by gate B, which loads that catalog and, measured, is precisely what surfaced the
    `WFCreateNoteInput` divergence. Correct the comment to say the guard is the only *mandatory*
    gate and that gate B is a second, advisory one, and cite CLAUDE.md §1. **Edit the comment
    text only. Change no dictionary entry, no code, no docstring, no build logic.**

    Do not touch `src/`, any Phase 11 artifact, spikes 006/007/008, or `.claude/worktrees/`.
  </action>
  <verify>
    <automated>set -e
# DEV-01's original measurement survives verbatim — append-only proof.
grep -q "3675 of 3675" docs/BUILD-NOTES.md
grep -q "is.workflow.actions.conditional" docs/BUILD-NOTES.md
# An amendment now sits alongside it and cites the new evidence section.
grep -q "DEV-01" docs/BUILD-NOTES.md
grep -q "^## 22\." docs/BUILD-NOTES.md
# BUILD-NOTES §3 now carries both gate commands.
grep -q -- "--target-macos 26 --target-platform all" docs/BUILD-NOTES.md
grep -q -- "--target-macos 27 --target-platform all" docs/BUILD-NOTES.md
# The builder change is comment-only: identical AST before and after.
python3 -c "
import ast, subprocess
old = subprocess.run(['git','show','HEAD:tools/build_state_engine.py'], capture_output=True, text=True, check=True).stdout
new = open('tools/build_state_engine.py').read()
assert ast.dump(ast.parse(old)) == ast.dump(ast.parse(new)), 'BUILD LOGIC CHANGED - not a comment-only edit'
print('AST-IDENTICAL')
"
# Both forks still validate at gate A, and src/ is untouched.
PLUG=~/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1
for f in src/PROSOCHE-Dumb.xml src/PROSOCHE-Sentient.xml; do
  "$PLUG/bin/validate-shortcut" "$f" --target-macos 26 --target-platform all | grep -q "Validation passed."
done
git diff --quiet -- src/
echo TASK3-OK</automated>
  </verify>
  <done>
    §13 DEV-01's original text is intact with a dated amendment appended that separates what
    held from what did not; §3's command block and §12's sentence are corrected and point at
    the canonical rule; §5 DEV-04 is cross-referenced. `tools/build_state_engine.py` parses to
    an identical AST, proving the edit was comment-only. Gate A still passes on both forks and
    `src/` is unmodified.
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| standing-instruction docs → future agents | `.claude/CLAUDE.md` is injected into every agent's context. A wrong or contradictory rule here propagates silently into shipped artifacts. |
| generator source → generated doc | `.planning/research/STACK.md` is upstream of CLAUDE.md's Technology Stack section; a stale upstream reinstates a retired rule on regeneration. |
| this task ↔ concurrent sessions | Phase 11 is executing and three spikes are being written in parallel, in this repo and in sibling worktrees. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-ewg-01 | Tampering | `tools/build_state_engine.py` | high | mitigate | AST-equality check against `HEAD` in Task 3 proves the edit was comment-only; any code or docstring change fails the task. |
| T-ewg-02 | Tampering | `src/PROSOCHE-*.xml` | high | mitigate | `git diff --quiet -- src/` asserted in all three tasks; no rebuild or re-sign is invoked anywhere in this plan. |
| T-ewg-03 | Repudiation | `docs/BUILD-NOTES.md` §13 DEV-01 | medium | mitigate | Deviation history is append-only; Task 3 verifies the original measurement string survives verbatim rather than trusting the edit. |
| T-ewg-04 | Denial of Service | in-flight Phase 11 execution | medium | mitigate | Gate B is defined as advisory and gate A is left byte-identical, so no Phase 11 acceptance criterion, pending todo, or `docs/*.py` checker changes. Task 2 asserts nothing under `.planning/phases/` was written. |
| T-ewg-05 | Information Disclosure | untracked spikes 006/007/008 | low | accept | No claim depends on them and no task reads or writes them; Task 2 asserts they are unmodified. Their content may change under us, which is precisely why nothing cites them. |
| T-ewg-06 | Tampering | npm/pip/cargo installs | high | accept | No package installs occur in this plan. No new dependency, no new checker script, no new tooling. |
</threat_model>

<verification>
- Gate A: `Validation passed.` exit 0 on both forks, before and after — unchanged.
- Gate B: exit 1 with exactly one error line per fork, matching the recorded waiver verbatim
  once indices are normalised.
- `docs/manifest_check.py` exits 0.
- `tools/build_state_engine.py` parses to an identical AST against `HEAD`.
- `git diff --quiet -- src/` — no shortcut artifact touched.
- Nothing written under `.planning/phases/`, `.claude/worktrees/`, or spikes 006/007/008.
- The canonical pointer string resolves at all five documentation sites.
</verification>

<success_criteria>
- One canonical rule, in `.claude/CLAUDE.md` §1, complete enough to apply without opening
  another file — including the mechanism, so the fifth re-derivation has nothing left to
  re-derive.
- One canonical evidence record, in `docs/BUILD-NOTES.md` §22, carrying the measured numbers,
  the reproduction commands, the index-normalised waiver a future run can diff against, and the
  synthetic-mutation control.
- Five propagation sites reduced to pointers; zero sites still asserting an independent rule.
- Deviation history preserved and superseded, never deleted.
- The mandatory gate command is unchanged, so nothing downstream breaks.
- The headline is recorded plainly and without inflation: no shipped defect was found; gate B
  added no new information about the current artifacts; its demonstrated value rests on a
  synthetic control, not on a discovery.
</success_criteria>

<follow_ups>
Record as a todo rather than acting on it here — out of scope by the task's own limits:

- **Fold gate B into the standard rebuild recipe once Phase 11 closes.** Phase 11's in-flight
  plans assert the 27 target appears nowhere in their commands, so gate B stays a manual
  advisory read until Phase 11 lands. After that, the natural home is the same command chain
  that runs the twelve `docs/*.py` checkers, reading gate B's output against the recorded
  waiver rather than chaining it with `&&`.
- **`VERIFIED_PARAMETER_KEYS` in `tools/build_state_engine.py` is now partly redundant with
  gate B.** Gate B checks parameter keys against the same v78 catalog the hand-maintained
  table was built from. Not touched here — this plan changes no build logic — but worth an
  audit of which entries the automated gate now covers.
</follow_ups>

<output>
Create `.planning/quick/260817-ewg-reconcile-validator-invocation-rule/260817-ewg-SUMMARY.md` when done.
</output>
