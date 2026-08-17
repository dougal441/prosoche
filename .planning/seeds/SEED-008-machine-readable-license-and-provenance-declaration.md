---
id: SEED-008
status: dormant
planted: 2026-08-17
planted_during: Phase 10 complete / phases 11-20 scoped (v1.0 milestone)
trigger_when: before any public release, launch post, or Substack announcement — and before any decision to accept money for PROSOCHĒ
scope: medium (a declaration file is small; the licensing decision underneath it is not)
---

# SEED-008: A robots.txt-equivalent for AI readers, carrying licence and attribution intent

Ship a machine-readable declaration aimed at the AI agents that will parse this
repo and the signed `.shortcut` files — to reverse-engineer them, to judge whether
they are safe, and possibly to lift them. Allow much of that deliberately, while
imbuing the artifact with terms: always free to share, always credited, and if
someone finds value in it — including in a spin-off — attribution survives and
there is a path for the author to be paid.

## Why This Matters

PROSOCHĒ is unusually exposed to AI-mediated reading. It ships as plist XML and as
AEA1 archives that decrypt to plist XML, with no compiled binary and no server. Anyone
who wants to understand it can, and increasingly the "anyone" is an agent doing it on
someone's behalf. Three of those readings are ones we actively *want*:

- **Safety adjudication.** A tool that dims the screen, silences audio, toggles Color
  Filters and locks the phone should be legible to whoever is checking it is not
  malware. Obscurity would be the wrong defence and would undercut the privacy claim.
- **Trust.** "No behavioural data leaves the device" is verifiable by reading the graph.
  That verification is a feature.
- **Reuse and study.** The behavioural design is the contribution; other people building
  on it is the point.

The reading we want to shape rather than block is the fourth: an agent ingests the whole
thing, and a spin-off appears with the design intact and the provenance gone.

## The constraint this idea has to survive

**The project is MIT licensed** (`LICENSE`, "Copyright (c) 2026 Dougal Hanson") **and the
repository is public** — 102 commits pushed to `github.com:dougal441/prosoche` on
2026-08-17. That matters more than the declaration file does:

- MIT **permits** commercial use, closed-source forks, sublicensing and resale. It
  requires only that the copyright notice be retained in copies of *the software*. It
  imposes **no royalty, no share-alike, and no product-facing attribution**.
- So "if people see value, even in a spin-off, I can collect money" is **exactly what MIT
  gives away**, and "I always get credit" is weaker under MIT than it sounds — a
  notice in a source file is not a credit in a product.
- **The grant already made is irrevocable for everything published so far.** Re-licensing
  changes future versions only; anyone may fork today's tree under MIT permanently.

None of that blocks the idea. It means the declaration is the *second* half of the work,
and the licensing decision is the first.

## The two layers, which must not be conflated

**1. Advisory — the robots.txt analogue.** A declaration file (`ai.txt` / `llms.txt` /
an embedded header in the Note and the plist comments) stating what the author permits,
what they ask for, and how to attribute. Like `robots.txt`, it is **a request, not a
control**. Honouring it is voluntary and unenforceable; well-behaved agents increasingly
do, badly-behaved ones never will. Its value is in making intent unmissable and in
giving a good-faith reuser something unambiguous to comply with.

**2. Operative — the licence.** The only layer with teeth. Options span a real spectrum,
and they trade against each other:

| Direction | Gets you | Costs you |
|---|---|---|
| Stay MIT | Maximum spread, genuinely open source, no friction | No royalty path, weak attribution, spin-offs owe nothing |
| Copyleft (GPL/AGPL) | Derivatives stay open, spin-offs cannot close it | Still no royalty; largely unenforceable against a Shortcut fork in practice |
| Dual licence (e.g. AGPL + commercial) | Free for individuals, paid for commercial use | Requires you to hold all rights and to actually pursue licensees |
| CC BY-SA | Strong attribution, share-alike | Not designed for software; NC variants are **not** open source |
| Source-available (BSL, PolyForm) | Explicit non-compete window, delayed open release | Forfeits the "open source" label, which this project currently claims |

**Positioning consequence worth deciding deliberately:** `PROJECT.md` and the README
describe PROSOCHĒ as "free, open-source". Any non-commercial or source-available term
would make that description inaccurate in the OSI sense, and the honest move would be to
change the wording alongside the licence rather than keep the label.

**This is a decision with legal and financial consequences, and I am not a lawyer.** The
option map above is factual, not advice. Anything involving revenue from third-party
commercial use is worth an actual solicitor before it ships.

## When to Surface

**Trigger:** before any public release, launch post, or Substack announcement — and
before any decision to accept money for PROSOCHĒ.

Surface it early rather than late. The irrevocability point above is the reason: every
day the repo sits public under MIT widens the set of code that can never be pulled back
under different terms. If the licensing intent is going to change, the cheapest moment
is before the audience arrives, not after.

## Scope Estimate

**Medium.** The declaration file itself is an afternoon. Deciding what it declares is
the real work, and it is a decision the author has to make rather than delegate.

Rough shape if pursued:
1. Settle the licensing intent — free-to-share vs. paid-commercial, and whether "open
   source" survives as a claim.
2. Take advice if any revenue path is involved.
3. Replace or supplement `LICENSE`; update README and `PROJECT.md` wording to match.
4. Write the advisory declaration: what reuse is welcomed (safety audit, study,
   personal forks), what attribution is asked for, where the canonical source lives,
   how to contact for commercial terms.
5. Embed it where an AI reader will actually hit it — repo root, the Control Room Note
   body, and a comment action near the top of both plists, since the signed artifact
   travels independently of the repo.
6. Decide whether the signed `.shortcut` should carry it too, given §8's decrypt path
   makes the plist readable to anyone who wants it.

## Breadcrumbs

- `LICENSE` — MIT, Copyright (c) 2026 Dougal Hanson. The thing the idea has to reckon with.
- `.planning/PROJECT.md`, `README.md` — both describe the project as "free, open-source";
  wording is coupled to any licence change.
- `.claude/CLAUDE.md` §8 — the `aea decrypt` + `aa extract` recovery path. The reason a
  signed artifact is not opaque and a declaration inside it is worth carrying.
- `docs/BUILD-NOTES.md` §20 — records that both forks currently name
  `PROSOCHĒ — Nine Circles — Dumb` as the Run Shortcut target; a fork-naming decision
  owned by Build Addendum 01 (Phase 11), and adjacent to how the product identifies itself.
- Canonical strategy §27 — the privacy model. The "verifiable by reading it" property is
  the argument against obscurity as a defence.

## Related

- **SEED-002** (open-source release readiness) — the closest neighbour. If that seed is
  actioned, this one should be actioned in the same pass; releasing before settling the
  licence is the failure mode both describe.
- **SEED-007** (Substack) — a launch post is a trigger condition for this seed, not an
  independent activity.

## Notes

Captured 2026-08-17 via one-shot seed capture, then enriched in place with the MIT/public
-repo constraint, which the original idea text did not account for and which materially
changes the work.
