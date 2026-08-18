# Shortcut Distribution Manifest

**This table's six hash/size rows describe the PHASE 11 GAP-CLOSURE re-sign (2026-08-18, plan
11-08), superseding the plan 11-07 re-sign whose header block follows immediately below.** Per
this file's own convention, that block is retained as its own rebuild's record and is
superseded by this one wherever the two conflict. Everything else carries forward untouched —
the capture-persistence fix, D-01's zeroed floor and dim target, the retired-clause sweep and
11-07's `text.match` output-name fix. This rebuild carries **one change**, and it is the one
that makes two of the nine interventions intervene at all.

**Dimming and Silence were unreachable, and this build makes them reachable.** Both functions
opened on a `has any value` gate over the `settings_snapshot.<group>` **container**, with the
whole capture-and-apply body — the device read, the snapshot write, the environmental write,
the save, and even the "could not be captured, so nothing was changed" alert — sitting in the
arm taken only when the container is **absent**. `clear_snapshot()` writes the *leaf* and never
the container, deliberately, so that the seeded subtree stays a permanent invariant. The gate
could therefore never read false. Measured against the previously shipped artifact: **44
environmental actions per fork** in the never-taken arm — 22 Get Device Details, 11 Set
Brightness, 11 Set Volume, which is *every* Get Device Details in the artifact and every
non-restore environmental write. A Circle configured to dim or quieten produced **nothing** on
device: no change, no state write, no alert, no error. Plan 11-08 re-gates both onto
`settings_snapshot.<group>.original_value` with the numeric `> 0` test
`restore_managed_settings()` already used, and arms a new build guard,
`verify_environmental_reachability`, in **both** builders with no exemption set. **0 actions
per fork remain unreachable.** The fix re-gates existing actions and emits none, so all site
counts held exactly — 15 Set Brightness / 15 Set Volume / 22 Get Device Details, coercion split
15-of-15 and 4-of-15, action totals 4304 Core and 4372 Aware, every one re-measured against the
rebuilt forks rather than carried forward.

**Three older claims a reader might otherwise trust at face value, corrected here rather than
edited away.** All three are retained below as the record of what was honestly believed:

1. **"Dimming and Silence writes now execute where they previously no-opped"** — the Phase
   9-era warning block further down this file. That coercion fix was necessary and it was
   **not sufficient**. The writes were correctly typed and still could not be reached, so they
   went on no-opping for three further phases.
2. **Phase 16's belief that the container gate was intentional input validation.** `dimming()`'s
   pre-11-08 docstring stated that both the condition-100 container gate and the numeric
   capture gate were "input validation over an absent or untrusted Get Device Details reading
   (T-16-03)", and Phase 16 therefore left the broken one alone on purpose. That is true of the
   inner gate and false of the outer one, which fires **before** Get Device Details runs and so
   validated no reading at all. Phase 16 did not introduce this defect and its own
   persistence fix is correct and untouched — but that fix was ordering *inside* a body that
   had never been reached.
3. **11-07's "the probe could not be installed"**, in the block immediately below. That was
   retracted the same day: the simulator import channel works, the probe's own missing
   normalisation pass was the real cause, and the consumption shape is now settled at rung 2.
   See `docs/BUILD-NOTES.md` §31 (rewritten).

**REACHABLE IS NOT PROVEN ON A DEVICE, and this build does not claim it is.** What is proven is
structural, and only structural: the writes are correctly coerced, they are persisted before
the device changes, and they are now reachable. The capture-and-restore loop those three
properties exist to serve **has still never executed on hardware**, Emergency Restore has still
never been tapped on a phone, and `16-UAT.md`'s twelve tests — which are exactly the
force-quit, restart, missed-CLOSE, overlapping-session and lock-screen failure modes this
change makes reachable — have never run. DIST-03 is open and Phase 16 owns that proof. This
plan changes *what that UAT will be testing* — a live loop instead of a dead one — and nothing
about its outcome.

---

**This table's six hash/size rows describe the PHASE 11 GAP-CLOSURE re-sign (2026-08-18, plan
11-07), superseding the phase 16 plan 16-06 re-sign whose header block follows immediately
below.** Per this file's own convention, that block is retained as its own rebuild's record
and is superseded by this one wherever the two conflict. **Everything else in this build is
unchanged from the Phase-16 re-sign it supersedes** — the capture-persistence fix, decision
D-01's zeroed brightness floor and dim target, and the retired-clause sweep all carry forward
untouched. This rebuild carries **one change**, in two places:

1. **The `text.match` output-name class fix (plan 11-07, closing `11-REVIEW.md` CR-02).**
   `is.workflow.actions.text.match` publishes its output as **`Matches`** — corpus-attested 15
   times across the 19 shipped golden XMLs, against **zero** occurrences of the label this
   engine had guessed. The engine guessed wrongly at two sites while `tools/build_sentient.py`
   already used the real name, so one artifact shipped **two contradictory names for one
   identifier**. The wrong name raises nothing: the reference simply does not resolve, the
   Panic Escape section reads **empty**, the condition-99 contains test over it is therefore
   **always false**, and a user who asked to remove their bypass was shown a confident
   *"Nothing was changed."* — the removal half of Phase 11's headline deliverable silently did
   nothing, for three phases, with no error anywhere. Both sites are corrected in one pass:
   `panic_escape_branch()`'s section read and `manual_note_refresh()`'s Sync My Profile
   proforma. `ACTION_OUTPUT_NAMES` now lists the identifier, which is what arms
   `verify_output_names()` to fail the build on any future site — while the identifier was
   absent, the guard that exists for exactly this defect class was blind to both sites. A
   negative control confirms the guard raises on a deliberate regression and was silent on the
   identical regression beforehand.
