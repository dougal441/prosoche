# Evidence and Probes

How to settle an open question about Shortcuts at the lowest cost that actually settles it.

## Requirements

- **Device ground truth beats guessing, every time.** Decrypt a real donor before guessing
  any parameter literal.
- **Never climb the evidence ladder higher than the open question requires, and never skip a
  rung that would have caught a defect in the probe itself.** Both halves bite.
- A probe's result is **recorded, not consumed** — into `docs/BUILD-NOTES.md` and
  `docs/CAPABILITY-DECISIONS.md`. Probes are cheap to build and expensive to re-run.

## How to Build It

### The evidence hierarchy

When sources disagree, prefer in this order:

1. **User-built donor shortcuts, decrypted** — device ground truth from the target iPhone
2. **Apple's own `.intentdefinition` files** on the build Mac — for *what parameters exist*
   and *what a picker's cases are called*, never for the plist encoding
3. **The golden-shortcut corpus** — 19 real-world shipped plists
4. **The ToolKit catalog** — incomplete; carries no required/optional bit, and omits the
   control-flow identifiers entirely
5. **Inference** — last resort, and record it as a deviation

### The evidence-escalation ladder

| Rung | Channel | Settles | Costs |
|---|---|---|---|
| 1 | File-level analysis — validator, catalog, golden corpus, decrypted plist | Structure, identifier presence, parameter shape | Nothing |
| 2 | Simulator — build, sign, **import, run and observe** | The file is well-formed and signable; import success; editor render; runtime control flow | Agent time |
| 3 | Device probe over iPhone Mirroring | Real-hardware behaviour the simulator cannot reach | One connected session |
| 4 | User-run probe or donor export | Anything mirroring cannot reach | The user's time — the scarcest input |

**Rung 2 reaches the editor and the runtime — measured by spike
`010-coercion-at-a-direct-set-parameter`, 2026-08-18.** An earlier revision of this table
said the opposite, on spike 007's evidence: *"the booted simulator cannot import a signed
`.shortcut` through any channel… rung 2 tests the build, not the import."* **That claim is
RETIRED.** `.claude/CLAUDE.md` §9's original rung-2 row was right all along.

```bash
open -a Simulator                                        # a simctl-booted sim has NO window until this
xcrun simctl openurl <udid> "file:///abs/path.shortcut"  # → the Shortcuts import sheet
# then ONE synthesized tap on "Add Shortcut" completes the import
```

Spike 007 tried five channels and generalised from five failures. Its `file://` row —
*"blocked by the tool's scheme allowlist"* — was measured against the **MCP simulator tool's**
allowlist, **not** against `simctl`, which it never tried. The other four rows stand, and are
worth keeping so nobody re-walks them:

| channel | result | status |
|---|---|---|
| `xcrun simctl openurl "file:///…"` **+ one synthesized tap** | **Import sheet renders; the tap completes the import** | ✅ **the working channel** |
| `shortcuts://import-shortcut?url=…` | "Import Failed — The shortcut URL provided was invalid." Requires an iCloud link; re-measured 2026-08-18 with a `file://` URL and `silent=true` — still rejected, because the URL is refused before the flag is consulted | ✗ still true |
| Safari → download the served file | Prompt names the file correctly, but the Download button ignores synthesized taps | ✗ still true |
| Files "On My iPhone" (`group.com.apple.FileProvider.LocalStorage`) | File lands on disk; Files never surfaces the location | ✗ still true |
| iCloud Drive | Needs an Apple Account | ✗ still true |

**Two mechanics that are invisible until you hit them.** Coordinates must be **fractions of the
device screen mapped through the window rect measured at run time**, never pixels — the window
moves. And **`Show Alert` modals accept neither a synthesized tap nor a hardware Return**: the
run wedges permanently at the first one, while ordinary in-app UI (buttons, list scrolling) takes
taps normally. **Build simulator-bound probes with no blocking UI** and let a clean completion or
an error dialog be the signal. Instrument, with every dead end recorded:
`.planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/sim_input.py`.

