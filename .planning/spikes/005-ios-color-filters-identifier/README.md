---
spike: 005
name: ios-color-filters-identifier
type: standard
validates: "Given the Color Filters donors in `.planning/debug/` (Set Colour Filters, Donor 9, Donor 9.1), when decrypted via the AEA1 round-trip, then the real iOS 26 Color Filters action identifier and the exact serialization of both its apply and restore legs are established as device ground truth"
verdict: VALIDATED
related: [001, 003]
tags: [capability-audit, evidence-hierarchy, accessibility, ash, donor, intentdefinition]
---

# Spike 005: iOS Color Filters Identifier and Serialization

## What This Validates

**Given** the Color Filters donors in `.planning/debug/` — exported from the owner's iPhone —
**when** decrypted and inspected, **then** establish whether a Color Filters action exists on
iOS 26 at all, under what identifier, and the exact serialization of both the **apply** and
**restore** legs Ash needs.

Started from `Set Colour Filters.shortcut`, which had sat unopened in `.planning/debug/`.
`Donor 9` and `Donor 9.1` were built to order during the spike, each one correcting a
conclusion the previous pass had drawn from schema rather than from a device.

Driven by `.planning/phases/999.3-grayscale-ash-capability-donor-test/2026-08-16-grayscale-ash-capability-donor-test.md`
(step 1: "Decrypt the donor already on disk").

## Research

No external research was needed — this spike is answered entirely from local evidence:

| Source | Tier | What it settles | Where it misled |
|---|---|---|---|
| Three decrypted donors (`Set Colour Filters`, `Donor 9`, `Donor 9.1`) | 1 — device ground truth | The identifier, and the exact serialization of On, Off, and Toggle | — |
| `/System/Library/PrivateFrameworks/AccessibilityUtilities.framework/…/Intents.intentdefinition` | Apple's own schema | Parameter *names*, the `turn`/`toggle` case ids, the response parameter, and that no read-back intent exists | Its declared `Integer` types and `on`=1/`off`=2 case indices are **not** the plist encoding — see Finding 2 |
| Bundled ToolKit snapshots (v63 / v78 / v78-ios27) | 3 — catalog | The AX identifier is absent from **all three** — a genuine catalog gap | Its `state: bool` typing was **right**, and closer to the truth than the schema |

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

Repeat for `Donor 9.shortcut` and `Donor 9.1.shortcut`.

Archived outputs: `SetColourFilters-Shortcut.xml`, `Donor9-Shortcut.xml`,
`Donor9.1-Shortcut.xml`, `AXToggleColorFilters-intentdefinition.txt`.

## What to Expect

Small plists, one to two actions each. Either they contain a Color Filters identifier
(settling CAP-20 as available on iOS), or they do not (closing CAP-20 as confirmed-by-donor).
If present, the parameter values across the On / Off / Toggle donors pin the serialization.

## Results

### VALIDATED — Color Filters exists on iOS 26, under a different identifier than the audit trail records, and both legs of Ash are now donor-confirmed

The first donor's entire action list is one action:

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

### Finding 2 — `state` is a **bool-as-integer** (`0` = Off, `1` = On); `operation` is a string and should be omitted

This finding was rewritten twice as donors arrived. Both revisions mattered, and the second
one caught a value that would have shipped a broken restore.

**Donor evidence, all three artifacts:**

| Donor | Serialized parameters | Built in the UI as |
|---|---|---|
| `Set Colour Filters.shortcut` | `state` `<integer>1</integer>` | Turn Color Filters **On** |
| `Donor 9.shortcut` action 1 | `operation` `<string>toggle</string>`, `state` `<integer>1</integer>` | **Toggle** Color Filters |
| `Donor 9.shortcut` action 2 | *(none)* | untouched default |
| `Donor 9.1.shortcut` | `state` `<integer>0</integer>` | Turn Color Filters **Off** |

Donor 9.1 carries the same `UUID` as Donor 9's action 2 — it is that untouched action, set to
Off. So the pairing is exact and the reading is unambiguous.

**Final shapes:**

| Parameter | Serialized as | Values | Donor-confirmed |
|---|---|---|---|
| `state` | integer, **boolean-valued** | **`0` = Off, `1` = On** | both ✓ |
| `operation` | **string** (enum case id) | `toggle` when explicitly chosen; **elided when Turn** | `"toggle"` ✓, elision ✓ |