2. **The consumption shape at those two sites, adopted as a bounded fallback and NOT settled
   by observation.** `text.match` publishes a **list**, and no golden shortcut feeds that list
   to either `gettext` or `getitemfromlist` — so neither candidate shape is corpus-attested.
   A rung-2 probe was built and signed to answer it; it could not be installed, so **the
   question is recorded OPEN and no claim, device or simulator, is made**. The in-repo
   precedent from `audit_block()` is adopted instead: `getitemfromlist` with the literal enum
   case `First Item`, which is deterministic about which element is taken and cannot be worse
   than stringifying a one-element list. Recorded as a deviation in `docs/BUILD-NOTES.md` §31.
   **+2 actions per fork** (4302 → **4304** Core, 4370 → **4372** Aware).

**Nothing in this rebuild is device-verified.** DIST-03 remains open; the repaired removal path
has never run on a phone, and this build does not change that.

---

**This table's six hash/size rows describe the PHASE 16 re-sign (2026-08-18, plan 16-06),
not the phase 13 CODE-REVIEW re-sign, not the phase 13 plan 04 re-sign, not the phase 12 plan
05 refresh and not the phase 11 plan 06 rebuild.** Every paragraph below this one is retained
as its own rebuild's record and is superseded by this one wherever the two conflict. This
rebuild carries **three changes**, all of them in the capture-and-restore surface this phase
exists to make real:

1. **The capture-persistence fix (plan 16-01).** `dimming()` and `silence()` now write the
   captured original to `state.json` **before** Set Brightness / Set Volume runs. Until this
   build the capture was written into the `State` dictionary, which is never saved again after
   the OPEN arm's last save — so it never reached disk, and CLOSE and Emergency Restore both
   found the cleared sentinel, failed the `> 0` gate and skipped. **The screen dimmed and
   nothing in the product un-dimmed it.** A build guard, `verify_capture_persistence`, pins the
   ordering on both forks and a negative control proves it fires. +44 actions per fork.
2. **The brightness floor and the dim target both reach zero (decision D-01, plan 16-03).**
   `safety.brightness_floor` `0.10 → 0` and `safety.dim_target` `0.12 → 0`. The eleven-per-fork
   emitted `comment()` actions that asserted a lower bound on the brightness write — 22 shipped
   user-visible comment actions across the pair, asserting a bound this same build sets to zero
   — were replaced by a statement of the property the build actually guarantees. Measured
   11 → 0 per fork. `silence()`'s parallel SAFE-02 comment was deliberately **not** edited and
   is asserted still present 11× per fork. `docs/CAPABILITY-DECISIONS.md` BD-02's Supersession
   note is the authority; canonical strategy §21 is retained unmodified as the original design
   input.
3. **The two dead snapshot leaves are removed (decision D-02 / DEV-06, plan 16-04).**
   `settings_snapshot.<group>.changed_at` and `.changed_by_session_id` had 44 writes per fork
   and **zero** readers; both are gone from the writes, from the bootstrap seed and from the
   phase5 assertion, and `verify_no_removed_snapshot_leaf_reads` fails any future build that
   reads one. −88 actions per fork (each removed `set_value` also removes the `normalize_setters()`
   rebind). `settings_snapshot`, both group sub-dictionaries and both `original_value` leaves
   survive — only leaves were removed.

Net action delta across the phase: **+44 − 88 = −44** per fork, 4346 → **4302** (Core) and
4414 → **4370** (Aware), each confirmed on the **decrypted** payload rather than on `src/`.
Both forks were regenerated in one pass after the provenance ancestor check passed, and the
rebuild is byte-idempotent — a second consecutive build left `git status` empty, so these
digests are reproducible rather than run-specific. **Gate A** (`--target-macos 26
--target-platform all`) `Validation passed.` exit 0 on both forks before signing; **gate B**
(`--target-macos 27 --target-platform all`) read standalone and advisorily per fork, reporting
exactly the one permanent `WFCreateNoteInput` waiver each — at index **4148** (Core) and
**4216** (Aware) — and nothing else. All thirteen `docs/*.py` checkers exit 0 at this commit,
`manifest_check` included once this table was refreshed, and `docs/retired_clause_check.py` —
new in plan 16-05 — among them. The superseded previous rows, retained so a reader can identify
a build already on a device: **phase 13 CR-01** Core source/archive `2901248` bytes
`c6270691…`, Core signed `233802` bytes `b07497ba…`, Aware source/archive `2937929` bytes
`709f53f8…`, Aware signed `237842` bytes `212598cf…`.

**⚠ Nothing in this rebuild has run on a real iPhone.** The capture-and-restore loop is now
**structurally capable** of restoring and remains **behaviourally unproven** — see the closing
`⚠` bullet and
`.planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-UAT.md`, which is
pinned to the two signed digests in the table below.

**This table's six hash/size rows described the phase 13 CODE-REVIEW re-sign (2026-08-17,
CR-01) until the phase 16 re-sign above superseded them.** Plan 04's artifacts are superseded:
they wrapped 44 attachment-free literal
rows per fork in the variable-row wrapper, a shape no donor exhibits, and the CR-01 fix moved
those 44 rows to the bare `<string>` form both donors show. See the **Phase 13 code review**
paragraph and the closing `⚠` bullet below. Every earlier paragraph in this file is retained
as its own rebuild's record — each describes the table as it stood then, not as it stands now —
and each is superseded where it conflicts with a later paragraph. The previous rows, retained
so a reader can identify a build already on a device: plan-04 Core source/archive `2916560`
bytes `99388cad…`, Core signed `234830` bytes `fe1bafdf…`, Aware source/archive `2953241` bytes
`d01154b3…`, Aware signed `239184` bytes `bd1264d5…`; and before those, Core source/archive
`2831992` bytes `589ee121…`, Core signed `229959` bytes `4acc696a…`, Aware source/archive
`2868673` bytes `ff50b453…`, Aware signed `234012` bytes `447eead5…`.

