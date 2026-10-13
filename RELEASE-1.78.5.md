# RadioCastOS 1.78.5 — Emergency Media Vault & Health Center fixes

## Safety
Still advisory only: nothing here starts playback, changes the authoritative queue, switches streams or bypasses Emergency Stop.

## Fixes
- Vault and Failover verify the audio actually configured for the station.
- Station Health Center reads the real settings and stream state.
- Failover finds real configuration backups.
- Duration probing works without ffprobe on PATH (bundled ffprobe or `ffmpeg -i` fallback).
- Vault and Health scans no longer freeze the window; Refresh no longer stacks timers.
- No console-window flash when presenter audio is joined.

## Added
- "Choose folder…" in the Emergency Media Vault.
