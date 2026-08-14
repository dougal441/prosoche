---
slug: open-routing-sequence-error
status: awaiting_human_verify
trigger: "Fix OPEN routing and Test Circle sequence error (from .planning/todos/pending/2026-08-13-fix-open-routing-and-test-circle-sequence-error.md)"
created: 2026-08-14
updated: 2026-08-14 (cycle 9)
severity: blocker
---

# Debug Session: OPEN routing misrouted + Test Circle `sequence` write fails

## Symptoms

<DATA_START>

### Expected behavior

Opening a configured target app fires the manually created App Is Opened Personal
Automation, which runs a wrapper containing a Text action holding exactly `OPEN`
followed by Run Shortcut with its Input set to that Text magic variable. The master
shortcut should take the OPEN path and immediately fire the Circle 1 intervention.

Separately: from the manual menu, choosing **Test a Circle** and then selecting one of
the nine Circle buttons should run that Circle's intervention.

### Actual behavior

1. **OPEN misrouting.** Opening a configured target app displays the manual menu
   (`Status`, `Open Control Room`, `Sync My Profile`, and so on) instead of firing the
   Circle 1 intervention. The received Shortcut Input is apparently not being matched
   as `OPEN`, so routing falls through to MANUAL.

2. **Test Circle `sequence` error.** From that unexpected menu, choosing **Test a
   Circle** displays nine buttons labelled Circle 1 through Circle 9. Selecting any
   Circle produces a runtime error.

### Error messages

> No value provided. No value was provided to the Set Dictionary Value action for the
> key "sequence".

### Timeline

Both observed during the **first** on-device automation test, on 2026-08-13. The OPEN
automation path has never been confirmed working on device. Prior verification for
Phase 08 was automated/structural only (validator + signing), not runtime.

### Reproduction

- OPEN misrouting: install the signed Dumb artifact, create an App Is Opened Personal
  Automation for a configured target app with the Text `OPEN` → Run Shortcut wrapper,
  then open that target app.
- Test Circle: from the menu that appears, choose **Test a Circle**, then tap any of
  Circle 1 … Circle 9.

### Additional context gathered at session start

- **Fork under test:** Dumb (`src/PROSOCHE-Dumb.xml`). Sentient is untested but is
  generated from the same source, so the same defect is presumed present in
  `src/PROSOCHE-Sentient.xml` unless proven otherwise.
- **Build vintage:** the installed `.shortcut` was built from today's artifacts, i.e.
  it reflects the current working-tree source. The bug is therefore expected to
  reproduce from `src/PROSOCHE-Dumb.xml` as it stands, not only from an older build.
- **Device access:** iPhone is available now for iterative on-device re-testing, so
  hypothesis → on-device test cycles are viable.

### Suspected sites (from the originating todo, unverified)

- `tools/build_state_engine.py:1045`
- `tools/build_state_engine.py:1067`
- `src/PROSOCHE-Dumb.xml:27277`
- `src/PROSOCHE-Dumb.xml:27283`
- `src/PROSOCHE-Dumb.xml:28185`
- `src/PROSOCHE-Sentient.xml:28519`
- `src/PROSOCHE-Sentient.xml:28525`
- `src/PROSOCHE-Sentient.xml:29427`

### Explicit non-assumption

It is **not** known whether the OPEN misrouting and the missing `sequence` value share
one cause. They are recorded together only because they were observed in the same
first on-device automation test. Do not assume they are causally related — trace each
independently, then check for a shared source before fixing.

</DATA_START>
<DATA_END>

## Investigation constraints

- The XML under `src/` is **generated** by `tools/build_state_engine.py`. Fixes must be
  made at the generator, then regenerated and propagated to both forks — never by
  hand-editing the generated XML alone.
- Shortcuts cannot be executed on the build Mac. Runtime confirmation requires
  validate → sign → import → on-device run, with the user driving the device.
- Project rules apply: never fabricate an action identifier or parameter shape; verify
  against the Shortcuts Playground bundled reference, and validate with
  `--target-macos 26 --target-platform ios`.

## Current Focus

bug_class: Bohrbug (all three symptoms deterministic and reproducible on every run)

CYCLE 9 reasoning_checkpoint (supersedes cycle 8, which is kept below for history):
  hypothesis: >
    SYMPTOM 1'S SECOND DEFECT, and the fifth axis of this session. A conditional's OPERATOR
    PICKER is populated from the STATIC TYPE of the variable sitting in WFInput. read_value()
    defines its variable from an is.workflow.actions.gettext output, so Shortcuts types it as
    Text and offers only the EIGHT STRING operators — is / is not / has any value / does not
    have any value / contains / does not contain / begins with / ends with. A numeric
    WFCondition (0, 1, 2, 3, 1003) then has NO CASE TO RENDER: the operator chip shows RED and
    iOS refuses to run the action.
    THIS AXIS IS INVISIBLE IN THE PLIST. Keys, envelope, picker literals and condition code are
    all well-formed at a defective site, which is why verify_parameter_keys,
    verify_string_envelopes, verify_required_pickers and verify_conditional_inputs all pass over
    it, and why eight cycles of static sweeps could not see it. Decrypting the signed artifact
    does not reveal it either. It surfaced only because the user photographed red operators.
    DEVICE-LOCALISED, not argued: the cycle-8 pass reached breadcrumb C and died. Action 170 —
    `Cooldown Until > Now Epoch` — is the first site of this class in the artifact and sits
    immediately after C. Both cycle-8 predictions landed in one run.
  confirming_evidence:
    - "DEVICE: build 2026-08-14h advanced the last breadcrumb from B to C and then failed. 'B again' was stated in advance as meaning the cycle-8 fix had not taken; it advanced, so 149/158 are cleared and the failure is a NEW, LATER defect. Action 170 is the first action of substance after C."
    - "UI EVIDENCE (the CAP-06 channel): six user screenshots show the operator rendered RED at six distinct Ifs, and the operator picker — opened on four of them — offers EXACTLY the eight STRING operators with no numeric comparator present. That is a type-driven menu, which is the mechanism itself rather than an inference about it."
    - "CLASSIFIER VALIDATED 6-FOR-6 AGAINST THAT INDEPENDENT UI EVIDENCE: the operand-provenance trace flags 18 sites per fork as gettext-fed; all six photographed red sites fall inside the 18 and ZERO fall outside it. Voice Enabled — the site that broke the initial 'five' sample — is fed by gettext at action 1184 and was always in the bucket."
    - "DEVICE GROUND TRUTH FOR THE EXACT CONSTRUCT — Donor 4.1, built in Shortcuts.app on the target iPhone and decrypted this cycle. A Get Dictionary Value output compared with WFCondition 2 against WFNumberValue '10' serialises its operand as {Type: ActionOutput, OutputName: 'Dictionary Value', OutputUUID: ..., Aggrandizements: [{Type: 'WFCoercionVariableAggrandizement', CoercionItemClass: 'WFNumberContentItem'}]}. iOS does NOT insert a Number action and does NOT change the read chain — it TYPES THE VARIABLE REFERENCE IN PLACE."
    - "THE CONTROL CASE IS IN THE SAME DONOR PAIR. Donor 4 is the same shortcut before the type was set: identical descriptor, NO Aggrandizements, and a code-100 test instead. The only delta between Donor 4 and Donor 4.1 is the coercion plus the numeric condition — which isolates the coercion as the thing that makes a numeric operator legal on a dictionary value."
    - "THE USER'S SCREENSHOT SHOWS THE MECHANISM DIRECTLY: IMG_5636.jpg is the type list for a 'Dictionary Value' chip — Contact / Date / Dictionary / ... / NUMBER / PDF. Choosing Number is what emitted the aggrandizement. The fix is the plist form of a UI action the user performed and photographed."
    - "THE AGGRANDIZEMENT ATTACHES TO A NAMED VARIABLE TOO, not only to an ActionOutput: golden shortcut 332c12a0060043b388b22b806be7ab58 carries WFCoercionVariableAggrandizement on both {Type: Variable, VariableName: ...} and {Type: ActionOutput, ...} descriptors, 24 instances across the corpus. Our operands are named variables, so this is the link that had to be checked and it holds."
    - "POST-FIX MEASUREMENT ON THE SHIPPED SIGNED FILE, decrypted with the BUILD-NOTES §14 recipe rather than read from the build tree: 3684 actions (Dumb) / 3752 (Sentient), 87 / 94 numeric conditionals, 20 / 25 Number-coerced, ZERO text-fed-and-uncoerced in either fork. Action 170 — the exact site that killed build h — now carries the coercion."
  falsification_test: >
    ONE device sitting on build 2026-08-14i. BREADCRUMBS RETAINED for the third cycle running,
    and this time their POSITIONS ARE UNCHANGED from build h (A=92, B=147, C=168, D=286, E=306,
    F=415, G=424, H=458, I=473, J=527) because the fix adds no actions. The next report is
    therefore directly comparable with the last one.
      last letter D or beyond -> the class fix is CONFIRMED. Action 170, the site that killed
        build h, has executed, and with it the first member of the class.
      last letter C again -> THE HYPOTHESIS IS WRONG, or the coercion is not sufficient at this
        site. Leading alternative: something else in span C->D that is not operand typing.
        Because the artifact differs from build h by NOTHING except 20 coercions and two stamp
        strings, a 'C again' result is an unusually clean refutation — it cannot be blamed on
        collateral change.
      all ten letters + the Leaving/Continue menu -> the OPEN pipeline has completed end-to-end
        for the first time in the project's history.
    "C again" is a wholly plausible outcome the fix cannot explain away, so this is a genuine
    falsification test.
  fix_rationale: >
    ONE generator-level change fixes the WHOLE CLASS, per the cycle-9 requirement: a
    normalise_numeric_operands() post-pass attaches Donor 4.1's Number coercion to the operand
    of every numeric-code conditional whose operand is not already Number-typed. Site-by-site
    fixing was explicitly rejected — the bisection can only ever localise the EARLIEST remaining
    site, so incremental fixing would cost one device round trip per site.
    A FIRST APPROACH WAS BUILT AND THEN DISCARDED, and that is worth recording. Before Donor 4.1
    arrived, the fix was composed from corpus evidence: golden 2e0fb675 feeds a Dictionary Value
    straight into is.workflow.actions.number, so a read_number() helper materialised each operand
    through a Number action with a code-100 null guard. It validated, signed and measured clean.
    It was discarded anyway, because the donor showed iOS doing something different for THIS
    construct and device evidence outranks corpus composition. The coercion is also strictly
    better on every axis that matters here: it adds NO actions (so breadcrumb positions and the
    comparability of the measurement survive), it leaves every device-proven read chain
    byte-identical, and it needs no null handling at all — coercing an absent value yields an
    absent value and the comparison simply evaluates false, whereas a Number action fed a JSON
    null was the one unevidenced link in the discarded design.
    SCOPE IS DELIBERATELY MINIMAL. Only operands that are NOT already numeric are touched, so the
    numeric conditionals that have executed on device — notably the Control Room refresh block
    from the cycle-5 pass — stay byte-identical. Total artifact delta versus the build the user
    just tested: 20 conditionals gain an Aggrandizements key, 2 display strings carry the new
    stamp, and every one of the other 3662 actions is byte-identical.
    RECURRENCE GUARD: verify_numeric_operands() asserts the invariant that
    normalise_numeric_operands() establishes, and both run in BOTH forks' builders. They share
    one provenance resolver so they cannot disagree. The generator now asserts five axes — KEY
    NAME, VALUE ENVELOPE, PICKER LITERAL, VARIABLE SLOT and OPERAND TYPE.
  blind_spots:
    - "THE COERCION IS DEVICE-PROVEN AS A SERIALISATION, NOT AS A RUNTIME OUTCOME. Donor 4.1 proves iOS WRITES this shape when the user types a dictionary value as Number, and therefore that the shape is legal and the operator renders. It does not prove what the comparison EVALUATES TO when the underlying value is JSON null, which is the case for cooldown_until on a fresh state.json. The expectation is 'absent coerces to absent, comparison false, no live cooldown' — which is the desired branch — but it is an expectation, not a measurement."
    - "PROVENANCE IS RESOLVED PER NAME, NOT PER EXECUTION PATH. Shortcuts types a named variable from ALL of its Set Variable definitions, so the pass treats a name as non-numeric if ANY definition is Text. That is the conservative direction (it coerces more sites, never fewer) and it is why 20 sites are coerced where the hand trace found 18 — Pressure Next and Overrun Seconds are mixed-typed names whose Text definition sits on a different arm entirely."
    - "THE RIGHT-HAND OPERAND IS DELIBERATELY UNCHANGED. 17 numeric conditionals still carry a gettext-fed WFNumberValue (Heat Cap, Heat Floor, Threshold, Overrun Minimum, Exploit Minimum, Gravity Cap). The evidenced mechanism is the OPERATOR PICKER, driven by the LEFT input only; WFNumberValue is a value field, not a picker, and Donor 4.1 itself pairs a coerced left operand with a plain literal right operand. Recorded as a residual, not fixed."
    - "MOST OF THE CLASS REMAINS UNTESTABLE THIS CYCLE. Only 170/377/384/409 sit before the first OPEN menu; the rest are on the per-Circle voice check and exit-stats paths the user has never reached. They are fixed by construction — the same pass — but this sitting cannot confirm them and they must not be reported as verified."
    - "THE 14 WFConditionalActionString = token(...) SITES ARE STILL UNRESOLVED, carried forward unchanged from cycle 8. Same family, but the WFInput evidence does not transfer: that is a TEXT slot where the Shortcuts UI genuinely allows mixed literal+variable text. All 14 sit past breadcrumb J and cannot affect this measurement."
    - "iOS STILL DOES NOT NAME THE OFFENDING ACTION. Unchanged since cycle 5. The breadcrumbs remain the only instrument, which is why they stay in."
  candidate_causes:
    - "code/generator OPERAND TYPE: a numeric condition code applied to a Text-typed operand, so the operator picker has no case to render (PRIMARY, this cycle's fix; 20 sites Dumb / 25 Sentient; device-proven shape from Donor 4.1, positionally matched to the build-h device result)"
    - "code/generator NAME COLLISION: a variable name assigned from BOTH a numeric and a Text source is mixed-typed, and one Text definition poisons every numeric comparison of that name (CONFIRMED sub-class — Pressure Next, Overrun Seconds, Circle Next; invisible to a hand trace that follows only each conditional's immediate feeding action; covered by the same pass)"
    - "data/state: cooldown_until is JSON null on fresh state (NOT a separate cause under this fix — the coercion has no failure mode on an absent value — but it is the reason the discarded Number-action design carried risk, and it is the residual uncertainty named in blind_spots)"
    - "code/generator ENVELOPE: WFConditionalActionString holds a text template at 14 sites (SAME FAMILY, UNRESOLVED, all past breadcrumb J, deliberately unchanged)"
    - "code/generator SCALAR TYPE: <integer> at number.random / repeat.count (LATENT AT MOST, downgraded in cycle 8, not on this path)"
  and_gate: >
    yes, and it is answered rather than assumed. Under the DISCARDED Number-action design the
    gate genuinely fired at action 170: the operand had to be both Number-typed AND non-null,
    because a Number action fed a JSON null was an unevidenced failure mode. The coercion design
    collapses that gate — it types the reference without converting anything, so an absent value
    stays absent and the comparison simply evaluates false. One condition, not two. That is a
    substantive reason to prefer it, not merely a smaller diff.
    The session's broader pattern still holds: the remaining defect count is NOT assumed to be
    one. The breadcrumbs stay in precisely so a further defect reports as a LATER letter —
    progress plus localisation — instead of an ambiguous "same error".

CYCLE 8 reasoning_checkpoint (superseded, kept below for history):
  hypothesis: >
    ROOT CAUSE FOUND, and asserted as CONFIRMED rather than ranked, because for the first time
    this session the evidence is positional as well as structural.
    THE DEFECT: a conditional's WFInput is {"Type":"Variable","Variable": <token>}, and the
    <token> slot must hold a VARIABLE REFERENCE serialization — WFTextTokenAttachment whose
    Value is a {Type, VariableName} or {Type, OutputUUID, OutputName} descriptor. At 25 sites
    the generator overwrites if_block()'s already-correct value with token(name), which returns
    a WFTextTokenString TEXT TEMPLATE — {"Value": {"string":"￼","attachmentsByRange":{...}}}.
    A text template is not a variable descriptor. Shortcuts cannot resolve the If's input,
    renders the input field as UNSET, and refuses to run the action with exactly the reported
    message, "Please choose a value for each parameter in this action".
    THE POSITIONAL PROOF: of those 25 sites, exactly TWO sit before breadcrumb J. They are
    actions 149 and 158 — BOTH INSIDE SPAN B->C, and 149 is the FIRST occurrence of the defect
    class in the entire 3684-action artifact. The user saw B and did not see C. The first
    instance of the only unproven shape in the span sits two actions past the last breadcrumb
    they saw.
    THIS IS AXIS 2 (value ENVELOPE), not the newest axis. It is the cycle-2 axis inverted:
    cycle 2 established that string-typed parameters need WFTextTokenString; this site needs
    the OPPOSITE, because WFInput.Variable is a variable slot, not a string slot. The generator
    had the right shape and hand-overwrote it with the wrong one.
  confirming_evidence:
    - "DEVICE GROUND TRUTH — Donor 3, action 4, the user's own iPhone, this exact construct (a variable-vs-variable If): WFInput = {'Type':'Variable','Variable':{'Value':{'Type':'Variable','VariableName':'A'},'WFSerializationType':'WFTextTokenAttachment'}}. iOS writes an ATTACHMENT. It does not write a text template. Zero ambiguity."
    - "GOLDEN CORPUS UNANIMOUS — 20 of 20 mode-0 conditionals that carry a WFInput across all 19 shortcuts use WFSerializationType WFTextTokenAttachment inside Variable. ZERO use WFTextTokenString. ZERO contain 'string'/'attachmentsByRange' in that slot. (18 further conditionals carry no WFInput at all and are not evidence either way.)"
    - "INTERNAL CONTROL GROUP, largest of the session — 307 mode-0 conditionals in our own artifact: 282 carry the correct WFTextTokenAttachment form, 25 carry the text template. The 282 include the DEVICE-PROVEN router at actions 37/39/41 (cond 100 and cond 4, which have executed on every single device run this session) and the Control Room refresh conditional at 3612 (executed when the user ran Open Control Room). Same natural-experiment shape that settled cycles 2, 4 and 5."
    - "EXECUTION-COVERAGE SEPARATION IS TOTAL: not one of the 25 defective sites has ever executed on device. 23 of them sit past breadcrumb J on the exit/contract paths the user has never reached; the remaining 2 are 149 and 158, which the bisection just proved were reached for the first time and killed the run."
    - "THE SPAN IS OTHERWISE FULLY DEVICE-PROVEN. All 20 actions in B->C were read individually. 18 of them are classes already executed on device: comment; number with WFNumberActionNumber (proven at action 1359 inside Open Control Room); setvariable with an ActionOutput attachment (proven throughout PRE); setvalueforkey with WFDictionaryValue as WFTextTokenString (this is the cycle-2/3 symptom-2 fix, device-CONFIRMED); conditional modes 1 and 2, which carry only GroupingIdentifier and WFControlFlowMode. Exactly 2 of 20 actions carry a shape that has never run, and both carry this defect."
    - "PRIORITY-3 DATE-ACTION LEAD CLOSED AFFIRMATIVELY, with device evidence rather than inference: gettimebetweendates appears at action 15 at control-flow DEPTH 0, unconditionally, 22 actions before the router. Every device run that reached the manual menu — cycles 3, 5, 6 and 7 — executed it. It carries WFTextTokenString in BOTH DateTime-typed slots (WFInput, WFTimeUntilFromDate) and 'Seconds' in WFTimeUntilUnit. Those shapes are therefore device-proven, and the date/adjustdate actions at 11/13/17/19 with them. No date action needs changing, and no donor is needed to settle it."
  falsification_test: >
    ONE device sitting on build 2026-08-14h. The BREADCRUMBS ARE DELIBERATELY RETAINED, so the
    result is informative under a multi-defect world instead of collapsing to pass/fail:
      last letter C or beyond -> span B->C is CLEARED. The fix is correct and any remaining
        failure is a DIFFERENT, later defect, reported as a new letter and localised in one
        more sitting rather than reading as "the fix did not work".
      last letter B again -> THE HYPOTHESIS IS WRONG. The defect in B->C is not the conditional
        envelope, and the 18 device-proven-by-class actions in that span must be re-examined
        individually rather than by class.
      all ten letters + the Leaving/Continue menu -> the OPEN pipeline has completed end-to-end
        for the first time in the project's history.
    This is a genuine falsification test: "last letter B again" is a wholly plausible outcome
    that the fix cannot explain away.
  fix_rationale: >
    The fix DELETES the 13 generator lines that overwrite WFInput. It does not invent a shape.
    Every one of those 13 overwrites passes the SAME variable name that if_block() was already
    called with on the line above — they change the envelope and nothing else. Deleting them
    leaves if_block()'s own output, which is byte-identical to the 282 correct sites and to
    Donor 3. Nothing is guessed, nothing is fabricated, and the resulting shape is the one iOS
    itself writes.
    RECURRENCE GUARD, so the diff is not deletion-only and the axis closes rather than the
    instance: verify_conditional_inputs() fails the build if any conditional's WFInput.Variable
    is not a WFTextTokenAttachment wrapping a Type-bearing descriptor. Cycle 5 added
    verify_required_pickers for the picker axis; this does the same for the variable-slot axis.
    The generator now asserts KEY, ENVELOPE, PICKER LITERAL and VARIABLE-SLOT shape.
  blind_spots:
    - "THE 14 WFConditionalActionString = token(...) SITES ARE LEFT UNCHANGED AND ARE NOT CLAIMED CORRECT. They are the same family — a variable placed in an operand slot as a text template — but the evidence that settles WFInput does NOT transfer: WFInput.Variable is structurally a variable slot, whereas WFConditionalActionString is a TEXT slot, and the Shortcuts UI genuinely allows mixed literal+variable text there. Corpus coverage is zero (every corpus conditional operand is a literal), catalog coverage is zero (is.workflow.actions.conditional is absent from the ToolKit catalog entirely), device coverage is zero. All 14 sit PAST breadcrumb J, so they cannot affect this cycle's measurement. A donor settles them and one is requested in parallel, at zero device cost to this sitting."
    - "THE SCALAR-TYPE AXIS IS NOW WEAKER THAN CYCLE 7 RECORDED, and this is a correction of my own prior reasoning, not a new finding. Donor 3 writes WFNumberActionNumber as plist <string>; our generator writes <integer>; and ours has EXECUTED SUCCESSFULLY ON DEVICE at action 1359 inside Open Control Room. So iOS demonstrably coerces plist scalar type on at least one of these numeric fields rather than failing to decode it. The cycle-7 inference 'iOS never writes <integer>, therefore <integer> is undecodable' does not follow, and the two latent sites at 418/454 are correspondingly weaker suspects than cycle 7 ranked them."
    - "THE 23 SITES PAST J ARE FIXED BUT UNTESTABLE THIS CYCLE. They sit on exit-selection and Circle-9 contract paths the user has never reached. The fix is applied to them by construction (same generator lines), but this sitting cannot confirm them, and they must not be reported as verified."
    - "A SECOND DEFECT IN B->C IS NOT EXCLUDED. The span's other 18 actions are cleared BY CLASS — the class has executed on device — not by having those specific instances execute. If a class-level clearance is wrong somewhere, the run stops at B again. That outcome is explicitly in the falsification test rather than argued away."
    - "iOS STILL DOES NOT NAME THE OFFENDING ACTION. Unchanged since cycle 5. The breadcrumbs remain the only instrument; that is why they stay in."
  candidate_causes:
    - "code/generator ENVELOPE: conditional WFInput.Variable holds a WFTextTokenString text template where a WFTextTokenAttachment variable descriptor is required (CONFIRMED — donor + corpus 20/20 + internal control 282/307 + exact positional match to the bisection result)"
    - "code/generator ENVELOPE: WFConditionalActionString holds a text template at 14 sites (SAME FAMILY, UNRESOLVED, all past breadcrumb J, donor requested, deliberately unchanged)"
    - "code/generator SCALAR TYPE: <integer> at number.random 418 / repeat.count 454 (LATENT AT MOST, and downgraded this cycle by the WFNumberActionNumber counter-evidence; NOT symptom 1 — execution stops hundreds of actions upstream)"
    - "environment/iOS: date-action DateTime slots carrying WFTextTokenString (ELIMINATED this cycle by device evidence — action 15 runs unconditionally at depth 0 on every successful manual invocation)"
    - "data/state: a stored behavioural_day value that changes which arm of the rollover runs (NOT the cause — BOTH arms are gated by a defective conditional, so the failure occurs at the gate regardless of state)"
  and_gate: >
    yes, and this cycle answers it with a measurement rather than an argument. The remaining
    defect count is NOT assumed to be one. That is precisely why the breadcrumbs are retained
    rather than stripped: under a multi-defect world the next run reports a LATER letter, which
    is progress plus localisation, instead of an ambiguous "same error" that would read as this
    fix having failed — the exact failure mode that made cycle 1's correct fix look like a
    refutation. The 14 unresolved WFConditionalActionString sites are a known, named, deferred
    second condition on the post-menu path, not an unknown.

CYCLE 7 reasoning_checkpoint (superseded, kept below for history):
  hypothesis: >
    TWO SEPARATE CLAIMS, DELIBERATELY KEPT APART, because conflating them is how three
    static "confirmations" got refuted on device in this session.

    CLAIM 1 — THE LOCALISATION, asserted with confidence. The failing action is INSIDE
    PROSOCHE, on the OPEN arm, in actions 91-520 (build-f indexing), before the first OPEN
    menu at 521. Cycle 6 closed the last device-side confound: the SAME unmodified wrapper
    echoed RAW [OPEN] / NORMALISED [OPEN] through Probe 5 and then, on a FRESH re-selection
    of PROSOCHE from the list, failed identically. Handoff proven, stored reference proven.

    CLAIM 2 — THE RANKED PREDICTION, asserted as a candidate and NOT shipped as a fix.
    A FOURTH defect axis exists, and it is one no sweep in this session modelled: the plist
    SCALAR TYPE of numeric literal parameters. Cycle 6 predicted a fourth axis was
    base-rate-likely; this is it. Neither the 19-shortcut golden corpus nor Donor 3 ever
    writes these fields as <integer> — iOS uses <real> or <string> without exception. Our
    generator emits <integer> at 78 sites. The axis is NOT broadly guilty (see below), but
    it survives at EXACTLY TWO sites, and those two are precisely the sites with zero corpus
    precedent, zero device coverage, and a donor that contradicts them:
      action 418  number.random  WFRandomNumberMinimum/Maximum  <integer>  (donor: <string>)
      action 454  repeat.count   WFRepeatCount = 9              <integer>  (donor: <real>)
    A number field iOS cannot decode renders as an unfilled picker/field, which is exactly
    "Please choose a value for each parameter in this action".
  confirming_evidence:
    - "DEVICE GROUND TRUTH, Donor 3 decrypted this cycle: iOS writes number.random's min/max as plist <string> and repeat.count's WFRepeatCount as plist <real>. We write <integer> for both."
    - "GOLDEN CORPUS, all 19 shortcuts: conditional.WFNumberValue is <real> 4/4; number.WFNumberActionNumber is <real> 2 / <string> 1 / attachment 2; repeat.count.WFRepeatCount is attachment 2/2 with NO literal instance anywhere. Zero <integer> in any of them."
    - "PERFECT SEPARATION against the device-proven MANUAL path — the same internal-control-group shape that settled cycles 2, 4 and 5, and applied here with cycle 6's stricter standard (EXECUTED, not merely 'appears on the manual arm'): number.WFNumberActionNumber <integer> at action 1359 sits inside the menu case 'Open Control Room' WHICH THE USER RAN SUCCESSFULLY, and conditional.WFNumberValue <integer> at 3646/3653 sits in the Control Room refresh block that ran on that same pass. Those two classes are therefore DEVICE-PROVEN FINE as <integer>, which is what narrows the axis from 78 sites to 2 rather than leaving it as a vague suspicion."
    - "THE DONOR'S PRIMARY VALUE THIS CYCLE WAS ELIMINATION, and that is recorded as a positive result: cycle 6's #1 and #3 ranked candidates (variable-backed WFNumberValue; math with WFMathOperation omitted) are BYTE-IDENTICAL to iOS's own serialization, and round is a superset of it. DEV-05 is settled affirmatively. Three of four ranked candidates died on device evidence at zero device cost."
  falsification_test: >
    ONE device sitting. Install build 2026-08-14g (signed, decrypt-verified), re-point the
    automation's Run Shortcut, open a watched app, report the LAST letter seen.
    Ten breadcrumb alerts A-J sit at OPEN-arm base depth. The last letter localises the
    failure to the span that follows it.
      last letter G  -> number.random (suspect 1) is in span G->H. PREDICTION CONFIRMED.
      last letter H  -> repeat.count  (suspect 2) is in span H->I. PREDICTION CONFIRMED.
      any other letter -> PREDICTION KILLED, and the span is localised anyway, which is the
        whole point of measuring instead of guessing.
      NO letters at all -> would CONTRADICT cycle 6's probe result (execution never reaches
        action 92) and reopens the router/PRE region as its own investigation.
      all ten + the Leaving/Continue menu -> the OPEN pipeline completed for the first time
        in the project's history and symptom 1's blocking defect is gone.
  fix_rationale: >
    NO FIX IS SHIPPED, for the second cycle running, and again deliberately. The cycle-7
    instruction is explicit: a donor-derived defect is a CANDIDATE for the bisection to
    confirm, never a blind ship, and the bisection is a MEASUREMENT that must not be
    confounded. Shipping the <integer>-to-<string>/<real> change now would make a G/H result
    uninterpretable and would be the fourth static guess of this session.
    What IS shipped is the instrument. Its design rationale: (a) breadcrumbs sit at OPEN-arm
    base depth or on the normal arm of each guard, so a breadcrumb cannot be skipped by the
    conditional the failing action sits inside; (b) the alert introduces no inferred shape —
    plain-string title is device-proven from the cycle-3 ROUTER TRACE, plain-string message is
    corpus-verified 5 of 13 — and references no variable, so it cannot fail for its own
    reason; (c) breadcrumb() calls no uid(), so the deterministic UUID counter never advances
    and the artifact minus the alerts is byte-identical to build f at all 3674 actions bar the
    two display-only stamp strings. Symptoms 2 and 3 are preserved BY CONSTRUCTION and that is
    verified by comparison, not asserted.
  blind_spots:
    - "ONE PASS DOES NOT LOCALISE SPANS C, E OR I. C->D is 117 actions with 11 nested blocks at depth 4 (cooldown: live-Ice menu plus Ice-expiry restore); E->F is 108 actions, 11 blocks, depth 4 (the whole Heat pipeline); I->J is 53 actions, 3 blocks, depth 3 (pending exit, two repeat-each loops). A last letter of C, E or I buys a span, not an action, and REQUIRES a second finer bisection round inside it. This is stated in the shipped protocol rather than glossed."
    - "THE PREDICTION MAY BE RIGHT ABOUT THE AXIS AND WRONG ABOUT THE SITE. <integer> could be benign everywhere (iOS may coerce NSNumber freely) and the real defect at 418/454 could be something else entirely in those spans — Detect Dictionary, the Gravity conditional, or the threshold Get Dictionary Value with a composite key. A G or H result CONFIRMS THE SPAN, not the mechanism; the follow-up fix must still be single-variable."
    - "iOS DOES NOT NAME THE OFFENDING ACTION — unchanged since cycle 5. The user cannot narrow this by inspecting and must not be asked to."
    - "TEN TAPS IS A REAL COST and a real risk: a mis-remembered last letter sends the next cycle at the wrong span. Mitigated by making each alert show one letter plus 'Report the LAST letter you see', but not eliminated."
    - "THE RE-POINT IS LOAD-BEARING AND EASY TO SKIP. Deleting PROSOCHE to install build g orphans the automation's Run Shortcut target (BUILD-NOTES §automation-wrapper). If the user re-imports without re-selecting the target, the run fails with the SAME error for a wholly different reason and the cycle is wasted. It is step 0 of the protocol and flagged as unskippable."
    - "SCALAR TYPE WAS NEVER CHECKED BEFORE CYCLE 7, across six cycles of sweeps that each believed they were exhaustive. Whatever the device says next, that is the recurrence-guard lesson: the generator has no invariant asserting the plist TYPE of any emitted parameter, only its key, envelope and picker literal."
  candidate_causes:
    - "code/generator SCALAR TYPE: number.random min/max emitted as <integer> where iOS writes <string> (PRIMARY prediction, action 418, span G->H, donor-contradicted, zero device coverage)"
    - "code/generator SCALAR TYPE: repeat.count WFRepeatCount emitted as <integer> where iOS writes <real> (PRIMARY prediction, action 454, span H->I, donor-contradicted, zero corpus literal anywhere)"
    - "code/generator: something else inside spans G->H or H->I — Detect Dictionary, the Gravity conditional, or the composite-key threshold lookup (SECONDARY; a G/H result confirms the span, not the mechanism)"
    - "code/generator: a defect inside one of the deep spans C, E or I, requiring a second bisection round (LIVE, and the single most likely outcome by action count — those three spans hold 278 of the 429 measured actions)"
    - "environment/iOS: Run Shortcut handoff semantics for a large nested shortcut (RESIDUAL only — Probe 5 was small, so a size interaction is not fully excluded, but the failure is now known to be inside PROSOCHE)"
  and_gate: >
    yes, and this cycle sharpens rather than repeats the point. The session's established
    pattern is that reaching Circle 1 required THREE simultaneous conditions, each fixed in a
    different cycle (Input Key envelope, positive-match router, picker parameters). Cycle 7
    does not assume the remaining count is one. The bisection is designed to be informative
    under a MULTI-DEFECT world too: it reports the FIRST failing span, so if there are two
    remaining defects it finds the earlier one and the next round finds the next, rather than
    a single "fix" appearing to fail because a second condition still gates the same outcome.
    That is precisely the failure mode that made cycle 1's correct fix read as a refutation.