Rebuilt 2026-08-17 by phase 11 plan 06: **the two variants ship under their new names.**
`Dumb` becomes **`Core`** and `Sentient` becomes **`Aware`**, at every site where the name is
load-bearing — the root `WFWorkflowName`, the bootstrap `"fork"` seed, the Control Room Note's
two Run Shortcut targets, the Note's settings-block fork label, `docs/manifest_check.py`'s
`DISPLAY_NAMES`, `README.md` and the two signed basenames below. **This is a breaking change
for anyone who imported an earlier build**, and it is stated as one in the Note, in
`README.md`, in `docs/BUILD-NOTES.md` §25 and in `docs/CAPABILITY-DECISIONS.md` BD-06-A4
rather than smoothed over. The same rebuild closes the defect this phase inherited by name:
the Aware fork's Note previously instructed its users to select the **other** fork's shortcut
in both automation steps and reported the other fork's label in its settings block. The
preceding rebuild was phase 11 plan 05 — Panic Escape became deliberately removable and
reversibly so, `panic_escape_enabled` became a first-class flat state field, and
`schema_version` moved 2 → 3 per BD-06-A3. **Emergency Restore remains untouched by any of
it.** Built with Shortcuts Playground
under the project's **two-gate rule** (stated in full in `.claude/CLAUDE.md` §1
`### Exact validator invocation`). These artifacts were built and validated under **gate A**,
`--target-macos 26 --target-platform all`, which passes clean on both forks. **Gate B**,
`--target-macos 27 --target-platform all`, was read against them advisorily and reported the
one recorded waiver (`WFCreateNoteInput`, device-donor ground truth) and nothing else —
measurements in `docs/BUILD-NOTES.md` §22.

Both forks were regenerated from the same generator run rather than either being carried
forward: `src/PROSOCHE-*.xml` are generated files, and Sentient is a fork *of the built Dumb
source*, so a Sentient carried across a Dumb change is a fork of a file that no longer
exists. Regenerating both in one pass is the only way the shipped pair provably matches
`tools/build_state_engine.py` at this commit.

| Fork | Source / archive / signed artifact | Bytes | SHA-256 |
|---|---|---:|---|
| Core source | `src/PROSOCHE-Dumb.xml` | 2864203 | `34c2ba05968b0e35c723892404c5f4d3a334d51c3f14263f7d6809997e668b02` |
| Core archive | `artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Core-132716.xml` | 2864203 | `34c2ba05968b0e35c723892404c5f4d3a334d51c3f14263f7d6809997e668b02` |
| Core signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` | 231148 | `873fa3dbda7b1f3440bfc76997c2962198ddec2052096833787547b52f129f10` |
| Aware source | `src/PROSOCHE-Sentient.xml` | 2900884 | `e2c94746e5acf49b82d4f3ba7f89768122c2d3c409b574b27cb8e415c523dcda` |
| Aware archive | `artifacts/shortcuts/2026-08-18/PROSOCHĒ — Nine Circles — Aware-132729.xml` | 2900884 | `e2c94746e5acf49b82d4f3ba7f89768122c2d3c409b574b27cb8e415c523dcda` |
| Aware signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` | 235592 | `4d985aefa04c1cf99405bd01189d7d6e2d30fa4c3b98d94a9bd0855e66f276f1` |

**Re-archived and re-signed by the phase 13 CODE REVIEW, finding CR-01 (2026-08-17).** This is
the record for the six rows in the table above; the plan-04 paragraph immediately below is its
own re-sign's record and is **SUPERSEDED** by this one wherever the two conflict. Plan 04's
`_list_row()` discriminated on Python type (`isinstance(item, str)`), so every non-`str` got the
`{WFItemType, WFValue}` wrapper — including two Mirror templates that carry no `￼` placeholder
and therefore have an **empty** `attachmentsByRange`. Those are literal rows by content, and
Donors 4 and 4.1 write a literal row as a bare `<string>`. 44 rows per fork shipped in a shape
**no donor exhibits**, all of them at row position 8 — the row `getitemfromlist` selects at
**Circle VIII** on both the success and the lapse family, so a device mishandling would have
looked exactly like the blank Mirror this phase set out to fix. `_list_row()` now discriminates
on attachment-bearing-ness, `verify_list_item_wrappers()` asserts the inverse rule, and the
whole ship chain was redone: provenance ancestor check exit 0, both generators re-run, **gate A**
`Validation passed.` exit 0 on both forks, **gate B** read standalone and advisorily per fork
(exit 1, exactly the one permanent `WFCreateNoteInput` waiver each and nothing else), both forks
re-archived and re-signed under the canonical names with no suffix, and all six rows above
recomputed from disk in one pass. Both signed containers were then **decrypted** through the
AEA1 recipe and measured on the recovered plists: 67 `is.workflow.actions.list` actions, 666
rows, **616** wrapped as `{WFItemType: 0, WFValue: …}`, **50** bare-string rows, **0** dict rows
missing `WFItemType` and **0** wrapped rows carrying an empty `attachmentsByRange`, per fork.
Per-action row counts are unchanged at `[6] + [10]*66`, so no row was added, dropped or
reordered. All twelve `docs/*.py` checkers exit 0. Full record in `docs/BUILD-NOTES.md` §28.

