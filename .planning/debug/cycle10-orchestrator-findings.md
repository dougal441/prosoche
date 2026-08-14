# Cycle 10 — orchestrator findings (produced while the debugger was rate-limited)

Status: **diagnosis complete, fix NOT applied.** The user chose to wait for the
debugger rather than have the orchestrator edit the generator. Nothing in the repo
has been changed. Build `2026-08-14i` is the current committed state (`d2e1ebe`).

These findings were derived by the orchestrator via direct static analysis of
`src/PROSOCHE-Dumb.xml` and `tools/build_state_engine.py`. The debugger should
**verify rather than trust** them; where its own analysis disagrees, the debugger's
wins, having full session context.

## 1. Enumeration of `settings_snapshot` (Dumb fork)

**Reads**

| key | n | first |
|---|---|---|
| `settings_snapshot.brightness` | 14 | **177** |
| `settings_snapshot.brightness.original_value` | 4 | 182 |
| `settings_snapshot.volume` | 14 | 196 |
| `settings_snapshot.volume.original_value` | 4 | 201 |

**Writes**

| key | n | first |
|---|---|---|
| `settings_snapshot.brightness` | 4 | **188** |
| `settings_snapshot.brightness.original_value` | 10 | 1132 |
| `settings_snapshot.brightness.changed_at` | 10 | 1134 |
| `settings_snapshot.brightness.changed_by_session_id` | 10 | 1136 |
| `settings_snapshot.volume` | 4 | 207 |
| `settings_snapshot.volume.original_value` | 10 | 1038 |
| `settings_snapshot.volume.changed_at` | 10 | 1040 |
| `settings_snapshot.volume.changed_by_session_id` | 10 | 1042 |

Sentient not yet enumerated — the debugger should run the same pass on it.

## 2. Read-before-write, and no top-level creation

First read is **177**; first write is **188** — eleven actions later, both inside the
C→D span (168–286) where the device stops.

The bootstrap `dictionary` actions at **8** and **25** are built with **zero keys**.
Every `setvalueforkey` in actions 0–176 is just four writes: `opens_today` (152, 162)
and `behavioural_day` (154, 164). **No action anywhere creates the top-level
`settings_snapshot` key** — the subtree only comes into existence as a side effect of
a nested write much later in the pipeline.

## 3. This predicts both observed device errors exactly, in order

- **Clean install** → read at 177, subtree absent →
  `In '', no value was found for dictionary key 'settings_snapshot'`.
  The empty `In ''` is the root State dictionary.
- **After the user exercised Change Profile / Change Sequence / Test a Circle** →
  those paths wrote `settings_snapshot.volume.*` (1038–1042), creating the subtree
  with `volume` but never `brightness` → read at 177 fails one level deeper →
  `In 'settings_snapshot', no value was found for dictionary key 'brightness'`.

The user's menu exploration produced precisely the intermediate state that
distinguishes "subtree missing" from "subtree incomplete". It should be treated as a
deliberate experiment; it is what pins the diagnosis.

## 4. ROOT CAUSE — the defensive pattern rests on a false assumption

`restore_managed_settings` (`tools/build_state_engine.py:335`) is written carefully and
its stated intent is *"never guess an original setting."* It reads the snapshot, then
gates on `has any value` (condition 100).

That design assumes **a missing dictionary key reads as empty**, so the gate would be
false and the branch skipped. It does not. `Get Dictionary Value` on a missing key
**raises a hard runtime error**. The read at 177 fails before the gate at 178 can
evaluate. The guard cannot protect anything, because the condition it guards against
kills the read first.

This is a design-level assumption failure, not a serialization defect — the first such
in the session. Every previous defect (key name, `str` envelope, `AttributedString`
envelope, picker enum, variable slot, operand type) was a wrong shape in the emitted
plist. This one is a wrong belief about iOS semantics.

## 5. SECOND DEFECT — `clear_snapshot` writes the literal string `"null"`

