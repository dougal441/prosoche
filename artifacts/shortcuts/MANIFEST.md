# Shortcut Distribution Manifest

**This table's six hash/size rows describe the phase 12 plan 05 refresh (commit `ea7a0f4`,
2026-08-17), not the phase 11 plan 06 rebuild.** That refresh re-signed both forks under their
live display names after phase 12's state-shape work landed; see the **Phase 12** paragraph
and closing `⚠` bullet below for what that work actually changed in the signed artifact. The
paragraph immediately below is retained as the phase 11 plan 06 rebuild's own record — it
describes the rename, not the current table — and is superseded where it conflicts with the
Phase 12 paragraph that follows it.

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
| Core source | `src/PROSOCHE-Dumb.xml` | 2831992 | `589ee1211bc66071d25fed4834ca3041df71d400874909e6c428a422ee891190` |
| Core archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Core-164519.xml` | 2831992 | `589ee1211bc66071d25fed4834ca3041df71d400874909e6c428a422ee891190` |
| Core signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Core.shortcut` | 229959 | `4acc696af87eb66ad4fffe9fb265ff58311b8a79dc6a0d1f9724c5ded83406fc` |
| Aware source | `src/PROSOCHE-Sentient.xml` | 2868673 | `ff50b4532df0867790444fbebc2e6be02598347859a0ff8bfcfd26ff03c741ec` |
| Aware archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Aware-164529.xml` | 2868673 | `ff50b4532df0867790444fbebc2e6be02598347859a0ff8bfcfd26ff03c741ec` |
| Aware signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Aware.shortcut` | 234012 | `447eead5020ab78292ec56275e6f5ae1f1b3f8e307ebc002f9e6a11f9246e9cd` |

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
> are proven present in the generator tuple, in all three `sequences` arrays, on all ninety
> emitted dispatch branches and in the decrypted payload of both signed containers, and every
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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
