#!/usr/bin/env python3
"""Small structural guard for Phase 5's non-trivial Shortcuts graph."""
from __future__ import annotations

import hashlib
import plistlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"


def digest() -> str:
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def marker_index(actions, marker: str) -> int:
    matches = [index for index, item in enumerate(actions)
               if item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "").startswith(f"--- {marker} ---")]
    require(len(matches) == 1, f"expected one {marker} marker")
    return matches[0]


def conditional_ancestry(actions, until: int) -> list[tuple[str, int]]:
    """Return each enclosing conditional and the arm containing action ``until``."""
    stack: list[list[object]] = []
    for item in actions[:until]:
        if item["WFWorkflowActionIdentifier"] != "is.workflow.actions.conditional":
            continue
        params = item["WFWorkflowActionParameters"]
        mode, group = params.get("WFControlFlowMode"), params.get("GroupingIdentifier")
        if mode == 0:
            stack.append([group, 0])
        elif mode == 1:
            require(stack and stack[-1][0] == group, "otherwise without matching conditional")
            stack[-1][1] = 1
        elif mode == 2:
            require(stack and stack[-1][0] == group, "end conditional without matching start")
            stack.pop()
    return [(group, arm) for group, arm in stack]


def main() -> None:
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = digest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == digest(), "builder output is not idempotent")

    workflow = plistlib.loads(SOURCE.read_bytes())
    actions = workflow["WFWorkflowActions"]
    text = SOURCE.read_text()
    ids = [item["WFWorkflowActionIdentifier"] for item in actions]
    comments = "\n".join(item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for item in actions)

    require(ids[:5] == ["is.workflow.actions.comment", "is.workflow.actions.comment", "is.workflow.actions.gettext",
                         "is.workflow.actions.setvariable", "is.workflow.actions.gettext"], "pinned imports changed")
    for name in ("Knock", "Ash", "Silence", "Confession", "Dimming", "Exile", "Mirror", "Voice", "Ice",
                 "Ash+Confession", "Silence+Mirror", "Classic", "BlackMirror", "Ambient"):
        require(name in text, f"missing sequence or primitive: {name}")
    for marker in ("PHASE 5 PRIMITIVE DISPATCH", "PHASE 5 LIVE ICE REDIRECT", "PHASE 5 ICE EXPIRY",
                   "PHASE 5 RESTORE MANAGED SETTINGS", "PHASE 5 MANUAL EMERGENCY RESTORE"):
        require(marker in comments, f"missing semantic marker: {marker}")
    for key in ("settings_snapshot.brightness.original_value", "settings_snapshot.volume.original_value",
                "changed_at", "changed_by_session_id", "cooldown_until"):
        require(key in text, f"missing state safety key: {key}")
    require("AXToggleColorFiltersIntent" not in text and "UAToggleColorFiltersIntent" not in text,
            "unsupported Color Filters action was emitted")
    for item in actions:
        params = item.get("WFWorkflowActionParameters", {})
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.setvolume":
            require(params.get("WFVolumeSetting") == "Media", "non-Media volume write")
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.setbrightness":
            require(params.get("WFBrightness") not in (0, "0", 0.0), "brightness may reach zero")

    cooldown_index, cooldown = next(
        ((index, item) for index, item in enumerate(actions)
         if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
         and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 0
         and item["WFWorkflowActionParameters"].get("WFInput", {}).get("Variable", {}).get("Value", {})
         .get("VariableName") == "Cooldown Until"),
        (None, None),
    )
    require(cooldown is not None, "named cooldown conditional missing")
    cooldown_group = cooldown["WFWorkflowActionParameters"]["GroupingIdentifier"]
    input_present_group = next(
        item["WFWorkflowActionParameters"]["GroupingIdentifier"] for item in actions
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
        and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 0
        and item["WFWorkflowActionParameters"].get("WFCondition") == 100
        and item["WFWorkflowActionParameters"].get("WFInput", {}).get("Variable", {}).get("Value", {})
        .get("VariableName") == "Input Key")
    open_group = next(
        item["WFWorkflowActionParameters"]["GroupingIdentifier"] for item in actions
        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
        and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 0
        and item["WFWorkflowActionParameters"].get("WFCondition") == 4
        and item["WFWorkflowActionParameters"].get("WFConditionalActionString") == "OPEN"
        and item["WFWorkflowActionParameters"].get("WFInput", {}).get("Variable", {}).get("Value", {})
        .get("VariableName") == "Input Key")
    otherwise_index = next(index for index, item in enumerate(actions[cooldown_index + 1:], cooldown_index + 1)
                           if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                           and item["WFWorkflowActionParameters"].get("GroupingIdentifier") == cooldown_group
                           and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 1)
    cooldown_end = next(index for index, item in enumerate(actions[otherwise_index + 1:], otherwise_index + 1)
                        if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
                        and item["WFWorkflowActionParameters"].get("GroupingIdentifier") == cooldown_group
                        and item["WFWorkflowActionParameters"].get("WFControlFlowMode") == 2)
    live_index = marker_index(actions, "PHASE 5 LIVE ICE REDIRECT")
    expiry_index = marker_index(actions, "PHASE 5 ICE EXPIRY")
    require(conditional_ancestry(actions, live_index) == [(input_present_group, 0), (open_group, 0), (cooldown_group, 0)],
            "live-Ice marker is not exactly in the live-cooldown branch")
    require(conditional_ancestry(actions, expiry_index) == [(input_present_group, 0), (open_group, 0), (cooldown_group, 1)],
            "expiry marker is not exactly in the expired-cooldown branch")
    live_actions = actions[cooldown_index + 1:otherwise_index]
    require(any(item["WFWorkflowActionIdentifier"] == "is.workflow.actions.returntohomescreen" for item in live_actions),
            "live-cooldown branch has no redirect")
    live_keys = "\n".join(str(item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey", "")) for item in live_actions)
    require("heat" not in live_keys and "opens_today" not in live_keys,
            "live-cooldown branch inflates Heat or open count")
    expiry_actions = actions[otherwise_index + 1:cooldown_end]
    expiry_keys = "\n".join(str(item.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey", "")) for item in expiry_actions)
    require("cooldown_until" in expiry_keys and "heat" in expiry_keys,
            "expired-cooldown branch does not clear cooldown and apply relief")

    stack: list[str] = []
    flow_ids = {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count",
                "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}
    for item in actions:
        if item["WFWorkflowActionIdentifier"] not in flow_ids:
            continue
        params = item["WFWorkflowActionParameters"]
        mode, group = params.get("WFControlFlowMode"), params.get("GroupingIdentifier")
        if mode == 0:
            stack.append(group)
        elif mode == 2:
            require(stack and stack[-1] == group, "unbalanced control flow")
            stack.pop()
    require(not stack, "unclosed control flow")
    require("superseded CLOSE reaches no restore" in comments, "superseded CLOSE restore guard missing")
    print("phase5 self-check: passed")


if __name__ == "__main__":
    main()