CYCLE 6 reasoning_checkpoint (superseded, kept below for history):
  hypothesis: >
    NOT ASSERTED AS A CAUSE. Cycle 6 deliberately declines to nominate a fourth code-side
    hypothesis, because static analysis has now been driven to exhaustion on the OPEN pre-UI
    region and the honest state of the evidence is a CONTRADICTION, not a lead.
    What cycle 6 DOES assert, and what the device test is designed to settle, is the PARTITION:
      (A) input reaches PROSOCHĒ and the defect is inside the OPEN pipeline, or
      (B) the failure occurs at/above the Run Shortcut handoff and no PROSOCHĒ action ever runs.
    Five cycles have assumed (A) without ever testing it. The INPUT PROBE, designed in cycle 1
    and deferred five times, is the experiment that decides it, and it is executed FIRST this
    cycle rather than behind another static pass.
    Two sub-hypotheses under (B), both live and both untested:
      (B1) STALE STORED REFERENCE. The wrapper's Run Shortcut chip renders from a cached NAME,
           while its stored workflowIdentifier still points at the shortcut instance that was
           DELETED during a clean install. The chip therefore looks correct while the parameter
           resolves to nothing. This is not the refuted orphan theory: that was refuted on the
           user's VISUAL inspection, which the debug file itself flagged as caveat (i), weaker
           than stored-representation evidence. Timeline fits exactly — the automation ran in
           cycle 1 and has failed at the handoff ever since the first delete-and-reimport.
      (B2) The automation TRIGGER's own app selection, not an action, holds the unset parameter.
  confirming_evidence:
    - "USER TESTIMONY, cycle 5 Q1, verbatim: 'No - nothing at all, straight to the error.' The first UI on the OPEN path is action 521; if execution had entered the OPEN arm and failed anywhere in 91-520, this is equally consistent. But it is ALSO exactly what (B) predicts, and (B) has never been excluded."
    - "NEGATIVE STATIC RESULT, this cycle, on the region the device implicates: the OPEN pre-UI region is 91-520 (confirmed: the first UI action reachable on a normal OPEN is the choosefrommenu at 521; the only earlier UI, 169, sits inside the cooldown branch at 167). Across 91-520 there are ZERO empty-valued parameters, ZERO absent catalog parameters other than the four already-exonerated classes, and ZERO invalid picker literals."
    - "PICKER-VALIDITY AXIS CLOSED, a genuinely new check: every emitted picker literal in the artifact was validated against the catalog's enum CASE lists (ids and titles), not merely checked for presence and literalness as in cycle 5. All 20 distinct literals are valid cases - round 'Ones Place'/'Always Round Down', gettimebetweendates 'Seconds', count 'Items', getitemfromlist 'Item At Index'/'First Item', setvolume 'Media', changecase 'UPPERCASE', adjustdate 'Subtract', ask 'Text'/'Number'/'URL', math '×'/'÷'/'-', searchweb 'Google', format.date 'Custom', getdevicedetails 'Current Volume'/'Current Brightness', appendnote 'append'. Zero invalid. A wrong enum case would render an unfilled picker exactly like a missing one, so this was a real candidate axis and it is now eliminated."
    - "THE FOURTH AXIS IS REAL BUT IS A BLIND SPOT, NOT A DEFECT: 336 of the OPEN body's actions are the control-flow family (conditional 263, choosefrommenu 53, repeat.each 18, repeat.count 2), and NONE of these identifiers exists in the ToolKit catalog at all. Every catalog-driven sweep, including cycle 5's, is structurally blind to all of them. Inspecting them by hand shows the operand shapes are internally consistent (numeric codes 0/1/2/3 carry WFNumberValue, string codes 4/5/99 carry WFConditionalActionString, presence codes 100/101 carry WFInput alone) and cond 4 and cond 100 are both DEVICE-PROVEN by the router and the PRE region."
    - "EXONERATION-BY-MANUAL-PATH IS WEAKER THAN CYCLE 5 TREATED IT. Cycle 5 exonerated a class if it 'also appears on the device-proven MANUAL path'. Appearing is not executing: the user exercised only the menu, Change Sequence -> Classic, and Open Control Room. The only region certain to have executed is PRE (0-89) plus those specific cases. Re-scored against PRE alone, these OPEN pre-UI shapes have NEVER run on device: conditional+WFNumberValue (13), math without WFMathOperation (13), math with WFMathOperation (3), setvalueforkey (29), number (5), number.random (1), round (1), repeat.count, repeat.each, appendvariable (2), getitemfromlist, returntohomescreen, setbrightness, setvolume."
    - "CORPUS COVERAGE IS GENUINELY ABSENT for the top remaining candidates, so they cannot be settled statically: is.workflow.actions.round has ZERO golden-corpus instances; is.workflow.actions.number.random has ZERO; and across all 19 golden shortcuts EVERY conditional operand is a LITERAL - there is not one instance of a variable-backed WFNumberValue or WFConditionalActionString anywhere in the corpus."
    - "DEV-05 RE-CHECKED INDEPENDENTLY rather than inherited: the corpus is 1 math WITH WFMathOperation ('-', golden 332c12a0) and 1 WITHOUT (golden 2e0fb675, our exact WFInput+WFMathOperand shape). Cycle 5 reported this as a refutation of the missing-operation theory; it is more accurately a 1-of-2 split. The omission stays UNCHANGED this cycle - it is corpus-supported and changing it would confound the probe - but it is NOT as settled as cycle 5 recorded, and it is on the donor request."
  falsification_test: >
    ONE device sitting, three ordered experiments, NO PROSOCHE rebuild and NO clean install.
    ORDER IS LOAD-BEARING: a clean install of PROSOCHE would silently repair sub-hypothesis
    (B1) and destroy the experiment, so the user is told explicitly not to reinstall.
    STEP 1 - INPUT PROBE. Repoint the automation's Run Shortcut at "PROSOCHE Probe 5 - Input
      Echo" (signed, 5 actions, mirrors PROSOCHE's own normalisation chain and root input
      declaration byte-for-byte). Open a target app.
        alert shows RAW [OPEN] / NORMALISED [OPEN]  -> handoff delivers input; pursue (A)
        alert shows [] / []                          -> handoff runs but delivers nothing
        SAME "please choose a value" error, no alert -> failure is AT/ABOVE the handoff, in the
          wrapper or trigger, and is INDEPENDENT of shortcut content. This single outcome
          refutes five cycles of plist-side theory outright and confirms (B).
    STEP 2 - REPOINT BACK. Set the Run Shortcut target back to PROSOCHE by selecting it fresh
      from the list. Open a target app again. This is a clean single-variable test of (B1),
      because re-selecting rewrites the stored reference without changing anything else.
        now works        -> (B1) CONFIRMED: the stored reference was stale; the plist was never
                            the problem after cycle 3, and the recurrence guard belongs in the
                            shipped setup instructions, not in the generator.
        fails identically -> (B1) REFUTED with stored-representation evidence rather than a UI
                            reading, and the defect is inside PROSOCHE's OPEN pipeline.
    STEP 3 - DONOR 3 (only if step 1 shows input arriving). The user builds a small shortcut in
      Shortcuts.app on the iPhone containing exactly the constructs that have zero corpus and
      zero device coverage, then exports it. Decrypting it gives iOS's OWN serialization as
      ground truth - the identical technique that cracked symptom 3 in cycle 4.
  fix_rationale: >
    NO CODE FIX IS SHIPPED THIS CYCLE, and that is the deliberate decision rather than an
    absence of one. Three static-only "confirmations" have been refuted on device in this
    session (cycles 1, 2, 5). The remaining plist-side candidates are all unverifiable on the
    build Mac - zero corpus coverage and zero device coverage - so shipping a fix for any of
    them would be a fourth guess, and would additionally confound the probe by changing the
    artifact under test. The cheapest decisive move is to measure the partition first.
    The cycle-5 picker fixes are RETAINED unchanged, per instruction and on their own merits.
    Symptoms 2 and 3 are untouched: no generator change is made at all this cycle, so both
    remain byte-identical to the build that device-confirmed them.
  blind_spots:
    - "STEP 2 IS ORDER-SENSITIVE AND SELF-REPAIRING. Repointing at the probe in step 1 already rewrites the wrapper's stored Run Shortcut reference. If (B1) is true, step 1 CANNOT show the handoff error - it will show the alert - and only step 2 distinguishes 'the reference was stale' from 'the handoff was always fine'. This is why step 2 exists and why its result must be read against step 1 rather than alone."
    - "THE PROBE CANNOT PROVE PROSOCHE-SPECIFIC HANDOFF HEALTH. It is a different, much smaller shortcut. If input reaches the probe it does not strictly follow that input reaches PROSOCHE - e.g. a size/complexity or input-content-class interaction remains conceivable. The probe's root input declaration is therefore made identical to PROSOCHE's (WFWorkflowInputContentItemClasses = ['WFStringContentItem'], WFWorkflowHasShortcutInputVariables = true) to remove the most plausible confound, but this residual is recorded rather than argued away."
    - "iOS DOES NOT NAME THE OFFENDING ACTION - re-confirmed in cycle 5 and unchanged. The user cannot narrow this by inspecting further and must not be asked to."
    - "IF STEP 1 SHOWS INPUT ARRIVING AND STEP 2 STILL FAILS, the next move is BISECTION BY BREADCRUMB, not a fifth static sweep: flag-gated alerts at OPEN-arm base depth (91, ~200, ~300, ~400, ~470, 519) so the last letter the user sees localises the failing action to a span of tens. Static reading has now produced three refuted confirmations and one exhausted region; it should not be the primary instrument again."
    - "REPO HAZARD, discovered this cycle and NOT a code finding: at session start the working tree was checked out at efb5a79 - a commit predating ALL of cycles 1-5, in which none of the generator fixes exist. It has since been moved to branch codex/automation-parameter-diagnosis at 7ca8ebb, which does carry them (BUILD_STAMP 'build 2026-08-14f', signed Dumb 188441 bytes, matching the cycle-5 record exactly). Anyone rebuilding while the tree is on codex/prosochedebug1 or codex/round1 would silently produce a pre-cycle-1 artifact and see all three original symptoms return. Verify HEAD before any rebuild."
  candidate_causes:
    - "config/device: the wrapper's Run Shortcut holds a STALE stored workflowIdentifier from a deleted install while rendering a valid-looking name chip (B1, PRIMARY untested candidate, step 2 decides it)"
    - "config/device: the automation TRIGGER's own app selection carries the unset parameter (B2, untested)"
    - "code/generator: a variable-backed WFNumberValue on the OPEN path resolves as an unfilled number field (A1 - zero corpus coverage, first site action 167, guaranteed path; donor step 3 settles it)"
    - "code/generator: round / number.random parameter shapes, both with ZERO corpus instances (A2, guaranteed path at 316 and 418)"
    - "code/generator: math with WFMathOperation omitted for '+' (A3, DEV-05; corpus 1-of-2, weaker than cycle 5 recorded)"
    - "environment/iOS: Run Shortcut handoff semantics for a large nested shortcut invoked from an App automation (A4/B, residual)"
  and_gate: >
    yes, and cycle 6 is the first cycle to notice that the AND-gate may span the DEVICE
    CONFIGURATION and the PLIST rather than two plist defects. Every prior cycle tested
    plist-side conditions against a wrapper whose stored state was never verified - only its
    rendering was. If (B1) holds, then cycles 3-5 were each testing a necessary plist fix
    against a device-side condition that guaranteed failure regardless, which is precisely the
    silent AND-gate the cycle-4 checkpoint warned about and then closed on the weaker evidence.

CYCLE 5 reasoning_checkpoint (superseded, kept below for history):
  hypothesis: >
    SYMPTOM 1 is a THIRD instance of the session's recurring defect family — "the parameter
    key/shape iOS actually reads was never emitted" — this time on a THIRD axis the previous
    two passes never examined: REQUIRED PICKER (enum) PARAMETERS.
    Cycle 1 fixed the KEY NAME axis. Cycles 2/4 fixed the VALUE ENVELOPE axis. Neither pass
    ever asked "is a required enum picker present, and does it hold a literal enum case?"
    Two sites violate it, and they are the ONLY two in the whole artifact:
      is.workflow.actions.count.WFCountType         MISSING entirely (1 Dumb / 2 Sentient)
      is.workflow.actions.getitemfromlist.WFItemSpecifier  holds a VARIABLE TOKEN, not a
        literal enum case, at 31 of 33 sites, with WFItemIndex absent
    An enum picker that is absent or holds a non-literal renders in Shortcuts as an unfilled
    picker, and iOS refuses to run the action with exactly "Please choose a value for each
    parameter in this action" — the user's verbatim error.
    WHY IT SURFACED ONLY NOW, and why four cycles of router work never touched it: the OPEN
    branch had NEVER ONCE EXECUTED on device before build d. On 2026-08-13 the automation DID
    run PROSOCHĒ successfully, but Input Key was empty (pre-envelope-fix), so routing took the
    MANUAL arm and the OPEN pipeline was skipped entirely. The cycle-2 envelope fix made
    Input Key resolve to "OPEN" for the first time, so build d was the first build ever to
    ENTER the OPEN branch — and it failed on the first defective action it met there.
  confirming_evidence:
    - "PERFECT SEPARATION across picker parameters, both forks, same artifact: 8 picker classes carry a literal enum case (searchweb 'Google', changecase 'UPPERCASE', getdevicedetails 'Current Volume'/'Current Brightness', setvolume 'Media', gettimebetweendates 'Seconds', round 'Ones Place', searchmaps 'Maps', getitemfromlist 'First Item' x2). EXACTLY TWO deviate: count.WFCountType missing, getitemfromlist.WFItemSpecifier non-literal x31. Same internal-control-group shape that settled cycles 2 and 4."
    - "GOLDEN CORPUS UNANIMOUS on count: 11/11 real is.workflow.actions.count actions emit WFCountType (all 'Items'); 0 omit it. Catalog agrees — WFCountType is the FIRST parameter, name 'Type'."
    - "GOLDEN CORPUS UNANIMOUS on getitemfromlist SHAPE: every corpus instance puts a LITERAL enum in WFItemSpecifier ('First Item' / 'Item At Index' / 'Items in Range') and the DYNAMIC index in WFItemIndex. Golden 332c12a0060043b388b2 does precisely what we need — WFItemSpecifier='Item At Index' with WFItemIndex holding a Repeat Index VARIABLE token. Our generator inverted this: it put the variable in the specifier and emitted no WFItemIndex."
    - "INTERNAL CONTROL GROUP inside our own generator: build_state_engine.py:820 emits WFItemSpecifier='First Item' (literal, correct) while :435 and :552 emit WFItemSpecifier=variable(...) (wrong). Same action, same build, two shapes — the cycle-2/cycle-4 natural experiment recurring a third time."
    - "PRE-FLIGHT VALIDATION REFUTED, so the failing action must genuinely EXECUTE: count/getitemfromlist/speaktext carried these identical defects in the 2026-08-13 build, and that build ran from the automation all the way to the MANUAL menu without this error. iOS therefore does not validate the whole shortcut on load; it errors on the action it reaches."
    - "SEARCH SPACE CONFINED BY EXECUTION, not assumption: 12 identifiers appear in the OPEN body and NEVER in the device-exercised PRE+MANUAL population. Every missing-picker class that ALSO appears on the device-proven MANUAL path is exonerated by direct evidence."
  falsification_test: >
    Device, one clean install of build 2026-08-14f, opening a configured target app.
    (a) If the automation still fails with "Please choose a value for each parameter in this
        action", the required-picker hypothesis is WRONG for symptom 1 and the cause is not a
        picker parameter.
    (b) If a PROSOCHĒ menu now appears (prompt "PROSOCHĒ", options Leaving / Continue), the
        OPEN pipeline has executed end-to-end for the first time in the project's history and
        symptom 1's routing is resolved.
    DISCRIMINATOR THAT COSTS NOTHING AND MUST BE READ FIRST: whether ANY PROSOCHĒ UI appears
    before the failure. This single bit was never captured in cycles 3 or 4 and it partitions
    the remaining space cleanly — see blind_spots.
  fix_rationale: >
    Emits the picker value iOS actually reads, in the literal enum form the golden corpus uses
    unanimously, and moves the dynamic index to WFItemIndex where the corpus puts it. This
    repairs the field the OS reads rather than masking a symptom, and every literal used is
    corpus-verified — nothing is fabricated.
    Generalised rather than patched: a new REQUIRED_PICKER_PARAMS table plus
    verify_required_pickers() makes "a required enum picker must be present AND literal" a
    build-failing invariant across NINE picker classes, not just the two that were broken. The
    previous two cycles each fixed one axis and left the next one undefended; this closes the
    axis itself.
    speaktext.WFInput -> WFText is included because the same audit settled DEV-03: the catalog
    DOES define speaktext parameters (WFText, str) — the earlier note that it "lists no
    parameters at all" was simply wrong, so no fabrication is required to fix it.
  blind_spots:
    - "LOAD-BEARING UNVERIFIED ASSUMPTION, stated plainly: it is NOT established that the failure occurs before any PROSOCHĒ UI appears. That was the coordinator's characterisation; the user's verbatim reports in cycles 3 and 4 say only that the automation failed and never mention whether a menu appeared. It matters because the pre-menu OPEN region (actions 91-521) was swept EXHAUSTIVELY this cycle and is statically CLEAN — every parameter complete and correctly valued. Both confirmed defects sit AFTER the first OPEN menu (count at 576 inside case 'Leaving'; getitemfromlist at 580/1155/1160/1166). So if no menu ever appeared, this fix cannot be the whole story and the cause is upstream of action 521."
    - "iOS DOES NOT NAME THE OFFENDING ACTION. The automation-failure notification reports the AUTOMATION's name and the message only. There is no drill-down, no action index, no log. The user cannot discover which action iOS objects to by inspecting further, and should not be asked to try."
    - "getitemfromlist index base is asserted from the generator, not observed: Rotation Index = (counter % count) + 1 and Circle Next is seeded to 1 / assigned from Repeat Index, so both are 1-based and match Shortcuts' 1-based Item At Index. If Shortcuts were 0-based here the fix would be off by one — but the action has never once run successfully, so there is no prior behaviour to regress."
    - "The 31 getitemfromlist sites span OPEN and MANUAL. The MANUAL ones sit on the Test-a-Circle / Circle-dispatch path, which the user exercised on 2026-08-13 and which failed then with the symptom-2 error — so it is UNKNOWN whether a defective getitemfromlist has ever been reached. This fix may therefore also repair a latent MANUAL-path failure that has been masked."
    - "openapp emits a legacy WFAppIdentifier alongside the donor-verified WFSelectedApp, and omits the OS27-only WFWindowingFormat. Left UNCHANGED: extra keys are provably ignored (WFShowFilePicker, ShowWhenRun coexist on working paths) and WFWindowingFormat is OS27-gated, so adding it would violate the iOS-26 target."
    - "math WFMathOperation is DELIBERATELY left absent at 25 sites. It looked like the leading candidate — a required enum picker missing on the OPEN Heat path — and was REFUTED by the corpus: golden 2e0fb675e459 (client 1146.11.1, minClient 900, same vintage as ours) omits WFMathOperation with our exact key shape. Per this project's own cycle-2 precedent, corpus evidence outranks catalog inference."
  candidate_causes:
    - "code/generator PICKER: required enum parameters absent or holding a variable token instead of a literal enum case (PRIMARY, this cycle's fix; corpus-unanimous on both sites)"
    - "code/generator KEY: speaktext emits WFInput where the catalog defines WFText (SECONDARY, fixed, closes DEV-03)"
    - "config/device: the automation wrapper (ELIMINATED this cycle by screenshot — two actions, both parameters bound, no third action)"
    - "environment/iOS: whole-shortcut pre-flight validation on automation launch (ELIMINATED — the 2026-08-13 build carried the identical picker defects and ran from the automation to the MANUAL menu)"
    - "data/state: a state value that makes the OPEN branch take a different path (NOT RULED OUT; the pre-menu region is clean for every branch, so this would have to act after action 521)"
  and_gate: >
    yes, and it is now the recorded pattern of this whole session rather than a suspicion.
    Reaching Circle 1 from an OPEN required THREE conditions simultaneously, each fixed in a
    different cycle: a populated Input Key (cycle 2 envelope), a router that routes on positive
    match (cycle 3), and an OPEN pipeline whose actions all carry the parameters iOS reads
    (cycle 5). Each earlier fix was necessary and none was sufficient, which is exactly why
    symptom 1 appeared untouched for four cycles — and why cycle 2's fix, by finally letting
    execution ENTER the OPEN branch, is what exposed this defect rather than causing it.

CYCLE 4 reasoning_checkpoint (superseded, kept below for history):
  hypothesis: >
    SYMPTOM 3 is the SAME value-envelope mechanism as symptom 2, at THREE sites the cycle-2
    allowlist never covered, because the allowlist was scoped to catalog type `str` and the
    Notes body parameters are catalog type `AttributedString` — a third type category that
    was never considered and that behaves like `str`, not like a content item.
    Specifically: com.apple.mobilenotes.SharingExtension.WFCreateNoteInput (the note BODY)
    carries a bare WFTextTokenAttachment, so the body resolves to EMPTY at run time while
    the create call itself still succeeds — which is exactly "note exists but is empty".
    A second, independent divergence sits in the same two-action chain: our reference to the
    Make Rich Text from Markdown output names it "Rich Text"; its real output name is
    "Rich Text from Markdown".
    A third site, is.workflow.actions.appendnote.text (the manual Control Room refresh
    snapshot), carries the same bare attachment and would append empty content.
  confirming_evidence:
    - "DEVICE DONOR, decrypted this cycle from .planning/debug/'Donor - notes.shortcut' (an Apple-signed Create Note shortcut exported from the USER'S OWN iPhone): its WFCreateNoteInput is {'string': '￼', 'attachmentsByRange': {'{0, 1}': <token>}} with WFSerializationType WFTextTokenString. Ours is a bare WFTextTokenAttachment. This is ground truth from the target device, not catalog inference."
    - "The donor also names the markdown output 'Rich Text from Markdown'; ours says 'Rich Text'. INDEPENDENTLY CORROBORATED by golden shortcut f44f5caf5e3e action 14, which references a getrichtextfrommarkdown output by exactly that name. Two independent sources agree against us."
    - "Exactly ONE link in the three-action create chain diverges from the donor. 3613 gettext (WFTextTokenString) matches; 3615 getrichtextfrommarkdown.WFInput as a BARE attachment matches the donor AND golden f44f5caf action 13 (WFInput is catalog-typed com_apple_shortcuts_wfcontent_item, so bare is correct there); 3616's body parameter is the only mismatch. The divergence is at the exact link whose output is empty."
    - "ToolKit v78 catalog: SharingExtension.contents and appendnote.text are both typePythonName AttributedString. The cycle-2 allowlist keyed on `str` only, so BOTH were structurally invisible to normalise_string_envelopes AND to its recurrence guard."
    - "INTERNAL CONTROL GROUP, same fork, same action identifier: appendnote at action 3668 already carries a WFTextTokenString (it is a composite template, so it was authored that way by accident of shape) while appendnote at 3648 carries a bare attachment. Same parameter, same action, two envelopes — the cycle-2 natural experiment repeating."
    - "MECHANISM IS RUNTIME-CONFIRMED, not theorised: symptom 2 passed on device in cycle 3 precisely because its bare attachment was converted to WFTextTokenString. This cycle applies an already-proven mechanism to sites it never reached."
  falsification_test: >
    Device, one clean install of build 2026-08-14e. The two note writes are deliberately
    instrumented as SEPARATE experiments:
    (a) CREATE path (note body). Changes on TWO axes — envelope AND output name — so a pass
        confirms the path but does NOT discriminate between them. If the note body is still
        empty, the AttributedString-envelope hypothesis is WRONG for the create path.
    (b) APPEND path (Control Room refresh snapshot, action 3648). Changes on the ENVELOPE
        AXIS ONLY — its OutputName 'Text' is already correct for a gettext source. This is a
        clean single-variable test. If the "## CURRENT SETTINGS" block does NOT appear after
        choosing Open Control Room, the AttributedString-envelope hypothesis is refuted
        outright, and the create-path result is uninterpretable.
    (c) If the append block appears but the body is still empty, the envelope is right and
        the create action has a further problem (the omitted folder/WFNoteGroup, or the
        `name` parameter our build emits and the donor does not).
  fix_rationale: >
    Extends the existing, device-proven normalise_string_envelopes allowlist to the two
    AttributedString-typed Notes body parameters, so the SAME converter and the SAME
    build-failing recurrence guard now cover them. It repairs the field iOS actually reads
    rather than masking the symptom, and it is derived from a device export of the target
    iPhone rather than from catalog inference.
    Deliberately NOT done, to keep the fix minimal and the test interpretable: the donor's
    `folder`/`WFNoteGroup` parameters are not added (the note demonstrably creates without
    them, and adding unproven parameters is how the resolved unsupported-device-import
    session's import blocker was created), and the `name` parameter is left in place (it is
    not implicated in an empty BODY, and removing it risks the Find-Notes reuse path).
  blind_spots:
    - "No golden-corpus instance of appendnote exists, so appendnote.text rests on catalog type + the donor's AttributedString analogue + the internal control group. Same shape of weakest link as cycle 2's setvalueforkey — which turned out to be correct."
    - "Whether OutputName is load-bearing at all, or purely a display label, is not determinable on the build Mac. It is corrected because two independent sources say ours is wrong, not because it is believed to be the cause."
    - "SYMPTOM 1 IS NOT ADDRESSED IN CODE THIS CYCLE and must not be recorded as progressed. Cycle 3 produced zero plist-side OPEN evidence. The plist-side OPEN path has never once been exercised on device with both the envelope fix and the router fix present."
    - "The user has deleted the shortcut before every clean install. Deleting a shortcut orphans any Personal Automation's Run Shortcut reference. This is a strong, mechanistic explanation for the cycle-3 automation error but it is a HYPOTHESIS, not established — a screenshot settles it."
    - "TEST-INVALIDATING CONFOUND, must be controlled on the next run: iOS Notes 'delete' moves a note to Recently Deleted for 30 days rather than destroying it. If Find Notes (action 3599, filter Name contains 'PROSOCHĒ — Control Room') matches a soft-deleted note, the REUSE branch at 3609 fires, no note is created, and the body stays empty NO MATTER WHAT THE FIX DOES. Whether Find Notes searches Recently Deleted is not determinable on the build Mac. The device protocol therefore requires emptying Recently Deleted, and the run is uninterpretable for the create path if it is skipped. The append path (3648) is unaffected by this confound, which is a further reason to read it first."
    - "Diagnostic available for free on the next run: if the leftover empty notes are TITLED 'PROSOCHĒ — Control Room', the `name` parameter is honoured on device; if they are untitled, `name` is ignored and the title must come from the body's first line. This settles DEV-04's open question without a dedicated cycle."
  candidate_causes:
    - "code/generator ENVELOPE: AttributedString-typed Notes body parameters carry bare attachments (PRIMARY, this cycle's fix; runtime-proven mechanism, device-donor-verified shape)"
    - "code/generator REFERENCE: the markdown output is referenced by the wrong OutputName (SECONDARY, corrected, donor + corpus evidenced)"
    - "config/device: the Personal Automation's Run Shortcut target was orphaned by the clean-install delete (SYMPTOM 1, PRIMARY, addressed by instructions + screenshot request, NOT by code)"
    - "data/Notes: the omitted folder/WFNoteGroup parameters (NOT changed; discriminated by outcome (c) above)"
  and_gate: >
    yes. Symptom 3 needs BOTH a correct body envelope AND a create action iOS accepts;
    symptom 1 needs BOTH a correctly configured automation wrapper AND a correct plist-side
    OPEN path, and only the second has ever been worked on. Three cycles of plist-side OPEN
    theory were tested against a wrapper whose health was never once verified — that is the
    AND-gate failing silently, and it is why the cycle-1 INPUT PROBE mattered.

