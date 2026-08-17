#!/usr/bin/env python3
"""Small factual guard for the Phase 7 Dumb fork."""
from __future__ import annotations

import hashlib
import importlib.util
import plistlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"
# ORDER-SENSITIVE, and it mirrors manual_emergency_restore()'s `choices` list exactly.  A
# choosefrommenu's mode-1 case titles must equal its WFMenuItems element for element AND in
# the same order (.claude/CLAUDE.md §4: the top documented real-world failure mode), so this
# list and the generator's must be edited in the same commit.
# PHASE 11 (11-05) added the eleventh item, "Panic Escape" -- the deliberate, reversible
# removal-and-restore path for the Leaving bypass.  It is NOT Emergency Restore, which keeps
# its own separate item at position nine and is never gated on the Panic Escape flag.
MENU = ["Status", "Open Control Room", "Sync My Profile", "Change Profile", "Change Sequence", "Toggle Voice", "Test a Circle", "Reset Today", "Emergency Restore", "Setup Check", "Panic Escape"]


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> None:
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "builder is not idempotent")
    actions = plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"]
    params = [item.get("WFWorkflowActionParameters", {}) for item in actions]
    menus = [value["WFMenuItems"] for value in params if value.get("WFMenuItems") == MENU]
    require(len(menus) == 1, "manual menu is not the exact eleven required items, in order")
    # PHASE 10 (10-02) -- the Control Room Note must open only on request.  Before the
    # gate, the single shownote sat at depth 0 in the MANUAL arm, so all nine menu items
    # ended by launching the Notes app.  Pin the gate structurally, not by action index.
    shownote = [index for index, item in enumerate(actions)
                if item["WFWorkflowActionIdentifier"] == "is.workflow.actions.shownote"]
    require(len(shownote) == 1, "expected exactly one Show Note action")
    gate = actions[shownote[0] - 1]
    gate_params = gate.get("WFWorkflowActionParameters", {})
    require(gate["WFWorkflowActionIdentifier"] == "is.workflow.actions.conditional"
            and gate_params.get("WFControlFlowMode") == 0
            and gate_params.get("WFCondition") == 2
            and gate_params.get("WFInput", {}).get("Variable", {}).get("Value", {}).get("VariableName")
            == "Manual Show Note Requested",
            "Show Note is not gated on a 'Manual Show Note Requested > 0' conditional")
    # PHASE 10 (10-02) -- Setup Check reads two FLAT epoch keys and nothing else.
    # Some dictionary keys are text tokens (dicts), not literals; only literals matter here.
    setup_keys = {value["WFDictionaryKey"] for value in params
                  if isinstance(value.get("WFDictionaryKey"), str)}
    require({"last_open_at", "last_close_at"} <= setup_keys, "Setup Check state reads missing")
    require(any(value.get("WFVariableName") == "Manual Setup Check Requested" for value in params),
            "Setup Check request flag missing")
    comments = "\n".join(value.get("WFCommentActionText", "") for value in params)
    require("PHASE 7 MANUAL CONTROL ROOM REFRESH" in comments, "manual Note refresh missing")
    require("Test Circle uses a copied Circle value" in comments, "Test Circle safety statement missing")
    spec = importlib.util.spec_from_file_location("phase7_builder", BUILDER)
    builder = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(builder)
    require(len({*builder.MIRROR_BASELINES, *builder.MIRROR_SUCCESSES, *builder.MIRROR_LAPSES}) >= 30, "fewer than 30 mirror templates")
    ids = [item["WFWorkflowActionIdentifier"] for item in actions]
    require("is.workflow.actions.askllm" not in ids and "Apple Intelligence" not in SOURCE.read_text(), "Dumb fork has model dependency")
    require("profile_snapshot.proforma" in str(actions), "manual proforma sync missing")
    print("phase7 self-check: passed")


if __name__ == "__main__":
    main()
