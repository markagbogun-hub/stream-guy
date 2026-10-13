# RadioCastOS 1.69.0 — Intelligence Orchestration

## Added

- Show-level Intelligence Orchestration.
- Shared context across intelligence capabilities.
- Explicit dependency ordering: metadata → news/music → presenter → show preparation → social/archive.
- Consolidated `IntelligencePackage` advisory result.
- Per-capability runtime deadlines inherited from Intelligence Runtime.
- Orchestration cancellation.
- Capability result correlation through request IDs.
- Safe continuation when any capability fails or falls back.

## Safety

The orchestrator never owns scheduling, queue mutation, playout, emergency handling, or reliability recovery. AI and orchestration remain advisory. A capability failure, timeout, rejection, cancellation, or missing provider cannot become a broadcast failure.
