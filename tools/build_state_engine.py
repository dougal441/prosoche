#!/usr/bin/env python3
"""Fill the semantic OPEN/CLOSE anchors in the PROSOCHE shortcut once.

This deliberately parses and serializes the plist once.  Anchors are found by
their branch comments, never by mutable action indexes.
"""
from __future__ import annotations

import json
import plistlib
import uuid
from pathlib import Path


SOURCE = Path("src/PROSOCHE-Dumb.xml")
# comment_index matches on startswith, so this prefix is a structural locator, not prose.
# replace_branch_body uses it to bound the CLOSE arm; keep it as the literal start of that
# comment's text.
ROUTE_FALLBACK_MARKER = "Input Key was neither OPEN nor CLOSE"
DISPATCH_MARKER = "--- PHASE 5 PRIMITIVE DISPATCH ---"
RESTORE_MARKER = "--- PHASE 5 RESTORE MANAGED SETTINGS ---"
MANUAL_MARKER = "--- PHASE 5 MANUAL EMERGENCY RESTORE ---"
LIVE_ICE_MARKER = "--- PHASE 5 LIVE ICE REDIRECT ---"
EXPIRY_MARKER = "--- PHASE 5 ICE EXPIRY ---"
EXIT_MARKER = "--- PHASE 6 UNIVERSAL LEAVING ---"
CONTRACT_MARKER = "--- PHASE 6 CONTRACT CLOSE ---"
EXIT_NAMES = ("Capture", "Coordinate", "Create", "Connect", "Consult", "Close")

# Dante's nine Circles, canonical order, index 0 == Circle 1.  BD-06 Decision 1: the names
# are POSITIONAL -- they label the DEPTH, not the intervention.  Which intervention fires at
# a given depth is decided by the Config literal's `sequences` arrays, and the three
# sequences deliberately order the interventions differently at the same Circle numbers, so
# a name can never be read as an intervention name.  Build Addendum 01 §1 asks for the names;
# eight of the nine were measured absent from the artifact entirely, so this ADDS a name
# surface rather than renaming one.
#
# ONE SOURCE OF TRUTH, deliberately.  The Test-a-Circle submenu builds both its `WFMenuItems`
# array and each case's `WFMenuItemTitle` from this tuple, so the two are identical
# element-for-element and in order BY CONSTRUCTION.  A choosefrommenu whose case titles drift
# from its items is `.claude/CLAUDE.md` §4's top documented real-world failure mode; deriving
# both from one expression is what makes that drift unrepresentable rather than merely
# unlikely.
#
# NOT a profile name.  `Limbo` here is Circle 1's positional name and nothing else -- the
# middle profile was renamed to `Purgatory` by BD-06-A1 precisely so that this word names
# exactly one thing.
CIRCLE_NAMES = ("Limbo", "Lust", "Gluttony", "Greed", "Wrath",
                "Heresy", "Violence", "Fraud", "Treachery")

# The three descent profiles, which are the three CANTICLES of the Commedia -- BD-06-A1
# renamed the middle one from `Limbo` to `Purgatory` because `Limbo` is a circle, not a
# canticle, and BD-06 had just given that word to Circle 1.  A profile name is a live Config
# key path (`thresholds.<profile>`, `cooldown_seconds.<profile>`), and a dotted read with a
# missing segment is a HARD ERROR in this runtime, so a partial rename here is a crash rather
# than a degradation.
PROFILE_NAMES = ("Paradise", "Purgatory", "Inferno")

UUID_COUNTER = 0


def circle_menu_title(circle: int) -> str:
    """The one expression that renders a Test-a-Circle label, for items AND case titles."""
    return f"Circle {circle} · {CIRCLE_NAMES[circle - 1]}"

# Every sentence below is selected only in an OPEN run after its named facts are
# present.  The strings are deliberately local and deterministic: Dumb never
# asks a model to interpret a person or fabricate telemetry.
MIRROR_BASELINES = (
    "Circle ￼ follows recorded pressure ￼ and heat ￼.",
    "Recorded now: Circle ￼, pressure ￼, heat ￼.",
    "This open reaches Circle ￼ from pressure ￼ and heat ￼.",
    "The current record places this at Circle ￼, pressure ￼, heat ￼.",
    "Facts for this interruption: Circle ￼; pressure ￼; heat ￼.",
    "The saved calculation is Circle ￼ with pressure ￼ and heat ￼.",
    "This is Circle ￼ on recorded pressure ￼ and heat ￼.",
    "The deterministic reading is Circle ￼, pressure ￼, heat ￼.",
    "Recorded signals: Circle ￼, pressure ￼, heat ￼.",
    "This run has Circle ￼, pressure ￼, and heat ￼.",
)
MIRROR_SUCCESSES = (
    "A recorded boundary was kept before this Circle ￼ open.",
    "The last recorded boundary was respected; this open is Circle ￼.",
    "There is a kept boundary in the record; current Circle: ￼.",
    "The previous contract was kept. Recorded pressure is ￼.",
    "A kept boundary is part of this record; heat is ￼.",
    "The record includes a respected contract before Circle ￼.",
    "One prior boundary was kept; this run's pressure is ￼.",
    "Success is recorded too: the prior boundary was respected.",
    "The last contract was kept; the current heat is ￼.",
    "A recorded success precedes this Circle ￼ interruption.",
)
MIRROR_LAPSES = (
    "A prior recorded boundary ran over; this open is Circle ￼.",
    "The record shows a prior overrun; current pressure is ￼.",
    "One earlier boundary exceeded its time; heat is now ￼.",
    "A recorded contract overran before this Circle ￼ open.",
    "The previous boundary was exceeded; pressure is ￼.",
    "This record includes an overrun; current Circle: ￼.",
    "A prior contract exceeded its boundary; heat is ￼.",
    "The recorded lapse is a time overrun, not a judgment.",
    "There was a previous overrun; this run reaches Circle ￼.",
    "A time boundary ran over earlier; pressure is now ￼.",
)


def uid() -> str:
    global UUID_COUNTER
    UUID_COUNTER += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche-state-engine/{UUID_COUNTER}")).upper()


def action(identifier: str, **parameters):
    return {"WFWorkflowActionIdentifier": identifier,
            "WFWorkflowActionParameters": parameters}


APPS = {
    "Notes": "com.apple.mobilenotes",
    "Voice Memos": "com.apple.VoiceMemos",
    "Camera": "com.apple.camera",
    "Reminders": "com.apple.reminders",
    "Calendar": "com.apple.mobilecal",
    "Contacts": "com.apple.MobileAddressBook",
}


def open_app(name: str):
    bundle_identifier = APPS[name]
    return action("is.workflow.actions.openapp", WFAppIdentifier=bundle_identifier,
                  WFSelectedApp={"BundleIdentifier": bundle_identifier, "Name": name,
                                 "TeamIdentifier": "0000000000"})


def output(uuid_value: str, name: str):
    return {"Value": {"OutputUUID": uuid_value, "OutputName": name,
                      "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def token(name: str):
    return {"Value": {"string": "\ufffc", "attachmentsByRange":
            {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}


def text_token(parts: list[tuple[str, str | None]]):
    string, attachments, cursor = "", {}, 0
    for literal, name in parts:
        string += literal
        cursor += len(literal)
        if name:
            attachments[f"{{{cursor}, 1}}"] = {"Type": "Variable", "VariableName": name}
            string += "\ufffc"
            cursor += 1
    return {"Value": {"string": string, "attachmentsByRange": attachments},
            "WFSerializationType": "WFTextTokenString"}


# CYCLE 12, axis 6b -- the CLEARED sentinel, KEPT, and the gates moved to meet it.
#
# DONOR 6.1 (correctly wired, run on the target iPhone) measured the four semantics this
# whole area turns on:
#   flat read, MISSING key            -> returns nothing, no error -> `has any value` FALSE
#   flat read, PRESENT BUT EMPTY      ->                              `has any value` TRUE
#   DOTTED read, missing segment      -> HARD ERROR, "could not evaluate the key path"
#   "null" -> WFNumberContentItem, >0 -> FALSE, no error
#
# The third and second lines together make the READ-THEN-EXISTENCE-GATE pattern IMPOSSIBLE
# for a dotted key: the read raises unless the final key exists, and if it exists the gate
# is true.  There is NO state in which the gate reads false without the read having already
# raised.  No sentinel swap can fix that -- the construct itself is the defect, and cycle
# 11's "the sentinel is the open question" framing was one level too shallow.
#
# So the sentinel STAYS "null" and the CONSUMERS change:
#   * "null" is PRESENT, so a dotted read of a seeded leaf succeeds instead of raising.
#   * "null" is NON-EMPTY, so it satisfies validate_shortcut.py's iter_empty_strings rule
#     and the cycle-11 Half-2 write-side blocker DISSOLVES ENTIRELY.  Clearing to empty is
#     no longer needed, so the empty-write question does not have to be settled at all.
#   * The gate that must distinguish "cleared" from "captured" is a NUMERIC "> 0", not an
#     existence test.  See restore_managed_settings() for why it is numeric and not code 5.
#
# COOLDOWN_UNTIL IS NOW DEVICE-VERIFIED SAFE and stays inline at its three sites.  Donor
# 6.1 test 2 read the literal "null" out of the Dictionary, coerced it to Number and
# compared it > 0: FALSE, no error.  That is already the semantically correct reading of a
# cleared cooldown ("not in cooldown"), at the most critical position on the OPEN path --
# action 170, the conditional the build-i coercion fix repaired.  Do not touch it.
CLEARED_SENTINEL = "null"
# Keys whose EXISTENCE gate was knowingly still condition 100 even though the key is
# written with the sentinel.
#
# pending_exit FIXED CYCLE 16, device-confirmed LIVE, not latent: a flat read of
# "pending_exit" -- entirely absent from the bootstrap template -- hard-errored on the
# very first OPEN this session's device pass exercised ("In '', no value was found for
# dictionary key 'pending_exit'"), on the OPEN critical path itself, between breadcrumbs
# I and J (complete_pending_exit()). Fixed with the SAME container/leaf split
# settings_snapshot already uses (see clear_snapshot()'s docstring for the original
# cycle-10 finding this mirrors): seed_pending_exit() establishes pending_exit as a
# PERMANENT {"type", "timestamp"} container, never again replaced wholesale, so its own
# existence is now an invariant; record_exit_and_route() and complete_pending_exit()
# write and clear only the .type/.timestamp LEAVES, gated by a STRING "is not sentinel"
# test (condition 5), not an existence test. Full trace in seed_pending_exit()'s docstring.
#
# active_session remains LATENT and UNCHANGED this cycle: the confirmed device run
# reached breadcrumb I (past every active_session read on the OPEN critical path) with
# no active_session-related error, so it is not live -- the cycle-16 directive against
# fixing a non-reachable defect speculatively applies. Its bootstrap state is a bare JSON
# null (present, unlike pending_exit's former total absence), and a flat read of an
# absent key returns nothing -- which passes `is not "null"` and would then run the
# nested DOTTED read of .id against a missing parent, i.e. it would trade a latent hard
# error for an immediate one. Fixing it needs the same container/leaf treatment
# pending_exit just received; recorded as a candidate follow-up, not done here.
KNOWN_SENTINEL_EXISTENCE_GATES = ("active_session",)


def cleared_value():
    """The CLEARED sentinel for a gate-consumed state key.  See the note above."""
    return text_token([(CLEARED_SENTINEL, None)])


def comment(text: str):
    return action("is.workflow.actions.comment", WFCommentActionText=text)


def set_var(name: str, source):
    return action("is.workflow.actions.setvariable", WFInput=source, WFVariableName=name)


def get_value(key, source, name: str):
    """Get a dictionary value and bind it directly, preserving its native type.

    CYCLE 15.  Use this instead of read_value() whenever the underlying state field
    is COMPOUND (a List/Array in this schema -- recent_sessions, exit_events,
    exit_stats.<name>.samples, profile_snapshot.enabled_exits are the confirmed
    instances) and a downstream action consumes it as a List: Get Item From List
    WFInput, or Repeat With Each WFInput.

    read_value()'s extra Get Text step is correct for a SCALAR meant for a text or
    numeric comparison, but it stringifies a compound value: the array collapses
    into one Text blob, so a Repeat With Each over it iterates wrong (or not at
    all), and a Get Item From List "First Item" off it returns that same Text blob
    rather than a genuine Dictionary item.  A subsequent Get Dictionary Value read
    against that item then fails with "couldn't convert from Text to Dictionary" --
    this is the exact breadcrumb E->F device error this cycle traces back to
    exactly this pattern, at recent_sessions (open_pipeline's own Previous Session
    lookup).  Donor 7 previously established the analogous lesson for DATE-typed
    values (elapsed_since(), cycle 14): use the plain construct this artifact's own
    write side already assumes, rather than inserting a coercion step that fits a
    different field shape.

    This is the SAME getvalueforkey call read_value() already makes -- no new
    action identifier, no new parameter key -- with the gettext step removed,
    binding the variable straight to "Dictionary Value", the output that already
    carries the key's real underlying JSON type (string, number, boolean, array,
    or object).  This artifact's own WRITE side already assumes exactly this: e.g.
    recent_sessions is written back via set_value(key, variable("Recent Sessions
    Next")), where "Recent Sessions Next" is built purely by appendvariable (a
    genuine List, never re-serialized to text) -- so an un-stringified read is what
    makes the round trip symmetric, not a new assumption about iOS.
    Same action count minus the removed gettext step (2 actions instead of 3).
    """
    get_id = uid()
    return [
        action("is.workflow.actions.getvalueforkey", UUID=get_id, WFDictionaryKey=key, WFInput=source),
        set_var(name, output(get_id, "Dictionary Value")),
    ]


def read_value(key, source, name: str):
    """Get a dictionary value, coerce via Text, then name it for comparison."""
    value_id, text_id = uid(), uid()
    return [
        action("is.workflow.actions.getvalueforkey", UUID=value_id, WFDictionaryKey=key, WFInput=source),
        action("is.workflow.actions.gettext", UUID=text_id,
               WFTextActionText=output(value_id, "Dictionary Value")),
        set_var(name, output(text_id, "Text")),
    ]


def set_value(key: str, value, dictionary_name="State"):
    # Set Dictionary Value reads its Value from WFDictionaryValue, never WFInput.
    # ToolKit v78 first-party catalog, is.workflow.actions.setvalueforkey:
    # WFDictionaryKey (Key), WFDictionaryValue (Value), WFDictionary (Dictionary).
    # Passing the value as WFInput leaves the Value field empty and iOS raises
    # "No value was provided to the Set Dictionary Value action for the key <key>".
    return action("is.workflow.actions.setvalueforkey", UUID=uid(), WFDictionaryKey=key,
                  WFDictionary=variable(dictionary_name), WFDictionaryValue=value)


def if_block(value_name: str, condition: int, *, number=None, string=None):
    # WFInput.Variable is a VARIABLE SLOT, not a string slot.  It must hold a
    # WFTextTokenAttachment wrapping a Type-bearing descriptor -- variable() or output().
    # It must NOT hold token()/text_token(), which produce a WFTextTokenString TEXT
    # TEMPLATE ({"string": "￼", "attachmentsByRange": {...}}).  Shortcuts cannot
    # resolve a text template as a conditional input: it renders the If's input field as
    # unset and refuses to run with "Please choose a value for each parameter in this
    # action".  This is the cycle-2 string-envelope rule INVERTED, which is exactly how 13
    # hand-written overwrites of this parameter went unnoticed for seven debug cycles.
    # Evidence: Donor 3 action 4 (device export, variable-vs-variable If) uses the
    # attachment form; 20/20 golden-corpus conditionals carrying WFInput use it; 0 use a
    # text template.  Enforced by verify_conditional_inputs().
    group = uid()
    params = {"GroupingIdentifier": group, "WFControlFlowMode": 0,
              "WFCondition": condition,
              "WFInput": {"Type": "Variable", "Variable": variable(value_name)}}
    if number is not None:
        params["WFNumberValue"] = number
    if string is not None:
        params["WFConditionalActionString"] = string
    return group, action("is.workflow.actions.conditional", **params)


def otherwise(group):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=1)


def end_if(group):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=2)


def number(value, name: str):
    number_id = uid()
    return [action("is.workflow.actions.number", UUID=number_id, WFNumberActionNumber=value),
            set_var(name, output(number_id, "Number"))]


def math(left_name: str, right, result_name: str, op=None):
    math_id, params = uid(), {"UUID": uid(), "WFInput": variable(left_name), "WFMathOperand": right}
    params["UUID"] = math_id
    if op and op != "+":
        params["WFMathOperation"] = op
    return [action("is.workflow.actions.math", **params), set_var(result_name, output(math_id, "Calculation Result"))]


def expression(parts: list[tuple[str, str | None]], name: str):
    expression_id = uid()
    return [action("is.workflow.actions.calculateexpression", UUID=expression_id,
                   Input=text_token(parts)), set_var(name, output(expression_id, "Result"))]


def elapsed_since(earlier_name: str, result_name: str, now_name: str = "Now Epoch"):
    """Seconds between now and a STORED epoch reading -- numeric subtraction, not dates.

    CYCLE 14 REPLACEMENT for the former elapsed()/gettimebetweendates helper, which was
    the actual root cause of symptom 1's breadcrumb D->E device failure ("Get Time Between
    Dates failed because Shortcuts couldn't convert from Text to Date").
    last_open_at, last_close_at and pending_exit.timestamp are all written with
    variable("Now Epoch") -- a NUMBER (elapsed seconds since the 1970-01-01 anchor; see the
    hand-authored CLOCK block at the top of the artifact), never a Date object.  Reading
    them back through read_value() (get + gettext) yields a TEXT variable holding that
    same number as a string, e.g. "1755000000".  The former elapsed() helper fed that
    string into gettimebetweendates.WFTimeUntilFromDate, a DATE-typed parameter -- asking
    Shortcuts to parse a bare epoch-seconds string as a calendar date, which it cannot do.
    Donor 7's device-confirmed chain (Date -> Format Date -> Adjust Date -> Get Time
    Between Dates, all genuine Date-typed operands, zero coercion) is untouched by this
    change and remains the CLOCK block's own construct for producing "Now Epoch" itself.
    This helper is for the DOWNSTREAM case: two already-numeric epoch readings, so the
    correct construct is the one this artifact already uses for the identical shape at
    Session Duration (close_pipeline(): math("Now Epoch", variable("Captured Start"),
    "Session Duration", "-")) -- plain subtraction, no Date object, no coercion class to
    establish or guess.  Same action count as the helper it replaces (2: math + setvar).
    """
    return math(now_name, variable(earlier_name), result_name, "-")


def round_down(source_name: str, result_name: str):
    round_id = uid()
    return [action("is.workflow.actions.round", UUID=round_id, WFInput=variable(source_name),
                   WFRoundMode="Always Round Down", WFRoundTo="Ones Place"),
            set_var(result_name, output(round_id, "Rounded Number"))]


def save_state(source_name="State"):
    """Save exactly the final full dictionary from this branch, once."""
    named_id = uid()
    return [
        action("is.workflow.actions.setitemname", UUID=named_id, WFName="state.json", WFInput=variable(source_name)),
        action("is.workflow.actions.documentpicker.save", WFInput=output(named_id, "Renamed Item"),
               WFAskWhereToSave=False, WFFileDestinationPath="PROSOCHE/state.json", WFSaveFileOverwrite=True),
    ]


def alert(title: str, message):
    return action("is.workflow.actions.alert", WFAlertActionTitle=title,
                  WFAlertActionMessage=message)


def notification(title: str, body):
    """Non-blocking on-device confirmation. Same minimal-params shape as alert():
    no WFNotificationActionSound, no WFInput -- both VERIFIED-usable params per
    docs/BUILD-NOTES.md's CAP-S07 entry, matching this project's "no unsafe or
    startling" default posture."""
    return action("is.workflow.actions.notification", WFNotificationActionTitle=title,
                  WFNotificationActionBody=body)


def list_items(items, name: str):
    list_id = uid()
    return [action("is.workflow.actions.list", UUID=list_id, WFItems=list(items)),
            set_var(name, output(list_id, "List"))]


def reload_state(name="Reloaded State"):
    file_id, dictionary_id = uid(), uid()
    return [action("is.workflow.actions.documentpicker.open", UUID=file_id,
                   WFFileErrorIfNotFound=False, WFGetFilePath="PROSOCHE/state.json", WFShowFilePicker=False),
            action("is.workflow.actions.detect.dictionary", UUID=dictionary_id, WFInput=output(file_id, "File")),
            set_var(name, output(dictionary_id, "Dictionary"))]


def menu(group: str, mode: int, *, prompt=None, items=None, title=None):
    params = {"GroupingIdentifier": group, "WFControlFlowMode": mode}
    if prompt is not None:
        params["WFMenuPrompt"] = prompt
    if items is not None:
        params["WFMenuItems"] = items
    if title is not None:
        params["WFMenuItemTitle"] = title
    return action("is.workflow.actions.choosefrommenu", **params)


def device_detail(detail: str, name: str):
    detail_id = uid()
    return [action("is.workflow.actions.getdevicedetails", UUID=detail_id,
                   WFDeviceDetail=detail),
            set_var(name, output(detail_id, "Device Details"))]


def set_brightness(source):
    return action("is.workflow.actions.setbrightness", WFBrightness=source,
                  ShowWhenRun=False)


def set_media_volume(source):
    return action("is.workflow.actions.setvolume", WFVolume=source,
                  WFVolumeSetting="Media", ShowWhenRun=False)


def clear_snapshot(key: str, dictionary_name="State"):
    """Clear the captured ORIGINAL, never the container that holds it.

    Cycle 10 finding 5: clearing `settings_snapshot.<key>` replaced the sub-DICTIONARY
    with a string, so the very next run's dotted read of `.original_value` ran against a
    string parent and hard-errored -- the identical failure the bootstrap seed exists to
    prevent, reintroduced one run later and presenting as a regression.
    Clearing the LEAF instead makes the seeded subtree a PERMANENT invariant: once
    bootstrap has created the container it is never overwritten by anything, so the
    container's own condition-100 gate can never be reached with a non-dictionary value
    and the dotted read beneath it can never raise.  That is what licenses keeping the
    container gates at 100 while the leaf gates change -- the split is enforced by
    verify_sentinel_gates(), not asserted.
    Same action count as clearing the container: one Set Dictionary Value, deeper key.
    changed_at / changed_by_session_id are deliberately left: they are written at 20 sites
    and READ AT NONE in either fork (the ownership check does not exist -- DEV-06, deferred
    to the user as a design change), so stale values there have no consumer.
    """
    return set_value(f"settings_snapshot.{key}.original_value", cleared_value(), dictionary_name)


def restore_managed_settings(dictionary_name="State"):
    """Restore only captured values; never guess an original setting.

    THE LEAF GATES ARE NUMERIC "> 0", AND CODE 5 WAS VERIFIED AND THEN REJECTED.
    Code 5 ("is not", string family, WFConditionalActionString) is a real construct --
    CONTROL_FLOW.md's definitive table lists it, and four code-5 sites already ship in both
    forks, one of them action 149 inside span B->C which the device has executed.  It is
    also the obvious reading of "skip when the leaf holds the sentinel".
    It is still WRONG HERE, because `is not "null"` is TRUE for an EMPTY value, and build
    2026-08-14j seeded exactly "" into these leaves.  On any device that rebuilt state.json
    under build j, a code-5 gate would pass empty straight into Set Brightness -- the black
    screen this fix exists to remove.  Code 5 closes the sentinel case and leaves the empty
    case open.
    A numeric "> 0" closes BOTH, and both inputs are device-measured, not inferred:
      "null" -> WFNumberContentItem -> > 0  ->  FALSE, no error   (Donor 6.1 test 2)
      ""     -> WFNumberContentItem -> > 0  ->  FALSE, no error   (Donor 6 action 8)
    It is also the safety property itself rather than a proxy for it -- only a strictly
    positive reading is ever written back, so a zero or absent original can never darken the
    screen -- and it is the EXACT test the CAPTURE side already uses on the same quantity
    (dim(): if_block("Captured Brightness", 2, number=0)).  Capture and restore now agree on
    what counts as a real reading.
    The operand is gettext-fed, so normalise_numeric_operands() attaches Donor 4.1's
    WFCoercionVariableAggrandizement automatically; this adds no new shape to the artifact.
    The COST is stated rather than hidden: a genuine captured Media volume of exactly 0 is
    not restored.  Skipping a restore leaves the current setting untouched, which is the
    fail-safe direction and is what "never guess an original setting" already requires.
    """
    a = [comment("""Restore managed settings only when a captured original exists:
- Brightness uses the saved original value, never a new target.
- Volume is always Media volume and never exceeds its saved original.
- A restored original is cleared to the sentinel while its container and all unrelated State remain intact.""")]
    a += read_value("settings_snapshot.brightness", variable(dictionary_name), "Restore Brightness Snapshot")
    snapshot_g, snapshot_if = if_block("Restore Brightness Snapshot", 100)
    a += [snapshot_if] + read_value("settings_snapshot.brightness.original_value", variable(dictionary_name), "Restore Brightness")
    bright_g, bright_if = if_block("Restore Brightness", 2, number=0)
    a += [bright_if, set_brightness(variable("Restore Brightness")), clear_snapshot("brightness", dictionary_name),
          otherwise(bright_g), action("is.workflow.actions.nothing"), end_if(bright_g), otherwise(snapshot_g),
          action("is.workflow.actions.nothing"), end_if(snapshot_g)]
    a += read_value("settings_snapshot.volume", variable(dictionary_name), "Restore Volume Snapshot")
    snapshot_g, snapshot_if = if_block("Restore Volume Snapshot", 100)
    a += [snapshot_if] + read_value("settings_snapshot.volume.original_value", variable(dictionary_name), "Restore Volume")
    volume_g, volume_if = if_block("Restore Volume", 2, number=0)
    a += [volume_if, set_media_volume(variable("Restore Volume")), clear_snapshot("volume", dictionary_name),
          otherwise(volume_g), action("is.workflow.actions.nothing"), end_if(volume_g), otherwise(snapshot_g),
          action("is.workflow.actions.nothing"), end_if(snapshot_g)]
    return a


def knock():
    # Renders the primitive BD-06 ships as "Pause"; the Python name is deliberately unchanged
    # (see the dispatch tuple in primitive_dispatch()).
    return [comment("""Pause is a brief factual interruption:
- Circle, Pressure, and Heat come from this OPEN run.
- It does not infer intent or alter State."""),
            alert("PROSOCHĒ", text_token([("Circle ", "Circle Next"),
                                           (" · pressure ", "Pressure Next"),
                                           (" · heat ", "Heat Final")] ))]


def ash():
    # Renders the primitive BD-06 ships as "Black and White"; the Python name is deliberately
    # unchanged (see the dispatch tuple in primitive_dispatch()).
    return [comment("""Black and White is the validator-clean visual-pause fallback:
- It changes no accessibility setting.
- Color Filters is deliberately excluded because the iOS action is not validator-supported."""),
            # The body must not open with another primitive's shipped name: "Pause" is now
            # Circle 1's intervention, and this alert read as if that one had fired.
            alert("Black and White", "One breath away from the screen before you go on.")]


def confession():
    ask_id = uid()
    group = uid()
    a = [comment("""Confession accepts any wording, including a blank intention:
- Ask for Input collects free text without judging it.
- Choose from Menu offers 2, 5, 10, 15, or a custom boundary."""),
         action("is.workflow.actions.ask", UUID=ask_id,
                WFAskActionPrompt="What are you reaching for? (optional)", WFInputType="Text"),
         set_var("Confession Intention", output(ask_id, "Provided Input")),
         comment("Choose a boundary after accepting the intention:\n- Menu options preserve the user's free-text answer.\n- Custom asks for a numeric number of minutes."),
         menu(group, 0, prompt="Choose a boundary", items=["2 minutes", "5 minutes", "10 minutes", "15 minutes", "Custom"])]
    for label, minutes in (("2 minutes", 2), ("5 minutes", 5), ("10 minutes", 10), ("15 minutes", 15)):
        a += [menu(group, 1, title=label)] + number(minutes, "Declared Boundary Minutes")
    custom_id = uid()
    a += [menu(group, 1, title="Custom"),
          action("is.workflow.actions.ask", UUID=custom_id,
                 WFAskActionPrompt="How many minutes?", WFInputType="Number"),
          set_var("Declared Boundary Minutes", output(custom_id, "Provided Input")),
          menu(group, 2)]
    valid_group, valid = if_block("Declared Boundary Minutes", 2, number=0)
    a += [comment("Boundary validation:\n- Only the numeric minute boundary must be positive.\n- Blank intention remains valid and has no keyword or sincerity gate."), valid]
    a += math("Declared Boundary Minutes", 60, "Declared Duration Seconds", "×") + persist_contract()
    a += [otherwise(valid_group), alert("Boundary", "Choose a positive number of minutes."), end_if(valid_group)]
    return a


def persist_contract():
    """Write Confession only when this primitive still owns the open session."""
    a = [comment("Reload before writing a contract. A superseded session has a Nothing-only path.")]
    a += reload_state() + read_value("active_session", variable("Reloaded State"), "Contract Active Session")
    active_group, active = if_block("Contract Active Session", 100)
    a += [active] + read_value("active_session.id", variable("Reloaded State"), "Contract Owner ID")
    owns_group, owns = if_block("Contract Owner ID", 4, string="captured-session-placeholder")
    owns["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    owns["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID")
    a += [owns, set_value("active_session.intention", variable("Confession Intention"), "Reloaded State"),
          set_value("active_session.declared_duration_seconds", variable("Declared Duration Seconds"), "Reloaded State")]
    a += save_state("Reloaded State") + [otherwise(owns_group), action("is.workflow.actions.nothing"), end_if(owns_group),
                                            otherwise(active_group), action("is.workflow.actions.nothing"), end_if(active_group)]
    return a


def dimming():
    a = [comment("""Dimming is reversible or message-only:
- Capture Current Brightness once when no snapshot exists.
- Do not brighten an already dim screen and never set zero.
- Keep an existing unrestored snapshot unchanged.""")]
    a += read_value("settings_snapshot.brightness", variable("State"), "Brightness Snapshot")
    snapshot_g, snapshot_if = if_block("Brightness Snapshot", 100)
    a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
    a += device_detail("Current Brightness", "Captured Brightness")
    capture_g, capture_if = if_block("Captured Brightness", 2, number=0)
    a += [capture_if, set_value("settings_snapshot.brightness.original_value", variable("Captured Brightness")),
          set_value("settings_snapshot.brightness.changed_at", variable("Now Epoch")),
          set_value("settings_snapshot.brightness.changed_by_session_id", variable("Session ID"))]
    a += config("safety.dim_target", "Dim Target")
    already_dim_g, already_dim_if = if_block("Captured Brightness", 1, number=variable("Dim Target"))
    a += [already_dim_if, action("is.workflow.actions.nothing"), otherwise(already_dim_g),
          set_brightness(variable("Dim Target")), end_if(already_dim_g), otherwise(capture_g),
          alert("Dim", "Brightness could not be captured, so nothing was changed."), end_if(capture_g),
          end_if(snapshot_g)]
    return a


def silence():
    a = [comment("""Silence is reversible or message-only:
- Capture Current Volume once when no snapshot exists.
- Use Media volume only and never increase it.
- Keep an existing unrestored snapshot unchanged.""")]
    a += read_value("settings_snapshot.volume", variable("State"), "Volume Snapshot")
    snapshot_g, snapshot_if = if_block("Volume Snapshot", 100)
    a += [snapshot_if, action("is.workflow.actions.nothing"), otherwise(snapshot_g)]
    a += device_detail("Current Volume", "Captured Volume")
    capture_g, capture_if = if_block("Captured Volume", 2, number=0)
    a += [capture_if, set_value("settings_snapshot.volume.original_value", variable("Captured Volume")),
          set_value("settings_snapshot.volume.changed_at", variable("Now Epoch")),
          set_value("settings_snapshot.volume.changed_by_session_id", variable("Session ID"))]
    target = number(0.10, "Silence Target")
    a += target
    quiet_g, quiet_if = if_block("Captured Volume", 1, number=variable("Silence Target"))
    a += [quiet_if, action("is.workflow.actions.nothing"), otherwise(quiet_g),
          set_media_volume(variable("Silence Target")), end_if(quiet_g), otherwise(capture_g),
          alert("Silence", "Volume could not be captured, so nothing was changed."), end_if(capture_g),
          end_if(snapshot_g)]
    return a


def exile():
    return [comment("""Exile is immediate and deterministic:
- Return to Home Screen does not ask a permission question.
- Phase 6 may replace this route with learned exits."""),
            action("is.workflow.actions.returntohomescreen")]


def mirror_text(items, name: str):
    """Select one non-empty template from a fact-gated list using Circle 1..9."""
    list_id, item_id = uid(), uid()
    a = [action("is.workflow.actions.list", UUID=list_id, WFItems=list(items)),
         action("is.workflow.actions.getitemfromlist", UUID=item_id,
                WFItemSpecifier="Item At Index", WFItemIndex=variable("Circle Next"),
                WFInput=output(list_id, "List")),
         set_var(name, output(item_id, "Item from List"))]
    return a


def mirror_templates(templates):
    facts = ("Circle Next", "Pressure Next", "Heat Final")
    return tuple(text_token([(part, facts[index] if index < len(template.split("￼")) - 1 else None)
                             for index, part in enumerate(template.split("￼"))]) for template in templates)


def mirror_and_voice():
    baseline = mirror_templates(MIRROR_BASELINES)
    success = mirror_templates(MIRROR_SUCCESSES)
    lapse = mirror_templates(MIRROR_LAPSES)
    a = [comment("""Mirror selects from 30 fact-gated, local templates:
- Baselines use only this OPEN's Circle, Pressure, and Heat.
- Success and lapse wording runs only when the recorded previous contract says so.
- No model, interpretation, or empty telemetry path exists.""")]
    # Baseline is always available: Circle, Pressure, and Heat are prepared in this OPEN run.
    a += mirror_text(baseline, "Mirror Text")
    respected_g, respected_if = if_block("Previous Respected", 4, string="true")
    lapsed_g, lapsed_if = if_block("Previous Respected", 4, string="false")
    a += [respected_if] + mirror_text(success, "Mirror Text") + [otherwise(respected_g), lapsed_if]
    a += mirror_text(lapse, "Mirror Text") + [otherwise(lapsed_g), action("is.workflow.actions.nothing"), end_if(lapsed_g), end_if(respected_g),
          alert("Mirror", variable("Mirror Text"))]
    a += read_value("voice_enabled", variable("State"), "Voice Enabled")
    voice_g, voice_if = if_block("Voice Enabled", 2, number=0)
    spoken_g, spoken_if = if_block("Spoken This Run", 101)
    # DEV-03 closed: the ToolKit v78 catalog DOES define speaktext parameters, and its text
    # parameter is WFText (type str, name "Text").  WFInput is not among them, so the spoken
    # text was never being read.  str-typed, so it also takes the WFTextTokenString envelope.
    a += [voice_if, spoken_if, action("is.workflow.actions.speaktext", WFText=variable("Mirror Text"))]
    a += number(1, "Spoken This Run")
    a += [otherwise(spoken_g), action("is.workflow.actions.nothing"), end_if(spoken_g),
          otherwise(voice_g), action("is.workflow.actions.nothing"), end_if(voice_g)]
    return a


def ice_start():
    a = [comment("""Ice is profile-aware and deterministic:
- Read the active profile duration from Config.
- Record one cooldown deadline and route to Home Screen.
- Model output is not involved.""")]
    a += read_value("profile", variable("State"), "Ice Profile")
    a += config(text_token([("cooldown_seconds.", "Ice Profile")]), "Ice Seconds")
    a += math("Now Epoch", variable("Ice Seconds"), "Ice Until")
    a += [set_value("cooldown_until", variable("Ice Until")), exile()[-1]]
    return a


def primitive_dispatch(circle_name: str | None = None):
    a = [comment(DISPATCH_MARKER + "\n\n- Select exactly one configured sequence entry for Circle after Leaving is offered.\n- The entry must name its primitive exactly; every entry names exactly one.")]
    a += read_value("sequence", variable("State"), "Sequence")
    if circle_name is None:
        a += read_value("circle", variable("State"), "Dispatch Circle")
    else:
        a += [set_var("Dispatch Circle", variable(circle_name))]
    entry_id, entry_text_id = uid(), uid()
    a += [action("is.workflow.actions.getvalueforkey", UUID=entry_id,
                 WFDictionaryKey=text_token([("sequences.", "Sequence"), (".", None), ("", "Dispatch Circle")]),
                 WFInput=variable("Config")),
          action("is.workflow.actions.gettext", UUID=entry_text_id,
                 WFTextActionText=output(entry_id, "Dictionary Value")),
          set_var("Selected Primitive", output(entry_text_id, "Text"))]
    # The tuple carries the SHIPPED name, the function carries the INTERNAL name.  BD-06
    # Decision 3 renames the roster, but knock(), ash(), confession(), dimming(), exile(),
    # mirror_and_voice() and ice_start() all keep their Python identifiers because
    # docs/environmental_restore_check.py:49-60 imports generator functions BY NAME.
    #
    # "Loud Mirror" (Circle 8 in all three sequences) reuses mirror_and_voice() as a
    # DELIBERATE INTERIM, not as the designed behaviour.  It is here so the dispatch-coverage
    # guard can be a hard gate from this commit onwards rather than waiting on a primitive
    # that does not exist yet: mirror_and_voice() already carries the once-per-run and
    # voice-enabled gates CIRC-08 requires.  PHASE 15 replaces it with the designed Voice
    # primitive; until then Circle 8 is a real dispatch, not the designed one.
    for name, implementation in (("Pause", knock), ("Black and White", ash), ("Silence", silence),
                                 ("Intention", confession), ("Dim", dimming), ("Eject", exile),
                                 ("Mirror", mirror_and_voice), ("Loud Mirror", mirror_and_voice),
                                 ("Frozen", ice_start)):
        # Condition 4 ("string is"), never 99 ("contains").  BD-06 Decision 5 abolished the
        # combined entries that were 99's only reason to exist, and under 99 the entry
        # "Loud Mirror" would ALSO fire the "Mirror" branch -- a silent double dispatch that
        # no validator, catalog lookup or decrypt can see.
        group, check = if_block("Selected Primitive", 4, string=name)
        a += [comment(f"Dispatch {name} only when the selected Config entry names it exactly:\n- Input uses Selected Primitive from the sequence lookup.\n- The otherwise path leaves State unchanged."), check]
        a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
    a += [comment("--- PHASE 5 PRIMITIVE DISPATCH END ---")]
    return a


def enabled_exits(source="State"):
    """Filter in canonical order; no disabled name can enter a selection menu."""
    a = [comment("Build Enabled Exits in canonical order by intersecting the saved profile list.")]
    # CYCLE 15: get_value(), not read_value() -- enabled_exits is a compound Array
    # (["Capture", ...]) consumed below by Repeat With Each; read_value()'s gettext
    # step would stringify it into one Text blob. See get_value()'s docstring.
    a += get_value("profile_snapshot.enabled_exits", variable(source), "Profile Enabled Exits")
    a += list_items(EXIT_NAMES, "Canonical Exits")
    outer = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=outer, WFControlFlowMode=0,
                 WFInput=variable("Canonical Exits")), set_var("Canonical Exit", variable("Repeat Item"))]
    inner = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=inner, WFControlFlowMode=0,
                 WFInput=variable("Profile Enabled Exits")), set_var("Enabled Exit Candidate", variable("Repeat Item"))]
    matches_group, matches = if_block("Enabled Exit Candidate", 4, string="canonical-exit-placeholder")
    matches["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    matches["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Canonical Exit")
    a += [matches, action("is.workflow.actions.appendvariable", WFInput=variable("Canonical Exit"), WFVariableName="Enabled Exits"),
          otherwise(matches_group), action("is.workflow.actions.nothing"), end_if(matches_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=inner, WFControlFlowMode=2),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=outer, WFControlFlowMode=2)]
    return a


