# Shortcut Distribution Manifest

Rebuilt 2026-08-17 by phase 11 plan 02: BD-06 Decision 4's whole slot table applied in one
commit — nine shipped primitive names live in all three `sequences` arrays, ninety
`Selected Primitive` conditionals moved from condition 99 ("contains") to condition 4
("string is"), and `Loud Mirror` given a real dispatch branch so Circle 8 is no longer dead.
The preceding rebuild was phase 11 plan 01, the tracer that moved one name (`Knock` →
`Pause`) end to end. Built with Shortcuts Playground
target `--target-macos 26 --target-platform all`. The `all` platform target is deliberate and
is recorded as `docs/BUILD-NOTES.md` DEV-01: the `ios` target rejects the file wholesale —
including the `conditional` and comment identifiers — because the bundled iOS snapshot is
incomplete, not because the shortcut is unsound.

Both forks were regenerated from the same generator run rather than either being carried
forward: `src/PROSOCHE-*.xml` are generated files, and Sentient is a fork *of the built Dumb
source*, so a Sentient carried across a Dumb change is a fork of a file that no longer
exists. Regenerating both in one pass is the only way the shipped pair provably matches
`tools/build_state_engine.py` at this commit.

| Fork | Source / archive / signed artifact | Bytes | SHA-256 |
|---|---|---:|---|
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,667,477 | `c92ccb3087e7fdb086f51a579ea67bf634bd8efd51af595a53de067b4feae102` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-105621.xml` | 2,667,477 | `c92ccb3087e7fdb086f51a579ea67bf634bd8efd51af595a53de067b4feae102` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 218,979 | `7a9ba1fee55d404b1cd79ff5c8cecac3d61b643e4497fbbe22d258e9a10d0357` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,704,157 | `2b83f7915982d62001f6345da5c68feefe5a4dec15089cf4de3a4e83e3c17f6e` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-105633.xml` | 2,704,157 | `2b83f7915982d62001f6345da5c68feefe5a4dec15089cf4de3a4e83e3c17f6e` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 223,070 | `e7c8f31141f18cb526d008242e89cd887df1c43333f2a99f8a25bf14ad28f04a` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both sources grew by roughly 407 KB against the preceding rebuild: adding
the ninth dispatch branch costs one wrapper plus one `mirror_and_voice()` expansion in each
of the ten `primitive_dispatch()` renderings, taking the dispatch surface from 80 branches
to 90. Both forks passed the validator and all eleven prior static checks plus
`docs/note_identity_check.py` in a single run at this commit, and `manifest_check` as the
twelfth once this table was refreshed.

Both signed containers were decrypted via the AEA1 recipe and asserted against the roster
move: `plutil -lint OK` on both recovered plists; the retired names `Knock`,
`Ash+Confession`, `Silence+Mirror` and `Dimming+Mirror` appear on **zero** lines of either
payload; `Loud Mirror` appears on **23** lines of each, so the Circle-8 entry reached the
shipped artifact; every `Selected Primitive` conditional in both payloads carries condition
code **4** and none carries 99; and the recovered `sequences` object holds exactly the nine
shipped names, nine per array, with `Eject` at Circle 6 in all three. The global attachment
invariant was re-measured on the recovered payloads rather than only on `src/`: **1,105**
`WFTextTokenString` values in Dumb and **1,109** in Sentient, every one with
`attachmentsByRange` keys equal to its own `U+FFFC` offsets, zero mismatches. This is
structural evidence only.

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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