**Re-archived and re-signed by phase 13 plan 04 (2026-08-17). SUPERSEDED by the code-review
re-sign above — every figure in this paragraph describes the plan-04 artifacts, which the table
above no longer names.** All six rows *of that build* were
recomputed from disk in one pass — both sources, both new dated archives and both signed
artifacts — rather than only the rows believed to have moved, because Phase 10 measured three
of six wrong at once. `src/*.xml` were regenerated from `tools/build_state_engine.py` and
`tools/build_sentient.py` after the provenance ancestor check passed, and the rebuild was
**byte-idempotent**: a rebuild on an already-built tree left `git status` empty, so the digests
above are reproducible rather than run-specific. Both forks passed **gate A**
(`--target-macos 26 --target-platform all`, `Validation passed.`, exit 0) before signing, and
**gate B** (`--target-macos 27 --target-platform all`) was read **standalone and advisorily**
per fork, reporting exactly the one permanent `WFCreateNoteInput` waiver each and nothing else
— the run most likely to surface a regression, since this phase moved 660 row serializations.
Both signed containers were then **decrypted** through the AEA1 recipe and measured: 67
`is.workflow.actions.list` actions, **660** rows wrapped as `{WFItemType: 0, WFValue: …}`,
**6** bare-string rows (the exit names, deliberately unwrapped) and **0** dict rows missing
`WFItemType`, per fork. That is what actually shipped, not what the source claims. Full record
in `docs/BUILD-NOTES.md` §28. The paragraph immediately below is the phase 12 WR-01 re-sign's
own record and is **SUPERSEDED** by this one where the two conflict.

**Re-archived and re-signed against the corrected source (2026-08-17, same session as WR-01).**
`seed_active_session()`'s double-indent bug (WR-01, commit `5f55edc`) shortened the `active_session`
bootstrap line by 2 bytes per fork; that fix landed in `src/*.xml` first, and the archive/signed rows
above were then refreshed to match — every row in this table, including the two `.shortcut` files, is
now byte-identical in provenance to the same corrected `src/*.xml` this table's source rows describe.
The archive rows are therefore byte-identical to their `src/` counterparts (size and hash match
exactly), consistent with the "byte-identical" claim below. `docs/manifest_check.py` passes.

**The two old-named signed artifacts were DELETED, not retained**, per
`docs/CAPABILITY-DECISIONS.md` BD-06-A3 Decision 2. `artifacts/shortcuts/` now holds exactly
two signed files, and their basenames are exactly the two canonical display names.
`docs/manifest_check.py` cannot see an orphaned file — it asserts only the rows this table
gives it — so retention would have been an unchecked state, and four signed files with no way
to tell which two are current is precisely the confusion the signed-name discipline exists to
prevent. Nothing unrecoverable was discarded: both deleted files were git-tracked, so
`git show` recovers their exact bytes. The **source filenames are deliberately unchanged** and
still read `PROSOCHE-Dumb.xml` / `PROSOCHE-Sentient.xml`; renaming them is churn across ten
code files and some seventy planning documents and would break every historical plan's
reproducibility, and the addendum renames the products, not the sources
(`docs/BUILD-NOTES.md` §25).

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. **This rebuild is a copy and identity change, not a structural one**: both
sources grew by roughly 0.4 KB, entirely the renamed strings and the Note's new rename
notice. No control flow moved, no action was added or removed, and the environmental
site-count tables are unchanged from the preceding rebuild at their measured values — 15 Set
Brightness, 15 Set Volume, 22 Get Device Details, with 15 of 15 brightness sites coerced and
4 of 15 volume sites coerced. All twelve static checks passed at this commit,
`manifest_check` included once this table was refreshed. **This paragraph describes the phase
11 plan 06 rebuild only** — see the **Phase 12** paragraph immediately below for the structural
changes phase 12 subsequently made to the artifact this table's rows now describe.

**Phase 12 — state-shape sentinel gaps: `exit_events`, `active_session`, `create_target_url`
(plans 12-01 through 12-05, 2026-08-17).** Both of the claims in the paragraph above are now
**false** for the artifact this table describes: this was a structural rebuild, not a copy-only
one, and `schema_version` moved **3 → 4**, not 2 → 3 (the 2→3 bump was phase 11 plan 05's, a
rebuild earlier than the one the paragraph above narrates). Phase 12 closed three state-shape
sentinel gaps in `tools/build_state_engine.py`: seeded `exit_events` (an array) and
`exit_selection_counter` (a flat counter) into the bootstrap template where neither previously
existed; converted `active_session` from a bare `null` into a permanent four-leaf sentinel
container (`id`, `started_at`, `declared_duration_seconds`, `intention`), removing a class of
dotted-read hard-error that could stall `restore_managed_settings("Reloaded State")` mid-close
and strand the user dimmed or silenced; and seeded `profile_snapshot.create_target_url`,
closing the single most likely first-exit crash surface this phase found (`T-12-18`) — choosing
Create on a clean install previously hard-errored on an unseeded dotted read. Roughly a dozen
condition-100 (has-any-value) gates converted to condition-5 (string-is-not) gates across
`persist_contract()`, `record_exit_and_route()`, `close_pipeline()`, and `route_exit()`'s Create
branch, consistent with the sentinel-seeded invariant these three fields now guarantee; see
`docs/BUILD-NOTES.md` §26-27 for the full decision record, including the option-A/B/C
comparison for `create_target_url`'s seed shape and the assumptions this phase carried without
a fresh device measurement (A1, A2, A5). **Structurally proven, device-unobserved**: all three
changes are proven present and correctly gated in the generator, in both `src/*.xml` artifacts,
and (per §27, re-verified after the WR-01 re-sign above) in the decrypted signed payloads of the
current `.shortcut` files; none of it has run on a real iPhone — `12-UAT.md` recorded **BLOCKED**
(`xcrun devicectl list devices` reported no devices, so no criterion in that file was exercised).
Read `docs/BUILD-NOTES.md` §26-27 and `12-UAT.md` before treating any of this phase's behaviour
as device-confirmed.

