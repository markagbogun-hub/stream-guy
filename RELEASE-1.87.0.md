# RadioCastOS 1.87.0 — Guarded Scheduled Playout & As-Run Reconciliation

## Added
- `src/scheduled_playout.py`: opt-in scheduled queue dispatcher, station/AutoDJ/player safety gates, retry backoff, optional JSONL audit trail, dashboard counters, and exact-path/item-ID as-run reconciliation.
- `scripts/test_scheduled_playout.py`: regression coverage for gating, timing, retries, player completion vs independent confirmation, and unmatched as-run records.

## Operational safety
- Automatic scheduling is disabled by default; merely installing this release does not enable automatic playout.
- The station integration must supply truthful station mode, AutoDJ activity, and player-busy state, and must wire player callbacks through `observe_track`.
- A successful local player start or natural end is not proof that audio reached the encoder or listeners. Only a trusted external as-run completion record counts as independent confirmation.
- Windows packaging and real station/encoder behavior require validation in the target station environment.
