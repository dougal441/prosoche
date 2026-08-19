---
id: SEED-009
status: dormant
planted: 2026-08-17
planted_during: Phase 10 complete / phases 11-24 scoped (v1.0 milestone)
trigger_when: when planning Phase 17, Phase 19 or Phase 20 — each item below names its phase
scope: medium — one rename is trivial, the salience and sequence questions are design work with device evidence as their input
---

> **COVENANT OVERHAUL (2026-08-19):** Items 1, 3 and 4 are RESOLVED BY DESIGN, not deferred to tuning: BD-09 retires the `Leaving / Continue` pre-menu entirely (item 1's sharp half), folds the leave affordance into each interactive surface with the `Exit / Stay`-style naming landing in Phase 18 (item 3), and supersedes BD-06 Decision 4's slot table with the covenant ladder (item 4 — the re-cut this seed said must land as a decision record did, as BD-09 Decision 7). Item 2 (record dismissibility per Circle) STAYS LIVE and is written into Phase 22's device-UAT goal. Old phase numbers in this seed read through STATE.md's 2026-08-19 renumbering entry.


# SEED-009: Intervention salience, notification volume, and sequence tuning

Four related observations about how PROSOCHĒ *feels* in use rather than whether it works.
They share one root: an intervention that is too frequent or too weak trains the user to
dismiss it, and a dismissed intervention is indistinguishable from no product. Canonical
§30's first-named failure mode is intervention fatigue, and §12's stated key failure is that
the user disables PROSOCHĒ because it is annoying — a product failure even if it blocks more
opens.

## 1. Too many notifications — hum silently until an intervention, not before it → **Phase 20**

The product is too much in the user's face. It gets in the way of ordinary phone use, and
people will simply delete it. It should **hum silently in the background until an
intervention actually happens** — not until it announces that one is coming.

**Partly addressed already; the sharp half is not.** Phase 10 removed the OPEN notification
entirely and added the Circle 0 silent band, so a low-Pressure open now shows nothing at all.
What Phase 10 did *not* address is the distinction this item is really making:

> At every Circle ≥ 1 the user first gets `Circle N opened. Leave now, or continue?` —
> a menu — and only after tapping Continue does the primitive fire. **That menu is an
> announcement that an intervention is about to happen.** It is exactly the "telling you
> there's going to be an intervention" this item objects to.

**This is a genuine tension, not a simple fix, and it should be resolved deliberately.**
That menu is also §6.4's easy-dismissal mechanism — the field study's finding is that giving
the user an easy way to abandon the consumption attempt is the *single strongest* lever,
stronger than the deliberation message. So the menu is simultaneously the best thing in the
design and the thing that makes the product feel talkative. Candidate resolutions, none free:

- Let the primitive fire **first** and carry the exit affordance *within* it, so there is one
  surface instead of two — preserves dismissal, removes the announcement.
- Keep the menu only at the depths where a pre-warning is itself the intervention.
- Widen the silent band further so fewer opens reach any surface at all — cheap, and Phase 10
  already made the thresholds tunable for exactly this.

Measure before choosing. The tuning signal already exists: `10-UAT.md` Test 2 reports
opens-to-first-interruption.

## 2. "Pause, take a breath" is too easy to dismiss → **Phase 19**

A notification whose entire content is *pause, take a breath* costs nothing to swipe away.
This is about **intervention potency**, and it belongs with device UAT because dismissibility
is only observable in use — a structural check cannot see it.

**Do not confuse this with §6.4.** That finding is that an easy way to *leave the app* is the
strongest mechanism. This item is about an intervention that is easy to *ignore*. Those are
opposite properties: the **exit** should be one tap; the **interruption** should not be
frictionless to wave through. Conflating them would justify weakening exactly the wrong half.

**Phase 14 is already the substantive answer for the specific example.** Ash currently ships
as an alert reading *"Pause. Put the phone down for one breath."* — Phase 14 replaces it with
a real Color Filters grayscale toggle, which is a state change the user must actively undo
rather than a sentence they can swipe. Grayscale also carries the strongest single piece of
research support in the whole strategy (§6.5).

**What Phase 19 should add:** make dismissibility an explicit observation, not an incidental
one. For each Circle record *what it cost to get past it* — taps, seconds, whether the user
had to do anything at all — alongside whether it fired. A Circle that fires and is waved
through in under a second has not been verified working in any sense that matters.

## 3. Rename `Leaving / Continue` → `Exit / Stay` → **Phase 17**

Shorter, plainer, and `Exit` aligns the menu with the product's own exit vocabulary — the six
exit routes, `select_exit()`, `record_exit_and_route()`. `Stay` is more honest than `Continue`
about what the choice actually is.

**Sequencing caution, worth deciding rather than absorbing.** These two words will have been
touched three times by the time Phase 17 lands: Phase 10 already reworded the prompt, Phase 11
is the rename phase, and this would be a third pass. The link to Phase 17 is defensible —
that is where exit vocabulary is settled and the routed Exile arrives — but if Phase 11 is
already editing this string, folding the rename in there is one pass instead of two. Decide
when planning 11; do not let it happen twice by default.

## 4. Fine-tune the Circle order, and what happens immediately → **Phase 20**

Revisit which primitive fires at which depth, what escalation feels like in sequence, and
what happens *immediately* on an open versus after a beat.

**This means revisiting BD-06 Decision 4, which is fine — but not quietly.** The slot table
is recorded in `docs/CAPABILITY-DECISIONS.md` and is binding on Phases 11, 14, 15, 16 and 17
precisely so five phases do not each re-cut it. Tuning it at Phase 20, *after* device evidence
exists, is the right moment — but it must land as a superseding decision record in the same
file, not an edit to `src/CONFIG-BLOCK.md`'s arrays. That file already warns that sequences
are "a deliberate tuning act, not a casual edit."

**"What happens immediately" is partly a latency question, and it is measurable.** An OPEN
automation fires, Shortcuts launches, the graph runs, and only then does anything appear.
Phase 20's interaction-cost pass should measure perceived latency on device — an intervention
that arrives two seconds after the user is already scrolling has missed the interval the whole
product exists to create.

Items 1 and 4 are the same question from two directions: item 1 asks *how often anything
surfaces at all*, item 4 asks *what surfaces when it does*. Plan them together in Phase 20
rather than as separate passes.

## When to Surface

**Trigger:** when planning **Phase 17** (item 3), **Phase 19** (item 2), or **Phase 20**
(items 1 and 4). Pointers to this seed are written into all three ROADMAP goals so a planner
meets it without needing a milestone scan.

## Scope Estimate

**Medium.** Item 3 is a string change. Item 2 is an added observation dimension in an existing
UAT. Items 1 and 4 are real design work whose input is device evidence that does not exist
yet — which is why they sit at Phase 20, after Phase 19.

## Breadcrumbs

- `tools/build_state_engine.py` — `universal_leaving()` emits the `Leaving / Continue` menu
  and calls `primitive_dispatch()`; the menu/primitive ordering is item 1's whole subject.
- `src/CONFIG-BLOCK.md` `sequences` — the slot table item 4 would tune, with its own
  do-not-edit-casually warning.
- `docs/CAPABILITY-DECISIONS.md` BD-06 Decision 4 — the binding slot allocation.
- `.planning/phases/10-.../10-UAT.md` Test 2 — reports opens-to-first-interruption, the
  existing tuning signal for item 1.
- Canonical strategy §6.4 (dismissal is the strongest mechanism — the finding item 2 must not
  be confused with), §6.5 (the grayscale evidence), §12, §29 (voice), §30 (intervention
  fatigue).

## Related

- **Phase 14** — Ash as real grayscale, the substantive answer to item 2's specific example.
- **Phase 10** — already removed the OPEN notification and added the Circle 0 silent band;
  item 1 is what remains after that.
- **SEED-004 / Phase 23** — the Attention Receipt carries the opposite risk (rendering depth
  as achievement); tuning frequency down and framing depth as cost are the same instinct.

## Notes

Captured 2026-08-17 from four linked observations. Item 1's second paragraph and item 2's
§6.4 distinction were added during capture — the original text did not separate the
announcement from the intervention, or easy-to-leave from easy-to-ignore, and both
distinctions change what the fix is.
