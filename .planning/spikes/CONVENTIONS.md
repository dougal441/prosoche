# Spike Conventions

Patterns and stack choices established across spike sessions. New spikes follow these
unless the question requires otherwise.

## Stack

PROSOCHĒ spikes are iOS Shortcuts (`.shortcut` files), authored and signed via the
Shortcuts Playground toolchain (`.claude/CLAUDE.md`), not code. There is no runnable app
stack in the usual sense and no package manager — "running" a spike means importing a
signed `.shortcut` onto a real iPhone and exercising it there. The build Mac cannot
execute Shortcuts itself.

## Structure

- Each spike directory (`.planning/spikes/NNN-name/`) holds: `README.md` (frontmatter +
  findings), the signed `.shortcut` artifact when the spike produces one, the unsigned
  editable `.xml` source (in `drafts/`), and a timestamped archive copy.
- Delegate the actual build to the `shortcut-builder` agent in the background — write the
  README's frontmatter and "What This Validates"/"How to Run"/"What to Expect" sections
  yourself before delegating, so the spike's intent is pinned down independent of the
  build.
- Diagnostic/probe shortcuts built for a spike are named descriptively (e.g. "Lock Signal
  Probe", "Device Probe") and kept fully standalone — no dependency on the production
  PROSOCHĒ shortcut or its `state.json`, unless the spike is specifically about that
  state file.
- When a spike's evidence is a decrypted donor `.shortcut` (from `.planning/debug/`), the
  recovered XML is archived in the spike folder for reference.

## Patterns

- **Building the probe:** dispatch the `shortcuts-playground:shortcut-builder` agent
  rather than authoring plist XML by hand — it owns the full build→validate→sign loop and
  already carries this project's wiring-pitfall knowledge (`.claude/CLAUDE.md`
  "seven parameter-defect axes").