**`off` is `0`, not `2`.** The intentdefinition's `State` enum lists `unknown`, `on`=1,
`off`=2 — and Shortcuts does **not** use those indices. It renders a `State`-typed enum as an
On/Off switch and writes a plain boolean as an integer. This is exactly what the macOS ToolKit
catalog was saying all along when it typed `state` as `typePythonName: bool` with trueString
`On` / falseString `Off`; the catalog was right and the enum indices were a red herring.

Writing `state = 2` for Off — which this spike asserted from Apple's schema before Donor 9.1
existed — would have been a live bug on the **restore** leg, the leg whose failure leaves a
user stuck in grayscale. It was caught only because the donor was requested rather than
inferred.

**`operation` should simply be omitted.** Both a "Turn On" and a "Turn Off" configuration
serialize with no `operation` key at all; the key appears only when the user picks `toggle`.
So `turn` is the elided default, and PROSOCHĒ never needs to write the `"turn"` literal — the
one literal in this whole investigation that no donor has ever emitted. Omitting it is both
the donor-verified shape *and* the shape that avoids an unconfirmed string.

**Corrected rule for `INEnumType`:** `Regular` → picker, serializes its **case id string**;
`State` → On/Off switch, serializes a **boolean as `0`/`1`** — *not* the enum's declared case
index. The intentdefinition's `Integer` storage type predicts neither.

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
8. **A second donor arrived and corrected me.** `Donor 9.shortcut` landed after the first
   pass had been written and committed. It carries `operation` as the **string** `"toggle"`,
   not an integer — so my step-5 reading of the intentdefinition (both parameters are
   `Integer`, therefore both serialize as integers) was wrong, and BD-01-R's original
   `operation = turn` string was right on that point.
9. **A third donor corrected me again, on the value that actually mattered.** `Donor 9.1`
   is Donor 9's untouched action set to **Off** — same UUID — and it writes
   `state` `<integer>0</integer>`. So `state` is a plain **bool-as-integer**, and the
   intentdefinition's `on`=1 / `off`=2 case indices are not the serialization at all. My
   asserted `state = 2` for the restore leg was wrong and would have shipped a bug that
   leaves a user stuck in grayscale.

   The pattern across steps 5, 8 and 9 is one mistake made three times: treating Apple's
   `.intentdefinition` as top-tier evidence. It is genuinely valuable — it named the
   parameters and the `turn`/`toggle` cases correctly — but it describes the *intent's*
   type system, not what Shortcuts writes to the plist. The macOS ToolKit catalog, which
   typed `state` as a plain `bool`, was closer to the truth than the schema was, and the
   donor was closer still. The evidence hierarchy in `.claude/CLAUDE.md` already says this;
   I ranked a new source above a donor because it was precise, and precision is not rank.

## Impact on the Audit Trail

BD-01-R's **conclusion** — Ash is a real, restorable environmental primitive on iOS — is
confirmed, and is now backed by device ground truth rather than by simulator-artefact
reasoning plus owner assertion.

BD-01-R's **build recipe is wrong in three ways** and would not have produced a working
Ash if Phase 5 had built it verbatim:

| BD-01-R says | Donors say |
|---|---|
| `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent` | `com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent` |
| `operation = turn` (string) | right in shape, but **omit it** — `turn` is the elided default and no donor ever emits that literal |
| `state = On` (bool) | right that it is a bool — serialized as an integer, `1` = On, `0` = Off |
| set `ShowWhenRun = Off` | no such parameter on the iOS intent |

**BD-01-R got exactly one thing wrong: the identifier.** Its parameter model — `operation` a
string, `state` a bool — was correct, and this spike's two intermediate "corrections" of it
were both wrong. The only substantive change to its Design section is the identifier, plus
dropping `ShowWhenRun` and preferring omission of `operation`.

Superseded by **BD-01-R2** in `docs/CAPABILITY-DECISIONS.md`; CAP-20 updated in
`docs/BUILD-NOTES.md`.

## Open Questions (next donor)

**Closed by Donor 9.1:** the OFF write. Both legs Ash needs are now donor-confirmed —
`state = 1` to apply, `state = 0` to restore, `operation` omitted in both. Nothing in
CIRC-02's write path rests on inference any more.

**Still open — one question, and it is optional:**

1. **Is the `state` response consumable?** A donor wiring Set Color Filters → Show Result
   (its output) would establish whether the response parameter surfaces as a magic variable,
   and therefore whether the toggle-probe read-back of Finding 3 is buildable. This would
   only *improve* §21 compliance — it would let Ash detect and preserve a user's
   pre-existing filter rather than requiring them to opt out. Ash ships without it under
   BD-01-R2's opt-in guard, so this is an enhancement, not a gate.
