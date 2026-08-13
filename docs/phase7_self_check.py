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
MENU = ["Status", "Open Control Room", "Sync My Profile", "Change Profile", "Change Sequence", "Toggle Voice", "Test a Circle", "Reset Today", "Emergency Restore"]


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
    require(len(menus) == 1, "manual menu is not the exact nine required items")
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