`tools/build_state_engine.py:330`:

```python
def clear_snapshot(key: str, dictionary_name="State"):
    return set_value(f"settings_snapshot.{key}", text_token([("null", None)]), dictionary_name)
```

`text_token([("null", None)])` produces the four-character string `null` — non-empty,
so `has any value` evaluates **true**. It also replaces the sub-dictionary with a
string, destroying `original_value` beneath it.

Consequence, on the run *after* a successful restore: `settings_snapshot.brightness`
is `"null"` → passes the gate → reads `settings_snapshot.brightness.original_value` →
parent is now a string, key gone → **the same hard error returns**.

This is latent. It only bites once the OPEN path works well enough to perform a
restore, so fixing bootstrap alone would clear the current error and then reintroduce
it a run or two later, presenting as a regression.

## 6. THIRD FINDING — the ownership check is not implemented

Four keys are **written but never read anywhere in either fork**:

```
settings_snapshot.brightness.changed_at
settings_snapshot.brightness.changed_by_session_id
settings_snapshot.volume.changed_at
settings_snapshot.volume.changed_by_session_id
```

`changed_by_session_id` exists so the restore path can verify it owns a change before
reverting it. Nothing consults it, so that ownership check **does not exist**.

This reframes the `Session ID` scope defect the debugger found (assigned only under
[OPEN → not-in-cooldown → genuine-open]; only 2 of 20 `changed_by_session_id` writes
share that ancestry). Correcting the scope so it records a valid owner would not help,
because no code reads the owner. Per the project rule that stateful brightness/volume
changes must be reliably restorable, the ownership half of that guarantee is currently
**absent**, not merely mis-scoped.

Implementing an ownership check is a **design change, not a bug fix** — it should be
put to the user rather than added silently.

## 7. Proposed fix (NOT applied — for the debugger to verify and implement)

Both defects in §4 and §5 resolve the same way: **write empty text, not `"null"`, and
establish the shape at bootstrap.**

1. Bootstrap creates `settings_snapshot.brightness` and `settings_snapshot.volume` as
   **empty text**, so the reads at 177/196 succeed and the `has any value` gate reads
   false, skipping the nested reads at 182/201 entirely.
2. `clear_snapshot` clears to **empty text** for the same reason.

Then the "never guess an original setting" design works as written. No new actions, no
action-index shifts, so breadcrumb spans stay valid and the letter stays comparable.

**To verify before implementing:**
- Confirm empty text makes condition 100 evaluate false on device. If it does not, the
  sentinel must be something that does, and that must be established from a donor
  rather than assumed — this is exactly the class of assumption that caused §4.
- Run the §1 enumeration against Sentient.
- Decide and state what `original_value` defaults to, if anything. A wrong default
  could restore brightness or volume to a value the user never had. If a safe default
  cannot be established, skipping the restore is safer than guessing — the project's
  own rule already says so.

## 8. Still open, unrelated to the above

- Donor 5 (`.planning/debug/Donor 5.shortcut`, 22,458 bytes, AEA1, 16:14) — the
  cycle-8 optional donor for the 14 `WFConditionalActionString = token()` sites. These
  are right-hand operands, and cycle 9 established the operator picker is driven by the
  left input only, so establish whether they are genuinely defective or merely
  residual before fixing.
- `List` / `WFItems` wrapper at action 1164 — shape already recovered from Donors 4/4.1
  as `{"WFItemType": 0, "WFValue": <WFTextTokenString>}`; ours omits the wrapper. Past
  breadcrumb J, non-blocking.

---

## 8. SESSION-MANAGER ADDENDUM — the `"null"` literal is SYSTEMIC, not one site

Finding 4 above identifies `clear_snapshot` (line 332) as writing the literal four-character
string `null`. **It is not one site. It is seven, across four distinct state keys.**