def select_exit():
    """Deterministic, state-driven selector. The concrete menu always shares recorder/router."""
    a = [comment("--- PHASE 6 EXIT SELECTOR ---\n\n- Sparse data rotates enabled exits by the persisted counter.\n- Sufficient data uses integer averages, canonical ties, then configured epsilon exploration.")]
    a += enabled_exits() + read_value("exit_selection_counter", variable("State"), "Exit Selection Counter")
    # Condition 101 ("does not have any value") tests absence directly on the read
    # variable, matching the has-any-value idiom already used throughout this file
    # (e.g. "Contract Active Session", "Spoken This Run") -- a literal empty-string
    # comparator (condition 5 vs "") cannot express this: the validator's
    # iter_empty_strings rejects any empty WFConditionalActionString outright (raw or
    # WFTextTokenString-wrapped), and even if it didn't, "is not <sentinel>" is true for
    # every real, present counter value too, so it could never distinguish missing from
    # present. See 04-02-SUMMARY.md for the recorded deviation from the plan's literal
    # "pass the empty string" instruction.
    missing_counter, counter = if_block("Exit Selection Counter", 101)
    a += [counter] + number(0, "Exit Selection Counter") + [otherwise(missing_counter), action("is.workflow.actions.nothing"), end_if(missing_counter)]
    a += config("exits.exploit_min_observations", "Exploit Minimum") + config("exits.exploration_rate", "Exploration Rate")
    a += number(0, "Sparse Selection")
    enough = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=enough, WFControlFlowMode=0, WFInput=variable("Enabled Exits")),
          set_var("Stats Exit", variable("Repeat Item"))]
    a += read_value(text_token([("exit_stats.", "Stats Exit"), (".count", None)]), variable("State"), "Stats Count")
    sparse_group, sparse = if_block("Stats Count", 0, number=variable("Exploit Minimum"))
    a += [sparse, *number(1, "Sparse Selection"), otherwise(sparse_group), action("is.workflow.actions.nothing"), end_if(sparse_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=enough, WFControlFlowMode=2)]
    count_id = uid()
    # WFCountType is a required picker ("Type"): golden corpus 11/11 emit it, 0 omit it.
    a += [action("is.workflow.actions.count", UUID=count_id, WFCountType="Items",
                 WFInput=variable("Enabled Exits"), Input=variable("Enabled Exits")),
          set_var("Enabled Exit Count", output(count_id, "Count"))]
    a += expression([( "(", None), ("", "Exit Selection Counter"), (" % ", None), ("", "Enabled Exit Count"), (") + 1", None)], "Rotation Index")
    item_id = uid()
    a += [action("is.workflow.actions.getitemfromlist", UUID=item_id, WFItemSpecifier="Item At Index",
                 WFItemIndex=variable("Rotation Index"), WFInput=variable("Enabled Exits")),
          set_var("Selected Exit", output(item_id, "Item from List"))]
    # Keep the sparse selection as the default, then replace it only when all exits have evidence.
    exploit_group, exploit = if_block("Sparse Selection", 2, number=0)
    a += [exploit, *number(-1, "Best Average"), *number(0, "Best Seen")]
    score_loop = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=score_loop, WFControlFlowMode=0, WFInput=variable("Enabled Exits")),
          set_var("Stats Exit", variable("Repeat Item"))]
    a += read_value(text_token([("exit_stats.", "Stats Exit"), (".count", None)]), variable("State"), "Stats Count")
    a += read_value(text_token([("exit_stats.", "Stats Exit"), (".sum_return_seconds", None)]), variable("State"), "Stats Sum")
    a += math("Stats Sum", variable("Stats Count"), "Stats Average Raw", "÷") + round_down("Stats Average Raw", "Stats Average")
    higher_group, higher = if_block("Stats Average", 3, number=variable("Best Average"))
    a += [higher, set_var("Best Average", variable("Stats Average")), set_var("Best Exit", variable("Stats Exit")), set_var("Selected Exit", variable("Stats Exit")),
          otherwise(higher_group), action("is.workflow.actions.nothing"), end_if(higher_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=score_loop, WFControlFlowMode=2)]
    a += expression([( "", "Exit Selection Counter"), (" % 100", None)], "Exploration Roll") + math("Exploration Rate", 100, "Exploration Threshold Raw", "×") + round_down("Exploration Threshold Raw", "Exploration Threshold")
    explore_group, explore = if_block("Exploration Roll", 0, number=variable("Exploration Threshold"))
    a += [explore, *number(0, "Exploration Selected"), *number(0, "Past Best")]
    next_loop = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=next_loop, WFControlFlowMode=0, WFInput=variable("Enabled Exits")),
          set_var("Candidate Exit", variable("Repeat Item"))]
    is_best_group, is_best = if_block("Candidate Exit", 4, string="best-exit-placeholder")
    is_best["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    is_best["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Best Exit")
    a += [is_best, *number(1, "Past Best"), otherwise(is_best_group)]
    choose_after_group, choose_after = if_block("Past Best", 2, number=0)
    a += [choose_after]
    unchosen_group, unchosen = if_block("Exploration Selected", 4, string="0")
    a += [unchosen, set_var("Selected Exit", variable("Candidate Exit")), *number(1, "Exploration Selected"), otherwise(unchosen_group), action("is.workflow.actions.nothing"), end_if(unchosen_group),
          otherwise(choose_after_group), action("is.workflow.actions.nothing"), end_if(choose_after_group), end_if(is_best_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=next_loop, WFControlFlowMode=2)]
    wrap_loop = uid()
    a += [comment("Exploration wrap:\n- After Close, choose the first canonical non-best exit exactly once."),
          action("is.workflow.actions.repeat.each", GroupingIdentifier=wrap_loop, WFControlFlowMode=0, WFInput=variable("Enabled Exits")),
          set_var("Candidate Exit", variable("Repeat Item"))]
    needs_wrap_group, needs_wrap = if_block("Exploration Selected", 4, string="0")
    # FOLLOW-UP (not part of this defect-class fix): this condition uses code 99
    # ("contains") to select "the first non-best exit", which is worth a second look
    # against that stated intent -- flagged here for whoever next touches select_exit(),
    # left unchanged per this plan's explicit scope boundary.
    wrap_non_best_group, wrap_non_best = if_block("Candidate Exit", 99, string="best-exit-placeholder")
    wrap_non_best["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    wrap_non_best["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Best Exit")
    a += [needs_wrap, wrap_non_best, set_var("Selected Exit", variable("Candidate Exit")), *number(1, "Exploration Selected"),
          otherwise(wrap_non_best_group), action("is.workflow.actions.nothing"), end_if(wrap_non_best_group),
          otherwise(needs_wrap_group), action("is.workflow.actions.nothing"), end_if(needs_wrap_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=wrap_loop, WFControlFlowMode=2),
          otherwise(explore_group), action("is.workflow.actions.nothing"), end_if(explore_group),
          otherwise(exploit_group), action("is.workflow.actions.nothing"), end_if(exploit_group)]
    suggestion = uid()
    a += [menu(suggestion, 0, prompt="Leave now", items=["Take suggested exit", "Choose another"]),
          menu(suggestion, 1, title="Take suggested exit")] + record_exit_and_route("Selected Exit")
    chooser = uid()
    a += [menu(suggestion, 1, title="Choose another"),
          action("is.workflow.actions.choosefromlist", UUID=chooser, WFInput=variable("Enabled Exits")),
          set_var("Selected Exit", output(chooser, "Chosen Item"))] + record_exit_and_route("Selected Exit") + [menu(suggestion, 2)]
    return a


def route_exit(choice_name: str):
    """All routes are first-party, non-contacting exits selected by state only."""
    a = [comment("Route the already-owned exit. Contacts opens Contacts only; no send, call, or message action exists.")]
    routes = {
        "Capture": [menu(uid(), 0, prompt="Capture", items=["Notes", "Voice Memos", "Camera"])],
        "Coordinate": [menu(uid(), 0, prompt="Coordinate", items=["Reminders", "Calendar"])],
        "Connect": [open_app("Contacts")],
        "Close": [action("is.workflow.actions.returntohomescreen")],
    }
    for name, actions in routes.items():
        group, check = if_block(choice_name, 4, string=name)
        a += [comment("Route check:\n- Compare the owned Selected Exit with this fixed first-party route.\n- The otherwise arm makes no route or state change."), check]
        if name == "Capture":
            capture = actions[0]["WFWorkflowActionParameters"]["GroupingIdentifier"]
            a += actions + [menu(capture, 1, title="Notes"), open_app("Notes"),
                            menu(capture, 1, title="Voice Memos"), open_app("Voice Memos"),
                            menu(capture, 1, title="Camera"), open_app("Camera"), menu(capture, 2)]
        elif name == "Coordinate":
            coordinate = actions[0]["WFWorkflowActionParameters"]["GroupingIdentifier"]
            a += actions + [menu(coordinate, 1, title="Reminders"), open_app("Reminders"),
                            menu(coordinate, 1, title="Calendar"), open_app("Calendar"), menu(coordinate, 2)]
        else:
            a += actions
        a += [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
    create_group, create = if_block(choice_name, 4, string="Create")
    a += [create] + read_value("profile_snapshot.create_target_url", variable("Reloaded State"), "Create Target URL")
    target_group, target = if_block("Create Target URL", 100)
    a += [target, action("is.workflow.actions.openurl", WFInput=variable("Create Target URL")), otherwise(target_group)]
    ask_id = uid()
    a += [action("is.workflow.actions.ask", UUID=ask_id, WFAskActionPrompt="Where should Create open?", WFInputType="URL"),
          set_var("Create Target URL", output(ask_id, "Provided Input"))]
    valid_group, valid = if_block("Create Target URL", 100)
    a += [valid, comment("Reload after Create input; stale sessions neither save the URL nor route it."), *reload_state(),
          *read_value("active_session.id", variable("Reloaded State"), "Create Owner ID")]
    create_owner_group, create_owner = if_block("Create Owner ID", 4, string="captured-session-placeholder")
    create_owner["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID")
    a += [create_owner, set_value("profile_snapshot.create_target_url", variable("Create Target URL"), "Reloaded State"),
          *save_state("Reloaded State"), action("is.workflow.actions.openurl", WFInput=variable("Create Target URL")),
          otherwise(create_owner_group), action("is.workflow.actions.nothing"), end_if(create_owner_group),
          otherwise(valid_group), alert("Create", "No target was saved or opened."), end_if(valid_group), end_if(target_group),
          otherwise(create_group), action("is.workflow.actions.nothing"), end_if(create_group)]
    consult_group, consult = if_block(choice_name, 4, string="Consult")
    consult_menu = uid()
    ask_query = uid()
    a += [consult, action("is.workflow.actions.ask", UUID=ask_query, WFAskActionPrompt="What are you trying to find?", WFInputType="Text"),
          set_var("Consult Query", output(ask_query, "Provided Input")),
          menu(consult_menu, 0, prompt="Consult", items=["Search Web", "Search Maps", "Open Notes", "Open Reminders", "Open Calendar", "Back"]),
          menu(consult_menu, 1, title="Search Web"), action("is.workflow.actions.searchweb", WFSearchWebDestination="Google", WFInputText=variable("Consult Query")),
          menu(consult_menu, 1, title="Search Maps"), action("is.workflow.actions.searchmaps", WFInput=variable("Consult Query"), WFSearchMapsActionApp="Maps"),
          menu(consult_menu, 1, title="Open Notes"), open_app("Notes"),
          menu(consult_menu, 1, title="Open Reminders"), open_app("Reminders"),
          menu(consult_menu, 1, title="Open Calendar"), open_app("Calendar"),
          menu(consult_menu, 1, title="Back"), action("is.workflow.actions.nothing"),
          menu(consult_menu, 2), otherwise(consult_group), action("is.workflow.actions.nothing"), end_if(consult_group)]
    return a


def record_exit_and_route(choice_name: str):
    """Reload, own, write one bounded event, then route from the fresh full State."""
    a = [comment("Record an exit only after reloading and proving the captured OPEN still owns State.")]
    a += reload_state() + read_value("active_session", variable("Reloaded State"), "Exit Active Session")
    active_group, active = if_block("Exit Active Session", 100)
    a += [active] + read_value("active_session.id", variable("Reloaded State"), "Exit Owner ID")
    owner_group, owner = if_block("Exit Owner ID", 4, string="captured-session-placeholder")
    owner["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID")
    a += read_value("last_app", variable("Reloaded State"), "Triggering App")
    event_text = text_token([('{"type":"', choice_name), ('","timestamp":', "Now Epoch"), (',"app":"', "Triggering App"), ('","circle":', "Circle Next"), (',"heat":', "Heat Final"), ('}', None)])
    event_json, event_dict = uid(), uid()
    # CYCLE 15: get_value(), not read_value(), for exit_events -- same compound-Array
    # class as recent_sessions, consumed below by Repeat With Each. NOTE (recorded,
    # not fixed this cycle): exit_events is also ABSENT from the bootstrap template
    # entirely (grep of src/PROSOCHE-Dumb.xml's state.json seed confirms no
    # "exit_events" key), a separate STATE-SHAPE gap in the same family as
    # KNOWN_SENTINEL_EXISTENCE_GATES. A flat read of a missing key returns nothing
    # (no error, per this session's verified iOS semantics), so this swap cannot
    # regress the pre-fix behaviour; it is not device-confirmed to fully resolve
    # this function, only to stop double-corrupting the type once a value exists.
    a += [owner, action("is.workflow.actions.gettext", UUID=event_json, WFTextActionText=event_text),
          action("is.workflow.actions.detect.dictionary", UUID=event_dict, WFInput=output(event_json, "Text")),
          set_var("Exit Event", output(event_dict, "Dictionary")), *get_value("exit_events", variable("Reloaded State"), "Exit Events")]
    a += [action("is.workflow.actions.appendvariable", WFInput=variable("Exit Event"), WFVariableName="Exit Events Next")]
    cap_loop = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=cap_loop, WFControlFlowMode=0, WFInput=variable("Exit Events"))]
    cap_group, cap = if_block("Repeat Index", 0, number=20)
    a += [cap, action("is.workflow.actions.appendvariable", WFInput=variable("Repeat Item"), WFVariableName="Exit Events Next"), otherwise(cap_group), action("is.workflow.actions.nothing"), end_if(cap_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=cap_loop, WFControlFlowMode=2)]
    # CYCLE 16: write the pending_exit LEAVES (.type, .timestamp), never the container
    # itself -- the container is a PERMANENT invariant established once by
    # seed_pending_exit() and must never again be replaced wholesale (the exact
    # cycle-10-finding-5 anti-pattern the old set_value("pending_exit", ...) reproduced
    # at the top level: complete_pending_exit() clears the container to the sentinel, and
    # a NEXT exit's dotted read of .type against a string parent would hard-error). Both
    # values are the same source variables event_text already interpolates into "Exit
    # Event" above, so this introduces no new value, only a different destination shape.
    a += [set_value("exit_events", variable("Exit Events Next"), "Reloaded State"),
          set_value("pending_exit.type", variable(choice_name), "Reloaded State"),
          set_value("pending_exit.timestamp", variable("Now Epoch"), "Reloaded State"),
          *read_value("exit_selection_counter", variable("Reloaded State"), "Reloaded Exit Counter")]
    # Condition 101 ("does not have any value") -- see the identical comment at
    # select_exit()'s "Exit Selection Counter" guard for why condition 5 vs an empty
    # string cannot work here.
    missing_counter, counter = if_block("Reloaded Exit Counter", 101)
    a += [counter] + number(0, "Reloaded Exit Counter") + [otherwise(missing_counter), action("is.workflow.actions.nothing"), end_if(missing_counter)]
    a += math("Reloaded Exit Counter", 1, "Exit Counter Next", "+") + [set_value("exit_selection_counter", variable("Exit Counter Next"), "Reloaded State")]
    a += save_state("Reloaded State") + route_exit(choice_name)
    a += [otherwise(owner_group), action("is.workflow.actions.nothing"), end_if(owner_group), otherwise(active_group), action("is.workflow.actions.nothing"), end_if(active_group)]
    return a


def universal_leaving():
    """Offer the Panic Escape bypass, or -- if the user removed it -- dispatch straight through.

    PHASE 11 (11-05), Build Addendum 01 §3.  "Panic Escape" is the `Leaving` case of the
    menu below: the easy behavioural bypass offered before every primitive, in every
    sequence and every Circle.  It is now REMOVABLE, gated on the first-class flat state
    field `panic_escape_enabled` (seeded by seed_panic_escape(), asserted by
    verify_panic_escape_seed()).

    PANIC ESCAPE IS NOT EMERGENCY RESTORE.  Emergency Restore is a SAFETY mechanism -- a
    MANUAL menu item (manual_emergency_restore()) and one of the two options inside the
    live-cooldown redirect (live_ice_redirect()).  Neither is represented by this flag,
    neither is enclosed by the conditional below, and neither may ever be gated on any
    Note-editable setting, Circle or Pressure value.  A user who has removed the bypass and
    cannot reach Emergency Restore is stranded inside an intervention; that is threat
    T-11-22, the only `critical` in this phase, and the separation is what mitigates it.

    MECHANISM A (11-RESEARCH.md §8.3), chosen over hoisting the dispatch out of the menu:
      If Panic Escape Enabled > 0   ->  the existing Leaving/Continue menu, unchanged
      Otherwise                     ->  primitive_dispatch(), the eleventh rendering
    Only the enabled arm emits the menu, so verify_circle_zero_silence() property (b) --
    EXACTLY ONE ["Leaving","Continue"] menu, enclosed by the `Circle Next > 0` band -- still
    holds.  universal_leaving() is called from inside that band (open_pipeline()), so BOTH
    arms of the new conditional inherit the enclosure, which is what keeps property (c) and
    docs/router_ui_census.py green for the otherwise arm's new dotted `sequences.` read.

    The gate is a NUMERIC "> 0" test, never a condition-100 existence test.  Per
    .claude/CLAUDE.md's device-verified runtime semantics a read-then-`has any value` gate
    is unimplementable on a dotted path and uninformative on a flat one, while "> 0" reads
    false for a JSON null, for the string "null" and for an empty string under every
    measured coercion -- the same idiom Setup Check already uses for its two epoch keys.

    COST, paid deliberately: the eleventh primitive_dispatch() rendering moves the two
    environmental site-count tables (docs/environmental_restore_check.py,
    docs/phase9_self_check.py) from ten renderings to eleven.  Both were moved to MEASURED
    values in the same commit, with their derivations rewritten.
    """
    group = uid()
    a = [comment(EXIT_MARKER + "\n\n- The session was saved before every interactive action.\n- Leaving -- Panic Escape -- is offered before every primitive whenever the user has kept it.\n- Continue reaches exactly the selected primitive.\n- A user who removed Panic Escape reaches that same primitive directly, with no menu.")]
    # Read the flag FLAT, from State.  A flat read of a missing key returns nothing and
    # cannot raise; a dotted read of a missing segment is a hard error, which is why this
    # field is deliberately top-level rather than nested under a settings object.
    a += read_value("panic_escape_enabled", variable("State"), "Panic Escape Enabled")
    panic_group, panic_if = if_block("Panic Escape Enabled", 2, number=0)
    a += [comment("Decide whether the Panic Escape bypass is still offered:\n"
                  "- Input is panic_escape_enabled, read flat from State directly above, compared numerically against zero.\n"
                  "- Greater than zero offers the Leaving/Continue menu exactly as before.\n"
                  "- Anything else -- zero, missing, null or empty -- goes straight to this Circle's intervention.\n"
                  "- Emergency Restore is NOT gated here and is not enclosed by this block; it stays reachable from the manual menu and from the cool-down redirect."),
          panic_if,
         # G-04-4b, revision 1: named the active Circle and stated that this menu belongs to
         # the OPEN path, so it could no longer be mistaken for a CLOSE-path signal.
         # G-04-4b, revision 2 (PHASE 10-01): revision 1 still named neither what is being
         # left nor what continuing costs -- "Leave now, or continue?" is only answerable by
         # someone who already knows the system. That terseness was affordable while this
         # menu fired on every single open, including the first of a cold day, where a long
         # prompt would have read as nagging. It no longer fires in the silent band
         # (Circle 0), so it now appears only once Pressure has genuinely built, at which
         # point the copy can afford to explain both options. Built with text_token(), which
         # computes the attachmentsByRange offsets -- never hand-edit the string.
         # "Circle Next" is already set (breadcrumb I, above) at every call site.
         menu(group, 0, prompt=text_token([("You just opened a tracked app. PROSOCHĒ is at Circle ", "Circle Next"),
                                            (".\n\nLeaving: PROSOCHĒ suggests somewhere better to go and takes you there.\n"
                                             "Continue: you go into the app, after this Circle's intervention.", None)]),
              items=["Leaving", "Continue"]), menu(group, 1, title="Leaving")]
    a += select_exit() + [menu(group, 1, title="Continue")] + primitive_dispatch() + [menu(group, 2)]
    a += [otherwise(panic_group),
          comment("Panic Escape was removed by the user, so no bypass is offered:\n"
                  "- This arm renders the SAME primitive dispatch the Continue case renders, verbatim, so no capture-and-restore gate is skipped.\n"
                  "- It is inside the Circle Next > 0 band with the arm above it, so a Circle-0 open still shows nothing.\n"
                  "- The user restores Panic Escape from the manual menu; this arm never writes the flag.")]
    a += primitive_dispatch()
    a += [end_if(panic_group), comment("--- PHASE 6 UNIVERSAL LEAVING END ---")]
    return a


def complete_pending_exit():
    """The one guarded genuine OPEN that follows an exit records its time away once."""
    a = [comment("--- PHASE 6 PENDING EXIT OUTCOME ---\n\n- This runs only after cooldown and duplicate OPEN guards.\n- A pending exit records one elapsed sample, then is cleared before the new session begins.")]
    # CYCLE 16: read pending_exit.type FIRST and gate on IT directly (condition 5, "is
    # not" the cleared sentinel) instead of a flat existence read of the "pending_exit"
    # container. The container is now a PERMANENT invariant (seed_pending_exit()): it is
    # never absent, so a condition-100 existence gate on it would never distinguish
    # "genuinely captured" from "cleared" (the sentinel is present and non-empty) -- the
    # exact GATE SEMANTICS failure verify_sentinel_gates() checks for. "Pending Exit
    # Type" is read once here and reused unmodified as the exit_stats.<type> key below;
    # no second read of it is needed.
    a += read_value("pending_exit.type", variable("State"), "Pending Exit Type")
    pending_group, pending = if_block("Pending Exit Type", 5, string=CLEARED_SENTINEL)
    a += [pending] + read_value("pending_exit.timestamp", variable("State"), "Pending Exit Timestamp")
    a += elapsed_since("Pending Exit Timestamp", "Return Seconds")
    # CYCLE 15: get_value(), not read_value() -- .samples is a compound Array
    # consumed below by Repeat With Each; read_value()'s gettext step would
    # stringify it. This site sits on the OPEN critical path (breadcrumb I->J),
    # reachable once a genuine pending_exit exists (second+ OPEN after an exit).
    a += get_value(text_token([("exit_stats.", "Pending Exit Type"), (".samples", None)]), variable("State"), "Exit Samples")
    a += [action("is.workflow.actions.appendvariable", WFInput=variable("Return Seconds"), WFVariableName="Exit Samples Next")]
    cap_loop = uid()
    a += [comment("Bound outcome samples:\n- Retain the just-recorded return duration.\n- Keep at most nineteen prior samples so the list never grows without bound."),
          action("is.workflow.actions.repeat.each", GroupingIdentifier=cap_loop, WFControlFlowMode=0, WFInput=variable("Exit Samples"))]
    cap_group, cap = if_block("Repeat Index", 0, number=20)
    a += [cap, action("is.workflow.actions.appendvariable", WFInput=variable("Repeat Item"), WFVariableName="Exit Samples Next"), otherwise(cap_group), action("is.workflow.actions.nothing"), end_if(cap_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=cap_loop, WFControlFlowMode=2)]
    a += read_value(text_token([("exit_stats.", "Pending Exit Type"), (".count", None)]), variable("State"), "Exit Count")
    a += read_value(text_token([("exit_stats.", "Pending Exit Type"), (".sum_return_seconds", None)]), variable("State"), "Exit Sum")
    a += math("Exit Count", 1, "Exit Count Next", "+") + math("Exit Sum", variable("Return Seconds"), "Exit Sum Next", "+")
    a += [set_value(text_token([("exit_stats.", "Pending Exit Type"), (".samples", None)]), variable("Exit Samples Next")),
          set_value(text_token([("exit_stats.", "Pending Exit Type"), (".count", None)]), variable("Exit Count Next")),
          set_value(text_token([("exit_stats.", "Pending Exit Type"), (".sum_return_seconds", None)]), variable("Exit Sum Next")),
          # Clear the LEAF, never the container -- clear_snapshot()'s own established
          # rule. .timestamp is deliberately left stale: it is read nowhere outside this
          # same branch, which this very clear makes unreachable on the next OPEN.
          set_value("pending_exit.type", cleared_value()),
          otherwise(pending_group), action("is.workflow.actions.nothing"), end_if(pending_group),
          comment("--- PHASE 6 PENDING EXIT OUTCOME END ---")]
    return a


def config(key: str, name: str):
    return read_value(key, variable("Config"), name)


def open_pipeline():
    a = [comment("""--- OPEN STATE ENGINE ---

- Start from the loaded full State dictionary and the shared run clock.
- A duplicate or active cooldown changes no Heat; a genuine open writes one final State.
- The persisted Circle is arithmetic only; Phase 5 attaches behaviour at the marker below.""")]
    # Read all mutable fields before any state mutation; null values are guarded.
    a += read_value("behavioural_day", variable("State"), "Stored Day")
    a += read_value("last_open_at", variable("State"), "Last Open")
    a += read_value("last_close_at", variable("State"), "Last Close")
    a += read_value("cooldown_until", variable("State"), "Cooldown Until")
    a += config("heat.open_base", "Open Base") + config("heat.floor", "Heat Floor") + config("heat.cap", "Heat Cap")
    a += config("heat.decay_interval_seconds", "Decay Interval") + config("heat.decay_amount", "Decay Amount")
    a += config("heat.reopen_under_120s_bonus", "Reopen 120 Bonus") + config("heat.reopen_under_600s_bonus", "Reopen 600 Bonus")
    a += config("heat.reopen_bonus_mode", "Reopen Bonus Mode") + config("heat.overrun_penalty", "Overrun Penalty")
    a += config("heat.overrun_ratio", "Overrun Ratio") + config("heat.overrun_min_seconds", "Overrun Minimum")
    a += config("heat.contract_respected_relief", "Respect Relief") + config("gravity.opens_per_point", "Opens Per Gravity") + config("gravity.cap", "Gravity Cap")
    # Behavioural day rollover is the first state update (only opens_today resets).
    # Condition 101 ("does not have any value") -- see the identical comment at
    # select_exit()'s "Exit Selection Counter" guard for why condition 5 vs an empty
    # string cannot work here.
    g, start = if_block("Stored Day", 101)
    a += [comment("""Check whether a saved behavioural day exists before comparing it to today:
- A missing value is treated as rollover so the counter is safe on migrated state.
- A present value continues to the same-day comparison below.
- Only opens_today is reset; Heat and histories remain untouched."""), start]
    a += number(0, "Zero") + [set_value("opens_today", variable("Zero")), set_value("behavioural_day", variable("Behavioural Day")), otherwise(g)]
    day_group, day_if = if_block("Stored Day", 4, string="same-day-placeholder")
    day_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    day_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Behavioural Day")
    # The explicit Text variable is compared as a string to the Behavioural Day token.
    a += [comment("""Compare the stored behavioural day with today's adjusted day:
- Both values are text, so equality is the supported string comparison.
- A different day resets only opens_today and records today's key.
- A matching day leaves the counter intact."""), day_if, otherwise(day_group)]
    a += number(0, "Zero") + [set_value("opens_today", variable("Zero")), set_value("behavioural_day", variable("Behavioural Day")), end_if(day_group), end_if(g)]
    # Cooldown and debounce each choose their own genuine no-inflation branch.
    a += [comment("""Short-circuit a live cooldown before any Heat arithmetic:
- Input is the saved cooldown deadline routed through text.
- A future deadline leaves Heat and the open count unchanged, then records the state once.
- Otherwise the regular duplicate guard and OPEN pipeline continue.""")]
    cooldown_group, cooldown_if = if_block("Cooldown Until", 2, number=variable("Now Epoch"))
    a += [cooldown_if] + save_state() + [otherwise(cooldown_group)]
    a += [comment("""Debounce duplicate OPEN triggers with the saved last-open timestamp:
- A short repeat OPEN is not a new interaction and takes the no-mutation path.
- A genuine later OPEN continues to ordered Heat arithmetic.
- This is timestamp comparison only, not a second event system.""")]
    # Prototype 2-second debounce: config intentionally has no debounce field.
    a += number(1, "Genuine Open")
    debounce_exists, debounce_exists_if = if_block("Last Open", 100)
    a += [debounce_exists_if] + elapsed_since("Last Open", "Seconds Since Open")
    debounce_group, debounce_if = if_block("Seconds Since Open", 0, number=2)
    a += [comment("Duplicate OPEN guard (prototype 2 seconds):\n- Compare the elapsed seconds from the captured last-open timestamp.\n- A value below two exits through Nothing with no dictionary mutation.\n- A later event continues to the complete Heat pipeline."), debounce_if,
          *number(0, "Genuine Open"), otherwise(debounce_group), action("is.workflow.actions.nothing"), end_if(debounce_group), otherwise(debounce_exists), action("is.workflow.actions.nothing"), end_if(debounce_exists)]
    genuine_group, genuine = if_block("Genuine Open", 2, number=0)
    a += [genuine]
    # Current state values are loaded only after the short circuit branches.
    a += read_value("heat", variable("State"), "Heat Current") + read_value("opens_today", variable("State"), "Opens Today")
    a += [comment("""Compute Heat in its required order, then clamp it last:
- Decay applies first from time away, then base OPEN and the exclusive/cumulative reopen rule.
- Previous overrun or respected contract adjustment follows the reopen adjustment.
- Floor and cap are the final two guards before Gravity and Pressure.""")]
    # Decay uses the previous genuine close; absent first-run values leave Heat intact.
    a += [set_var("Heat After Decay", variable("Heat Current"))]
    decay_exists, decay_exists_if = if_block("Last Close", 100)
    a += [decay_exists_if] + elapsed_since("Last Close", "Seconds Away") + math("Seconds Away", variable("Decay Interval"), "Decay Intervals Raw", "÷") + round_down("Decay Intervals Raw", "Decay Intervals") + math("Decay Intervals", variable("Decay Amount"), "Decay Delta", "×") + math("Heat After Decay", variable("Decay Delta"), "Heat After Decay") + [otherwise(decay_exists), action("is.workflow.actions.nothing"), end_if(decay_exists)]
    a += math("Heat After Decay", variable("Open Base"), "Heat After Base")
    # Reopen bands read their seconds from the same real last-close timestamp.
    reopen120, if120 = if_block("Last Close", 100)
    a += [if120] + elapsed_since("Last Close", "Seconds Since Close")
    under120_g, under120_if = if_block("Seconds Since Close", 0, number=120)
    exclusive_g, exclusive_if = if_block("Reopen Bonus Mode", 4, string="exclusive")
    a += [under120_if, exclusive_if] + math("Heat After Base", variable("Reopen 120 Bonus"), "Heat After Reopen") + [otherwise(exclusive_g)] + math("Heat After Base", variable("Reopen 120 Bonus"), "Heat After Reopen") + math("Heat After Reopen", variable("Reopen 600 Bonus"), "Heat After Reopen") + [end_if(exclusive_g), otherwise(under120_g)]
    under600_g, under600_if = if_block("Seconds Since Close", 0, number=600)
    a += [under600_if] + math("Heat After Base", variable("Reopen 600 Bonus"), "Heat After Reopen") + [otherwise(under600_g), set_var("Heat After Reopen", variable("Heat After Base")), end_if(under600_g), end_if(under120_g), otherwise(reopen120), set_var("Heat After Reopen", variable("Heat After Base")), end_if(reopen120)]
    # Previous session's recorded overrun is the cross-run contract signal.
    # CYCLE 15 -- CONFIRMED ROOT CAUSE of the breadcrumb E->F device failure
    # ("Get Dictionary Value failed because Shortcuts couldn't convert Text to
    # Dictionary"): get_value(), not read_value(). recent_sessions is a compound
    # Array of session dictionaries; read_value()'s gettext step stringified it
    # into one Text blob, so the getitemfromlist "First Item" below returned that
    # same Text blob (not a genuine Dictionary item), and the very next
    # getvalueforkey read against it (Previous Session's declared_duration_seconds)
    # then failed exactly as reported. See get_value()'s docstring for the full
    # trace and the write-side symmetry evidence.
    a += get_value("recent_sessions", variable("State"), "Recent Sessions")
    session_exists, session_exists_if = if_block("Recent Sessions", 100)
    first_session = uid()
    a += [session_exists_if, action("is.workflow.actions.getitemfromlist", UUID=first_session, WFItemSpecifier="First Item", WFInput=variable("Recent Sessions")), set_var("Previous Session", output(first_session, "Item from List"))]
    a += read_value("declared_duration_seconds", variable("Previous Session"), "Previous Declared Duration") + read_value("respected", variable("Previous Session"), "Previous Respected") + read_value("overrun_seconds", variable("Previous Session"), "Previous Overrun")
    has_previous_contract_g, has_previous_contract = if_block("Previous Declared Duration", 2, number=0)
    respected_g, respected_if = if_block("Previous Respected", 4, string="true")
    overrun_g, overrun_if = if_block("Previous Overrun", 2, number=variable("Overrun Minimum"))
    a += [has_previous_contract, respected_if] + math("Heat After Reopen", variable("Respect Relief"), "Heat After Contract") + [otherwise(respected_g), overrun_if] + math("Heat After Reopen", variable("Overrun Penalty"), "Heat After Contract") + [otherwise(overrun_g), set_var("Heat After Contract", variable("Heat After Reopen")), end_if(overrun_g), end_if(respected_g), otherwise(has_previous_contract_g), set_var("Heat After Contract", variable("Heat After Reopen")), end_if(has_previous_contract_g), otherwise(session_exists), set_var("Heat After Contract", variable("Heat After Reopen")), end_if(session_exists)]
    # Clamp lower then upper, deliberately the last Heat mutations.
    floor_g, floor_if = if_block("Heat After Contract", 0, number=variable("Heat Floor"))
    a += [floor_if, set_value("heat", variable("Heat Floor")), otherwise(floor_g), set_value("heat", variable("Heat After Contract")), end_if(floor_g)]
    a += read_value("heat", variable("State"), "Heat Clamped")
    cap_g, cap_if = if_block("Heat Clamped", 2, number=variable("Heat Cap"))
    a += [cap_if, set_value("heat", variable("Heat Cap")), otherwise(cap_g), action("is.workflow.actions.nothing"), end_if(cap_g)]
    # Genuine OPEN writes active session and all derived fields to the same rooted State dictionary.
    a += math("Opens Today", variable("Open Base"), "Opens Today Next")
    a += [set_value("opens_today", variable("Opens Today Next")), set_value("last_open_at", variable("Now Epoch")), set_value("last_app", text_token([("tracked", None)]))]
    random_id, session_id = uid(), uid()
    # Random Number takes WFRandomNumberMinimum/WFRandomNumberMaximum (ToolKit v78
    # catalog); WFNumberMin/WFNumberMax are not parameters of this action.
    a += [action("is.workflow.actions.number.random", UUID=random_id,
                 WFRandomNumberMinimum=1, WFRandomNumberMaximum=2147483647),
          set_var("Random Suffix", output(random_id, "Random Number")),
          action("is.workflow.actions.gettext", UUID=session_id,
                 WFTextActionText=text_token([("session-", "Now Epoch"), ("-", None), ("", "Random Suffix")])),
          set_var("Session ID", output(session_id, "Text"))]
    session_text = text_token([('{"id":"', "Session ID"), ('","started_at":', "Now Epoch"), (',"declared_duration_seconds":0}', None)])
    session_json = uid()
    a += [action("is.workflow.actions.gettext", UUID=session_json, WFTextActionText=session_text),
          action("is.workflow.actions.detect.dictionary", UUID=uid(), WFInput=output(session_json, "Text"))]
    # Detect Dictionary output cannot safely be re-derived from action position: name it immediately.
    a += [set_var("Active Session Next", output(a[-1]["WFWorkflowActionParameters"]["UUID"], "Dictionary")), set_value("active_session", variable("Active Session Next"))]
    # Gravity = floor(opens / config divisor), bounded by config cap. The Math division yields the documented integer conversion.
    a += math("Opens Today Next", variable("Opens Per Gravity"), "Gravity Raw", "÷")
    gravity_g, gravity_if = if_block("Gravity Raw", 2, number=variable("Gravity Cap"))
    a += [gravity_if, set_value("gravity", variable("Gravity Cap")), otherwise(gravity_g), set_value("gravity", variable("Gravity Raw")), end_if(gravity_g)]
    a += read_value("heat", variable("State"), "Heat Final") + read_value("gravity", variable("State"), "Gravity Final")
    a += math("Heat Final", variable("Gravity Final"), "Pressure Next") + [set_value("pressure", variable("Pressure Next"))]
    # Ordered nine-item threshold scan.
    a += read_value("profile", variable("State"), "Profile")
    a += [comment("""Resolve Circle by an ordered nine-step threshold scan:
- Start at Circle 0 and use the active profile's Config threshold list.
- Each satisfied greater-than-or-equal comparison overwrites Circle with the current index.
- Ascending thresholds make the final satisfied index the correct Circle; no numeric equality is used.
- An unmet first threshold leaves Circle at 0, the silent band, in which nothing is shown.""")]
    a += number(0, "Circle Next")
    scan = uid()
    a += [action("is.workflow.actions.repeat.count", GroupingIdentifier=scan, WFControlFlowMode=0, WFRepeatCount=9)]
    threshold_id = uid()
    a += [action("is.workflow.actions.getvalueforkey", UUID=threshold_id,
                 WFDictionaryKey=text_token([("thresholds.", "Profile"), (".", None), ("", "Repeat Index")]), WFInput=variable("Config")),
          action("is.workflow.actions.gettext", UUID=uid(), WFTextActionText=output(threshold_id, "Dictionary Value"))]
    threshold_text_uuid = a[-1]["WFWorkflowActionParameters"]["UUID"]
    a += [set_var("Threshold", output(threshold_text_uuid, "Text"))]
    hit_g, hit_if = if_block("Pressure Next", 3, number=variable("Threshold"))
    a += [hit_if, set_var("Circle Next", variable("Repeat Index")), otherwise(hit_g), action("is.workflow.actions.nothing"), end_if(hit_g),
          action("is.workflow.actions.repeat.count", UUID=uid(), GroupingIdentifier=scan, WFControlFlowMode=2)]
    a += [set_value("circle", variable("Circle Next")), set_value("behavioural_day", variable("Behavioural Day"))]
    a += complete_pending_exit()
    # State is persisted before any menu/Ask action. The wrapper owns all later interaction.
    # save_state() stays OUTSIDE the silent-band gate: Circle 0 must still accumulate and
    # persist behavioural day, Heat, Gravity, Pressure, open count and the active session.
    a += save_state()
    silent_group, silent_if = if_block("Circle Next", 2, number=0)
    a += [comment("""Circle 0 is the silent band: state has already been saved directly above, and nothing at all is shown below it.
- Everything user-facing on the OPEN path -- the Leaving/Continue menu and every primitive -- lives inside universal_leaving(), so gating that one call suppresses every surface at once.
- This gate is also a correctness requirement, not only a UX one: primitive_dispatch() reads sequences.<Sequence>.<Dispatch Circle> as a DOTTED key, and at index 0 the final segment is absent, which iOS raises as a hard "could not evaluate the key path" error -- after active_session was already written, leaving a session no CLOSE would ever own.
- Enforced structurally by verify_circle_zero_silence(); do not move universal_leaving() back outside this block.""")]
    a += [silent_if] + universal_leaving() + [otherwise(silent_group), action("is.workflow.actions.nothing"), end_if(silent_group)]
    a += [end_if(genuine_group), end_if(cooldown_group)]
    return a


def close_pipeline():
    a = [comment("""--- CLOSE SESSION PIPELINE ---

- Capture the active session from the entry State, wait briefly, then reload the file.
- A newer OPEN wins by session ID and takes a genuine no-write path.
- Only the matching owner appends a bounded record, clears the session, restores settings, and saves once.""")]
    a += read_value("active_session", variable("State"), "Entry Active Session")
    has_g, has_if = if_block("Entry Active Session", 100)
    a += [has_if]
    # Nested reads happen only after the parent exists.
    a += read_value("active_session.id", variable("State"), "Captured Session ID") + read_value("active_session.started_at", variable("State"), "Captured Start")
    a += [comment("""Let an interleaved OPEN claim state before ownership is checked:
- The captured ID and start remain the entry snapshot.
- State is read fresh from disk after the brief wait.
- No write occurs before the ownership comparison."""), action("is.workflow.actions.delay", WFDelayTime=0.5)]
    re_file, re_dict = uid(), uid()
    a += [action("is.workflow.actions.documentpicker.open", UUID=re_file, WFFileErrorIfNotFound=False, WFGetFilePath="PROSOCHE/state.json", WFShowFilePicker=False),
          action("is.workflow.actions.detect.dictionary", UUID=re_dict, WFInput=output(re_file, "File")),
          set_var("Reloaded State", output(re_dict, "Dictionary"))]
    a += read_value("active_session", variable("Reloaded State"), "Reloaded Active Session")
    reload_g, reload_if = if_block("Reloaded Active Session", 100)
    a += [reload_if] + read_value("active_session.id", variable("Reloaded State"), "Reloaded Session ID")
    owns_g, owns_if = if_block("Reloaded Session ID", 4, string="captured-session-placeholder")
    owns_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    owns_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Captured Session ID")
    a += [comment("""Compare the reloaded active session with the captured owner:
- A matching ID means this CLOSE still owns the session.
- A different ID means a newer OPEN owns state; this otherwise branch is intentionally Nothing only.
- The sole CLOSE save action is nested in the matching branch."""), owns_if]
    # Owner branch operates only on Reloaded State, preserving unrelated fields from the fresh dictionary.
    a += math("Now Epoch", variable("Captured Start"), "Session Duration", "-")
    a += read_value("active_session.declared_duration_seconds", variable("Reloaded State"), "Declared Duration")
    a += [comment(CONTRACT_MARKER + """

- Compare the measured duration with any declared contract:
- A zero or absent declared duration has no contract penalty.
- A genuine overrun is recorded in the session object for the next OPEN.
- The configured penalty is applied by OPEN, preserving its ordered Heat pipeline.""")]
    has_contract_g, has_contract = if_block("Declared Duration", 2, number=0)
    a += [has_contract] + math("Session Duration", variable("Declared Duration"), "Overrun Seconds", "-")
    respected_g, respected_if = if_block("Overrun Seconds", 1, number=0)
    respected_true, respected_false = uid(), uid()
    no_overrun, no_respected = uid(), uid()
    a += [comment("Contract outcome:\n- A non-positive overrun is respected only when a contract exists.\n- No declared duration stores null and never shows an overrun result."), respected_if,
          action("is.workflow.actions.gettext", UUID=respected_true, WFTextActionText="true"),
          set_var("Contract Respected", output(respected_true, "Text")),
          otherwise(respected_g), action("is.workflow.actions.gettext", UUID=respected_false, WFTextActionText="false"),
          set_var("Contract Respected", output(respected_false, "Text")), end_if(respected_g),
          otherwise(has_contract_g), action("is.workflow.actions.gettext", UUID=no_overrun, WFTextActionText="null"), set_var("Overrun Seconds", output(no_overrun, "Text")),
          action("is.workflow.actions.gettext", UUID=no_respected, WFTextActionText="null"), set_var("Contract Respected", output(no_respected, "Text")), end_if(has_contract_g)]
    record_text = text_token([('{"id":"', "Captured Session ID"), ('","started_at":', "Captured Start"), (',"ended_at":', "Now Epoch"), (',"duration_seconds":', "Session Duration"), (',"declared_duration_seconds":', "Declared Duration"), (',"overrun_seconds":', "Overrun Seconds"), (',"respected":', "Contract Respected"), ('}', None)])
    record_json, record_dict = uid(), uid()
    a += [action("is.workflow.actions.gettext", UUID=record_json, WFTextActionText=record_text),
          action("is.workflow.actions.detect.dictionary", UUID=record_dict, WFInput=output(record_json, "Text")),
          set_var("Session Record", output(record_dict, "Dictionary"))]
    # CYCLE 15: get_value(), not read_value() -- same class as the OPEN-pipeline
    # recent_sessions site above; consumed below by Repeat With Each.
    a += get_value("recent_sessions", variable("Reloaded State"), "Recent Sessions")
    # Newest-first rolling window: this record plus only the first 19 prior ones.
    a += [action("is.workflow.actions.appendvariable", WFInput=variable("Session Record"), WFVariableName="Recent Sessions Next")]
    window = uid()
    a += [comment("""Keep recent sessions bounded at twenty records:
- Append the completed record first so it is the newest entry.
- Copy only prior entries whose repeat index is below twenty.
- The final list therefore contains at most one new plus nineteen older records."""),
          action("is.workflow.actions.repeat.each", GroupingIdentifier=window, WFControlFlowMode=0, WFInput=variable("Recent Sessions"))]
    keep_g, keep_if = if_block("Repeat Index", 0, number=20)
    a += [keep_if, action("is.workflow.actions.appendvariable", WFInput=variable("Repeat Item"), WFVariableName="Recent Sessions Next"), otherwise(keep_g), action("is.workflow.actions.nothing"), end_if(keep_g),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=window, WFControlFlowMode=2)]
    a += [set_value("recent_sessions", variable("Recent Sessions Next"), "Reloaded State"),
          set_value("last_close_at", variable("Now Epoch"), "Reloaded State"),
          set_value("active_session", cleared_value(), "Reloaded State")]
    display_contract_g, display_contract = if_block("Declared Duration", 2, number=0)
    a += [comment("Contract result display:\n- Only sessions with a declared boundary show contract feedback.\n- Sessions without one make no overrun claim."), display_contract,
          alert("Contract", text_token([("Overrun seconds: ", "Overrun Seconds")])), otherwise(display_contract_g), action("is.workflow.actions.nothing"), end_if(display_contract_g)]
    a += [comment(RESTORE_MARKER + "\n\n- Only the matching CLOSE owner restores captured settings.\n- A superseded CLOSE reaches no restore or Save File action.")]
    a += restore_managed_settings("Reloaded State") + [comment("--- PHASE 5 RESTORE MANAGED SETTINGS END ---")]
    # Permanent, unconditional CLOSE confirmation -- fires whenever this CLOSE owns
    # the session, independent of whether a contract was declared (unlike the
    # "Contract" alert above, which only fires when Declared Duration > 0). G-04-4b.
    a += [notification("PROSOCHĒ", text_token([("Session closed · ", "Session Duration"), (" sec", None)]))]
    a += save_state("Reloaded State") + [otherwise(owns_g), action("is.workflow.actions.nothing"), end_if(owns_g), otherwise(reload_g), action("is.workflow.actions.nothing"), end_if(reload_g), otherwise(has_g), action("is.workflow.actions.nothing"), end_if(has_g)]
    return a


