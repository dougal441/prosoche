# iPhone import probes

Open these on the iPhone in order. Record only whether Shortcuts imports each file; you do not need to run it.

| Probe | Isolated payload | Result |
|---|---|---|
| 1 — Baseline | Signing and shared workflow metadata only | ☐ imports ☐ unsupported |
| 2 — Open App | Bare-string Notes app selection from the rejected builds | ☐ imports ☐ unsupported |
| 3 — Notes Intent | Create Note AppIntent descriptor from the rejected builds | ☐ imports ☐ unsupported |
| 4 — Round Mode | `Down` round-mode value from the rejected builds | ☐ imports ☐ unsupported |

Interpretation:

- If probe 1 fails, the candidate probes are not yet meaningful; investigate signing or root metadata.
- If probe 1 imports and probe 2, 3, or 4 fails, that probe's isolated payload is a confirmed importer blocker.
- More than one failed candidate means the original shortcuts contain multiple blockers.
- If all four import, the blocker is elsewhere in the shared action graph.

Probe 3 creates a note only if run. Probe 2 opens Notes only if run.
