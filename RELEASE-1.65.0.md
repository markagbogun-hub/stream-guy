# RadioCastOS 1.65.0 — Broadcast Intelligence

## Release focus

RadioCastOS now has an explicit AI/advisory boundary above the deterministic broadcast engine.

### AI capabilities
- AI Presenter
- AI News
- Music Intelligence
- Metadata
- Show Preparation
- Social Content
- Archive Intelligence

### Broadcast-safety contract
- AI never owns the scheduler, Broadcast Queue, Broadcast Engine, playout clock, or emergency path.
- Missing AI providers use deterministic fallbacks.
- Provider errors use deterministic fallbacks.
- Provider timeouts use deterministic fallbacks.
- AI can enrich metadata, but cannot change the scheduler-selected path, item type, artist, or title.
- Intelligence results are recorded with status, reason and request ID.
- `intelligence.result` is an advisory broadcast-domain event only.

## Validation

Passed:
- Broadcast Intelligence tests
- Automation Pro tests
- Broadcast Queue tests
- Broadcast Engine tests
- Broadcast Core tests
- Version consistency
- Self-test
- Python compilation
- Source imports

The Windows PyInstaller executable/installer remains a Windows build step using `local-build.bat`.
