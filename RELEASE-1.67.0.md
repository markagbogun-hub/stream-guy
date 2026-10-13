# RadioCastOS 1.68.0 — Intelligence Studio

RadioCastOS 1.68 brings the AI layer into the operator workflow without placing AI on the critical broadcast path.

## Added
- Intelligence Studio operator page.
- Live AI advisory status and deterministic-path status.
- Per-capability Auto / Review / Deny controls.
- Minimum-confidence controls.
- Pending approval queue with Approve and Reject / Fallback actions.
- Recent intelligence audit viewer.
- JSONL audit export.
- Explicit AI-disabled state with deterministic fallbacks.
- Producer role access to Intelligence Studio.

## Safety
AI remains advisory. Scheduler, Broadcast Queue, Broadcast Engine, emergency and playout paths remain authoritative. AI failure, timeout, rejection, denial or disablement cannot become broadcast failure.