CYCLE 3 reasoning_checkpoint (retained for history):
  hypothesis: >
    The router's emptiness test is TOO WEAK to survive a correctly-enveloped empty input.
    DERIVED FROM DEVICE EVIDENCE, not assumed: on a manual tap (no Shortcut Input at all),
    the normalisation chain now yields a NON-EMPTY Input Key that equals neither OPEN nor
    CLOSE. Proof is a two-point differential, both points observed on device:
      pre-fix  -> cond 100 "Input Key has any value" evaluated FALSE (manual menu shown)
      post-fix -> cond 100 evaluated TRUE (action 1349's unrecognised-input arm is
                  reachable ONLY when cond 100 passes AND neither literal matches)
    The ONLY difference in the 84->87 chain between those two builds is that actions 85
    (Trim Whitespace) and 86 (Change Case) gained WFTextTokenString envelopes. Therefore
    Uppercase(Trim(Text)) is non-empty when the Shortcut Input token is empty.
    The EXACT identity of that value (call it X) is NOT determinable statically and I do
    not claim it. Two live candidates, both consistent with every observation:
      (i)  the literal U+FFFC placeholder survives unresolved-token substitution, so X is
           a one-character non-printing string (the coordinator's hypothesis)
      (ii) an unresolved ExtensionInput renders as some other non-empty text
    BOTH candidates yield the identical actionable conclusion, which is why the fix does
    not depend on resolving them: routing on ABSENCE is unsafe, routing on PRESENCE is not.
  confirming_evidence:
    - "Structural: action 1349 sits in the Otherwise of A2F7 (CLOSE), nested inside FA04-otherwise (OPEN), nested inside F646 (cond 100). Reaching its alert REQUIRES cond 100 to have passed. The user saw exactly that alert's verbatim text."
    - "Differential: the 84->87 chain differs between the two device builds in exactly two actions (85 WFInput, 86 text), both bare-attachment -> WFTextTokenString. Action 84 was ALREADY WFTextTokenString in BOTH builds, so 84 is not the variable that changed."
    - "cond-100 semantics ELIMINATED as the cause: pre-fix, actions 85/86 still emitted an output ITEM whose text was empty, and cond 100 evaluated FALSE on it. So cond 100 tests string emptiness, not item existence. The coordinator's third alternative is ruled out by the project's own prior device data."
    - "U+FFFC is Unicode category So (OBJECT REPLACEMENT CHARACTER), not Zs/Zl/Zp and not whitespace. A Trim Whitespace step would NOT strip it. The coordinator's stated falsification test ('if Trim already strips it, this hypothesis is WRONG') therefore does not fire — candidate (i) survives it. Supporting, not decisive: iOS Trim semantics are not executable on the build Mac."
    - "Nesting-depth check on the proposed restructure: current max control-flow depth is 12, restructured is 11. The fix REDUCES maximum nesting rather than deepening it."
  falsification_test: >
    Device step 1 (manual tap). The build shows a ROUTER TRACE alert as the first thing on
    the manual arm, printing the normalised Input Key in brackets beside a literal
    empty-string reference on the next line. (The trace contains no conditional: an earlier
    draft tested cond 100 here, but that conditional was byte-identical to the router gate
    being removed and broke both the recurrence guard and generator idempotency. The
    cond-100 verdict is not needed — cycle 2 already established on device that it passes.)
    (a) If the "Unrecognised Input" alert still appears -> the restructure did not take
        effect on the device; hypothesis wrong about where that branch lives.
    (b) If the menu appears with NO trace alert first -> the trace was not reached, so the
        manual arm is not being entered the way this model predicts.
    (c) If the two bracket lines render DIFFERENTLY -> Input Key holds visible text, so
        candidate (ii) holds and candidate (i) (lone U+FFFC) is refuted.
    Expected under the hypothesis: the trace appears, its two bracket lines look identical
    (a present-but-non-printing value, i.e. candidate i), and the manual menu follows.
    Either way the router fix stands, because it does not depend on which candidate is true.
  fix_rationale: >
    Route on POSITIVE identification instead of on absence. The outer "Input Key has any
    value" gate is deleted; MANUAL becomes the Otherwise-of-Otherwise, so the router reads
    "is it OPEN? else is it CLOSE? else this is a manual run". This is correct for EVERY
    possible value of X without needing to know X, which is the whole point: cycle 2 failed
    precisely because it changed what X is while leaving a test that depended on X being
    exactly empty. It addresses the root cause (the router trusted absence as its manual
    signal) rather than the symptom (this particular non-empty value).
    It preserves the automation path unchanged: OPEN still matches literal OPEN at the same
    conditional with the same cond-4 test, CLOSE likewise. Nothing on the OPEN/CLOSE arms
    is touched; those arms simply become one level shallower.
    The envelope fix is NOT reverted, per the coordinator's instruction and on its own
    merits: the 367-site diagnosis and its internal control group still stand, and the old
    emptiness was empty-by-accident.
  blind_spots:
    - "X's identity is unresolved and deliberately so. The fix is designed to be correct either way, but the ROUTER TRACE is included specifically to measure X on this round-trip so the question stops being open."
    - "Losing the unrecognised-input fail-safe: a mis-typed automation now shows the manual menu instead of an explicit rejection. Accepted deliberately — the menu is inert until the user chooses, so the safety property ('a stray caller injects no phantom event into Heat/Pressure') is preserved; only the diagnostic distinction is lost. Recorded as a design deviation."
    - "SYMPTOMS 1 AND 3 REMAIN UNMEASURED from cycle 2. Nothing in this cycle observes them. The cycle-2 envelope fix's effect on them is still entirely unknown, and this build is the first that can even reach them."
    - "The trace alert adds one tap to every manual run. It is scaffolding behind a ROUTER_TRACE flag, alongside the BUILD_STAMP debt."
    - "Whether iOS Trim Whitespace strips U+FFFC is asserted from Unicode properties, not observed. Irrelevant to the fix's correctness, relevant only to interpreting the trace."
  candidate_causes:
    - "code/generator ROUTER: manual invocation is detected by absence-of-input rather than by non-match, so it breaks whenever the empty case stops being byte-empty (PRIMARY, this cycle's fix)"
    - "code/generator ENVELOPE: the cycle-2 WFTextTokenString conversion changed what an empty Shortcut Input resolves to (CONTRIBUTING, retained deliberately, not reverted)"
    - "environment/iOS runtime: unresolved-token substitution semantics for U+FFFC in a WFTextTokenString (UNRESOLVED — now instrumented rather than guessed)"
    - "data/input: the automation wrapper's Run Shortcut Input field (untouched this cycle; step 2 still tests it)"
  and_gate: >
    yes, and this is the third consecutive cycle where a single-cause reading was wrong.
    The cycle-2 regression required BOTH conditions simultaneously: the envelope change
    (which made the empty case non-empty) AND the router's absence-based manual test (which
    could only tolerate a byte-empty value). Neither alone produces the observed failure —
    the envelope change is harmless under positive-match routing, and the weak router was
    harmless while the chain happened to evaporate. Fixing only the envelope, or only
    reverting it, would leave the pair intact.

CYCLE 2 reasoning_checkpoint (retained for history):
  hypothesis: >
    ONE systemic defect explains all three symptoms. The generator serializes every
    variable / action-output reference as `WFTextTokenAttachment`. That is correct only
    for parameters iOS types as a content item (WFInput on Set Variable, WFDictionary on
    Set Dictionary Value, File, Placemark, float...). For parameters iOS types as a plain
    string, the value must be a `WFTextTokenString` — a "￼" placeholder plus
    attachmentsByRange. A bare attachment in a string-typed parameter imports cleanly,
    validates cleanly, and resolves to EMPTY at run time.
    -> symptom 2: setvalueforkey.WFDictionaryValue (catalog type `str`) held a bare
       attachment, so the Value field was empty and iOS raised "No value was provided to
       the Set Dictionary Value action for the key sequence".
    -> symptom 1: text.trimwhitespace.WFInput and text.changecase.text (both `str`) held
       bare attachments, so the OPEN/CLOSE normalisation chain evaporated between
       action 84 and action 87, Input Key was empty, and routing took the MANUAL arm.
    -> symptom 3: the Control Room refresh chain (actions 3623-3639+) reads each snapshot
       field through gettext.WFTextActionText (`str`) carrying a bare attachment, so every
       Snapshot* variable was empty and the refresh appended a contentless block.
    Cycle 1 renamed the parameter KEY correctly but never examined the VALUE ENVELOPE,
    which is exactly why the key fix was necessary but not sufficient.
  confirming_evidence:
    - "ToolKit v78 catalog TYPES (not just key names): setvalueforkey.WFDictionaryValue is typePythonName `str`, while WFDictionary/WFInput are `com_apple_shortcuts_wfcontent_item`. Cycle 1 compared key names only."
    - "Golden corpus is unanimous where it has data: gettext.WFTextActionText is WFTextTokenString in 36/36 real actions and WFTextTokenAttachment in 0. text.match.text 8/8, text.replace.WFInput 3/3, alert.WFAlertActionMessage 8/8 — all WFTextTokenString."
    - "INTERNAL CONTROL GROUP (the decisive evidence): within the same artifact, every path the user reported as WORKING uses WFTextTokenString on its string parameter — state.json template (action 75), Shortcut Input read (action 84), Control Room body (action 3615). Every path the user reported as FAILING used a bare attachment — actions 85/86 (Input Key), 1405 (key `sequence`), 3624+ (Note refresh). Perfect separation, same build, same device, same run."
    - "Execution-order proof that the working state.json does NOT contradict the hypothesis: zero setvalueforkey actions exist before the routing gate at action 84. state.json is written at action 79 from the action-75 WFTextTokenString template. Actions 151/153 sit inside the OPEN branch and never executed, because Input Key was empty."
    - "BEST_PRACTICES.md and VARIABLES.md both document the mechanism as runtime-verified: a bare WFTextTokenAttachment in a string-typed/display parameter renders default/empty at run time while importing and validating fine."
  falsification_test: >
    Run the rebuilt artifact on device after confirming the build stamp.
    (a) If Change Sequence -> Classic still raises "No value provided" for key `sequence`,
        the envelope hypothesis is wrong for symptom 2.
    (b) If opening a configured target app still shows the manual menu (bearing the NEW
        stamp), the envelope hypothesis is wrong for symptom 1.
    The build stamp is what makes these tests meaningful: without it a stale install is
    indistinguishable from a failed fix, which is the confound that made cycle 1's two
    "refutations" uninterpretable.
  fix_rationale: >
    The converter re-wraps the same token payload, unchanged, inside the "￼" +
    attachmentsByRange form that iOS reads for string-typed parameters. It restores the
    field iOS actually reads rather than masking a symptom, and it is applied from a
    catalog-and-corpus-derived allowlist rather than blanket-applied.
  blind_spots:
    - "SETTLED FOR THIS CYCLE, NOT PROVEN: no golden-corpus instance of setvalueforkey exists anywhere in the 19-shortcut corpus, so WFDictionaryValue's envelope is inferred from its `str` catalog type plus the unanimous behaviour of every other `str` parameter. It is the single weakest link and is exactly what device step 2 tests."
    - "Symptom 3 may not be fully explained. The note-creation chain (3615/3617/3618) is byte-identical to the 2026-08-13 build in which the Note was confirmed created successfully, so the empty Note is NOT a cycle-1 regression. The envelope fix repairs the refresh block that appends snapshot content, but if the note body itself is empty on a fresh create, a second cause remains."
    - "openurl.WFInput (4 sites) is catalog-typed `str` but the golden corpus uses a bare attachment 2/2, so it was deliberately left alone. Recorded as a knowing deviation; corpus evidence outranks catalog inference."
    - "The 2026-08-13 report named Test a Circle while the only `sequence` setters live in Change Sequence. Day-old recall; unresolved, and it does not change the fix since the defect affected all 147 setters."
  candidate_causes:
    - "code/generator: string-typed parameters carry a bare WFTextTokenAttachment (PRIMARY, this cycle's fix)"
    - "environment/device: stale duplicate install left the automation wrapper pointed at the pre-fix shortcut (UNRULED-OUT — now discriminated by the build stamp)"
    - "config/plist root: WFWorkflowHasShortcutInputVariables (ELIMINATED as sufficient by the 2026-08-14 device test; kept because it matches every modern golden shortcut)"
    - "data/Notes: note body or create-vs-reuse branch selection (symptom 3, partially open)"
  and_gate: >
    yes, and this is the crux of cycle 1's failure. Reaching Circle 1 requires BOTH a
    populated Input Key AND a working setter chain. Cycle 1 fixed one contributing
    condition (the parameter key) while a second (the value envelope) remained, so the
    user-visible outcome did not move at all and the fix read as a total refutation. A
    single-condition reading of this failure was wrong both times.

superseded_next_action_cycle2_checkpoint: >
  (ANSWERED 2026-08-14 — build "c" round-trip. Outcome: manual-invocation REGRESSION,
  symptoms 1 and 3 unmeasured. Superseded by the cycle-4 next_action at the top of
  Current Focus. Retained for history only — DO NOT ACT ON THIS.)
  CHECKPOINT — awaiting the device round-trip. The rebuilt, re-signed artifacts carry the
  visible stamp "PROSOCHĒ · build 2026-08-14c" in the manual menu prompt.

--- cycle-1 reasoning_checkpoint, retained for history (both hypotheses refuted on device) ---
reasoning_checkpoint:
  hypothesis: >
    SYMPTOM 2 (confirmed): every `is.workflow.actions.setvalueforkey` emitted by the
    generator supplies the value under `WFInput`, but the action's Value parameter is
    `WFDictionaryValue`. iOS ignores the unknown key, so the Value field is empty and
    Shortcuts raises "No value was provided to the Set Dictionary Value action for the
    key <WFDictionaryKey>".
    SYMPTOM 1 (unconfirmed): the master shortcut consumes Shortcut Input via the
    `ExtensionInput` token but the root plist omits `WFWorkflowHasShortcutInputVariables`,
    so the Shortcut Input variable is not provisioned at run time, `Input Key` resolves
    empty, and routing takes the documented empty-input arm to MANUAL.
  confirming_evidence:
    - "ToolKit v78 first-party parameter catalog: is.workflow.actions.setvalueforkey has exactly {WFDictionaryKey, WFDictionaryValue, WFDictionary}. No WFInput."
    - "All 147 setters in both forks emit WFInput and none emit WFDictionaryValue."
    - "Catalog displayName confirms setvalueforkey = 'Set Dictionary Value' and getvalueforkey = 'Get Dictionary Value', so the reported action is unambiguously the setter."
    - "Router ancestry proves the MANUAL menu sits in the Otherwise arm of the 'Input Key has any value' conditional, so the observed menu means Input Key was empty."
    - "Golden shortcut 51cc4e26 matches our Shortcut-Input pattern exactly (WFStringContentItem + gettext/WFTextTokenString/ExtensionInput) and differs from ours in exactly one root key: WFWorkflowHasShortcutInputVariables = true."
  falsification_test: >
    Symptom 2: if a rebuilt artifact using WFDictionaryValue still raises "No value
    provided" on a Set Dictionary Value, the hypothesis is wrong.
    Symptom 1: if an on-device probe shortcut receives "OPEN" from the same wrapper via
    Run Shortcut while the imported PROSOCHE still falls through to MANUAL, the defect is
    inside the imported plist (supports the hypothesis). If the probe ALSO receives
    nothing, the wrapper is at fault and the hypothesis is refuted.
  fix_rationale: >
    Renaming the value parameter to the catalog-verified key restores the Value field that
    Shortcuts actually reads — this is the mechanism, not a symptom workaround. Setting
    the documented root key declares that the shortcut uses input variables.
  blind_spots:
    - "The reported key was 'sequence', but no setter with key 'sequence' is reachable inside the Test-a-Circle case (only inside Change Sequence). The defect class is proven; the exact menu path the user took is unresolved and must be confirmed on device."
    - "WFWorkflowHasShortcutInputVariables is documented in PLIST_FORMAT.md but its runtime effect is not verifiable on the build Mac."
  candidate_causes:
    - "code/generator: wrong parameter key on setvalueforkey (CONFIRMED)"
    - "config/plist root: missing WFWorkflowHasShortcutInputVariables (UNDER TEST)"
    - "environment/device: wrapper's Run Shortcut Input field not actually wired (UNDER TEST via probe)"
  and_gate: >
    yes for symptom 1 — reaching Circle 1 needs BOTH a populated Shortcut Input AND a
    working setter chain, because the OPEN pipeline writes opens_today via
    Set Dictionary Value before it can reach the Circle dispatch. The two defects are
    independent but both gate the same user-visible outcome.

next_action: >
  CHECKPOINT — awaiting the cycle-8 device sitting. A FIX IS SHIPPED this cycle (the first since
  cycle 5), and the root cause is CONFIRMED, not ranked.
  ROOT CAUSE: conditional WFInput.Variable held a WFTextTokenString TEXT TEMPLATE where a
  WFTextTokenAttachment VARIABLE DESCRIPTOR is required. 25 sites; the first two are actions
  149/158, inside span B->C, two actions after the breadcrumb the user last saw.
  FIX: deleted the 13 generator lines that overwrote if_block()'s already-correct WFInput with
  token(name). Verified programmatically that all 13 passed the SAME variable name, so the
  deletion changes only the envelope. Added verify_conditional_inputs() as a build-failing
  recurrence guard, wired into BOTH fork builders.
  ARTIFACTS: artifacts/shortcuts/"PROSOCHĒ — Nine Circles — Dumb.shortcut" (AEA1, 188480 bytes,
  3684 actions) and Sentient (AEA1, 192095 bytes, 3752 actions). Stamp "build 2026-08-14h"
  verified INSIDE both signed files by decryption; "14g" verified absent. 307/317 conditional
  inputs correct, 0 defective, confirmed in the DECRYPTED SIGNED artifacts. Both validate at
  --target-macos 26 --target-platform all; plutil -lint OK.
  PROTOCOL: artifacts/device-import-probes/TESTING-cycle8.md. Step 0 (delete, import, RE-POINT
  the automation's Run Shortcut) remains unskippable. Step 1: menu prompt must read
  "build 2026-08-14h".
  BREADCRUMBS DELIBERATELY RETAINED. Rationale, stated so the next cycle does not re-litigate
  it: under a multi-defect world a retained instrument turns "same error again" into "a LATER
  letter", i.e. progress plus localisation in the same sitting, instead of a result that reads
  as this fix having failed — the exact failure mode that made cycle 1's correct fix look like a
  refutation. Strip with OPEN_BISECT = False once the OPEN path completes end to end.
  READING THE RESULT:
    last letter C or later -> span B->C CLEARED, fix correct, remaining failure is a DIFFERENT
      and later defect; localise from the new letter.
    all ten + the Leaving/Continue menu -> OPEN pipeline complete for the first time ever.
    last letter B again -> HYPOTHESIS REFUTED. Re-examine the other 18 actions in the span
      INDIVIDUALLY rather than by class; class-level device clearance would then be the wrong
      standard and that is the lesson to record.
  DELIBERATELY UNCHANGED, AND NOT CLAIMED CORRECT — the 14 WFConditionalActionString = token()
  sites (generator lines 398/682/712 pre-edit). Same family, but the WFInput evidence does NOT
  transfer: WFInput.Variable is a variable slot whereas WFConditionalActionString is a TEXT slot
  that legitimately accepts mixed literal+variable content. Corpus coverage zero (all corpus
  conditional operands are literals), catalog coverage zero (is.workflow.actions.conditional is
  absent from the ToolKit catalog entirely), device coverage zero. All 14 sit past breadcrumb J
  so they cannot confound this sitting. DONOR 4 IS REQUESTED in TESTING-cycle8.md as an optional
  parallel task at zero device-testing cost; it settles them outright.
  LATENT, NOT THIS BUG, AND NOW WEAKER THAN CYCLE 7 RANKED THEM: the two <integer> sites at
  418/454. Left UNCHANGED. Cycle 7 inferred that because iOS never WRITES <integer>, <integer>
  must be undecodable; that inference is refuted by our own <integer> WFNumberActionNumber at
  action 1359, which has executed on device. Keeping them unchanged also keeps spans G and H
  interpretable if the next run reaches them.
  RECURRENCE GUARD ADDED: verify_conditional_inputs(). MUTATION-TESTED — re-introducing the exact
  defect at line 802 makes the build exit non-zero and names "action 149: WFInput.Variable is
  'WFTextTokenString', expected WFTextTokenAttachment". The generator now asserts KEY, ENVELOPE,
  PICKER LITERAL and VARIABLE-SLOT shape. A verify_scalar_types() pass remains UNBUILT and is no
  longer clearly warranted — see the scalar-type evidence entry.
  PRESERVED BY CONSTRUCTION AND VERIFIED BY COMPARISON, not asserted: action counts unchanged
  (3684 / 3752); the ONLY differing actions between build g and build h are the 25 conditional
  WFInput envelopes plus TWO display-only build-stamp strings. All 147 setvalueforkey still carry
  WFDictionaryValue (symptom 2); WFCreateNoteInput and both appendnote.text still carry
  WFTextTokenString (symptom 3). Every internal UUID is unchanged.
  REPO HAZARD — CHECK BEFORE ANY REBUILD: HEAD must be codex/automation-parameter-diagnosis.
  A rebuild on codex/prosochedebug1 or codex/round1 emits a pre-cycle-1 artifact and all three
  symptoms return looking like a regression.
  HOUSEKEEPING, non-urgent and untouched: the DEV-03 collision in docs/BUILD-NOTES.md;
  correcting .claude/CLAUDE.md §8's claim that signed artifacts cannot be decrypted; stripping
  BUILD_STAMP / ROUTER_TRACE / OPEN_BISECT before ship.

superseded_next_action_cycle7_checkpoint: >
  CHECKPOINT — awaiting the cycle-7 device sitting. (ANSWERED: last letter "B" — localised to
  span B->C.) NO FIX WAS SHIPPED; this cycle shipped a MEASUREMENT. Protocol: artifacts/device-import-probes/TESTING-cycle7.md.
  ARTIFACT: artifacts/shortcuts/"PROSOCHĒ — Nine Circles — Dumb.shortcut", AEA1, 188667 bytes,
  3684 actions, stamp "build 2026-08-14g" verified INSIDE the signed file by decryption ("14f"
  verified absent). Sentient rebuilt/re-signed identically (192807 bytes). Both forks validate at
  --target-macos 26 --target-platform all; plutil -lint OK.
  STEP 0 IS UNSKIPPABLE: delete PROSOCHĒ, import build g, then RE-POINT the automation's Run
  Shortcut by fresh selection. Deleting orphans the target and would produce the SAME error for a
  wholly different reason, wasting the sitting.
  STEP 1: manual tap — the menu prompt must read "build 2026-08-14g", else the old copy is live.
  STEP 2: open a watched app; report the LAST of the ten breadcrumb letters A-J.
  READING THE RESULT (spans and nesting computed from the artifact, build-g indices):
    A@92  -> B@147  54 actions, flat            (state + config reads)
    B@147 -> C@168  20 actions, 2 blocks d2     (behavioural-day rollover)
    C@168 -> D@286 117 actions, 11 blocks d4    (cooldown: live-Ice menu + Ice-expiry restore)
    D@286 -> E@306  19 actions, 3 blocks d2     (duplicate-OPEN debounce)
    E@306 -> F@415 108 actions, 11 blocks d4    (whole ordered Heat pipeline)
    F@415 -> G@424   8 actions, flat            (opens-today math + 3 dictionary writes)
    G@424 -> H@458  33 actions, 1 block         <- CONTAINS number.random, SUSPECT 1
    H@458 -> I@473  14 actions, 2 blocks        <- CONTAINS repeat.count, SUSPECT 2
    I@473 -> J@527  53 actions, 3 blocks d3     (pending exit, 2 repeat-each loops)
    J@527 -> menu@531  3 actions, flat          (Save File only)
  A LAST LETTER OF C, E OR I DOES NOT LOCALISE TO AN ACTION — those three spans hold 278 of the
  429 measured actions and nest to depth 4. Ship a SECOND, finer bisection inside that span; do
  not attempt to reason the answer out statically, which has failed three times.
  A LAST LETTER OF G OR H CONFIRMS this cycle's ranked prediction (donor-derived scalar-type
  divergence). The follow-up fix is then SINGLE-VARIABLE: emit number.random's
  WFRandomNumberMinimum/Maximum as plist <string> (donor shape) or repeat.count's WFRepeatCount as
  plist <real> (donor shape) — ONE of them, not both, so the next result stays interpretable.
  Note the fix would still confirm only the SPAN, not the mechanism: Detect Dictionary, the Gravity
  conditional and the composite-key threshold lookup also live in those spans.
  NO LETTERS AT ALL would contradict cycle 6's probe result and reopens the router/PRE region.
  ALL TEN + the Leaving/Continue menu means the OPEN pipeline completed for the first time ever.
  RECURRENCE GUARD TO ADD once the axis is settled, independent of the outcome: the generator has
  invariants for parameter KEY, value ENVELOPE and picker LITERAL, but NONE for the plist TYPE of
  an emitted parameter. Six cycles of "exhaustive" sweeps never modelled it. Add a
  verify_scalar_types() pass keyed off the donor/corpus evidence.
  ALSO NOW SETTLED, no action needed: DEV-05 (math WFMathOperation omitted at the default
  operation is what iOS itself does — keep the omission). Donor 3 raw plist worth preserving:
  it is the only device serialization we hold for variable-backed conditionals, round,
  number.random and repeat.count.
  RETAINED, DO NOT REVERT: every cycle-2/3/4/5 fix. KEEP BUILD_STAMP, ROUTER_TRACE, OPEN_BISECT
  on until the OPEN path completes; strip OPEN_BISECT with OPEN_BISECT = False.
  REPO HAZARD — CHECK BEFORE ANY REBUILD: HEAD must be codex/automation-parameter-diagnosis.
  Verified this cycle at 7ca8ebb before regenerating. A rebuild on codex/prosochedebug1 or
  codex/round1 emits a pre-cycle-1 artifact and all three symptoms return looking like a regression.
  HOUSEKEEPING, non-urgent and untouched: the DEV-03 collision in docs/BUILD-NOTES.md (Use Model
  literal still open vs speaktext key now closed); correcting .claude/CLAUDE.md §8's claim that
  signed artifacts cannot be decrypted; stripping scaffolding before ship.

superseded_next_action_cycle7_entry: >
  CYCLE 7 — THE FAULT IS ISOLATED TO PROSOCHĒ'S OPEN PATH, actions 91-520, before the first
  OPEN menu. Cycle 6 closed the wrapper and stale-reference hypotheses affirmatively: the SAME
  wrapper succeeds against Probe 5 and fails against PROSOCHĒ. No device-side confound remains.
  TWO WORKSTREAMS, RUN IN PARALLEL, SHIPPED AS SEPARATE ARTIFACTS:
  (A) BISECTION — the primary instrument. Static reading is retired (three device-refuted
      confirmations, one exhausted region, and 336 control-flow actions no catalog sweep can
      evaluate). Ship flag-gated breadcrumb alerts at OPEN-arm base depth (91, ~200, ~300,
      ~400, ~470, 519) as a SIGNED artifact, same as Probe 5 — the user reads letters rather
      than judging state. TWO REQUIREMENTS:
        - Place breadcrumbs at OPEN-ARM BASE DEPTH so a breadcrumb cannot itself be skipped by
          a conditional that the failing action sits inside. If a span turns out to contain
          nested control flow, SAY SO and plan a second bisection round rather than claiming
          one pass localises to a single action.
        - The breadcrumb alert must NOT introduce a parameter shape being inferred. Use the
          alert shape already proven on device this session.
  (B) DONOR 3 ANALYSIS — already in hand at .planning/debug/"Donor 3.shortcut" (AEA1, 22907
      bytes, verified). Costs zero device time. Decrypt with the cycle-4 recipe. Settles:
      DEV-05 outright; the first device ground truth for variable-backed WFNumberValue (13
      sites, first at action 167, ON THE GUARANTEED PATH, zero corpus precedent anywhere);
      plus `round`, `number.random`, `repeat.count` shapes (all zero-corpus).
      If the donor diff reveals a defect at or before action 167, that is a CANDIDATE for the
      bisection to confirm — not a fix to ship blind.
  HARD SEPARATION: do NOT ship a donor-derived fix and the bisection build in the same
  artifact. The bisection is a MEASUREMENT and must not be confounded.
  PRESERVE BY CONSTRUCTION: symptoms 2 and 3 stay closed; keep the cycle-5 picker fixes and the
  scaffolding. Confirm the tree is on codex/automation-parameter-diagnosis before ANY rebuild —
  a rebuild on codex/prosochedebug1 or codex/round1 would silently emit a pre-cycle-1 artifact
  and all three symptoms would return looking like a regression.

