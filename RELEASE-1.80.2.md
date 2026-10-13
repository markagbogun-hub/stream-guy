# RadioCastOS 1.80.2 — One-Click AI Show & Air

## Added
- Renamed the AI Presenter Autopilot action to **CREATE + AIR COMPLETE AI SHOW**.
- A single operator click now fetches current headlines from configured HTTPS feeds, validates them against the trusted-domain allow-list and freshness policy, generates/voices the show segments, and submits the completed audio assets to the canonical broadcast queue.
- The one-time button action does not enable persistent unattended Autopilot. Existing queue/playout rules remain in control and current playback is not forcibly interrupted.
- News-led show preparation now fails closed when trusted fresh headlines cannot be validated; it will not generate or queue an empty/unverified news bulletin.

## Requirements / boundaries
- A configured HTTPS news feed, trusted news-domain allow-list, selected consented clone voice, and configured clone runtime are required for this full-show workflow.
- The action queues prepared audio segments for deterministic playout; it does not forcibly seize the live output or bypass emergency/queue controls.
- This release builds on the supplied 1.80.1 source and preserves the existing persistent Autopilot run history.