**Phase 13 — the `WFItems` row wrapper (plans 13-01 through 13-04, 2026-08-17).** Every
`is.workflow.actions.list` row this generator emitted was a bare `WFTextTokenString` dict with
no row framing around it. Donors 4 and 4.1 — device-authored `WFItems` arrays — show that a
non-literal row must be wrapped as `{WFItemType: 0, WFValue: <the token string>}`, and that a
plain literal row is a bare string. An unwrapped row is not a wrong *envelope*; it is a missing
*container*, which is why a type-scoped sweep for a wrong string envelope was structurally
blind to it for three cycles and why it is recorded as its own defect axis (**8**) in
`.claude/CLAUDE.md` rather than filed under axis 2. **66** call sites were fixed. Of the 666
rows, the **616** that are attachment-bearing are wrapped and the **50** that are not —
the six exit names, plus the two placeholder-free Mirror templates at 22 call sites each —
stay bare `<string>` literals, and Donors 4 and 4.1 show exactly that mix in a single
device-authored array. **The interim "660 wrapped + 6 bare" figure carried by plans 13-01
through 13-04 described 44 rows per fork as "variable-bearing" when their
`attachmentsByRange` was empty; it is corrected here and in `docs/BUILD-NOTES.md` §28 and
BD-08, and the artifact itself was corrected by CR-01.** A new build guard,
`verify_list_item_wrappers()`, raises before any write in both builders. The visible symptom
this predicts is a **Mirror alert whose body is empty** — the phase exists so that a blank
Circle in Phase 19 device testing is a real finding rather than a known artifact. The
**conditional operand** family was the other half of the phase's hypothesis and was
**REFUTED**: Donor 5 shows the `TEXT`-slot comparison target is already correct at every site,
so this phase deliberately changed **nothing** there and pinned the correct shape with a
positive assertion instead. See `docs/BUILD-NOTES.md` §28 and
`docs/CAPABILITY-DECISIONS.md` BD-07 / BD-08. **Structurally proven, device-unobserved**: the
wrapping is proven in the generator, in both `src/*.xml` and in both decrypted signed payloads;
none of it has run on a real iPhone. `xcrun devicectl list devices` reported `No devices
found.` on 2026-08-17, so `13-UAT.md` is recorded **BLOCKED** with every outcome left blank —
the same posture Phases 10 and 12 recorded, and DIST-03 stays open.

**A signed artifact's filename is the only carrier of its display name — re-measured on this
build.** Both containers were decrypted and neither recovered `Shortcut.wflow` contains a
`WFWorkflowName` key at all, even though both `src/*.xml` files set it: the signer strips it.
That is why the rename had to reach the filename, why no suffix of any kind is permitted, and
why the rename is a breaking change nothing on the device can repair — the user's two Personal
Automations reference the library entry by that name and no API can re-point them.

**The Aware fork now names itself.** Until this rebuild, `tools/build_sentient.py` made no
content change at all to the forked source, so the Aware fork shipped the Core fork's Note
verbatim — instructing every Aware user to select a shortcut they do not have, in both
automation steps, and reporting `- Fork: Dumb` in its settings block. A new
`fix_fork_strings()` applies the divergence through the offset-recomputing round trip with an
expected occurrence count per site, and fails the build naming the dead-install consequence if
any count is wrong. Because that is the first deliberate divergence between the forks,
`docs/sentient_core_check.py`'s whole-list equality became false by design; it was **not**
deleted but replaced by a fork-normalised equality with bounded per-site counts, paired with a
positive assertion that the Aware Note names Aware at least twice and Core exactly zero times.
Both halves are asserted on the decrypted payloads, not only on `src/`.

**Panic Escape is removable, and Emergency Restore is provably not the same thing.** Panic
Escape is the `Leaving` case of the menu PROSOCHĒ shows before an intervention — the easy
behavioural bypass. Some people find the option to leave is itself the thing they reach for
automatically, so it can now be given up. Emergency Restore is a *safety mechanism*: it is
what puts back a screen a run left dim or a media volume a run left down. The two are kept
apart at every level, and that separation is the whole safety argument of this build:
`panic_escape_enabled` does not represent Emergency Restore, no conditional introduced here
encloses it, and it remains both a manual menu item and one of the two options inside the
cool-down redirect. Re-measured on the **decrypted payloads**, not on `src/`: two menus offer
Emergency Restore and two case bodies implement it in each fork, and **none of the four is
enclosed by any Panic Escape conditional**. The literal string `Emergency Restore` appears 14
times in each recovered plist, up from 7 at the phase baseline — the new copy names it as
unaffected in the Note section, in both confirmation prompts and in both ledger lines.

**Removal takes two deliberate acts, and it is reversible by the same route.** The Note gained
a stable `## PANIC ESCAPE` section immediately before `## MY PHONE, ON PURPOSE` — a region the
manual refresh never appends to, so the setting cannot be buried under machine-appended
`## CURRENT SETTINGS` duplicates. It carries one editable line. Changing that line alone does
nothing; choosing the menu item alone does nothing. Only the two together, with an explicit
confirmation, write the flag. Putting the word back and choosing the same item restores the
bypass, with its own confirmation. A Note with no readable section, or a reworded one, can
only ever restore — never remove.

**The gate is numeric, and the field is flat.** `panic_escape_enabled` is seeded flat at the
top level of the bootstrap template and gated with a `> 0` test, never a `has any value` test.
Both choices are forced by this runtime's verified semantics: a **dotted** read whose final
segment is absent is a hard error, so a nested field could not be gated at all on a
`state.json` written before it existed, while an existence test reads TRUE for the string
`"null"` and for `""` — precisely the states that must read as removed. A new build guard,
`verify_panic_escape_seed()`, asserts the seed, forbids a dotted read of the flag and forbids
a non-numeric gate on it. It exists because `verify_state_seed()` was measured to be scoped to
the `settings_snapshot` subtree and would not have covered this field.

