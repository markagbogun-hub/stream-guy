# RadioCastOS 1.85.0 — Scheduler Integration & Broadcast Telemetry

## Included
- Persistent one-time schedule bookings from AI Programme Studio.
- Explicit authorization gate before a due booking is dispatched to the canonical BroadcastEngine queue.
- Per-segment start/completion/failure telemetry written to `%APPDATA%/RadioCastOS/broadcast_telemetry.jsonl` on Windows or `~/.radiocastos/broadcast_telemetry.jsonl` elsewhere.
- Air-status panel reports booking state and observed broadcast-engine events separately from imported external as-run confirmations.
- PLAYOUT_ENDED now carries the item that completed rather than only a post-completion empty queue snapshot.

## Operational boundaries
The scheduler dispatches due authorized segments to the canonical in-app BroadcastEngine queue. A downstream playout adapter must consume that queue for actual playback. Broadcast-engine events are application telemetry, not independent encoder confirmation; retain external as-run/encoder records for authoritative aired reporting. A schedule booking does not authorize itself.

## Validation
Run `python scripts/test_programme_runtime.py`, `python scripts/test_broadcast_engine.py`, `python scripts/test_preflight.py`, and `python scripts/check_version.py` from the repository root.
