#!/usr/bin/env python3
"""Focused evidence for the bounded Sentient audit protocol."""
import plistlib
from pathlib import Path

a = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())["WFWorkflowActions"]
start = next(i for i, x in enumerate(a) if "--- SENTIENT CONTRACT AUDIT ---" in x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
end = next(i for i, x in enumerate(a[start + 1:], start + 1) if "--- SENTIENT CONTRACT AUDIT END ---" in x.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
block = a[start:end + 1]
raw = str(block)
assert raw.count("is.workflow.actions.askllm") == 1
for phrase in ("ALLOW", "CHALLENGE", "DENY", "deliberate leisure", "lying", "diagnosis", "feelings", "app contents", "Intention", "Boundary minutes", "Circle", "Heat", "Open count"):
    assert phrase in raw, phrase
assert "WFAllowWebSearch" not in raw and "FollowUp" not in raw
assert "gettimebetweendates" in raw and "Audit Seconds" in raw and "WFNumberValue': 8" in raw
assert raw.count("Revise or continue") == 1 and "Circle Next" in raw and "returntohomescreen" in raw
for forbidden in ("setbrightness", "setvolume", "setvalueforkey", "number.random", "WFDelayTime"):
    assert forbidden not in raw, forbidden
print("sentient audit check: compact prompt, one challenge, bounded fallback")
