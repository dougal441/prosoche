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
# Shown in the manual menu prompt so a device run states, in its first seconds,
# which build is actually executing.  Importing a .shortcut whose display name
# matches an installed one can create a second copy and leave an automation
# wrapper pointed at the old shortcut; without a visible stamp that stale-install
# case is indistinguishable from a failed fix.  Bump on every device-bound build.
BUILD_STAMP = "build 2026-08-14j"
# CYCLE 7 MEASUREMENT INSTRUMENT, not a fix.  Cycle 6 proved on device that the Run
# Shortcut handoff DOES deliver "OPEN" (Probe 5 echoed it) while PROSOCHE still fails,
# so the failing action is inside the OPEN arm, before the first OPEN menu.  Static
# reading has produced three device-refuted "confirmations" and cannot evaluate the 336
# control-flow actions that exist in no ToolKit catalog, so the primary instrument is now
# bisection: one plain alert per span, at OPEN-arm base depth, so the LAST letter the user
# sees localises the failure to a span of tens in one round trip.
# The alert carries a plain-string title and a plain-string message.  Both shapes are
# already evidenced: the plain-string title ran on device as the cycle-3 ROUTER TRACE, and
# a plain-string WFAlertActionMessage appears in 5 of the 13 golden-corpus alerts.  No
# variable is referenced, so a breadcrumb cannot fail for a reason of its own.
# Set False to strip every breadcrumb; nothing else depends on them.
OPEN_BISECT = True
BISECT_TITLE = "PROSOCHĒ OPEN TRACE"
# One-run debug scaffolding on the MANUAL arm: report the cond-100 verdict and the
# bracketed Input Key value.  It exists because what an ABSENT Shortcut Input resolves
# to after normalisation is not determinable on the build Mac, and guessing it is what
# cost cycle 2.  Set False to strip it; the router fix does not depend on it.
ROUTER_TRACE = True
TRACE_MARKER = "--- ROUTER TRACE ---"
TRACE_END_MARKER = "--- ROUTER TRACE END ---"
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
UUID_COUNTER = 0

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


# CYCLE 11, axis 6b -- the CLEARED sentinel, single-sourced but DELIBERATELY UNCHANGED.
#
# Four state keys are written back as "cleared" and every one of them is consumed by an
# `If` with condition 100, HAS ANY VALUE: settings_snapshot.* (@181/186/200/205/1031/
# 1125), pending_exit (@483) and active_session (@689/1094/1232/1248).  The literal
# four-character string "null" is NON-EMPTY, so all of those gates read TRUE -- the exact
# inverse of the intent -- and the guarded NESTED reads then run against a string parent
# (active_session.id, active_session.declared_duration_seconds).  That is the same defect
# class as the settings_snapshot failure this cycle fixes, latent one level over.
#
# THE OBVIOUS REPAIR -- clear to EMPTY text -- WAS BUILT AND THEN REVERTED, and the reason
# is the whole finding.  It fails the project's mandatory validation gate at 12 sites:
#   Empty parameter at index 188: is.workflow.actions.setvalueforkey
#                                 -> WFDictionaryValue/Value/string
# validate_shortcut.py's iter_empty_strings() rejects an empty string in ANY parameter,
# with one narrow Send-Message-spacer exemption; "string" is in neither allow-list.  That
# rule encodes exactly this session's DEVICE-CONFIRMED symptom 2 -- an unset Value on Set
# Dictionary Value raises "No value was provided to the Set Dictionary Value action for
# the key <key>".  Clearing to empty would therefore trade a read-side hard error for a
# write-side one.
#
# The device evidence offered for empty -- EMPTY: NO VALUE -- is a READ-side measurement:
# a blank value reads as absent to condition 100.  It says nothing about whether Set
# Dictionary Value ACCEPTS a blank value.  Applying read-side evidence to a write is the
# same category error as the root cause being fixed this cycle, so it is refused here.
# The sentinel question is now a PRODUCER-vs-CONSUMER design choice (change the write, or
# change the six gates from cond 100 to cond 5 "is not null"), needs a donor to settle,
# and is deliberately not decided inside a cycle whose measurement must stay clean.
#
# NOT used for cooldown_until (3 further sites, left inline).  Its only consumer is the
# NUMERIC comparison at action 170, device-measured as NULL COERCED FALSE with no error,
# which is already the semantically correct reading of a cleared cooldown ("not in
# cooldown").  Changing it would alter behaviour at the most critical position on the
# OPEN path -- the conditional the build-i coercion fix just repaired.
CLEARED_SENTINEL = "null"


