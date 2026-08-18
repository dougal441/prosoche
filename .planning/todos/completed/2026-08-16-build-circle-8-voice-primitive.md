---
created: 2026-08-16T23:20:00.000Z
title: Build Circle 8 — the Voice primitive dispatches nothing
area: general
severity: major
files:
  - tools/build_state_engine.py:644
  - tools/build_state_engine.py:604
  - src/CONFIG-BLOCK.md:46
---

## Problem

**Circle 8 fires no intervention at all, in every sequence.** The product ships eight
working Circles, not nine.

`primitive_dispatch()` (`tools/build_state_engine.py:644`) iterates the nine primitive
names but explicitly skips emitting a branch for one of them:

```python
for name, implementation in (("Knock", knock), ..., ("Mirror", mirror_and_voice),
                             ("Voice", mirror_and_voice), ("Ice", ice_start)):
    # Mirror is rendered once for a combined Silence+Mirror entry; Voice is a separate sequence name.
    if name == "Voice":
        continue
    group, check = if_block("Selected Primitive", 99, string=name)
```

All three sequences in `src/CONFIG-BLOCK.md` place the literal entry `"Voice"` at
position 8 — Classic, BlackMirror, and Ambient alike. The dispatch comparison is condition
code 99 ("contains"), and the string `"Voice"` contains neither `"Mirror"` nor any other
emitted branch name, so nothing catches it.

**Confirmed against the shipped artifact, not inferred.** Parsing `src/PROSOCHE-Dumb.xml`
and counting `WFConditionalActionString` values across every dispatch site gives:

| Primitive | Dispatch branches in artifact |
|---|---|
| Knock, Ash, Silence, Confession, Dimming, Exile, Mirror, Ice | 10 each |
| **Voice** | **0** |

(Ten because the general OPEN dispatch plus the nine `Test a Circle` harness branches each
render the block once.)

The user-visible consequence: at Circle 8 you get the "Circle 8 opened. Leave now, or
continue?" menu, tap Continue, and nothing happens. The escalation ladder goes quiet at
exactly the point before Ice — the second-strongest Circle in the design.

The Voice *capability* is not missing. `is.workflow.actions.speaktext` with the corrected
`WFText` parameter (DEV-C3-03) is built and renders 10 times, but only inside
`mirror_and_voice()` (`tools/build_state_engine.py:604`), gated on `voice_enabled > 0` and
a `Spoken This Run` once-only guard — so speech only ever happens as a rider on The Mirror.
Canonical strategy §11 Primitive H treats The Voice as its own escalation step above The
Mirror, not as Mirror's optional audio.

Never run on device: Circles 2–9 have never executed on real hardware
(`.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md`), so this was never
going to surface from testing. It was found by static comparison of the sequence table
against the shipped dispatch branches.

## Solution

1. **Decide the semantics first.** The most likely intent, consistent with §11 Primitive H
   and with the existing `voice_enabled` toggle:
   - **Mirror (Circle 7)** — shows the text, speaks it *only if* `voice_enabled`;
   - **Voice (Circle 8)** — the spoken address is the primitive; the escalation is that
     the phone talks to you. Whether `voice_enabled = 0` degrades Circle 8 to a
     Mirror-equivalent alert or skips it entirely is a real product decision, not an
     implementation detail. Decide it explicitly and record it.
2. **Emit a real `Voice` branch.** Either remove the `continue` and give `mirror_and_voice()`
   a mode parameter, or split it into `mirror()` and `voice()` sharing the template
   selector. Watch the `Spoken This Run` guard — if Circle 8 is reached in a run where
   Mirror already spoke, the guard currently suppresses the second utterance.
3. **Check the combined entries.** BlackMirror uses `"Silence+Mirror"` and
   `"Dimming+Mirror"`, which work today precisely *because* the match is "contains". Any
   change to the matching strategy (e.g. exact match, code 4) must not break those, and a
   future `"…+Voice"` entry would need the same treatment.
4. **Rebuild and re-verify.** Honour the build provenance guard in `.claude/CLAUDE.md`
   (`git merge-base --is-ancestor 7ca8ebb HEAD`) before running
   `tools/build_state_engine.py`. Then `docs/state_engine_self_check.py`, validate at
   `--target-macos 26 --target-platform all`, sign, and refresh
   `artifacts/shortcuts/MANIFEST.md`.
