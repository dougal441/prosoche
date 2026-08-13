#!/usr/bin/env python3
"""Fill the semantic OPEN/CLOSE anchors in the PROSOCHE shortcut once.

This deliberately parses and serializes the plist once.  Anchors are found by
their branch comments, never by mutable action indexes.
"""
from __future__ import annotations

import plistlib
import uuid
from pathlib import Path


SOURCE = Path("src/PROSOCHE-Dumb.xml")
DISPATCH_MARKER = "--- PHASE 5 PRIMITIVE DISPATCH ---"
RESTORE_MARKER = "--- PHASE 5 RESTORE MANAGED SETTINGS ---"
MANUAL_MARKER = "--- PHASE 5 MANUAL EMERGENCY RESTORE ---"
LIVE_ICE_MARKER = "--- PHASE 5 LIVE ICE REDIRECT ---"
EXPIRY_MARKER = "--- PHASE 5 ICE EXPIRY ---"
UUID_COUNTER = 0


def uid() -> str:
    global UUID_COUNTER
    UUID_COUNTER += 1
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche-state-engine/{UUID_COUNTER}")).upper()


def action(identifier: str, **parameters):
    return {"WFWorkflowActionIdentifier": identifier,
            "WFWorkflowActionParameters": parameters}


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
    return action("is.workflow.actions.setvalueforkey", UUID=uid(), WFDictionaryKey=key,
                  WFDictionary=variable(dictionary_name), WFInput=value)


def if_block(value_name: str, condition: int, *, number=None, string=None):
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
    if op:
        params["WFMathOperation"] = op
    return [action("is.workflow.actions.math", **params), set_var(result_name, output(math_id, "Calculation Result"))]


def elapsed(later_name: str, earlier_name: str, result_name: str):
    elapsed_id = uid()
    return [action("is.workflow.actions.gettimebetweendates", UUID=elapsed_id,
                   WFInput=token(later_name), WFTimeUntilFromDate=token(earlier_name),
                   WFTimeUntilUnit="Seconds"),
            set_var(result_name, output(elapsed_id, "Time Between Dates"))]


