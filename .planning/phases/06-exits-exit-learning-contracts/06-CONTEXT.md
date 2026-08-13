# Phase 6: Exits, Exit Learning & Contracts - Context

**Gathered:** 2026-08-13
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Every exit is reachable and honestly recorded, the system learns over time which exits actually get the user away from the phone, and every contract the user makes is honoured, recorded, and feeds back into Heat.

</domain>

<decisions>
## Implementation Decisions

### The agent's Discretion
All implementation choices are at the agent's discretion. Use ROADMAP Phase 6, the completed state/session engine, Phase 5 primitive dispatch, the config-driven exploration rate, Shortcuts Playground rules, and existing plist conventions. Keep selection deterministic and never initiate human contact on the user's behalf.

</decisions>

<code_context>
## Existing Code Insights

Reuse the bounded state schema, active-session race protocol, previous-contract Heat input, primitive routing, and verified first-party action shapes. Plan-phase research should identify the smallest complete exit and contract paths in the current graph.

</code_context>

<specifics>
## Specific Ideas

No additional requirements beyond ROADMAP Phase 6 and EXIT-01..09 / LEARN-01..05 / CONT-01..06.

</specifics>

<deferred>
## Deferred Ideas

Control Room presentation and template breadth remain Phase 7; model auditing remains Phase 8.

</deferred>
