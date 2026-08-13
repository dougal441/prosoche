#!/usr/bin/env python3
"""Structural regression check for Phase 6's deterministic exit graph."""
from __future__ import annotations

import hashlib
import plistlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/PROSOCHE-Dumb.xml"
BUILDER = ROOT / "tools/build_state_engine.py"


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def digest() -> str:
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def main() -> None:
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    first = digest()
    subprocess.run(["python3", str(BUILDER)], cwd=ROOT, check=True)
    require(first == digest(), "builder output is not idempotent")
    actions = plistlib.loads(SOURCE.read_bytes())["WFWorkflowActions"]
    comments = "\n".join(x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", "") for x in actions)
    ids = [x["WFWorkflowActionIdentifier"] for x in actions]
    keys = "\n".join(str(x.get("WFWorkflowActionParameters", {}).get("WFDictionaryKey", "")) for x in actions)
    require("PHASE 6 UNIVERSAL LEAVING" in comments, "universal Leaving wrapper missing")
    require("PHASE 6 EXIT SELECTOR" in comments and "PHASE 6 PENDING EXIT OUTCOME" in comments, "selection/outcome graph missing")
    require(comments.index("PHASE 6 UNIVERSAL LEAVING") < comments.index("PHASE 5 PRIMITIVE DISPATCH"), "Leaving must precede primitive dispatch")
    for name in ("Capture", "Coordinate", "Create", "Connect", "Consult", "Close"):
        require(name in comments or name in str(actions), f"exit missing: {name}")
    for key in ("profile_snapshot.enabled_exits", "exit_selection_counter", "pending_exit", "exit_stats.",
                "active_session.id", "active_session.intention", "active_session.declared_duration_seconds"):
        require(key in keys, f"state key missing: {key}")
    allowed = {
        "is.workflow.actions.openapp", "is.workflow.actions.searchweb", "is.workflow.actions.searchmaps",
        "is.workflow.actions.openurl", "is.workflow.actions.returntohomescreen",
    }
    routes = [x for x in actions if x["WFWorkflowActionIdentifier"] in allowed]
    require(routes, "no exit route actions")
    for item in routes:
        ident, params = item["WFWorkflowActionIdentifier"], item["WFWorkflowActionParameters"]
        if ident == "is.workflow.actions.openapp":
            require("WFSelectedApp" in params and "WFAppName" in params, "Open App route shape")
        if ident == "is.workflow.actions.searchweb":
            require({"WFSearchWebDestination", "WFInputText"} <= params.keys(), "Search Web route shape")
        if ident == "is.workflow.actions.searchmaps":
            require({"WFInput", "WFSearchMapsActionApp"} <= params.keys(), "Search Maps route shape")
    banned = ("send", "call", "message", "askllm", "random", "downloadurl")
    require(not any(any(word in ident.lower() for word in banned) for ident in ids if ident != "is.workflow.actions.number.random"), "forbidden side-effect action")
    require(ids.count("is.workflow.actions.number.random") == 1, "only session ID generation may use random")
    print("phase6 self-check: passed")


if __name__ == "__main__":
    main()