def comment_index(actions, prefix: str):
    for index, candidate in enumerate(actions):
        if (candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.comment"
                and candidate.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "").startswith(prefix)):
            return index
    raise SystemExit(f"semantic marker not found: {prefix}")


def replace_marker_block(actions, start: str, end: str, replacement):
    """Replace a named generated region without depending on its action number."""
    begin = comment_index(actions, start)
    try:
        finish = comment_index(actions[begin + 1:], end) + begin + 1
    except SystemExit:
        # The Phase 3/4 hooks are a single comment before their first expansion.
        finish = begin
    actions[begin:finish + 1] = replacement


def replace_branch_body(actions, marker: str, route_marker: str, replacement):
    """Replace a router arm without consuming its enclosing Otherwise branch."""
    begin = comment_index(actions, marker)
    route = comment_index(actions, route_marker)
    outer_start = next(item for item in reversed(actions[:begin])
                       if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
                       and item.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 0)
    outer_group = outer_start["WFWorkflowActionParameters"]["GroupingIdentifier"]
    outer_otherwise = next(index for index in range(begin, route)
                           if actions[index].get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
                           and actions[index].get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 1
                           and actions[index].get("WFWorkflowActionParameters", {}).get("GroupingIdentifier") == outer_group)
    actions[begin:outer_otherwise] = replacement


