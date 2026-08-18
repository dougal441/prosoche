#!/usr/bin/env python3
"""Pin the CANCELLED brightness/volume cut, so a re-attempt fails loudly.

Why this file exists, stated plainly so nobody has to reconstruct it from git:

A "ship-readiness" proposal would have CUT the environmental primitives -- deleting
`dimming()`, `silence()`, `restore_managed_settings()`, the `settings_snapshot` subtree and
the `NUMERIC_OPERAND_FIELDS` entries that make the brightness/volume writes actually take a
value.  That cut was **proposed and then CANCELLED by user decision on 2026-08-16, and the
cancellation was reaffirmed on 2026-08-17**.  Dimming and Silence stay, each as its own
distinct Circle, each with a working capture-and-restore loop.

That leaves a hazard with no guard: the machinery is now load-bearing safety code that a
future subtractive pass could remove with nothing anywhere to stop it, and its removal is
invisible to `validate_shortcut.py`, to the plist, and to every other check in `docs/`.
This script is that guard.  It asserts the symbols, both restore call sites, the numeric
coercion table entries, media-only volume scoping, a dim target at or above the configured
brightness floor (relaxed from a stricter test by decision D-01 -- read the note carried at
that assertion) and the bootstrap seed -- so a re-attempt at the cut turns a check red
instead of silently removing
the mechanism that `SAFE-03` (never change a setting whose original cannot be captured) and
`SAFE-05` (Emergency Restore restores recoverable environmental state) depend on.

Governing decisions: `docs/CAPABILITY-DECISIONS.md` **BD-02** (Dimming / brightness
read-back -- stateful capture-and-restore, with a per-run degrade-to-message-only branch)
and **BD-03** (Silence / volume read-back -- the same structure, plus `WFVolumeSetting =
"Media"`, never `"Ringtone"`).  Both are the same canonical-strategy §21 rule applied to
two evidentiary outcomes, and neither authorises a stateful environmental change whose
original value cannot be captured on the run that fires it.

Read-only: this script parses the built artifact with `plistlib` and imports the generator
as a module.  It never shells out and never rebuilds `src/PROSOCHE-Dumb.xml`.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import plistlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"
SENTIENT_BUILDER = ROOT / "tools/build_sentient.py"

# Every generator symbol the cancelled cut would have deleted.  Each must exist and be
# callable; the cut's whole shape was "remove these ten and the table entries below".
REQUIRED_SYMBOLS = (
    "device_detail",              # the Get Device Details read -- BD-02/BD-03's capture path
    "set_brightness",             # the Set Brightness write
    "set_media_volume",           # the Set Volume write, Media-scoped by construction
    "clear_snapshot",             # clears the captured LEAF, never its container
    "restore_managed_settings",   # the restore expansion, SAFE-05 and SESS-07
    "dimming",                    # Circle primitive, capture -> dim
    "silence",                    # Circle primitive, capture -> quieten
    "seed_settings_snapshot",     # establishes the subtree at bootstrap
    "verify_state_seed",          # build guard: every snapshot READ has a seeded counterpart
    "verify_restore_gates",       # build guard: every snapshot-fed write is numerically gated
    # PHASE 16 (16-01): the ordering half of the same safety property.  verify_restore_gates
    # proves a restore never writes a junk value; this proves a capture reaches DISK before
    # the device is changed, so there is something to restore FROM.  Listed here so a future
    # subtractive pass cannot silently delete the guard that makes SAFE-05 effective.
    "verify_capture_persistence",  # build guard: no apply is reachable from an unpersisted capture
    # PHASE 11 (11-08): the third axis of the same safety property, and the one whose absence
    # is INVISIBLE at runtime.  verify_restore_gates proves a restore never writes junk;
    # verify_capture_persistence proves a capture reaches disk before the device changes; this
    # proves the arm holding both can actually be TAKEN.  Delete it and the primitives can
    # silently return to doing nothing at all, with every count in this file still green.
    "verify_environmental_reachability",  # build guard: no environmental action sits in a dead arm
    # PHASE 11 (11-10): the fourth axis, and the only one that is not about the write itself.
    # The three guards above make the environmental change happen correctly; this one keeps the
    # WAY OUT of it reachable.  SAFE-05 -- named in this file's own docstring as one of the two
    # requirements the cancelled cut would have broken -- is Emergency Restore, and it is only
    # a safety mechanism while a user can still reach it.  T-11-22, this phase's only
    # `critical`: a user who removed the removable Panic Escape bypass and finds Emergency
    # Restore gone with it is stranded inside an intervention, on a dimmed screen or a silenced
    # device.  Until 11-08 that state was unreachable because both primitives sat in a dead
    # arm; it is reachable now, which is what turned a latent separation into a live one.
    # Listed here for the same reason as the three above: deleting the guard is invisible at
    # runtime and every count in this file would stay green.
    "verify_panic_escape_isolation",  # build guard: no Panic Escape gate encloses Emergency Restore
)

# PHASE 11 CODE REVIEW (WR-17).  REQUIRED_SYMBOLS above proves each guard is DEFINED and
# callable.  It has never proved that a builder RUNS it, and those are different properties --
# what disarms a guard in this codebase is deleting its CALL, not its definition.  So the
# comments beside the two entries added this phase ("delete it and the primitives can silently
# return to doing nothing at all, with every count in this file still green") described a
# failure this file could not actually see.  Measured 2026-08-18: with
# verify_environmental_reachability(actions) and verify_panic_escape_isolation(actions) deleted
# from main() in BOTH builders and both function definitions left untouched, both builds exited
# 0 and all 13 checkers exited 0.
#
# These five are the guards among REQUIRED_SYMBOLS, and both builders call all five today.  A
# guard listed here must be CALLED, not merely importable; a guard that genuinely cannot apply
# to a fork should be excluded by name with a written reason rather than dropped silently.
CALLED_GUARDS = (
    "verify_state_seed",
    "verify_restore_gates",
    "verify_capture_persistence",
    "verify_environmental_reachability",
    "verify_panic_escape_isolation",
)

SET_BRIGHTNESS = "is.workflow.actions.setbrightness"
SET_VOLUME = "is.workflow.actions.setvolume"
DEVICE_DETAILS = "is.workflow.actions.getdevicedetails"

# Derivation of these three counts, so a future reader can tell a legitimate change from a
# regression rather than re-deriving it or, worse, "fixing" the number:
#   restore_managed_settings() is expanded at FOUR call sites -- close_pipeline(),
#   live_ice_redirect(), ice_expiry() and manual_emergency_restore() -- and each expansion
#   emits exactly one Set Brightness and one Set Volume.            -> 4 + 4
#   primitive_dispatch() is rendered ELEVEN times, and each rendering emits dimming() once
#   and silence() once.  dimming() emits one Set Brightness and one Get Device Details
#   ("Current Brightness"); silence() emits one Set Volume and one Get Device Details
#   ("Current Volume").                                             -> 11 + 11
#   Totals: 15 Set Brightness, 15 Set Volume, 22 Get Device Details.
#
# WHERE THE ELEVEN RENDERINGS ARE, and why the count moved.  Nine are the Test-a-Circle
# submenu in the MANUAL arm, unchanged.  The other TWO are both in universal_leaving(), and
# the second of them is new in PHASE 11 (plan 11-05, Build Addendum 01 §3): Panic Escape --
# the `Leaving` case of the Leaving/Continue menu -- became removable, gated on the flat
# state field `panic_escape_enabled`.  Mechanism A gates the WHOLE menu, so the enabled arm
# renders the dispatch inside the Continue case as before and the otherwise arm renders it
# directly, verbatim.  That preserves verify_circle_zero_silence()'s "exactly one
# Leaving/Continue menu" invariant at the price of one extra rendering, and the otherwise
# arm renders primitive_dispatch() unmodified, so no capture-and-restore gate is skipped on
# the no-bypass path.
#
# MEASURED, not projected.  Before 11-05: 14 / 14 / 20 at ten renderings.  After: 15 / 15 /
# 22, each delta exactly one rendering's worth (+1 Set Brightness, +1 Set Volume, +2 Get
# Device Details -- one per primitive).  11-RESEARCH.md §8.2 projected these same three
# numbers; they were re-measured against the rebuilt artifact rather than transcribed.
#
# A change to the number of restore call sites or to the number of dispatch renderings is a
# legitimate reason for these to move -- but only by exactly what that change explains.  A
# larger delta, or a change caused by deleting dimming() or silence(), is the regression
# this file exists to catch; investigate it rather than editing the table to match.
#
# WHAT THESE THREE NUMBERS DID NOT SAY UNTIL PHASE 11 (plan 11-08), and now do.  A site count
# asserts that an action EXISTS.  For most of this file's life it was silently read as also
# asserting the action can RUN, and for 44 of the sites below that reading was false.
# dimming() and silence() opened on a condition-100 existence gate over the
# settings_snapshot.<group> CONTAINER, with their whole capture-and-apply body in the
# OTHERWISE arm.  clear_snapshot() writes the LEAF and never the container -- deliberately, so
# the seeded subtree stays a permanent invariant -- so that gate could never read false and
# the otherwise arm was dead code.  Measured against the shipped artifact at HEAD e6b96e3:
# 22 Get Device Details + 11 Set Brightness + 11 Set Volume = 44 unreachable actions PER FORK,
# which is EVERY Get Device Details in the artifact and every non-restore environmental write.
# The eight restore-side writes were always fine: restore_managed_settings() opens on the same
# container gate but puts its work in the TRUE arm, and its own numeric leaf gate decides
# inside it.  Polarity, not the gate, was the whole defect.
#
# 11-08 re-gated both capture sites onto settings_snapshot.<group>.original_value with the
# same numeric `> 0` test the restore side already used, so all 44 are now reachable, and
# armed verify_environmental_reachability() in BOTH builders so the dead-arm shape is a build
# failure rather than something this table can certify.
#
# THE NUMBERS BELOW DID NOT MOVE, AND THAT IS THE POINT.  The fix re-gates existing actions
# and emits none, so 15 / 15 / 22 held exactly across it -- re-measured against both rebuilt
# forks, not assumed.  A future reader should read the stillness of these three numbers as the
# evidence that the reachability fix added and removed nothing; if they HAD moved, that would
# have been a finding to investigate rather than a table to update.
#
# STILL NOT ASSERTED HERE, and not by anything else either: that the capture-and-restore loop
# WORKS on a phone.  Reachable is a structural property of the build.  DIST-03 is open, Phase
# 16 owns the device proof, and 16-UAT.md's twelve tests have never run.
EXPECTED_SITES = {SET_BRIGHTNESS: 15, SET_VOLUME: 15, DEVICE_DETAILS: 22}

# The only two device properties this Shortcut is permitted to read.  Anything else is an
# unaudited read of the user's device and is not covered by BD-02/BD-03's evidence.
ALLOWED_DEVICE_DETAILS = {"Current Brightness", "Current Volume"}


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def load_module(name: str, path: Path):
    """Import a generator by spec so assertions can inspect real module attributes.

    Same idiom as docs/phase7_self_check.py.  `tools/` goes on sys.path first because
    build_sentient.py does a plain `from build_state_engine import ...`.
    """
    tools = str(ROOT / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def source_check(builder) -> None:
    """Assertions against the generator module itself."""
    for name in REQUIRED_SYMBOLS:
        require(hasattr(builder, name),
                f"the brightness/volume cut is CANCELLED, but {name}() is gone from "
                f"{BUILDER.name} -- restore it or revert the change that removed it")
        require(callable(getattr(builder, name)),
                f"{name} exists in {BUILDER.name} but is no longer callable")

    # The two NUMERIC_OPERAND_FIELDS entries are the SPECIFIC exemption the cancelled cut
    # would have introduced.  Without them, normalise_numeric_operands() stops attaching the
    # Donor-4.1 WFCoercionVariableAggrandizement to a variable-fed brightness/volume write,
    # the operand goes back to being Text-typed, and the write silently no-ops on device --
    # which is exactly the Phase 9 defect.  Their ABSENCE is the property being pinned.
    fields = getattr(builder, "NUMERIC_OPERAND_FIELDS", None)
    require(isinstance(fields, dict), "NUMERIC_OPERAND_FIELDS is missing or is not a mapping")
    require(SET_BRIGHTNESS in fields,
            f"NUMERIC_OPERAND_FIELDS has no {SET_BRIGHTNESS} entry -- a variable-fed "
            "Set Brightness would lose its numeric coercion and silently no-op")
    require("WFBrightness" in tuple(fields[SET_BRIGHTNESS]),
            f"NUMERIC_OPERAND_FIELDS[{SET_BRIGHTNESS}] no longer names WFBrightness")
    require(SET_VOLUME in fields,
            f"NUMERIC_OPERAND_FIELDS has no {SET_VOLUME} entry -- a variable-fed "
            "Set Volume would lose its numeric coercion and silently no-op")
    require("WFVolume" in tuple(fields[SET_VOLUME]),
            f"NUMERIC_OPERAND_FIELDS[{SET_VOLUME}] no longer names WFVolume")

    # SAFE-05.  Emergency Restore is the user's last resort when a run left the screen dim
    # or the media volume down; the cut would have contradicted this requirement outright.
    manual = inspect.getsource(builder.manual_emergency_restore)
    require("restore_managed_settings" in manual,
            "manual_emergency_restore() no longer calls restore_managed_settings() -- "
            "SAFE-05 requires Emergency Restore to restore recoverable environmental state")

    # SESS-07.  Without this the ordinary owning CLOSE leaves the change outstanding, so a
    # user who simply closes the app stays dimmed or silenced until some later trigger.
    close = inspect.getsource(builder.close_pipeline)
    require("restore_managed_settings" in close,
            "close_pipeline() no longer calls restore_managed_settings() -- SESS-07 "
            "requires the owning CLOSE to restore what the session changed")


def _state_template_string(actions) -> str:
    """The bootstrap state.json template's literal text, located by content not by index."""
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if not isinstance(value, dict):
            continue
        inner = value.get("Value")
        if isinstance(inner, dict) and isinstance(inner.get("string"), str) \
                and '"schema_version"' in inner["string"]:
            return inner["string"]
    raise AssertionError("bootstrap state.json template not found in the artifact")


