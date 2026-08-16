---
spike: 005
name: ios-color-filters-identifier
type: standard
validates: "Given the unanalysed donor `.planning/debug/Set Colour Filters.shortcut`, when decrypted via the AEA1 round-trip, then the real iOS 26 Color Filters action identifier and its parameter serialization are established as device ground truth"
verdict: VALIDATED
related: [001, 003]
tags: [capability-audit, evidence-hierarchy, accessibility, ash, donor, intentdefinition]
---

# Spike 005: iOS Color Filters Identifier (Donor "Set Colour Filters")

## What This Validates

**Given** the donor `.planning/debug/Set Colour Filters.shortcut` — exported from the
owner's iPhone and never opened — **when** decrypted and inspected, **then** establish
whether a Color Filters action exists on iOS 26 at all, under what identifier, and with
what parameter shape.

Driven by `.planning/phases/999.3-grayscale-ash-capability-donor-test/2026-08-16-grayscale-ash-capability-donor-test.md`
(step 1: "Decrypt the donor already on disk").

## Research

No external research was needed — this spike is answered entirely from two local evidence
sources, both above the ToolKit catalog in this project's evidence hierarchy:

| Source | Tier | What it settles |
|---|---|---|
| `.planning/debug/Set Colour Filters.shortcut`, decrypted | 1 — device ground truth | The identifier the device actually emits, and its serialization |
| `/System/Library/PrivateFrameworks/AccessibilityUtilities.framework/…/Intents.intentdefinition` | Apple's own schema | Parameter types, enum cases and their integer indices, response parameters |
| Bundled ToolKit snapshots (v63 / v78 / v78-ios27) | 3 — catalog | Confirms the AX identifier is absent from **all three** — a genuine catalog gap |

The Playground's own `APPINTENTS.md` (line 116) already documents the general pattern:
`AccessibilityUtilities.framework` defines private `AX*Intent` variants carrying
`operation` and `state`, paralleling the public macOS `UA*Intent` ToolKit rows — and its
own rule is "do not author … until an exported shortcut or a device ToolKit database
confirms the `WFWorkflowActionIdentifier` and parameter serialization." This donor is
exactly that exported shortcut.

## How to Run

```bash
signed=".planning/debug/Set Colour Filters.shortcut"
dir="$(mktemp -d)"
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed" "$dir/leaf.der"
openssl x509 -inform DER -in "$dir/leaf.der" -noout -pubkey > "$dir/pub.pem"
aea decrypt -i "$signed" -o "$dir/payload.aa" -sign-pub "$dir/pub.pem"
mkdir -p "$dir/unwrapped" && aa extract -i "$dir/payload.aa" -d "$dir/unwrapped"
plutil -convert xml1 -o "$dir/Shortcut.xml" "$dir/unwrapped/Shortcut.wflow"
```

Then, for the schema:

```bash
plutil -convert xml1 -o /tmp/ax.xml /System/Library/PrivateFrameworks/AccessibilityUtilities.framework/Versions/A/Resources/Base.lproj/Intents.intentdefinition
```

Archived outputs: `SetColourFilters-Shortcut.xml`, `AXToggleColorFilters-intentdefinition.txt`.

## What to Expect

A single-action plist. Either it contains a Color Filters identifier (settling CAP-20 as
available on iOS), or it does not (closing CAP-20 as confirmed-by-donor).

## Results

### VALIDATED — Color Filters exists on iOS 26, under a different identifier than the audit trail records

The donor's entire action list is one action:

```xml
<key>WFWorkflowActionIdentifier</key>
<string>com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent</string>
<key>WFWorkflowActionParameters</key>
<dict>
    <key>UUID</key><string>05477FE4-67CE-42DD-8421-44EE444E3CE8</string>
    <key>state</key><integer>1</integer>
</dict>
```

`WFWorkflowClientVersion` is `4711`; `WFWorkflowMinimumClientVersion` is `900`.

### Finding 1 — the iOS identifier is `AX*`, not `UA*`

| Platform | Identifier |
|---|---|
| macOS (ToolKit v63 + v78) | `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` |
| **iOS 26 (this donor)** | **`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`** |

The AX identifier is absent from **all three** bundled snapshots — `toolkit-v63-tool-ids.json`
(1794 ids), `toolkit-v78-tool-ids.json` (2731), `toolkit-v78-ios27-tool-ids.json` (1206).
The container prefix mirrors the macOS one exactly (`AXSettingsShortcuts` ↔
`UASettingsShortcuts`), so the whole 29-strong `UAToggle*` accessibility family very likely
has an `AXToggle*` iOS twin — but only Color Filters is donor-confirmed here.

### Finding 2 — parameters are **integers**, not enum id strings and not bools

From Apple's `Intents.intentdefinition` for intent `ToggleColorFilters` (class prefix `AX`):

