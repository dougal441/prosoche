#!/usr/bin/env python3
"""Build the Sentient shortcut as an additive, repeatable Dumb fork."""
from __future__ import annotations

import hashlib
import os
import plistlib
import tempfile
import uuid
from pathlib import Path

SOURCE = Path("src/PROSOCHE-Dumb.xml")
TARGET = Path("src/PROSOCHE-Sentient.xml")
MODEL = "Apple Intelligence on Device"  # direct device-export evidence
MARKER = "--- SENTIENT CONTRACT AUDIT ---"


def uid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"prosoche/sentient/{name}")).upper()


def action(identifier: str, **parameters):
    return {"WFWorkflowActionIdentifier": identifier, "WFWorkflowActionParameters": parameters}


def output(id_: str, name: str):
    return {"Value": {"OutputUUID": id_, "OutputName": name, "Type": "ActionOutput"},
            "WFSerializationType": "WFTextTokenAttachment"}


def variable(name: str):
    return {"Value": {"Type": "Variable", "VariableName": name},
            "WFSerializationType": "WFTextTokenAttachment"}


def token(name: str):
    return {"Value": {"string": "\ufffc", "attachmentsByRange": {"{0, 1}": {"Type": "Variable", "VariableName": name}}},
            "WFSerializationType": "WFTextTokenString"}


def text(parts: list[tuple[str, str | None]]):
    string, ranges, offset = "", {}, 0
    for literal, name in parts:
        string += literal
        offset += len(literal)
        if name:
            ranges[f"{{{offset}, 1}}"] = {"Type": "Variable", "VariableName": name}
            string += "\ufffc"
            offset += 1
    return {"Value": {"string": string, "attachmentsByRange": ranges}, "WFSerializationType": "WFTextTokenString"}


def comment(value: str):
    return action("is.workflow.actions.comment", WFCommentActionText=value)


def set_var(name: str, value):
    return action("is.workflow.actions.setvariable", WFInput=value, WFVariableName=name)


def if_block(name: str, condition: int, *, number=None, string=None, key="if"):
    group = uid(key)
    params = {"GroupingIdentifier": group, "WFControlFlowMode": 0, "WFCondition": condition,
              "WFInput": {"Type": "Variable", "Variable": variable(name)}}
    if number is not None:
        params["WFNumberValue"] = number
    if string is not None:
        params["WFConditionalActionString"] = string
    return group, action("is.workflow.actions.conditional", **params)


def otherwise(group: str):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=1)


def end(group: str):
    return action("is.workflow.actions.conditional", GroupingIdentifier=group, WFControlFlowMode=2)


