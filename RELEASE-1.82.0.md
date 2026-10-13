# RadioCastOS 1.82.0 — End-to-End AI Broadcast Workflow

## Included
- New `src/ai_broadcast_workflow.py` orchestration layer.
- Durable workflow state for prepare/failed/ready-for-review/submitted runs.
- Explicit injected interfaces for news retrieval, news audio, presenter audio, approved asset inventory, progress reporting, and queue sink.
- Fail-closed behaviour for missing news configuration, empty validated news, missing bulletin rendering, invalid asset kinds, and missing audio files.
- Operator authorization and duplicate submission protection.

## Verification
- `python scripts/test_ai_broadcast_workflow.py`
- `python scripts/test_ai_programme_director.py`
- `python scripts/test_ai_presenter_autopilot.py`
- `python scripts/test_web_news.py`
- `python scripts/check_version.py`

## Integration note
The workflow API is ready for the configured station adapters. This package does not claim that an arbitrary installation already has working external news/TTS credentials or that the encoder/stream is live. Queue submission is not equivalent to confirmed on-air output.