def remove_marker_block(actions, start: str, end: str):
    """Remove one named generated region, wherever an earlier build put it."""
    try:
        begin = comment_index(actions, start)
    except SystemExit:
        return
    finish = comment_index(actions[begin + 1:], end) + begin + 1
    del actions[begin:finish + 1]


def insert_or_replace_after(actions, anchor: str, start: str, end: str, replacement):
    """Keep ordinary one-location generated blocks adjacent to their anchor."""
    try:
        replace_marker_block(actions, start, end, replacement)
    except SystemExit:
        at = comment_index(actions, anchor)
        actions[at + 1:at + 1] = replacement


def flow_index(actions, group: str, mode: int):
    """Index of one endpoint of a named control-flow block."""
    for index, item in enumerate(actions):
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("GroupingIdentifier") == group and parameters.get("WFControlFlowMode") == mode:
            return index
    raise SystemExit(f"control-flow group {group} has no mode {mode} endpoint")


def input_key_tests(actions):
    """Every conditional that tests the normalised Input Key, in document order."""
    found = []
    for index, item in enumerate(actions):
        parameters = item.get("WFWorkflowActionParameters", {})
        if (item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
                and parameters.get("WFControlFlowMode") == 0
                and parameters.get("WFInput", {}).get("Variable", {})
                              .get("Value", {}).get("VariableName") == "Input Key"):
            found.append((index, parameters.get("WFCondition"),
                          parameters.get("WFConditionalActionString")))
    return found


def find_absence_gate(actions):
    """Index of the legacy 'Input Key has any value' gate, or None once it is gone."""
    for index, condition, _ in input_key_tests(actions):
        if condition == 100:
            return index
    return None


# The routing overview comment that replaces the one explaining the deleted gate.  The
# skill requires a repair-oriented bulleted comment immediately before every control-flow
# start; this is that comment for the OPEN test.
ROUTER_OVERVIEW = """Route this run by POSITIVE identification of the normalised Input Key, never by its absence:
- Input Key is built just above by composing the Shortcut Input into text, trimming surrounding whitespace, then uppercasing the result.
- If Input Key is exactly OPEN this is Automation A; if it is exactly CLOSE this is Automation B; anything else — including a plain manual tap with no input at all — is a manual run and falls through to the MANUAL menu.
- This deliberately does NOT gate on "Input Key has any value". That earlier gate assumed an absent Shortcut Input normalises to a completely empty string. It does not: once Trim Whitespace and Change Case were given the text serialization iOS actually reads, the empty case stopped being empty, the gate passed, and every manual tap was rejected as unrecognised input. Absence is not a reliable signal; presence is.
- A mis-typed automation therefore reaches the manual menu rather than an explicit rejection. That is intended: the menu is inert until the person chooses something, so no phantom open is ever injected into Heat or Pressure."""

ROUTE_FALLBACK_COMMENT = ROUTE_FALLBACK_MARKER + """, so this run is MANUAL.
- A plain manual tap sends no Shortcut Input at all and lands here, which is the normal first-run case for a freshly imported Shortcut, before either Personal Automation exists.
- A stray or mis-typed caller also lands here. Nothing below reads, writes, or mutates anything until the person picks a menu item, so an unrecognised caller still injects no event into Heat or Pressure.
- OPEN and CLOSE never reach this arm."""


def restructure_router(actions):
    """Route on positive identification (OPEN / CLOSE / else MANUAL), not on absence.

    Before:  If Input Key HAS ANY VALUE -> If OPEN | If CLOSE | unrecognised alert
             Otherwise                  -> MANUAL
    After:   If OPEN -> OPEN | Otherwise If CLOSE -> CLOSE | Otherwise -> MANUAL

    The old shape made manual invocation depend on the normalised input being byte-empty.
    That held only by accident: Trim Whitespace and Change Case carried bare
    WFTextTokenAttachments and their output evaporated. Correcting those envelopes made
    the empty case non-empty, so the gate passed and every manual tap hit the
    unrecognised-input fail-safe. The new shape is correct for EVERY value the empty case
    can take, which is the point — it does not require knowing what that value is.

    Both literal comparisons on the automation path are carried over untouched: the same
    conditionals, the same cond-4 tests against OPEN and CLOSE, the same bodies. Those
    arms simply lose one enclosing level.

    Idempotent: returns immediately once the absence gate is gone.
    """
    gate = find_absence_gate(actions)
    if gate is None:
        return
    gate_group = actions[gate]["WFWorkflowActionParameters"]["GroupingIdentifier"]
    gate_else, gate_end = flow_index(actions, gate_group, 1), flow_index(actions, gate_group, 2)
    fallback = comment_index(actions, ROUTE_FALLBACK_MARKER)
    close_else = actions[fallback - 1]
    close_parameters = close_else.get("WFWorkflowActionParameters", {})
    if not (close_else.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
            and close_parameters.get("WFControlFlowMode") == 1):
        raise SystemExit("the routing fallback comment is not the first action of the CLOSE Otherwise arm")
    close_end = flow_index(actions, close_parameters["GroupingIdentifier"], 2)
    manual = actions[gate_else + 1:gate_end]
    if not (gate < fallback < close_end < gate_else < gate_end) or not manual:
        raise SystemExit("unexpected router topology; refusing to restructure")
    overview = gate - 1
    if actions[overview].get("WFWorkflowActionIdentifier") != "is.workflow.actions.comment":
        raise SystemExit("no routing overview comment precedes the input gate")
    actions[overview] = comment(ROUTER_OVERVIEW)
    actions[fallback] = comment(ROUTE_FALLBACK_COMMENT)
    actions[:] = (actions[:gate]                    # everything up to and including the overview
                  + actions[gate + 1:fallback + 1]  # OPEN and CLOSE arms, ending at the fallback comment
                  + manual                          # MANUAL now occupies the CLOSE Otherwise arm
                  + actions[close_end:gate_else]    # the CLOSE and OPEN End Ifs, in order
                  + actions[gate_end + 1:])         # anything that followed the old gate's End If


def verify_router_shape(actions):
    """Fail the build if manual invocation is ever gated on absence of input again.

    This is the recurrence guard for cycle 3. The defect class is "the router treats an
    empty normalised input as its manual signal", which is invisible to the validator and
    only shows up as a device-visible regression one round-trip later.
    """
    if find_absence_gate(actions) is not None:
        raise SystemExit("router gates MANUAL on 'Input Key has any value': manual invocation must be "
                         "the non-matching fallback, never the empty case (see restructure_router)")
    literals = [(condition, string) for _, condition, string in input_key_tests(actions)]
    if literals != [(4, "OPEN"), (4, "CLOSE")]:
        raise SystemExit(f"router must test Input Key against OPEN then CLOSE only, found {literals}")
    close_index = input_key_tests(actions)[1][0]
    close_group = actions[close_index]["WFWorkflowActionParameters"]["GroupingIdentifier"]
    manual = comment_index(actions, MANUAL_MARKER)
    if not flow_index(actions, close_group, 1) < manual < flow_index(actions, close_group, 2):
        raise SystemExit("the MANUAL arm must sit inside the CLOSE conditional's Otherwise branch")


# Every identifier that opens (mode 0) and closes (mode 2) a control-flow block.  Used to
# compute enclosure structurally rather than by action index, which shifts on every rebuild.
CONTROL_FLOW_IDENTIFIERS = {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count",
                            "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}


def enclosing_groups(actions):
    """For each action, the list of control-flow GroupingIdentifiers enclosing it.

    One left-to-right pass maintaining a stack.  A mode-2 endpoint pops before it is
    recorded, so an End If is reported outside its own block; a mode-0 start pushes after
    it is recorded, so an If is likewise reported outside itself.  Everything between them
    -- which is the only thing any caller here asks about -- reports the block as enclosing.
    """
    stack, out = [], []
    for index, item in enumerate(actions):
        parameters = item.get("WFWorkflowActionParameters", {})
        identifier = item.get("WFWorkflowActionIdentifier")
        mode = parameters.get("WFControlFlowMode")
        if identifier in CONTROL_FLOW_IDENTIFIERS and mode == 2 and stack:
            stack.pop()
        out.append(tuple(stack))
        if identifier in CONTROL_FLOW_IDENTIFIERS and mode == 0:
            stack.append(parameters.get("GroupingIdentifier"))
    return out


def _is_silent_band_conditional(item):
    """A mode-0 If testing `Circle Next > 0` -- the Circle-0 silent-band gate."""
    parameters = item.get("WFWorkflowActionParameters", {})
    return (item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
            and parameters.get("WFControlFlowMode") == 0
            and parameters.get("WFCondition") == 2
            and parameters.get("WFNumberValue") == 0
            and parameters.get("WFInput", {}).get("Variable", {})
                          .get("Value", {}).get("VariableName") == "Circle Next")


def _dictionary_key_string(parameters):
    """The literal text of a WFDictionaryKey, whether a plain string or a text token."""
    key = parameters.get("WFDictionaryKey")
    if isinstance(key, str):
        return key
    if isinstance(key, dict):
        return key.get("Value", {}).get("string", "")
    return ""


def verify_circle_zero_silence(actions):
    """Fail the build if a Circle-0 OPEN can reach any surface, or primitive_dispatch().

    Symptom this prevents: a genuine OPEN whose Pressure is below the active profile's
    first threshold resolves to Circle 0.  If universal_leaving() still ran there,
    primitive_dispatch() would read `sequences.<Sequence>.<Dispatch Circle>` as a DOTTED
    key with Dispatch Circle == 0.  Per CLAUDE.md's device-verified runtime semantics a
    dotted read whose final segment is absent is a HARD ERROR ("could not evaluate the key
    path") -- and it would fire after active_session was already written, leaving a session
    that no CLOSE will ever own.  mirror_text()'s Get Item From List at WFItemIndex 0 is
    out of range on the same path.  Neither failure is visible to validate_shortcut.py.

    Four properties, each with its own message:
      (a) the Circle scan seeds at 0, not 1;
      (b) the Leaving/Continue menu -- the OPEN path's sole entry point to every primitive
          -- is enclosed by the silent-band conditional;
      (c) every sequences-addressing dotted read INSIDE THE OPEN ARM is enclosed by that
          same conditional group;
      (d) the OPEN arm emits no notification.

    TEST-A-CIRCLE EXEMPTION, deliberate and load-bearing.  Property (c) is scoped to the
    OPEN arm and must NOT be rewritten as an artifact-wide invariant.  There are ten
    sequences reads in the artifact: one in the OPEN arm from universal_leaving(), and nine
    in the MANUAL arm from primitive_dispatch("Test Circle"), rendered once per Circle by
    the Test-a-Circle submenu.  Those nine are correctly outside any silent-band
    conditional and must stay that way -- their Dispatch Circle is copied from Test Circle,
    which is always 1 through 9, so index 0 is unreachable there by construction.  An
    artifact-wide assertion would raise on the very first build.
    """
    # (a) the scan floor.
    seeds = [index for index, item in enumerate(actions)
             if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
             and item.get("WFWorkflowActionParameters", {}).get("WFVariableName") == "Circle Next"
             and index > 0
             and actions[index - 1].get("WFWorkflowActionIdentifier") == "is.workflow.actions.number"]
    if len(seeds) != 1:
        raise SystemExit("Circle floor: expected exactly one number-seeded 'Circle Next' set-variable, "
                         f"found {len(seeds)}")
    seed_value = actions[seeds[0] - 1]["WFWorkflowActionParameters"].get("WFNumberActionNumber")
    if seed_value != 0:
        raise SystemExit(f"Circle floor: the Circle scan seeds at {seed_value!r}, must be 0 -- a seed of 1 "
                         "abolishes the silent band and shows a surface on the very first open of the day")

    # The OPEN arm's boundaries, derived structurally the same way verify_router_shape does.
    open_test = next(((index, string) for index, condition, string in input_key_tests(actions)
                      if condition == 4 and string == "OPEN"), None)
    if open_test is None:
        raise SystemExit("silent band: no conditional tests Input Key against the OPEN literal; the router "
                         "has been restructured and this guard can no longer locate the OPEN arm")
    open_index = open_test[0]
    open_group = actions[open_index]["WFWorkflowActionParameters"]["GroupingIdentifier"]
    open_end = flow_index(actions, open_group, 1)
    enclosure = enclosing_groups(actions)

    silent_group_ids = {item["WFWorkflowActionParameters"]["GroupingIdentifier"]
                        for item in actions if _is_silent_band_conditional(item)}

    # (b) the Leaving / Continue menu.
    menus = [index for index, item in enumerate(actions)
             if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.choosefrommenu"
             and item.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 0
             and item.get("WFWorkflowActionParameters", {}).get("WFMenuItems") == ["Leaving", "Continue"]]
    if len(menus) != 1:
        raise SystemExit(f"silent band: expected exactly one Leaving/Continue menu, found {len(menus)}")
    menu_bands = {group for group in enclosure[menus[0]] if group in silent_group_ids}
    if not menu_bands:
        raise SystemExit("silent band: the Leaving/Continue menu is not enclosed by a 'Circle Next > 0' "
                         "conditional, so a Circle-0 OPEN would show a menu and reach every primitive")

    # (c) the dotted sequences read, OPEN arm only -- see the Test-a-Circle exemption above.
    for index in range(open_index, open_end):
        item = actions[index]
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.getvalueforkey":
            continue
        if not _dictionary_key_string(item.get("WFWorkflowActionParameters", {})).startswith("sequences."):
            continue
        if not ({group for group in enclosure[index] if group in silent_group_ids} & menu_bands):
            raise SystemExit("silent band: an OPEN-arm dotted read of the sequences subtree escapes the "
                             "'Circle Next > 0' conditional; at Circle 0 its final segment is absent and "
                             "iOS raises 'could not evaluate the key path' after active_session was written")

    # (d) no OPEN-path notification.
    banners = [index for index in range(open_index, open_end)
               if actions[index].get("WFWorkflowActionIdentifier") == "is.workflow.actions.notification"]
    if banners:
        raise SystemExit(f"silent band: the OPEN arm emits {len(banners)} notification(s); no OPEN of any "
                         "kind may produce a Circle/pressure/heat banner")


# ---------------------------------------------------------------------------
# BD-06 Decision 5 -- the EIGHTH defect class, alongside the seven parameter-defect axes
# recorded in .claude/CLAUDE.md.  Each of those seven is a parameter whose SHAPE is wrong.
# This one is different in kind: two independently well-formed halves that no longer agree
# with each other.  The name primitive_dispatch() writes into the Selected Primitive
# variable, and the name it compares that variable against, are produced by two different
# sources -- the Config literal's `sequences` arrays and the generator's own branch tuple --
# and nothing at run time reconciles them.  iOS merely compares two strings.

# The variable primitive_dispatch() writes the looked-up sequence entry into, and the one
# every dispatch arm tests.  A NAME, not a code: see verify_dispatch_coverage()'s docstring.
SELECTED_PRIMITIVE = "Selected Primitive"


def verify_dispatch_coverage(actions):
    """Fail the build if any sequence entry dispatches nothing, or any branch is unnamed.

    BD-06 Decision 5 states the invariant: every distinct primitive name appearing in any
    `sequences` array must have EXACTLY ONE matching dispatch branch, and every dispatch
    branch must be named by at least one sequence entry.

    Why this needs a build guard at all.  A dispatch entry that matches no branch produces
    no error anywhere -- the Circle silently does nothing, the run completes, State is
    written, and the user sees an ordinary open.  It is invisible to validate_shortcut.py,
    to the ToolKit catalog, and to decrypting the signed artifact, because all three see a
    structurally perfect plist.  That is exactly how Circle 8 shipped dead for four phases:
    the entry "Voice" named no emitted branch and matched nothing, with no error anywhere.

    Four distinct failure classes, each with its own message:
      orphan      -- a sequence component that no branch resolves for;
      unreachable -- a distinct branch name that no component resolves for;
      unknown     -- a branch whose matching rule cannot be resolved, either because its
                     condition code is one neither rule knows or because its comparison
                     target is not a plain literal;
      duplicate   -- a component matched by more than one DISTINCT branch name.  Distinct
                     NAMES are counted, never action instances: each branch name is
                     legitimately rendered once per primitive_dispatch() rendering, so an
                     instance count is not the invariant BD-06 states.

    Matching semantics are resolved PER BRANCH from that branch's own WFCondition and never
    from a hardcoded constant -- 99 is "contains", 4 is "string is".  Hardcoding either
    would make this guard silently wrong on the exact commit that changes the code it
    hardcoded, which is the one commit it most needs to be right on.
    """
    literals = [item["WFWorkflowActionParameters"]["WFTextActionText"] for item in actions
                if item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.gettext"
                and isinstance(item.get("WFWorkflowActionParameters", {}).get("WFTextActionText"), str)
                and '"config_version"' in item["WFWorkflowActionParameters"]["WFTextActionText"]]
    if len(literals) != 1:
        raise SystemExit(
            f"dispatch coverage: found {len(literals)} Config JSON literal(s) -- a gettext whose "
            "WFTextActionText is a plain string containing config_version -- and exactly 1 is "
            "required.  Zero means this guard silently checks nothing and every sequence entry "
            "goes unverified; more than one means it would check an arbitrary member of a set "
            "the caller did not know existed")
    try:
        config = json.loads(literals[0])
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"dispatch coverage: the Config literal is not parseable JSON ({error}) -- "
            "detect.dictionary consumes it at run time, so an unparseable literal means the "
            "whole Config subtree, not merely the dispatch surface, is unreadable on device")

    # Every distinct name any sequence names, with where it names it.  Split on '+'
    # unconditionally: a name with no '+' yields itself, so this reads a legacy combined
    # entry correctly and FAILS on it rather than silently mis-parsing it as one name.
    components: dict[str, list[str]] = {}
    for sequence, entries in config.get("sequences", {}).items():
        for position, entry in enumerate(entries, start=1):
            for component in str(entry).split("+"):
                component = component.strip()
                if component:
                    components.setdefault(component, []).append(f"{sequence} (Circle {position})")

    # NO FILTERING BY CONDITION CODE.  Excluding a branch here because its code is
    # unfamiliar would make an unrecognised dispatch scheme look like an empty dispatch
    # surface -- the precise silent failure this guard exists to expose.
    branches = []
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFControlFlowMode") != 0:
            continue
        variable_name = (parameters.get("WFInput", {}).get("Variable", {})
                         .get("Value", {}).get("VariableName"))
        if variable_name != SELECTED_PRIMITIVE:
            continue
        code = parameters.get("WFCondition")
        tested = parameters.get("WFConditionalActionString")
        if not isinstance(tested, str):
            strategy = "unknown"
        elif code == 99:      # "contains": the tested string need only appear inside the entry
            strategy = "contains"
        elif code == 4:       # "string is": the tested string must equal the entry exactly
            strategy = "exact"
        else:
            strategy = "unknown"
        branches.append((tested, code, strategy))

    def resolving_names(component: str) -> set:
        """The distinct branch NAMES that fire for this sequence component."""
        names = set()
        for tested, _code, strategy in branches:
            if strategy == "contains" and tested in component:
                names.add(tested)
            elif strategy == "exact" and tested == component:
                names.add(tested)
        return names

    unknown = [(tested, code) for tested, code, strategy in branches if strategy == "unknown"]
    if unknown:
        raise SystemExit(
            f"dispatch coverage: {len(unknown)} dispatch branch(es) have unresolvable matching "
            f"semantics {sorted(set(unknown), key=repr)} -- a condition code neither 99 "
            "('contains') nor 4 ('string is'), or a comparison target that is not a plain "
            "literal.  Guessing which rule applies would let this guard report a clean "
            "dispatch surface it never actually checked")

    orphans = sorted(name for name in components if not resolving_names(name))
    if orphans:
        detail = "; ".join(f"{name!r} at {', '.join(components[name])}" for name in orphans)
        raise SystemExit(
            f"dispatch coverage: {len(orphans)} sequence entr(y/ies) dispatch NOTHING -- {detail}.  "
            "An undispatched entry is a silent runtime no-op: the Circle produces no "
            "intervention, no error and no log, which is how Circle 8 shipped dead for four "
            "phases.  It is invisible to validate_shortcut.py, to the ToolKit catalog and to "
            "the signed-artifact decrypt, so this build guard is the only place it can be "
            "caught.  Either add the branch to primitive_dispatch()'s name tuple or correct "
            "the name in the Config literal's sequences array -- never relax this guard")

    duplicates = sorted(name for name in components if len(resolving_names(name)) > 1)
    if duplicates:
        detail = "; ".join(f"{name!r} matched by {sorted(resolving_names(name))}" for name in duplicates)
        raise SystemExit(
            f"dispatch coverage: {len(duplicates)} sequence entr(y/ies) match MORE THAN ONE "
            f"distinct dispatch branch -- {detail}.  BD-06 Decision 5 requires exactly one.  "
            "Under condition 99 ('contains') a branch fires whenever its name is a substring "
            "of the entry, so an entry silently runs two interventions back to back and the "
            "user sees the wrong Circle.  Move the dispatch to condition 4 ('string is') or "
            "rename the colliding branch")

    named = set()
    for name in components:
        named |= resolving_names(name)
    unreachable = sorted({tested for tested, _code, _strategy in branches} - named)
    if unreachable:
        raise SystemExit(
            f"dispatch coverage: {len(unreachable)} dispatch branch(es) {unreachable} are named "
            "by NO sequence entry.  Dead generated code is not harmless here: it is the "
            "signature of a half-applied rename, where the tuple moved and the Config literal "
            "did not, and the matching orphan on the other side is the Circle that now "
            "dispatches nothing.  Name it in a sequence or stop emitting it")