**What rung 2 still cannot close, sharpened by the same spike.** `Set Brightness` **cannot
succeed on a simulator at all** ("There was a problem setting the brightness"), and
`Get Device Details → Current Brightness` reads **`0`** there — so brightness/volume *consumption*
stays device-gated however good the import channel is, and any such reading is **never promotable
above `UNVERIFIED`**. Also measured: the **"coercion chip does not render red" gate does not work
at a direct Set-action parameter** (no operator picker, so coerced and uncoerced render
identically — it remains valid for conditionals only), and **`setbrightness.WFBrightness` is
optional, defaulting to 50%**, so an unresolved operand fails *silently* rather than raising the
unfilled-parameter error. Verify **the value applied**, never merely the absence of an error.

Measured simulator inventory: one runtime, **iOS 26.5 (23F77)**, inside the project's
declared iOS 26.x target. `com.apple.shortcuts` present, `com.apple.mobilenotes` **absent** —
so no Notes behaviour can be exercised there at all. Re-derive with
`xcrun simctl list runtimes`, `list devices available`, `listapps <udid>`.

### Recovering a donor's plist (the AEA1 round-trip)

Signed `.shortcut` files **are** recoverable. `plutil`/`xxd`/`file` see the AEA1 container,
not the plist payload — that is not proof of opacity.

```bash
signed="/absolute/path/to/Signed.shortcut"
dir="$(mktemp -d)"
python3 -c 'import struct,plistlib,pathlib,sys; d=pathlib.Path(sys.argv[1]).read_bytes(); sz=struct.unpack_from("<I",d,8)[0]; pathlib.Path(sys.argv[2]).write_bytes(plistlib.loads(d[12:12+sz])["SigningCertificateChain"][0])' "$signed" "$dir/leaf.der"
openssl x509 -inform DER -in "$dir/leaf.der" -noout -pubkey > "$dir/pub.pem"
aea decrypt -i "$signed" -o "$dir/payload.aa" -sign-pub "$dir/pub.pem"
mkdir -p "$dir/unwrapped" && aa extract -i "$dir/payload.aa" -d "$dir/unwrapped"
plutil -convert xml1 -o "$dir/Shortcut.xml" "$dir/unwrapped/Shortcut.wflow"
```

All 16 donors in `.planning/debug/` decrypt cleanly with this, zero failures.
`shortcut-remixer` refuses a signed `.shortcut` directly — give it the recovered XML.

### Reading Apple's own schema

For any `com.apple.*` AppIntent action, on the build Mac:

```bash
plutil -convert xml1 -o /tmp/ax.xml \
  /System/Library/PrivateFrameworks/<Framework>.framework/Versions/A/Resources/Base.lproj/Intents.intentdefinition
```

Read `INIntents` / `INEnums`. It gives exact parameter names, types, enum cases, integer
indices, and response parameters — for actions absent from every bundled snapshot. Read the
caveat in `authoring-parameters.md` before trusting any value from it.

### Sweeping the corpus for a parameter class

`sources/006-picker-serialisation-taxonomy/sweep.py` walks every action's parameter tree
across a donor directory and the golden corpus, flagging bare UUIDs outside structural
slots, URI-shaped identifiers, app-identity fields, and binary/base64 blobs:

```bash
python3 sweep.py <donor-xml-dir> <golden-xml-dir>
```

### Building and validating a probe

```bash
R="$HOME/.claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1"
"$R/bin/validate-shortcut" --target-macos 26 --target-platform all "Probe.xml"  # gate A: generic v63 baseline
"$R/bin/validate-shortcut" --target-macos 27 --target-platform all "Probe.xml"  # gate B: loads the v78 enum catalog
"$R/bin/sign-shortcut" "Probe.xml" --mode anyone --output-dir "<spike-dir>"
```