**`schema_version` moved 2 → 3, across three coupled literals.** Without it the new bootstrap
field never reaches a device that already holds a valid `state.json`, and the removal path
would be dead there. BD-06-A3 records the decision and the cost accepted: there is no
field-preserving migration, so a device that rebuilds discards accumulated heat, gravity,
pressure, the rolling windows, the session record and the exit-learning samples. BD-06-A1
Amendment 3 records that PROSOCHĒ is undeployed and old `state.json` files are explicitly not
a consideration, which is what makes that free here — **the gate reinstates itself if a real
installed base ever exists.** The three literals are the template seed, the runtime validity
gate, and the *recognition tuple* the transformer uses to locate that gate; the third is the
one plan 11-04 measured and neither the plan nor the research had recorded. Omitting it fails
the **next** build, not this one, with an error pointing at a missing conditional rather than
at the bump. All three now derive from named constants so they cannot drift apart again.

**The Apple Note's identity moved, and all three sites moved together.** PROSOCHĒ finds its
Note by NAME, and three separate strings decide that name: the `is.workflow.actions.filter.notes`
lookup predicate, the H1 heading a person reads at the top of the body, and the
`com.apple.mobilenotes.SharingExtension` `name` parameter that actually titles it. If the
predicate and the title ever disagree, PROSOCHĒ creates a Note it can never find again and
appends the ledger to a fresh one on every state-changing run — silently, with no error on
device or in any check. All three now read `PROSOCHĒ`, asserted against one constant by
`docs/note_identity_check.py`. The **internal** name is unchanged: the `Open Control Room`
menu item, the `Control Room Note` variable, the structural comment markers and the
`gate_control_room_shownote()` / `fix_shownote_key()` / `fix_notes_filter_limit()` function
names all still say Control Room, per commit `e84ee77`.

**The lookup operator was deliberately NOT tightened.** Shortening the title widens what the
`contains` predicate can match — a leftover Note from an earlier install now matches too, and
with a limit of 1 plus First Item PROSOCHĒ would bind to it permanently. The operator stayed
at 99 because it is BOOT-08's recorded decision and because `Operator: 4` is UNVERIFIED for a
`WFContentPredicateTableTemplate` on the Notes `Name` property. Mitigated in copy instead —
the Note's `## READ THIS FIRST` tells the user to delete or rename an old-titled Note — and
recorded in full, with the donor export that would settle it, as `docs/CAPABILITY-DECISIONS.md`
BD-06-A2. `docs/note_identity_check.py` pins the operator so any future move is deliberate.

**Dante's nine Circle names are surfaced for the first time.** Eight of the nine were measured
absent from the artifact entirely, so this adds a name surface rather than renaming one. They
live in one generator constant, `CIRCLE_NAMES`, from which the Test-a-Circle submenu builds
**both** its `WFMenuItems` array and every case's `WFMenuItemTitle` — so the two are identical
element-for-element and in order *by construction*, not by review. A `choosefrommenu` whose
case titles drift from its items is the top documented real-world failure mode for that
action. The names are **positional** per BD-06 Decision 1: they label the depth, not the
intervention, and which intervention fires at a depth is still the `sequences` arrays' decision.

**The middle profile is `Purgatory`.** BD-06-A1 renamed it from `Limbo`, which BD-06 had just
made Circle 1's name — one word naming both a depth and a pace. The three profiles are now the
three canticles: Paradise / Purgatory / Inferno. The rename had to be total rather than
partial, because a profile name is a live dotted Config key path (`thresholds.<profile>`) and a
dotted read with a missing segment is a **hard error** in this runtime — a half-done rename
would be a crash, not a degradation. Verified per fork on the shipped payload: `Limbo` survives
on exactly **three** sites in each, and every one is a `Circle 1 · Limbo` label. No migration,
dual-key alias or read-time normalisation was built; BD-06-A1 records that PROSOCHĒ is
undeployed and old `state.json` files are explicitly not a consideration.