def cleared_value():
    """The CLEARED sentinel for a gate-consumed state key.  See the note above."""
    return text_token([(CLEARED_SENTINEL, None)])


def comment(text: str):
    return action("is.workflow.actions.comment", WFCommentActionText=text)


def set_var(name: str, source):
    return action("is.workflow.actions.setvariable", WFInput=source, WFVariableName=name)


def get_value(key, source, name: str):
    get_id = uid()
    return [
        action("is.workflow.actions.getvalueforkey", UUID=get_id, WFDictionaryKey=key, WFInput=source),
        action("is.workflow.actions.gettext", UUID=uid(), WFTextActionText=output(get_id, "Dictionary Value")),
        set_var(name, output(uid_value := "", name)) if False else set_var(name, variable(name + " Text")),
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


def elapsed(later_name: str, earlier_name: str, result_name: str):
    elapsed_id = uid()
    return [action("is.workflow.actions.gettimebetweendates", UUID=elapsed_id,
                   WFInput=token(later_name), WFTimeUntilFromDate=token(earlier_name),
                   WFTimeUntilUnit="Seconds"),
            set_var(result_name, output(elapsed_id, "Time Between Dates"))]


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


def breadcrumb(letter: str):
    """One OPEN-path bisection breadcrumb (cycle 7 measurement, see OPEN_BISECT).

    Returns a list so call sites can splice it unconditionally.  Deliberately
    contains no variable reference, no control flow and no UUID: it must be
    incapable of failing for a reason of its own, and it must not perturb the
    deterministic uid() counter, so that every action downstream of the OPEN arm
    keeps the UUIDs it had in build 2026-08-14f.
    """
    if not OPEN_BISECT:
        return []
    return [alert(BISECT_TITLE, f"{letter}\n\nReport the LAST letter you see.")]


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
    """Clear only a snapshot we have just restored from the full State."""
    return set_value(f"settings_snapshot.{key}", cleared_value(), dictionary_name)


def restore_managed_settings(dictionary_name="State"):
    """Restore only captured values; never guess an original setting."""
    a = [comment("""Restore managed settings only when a captured original exists:
- Brightness uses the saved original value, never a new target.
- Volume is always Media volume and never exceeds its saved original.
- A restored snapshot key is cleared while all unrelated State remains intact.""")]
    a += read_value("settings_snapshot.brightness", variable(dictionary_name), "Restore Brightness Snapshot")
    snapshot_g, snapshot_if = if_block("Restore Brightness Snapshot", 100)
    a += [snapshot_if] + read_value("settings_snapshot.brightness.original_value", variable(dictionary_name), "Restore Brightness")
    bright_g, bright_if = if_block("Restore Brightness", 100)
    a += [bright_if, set_brightness(variable("Restore Brightness")), clear_snapshot("brightness", dictionary_name),
          otherwise(bright_g), action("is.workflow.actions.nothing"), end_if(bright_g), otherwise(snapshot_g),
          action("is.workflow.actions.nothing"), end_if(snapshot_g)]
    a += read_value("settings_snapshot.volume", variable(dictionary_name), "Restore Volume Snapshot")
    snapshot_g, snapshot_if = if_block("Restore Volume Snapshot", 100)
    a += [snapshot_if] + read_value("settings_snapshot.volume.original_value", variable(dictionary_name), "Restore Volume")
    volume_g, volume_if = if_block("Restore Volume", 100)
    a += [volume_if, set_media_volume(variable("Restore Volume")), clear_snapshot("volume", dictionary_name),
          otherwise(volume_g), action("is.workflow.actions.nothing"), end_if(volume_g), otherwise(snapshot_g),
          action("is.workflow.actions.nothing"), end_if(snapshot_g)]
    return a


def knock():
    return [comment("""Knock is a brief factual interruption:
- Circle, Pressure, and Heat come from this OPEN run.
- It does not infer intent or alter State."""),
            alert("PROSOCHĒ", text_token([("Circle ", "Circle Next"),
                                           (" · pressure ", "Pressure Next"),
                                           (" · heat ", "Heat Final")] ))]


def ash():
    return [comment("""Ash is the validator-clean visual-pause fallback:
- It changes no accessibility setting.
- Color Filters is deliberately excluded because the iOS action is not validator-supported."""),
            alert("Ash", "Pause. Put the phone down for one breath.")]


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
          alert("Dimming", "Brightness could not be captured, so nothing was changed."), end_if(capture_g),
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
    a = [comment(DISPATCH_MARKER + "\n\n- Select exactly one configured sequence entry for Circle after Leaving is offered.\n- Combined entries call only their named primitives.")]
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
    for name, implementation in (("Knock", knock), ("Ash", ash), ("Silence", silence),
                                 ("Confession", confession), ("Dimming", dimming), ("Exile", exile),
                                 ("Mirror", mirror_and_voice), ("Voice", mirror_and_voice), ("Ice", ice_start)):
        # Mirror is rendered once for a combined Silence+Mirror entry; Voice is a separate sequence name.
        if name == "Voice":
            continue
        group, check = if_block("Selected Primitive", 99, string=name)
        a += [comment(f"Dispatch {name} only when the selected Config entry names it:\n- Input uses Selected Primitive from the sequence lookup.\n- The otherwise path leaves State unchanged."), check]
        a += implementation() + [otherwise(group), action("is.workflow.actions.nothing"), end_if(group)]
    a += [comment("--- PHASE 5 PRIMITIVE DISPATCH END ---")]
    return a


def enabled_exits(source="State"):
    """Filter in canonical order; no disabled name can enter a selection menu."""
    a = [comment("Build Enabled Exits in canonical order by intersecting the saved profile list.")]
    a += read_value("profile_snapshot.enabled_exits", variable(source), "Profile Enabled Exits")
    a += list_items(EXIT_NAMES, "Canonical Exits")
    outer = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=outer, WFControlFlowMode=0,
                 WFInput=variable("Canonical Exits")), set_var("Canonical Exit", variable("Repeat Item"))]
    inner = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=inner, WFControlFlowMode=0,
                 WFInput=variable("Profile Enabled Exits")), set_var("Enabled Exit Candidate", variable("Repeat Item"))]
    matches_group, matches = if_block("Enabled Exit Candidate", 4, string="canonical-exit-placeholder")
    matches["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    a += [matches, action("is.workflow.actions.appendvariable", WFInput=variable("Canonical Exit"), WFVariableName="Enabled Exits"),
          otherwise(matches_group), action("is.workflow.actions.nothing"), end_if(matches_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=inner, WFControlFlowMode=2),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=outer, WFControlFlowMode=2)]
    return a


