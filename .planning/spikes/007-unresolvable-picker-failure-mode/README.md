---
spike: 007
name: unresolvable-picker-failure-mode
type: standard
validates: "Given a shortcut authored offline whose picker value we cannot know, when imported and run, then determine whether it fails at import, fails at run, or silently renders empty — and whether the bare bundle identifier alone is sufficient"
verdict: VALIDATED
related: [006, 009]
tags: [capability-audit, pickers, openapp, simulator, rung-2, probe]
---

# Spike 007: Unresolvable Picker Failure Mode

## What This Validates

**Given** a shortcut authored offline whose picker value we cannot know, **when** imported
and run, **then** determine whether it fails at import, fails at run, or silently renders
empty — and whether `WFAppIdentifier` alone is sufficient without `WFSelectedApp`.

Spike 006 established that `WFSelectedApp` is Class A (synthesizable) **for first-party
apps**, where `TeamIdentifier` is always the literal `0000000000`. All six `Open App`
donors are first-party, so the third-party case was unproven — and PROSOCHĒ's tracked
apps are third-party by definition.

## How to Run

`App Picker Probe.shortcut` (signed, in this folder; unsigned source in `drafts/`) holds
five `Open App` actions with descending knowledge of the target:

| leg | app | descriptor | tests |
|---|---|---|---|
| A | Calendar | complete, donor-exact | control |
| B | Reminders | **omitted entirely** | is the descriptor load-bearing? |
| C | Contacts | correct bundle id, **wrong name + nonsense team id** | does the editor trust it or re-resolve? |
| D | Instagram (not installed) | omitted | PROSOCHĒ's real target class |
| E | TikTok (not installed) | **fabricated**, placeholder team id | separates "not installed" from "descriptor unknown" |

Import it and inspect how each leg renders in the editor. Do **not** run it — the
question is authoring-time resolution, not launch behaviour.

## Investigation Trail

**Built and signed successfully.** The probe passes both validator invocations required by
CONVENTIONS.md — `--target-macos 26` and `--target-macos 27 --target-platform ios` — and
signs to a 23,166-byte artifact.

*Deviation from CONVENTIONS.md, recorded:* authored the plist directly rather than
dispatching the `shortcut-builder` agent. Justification — the probe is five `Open App`
actions whose exact byte shape is already given by `Donor - apps`; copying donor bytes is
strictly safer here than having an agent re-derive them, and the probe's whole purpose is
to vary that shape deliberately. An agent would likely have "corrected" the fabricated
values that are the entire point.

**Installation into the simulator failed on every channel tried.** This is the finding
that stopped the spike, and it is worth recording precisely:

| channel | result |
|---|---|
| `shortcuts://import-shortcut?url=http://127.0.0.1:8777/…` | **"Import Failed — The shortcut URL provided was invalid."** The scheme requires an iCloud shortcut link; an arbitrary HTTP URL is rejected. |
| Safari → download the served file | Download prompt appears and correctly names the file, but the **Download button does not respond to synthesized taps**. Other taps in the same session (dialog OK, Start Page dismiss, tab bar) all registered, so this is specific to the WebKit download banner. |
| Copy into Files "On My iPhone" (`group.com.apple.FileProvider.LocalStorage`) | File lands on disk, but **Files never surfaces an "On My iPhone" location** — the app opens straight into iCloud Drive and the back chevron does not pop to the Browse root. Survived a SpringBoard respring and a seeded subfolder. |
| iCloud Drive | Simulator is **not signed in to iCloud**, so this route needs an Apple Account. |
| `open_url` with a `file://` URL | Blocked by the tool's scheme allowlist. |

**Then the question dissolved.** Rather than keep climbing, checked whether the
third-party case is on PROSOCHĒ's critical path at all. It is not:

`tools/build_state_engine.py:82-96` defines a **closed set of six first-party apps** and
one `open_app()` helper that writes exactly the donor shape:

```python
APPS = {
    "Notes": "com.apple.mobilenotes",      "Voice Memos": "com.apple.VoiceMemos",
    "Camera": "com.apple.camera",          "Reminders": "com.apple.reminders",
    "Calendar": "com.apple.mobilecal",     "Contacts": "com.apple.MobileAddressBook",
}

def open_app(name):
    bundle_identifier = APPS[name]
    return action("is.workflow.actions.openapp", WFAppIdentifier=bundle_identifier,
                  WFSelectedApp={"BundleIdentifier": bundle_identifier, "Name": name,
                                 "TeamIdentifier": "0000000000"})
```

Those six are **precisely the six apps in `Donor - apps.shortcut`** — which is why that
donor exists. The generator emits a donor-exact shape for every one of them.

**PROSOCHĒ never writes a third-party bundle id into an `Open App` action.** The tracked
apps (Instagram, TikTok, …) are chosen by the user inside the Personal Automation, which
is user-created by design and never appears in any plist we generate.

## Results

**PARTIAL.**

**Settled (rung 1, and it is the part that mattered):** the third-party `WFSelectedApp`
question is **off PROSOCHĒ's critical path**. Every `Open App` the generators emit targets
one of six first-party apps with a donor-confirmed `TeamIdentifier` of `0000000000`.
Spike 006's Class A verdict stands unqualified for PROSOCHĒ's actual usage.

**Not settled:** the general failure mode of an unresolvable picker — whether it breaks at
import, at run, or renders silently empty. The probe that would answer it is built,
validated, signed, and preserved here. It costs nothing to run whenever a device session
is next live, and it is no longer blocking anything.

### The finding worth carrying forward

