# RadioCastOS 1.74.0 — Copilot Voice & Presenter Assist

1.74.0 adds a voice-ready presenter assistance layer above the Live Show Copilot.

## Added

- Presenter script generation for intro, transition, outro, news-link and handoff segments.
- Target word-count and read-time controls.
- Deterministic read-time estimation and safe script trimming.
- Preview, edit, approve, reject and expiry state for generated scripts.
- Operator-visible approval metadata and script revision correlation.
- Voice-readiness metadata for future TTS integration.

## Safety

- Scripts are advisory and do not execute automatically.
- Approval changes only copilot presenter-assist state.
- TTS/audio generation is decoupled from deterministic playout.
- The presenter-assist module has no queue mutation or playout-control API.
