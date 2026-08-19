---
id: SEED-002
status: dormant
planted: 2026-08-16
planted_during: PROSOCHĒ Nine Circles — post OPEN-path device confirmation
trigger_when: after the device-UAT backlog (Phases 999.1-999.7) closes — do not publish before CLOSE, Circles, contracts, exits, and cooldown have run on a device
scope: medium — README, licence, docs, and a public-facing extraction of the iOS Shortcuts findings
---

> **COVENANT OVERHAUL (2026-08-19):** Re-scope before acting on this seed. BD-12 (2026-08-19) changed the licence to PolyForm Noncommercial 1.0.0 going forward, so this seed's 'free and open source' framing and its claim that no licence file exists are both superseded — a LICENSE exists and the honest public phrasing is now 'source-available, free for noncommercial use' (canon v2 §26). Its trigger anchored on the retired 999.x backlog phases; re-anchor on Phase 22 (device UAT complete) or the first public-release decision. Release readiness now includes propagating the PolyForm notice and the non-retroactive MIT history into public-facing surfaces.


# SEED-002: Open-source release readiness

## Why This Matters

"Free and open source" is in the product's first sentence (§0), has its own section (§26),
and is a canonical decision (§35) — yet it is the only major strategy commitment with **no
todo, no phase, and no artifact** behind it. `README.md` is 1.3KB. No licence file, no
contribution guide, no changelog, no privacy explanation, no published repository (work
lives on an unpushed branch).

§26 requires the README to state plainly: all behavioural data stays on device, no
external analytics, Sentient uses Apple's On-Device model, model output can be wrong, the
system is self-directed and bypassable, and the user owns and can inspect the Shortcut.
Two of those can't be honestly claimed yet — the On-Device guarantee is gated on
CAP-26/UA-02 (see the "Recover the Use Model On-Device literal" todo), and "nothing leaves
the device" needs qualifying once the support-link seed lands.

The most valuable thing to extract is arguably not PROSOCHĒ itself but the seven
authoring-axes findings and verified iOS runtime semantics in `.claude/CLAUDE.md` —
genuinely novel, hard-won knowledge for anyone else building iOS Shortcuts, currently
buried in a project-private config file.

## When to Surface

**Trigger:** after the device-UAT backlog closes. Publishing an artifact whose CLOSE path,
Circles, contracts, exits, and cooldown have never run on a device would put strangers in
the position of discovering the failures — the six device-UAT backlog phases are the real
gate, not a formality.

This seed will surface during `/gsd-new-milestone` when the milestone scope touches
release, distribution, licensing, or public documentation.

## Scope Estimate

**Medium.** Licence choice, a README rewrite against §26's checklist, an architecture doc
for outsiders, extracting the model prompts and the iOS Shortcuts findings into public
docs, a changelog/contribution guide, a privacy statement, then pushing the branch.
Mechanically straightforward; the substance (the iOS findings write-up) is the largest
single piece.

## Breadcrumbs

- Canonical strategy §26 (open-source principles, full checklist), §27 (privacy model),
  §5.1 (never claim tamper-proof), §1 (the anti-subscription argument), §35
  (`Open source | Yes`).
- `.claude/CLAUDE.md` § Conventions — the findings worth extracting publicly.
- `.planning/phases/999.*` — the device-UAT backlog gating publication.
- SEED-005 (Recover the Use Model On-Device literal) — gates the On-Device claim.
- SEED-003 (Support PROSOCHĒ contribution path) — adds the one outbound link the privacy
  statement must qualify.

## Notes

Originally captured as a standalone todo
(`2026-08-16-open-source-release-readiness.md`); full original text (§26 checklist
mapping, item-by-item plan) is preserved in git history —
`git log -p -- .planning/todos/pending/2026-08-16-open-source-release-readiness.md`.