superseded_next_action_cycle6_checkpoint: >
  CHECKPOINT — awaiting the cycle-6 device sitting. (ANSWERED: probe received [OPEN]; repoint
  still failed; Donor 3 delivered.) NO generator change was made this cycle, so
  both forks and both signed artifacts are byte-identical to build 2026-08-14f and symptoms 2
  and 3 remain exactly as device-confirmed. Nothing from cycles 2-5 is reverted.
  SHIPPED FOR TEST: artifacts/device-import-probes/"PROSOCHE Probe 5 - Input Echo.shortcut"
  (AEA1, 22953 bytes, decrypt-verified). Protocol written to
  artifacts/device-import-probes/TESTING-cycle6.md. Generator: build_probe5.py in the same dir.
  THE USER MUST NOT CLEAN-INSTALL OR RE-IMPORT PROSOCHĒ THIS SITTING. Step 1 already rewrites
  the wrapper's stored Run Shortcut reference; a reinstall on top of that destroys step 2's
  discriminating power.
  STEP 1 (probe): repoint the OPEN automation's Run Shortcut at Probe 5, open a watched app.
    RAW [OPEN] / NORMALISED [OPEN] -> handoff delivers input; defect is INSIDE PROSOCHĒ -> go to
      breadcrumb bisection (below), NOT another static sweep.
    RAW [] / NORMALISED []         -> handoff runs but delivers nothing.
    same error, NO alert           -> failure is AT/ABOVE the handoff; five cycles of plist-side
      theory were aimed at the wrong layer. Investigate the wrapper/trigger, not the generator.
  STEP 2 (repoint back, fresh selection from the list): tests whether the stored reference was
    STALE while the chip rendered from a cached name. Works now -> device-config root cause, and
    the guard belongs in the shipped setup copy, not the generator. Fails identically -> stale
    reference refuted on stored-representation evidence, defect is in the OPEN pipeline.
  STEP 3 (donor 3, only if step 1 showed [OPEN]): user builds a shortcut in Shortcuts.app with a
    variable-vs-VARIABLE numeric If, a default-operation Calculate, a Round, a Random Number and
    a literal-count Repeat, then exports it. Decrypting it gives iOS's own serialization for the
    five constructs with zero corpus coverage. Same technique that cracked symptom 3.
  IF THE DEFECT IS INSIDE PROSOCHĒ, THE NEXT INSTRUMENT IS BISECTION, NOT READING. Flag-gated
    breadcrumb alerts at OPEN-arm base depth (91, ~200, ~300, ~400, ~470, 519); the last letter
    the user sees localises the failing action to a span of tens in ONE round-trip. Static
    reading has now produced three device-refuted confirmations and one exhausted region.
  CANDIDATE FIX SITES, ranked, all UNVERIFIABLE on the build Mac and none to be shipped on static
    evidence alone: conditional WFNumberValue holding a variable (13 sites, first at 167, zero
    corpus coverage); round (zero corpus instances, action 316); number.random (zero corpus
    instances, action 418); math with WFMathOperation omitted for '+' (DEV-05, corpus 1-of-2 —
    weaker than cycle 5 recorded, but still corpus-supported, so unchanged).
  CHEAP GUARD IMPROVEMENT, independent of the outcome: extend verify_required_pickers() to
    validate each literal against the catalog's enum CASE list, not just presence + literalness.
    Cycle 6 ran that check by hand and it passed, so it is a recurrence guard rather than a fix.
  REPO HAZARD — CHECK BEFORE ANY REBUILD: the tree was found at efb5a79 (branch
    codex/prosochedebug1) at session start, which predates ALL cycle 1-5 work. It is now on
    codex/automation-parameter-diagnosis at 7ca8ebb, which is correct. Confirm HEAD and that
    BUILD_STAMP reads "build 2026-08-14f" before regenerating anything.
  RETAINED, DO NOT REVERT: all cycle-2/3/4/5 fixes. KEEP BUILD_STAMP and ROUTER_TRACE ON.
  Carried, NOT for this agent to act on unilaterally: correcting .claude/CLAUDE.md §8's claim
    that signed artifacts cannot be decrypted; stripping scaffolding before ship.
  HOUSEKEEPING, non-urgent and untouched this cycle: the DEV-03 collision in docs/BUILD-NOTES.md
    (Use Model literal, still open, vs speaktext key, now closed). DEV-05 stays open.

superseded_next_action_cycle6_entry: >
  CYCLE 6 — SYMPTOM 1 IS THE SOLE REMAINING OPEN ITEM. Symptoms 2 and 3 are CLOSED and
  verified; do not disturb them.
  THE INPUT PROBE GOES FIRST. It has now been deferred for FIVE cycles and it is the decisive
  experiment: every remaining hypothesis branches on its one bit. Design it and put it first;
  do NOT defer it again behind another static pass. Run any static re-sweep in PARALLEL, not
  instead.
    Probe: a trivial one-action shortcut receiving the wrapper's input.
      Shows OPEN  -> handoff works, defect is INSIDE PROSOCHĒ -> pursue (1)/(2) below.
      Shows nothing / errors -> failure is AT OR BEFORE the handoff -> pursue (3).
  CONTRADICTION TO RESOLVE: the cycle-5 sweep says actions 91-521 are clean; the device says
  something at or before that region has an unfilled required parameter. Both cannot be true.
  Candidate resolutions, ranked — ESTABLISH, do not assume:
  (1) A FOURTH required-parameter axis the sweep does not model. Three have been found this
      session (key name, value envelope, picker enum) and EACH was invisible to the previous
      sweep's criteria — a fourth is the base-rate-likely answer. Enumerate what "required
      parameter" can mean in the catalog beyond those three: required content-item inputs,
      required entity/app references, required quantity fields with WFQuantityFieldValue
      shape, anything carrying a non-optional flag. Re-sweep 91-521 against the FULL set.
  (2) A parameter STRUCTURALLY PRESENT but resolving UNSET at run time. iOS may report an
      action as lacking a value when its parameter holds a token that resolves to nothing on
      the OPEN path specifically. Invisible to any purely structural sweep — which is exactly
      how 91-521 can be "clean" and still fail. The manual path exercises different data,
      which would explain why it survives.
  (3) The failing action is NOT inside PROSOCHĒ at all. The orphaned-reference theory is
      refuted and the wrapper screenshot shows both actions bound, BUT "no PROSOCHĒ UI
      appears" is equally consistent with failure at the Run Shortcut HANDOFF itself, before
      PROSOCHĒ's first action executes. Do not treat this as excluded merely because the
      wrapper renders correctly.
  ALSO WEIGH: bisection. If the probe proves input arrives, a cut-down harness containing only
  PROSOCHĒ's actions 91-N on the OPEN path would localise the failing action far faster than a
  fourth exhaustive read — decryption and rebuilding are both cheap now.
  RETAINED, DO NOT REVERT: the cycle-5 picker fixes (corpus-verified 11/11 and 33/33, genuine
  latent defects on a path that will execute once this is unblocked).
  HOUSEKEEPING, non-urgent: disambiguate the DEV-03 collision in docs/BUILD-NOTES.md (Use
  Model literal, still open, vs speaktext key, now closed). DEV-05 stays open, correctly.

superseded_next_action_cycle5_checkpoint: >
  CHECKPOINT — awaiting the cycle-5 device round-trip. (ANSWERED: no PROSOCHĒ UI appeared at
  all; picker fixes refuted as the cause of symptom 1.) Stamp "build 2026-08-14f" (VERIFIED
  PRESENT INSIDE THE SIGNED FILE by
  decryption, and "14e" verified absent). Symptoms 2 and 3 remain CLOSED; symptom 1 is the
  only open one.
  ONE TEST, TWO BITS OF INFORMATION. Clean install, then open a configured target app.
  BIT 1, READ IT FIRST AND REPORT IT EVEN IF THE RUN STILL FAILS: did ANY PROSOCHĒ UI appear
    before the failure — specifically a menu prompted "PROSOCHĒ" offering "Leaving" and
    "Continue"? This bit was never captured in cycles 3 or 4 and it partitions the remaining
    space cleanly, because the OPEN region BEFORE that menu was swept exhaustively this cycle
    and is statically CLEAN:
      menu appeared  -> execution reached action 521, so both fixed defects were live and the
                        fix is on the right path
      nothing at all -> the failure is UPSTREAM of action 521, where no parameter defect
                        exists, so the cause is NOT a picker parameter and the INPUT PROBE
                        (designed in cycle 1, still never executed) becomes the next move
  BIT 2: does the intervention now complete without "please choose a value"?
  DO NOT ASK THE USER WHICH ACTION iOS OBJECTS TO. Established this cycle: iOS does not expose
  it. The automation-failure notification carries the automation's name and the message only —
  no action index, no drill-down, no log.
  KEEP BUILD_STAMP and ROUTER_TRACE ON.
  Carried open, NOT for this agent to act on unilaterally: correcting .claude/CLAUDE.md §8's
  claim that signed artifacts cannot be decrypted (BUILD-NOTES §14 disproves it); stripping the
  scaffolding constants before ship.
  DEV-03 is now CLOSED (speaktext WFText, catalog-verified). DEV-04 confirmed NOT needed.
  New recorded deviations: DEV-05 (math.WFMathOperation deliberately untouched, corpus-refuted)
  and DEV-06 (openapp/count redundant keys retained).

superseded_next_action_cycle5_entry: >
  CYCLE 5 — SYMPTOM 1 IS THE ONLY REMAINING OPEN SYMPTOM. Symptoms 2 and 3 are CLOSED
  (device-confirmed cycles 3 and 4). The orphaned-Run-Shortcut-reference theory is REFUTED.
  THE WRAPPER IS NOW VERIFIED CORRECT BY SCREENSHOT (two actions, both parameters bound), so
  the search space has INVERTED: the failing action almost certainly lives INSIDE PROSOCHĒ on
  the OPEN pipeline, with iOS attributing the failure to the outermost automation by name.
  (1) PRIORITY — STATIC ENUMERATION, no device round-trip needed. Do this FIRST; it may make
      the INPUT PROBE unnecessary. Enumerate every action reachable on the OPEN branch but NOT
      on the MANUAL branch, and check each one's REQUIRED parameters against the ToolKit
      catalog for an unset or missing value. The manual path is now well exercised and works,
      so the defect is confined to OPEN-only actions.
      Specific leads: this session has already found TWO defect classes of exactly this kind —
      wrong key name (WFInput vs WFDictionaryValue) and wrong value envelope
      (WFTextTokenAttachment where WFTextTokenString/AttributedString was required). The
      AttributedString case proved the converter's allowlist was scoped too narrowly BY
      CATALOG TYPE. Check whether a THIRD type bucket on the OPEN-only path was missed by the
      same allowlist logic. Also re-check speaktext (recorded as DEV-03, keys unverified, no
      catalog parameters) — if it sits on the OPEN path, an unset required parameter there
      would produce precisely this error.
      Verify against the SHIPPED artifact too, not just the generated source — signed
      .shortcut decryption is proven and available.
  (2) FALLBACK ONLY — keep the INPUT PROBE ready if the static pass comes up empty. It would
      then discriminate whether the input reaches PROSOCHĒ at all. Design it for unambiguous
      pass/fail without the user judging a UI field.
  (3) State plainly for the user whether iOS exposes WHICH nested action it is objecting to.
      If it does not, say so rather than implying they can find out by inspecting further.
  KEEP BUILD_STAMP and ROUTER_TRACE ON.
  Carried open, NOT for this agent to act on unilaterally: correcting .claude/CLAUDE.md §8's
  claim that signed artifacts cannot be decrypted; stripping the scaffolding constants before
  ship. Both surfaced to the user by the coordinator.
  Still open: DEV-03 (speaktext key unverified). DEV-04 confirmed NOT needed for correctness.

superseded_next_action_cycle4_checkpoint: >
  CHECKPOINT — awaiting the cycle-4 device round-trip. Artifacts staged and signed at
  artifacts/shortcuts/, stamp "build 2026-08-14e" (verified present inside the SIGNED file,
  not just the source). Two independent experiments in one pass:
  (A) SYMPTOM 3, plist-side. Note body + Control Room refresh. The refresh append (action
      3648) changed on the ENVELOPE AXIS ONLY and is the clean single-variable test; the
      create path (3616) changed on two axes and cannot discriminate alone. Read the append
      result FIRST — if the "## CURRENT SETTINGS" block is missing, the AttributedString
      hypothesis is refuted and the body result is uninterpretable.
  (B) SYMPTOM 1, device-side. REPAIR THE AUTOMATION WRAPPER, do not rebuild it: open the
      existing "When any of 3 apps are opened" automation and check the Run Shortcut action's
      SHORTCUT field first — deleting the shortcut for each clean install orphans that
      reference, and an unset target produces the exact observed error. Screenshot requested.
      Design answer, settled this cycle and not to be re-litigated: ONE automation covering
      all watched apps is CORRECT (the shortcut consumes zero app identity; ARCHITECTURE.md
      §5 makes Heat/Gravity/Pressure/Circle/active_session global). OPEN and CLOSE must stay
      as two separate automations because they pass different literals.
  IF (A) PASSES AND (B) STILL FAILS AFTER REPAIR: symptom 1 returns to the plist with, for
  the first time, a wrapper whose health has been positively verified — at which point run
  the cycle-1 INPUT PROBE that has still never been executed.
  KEEP BUILD_STAMP and ROUTER_TRACE ON. DEV-03 (speaktext key) remains open and untouched.
  CLOSED SO FAR: symptom 2 (device-confirmed), the cycle-2 manual-invocation regression,
  DEV-01, and the "one shared automation" design question.

superseded_next_action_cycle4_entry: >
  CYCLE 4 — two workstreams, both in ONE pass so the next device test covers both.
  (1) PRIORITY, plist-side and statically tractable: SYMPTOM 3, the Control Room note-body
      write. Now cleanly isolated — the note is CREATED but its BODY is empty, and the
      envelope defect is EXCLUDED BY DIRECT EVIDENCE (same build, same run, symptom 2 passed).
      Investigate the note-body write specifically: is the body parameter content-item typed
      or string typed, and do BOTH its parameter key and its value envelope match the catalog?
      Known live candidate from the earlier whole-plist audit:
      com.apple.mobilenotes.SharingExtension emits WFCreateNoteInput where the catalog defines
      name/contents. .claude/CLAUDE.md flagged Notes actions as catalog-gated to macOS 27 with
      an explicit "verify empirically on device" — that flag is now cashing in.
  (2) CHEAP, unblocks the user in parallel: SYMPTOM 1 is no longer a plist question this
      cycle. Produce precise, unambiguous instructions for the user to INSPECT AND REPAIR the
      Personal Automation wrapper — action by action, which action, which field, what it must
      contain. Must cover: the Run Shortcut action's target Shortcut field, and that its Input
      field must carry the Text action's magic variable; that a Run Shortcut with NO target
      shortcut selected produces exactly the observed error; and whether one shared automation
      covering "any of 3 apps" is correct for PROSOCHĒ's design or whether it must be split
      per-app. If a screenshot would settle it faster than prose, ask for one.
  KEEP BUILD_STAMP and ROUTER_TRACE ON — still iterating.
  CLOSED SO FAR: symptom 2 (device-confirmed), the cycle-2 manual-invocation regression,
  and DEV-01 (--target-platform ios deviation recorded in docs/BUILD-NOTES.md §13).

superseded_next_action_cycle3_checkpoint: >
  CHECKPOINT — awaiting the cycle-3 device round-trip. Artifacts staged, stamp
  "build 2026-08-14d", ROUTER TRACE alert prints normalised Input Key beside an empty
  reference. (Answered 2026-08-14: manual invocation restored, symptom 2 fixed, symptom 1
  moved off-plist to the automation wrapper, symptom 3 persists.)

superseded_next_action_cycle3_entry: >
  CYCLE 3 — the cycle-2 envelope fix REGRESSED the manual-invocation path. Restoring manual
  invocation is the TOP priority: it is the gate on measuring symptoms 1 and 3, and every
  remaining test route runs through it.
  COORDINATOR HYPOTHESIS (proposed, NOT established — verify before adopting): a
  WFTextTokenString carries a literal U+FFFC placeholder in its string body with
  attachmentsByRange mapping that offset to the token. When the referenced token resolves to
  nothing — exactly the manual-tap / no-Shortcut-Input case — does Shortcuts substitute empty,
  or leave the placeholder standing as literal text? If the placeholder survives, Input Key
  becomes a 1-character non-empty string, "has any value" (cond 100) PASSES, neither OPEN nor
  CLOSE matches, and action 1349 emits exactly the observed message. The old bare
  WFTextTokenAttachment form had no placeholder character and so degraded to genuinely empty,
  which is why the previous build fell through to the manual menu.
  MUST RULE IN OR OUT EXPLICITLY: is the Trim step even reached, and does Trim on a lone
  U+FFFC yield empty or the character unchanged? If Trim already strips it, this hypothesis is
  WRONG and the cause is elsewhere. Verify against the bundled Shortcuts Playground reference
  rather than assuming U+FFFC behaviour.
  IF CONFIRMED, this is NOT an argument for reverting the envelope fix — the 367-site
  diagnosis and its control-group evidence still stand, and the old behaviour was
  empty-by-accident. It means the router's emptiness test is too weak to survive a correctly
  enveloped empty input and must treat a lone-placeholder / whitespace-only value as empty.
  Fix at the ROUTER, in the generator — not by reverting envelopes.
  Then re-run the full three-step device test in ONE pass.
  Still open: record the `--target-platform ios` deviation (rejects 3675/3675 including
  is.workflow.actions.comment) against the mandated invocation in .claude/CLAUDE.md.
  DEBT: decide whether the "· build 2026-08-14c" menu-title stamp ships or gets stripped.

superseded_next_action_cycle2: >
  AWAITING DEVICE (cycle 2 fix staged). The stale-install confound is RULED OUT — the user
  performed a fully clean install before the 2026-08-14 test (deleted the old shortcut,
  deleted the Control Room Note, deleted the folder containing state.json). All three cycle-1
  refutations therefore stand and are load-bearing.
  The cycle-2 value-envelope fix (367 sites/fork converted from bare WFTextTokenAttachment to
  WFTextTokenString on string-typed parameters) is built, validated, signed and staged at
  artifacts/shortcuts/ (rebuilt 08:10, AEA1, 187758 / 191335 bytes).
  User must run: (1) Change Sequence -> Classic [symptom 2], (2) open a configured target app
  [symptom 1], (3) delete the Control Room Note, tap the shortcut once, reopen the note
  [symptom 3]. The menu title carries the stamp "PROSOCHĒ · build 2026-08-14c" as a positive
  confirmation that the fresh build is the one executing.
  Still open regardless of outcome: `--target-platform ios` rejects 3675/3675 actions
  including is.workflow.actions.comment (present in its own snapshot) — now VERIFIED as
  indiscriminate tooling noise rather than inherited assumption, but the project mandates that
  flag, so the validation invocation in .claude/CLAUDE.md needs a recorded deviation.
  DEBT: the "· build 2026-08-14c" menu-title stamp is debug scaffolding. Decide whether to
  keep it as a build identifier or strip it before ship — do not let it leak silently.

## Evidence

- timestamp: 2026-08-14 (cycle 8)
  checked: "All 20 actions in bisection span B->C (build-h indices 148-167), read individually against all four defect axes established this session: parameter KEY NAME, value ENVELOPE, picker ENUM literal, and PLIST SCALAR TYPE"
  found: "18 of the 20 actions belong to classes ALREADY EXECUTED ON DEVICE — comment; number with WFNumberActionNumber (proven at action 1359 inside Open Control Room); setvariable with an ActionOutput attachment (proven throughout PRE); setvalueforkey with WFDictionaryValue as WFTextTokenString (the device-CONFIRMED symptom-2 fix); and conditional modes 1/2, which carry only GroupingIdentifier + WFControlFlowMode. The remaining 2 are the block's two If actions, 149 and 158. BOTH carry WFInput = {'Type':'Variable','Variable': <WFTextTokenString TEXT TEMPLATE>} instead of a WFTextTokenAttachment variable descriptor."
  implication: "ROOT CAUSE (symptom 1). WFInput.Variable is a VARIABLE SLOT. A text template ({'string':'\ufffc','attachmentsByRange':{...}}) is not a variable reference, so Shortcuts cannot resolve the If's input, renders the field unset, and refuses to run with 'Please choose a value for each parameter in this action'. Exactly 2 of 20 actions in the span carry a never-executed shape and both carry this defect."

- timestamp: 2026-08-14 (cycle 8)
  checked: "Every mode-0 conditional in the artifact (307 in Dumb), classified by the serialization shape of WFInput.Variable; cross-checked against Donor 3 and all 19 golden shortcuts"
  found: "PERFECT SEPARATION, largest control group of the session. 282/307 carry the correct WFTextTokenAttachment descriptor form — including the DEVICE-PROVEN router at 37/39/41 (executed on every device run) and the Control Room refresh conditional at 3612 (executed when the user ran Open Control Room). Exactly 25 carry the text template. DONOR 3 action 4 (device export, a variable-vs-variable If built in Shortcuts.app on the target iPhone) writes WFInput.Variable as {'Value':{'Type':'Variable','VariableName':'A'},'WFSerializationType':'WFTextTokenAttachment'}. GOLDEN CORPUS: 20 of 20 WFInput-carrying conditionals use the attachment form; ZERO use a text template."
  implication: "Three independent sources — device donor, corpus, and our own internal control group — agree against the 25 sites. This is the same natural-experiment evidence shape that settled cycles 2, 4 and 5."

- timestamp: 2026-08-14 (cycle 8)
  checked: "Position of all 25 defective conditionals relative to the ten breadcrumbs"
  found: "23 of the 25 sit PAST breadcrumb J, on exit-selection and Circle-9 contract paths the user has never reached. The only two before J are 149 and 158 — BOTH inside span B->C. Action 149 is the FIRST occurrence of the defect class in the entire 3684-action artifact, two actions after breadcrumb B."
  implication: "POSITIONAL CONFIRMATION, not merely structural. The user saw B and did not see C. The first instance of the artifact's only unproven shape sits two actions past the last breadcrumb they saw. No other candidate in the span has this property."

- timestamp: 2026-08-14 (cycle 8)
  checked: "Whether the priority-3 DATE ACTION lead (format.date / adjustdate / gettimebetweendates with conventional-but-unconfirmed shapes) is implicated"
  found: "gettimebetweendates appears at action 15 at control-flow DEPTH 0, unconditionally, 22 actions before the router — so it executes on every run that reaches the manual menu, which cycles 3, 5, 6 and 7 all did. It carries WFTextTokenString in BOTH DateTime-typed slots (WFInput, WFTimeUntilFromDate) and the literal 'Seconds' in WFTimeUntilUnit. date at 11/13/19 and adjustdate at 17 are likewise at depth 0."
  implication: "The date-action axis is ELIMINATED by direct device evidence rather than inference, and no donor is needed for it. The catalog records these slots as DateTime-typed and our shape is a text template, yet it demonstrably runs — which also shows iOS coerces on that slot."

- timestamp: 2026-08-14 (cycle 8)
  checked: "Donor 3's plist scalar types vs ours, re-examined after the cycle-7 prediction was killed"
  found: "Donor writes WFNumberActionNumber as <string> ('5','3'), WFRandomNumberMinimum/Maximum as <string>, WFRepeatCount as <real>. Our generator writes <integer> for all of these. BUT our <integer> WFNumberActionNumber at action 1359 has EXECUTED SUCCESSFULLY ON DEVICE inside Open Control Room."
  implication: "SELF-CORRECTION of cycle 7's reasoning. 'iOS never writes <integer>, therefore <integer> is undecodable' does not follow — iOS demonstrably coerces plist scalar type on at least one of these numeric fields. The scalar-type axis is a serialization-STYLE difference, not an established decode failure, and the two latent sites at 418/454 are weaker suspects than cycle 7 ranked them. They remain UNCHANGED this cycle."

- timestamp: 2026-08-14 (cycle 8)
  checked: "Whether each of the 13 generator lines overwriting a conditional's WFInput changes anything other than the envelope (verified programmatically, not by eye)"
  found: "13 of 13 pass the SAME variable name that if_block() was called with on the line immediately above. Zero mismatches. if_block() already emits the correct WFInput = {'Type':'Variable','Variable': variable(name)}; each overwrite replaces variable(name) with token(name), changing the envelope and nothing else."
  implication: "Deleting all 13 lines is provably semantics-preserving apart from the envelope, and restores a shape byte-identical to the 282 correct sites and to Donor 3. No shape is invented, so the project's never-fabricate rule is honoured."


- timestamp: 2026-08-14
  checked: "Structural integrity of src/PROSOCHE-Dumb.xml (3675 actions)"
  found: "0 duplicate action UUIDs; 342 control-flow groups all single-identifier; 0 nesting-balance errors; 23 menus with WFMenuItems exactly matching their mode-1 WFMenuItemTitle lists in order."
  implication: "Control-flow wiring, GroupingIdentifier discipline, and menu wiring are NOT the cause. The generator's structural invariants hold. Eliminates the whole 'broken branch structure' family."

- timestamp: 2026-08-14
  checked: "Control-flow ancestry of the MANUAL menu block (action 1355) and the router conditionals"
  found: "Action 89 = If 'Input Key' has any value (cond 100). Action 91 = If Input Key is 'OPEN' (cond 4). Action 1217 = If 'CLOSE'. Action 1349 (unrecognised-input arm) is nested three deep inside 89>91-otherwise>1217-otherwise. Action 1355 (PHASE 5 MANUAL EMERGENCY RESTORE, the observed menu) sits directly in the OTHERWISE arm of 89."
  implication: "Seeing the manual menu proves Input Key had NO value at run time. The router itself is correctly built; the failure is upstream, in how Shortcut Input reaches the shortcut. Also eliminates 'the manual block was inserted into the wrong branch'."

- timestamp: 2026-08-14
  checked: "Parameter shape of every action in the input-normalisation chain (actions 84-87) against the ToolKit v78 first-party parameter catalog"
  found: "gettext/WFTextActionText, text.trimwhitespace/WFInput, text.changecase/text+WFCaseType, setvariable/WFInput+WFVariableName — all four match the catalog exactly, all present on 'iOS 27 Simulator'. The ExtensionInput token form matches VARIABLES.md:181 and PARAMETER_TYPES.md:423 and is byte-equivalent to golden shortcut 51cc4e26."
  implication: "The normalisation chain is correctly authored. A malformed Change Case / Trim Whitespace is eliminated as the cause of the empty Input Key."

- timestamp: 2026-08-14
  checked: "ToolKit v78 catalog entry for is.workflow.actions.setvalueforkey"
  found: "displayName 'Set Dictionary Value'; parameters are exactly WFDictionaryKey (Key), WFDictionaryValue (Value), WFDictionary (Dictionary), all present on both iOS 27 Simulator and macOS 27. There is NO WFInput parameter. The companion getvalueforkey entry displayName is 'Get Dictionary Value' and DOES take WFInput as its Dictionary."
  implication: "ROOT CAUSE (symptom 2). set_value() in the generator passes the value as WFInput, which the action does not define. The Value field is therefore unset and iOS reports 'No value was provided to the Set Dictionary Value action for the key X' — matching the reported text verbatim, including the key quoting. The displayName evidence also proves the reported action is the setter, not the getter."

- timestamp: 2026-08-14
  checked: "Whole-plist audit of every emitted (action identifier, parameter key) pair against the ToolKit catalog"
  found: "147/147 setvalueforkey use WFInput, 0 use WFDictionaryValue — in BOTH forks. Additional independent shape defects: speaktext uses WFInput instead of WFText (10x); number.random uses WFNumberMin/WFNumberMax instead of WFRandomNumberMinimum/WFRandomNumberMaximum (1x, inside the OPEN Session-ID step); com.apple.mobilenotes.SharingExtension uses WFCreateNoteInput instead of name/contents; format.date sets WFDateFormatString which the OS27 catalog does not define (but DATE_TIME.md does); openapp carries a legacy extra WFAppIdentifier alongside a valid WFSelectedApp; documentpicker.open carries legacy WFShowFilePicker."
  implication: "The defect is systemic parameter-key drift, not a single typo. The validator cannot catch it: at --target-macos 26 it checks identifier presence only and never loads the v78 parameter catalog. number.random sits on the OPEN critical path, so leaving it would waste the next device round-trip."

- timestamp: 2026-08-14
  checked: "Root plist keys of both forks vs the golden corpus (6 shortcuts that consume ExtensionInput)"
  found: "Both forks: WFWorkflowInputContentItemClasses = ['WFStringContentItem'], WFWorkflowHasShortcutInputVariables ABSENT. All three modern golden shortcuts (client 1145.8/1306.1) that reference Shortcut Input set WFWorkflowHasShortcutInputVariables = true; only the three pre-iOS-14 ones (client 736/770, min client 411) omit it. Golden 51cc4e26 is an exact structural analogue of our usage and sets it true. PLIST_FORMAT.md:87 documents the key as 'True if shortcut uses input variables'."
  implication: "Leading hypothesis for symptom 1. Our shortcut declares client 2700.0.4 / min 900 (modern), uses input variables, and omits the key that declares this. Not runtime-verifiable on the build Mac — needs the device probe."

- timestamp: 2026-08-14
  checked: "Reachability of a Set Dictionary Value with key 'sequence' from the Test-a-Circle menu case (actions 1448-3540)"
  found: "The only three setters with key 'sequence' are actions 1405/1414/1423, all inside the 'Change Sequence' case. Inside the Test-a-Circle case the setter keys are only settings_snapshot.*, active_session.*, and cooldown_until (9 of each, one per Circle). The Test path's only 'sequence' reference is a Get Dictionary Value at action 1466."
  implication: "The defect class is proven but the reported key implies the Change Sequence branch was exercised, not Test a Circle. Recorded as an open discrepancy to settle on device — it does not change the fix, since the same defect affects all 147 setters."

