# ⛔ DO NOT RUN BUILD `2026-08-14j` — SAFETY DEFECT

**Status: build `j` is UNSAFE and must not be installed or run on device.**
Superseded by the next build. Recorded 2026-08-14.

## The defect

Build `j` seeded the `settings_snapshot` leaves as **empty strings**. Donor 6.1 then measured
that **a present-but-empty value passes `has any value` (TRUE)**. That combination turns the
restore path into an unguarded write:

```
[177] read settings_snapshot.brightness              -> var 'Restore Brightness Snapshot'
[181] If cond=100 (has any value)                    -> dict present, TRUE
[182] read settings_snapshot.brightness.original_value -> var 'Restore Brightness'  == ""
[186] If cond=100 (has any value)                    -> present-but-empty, TRUE
[187] setbrightness  WFBrightness = var 'Restore Brightness'   <-- writes ""
```

Identical shape at [196]-[206] for `setvolume`.

**Consequence:** a brightness write with no value — a runtime error, or brightness 0, i.e. a
black screen. `.claude/CLAUDE.md` forbids zero brightness explicitly. These reads sit at actions
177/196, inside the C->D region that executes on **every OPEN**, so it is on the hot path.

Build `j` removed the read errors and walked straight into the unguarded write. It was built
before the present-empty semantics were known; seeding empty was reasonable on the information
available at the time. The information changed after it shipped.

## The deeper finding — the construct is impossible, not merely mis-parameterised

Measured semantics (Donor 6.1, correctly wired):

| construct | behaviour |
|---|---|
| flat read, **missing** key | returns nothing, no error -> `has any value` **FALSE** |
| flat read, **present but empty** | -> `has any value` **TRUE** |
| **dotted** read, missing segment | **hard error**, "could not evaluate the key path" |
| `"null"` -> `WFNumberContentItem`, `> 0` | **FALSE**, no error |

For a dotted path the read raises unless the final key exists; if it exists, `has any value` is
true. **There is no state in which the gate reads false without the read having already raised.**
`restore_managed_settings` cannot work for ANY sentinel value. This supersedes the earlier
"missing key raises" formulation, and it is why no sentinel swap can fix it.

## Vindication of the Half-2 refusal

Cycle 11 refused to write empty at the four `setvalueforkey` sites because `validate-shortcut`
rejects it and because read-side evidence does not license an empty write. Both correct — **and
empty would not have worked anyway**, because it fails the gate semantics. The refusal prevented
shipping a fix that was wrong for a second, independent reason that had not yet been measured.

## The corrected fix (next build)

1. **Keep `CLEARED_SENTINEL = "null"`** — present, so dotted reads succeed without raising, and
   it satisfies the validator's non-empty rule, so the Half-2 blocker dissolves entirely.
2. **Seed the bootstrap leaves as `"null"`, not `""`** — the shape half of the diagnosis stands.
3. **Change the LEAF gates from code 100 to code 5 (`is not`) against the literal `"null"`.**
   Cleared -> reads `"null"` -> `is not "null"` false -> skip. Real -> reads a value -> true ->
   restore. Verify code 5 against the corpus and CONTROL_FLOW.md before emitting.
4. **Container gates (181, 200) may remain code 100** — once bootstrap guarantees the container
   dict exists, the dotted leaf read beneath cannot raise. The decisive gates are the LEAF ones
   (186 brightness, 205 volume). Confirm this split rather than changing all gates blindly.
5. **Check `pending_exit` (@483) and `active_session` (@689, 1094, 1232, 1248)** for the same
   impossible construct. `active_session` matters most — `.id` and
   `.declared_duration_seconds` are read nested behind those gates.
6. **`cooldown_until` (lines 1249/1258/1300) is now DEVICE-VERIFIED SAFE** — leave untouched.