```
tools/build_state_engine.py
  332   set_value(f"settings_snapshot.{key}", text_token([("null", None)]), ...)
  768   set_value("pending_exit",    text_token([("null", None)]))
 1249   set_value("cooldown_until",  text_token([("null", None)]))
 1250   set_value("active_session",  text_token([("null", None)]))
 1258   set_value("cooldown_until",  text_token([("null", None)]))
 1300   set_value("cooldown_until",  text_token([("null", None)]))
 1301   set_value("active_session",  text_token([("null", None)]))
```

Affected keys: `settings_snapshot.*`, `pending_exit`, `cooldown_until`, `active_session`.

### Why this is critical path, not a tidy-up

**`cooldown_until` is the operand of action 170** — the exact conditional the build-`i` coercion
fix just repaired, and the first numeric comparison on the OPEN path. It is written as the
literal text `"null"` at three sites. So the OPEN path performs a *numeric* comparison against
the four-character string `null` whenever a cooldown has been cleared.

The build-`i` fix declared that operand `WFNumberContentItem`. **Coercing the string `"null"` to
a number is undefined** — it may yield 0, empty, or a hard error. Action 170 has not yet
executed against a cleared-cooldown state on device, so this is unmeasured.

`pending_exit` is read at actions 479/484/487, inside span I→J (I=473, J=527).

### Consequence for the fix

Fixing `settings_snapshot` alone leaves three more keys carrying the same disease, one of them on
the critical path immediately after the current failure point. Every one of these writes is the
same wrong belief: that `"null"` reads as absent. It does not — it is a non-empty string, so
`has any value` (code 100) returns **true** for all four keys.

**The fix must be applied to `text_token([("null", None)])` as a construct, not to `clear_snapshot`
as a function.** Whatever sentinel replaces it must be verified on device, per §7's open question,
and must satisfy BOTH consumers: the `has any value` gates AND the numeric coercion at 170.

That dual constraint is new information: a sentinel that reads as absent to code 100 must also not
break a `WFNumberContentItem` coercion on the same key. Establish both from a donor before
shipping; they may not have the same answer.

---

## 9. PER-KEY CONSUMPTION MAP — 4 of the 7 `"null"` sites change, 3 must NOT

Built by tracing each `getvalueforkey` forward through its `gettext` → `setvariable` hop to the
condition code that actually consumes it. This is the map that decides the fix scope.

| state key | consumed by | `"null"` verdict |
|---|---|---|
| `settings_snapshot.brightness` | **code 100 HAS ANY VALUE** @181 | **DEFECT** |
| `settings_snapshot.brightness.original_value` | **code 100** @186 | **DEFECT** |
| `settings_snapshot.volume` | **code 100** @200, @1031 | **DEFECT** |
| `settings_snapshot.volume.original_value` | **code 100** @205 | **DEFECT** |
| `settings_snapshot.brightness` (Circle path) | **code 100** @1125 | **DEFECT** |
| `pending_exit` | **code 100 HAS ANY VALUE** @483 | **DEFECT** |
| `active_session` | **code 100 HAS ANY VALUE** @689, @1094, @1232, @1248 | **DEFECT** |
| `active_session.id` | code 4 string-is @697, @794, @1099, @1253 | (gated by the 100s above) |
| `active_session.declared_duration_seconds` | code 2 numeric @1260 | (gated by the 100s above) |
| **`cooldown_until`** | **code 2 `>` NUMERIC ONLY** @170 | **SAFE — DO NOT CHANGE** |

### Verdict

**Change 4 sites** — line 332 (`settings_snapshot.*`), 768 (`pending_exit`), 1250 and 1301
(`active_session`). All three keys are consumed by `has any value`, and the device result
`EMPTY: NO VALUE` confirms an empty sentinel makes that gate read false as intended.

**Do NOT change 3 sites** — lines 1249, 1258, 1300 (`cooldown_until`). Its *only* consumer is the
numeric comparison at action 170, and the device result `NULL COERCED FALSE` (no error) means the
current literal already evaluates false, which is semantically correct: **"cleared cooldown" →
"not in cooldown"**. Changing it would alter behaviour on the single most critical position on
the OPEN path — the conditional the build-`i` coercion fix just repaired. **That would be a
regression, not a fix.**