- timestamp: 2026-08-14
  checked: "ON-DEVICE test of the REBUILT Dumb artifact (post-fix, WFDictionaryValue + WFWorkflowHasShortcutInputVariables + random-number keys). User-reported, verbatim."
  found: >
    (a) OPEN automation: "Manual menu again. but this time the bootstrapped control room
    note is empty as well. can confirm the .json was made correctly."
    (b) Manual menu: "I get the No Value Provided error as soon as I click change
    sequence., didn't even get to test a circle menu."
    (c) Menu item tapped when the error FIRST appeared on 2026-08-13: "Test a Circle".
  implication: >
    BOTH falsification tests tripped. Symptom 1 hypothesis (missing
    WFWorkflowHasShortcutInputVariables) is REFUTED — input still empty. Symptom 2 root
    cause is REFUTED per its own stated criterion ("if a rebuilt artifact using
    WFDictionaryValue still raises 'No value provided', the hypothesis is wrong"). The
    catalog key match may be correct but INSUFFICIENT — e.g. the value may need a typed
    serialization envelope (WFTextTokenString / WFTextTokenAttachment / dictionary-value
    wrapper) rather than the bare token the emitter produces. Demoted from CONFIRMED.

- timestamp: 2026-08-14
  checked: "Where the 'sequence' error fires, across the original and the post-fix run"
  found: >
    2026-08-13 (pre-fix): fired after tapping Test a Circle, then a Circle button.
    2026-08-14 (post-fix): fires immediately on tapping Change Sequence, before the Test a
    Circle menu is even reached.
  implication: >
    The error is raised from BOTH menu paths. Static reachability showed the only three
    'sequence' setters live inside Change Sequence, which contradicts the original Test a
    Circle report. Two paths raising the same key points at a SHARED UPSTREAM write
    (executed before menu-case dispatch) rather than a per-case setter. Locate where the
    error actually originates instead of assuming which menu case owns it.

- timestamp: 2026-08-14
  checked: "NEW SYMPTOM (3) — Control Room Note bootstrap, on-device"
  found: "The bootstrapped Control Room Note is EMPTY, while the user confirms state.json was written correctly."
  implication: >
    Third INDEPENDENT failure. The state-file write path works; the Note write path does
    not. Do not fold into symptoms 1/2 without evidence. May share a defect class with
    symptom 2 (wrong or under-specified parameter key / value envelope on the Notes action
    family) — note that .claude/CLAUDE.md flags the Notes actions as catalog-gated to
    macOS 27 and explicitly "verify empirically on device". The whole-plist audit already
    found com.apple.mobilenotes.SharingExtension emitting WFCreateNoteInput instead of the
    catalog's name/contents, which is a live candidate.

- timestamp: 2026-08-14
  checked: "Staged signed artifacts on the build Mac (independent check by session-manager)"
  found: "Both .shortcut files carry AEA1 magic, rebuilt 07:45 2026-08-14 (183613 / 187866 bytes); generator + both forks show as modified in git."
  implication: >
    The BUILD side is confirmed fresh. This does NOT confirm the DEVICE ran the fresh
    build — importing a .shortcut whose display name matches an installed shortcut can
    create a second copy rather than replacing it, leaving the automation wrapper's Run
    Shortcut pointed at the OLD one. This stale-install confound is UNRULED-OUT and could
    explain all three failed observations at once. It must be discriminated FIRST.

- timestamp: 2026-08-14 (cycle 2)
  checked: "Golden-shortcut corpus for real setvalueforkey examples, as directed"
  found: "ZERO instances of is.workflow.actions.setvalueforkey exist across all 19 golden shortcuts. That specific avenue is empty."
  implication: >
    The corpus cannot settle WFDictionaryValue's envelope directly. It does, however,
    settle the general rule decisively via the parameters it does contain — see the next
    entry. WFDictionaryValue's envelope therefore rests on its catalog type plus the
    unanimous behaviour of every other string-typed parameter, and is the weakest link in
    this cycle's chain.

- timestamp: 2026-08-14 (cycle 2)
  checked: "Catalog parameter TYPES (typePythonName) rather than key names, plus golden-corpus envelope usage for every string-typed parameter"
  found: >
    setvalueforkey parameters are WFDictionaryKey `str`, WFDictionaryValue `str`,
    WFDictionary `com_apple_shortcuts_wfcontent_item`. Across the corpus, string-typed
    parameters use WFTextTokenString 99 times and WFTextTokenAttachment 12 times, and the
    12 are concentrated in list-shaped or URL parameters (text.combine.text 4/4,
    text.split.text 4/4, openurl.WFInput 2/2, evernote 2). Single-value text parameters are
    unanimous: gettext.WFTextActionText 36/36 WFTextTokenString and 0 attachment;
    text.match.text 8/8; text.replace.WFInput 3/3; alert.WFAlertActionMessage 8/8.
    Content-item, File, Placemark and float parameters use attachments in the corpus.
  implication: >
    Cycle 1 verified that key NAMES matched the catalog but never checked the VALUE
    ENVELOPE, which is a distinct axis. This is the precise blind spot that let the defect
    survive a full cycle.

- timestamp: 2026-08-14 (cycle 2)
  checked: "Whole-plist audit of emitted envelope vs catalog parameter type, both forks"
  found: >
    Nine string-typed parameters carried bare WFTextTokenAttachments:
    gettext.WFTextActionText x220, setvalueforkey.WFDictionaryValue x131,
    alert.WFAlertActionMessage x10, openurl.WFInput x4, searchweb.WFInputText x2,
    text.trimwhitespace.WFInput x1, text.changecase.text x1, text.match.text x1.
    Meanwhile 16 setvalueforkey and 11 gettext actions ALREADY used WFTextTokenString.
  implication: >
    The artifact contained a mixed population of both envelopes for the same parameters —
    a natural experiment usable as an internal control group.

- timestamp: 2026-08-14 (cycle 2)
  checked: "DECISIVE — mapping the mixed envelope population onto the user's own working/failing observations"
  found: >
    WORKING (user-confirmed): action 75 builds the state.json body as a WFTextTokenString
    template (1178 chars, 4 attachments) -> "can confirm the .json was made correctly".
    Action 84 reads Shortcut Input as WFTextTokenString/ExtensionInput -> correctly formed.
    Action 3615 builds the Control Room body as WFTextTokenString (5121 chars).
    FAILING (user-observed): actions 85 and 86 (Trim Whitespace, Change Case) carried bare
    attachments -> Input Key empty -> MANUAL menu. Action 1405 (key `sequence`) carried a
    bare attachment -> "No value provided". Actions 3624-3639+ (Snapshot* reads) carried
    bare attachments -> empty refresh content appended to the Note.
  implication: >
    Perfect separation between envelope form and observed outcome, within one build, one
    device and one run. This is far stronger than the catalog inference that failed in
    cycle 1, because the control and treatment groups are both inside the artifact the user
    actually ran.

- timestamp: 2026-08-14 (cycle 2)
  checked: "Execution order — does the working state.json contradict the envelope hypothesis?"
  found: >
    Zero setvalueforkey actions exist before the routing gate (action 84); the pre-gate
    region contains no literal `dictionary` action either. state.json is written at action
    79 from the action-75 template. The bootstrap setters at 151/153/161/163 sit INSIDE the
    OPEN branch (conditional 91), which was never entered because Input Key was empty.
  implication: >
    A correct state.json and a failing Set Dictionary Value are fully consistent: the
    working writer uses the correct envelope, and the mis-enveloped setters never ran on
    that pass. The apparent counter-evidence dissolves.

- timestamp: 2026-08-14 (cycle 2)
  checked: "Differential of the current build against the 2026-08-13 build in which the Note was confirmed created successfully (per the resolved unsupported-device-import session)"
  found: >
    Exactly 148 actions differ (147 setvalueforkey + 1 number.random) — i.e. only cycle 1's
    changes. The note chain at actions 3615 / 3617 / 3618 is byte-identical between the two
    builds.
  implication: >
    The empty Note is NOT a cycle-1 regression. The note-creation path is unchanged from a
    build where creation succeeded. The envelope defect explains the empty REFRESH block
    appended at 3623+, but if the body is empty on a fresh create there is a second,
    still-unidentified cause. Symptom 3 is only partially explained.

- timestamp: 2026-08-14 (cycle 2)
  checked: "The inherited claim that `--target-platform ios` failure is pre-existing tooling noise, verified rather than assumed"
  found: >
    At --target-macos 26 --target-platform ios the validator rejects 3675 of 3675 actions —
    every single one, including is.workflow.actions.comment and is.workflow.actions.nothing,
    which ARE present in the bundled iOS-27 snapshot. So rejection is not driven by
    identifier presence. The snapshots are also demonstrably incomplete:
    is.workflow.actions.conditional is absent from BOTH the iOS-27 and v63 snapshots.
    --target-macos 26 --target-platform all passes cleanly for both forks.
  implication: >
    Confirmed genuine tooling noise, not a masked real error — nothing can hide inside a
    check that fails 100% of inputs indiscriminately. The claim inherited from cycle 1 is
    now verified rather than assumed, and this line of inquiry is closed.

- timestamp: 2026-08-14
  checked: "Stale-install confound — whether the device actually ran the rebuilt artifact during the 2026-08-14 test"
  found: >
    User-reported, verbatim: "i did delete the old shortcut before importing, as well as
    delete the control room note, and delete the folder containing the json, for a clean
    install". Session-manager independently confirmed the build side: both .shortcut files
    carry AEA1 magic, rebuilt 08:10 2026-08-14 (187758 / 191335 bytes); the build stamp
    appears exactly once in each generated fork; Dumb now carries 792 WFTextTokenString.
  implication: >
    CONFOUND RULED OUT. No duplicate-name shadowing was possible, so the automation wrapper
    cannot have targeted a pre-fix copy; the empty Note is a genuine fresh-bootstrap result,
    not a stale leftover; and bootstrap ran from nothing. All three cycle-1 refutations are
    load-bearing. Critically, this SHARPENS the decisive asymmetry: within ONE bootstrap pass
    on freshly-created state, the file-write path succeeded while the Note-write path produced
    an empty Note. A defect that killed value payloads universally would have emptied
    state.json too — so the defect is action-family / parameter-type specific, which is
    exactly what the cycle-2 value-envelope hypothesis predicts (string-typed parameters fail,
    content-item-typed parameters do not).

- timestamp: 2026-08-14
  checked: "ON-DEVICE test of the cycle-2 envelope-fix artifact (367 sites/fork converted to WFTextTokenString). Clean install. User-reported, verbatim."
  found: >
    (a) Step 1, manual tap / Change Sequence: "import success. first run gives 'unrecognised
    input. prosoche received input it did not recognise and took no action. nothing was read,
    written, or changed.'. Well done, you made a brand new error we didn't have before."
    (b) Step 2, open a configured target app: "didn't get here."
    (c) Step 3, Control Room note: "couldn't test."
  implication: >
    REGRESSION introduced by the cycle-2 envelope fix, on the MANUAL-INVOCATION path.
    Before: tapping the shortcut with no input reached the manual menu. After: it hits
    PROSOCHĒ's own unrecognised-input rejection and takes no action.
    SYMPTOMS 1 AND 3 ARE UNMEASURED THIS CYCLE — not untested-but-probably-fine, simply no
    data. The rejection fires first and blocks both remaining test routes.
    The build IS live: the import succeeded and execution reached PROSOCHĒ's own guard
    message. The `· build 2026-08-14c` stamp is NEITHER confirmed NOR missing — the user
    never reached a menu, so it was never displayed.
    Diagnostic significance: the error text is PROSOCHĒ's own branch, not an iOS error. That
    branch (action 1349) is reachable ONLY when "Input Key has any value" PASSES and the value
    matches neither OPEN nor CLOSE. So a manual tap now yields something NON-EMPTY matching
    neither literal, where it previously yielded empty. The envelope change altered what Input
    Key resolves to when there is no input at all. This is new information about the router
    that the previous two cycles could not have obtained.

- timestamp: 2026-08-14 (cycle 3)
  checked: "Exact router topology in the regressed build, by GroupingIdentifier, in src/PROSOCHE-Dumb.xml (3675 actions)"
  found: >
    F646324A (cond 100, 'Input Key has any value') = actions 89 / 1353 / 3674.
    FA045F2B (cond 4, 'OPEN')                      = actions 91 / 1215 / 1352.
    A2F7247B (cond 4, 'CLOSE')                     = actions 1217 / 1348 / 1351.
    The unrecognised-input arm is exactly two actions: comment 1349 + alert 1350, sitting in
    A2F7's Otherwise. Alert 1350's WFAlertActionMessage is the literal string the user quoted,
    verbatim and complete: "PROSOCHĒ received input it did not recognise and took no action.
    Nothing was read, written, or changed."
    The MANUAL arm is actions 1354-3673, sitting in F646's Otherwise, and F646's End If is the
    LAST action in the shortcut (3674).
  implication: >
    The user's reported error is positively identified as alert 1350, three conditionals deep.
    Its reachability precondition is unambiguous: cond 100 PASSED. This converts the
    coordinator's inference into a structural fact and pins the exact edit sites.

- timestamp: 2026-08-14 (cycle 3)
  checked: "Which actions in the input-normalisation chain actually changed between the two device builds"
  found: >
    Action 84 (gettext, WFTextActionText = '￼' + ExtensionInput) is WFTextTokenString in BOTH
    builds — it was never a bare attachment and was never converted. Only actions 85
    (text.trimwhitespace.WFInput) and 86 (text.changecase.text) changed. Action 87
    (setvariable.WFInput -> 'Input Key') is a content-item parameter and remains a bare
    attachment by design, in both builds.
  implication: >
    Narrows the cycle-2 regression to a two-action delta. Combined with the two device
    observations (cond 100 FALSE before, TRUE after), this yields the derived fact that
    Uppercase(Trim(<action 84 output>)) is NON-EMPTY when Shortcut Input is absent — without
    needing to know what that value is. It also shows the placeholder was already being
    produced at action 84 pre-fix and was simply being discarded by 85's bare attachment.

- timestamp: 2026-08-14 (cycle 3)
  checked: "The coordinator's own stated falsification test for the U+FFFC candidate — does Trim strip it?"
  found: >
    U+FFFC is OBJECT REPLACEMENT CHARACTER, Unicode general category So. It is not in Zs/Zl/Zp
    and is not whitespace under any standard definition; Python's str.strip() leaves it intact.
  implication: >
    The stated refutation condition ("if Trim already strips it, THIS HYPOTHESIS IS WRONG")
    does not fire. Candidate (i) survives. This is supporting evidence only — iOS Trim
    Whitespace cannot be executed on the build Mac, so it is NOT treated as confirmation, and
    the fix is deliberately built to be correct whether or not (i) is true.

- timestamp: 2026-08-14 (cycle 3)
  checked: "Nesting-depth impact of the proposed positive-match restructure, simulated over the real action list"
  found: >
    Current maximum control-flow depth is 12; after the restructure it is 11, with balanced
    open/close (final depth 0) in both. OPEN and CLOSE each become one level shallower; the
    MANUAL body becomes one level deeper. Action count goes 3675 -> 3671 (removing the gate
    If, its Otherwise, its End If, and the unrecognised alert).
  implication: >
    The restructure does not deepen the shortcut and does not risk the nesting ceiling. It
    reduces it. (Both figures already exceed the depth-7 corpus evidence cited in CLAUDE.md;
    that is pre-existing and this change moves it in the safe direction.)

- timestamp: 2026-08-14
  checked: "ON-DEVICE test of the cycle-3 router-restructure artifact (build 2026-08-14d). Clean install. User-reported, verbatim."
  found: >
    Step 1 (manual tap): "Identical. / Input Key: [] / Empty ref: []"
    Step 2 (open target app): "Automation failed. 'When any of 3 apps are opened' encountered
    an error: Please choose a value for each parameter in this action."
    Step 3 (Change Sequence -> Classic): "first I get an allow prosoche to save 1 dictionary
    to a file. looks like a success."
    Step 4 (Control Room note): "Exists but empty"
  implication: >
    MANUAL INVOCATION RESTORED — cycle-2 regression CLOSED. The router restructure took on
    device; the unrecognised-input rejection is gone and the user reached the menu.
    SYMPTOM 2 FIXED — first genuine device confirmation. Change Sequence -> Classic completed
    with no "No value provided"; the expected iOS file-save permission prompt appeared and
    succeeded. The WFDictionaryValue key + WFTextTokenString envelope combination is now
    confirmed at RUNTIME, not merely statically. This retroactively validates the cycle-2
    envelope diagnosis that looked refuted at the time — it was necessary but had been
    masked by the router defect (A).
    ROUTER TRACE — candidate (i) SUPPORTED, candidate (ii) ELIMINATED. Input Key renders
    identically to the known-empty reference, so on a manual tap it holds a value that is
    non-empty to cond 100 but renders as nothing: a non-printing character, not visible text.
    Consistent with a lone U+FFFC. Moot for correctness after the restructure; logged as
    observed.

- timestamp: 2026-08-14
  checked: "SYMPTOM 1 — where the OPEN failure now originates"
  found: >
    The automation fails BEFORE PROSOCHĒ runs at all: iOS reports "When any of 3 apps are
    opened" encountered an error: "Please choose a value for each parameter in this action."
    No PROSOCHĒ action produced this; the shortcut was never reached.
  implication: >
    CAUSE HAS MOVED OFF THE PLIST. This is iOS reporting an action inside the user's
    manually-created Personal Automation WRAPPER with a required parameter left unset. This
    cycle therefore produced ZERO evidence about the plist-side OPEN path — do not record it
    as progressed.
    This is precisely the discrimination the cycle-1 INPUT PROBE was designed to make and
    which was never executed. LIVE HYPOTHESIS, ranked first, not yet asserted: the wrapper's
    Run Shortcut action may never have passed `OPEN` at all because its Shortcut and/or Input
    parameter is unset — in which case every plist-side OPEN theory across three cycles was
    chasing a device-side misconfiguration. A Run Shortcut with no target shortcut selected
    produces exactly this error text.
    Also unresolved: "any of 3 apps" means one shared automation covers three target apps —
    whether that is correct for PROSOCHĒ's design or needs splitting per-app must be stated.

- timestamp: 2026-08-14
  checked: "SYMPTOM 3 — Control Room note, first hard data in three cycles"
  found: "Note EXISTS but is EMPTY, on a clean install, in the SAME run where the envelope fix demonstrably worked for Set Dictionary Value (symptom 2 passed)."
  implication: >
    SYMPTOM 3 IS NOT THE ENVELOPE DEFECT. Excluded by DIRECT EVIDENCE now, not by argument:
    the same build, same run, same envelope treatment produced a working dictionary write and
    an empty note. It is a separate cause in the Note WRITE path specifically.
    The note is CREATED (it exists) but its BODY is empty — so the create call succeeds and
    the body parameter is what fails. .claude/CLAUDE.md flagged the Notes actions' parameter
    shapes as catalog-gated to macOS 27 with an explicit "verify empirically on device"; that
    flag is now cashing in. The prior whole-plist audit already found
    com.apple.mobilenotes.SharingExtension emitting WFCreateNoteInput instead of the catalog's
    name/contents — a live candidate. Investigate whether the body parameter is content-item
    or string typed, and whether its key AND value envelope match the catalog.

- timestamp: 2026-08-14 (cycle 4)
  checked: "The note-write chain end to end (actions 3613-3617, 3646-3648) against the ToolKit v78 catalog, the golden corpus, AND a Create Note shortcut exported from the USER'S OWN iPhone (.planning/debug/'Donor - notes.shortcut'), decrypted this cycle"
  found: >
    The donor decrypts to a three-action chain identical in structure to ours:
    gettext -> getrichtextfrommarkdown -> com.apple.mobilenotes.SharingExtension with
    AppIntentIdentifier CreateNoteLinkAction. EXACTLY ONE LINK DIVERGES.
    Link 1 (3613 gettext, WFTextTokenString)              matches.
    Link 2 (3615 getrichtextfrommarkdown.WFInput, BARE)   matches the donor AND golden
      f44f5caf action 13; catalog-typed com_apple_shortcuts_wfcontent_item, so bare is
      CORRECT and must not be converted.
    Link 3 (3616 WFCreateNoteInput)                       DIVERGES. Donor serialises it as
      {'string': '￼', 'attachmentsByRange': {'{0, 1}': <token>}} / WFTextTokenString.
      Ours was a bare WFTextTokenAttachment.
    Second divergence in the same pair: the donor names the markdown output
    'Rich Text from Markdown'; ours said 'Rich Text'. Golden f44f5caf action 14 independently
    uses the donor's name.
    Catalog types: SharingExtension.contents and appendnote.text are BOTH `AttributedString`.
  implication: >
    ROOT CAUSE (symptom 3). The cycle-2 envelope rule is correct and already runtime-proven,
    but its allowlist was scoped to catalog type `str`. `AttributedString` is a THIRD type
    category — a text type, not a content item — that obeys the same rule and was never
    considered, so both Notes body parameters were invisible to the normaliser AND to its
    recurrence guard. A bare attachment there creates the note successfully with an EMPTY
    BODY, which is precisely "exists but empty".
    The divergence sits at the exact link whose output is empty, and the device donor is
    higher authority than the macOS-27-tagged catalog for this action family.

- timestamp: 2026-08-14 (cycle 4)
  checked: "Whole-plist re-audit by catalog TYPE, both forks, after adding AttributedString to the analysis"
  found: >
    Only three sites in the whole artifact were affected: 3616 WFCreateNoteInput (envelope +
    output name), 3648 appendnote.text (envelope only). The state-recovery appendnote at 3668
    was ALREADY a WFTextTokenString because it happens to be a composite template.
    Remaining bare attachments on text-typed parameters after the fix: only the 4 deliberately
    excluded openurl.WFInput sites (corpus-evidenced, unchanged since cycle 2).
  implication: >
    A second internal control group, same action identifier: appendnote 3668 (correct
    envelope, authored that way by accident of shape) beside appendnote 3648 (bare). Same
    natural experiment that settled cycle 2, now inside the Notes family.
    It also gives the next device test its discriminator: 3648 changes on the ENVELOPE AXIS
    ONLY (its OutputName 'Text' was already correct), so the Control Room refresh block is a
    clean single-variable test of the AttributedString hypothesis, while the create path
    changes on two axes and cannot discriminate on its own.

- timestamp: 2026-08-14 (cycle 4)
  checked: "SYMPTOM 1 — whether one shared automation covering 3 apps is correct for PROSOCHĒ's design; answered from the design, not deferred"
  found: >
    `CurrentApp` appears ZERO times in either fork — the master shortcut consumes no app
    identity whatsoever. .planning/research/ARCHITECTURE.md §5 states the decision explicitly:
    "Heat, Gravity, Pressure, Circle, and `active_session` are GLOBAL across all tracked apps,
    not per-app... there is exactly one `active_session` pointer at a time", and §5 further
    records the cross-app rapid-return approximation as INTENTIONAL. The shipped Control Room
    copy (Automation A / Automation B) tells the user to select "the apps" plural in ONE
    automation per trigger.
  implication: >
    ONE App automation covering all watched apps is CORRECT; splitting per-app is unnecessary
    and would not improve anything, because the shortcut cannot tell the apps apart by design.
    What must remain split is OPEN from CLOSE — two automations, one per trigger, because they
    pass different literals. The user's "any of 3 apps" automation is therefore not the defect.

- timestamp: 2026-08-14 (cycle 4)
  checked: "SYMPTOM 1 — a mechanistic explanation for the automation-side error that fits the session's own history"
  found: >
    The user has performed a full clean install before EVERY cycle, explicitly including
    deleting the installed shortcut. Deleting a shortcut orphans any Personal Automation's
    Run Shortcut reference, leaving that action with no target selected. iOS reports a Run
    Shortcut with no target selected as exactly "Please choose a value for each parameter in
    this action" — the user's verbatim error — attributed to the automation's own name
    ("When any of 3 apps are opened"), which is why no PROSOCHĒ action appears in the message.
    Timeline fit: cycle 1 the automation ran (manual menu appeared, so the shortcut executed);
    cycle 2 step 2 was never reached; cycle 3 the automation errored. The break appears after
    the first delete-and-reimport, not before.
  implication: >
    STRONG HYPOTHESIS, NOT ESTABLISHED — a screenshot settles it in one exchange and costs
    nothing. If true, symptom 1's cycle-1 appearance is separately and fully explained by the
    envelope defect (input arrived as OPEN, actions 85/86 evaporated it, Input Key empty,
    MANUAL menu), meaning the plist-side OPEN path may already be repaired by cycles 2+3 and
    has simply never been exercised. Recorded as a hypothesis precisely because that would be
    a very convenient conclusion to reach without evidence.

- timestamp: 2026-08-14 (cycle 4)
  checked: "NEW CAPABILITY — reading a signed .shortcut back on the build Mac"
  found: >
    A signed .shortcut's AEA1 header carries its own signing certificate chain as a bplist in
    the auth-data blob at offset 12. Extract the leaf, take its public key AS PEM (aea rejects
    the raw X9.63 point and the DER SPKI; PEM works), then `aea decrypt -sign-pub pub.pem`
    followed by `aa extract` yields Shortcut.wflow, a normal binary plist. Recipe recorded in
    docs/BUILD-NOTES.md §14.
  implication: >
    Closes a verification gap that stood through cycles 1-3, where build freshness could only
    be argued from the unsigned XML plus file mtime. The cycle-4 signed Dumb artifact was
    decrypted and confirmed to carry 3674 actions, WFCreateNoteInput as WFTextTokenString,
    both appendnote.text as WFTextTokenString, and the stamp "PROSOCHĒ · build 2026-08-14e".
    "Did the device get the artifact we think it got" is now answerable from the shipped file.

- timestamp: 2026-08-14
  checked: "ON-DEVICE test of the cycle-4 AttributedString-envelope artifact (build 2026-08-14e). Clean install WITH Recently Deleted purged. User-reported, verbatim."
  found: >
    Router trace, manual tap: "the inputkey[] is still empty ref[]"
    Note creation: "note creates successfully"
    Step 1(b) "## CURRENT SETTINGS" block with real values: "Present, with real values"
    Step 1(a) full note body: "Full body present"
    Step 2 Run Shortcut Shortcut+Input fields: "Both look correctly set"
    Automation behaviour: "when I run the automation it says 'failed... please choose a value
    for each parameter in this action.'"
    (User had a session crash mid-test and re-answered from the same build; treated as one
    coherent cycle-4 result set.)
  implication: >
    SYMPTOM 3 CLOSED. Both experiments passed. (b) the APPEND path — the clean
    single-variable test, changed on the envelope axis only — produced a real CURRENT
    SETTINGS block, confirming the AttributedString envelope fix at RUNTIME. Because (b)
    passed, (a) is interpretable, and (a) passed too, so DEV-04 (the deferred donor
    folder/WFNoteGroup parameter) is NOT required for correctness. This was also the first
    cycle with Recently Deleted purged, so the soft-deleted-note reuse-branch contamination
    was a real risk and is now excluded.
    ROUTER TRACE unchanged and expected — Input Key still renders identically to Empty ref on
    a manual tap. Harmless post-restructure. Manual invocation remains working.
    TWO OF THREE ORIGINAL SYMPTOMS NOW CLOSED: symptom 2 (cycle 3), symptom 3 (cycle 4).

- timestamp: 2026-08-14
  checked: "SYMPTOM 1 — the orphaned Run Shortcut reference theory"
  found: >
    User inspected the Run Shortcut action in the Personal Automation: both the Shortcut and
    Input fields "look correctly set". The automation still fails with "please choose a value
    for each parameter in this action".
  implication: >
    ORPHANED-REFERENCE THEORY REFUTED. Symptom 1 returns to the plist with a positively
    verified wrapper — the exact condition under which the cycle-1 INPUT PROBE becomes the
    next move. It was designed in cycle 1 and has still NEVER been executed; it is now the
    priority.
    TWO CAVEATS that must be built into the next step rather than assumed past:
    (i) "Both look correctly set" is the user's VISUAL INSPECTION of a Shortcuts UI, not proof
        that the parameters are populated in the automation's stored representation. Shortcuts
        can render a field as populated while the underlying parameter is unset — precisely
        the class of error the message describes. The probe is valuable exactly because it
        does not depend on trusting that inspection, so it must be designed to give an
        unambiguous pass/fail WITHOUT the user judging a UI field.
    (ii) It is NOT established that the failing action is the Run Shortcut. The error names the
        AUTOMATION, not an action. Other candidates in the user's hand-built wrapper must be
        enumerated — the Text action holding OPEN, the trigger configuration itself, anything
        else it contains — and the user given a way to identify WHICH action iOS objects to,
        or told plainly that Shortcuts does not expose one.
    NEW LEVERAGE: signed .shortcut decryption (proven this cycle on the Notes donor) may let
    the wrapper's STORED parameters be read directly, settling both caveats from ground truth
    instead of UI inspection — the same move that cracked symptom 3.

- timestamp: 2026-08-14
  checked: "SCREENSHOT of the Personal Automation's action list (user-supplied). Ground truth on the wrapper's contents, not UI-field inspection."
  found: >
    Automation "When any of 3 apps are open…" contains EXACTLY TWO actions:
    (1) Text — body contains exactly `OPEN`, single line, no visible whitespace or extra
        characters.
    (2) Run — target shortcut chip reads "PROSOCHĒ — Nine Circles — Dumb", rendered as a live
        shortcut chip with its icon (populated, not a placeholder). Directly below, `Input`
        carries a yellow Text magic-variable chip, i.e. wired to action 1's output.
    No third action. No visibly blank or placeholder parameter anywhere in the wrapper.
  implication: >
    THE WRAPPER IS VERIFIED CORRECT. Both standing caveats are closed by evidence rather than
    by trusting a field reading: the Shortcut reference is populated (not orphaned) and the
    Input carries the Text magic variable. There is no third action that could hold an unset
    parameter.
    THIS INVERTS THE SEARCH SPACE. "Please choose a value for each parameter in this action"
    is attributed to the automation BY NAME, but the automation contains no action lacking a
    value. The remaining reading: the failing action lives INSIDE PROSOCHĒ, invoked via Run
    Shortcut, with iOS surfacing the failure against the OUTERMOST automation rather than the
    nested shortcut. LEADING HYPOTHESIS — test before anything else.
    It explains the whole shape of symptom 1 and why it survived four cycles of router work:
    manual invocation reaches the MANUAL menu and is now well exercised (Change Sequence,
    Open Control Room, note creation all succeed); the OPEN literal path fails immediately,
    before any PROSOCHĒ alert appears. Therefore the defective action executes on the OPEN
    pipeline and NOT on the manual path — an action with a required parameter empty or unset
    in the emitted plist.
    CRITICALLY: this is STATICALLY ANSWERABLE on the build machine with no device round-trip.

- timestamp: 2026-08-14 (cycle 5)
  checked: "STATIC ENUMERATION of every action reachable on the OPEN branch but NOT on the device-exercised (PRE + MANUAL) population, per the cycle-5 priority order"
  found: >
    Router spans, by GroupingIdentifier: OPEN body = actions 91-1213; CLOSE body = 1217-1346;
    MANUAL body = 1348-3671; PRE (runs on every path) = 0-89.
    TWELVE identifiers appear in the OPEN body and NEVER in PRE+MANUAL: repeat.each(18),
    openapp(18), appendvariable(7), openurl(4), round(3), repeat.count(2),
    calculateexpression(2), searchweb(2), searchmaps(2), number.random(1), count(1),
    choosefromlist(1).
  implication: >
    The search space really did invert and really is small — 12 identifiers, not 3674 actions.
    Every parameter-defect class that ALSO appears on the device-proven MANUAL path is
    exonerated by direct evidence rather than by argument, which is the same control-group
    method that settled cycles 2 and 4.

- timestamp: 2026-08-14 (cycle 5)
  checked: "Whether iOS pre-flight-validates the whole shortcut on automation launch, or errors only on the action it reaches"
  found: >
    count.WFCountType, getitemfromlist.WFItemSpecifier and speaktext.WFInput carried IDENTICAL
    defects in the 2026-08-13 build. That build ran from the Personal Automation and reached
    the MANUAL menu — the user saw it. No "please choose a value" error occurred.
  implication: >
    PRE-FLIGHT VALIDATION REFUTED. iOS errors on the action it EXECUTES, not on load. Combined
    with the verified-correct wrapper, this pins the failing action to the OPEN branch and
    makes the coordinator's inversion an evidenced conclusion rather than an assumption.
    It also explains the timeline exactly: the OPEN branch had NEVER executed on device before
    build d, because Input Key was empty pre-envelope-fix and every automation run took the
    MANUAL arm. Cycle 2's fix did not cause this defect — it EXPOSED it.

- timestamp: 2026-08-14 (cycle 5)
  checked: "Every picker/enum-typed parameter in both forks, for presence and for literal-vs-token value"
  found: >
    PERFECT SEPARATION, identical in both forks. Eight picker classes carry a literal enum
    case: searchweb 'Google', text.changecase 'UPPERCASE', getdevicedetails 'Current Volume'
    and 'Current Brightness', setvolume 'Media', gettimebetweendates 'Seconds', round
    'Ones Place', searchmaps 'Maps', getitemfromlist 'First Item' (x2).
    EXACTLY TWO deviate:
      is.workflow.actions.count.WFCountType             MISSING (1 Dumb / 2 Sentient)
      is.workflow.actions.getitemfromlist.WFItemSpecifier  a VARIABLE TOKEN at 31/33 sites,
        with WFItemIndex absent entirely.
    Generator source shows the same split internally: build_state_engine.py:820 emits the
    literal 'First Item' (correct) while :435 and :552 emit WFItemSpecifier=variable(...).
  implication: >
    ROOT CAUSE (symptom 1), identified. A picker parameter that is absent or non-literal
    renders as an unfilled picker, and iOS refuses to run the action with exactly
    "Please choose a value for each parameter in this action" — attributing it to the
    outermost caller (the automation, by name) and never naming the action.
    Third instance of this session's recurring family: the parameter shape iOS actually reads
    was never emitted. Cycle 1 = key name. Cycles 2/4 = value envelope. Cycle 5 = required
    picker. Each pass fixed one axis and left the next undefended.

- timestamp: 2026-08-14 (cycle 5)
  checked: "Golden-shortcut corpus for count and getitemfromlist, to source the enum literals rather than fabricate them"
  found: >
    count: 11/11 corpus instances emit WFCountType (all 'Items'); 0 omit it. Catalog agrees —
    WFCountType is the action's FIRST parameter, display name 'Type'.
    getitemfromlist: every corpus instance puts a LITERAL in WFItemSpecifier and the DYNAMIC
    index in WFItemIndex. Golden 332c12a0060043b388b2 does precisely what we need:
    WFItemSpecifier='Item At Index' with WFItemIndex holding a Repeat Index VARIABLE token.
  implication: >
    Both literals are corpus-sourced, so the fix fabricates nothing. The corpus also supplies
    the correct SHAPE for a dynamic index, which is what the generator had inverted.

- timestamp: 2026-08-14 (cycle 5)
  checked: "math.WFMathOperation — the strongest-looking candidate, tested against the corpus before acting"
  found: >
    25 of 42 math actions omit WFMathOperation (the generator's helper does
    `if op and op != "+"`), and 13 of those sit in the pre-menu OPEN Heat-arithmetic path —
    a required enum picker missing on the guaranteed OPEN path. But golden shortcut
    2e0fb675e459 (client 1146.11.1, minimum client 900 — our exact vintage) omits
    WFMathOperation with our exact key shape (WFInput + WFMathOperand).
  implication: >
    REFUTED, and deliberately NOT changed. Corpus evidence outranks catalog inference under
    this project's own cycle-2 openurl precedent; '+' is genuinely the implicit default.
    Recorded as DEV-05. This is the check that stopped a plausible-looking wrong fix.

- timestamp: 2026-08-14 (cycle 5)
  checked: "The pre-menu OPEN region (actions 91-521, everything before the first OPEN-path menu) exhaustively, against the ToolKit catalog"
  found: >
    STATICALLY CLEAN. Every action's parameters are complete and correctly valued:
    round WFRoundTo='Ones Place' (so TenToThePowerOf is not needed), setvolume
    WFVolumeSetting='Media', gettimebetweendates WFTimeUntilUnit='Seconds',
    number.random keys correct, getitemfromlist@360 WFItemSpecifier='First Item',
    repeat.count WFRepeatCount=9 (matches corpus shape). No empty-valued parameter anywhere in
    the OPEN body. Every remaining discrepancy in the region is a class that also appears on
    the MANUAL path and was demonstrably EXECUTED there (getvalueforkey missing
    WFGetDictionaryValueType, documentpicker.save missing WFFolder, documentpicker.open
    WFShowFilePicker, setitemname missing WFDontIncludeFileExtension).
    Both confirmed defects sit AFTER the first OPEN menu: count at 576 inside case 'Leaving',
    getitemfromlist at 580 / 1155 / 1160 / 1166.
  implication: >
    LOAD-BEARING CAVEAT, recorded rather than smoothed over. The claim "the OPEN path fails
    before any PROSOCHĒ alert appears" is the coordinator's characterisation; the user's
    verbatim cycle-3 and cycle-4 reports say only that the automation failed and never state
    whether a menu appeared. If NO PROSOCHĒ UI ever appeared, this cycle's fix cannot be the
    whole story, because the region before the first menu is clean. That single bit was never
    captured and is the cheapest discriminator available — it is now requested explicitly.

- timestamp: 2026-08-14 (cycle 5)
  checked: "Whether iOS exposes WHICH nested action it is objecting to (coordinator priority 3)"
  found: >
    It does not. The automation-failure notification reports the AUTOMATION's name and the
    message text only. There is no action index, no drill-down, and no log. Shortcuts does not
    surface the offending action for a failure inside a nested Run Shortcut.
  implication: >
    The user cannot narrow this by inspecting further and must not be asked to try. This is
    stated plainly to them rather than implied away.

- timestamp: 2026-08-14 (cycle 5)
  checked: "Ask-Each-Time tokens and import questions, as an alternative mechanism for an unset parameter"
  found: >
    Zero 'Ask' tokens anywhere in either fork (token census: 2016 Variable, 963 ActionOutput,
    1 ExtensionInput). WFWorkflowImportQuestions targets only actions 2 and 4, both Text
    actions in the PRE region that run on every path including the working MANUAL one.
  implication: "Ask-Each-Time and import-question mechanisms are ELIMINATED as the cause."

- timestamp: 2026-08-14
  checked: "ON-DEVICE test of the cycle-5 picker-axis artifact (build 2026-08-14f). Clean install. User-reported, verbatim."
  found: >
    Q1, did ANY PROSOCHĒ UI appear first (the menu offering Leaving / Continue)?
      "No — nothing at all, straight to the error"
    Q2, does the intervention complete without a "please choose a value" error?
      "'Please choose a value' again"
  implication: >
    CYCLE 5 REFUTED for symptom 1. The picker-axis fixes did not resolve it. Q1 settles the
    caveat the debugger correctly isolated: NO PROSOCHĒ UI appears at all, so the failure is
    UPSTREAM of the first OPEN menu — inside the region (actions 91-521) that the cycle-5
    sweep read exhaustively and pronounced statically clean.
    METHODOLOGICAL NOTE: the debugger flagged that "fails before any PROSOCHĒ UI appears" was
    an unverified INFERENCE carried by the coordinator and session-manager, not user
    testimony, and designed the single bit that would settle it. It returned opposite to what
    the fix required. This is falsification working as intended, not a wasted cycle.
    THE PICKER FIXES STAND. They were corpus-verified (11/11 and 33/33), are genuine latent
    defects on a path that will execute once this is unblocked, and the new guard caught a
    real second instance in the Sentient-only insertion path. Do NOT revert them merely
    because they did not fix this symptom.
    DIRECT CONTRADICTION TO RESOLVE: the sweep says 91-521 is clean; the device says something
    at or before that region has an unfilled required parameter. Both cannot be true.

- timestamp: 2026-08-14 (cycle 6)
  checked: "REPO STATE, before any analysis — which commit the working tree actually held"
  found: >
    At session start the tree was checked out at efb5a79 on branch codex/prosochedebug1, a
    commit predating ALL of cycles 1-5: grep for REQUIRED_PICKER_PARAMS, verify_required_pickers,
    normalise_string_envelopes, verify_string_envelopes, restructure_router, verify_router_shape,
    ACTION_OUTPUT_NAMES, BUILD_STAMP and ROUTER_TRACE returned 0 hits each in
    tools/build_state_engine.py, and artifacts/shortcuts/ held the 183703/187660-byte pre-cycle
    artifacts. The tree has since moved to branch codex/automation-parameter-diagnosis at 7ca8ebb,
    which carries all of it (BUILD_STAMP = "build 2026-08-14f", signed Dumb 188441 bytes,
    Dumb.xml 3674 actions) — matching the cycle-5 record exactly.
  implication: >
    NOT A CODE FINDING, but a live operational hazard worth more than most code findings: a
    rebuild performed while the tree sits on codex/prosochedebug1 or codex/round1 would silently
    regenerate a PRE-CYCLE-1 artifact, and all three original symptoms would return looking like
    a regression. Verify `git rev-parse --abbrev-ref HEAD` and the BUILD_STAMP value before any
    rebuild or re-sign. All cycle-6 analysis was run against blobs read out of 7ca8ebb rather
    than the working tree, so it is unaffected.

- timestamp: 2026-08-14 (cycle 6)
  checked: "The true extent of the OPEN pre-UI region, computed rather than assumed"
  found: >
    OPEN body = actions 91-1213 (GroupingIdentifier FA045F2B spans 90/1214/3673). There is NO
    UI action at the OPEN arm's base depth anywhere in the body — every OPEN-path UI is inside a
    conditional. Only three UI actions exist in the whole body: 169 (menu "Ice is active", depth
    2, reachable only through the live-cooldown conditional at 167), 521 (menu "PROSOCHĒ",
    items ["Leaving","Continue"]) and 669 (menu "Leave now").
  implication: >
    On a normal OPEN with no live cooldown the FIRST thing a user can see is action 521.
    "Nothing at all, straight to the error" therefore localises the failure to actions 91-520 —
    IF execution entered the OPEN arm at all. It is equally consistent with PROSOCHĒ never
    having run, which is the partition cycle 6 exists to settle. Cycle 5's 91-521 region was
    the right region.

- timestamp: 2026-08-14 (cycle 6)
  checked: "The FOURTH required-parameter axis, per the coordinator's priority (1) — what 'required parameter' can mean in the catalog beyond key name, value envelope and picker presence"
  found: >
    The catalog exposes NO required/optional bit at all. Parameter `flags` takes only four
    values across all 2585 tools — 0 (4658 params), 1 (3098, entity sort/compound query keys),
    2 (260, exclusively ShowWhenRun/OpenWhenRun) and 4 (68, exclusively AttributedString rich-text
    params). None of these encodes "required". A sweep therefore cannot enumerate required
    parameters from the catalog; it can only compare emitted keys against the full key list.
    Run that way over actions 91-520: ZERO empty-valued parameters of any shape, and the only
    absent catalog keys are round.TenToThePowerOf (not applicable at WFRoundTo='Ones Place'),
    getvalueforkey.WFGetDictionaryValueType, documentpicker.save.WFFolder,
    setitemname.WFDontIncludeFileExtension, getitemfromlist's index/range keys (correct for
    'First Item'), and math's scientific keys.
  implication: >
    The axis the coordinator predicted is REAL but it is a COVERAGE hole, not a defect: 336 of
    the OPEN body's actions are the control-flow family — conditional (263), choosefrommenu (53),
    repeat.each (18), repeat.count (2) — and NONE of those four identifiers exists in the ToolKit
    catalog at all. Every catalog-driven sweep, cycle 5's included, is structurally blind to all
    336. That fully explains how 91-520 can read "clean" and still fail, without requiring any
    new defect class.