def install_cooldown_branches(actions):
    """Install Ice only in the true/otherwise arms of the named cooldown If."""
    # Removing both first repairs builds made by the earlier broad-anchor helpers.
    # Expiry may have been nested inside the live block, so remove the outer block first.
    remove_marker_block(actions, LIVE_ICE_MARKER, "--- PHASE 5 LIVE ICE REDIRECT END ---")
    remove_marker_block(actions, EXPIRY_MARKER, "--- PHASE 5 ICE EXPIRY END ---")
    at = comment_index(actions, "Short-circuit a live cooldown")
    cooldown_index, cooldown_action = next(
        ((index, candidate) for index, candidate in enumerate(actions[at + 1:], at + 1)
         if candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
         and candidate.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 0
         and candidate.get("WFWorkflowActionParameters", {}).get("WFInput", {}).get("Variable", {})
         .get("Value", {}).get("VariableName") == "Cooldown Until"),
        (None, None),
    )
    if cooldown_action is None:
        raise SystemExit("named live cooldown conditional not found")
    actions[cooldown_index + 1:cooldown_index + 1] = live_ice_redirect()
    group = cooldown_action["WFWorkflowActionParameters"]["GroupingIdentifier"]
    for index, candidate in enumerate(actions[at + 1:], start=at + 1):
        params = candidate.get("WFWorkflowActionParameters", {})
        if (candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
                and params.get("GroupingIdentifier") == group and params.get("WFControlFlowMode") == 1):
            actions[index + 1:index + 1] = ice_expiry()
            return
    raise SystemExit("live cooldown Otherwise path not found")


def live_ice_redirect():
    group = uid()
    a = [comment(LIVE_ICE_MARKER + "\n\n- A live cooldown routes away before OPEN arithmetic.\n- Emergency Restore is available even during Ice.\n- This branch uses the existing single Save File below."),
         # User-visible prompt only.  LIVE_ICE_MARKER and every "Ice ..." variable name around
         # it are structural anchors and stay as they are; BD-06 renames the shipped primitive
         # to "Frozen", not the generator's internals.
         menu(group, 0, prompt="Frozen is active", items=["Return Home", "Emergency Restore"]),
         menu(group, 1, title="Return Home"), action("is.workflow.actions.returntohomescreen"),
         menu(group, 1, title="Emergency Restore")]
    a += restore_managed_settings("State")
    a += [set_value("cooldown_until", text_token([("null", None)])),
          set_value("active_session", cleared_value()),
          menu(group, 2), comment("--- PHASE 5 LIVE ICE REDIRECT END ---")]
    return a


def ice_expiry():
    a = [comment(EXPIRY_MARKER + "\n\n- A past cooldown restores captured settings before normal OPEN work.\n- Clear cooldown only after restoration.\n- Apply the configured Heat relief and clamp it." )]
    a += restore_managed_settings("State")
    a += [set_value("cooldown_until", text_token([("null", None)]))]
    a += config("heat.ice_expiry_relief", "Ice Expiry Relief") + config("heat.floor", "Heat Floor")
    a += read_value("heat", variable("State"), "Heat Before Ice Relief")
    a += math("Heat Before Ice Relief", variable("Ice Expiry Relief"), "Heat After Ice Relief")
    floor_g, floor_if = if_block("Heat After Ice Relief", 0, number=variable("Heat Floor"))
    a += [floor_if, set_value("heat", variable("Heat Floor")), otherwise(floor_g),
          set_value("heat", variable("Heat After Ice Relief")), end_if(floor_g),
          comment("--- PHASE 5 ICE EXPIRY END ---")]
    return a


def manual_emergency_restore():
    group = uid()
    choices = ["Status", "Open Control Room", "Sync My Profile", "Change Profile", "Change Sequence", "Toggle Voice", "Test a Circle", "Reset Today", "Emergency Restore", "Setup Check"]
    a = [comment(MANUAL_MARKER + "\n\n- Manual control is the only path that refreshes the Control Room or reads its proforma.\n- OPEN and CLOSE never enter this menu or parse the Note.\n- Test Circle copies recorded values into test variables and never writes Pressure.\n- CYCLE 14 (checkpoint decision): Status and Open Control Room are read-only. Neither sets Manual Refresh Requested; only explicit state-changing choices (Sync My Profile, Change Profile, Change Sequence, Toggle Voice, Reset Today, Emergency Restore) append to the Note."),
         # PHASE 10 (10-02): the prompt was the bare product name, which told a user who
         # arrived here unintentionally nothing at all.  A plain str is correct for
         # WFMenuPrompt when nothing is interpolated -- the "Choose profile" and "Choose
         # sequence" submenus below use the same form.  It names the fall-through case
         # explicitly: this menu is where a run lands when the Shortcut is run by hand AND
         # when an automation passed anything other than the two recognised inputs (the
         # router's CLOSE Otherwise branch).  That is a deliberate routing tradeoff, not a
         # defect, so the honest fix is to say so rather than to restructure the router --
         # verify_router_shape() hard-fails the build on any such restructuring.
         menu(group, 0, prompt="This is PROSOCHĒ's manual control menu. You are here because the Shortcut was run by hand, or because an automation passed it something other than OPEN or CLOSE. If you did not mean to be here, choose Open Control Room — that Note has the setup instructions.", items=choices)]
    # CYCLE 14 -- checkpoint decision: "Open Control Room" is decoupled from the
    # refresh-append mechanism entirely (read-only; the common tail below still finds
    # or creates the note, but never appends a snapshot).
    # "Status" gets its own read path (Manual Status Requested), so it isn't left
    # without a mechanism -- see manual_note_refresh() for the display branch.
    # PHASE 10 (10-02) amendment: "Open Control Room" is STILL read-only with respect
    # to the Note -- it sets no Manual Refresh Requested and appends nothing -- but it
    # is no longer a bare Nothing riding on an unconditional tail.  It now carries its
    # own request flag, Manual Show Note Requested, and gate_control_room_shownote()
    # makes the single is.workflow.actions.shownote depend on it, so the other nine
    # menu items no longer end by launching the Notes app.  The note itself is still
    # found or created unconditionally below, so BOOT-08's deleted-note self-heal and
    # manual_note_refresh()'s "Control Room Note" binding are both unaffected.
    a += [menu(group, 1, title="Status"), *number(1, "Manual Status Requested")]
    a += [menu(group, 1, title="Open Control Room"), *number(1, "Manual Show Note Requested")]
    a += [menu(group, 1, title="Sync My Profile"), *number(1, "Manual Refresh Requested"), *number(1, "Manual Sync Requested")]
    profile_menu = uid()
    # BD-06-A1: the middle profile is `Purgatory`, not `Limbo`.  Items and case titles both
    # come from PROFILE_NAMES so they cannot drift, and the chosen literal is written
    # straight into `profile`, which is then read back as `thresholds.<profile>` -- a dotted
    # path, so a name here that no threshold key matches is a hard runtime error.
    a += [menu(group, 1, title="Change Profile"), menu(profile_menu, 0, prompt="Choose profile", items=list(PROFILE_NAMES))]
    for profile in PROFILE_NAMES:
        text_id = uid()
        a += [menu(profile_menu, 1, title=profile), action("is.workflow.actions.gettext", UUID=text_id, WFTextActionText=profile), set_var("Manual Profile", output(text_id, "Text")), set_value("profile", variable("Manual Profile")), *number(1, "Manual Refresh Requested"), *save_state()]
    a += [menu(profile_menu, 2)]
    sequence_menu = uid()
    a += [menu(group, 1, title="Change Sequence"), menu(sequence_menu, 0, prompt="Choose sequence", items=["Classic", "BlackMirror", "Ambient"])]
    for sequence in ("Classic", "BlackMirror", "Ambient"):
        text_id = uid()
        a += [menu(sequence_menu, 1, title=sequence), action("is.workflow.actions.gettext", UUID=text_id, WFTextActionText=sequence), set_var("Manual Sequence", output(text_id, "Text")), set_value("sequence", variable("Manual Sequence")), *number(1, "Manual Refresh Requested"), *save_state()]
    a += [menu(sequence_menu, 2), menu(group, 1, title="Toggle Voice")]
    a += read_value("voice_enabled", variable("State"), "Manual Voice")
    voice_g, voice_if = if_block("Manual Voice", 2, number=0)
    a += [voice_if, *number(0, "Manual Voice Next"), otherwise(voice_g), *number(1, "Manual Voice Next"), end_if(voice_g), set_value("voice_enabled", variable("Manual Voice Next")), *number(1, "Manual Refresh Requested"), *save_state()]
    test_menu = uid()
    # Items and case titles BOTH come from circle_menu_title(), so they are the same list in
    # the same order by construction -- see CIRCLE_NAMES.  Do not hand-write either.  This
    # submenu sits in the MANUAL arm, so surfacing the Dante names here adds no OPEN-arm
    # surface and cannot touch Circle 0's silent band (verify_circle_zero_silence()).
    a += [menu(group, 1, title="Test a Circle"), menu(test_menu, 0, prompt="Test a Circle", items=[circle_menu_title(number) for number in range(1, 10)])]
    for test_circle in range(1, 10):
        a += [menu(test_menu, 1, title=circle_menu_title(test_circle)), *number(test_circle, "Test Circle")]
        a += read_value("pressure", variable("State"), "Pressure Next") + read_value("heat", variable("State"), "Heat Final") + read_value("circle", variable("State"), "Circle Next")
        a += [set_var("Circle Next", variable("Test Circle")), comment("Test Circle uses a copied Circle value:\n- Pressure remains the saved recorded value.\n- This branch does not set or save Pressure.\n- Chosen Circle behaviour runs with the copied value only.")] + primitive_dispatch("Test Circle")
    a += [menu(test_menu, 2), menu(group, 1, title="Reset Today"), *number(0, "Manual Zero"), set_value("opens_today", variable("Manual Zero")), set_value("gravity", variable("Manual Zero")), *number(1, "Manual Refresh Requested"), *save_state(), menu(group, 1, title="Emergency Restore")]
    a += restore_managed_settings("State")
    a += [set_value("cooldown_until", text_token([("null", None)])),
          set_value("active_session", cleared_value()), *number(1, "Manual Refresh Requested")]
    a += save_state()
    # PHASE 10 (10-02): the tenth item.  Emitted last so the case order matches the
    # choices order element for element -- a choosefrommenu whose case titles drift from
    # its WFMenuItems order is CONTROL_FLOW.md's top documented real-world failure mode.
    # Read-only, like Status: it sets no Manual Refresh Requested and appends nothing.
    a += [menu(group, 1, title="Setup Check"), *number(1, "Manual Setup Check Requested")]
    a += [menu(group, 2), comment("--- PHASE 5 MANUAL EMERGENCY RESTORE END ---")]
    return a


def manual_note_refresh():
    """Append current settings/state only after an explicit manual menu choice."""
    a = [comment("--- PHASE 7 MANUAL CONTROL ROOM REFRESH ---\n\n- This runs after the Note is found or created in the MANUAL branch only.\n- It appends a factual current snapshot and meaningful manual events.\n- OPEN never reaches this Note parsing or append block.\n- Status is read-only (Manual Status Requested): it displays the snapshot directly and never appends to the Note.")]
    for key, name in (("fork", "Snapshot Fork"), ("profile", "Snapshot Profile"), ("sequence", "Snapshot Sequence"), ("voice_enabled", "Snapshot Voice"), ("pressure", "Snapshot Pressure"), ("circle", "Snapshot Circle"), ("cooldown_until", "Snapshot Cooldown"), ("profile_snapshot.enabled_exits", "Snapshot Exits")):
        a += read_value(key, variable("State"), name)
    # PHASE 10 (10-02) -- Setup Check reads the two epoch keys the engine already writes:
    # last_open_at (open_pipeline(), on a genuine open) and last_close_at (close_pipeline(),
    # on an owning close).  Both are FLAT single-segment keys, so per CLAUDE.md's verified
    # runtime semantics a read cannot hard-error even on a legacy state.json predating them
    # -- a missing flat key simply returns nothing.  read_value(), never get_value():
    # get_value() is reserved for COMPOUND_STATE_KEYS, and these are numeric leaves.
    a += read_value("last_open_at", variable("State"), "Setup Last Open")
    a += read_value("last_close_at", variable("State"), "Setup Last Close")
    refresh_g, refresh_if = if_block("Manual Refresh Requested", 2, number=0)
    snapshot_id = uid()
    snapshot = text_token([("\n\n## CURRENT SETTINGS\n- Fork: ", "Snapshot Fork"), ("\n- Profile: ", "Snapshot Profile"), ("\n- Sequence: ", "Snapshot Sequence"), ("\n- Voice: ", "Snapshot Voice"), ("\n- AI: not used by this fork\n- Enabled exits: ", "Snapshot Exits"), ("\n\n## CURRENT STATE\n- Circle (0 means the silent band: PROSOCHĒ recorded the open and showed nothing) — ", "Snapshot Circle"), ("\n- Pressure: ", "Snapshot Pressure"), ("\n- Cool-down until: ", "Snapshot Cooldown"), ("\n\n## ATTENTION LEDGER\n- Manual Control Room refresh at ", "Now Epoch")])
    a += [refresh_if, action("is.workflow.actions.gettext", UUID=snapshot_id, WFTextActionText=snapshot), action("is.workflow.actions.appendnote", operation="append", entity=variable("Control Room Note"), text=output(snapshot_id, "Text")), otherwise(refresh_g), action("is.workflow.actions.nothing"), end_if(refresh_g)]
    # CYCLE 14 -- checkpoint decision: Status gets its own read-only display branch.
    # It reuses the SAME Snapshot* variables read unconditionally above (no new
    # dictionary reads) and shows them via the already-verified alert() helper
    # (is.workflow.actions.alert, VERIFIED_PARAMETER_KEYS since cycle 1) instead of
    # appendnote -- Status never writes to the Note.
    status_g, status_if = if_block("Manual Status Requested", 2, number=0)
    a += [status_if, comment("Status is read-only:\n- Displays the current snapshot directly, via an alert.\n- Never appends to or otherwise writes the Note."),
          alert("Status", text_token([("Fork: ", "Snapshot Fork"), ("\nProfile: ", "Snapshot Profile"), ("\nSequence: ", "Snapshot Sequence"), ("\nVoice: ", "Snapshot Voice"), ("\nCircle (0 means the silent band: recorded, nothing shown): ", "Snapshot Circle"), ("\nPressure: ", "Snapshot Pressure"), ("\nCool-down until: ", "Snapshot Cooldown")])),
          otherwise(status_g), action("is.workflow.actions.nothing"), end_if(status_g)]
    # PHASE 10 (10-02) -- Setup Check: did the two Personal Automations the user built by
    # hand actually fire?  Derived, not stored: no new state key, no bootstrap-template
    # edit, no schema_version bump.  Each verdict is a numeric "> 0" test on the epoch,
    # NEVER a condition-100 existence test -- that is the axis-7 gate-semantics trap
    # verify_sentinel_gates() exists to prevent, and a numeric "> 0" reads false for a
    # JSON null, for the string "null" and for an empty string under every device-measured
    # coercion, while every value ever written to these keys is a strictly positive epoch.
    for read_name, verdict_name, automation in (("Setup Last Open", "Setup Open Verdict", "A"),
                                                ("Setup Last Close", "Setup Close Verdict", "B")):
        seen_id, unseen_id = uid(), uid()
        verdict_g, verdict_if = if_block(read_name, 2, number=0)
        a += [comment(f"Decide whether Automation {automation} has ever been recorded firing:\n"
                      f"- Input is the stored epoch read above, compared numerically against zero.\n"
                      "- A positive epoch means PROSOCHĒ has written it at least once.\n"
                      "- Anything else -- missing, null or empty -- reads as not yet seen, never as an error."),
              verdict_if,
              action("is.workflow.actions.gettext", UUID=seen_id, WFTextActionText="seen"),
              set_var(verdict_name, output(seen_id, "Text")),
              otherwise(verdict_g),
              action("is.workflow.actions.gettext", UUID=unseen_id, WFTextActionText="not seen yet"),
              set_var(verdict_name, output(unseen_id, "Text")),
              end_if(verdict_g)]
    setup_g, setup_if = if_block("Manual Setup Check Requested", 2, number=0)
    a += [setup_if, comment("Setup Check is read-only:\n- Displays the two derived verdicts directly, via an alert.\n- Never appends to or otherwise writes the Note, and sets no refresh flag.\n- Reports what PROSOCHĒ has recorded, which is sufficient evidence but not necessary evidence."),
          alert("Setup Check", text_token([
              ("Automation A — App Is Opened, passing OPEN: ", "Setup Open Verdict"),
              ("\nAutomation B — App Is Closed, passing CLOSE: ", "Setup Close Verdict"),
              ("\n\nThis reports whether PROSOCHĒ has ever recorded a genuine open or an owning close. A close that a newer open superseded, or an open during a cool-down, records nothing — so a \"not seen yet\" verdict can be wrong, but a \"seen\" verdict never is.", None)])),
          otherwise(setup_g), action("is.workflow.actions.nothing"), end_if(setup_g)]
    sync_g, sync_if = if_block("Manual Sync Requested", 2, number=0)
    text_id, match_id = uid(), uid()
    a += [sync_if, comment("Sync My Profile parses only the editable proforma between its two headings:\n- Input is the selected Control Room Note from this manual run.\n- No OPEN action can enter this branch.\n- The extracted text is saved with its sync time."), action("is.workflow.actions.gettext", UUID=text_id, WFTextActionText=variable("Control Room Note")), action("is.workflow.actions.text.match", UUID=match_id, WFMatchTextPattern="(?s)## MY PHONE, ON PURPOSE.*?(?=## CURRENT SETTINGS)", text=output(text_id, "Text")), set_value("profile_snapshot.proforma", output(match_id, "Matched Text")), set_value("profile_snapshot.synced_at", variable("Now Epoch")), *save_state(), otherwise(sync_g), action("is.workflow.actions.nothing"), end_if(sync_g), comment("--- PHASE 7 MANUAL CONTROL ROOM REFRESH END ---")]
    return a


def normalize_setters(actions):
    """Set Dictionary Value returns a full dictionary; rebind it exactly once."""
    normalized, index = [], 0
    while index < len(actions):
        candidate = actions[index]
        normalized.append(candidate)
        params = candidate.get("WFWorkflowActionParameters", {})
        source = params.get("WFDictionary", {}).get("Value", {})
        target = source.get("VariableName")
        if candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvalueforkey" and target:
            following = actions[index + 1] if index + 1 < len(actions) else None
            follows_setter = (following and following.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
                               and following.get("WFWorkflowActionParameters", {}).get("WFVariableName") == target
                               and following.get("WFWorkflowActionParameters", {}).get("WFInput", {}).get("Value", {}).get("OutputUUID") == params.get("UUID"))
            normalized.append(set_var(target, output(params["UUID"], "Dictionary")))
            if follows_setter:
                index += 1
        index += 1
    actions[:] = normalized


# Parameter keys verified against the Shortcuts Playground ToolKit v78 first-party
# catalog (data/toolkit-v78-first-party-parameter-keys.json), each confirmed present
# on "iOS 27 Simulator".  The bundled validator cannot catch parameter-key drift at
# --target-macos 26 because it never loads that catalog, so this build-time guard is
# the only MANDATORY gate standing between a renamed key and a runtime
# "No value provided".
#
# 2026-08-17 (quick task 260817-ewg) -- corrected.  The first half above still holds:
# gate A (--target-macos 26 --target-platform all) genuinely loads no parameter-key or
# enum-case catalog.  The "only gate" claim did not: gate B
# (--target-macos 27 --target-platform all) DOES load that catalog, and measured, it is
# precisely what surfaced the com.apple.mobilenotes.SharingExtension WFCreateNoteInput
# divergence this file deliberately retains on donor evidence.  Gate B is a second,
# ADVISORY gate -- it carries a permanent waiver, can never exit 0, and must never be
# chained into a definition of done.  Two-gate rule: .claude/CLAUDE.md §1
# "Exact validator invocation"; measurements: docs/BUILD-NOTES.md §22.
VERIFIED_PARAMETER_KEYS = {
    "is.workflow.actions.setvalueforkey": {"WFDictionaryKey", "WFDictionaryValue", "WFDictionary"},
    "is.workflow.actions.getvalueforkey": {"WFGetDictionaryValueType", "WFDictionaryKey", "WFInput"},
    "is.workflow.actions.number.random": {"WFRandomNumberMinimum", "WFRandomNumberMaximum"},
    "is.workflow.actions.setvariable": {"WFInput", "WFVariableName"},
    "is.workflow.actions.gettext": {"WFTextActionText"},
    "is.workflow.actions.text.trimwhitespace": {"WFInput"},
    "is.workflow.actions.text.changecase": {"text", "WFCaseType", "ShowWhenRun"},
    # count: catalog defines WFCountType + Input.  WFInput is NOT defined and is therefore
    # ignored by iOS; it is retained deliberately (extra keys are provably inert here -- see
    # WFShowFilePicker / ShowWhenRun / WFAppIdentifier on device-proven working paths) so the
    # input binds whichever key iOS actually reads.
    "is.workflow.actions.count": {"WFCountType", "Input", "WFInput"},
    "is.workflow.actions.getitemfromlist": {"WFItemSpecifier", "WFItemIndex",
                                            "WFItemRangeStart", "WFItemRangeEnd", "WFInput"},
    "is.workflow.actions.speaktext": {"WFText", "WFSpeakTextWait", "WFSpeakTextRate",
                                      "WFSpeakTextPitch", "WFSpeakTextLanguage",
                                      "WFSpeakTextVoice"},
    # CYCLE 14 -- Donor 8 (device ground truth): shownote reads WFInput.  This artifact's
    # one shownote site carried `target`, a key the action does not define at all -- the
    # exact same axis-1 defect class as the 147 sites fixed in cycle 1, on a hand-authored
    # site outside every prior sweep.  fix_shownote_key() corrects it; this entry is the
    # recurrence guard so the wrong key can never ship silently again.
    "is.workflow.actions.shownote": {"WFInput"},
    # CYCLE 16 -- Donor 8 (device ground truth): filter.notes ("Find Notes") as genuinely
    # authored on the target iPhone carries AppIntentDescriptor and an explicit
    # WFContentItemLimitEnabled/WFContentItemLimitNumber result bound. This artifact's one
    # filter.notes site (same hand-authored block as shownote above) carried neither --
    # fix_notes_filter_limit() adds them; this entry is the recurrence guard so they can
    # never be silently dropped again.
    "is.workflow.actions.filter.notes": {"AppIntentDescriptor", "WFContentItemFilter",
                                         "WFContentItemLimitEnabled", "WFContentItemLimitNumber"},
}
STRUCTURAL_KEYS = {"UUID", "GroupingIdentifier", "WFControlFlowMode", "CustomOutputName"}

