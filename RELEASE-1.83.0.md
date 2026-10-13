# RadioCastOS 1.83.0 — AI Programme Studio

## Included
- Dedicated AI Programme Studio tab with one-click programme creation from five templates.
- Timed rundown editor with reordering, audio preview, script editing, and clear regeneration-adapter messaging.
- Local-asset preflight, explicit review, schedule-draft persistence, and operator-authorized queue handoff.
- Post-queue reporting separates pending items from queue items marked PLAYED and cautions that independent as-run confirmation is not yet connected.
- Existing Show Builder and production queue remain available.

## Integration status
This release wires the operator UI to existing local AutoDJ tracks, approved AI presenter clips, ShowBuilder persistence, and the AI production queue. The screen does not fabricate news/audio. Trusted live-news retrieval, new voice rendering, station scheduler submission, and independent broadcast-engine/as-run confirmation still require configured adapters. Schedule Draft is metadata only; queue submission is not proof of on-air transmission.

## Verification
- `python scripts/test_ai_broadcast_workflow.py`
- `python scripts/test_ai_programme_director.py`
- `python scripts/check_version.py`
- Python syntax compilation for changed source files