def round_down(source_name: str, result_name: str):
    round_id = uid()
    return [action("is.workflow.actions.round", UUID=round_id, WFInput=variable(source_name),
                   WFRoundMode="Down", WFRoundTo="Ones Place"),
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
    return set_value(f"settings_snapshot.{key}", text_token([("null", None)]), dictionary_name)


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


def mirror_and_voice():
    a = [comment("""Mirror states only guarded recorded facts:
- Circle, Pressure, and Heat are prepared by this OPEN run.
- Voice uses this same text at most once when it is enabled.""")]
    mirror_id = uid()
    a += [action("is.workflow.actions.gettext", UUID=mirror_id,
                 WFTextActionText=text_token([("Circle ", "Circle Next"),
                                               (" follows recorded pressure ", "Pressure Next"),
                                               (" and heat ", "Heat Final")])),
          set_var("Mirror Text", output(mirror_id, "Text")),
          alert("Mirror", variable("Mirror Text"))]
    a += read_value("voice_enabled", variable("State"), "Voice Enabled")
    voice_g, voice_if = if_block("Voice Enabled", 2, number=0)
    spoken_g, spoken_if = if_block("Spoken This Run", 101)
    a += [voice_if, spoken_if, action("is.workflow.actions.speaktext", WFInput=variable("Mirror Text"))]
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


def primitive_dispatch():
    a = [comment(DISPATCH_MARKER + "\n\n- Select exactly one configured sequence entry for Circle.\n- Combined entries call only their named primitives.\n- Heat, Gravity, Pressure, and Circle are already computed and remain untouched.")]
    a += read_value("sequence", variable("State"), "Sequence") + read_value("circle", variable("State"), "Dispatch Circle")
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
    a += config("heat.contract_respected_relief", "Respect Relief") + config("gravity.opens_per_point", "Opens Per Gravity") + config("gravity.cap", "Gravity Cap")
    # Behavioural day rollover is the first state update (only opens_today resets).
    g, start = if_block("Stored Day", 5, string=None)
    # Code 5 requires a string; textual empty guards avoid direct null compare.
    start["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    start["WFWorkflowActionParameters"]["WFInput"] = {"Type": "Variable", "Variable": token("Stored Day")}
    a += [comment("""Check whether a saved behavioural day exists before comparing it to today:
- A missing value is treated as rollover so the counter is safe on migrated state.
- A present value continues to the same-day comparison below.
- Only opens_today is reset; Heat and histories remain untouched."""), start]
    a += number(0, "Zero") + [set_value("opens_today", variable("Zero")), set_value("behavioural_day", variable("Behavioural Day")), otherwise(g)]
    day_group, day_if = if_block("Stored Day", 4, string="same-day-placeholder")
    day_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = "\ufffc"
    day_if["WFWorkflowActionParameters"]["WFInput"] = {"Type": "Variable", "Variable": token("Stored Day")}
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
    debounce_exists, debounce_exists_if = if_block("Last Open", 100)
    a += [debounce_exists_if] + elapsed("Now Date", "Last Open", "Seconds Since Open")
    debounce_group, debounce_if = if_block("Seconds Since Open", 0, number=2)
    a += [comment("Duplicate OPEN guard (prototype 2 seconds):\n- Compare the elapsed seconds from the captured last-open timestamp.\n- A value below two exits through Nothing with no dictionary mutation.\n- A later event continues to the complete Heat pipeline."), debounce_if,
          action("is.workflow.actions.nothing"), otherwise(debounce_group), end_if(debounce_group), otherwise(debounce_exists), action("is.workflow.actions.nothing"), end_if(debounce_exists)]
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
    a += read_value("overrun_seconds", variable("Previous Session"), "Previous Overrun")
    overrun_g, overrun_if = if_block("Previous Overrun", 2, number=120)
    a += [overrun_if] + math("Heat After Reopen", variable("Overrun Penalty"), "Heat After Contract") + [otherwise(overrun_g), set_var("Heat After Contract", variable("Heat After Reopen")), end_if(overrun_g), otherwise(session_exists), set_var("Heat After Contract", variable("Heat After Reopen")), end_if(session_exists)]
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
    a += [action("is.workflow.actions.number.random", UUID=random_id, WFNumberMin=1, WFNumberMax=2147483647),
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
    a += [set_value("circle", variable("Circle Next")), set_value("behavioural_day", variable("Behavioural Day"))]
    a += [comment("""--- PHASE 5 DISPATCH HOOK ---

- Circle has been computed and persisted from the full State dictionary.
- Phase 5 attaches the selected primitive sequence after this marker.
- This phase intentionally performs no Circle behaviour.""")]
    a += save_state() + [end_if(cooldown_group)]
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
    owns_if["WFWorkflowActionParameters"]["WFInput"] = {"Type": "Variable", "Variable": token("Reloaded Session ID")}
    a += [comment("""Compare the reloaded active session with the captured owner:
- A matching ID means this CLOSE still owns the session.
- A different ID means a newer OPEN owns state; this otherwise branch is intentionally Nothing only.
- The sole CLOSE save action is nested in the matching branch."""), owns_if]
    # Owner branch operates only on Reloaded State, preserving unrelated fields from the fresh dictionary.
    a += math("Now Epoch", variable("Captured Start"), "Session Duration", "-")
    a += read_value("active_session.declared_duration_seconds", variable("Reloaded State"), "Declared Duration")
    a += [comment("""Compare the measured duration with any declared contract:
- A zero or absent declared duration has no contract penalty.
- A genuine overrun is recorded in the session object for the next OPEN.
- The configured penalty is applied by OPEN, preserving its ordered Heat pipeline.""")]
    overrun_g, overrun_if = if_block("Declared Duration", 2, number=0)
    a += [overrun_if] + math("Session Duration", variable("Declared Duration"), "Overrun Seconds", "-") + [otherwise(overrun_g)] + number(0, "Overrun Seconds") + [end_if(overrun_g)]
    record_text = text_token([('{"id":"', "Captured Session ID"), ('","started_at":', "Captured Start"), (',"ended_at":', "Now Epoch"), (',"duration_seconds":', "Session Duration"), (',"overrun_seconds":', "Overrun Seconds"), ('}', None)])
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
          set_value("active_session", text_token([( "null", None)]), "Reloaded State")]
    a += [comment("""--- PHASE 5 RESTORE HOOK ---

- Any settings snapshot restored here must come from the reloaded full State dictionary.
- This phase records the hook but changes no environmental setting yet.
- State is persisted only after the eventual restore work.""")]
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
          set_value("active_session", text_token([("null", None)])),
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
    a = [comment(MANUAL_MARKER + "\n\n- Manual control offers an independent Emergency Restore.\n- It roots every mutation in the full loaded State.\n- The branch saves exactly once before the Control Room is shown."),
         menu(group, 0, prompt="PROSOCHĒ", items=["Open Control Room", "Emergency Restore"]),
         menu(group, 1, title="Open Control Room"), action("is.workflow.actions.nothing"),
         menu(group, 1, title="Emergency Restore")]
    a += restore_managed_settings("State")
    a += [set_value("cooldown_until", text_token([("null", None)])),
          set_value("active_session", text_token([("null", None)]))]
    a += save_state()
    a += [menu(group, 2), comment("--- PHASE 5 MANUAL EMERGENCY RESTORE END ---")]
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


def main():
    global UUID_COUNTER
    UUID_COUNTER = 0
    data = plistlib.loads(SOURCE.read_bytes())  # exactly one parse
    actions = data["WFWorkflowActions"]
    pinned = plistlib.dumps(actions[:5], fmt=plistlib.FMT_XML)
    # Phase 3/4 already expanded their original anchors. Phase 5 owns named
    # markers inside that complete graph, so every rerun replaces whole sections
    # deterministically instead of relying on mutable numeric action offsets.
    replace_marker_block(actions, DISPATCH_MARKER, "--- PHASE 5 PRIMITIVE DISPATCH END", primitive_dispatch())
    replace_marker_block(actions, RESTORE_MARKER, "--- PHASE 5 RESTORE MANAGED SETTINGS END",
                         [comment(RESTORE_MARKER + "\n\n- Only the matching CLOSE owner restores captured settings.\n- A superseded CLOSE reaches no restore or Save File action."),
                          *restore_managed_settings("Reloaded State"),
                          comment("--- PHASE 5 RESTORE MANAGED SETTINGS END ---")])
    install_cooldown_branches(actions)
    insert_or_replace_after(actions, "--- CONTROL ROOM: confirm", MANUAL_MARKER,
                            "--- PHASE 5 MANUAL EMERGENCY RESTORE END ---", manual_emergency_restore())
    normalize_setters(actions)
    # The skill requires a repair-oriented, bulleted Comment immediately before
    # every control-flow start.  Make this invariant structural, not index-based.
    index = 0
    while index < len(actions):
        parameters = actions[index].get("WFWorkflowActionParameters", {})
        starts_flow = (actions[index].get("WFWorkflowActionIdentifier") in
                       {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count"}
                       and parameters.get("WFControlFlowMode") == 0)
        prior_is_comment = index > 0 and actions[index - 1].get("WFWorkflowActionIdentifier") == "is.workflow.actions.comment"
        if starts_flow and not prior_is_comment:
            actions.insert(index, comment("Control-flow check:\n- Use the named value prepared directly above.\n- Keep the true and otherwise paths balanced.\n- Continue with the full State dictionary unchanged unless this branch explicitly updates it."))
            index += 1
        index += 1
    if plistlib.dumps(actions[:5], fmt=plistlib.FMT_XML) != pinned:
        raise SystemExit("pinned actions 0-4 changed")
    SOURCE.write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False))  # exactly one serialization/write


if __name__ == "__main__":
    main()
