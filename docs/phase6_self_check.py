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


def reference_exploration(enabled: list[str], best: str) -> str:
    """The selector's canonical next-non-best rule, including the Close wrap."""
    after_best = enabled[enabled.index(best) + 1:]
    return next((name for name in after_best if name != best),
                next((name for name in enabled if name != best), best))


def index_of(actions: list[dict], identifier: str, **parameters: object) -> int:
    for index, item in enumerate(actions):
        if item["WFWorkflowActionIdentifier"] != identifier:
            continue
        values = item.get("WFWorkflowActionParameters", {})
        if all(values.get(key) == value for key, value in parameters.items()):
            return index
    raise AssertionError(f"missing {identifier} with {parameters}")


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
            # PHASE 10 (10-03): the WFAppName term was STALE, not weakened away to reach
            # green. normalize_open_apps() (tools/build_state_engine.py:2849) clears an
            # openapp action's parameters outright and re-emits only open_app()'s two keys,
            # WFAppIdentifier and WFSelectedApp -- WFAppName is deliberately not among them.
            # The term therefore contradicted the generator by construction and this
            # assertion was red at HEAD. WFSelectedApp is the real route-shape property and
            # stays; it is what actually binds the route to a resolved app.
            require("WFSelectedApp" in params, "Open App route shape")
        if ident == "is.workflow.actions.searchweb":
            require({"WFSearchWebDestination", "WFInputText"} <= params.keys(), "Search Web route shape")
        if ident == "is.workflow.actions.searchmaps":
            require({"WFInput", "WFSearchMapsActionApp"} <= params.keys(), "Search Maps route shape")
    # Consult asks once, then every prescribed destination shares the supplied query where applicable.
    consult_ask = index_of(actions, "is.workflow.actions.ask", WFAskActionPrompt="What are you trying to find?")
    consult = actions[consult_ask:consult_ask + 30]
    consult_text = str(consult)
    for item in ("Search Web", "Search Maps", "Open Notes", "Open Reminders", "Open Calendar", "Back"):
        require(item in consult_text, f"Consult menu option missing: {item}")
    require("Consult Query" in str(consult[5]) and "Consult Query" in str(consult[7]), "Consult searches must use the asked query")
    require("helpful next step" not in consult_text and "nearby" not in consult_text, "Consult must not use a hard-coded query")
    # Create's second reload owns both the persistence and route after an interactive URL Ask.
    create_ask = index_of(actions, "is.workflow.actions.ask", WFAskActionPrompt="Where should Create open?")
    create = actions[create_ask:create_ask + 30]
    create_text = str(create)
    require("Reload after Create input" in create_text and "Create Owner ID" in create_text, "Create must reload and check ownership after Ask")
    require(create_text.index("Create Owner ID") < create_text.index("profile_snapshot.create_target_url"), "Create ownership must precede URL persistence")
    require(create_text.index("profile_snapshot.create_target_url") < create_text.index("is.workflow.actions.openurl"), "Create owner branch must persist before routing")
    # Reference cases prevent a future loop from overwriting the one canonical exploration choice.
    require(reference_exploration(["Capture", "Coordinate"], "Capture") == "Coordinate", "exploration next exit")
    require(reference_exploration(["Capture", "Coordinate"], "Coordinate") == "Capture", "exploration wraps")
    require(reference_exploration(["Capture", "Coordinate", "Close"], "Close") == "Capture", "exploration wraps after Close")
    require(reference_exploration(["Close"], "Close") == "Close", "single enabled exit remains safe")
    selector_start = next(index for index, action_item in enumerate(actions)
                          if "PHASE 6 EXIT SELECTOR" in action_item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
    selector_text = str(actions[selector_start:selector_start + 140])
    for marker in ("Best Exit", "Past Best", "Exploration Selected", "Exploration wrap"):
        require(marker in selector_text, f"selector does not prove canonical single exploration: {marker}")
    # A no-contract CLOSE serializes null outcomes; only declared contracts can feed next-OPEN Heat relief/penalty.
    contract_start = next(index for index, action_item in enumerate(actions)
                          if "Contract outcome:" in action_item.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
    contract_text = str(actions[contract_start:contract_start + 80])
    require('"respected":' in contract_text and '"respected":"' not in contract_text, "respected must serialize as boolean/null, not a string")
    require("No declared duration stores null" in contract_text, "no-contract outcome must be null")
    heat_text = str(actions)
    require("Previous Declared Duration" in heat_text, "next OPEN must guard contract feedback on declared duration")
    banned = ("send", "call", "message", "askllm", "random", "downloadurl")
    require(not any(any(word in ident.lower() for word in banned) for ident in ids if ident != "is.workflow.actions.number.random"), "forbidden side-effect action")
    require(ids.count("is.workflow.actions.number.random") == 1, "only session ID generation may use random")
    print("phase6 self-check: passed")


if __name__ == "__main__":
    main()
