# RadioCastOS 1.77.0 — AI Presenter Autopilot

## v1.77.0

Adds an opt-in full AI Presenter Autopilot layer.

### Operator profile
- mode=full
- voice=clone
- verified news=true
- station announcements=true
- music introductions and transitions=true
- automatic running=false by default (supervised)

### Implemented
- One-button full-show preparation API
- Persistent show/run state with atomic recovery
- Authorized clone-profile enforcement
- Existing consented voice-clone engine integration
- Verified-news validation with HTTPS, freshness and explicit trusted-domain allow-list
- Presenter script generation for intro, announcement, news, transitions and close
- TTS/audio QA through the existing 1.75 runtime
- Audio asset registration through the existing 1.76 workflow
- Configured fallback audio and recovery records
- Explicit opt-in automatic running
- Deterministic playout bridge using only the supplied approved sink interface
- No direct player, stream, emergency, or queue-policy control from the autopilot

### Capability boundary
1.77.0 does not bundle a voice-cloning model, a news subscription, or a cloud TTS account. A real cloned voice requires an existing consented clone profile and configured clone runtime. Verified news requires configured HTTPS feeds plus an explicit trusted-domain list. Human-quality output therefore depends on those external/runtime resources being available.

Automatic running is never enabled merely because Autopilot exists. The saved operator setting must explicitly enable it, and a deterministic playout sink must be supplied at runtime. Restart recovery restores state only; it never resumes playout by itself.