# Parameters whose iOS type is a plain string.  A string-typed parameter must carry
# a WFTextTokenString (a "￼" placeholder plus attachmentsByRange); a bare
# WFTextTokenAttachment is accepted by the importer and by the bundled validator but
# resolves to EMPTY at run time.  That silent-empty behaviour is what produced all
# three reported failures, and the artifact itself contains the control group:
# every path that worked already used WFTextTokenString on its string parameter
# (the state.json template, the Shortcut Input read, the Control Room body), while
# every path that failed used a bare attachment.
#
# Evidence per entry -- catalog type is "str" in the ToolKit v78 first-party
# parameter catalog for all of them, plus:
#   gettext.WFTextActionText        36/36 golden-corpus actions use WFTextTokenString, 0 use attachment
#   text.match.text                  8/8 golden-corpus actions use WFTextTokenString
#   alert.WFAlertActionMessage       8/8 golden corpus + VARIABLES.md display-parameter table
#   text.trimwhitespace.WFInput      by analogue with text.replace.WFInput (3/3 golden) and
#                                    BEST_PRACTICES.md: Replace Text WFInput must not be a bare attachment
#   text.changecase.text             by analogue with text.match.text
#   setvalueforkey.WFDictionaryValue no golden instance exists; catalog type "str" and this is the
#                                    exact action named in the reported runtime error
#   searchweb.WFInputText            no golden instance exists; catalog type "str" -- DEVIATION, see below
#
# Deliberately EXCLUDED despite a "str" catalog type, because the golden corpus shows
# real shortcuts using a bare attachment there and corpus evidence outranks catalog
# inference: openurl.WFInput (2/2 attachment), text.combine.text (4/4), text.split.text (4/4).
# Float/File/Placemark/content-item parameters are excluded for the same reason -- the
# corpus uses attachments for those.
#
# CYCLE 4 -- the same rule extends to catalog type "AttributedString", which the original
# allowlist missed because it was scoped to "str" alone.  AttributedString is a TEXT type,
# not a content item, so it needs the placeholder envelope exactly like "str" does.  Both
# entries below are evidenced against a Create Note shortcut exported from the TARGET
# iPhone itself (.planning/debug/"Donor - notes.shortcut", decrypted 2026-08-14):
#   mobilenotes.SharingExtension.WFCreateNoteInput
#       device donor serialises this as {"string": "￼", "attachmentsByRange": {...}}
#       with WFSerializationType WFTextTokenString.  A bare attachment here creates the
#       note with an EMPTY BODY -- the create call still succeeds, which is exactly the
#       reported "note exists but is empty".  Catalog names this parameter "contents",
#       typePythonName AttributedString; the donor proves iOS 26.6 reads WFCreateNoteInput.
#   appendnote.text
#       catalog typePythonName AttributedString.  No golden-corpus instance exists, so this
#       rests on the catalog type plus the donor's AttributedString analogue plus an
#       internal control group: this artifact already carries one appendnote whose `text`
#       is a WFTextTokenString (the state-recovery line, a composite template) beside one
#       carrying a bare attachment (the Control Room refresh snapshot).
STRING_ENVELOPE_PARAMS = {
    "is.workflow.actions.gettext": {"WFTextActionText"},
    "is.workflow.actions.setvalueforkey": {"WFDictionaryValue"},
    "is.workflow.actions.text.trimwhitespace": {"WFInput"},
    "is.workflow.actions.text.changecase": {"text"},
    "is.workflow.actions.text.match": {"text"},
    "is.workflow.actions.alert": {"WFAlertActionMessage", "WFAlertActionTitle"},
    "is.workflow.actions.notification": {"WFNotificationActionTitle", "WFNotificationActionBody"},
    "is.workflow.actions.searchweb": {"WFInputText"},
    "com.apple.mobilenotes.SharingExtension": {"WFCreateNoteInput"},
    "is.workflow.actions.appendnote": {"text"},
    "is.workflow.actions.speaktext": {"WFText"},
}

# CYCLE 5 -- the THIRD axis on which an emitted parameter can be wrong.
#
# Cycle 1 fixed the KEY NAME axis (WFInput -> WFDictionaryValue).  Cycles 2 and 4 fixed the
# VALUE ENVELOPE axis (bare WFTextTokenAttachment -> WFTextTokenString, for catalog types
# "str" and then "AttributedString").  Neither pass ever asked whether a REQUIRED PICKER
# (enum) parameter was present at all, or whether it held a literal enum case.
#
# A picker parameter that is ABSENT, or that holds a variable/attachment token instead of a
# literal enum case, renders in Shortcuts as an unfilled picker.  iOS then refuses to run the
# action with "Please choose a value for each parameter in this action" -- attributing the
# failure to the outermost caller (a Personal Automation, by its own name), never naming the
# offending action.
#
# The artifact contained its own control group: eight picker classes already carried literal
# enum cases and only two deviated --
#   count.WFCountType              MISSING entirely
#   getitemfromlist.WFItemSpecifier  held a VARIABLE token at 31 of 33 sites, WFItemIndex absent
# Golden corpus is unanimous on both: 11/11 count actions emit WFCountType; every corpus
# getitemfromlist puts a LITERAL in WFItemSpecifier and the DYNAMIC index in WFItemIndex
# (golden 332c12a0060043b388b2 does exactly that with a Repeat Index variable).
#
# DELIBERATELY ABSENT from this table: math.WFMathOperation.  It looks like the same defect --
# 25 sites omit it -- but golden 2e0fb675e459 (client 1146.11.1, minClient 900, our vintage)
# omits it with our exact key shape, so "+" is genuinely the implicit default.  Corpus
# evidence outranks catalog inference, per the cycle-2 openurl precedent.
REQUIRED_PICKER_PARAMS = {
    "is.workflow.actions.count": {"WFCountType"},
    "is.workflow.actions.getitemfromlist": {"WFItemSpecifier"},
    "is.workflow.actions.setvolume": {"WFVolumeSetting"},
    "is.workflow.actions.gettimebetweendates": {"WFTimeUntilUnit"},
    "is.workflow.actions.round": {"WFRoundTo", "WFRoundMode"},
    "is.workflow.actions.searchweb": {"WFSearchWebDestination"},
    "is.workflow.actions.searchmaps": {"WFSearchMapsActionApp"},
    "is.workflow.actions.text.changecase": {"WFCaseType"},
    "is.workflow.actions.getdevicedetails": {"WFDeviceDetail"},
}


def verify_required_pickers(actions):
    """Fail the build if a required enum picker is missing or holds a non-literal value.

    Both failure modes present identically on device: an unfilled picker, and the runtime
    error "Please choose a value for each parameter in this action".
    """
    offenders = []
    for index, item in enumerate(actions):
        keys = REQUIRED_PICKER_PARAMS.get(item.get("WFWorkflowActionIdentifier"))
        if not keys:
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        # Control-flow end markers carry no parameters of their own.
        if parameters.get("WFControlFlowMode") in (1, 2):
            continue
        for key in sorted(keys):
            if key not in parameters:
                offenders.append((index, item["WFWorkflowActionIdentifier"], key, "missing"))
            elif not isinstance(parameters[key], str):
                offenders.append((index, item["WFWorkflowActionIdentifier"], key, "non-literal"))
    if offenders:
        raise SystemExit("required picker parameters are unset or non-literal "
                         "(iOS: 'Please choose a value for each parameter in this action'): "
                         + "; ".join(f"action {i} {ident}.{key} {why}"
                                     for i, ident, key, why in offenders[:5])
                         + f" ({len(offenders)} total)")

def verify_conditional_inputs(actions):
    """Fail the build if a conditional's input slot holds a text template.

    WFInput on is.workflow.actions.conditional is {"Type": "Variable", "Variable": <token>}.
    The <token> must be a WFTextTokenAttachment wrapping a descriptor that carries a Type key
    ({Type: Variable, VariableName: ...} or {Type: ActionOutput, OutputUUID/OutputName: ...}).

    A WFTextTokenString text template in that slot -- Value = {"string": "￼",
    "attachmentsByRange": {...}} -- is NOT a variable reference.  iOS renders the If's input
    field as unset and refuses to run the action with "Please choose a value for each
    parameter in this action".  This is the fourth defect axis found in this debug session
    and the first one that inverts an earlier rule: string-typed PARAMETERS need
    WFTextTokenString (see normalise_string_envelopes), but variable SLOTS need the bare
    attachment.  No catalog entry exists for is.workflow.actions.conditional, so no
    catalog-driven sweep can see this -- hence an explicit invariant.

    Ground truth: Donor 3 action 4 (device export from the target iPhone) and 20/20
    WFInput-carrying conditionals across the 19 golden shortcuts.
    """
    offenders = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        # Otherwise (1) and End If (2) carry no input of their own.
        if parameters.get("WFControlFlowMode") != 0:
            continue
        wrapper = parameters.get("WFInput")
        if not isinstance(wrapper, dict):
            offenders.append((index, "WFInput missing or not a dict"))
            continue
        holder = wrapper.get("Variable")
        if not isinstance(holder, dict):
            offenders.append((index, "WFInput.Variable missing or not a dict"))
            continue
        if holder.get("WFSerializationType") != "WFTextTokenAttachment":
            offenders.append((index, f"WFInput.Variable is {holder.get('WFSerializationType')!r}, "
                                     "expected WFTextTokenAttachment"))
            continue
        inner = holder.get("Value")
        if not isinstance(inner, dict) or "Type" not in inner or "string" in inner:
            offenders.append((index, "WFInput.Variable.Value is a text template, "
                                     "not a variable descriptor"))
    if offenders:
        raise SystemExit("conditional input slots hold a non-variable value "
                         "(iOS: 'Please choose a value for each parameter in this action'): "
                         + "; ".join(f"action {i}: {why}" for i, why in offenders[:5])
                         + f" ({len(offenders)} total)")


def verify_conditional_action_string(actions):
    """Fail the build if a conditional's comparison target is the abandoned bare placeholder.

    WFConditionalActionString is the RIGHT/comparison-target side of a conditional (WFInput,
    checked by verify_conditional_inputs() above, is the LEFT/compared-variable side). The
    generator's established idiom for a variable-backed comparison target is:
    if_block(..., string=<placeholder text>) immediately followed by a reassignment to a real
    token(<variable>) envelope. At least ten sites left that reassignment out and shipped the
    bare, un-enveloped single placeholder character ("￼") instead -- structurally valid,
    silently wrong at runtime (the comparison can never match a real value). This was the
    confirmed root cause of G-04-1 (session duration always 0) and G-04-3 (CLOSE never
    switches, permanent no-op); see .planning/debug/G-04-1-close-duration-zero.md and
    .planning/debug/G-04-3-session-race-not-switching.md. Neither verify_conditional_inputs()
    (WFInput side only) nor STRING_ENVELOPE_PARAMS (does not cover
    is.workflow.actions.conditional) catches this axis, so this is a dedicated guard against
    the exact same defect class shipping silently again.
    """
    offenders = []
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        # Otherwise (1) and End If (2) never carry a comparison target of their own.
        if parameters.get("WFControlFlowMode") != 0:
            continue
        if "WFConditionalActionString" not in parameters:
            continue
        if parameters["WFConditionalActionString"] == "￼":
            offenders.append(index)
    if offenders:
        raise SystemExit("conditional comparison targets hold the abandoned bare placeholder "
                         "character instead of a wired token() reference: actions "
                         + ", ".join(str(i) for i in offenders[:5])
                         + f" ({len(offenders)} total)")


# ---------------------------------------------------------------------------
# CYCLE 11 -- STATE SHAPE, the sixth defect axis.  Not a wrong shape in the emitted
# plist at all: a wrong BELIEF about iOS semantics, held by the generator's authors.
#
# restore_managed_settings() reads settings_snapshot.brightness (action 177) and gates it
# on condition 100, HAS ANY VALUE.  That design assumes a MISSING dictionary key reads as
# empty, so the gate would be false and the guarded branch skipped.  It does not.  Get
# Dictionary Value on a missing key raises a HARD RUNTIME ERROR: the read at 177 dies
# before the gate at 181 can evaluate, and the guard cannot protect anything because the
# condition it guards against kills the read first.
#
# The bootstrap state.json template seeded settings_snapshot as {} -- the top-level key
# exists, but neither sub-key does.  Reads sit at depth 2 and 3; the writes that would
# create them sit at depth 4 and 7 on Circle paths (1132-1136, 1038-1042) that a first
# run never reaches.  So the reads are reachable on paths where the writes never ran, and
# both observed device errors follow exactly and in order:
#   clean state    -> "In '', no value was found for dictionary key 'settings_snapshot'"
#   after the user exercised the manual menu (which wrote settings_snapshot.volume.*)
#                  -> "In 'settings_snapshot', no value was found for key 'brightness'"
#
# The fix is to establish the COMPLETE subtree at bootstrap, so the shape exists before
# any read regardless of execution history.  Every leaf is seeded EMPTY -- the cleared
# sentinel -- and never a fabricated number: a fabricated original_value could restore
# brightness or volume to a value the user never had.  Empty plus the existing condition
# 100 gates means "no capture recorded -> skip restore", which fails safe and is what
# .claude/CLAUDE.md requires of a stateful brightness/volume change.
#
# This is a TEXT edit to the existing template action, not new actions, so it adds nothing
# to the artifact and every breadcrumb keeps its build-i position.
SNAPSHOT_SEED = {
    "brightness": ("original_value", "changed_at", "changed_by_session_id"),
    "volume": ("original_value", "changed_at", "changed_by_session_id"),
}
SNAPSHOT_EMPTY = '"settings_snapshot": {},'


def _snapshot_seed_text(indent: str) -> str:
    inner = ",\n".join(
        f'{indent}  "{group}": {{'
        + ", ".join(f'"{leaf}": "{CLEARED_SENTINEL}"' for leaf in leaves)
        + "}"
        for group, leaves in SNAPSHOT_SEED.items())
    return '"settings_snapshot": {\n' + inner + "\n" + indent + "},"


# Build j seeded these leaves EMPTY.  That was the safety defect: Donor 6.1 then measured
# that a present-but-empty value passes `has any value`, so the leaf gate read TRUE and the
# restore wrote an empty value into Set Brightness.  Recognise that shape and correct it in
# place, so a re-run over a build-j tree converges instead of silently keeping "".
SNAPSHOT_SEEDED_EMPTY = '"original_value": "", "changed_at": "", "changed_by_session_id": ""'


def _state_template(actions):
    """The bootstrap state.json template action, located by content, never by index."""
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.gettext":
            continue
        value = item.get("WFWorkflowActionParameters", {}).get("WFTextActionText")
        if not isinstance(value, dict):
            continue
        inner = value.get("Value")
        if isinstance(inner, dict) and isinstance(inner.get("string"), str) \
                and '"schema_version"' in inner["string"]:
            return index, inner
    raise SystemExit("bootstrap state.json template not found")


def _replace_in_token(inner: dict, old: str, new: str):
    """Replace text inside a WFTextTokenString and SHIFT every attachment offset.

    attachmentsByRange keys are "{offset, 1}" byte-for-character offsets into the final
    string.  BEST_PRACTICES/VARIABLES both warn that an out-of-bounds or stale range can
    crash Shortcuts on import, so a text edit that ignores them is not a smaller change
    than one that recomputes them -- it is a corrupt one.  The template carries four
    attachments and one of them sits AFTER the settings_snapshot line.
    """
    string = inner["string"]
    at = string.find(old)
    if at < 0:
        raise SystemExit(f"state template does not contain {old!r}")
    delta = len(new) - len(old)
    inner["string"] = string[:at] + new + string[at + len(old):]
    shifted = {}
    for key, attachment in inner.get("attachmentsByRange", {}).items():
        offset, length = (int(part) for part in key.strip("{}").split(","))
        if offset > at:
            offset += delta
        shifted[f"{{{offset}, {length}}}"] = attachment
    inner["attachmentsByRange"] = shifted
    for key in inner["attachmentsByRange"]:
        offset, _ = (int(part) for part in key.strip("{}").split(","))
        if inner["string"][offset] != "￼":
            raise SystemExit(f"attachment offset {offset} no longer points at a placeholder")


def seed_settings_snapshot(actions):
    """Establish the complete settings_snapshot subtree in the bootstrap template."""
    _, inner = _state_template(actions)
    while SNAPSHOT_SEEDED_EMPTY in inner["string"]:
        # A build-j tree: right shape, wrong sentinel.  Correct the leaves in place.
        _replace_in_token(inner, SNAPSHOT_SEEDED_EMPTY,
                          ", ".join(f'"{leaf}": "{CLEARED_SENTINEL}"'
                                    for leaf in SNAPSHOT_SEED["brightness"]))
    if SNAPSHOT_EMPTY not in inner["string"]:
        return  # already seeded; verify_state_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if SNAPSHOT_EMPTY in text)
    indent = line[:len(line) - len(line.lstrip())]
    _replace_in_token(inner, SNAPSHOT_EMPTY, _snapshot_seed_text(indent))


def verify_state_seed(actions):
    """Fail the build if any settings_snapshot READ has no bootstrap counterpart.

    Reads are the authority: a key that restore_managed_settings() reads must resolve in
    the seeded template, at the full depth it is read at, or the read is a hard runtime
    error on any path that reaches it before a write created the key.  This is the
    invariant that seed_settings_snapshot() establishes, asserted separately so the two
    cannot drift -- the same discipline as the five axes before it (KEY NAME, VALUE
    ENVELOPE, PICKER LITERAL, VARIABLE SLOT, OPERAND TYPE; this is STATE SHAPE).
    """
    _, inner = _state_template(actions)
    # The template is a text template, so it is not valid JSON as written: quoted
    # placeholders stand in for strings, and one bare placeholder for a boolean.
    document = inner["string"].replace('"￼"', '"x"').replace("￼", "0")
    try:
        seed = json.loads(document)
    except json.JSONDecodeError as error:
        raise SystemExit(f"bootstrap state.json template is not valid JSON: {error}")
    wanted = sorted({f"settings_snapshot.{group}.{leaf}"
                     for group, leaves in SNAPSHOT_SEED.items() for leaf in leaves})
    read_keys = set()
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.getvalueforkey":
            continue
        key = item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey")
        # Composite keys are built from a token and cannot be resolved statically; none
        # of them is rooted at settings_snapshot, and that is asserted rather than assumed.
        if isinstance(key, str) and key.split(".")[0] == "settings_snapshot":
            read_keys.add(key)
        elif not isinstance(key, str) and "settings_snapshot" in str(key):
            raise SystemExit("a settings_snapshot read uses a composite key and cannot be verified")
    missing = []
    for key in sorted(read_keys) + wanted:
        node = seed
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                missing.append(key)
                break
            node = node[part]
    if missing:
        raise SystemExit(
            "bootstrap state.json does not establish every settings_snapshot key that is "
            "read (Get Dictionary Value on a missing key is a HARD RUNTIME ERROR, so a "
            "condition-100 guard cannot protect the read): "
            + ", ".join(sorted(set(missing))))
    for key in wanted:
        node = seed
        for part in key.split("."):
            node = node[part]
        if node != CLEARED_SENTINEL:
            # CYCLE 12 CORRECTION.  This assertion previously demanded EMPTY, and that was
            # the build-j safety defect written down as an invariant: Donor 6.1 measured a
            # present-but-empty value passing `has any value`, so an empty seed let the
            # restore write an empty value into Set Brightness.  The leaf must carry the
            # SENTINEL -- present, so the dotted read cannot raise; non-empty, so the write
            # side needs no empty value; and numerically zero-or-absent, so the "> 0" leaf
            # gate reads false.  Never a fabricated number: that could restore a setting the
            # user never had.
            raise SystemExit(f"{key} is seeded as {node!r}; it must be the cleared sentinel "
                             f"{CLEARED_SENTINEL!r} -- an EMPTY seed passes `has any value` "
                             "(Donor 6.1) and a fabricated number could restore a setting the "
                             "user never had")


# CYCLE 16 -- pending_exit gets the SAME container/leaf treatment as settings_snapshot
# (axis 6, STATE SHAPE), confirmed live by device error rather than inferred: "In '', no
# value was found for dictionary key 'pending_exit'" -- the identical error SHAPE cycle 11
# found for settings_snapshot ("In '', no value was found for dictionary key
# 'settings_snapshot'"), on a key the bootstrap template never declared at all. See the
# note beside KNOWN_SENTINEL_EXISTENCE_GATES for the full before/after.
PENDING_EXIT_SEED = {"type": CLEARED_SENTINEL, "timestamp": CLEARED_SENTINEL}
PENDING_EXIT_ANCHOR = '"active_session": null,'


def seed_pending_exit(actions):
    """Establish pending_exit as a permanent {type, timestamp} container in bootstrap.

    A naive "just seed the flat key with the cleared sentinel" fix would reintroduce the
    OTHER half of this defect family the moment any exit is later recorded and cleared:
    the FORMER complete_pending_exit() cleared the whole "pending_exit" key wholesale
    (cycle-10 finding 5's exact anti-pattern -- see clear_snapshot()'s docstring --
    replayed at the top level instead of a nested leaf), so the SECOND OPEN following any
    exit would gate a sentinel-written key with a condition-100 existence test and then
    dotted-read beneath a string parent -- axis 7, GATE SEMANTICS, "could not evaluate
    the key path". The container/leaf split closes both halves at once: the CONTAINER is
    established once, here, and is never again replaced wholesale by any write (matching
    settings_snapshot's own already-verified invariant); record_exit_and_route() and
    complete_pending_exit() now write and clear only the LEAVES.
    Idempotent: a second run finds "pending_exit" already in the template and returns;
    verify_pending_exit_seed() re-proves the shape either way.
    """
    _, inner = _state_template(actions)
    if '"pending_exit"' in inner["string"]:
        return  # already seeded; verify_pending_exit_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PENDING_EXIT_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    leaves = ", ".join(f'"{leaf}": "{value}"' for leaf, value in PENDING_EXIT_SEED.items())
    _replace_in_token(inner, PENDING_EXIT_ANCHOR,
                      PENDING_EXIT_ANCHOR + f'\n{indent}"pending_exit": {{{leaves}}},')


def verify_pending_exit_seed(actions):
    """Fail the build unless pending_exit is seeded exactly as a {type, timestamp} container.

    Same discipline as verify_state_seed(): the invariant seed_pending_exit() establishes
    is asserted separately so the two cannot silently drift.
    """
    _, inner = _state_template(actions)
    document = inner["string"].replace('"￼"', '"x"').replace("￼", "0")
    try:
        seed = json.loads(document)
    except json.JSONDecodeError as error:
        raise SystemExit(f"bootstrap state.json template is not valid JSON: {error}")
    pending = seed.get("pending_exit")
    if not isinstance(pending, dict) or any(pending.get(leaf) != value
                                            for leaf, value in PENDING_EXIT_SEED.items()):
        raise SystemExit(
            f"pending_exit is seeded as {pending!r}; it must be exactly {PENDING_EXIT_SEED!r} "
            "-- an absent or malformed seed reproduces the confirmed cycle-16 hard error "
            "(\"no value was found for dictionary key 'pending_exit'\"), and any other "
            "leaf value risks the same sentinel-vs-real-value confusion axis 7 already "
            "closed for settings_snapshot")


# PHASE 11 (11-05) -- the Panic Escape flag.  Same STATE SHAPE discipline as
# settings_snapshot and pending_exit above: the seeder establishes it, a separate verifier
# asserts it, so the two cannot drift.  Deliberately FLAT and top-level, and deliberately
# NUMERIC.
#
# Flat, because universal_leaving()'s gate must be able to read false.  Per
# .claude/CLAUDE.md's device-verified runtime semantics a DOTTED read whose final segment is
# absent is a HARD ERROR, so a nested `settings.panic_escape_enabled` could not be gated at
# all on a state.json written before this field existed -- the read would raise before any
# conditional saw it.  A FLAT read of a missing key returns nothing, no error.
#
# Numeric, because "> 0" is the only comparison that reads false for all four of the states
# this field can be in on a real device -- 0, missing, JSON null and empty string -- while
# condition 100 ("has any value") reads TRUE for the string "null" and for "".  That is the
# axis-7 gate-semantics trap verify_sentinel_gates() exists to prevent.
#
# Seeded to 1 (enabled): the bypass is present unless the user deliberately removes it, and
# removal takes two acts (a hand edit in the Note plus an explicit confirmation).
PANIC_ESCAPE_KEY = "panic_escape_enabled"
PANIC_ESCAPE_SEED = 1
# Anchored on the neighbouring boolean-ish settings line, never on a line number: the
# template is one long WFTextTokenString and every offset in it moves on any edit.
PANIC_ESCAPE_ANCHOR = '"ai_enabled": false,'


def seed_panic_escape(actions):
    """Establish panic_escape_enabled as a flat, numeric, top-level bootstrap field.

    Idempotent: a second run finds the key already present and returns.  _replace_in_token()
    does the guarded round trip -- it shifts every attachmentsByRange offset that sits after
    the edit and re-asserts that each one still lands on a U+FFFC placeholder, which is the
    same six-step method tools/plist_text_edit.py implements standalone.  An unshifted offset
    points into unrelated prose and .claude/CLAUDE.md §5 records that an out-of-bounds range
    can crash Shortcuts on import.
    """
    _, inner = _state_template(actions)
    if f'"{PANIC_ESCAPE_KEY}"' in inner["string"]:
        return  # already seeded; verify_panic_escape_seed() proves it is the right shape
    line = next(text for text in inner["string"].splitlines() if PANIC_ESCAPE_ANCHOR in text)
    indent = line[:len(line) - len(line.lstrip())]
    _replace_in_token(inner, PANIC_ESCAPE_ANCHOR,
                      PANIC_ESCAPE_ANCHOR + f'\n{indent}"{PANIC_ESCAPE_KEY}": {PANIC_ESCAPE_SEED},')