5. **Add a build guard.** The generator already asserts seven parameter-defect axes. Add an
   eighth-class check: *every distinct primitive name appearing in any `sequences` array in
   `src/CONFIG-BLOCK.md` must have at least one matching dispatch branch in the generated
   actions.* This defect class — a Config entry with no receiver — is invisible to the
   validator, the ToolKit catalog, and the signed-artifact decrypt, and would have silently
   survived any future sequence edit.

## Related

- Canonical strategy §11 Primitive H (The Voice), §12 (sequences).
- `2026-08-16-device-uat-nine-circles-and-sequence-switching.md` — the meta UAT that
  covers whether all nine actually fire; this todo is a hard prerequisite for its
  "all nine primitives fire" test.
- `.planning/phases/05-nine-primitives-environmental-safety/05-UAT.md` — notes The Voice
  "has never been heard on device"; this explains why.

## Closed — 2026-08-18 (Phase 15 — Circle 8 — the Voice primitive)

**Closed. All five Solution steps are satisfied, across two phases:**

1. **Decide the semantics first.** Answered by **D-01, D-02 and D-03**, confirmed with the user
   2026-08-18 and recorded verbatim in
   `.planning/phases/15-circle-8-the-voice-primitive/15-CONTEXT.md`, implemented in plan **15-01**.
   D-01: voice-off degrades Circle 8 to a Mirror-equivalent alert, never skips. D-02: speech is
   removed from Circle 7 entirely — this is what makes Circle 8 an escalation. D-03: Circle 8
   reuses the same 30 fact-gated Mirror templates; no new copy.
2. **Emit a real `Voice` branch.** Delivered by plan **15-01**'s split of the interim
   `mirror_and_voice()` into `mirror()` (Circle 7, shows only) and `voice()` (Circle 8, shows and
   speaks once, consent-gated), with `primitive_dispatch()`'s tuple retargeted to
   `("Mirror", mirror), ("Loud Mirror", voice)` and a new build guard,
   `verify_speaktext_placement()`, holding the split in place.
3. **Check the combined entries.** Already closed by **Phase 11** (plan 11-02, BD-06 Decision 5)
   — the sequence entry is `"Loud Mirror"`, not `"Voice"`, and dispatch moved from condition 99
   ("contains") to condition 4 ("string is") before Phase 15 began, which is what let this todo's
   own step-3 concern about combined `"…+Mirror"` entries become moot: exact matching cannot
   partially match a combined entry the way "contains" could.
4. **Rebuild and re-verify.** Delivered by plan **15-05** (this plan): provenance gate, both
   builders, gate A on both forks, re-sign under exact display names, `artifacts/shortcuts/MANIFEST.md`
   re-derived from the signed files, `docs/manifest_check.py` closed (deliberately red since
   wave 1, closed here by re-signing, never by row editing).
5. **Add a build guard** (Config entry with no matching dispatch branch). Already closed by
   **Phase 11** (plan 11-02) — `verify_dispatch_coverage()`, armed in both builders, plus
   `docs/sequence_dispatch_check.py` as a standalone hard gate with `KNOWN_ORPHANS = {}`.

**Residue carried forward, by name — not silently dropped.** Closing this todo does **not** mean
Circle 8 fires audibly on a phone. The Mirror primitive both `mirror()` and `voice()` are built on
carries a **separate, still-open** device-reproduced defect — the axis-4 unfilled-required-picker
failure, tracked in its own todo,
`.planning/todos/pending/2026-08-18-mirror-primitive-unfilled-picker.md`, which this phase's own
plan 15-02 (spike 011) attempted to discriminate at rung 2 and could not (verdict:
`not discriminated at rung 2`, routed to Branch B, no fix attempted). That todo **remains
pending**; CIRC-08 is recorded device-unproven in `docs/BUILD-NOTES.md` §36 and in
`artifacts/shortcuts/MANIFEST.md`'s plan-15-05 block. Full record:
`docs/BUILD-NOTES.md` §36, `.planning/phases/15-circle-8-the-voice-primitive/15-UAT.md`.
