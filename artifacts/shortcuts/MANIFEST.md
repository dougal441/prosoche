# Shortcut Distribution Manifest

Rebuilt 2026-08-17 by phase 11 plan 01, the Build Addendum 01 tracer: the single BD-06
primitive rename `Knock` → `Pause`, driven from the generator's dispatch tuple through the
Config literal in `src/PROSOCHE-Dumb.xml` action 7 and read back out of both signed
containers by decryption. The preceding rebuild was quick task `260817-au7`, which repaired
the iOS 26 Personal Automation onboarding steps in the Control Room Note (see
`docs/BUILD-NOTES.md` §20). Built with Shortcuts Playground
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
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,260,491 | `efad0819d5c01ae6bced0eb42beca4a21bc66753bdfe7d602c1dc5e1930efe81` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-103801.xml` | 2,260,491 | `efad0819d5c01ae6bced0eb42beca4a21bc66753bdfe7d602c1dc5e1930efe81` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 193,836 | `bb93af559b92dedbee2e41a14187ff31d27ce213ada763e699e51ac6fbc575eb` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,297,171 | `8d9c61056e7395983298baf642f6a06bbbca5e2d53b9fcb75df5a03f5663cda1` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-103814.xml` | 2,297,171 | `8d9c61056e7395983298baf642f6a06bbbca5e2d53b9fcb75df5a03f5663cda1` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 198,150 | `e162be1643672d73c2bc603d222175f3d6e54caa5df07f29e0bcddeffa97b088` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both source byte counts are unchanged from the preceding rebuild because
`Knock` and `Pause` are the same length; the hashes are not, which is the point of recording
both. Both forks passed the validator and all ten static checks (`state_engine`, `phase5`,
`phase6`, `phase7`, `phase9`, `sentient_audit`, `sentient_core`, `environmental_restore`,
`router_ui_census`, `sequence_dispatch`) in a single run at this commit, plus
`manifest_check` as the eleventh once this table was refreshed.

Both signed containers were decrypted via the AEA1 recipe and asserted against the tracer
rename: `plutil -lint OK` on both recovered plists; the retired entry appears on **zero**
lines of either; `Pause` appears on 43 lines of each (three `sequences` cells plus ten
dispatch renderings × three sites, plus the ten pre-existing `Ash` alert bodies that already
contained the word); and the recovered `sequences` object holds `Pause` in exactly three
cells per fork. The global attachment invariant was re-measured on the recovered payloads
rather than only on `src/`: **775** `WFTextTokenString` values in Dumb and **779** in
Sentient, every one with `attachmentsByRange` keys equal to its own `U+FFFC` offsets, zero
mismatches. This is structural evidence only.

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
> **⚠ This build additionally carries the first BD-06 primitive rename, `Knock` → `Pause`,
> which has never dispatched on a real iPhone.** The name is proven present in the generator
> tuple, in all three `sequences` arrays, on all ten emitted dispatch branches and in the
> decrypted payload of both signed containers — all of it file-level structural proof. That a
> Circle-1 open actually reaches the renamed branch on device is **not** proven and is not
> claimed. Read `docs/BUILD-NOTES.md` §21.
>
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
