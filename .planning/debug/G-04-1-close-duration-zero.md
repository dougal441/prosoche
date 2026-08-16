---
status: diagnosed
trigger: "G-04-1-close-duration-zero: After a normal OPEN -> wait -> CLOSE cycle on a real iPhone, state.json's recent_sessions gets a new entry with a valid session ID, but its duration_seconds field records as 0 instead of the plausible elapsed time between OPEN and CLOSE."
created: 2026-08-16T09:03:21Z
updated: 2026-08-16T09:03:21Z
---

## Current Focus

hypothesis: CONFIRMED - close_pipeline()'s session-ownership conditional (the "does the
  reloaded active_session.id still match the ID this CLOSE captured" gate that wraps the
  ENTIRE Session Duration computation + record append + save) has its WFConditionalActionString
  left as a bare, unwired U+FFFC placeholder character instead of being bound to the
  "Captured Session ID" variable via token(). This is a demonstrably incomplete two-step
  wiring pattern: 3 sibling call sites in the same file implement the identical
  "compare reloaded/current session id to captured session id" check and correctly finish
  with token("Session ID"); this one site (tools/build_state_engine.py:1163-1164,
  emitted into src/PROSOCHE-Dumb.xml:26441-26472) stops after the bare "￼" assignment
  and never adds the finishing token("Captured Session ID") line.
test: N/A - goal is find_root_cause_only, no fix applied. Root cause established via direct
  code inspection (python generator + the actual shipped/tested XML), cross-referenced
  against 3 correctly-wired sibling implementations of the identical pattern in the same file.
expecting: N/A
next_action: N/A - returning ROOT CAUSE FOUND to caller.

## Symptoms

expected: state.json's recent_sessions gets a new entry with a plausible session duration (non-zero, matching elapsed wall-clock time) after open -> wait -> close.
actual: A session entry is written with a valid session ID, but duration_seconds is 0.
errors: None reported (no error dialog) - this is a silent wrong-value defect, not a crash.
reproduction: Open a tracked app, wait some time, close it (device UAT Test 1 in .planning/phases/04-close-pipeline-session-race/04-UAT.md). Then inspect state.json's recent_sessions entry.
started: Discovered during UAT of Phase 04 (close-pipeline-session-race), 2026-08-16.

## Eliminated

