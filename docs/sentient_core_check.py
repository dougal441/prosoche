#!/usr/bin/env python3
"""Structural proof that Sentient is an additive fork of Dumb."""
import plistlib
from pathlib import Path

DUMB = plistlib.loads(Path("src/PROSOCHE-Dumb.xml").read_bytes())
SENTIENT = plistlib.loads(Path("src/PROSOCHE-Sentient.xml").read_bytes())
da, sa = DUMB["WFWorkflowActions"], SENTIENT["WFWorkflowActions"]
assert SENTIENT["WFWorkflowName"].endswith("Sentient")
models = [a for a in sa if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.askllm"]
assert len(models) == 1
p = models[0]["WFWorkflowActionParameters"]
assert p["WFLLMModel"] == "Apple Intelligence on Device" and p["WFGenerativeResultType"] == "Text"
assert "WFAllowWebSearch" not in p and "FollowUp" not in p
marker = next(i for i, a in enumerate(sa) if "--- SENTIENT CONTRACT AUDIT ---" in a.get("WFWorkflowActionParameters", {}).get("WFCommentActionText", ""))
assert "Circle I" not in str(sa[:marker]) and "Circle IX" not in str(sa[marker:marker + 1])
assert all(a["WFWorkflowActionIdentifier"] != "is.workflow.actions.askllm" for a in da)
print("sentient core check: unchanged Dumb core and one bounded model gate")
