# Shortcut Distribution Manifest

Rebuilt 2026-08-17 after the Phase 10 ship-readiness and UX pass, with Shortcuts Playground
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
| Dumb source | `src/PROSOCHE-Dumb.xml` | 2,259,398 | `aeafe01ae86252c4922794219a9aeda888850b768b8ffdd65beb2415ef5efd81` |
| Dumb archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Dumb-013251.xml` | 2,259,398 | `aeafe01ae86252c4922794219a9aeda888850b768b8ffdd65beb2415ef5efd81` |
| Dumb signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut` | 193,498 | `47957dbf429bd2d5671b69d87d8510b08abf70bbe1cfca8975a192c96bcb6324` |
| Sentient source | `src/PROSOCHE-Sentient.xml` | 2,296,078 | `293ac146598f49dcb727f703bbd519722c68233faa3591c43ab83f3516ee1229` |
| Sentient archive | `artifacts/shortcuts/2026-08-17/PROSOCHĒ — Nine Circles — Sentient-013301.xml` | 2,296,078 | `293ac146598f49dcb727f703bbd519722c68233faa3591c43ab83f3516ee1229` |
| Sentient signed | `artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut` | 197,668 | `c8656495f2ce5a3e88b595d06544f5bcbb75029cd84e94e936cd80558416fcbf` |

Each dated archive is byte-identical to its `src/` counterpart, which is what makes the
archive a pre-sign record rather than a copy of something else. The two source checksums
differ by design. Both forks passed the validator and all ten static checks
(`state_engine`, `phase5`, `phase6`, `phase7`, `phase9`, `sentient_audit`, `sentient_core`,
`environmental_restore`, `router_ui_census`, `sequence_dispatch`) in a single run at this
commit, and both signed containers were decrypted via the AEA1 recipe and re-asserted
against the phase's structural invariants — 9 of 9 on each fork.

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
> **DIST-03 — device verification — remains OPEN.** `xcrun devicectl list devices` reports
> no devices, so no criterion in either UAT file has been exercised. Nothing in this manifest
> should be read as device evidence.
