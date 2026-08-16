---
spike: 001
name: device-is-locked-literal
type: standard
validates: "Given Donor 10's decrypted plist, when inspected for WFDeviceDetail, then the literal \"Device Is Locked\" is present as donor-confirmed ground truth"
verdict: VALIDATED
related: [002]
tags: [device-details, capability-audit, evidence-hierarchy]
---

# Spike 001: Device Is Locked Literal

## What This Validates

Given the user-built `Donor 10.shortcut` dropped in `.planning/debug/`, when its signed
AEA1 container is decrypted and its actions inspected, then `is.workflow.actions.getdevicedetails`
(Get Device Details) is present with `WFDeviceDetail = "Device Is Locked"` as a real,
device-authored literal — not an inferred or catalog-only value.

## Research

Prior state (`docs/BUILD-NOTES.md` CAP-17/CAP-19, `docs/CAPABILITY-DECISIONS.md` §CAP-17):
`Current Brightness` and `Current Volume` were promoted to `VERIFIED` by directly querying
`toolkit-v78-first-party-enum-cases.json` for the `getdevicedetails_wfdevice_detail` enum
type, which returned a 12-case list including `Device Is Locked` alongside the two cases
that were actually acted on. That query already surfaced `Device Is Locked` as a
*catalog-tier* fact — it was never separately promoted to a CAP row or exploited, because
no capability audit item at the time needed it.

Per this project's evidence hierarchy (`.claude/CLAUDE.md` "Evidence hierarchy"), donor
shortcuts decrypted from the target iPhone outrank the ToolKit catalog. `Donor 10.shortcut`
closes that gap for this specific literal.

## How to Run

```bash
signed_shortcut=".planning/debug/Donor 10.shortcut"
inspection_dir=$(mktemp -d)
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed_shortcut" "$inspection_dir/leaf.der"
openssl x509 -inform DER -in "$inspection_dir/leaf.der" -noout -pubkey > "$inspection_dir/pub.pem"
aea decrypt -i "$signed_shortcut" -o "$inspection_dir/payload.aa" -sign-pub "$inspection_dir/pub.pem"
mkdir -p "$inspection_dir/unwrapped"
aa extract -i "$inspection_dir/payload.aa" -d "$inspection_dir/unwrapped"
plutil -convert xml1 -o "$inspection_dir/Shortcut.xml" "$inspection_dir/unwrapped/Shortcut.wflow"
grep -A2 'WFDeviceDetail' "$inspection_dir/Shortcut.xml"
```

## What to Expect

Six `is.workflow.actions.getdevicedetails` actions, each with a distinct `WFDeviceDetail`
string parameter. The recovered plist is archived alongside this README as
`Donor10-Shortcut.xml`.

## Results

**Verdict: VALIDATED.**

Donor 10 is a device-authored settings-probe shortcut (also exercising
`is.workflow.actions.setbrightness` and two `is.workflow.actions.setvolume` calls — one
targeting `Ringtone` at `0.796875`). It contains six `Get Device Details` reads, each a
separate action instance with its own `WFDeviceDetail` literal:

| WFDeviceDetail literal | Prior status |
|---|---|
| `Device Model` | new — not previously exploited by any CAP row |
| `Current Brightness` | already `VERIFIED` (CAP-17) — now doubly confirmed by donor evidence |
| `Current Volume` | already `VERIFIED` (CAP-19) — now doubly confirmed by donor evidence |
| `Current Appearance` | new — not previously exploited by any CAP row |
| `Device Is Locked` | **new — promoted from catalog-only to donor-confirmed** |

**Consequence for the project:** `Device Is Locked` can now be cited as donor-shortcut
ground truth (tier 1 of the evidence hierarchy) wherever it's used, e.g. as a defensive
guard in future debugging cycles — checking screen-lock state at any point in the
OPEN/CLOSE pipeline without depending on Personal Automation trigger semantics. This is
exactly the kind of "invisible until the next failure" fact the project's seven
parameter-defect axes exist to catch — it was sitting in the enum-cases catalog the whole
time (§CAP-17 research) but nobody had cause to act on it until now.

**No new risk surfaced.** `Get Device Details` is a single-parameter, zero-wiring-hazard
action (no `WFTextTokenString`/`WFTextTokenAttachment` distinction applies to its own
input; only to what consumes its output downstream). The action identifier and this exact
enum case are unchanged from the already-`VERIFIED` CAP-17/CAP-19 rows — same action,
same enum type, different literal.

**This spike does not resolve** whether `Device Is Locked` reads accurately *during* an
automation's brief execution window (a locked screen and a running Shortcuts automation
are not mutually exclusive states — background automations can execute while the screen
is locked). That behavioral question belongs to Spike 002, not this one.