def audit_block():
    """One optional advisory call. Every non-ALLOW branch continues Dumb."""
    before, model, after, elapsed, matches, count, first, revision = (uid(x) for x in (
        "before", "model", "after", "elapsed", "matches", "count", "first", "revision"))
    enabled_g, enabled = if_block("Import AI", 4, string="yes", key="enabled")
    min_g, minimum = if_block("Circle Next", 3, number=2, key="circle-min")
    max_g, maximum = if_block("Circle Next", 0, number=9, key="circle-max")
    fast_g, fast = if_block("Audit Seconds", 1, number=8, key="fast")
    found_g, found = if_block("Audit Match Count", 2, number=0, key="found")
    challenge_g, challenge = if_block("Audit Token", 99, string="CHALLENGE", key="challenge")
    deny_g, deny = if_block("Audit Token", 99, string="DENY", key="deny")
    high_g, high = if_block("Circle Next", 3, number=7, key="deny-high")
    return [
        comment(MARKER + "\n\n- Audit only a voluntary contract after Confession and before its existing Dumb save.\n- The model receives compact recorded facts, never the Note or app contents.\n- Empty, malformed, unavailable, or slow output continues the unchanged Dumb path; platform hangs cannot be cancelled at target 26."),
        comment("AI preference gate:\n- A no response keeps this run entirely Dumb.\n- Only an explicit yes reaches the optional audit."), enabled,
        comment("Circle gate:\n- Circle I remains deterministic.\n- Only Circle II and above may reach the audit."), minimum,
        comment("Circle ceiling:\n- Circle IX remains deterministic Ice.\n- Only Circles II through VIII may reach the audit."), maximum,
        action("is.workflow.actions.date", UUID=before, WFDateActionMode="Current Date"),
        set_var("Audit Before", output(before, "Date")),
        action("is.workflow.actions.askllm", UUID=model,
               WFLLMModel=MODEL, WFGenerativeResultType="Text",
               WFLLMPrompt=text([(
                   "You are a bounded contract auditor. Return exactly one first token: ALLOW, CHALLENGE, or DENY. ", None),
                   ("ALLOW a clearly bounded deliberate leisure choice. Audit only specificity, boundedness, and guarded recorded consistency. ", None),
                   ("Never claim lying, diagnosis, addiction, morality, feelings, or knowledge of app contents. Do not prescribe settings, arithmetic, timers, exits, or Ice.\n", None),
                   ("Intention: ", "Confession Intention"), ("\nBoundary minutes: ", "Declared Boundary Minutes"),
                   ("\nCircle: ", "Circle Next"), ("\nHeat: ", "Heat Final"), ("\nOpen count: ", "Opens Today Next"),
               ])),
        action("is.workflow.actions.date", UUID=after, WFDateActionMode="Current Date"),
        set_var("Audit After", output(after, "Date")),
        action("is.workflow.actions.gettimebetweendates", UUID=elapsed, WFInput=text([("", None), ("", "Audit After")]),
               WFTimeUntilFromDate=text([("", None), ("", "Audit Before")]), WFTimeUntilUnit="Seconds"),
        set_var("Audit Seconds", output(elapsed, "Time Between Dates")),
        comment("Completed latency gate:\n- Use the dates immediately around Use Model.\n- A result over eight seconds takes the Dumb path."), fast,
        action("is.workflow.actions.text.match", UUID=matches, text=output(model, "Model Result"),
               WFMatchTextPattern=r"(?i)^\\s*(ALLOW|CHALLENGE|DENY)\\b"),
        action("is.workflow.actions.count", UUID=count, WFInput=output(matches, "Matches"), Input=output(matches, "Matches")),
        set_var("Audit Match Count", output(count, "Count")),
        comment("Parsed-token gate:\n- Only a matched first token is considered.\n- Empty or malformed output takes the Dumb path."), found,
        action("is.workflow.actions.getitemfromlist", UUID=first, WFItemSpecifier="First Item", WFInput=output(matches, "Matches")),
        set_var("Audit Token", output(first, "Item from List")),
        comment("Challenge branch:\n- CHALLENGE may ask once for revision or continuation.\n- The revision does not create another model call."), challenge,
        comment("One optional revision only:\n- The user may revise or continue the contract once.\n- This response is never sent to the model again."),
        action("is.workflow.actions.ask", UUID=revision, WFAskActionPrompt="Revise or continue your boundary? (optional)", WFInputType="Text"),
        set_var("Confession Intention", output(revision, "Provided Input")), otherwise(challenge_g),
        comment("Deny branch:\n- Only a DENY token may redirect.\n- Lower circles continue Dumb without punishment."), deny,
        comment("High-circle gate:\n- DENY redirects only at Circle VII or VIII.\n- It cannot alter deterministic state."), high,
        comment("High-circle DENY redirects without punishment:\n- Use the already offered Leaving route or return home.\n- No settings, arithmetic, timer, Ice, or exit selection changes here."),
        action("is.workflow.actions.returntohomescreen"), otherwise(high_g), action("is.workflow.actions.nothing"), end(high_g),
        otherwise(deny_g), action("is.workflow.actions.nothing"), end(deny_g),
        end(challenge_g), end(found_g), otherwise(fast_g), action("is.workflow.actions.nothing"), end(fast_g),
        end(max_g), end(min_g), end(enabled_g),
        comment("--- SENTIENT CONTRACT AUDIT END ---"),
    ]


def main() -> None:
    original = SOURCE.read_bytes()
    root = plistlib.loads(original)
    actions = root["WFWorkflowActions"]
    if any(MARKER in a.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for a in actions):
        raise SystemExit("source is already a Sentient fork")
    # Add the third import preference after the two frozen import literals.
    import_id = uid("import-ai")
    actions[6:6] = [action("is.workflow.actions.gettext", UUID=import_id, WFTextActionText="yes"),
                    set_var("Import AI", output(import_id, "Text"))]
    root["WFWorkflowImportQuestions"].append({"ActionIndex": 6, "Category": "Parameter", "DefaultValue": "yes",
                                               "ParameterKey": "WFTextActionText",
                                               "Text": "Use Apple's on-device intelligence contract audit when available? Answer yes or no."})
    root["WFWorkflowName"] = "PROSOCHĒ — Nine Circles — Sentient"
    root["WFWorkflowIcon"] = {"WFWorkflowIconGlyphNumber": 59856, "WFWorkflowIconStartColor": 431817727}
    for index, item in enumerate(actions):
        value = item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "")
        if value.startswith("Reload before writing a contract."):
            actions[index:index] = audit_block()
            break
    else:
        raise SystemExit("semantic Confession contract marker not found")
    payload = plistlib.dumps(root, fmt=plistlib.FMT_XML, sort_keys=False)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=TARGET.parent, delete=False) as tmp:
        tmp.write(payload)
        temporary = Path(tmp.name)
    os.replace(temporary, TARGET)
    if SOURCE.read_bytes() != original:
        raise SystemExit("frozen Dumb source changed")
    print(f"built {TARGET} ({hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
