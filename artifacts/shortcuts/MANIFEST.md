# Shortcut Distribution Manifest

Rebuilt 2026-08-17 by phase 11 plan 05: Build Addendum 01 §3 — **Panic Escape becomes
deliberately removable, and reversibly so**. `panic_escape_enabled` is now a first-class flat
state field; the `Leaving`/`Continue` menu is gated on it; a new eleventh manual menu item
reads a hand-editable setting line out of the Note, confirms explicitly in either direction,
and writes the flag. `schema_version` moves 2 → 3 per `docs/CAPABILITY-DECISIONS.md`
BD-06-A3, so the new bootstrap field actually reaches a device that already holds a
`state.json`. **Emergency Restore is untouched and is not gated by any of this** — the
separation is asserted structurally and re-asserted on both decrypted payloads. The preceding
rebuild was phase 11 plan 03: the Apple Note's title became the bare product name `PROSOCHĒ`
at all three identity sites, Dante's nine Circle names were surfaced from one generator
constant, and the middle descent profile was renamed `Limbo` → `Purgatory` per BD-06-A1.
Built with Shortcuts Playground
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
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,886,825 | `7ddd94b7e10099d524806d1fa6d9dd79f6d20630480974521af1b3add3ceb885` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-120124.xml` | 2,886,825 | `7ddd94b7e10099d524806d1fa6d9dd79f6d20630480974521af1b3add3ceb885` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 233,976 | `0768fc72fd7b3e41c44e336404aec036beea521b8a16a28206613813221b85b2` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,923,505 | `c04f73647f86a2c4bb262fe2e36623dbc7d35ab53e4082930221d3d66bdd948d` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-120136.xml` | 2,923,505 | `c04f73647f86a2c4bb262fe2e36623dbc7d35ab53e4082930221d3d66bdd948d` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 238,171 | `5dfed49d8e9b50285de36934677b7a0f9645b9a45443ddce378bbd4cfaaa3236` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both sources grew by roughly 213 KB against the preceding rebuild, and
unlike the last two rebuilds this one is **structural, not a copy change**: gating the
Leaving/Continue menu means `primitive_dispatch()` is now rendered **eleven** times rather
than ten — the otherwise arm renders it directly so a user who removed the bypass reaches the
Circle's intervention with no menu — and one rendering is roughly 200 actions. The two
environmental site-count tables moved with it, to **measured** values: 15 Set Brightness, 15
Set Volume, 22 Get Device Details, with 15 of 15 brightness sites coerced and 4 of 15 volume
sites coerced. That last number is the one worth reading twice: it did **not** move, because
`Silence Target` is `number()`-sourced and therefore already Number-typed, so all eleven of
its sites are deliberately left uncoerced. Research projected 5; the artifact measures 4, and
the measurement is what the tables carry. All twelve static checks passed at this commit,
`manifest_check` included once this table was refreshed.

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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
