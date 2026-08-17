# Environmental Primitives

Ash (Color Filters), Dimming (brightness) and Silence (volume) — the interventions that change the device's state and must restore it.

## Requirements

- **Every environmental change must be captured before it is applied and reliably restored.**
  Capture-and-restore reliability *is* the safety mechanism — not avoidance of the extreme.
- No unsafe or startling volume. No accessibility-stranding state. Emergency Restore always
  available.
- Where no read-back exists, the remedy is the **opt-in guard**
  (`safety.ash_managed_color_filters`), not inference.

## How to Build It

### Ash — Color Filters, both legs donor-confirmed

**The iOS identifier is `AX*`, not the `UA*` the audit trail argued over for two decisions:**

| Platform | Identifier |
|---|---|
| macOS (ToolKit v63 + v78) | `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` |
| **iOS 26 (donor)** | **`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`** |

The `AX*` identifier is absent from **all three** bundled ToolKit snapshots, so no catalog
query could ever have found it at any target setting.

**Apply leg** (`sources/005-.../SetColourFilters-Shortcut.xml`):

```xml
<key>WFWorkflowActionIdentifier</key>
<string>com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent</string>
<key>WFWorkflowActionParameters</key>
<dict>
    <key>UUID</key><string>…</string>
    <key>state</key><integer>1</integer>
</dict>
```

**Restore leg** — identical, with `<integer>0</integer>` (`sources/005-.../Donor9.1-Shortcut.xml`).

| Parameter | Serialized as | Values | Donor-confirmed |
|---|---|---|---|
| `state` | integer, **boolean-valued** | `0` = Off, `1` = On | both legs ✓ |
| `operation` | **string** (enum case id) | `"toggle"` when explicitly chosen; **omit entirely for Turn** | `"toggle"` ✓, elision ✓ |

**Omit `operation`.** Both the On and Off donors carry no `operation` key at all — `turn` is
the elided default. Omitting is both the donor-verified shape *and* the shape that avoids
committing to a literal no donor has ever emitted.

There is **no `ShowWhenRun`** parameter on the iOS intent; it exists only on the macOS row.

Donor 9.1 carries the **same `UUID`** as Donor 9's untouched second action, so the On/Off
pairing is exact and the reading is unambiguous.

### The corrected rule for `INEnumType`

- `Regular` → picker, serializes its **case-id string**
- `State` → rendered as an On/Off switch, serializes a **boolean as `0`/`1`** — *not* the
  enum's declared case index

The `.intentdefinition`'s `Integer` storage type predicts neither.

### Dimming and Silence

- `is.workflow.actions.setbrightness` — `WFBrightness` (float). Confirmed on **both**
  `["iOS 27 Simulator","macOS 27"]` — the one system-control action with confirmed iOS *and*
  macOS provenance. Also exercised on Donor 10.
- `is.workflow.actions.setvolume` — exercised on Donor 10, including a call targeting
  `Ringtone` at `0.796875`.
- Read-back for both: `is.workflow.actions.getdevicedetails` with `Current Brightness` /
  `Current Volume`, both **donor-confirmed** on Donor 10 (spike 001) — these were previously
  catalog-only (CAP-17/CAP-19) and are now tier-1.

**The brightness floor was corrected** (Phase 9, experimental fork, 2026-08-16): iOS's
practical minimum is dim, not a literal black screen, per on-device report. The relaxed floor
is **provisional** until Phase 9 proves the capture/restore loop holds under real failure
modes — force-quit, restart, missed CLOSE, overlapping sessions. Main line unaffected.

## What to Avoid

- **Do not write `state = 2` for Off.** The `.intentdefinition`'s `State` enum lists
  `unknown`, `on`=1, `off`=2 — and Shortcuts does **not** use those indices. Spike 005
  asserted `state = 2` from the schema before Donor 9.1 existed; it would have shipped a
  restore leg that leaves users stuck in grayscale. The macOS ToolKit catalog, which typed
  `state` as a plain `bool` with trueString `On` / falseString `Off`, was right all along,
  and the enum indices were a red herring.
- **Do not use `BD-01-R`'s build recipe verbatim.** It is wrong in three ways — the
  identifier, `ShowWhenRun` (does not exist), and writing `operation = turn` (should be
  omitted). Superseded by **BD-01-R2**. Note that BD-01-R's *parameter model* was correct;
  spike 005's two intermediate "corrections" of it were both wrong.
- **Do not perform a stateful environmental change you cannot reliably restore.** Where the
  original condition cannot be detected and restored safely, skip the primitive and record
  the deviation.

## Constraints

- **There is still no read-back for any accessibility setting.** No `Get*`/`Query*` intent
  exists across all 35 intents in `AccessibilityUtilities.framework`. §21's opt-in remedy
  (`safety.ash_managed_color_filters`) governs, unchanged.
- **One untested lead:** every `Toggle*` intent (all 24 of them) declares a `state`
  **response** parameter — so an `operation = toggle` probe would reveal the prior state by
  inversion, and a follow-up `turn` could restore it, at the cost of one visible flicker.
  Whether Shortcuts surfaces that response as a consumable output on iOS is **unverified**,
  and it is a *post*-operation read, not a non-destructive pre-read. This is the next donor
  test, not a capability. Ash ships without it; it would only *improve* §21 compliance.
- The whole 29-strong macOS `UAToggle*` accessibility family very likely has `AXToggle*` iOS
  twins, but **only Color Filters is donor-confirmed**. Do not assume the rest.
- `docs/BUILD-NOTES.md` CAP-20's claim that the `operation` enum has "no case list found" is
  **stale** — the list is there, under the file's top-level `types` key
  (`com_apple_universal_access_uasettings_shortcuts_operation` → `turn` / `toggle`).

## Origin

Synthesized from spikes: 001, 005
Source files: `sources/001-device-is-locked-literal/`, `sources/005-ios-color-filters-identifier/`