| Parameter | Type | Enum | Cases |
|---|---|---|---|
| `operation` | Integer | `Operation` | `unknown` = 0, `turn` = **1**, `toggle` = **2** |
| `state` | Integer | `State` | `unknown` = 0, `on` = **1**, `off` = **2** |

So the donor's `state = 1` is **On** — established, not inferred. To turn Color Filters
**off**, `state = 2` (not `0`, and not `<false/>`).

The donor omits `operation` entirely — Shortcuts elides unset/default parameters — proving
a `state`-only invocation is what the device writes and runs.

There is **no `ShowWhenRun` parameter** on the iOS intent. It exists only on the macOS
`UAToggleColorFiltersIntent` catalog row.

### Finding 3 — the intent declares a `state` **response** parameter

```
INIntentResponseParameters:
  state: type=Integer enumType=State displayName="State"
```

All 24 `Toggle*` intents in the framework declare the same. This is a *new* option for
§21 read-back that BD-01/BD-01-R did not have: the action returns the resulting state as
an output, so a `operation = toggle` probe would reveal the prior state by inversion, and
a follow-up `turn` could restore it — at the cost of one visible flicker.

**This is not established as usable.** The intentdefinition declares the response; whether
Shortcuts surfaces it as a consumable action output on iOS is unverified, and it is a
*post*-operation read, not a non-destructive pre-read. Recorded as the next donor test,
not as a capability.

### Finding 4 — a factual error in the audit trail

`docs/BUILD-NOTES.md` CAP-20 states the `operation` enum has "no case list found in
`toolkit-v78-first-party-enum-cases.json`." The case list **is** there, under the file's
top-level `types` key (`com_apple_universal_access_uasettings_shortcuts_operation` →
`turn` / `toggle`). This is precisely the lookup gotcha `CONVENTIONS.md` already documents.
BD-01-R's `turn`/`toggle` literals were therefore correctly sourced; CAP-20's parenthetical
is the stale claim.

## Investigation Trail

1. **Located the donor.** No file named "Donor 9" exists anywhere on disk or in any repo
   document — the donor sequence runs 3, 4, 4.1, 5, 6, 6.1, 7, 7.1, 8, **10**, with
   `Set Colour Filters.shortcut` occupying the gap by timestamp (15:57, alongside donors
   3–8; Donor 10 is 19:04). Treated it as the artifact under test.
2. **Decrypted it.** AEA1 round-trip per `.claude/CLAUDE.md` §8 — clean, 70-line plist,
   one action.
3. **Hit the identifier mismatch.** The emitted identifier was neither the one CAP-20
   ruled out nor the one BD-01-R reinstated. Checked all three ToolKit snapshots: absent
   from every one.
4. **Found the pattern already documented.** Grepped the Playground docs for
   `AccessibilityUtilities` — `APPINTENTS.md` line 116 already describes the private
   `AX*Intent` / public `UA*Intent` split for two sibling accessibility toggles, and
   states the exact rule this donor satisfies.
5. **Went to Apple's schema rather than inferring what `state: 1` meant.** The
   framework's own `Intents.intentdefinition` is on this Mac; it gave the integer indices
   directly, turning "1 probably means On" into a fact and yielding `off = 2` (not the
   `0` a bool intuition would suggest).
6. **Swept all 35 intents for a read-back.** No `Get*`/`Query*` intent exists for any
   accessibility setting — confirming §21's core problem stands. But the sweep surfaced
   the `state` *response* parameter on all 24 `Toggle*` intents, which is a genuinely new
   angle (Finding 3).
7. **Re-checked the enum-cases file properly** before accusing BD-01-R of a guessed
   literal — descending into `types` showed its `turn`/`toggle` values are sound, and that
   CAP-20's "no case list found" note is the error instead.

## Impact on the Audit Trail

BD-01-R's **conclusion** — Ash is a real, restorable environmental primitive on iOS — is
confirmed, and is now backed by device ground truth rather than by simulator-artefact
reasoning plus owner assertion.

BD-01-R's **build recipe is wrong in three ways** and would not have produced a working
Ash if Phase 5 had built it verbatim:

| BD-01-R says | Donor + Apple schema say |
|---|---|
| `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` |
| `operation = turn` (string), `state = On` (bool) | integers — `operation = 1`, `state = 1` (on) / `2` (off) |
| set `ShowWhenRun = Off` | no such parameter on the iOS intent |

Superseded by **BD-01-R2** in `docs/CAPABILITY-DECISIONS.md`; CAP-20 updated in
`docs/BUILD-NOTES.md`.

## Open Questions (next donor)

1. **Confirm the OFF write.** The donor only proves the ON serialization. A second donor
   built as "Turn Color Filters Off" would confirm `state = 2` and whether `operation` is
   still elided.
2. **Is the `state` response consumable?** A donor with Set Color Filters → Show Result
   (its output) would establish whether the response parameter surfaces as a magic
   variable — and therefore whether the toggle-probe read-back of Finding 3 is buildable.
