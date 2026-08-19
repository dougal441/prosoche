#!/usr/bin/env python3
"""Gate A's waiver, made EXECUTABLE: the residue must equal exactly what is enumerated here.

**What this check exists to prove.**  That the mandatory validator gate reports the two
permitted line families for ONE named identifier and NOTHING ELSE, on BOTH forks.  Gate A is
the identifier / availability baseline at this project's real iOS 26.x target -- the gate
every plan, todo and `docs/*.py` checker names.  It is the only thing standing between an
unknown identifier, a missing parameter key or an availability failure and a shipped
artifact, so its waiver may never be a thing somebody REMEMBERS.  A remembered waiver widens
one reading at a time until the gate certifies nothing.  This file is that waiver in code.

**Why gate A can never exit zero again.**  Phase 14 ships
`com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent`, and that
identifier is absent from ALL THREE bundled ToolKit snapshots (v63, v78, v78-ios27).  The
validator offers no allowlist, no ignore flag, no waiver file, no environment override, and
its data path resolves relative to its own script OUTSIDE this repository -- all measured,
not assumed.  So the report is permanently non-empty and the old obligation ("clean report,
exit zero") became permanently unsatisfiable the moment the action shipped.  `.claude/CLAUDE.md`
sec 1 `### Exact validator invocation` records the amended obligation; this script is the
executable form of it, and a plan satisfies gate A by RUNNING THIS, never by chaining the raw
validator command into an `&&` success condition.

**The identifier is device-donor-established, not inferred.**  Three shortcuts exported from
the owner's iPhone and decrypted through the AEA1 round trip pin every value the build emits.
Two records carry that evidence and are the authority here:

  * `docs/BUILD-NOTES.md` sec 4, the CAP-20 capability row (verdict VERIFIED, donor-confirmed)
  * `docs/CAPABILITY-DECISIONS.md` BD-01-R2 (supersedes BD-01-R, which supersedes BD-01)

The catalog's silence is a GENUINE CATALOG GAP, matching the `AX*`-private / `UA*`-public
split the Playground's own `APPINTENTS.md` documents for sibling accessibility toggles.  A
tool that lacks a fact does not overrule the evidence that has it.

**The rejected alternatives, and why each is worse than a red gate.**

  1. **Synthesise an `AppIntentDescriptor`.**  It does not even work -- the unknown-identifier
     family is emitted independently of the descriptor family -- and it would fabricate three
     field values no donor supplies.  Forbidden by decision D-14-01.
  2. **Vendor or patch the plugin's bundled ToolKit snapshot.**  There is no override path,
     the file lives outside this repository, and the edit is lost on the next plugin update.
     A gate that depends on a mutated copy of its own reference data is not a gate.

  A third, not offered as an alternative but named because it is the CHEAPEST-LOOKING and the
  MOST DAMAGING: substituting the macOS twin
  `com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent`.  It is in the
  catalog, so it turns the gate green -- by shipping an action that does NOTHING on an iPhone.
  A green check that certifies nothing is strictly worse than a red one that certifies the
  truth.  `CLASSIFIER_MUST_NOT_PERMIT` below proves this file rejects it.

**If this check fires, investigate the new line.**  Never widen the waiver to accommodate it,
never synthesise a descriptor, never patch the catalog, and never substitute the macOS twin.
A residue that SHRANK is equally a finding: it means emitted sites disappeared, which would
otherwise present as good news.

Shells out to the validator -- deliberately, because the validator's verdict IS the subject.
It writes nothing and rebuilds nothing.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Both forks, by their real filenames.  The Core fork ships as PROSOCHE-Dumb.xml and the Aware
# fork as PROSOCHE-Sentient.xml; the source filenames predate the Dumb -> Core / Sentient ->
# Aware rename (BUILD-NOTES sec 25) and were deliberately not moved.  Module-level so a
# negative control can point the check at a scratch copy without editing this file.
FORK_SOURCES: dict[str, Path] = {
    "Core (src/PROSOCHE-Dumb.xml)": ROOT / "src/PROSOCHE-Dumb.xml",
    "Aware (src/PROSOCHE-Sentient.xml)": ROOT / "src/PROSOCHE-Sentient.xml",
}

# Gate A, exactly as `.claude/CLAUDE.md` sec 1 states it.  `--target-macos` is the controlling
# variable; pairing the iOS platform flag with target 26 admits NO snapshot at all and rejects
# 3675 of 3675 actions, so `all` is not a preference here, it is the only non-degenerate value.
GATE_A_FLAGS = ("--target-macos", "26", "--target-platform", "all")

VALIDATOR = "validate-shortcut"
PLUGIN_FALLBACK = Path.home() / (
    ".claude/plugins/cache/shortcuts-playground/shortcuts-playground/1.2.1/bin/validate-shortcut"
)

# The ONE identifier the waiver is scoped to, by its full string.  Scoping by name is what
# keeps the amendment narrow: every OTHER unknown identifier, every missing parameter key and
# every availability failure still fails this check exactly as gate A always did.
AX_COLOR_FILTERS = (
    "com.apple.AccessibilityUtilities.AXSettingsShortcuts.AXToggleColorFiltersIntent"
)

# The macOS twin.  Never emitted, never waived -- named here so the classifier's negative
# control can prove that swapping it in does NOT buy a green run.
UA_COLOR_FILTERS_MACOS_TWIN = (
    "com.apple.UniversalAccess.UASettingsShortcuts.UAToggleColorFiltersIntent"
)

# BOTH line families, because a descriptor-less action emits BOTH per instance and D-14-01
# forbids synthesising a descriptor.  A one-family waiver would be permanently unsatisfiable
# -- the exact outcome the decision exists to prevent.  Each pattern demands the full
# identifier string, so a line naming any other identifier cannot match either family.
FAMILIES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "Unknown AppIntent identifier",
        re.compile(r"^Unknown AppIntent identifier at index \d+: " + re.escape(AX_COLOR_FILTERS) + r"$"),
    ),
    (
        "AppIntent action missing AppIntentDescriptor",
        re.compile(
            r"^AppIntent action missing AppIntentDescriptor at index \d+: "
            + re.escape(AX_COLOR_FILTERS)
            + r"$"
        ),
    ),
)

# ---------------------------------------------------------------------------------------
# THE PERMITTED COUNT -- DERIVED FROM THE EMITTED SITE CENSUS, NOT CHOSEN.
#
#   AX_SITES_PER_FORK = 15
#     = 11 renderings of primitive_dispatch() emitting the ON leg (state = 1)
#         -- nine Test-a-Circle submenu cases plus two in universal_leaving()
#     + 4 call sites of restore_managed_settings() emitting the OFF leg (state = 0)
#         -- close_pipeline(), manual_emergency_restore(), ice_expiry(), live_ice_redirect()
#   Derived from the built artifact with plistlib in plan 14-01; the same 15 is pinned
#   independently by docs/environmental_restore_check.py's EXPECTED_SITES and by
#   docs/phase5_self_check.py's EXPECTED_COLOR_FILTER_SITES.
#
#   EXPECTED_PERMITTED_LINES = 15 sites x 2 families = 30 lines per fork.
#
# ASSERTED IN BOTH DIRECTIONS.  A residue LARGER than this means something new is wrong.  A
# residue SMALLER than this means emitted sites DISAPPEARED -- the failure mode a one-sided
# check would miss entirely, and the one that would otherwise read as good news.  Do NOT
# relax this constant to accept fewer lines; if the census legitimately moves, move the
# census comment above with it and say why.
# ---------------------------------------------------------------------------------------
AX_SITES_PER_FORK = 15
EXPECTED_PERMITTED_LINES = AX_SITES_PER_FORK * len(FAMILIES)

# ---------------------------------------------------------------------------------------
# CLASSIFIER CONTROL -- run on EVERY invocation, because a guard that cannot fail is this
# project's top defect class and a waiver that silently widened would look exactly like a
# passing run.  MUST-PERMIT rows are the two real families verbatim.  MUST-NOT-PERMIT rows
# are the near misses that a careless widening would admit: the macOS twin, an unrelated
# unknown identifier, a different validator finding on the SAME identifier, and a line that
# merely mentions the identifier in passing.
# ---------------------------------------------------------------------------------------
CLASSIFIER_MUST_PERMIT: tuple[str, ...] = (
    f"Unknown AppIntent identifier at index 176: {AX_COLOR_FILTERS}",
    f"AppIntent action missing AppIntentDescriptor at index 4168: {AX_COLOR_FILTERS}",
)

CLASSIFIER_MUST_NOT_PERMIT: tuple[str, ...] = (
    f"Unknown AppIntent identifier at index 176: {UA_COLOR_FILTERS_MACOS_TWIN}",
    f"AppIntent action missing AppIntentDescriptor at index 176: {UA_COLOR_FILTERS_MACOS_TWIN}",
    "Unknown AppIntent identifier at index 12: com.apple.some.other.MadeUpIntent",
    f"Unknown AppIntent parameter key(s) for {AX_COLOR_FILTERS} at index 176: operation.",
    f"Action at index 176 requires macOS 27+: {AX_COLOR_FILTERS}",
    f"Unknown AppIntent identifier at index 176: {AX_COLOR_FILTERS} (and one more)",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def classify(line: str) -> str | None:
    """The family a reported line belongs to, or None if it is a real finding."""
    for family, pattern in FAMILIES:
        if pattern.match(line):
            return family
    return None


def classifier_control() -> int:
    """Prove the classifier still catches the real families and still rejects near misses."""
    for line in CLASSIFIER_MUST_PERMIT:
        require(
            classify(line) is not None,
            f"the classifier no longer recognises a REAL waived line: {line!r}. The waiver "
            f"has drifted from what the validator actually emits and this check is now "
            f"decoration -- every run would report the whole residue as findings",
        )
    for line in CLASSIFIER_MUST_NOT_PERMIT:
        require(
            classify(line) is None,
            f"the classifier PERMITS a line it must never permit: {line!r}. A waiver broad "
            f"enough to swallow this is a waiver that certifies nothing -- it would admit "
            f"the {UA_COLOR_FILTERS_MACOS_TWIN} macOS twin, an unrelated unknown identifier, "
            f"or a different finding on the same identifier",
        )
    return len(CLASSIFIER_MUST_PERMIT) + len(CLASSIFIER_MUST_NOT_PERMIT)


def locate_validator() -> str:
    """The validator, or an explicit failure.

    A checker that silently passes when its subject could not be examined is the
    false-reassurance class this repository has already paid for.  An absent or unrunnable
    validator is a FAILURE here, never a skip and never a pass.
    """
    found = shutil.which(VALIDATOR)
    if found:
        return found
    if PLUGIN_FALLBACK.is_file():
        return str(PLUGIN_FALLBACK)
    raise AssertionError(
        f"{VALIDATOR!r} is not on PATH and the Shortcuts Playground fallback "
        f"{PLUGIN_FALLBACK} does not exist, so gate A could not be run at all. This is a "
        f"FAILURE, not a skip: the residue was never examined, so nothing about it is known"
    )


def run_gate_a(validator: str, source: Path) -> tuple[int, str]:
    """Gate A on one fork: (exit status, combined report)."""
    require(source.is_file(), f"{source} does not exist, so gate A has nothing to validate")
    try:
        completed = subprocess.run(
            [validator, str(source), *GATE_A_FLAGS],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise AssertionError(
            f"gate A could not be run against {source.name}: {error!r}. The residue was "
            f"never examined -- treat this as a failure, never as a pass"
        ) from error
    return completed.returncode, completed.stdout + completed.stderr


def reported_lines(report: str) -> list[str]:
    """Every finding the validator reported, stripped of its `- ` bullet."""
    return [line[2:].strip() for line in report.splitlines() if line.startswith("- ")]


def check_fork(validator: str, label: str, source: Path) -> dict[str, int]:
    status, report = run_gate_a(validator, source)

    require(
        status != 0,
        f"{label}: gate A exited 0 -- the residue is EMPTY. Either the bundled ToolKit "
        f"snapshot has gained {AX_COLOR_FILTERS} (in which case this whole waiver is "
        f"retired and this file should be deleted, deliberately and with a record), or the "
        f"AX Color Filters action stopped being emitted. Both are findings. Investigate "
        f"before touching this check",
    )

    findings = reported_lines(report)
    require(
        findings,
        f"{label}: gate A exited {status} but reported no parseable `- ` finding lines. The "
        f"validator's report format may have changed, which would make every classification "
        f"below vacuous. Raw report:\n{report}",
    )

    per_family: dict[str, int] = {family: 0 for family, _ in FAMILIES}
    unexpected: list[str] = []
    for line in findings:
        family = classify(line)
        if family is None:
            unexpected.append(line)
        else:
            per_family[family] += 1

    require(
        not unexpected,
        f"{label}: gate A reported {len(unexpected)} line(s) OUTSIDE the enumerated waiver. "
        f"Each one is a real finding and must be investigated -- never waived, never "
        f"'fixed' by substituting {UA_COLOR_FILTERS_MACOS_TWIN}:\n"
        + "\n".join(f"    {line}" for line in unexpected),
    )

    total = sum(per_family.values())
    require(
        total == EXPECTED_PERMITTED_LINES,
        f"{label}: the permitted residue is {total} line(s), expected exactly "
        f"{EXPECTED_PERMITTED_LINES} ({AX_SITES_PER_FORK} emitted AX sites x {len(FAMILIES)} "
        f"line families). Per family: "
        + ", ".join(f"{name}={count}" for name, count in per_family.items())
        + (
            ". A SMALLER residue means emitted AX sites DISAPPEARED -- colour may no longer "
            "be applied at a Circle, or restored at a recovery path, and this is why the "
            "count is asserted in both directions. Do NOT relax this check to accept fewer "
            "lines."
            if total < EXPECTED_PERMITTED_LINES
            else ". A LARGER residue means something new is being reported. Investigate the "
            "extra lines; do NOT widen the waiver."
        ),
    )

    for family, count in per_family.items():
        require(
            count == AX_SITES_PER_FORK,
            f"{label}: family {family!r} contributed {count} line(s), expected "
            f"{AX_SITES_PER_FORK} (one per emitted AX site). The two families must move "
            f"together -- a descriptor-less action emits both per instance, so a split "
            f"count means either the emitted census moved or the validator changed",
        )

    return per_family


def main() -> None:
    controlled = classifier_control()
    validator = locate_validator()
    totals: list[str] = []
    for label, source in FORK_SOURCES.items():
        per_family = check_fork(validator, label, source)
        totals.append(f"{label}: {sum(per_family.values())} permitted")
    print(
        "gate A residue check: passed -- residue equals exactly the enumerated waiver on "
        f"{len(FORK_SOURCES)} fork(s) ({'; '.join(totals)}); "
        f"{len(FAMILIES)} line families scoped to {AX_COLOR_FILTERS}; "
        f"{controlled} classifier control rows. Gate A exits 1 by construction -- that is "
        "the expected result, and this script, not the raw validator command, is the "
        "gate-A obligation."
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"gate A residue check: FAILED -- {error}", file=sys.stderr)
        raise SystemExit(1)