def _config_literal(actions) -> dict:
    """The Config JSON literal, located by content not by index."""
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if isinstance(value, str) and '"config_version"' in value:
            return json.loads(value)
    raise AssertionError("the Config JSON literal was not found in the artifact")


def artifact_check(actions) -> None:
    """Assertions against the built src/PROSOCHE-Dumb.xml."""
    counts: dict[str, int] = {}
    for item in actions:
        identifier = item.get("WFWorkflowActionIdentifier")
        if identifier in EXPECTED_SITES:
            counts[identifier] = counts.get(identifier, 0) + 1
    for identifier, expected in EXPECTED_SITES.items():
        require(counts.get(identifier) == expected,
                f"expected {expected} {identifier} actions, found {counts.get(identifier, 0)} "
                "-- see this file's site derivation before changing the number")

    # SAFE-02, enforced structurally rather than by reading the emitter.  BD-03 scopes every
    # write to Media so the ringer is never touched; a Ringtone write is the startling-output
    # failure mode the requirement names.
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != SET_VOLUME:
            continue
        setting = item.get("WFWorkflowActionParameters", {}).get("WFVolumeSetting")
        require(setting == "Media",
                f"action {index} writes volume with WFVolumeSetting={setting!r}; every write "
                "must target Media audio and never the ringer (SAFE-02, BD-03)")

    # No unaudited device property is read.  BD-02/BD-03's evidence covers exactly these two
    # enum cases of getdevicedetails_wfdevice_detail and nothing else.
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != DEVICE_DETAILS:
            continue
        detail = item.get("WFWorkflowActionParameters", {}).get("WFDeviceDetail")
        require(detail in ALLOWED_DEVICE_DETAILS,
                f"action {index} reads device detail {detail!r}; only "
                f"{sorted(ALLOWED_DEVICE_DETAILS)} are audited (BD-02, BD-03)")

    # The bootstrap seed survived.  Without the full subtree, a dotted read beneath
    # settings_snapshot is a hard runtime error on any device whose state.json predates a
    # write -- the exact failure seed_settings_snapshot() exists to prevent.
    template = _state_template_string(actions)
    document = template.replace('"￼"', '"x"').replace("￼", "0")
    try:
        seed = json.loads(document)
    except json.JSONDecodeError as error:
        raise AssertionError(f"bootstrap state.json template is not valid JSON: {error}")
    snapshot = seed.get("settings_snapshot")
    require(isinstance(snapshot, dict) and snapshot,
            "the bootstrap state template no longer seeds a settings_snapshot subtree")
    for group in ("brightness", "volume"):
        leaves = snapshot.get(group)
        require(isinstance(leaves, dict) and "original_value" in leaves,
                f"settings_snapshot.{group}.original_value is missing from the bootstrap "
                "seed, so a restore-side dotted read can hard-error on a fresh install")

    # SAFE-01 as shipped and SAFE-02 as configured.
    #
    # WHAT THIS ASSERTS NOW, AND WHY IT WAS RELAXED -- PHASE 16 (plan 16-03).
    #
    # The lower bound this check used to place under the dim target is RETIRED by user
    # decision D-01 (LOCKED 2026-08-17; the current record is the 2026-08-18 revision block
    # in .planning/phases/16-dimming-and-silence-as-distinct-device-proven-circles/
    # 16-CONTEXT.md).  The retired clause is CITED here and deliberately not quoted -- it
    # lived in BD-02's original Decision paragraph in docs/CAPABILITY-DECISIONS.md and in
    # the canonical strategy's Sec 21.  Quoting it back into a live file would leave a
    # surviving occurrence inside its own supersession note.
    #
    # BD-02's Phase 9 addendum (2026-08-16) had already corrected that clause, on an
    # on-device user report that iOS renders its dimmest practical setting as dim rather
    # than as a black or unusable screen.  That addendum was provisional and scoped to the
    # experimental fork.  D-01 SETTLES it on the main line: it is neither provisional nor
    # fork-scoped any longer.  The canonical strategy is frozen as the historical design
    # input, and BD-02 is the authority where the two disagree.
    #
    # The safety property was never the bound.  It is capture-and-restore reliability: the
    # original is read, persisted to disk BEFORE the device is changed (PHASE 16 plan 16-01,
    # pinned by verify_capture_persistence) and restored by four independent triggers.  So
    # what survives here is the RELATIONSHIP -- the dim target sits at or above the
    # configured floor -- and that assertion is left byte-identical on purpose.  With both
    # keys at 0 it holds AT EQUALITY, which is precisely what makes the floor bind exactly
    # rather than never bind: one step below the floor is unreachable because the target IS
    # the floor.
    config = _config_literal(actions)
    safety = config.get("safety")
    require(isinstance(safety, dict), "the Config literal has no safety block")
    dim_target = safety.get("dim_target")
    floor = safety.get("brightness_floor")
    require(isinstance(dim_target, (int, float)) and dim_target >= 0,
            f"safety.dim_target is {dim_target!r}; the dim target must be a number at or "
            "above 0 -- D-01 retired the stricter test, it did not remove the check")
    require(isinstance(floor, (int, float)) and dim_target >= floor,
            f"safety.dim_target {dim_target!r} is below safety.brightness_floor {floor!r}")
    require(safety.get("allow_volume_increase") is False,
            "safety.allow_volume_increase is not false; SAFE-02 forbids ever raising volume")

    # DELIBERATELY NOT ASSERTED: a count of numeric coercion aggrandizements.
    # Measured at this artifact (PHASE 11, eleven dispatch renderings): 15 of 15 Set
    # Brightness sites carry an explicit WFCoercionVariableAggrandizement, and 4 of 15 Set
    # Volume sites do.  The other 11 volume sites are fed by "Silence Target", which
    # number() already emits Number-typed, so normalise_numeric_operands()'s
    # _already_numeric() check deliberately leaves them alone.  That 19/30 split is an
    # artifact of how the emitter sources each operand, not a
    # safety property, and docs/phase9_self_check.py already pins it where it belongs.
    # Pinning it here too would make every future operand-sourcing change a false failure.
    # This note exists so a reader does not mistake the 10 uncoerced sites for a gap.


