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
