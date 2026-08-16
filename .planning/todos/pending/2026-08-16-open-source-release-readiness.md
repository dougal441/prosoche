---
created: 2026-08-16T00:20:00.000Z
title: Open-source release readiness
area: docs
severity: minor
files:
  - README.md
  - docs/BUILD-NOTES.md
---

## Problem

"Free and open source" is in the product's first sentence (§0), has its own section (§26),
and is a canonical decision (§35). It is also the only major strategy commitment with **no
todo, no phase, and no artifact** behind it. `README.md` is 1.3KB. There is no licence
file, no contribution guide, no changelog, no privacy explanation, and no published
repository — the work lives on an unpushed branch (`codex/automation-parameter-diagnosis`).

§26 lists what the repository should eventually contain:

- signed release `.shortcut` (exists for Dumb; Sentient is stale)
- unsigned XML source (exists)
- human-readable architecture docs (partially — `docs/BUILD-NOTES.md` is a debug record,
  not an architecture doc)
- model prompts (exist in the generator, not extracted or documented)
- Heat/Gravity logic (exists in `src/CONFIG-BLOCK.md`, undocumented for outsiders)
- known iOS limitations (**this is genuinely excellent already** — the seven authoring axes
  and verified runtime semantics in `.claude/CLAUDE.md` are the most valuable thing in the
  repo for anyone else building iOS Shortcuts, and are currently buried in a project-private
  config file)
- privacy explanation, contribution guide, changelog (none)

§26 also requires the README to state plainly that: all behavioural data stays on device,
there is no external analytics, Sentient uses Apple's On-Device model, model output can be
wrong, **the system is self-directed and bypassable**, and the user owns and can inspect
the Shortcut. Two of those are claims the project cannot currently make honestly — the
On-Device guarantee is gated on CAP-26/UA-02, and any "nothing leaves the device" phrasing
needs qualifying once the support link exists.

This is low severity because nothing is broken, but it is on the critical path to the
project existing publicly at all, and it is the difference between a personal shortcut and
the thing §1 argues for — a free alternative to a subscription for regaining control of
your own device.

## Solution

1. **Do not publish before the device UAT set closes.** Publishing an artifact whose CLOSE
   path, Circles, contracts, exits, and cooldown have never run on a device would put
   strangers in the position of discovering the failures. The six `device-uat-*` todos are
   the real gate.
2. **Choose and add a licence.** Not yet decided anywhere in the repo. Worth an explicit
   choice given §26's forkability goal.
3. **Write the README against §26's checklist**, stating each required claim plainly — and
   only the ones that are true today. In particular: the system is **bypassable and not
   tamper-proof** (§5.1) must be stated up front, not buried; that honesty is load-bearing
   for a self-directed behaviour-change tool and distinguishes it from parental control.
4. **Extract the iOS Shortcuts findings into a public document.** The authoring axes,
   verified runtime semantics, the AEA1 decryption recipe, and the donor-evidence method
   are genuinely novel and useful to people who will never use PROSOCHĒ. Publishing them
   separately is probably the project's largest contribution outside its own users.
5. **Write an architecture doc for outsiders** — the OPEN/CLOSE loop, Heat/Gravity/Pressure,
   the nine Circles, the six exits, and where state lives. `docs/BUILD-NOTES.md` is an audit
   trail, not an explanation, and should stay that way.
6. **Document the model prompts** (§14.6) verbatim, since a user cannot audit what they
   cannot read — this is part of the privacy argument, not decoration.
7. **Add a changelog and contribution guide**, and decide what "contribution" means for a
   product distributed as a signed binary artifact built from a Python generator — this is
   not a normal repo and the guide should say so.
8. **Privacy statement** (§27) covering: local-only by default, iCloud sync of Note/JSON is
   the user's own configuration, no telemetry to the creator, and — once the support link
   exists — that the outbound link is the single exception.
9. **Push the branch and open the repository.** Confirm the provenance guard passes and
   that no device evidence containing personal data (the donor shortcuts, the screenshots
   in `.planning/debug/`) is published without review — several are photographs of the
   owner's phone.

## Related

- Canonical strategy §26 (open-source principles — the full checklist), §27 (privacy
  model), §5.1 (never claim tamper-proof), §1 (the anti-subscription argument this
  fulfils), §35 (`Open source | Yes`).
- `.claude/CLAUDE.md` § Conventions — the findings worth extracting publicly.
- The six `2026-08-16-device-uat-*.md` todos — the real gate on publishing.
- `2026-08-16-recover-the-use-model-on-device-literal.md` — gates the On-Device claim in
  the README.
- `2026-08-16-build-support-prosoche-low-salience.md` — adds the one outbound link the
  privacy statement must qualify.