def cross_fork_check():
    """Standing smoke test: build_sentient.py's verify_* imports all still resolve.

    build_sentient.py imports a dozen names from build_state_engine at module scope,
    including verify_restore_gates and verify_state_seed.  Deleting either as part of a cut
    would break the Sentient build at import time; importing the module here surfaces that
    immediately rather than at the next fork rebuild.

    Returns the loaded module so call_site_check() can read its main() without a second load.
    """
    return load_module("environmental_restore_sentient", SENTIENT_BUILDER)


def call_site_check(builder, sentient) -> None:
    """Every CALLED_GUARDS entry is INVOKED by each builder's main(), not merely defined.

    PHASE 11 CODE REVIEW (WR-17).  See CALLED_GUARDS for the measurement that forced this:
    both guards this phase added can be removed from the build pipeline with every count in
    this file still green, because REQUIRED_SYMBOLS only asks hasattr/callable.

    The test is a source read of main() rather than a runtime trace, using the same
    inspect.getsource() idiom source_check() already applies to manual_emergency_restore().
    That is deliberate: this file is documented read-only and must never rebuild an artifact,
    so it cannot observe a guard running.  The limit of a source read is recorded rather than
    hidden -- it proves the NAME appears applied inside main(), so a call commented out or
    moved behind a never-taken branch would still read as present.  It catches deletion, which
    is the failure mode the cancelled cut and this phase's own negative control both take.
    """
    for module, label in ((builder, BUILDER.name), (sentient, SENTIENT_BUILDER.name)):
        body = inspect.getsource(module.main)
        for name in CALLED_GUARDS:
            require(f"{name}(" in body,
                    f"{label}'s main() no longer CALLS {name}() -- the function still exists, "
                    "so the REQUIRED_SYMBOLS check above stays green while the guard is "
                    "disarmed: the environmental primitives can silently return to a dead arm, "
                    "or a Panic Escape gate can enclose Emergency Restore, with nothing in this "
                    "file or any other checker able to see it")


def main() -> None:
    builder = load_module("environmental_restore_builder", BUILDER)
    source_check(builder)
    artifact_check(plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"])
    sentient = cross_fork_check()
    call_site_check(builder, sentient)
    print("environmental restore check: passed")


if __name__ == "__main__":
    main()
