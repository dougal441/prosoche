---
created: 2026-08-16T00:00:00.000Z
title: Physical unlock (QR scan or NFC tap) to exit Circle IX / Frozen
area: product
severity: major
files:
  - tools/build_state_engine.py
  - src/CONFIG-BLOCK.md
  - PROSOCHE_Nine_Circles_Canonical_Strategy.md
---

## Problem

Idea: while the user is frozen in the ninth Circle (`Treachery` / **Frozen** under Build
Addendum 01; `Ice` in the original naming), require a **physical act** to get out — scan a
QR code, or tap an NFC tag — deliberately located somewhere that forces movement and
separation from the trigger context. This is a commitment device: the cost of exiting
becomes physical distance rather than willpower.

It fits the product's own philosophy well (§34 Phase D describes exactly this: "a
deliberately located physical tag; optional Circle IX unlock; commitment through
movement/physical separation"). But it is **currently out of scope by explicit canonical
decision** and cannot be built without amending the strategy first.

**This requires a strategy amendment, not just an implementation.** The canonical strategy
says, in three separate places:

- §4 "Explicitly out of scope for the current build → NFC … deliberately removed from v1";
- §22 "Circle IX — Ice: No NFC in this version";
- §35 canonical decision table: `NFC | No`.

§38 also states that where earlier conversation ideas conflict with the strategy document,
the document wins. So the first deliverable here is a decision recorded against §35 that
promotes Phase D, not a code change.

**Two hard safety constraints that the canonical strategy already imposes and that this
idea directly stresses:**

1. §22: "There must be a route out. The product should not trap the user in permanent
   escalating punishment." A physical unlock that the user cannot reach — tag left at
   home, QR code in another building, phone with no camera access, dead of night —
   converts a time-bounded cooldown into an indefinite lockout. **Ice must remain
   time-bounded regardless.** The physical unlock can only ever be an *early* exit from a
   cooldown that would expire on its own anyway; it must never be the sole route out.
2. Build Addendum 01 §3 already establishes the pattern for deliberately raising the
   bypass cost — Panic Escape removal requires manual editing of the Note plus explicit
   confirmation. Whatever this feature does must compose with that, not contradict it.

**Capability position — checked against the bundled ToolKit, not assumed:**

| mechanism | finding |
|---|---|
| **NFC as an in-shortcut action** | **Does not exist.** Zero NFC identifiers across all three bundled ToolKit snapshots (v63, v78, v78-iOS27). A shortcut cannot *await* an NFC tap mid-run. |
| **NFC as an automation trigger** | Exists — `when_nfc_scan_tag` (`AUTOMATION_TRIGGERS.md:106`), a Personal Automation trigger. So NFC can only *start* a shortcut, never be awaited inside one. |
| **QR / barcode scan** | `is.workflow.actions.scanbarcode` ("Scan QR or Barcode") is present in the generic v63 snapshot and in v78 — **but is absent from the bundled iOS-27-Simulator snapshot**, which instead carries `com.apple.BarcodeScanner.BarcodeScannerIntent`. An OS27 `imageFile` parameter exists for scanning an *image file* (`ACTIONS.md:133`), and is target-gated — it must not be set at `--target-macos 26`. Whether the iOS 26 action opens a **live camera scanner** (which is what this feature needs) is **UNVERIFIED** and must not be assumed. |

The NFC finding is architecturally decisive: because NFC cannot be awaited inside a
running shortcut, an NFC unlock cannot be a blocking prompt. It must be a **second
shortcut**, fired by an NFC Personal Automation, that writes an unlock token into
`state.json` which the main shortcut then observes on the next OPEN. That is a materially
different (and more complex, more race-prone) design than the QR path — which, *if* the
live-camera behaviour verifies, can be a blocking in-run prompt. This asymmetry should
drive the choice between them.

## Solution

1. **Amend the strategy first, or don't build it.** Record an explicit decision promoting
   Phase D's physical-commitment scope into the current build, updating §4, §22 and §35's
   decision table together so the document stays internally consistent. Without this,
   §38 means any implementation is out of policy.

2. **Settle the QR capability with a donor shortcut before designing anything.** This
   project's evidence hierarchy puts user-built donors first for exactly this class of
   question. Build a one-action shortcut in Shortcuts.app on the target iPhone using
   "Scan QR or Barcode", run it, export it, and decrypt it (`aea decrypt` + `aa extract`,
   `.claude/CLAUDE.md` §8). That answers all three open questions at once: which
   identifier iOS 26 actually emits, whether it opens a live camera scanner or demands an
   image file, and what its real parameter shape and output are. **Do not author against
   `scanbarcode` before this donor exists** — the identifier discrepancy between the
   generic and iOS-specific snapshots is precisely the pattern that has produced
   validates-signs-imports-then-fails-at-runtime defects eight times in this project.

3. **Choose the mechanism on the evidence.** If the QR donor shows a live camera scan,
   QR is strongly preferred: it is a blocking in-run prompt, needs no second shortcut, no
   token in `state.json`, and no cross-automation race. NFC requires the token-passing
   architecture above and inherits every state-race concern §30 already names — only take
   it on if QR is refuted or if a physical tag is specifically wanted for the commitment
   ritual.

4. **Keep the time-bound floor, non-negotiably.** Ice expires on its existing
   profile-configured duration (~60s Paradise / ~3m Limbo / ~5m Inferno, Config-tunable)
   whether or not the physical unlock is ever performed. The physical act only ends it
   *early*. Also decide and document what happens on a *failed* scan (wrong code, camera
   denied, no tag) — the answer must be "nothing worse than waiting it out", never an
   extension.

5. **Make it opt-in and reversible.** Off by default; enabled from the Note/Config the way
   Addendum 01 handles Panic Escape removal, with explicit confirmation. The user who
   enables it should be told plainly, at enable time, what happens if the tag or code is
   unreachable.

6. **Bind the code/tag to this user's own PROSOCHĒ.** A QR code that any QR code satisfies
   is not a commitment device. Decide how the expected payload is stored and compared
   (Config or `state.json`, seeded at bootstrap with a build guard per the state-shape
   discipline) — and remember §5.1: PROSOCHĒ must never claim to be tamper-proof. This
   raises the cost of an impulsive exit; it does not prevent a determined one, and the
   copy must not pretend otherwise.

## Related

- Canonical strategy §4 (NFC out of scope), §22 (Ice — no NFC, and "there must be a route
  out"), §34 Phase D (physical commitment — the scope this promotes), §35 (decision table
  row `NFC | No`), §38 (the document wins over conversation), §5.1 (never claim
  tamper-proof).
- `PROSOCHE_Build_Addendum_01.md` §3 (Panic Escape removal — the established pattern for
  deliberately raising bypass cost) and §5 (Treachery → Frozen naming).
- `.claude/CLAUDE.md` §8 (signed-artifact decryption recipe, for the donor step) and
  § Conventions (the seven authoring axes any new action must satisfy).