- **Toolchain correction — validator invocation:** `--target-macos 26 --target-platform ios`
  (the invocation documented in this project's `CLAUDE.md` §1) is currently vacuous in
  Shortcuts Playground v1.2.1 and rejects every shortcut — `toolkit-v63` is macOS-labelled
  (filtered out by `ios`), and the only iOS snapshot is version-gated to 27 (filtered out
  by `26`), leaving an empty allowlist. Verified against a control golden shortcut (7
  identical false-rejection errors). **Use both of these and require both to pass:**
  `--target-macos 26` (generic v63 baseline) and `--target-macos 27 --target-platform ios`
  (the only mode that loads the v78 enum-case catalog and can catch an invalid picker
  literal — this is the valuable one, not just a fallback).
- **Enum-case catalog lookup gotcha:** `data/toolkit-v78-first-party-enum-cases.json`
  nests entries one level under a top-level `types` key. A top-level sweep finds nothing
  and produces a false "undocumented" conclusion — always descend into `types` before
  concluding a picker's cases aren't catalogued.
- **Device ground truth beats guessing, every time.** Decrypt a real donor `.shortcut`
  (AEA1 round-trip, CLAUDE.md §8) before guessing any parameter literal. When no donor
  exists, check the enum-case catalog before shipping a guessed literal — spike 003 found
  the complete correct answer this way with zero device round trips, after two of three
  guessed literals turned out wrong.
- **Verifying a device-behavior question:** decrypting/inspecting a plist only answers
  *structural* questions (does an action/parameter exist). *Behavioral* questions (does an
  automation trigger fire under condition X, does a Use Model failure halt gracefully)
  require a real on-device log and a human checkpoint — these spikes stay PENDING until
  the user reports back what the device shows, per this project's own evidence hierarchy
  (donor/device ground truth outranks catalog or inference).
- **No try/catch exists anywhere in Shortcuts.** An action failure halts the entire
  shortcut; nothing after it runs. Any safety design for a potentially-failing action
  (e.g. `Use Model` on hardware that may not support it) must use **ordering**, not
  detection or recovery: place the non-negotiable core logic before the risky optional
  step, so a failure there costs only the optional step, never the core behavior. Confirmed
  in spike 004 both in the shipped plist bytes and on real ineligible hardware.
- **`WFFileErrorIfNotFound = false`** on Get File is the real "does this file exist"
  mechanism — cleaner than attempt-and-treat-as-absent.
- **State-dictionary presence check:** gate on whether `Detect Dictionary`'s output itself
  `has any value` (condition code `100`), never on reading a specific key — a dotted read
  hard-errors when any segment is missing, so a read-then-gate on a dotted path is
  unimplementable.
- **Save File triggers a one-time OS permission prompt** ("Allow to save 1 dictionary to a
  file") on first write per installation. Expected UX, not a bug — but note it can also
  re-prompt on every automation run and cannot be granted while the screen is locked (see
  spike 002's spun-out todo).
- **A catalog miss is not an absence — check the identifier *family* before concluding.**
  iOS ships private `AX*Intent` twins of the public macOS `UA*Intent` accessibility actions,
  under container `com.apple.AccessibilityUtilities.AXSettingsShortcuts` mirroring
  `com.apple.UniversalAccess.UASettingsShortcuts`. The `AX*` identifiers are in **none** of
  the three bundled ToolKit snapshots, so no catalog query over those files can find them at
  any target setting. Spike 005 found this after two prior decisions had argued the
  availability question using the macOS identifier without noticing iOS emits a different
  one. When a capability "doesn't exist" but users demonstrably do it on their phones, the
  identifier is the thing to doubt.
- **Apple's own `.intentdefinition` files are a first-class evidence source on the build
  Mac** — between donor ground truth and the ToolKit catalog in the hierarchy. For any
  `com.apple.*` AppIntent action, look for
  `/System/Library/PrivateFrameworks/<Framework>.framework/Versions/A/Resources/Base.lproj/Intents.intentdefinition`,
  `plutil -convert xml1` it, and read `INIntents` / `INEnums` directly. It gives exact
  parameter names, types, enum cases **and their integer indices**, and response parameters —
  for actions absent from every bundled snapshot. This is how spike 005 turned "the donor
  wrote `state = 1`, which probably means On" into a fact, and recovered `off = 2`.
- **An `.intentdefinition` does not describe the plist encoding — only a donor does.** It
  declares the intent's *type system*: parameter names, enum case ids, response parameters.
  Shortcuts then serializes through its own UI rendering, and the two do not match. Spike 005
  got this wrong twice in a row: it read the declared `Integer` storage type as the encoding
  (wrong — `operation` writes a case-id **string**), then read the `State` enum's case indices
  as the values (wrong — `on`=1/`off`=2 in the schema, but Shortcuts renders a `State` enum as
  an On/Off switch and writes a plain **bool as `0`/`1`**). The second error would have
  shipped a broken restore leg. **Use `.intentdefinition` to learn what parameters exist and
  what a picker's cases are called; use a donor to learn what gets written.**
- **A picker enum serializes its case-id string; an On/Off switch serializes `0`/`1`.** That
  is the working rule for `AXToggle*`-family actions, established across three donors.
- **Parameter absence often means "left at default" — and the default may be the value you
  want.** Both the On and Off Color Filters donors omit `operation` entirely, because `turn`
  is its default. Omitting a parameter is therefore sometimes *better* than authoring it: it
  matches the device byte-for-byte and avoids committing to an unconfirmed literal. But
  absence is not proof of a default value either — Donor 9 contains a fully parameter-less
  instance of an action another donor writes with `state` set. Read absence across several
  donors before concluding anything from it.
- **Classify a parameter before authoring it — the three-class rule.** Look up its
  `typePythonName` in `toolkit-v78-first-party-parameter-keys.json`:
  a **primitive** (`str`/`bool`/`float`/`int`/`DateTime`/`File`/`URL`) is always writable;
  a **`*_parameter`** enum is writable if catalogued in `toolkit-v78-first-party-enum-cases.json`
  (525 of 526 are), else it needs a donor or an `.intentdefinition`;
  a **`*_entity`** is writable *only via a runtime variable*, and only if its family has a
  `filter.*` query action. The 14 queryable families are `apps articles calendarevents
  contacts displays eventattendees files images locations music notes photos reminders
  windows`. An entity family outside that list (Home, Focus, Safari tabs, Mail, Wallet,
  Podcasts) genuinely cannot be authored offline — it must be hand-picked on the device and
  exported. Run this check before adopting any new action.
- **Never write an entity identifier — find the entity at runtime.** Donor 8 is the
  reference pattern: `filter.notes` with a plain string predicate (`Name` contains, operator
  `99`) produces a `Note` output, and `shownote`/`appendnote` consume it as an ordinary
  `WFTextTokenAttachment`. No identifier appears in the plist at all. The generators already
  do this (`entity=variable("Control Room Note")`); keep it that way.
- **The booted simulator cannot import a signed `.shortcut`.** Measured 2026-08-17 on
  iPhone 17 Pro / iOS 26.5: `shortcuts://import-shortcut?url=…` rejects a plain HTTP URL
  ("The shortcut URL provided was invalid" — it wants an iCloud link); the Files app never
  surfaces "On My iPhone" even with files seeded into
  `group.com.apple.FileProvider.LocalStorage` and a SpringBoard respring; Safari's download
  banner does not respond to synthesized taps; iCloud Drive needs an Apple Account.
  **Rung 2 therefore tests the *build* (validator, signer, byte shape), not the *import*.**
  This narrows `.claude/CLAUDE.md` §9, which currently lists "import success" as rung-2.
  Signing the simulator into an Apple Account would likely unlock it — a user decision.
- **Silent automation probes:** any shortcut wired into a Personal Automation must have
  zero UI (no Show Result/Show Alert) — an automation that displays something interrupts
  the user on every trigger. Log to a Note instead.

## Tools & Libraries

- `shortcuts-playground:shortcut-builder` agent for all build work — handles the Craig
  Loop internally.
- `aea decrypt` + `aa extract` (per `.claude/CLAUDE.md` §8) to recover plist XML from any
  signed `.shortcut`, including donor artifacts and this project's own probe outputs.