- timestamp: 2026-08-14 (cycle 6)
  checked: "PICKER VALIDITY — a genuinely new axis: cycle 5 checked that required pickers are PRESENT and LITERAL, but never that the literal is a VALID enum case"
  found: >
    Every emitted picker literal in the artifact was validated against the catalog's enum case
    lists (both `id` and `title` forms). All 20 distinct literals are valid cases: getitemfromlist
    'Item At Index' (31) and 'First Item' (2), setvolume 'Media' (14), math '×' (12) '÷' (3) '-'
    (2), ask 'Text' (12) 'Number' (10) 'URL' (2), getdevicedetails 'Current Volume' (10) and
    'Current Brightness' (10), gettimebetweendates 'Seconds' (5), round 'Ones Place' (3) and
    'Always Round Down' (3), searchweb 'Google' (2), appendnote 'append' (2), adjustdate
    'Subtract', format.date 'Custom', text.changecase 'UPPERCASE', count 'Items'. ZERO invalid.
  implication: >
    A picker holding an INVALID case would render as an unfilled picker and produce the observed
    error exactly like a missing one, so this was a live candidate axis. It is now ELIMINATED.
    Worth keeping as a guard extension: verify_required_pickers() currently checks presence and
    literalness; validating the literal against the enum case list costs nothing and closes the
    axis permanently.

- timestamp: 2026-08-14 (cycle 6)
  checked: "Cycle 5's exoneration rule re-scored — 'the class also appears on the device-proven MANUAL path' vs 'that class actually EXECUTED'"
  found: >
    The only region certain to have executed is PRE (actions 0-89, which runs on every
    invocation), plus the specific manual cases the user drove: the menu, Change Sequence ->
    Classic, and Open Control Room. Re-scored against PRE alone, these shapes in the OPEN pre-UI
    region have NEVER run on device: conditional+WFNumberValue (13), math without WFMathOperation
    (13), math with WFMathOperation (3), setvalueforkey (29), number (5), number.random (1),
    round (1), repeat.count, repeat.each, appendvariable (2), getitemfromlist, returntohomescreen,
    setbrightness, setvolume.
  implication: >
    Cycle 5's exoneration was weaker than recorded — appearing on a branch is not executing on it,
    and the user exercised only a handful of manual cases. This does not overturn any cycle-5 fix,
    but it means the OPEN-path candidate set is larger than cycle 5 concluded, and it is why
    cycle 6 declines to nominate a fourth static hypothesis.

- timestamp: 2026-08-14 (cycle 6)
  checked: "Golden-corpus coverage for every construct still unverified on the guaranteed OPEN path"
  found: >
    is.workflow.actions.round — ZERO corpus instances. is.workflow.actions.number.random — ZERO.
    Across all 19 golden shortcuts EVERY conditional operand is a LITERAL: not one instance of a
    variable-backed WFNumberValue or WFConditionalActionString exists anywhere in the corpus
    (numeric operands appear 4 times, all literal floats; string operands 18 times, all literal
    strings). repeat.count's WFRepeatCount is a variable attachment 2/2 in the corpus where ours
    is the literal string '9' — though the `number` action shows numeric fields accepting plain
    strings ("0") and reals (10.0) interchangeably, so that is not itself suspicious.
    DEV-05 re-checked independently: the corpus is 1 math WITH WFMathOperation ('-', golden
    332c12a0 action 105) and 1 WITHOUT (golden 2e0fb675 action 21, our exact WFInput+WFMathOperand
    shape) — a 1-of-2 split, not the unanimous refutation cycle 5 recorded.
  implication: >
    The remaining plist-side candidates are genuinely UNDECIDABLE on the build Mac. The corpus has
    no coverage and the device has no execution history for any of them. Shipping a fix for one
    would be a fourth guess and would confound the probe by changing the artifact under test.
    This is why cycle 6 ships NO generator change and spends the round-trip on measurement.
    It also defines the donor request precisely: the constructs to have iOS serialise are a
    variable-vs-variable numeric If, a default-operation Calculate, a Round, a Random Number and
    a literal-count Repeat.

- timestamp: 2026-08-14 (cycle 6)
  checked: "PROBE 5 built, validated, signed and verified end-to-end on the SHIPPED file"
  found: >
    artifacts/device-import-probes/PROSOCHE Probe 5 - Input Echo.shortcut — AEA1 (41454131),
    22953 bytes, generated by artifacts/device-import-probes/build_probe5.py (never hand-written
    XML), plutil -lint OK, validator passes at --target-macos 26 --target-platform all.
    Decrypted via the §14 recipe and confirmed to carry: 7 actions
    [comment, comment, gettext, text.trimwhitespace, text.changecase, comment, alert],
    WFWorkflowHasShortcutInputVariables = true, WFWorkflowInputContentItemClasses =
    ['WFStringContentItem'], the ExtensionInput token as a WFTextTokenString, and an alert whose
    attachmentsByRange offsets {12,1} and {27,1} both land on real U+FFFC placeholders.
  implication: >
    The normalisation chain is copied in shape from PROSOCHĒ's device-proven actions 84-86
    (same envelopes, same producing-action output names 'Text' and 'Trimmed Text'), and the two
    root keys that govern input handoff are identical to PROSOCHĒ's — so a null result cannot be
    dismissed as "the probe declares its input differently". Pass/fail is read as literal
    characters inside brackets, so it does not depend on the user judging whether a UI field
    looks populated, which was the explicit weakness of the cycle-4 refutation.

- timestamp: 2026-08-14 (cycle 7)
  checked: "DONOR 3 decrypted — .planning/debug/'Donor 3.shortcut' (AEA1, 22907 bytes, built in Shortcuts.app on the target iPhone and exported). 13 actions. Decrypted with the §14 recipe; raw plist retained at scratchpad d3/donor3.xml."
  found: >
    iOS's OWN serialization for the five constructs that had ZERO corpus and ZERO device coverage:
    (1) VARIABLE-BACKED WFNumberValue, conditional cond 2 (A > B):
        WFInput  = {"Type":"Variable","Variable":{"Value":{"Type":"Variable","VariableName":"A"},
                    "WFSerializationType":"WFTextTokenAttachment"}}
        WFNumberValue = {"Value":{"Type":"Variable","VariableName":"B"},
                    "WFSerializationType":"WFTextTokenAttachment"}
        Our if_block() emits BYTE-IDENTICAL shapes via variable().
    (2) MATH AT DEFAULT OPERATION: WFInput + WFMathOperand, both bare WFTextTokenAttachment,
        and WFMathOperation ABSENT ENTIRELY. Ours is byte-identical.
    (3) ROUND: WFInput bare attachment + WFRoundMode "Always Round Down", WFRoundTo ABSENT
        (left at its default). Ours emits both, i.e. an explicit valid default — a superset.
    (4) NUMBER.RANDOM: WFRandomNumberMinimum "1" and WFRandomNumberMaximum "100", both as
        plist <string>. Ours emits <integer>.
    (5) REPEAT.COUNT: WFRepeatCount as plist <real> 9. Ours emits <integer>.
    Also: is.workflow.actions.number emits WFNumberActionNumber as <string> "5"; an alert with a
    completely EMPTY parameter dict is legal; device WFWorkflowClientVersion is "4711".
  implication: >
    The donor did its work by ELIMINATING, which is the more valuable outcome here. The top TWO
    ranked cycle-6 candidates (A1 variable-backed WFNumberValue, A3 math WFMathOperation omitted)
    are refuted against ground truth from the target device, and A2's round half is exonerated.
    DEV-05 IS SETTLED AFFIRMATIVELY: omitting WFMathOperation at the default operation is what iOS
    itself does, upgrading it from "corpus 1-of-2" to device-proven. What survives is a genuinely
    NEW axis — the plist SCALAR TYPE of numeric literals — see the next entry.

- timestamp: 2026-08-14 (cycle 7)
  checked: "SCALAR-TYPE AXIS (a fourth axis, and the first one cycle 6 predicted would exist): plist type of every numeric literal parameter, swept across both forks by region, cross-checked against the 19-shortcut golden corpus and Donor 3."
  found: >
    NEITHER the golden corpus NOR the device donor EVER serializes these fields as plist <integer>.
    Corpus: conditional.WFNumberValue 4/4 <real>; number.WFNumberActionNumber 2 <real> / 1 <string>
    / 2 attachment; repeat.count.WFRepeatCount 2/2 attachment (no literal instance anywhere).
    Donor: number.random min/max <string>; repeat.count <real>; number <string>.
    Our artifact emits <integer> at 78 sites. BUT the axis has PERFECT SEPARATION against the
    device-proven MANUAL path, which is the discriminator that settled cycles 2, 4 and 5:
      - number.WFNumberActionNumber <integer> — action 1359 sits inside the menu case "Open Control
        Room", which the user EXERCISED SUCCESSFULLY (the note refresh ran). DEVICE-PROVEN OK.
      - conditional.WFNumberValue <integer> — actions 3646 and 3653 sit in the Control Room refresh
        block (3620-3666) that ran on the same successful pass. DEVICE-PROVEN OK.
      - EXACTLY TWO <integer> sites are uniquely OPEN, have zero corpus precedent, zero device
        coverage, AND a donor that says iOS writes them differently:
          action 418  is.workflow.actions.number.random  WFRandomNumberMinimum/Maximum  (donor: <string>)
          action 454  is.workflow.actions.repeat.count   WFRepeatCount = 9              (donor: <real>)
        Both sit inside the pre-UI region 91-520 that the device implicates. (build-f indices)
  implication: >
    This is a ranked, falsifiable PREDICTION, not a fix to ship. Three static "confirmations" have
    been refuted on device this session, and the cycle-7 instruction is explicit that a donor-derived
    defect is a candidate for the bisection to confirm, never a blind ship. The bisection is therefore
    built so breadcrumb G immediately precedes Random Number and breadcrumb H immediately follows the
    session/gravity/pressure block: span G->H isolates suspect 1 and span H->I isolates suspect 2.
    A last-letter of G or H confirms the prediction; ANY other letter kills it. Nothing was changed.

- timestamp: 2026-08-14 (cycle 7)
  checked: "BISECTION INSTRUMENT built, validated, signed, and verified INSIDE the shipped signed file by decryption."
  found: >
    artifacts/shortcuts/'PROSOCHĒ — Nine Circles — Dumb.shortcut' — AEA1 (41454131), 188667 bytes,
    3684 actions, stamp 'build 2026-08-14g' present and '14f' verified ABSENT. Sentient rebuilt and
    re-signed identically (192807 bytes). Validator passes for BOTH forks at --target-macos 26
    --target-platform all; plutil -lint OK. (--target-platform ios still rejects every action
    indiscriminately including is.workflow.actions.comment — DEV-01, unchanged tooling noise.)
    Ten breadcrumbs land at actions 92 A, 147 B, 168 C, 286 D, 306 E, 415 F, 424 G, 458 H, 473 I,
    527 J; the first OPEN menu (terminal signal) is action 531.
    Span sizes and nesting, computed from the artifact rather than asserted:
      A->B  54 actions, 0 nested blocks (flat state+config reads)
      B->C  20 actions, 2 nested blocks, depth 2 (behavioural-day rollover)
      C->D 117 actions, 11 nested blocks, depth 4 (cooldown: live-Ice menu + Ice-expiry restore)
      D->E  19 actions, 3 nested blocks, depth 2 (duplicate-OPEN debounce)
      E->F 108 actions, 11 nested blocks, depth 4 (whole ordered Heat pipeline)
      F->G   8 actions, 0 nested blocks (opens-today math + 3 dictionary writes)
      G->H  33 actions, 1 nested block  — CONTAINS number.random (suspect 1)
      H->I  14 actions, 2 nested blocks — CONTAINS repeat.count (suspect 2)
      I->J  53 actions, 3 nested blocks, depth 3 (pending-exit, 2 repeat-each loops)
      J->menu 3 actions, 0 nested blocks (Save File only)
  implication: >
    ONE pass does NOT localise to a single action for spans C, E and I — each carries 3-11 nested
    blocks up to depth 4, so a last-letter of C, E or I requires a SECOND, finer bisection round
    inside that span. This is stated rather than glossed, per the cycle-7 instruction. Spans A, F,
    G, H and J are small or flat enough to localise effectively immediately.
    PRESERVATION IS PROVEN, NOT ASSERTED: with the 10 breadcrumb alerts removed, build g is
    byte-identical to build f across all 3674 actions except exactly two — both the BUILD_STAMP
    display string ('14f'->'14g') at actions 1350 and 1354, both on the MANUAL arm. breadcrumb()
    calls no uid(), so the deterministic UUID counter never advances and every downstream action
    keeps the UUID it had in build f. Symptoms 2 and 3 are therefore preserved BY CONSTRUCTION.
    The breadcrumb alert introduces NO inferred parameter shape: plain-string WFAlertActionTitle is
    device-proven (the cycle-3 ROUTER TRACE alert displayed on device) and plain-string
    WFAlertActionMessage is corpus-verified in 5 of the 13 golden-corpus alerts. It references no
    variable and contains no control flow, so it cannot fail for a reason of its own.

- timestamp: 2026-08-14 (cycle 7 result)
  checked: "TEN-LETTER BISECTION on device, build 2026-08-14g. Ten flag-gated breadcrumb alerts A-J at OPEN-arm base depth. User-reported, verbatim."
  found: '"B. Same error."'
  implication: >
    LOCALISED TO SPAN B->C: 20 actions, nesting depth 2, the DAY-ROLLOVER section.
    Breadcrumb B was seen; C was not. Execution reached B and died before reaching C, still
    producing "Please choose a value for each parameter in this action".
    BEST-CASE OUTCOME the protocol allowed. B->C is the second-smallest span and is NOT one of
    the C/E/I spans that would have bought only a region. NO SECOND BISECTION ROUND NEEDED —
    20 actions at depth 2 is directly readable.
    THE DONOR-DERIVED PREDICTION IS DEAD. Both nominated suspects — number.random (action 418,
    span G->H) and repeat.count (action 454, span H->I) — sit hundreds of actions DOWNSTREAM of
    where execution stopped. They cannot be the cause. Cycle 7's own stated criterion was that
    any letter other than G or H kills the prediction; B does.
    UNSTAGE THE DEFERRAL: the two <integer> sites at 418/454 no longer need holding back to
    keep a measurement clean, because the measurement is COMPLETE. Decide them on their merits
    — donor evidence says iOS writes <string> and <real> there while we write <integer>, so
    they are plausibly real LATENT defects on a path that has never executed. They are NOT
    this bug and must not be described as a fix for it.
    DO NOT CONCLUDE THE <integer> AXIS IS EXONERATED. Cycle 7 cleared two PARTICULAR sites
    because they had demonstrably executed on device, and nominated two others by elimination.
    A THIRD site inside B->C would be entirely consistent with everything established and
    would now carry the strongest possible evidence. The day-rollover section is exactly where
    date arithmetic and numeric comparison live.