def verify_panic_escape_seed(actions):
    """Fail the build unless the Panic Escape flag is seeded flat and read flat and numerically.

    Three assertions, each naming the failure it prevents:
      (1) the key is seeded at the TOP LEVEL with the numeric enabled value -- an unseeded
          field makes the removal path dead on any device, because the gate reads a key that
          is simply not there;
      (2) no read of it is DOTTED -- a dotted read is unnecessary for a top-level field and
          would hard-error on the very state.json shapes the flat form tolerates;
      (3) every conditional gating it uses a NUMERIC condition code, never 100/101 -- an
          existence gate reads TRUE for the string "null" and for "", so it could not
          express "the user removed the bypass".

    NOTE, measured 2026-08-17: verify_state_seed() does NOT cover this field.  Its read-side
    scan is scoped to keys rooted at `settings_snapshot`, so it would not have noticed an
    unseeded panic_escape_enabled.  This verifier is why the seed is guarded at all.
    """
    _, inner = _state_template(actions)
    document = inner["string"].replace('"￼"', '"x"').replace("￼", "0")
    try:
        seed = json.loads(document)
    except json.JSONDecodeError as error:
        raise SystemExit(f"bootstrap state.json template is not valid JSON: {error}")
    if seed.get(PANIC_ESCAPE_KEY) != PANIC_ESCAPE_SEED:
        raise SystemExit(
            f"{PANIC_ESCAPE_KEY} is seeded as {seed.get(PANIC_ESCAPE_KEY)!r} at the top level; "
            f"it must be exactly {PANIC_ESCAPE_SEED!r} -- an unseeded or non-numeric flag "
            "leaves universal_leaving()'s gate reading a key that is not there, so the "
            "removal path 11-05 builds is dead on every device")

    dotted, existence = [], []
    for index, item in enumerate(actions):
        identifier = item.get("WFWorkflowActionIdentifier")
        parameters = item.get("WFWorkflowActionParameters", {})
        if identifier == "is.workflow.actions.getvalueforkey":
            key = _dictionary_key_string(parameters)
            if PANIC_ESCAPE_KEY in key and key != PANIC_ESCAPE_KEY:
                dotted.append((index, key))
        if identifier == "is.workflow.actions.conditional" and parameters.get("WFControlFlowMode") == 0:
            name = parameters.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")
            if name == "Panic Escape Enabled" and parameters.get("WFCondition") not in NUMERIC_CONDITION_CODES:
                existence.append((index, parameters.get("WFCondition")))
    if dotted:
        raise SystemExit(
            f"{PANIC_ESCAPE_KEY} is read through a composite or dotted key "
            + "; ".join(f"action {i}: {key!r}" for i, key in dotted)
            + " -- it is a flat top-level field precisely so a read on a state.json that "
              "predates it returns nothing instead of raising 'could not evaluate the key path'")
    if existence:
        raise SystemExit(
            "a Panic Escape gate uses a non-numeric condition code "
            + "; ".join(f"action {i}: condition {code}" for i, code in existence)
            + " -- an existence test reads TRUE for the string \"null\" and for an empty "
              "string, so it cannot distinguish a removed bypass from a present one; the "
              "gate must be a numeric '> 0' test")


# ---------------------------------------------------------------------------
# CYCLE 12 -- GATE SEMANTICS, the seventh axis.  Axis 6 (STATE SHAPE) asserted that every
# key a read reaches EXISTS.  This asserts that the GATE standing over it can actually
# distinguish the states that key can be in.  The two are different failures: build j
# satisfied axis 6 completely and still wrote an empty value into Set Brightness.
#
# The measured rule, from Donor 6.1 on the target iPhone:
#   an EXISTENCE gate (condition 100 / 101) cannot distinguish "cleared" from "captured"
#   for any key that is ever written with the sentinel, because the sentinel is PRESENT and
#   NON-EMPTY -- so the gate reads TRUE in exactly the case it exists to exclude.
# Everything the restore path got wrong follows from that one sentence, so it is the thing
# asserted, rather than the individual condition codes at the individual sites.
#
# Two invariants, both of which FAIL on the build-j generator and pass on this one:
#   (1) SAFETY.  A brightness/volume write whose value is a variable read out of
#       settings_snapshot must be dominated by a NUMERIC conditional on that same variable.
#       This is the invariant build j violated; it is stated over the WRITE, so no future
#       re-gating can reintroduce an empty or zero write without tripping it.
#   (2) GATES.  No sentinel-written key may be gated by condition 100/101, and no dotted
#       read may hang beneath a sentinel-written parent.  This enforces the CONTAINER vs
#       LEAF split automatically rather than by convention: once clear_snapshot() writes the
#       leaf instead of the container, `settings_snapshot.brightness` stops being
#       sentinel-written and its condition-100 container gate becomes legal again, while the
#       leaf beneath it must be numeric.  Change the clear back to the container and the
#       build fails.
EXISTENCE_CONDITION_CODES = {100, 101}
SNAPSHOT_ROOT = "settings_snapshot"


def _sentinel_written_keys(actions):
    """Literal dictionary keys ever written with the cleared sentinel."""
    keys = set()
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setvalueforkey":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        key, value = parameters.get("WFDictionaryKey"), parameters.get("WFDictionaryValue")
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        inner = value.get("Value")
        if isinstance(inner, dict) and inner.get("string") == CLEARED_SENTINEL \
                and not inner.get("attachmentsByRange"):
            keys.add(key)
    return keys


def _read_variable_keys(actions):
    """Map each named variable to the literal dictionary key it is read from.

    read_value() emits getvalueforkey -> gettext -> setvariable, so the variable's key is
    recovered by walking that chain backwards through the two output UUIDs.
    """
    key_by_uuid, text_by_uuid = {}, {}
    for item in actions:
        identifier = item.get("WFWorkflowActionIdentifier")
        parameters = item.get("WFWorkflowActionParameters", {})
        if identifier == "is.workflow.actions.getvalueforkey":
            if isinstance(parameters.get("WFDictionaryKey"), str) and "UUID" in parameters:
                key_by_uuid[parameters["UUID"]] = parameters["WFDictionaryKey"]
        elif identifier == "is.workflow.actions.gettext" and "UUID" in parameters:
            # normalise_string_envelopes() rewrites this parameter into a WFTextTokenString
            # TEXT TEMPLATE, so the producing action is reached through attachmentsByRange
            # rather than through a bare descriptor.  Accept both forms: reading only the
            # bare form silently returns no provenance and the guard becomes decoration.
            holder = parameters.get("WFTextActionText")
            source = holder.get("Value") if isinstance(holder, dict) else None
            if not isinstance(source, dict):
                continue
            sources = [source] + list((source.get("attachmentsByRange") or {}).values())
            for candidate in sources:
                if isinstance(candidate, dict) and candidate.get("Type") == "ActionOutput" \
                        and candidate.get("OutputUUID") in key_by_uuid:
                    text_by_uuid[parameters["UUID"]] = key_by_uuid[candidate["OutputUUID"]]
                    break
    keys = {}
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setvariable":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        source = (parameters.get("WFInput") or {}).get("Value")
        if not isinstance(source, dict) or source.get("Type") != "ActionOutput":
            continue
        key = text_by_uuid.get(source.get("OutputUUID"))
        if key:
            keys.setdefault(parameters.get("WFVariableName"), set()).add(key)
    return keys


def _enclosing_if_arms(actions):
    """For each action index, the conditionals whose IF arm currently encloses it."""
    stack, enclosing = [], []
    for item in actions:
        parameters = item.get("WFWorkflowActionParameters", {})
        is_conditional = item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
        mode = parameters.get("WFControlFlowMode") if is_conditional else None
        if mode == 2 and stack:
            stack.pop()
            enclosing.append([entry for entry, arm in stack if arm])
            continue
        enclosing.append([entry for entry, arm in stack if arm])
        if mode == 0:
            stack.append((parameters, True))
        elif mode == 1 and stack:
            stack[-1] = (stack[-1][0], False)
    return enclosing


def _tested_variable(parameters):
    descriptor = (parameters.get("WFInput") or {}).get("Variable", {}).get("Value")
    if isinstance(descriptor, dict) and descriptor.get("Type") == "Variable":
        return descriptor.get("VariableName")
    return None


def verify_restore_gates(actions):
    """Fail the build if a brightness/volume write is not numerically gated.

    THE INVARIANT BUILD 2026-08-14j VIOLATED, stated over the write rather than the gate.
    Its leaf gate was condition 100 and the leaf was seeded EMPTY, and a present-but-empty
    value passes `has any value` (Donor 6.1), so Set Brightness was reached with an empty
    value -- a runtime error or brightness 0, which .claude/CLAUDE.md forbids outright, on
    the C->D span that runs on EVERY OPEN.
    A value read out of settings_snapshot must be gated by a NUMERIC comparison on that
    same variable, because only a numeric test excludes BOTH the sentinel and empty; the
    string family (code 4/5) excludes one and passes the other.
    """
    reads, offenders = _read_variable_keys(actions), []
    for index, enclosing in enumerate(_enclosing_if_arms(actions)):
        item = actions[index]
        identifier = item.get("WFWorkflowActionIdentifier")
        if identifier not in {"is.workflow.actions.setbrightness", "is.workflow.actions.setvolume"}:
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        value = parameters.get("WFBrightness") or parameters.get("WFVolume")
        descriptor = value.get("Value") if isinstance(value, dict) else None
        if not isinstance(descriptor, dict) or descriptor.get("Type") != "Variable":
            continue  # a literal target is not a state-derived write
        name = descriptor.get("VariableName")
        numeric = [parameters for parameters in enclosing
                   if parameters.get("WFCondition") in NUMERIC_CONDITION_CODES]
        from_snapshot = any(key.split(".")[0] == SNAPSHOT_ROOT for key in reads.get(name, ()))
        if from_snapshot:
            if not any(_tested_variable(gate) == name for gate in numeric):
                offenders.append((index, f"writes {name!r}, read from {SNAPSHOT_ROOT}, with no "
                                         f"numeric gate on {name!r} above it"))
        elif not numeric:
            offenders.append((index, f"writes {name!r} with no numeric gate above it"))
    if offenders:
        raise SystemExit(
            "a brightness/volume write is not numerically gated -- an existence or string "
            "gate passes the cleared sentinel or an empty value straight into the write, "
            "which is a runtime error or a black screen: "
            + "; ".join(f"action {i}: {why}" for i, why in offenders[:5])
            + f" ({len(offenders)} total)")


def verify_sentinel_gates(actions):
    """Fail the build if an existence gate stands over a key written with the sentinel.

    The sentinel is PRESENT and NON-EMPTY, so condition 100 reads TRUE in exactly the case
    it exists to exclude, and any dotted read inside that branch then runs against a string
    parent and raises "could not evaluate the key path" (Donor 6.1, line 3).
    KNOWN_SENTINEL_EXISTENCE_GATES records the key(s) still carrying this defect (pending_exit
    was CLOSED cycle 16 via the container/leaf split and removed from this set; only
    active_session remains, deliberately, per the note beside that constant), with the
    reason they cannot be flipped in isolation; see the note beside CLEARED_SENTINEL.
    """
    sentinel, reads, offenders = _sentinel_written_keys(actions), _read_variable_keys(actions), []
    deferred = set(KNOWN_SENTINEL_EXISTENCE_GATES)
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFCondition") not in EXISTENCE_CONDITION_CODES:
            continue
        for key in sorted(reads.get(_tested_variable(parameters), set()) & sentinel):
            if key.split(".")[0] not in deferred:
                offenders.append((index, f"condition {parameters['WFCondition']} gates {key!r}, "
                                         "which is written with the cleared sentinel"))
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.getvalueforkey":
            continue
        key = item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey")
        if not isinstance(key, str) or "." not in key:
            continue
        parent = key.rsplit(".", 1)[0]
        if parent in sentinel and parent.split(".")[0] not in deferred:
            offenders.append((index, f"dotted read {key!r} hangs beneath {parent!r}, which is "
                                     "written with the cleared sentinel and is therefore not "
                                     "always a dictionary"))
    if offenders:
        raise SystemExit(
            "an existence gate or a dotted read stands over a sentinel-written key -- the "
            "sentinel is present and non-empty, so condition 100 reads TRUE for a cleared "
            "key and the nested read then hard-errors on a string parent: "
            + "; ".join(f"action {i}: {why}" for i, why in offenders[:5])
            + f" ({len(offenders)} total)")


# ---------------------------------------------------------------------------
# CYCLE 15 -- the eighth axis, STRUCTURED VALUE (compound state fields).  Confirmed by
# device error: "Get Dictionary Value failed because Shortcuts couldn't convert Text to
# Dictionary", traced to recent_sessions being read through read_value(), which
# gettext-coerces every value it touches into a Text scalar.  That coercion is exactly
# right for a leaf meant for a text/numeric comparison and exactly wrong for a compound
# Array meant to be consumed structurally by Get Item From List or Repeat With Each --
# get_value() is the un-coercing counterpart (see its own docstring for the full
# device-error trace).  This guard makes the split mechanical rather than a convention:
# any state key seeded in the bootstrap template as a JSON array must never be read
# through read_value()'s gettext chain.
COMPOUND_STATE_KEYS = frozenset({
    "recent_sessions", "recent_contracts", "exit_events",
    "profile_snapshot.enabled_exits",
})
# exit_stats.<name>.samples is a dynamic, per-exit-type key (text_token-built, not a
# literal string), so it cannot be matched by this guard's literal-key scan.  It is the
# fifth confirmed instance of this axis (complete_pending_exit(), fixed cycle 15) and is
# recorded here so it is not lost from the class even though the guard below cannot see
# it mechanically.


LIST_CONSUMING_ACTIONS = {
    "is.workflow.actions.repeat.each", "is.workflow.actions.getitemfromlist",
    "is.workflow.actions.count", "is.workflow.actions.filter.contentitems",
}


def _list_consumed_variables(actions):
    """Named variables fed as WFInput to an action that expects a List/Array."""
    consumed = set()
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") not in LIST_CONSUMING_ACTIONS:
            continue
        descriptor = (item.get("WFWorkflowActionParameters", {}).get("WFInput") or {}).get("Value")
        if isinstance(descriptor, dict) and descriptor.get("Type") == "Variable":
            consumed.add(descriptor.get("VariableName"))
    return consumed


def verify_compound_value_reads(actions):
    """Fail the build if a compound (Array) state key, read via read_value(), then
    feeds a List-consuming action.

    read_value()'s gettext step stringifies whatever it touches.  For a scalar this is
    the intended coercion for text/numeric comparison -- including a compound value read
    ONLY for text DISPLAY (e.g. manual_note_refresh()'s Snapshot Exits), which this guard
    deliberately does not flag.  It is exactly wrong when the same value is consumed
    STRUCTURALLY downstream by Get Item From List / Repeat With Each / Count: the array
    collapses into one Text blob before that consumer ever sees it -- device-confirmed
    cycle 15 (recent_sessions, breadcrumb E->F: "Get Dictionary Value failed because
    Shortcuts couldn't convert Text to Dictionary"). get_value() is the correct helper
    for every key in COMPOUND_STATE_KEYS when the read feeds a List consumer.
    """
    reads, consumed, offenders = _read_variable_keys(actions), _list_consumed_variables(actions), []
    for name, keys in reads.items():
        if name not in consumed:
            continue  # text-display-only reads of a compound key are legitimate
        hit = keys & COMPOUND_STATE_KEYS
        if hit:
            offenders.append(f"{name!r} is read via read_value() from {sorted(hit)} and fed to a List-consuming action")
    if offenders:
        raise SystemExit(
            "a compound (Array) state key is read via read_value(), which stringifies it "
            "via Get Text, and the resulting Text is then fed to a Get Item From List / "
            "Repeat With Each / Count action expecting a List -- use get_value() instead: "
            + "; ".join(offenders))


# ---------------------------------------------------------------------------
# CYCLE 9 -- OPERAND TYPE, the fifth defect axis and the first invisible in the plist.
#
# A conditional's OPERATOR PICKER is populated from the STATIC TYPE of the variable in
# WFInput.  read_value() defines its variable from an is.workflow.actions.gettext output,
# so Shortcuts types it Text and offers only the EIGHT STRING operators -- is / is not /
# has any value / does not have any value / contains / does not contain / begins with /
# ends with.  A numeric WFCondition (0, 1, 2, 3, 1003) then has NO CASE TO RENDER: the
# operator chip shows RED and iOS refuses to run the action.
#
# Every key, envelope, picker literal and condition code is well-formed at a defective
# site, so verify_parameter_keys, verify_string_envelopes, verify_required_pickers and
# verify_conditional_inputs all pass over it.  Decrypting the signed artifact does not
# reveal it either.  It was found only because the user photographed red operators.
#
# DEVICE GROUND TRUTH -- Donor 4.1, built in Shortcuts.app on the target iPhone and
# decrypted 2026-08-14 (.planning/debug/"Donor 4.1.shortcut").  A Get Dictionary Value
# output compared with WFCondition 2 against WFNumberValue "10" serialises as:
#
#   "WFInput": {"Type": "Variable", "Variable": {
#       "Value": {"Type": "ActionOutput", "OutputName": "Dictionary Value",
#                 "OutputUUID": "...",
#                 "Aggrandizements": [{"Type": "WFCoercionVariableAggrandizement",
#                                      "CoercionItemClass": "WFNumberContentItem"}]},
#       "WFSerializationType": "WFTextTokenAttachment"}}
#
# iOS does NOT insert a Number action and does NOT change the read chain.  It attaches a
# COERCION AGGRANDIZEMENT to the variable reference in the conditional's own input slot --
# which is precisely what the user did in the UI by tapping the chip and choosing "Number"
# from its type list (screenshot .planning/debug/IMG_5636.jpg).  Donor 4, the same shortcut
# before that tap, carries the identical descriptor with NO Aggrandizements and a code-100
# test, which is the control case.
#
# Corroboration that the aggrandizement attaches to a NAMED variable as well as to an
# ActionOutput: golden shortcut 332c12a0060043b388b22b806be7ab58 carries
# WFCoercionVariableAggrandizement on both {Type: Variable, VariableName: ...} and
# {Type: ActionOutput, ...} descriptors (24 instances across the corpus).
#
# WHY A COERCION AND NOT A Number ACTION.  Golden corpus 2e0fb675 does feed a Dictionary
# Value straight into is.workflow.actions.number, so that construct is also real -- but it
# is the shape for MATERIALISING a number into the data flow, not for typing a conditional
# operand.  For this exact construct the device is unambiguous, and device evidence
# outranks corpus composition.  The coercion is also strictly smaller: it adds no actions,
# leaves every device-proven read chain byte-identical, and needs no null handling, because
# coercing an absent value yields an absent value and the comparison simply evaluates false.
# ---------------------------------------------------------------------------
NUMERIC_CONDITION_CODES = {0, 1, 2, 3, 1003}
NUMBER_COERCION = {"Type": "WFCoercionVariableAggrandizement",
                   "CoercionItemClass": "WFNumberContentItem"}
# Action identifiers whose output is already Number-typed, so their operands need no
# coercion.  Derived from the cycle-9 provenance trace of all 87 (Dumb) / 94 (Sentient)
# numeric conditionals; leaving these untouched keeps every device-proven site -- notably
# the Control Room refresh conditionals that executed on the cycle-5 pass -- byte-identical.
NUMERIC_SOURCE_ACTIONS = {
    "is.workflow.actions.number",
    "is.workflow.actions.number.random",
    "is.workflow.actions.math",
    "is.workflow.actions.round",
    "is.workflow.actions.calculateexpression",
    "is.workflow.actions.gettimebetweendates",
    "is.workflow.actions.getdevicedetails",
    "is.workflow.actions.count",
    # Ask For Input is numeric ONLY when its picker is Number; the token is synthesised
    # per action below so a Text-typed Ask can never satisfy this.
    "is.workflow.actions.ask#Number",
}
# Built-in variables that are numeric without a Set Variable of their own.
NUMERIC_BUILTIN_VARIABLES = {"Repeat Index"}

# CYCLE 14 -- axis 6 GENERALISED beyond conditionals.  HANDOFF.md's own type-audit first
# pass named math.WFInput/WFMathOperand and getitemfromlist.WFItemIndex as unaudited
# numeric-typed fields; the cycle-14 nested-descent second pass (which also unwraps the
# {"Value": desc} shape a direct variable()/output() reference carries, not just
# conditional's {"Type":"Variable","Variable":{"Value": desc}} wrapper the first pass was
# scoped to) found 85 real uncoerced offenders: 30 getitemfromlist.WFItemIndex, 26
# math.WFMathOperand, 11 math.WFInput, plus 18 setbrightness/setvolume (left untouched --
# see the brightness/volume MVP-cut deferral in the debug session; those two fields are
# deliberately NOT in this table).
# The getitemfromlist offenders are load-bearing for symptom 1: mirror_text()'s
# WFItemIndex=variable("Circle Next") is on the Circle 1 intervention itself, and "Circle
# Next" is mixed-typed -- manual_emergency_restore()'s Test Circle loop assigns it from
# read_value() (Text) as well as from number() (Number) -- so every Item At Index call
# using it is exactly the axis-5/6 "one Text definition anywhere poisons every numeric use
# of that name" class this session already fixed once for conditionals.  The math
# offenders are the direct consequence of the elapsed_since() fix: "Last Open", "Last
# Close" and "Pending Exit Timestamp" are Text (gettext-read), fed as the right-hand
# WFMathOperand of a numeric subtraction, on the OPEN critical path.
# Each site takes the SAME Donor-4.1 WFCoercionVariableAggrandizement:WFNumberContentItem
# shape already established for conditionals -- not a new, unverified construct.
NUMERIC_OPERAND_FIELDS = {
    "is.workflow.actions.math": ("WFInput", "WFMathOperand"),
    "is.workflow.actions.getitemfromlist": ("WFItemIndex",),
    "is.workflow.actions.setbrightness": ("WFBrightness",),
    "is.workflow.actions.setvolume": ("WFVolume",),
}


def _numeric_operand_sites(item):
    """Yield (field_name, raw_value) for every numeric-typed field this action carries.

    Covers the numeric-code conditional (as before) plus math and Item-At-Index
    getitemfromlist, table-driven so a future numeric field is one line to add.
    """
    identifier = item.get("WFWorkflowActionIdentifier")
    parameters = item.get("WFWorkflowActionParameters", {})
    if identifier == "is.workflow.actions.conditional":
        if parameters.get("WFControlFlowMode") == 0 and parameters.get("WFCondition") in NUMERIC_CONDITION_CODES:
            yield "WFInput", parameters.get("WFInput")
        return
    if identifier == "is.workflow.actions.getitemfromlist" and parameters.get("WFItemSpecifier") != "Item At Index":
        return
    for field in NUMERIC_OPERAND_FIELDS.get(identifier, ()):
        if field in parameters:
            yield field, parameters[field]


def _operand_descriptor(value):
    """Unwrap a numeric field's raw value to its coercable descriptor, or None.

    Two shapes occur for a variable/output reference in this artifact:
      conditional-style : {"Type": "Variable", "Variable": {"Value": desc, ...}}
      direct (variable()/output()) : {"Value": desc, "WFSerializationType": ...}
    A bare literal number (e.g. math's WFMathOperand=60) is neither -- it is already
    Number-typed by construction and returns None so the caller skips it untouched.
    """
    if not isinstance(value, dict):
        return None
    if isinstance(value.get("Variable"), dict):
        descriptor = value["Variable"].get("Value")
    elif "Value" in value:
        descriptor = value.get("Value")
    else:
        return None
    return descriptor if isinstance(descriptor, dict) else None


def _numeric_operand_report(actions):
    """Every numeric-typed operand site, with its operand descriptor and provenance.

    Shared by the normalise and verify passes so the two can never disagree about which
    operands count as already-numeric.
    """
    produced = {}
    for item in actions:
        parameters = item.get("WFWorkflowActionParameters", {})
        if "UUID" not in parameters:
            continue
        identifier = item.get("WFWorkflowActionIdentifier")
        if identifier == "is.workflow.actions.ask":
            identifier += "#" + str(parameters.get("WFInputType"))
        produced[parameters["UUID"]] = identifier
    # Shortcuts types a NAMED variable from ALL of its Set Variable definitions, so one
    # Text definition anywhere poisons every numeric comparison of that name -- including
    # comparisons on an arm the Text definition can never reach.  Collect them all.
    definitions = {}
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.setvariable":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        value = (parameters.get("WFInput") or {}).get("Value")
        sources = definitions.setdefault(parameters.get("WFVariableName"), set())
        if not isinstance(value, dict):
            sources.add("<literal>")
        elif value.get("Type") == "ActionOutput":
            sources.add(produced.get(value.get("OutputUUID"), "<unknown>"))
        elif value.get("Type") == "Variable":
            sources.add("variable:" + str(value.get("VariableName")))
        else:
            sources.add(str(value.get("Type")))

    def resolve(name, seen=()):
        if name in seen:
            return {"<cycle>"}
        found = set()
        for source in definitions.get(name, set()):
            if source.startswith("variable:"):
                found |= resolve(source[len("variable:"):], (*seen, name))
            else:
                found.add(source)
        return found

    report = []
    for index, item in enumerate(actions):
        for field, raw in _numeric_operand_sites(item):
            descriptor = _operand_descriptor(raw)
            if descriptor is None:
                if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                    continue  # literal number -- already Number-typed, nothing to coerce
                report.append((index, field, None, {"<not-a-descriptor>"}))
                continue
            if descriptor.get("Type") == "ActionOutput":
                sources = {produced.get(descriptor.get("OutputUUID"), "<unknown>")}
            elif descriptor.get("VariableName") in NUMERIC_BUILTIN_VARIABLES:
                sources = {"<builtin>"}
            else:
                sources = resolve(descriptor.get("VariableName")) or {"<undefined>"}
            report.append((index, field, descriptor, sources))
    return report


def _already_numeric(sources):
    return bool(sources) and sources <= (NUMERIC_SOURCE_ACTIONS | {"<builtin>"})


def normalise_numeric_operands(actions):
    """Type every numeric operand as a Number, the way iOS does.

    Attaches Donor 4.1's WFCoercionVariableAggrandizement to the operand descriptor of any
    numeric-typed site (numeric-code conditional, math, or Item-At-Index getitemfromlist)
    whose operand is not already Number-typed.  Structural rather than site-by-site: a
    future numeric comparison or calculation on a text-coerced value is corrected
    automatically, and the matching invariant is asserted by verify_numeric_operands().
    Operands that are already numeric are left untouched, so sites that have executed on
    device stay byte-identical.
    """
    for _index, _field, descriptor, sources in _numeric_operand_report(actions):
        if descriptor is None or _already_numeric(sources):
            continue
        existing = descriptor.setdefault("Aggrandizements", [])
        if not any(a.get("Type") == "WFCoercionVariableAggrandizement" for a in existing):
            # Coercion goes FIRST: golden 332c12a0 orders coercion before any property
            # aggrandizement, because the property is read from the coerced item.
            existing.insert(0, dict(NUMBER_COERCION))


