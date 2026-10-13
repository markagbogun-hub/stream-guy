# RadioCastOS 1.71.0 — Live Show Copilot

## Summary

RadioCastOS 1.71 adds a live operator copilot that observes the authoritative broadcast state and produces bounded, real-time advisory cues without becoming part of deterministic playout.

### Added

- Current/next awareness correlated to the authoritative queue revision.
- Presenter cue timing from the observed current item duration.
- Periodic talking-point refresh.
- Breaking-news advisory detection from supplied headline context.
- Transition and immediate-next cues.
- Operator acknowledgement and acknowledgement events.
- Stale asynchronous refresh protection.

### Safety

- No queue mutation API is called by the copilot.
- The authoritative BroadcastEngine/BroadcastQueue remains the only source of playout decisions.
- AI is optional enrichment; deterministic fallback cues remain available.
- AI timeout/failure cannot block playout, reliability recovery, or emergency handling.