This is the project's **two-gate rule**, stated in full in `.claude/CLAUDE.md` §1
`### Exact validator invocation`; measurements in `docs/BUILD-NOTES.md` §22.

**Only gate A must pass** (`Validation passed.`, exit 0). **Gate B is advisory and cannot
exit 0** — it carries a permanent one-line waiver per fork (`WFCreateNoteInput` on
`com.apple.mobilenotes.SharingExtension`, device-donor ground truth that outranks the
`macOS 27`-tagged catalog entry). Expect that one line; treat anything else gate B reports
as a real finding. Do not read gate B's nonzero exit as a build failure, and never chain it
into a definition of done.

Gate B is still the valuable one — it is the only mode that loads the enum-case catalog and
can catch an invalid picker literal. It uses `--target-platform all`, **not** `ios`: the
`ios` setting excludes every `macOS 27`-tagged catalog entry, which drops all four Notes
actions out of parameter-key and enum-case checking (1105 enum-checked identifiers under
`all` versus 455 under `ios`) and adds five spurious identifier rejections.

Note the signer's argument form: positional input, `--output-dir`, **not** `--input/--output`.

## What to Avoid

- **Do not use `--target-macos 26 --target-platform ios`.** In Playground v1.2.1 that pair
  is degenerate — it rejects every action including `is.workflow.actions.comment`, because
  `toolkit-v63` is macOS-labelled (filtered out by `ios`) and the only iOS snapshot is
  version-gated to 27 (filtered out by `26`), leaving an empty allowlist. Verified against a
  control golden shortcut: 7 identical false rejections. A check that fails 100% of its
  inputs carries zero signal.
- **Do not treat a validator pass as done.** A valid XML draft without a signed `.shortcut`
  is not a useful stopping point.
- **Do not hand the user an untested probe.** A probe that fails on import, or fails for a
  reason unrelated to the question it was built to answer, burns a device round trip and
  teaches nothing. Misattributed failures have cost this project multiple cycles.
- **Read the error text, not just the letter.** Three times in one session a correct fix
  looked refuted because the bisection letter was unchanged while the error text had changed
  completely.
- **Any shortcut wired into a Personal Automation must have zero UI** — no Show Result, no
  Show Alert. An automation that displays something interrupts the user on every trigger.
  Log to a Note instead.
- **Do not spend a device session on a rung-1 question.** Spike 003 found the complete
  correct answer from the enum-cases catalog with zero device round trips, after two of three
  guessed literals turned out wrong.
- **Do not keep climbing when the question dissolves.** Spike 007 stopped mid-probe once a
  five-line check of `tools/build_state_engine.py` showed the question was off the critical
  path. That is the correct outcome, not a failure.

## Constraints

- The build Mac cannot execute Shortcuts. Signing is macOS-only and cannot be done on
  Linux/CI without a Mac in the loop.
- Personal Automation triggers (App Is Opened / Is Closed) are user-created on the device and
  **cannot be exercised on a simulator at any effort**.
- Apple Intelligence is unavailable on the simulator — the Sentient `Use Model` path needs
  rung 3+.
- Known signer quirks, both auto-retried by `sign-shortcut`: `Error: The file doesn't exist.`
  for a file that does exist (retry from a clean copy); `Error: … isn't in the correct
  format.` even when `validate-shortcut` and `plutil -lint` both pass (retry after
  `plutil -convert binary1`).
- The signed output filename must equal the intended display name — no `_signed` suffix.
- **Breadcrumb bisection**: flag-gated alerts at control-flow base depth localise a failure to
  one span per device run. Keep them in across cycles — a second defect then reports as a
  *later letter* rather than an ambiguous repeat.

## Origin

Synthesized from spikes: 002, 003, 005, 007
Source files: `sources/002-close-automation-vs-screen-lock/`, `sources/003-device-model-literal/`,
`sources/005-ios-color-filters-identifier/`, `sources/007-unresolvable-picker-failure-mode/`