Both signed containers were decrypted via the AEA1 recipe and asserted against this wave:
`plutil -lint OK` on both recovered plists; `## PANIC ESCAPE` present 5 times and
`panic_escape_enabled` 7 times in each; `"schema_version": 3` present in each bootstrap
template; **exactly one** `["Leaving","Continue"]` menu per fork; two Emergency Restore menus
and two case bodies per fork, none of them enclosed by a Panic Escape conditional; and the
environmental site counts reading 15 / 15 / 22. The global attachment invariant was
re-measured on the recovered payloads rather than only on `src/`: **1,205**
`WFTextTokenString` values in Dumb and **1,209** in Sentient (up from 1,105 / 1,109, the new
branch's own token strings), every one with `attachmentsByRange` keys equal to its own
`U+FFFC` offsets, zero mismatches — the invariant that matters most, since the Note body edit
inserted 1,157 characters upstream of both of that body's attachments, which moved from
offsets 6982 / 7013 to 8139 / 8170. This is structural evidence only.

The two checker promotions from the preceding rebuild are unchanged and still in force.
`docs/sequence_dispatch_check.py` exits non-zero on any orphaned sequence entry, unreachable
dispatch branch, branch of unknown matching semantics, or entry matched by more than one
distinct branch name, with an empty `KNOWN_ORPHANS`; `tools/build_state_engine.py`'s
`verify_dispatch_coverage()` enforces the same invariant in both builders before any write.

**Do not rename these files.** A signed `.shortcut` carries no display name inside it:
measured this phase, the AEA1 auth-data plist holds only `SigningCertificateChain`, and the
signer strips `WFWorkflowName` from the recovered `Shortcut.wflow` even though both
`src/*.xml` files set it. The display name lives in the filename and nowhere else, so any
suffix produces a second, differently named library entry that the user's two Personal
Automations do not reference. `docs/manifest_check.py` asserts both rows against that rule
and recomputes every size and hash above from the files themselves.

> **⚠ These artifacts carry the Phase 9 dimming/silence coercion fix, which is UNTESTED on
> device.** Dimming and Silence writes now execute where they previously no-opped, making
> `restore_managed_settings()` load-bearing on a path with zero device evidence. Read
> `docs/BUILD-NOTES.md` §18 before distributing or relying on these builds, and run
> `.planning/phases/09-reintroduce-and-validate-dimming-silence-stateful-restore-on/09-UAT.md`
> when a device is available.
>
> **⚠ This build additionally carries four Phase 10 behaviours that have likewise never run
> on a real iPhone:** Circle 0, the silent band, in which a low-Pressure open records state
> and shows nothing at all; the removal of the unconditional OPEN notification (the CLOSE
> confirmation survives); the Control Room Note now opening only when `Open Control Room`
> was chosen rather than after every manual menu choice; and a tenth manual menu item,
> `Setup Check`. Every one of these is proven structurally and none is proven behaviourally.
> Read `docs/BUILD-NOTES.md` §19, and run
> `.planning/phases/10-ship-readiness-remainder-and-ux-lite-pass/10-UAT.md` when a device is
> available.
>
> **⚠ This build additionally carries repaired iOS 26 automation onboarding copy that has
> never been followed on a real iPhone.** The Control Room Note's Automation A and B steps
> now describe the `Create New Shortcut` wrapper — a `Text` action holding the literal, then
> `Run Shortcut` with its Input bound to that Text. The **handoff mechanism** is device-proven
> (the INPUT PROBE run of the `open-routing-sequence-error` session reported `RAW [OPEN]`),
> but **these specific rendered steps are not**: no one has yet followed them end to end and
> arrived at a working automation. Read `docs/BUILD-NOTES.md` §20, and confirm the flow during
> the outstanding device UAT.
>
> **⚠ This build additionally carries BD-06's entire renamed primitive roster and a changed
> dispatch comparator, none of which has ever run on a real iPhone.** All nine shipped names
> are proven present in the generator tuple, in all three `sequences` arrays, on all 99
> emitted dispatch branches (9 shipped names × 11 primitive-dispatch renderings = 99, measured
> fresh against this rebuild and equal across both forks; `docs/BUILD-NOTES.md` §24.3 carries
> the rendering-count derivation, and `docs/sequence_dispatch_check.py` reports the same 99
> on every run) and in the decrypted payload of both signed containers, and every
> one of those branches is proven to carry condition code 4 — all of it file-level structural
> proof. That any Circle actually reaches its renamed branch under exact matching on device is
> **not** proven and is not claimed. Read `docs/BUILD-NOTES.md` §21.
>
> **⚠ Two states in this build are deliberately INTERIM, not designed behaviour.** Circle 8
> (`Loud Mirror`) dispatches `mirror_and_voice()` — the same implementation as Circle 7's
> `Mirror` — so that the entry reaches a real branch and the dispatch-coverage guard can be a
> hard gate; **Phase 15** replaces it with the designed Voice primitive. Circle 6 holds
> `Eject` in all three sequences, where BD-06 gives `Classic` and `Ambient` to `Redirect`;
> `Redirect` has no implementation until **Phase 17**, and naming it now would be an entry
> that dispatches nothing. Neither is a finished decision.
>
> **⚠ This build additionally carries a renamed Apple Note, a renamed descent profile and a
> new Circle-name surface, none of which has ever been seen on a real iPhone.** The Note is
> now titled `PROSOCHĒ` at all three identity sites, and the lookup that finds it is still a
> `contains` match — so a Note left over from an earlier install **will** match the new
> predicate, which is why the Note's own `## READ THIS FIRST` now asks the user to delete or
> rename it. Whether the lookup binds to the intended Note on a device holding both is
> **structurally reasoned, not observed**; the operator decision and the donor export that
> would settle it are recorded as `docs/CAPABILITY-DECISIONS.md` BD-06-A2. The middle profile
> is now `Purgatory`, which changes live Config key paths (`thresholds.Purgatory`,
> `cooldown_seconds.Purgatory`); a device still holding `profile: "Limbo"` would hard-error on
> its next OPEN. BD-06-A1 accepts that consequence explicitly on the grounds that PROSOCHĒ is
> undeployed and the only installs are the owner's own testing — **if that is not true of your
> device, re-run the setup rather than this build.** Read `docs/BUILD-NOTES.md` §23.
>
> **⚠ This build additionally carries a removable Panic Escape and a `schema_version` bump,
> neither of which has ever run on a real iPhone.** The flag, the gate, the Note section, the
> eleventh menu item and both confirmation directions are proven present in the generator, in
> both `src/` artifacts and in the decrypted payload of both signed containers — file-level
> structural proof, and nothing more. That a user editing the setting line and confirming
> actually removes the bypass, that the restore direction actually restores it, that the
> bounded `text.match` binds to the intended section on a Note carrying appended
> `## CURRENT SETTINGS` blocks, and that the numeric gate resolves as intended against a
> Text-coerced operand are all **unobserved**. So is the bump's central claim: that a device
> holding `"schema_version": "2"` takes the rebuild branch on its next run. **Installing this
> build over an existing one discards that device's accumulated behavioural state** — heat,
> gravity, pressure, the rolling windows, the session record and the exit-learning samples.
> BD-06-A3 accepts that on the recorded grounds that PROSOCHĒ is undeployed; if that is not
> true of your device, read BD-06-A3 before importing. Read `docs/BUILD-NOTES.md` §24.
>
> **⚠ This build is named differently from every build before it, and the rename has never
> been exercised on a real iPhone.** `Dumb` is now `Core` and `Sentient` is now `Aware`.
> **If you already imported an earlier build, importing this one does not replace it** — the
> old entry stays in your library under its old name, and both of your Personal Automations
> keep pointing at it. There is no mechanism, in this Shortcut or in iOS, that can re-point
> them: open each automation, tap its Run Shortcut action and select the new name by hand,
> then delete the old shortcut. That the renamed Note's automation steps lead to a working
> automation is **structurally proven and behaviourally unobserved** — the strings are proven
> present in both decrypted payloads and nothing more. Read `docs/BUILD-NOTES.md` §25 and
> `docs/CAPABILITY-DECISIONS.md` BD-06-A4.
>
> **⚠ This build additionally carries three phase 12 state-shape sentinel fixes, none of which
> has ever run on a real iPhone.** `exit_events`/`exit_selection_counter` and a four-leaf
> `active_session` container are now seeded in the bootstrap `state.json` template where
> neither previously existed, and `profile_snapshot.create_target_url` is seeded with the
> project's `CLEARED_SENTINEL` so a clean-install Create exit no longer hard-errors on an
> unseeded dotted read. `schema_version` moved **3 → 4**. All three are proven present, in the
> right shape, and correctly gated (roughly a dozen condition-100 gates converted to
> condition-5 across `persist_contract()`, `record_exit_and_route()`, `close_pipeline()` and
> `route_exit()`'s Create branch) in the generator, in both `src/*.xml` artifacts, and in the
> decrypted payload of both signed containers at commit `ea7a0f4` — file-level structural proof
> and nothing more. `12-UAT.md` recorded **BLOCKED**: no device was available, so none of this
> is device-confirmed. As with the phase 11 plan 05 bump, installing this build over an
> existing one discards that device's accumulated behavioural state. Read
> `docs/BUILD-NOTES.md` §26-27 before distributing or relying on these builds.
>
> **⚠ This build additionally carries phase 13's `WFItems` row wrapper across 616 rows, which
> has never run on a real iPhone — and it is the build you must re-import to get it.** Every
> **attachment-bearing** List row is now framed as `{WFItemType: 0, WFValue: …}` per Donors 4
> and 4.1; the **50** attachment-free rows — the six exit names and the two Mirror templates
> that carry no `￼` placeholder, at 22 call sites each — stay bare `<string>` literals, which
> is the other half of the same donor-observed two-kind rule. Proven present in the generator,
> in both `src/*.xml` and in the **decrypted payload** of both signed containers (67 List
> actions, 666 rows: 616 wrapped, 50 bare, 0 unwrapped, 0 wrapped-but-attachment-free, per
> fork) — file-level structural proof and nothing more.
> **If you are still running any earlier signed build, you keep the blank-row Mirror until you
> re-import this one**, and testing a stale install would observe the old defect and
> misattribute it to a fix that did land. Two things remain device-only and unobserved: that a
> Mirror renders **non-empty** text over a wrapped List, and that `getitemfromlist`'s Item At
> Index extraction returns the **intended** row rather than merely some non-empty one — a
> non-empty but wrong row would pass a non-emptiness-only test. The conditional operand family
> was **REFUTED and deliberately unchanged**, so any red operator chip observed on this build is
> a **new** finding with a live artifact to inspect. Read `docs/BUILD-NOTES.md` §28 and run
> `.planning/phases/13-red-operator-conditionals-and-the-wfitems-list-wrapper/13-UAT.md` when a
> device is available.
>
> **⚠ This build additionally carries the PHASE 16 capture-persistence fix, a brightness floor
> and dim target of zero, and the removal of two dead snapshot leaves — none of which has ever
> run on a real iPhone, and it is the build you must re-import to get any of it.** The three
> changes are enumerated in full in this file's leading paragraph. Two things about this
> particular build deserve to be read before it is imported:
>
> **First, the defect it fixes is live on any device holding an earlier post-coercion-fix
> build.** Since the phase 9 coercion fix merged, Dimming and Silence actually change the
> device where they previously no-opped — but until this build the captured original never
> reached disk, so **nothing in the product could put it back**. A phone that ran an earlier
> build and reached Dimming or Silence is dim or quiet **right now** with no capture on disk,
> and Emergency Restore cannot help it: it reads the same file and finds the same cleared
> sentinel. That phone must be restored by hand in iOS Settings. This is stated as a hazard,
> not as history.
>
> **Second, `safety.dim_target` is now `0`.** Dimming reaches the device's true minimum. The
> user's on-device report is that iOS renders that dim rather than black, and decision D-01
> accepts it on that basis — but **that report is unrepeated and this build has not tested
> it**. The safety property was never the floor; it is capture-and-restore reliability, which
> plan 16-01 made structurally real and which no run of this build has yet exercised on
> hardware. Everything in this phase is **structurally proven and behaviourally unproven.**
> Read `docs/BUILD-NOTES.md` §17 and §30, `docs/CAPABILITY-DECISIONS.md` BD-02, and run
> `.planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/16-UAT.md` — which
> is pinned to this table's two signed digests — when a device session can be arranged.
>
> **DIST-03 — device verification — remains OPEN, and its REASON was re-measured 2026-08-18.**
> ~~`xcrun devicectl list devices` reports no devices~~ — that wording described an earlier
> session and is **false as of this rebuild**; it is struck rather than deleted so the
> correction has something to point at. Measured at this commit: a **paired** iPhone 15 Pro
> (`iPhone16,1`) on **iOS 26.6**, `pairingState: paired`, **`tunnelState: unavailable`**,
> `transportType: none`. The `State` column reads `unavailable`. So a device is known but there
> is **no live tunnel and no active transport — no session to drive**, which is a different
> fact from "no device exists" and is recorded as the different fact it is. Personal
> Automations are user-created on the device regardless, so DIST-03 would gate this work even
> with a live tunnel. No criterion in any UAT file has been exercised. **Nothing in this
> manifest should be read as device evidence.**
