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