- timestamp: 2026-08-14 (cycle 8 addendum)
  checked: "SIX USER SCREENSHOTS (.planning/debug/IMG_5624.jpg .. IMG_5629.jpg, 15:38-15:40) — first UI-level evidence in the session. Cross-checked by session-manager against the 25 sites fixed in cycle 8."
  found: >
    User, verbatim: "I can eyeball the shortcut and see that a few of the if operators are red,
    so not accepted. you can't do is greater than or is less than."
    Five distinct If actions render their OPERATOR IN RED (invalid): Cooldown Until >,
    Previous Declared Duration >, Previous Overrun >, Heat Clamped >, Stats Count <. All five
    operand chips are orange-x named variables. The operator picker, opened on four of the
    five, offers EXACTLY EIGHT options — is / is not / has any value / does not have any value
    / contains / does not contain / begins with / ends with. NO numeric comparator appears.
    SESSION-MANAGER CROSS-CHECK (programmatic, plistlib, pre-fix vs post-fix Dumb):
    - The 25 cycle-8 sites carry condition codes 4, 5 and 99 ONLY — all STRING conditions.
      Their variables are Stored Day, Exit/Contract/Session Owner IDs, counters and flags.
    - The five red Ifs map to actions 170, 377, 384, 409, 579, all with NUMERIC codes
      (2 = is greater than, 0 = is less than).
    - NONE of the five is among the 25. Zero overlap.
    - All 87 numeric-code conditionals in the POST-FIX build already carry the correct
      ser=WFTextTokenAttachment envelope with WFNumberValue present.
  implication: >
    THE UNIFICATION HYPOTHESIS IS REFUTED. The red operators are NOT the visible symptom of
    the cycle-8 envelope defect. They are a SECOND, GENUINELY DISTINCT defect on the
    operator/operand-TYPE axis — a FIFTH axis for this session. Per the coordinator's own
    stated criterion ("if any of the five is NOT among your 25, that site is a distinct defect
    and you have found it for free"), all five qualify.
    MECHANISM (well-supported, not yet device-confirmed): the operand variables are TEXT-typed
    — image 1's own comment says the cooldown deadline is "routed through text". Shortcuts
    types the operand as text, a text-typed operand offers only the eight STRING operators, so
    the numeric comparator the plist specifies has no valid case to render and shows red.
    Donor 3 is the contrast case: it fed its operands from NUMBER actions and the numeric
    comparators rendered correctly with the identical envelope — which is exactly why the
    envelope check passes here while the UI still rejects the operator.
    .claude/CLAUDE.md anticipated this trap for EQUALITY ("there is no numeric-equals code;
    use string code 4 on text-coerced numbers") but the generator walked into it for ORDERING
    comparisons.
    KEY PREDICTION FOR THE BUILD-h DEVICE TEST: action 170 (Cooldown Until >) is the FIRST red
    site and sits immediately after breadcrumb C. The cycle-8 fix should carry execution past
    149/158 and reach C — then fail at 170. EXPECT THE LETTER TO ADVANCE FROM B TO C. That is
    progress plus a new location, not a failed fix. "B again" would instead mean the cycle-8
    fix did not take.
    NEW EVIDENCE CHANNEL, first-class: operator/operand-TYPE validity is visible in the
    Shortcuts UI and INVISIBLE in the plist file. Every static sweep in eight cycles was blind
    to it by construction. The on-device eyeball is not a nicety here — it is the only
    instrument that can see this defect class.
    NOT FIXED THIS CYCLE, deliberately: shipping a speculative fix now would confound the
    letter measurement already in flight.

- timestamp: 2026-08-14 (cycle 8 device result)
  checked: "ON-DEVICE test of build 2026-08-14h (cycle-8 WFInput.Variable envelope fix, 25 sites/fork). Clean install + automation re-point. User-reported, verbatim."
  found: '"ok, I ran build h and got to C, then same error."'
  implication: >
    CYCLE-8 FIX CONFIRMED ON DEVICE. The letter ADVANCED from B to C, so execution now passes
    actions 149 and 158 — the two WFInput.Variable text-template sites. Symptom 1's FIRST
    defect is device-verified, not merely statically argued.
    TWO INDEPENDENT PREDICTIONS BOTH LANDED IN ONE RUN:
      (1) the letter would advance from B to C rather than repeat B, with "B again" stated in
          advance as meaning the envelope fix had not taken. It advanced.
      (2) the next failure would be at ACTION 170 — the first numeric-operator-on-text-operand
          site — which sits immediately after breadcrumb C. The run reached C and then failed.
    RETROACTIVELY CONFIRMS THE REFUTATION OF THE UNIFICATION HYPOTHESIS. If the red operators
    had been a mere rendering artefact of the envelope defect, fixing 149/158 would have
    carried execution well past 170. It did not. The two defects are genuinely distinct, as the
    programmatic cross-check found, and the user's screenshots identified a real second cause
    that no static sweep could have seen.
    THE BISECTION MEASUREMENT IS NOW COMPLETE. The confounding argument that withheld the
    numeric-operator fix for two cycles no longer applies.

- timestamp: 2026-08-14 (session-manager provenance trace)
  checked: "Operand provenance for ALL 87 (Dumb) / 94 (Sentient) numeric-condition-code conditionals, traced Set Variable -> feeding action via OutputUUID."
  found: >
    DEFECTIVE — operand fed by `gettext` (text-coerced): 18 per fork.
      Dumb:     170, 377, 384, 409, 579, 1187, 1260, 1300, 1443, 1658, 1890, 2122, 2354,
                2586, 2818, 3050, 3282, 3514
      Sentient: 172, 379, 386, 411, 581, 1255, 1328, 1368, 1511, 1726, 1958, 2190, 2422,
                2654, 2886, 3118, 3350, 3582
      Eight distinct variables: Cooldown Until, Declared Duration, Heat Clamped, Manual Voice,
      Previous Declared Duration, Previous Overrun, Stats Count, Voice Enabled.
    NOT DEFECTIVE:
      40 fed by getdevicedetails — only two distinct sources, 'Current Volume' and
         'Current Brightness', both numeric.
      10 fed by ask — the numerically-compared one is action 1079, WFInputType='Number'.
      13 fed by number / math / gettimebetweendates / round — genuinely numeric.
       4 Repeat Index — built-in numeric.
       1 calculateexpression; 1 Heat After Contract (fed by math at 380).
  implication: >
    THE FIX SIZE IS 18 PER FORK — not 87, and not the 6 visible by eye.
    ALL SIX PHOTOGRAPHED RED SITES FALL INSIDE THE 18, AND ZERO FALL OUTSIDE IT. Voice Enabled
    — the site that broke the "five" sample — is fed by gettext at action 1184, so it was
    always in this bucket. Six-for-six correspondence between the classifier and independent
    UI evidence.
    Confirms the user's instinct exactly: there were more than five, the visual sample was not
    exhaustive, and the rest are unfixed.
    ROUTING TENSION TO SETTLE BEFORE FIXING: all 18 are dictionary values routed through Text —
    and that routing exists deliberately, because .claude/CLAUDE.md warns that a Dictionary
    Value compared directly in an If renders blank. So "replace Text with Number" is the very
    substitution the project docs caution against, and Donor 3 does NOT cover it (its operands
    came from Number actions, not dictionary values). Needs a donor or corpus proof.

- timestamp: 2026-08-14 (cycle 9)
  checked: "THE ROUTING TENSION the cycle-9 objective required settling before any fix: all 18 defective operands are dictionary values routed through Text, and that routing exists deliberately per .claude/CLAUDE.md. Searched the golden corpus first, then received Donor 4 / Donor 4.1 built on the target iPhone."
  found: >
    SETTLED, AND BY DEVICE EVIDENCE RATHER THAN INFERENCE.
    Donor 4.1 (.planning/debug/"Donor 4.1.shortcut", built in Shortcuts.app on the target
    iPhone, decrypted with the BUILD-NOTES §14 recipe) is EXACTLY the construct in question —
    a Get Dictionary Value output compared numerically:
      0  dictionary            {"heat": "42"}
      1  getvalueforkey        key "heat"          -> output "Dictionary Value"
      2  conditional  WFCondition 2, WFNumberValue "10",
         WFInput = {"Type":"Variable","Variable":{"Value":{
             "Type":"ActionOutput","OutputName":"Dictionary Value","OutputUUID":"...",
             "Aggrandizements":[{"Type":"WFCoercionVariableAggrandizement",
                                 "CoercionItemClass":"WFNumberContentItem"}]},
           "WFSerializationType":"WFTextTokenAttachment"}}
    iOS INSERTS NO Number ACTION AND CHANGES NO READ CHAIN. It types the variable reference in
    place, with a coercion aggrandizement, in the conditional's own input slot.
    THE CONTROL CASE IS THE SAME SHORTCUT ONE STEP EARLIER. Donor 4 has the identical
    descriptor with NO Aggrandizements and a code-100 test. The only delta between the two
    donors is the coercion plus the numeric condition, which isolates the coercion as the thing
    that makes a numeric operator legal on a dictionary value.
    THE UI ACTION IS PHOTOGRAPHED: IMG_5636.jpg is the type list for a "Dictionary Value"
    chip — Contact / Date / Dictionary / ... / NUMBER / PDF. Choosing Number emitted the
    aggrandizement. The fix is the plist form of a tap the user made and recorded.
    CORPUS CROSS-CHECK, needed because our operands are NAMED VARIABLES rather than raw
    ActionOutputs: golden 332c12a0060043b388b22b806be7ab58 carries
    WFCoercionVariableAggrandizement on both {Type: Variable, VariableName: ...} and
    {Type: ActionOutput, ...} descriptors (24 instances corpus-wide). The aggrandizement is a
    property of the descriptor, not of the ActionOutput form.
  implication: >
    THE TENSION DISSOLVES WITHOUT TOUCHING THE TEXT HOP AT ALL. The .claude/CLAUDE.md rule —
    materialise a Dictionary Value before comparing it — is not challenged by this fix, because
    the read chain is untouched. What was missing was never the materialisation; it was the
    TYPE DECLARATION on the reference at the point of comparison.
    None of the four candidate shapes the cycle-9 objective listed is what iOS does. It is the
    fifth, "something else iOS does that none of us has predicted" — which is precisely why the
    donor was worth having and why guessing between the four would have cost a device round trip.

- timestamp: 2026-08-14 (cycle 9)
  checked: "A FIRST FIX WAS BUILT, VALIDATED, SIGNED AND THEN DISCARDED. Recorded because the discard is the methodologically load-bearing part, not the build."
  found: >
    Before the donors arrived, the fix was composed from corpus evidence alone: golden
    2e0fb675e45948aaacee7e534f910492 actions 12->13->15 feed a Get Dictionary Value STRAIGHT
    into is.workflow.actions.number and consume the "Number" output in a numeric slot. A
    read_number() helper was written on that basis — Get Dictionary Value -> Number action ->
    Set Variable, with a WFCondition-100 null guard because cooldown_until is JSON null on a
    fresh state.json. It passed the new invariant, validated, signed, and measured clean:
    zero text-fed operands in both forks.
    It was discarded anyway when Donor 4.1 showed iOS doing something different for this exact
    construct.
  implication: >
    DEVICE EVIDENCE OUTRANKS CORPUS COMPOSITION, and this is the fourth time that ordering has
    mattered in this session. The corpus construct is REAL — it is the shape for materialising
    a number into the data flow — but it is not the shape for TYPING A CONDITIONAL OPERAND, and
    composing two separately-evidenced links into an unobserved chain is inference, not evidence.
    The coercion is additionally better on every axis that matters here: it adds NO actions, so
    breadcrumb positions survive and the next device report is directly comparable with the
    last; it leaves every device-proven read chain byte-identical; and it removes the one
    unevidenced link the discarded design carried, namely what a Number action does when handed
    a JSON null. That last point converts a two-condition AND-gate at action 170 into one
    condition.

- timestamp: 2026-08-14 (cycle 9 build)
  checked: "Build 2026-08-14i produced, validated, signed, and verified INSIDE THE SHIPPED SIGNED FILE by decryption (BUILD-NOTES §14 recipe), not read back from the build tree."
  found: >
    Dumb signed artifact decrypted: 3684 actions; 87 numeric conditionals; 20 Number-coerced;
    ZERO text-fed-and-uncoerced. Action 170 — the exact site that killed build h — now reads
    WFInput.Variable.Value = {VariableName: "Cooldown Until", Type: "Variable",
    Aggrandizements: [{Type: WFCoercionVariableAggrandizement,
    CoercionItemClass: WFNumberContentItem}]}. Stamp "build 2026-08-14i" x2, zero stale "h".
    10 breadcrumbs, ROUTER TRACE present, 147 setvalueforkey actions. AEA1 magic confirmed.
    Sentient: 3752 actions, 94 numeric conditionals, 25 coerced, zero uncoerced.
    Both forks pass validate-shortcut --target-macos 26.
    SYMPTOMS 2 AND 3 PRESERVED BY CONSTRUCTION, and this cycle the proof is total rather than
    class-by-class. A whole-artifact action-by-action comparison against build h — the build the
    user tested hours ago — gives: action counts IDENTICAL (3684 = 3684); exactly 22 actions
    differ; 20 of them are conditionals whose ONLY delta is the added Aggrandizements key (each
    verified by deleting that key and confirming byte-equality with build h); the remaining 2
    are the BUILD_STAMP display strings. Every other action in the artifact — all 3662 of them,
    including all 147 Set Dictionary Value actions and the entire Notes family — is BYTE-
    IDENTICAL to the build that device-confirmed symptoms 2 and 3.
    BREADCRUMB POSITIONS ARE UNCHANGED from build h: A=92, B=147, C=168, D=286, E=306, F=415,
    G=424, H=458, I=473, J=527.
  implication: >
    This is the cleanest single-variable experiment of the session. A "C again" result cannot be
    attributed to collateral change, because there is none: the artifact differs from the one
    the user just ran by 20 type declarations and two display strings. And because no actions
    were added, the letter the user reports next is directly comparable with the letter they
    reported last, with no re-indexing.

- timestamp: 2026-08-14 (cycle 9, carried-forward candidates)
  checked: "The three fold-in candidates, checked against the artifact. Cheap analysis only — NONE was fixed this cycle, deliberately, because any unmeasured change would confound the build-i letter measurement now in flight."
  found: >
    (b) 'Spoken This Run' — NOT A DEFECT, a cheap elimination rather than a deferral. The tests
        use WFCondition 101 ("does not have any value"), not a positive test:
        `if Spoken This Run does not have any value -> speak -> set Spoken This Run`. Six
        instances, each with its Set Variable immediately inside its own body. That is the
        CORRECT once-per-run latch idiom — unset on the first Circle so the branch runs, set
        thereafter so it does not. The reported concern ("it can never be available at its own
        test") is exactly the intended precondition.
    (a) 'Session ID' — REAL, SAFETY-RELEVANT, AND LARGER THAN REPORTED. Control-flow ancestry
        walk: Session ID is set once, at action 460, ancestry [90 OPEN, 177 not-in-cooldown,
        316 genuine-open]. Of the twenty `settings_snapshot.*.changed_by_session_id` writes,
        only TWO share that ancestry. The other EIGHTEEN sit under a different depth-1 branch
        (1279, not 177) on which Session ID is never assigned at all — so every
        brightness/volume snapshot taken outside the genuine-OPEN dispatch records an EMPTY
        owner, and the ownership check guarding restore cannot match it. Eighteen sites, not
        the three originally noted.
    (c) The variable-bearing WFItems List shape — SETTLED BY THE SAME DONORS, and our shape is
        WRONG. Donor 4 / 4.1 action 5 is a List whose WFItems mixes bare strings with a
        variable-bearing entry, and iOS WRAPS that entry:
          WFItems: ["Circle",
                    {"WFItemType": 0, "WFValue": {"Value": {"string": "\\ufffc",
                       "attachmentsByRange": {...}},
                     "WFSerializationType": "WFTextTokenString"}},
                    "follows"]
        Our artifact puts the {Value, WFSerializationType} object in the array DIRECTLY, with
        no {WFItemType, WFValue} wrapper. That is the shape the cycle-8 addendum recorded as
        matching neither golden List action; it does not match the device donor's shape either,
        and there is now a device precedent to conform to.
  implication: >
    (b) is closed at zero cost and removes a false lead from the board.
    (a) is the next non-blocking work item and should be fixed in its own cycle, where it can be
    measured alone. Fixing it now would put an unmeasured semantic change into the artifact
    whose letter result is the entire point of the next device sitting.
    (c) now has a device shape to conform to and no longer needs a donor request. It sits past
    breadcrumb J so it cannot affect this measurement; fix it alongside (a).

## Eliminated

- hypothesis: "'Spoken This Run' is defective because the If that tests it can never see it — its only Set Variable sits inside that If's own body."
  evidence: "The tests use WFCondition 101 ('does not have any value'), not a positive test. `if not set -> speak -> set` is the correct once-per-run latch: unset on the first Circle so the branch runs, set thereafter so it does not. Six instances, all identical. Checked against the rebuilt artifact at actions 1242/1748/2001/2254/2507/2760."
  timestamp: 2026-08-14 (cycle 9)

- hypothesis: "Fixing a numeric operand requires REPLACING the Text materialisation — either with a Number action or by restructuring the comparison — which is the substitution .claude/CLAUDE.md cautions against, so the Text hop and the numeric comparison are in genuine conflict."
  evidence: "Donor 4.1, built on the target iPhone and decrypted 2026-08-14: iOS neither replaces nor adds a materialising action. It attaches a WFCoercionVariableAggrandizement (CoercionItemClass WFNumberContentItem) to the variable reference IN THE CONDITIONAL'S OWN INPUT SLOT, leaving the read chain untouched. Donor 4 is the same shortcut before the type was set and carries the identical descriptor with no Aggrandizements, isolating the coercion as the operative difference. There was never a conflict: the missing thing was a TYPE DECLARATION on the reference, not a different materialiser. None of the four candidate shapes considered was correct."
  timestamp: 2026-08-14 (cycle 9)

- hypothesis: "The construct 'dictionary value fed into a numeric comparison' has zero coverage in the corpus, the catalog, or any existing donor, so it cannot be resolved without requesting a new one."
  evidence: "Partially wrong on the corpus and fully resolved by donor. Golden 2e0fb675e45948aaacee7e534f910492 actions 12->13->15 DOES feed a Get Dictionary Value output straight into is.workflow.actions.number — that construct was always covered; prior sweeps searched the corpus for CONDITIONALS when the evidence sat one action upstream in how the OPERAND was produced. It is nonetheless the wrong construct for this problem: it materialises a number into the data flow, whereas the conditional needs its reference TYPED. Donor 4.1 settles the actual construct on device."
  timestamp: 2026-08-14 (cycle 9)

- hypothesis: "The five red If operators seen in the user's screenshots are the visible symptom of the cycle-8 WFInput.Variable envelope defect — an unresolvable input cannot be typed, so Shortcuts falls back to offering only the eight string operators and the numeric comparator renders red. (Unification: one defect, two presentations.)"
  evidence: "Session-manager programmatic cross-check: the 25 cycle-8 sites carry ONLY string condition codes (4, 5, 99) with variables Stored Day / Owner IDs / counters. The five red Ifs are actions 170, 377, 384, 409, 579 with NUMERIC codes (0, 2) and entirely different variables. Zero overlap. Furthermore all 87 numeric-code conditionals in the POST-FIX build already carry the correct WFTextTokenAttachment envelope, so the envelope fix cannot be what makes them render — they were never envelope-defective."
  timestamp: 2026-08-14 (cycle 8 addendum)

- hypothesis: "The failing OPEN-path action is one of the two donor-contradicted <integer> literal sites — number.random (action 418) or the nine-step repeat.count (action 454) — where iOS writes <string> and <real> respectively."
  evidence: "Cycle 7 bisection, build 2026-08-14g: the user's last breadcrumb was B, so execution died in span B->C (actions ~145-165). Actions 418 and 454 sit in spans G->H and H->I, hundreds of actions downstream, and were never reached. Killed by cycle 7's own pre-stated criterion (only G or H would have confirmed). Retained as candidate LATENT defects, not as this bug."
  timestamp: 2026-08-14 (cycle 7 result)

- hypothesis: "A variable-backed WFNumberValue on a conditional resolves as an unfilled number field on the OPEN path (cycle 6's #1 ranked candidate A1; 13 sites, first on the guaranteed path, ZERO corpus precedent anywhere)."
  evidence: "Donor 3, built in Shortcuts.app on the target iPhone and decrypted 2026-08-14: iOS serializes a variable-vs-variable numeric If as WFInput {Type:Variable, Variable:<bare WFTextTokenAttachment>} plus WFNumberValue as a bare WFTextTokenAttachment. Our if_block()/variable() emit byte-identical shapes. Device ground truth, outranking every catalog and corpus inference."
  timestamp: 2026-08-14 (cycle 7)

- hypothesis: "math with WFMathOperation omitted for '+' is a missing required picker on the OPEN Heat path (DEV-05; cycle 5 called it refuted on corpus evidence, cycle 6 re-scored it as a weak 1-of-2 split and left it open)."
  evidence: "Donor 3: a Calculate action left at its DEFAULT operation carries WFInput + WFMathOperand as bare attachments and omits WFMathOperation ENTIRELY. Omitting it is what iOS itself does. DEV-05 is settled affirmatively on device evidence and the generator needs no change."
  timestamp: 2026-08-14 (cycle 7)

- hypothesis: "is.workflow.actions.round carries a defective parameter shape on the OPEN path (cycle 6 candidate A2, zero corpus instances)."
  evidence: "Donor 3: WFInput bare attachment + WFRoundMode literal, with WFRoundTo simply absent because it was left at its default. Ours emits the same WFInput and WFRoundMode plus an explicit, catalog-valid WFRoundTo 'Ones Place' — a superset of the device shape, not a divergence."
  timestamp: 2026-08-14 (cycle 7)

- hypothesis: "The plist SCALAR TYPE of numeric literals (<integer> where iOS writes <real> or <string>) is broadly responsible — 78 sites across both forks, and NEITHER the golden corpus NOR the device donor ever writes <integer>."
  evidence: "PARTIALLY eliminated, and the surviving remainder is this cycle's ranked prediction. Refuted for the two classes with device coverage: number.WFNumberActionNumber <integer> at action 1359 ran inside the device-exercised 'Open Control Room' menu case, and conditional.WFNumberValue <integer> at actions 3646/3653 ran in the Control Room refresh block on the same successful pass. Both are DEVICE-PROVEN to execute as <integer>. Survives ONLY at the two uniquely-OPEN, zero-precedent sites: number.random (418) and repeat.count (454) — deliberately NOT fixed, and bracketed by breadcrumbs G/H so the bisection confirms or kills it."
  timestamp: 2026-08-14 (cycle 7)

- hypothesis: "The Personal Automation WRAPPER is at fault — the Text action, the Run Shortcut handoff, the trigger configuration, or the input declaration fails to deliver `OPEN` to PROSOCHĒ. (Shadowed the session from cycle 1; the INPUT PROBE was designed in cycle 1 to test it and then deferred five times.)"
  evidence: "Cycle 6 device pass, step 1: Probe 5 — carrying an input declaration identical to PROSOCHĒ's (WFWorkflowHasShortcutInputVariables=true, WFWorkflowInputContentItemClasses=['WFStringContentItem']) and a normalisation chain copied from its device-proven actions 84-86 — received RAW [OPEN] / NORMALISED [OPEN] through the UNMODIFIED wrapper. Handoff proven end to end; the result transfers to PROSOCHĒ."
  timestamp: 2026-08-14 (cycle 6)

- hypothesis: "The wrapper's stored Run Shortcut reference is STALE — the chip renders from a cached name while the underlying target points at a deleted install — which would explain the error with no plist defect at all."
  evidence: "Cycle 6 device pass, step 2: PROSOCHĒ re-selected FRESH from the list (rewriting the stored reference) moments after the probe ran successfully through the same wrapper — identical 'Please choose a value' error. Refuted on stored-representation evidence rather than UI rendering, which the file had flagged as the weaker channel."
  timestamp: 2026-08-14 (cycle 6)

- hypothesis: "Symptom 1 is caused by a picker parameter holding an INVALID enum case (as opposed to a missing or non-literal one) somewhere on the OPEN path — which would render an unfilled picker and produce the identical error."
  evidence: "Cycle 6 validated every emitted picker literal in both forks against the ToolKit catalog's enum CASE lists (id and title forms). All 20 distinct literals are valid cases; zero invalid. Checked because cycle 5's REQUIRED_PICKER_PARAMS guard tests presence and literalness only, so an invalid literal would have passed it silently."
  timestamp: 2026-08-14 (cycle 6)

- hypothesis: "A FOURTH required-parameter axis exists in the catalog that cycle 5's sweep did not model — required content-item inputs, required entity/app references, required quantity fields, or anything carrying a non-optional flag."
  evidence: "The ToolKit catalog exposes no required/optional bit at all: parameter `flags` takes only 0, 1 (entity sort/compound query keys), 2 (ShowWhenRun/OpenWhenRun) and 4 (AttributedString rich text) across all 2585 tools. Re-sweeping 91-520 against the FULL catalog key list finds zero empty-valued parameters and no unexplained absent keys. PARTIALLY REPLACED rather than simply eliminated: the real gap is coverage, not axis — 336 OPEN-body actions are the control-flow family (conditional, choosefrommenu, repeat.each, repeat.count) and none of those identifiers exists in the catalog, so every catalog-driven sweep is blind to them."
  timestamp: 2026-08-14 (cycle 6)

- hypothesis: "Symptom 1 is caused by a required PICKER/ENUM parameter left unfilled on the OPEN path (count.WFCountType missing; getitemfromlist.WFItemSpecifier holding a variable token instead of a literal + WFItemIndex)."
  evidence: "Device test 2026-08-14 build f: both sites corpus-verified and fixed, shipped artifact decrypted and confirmed to carry them — yet the automation still fails identically, and Q1 established NO PROSOCHĒ UI appears at all, so execution never even reaches the fixed sites (both sit after the first OPEN menu). Refuted as the cause of symptom 1; the fixes are RETAINED as genuine latent defects."
  timestamp: 2026-08-14

- hypothesis: "Symptom 1's automation failure is caused by an ORPHANED Run Shortcut reference — deleting the installed shortcut for each clean install cleared the wrapper's target Shortcut field, and a Run Shortcut with no target produces exactly 'please choose a value for each parameter in this action'."
  evidence: "Device test 2026-08-14 build e: user inspected the Run Shortcut action directly; both the Shortcut and Input fields were populated, and the automation still failed with the identical error. NOTE: refuted on UI inspection, which is weaker than stored-representation evidence — see caveat (i)."
  timestamp: 2026-08-14

- hypothesis: "Symptom 3 (empty Control Room note) is the same value-envelope defect as symptom 2, manifesting on the Notes action family."
  evidence: "Device test 2026-08-14 build d: in ONE run on a clean install, the envelope fix demonstrably worked for Set Dictionary Value (symptom 2 passed, no 'No value provided') while the Control Room note was still created empty. Same build, same envelope treatment, opposite outcomes."
  timestamp: 2026-08-14
  RETRACTED: 2026-08-14 (cycle 4) — the phrase "same envelope treatment" was FALSE and is
    what made this elimination look decisive. Neither Notes body parameter was ever given the
    envelope treatment: the cycle-2 allowlist keyed on catalog type `str`, and both are typed
    `AttributedString`, so normalise_string_envelopes never touched them and
    verify_string_envelopes never checked them. The run compared a treated site against two
    UNTREATED sites and read the difference as evidence against the mechanism. Symptom 3 IS
    the envelope defect, at sites the allowlist did not reach. Reinstated and fixed in cycle 4.
    Lesson (third occurrence, see also the retraction below): an elimination that rests on
    "we already fixed that class" must first prove the specific site was in the fix's scope.

- hypothesis: "com.apple.mobilenotes.SharingExtension emitting WFCreateNoteInput instead of the catalog's name/contents is the cause of the empty Control Room Note."
  evidence: "The resolved unsupported-device-import session decrypted an Apple-signed donor shortcut exported from this exact iPhone: the device's own native Create Note uses AppIntentIdentifier CreateNoteLinkAction with a WFCreateNoteInput token attachment. Our emission matches the device donor. The catalog's name/contents entry is macOS-27-tagged and is the less authoritative source here."
  timestamp: 2026-08-14 (cycle 2)
  PARTIALLY RETRACTED: 2026-08-14 (cycle 4) — the KEY NAME verdict stands and is confirmed:
    WFCreateNoteInput is correct and the catalog's `contents` is not what iOS 26.6 reads. But
    "our emission matches the device donor" was checked on the key axis only. Re-decrypting
    the same donor this cycle shows its WFCreateNoteInput is a WFTextTokenString while ours
    was a bare WFTextTokenAttachment, and that it names the markdown output
    'Rich Text from Markdown' where ours said 'Rich Text'. This is the SAME blind spot as the
    cycle-1 retraction above — "keys match" is not "the serialization matches" — and it has
    now cost three of four cycles. Guard added: verify_output_names().

- hypothesis: "The 2026-08-14 device observations came from a STALE install — importing a .shortcut whose display name matches an installed one created a duplicate rather than replacing it, leaving the Personal Automation's Run Shortcut pointed at the pre-fix copy. If so, all three refutations would be void."
  evidence: "User performed a fully clean install: deleted the old shortcut before importing, deleted the Control Room Note, and deleted the folder containing state.json. Build side independently confirmed fresh (AEA1, 08:10 rebuild, stamp present once per fork)."
  timestamp: 2026-08-14

- hypothesis: "Broken Choose from Menu wiring (item/case title or order mismatch) causes the Test-a-Circle selection to fall into the Change Sequence body."
  evidence: "All 23 menus have WFMenuItems exactly equal to their ordered mode-1 WFMenuItemTitle list; stack-based nesting walk reports 0 imbalance and 0 unclosed groups."
  timestamp: 2026-08-14

- hypothesis: "Reused or colliding GroupingIdentifier / UUID values (the generator re-seeds a deterministic uuid5 counter on every run over a file it also rewrites) corrupt block boundaries."
  evidence: "0 duplicate action UUIDs across 3675 actions; every GroupingIdentifier maps to exactly one control-flow action identifier."
  timestamp: 2026-08-14

- hypothesis: "The MANUAL menu block was inserted into the wrong router arm, so an OPEN run reaches it."
  evidence: "Ancestry walk places action 1355 in the Otherwise arm of the 'Input Key has any value' conditional (action 89) — the correct, documented location for a no-input manual run."
  timestamp: 2026-08-14

- hypothesis: "A malformed action in the input-normalisation chain (Text / Trim Whitespace / Change Case) silently yields empty output, emptying Input Key."
  evidence: "All four actions' parameter keys match the ToolKit v78 catalog exactly and are marked available on iOS; the ExtensionInput token is byte-equivalent to golden shortcut 51cc4e26."
  timestamp: 2026-08-14
  RETRACTED: 2026-08-14 (cycle 2) — this elimination was WRONG and cost a cycle. The
    check compared parameter KEY NAMES only. Actions 85 (text.trimwhitespace.WFInput) and
    86 (text.changecase.text) are both string-typed and both carried a bare
    WFTextTokenAttachment, so the chain did silently yield empty output — exactly the
    hypothesis as originally stated. Reinstated and fixed in cycle 2. Lesson: "keys match
    the catalog" is not the same claim as "the serialization is correct".

- hypothesis: "The reported 'Set Dictionary Value' error actually came from a Get Dictionary Value on key 'sequence' (action 1466) on the Test path."
  evidence: "ToolKit catalog displayName for is.workflow.actions.getvalueforkey is 'Get Dictionary Value', distinct from setvalueforkey's 'Set Dictionary Value'. The user's quoted message names the setter."
  timestamp: 2026-08-14

- hypothesis: "The `--target-platform ios` validation failure might be masking a real error that survived two cycles."
  evidence: "It rejects 3675/3675 actions indiscriminately, including is.workflow.actions.comment and is.workflow.actions.nothing which are present in its own bundled iOS-27 snapshot. A check that fails every input carries no signal and can conceal nothing."
  timestamp: 2026-08-14 (cycle 2)

- hypothesis: "com.apple.mobilenotes.SharingExtension emitting WFCreateNoteInput instead of the catalog's name/contents is the cause of the empty Control Room Note."
  evidence: "The resolved unsupported-device-import session decrypted an Apple-signed donor shortcut exported from this exact iPhone: the device's own native Create Note uses AppIntentIdentifier CreateNoteLinkAction with a WFCreateNoteInput token attachment. Our emission matches the device donor. The catalog's name/contents entry is macOS-27-tagged and is the less authoritative source here."
  timestamp: 2026-08-14 (cycle 2)

- hypothesis: "Renaming the Set Dictionary Value parameter key from WFInput to WFDictionaryValue was the complete root cause of symptom 2."
  evidence: "Refuted on device by its own stated falsification criterion, then explained: the key was necessary but the value envelope remained wrong, so the Value field stayed empty either way. Retained as a required part of the fix, demoted from sufficient to necessary."
  timestamp: 2026-08-14 (cycle 2)

## Resolution

cycle_9_root_cause: >
  SYMPTOM 1, SECOND DEFECT — the fifth axis of this session, and the first that is invisible
  in the plist. A conditional's OPERATOR PICKER is populated from the STATIC TYPE of the
  variable in WFInput. read_value() defines its variable from an is.workflow.actions.gettext
  output, so Shortcuts types it Text and offers only the eight STRING operators; a numeric
  WFCondition (0/1/2/3/1003) then has no case to render, the operator chip shows RED, and iOS
  refuses to run the action. Keys, envelope, picker literals and condition code are all
  well-formed at a defective site, so every existing invariant passes over it and decrypting
  the signed artifact does not reveal it either.
  20 sites in Dumb / 25 in Sentient. That is more than the 18 the hand trace found, because a
  variable NAME assigned from both a numeric and a Text source anywhere in the artifact is
  mixed-typed, and one Text definition poisons every numeric comparison of that name — even on
  an arm the Text definition can never reach (Pressure Next, Overrun Seconds, Circle Next).
  Device-localised, not argued: the cycle-8 pass reached breadcrumb C and died, and action 170
  (Cooldown Until > Now Epoch) is the first site of the class in the artifact and sits
  immediately after C.

cycle_9_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated,
  validated and re-signed. Nothing from cycles 2, 3, 4, 5 or 8 is reverted.
  (1) NEW normalise_numeric_operands() — a post-pass that attaches
      {"Type": "WFCoercionVariableAggrandizement",
       "CoercionItemClass": "WFNumberContentItem"}
      to the operand descriptor of every numeric-code conditional whose operand is not already
      Number-typed. Shape taken verbatim from Donor 4.1, built in Shortcuts.app on the target
      iPhone and decrypted this cycle; Donor 4 is the same shortcut before the type was set and
      supplies the control case. Golden 332c12a0 confirms the aggrandizement attaches to a NAMED
      variable as well as to an ActionOutput, which is the form our operands take.
      Structural, not site-by-site: any future numeric comparison on a text-coerced value is
      corrected automatically.
  (2) NEW verify_numeric_operands() asserts the invariant that (1) establishes. Both run in
      BOTH forks' builders and share one provenance resolver, so they cannot disagree. The
      generator now asserts five axes — KEY NAME, VALUE ENVELOPE, PICKER LITERAL, VARIABLE SLOT
      and OPERAND TYPE.
  (3) Nothing else changes. Operands that are already numeric are deliberately left untouched,
      so the numeric conditionals that have executed on device stay byte-identical. No action is
      added, removed or reordered anywhere in either fork.
  BUILD_STAMP bumped to "build 2026-08-14i". OPEN_BISECT and ROUTER_TRACE remain ON, and because
  no actions were added the breadcrumb positions are UNCHANGED from build h: A=92, B=147, C=168,
  D=286, E=306, F=415, G=424, H=458, I=473, J=527.
  A FIRST FIX WAS BUILT AND DISCARDED — a read_number() helper materialising each operand
  through a Number action with a code-100 null guard, composed from golden corpus 2e0fb675. It
  validated, signed and measured clean, and was discarded when Donor 4.1 showed iOS doing
  something different for this exact construct. See Evidence for why the discard was correct.

cycle_9_verification: >
  NOT device-confirmed. Build-side only, and stated as such.
  - Both forks: validate-shortcut --target-macos 26 passes; signed files carry AEA1 magic.
  - Shipped signed Dumb artifact DECRYPTED and inspected (not read back from the build tree):
    3684 actions, 87 numeric conditionals, 20 Number-coerced, ZERO text-fed-and-uncoerced.
    Action 170 — the exact site that killed build h — carries the coercion. Stamp
    "build 2026-08-14i" x2 with zero stale "h", 10 breadcrumbs, ROUTER TRACE present.
  - Sentient: 3752 actions, 94 numeric conditionals, 25 coerced, zero uncoerced.
  - SYMPTOMS 2 AND 3 PRESERVED BY CONSTRUCTION, proven exhaustively rather than by class:
    whole-artifact action-by-action comparison against build h gives identical action counts
    (3684 = 3684) and exactly 22 differing actions — 20 conditionals whose ONLY delta is the
    added Aggrandizements key (each verified by deleting that key and confirming byte-equality
    with build h), plus the 2 BUILD_STAMP display strings. All 147 Set Dictionary Value actions
    and the entire Notes family are BYTE-IDENTICAL to the build that device-confirmed them.
  Awaiting the build-i device pass. Decision rule stated in advance: last letter D or beyond
  confirms the class fix; C again refutes it, and unusually cleanly, since the artifact differs
  from the one just tested by 20 type declarations and two display strings and nothing else.


cycle_8_root_cause: >
  SYMPTOM 1, CONFIRMED. A conditional's WFInput is {"Type":"Variable","Variable": <token>}, and
  that <token> slot must hold a WFTextTokenAttachment wrapping a Type-bearing descriptor. At 25
  sites the generator overwrote if_block()'s already-correct value with token(name), which
  returns a WFTextTokenString TEXT TEMPLATE ({"string":"\ufffc","attachmentsByRange":{...}}).
  A text template is not a variable reference: Shortcuts cannot resolve the If's input, renders
  the input field as UNSET, and refuses to run the action with exactly the reported message,
  "Please choose a value for each parameter in this action".
  This is the ENVELOPE axis (cycle 2's axis) INVERTED. Cycle 2 established that string-typed
  PARAMETERS require WFTextTokenString; a variable SLOT requires the opposite. That inversion is
  why 13 hand-written overwrites survived four static sweeps and six cycles.
  Localised by the cycle-7 breadcrumb bisection (user reported last letter "B"), then confirmed
  positionally: of the 25 sites, 23 sit past breadcrumb J on never-reached paths, and the only
  two before J are actions 149 and 158 — both inside span B->C, with 149 the FIRST occurrence of
  the class in the entire artifact, two actions after breadcrumb B.

cycle_8_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated,
  validated and re-signed. Nothing from cycles 2, 3, 4 or 5 is reverted.
  (1) Deleted the 13 lines matching
      <name>["WFWorkflowActionParameters"]["WFInput"] = {"Type":"Variable","Variable": token(...)}
      (pre-edit lines 397, 555, 569, 611, 617, 627, 630, 683, 713, 730, 802, 810, 966).
      VERIFIED PROGRAMMATICALLY before deletion: all 13 passed the SAME variable name that
      if_block() was called with on the line above, so the deletion changes only the envelope.
      No shape is invented; the result is byte-identical to the 282 already-correct sites and to
      Donor 3 action 4.
  (2) NEW verify_conditional_inputs() recurrence guard, wired into BOTH fork builders. Fails the
      build if any mode-0 conditional's WFInput.Variable is missing, is not a
      WFTextTokenAttachment, or wraps a text template rather than a Type-bearing descriptor.
      Closes the VARIABLE-SLOT axis rather than the two instances.
  (3) Documented the invariant at if_block() itself, with the donor and corpus citations, so the
      next author who reaches for token() there sees why not.
  (4) BUILD_STAMP bumped to "build 2026-08-14h". ROUTER_TRACE and OPEN_BISECT left ON —
      see next_action for why the breadcrumbs stay.
  DELIBERATELY NOT CHANGED: the 14 WFConditionalActionString = token() sites (no corpus, no
  catalog, no device evidence; all past breadcrumb J; Donor 4 requested); the two <integer> sites
  at 418/454 (not this bug, and the axis is weaker than cycle 7 recorded).

cycle_8_verification: >
  guardrail_verdict: static signals pass; the runtime signal is the open checkpoint.
  - GUARD SENSITIVITY (MUTATION TEST, not merely "the guard runs"): re-introducing the exact
    deleted line at 802 makes the build exit non-zero with
    "action 149: WFInput.Variable is 'WFTextTokenString', expected WFTextTokenAttachment (1 total)".
    Against the fixed artifacts all five guards accept. The guard bites at the true defect site.
  - SHAPE EQUALITY WITH DEVICE GROUND TRUTH: the repaired WFInput at 149/158 is structurally
    identical to Donor 3 action 4 (checked by recursive type comparison, not by eye).
  - RESIDUAL SCAN: 0 remaining text-template conditional inputs in either fork.
  - BLAST RADIUS, verified by action-by-action comparison of build g vs build h: action counts
    unchanged (3684 / 3752); exactly 27 actions differ per fork — the 25 conditional WFInput
    envelopes plus TWO display-only build-stamp strings (alert title, menu prompt). Every other
    action, including every internal UUID, is byte-identical.
  - SYMPTOMS 2 AND 3 PRESERVED BY CONSTRUCTION, verified rather than asserted: all 147
    setvalueforkey still carry WFDictionaryValue; WFCreateNoteInput and both appendnote.text
    still carry WFTextTokenString. None appears in the diff.
  - SHIPPED-ARTIFACT VERIFICATION (not just the source): both signed .shortcut files were
    DECRYPTED and inspected. AEA1 magic confirmed; Dumb 188480 bytes / 3684 actions, Sentient
    192095 bytes / 3752 actions; 307 and 317 conditional inputs correct with 0 defective; stamp
    "build 2026-08-14h" present and "14g" absent; 10 breadcrumbs present.
  - VALIDATOR: both forks pass at --target-macos 26 --target-platform all. plutil -lint OK.
  - RUNTIME: NOT YET VERIFIED. Requires the device sitting. The fix is not claimed to work until
    the user reports a letter later than B.

cycle_5_root_cause: >
  SYMPTOM 1 (OPEN routing) — IDENTIFIED, pending device confirmation.
  A THIRD parameter axis, never examined by cycles 1-4: REQUIRED PICKER (enum) PARAMETERS.
  A picker parameter must be PRESENT and must hold a LITERAL enum case. If it is absent, or
  holds a variable/attachment token, Shortcuts renders an unfilled picker and iOS refuses to
  run the action with "Please choose a value for each parameter in this action", attributing
  it to the outermost caller — the Personal Automation, by name — and never naming the action.
    is.workflow.actions.count.WFCountType              MISSING (1 Dumb / 2 Sentient)
    is.workflow.actions.getitemfromlist.WFItemSpecifier  VARIABLE TOKEN at 31/33 sites, with
      WFItemIndex absent entirely
  Both are corpus-unanimous defects; eight other picker classes in the same artifact were
  already correct, giving perfect internal separation in both forks.
  WHY IT SURVIVED FOUR CYCLES: the OPEN branch had never once executed on device. Pre-cycle-2,
  Input Key resolved empty, so every automation run took the MANUAL arm and skipped the OPEN
  pipeline. Build d was the first build ever to ENTER it. Cycle 2 did not cause this — it
  exposed it. Whole-shortcut pre-flight validation is refuted: the 2026-08-13 build carried
  these identical defects and ran from the automation to the MANUAL menu.
  ALSO FIXED, same axis-family: speaktext emitted WFInput where the catalog defines WFText —
  this closes DEV-03, whose original premise ("the catalog lists no parameters at all") was
  simply wrong.
  NOT ASSERTED: that this is sufficient. Both defective sites sit AFTER the first OPEN menu,
  and the region before that menu is statically clean — so if no PROSOCHĒ UI ever appeared,
  a further cause remains upstream. See the blind_spots entry in Current Focus.

cycle_5_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated,
  validated and re-signed. Nothing from cycles 2, 3 or 4 is reverted.
  (1) getitemfromlist: WFItemSpecifier="Item At Index" + WFItemIndex=<variable>, replacing
      WFItemSpecifier=<variable>. Corpus-verified shape (golden 332c12a0060043b388b2).
      Sites: build_state_engine.py:435 (Circle Next) and :552 (Rotation Index) -> 31 actions.
  (2) count: WFCountType="Items" added (corpus 11/11). Both forks, including the Sentient-only
      insertion at build_sentient.py:140.
  (3) speaktext: WFInput -> WFText, plus a STRING_ENVELOPE_PARAMS entry so the str-typed
      parameter takes the WFTextTokenString envelope. Closes DEV-03. 10 sites.
  (4) NEW REQUIRED_PICKER_PARAMS table + verify_required_pickers() recurrence guard covering
      NINE picker classes, run by BOTH fork builders. Generalises the axis rather than
      patching the two broken sites.
  (5) VERIFIED_PARAMETER_KEYS extended with count, getitemfromlist and speaktext so the
      existing unknown-key guard also covers them.
  (6) BUILD_STAMP bumped to "build 2026-08-14f". ROUTER_TRACE left ON.
  (7) docs/BUILD-NOTES.md §15 records CAP-06, DEV-03 CLOSED, DEV-05 (math deliberately
      untouched) and DEV-06 (openapp/count redundant keys retained).

cycle_5_verification: >
  guardrail_verdict: static signals pass; runtime signal is the open checkpoint.
  - GUARD SENSITIVITY: verify_required_pickers run against the PRE-FIX artifacts REJECTS both
    and names the exact sites — Dumb "action 576 count.WFCountType missing; action 580/1155/
    1160/1166 getitemfromlist.WFItemSpecifier non-literal (32 total)"; Sentient (33 total).
    Against the fixed artifacts, all four guards accept.
  - THE GUARD CAUGHT A REAL DEFECT DURING THIS CYCLE: a SECOND count action inserted only by
    build_sentient.py:140, invisible to the Dumb pass, failed the Sentient build until fixed.
    Same class of catch as cycle 2's text.match.text.
  - MUTATION at fix site: reintroducing WFItemSpecifier=variable() fails the build (exit 1,
    30 offenders named) and the artifact md5 is UNCHANGED, proving the guard runs before the
    single serialize/write. Restoring the fix reproduces a byte-identical artifact.
  - BLAST RADIUS, Dumb: 44 actions differ from build e — 1 count, 31 getitemfromlist,
    10 speaktext, plus the 2 build-stamp carriers. Sentient: 45 (2 count). Action counts
    UNCHANGED (3674 / 3742). No other action touched.
  - STRUCTURAL REGRESSION, both forks: 0 duplicate UUIDs, 0 multi-identifier
    GroupingIdentifiers, 0 nesting imbalance, final depth 0, 0 menu item/case mismatches.
    Max depth unchanged (11 Dumb / 14 Sentient). plutil -lint OK.
  - VALIDATOR: --target-macos 26 --target-platform all passes for BOTH forks.
  - IDEMPOTENCY: both generators re-run to byte-identical artifacts.
  - SIGNING: both signed, AEA1 magic 41454131, 188441 / 192341 bytes.
  - END-TO-END on the SHIPPED file: the signed Dumb .shortcut was decrypted (§14 recipe) and
    confirmed to carry 3674 actions, WFCountType present, WFItemSpecifier literal at 31 sites
    ('Item At Index') plus 2 'First Item', all 10 speaktext on WFText, the stamp
    "build 2026-08-14f" present and "build 2026-08-14e" ABSENT.
  - OUTSTANDING: no runtime signal. Shortcuts cannot execute on the build Mac.

cycle_4_root_cause: >
  SYMPTOM 3 (empty Control Room Note) — IDENTIFIED, pending device confirmation.
  The cycle-2 value-envelope rule is correct and runtime-proven, but its allowlist was scoped
  to catalog type `str`. The two Notes body parameters are typed `AttributedString` — a text
  type, not a content item — which obeys the same rule and was never considered. Both were
  therefore invisible to normalise_string_envelopes AND to verify_string_envelopes:
    com.apple.mobilenotes.SharingExtension.WFCreateNoteInput  -> note created, body EMPTY
    is.workflow.actions.appendnote.text (Control Room refresh) -> empty content appended
  A second, independent divergence in the same action pair: the reference to the Make Rich
  Text from Markdown output was named 'Rich Text'; its real name is 'Rich Text from Markdown'.
  Verified correct and deliberately untouched: getrichtextfrommarkdown.WFInput is
  content-item-typed and is a bare attachment in BOTH the device donor and golden f44f5caf.
  SYMPTOM 1 (OPEN misrouting) — NOT a plist question this cycle. Cycle 3 moved it off the
  plist entirely; the automation wrapper now fails before PROSOCHĒ runs. Leading hypothesis
  (not asserted): the clean-install delete orphaned the wrapper's Run Shortcut target.

cycle_4_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated,
  validated and re-signed. Nothing from cycles 2 or 3 is reverted.
  (1) STRING_ENVELOPE_PARAMS extended with com.apple.mobilenotes.SharingExtension
      {WFCreateNoteInput} and is.workflow.actions.appendnote {text}, with per-entry
      provenance in the source. This reuses the existing converter AND the existing
      build-failing guard rather than adding a parallel mechanism.
  (2) NEW ACTION_OUTPUT_NAMES table + normalise_output_names(): points every magic-variable
      reference at the producing action's real output name. Seeded with
      getrichtextfrommarkdown -> 'Rich Text from Markdown' (device donor AND golden
      f44f5caf action 14 agree).
  (3) NEW verify_output_names() recurrence guard: fails the build if any reference carries an
      output name that differs from the producing action's real one.
  (4) tools/build_sentient.py runs both new passes and both guards, since Sentient-only
      actions are inserted after the Dumb generator finishes.
  (5) BUILD_STAMP bumped to "build 2026-08-14e". ROUTER_TRACE left ON.
  (6) docs/BUILD-NOTES.md §14 records CAP-05a (AttributedString needs the text envelope),
      DEV-04 (donor folder/WFNoteGroup deliberately not emitted), the signed-.shortcut
      decrypt recipe, and the automation-wrapper design record.

cycle_4_verification: >
  guardrail_verdict: static signals pass; runtime signal is the open checkpoint.
  - GUARD SENSITIVITY (the meaningful test for an in-place generator): both new guards run
    directly against the PRE-FIX cycle-3 artifact REJECT it and name the exact sites —
    verify_string_envelopes -> "action 3616 SharingExtension.WFCreateNoteInput; action 3648
    appendnote.text (2 total)"; verify_output_names -> "action 3616 says 'Rich Text', real
    name is 'Rich Text from Markdown' (1 total)". Against the fixed artifact both accept.
  - MUTATION at fix site: artifact mutated back to the pre-fix defect AND the normalisers
    disabled -> build exits 1 and the artifact md5 is UNCHANGED, proving the guard runs
    before the single serialize/write. With the normalisers enabled the same mutated artifact
    self-heals to an md5 byte-identical to the good build.
  - BLAST RADIUS, Dumb: exactly 4 actions differ from the cycle-3 build — 3616 (envelope +
    output name), 3648 (envelope only), 1350/1354 (build stamp). Sentient: the same 4 at
    1418/1422/3684/3716. Action counts unchanged (3674 / 3742).
  - EXPERIMENTAL DESIGN PRESERVED: 3648's OutputName was already correct ('Text' from a
    gettext), so it changed on the envelope axis ONLY and remains a clean single-variable
    test on device. 3616 changed on two axes and is deliberately not treated as discriminating.
  - DONOR SHAPE EQUALITY: our emitted WFCreateNoteInput now matches the target iPhone's own
    export exactly — same WFSerializationType, same '￼' string, same '{0, 1}' range key,
    same token key set.
  - STRUCTURAL REGRESSION, both forks: 0 duplicate UUIDs, 0 multi-identifier
    GroupingIdentifiers, 0 nesting imbalance, final depth 0, 0 menu item/case mismatches.
    Max depth unchanged (11 Dumb / 14 Sentient). plutil -lint OK.
  - VALIDATOR: --target-macos 26 --target-platform all passes for BOTH forks.
  - IDEMPOTENCY: both generators re-run twice to byte-identical artifacts.
  - SIGNING: both signed, AEA1 magic 41454131, 188513 / 192368 bytes; dated archives verified
    byte-identical to their sources via cmp.
  - END-TO-END (new this cycle): the SIGNED Dumb .shortcut was decrypted and confirmed to
    carry 3674 actions, WFCreateNoteInput as WFTextTokenString with the corrected output
    name, both appendnote.text as WFTextTokenString, and the stamp "build 2026-08-14e".
    No prior cycle could verify the shipped artifact itself.
  - OUTSTANDING: no runtime signal. Shortcuts cannot execute on the build Mac.

cycle_3_root_cause: >
  TWO CONTRIBUTING CONDITIONS, both required simultaneously (the AND-gate fired):
  (A) ROUTER (primary, fixed this cycle): manual invocation was detected by ABSENCE of
      input — an outer "Input Key has any value" gate (cond 100) whose Otherwise arm held
      the MANUAL menu, with a non-matching non-empty value falling into an
      "Unrecognised Input" fail-safe. That design is only correct while an absent Shortcut
      Input normalises to a byte-empty string.
  (B) ENVELOPE (cycle 2, retained deliberately): string-typed parameters carried bare
      WFTextTokenAttachments and resolved to empty at run time. While that was true, the
      Trim/Change Case chain discarded its input and the empty case WAS byte-empty — so
      (A) worked by accident. Correcting (B) made the empty case non-empty, (A)'s gate
      passed, and every manual tap was rejected as unrecognised input.
  Neither condition alone produces the observed failure. Reverting (B) would restore the
  accident, not fix the defect, and would reinstate the three original symptoms.
  Still-unknown and deliberately not guessed: the exact value an absent Shortcut Input
  normalises to. The fix is correct for every possible value; the ROUTER TRACE measures it.

cycle_3_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated,
  validated and re-signed. The envelope fix is NOT reverted.
  (1) NEW restructure_router(): rebuilds the router as positive-match —
        If Input Key is "OPEN" -> OPEN | Otherwise If "CLOSE" -> CLOSE | Otherwise -> MANUAL
      Deletes the cond-100 absence gate (If / Otherwise / End If) and the unrecognised-input
      alert; moves the MANUAL arm into the CLOSE Otherwise; rewrites the two routing comments.
      Idempotent — returns immediately once the gate is gone, so the in-place generator can
      run any number of times.
  (2) NEW verify_router_shape() recurrence guard, run in BOTH fork builders: fails the build
      if the absence gate reappears, if the Input Key tests drift from exactly
      [(4,"OPEN"), (4,"CLOSE")], or if the MANUAL arm leaves the CLOSE Otherwise branch.
  (3) NEW ROUTER_TRACE scaffolding (flag-gated, marker-block managed so it is idempotent and
      strippable): one alert at the head of the MANUAL arm printing the normalised Input Key
      in brackets beside an empty-string reference. Deliberately contains NO control flow —
      an earlier draft tested cond 100 here, which was byte-identical to the router gate and
      broke both the guard and idempotency. The guard caught that during development.
  (4) BUILD_STAMP bumped to "build 2026-08-14d" in the manual menu prompt.
  (5) Deviations recorded in docs/BUILD-NOTES.md §13: DEV-01 (--target-platform ios not used,
      with the 3675/3675 measurement), DEV-02 (loss of the unrecognised-input distinction,
      with the safety argument), DEV-03 (speaktext key still unverified), plus the scaffolding
      debt table for BUILD_STAMP and ROUTER_TRACE.

cycle_3_verification: >
  guardrail_verdict: static signals pass; runtime signal is the open checkpoint.
  - PRESERVES BOTH PATHS (the explicit requirement): semantic diff of pre vs post shows the
    OPEN pipeline body and the CLOSE pipeline body are BYTE-IDENTICAL. The only changed
    actions are the two routing comments, the deleted gate, the deleted unrecognised alert,
    the 3 inserted trace actions, the menu-prompt stamp, and the two relocated End Ifs. Both
    literal comparisons keep the same conditional, the same cond-4 test and the same target
    strings; the automation arms merely lose one enclosing level.
  - mutation at fix site: commenting out the restructure_router() call fails the build with
    the guard's message, exit 1, and the source md5 is UNCHANGED after the rejected build —
    proving the guard runs before the single serialize/write.
  - guard sensitivity, unit-tested against synthetic mutants of the real artifact: MANUAL
    hoisted out of the CLOSE arm -> caught; OPEN literal drifted to "OPENN" -> caught;
    unmutated artifact -> accepted.
  - structural regression, both forks: 0 duplicate UUIDs, 0 multi-identifier
    GroupingIdentifiers, 0 nesting imbalance, 0 unclosed groups, 0 menu item/case mismatches,
    0 control-flow starts missing their required comment. plutil -lint OK.
  - nesting: max depth 12 -> 11 (Dumb) and 15 -> 14 (Sentient). The fix REDUCES depth.
  - action counts: 3675 -> 3674 (Dumb), 3743 -> 3742 (Sentient).
  - validator: --target-macos 26 --target-platform all passes for BOTH forks. It also caught
    a real defect in this cycle's work — the new routing comment used an internal parameter
    name — which was reworded before signing.
  - idempotency: both generators re-run to byte-identical artifacts across three runs.
  - signing: both signed, AEA1 magic confirmed (41454131), 188493 / 192130 bytes; dated
    archives verified byte-identical to their sources via cmp.
  - OUTSTANDING: no runtime signal. Shortcuts cannot execute on the build Mac.

cycle_2_root_cause: >
  IDENTIFIED (single systemic defect), PENDING DEVICE CONFIRMATION — not marked confirmed
  on static evidence alone, per this cycle's standing rule.
  The generator serialized every variable / action-output reference as a bare
  `WFTextTokenAttachment`. That envelope is correct only for parameters iOS types as a
  content item (Set Variable's WFInput, Set Dictionary Value's WFDictionary, File,
  Placemark, float). For parameters iOS types as a plain string, the value must be a
  `WFTextTokenString` — a "\ufffc" placeholder plus attachmentsByRange. A bare attachment in
  a string-typed parameter imports cleanly, passes the bundled validator, and resolves to
  EMPTY at run time. One mechanism, three symptoms:
   - symptom 2: setvalueforkey.WFDictionaryValue (`str`) -> Value empty -> "No value was
     provided to the Set Dictionary Value action for the key sequence".
   - symptom 1: text.trimwhitespace.WFInput and text.changecase.text (`str`) -> the
     OPEN/CLOSE normalisation chain evaporates between actions 84 and 87 -> Input Key
     empty -> routing takes the MANUAL arm.
   - symptom 3 (partial): the Control Room refresh reads every snapshot field through
     gettext.WFTextActionText (`str`) -> all Snapshot* variables empty -> a contentless
     block is appended to the Note.
  Cycle 1's key rename (WFInput -> WFDictionaryValue) is retained and was necessary, but it
  was never sufficient, because the value it named was still wrapped in the wrong envelope.

cycle_2_fix: >
  tools/build_state_engine.py and tools/build_sentient.py only; both forks regenerated.
  (1) NEW normalise_string_envelopes() re-wraps a bare WFTextTokenAttachment as
      WFTextTokenString ("\ufffc" + attachmentsByRange) for every parameter on a verified
      allowlist, preserving the token payload byte-for-byte. Allowlist derived from catalog
      TYPE plus golden-corpus usage, with provenance recorded per entry in the source.
      Applies to gettext.WFTextActionText, setvalueforkey.WFDictionaryValue,
      text.trimwhitespace.WFInput, text.changecase.text, text.match.text,
      alert.WFAlertActionMessage/Title, searchweb.WFInputText.
  (2) DELIBERATE EXCLUSION (recorded deviation): openurl.WFInput is catalog-typed `str` but
      the golden corpus uses a bare attachment 2/2, as do text.combine.text and
      text.split.text. Corpus evidence outranks catalog inference, so these are untouched.
      4 openurl sites remain as bare attachments by design.
  (3) NEW BUILD_STAMP surfaced in the manual menu prompt ("PROSOCHĒ · build 2026-08-14c").
      This exists solely to discriminate the stale-install confound: without a visible
      version marker, a duplicate install with the automation wrapper still pointed at the
      old shortcut is indistinguishable from a failed fix, which is what made cycle 1's two
      refutations uninterpretable.
  (4) RECURRENCE GUARD: new verify_string_envelopes() fails the build if any allowlisted
      string-typed parameter still holds a bare attachment. It runs before the single
      serialize/write, so a rejected build leaves the artifact untouched.
  (5) tools/build_sentient.py now imports and runs the same normaliser and guard, because
      Sentient-only actions are inserted after the Dumb generator has finished and
      previously bypassed the pass entirely (this caught a real leftover: text.match.text).

cycle_2_verification: >
  guardrail_verdict: static signals pass; runtime signal is the open checkpoint.
  - reproduction: pre-fix artifact had 9 distinct string-typed parameters carrying bare
    attachments (367 sites). Post-fix only the 4 deliberately excluded openurl.WFInput
    sites remain, in BOTH forks.
  - mutation at fix site: removing the normalise_string_envelopes() call fails the build
    with "string-typed parameters carry a bare WFTextTokenAttachment (resolves to empty at
    run time) ... (367 total)", exit 1, and the artifact md5 is unchanged after the
    rejected build — proving the guard runs before the write. Running the guard against the
    pre-fix artifact also rejects it, naming action 85 first.
  - blast radius: exactly 367 actions differ per fork (220 gettext, 131 setvalueforkey,
    10 alert, 2 searchweb, 1 each trimwhitespace/changecase/text.match) plus the 1 menu
    prompt stamp. Action counts unchanged (3675 / 3743). Automated payload-preservation
    check confirms every converted parameter carries the ORIGINAL token dict unchanged
    inside attachmentsByRange["{0, 1}"] with string "\ufffc"; the only non-conversion diff
    is the intended build stamp.
  - regression: structural invariants re-verified on both forks — 0 duplicate UUIDs,
    0 unclosed groups, 0 nesting imbalance, 0 multi-identifier GroupingIdentifiers,
    0 menu item/case mismatches. plutil -lint OK for both.
  - validator: --target-macos 26 --target-platform all passes for both forks.
    --target-platform ios rejects 3675/3675 actions indiscriminately (including
    is.workflow.actions.comment) and is now proven to be tooling noise rather than an
    inherited assumption.
  - idempotency: re-running both generators reproduces byte-identical artifacts (md5
    stable across runs).
  - signing: both forks signed, AEA1 magic confirmed, 187758 / 191335 bytes; dated
    archives are byte-identical to their sources.
  - OUTSTANDING: no runtime signal. Shortcuts cannot execute on the build Mac. Nothing is
    confirmed until the device checkpoint returns, and the build stamp must be read back
    FIRST or the results are not interpretable.

oracle_type: specified (user-observable device behaviour against stated expected behaviour)

files_changed:
  - tools/build_state_engine.py (cycle 3: restructure_router, verify_router_shape, router_trace, stamp 14d; cycle 2: envelope normaliser + guard)
  - tools/build_sentient.py (cycle 3: imports and runs verify_router_shape)
  - docs/BUILD-NOTES.md (§13 recorded deviations DEV-01/02/03 + scaffolding debt)
  - tools/build_state_engine.py (envelope normaliser, guard, build stamp)
  - tools/build_sentient.py (reuses the same normaliser and guard)
  - src/PROSOCHE-Dumb.xml (regenerated)
  - src/PROSOCHE-Sentient.xml (regenerated)
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Dumb.shortcut (re-signed)
  - artifacts/shortcuts/PROSOCHĒ — Nine Circles — Sentient.shortcut (re-signed)

open_findings_not_fixed: >
  - openurl.WFInput x4 — knowing deviation, see fix item (2).
  - speaktext passes WFInput; the catalog does not define WFInput for it and lists no
    parameters at all for that identifier, so no verified replacement key exists. NOT
    changed: fabricating a key would violate the project's hard rule. Needs its own
    device probe.
  - format.date sets WFDateFormatString, undefined in the OS27 catalog but documented in
    DATE_TIME.md — genuinely conflicting evidence, left alone.
  - documentpicker.open carries a legacy WFShowFilePicker; openapp carries WFAppIdentifier
    alongside a valid WFSelectedApp (the latter is donor-verified from the device).
  - Symptom 3 is only partially explained; see the blind_spots entry in Current Focus.