This supersedes the uniform seven-site plan in §8. The construct is not uniformly wrong; the
question is per-key whether the sentinel matches its consumption pattern, and for `cooldown_until`
it already does.

### Note on `active_session` — the empty sentinel is load-bearing here

`active_session` is read at 32 sites, and its sub-keys (`.id`, `.declared_duration_seconds`) are
read *nested*. Those nested reads would hard-error on a missing parent — the same failure as
`settings_snapshot`. They are protected only because the `has any value` gates at 689/1094/1232/
1248 skip them. So the empty sentinel is doing real work: with `"null"` those gates read **true**
and the nested reads execute against a string, which is exactly the `settings_snapshot` failure
one level over. Fixing `active_session` is not cosmetic.

### Still blocked on

Whether **empty** survives a Number coercion. Not needed for these four keys — all are
gate-consumed — but it decides whether empty is a single universal sentinel or whether
gate-consumed and numerically-consumed keys need different ones as a documented choice.

---

## 10. DONOR 6.1 — correctly wired, verified, AWAITING A RUN

Decrypted and structurally verified by the session-manager. **All three Donor 6 faults are
fixed** and the third test was added:

```
[0] dictionary        keys=['empty','nullish']  vals=['', 'null']
[1] getvalueforkey    KEY='empty'          <- act0   (trailing space FIXED)
[2] cond 100  AGG=WFStringContentItem      <- act1   -> 'EMPTY: HAS VALUE' / 'EMPTY: NO VALUE'
[7] getvalueforkey    KEY='nullish'        <- act0   (REWIRED to the Dictionary, was act1)
[8] cond 2 >0 AGG=WFNumberContentItem      <- act7   -> 'NULL COERCED OK' / 'NULL COERCED FALSE'
[13] getvalueforkey   KEY='missing.nested' <- act0   (NEW dotted-path test)
[14] cond 100 AGG=WFStringContentItem      <- act13  -> 'Path ok' / 'Path none'
```

Action 7 now genuinely reads the literal string `null` from the Dictionary, so line 2 measures
what we thought Donor 6 measured. Action 13 reads a dotted path where nothing exists.

**It has not been run. The three reported lines settle three open questions at once:**

| line | settles |
|---|---|
| 1 | whether a present-but-empty value reads as absent to code 100 — the sentinel premise |
| 2 | **what `"null"` does under `WFNumberContentItem`** — decides `cooldown_until` |
| 3 | **flat-vs-dotted read semantics** — decides the root-cause statement |

If line 3 **errors outright** rather than printing either branch, that is the strongest possible
confirmation of the dotted-path refinement, and the error text should be captured verbatim.

## 11. `cooldown_until` — DOWNGRADED to unproven-and-deferred

Donor 6's `NULL COERCED FALSE` did **not** measure `"null"`. Action 7 read `nullish` out of
action 1's result (an empty value) rather than out of the Dictionary, so it measured empty
coerced to Number, not the literal string.

**The three `cooldown_until` sites (generator lines 1292, 1301, 1343) remain untouched — which is
still the right default — but they are recorded as UNPROVEN, not proven-safe.** What `"null"`
does under `WFNumberContentItem` at action 170 is unknown until Donor 6.1 line 2 is reported.

The consumption map in §9 is unaffected: `cooldown_until` is still consumed solely by code 2 at
action 170 via the read at 102. Only the *safety of leaving the literal there* is unestablished.

Note the one thing Donor 6 did establish accidentally: action 8 coerced an **empty** value to
`WFNumberContentItem` and returned false **without erroring**. So empty survives Number coercion
cleanly — evidence that empty is viable as a single universal sentinel, though it came from a
miswired shortcut and Donor 6.1 line 2 re-confirms it properly.
