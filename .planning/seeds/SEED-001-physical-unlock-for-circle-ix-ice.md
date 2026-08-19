---
id: SEED-001
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: after the device-UAT backlog closes, and only once Phase 999.5 (Circle IX cooldown UAT) has proven the time-bound expiry on device
scope: medium — requires a canonical-strategy amendment before any code
---

> **COVENANT OVERHAUL (2026-08-19):** Trigger housekeeping only — the design is untouched by the overhaul (BD-11 explicitly keeps all variability and every unlock mechanism out of Frozen's determinism, which is this seed's own constraint). Its trigger anchored on retired 999.x phases; re-anchor on Phase 22, where Frozen gets its device scrutiny.


# SEED-001: Physical unlock (QR scan or NFC tap) to exit Circle IX / Frozen

## Why This Matters

While frozen in Circle IX (`Treachery` / **Frozen** under Build Addendum 01), require a
physical act — scan a QR code, or tap an NFC tag — deliberately located somewhere that
forces movement and separation from the trigger context. A commitment device: the cost of
exiting becomes physical distance rather than willpower. It matches the product's own
Phase D vision (§34: "a deliberately located physical tag; optional Circle IX unlock;
commitment through movement/physical separation").

It is **currently out of scope by explicit canonical decision** (§4, §22, §35 all say no
NFC in v1) and cannot be built without amending the strategy first — per §38, the document
wins over conversation until amended.

Two hard constraints any implementation must satisfy:

1. Ice must remain time-bounded regardless. A physical unlock the user can't reach (tag at
   home, no camera access, dead of night) must never convert a time-bounded cooldown into
   an indefinite lockout — it can only ever be an *early* exit.
2. It must compose with Build Addendum 01 §3's Panic Escape removal pattern (raised bypass
   cost via manual Note edit + confirmation), not contradict it.

Capability position already checked against the bundled ToolKit: NFC cannot be awaited
inside a running shortcut (zero NFC in-shortcut identifiers across all three snapshots) —
it can only *start* a second shortcut via a Personal Automation trigger, which is a more
complex, more race-prone design than QR. QR (`scanbarcode` / `BarcodeScannerIntent`)
*might* be a blocking in-run prompt, but whether it opens a live camera scanner on iOS 26
is unverified and must be settled with a donor shortcut before anything is designed.

## When to Surface

**Trigger:** after the device-UAT backlog closes, and specifically after Phase 999.5
(Circle IX cooldown UAT) proves the time-bound expiry works on a real cooldown cycle —
that proof is this feature's safety floor and hard prerequisite.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches Circle
IX, Ice, or physical/commitment-device features.

## Scope Estimate

**Medium.** Not just a build — the first deliverable is a canonical-strategy amendment
(§4, §22, §35 updated together), then a QR-vs-NFC capability decision settled by a donor
shortcut, then the actual gate design. Straightforward once the amendment and donor
evidence exist; blocked without them.

## Breadcrumbs

- Canonical strategy §4 (NFC out of scope), §22 (Ice — no NFC, "there must be a route
  out"), §34 Phase D (the scope this promotes), §35 (decision table row `NFC | No`), §38
  (document wins), §5.1 (never claim tamper-proof).
- `PROSOCHE_Build_Addendum_01.md` §3 (Panic Escape removal — the established pattern for
  raising bypass cost).
- `.claude/CLAUDE.md` §8 (signed-artifact decryption recipe, needed for the QR donor).
- `.planning/phases/999.5-device-uat-circle-ix-cooldown-and-route-out-of-ice/` — hard
  prerequisite; the time-bound expiry proven there is this feature's safety floor.

## Notes

Originally captured as a standalone todo (`2026-08-16-physical-unlock-for-circle-ix-ice.md`)
with a full capability audit already done (NFC: does not exist as an in-shortcut action;
QR: `scanbarcode` present in v63/v78 but absent from the iOS-27-Simulator snapshot, live-
camera behaviour unverified). That audit is preserved in full in this seed's git history —
recover it with `git log -p -- .planning/todos/pending/2026-08-16-physical-unlock-for-circle-ix-ice.md`
if the seed is promoted and the capability findings need re-checking.
