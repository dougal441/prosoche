# Shortcut Distribution Manifest

Rebuilt 2026-08-17 by phase 11 plan 03: the **user-facing** half of Build Addendum 01. The
Apple Note's title is now the bare product name `PROSOCHĒ` at all three sites that decide its
identity; Dante's nine Circle names are surfaced for the first time, from one generator
constant; the Note gained a nine-Circle legend and an optional-hardening section; and the
middle descent profile was renamed `Limbo` → `Purgatory` per BD-06-A1, so that `Limbo` names
exactly one thing — Circle 1's depth. The preceding rebuild was phase 11 plan 02, which
applied BD-06 Decision 4's whole slot table in one commit — nine shipped primitive names live
in all three `sequences` arrays, ninety `Selected Primitive` conditionals moved from condition
99 ("contains") to condition 4 ("string is"), and `Loud Mirror` given a real dispatch branch
so Circle 8 is no longer dead. Built with Shortcuts Playground
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
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,669,198 | `1e5bf2bd288b4306b0fb7aa3a430b3eefd2f329f429980f56941a4fe095ad789` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-112947.xml` | 2,669,198 | `1e5bf2bd288b4306b0fb7aa3a430b3eefd2f329f429980f56941a4fe095ad789` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 219,923 | `e12b2e3a29c4a8391185af72104e8304c817f13b1dc5cebbbef7235163d58913` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,705,878 | `567befdb164a96072fd4433fbc7bf2ad7beaf0e59bc523b56ad3e26bddf8828c` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-113000.xml` | 2,705,878 | `567befdb164a96072fd4433fbc7bf2ad7beaf0e59bc523b56ad3e26bddf8828c` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 224,186 | `14d40b0a1f7e599c0029139d277a8123c4ac021c675dafe067918279be876e22` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both sources grew by roughly 1.7 KB against the preceding rebuild — this is
a copy and naming change, not a structural one: the Note body gained two sections and one
paragraph, and nine menu labels gained a name each. All twelve static checks passed in a
single run at this commit, `manifest_check` included once this table was refreshed.

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
`plutil -lint OK` on both recovered plists; `## THE NINE CIRCLES` and `## OPTIONAL HARDENING`
each present; the three identity sites all reading `PROSOCHĒ` with the Name operator still 99;
the Test-a-Circle items equal to their nine case titles; the profile menu reading
`['Paradise', 'Purgatory', 'Inferno']`; the recovered `thresholds` and `cooldown_seconds`
objects keyed by exactly those three names with `Purgatory` holding the unchanged
`[3, 5, 7, 9, 11, 13, 16, 19, 22]` and `180`. The global attachment invariant was re-measured
on the recovered payloads rather than only on `src/`: **1,105** `WFTextTokenString` values in
Dumb and **1,109** in Sentient, every one with `attachmentsByRange` keys equal to its own
`U+FFFC` offsets, zero mismatches — the invariant that matters most this wave, since every
copy edit sat upstream of the Note body's two attachments. This is structural evidence only.

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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
