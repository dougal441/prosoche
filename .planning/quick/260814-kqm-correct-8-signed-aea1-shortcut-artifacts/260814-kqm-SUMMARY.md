---
quick_id: 260814-kqm
status: complete
commit: adc96a3
---

# Signed `.shortcut` recovery instructions corrected

Updated `.claude/CLAUDE.md` to permit and document AEA1 recovery with `aea decrypt` and `aa extract`, including XML conversion for inspection or remixing. Verified the documented commands against `.planning/debug/Donor - notes.shortcut`; the recovered XML passed `plutil -lint` and contained the expected Notes action.