- hypothesis: The CLOSE duration math still uses gettimebetweendates.WFTimeUntilFromDate with
    a raw epoch string fed into a Date-typed parameter (the hint's suggested candidate,
    matching the project's documented cycle-14 defect class).
  evidence: elapsed_since()'s docstring and close_pipeline() (tools/build_state_engine.py:1170)
    show CYCLE 14 already replaced this with plain numeric math("Now Epoch", variable("Captured
    Start"), "Session Duration", "-"). The shipped XML (src/PROSOCHE-Dumb.xml:26473-26516)
    confirms a plain is.workflow.actions.math action, not gettimebetweendates, and confirms
    the "Captured Start" operand correctly carries a WFCoercionVariableAggrandizement/
    WFNumberContentItem aggrandizement per rule 6.
  timestamp: 2026-08-16T09:15:00Z

- hypothesis: CLOSE reads the wrong/unset started_at field for the active session (e.g. an
    uninitialized or stale field instead of the just-written one).
  evidence: OPEN (open_pipeline(), tools/build_state_engine.py:1096) writes
    active_session = {"id":<Session ID>,"started_at":<Now Epoch>,"declared_duration_seconds":0}
    as a single JSON object with both id and started_at as sibling NUMBER/STRING fields.
    CLOSE's read (close_pipeline(), line 1151) uses the identical dotted key
    "active_session.started_at" against the same "State" dictionary loaded at this run's
    bootstrap. The read/write field names and shapes match; no mismatch found.
  timestamp: 2026-08-16T09:15:00Z

- hypothesis: The CLOCK block ("Now Epoch") is stale/cached and doesn't reflect genuine
    per-run wall-clock time, so CLOSE's "now" collapses toward OPEN's "now".
  evidence: src/PROSOCHE-Dumb.xml:226-369 shows the CLOCK block (Date "Specified Date"
    1970-01-01 -> "Epoch Anchor"; Date "Current Date" -> "Now Date"; Get Time Between Dates
    Now Date vs Epoch Anchor, unit Seconds -> "Now Epoch") runs fresh at the top of every
    single workflow invocation (OPEN and CLOSE are separate Personal-Automation-triggered
    runs of the same master shortcut, each executing this block anew). No caching/sharing
    mechanism across runs exists. Ruled out as a contributing factor.
  timestamp: 2026-08-16T09:15:00Z

## Evidence

- timestamp: 2026-08-16T09:10:00Z
  checked: tools/build_state_engine.py close_pipeline() (lines 1141-1218), the CLOSE handler
    generator function.
  found: The full sequence is: read active_session existence (has_g) -> capture
    "Captured Session ID"/"Captured Start" from the run's initial "State" -> delay 0.5s ->
    reload state.json fresh into "Reloaded State" -> read "Reloaded Active Session" existence
    (reload_g) -> read "Reloaded Session ID" -> compare "Reloaded Session ID" against the
    captured owner via an if_block (owns_g/owns_if, WFCondition=4 "Text is") -> ONLY inside
    that owns_if TRUE branch does Session Duration get computed
    (math("Now Epoch","Captured Start","Session Duration","-")) and the record built/appended/
    saved. The owns_if's WFConditionalActionString is built via
    if_block("Reloaded Session ID", 4, string="captured-session-placeholder") and then
    immediately overwritten: owns_if["WFWorkflowActionParameters"]["WFConditionalActionString"]
    = "￼" -- and nothing else follows.
  implication: duration_seconds is written in exactly one place in the entire codebase (this
    branch). Whatever gates entry to this branch gates 100% of duration_seconds values ever
    recorded.

- timestamp: 2026-08-16T09:11:00Z
  checked: The 3 other call sites in the same file implementing the identical "compare
    current/reloaded session id against the captured owner id" pattern: persist_contract()
    (lines 554-567, "Contract Owner ID"), create_owner check (lines 840-843, "Create Owner
    ID"), exit-owner check (lines 868-872, "Exit Owner ID").
  found: All 3 sibling sites use the SAME two-line idiom
    (if_block(..., 4, string="captured-session-placeholder") then
    X["WFWorkflowActionParameters"]["WFConditionalActionString"] = ...) but ALL THREE finish
    with a THIRD line assigning the real wiring: token("Session ID") -- e.g. line 562:
    owns["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Session ID").
    token() (line 140) produces the proper WFTextTokenString envelope:
    {"Value": {"string": "￼", "attachmentsByRange": {"{0, 1}": {"Type": "Variable",
    "VariableName": name}}}, "WFSerializationType": "WFTextTokenString"} -- i.e. a real
    variable reference. close_pipeline()'s owns_if (line 1163-1164) is missing this exact
    third line; it stops after assigning the bare, un-enveloped "￼" character.
  implication: This is a structural, provable omission relative to the file's own established
    correct pattern for the identical semantic operation -- not a matter of interpretation.

- timestamp: 2026-08-16T09:13:00Z
  checked: The actual shipped/tested plist, src/PROSOCHE-Dumb.xml, at the owns_if conditional
    (grep for GroupingIdentifier 7E794375-83F2-5670-B40F-86CBCB03CC5F; lines 26441-26472 for
    the If-open, lines 28448-28475 for Otherwise/EndIf). Cross-checked git status/diff: no
    uncommitted changes to this file or the generator -- current HEAD is what was signed and
    device-tested per 04-01-SUMMARY.md.
  found: WFConditionalActionString is serialized as a bare <string>￼</string> (single
    character, NO "Value"/"attachmentsByRange"/"WFSerializationType" wrapper) -- structurally
    different from every other WFTextTokenString-requiring field in this same file (compare
    lines 26383-26403 and 26570-26591 in the identical region, both properly wrapped with
    attachmentsByRange pointing at a real ActionOutput/Variable). Confirmed via direct
    GroupingIdentifier trace that the ENTIRE Session Duration math + contract check + record
    build + recent_sessions append/window + last_close_at + active_session clear + Save File
    sequence (lines 26473-28447) sits strictly inside this conditional's TRUE branch only.
  implication: The one and only site that ever computes/writes duration_seconds is gated by a
    conditional whose comparison target cannot resolve to the real "Captured Session ID"
    variable. Per this project's own documented rule (Generator authoring rules #2: "a bare
    [improperly-enveloped placeholder] resolves to empty at runtime") this field almost
    certainly resolves to blank/unresolved content rather than the intended dynamic value,
    making the ownership comparison unreliable for its intended purpose regardless of the
    exact pass/fail runtime resolution (which cannot be confirmed further without on-device
    XML export -- flagged as the residual uncertainty, recorded per this project's own
    evidence-hierarchy convention of "record it as a deviation" when direct device evidence
    is unavailable).

- timestamp: 2026-08-16T09:14:00Z
  checked: verify_conditional_inputs() (tools/build_state_engine.py:1721-1768), the build's
    own Craig-Loop self-check for conditional wiring correctness, and REQUIRED_PICKER_PARAMS
    validation (line ~1700).
  found: verify_conditional_inputs() only validates the WFInput slot of a conditional (the
    left/compared-variable side) for the "text-template-in-a-variable-slot" defect axis. It
    does NOT validate WFConditionalActionString (the right/comparison-target side) at all --
    no check exists anywhere in this file for "does WFConditionalActionString hold a properly
    enveloped token() when the comparison is meant to be variable-backed".
  implication: This is a validator blind spot, explaining why the defect passed
    validate_shortcut.py, the Python structural self-check (docs/state_engine_self_check.py
    per 04-01-SUMMARY.md), signing, and import without any warning -- fully consistent with
    the reported symptom class ("silent wrong-value defect, not a crash, no error dialog").

- timestamp: 2026-08-16T09:16:00Z
  checked: Grepped the whole generator file for the same
    if_block(..., string="<marker>") immediately followed by
    X["WFWorkflowActionParameters"]["WFConditionalActionString"] = "￼" idiom, to check
    whether close_pipeline's instance is isolated or systemic.
  found: The identical unfinished two-line idiom (bare "￼" with no following token()
    line) also appears at: enabled_exits() line 720-721 ("Enabled Exit Candidate" vs what
    should be "Canonical Exit"), select_exit() line 733-735 ("Exit Selection Counter" is-not
    check), line 774-776 ("Candidate Exit" vs what should be "Best Exit"), line 779-781
    ("unchosen" -- notably here it REPLACES an already-correct literal string="0" comparison
    with the broken "￼", i.e. actively regresses a working comparison), line 788-791
    (two more instances in the "exploration wrap" block), and open_pipeline() line 991-993
    ("Stored Day" is-not check) and line 999-1000 ("Stored Day" vs what should be
    "Behavioural Day", the same-day rollover comparison). Only the 3 sites listed in the
    prior evidence entry correctly finish the pattern with a real token(varname) line.
  implication: This is a systemic, not case-specific, authoring defect class -- an apparent
    9th/10th instance of the "incomplete two-step WFConditionalActionString wiring" pattern
    this project's CLAUDE.md documents as its established failure mode ("Fix whole classes,
    never site-by-site... every defect found this session was systematic"). The CLOSE
    ownership check (root cause of G-04-1) is one instance of this broader, previously
    undocumented defect axis. Recorded here for the fix owner; not in scope to fix under this
    read-only, find_root_cause_only investigation.

## Resolution

root_cause: close_pipeline()'s session-ownership conditional (tools/build_state_engine.py:1163-1164,
  emitted into src/PROSOCHE-Dumb.xml action at GroupingIdentifier 7E794375-83F2-5670-B40F-86CBCB03CC5F)
  has its WFConditionalActionString parameter left as a bare, un-enveloped U+FFFC placeholder
  character instead of being wired to the "Captured Session ID" variable via token(). This
  conditional is the sole gate for the only code path in the entire artifact that computes
  Session Duration and appends a record to recent_sessions (owns_if TRUE branch, lines
  26473-28447 of src/PROSOCHE-Dumb.xml). Because the comparator cannot resolve to the real
  captured session ID, the "does this CLOSE still own the session" check does not do what it
  is supposed to do, and the Session Duration / record data it gates is unreliable -- consistent
  with the observed duration_seconds:0 (record IS written -- confirming the branch is entered
  under real-device conditions -- but the value pipeline downstream of a broken ownership gate
  cannot be trusted). This is one instance of a wider, systemic "incomplete two-step
  WFConditionalActionString wiring" defect class (see final Evidence entry) affecting at least
  9 other conditional sites across open_pipeline()/select_exit()/enabled_exits(), none of
  which are caught by verify_conditional_inputs() (which only checks the WFInput side, not
  WFConditionalActionString).
fix: NOT APPLIED - goal is find_root_cause_only per task mode. Suggested direction: add
  owns_if["WFWorkflowActionParameters"]["WFConditionalActionString"] = token("Captured Session ID")
  immediately after the existing bare "￼" line (matching the 3 correct sibling sites),
  then sweep and fix the other ~9 sites in the same defect class in one pass (per this
  project's own "fix whole classes" discipline), then extend verify_conditional_inputs() (or
  add a sibling verify_conditional_action_string()) to catch this axis going forward, then
  regenerate/re-sign/re-verify on device per Test 1 and Test 3 (G-04-3 is very likely the same
  root cause).
verification: NOT PERFORMED - diagnose-only mode.
files_changed: []
