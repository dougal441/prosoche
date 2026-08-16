# Spike Conventions

Patterns and stack choices established across spike sessions. New spikes follow these
unless the question requires otherwise.

## Stack

PROSOCHĒ spikes are Shortcuts plists, built via the `shortcuts-playground:shortcut-builder`
agent (build → validate → sign → archive lifecycle), not code. No package manager, no
scripts — the deliverable is a signed `.shortcut` a human runs on a real iPhone.

## Structure

Each spike directory (`.planning/spikes/NNN-name/`) holds: the signed `.shortcut`, the
unsigned `drafts/*.xml`, a timestamped archive copy, and `README.md`. Delegate the actual
build to the `shortcut-builder` agent in the background — write the README's frontmatter
and "What This Validates"/"How to Run"/"What to Expect" sections yourself before
delegating, so the spike's intent is pinned down independent of the build.

## Patterns

- **Toolchain correction:** `--target-macos 26 --target-platform ios` (the invocation
  documented in this project's `CLAUDE.md` §1) is currently vacuous in Shortcuts
  Playground v1.2.1 and rejects every shortcut (empty allowlist, verified against a
  control golden shortcut). Use both of these and require both to pass:
  `--target-macos 26` and `--target-macos 27 --target-platform ios`. The second is the
  only mode that loads the v78 enum-case catalog and can catch an invalid picker literal.
- **Enum-case catalog lookup gotcha:** `data/toolkit-v78-first-party-enum-cases.json`
  nests entries one level under a top-level `types` key. A top-level sweep finds nothing
  and produces a false "undocumented" conclusion — always descend into `types` before
  concluding a picker's cases aren't catalogued.
- **Device ground truth beats guessing, every time.** Decrypt a real donor `.shortcut`
  (AEA1 round-trip, CLAUDE.md §8) before guessing any parameter literal. When no donor
  exists, check the enum-case catalog before shipping a guessed literal — spike 001 found
  the complete correct answer this way with zero device round trips, after two of three
  guessed literals turned out wrong.
- **No try/catch exists anywhere in Shortcuts.** An action failure halts the entire
  shortcut; nothing after it runs. Any safety design for a potentially-failing action
  (e.g. `Use Model` on hardware that may not support it) must use **ordering**, not
  detection or recovery: place the non-negotiable core logic before the risky optional
  step, so a failure there costs only the optional step, never the core behavior. Confirmed
  in spike 002 both in the shipped plist bytes and on real ineligible hardware.
- **`WFFileErrorIfNotFound = false`** on Get File is the real "does this file exist"
  mechanism — cleaner than attempt-and-treat-as-absent.
- **State-dictionary presence check:** gate on whether `Detect Dictionary`'s output itself
  `has any value` (condition code `100`), never on reading a specific key — a dotted read
  hard-errors when any segment is missing, so a read-then-gate on a dotted path is
  unimplementable.
- **Save File triggers a one-time OS permission prompt** ("Allow to save 1 dictionary to a
  file") on first write per installation. Expected UX, not a bug.

## Tools & Libraries

- `shortcuts-playground:shortcut-builder` agent for all build work — handles the Craig
  Loop internally.
- AEA1 decrypt round-trip (`aea decrypt` + `aa extract`, CLAUDE.md §8) for reading donor
  or previously-signed shortcuts.