def verify_numeric_operands(actions):
    """Fail the build if a numeric-typed operand is untyped and non-numeric.

    See the block comment above for the mechanism and the Donor 4.1 evidence.  This is the
    fifth axis the generator asserts, after key name, value envelope, picker literal and
    variable slot -- and the only one with no representation in the ToolKit catalog, the
    bundled validator, or the signed artifact.  CYCLE 14 widened its scope from
    conditionals alone to every numeric-typed field in NUMERIC_OPERAND_FIELDS.
    """
    offenders = []
    for index, field, descriptor, sources in _numeric_operand_report(actions):
        if descriptor is None:
            offenders.append((index, f"{field}: operand is not a variable descriptor"))
            continue
        if _already_numeric(sources):
            continue
        coerced = any(a.get("Type") == "WFCoercionVariableAggrandizement"
                      and a.get("CoercionItemClass") == "WFNumberContentItem"
                      for a in descriptor.get("Aggrandizements", []))
        if not coerced:
            offenders.append((index, f"{field}: operand is fed by {', '.join(sorted(sources))} "
                                     "and carries no Number coercion"))
    if offenders:
        raise SystemExit(
            "numeric-typed operands are not Number-typed -- a conditional's operator "
            "picker is populated from its operand's static type (no case to render, chip "
            "shows RED, action refuses to run); math and Item-At-Index getitemfromlist "
            "operands risk a runtime type-conversion failure instead ('Get Time Between "
            "Dates failed because Shortcuts couldn't convert from Text to Date' was this "
            "session's own instance of a sibling defect): "
            + "; ".join(f"action {i}: {why}" for i, why in offenders[:6])
            + f" ({len(offenders)} total)")


# Real output names, keyed by producing action identifier.  A magic-variable reference
# carries OutputUUID (the binding) plus OutputName (the label iOS shows and re-resolves
# against).  Hand-authored blocks in this artifact guessed some of these; where two
# independent sources give the real name, normalise to it rather than keep the guess.
#   getrichtextfrommarkdown -> "Rich Text from Markdown"
#       device donor (.planning/debug/"Donor - notes.shortcut") AND golden shortcut
#       f44f5caf5e3e48d4817e73af450c4404.xml action 14 both reference this action's
#       output by that name.  This artifact said "Rich Text".
ACTION_OUTPUT_NAMES = {
    "is.workflow.actions.getrichtextfrommarkdown": "Rich Text from Markdown",
}


def to_string_envelope(value):
    """Re-wrap a single bare token as the WFTextTokenString form iOS expects.

    Shape mirrors the golden corpus exactly: one "￼" placeholder whose
    attachmentsByRange entry is the original token dict, unchanged.
    """
    if not isinstance(value, dict) or value.get("WFSerializationType") != "WFTextTokenAttachment":
        return value
    inner = value.get("Value")
    if not isinstance(inner, dict) or "string" in inner:
        return value
    return {"Value": {"string": "￼", "attachmentsByRange": {"{0, 1}": inner}},
            "WFSerializationType": "WFTextTokenString"}


def normalise_string_envelopes(actions):
    """Convert bare attachments to WFTextTokenString on every string-typed parameter."""
    for item in actions:
        keys = STRING_ENVELOPE_PARAMS.get(item.get("WFWorkflowActionIdentifier"))
        if not keys:
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        for key in keys & set(parameters):
            parameters[key] = to_string_envelope(parameters[key])


def verify_string_envelopes(actions):
    """Fail the build if a string-typed parameter still holds a bare attachment."""
    offenders = []
    for index, item in enumerate(actions):
        keys = STRING_ENVELOPE_PARAMS.get(item.get("WFWorkflowActionIdentifier"))
        if not keys:
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        for key in sorted(keys & set(parameters)):
            value = parameters[key]
            if isinstance(value, dict) and value.get("WFSerializationType") == "WFTextTokenAttachment":
                offenders.append((index, item["WFWorkflowActionIdentifier"], key))
    if offenders:
        head = offenders[:5]
        raise SystemExit("string-typed parameters carry a bare WFTextTokenAttachment "
                         "(resolves to empty at run time): "
                         + "; ".join(f"action {i} {ident}.{key}" for i, ident, key in head)
                         + f" ({len(offenders)} total)")


def _walk_action_output_tokens(node):
    """Yield every {"Type": "ActionOutput", ...} token dict nested anywhere in a value."""
    if isinstance(node, dict):
        if node.get("Type") == "ActionOutput" and "OutputUUID" in node:
            yield node
        for child in node.values():
            yield from _walk_action_output_tokens(child)
    elif isinstance(node, list):
        for child in node:
            yield from _walk_action_output_tokens(child)


def _expected_output_names(actions):
    """Map producing-action UUID -> its real output name, for the actions we know."""
    names = {}
    for item in actions:
        expected = ACTION_OUTPUT_NAMES.get(item.get("WFWorkflowActionIdentifier"))
        uuid_value = item.get("WFWorkflowActionParameters", {}).get("UUID")
        if expected and uuid_value:
            names[uuid_value] = expected
    return names


def normalise_output_names(actions):
    """Point every magic-variable reference at the producing action's REAL output name."""
    names = _expected_output_names(actions)
    if not names:
        return
    for item in actions:
        for token_dict in _walk_action_output_tokens(item.get("WFWorkflowActionParameters", {})):
            expected = names.get(token_dict.get("OutputUUID"))
            if expected:
                token_dict["OutputName"] = expected


def verify_output_names(actions):
    """Fail the build if a reference still carries a guessed output name."""
    names = _expected_output_names(actions)
    offenders = []
    for index, item in enumerate(actions):
        for token_dict in _walk_action_output_tokens(item.get("WFWorkflowActionParameters", {})):
            expected = names.get(token_dict.get("OutputUUID"))
            if expected and token_dict.get("OutputName") != expected:
                offenders.append((index, token_dict.get("OutputName"), expected))
    if offenders:
        raise SystemExit("magic-variable references carry a wrong OutputName: "
                         + "; ".join(f"action {i} says {got!r}, real name is {want!r}"
                                     for i, got, want in offenders[:5])
                         + f" ({len(offenders)} total)")


def verify_parameter_keys(actions):
    """Fail the build when an action emits a key its iOS action does not define."""
    offenders = []
    for index, item in enumerate(actions):
        allowed = VERIFIED_PARAMETER_KEYS.get(item.get("WFWorkflowActionIdentifier"))
        if allowed is None:
            continue
        unknown = set(item.get("WFWorkflowActionParameters", {})) - allowed - STRUCTURAL_KEYS
        if unknown:
            offenders.append((index, item["WFWorkflowActionIdentifier"], sorted(unknown)))
    if offenders:
        head = offenders[:5]
        raise SystemExit("unverified parameter keys emitted: "
                         + "; ".join(f"action {i} {ident} -> {keys}" for i, ident, keys in head)
                         + f" ({len(offenders)} total)")


def normalize_open_apps(actions):
    """Rewrite legacy app-picker strings left by earlier generated blocks."""
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.openapp":
            continue
        parameters = item["WFWorkflowActionParameters"]
        name = parameters.get("WFAppName") or parameters.get("WFSelectedApp", {}).get("Name")
        if name in APPS:
            parameters.clear()
            parameters.update(open_app(name)["WFWorkflowActionParameters"])


def fix_shownote_key(actions):
    """Rename the Control Room shownote action's input key from `target` to `WFInput`.

    CYCLE 14 -- Donor 8 (device ground truth, decrypted 2026-08-15) shows
    is.workflow.actions.shownote reads its note reference from WFInput; `target` is not a
    parameter this action defines at all, so it was silently ignored (axis 1, the same
    "wrong parameter key name" class this session already fixed 147 times elsewhere -- this
    one site was outside every prior sweep because the action itself was hand-authored, not
    emitted through set_value()/read_value()). With WFInput unfilled, the action had no
    bound note to show; the reported symptom (choosing "Open Control Room" surfaces a
    picker listing every note, then an editable box, rather than opening the resolved
    Control Room Note directly) is the interactive fallback iOS takes for an unfilled
    required note reference. "Control Room Note" itself IS correctly bound earlier in this
    same hand-authored block, in both the found and the created branch (filter.notes ->
    Get Item from List "First Item", and Create Note's own output) -- that part was never
    broken; only the final shownote's key name was wrong.
    Idempotent: a second run over an already-patched artifact finds no `target` key left.
    """
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.shownote":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if "target" in parameters and "WFInput" not in parameters:
            parameters["WFInput"] = parameters.pop("target")


# Donor 8's OWN filter.notes action (device ground truth, decrypted 2026-08-15, the SAME
# donor that settled fix_shownote_key()) carries an AppIntentDescriptor identifying it as
# the NoteEntity query, plus WFContentItemLimitEnabled=true / WFContentItemLimitNumber=1.
NOTES_FILTER_APP_INTENT = {
    "ActionRequiresAppInstallation": True,
    "AppIntentIdentifier": "NoteEntity",
    "BundleIdentifier": "com.apple.mobilenotes",
    "Name": "Notes",
    "TeamIdentifier": "0000000000",
}


def fix_notes_filter_limit(actions):
    """Bound the Control Room note search to exactly one result, Donor-8-matched.

    CYCLE 16 -- reported symptom: choosing "Open Control Room" correctly opens the
    resolved Control Room Note (fix_shownote_key()'s own fix, confirmed working: "it
    takes me to the control room note (good)") but a list of every note ALSO appears.
    "Control Room Note" itself is bound correctly in both the found and created branches
    (fix_shownote_key()'s own finding; unaffected by this fix) -- the extra list is not a
    binding defect, it is the ONE is.workflow.actions.filter.notes ("Find Notes") site in
    this artifact having no declared result bound at all: only UUID and WFContentItemFilter
    were ever emitted (hand-authored, outside every prior sweep -- same discovery class as
    the adjacent shownote site fix_shownote_key() corrects in this exact hand-authored
    block). Donor 8's OWN Find Notes action (device-authored in Shortcuts.app on the target
    iPhone) carries AppIntentDescriptor + WFContentItemLimitEnabled=true +
    WFContentItemLimitNumber=1 -- an explicit "exactly one result, never a chooser" bound;
    this artifact's site had none of the three. This artifact's own search predicate
    (Name contains the Note's user-facing title -- `PROSOCHĒ` since plan 11-03 shortened it
    from `PROSOCHĒ — Control Room`; the Operator is still 99, pinned by
    docs/note_identity_check.py) and its Get Item From List "First Item"
    consumer are unchanged and already correctly find the intended note (per the reported
    symptom itself) -- only the missing result bound is added, matching Donor 8's shape
    exactly rather than guessing which subset of the three fields matters.
    Idempotent: a second run finds WFContentItemLimitEnabled already present and returns.
    """
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.filter.notes":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if "WFContentItemLimitEnabled" in parameters:
            return
        parameters["AppIntentDescriptor"] = dict(NOTES_FILTER_APP_INTENT)
        parameters["WFContentItemLimitEnabled"] = True
        parameters["WFContentItemLimitNumber"] = 1.0
        return


def gate_control_room_shownote(actions):
    """Show the Control Room Note only when "Open Control Room" was actually chosen.

    PHASE 10 (10-02) -- reported symptom: every manual menu choice ends by launching the
    Notes app.  Choosing Status, Toggle Voice, Reset Today, Change Profile, Change
    Sequence, Sync My Profile, Test a Circle or Emergency Restore does its own work and
    then, without being asked, opens the Control Room Note on top of it.
    Mechanism: the artifact's single is.workflow.actions.shownote sits at depth 0 in the
    MANUAL arm -- inside no conditional at all -- as the common tail of the hand-authored
    find-or-create block, and the one menu item that SHOULD open the note, "Open Control
    Room", was a bare is.workflow.actions.nothing relying on exactly that unconditional
    tail for its entire effect.  So the note opened for everybody, and the item whose
    name promises it had no mechanism of its own.  Same discovery class as
    fix_shownote_key() and fix_notes_filter_limit(): a hand-authored block outside every
    generated sweep.
    Fix: give "Open Control Room" a real numeric flag (Manual Show Note Requested, set in
    manual_emergency_restore()) and wrap the shownote -- and only the shownote -- in an
    `if_block(flag, 2, number=0)` gate.  is.workflow.actions.filter.notes, the Create Note
    action and the recovery-append block above it are deliberately left OUTSIDE the gate:
    the note must keep being found or created on every manual run so a deleted note still
    self-heals (BOOT-08), and manual_note_refresh() must keep finding a bound "Control
    Room Note" variable to append to.
    The gate is built through if_block() rather than a hand-built dict because
    WFInput.Variable is a variable slot taking a bare WFTextTokenAttachment (axis 5), and
    verify_conditional_inputs() fails the build on anything else.  This pass runs after
    fix_shownote_key(), so the action it moves already carries WFInput rather than the
    ignored `target` key.
    Idempotent: this pass INSERTS actions rather than editing parameters, so the probe is
    positional -- a second run finds the action immediately preceding the shownote is
    already a mode-0 conditional with WFCondition 2 and returns without wrapping again.
    """
    for index, item in enumerate(actions):
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.shownote":
            continue
        if index:
            prior = actions[index - 1]
            prior_parameters = prior.get("WFWorkflowActionParameters", {})
            if (prior.get("WFWorkflowActionIdentifier") == "is.workflow.actions.conditional"
                    and prior_parameters.get("WFControlFlowMode") == 0
                    and prior_parameters.get("WFCondition") == 2):
                return
        gate_group, gate_if = if_block("Manual Show Note Requested", 2, number=0)
        # Authored here rather than left to main()'s auto-comment pass, so the emitted
        # plist carries the reason instead of the generic "Control-flow check" filler.
        gate_comment = comment(
            "Show the Control Room note only when it was explicitly asked for:\n"
            "- Reported symptom: every manual menu choice ended by launching the Notes app.\n"
            "- Mechanism: this Show Note sat at depth 0 in the MANUAL arm, outside every conditional, and \"Open Control Room\" was a bare Nothing relying on that unconditional tail.\n"
            "- Input is Manual Show Note Requested, set only by the \"Open Control Room\" menu case; the note is still found or created above on every manual run, so a deleted note still self-heals.\n"
            "- Idempotent: a rebuild finds this conditional already immediately before the Show Note and does not wrap it a second time.")
        actions[index:index + 1] = [
            gate_comment,
            gate_if,
            item,
            otherwise(gate_group),
            action("is.workflow.actions.nothing"),
            end_if(gate_group),
        ]
        return


def fix_date_format_key(actions):
    """Correct the behavioural-day format.date action's pattern key.

    CYCLE 14 -- Donor 7.1 (device ground truth, decrypted 2026-08-15) shows
    is.workflow.actions.format.date reads its Custom pattern from WFDateFormat, not from
    WFDateFormatString (the key this artifact -- and DATE_TIME.md's own prose -- assumed).
    The artifact carried WFDateFormat = the literal word "Custom" (the key iOS actually
    reads, holding a value that is not a pattern at all -- this is what rendered as the
    format string "Custom" in the UI) while the real Config-driven pattern
    (behavioural_day.key_format, "yyyy-MM-dd") sat in WFDateFormatString, a key iOS never
    reads for this action. This did not hard-fail (Behavioural Day resolved to SOME text,
    which is why breadcrumbs C and D already executed on device before this cycle), but it
    is a real, silent defect in the value the day-rollover comparison depends on, and it is
    axis 1 (wrong parameter key name) at the one format.date site this artifact has.
    Per directive 7b: the "yyyy-MM-dd" sort-key format has no built-in preset equivalent
    (ISO 8601 in DATE_TIME.md's own table includes time and a T/Z separator, which would
    make every run of the same day look like a different day) -- Custom + a real pattern
    in the key iOS reads is genuinely required here, not over-engineering.
    Idempotent: a second run finds WFDateFormat already holding the pattern, not "Custom".
    """
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.format.date":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFDateFormat") == "Custom" and "WFDateFormatString" in parameters:
            parameters["WFDateFormat"] = parameters.pop("WFDateFormatString")


# PHASE 11 (11-05) -- the three coupled schema-version literals, named once so they cannot
# drift apart again.  See fix_state_rebind()'s docstring and docs/CAPABILITY-DECISIONS.md
# BD-06-A3 for why there are three and why they are one edit.
#
# A STRING, because site 3 is a WFConditionalActionString and the device compares its stored
# schema_version as text; the template interpolates the same characters unquoted, which is
# what makes the two halves comparable at all.
SCHEMA_VERSION = "3"
SCHEMA_VERSION_PREVIOUS = "2"
# The RECOGNITION tuple.  It must admit every literal this transformer has ever written --
# including the one it is about to write -- or the NEXT build fails to locate the
# conditional and aborts, one build downstream of the change that caused it.
SCHEMA_VERSION_ACCEPTED = ("1", "2", "3")


def fix_state_rebind(actions):
    """Force a stale device state.json to rebuild once, and make the rebuild reach State.

    CYCLE 14 -- two independent gaps found while verifying build k, neither device-tested
    until now (debug session cycle 12/13 blind_spots):
    (1) The three-check validity gate (schema_version present, == "1", profile non-empty)
        accepts ANY file whose schema_version is exactly "1" as valid and skips the rebuild
        branch entirely -- so a device's pre-existing state.json, written before this
        session's settings_snapshot/sentinel/gate fixes, is used as-is forever, and the
        corrected bootstrap template this generator produces never reaches that device.
    (2) When the rebuild branch DOES run (clean install, or corrupted file), it writes a
        fresh Default State JSON to disk but never rebinds the `State` variable, which
        stays bound to whatever the earlier read produced -- a hard-error-prone value on a
        clean install, or the STALE shape on a device whose old file was just superseded on
        disk but not in memory for the rest of THIS run.
    Bumping schema_version (bootstrap template text + the version-check literal) closes (1):
    it forces every existing device to take the rebuild branch on its very next run, exactly
    once. The rebind closes (2): after the fresh JSON is produced,
    parse it the same way the initial load does (Detect Dictionary) and rebind State to
    that Dictionary output, not to the raw JSON text -- everything downstream
    (getvalueforkey/setvalueforkey) expects a Dictionary-content-item, matching
    normalize_setters()'s own rule that Set Dictionary Value's output must be rebound as a
    Dictionary, never as text. Two new actions (Detect Dictionary + Set Variable State),
    inserted immediately after Default State JSON is assigned, before the file save --
    HANDOFF.md's own "schema bump + rebind, ~2 actions" estimate.
    Idempotent: a second run finds schema_version already at SCHEMA_VERSION and the rebind
    already present.

    PHASE 11 (11-05) -- the version moves 2 -> 3, per docs/CAPABILITY-DECISIONS.md BD-06-A3
    Decision 1 ("bump"). It is needed because 11-05 adds a new bootstrap field
    (panic_escape_enabled) and 11-06 changes an existing seed value (the fork label); without
    the bump, a device that already holds a valid state.json reuses it forever and neither
    change ever lands. BD-06-A1 Amendment 3 records that there is no installed base, so the
    unrecoverable loss a bump normally carries (heat, gravity, pressure, the rolling windows,
    the session record, exit_stats[*].samples) costs nothing here. No migration, no dual-key
    alias and no read-time normalisation was built; BD-06-A1 forbids all three by name.

    THREE COUPLED LITERALS, not two -- measured by plan 11-04 and recorded in BD-06-A3's
    implementation-surface table. They must move in the SAME commit:
      1. SCHEMA_VERSION_PREVIOUS -> SCHEMA_VERSION in the template text  (the seed a rebuilt
         state.json is written with);
      2. SCHEMA_VERSION_ACCEPTED, the RECOGNITION tuple used to LOCATE the version-check
         conditional (what makes this transformer idempotent);
      3. SCHEMA_VERSION in version_check["WFConditionalActionString"]  (the runtime validity
         gate the device compares its stored value against).
    Sites 1 and 3 are the obvious pair: move the template without the gate and every device
    rebuilds forever; move the gate without the template and even a clean install fails the
    check it just wrote its file for. Site 2 is the one that is easy to miss, and it fails
    LATE: once site 3 writes the new value, the NEXT build no longer recognises the
    conditional, version_check stays None, and the build aborts at "schema version check
    conditional not found" -- an error that points at a missing conditional rather than at
    the bump one build earlier. Expressing all three from the constants below is what stops
    them drifting apart again.
    """
    _, inner = _state_template(actions)
    previous = f'"schema_version": {SCHEMA_VERSION_PREVIOUS},'
    current = f'"schema_version": {SCHEMA_VERSION},'
    if previous in inner["string"]:
        _replace_in_token(inner, previous, current)
    if current not in inner["string"]:
        raise SystemExit(
            f"the bootstrap template carries neither {previous!r} nor {current!r} -- the "
            "schema bump cannot be applied or confirmed, and a template whose version the "
            "runtime gate does not accept fails its own validity check on every device")
    version_check = None
    for item in actions:
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        descriptor = parameters.get("WFInput", {}).get("Variable", {}).get("Value", {})
        if descriptor.get("VariableName") == "State Schema Text" \
                and parameters.get("WFConditionalActionString") in SCHEMA_VERSION_ACCEPTED:
            version_check = parameters
            break
    if version_check is None:
        raise SystemExit("schema version check conditional not found")
    version_check["WFConditionalActionString"] = SCHEMA_VERSION
    for index, item in enumerate(actions):
        if not (item.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
                and item.get("WFWorkflowActionParameters", {}).get("WFVariableName") == "Default State JSON"):
            continue
        already = (index + 2 < len(actions)
                   and actions[index + 1].get("WFWorkflowActionIdentifier") == "is.workflow.actions.detect.dictionary"
                   and actions[index + 2].get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvariable"
                   and actions[index + 2].get("WFWorkflowActionParameters", {}).get("WFVariableName") == "State"
                   and actions[index + 2].get("WFWorkflowActionParameters", {}).get("WFInput", {}).get("Value", {}).get("OutputUUID")
                       == actions[index + 1].get("WFWorkflowActionParameters", {}).get("UUID"))
        if already:
            return
        rebind_id = uid()
        actions[index + 1:index + 1] = [
            action("is.workflow.actions.detect.dictionary", UUID=rebind_id, WFInput=variable("Default State JSON")),
            set_var("State", output(rebind_id, "Dictionary")),
        ]
        return
    raise SystemExit("Default State JSON assignment not found")


def main():
    global UUID_COUNTER
    UUID_COUNTER = 0
    data = plistlib.loads(SOURCE.read_bytes())  # exactly one parse
    actions = data["WFWorkflowActions"]
    pinned = plistlib.dumps(actions[:5], fmt=plistlib.FMT_XML)
    # Rebuild the semantic router arms atomically.  This keeps the Phase 4 outer
    # OPEN/CLOSE control flow while replacing only their owned bodies.
    replace_branch_body(actions, "--- OPEN STATE ENGINE ---", "Input Key was not OPEN", open_pipeline())
    replace_branch_body(actions, "--- CLOSE SESSION PIPELINE ---", "Input Key was neither OPEN nor CLOSE", close_pipeline())
    install_cooldown_branches(actions)
    insert_or_replace_after(actions, "--- CONTROL ROOM: confirm", MANUAL_MARKER,
                            "--- PHASE 5 MANUAL EMERGENCY RESTORE END ---", manual_emergency_restore())
    insert_or_replace_after(actions, "Check whether this run had to rebuild the setup file", "--- PHASE 7 MANUAL CONTROL ROOM REFRESH ---",
                            "--- PHASE 7 MANUAL CONTROL ROOM REFRESH END ---", manual_note_refresh())
    # Runs last of the structural passes: it moves the whole MANUAL arm, so every
    # marker-addressed replacement above should already have landed.
    restructure_router(actions)
    normalize_setters(actions)
    normalize_open_apps(actions)
    seed_settings_snapshot(actions)
    seed_pending_exit(actions)
    # Must run BEFORE fix_state_rebind(): the rebind pass also edits the same template
    # token, and seeding a new field is the reason the schema_version bump below exists.
    seed_panic_escape(actions)
    fix_state_rebind(actions)
    fix_date_format_key(actions)
    fix_shownote_key(actions)
    fix_notes_filter_limit(actions)
    # After fix_shownote_key(), so the action being wrapped already carries WFInput, and
    # after fix_notes_filter_limit(), so the note search it follows is already bounded.
    gate_control_room_shownote(actions)
    # The skill requires a repair-oriented, bulleted Comment immediately before
    # every control-flow start.  Make this invariant structural, not index-based.
    index = 0
    while index < len(actions):
        parameters = actions[index].get("WFWorkflowActionParameters", {})
        starts_flow = (actions[index].get("WFWorkflowActionIdentifier") in
                       {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count", "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}
                       and parameters.get("WFControlFlowMode") == 0)
        prior_is_comment = index > 0 and actions[index - 1].get("WFWorkflowActionIdentifier") == "is.workflow.actions.comment"
        if starts_flow and not prior_is_comment:
            actions.insert(index, comment("Control-flow check:\n- Use the named value prepared directly above.\n- Keep each branch or iteration balanced.\n- Continue with the full State dictionary unchanged unless this branch explicitly updates it."))
            index += 1
        index += 1
    normalise_string_envelopes(actions)
    normalise_output_names(actions)
    normalise_numeric_operands(actions)
    verify_parameter_keys(actions)
    verify_string_envelopes(actions)
    verify_output_names(actions)
    verify_required_pickers(actions)
    verify_conditional_inputs(actions)
    verify_conditional_action_string(actions)
    verify_numeric_operands(actions)
    verify_state_seed(actions)
    verify_pending_exit_seed(actions)
    verify_panic_escape_seed(actions)
    verify_restore_gates(actions)
    verify_sentinel_gates(actions)
    verify_compound_value_reads(actions)
    verify_router_shape(actions)
    verify_circle_zero_silence(actions)
    verify_dispatch_coverage(actions)
    # Declare that this shortcut consumes Shortcut Input.  The routing block reads the
    # ExtensionInput token, and PLIST_FORMAT.md defines this root key as "True if
    # shortcut uses input variables"; every modern golden shortcut that references
    # Shortcut Input sets it.  Derived from the actions so it can never drift.
    uses_shortcut_input = "ExtensionInput" in str(actions)
    if uses_shortcut_input:
        data["WFWorkflowHasShortcutInputVariables"] = True
        if not data.get("WFWorkflowInputContentItemClasses"):
            raise SystemExit("Shortcut Input is referenced but no input content classes are declared")
    if plistlib.dumps(actions[:5], fmt=plistlib.FMT_XML) != pinned:
        raise SystemExit("pinned actions 0-4 changed")
    SOURCE.write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False))  # exactly one serialization/write


if __name__ == "__main__":
    main()