**The booted simulator cannot import a signed `.shortcut` through any channel tried.**

This contradicts `.claude/CLAUDE.md` §9, which lists **"import success"** as something
rung 2 settles. On this environment — iOS 26.5, iPhone 17 Pro, no iCloud account — it does
not. Every practical import path either needs an iCloud link, needs an Apple Account, or
depends on UI that does not respond to synthesized input.

The consequence for the evidence ladder is real: **rung 2 is narrower than documented.**
It can still settle what a *file* contains and what the *validator and signer* accept, but
"import it and look at it" is a rung-3 activity on this Mac unless someone signs the
simulator into iCloud. CLAUDE.md §9's rung-2 row should be corrected, and the standing
policy "probes are simulator-tested before they reach the user's iPhone" needs the caveat
that the simulator can test the *build*, not the *import*.

Worth one follow-up before accepting that as permanent: signing the simulator into an
Apple Account would likely unlock both the iCloud Drive and `import-shortcut` routes.
That is a user decision, not an agent one.

---

## RESOLVED 2026-08-18 — verdict PARTIAL → VALIDATED

Free-ridden during **spike 010**, which found the import channel this spike concluded did not
exist. The probe preserved here was imported and inspected at zero device cost.

### The import claim above is RETIRED, and the retiring evidence is specific

**`xcrun simctl openurl <udid> "file:///abs/path.shortcut"` renders the Shortcuts import sheet, and
one synthesized tap on "Add Shortcut" completes the import.** Measured on the same environment this
spike used — iPhone 17 Pro, iOS 26.5, still no iCloud account.

The `file://` row in the channel table above reads *"Blocked by the tool's scheme allowlist."* That
was true and it was measured against the **MCP simulator tool's** allowlist — **not** against
`simctl`, which this spike never tried. Every other row stands: `import-shortcut` still rejects a
non-iCloud URL (re-measured 2026-08-18 with a `file://` URL and `silent=true`), Files still never
surfaces "On My iPhone", iCloud Drive still needs an Apple Account.

So the generalisation *"the simulator cannot import a signed `.shortcut` through any channel"* was
too strong: it was drawn from five failures without the sixth channel having been tried. The
narrower true statement is that the **`shortcuts://` scheme** requires an iCloud link — `openurl`
with a plain file URL does not go through that scheme at all. **`.claude/CLAUDE.md` §9's rung-2
row was right and this spike's correction to it was wrong.** Import success IS a rung-2 capability.

Instrument: `.planning/spikes/010-coercion-at-a-direct-set-parameter/drafts/sim_input.py`.

### The five legs, as rendered in the editor

| leg | authored | renders as | reading |
|---|---|---|---|
| **A** | Calendar, donor-exact complete descriptor | **"Open [Calendar]"**, icon and name, normal | control passes — the donor shape resolves |
| **B** | Reminders — **first-party, INSTALLED**, `WFSelectedApp` **omitted** | **"Open [App]"** — an EMPTY placeholder | **the descriptor is load-bearing** |
| **C** | Contacts — correct bundle id, **fabricated** display name + nonsense team id | **"Open [ZZZ WRONG NAME ZZZ]"** with the Contacts icon | the editor **trusts the stored descriptor's Name** and does not re-resolve it from the bundle id |
| **D** | Instagram — third-party, **not installed**, bare identifier | **"Open [App]"** — empty, identical to B | "not installed" and "descriptor absent" are **indistinguishable** in the render |
| **E** | TikTok — third-party, not installed, **fabricated** descriptor with a placeholder team id | **"Open [AirDrop]"** in **RED** | **mis-resolves to a different, real app** |

Screenshots: `leg-A-control-rendered.png`, `legs-B-and-C-rendered.png`, `legs-C-and-D-rendered.png`,
`legs-D-and-E-rendered.png`.

### The answer to the original question

The question was: *does an unresolvable picker fail at import, fail at run, or render silently empty?*

**It renders silently empty — and in the worst case it renders silently WRONG.** Nothing fails at
import. Nothing warns. Legs B and D produce a bare "Open App" that a user would have to notice; leg E
produces a confident, fully-populated chip naming **AirDrop**, an app the author never mentioned.

**Leg E is the finding that matters.** A fabricated descriptor does not degrade toward emptiness — it
**resolves to something else**. That is the silent-wrong-behaviour class this project's do-not-fabricate
rule exists to prevent, now demonstrated end to end rather than argued. It also generalises spike 005's
lesson (`.intentdefinition` declares the type system; only a donor gives the encoding) from parameter
literals to **entity descriptors**: a plausible-looking fabricated descriptor is not a degraded correct
one, it is a *different* one.

**Leg B is the second finding, and it is the one that touches this project's code.** `WFAppIdentifier`
alone is **not** sufficient, even for a first-party app that is installed. Omit `WFSelectedApp` and the
action renders unfilled. Spike 006's Class-A verdict for `Open App` therefore holds **only because the
descriptor is written**, not because the bundle id would have carried it.

**PROSOCHĒ is unaffected, and now for a measured reason rather than an argued one.** `open_app()`
emits the full `WFSelectedApp` triple for all six first-party apps, which is leg A's shape exactly.
Leg C additionally shows the *cost of getting the Name wrong*: the editor would display the wrong name
indefinitely, since it never re-resolves. The generator's hardcoded names must stay correct.

**Still not settled:** launch behaviour. Every observation here is authoring-time render, which is what
the probe was built for ("do not run it — the question is authoring-time resolution"). What legs D and
E do when actually *launched* on a device that lacks those apps is untouched, and is not on PROSOCHĒ's
critical path.
