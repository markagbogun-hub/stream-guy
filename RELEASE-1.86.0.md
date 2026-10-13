# RadioCastOS 1.86.0 — Live Playout Bridge & End-to-End Verification

## Included
- Added an explicit `BroadcastPlayoutAdapter` that starts the next canonical queue item through the existing local `PlaylistPlayer` only after operator confirmation.
- Connected natural player-end callbacks back to the canonical BroadcastEngine so tracked queue items produce start and completion telemetry.
- Added a queue item identity check to prevent a stale queue observation from claiming a different segment.
- Added failure telemetry for missing media, player exceptions, player rejection, and queue races; failed starts do not become completed/confirmed-air records.
- Added Programme Studio's `PLAY NEXT QUEUED SEGMENT` operator action with a clear warning that the handoff may interrupt the currently playing asset.
- Expanded the air report with canonical queue depth, current queue item, and engine start/completion/failure counters.
- Added adapter regression tests for confirmation gating, missing assets, player rejection, natural completion, and unrelated track-end callbacks.

## Operational boundaries
- The bridge is operator-triggered; it does not automatically pre-empt AutoDJ or take over live playback on its own.
- A player-start or player-completion event is application telemetry, not independent proof that the encoder transmitted the full asset to listeners. Continue importing authoritative external as-run/encoder records for confirmed-air reporting.
- The station must test the handoff against its real player, automation, stream, and failover configuration before live use.

## Validation
Run `python scripts/test_broadcast_playout_adapter.py`, `python scripts/test_programme_runtime.py`, `python scripts/test_broadcast_engine.py`, `python scripts/test_programme_air_report.py`, and `python scripts/check_version.py` from the repository root.