def select_exit():
    """Deterministic, state-driven selector. The concrete menu always shares recorder/router."""
    a = [comment("--- PHASE 6 EXIT SELECTOR ---\n\n- Sparse data rotates enabled exits by the persisted counter.\n- Sufficient data uses integer averages, canonical ties, then configured epsilon exploration.")]
    a += enabled_exits() + read_value("exit_selection_counter", variable("State"), "Exit Selection Counter")
    missing_counter, counter = if_block("Exit Selection Counter", 5, string=None)
    counter["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
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
    a += [is_best, *number(1, "Past Best"), otherwise(is_best_group)]
    choose_after_group, choose_after = if_block("Past Best", 2, number=0)
    a += [choose_after]
    unchosen_group, unchosen = if_block("Exploration Selected", 4, string="0")
    unchosen["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    a += [unchosen, set_var("Selected Exit", variable("Candidate Exit")), *number(1, "Exploration Selected"), otherwise(unchosen_group), action("is.workflow.actions.nothing"), end_if(unchosen_group),
          otherwise(choose_after_group), action("is.workflow.actions.nothing"), end_if(choose_after_group), end_if(is_best_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=next_loop, WFControlFlowMode=2)]
    wrap_loop = uid()
    a += [comment("Exploration wrap:\n- After Close, choose the first canonical non-best exit exactly once."),
          action("is.workflow.actions.repeat.each", GroupingIdentifier=wrap_loop, WFControlFlowMode=0, WFInput=variable("Enabled Exits")),
          set_var("Candidate Exit", variable("Repeat Item"))]
    needs_wrap_group, needs_wrap = if_block("Exploration Selected", 4, string="0")
    needs_wrap["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    wrap_non_best_group, wrap_non_best = if_block("Candidate Exit", 99, string="best-exit-placeholder")
    wrap_non_best["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
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
    a += [owner, action("is.workflow.actions.gettext", UUID=event_json, WFTextActionText=event_text),
          action("is.workflow.actions.detect.dictionary", UUID=event_dict, WFInput=output(event_json, "Text")),
          set_var("Exit Event", output(event_dict, "Dictionary")), *read_value("exit_events", variable("Reloaded State"), "Exit Events")]
    a += [action("is.workflow.actions.appendvariable", WFInput=variable("Exit Event"), WFVariableName="Exit Events Next")]
    cap_loop = uid()
    a += [action("is.workflow.actions.repeat.each", GroupingIdentifier=cap_loop, WFControlFlowMode=0, WFInput=variable("Exit Events"))]
    cap_group, cap = if_block("Repeat Index", 0, number=20)
    a += [cap, action("is.workflow.actions.appendvariable", WFInput=variable("Repeat Item"), WFVariableName="Exit Events Next"), otherwise(cap_group), action("is.workflow.actions.nothing"), end_if(cap_group),
          action("is.workflow.actions.repeat.each", UUID=uid(), GroupingIdentifier=cap_loop, WFControlFlowMode=2)]
    a += [set_value("exit_events", variable("Exit Events Next"), "Reloaded State"),
          set_value("pending_exit", variable("Exit Event"), "Reloaded State"), *read_value("exit_selection_counter", variable("Reloaded State"), "Reloaded Exit Counter")]
    missing_counter, counter = if_block("Reloaded Exit Counter", 5, string=None)
    counter["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    a += [counter] + number(0, "Reloaded Exit Counter") + [otherwise(missing_counter), action("is.workflow.actions.nothing"), end_if(missing_counter)]
    a += math("Reloaded Exit Counter", 1, "Exit Counter Next", "+") + [set_value("exit_selection_counter", variable("Exit Counter Next"), "Reloaded State")]
    a += save_state("Reloaded State") + route_exit(choice_name)
    a += [otherwise(owner_group), action("is.workflow.actions.nothing"), end_if(owner_group), otherwise(active_group), action("is.workflow.actions.nothing"), end_if(active_group)]
    return a


def universal_leaving():
    group = uid()
    a = [comment(EXIT_MARKER + "\n\n- The session was saved before every interactive action.\n- Leaving is available before every primitive in every sequence and Circle.\n- Continue reaches exactly the selected primitive."),
         menu(group, 0, prompt="PROSOCHĒ", items=["Leaving", "Continue"]), menu(group, 1, title="Leaving")]
    a += select_exit() + [menu(group, 1, title="Continue")] + primitive_dispatch() + [menu(group, 2), comment("--- PHASE 6 UNIVERSAL LEAVING END ---")]
    return a


def complete_pending_exit():
    """The one guarded genuine OPEN that follows an exit records its time away once."""
    a = [comment("--- PHASE 6 PENDING EXIT OUTCOME ---\n\n- This runs only after cooldown and duplicate OPEN guards.\n- A pending exit records one elapsed sample, then is cleared before the new session begins.")]
    a += read_value("pending_exit", variable("State"), "Pending Exit")
    pending_group, pending = if_block("Pending Exit", 100)
    a += [pending] + read_value("pending_exit.type", variable("State"), "Pending Exit Type") + read_value("pending_exit.timestamp", variable("State"), "Pending Exit Timestamp")
    a += elapsed("Now Date", "Pending Exit Timestamp", "Return Seconds")
    a += read_value(text_token([("exit_stats.", "Pending Exit Type"), (".samples", None)]), variable("State"), "Exit Samples")
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
          set_value("pending_exit", cleared_value()),
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
    # BREADCRUMB A - the OPEN arm was entered at all.
    a += breadcrumb("A")
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
    # BREADCRUMB B - every state read and every config read completed.
    a += breadcrumb("B")
    # Behavioural day rollover is the first state update (only opens_today resets).
    g, start = if_block("Stored Day", 5, string=None)
    # Code 5 requires a string; textual empty guards avoid direct null compare.
    start["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    a += [comment("""Check whether a saved behavioural day exists before comparing it to today:
- A missing value is treated as rollover so the counter is safe on migrated state.
- A present value continues to the same-day comparison below.
- Only opens_today is reset; Heat and histories remain untouched."""), start]
    a += number(0, "Zero") + [set_value("opens_today", variable("Zero")), set_value("behavioural_day", variable("Behavioural Day")), otherwise(g)]
    day_group, day_if = if_block("Stored Day", 4, string="same-day-placeholder")
    day_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    # The explicit Text variable is compared as a string to the Behavioural Day token.
    a += [comment("""Compare the stored behavioural day with today's adjusted day:
- Both values are text, so equality is the supported string comparison.
- A different day resets only opens_today and records today's key.
- A matching day leaves the counter intact."""), day_if, otherwise(day_group)]
    a += number(0, "Zero") + [set_value("opens_today", variable("Zero")), set_value("behavioural_day", variable("Behavioural Day")), end_if(day_group), end_if(g)]
    # BREADCRUMB C - the behavioural-day rollover block resolved (either arm).
    a += breadcrumb("C")
    # Cooldown and debounce each choose their own genuine no-inflation branch.
    a += [comment("""Short-circuit a live cooldown before any Heat arithmetic:
- Input is the saved cooldown deadline routed through text.
- A future deadline leaves Heat and the open count unchanged, then records the state once.
- Otherwise the regular duplicate guard and OPEN pipeline continue.""")]
    cooldown_group, cooldown_if = if_block("Cooldown Until", 2, number=variable("Now Epoch"))
    a += [cooldown_if] + save_state() + [otherwise(cooldown_group)]
    # BREADCRUMB D - no live cooldown, and the Ice-expiry restoration block (which
    # install_cooldown_branches splices in immediately above this point) completed.
    a += breadcrumb("D")
    a += [comment("""Debounce duplicate OPEN triggers with the saved last-open timestamp:
- A short repeat OPEN is not a new interaction and takes the no-mutation path.
- A genuine later OPEN continues to ordered Heat arithmetic.
- This is timestamp comparison only, not a second event system.""")]
    # Prototype 2-second debounce: config intentionally has no debounce field.
    a += number(1, "Genuine Open")
    debounce_exists, debounce_exists_if = if_block("Last Open", 100)
    a += [debounce_exists_if] + elapsed("Now Date", "Last Open", "Seconds Since Open")
    debounce_group, debounce_if = if_block("Seconds Since Open", 0, number=2)
    a += [comment("Duplicate OPEN guard (prototype 2 seconds):\n- Compare the elapsed seconds from the captured last-open timestamp.\n- A value below two exits through Nothing with no dictionary mutation.\n- A later event continues to the complete Heat pipeline."), debounce_if,
          *number(0, "Genuine Open"), otherwise(debounce_group), action("is.workflow.actions.nothing"), end_if(debounce_group), otherwise(debounce_exists), action("is.workflow.actions.nothing"), end_if(debounce_exists)]
    genuine_group, genuine = if_block("Genuine Open", 2, number=0)
    a += [genuine]
    # BREADCRUMB E - the duplicate-OPEN debounce resolved and this is a genuine open.
    a += breadcrumb("E")
    # Current state values are loaded only after the short circuit branches.
    a += read_value("heat", variable("State"), "Heat Current") + read_value("opens_today", variable("State"), "Opens Today")
    a += [comment("""Compute Heat in its required order, then clamp it last:
- Decay applies first from time away, then base OPEN and the exclusive/cumulative reopen rule.
- Previous overrun or respected contract adjustment follows the reopen adjustment.
- Floor and cap are the final two guards before Gravity and Pressure.""")]
    # Decay uses the previous genuine close; absent first-run values leave Heat intact.
    a += [set_var("Heat After Decay", variable("Heat Current"))]
    decay_exists, decay_exists_if = if_block("Last Close", 100)
    a += [decay_exists_if] + elapsed("Now Date", "Last Close", "Seconds Away") + math("Seconds Away", variable("Decay Interval"), "Decay Intervals Raw", "÷") + round_down("Decay Intervals Raw", "Decay Intervals") + math("Decay Intervals", variable("Decay Amount"), "Decay Delta", "×") + math("Heat After Decay", variable("Decay Delta"), "Heat After Decay") + [otherwise(decay_exists), action("is.workflow.actions.nothing"), end_if(decay_exists)]
    a += math("Heat After Decay", variable("Open Base"), "Heat After Base")
    # Reopen bands read their seconds from the same real last-close timestamp.
    reopen120, if120 = if_block("Last Close", 100)
    a += [if120] + elapsed("Now Date", "Last Close", "Seconds Since Close")
    under120_g, under120_if = if_block("Seconds Since Close", 0, number=120)
    exclusive_g, exclusive_if = if_block("Reopen Bonus Mode", 4, string="exclusive")
    a += [under120_if, exclusive_if] + math("Heat After Base", variable("Reopen 120 Bonus"), "Heat After Reopen") + [otherwise(exclusive_g)] + math("Heat After Base", variable("Reopen 120 Bonus"), "Heat After Reopen") + math("Heat After Reopen", variable("Reopen 600 Bonus"), "Heat After Reopen") + [end_if(exclusive_g), otherwise(under120_g)]
    under600_g, under600_if = if_block("Seconds Since Close", 0, number=600)
    a += [under600_if] + math("Heat After Base", variable("Reopen 600 Bonus"), "Heat After Reopen") + [otherwise(under600_g), set_var("Heat After Reopen", variable("Heat After Base")), end_if(under600_g), end_if(under120_g), otherwise(reopen120), set_var("Heat After Reopen", variable("Heat After Base")), end_if(reopen120)]
    # Previous session's recorded overrun is the cross-run contract signal.
    a += read_value("recent_sessions", variable("State"), "Recent Sessions")
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
    # BREADCRUMB F - the whole ordered Heat pipeline is done: decay, base, reopen bands,
    # previous-contract adjustment, floor clamp and cap clamp.
    a += breadcrumb("F")
    # Genuine OPEN writes active session and all derived fields to the same rooted State dictionary.
    a += math("Opens Today", variable("Open Base"), "Opens Today Next")
    a += [set_value("opens_today", variable("Opens Today Next")), set_value("last_open_at", variable("Now Epoch")), set_value("last_app", text_token([("tracked", None)]))]
    # BREADCRUMB G - placed immediately BEFORE Random Number.  Span G->H isolates the
    # first of the two scalar-type suspects Donor 3 surfaced this cycle.
    a += breadcrumb("G")
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
- Start at Circle 1 and use the active profile's Config threshold list.
- Each satisfied greater-than-or-equal comparison overwrites Circle with the current index.
- Ascending thresholds make the final satisfied index the correct Circle; no numeric equality is used.""")]
    # BREADCRUMB H - Random Number, Session ID, Detect Dictionary, Gravity and Pressure
    # all completed.  Span H->I isolates the second scalar-type suspect (Repeat count).
    a += breadcrumb("H")
    a += number(1, "Circle Next")
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
    # BREADCRUMB I - the nine-step Circle threshold scan completed all nine iterations.
    a += breadcrumb("I")
    a += [set_value("circle", variable("Circle Next")), set_value("behavioural_day", variable("Behavioural Day"))]
    a += complete_pending_exit()
    # BREADCRUMB J - Circle written and any pending exit completed.  The only actions
    # left before the first OPEN menu are Save File and the Phase 6 leaving block.
    a += breadcrumb("J")
    # State is persisted before any menu/Ask action. The wrapper owns all later interaction.
    a += save_state() + universal_leaving() + [end_if(genuine_group), end_if(cooldown_group)]
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
    a += read_value("recent_sessions", variable("Reloaded State"), "Recent Sessions")
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


def router_trace():
    """Report what an absent Shortcut Input actually normalises to, on device.

    Placed at the head of the MANUAL arm so ONE round-trip measures two things: what
    Input Key is on a manual tap, and — if the OPEN automation still misroutes — what
    Input Key is on the automation path, which is the single most valuable unknown left.

    Deliberately contains NO control flow. An earlier draft tested "Input Key has any
    value" here to report the cond-100 verdict; that conditional was byte-identical to the
    router gate this build removes, so both find_absence_gate() and verify_router_shape()
    matched it and the pass stopped being idempotent. The verdict is not needed anyway:
    cycle 2 already established on device that cond 100 passes on a manual tap, because the
    unrecognised-input alert is unreachable otherwise. What remains unknown is the VALUE,
    and a printed empty-string reference on the adjacent line discriminates it: if the two
    bracket pairs render identically the value is present but non-printing.
    """
    return [comment(TRACE_MARKER + """

- Debug scaffolding only; it reads nothing, writes nothing, and branches nowhere.
- It shows the normalised Input Key in brackets beside an empty-string reference.
- Identical-looking brackets mean Input Key holds a non-printing character, since cycle 2 already proved on device that it is non-empty here.
- Remove by setting ROUTER_TRACE = False in tools/build_state_engine.py and rebuilding."""),
            alert("PROSOCHĒ " + BUILD_STAMP,
                  text_token([("MANUAL arm reached.\n\nInput Key: [", "Input Key"),
                              ("]\nEmpty ref: []\n\nIf those two lines look the same, Input Key is a "
                               "non-printing character rather than visible text.", None)])),
            comment(TRACE_END_MARKER)]


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
         menu(group, 0, prompt="Ice is active", items=["Return Home", "Emergency Restore"]),
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
    choices = ["Status", "Open Control Room", "Sync My Profile", "Change Profile", "Change Sequence", "Toggle Voice", "Test a Circle", "Reset Today", "Emergency Restore"]
    a = [comment(MANUAL_MARKER + "\n\n- Manual control is the only path that refreshes the Control Room or reads its proforma.\n- OPEN and CLOSE never enter this menu or parse the Note.\n- Test Circle copies recorded values into test variables and never writes Pressure."),
         menu(group, 0, prompt=f"PROSOCHĒ · {BUILD_STAMP}", items=choices)]
    for title in ("Status", "Open Control Room"):
        a += [menu(group, 1, title=title), *number(1, "Manual Refresh Requested")]
    a += [menu(group, 1, title="Sync My Profile"), *number(1, "Manual Refresh Requested"), *number(1, "Manual Sync Requested")]
    profile_menu = uid()
    a += [menu(group, 1, title="Change Profile"), menu(profile_menu, 0, prompt="Choose profile", items=["Paradise", "Limbo", "Inferno"])]
    for profile in ("Paradise", "Limbo", "Inferno"):
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
    a += [menu(group, 1, title="Test a Circle"), menu(test_menu, 0, prompt="Test a Circle", items=[f"Circle {number}" for number in range(1, 10)])]
    for test_circle in range(1, 10):
        a += [menu(test_menu, 1, title=f"Circle {test_circle}"), *number(test_circle, "Test Circle")]
        a += read_value("pressure", variable("State"), "Pressure Next") + read_value("heat", variable("State"), "Heat Final") + read_value("circle", variable("State"), "Circle Next")
        a += [set_var("Circle Next", variable("Test Circle")), comment("Test Circle uses a copied Circle value:\n- Pressure remains the saved recorded value.\n- This branch does not set or save Pressure.\n- Chosen Circle behaviour runs with the copied value only.")] + primitive_dispatch("Test Circle")
    a += [menu(test_menu, 2), menu(group, 1, title="Reset Today"), *number(0, "Manual Zero"), set_value("opens_today", variable("Manual Zero")), set_value("gravity", variable("Manual Zero")), *number(1, "Manual Refresh Requested"), *save_state(), menu(group, 1, title="Emergency Restore")]
    a += restore_managed_settings("State")
    a += [set_value("cooldown_until", text_token([("null", None)])),
          set_value("active_session", cleared_value()), *number(1, "Manual Refresh Requested")]
    a += save_state()
    a += [menu(group, 2), comment("--- PHASE 5 MANUAL EMERGENCY RESTORE END ---")]
    return a


def manual_note_refresh():
    """Append current settings/state only after an explicit manual menu choice."""
    a = [comment("--- PHASE 7 MANUAL CONTROL ROOM REFRESH ---\n\n- This runs after the Note is found or created in the MANUAL branch only.\n- It appends a factual current snapshot and meaningful manual events.\n- OPEN never reaches this Note parsing or append block.")]
    for key, name in (("fork", "Snapshot Fork"), ("profile", "Snapshot Profile"), ("sequence", "Snapshot Sequence"), ("voice_enabled", "Snapshot Voice"), ("pressure", "Snapshot Pressure"), ("circle", "Snapshot Circle"), ("cooldown_until", "Snapshot Cooldown"), ("profile_snapshot.enabled_exits", "Snapshot Exits")):
        a += read_value(key, variable("State"), name)
    refresh_g, refresh_if = if_block("Manual Refresh Requested", 2, number=0)
    snapshot_id = uid()
    snapshot = text_token([("\n\n## CURRENT SETTINGS\n- Fork: ", "Snapshot Fork"), ("\n- Profile: ", "Snapshot Profile"), ("\n- Sequence: ", "Snapshot Sequence"), ("\n- Voice: ", "Snapshot Voice"), ("\n- AI: not used by this fork\n- Enabled exits: ", "Snapshot Exits"), ("\n\n## CURRENT STATE\n- Circle: ", "Snapshot Circle"), ("\n- Pressure: ", "Snapshot Pressure"), ("\n- Cool-down until: ", "Snapshot Cooldown"), ("\n\n## ATTENTION LEDGER\n- Manual Control Room refresh at ", "Now Epoch")])
    a += [refresh_if, action("is.workflow.actions.gettext", UUID=snapshot_id, WFTextActionText=snapshot), action("is.workflow.actions.appendnote", operation="append", entity=variable("Control Room Note"), text=output(snapshot_id, "Text")), otherwise(refresh_g), action("is.workflow.actions.nothing"), end_if(refresh_g)]
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
# the only gate standing between a renamed key and a runtime "No value provided".
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
        + ", ".join(f'"{leaf}": ""' for leaf in leaves)
        + "}"
        for group, leaves in SNAPSHOT_SEED.items())
    return '"settings_snapshot": {\n' + inner + "\n" + indent + "},"


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
        if node != "":
            raise SystemExit(f"{key} is seeded as {node!r}; it must be EMPTY -- a fabricated "
                             "original_value could restore a setting the user never had")


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


def _numeric_operand_report(actions):
    """Every numeric-code conditional, with its operand descriptor and provenance.

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
        if item.get("WFWorkflowActionIdentifier") != "is.workflow.actions.conditional":
            continue
        parameters = item.get("WFWorkflowActionParameters", {})
        if parameters.get("WFControlFlowMode") != 0:
            continue
        if parameters.get("WFCondition") not in NUMERIC_CONDITION_CODES:
            continue
        descriptor = (parameters.get("WFInput") or {}).get("Variable", {}).get("Value")
        if not isinstance(descriptor, dict):
            report.append((index, None, {"<not-a-descriptor>"}))
            continue
        if descriptor.get("Type") == "ActionOutput":
            sources = {produced.get(descriptor.get("OutputUUID"), "<unknown>")}
        elif descriptor.get("VariableName") in NUMERIC_BUILTIN_VARIABLES:
            sources = {"<builtin>"}
        else:
            sources = resolve(descriptor.get("VariableName")) or {"<undefined>"}
        report.append((index, descriptor, sources))
    return report


def _already_numeric(sources):
    return bool(sources) and sources <= (NUMERIC_SOURCE_ACTIONS | {"<builtin>"})


def normalise_numeric_operands(actions):
    """Type every numeric conditional's operand as a Number, the way iOS does.

    Attaches Donor 4.1's WFCoercionVariableAggrandizement to the operand descriptor of any
    numeric-code conditional whose operand is not already Number-typed.  Structural rather
    than site-by-site: a future numeric comparison on a text-coerced value is corrected
    automatically, and the matching invariant is asserted by verify_numeric_operands().
    Operands that are already numeric are left untouched, so the numeric conditionals that
    have executed on device stay byte-identical.
    """
    for _index, descriptor, sources in _numeric_operand_report(actions):
        if descriptor is None or _already_numeric(sources):
            continue
        existing = descriptor.setdefault("Aggrandizements", [])
        if not any(a.get("Type") == "WFCoercionVariableAggrandizement" for a in existing):
            # Coercion goes FIRST: golden 332c12a0 orders coercion before any property
            # aggrandizement, because the property is read from the coerced item.
            existing.insert(0, dict(NUMBER_COERCION))


def verify_numeric_operands(actions):
    """Fail the build if a numeric conditional compares an untyped, non-numeric operand.

    See the block comment above for the mechanism and the Donor 4.1 evidence.  This is the
    fifth axis the generator asserts, after key name, value envelope, picker literal and
    variable slot -- and the only one with no representation in the ToolKit catalog, the
    bundled validator, or the signed artifact.
    """
    offenders = []
    for index, descriptor, sources in _numeric_operand_report(actions):
        if descriptor is None:
            offenders.append((index, "operand is not a variable descriptor"))
            continue
        if _already_numeric(sources):
            continue
        coerced = any(a.get("Type") == "WFCoercionVariableAggrandizement"
                      and a.get("CoercionItemClass") == "WFNumberContentItem"
                      for a in descriptor.get("Aggrandizements", []))
        if not coerced:
            offenders.append((index, f"operand is fed by {', '.join(sorted(sources))} "
                                     "and carries no Number coercion"))
    if offenders:
        raise SystemExit(
            "numeric conditional operands are not Number-typed -- Shortcuts populates the "
            "operator picker from the operand's type, so the numeric comparator has no case "
            "to render, the chip shows RED and the action refuses to run: "
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
    remove_marker_block(actions, TRACE_MARKER, TRACE_END_MARKER)
    if ROUTER_TRACE:
        fallback = comment_index(actions, ROUTE_FALLBACK_MARKER)
        actions[fallback + 1:fallback + 1] = router_trace()
    normalize_setters(actions)
    normalize_open_apps(actions)
    seed_settings_snapshot(actions)
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
    verify_numeric_operands(actions)
    verify_state_seed(actions)
    verify_router_shape(actions)
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
