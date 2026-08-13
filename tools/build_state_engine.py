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
OPEN_ANCHOR = "OPEN branch anchor."
CLOSE_ANCHOR = "CLOSE branch anchor."


def uid() -> str:
    return str(uuid.uuid4()).upper()


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


def replace_anchor(actions, prefix: str, replacement):
    for index, candidate in enumerate(actions[:-1]):
        parameters = candidate.get("WFWorkflowActionParameters", {})
        if candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.comment" and parameters.get("WFCommentActionText", "").startswith(prefix):
            following = actions[index + 1]
            if following.get("WFWorkflowActionIdentifier") != "is.workflow.actions.nothing":
                raise SystemExit(f"{prefix} is not followed by its Nothing anchor")
            actions[index:index + 2] = replacement
            return
    raise SystemExit(f"semantic anchor not found: {prefix}")


def main():
    data = plistlib.loads(SOURCE.read_bytes())  # exactly one parse
    actions = data["WFWorkflowActions"]
    pinned = plistlib.dumps(actions[:5], fmt=plistlib.FMT_XML)
    replace_anchor(actions, OPEN_ANCHOR, open_pipeline())
    replace_anchor(actions, CLOSE_ANCHOR, close_pipeline())
    # Set Dictionary Value returns a new whole dictionary.  Rebind that output
    # immediately so each later setter starts from the full, latest State, not a
    # stale action index or a partial dictionary.
    index = 0
    while index < len(actions):
        candidate = actions[index]
        parameters = candidate.get("WFWorkflowActionParameters", {})
        source = parameters.get("WFDictionary", {}).get("Value", {})
        target = source.get("VariableName")
        if candidate.get("WFWorkflowActionIdentifier") == "is.workflow.actions.setvalueforkey" and target:
            actions.insert(index + 1, set_var(target, output(parameters["UUID"], "Dictionary")))
            index += 1
        index += 1
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
