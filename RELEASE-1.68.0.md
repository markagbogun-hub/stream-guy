# RadioCastOS 1.68.0 — Intelligence Runtime

## Summary

RadioCastOS 1.68.0 connects advisory intelligence to the live broadcast-domain lifecycle without putting AI on the critical playout path.

## Added

- Asynchronous Intelligence Runtime.
- BroadcastEvent integration for intelligence state and health.
- Automatic metadata intelligence requests for current BroadcastItems.
- Strict per-request runtime deadlines.
- Deterministic fallback when AI is unavailable, rejected, denied, invalid, or late.
- Capability health metrics: requests, AI successes, fallbacks, reviews, errors, timeouts and latency.
- Runtime correlation IDs and operator notifications.

## Safety

The Broadcast Engine, queue, scheduler, emergency path and reliability recovery remain authoritative. Intelligence work executes outside the broadcast publisher thread and cannot block playout.
