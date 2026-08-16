# Shortcut Distribution Manifest

Rebuilt 2026-08-17 after quick task `260817-au7`, which repaired the iOS 26 Personal
Automation onboarding steps in the Control Room Note (see `docs/BUILD-NOTES.md` §20); the
preceding rebuild was the Phase 10 ship-readiness and UX pass. Built with Shortcuts Playground
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
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,260,491 | `1715c5fbe59cb5b2f4ae1cd8ed64b591eaceb5806b06f13b31f4e5f2f7fd444b` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-020725.xml` | 2,260,491 | `1715c5fbe59cb5b2f4ae1cd8ed64b591eaceb5806b06f13b31f4e5f2f7fd444b` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 193,819 | `b7fe5e96fc7e4e475f583576da04dd43e4062111d35fcf346c90cbc9d195b468` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,297,171 | `4e976cdec39aa0e994aeb86784d6a60a19adc1a02a20c7c26c44c96eb32dcda3` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-020737.xml` | 2,297,171 | `4e976cdec39aa0e994aeb86784d6a60a19adc1a02a20c7c26c44c96eb32dcda3` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 198,124 | `67e5fc3210e100502f9e895805f964fa4f904b65a1ce3fae52cc14678d27da3e` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both forks passed the validator and all ten static checks
(`state_engine`, `phase5`, `phase6`, `phase7`, `phase9`, `sentient_audit`, `sentient_core`,
`environmental_restore`, `router_ui_census`, `sequence_dispatch`) in a single run at this
commit, plus `manifest_check` as the eleventh once this table was refreshed. Both signed
containers were decrypted via the AEA1 recipe and re-asserted against the corrected Control
Room Note: exactly one note body per fork, still a `WFTextTokenString`, both attachment
ranges equal to the recomputed placeholder offsets (`{5478, 1}`, `{5509, 1}`), zero stale
onboarding strings, and all seven replacement strings present.

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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
