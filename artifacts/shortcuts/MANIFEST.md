# Shortcut Distribution Manifest

Rebuilt 2026-08-17 by phase 11 plan 02: BD-06 Decision 4's whole slot table applied in one
commit — nine shipped primitive names live in all three `sequences` arrays, ninety
`Selected Primitive` conditionals moved from condition 99 ("contains") to condition 4
("string is"), and `Loud Mirror` given a real dispatch branch so Circle 8 is no longer dead.
The preceding rebuild was phase 11 plan 01, the tracer that moved one name (`Knock` →
`Pause`) end to end. Built with Shortcuts Playground
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
differ by design. Both sources grew by roughly 407 KB against the preceding rebuild: adding
the ninth dispatch branch costs one wrapper plus one `mirror_and_voice()` expansion in each
of the ten `primitive_dispatch()` renderings, taking the dispatch surface from 80 branches
to 90. Both forks passed the validator and all eleven prior static checks plus
`docs/note_identity_check.py` in a single run at this commit, and `manifest_check` as the
twelfth once this table was refreshed.

Two of those checks changed status in this rebuild. `docs/sequence_dispatch_check.py` is no
longer a reporter: it now exits non-zero on any orphaned sequence entry, any unreachable
dispatch branch, any branch of unknown matching semantics, and any entry matched by more
than one distinct branch name, and its `KNOWN_ORPHANS` escape hatch is empty. It was proven
to fail before it was trusted to pass — a copy of the Dumb source with one sequence cell
replaced by a name no branch emits makes it exit 1. `tools/build_state_engine.py` gained
`verify_dispatch_coverage()`, armed in both builders, which enforces the same invariant
before any write. Neither instrument existed for the four phases during which Circle 8
dispatched nothing.

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
