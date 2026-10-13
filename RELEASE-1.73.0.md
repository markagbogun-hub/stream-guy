# RadioCastOS 1.73.0 — Copilot Intelligence Engine

1.73.0 adds contextual intelligence to the Live Show Copilot without entering deterministic playout authority.

## Added

- Segment classification and transition context
- Presenter handoff suggestions and timing
- Prioritized breaking/developing-news advisories
- Context-aware talking points
- Intelligence confidence and urgency indicators
- Operator UI status integration

## Safety

- Immutable queue snapshots are the only broadcast-state input.
- No queue mutation or playout control is exposed by the intelligence engine.
- AI remains optional enrichment; deterministic fallbacks remain available.
