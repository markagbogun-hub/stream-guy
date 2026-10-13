# RadioCastOS 1.66.0 — Intelligence Operations

## Focus
Operational controls around the AI advisory layer, while keeping the deterministic broadcast engine authoritative.

## Added
- Deterministic per-capability AI policies: auto, review, or deny.
- Confidence thresholds with bounded normalization to 0.0–1.0.
- Operator approval and rejection workflow for review-gated AI results.
- Bounded intelligence operations audit trail with request and operation IDs.
- JSONL audit export for diagnostics/archive tooling.
- Explicit fallback decisions for disabled, failed, rejected, or non-AI results.

## Safety
AI output is never allowed to become a prerequisite for scheduler, queue, playout, emergency, or recovery execution. Rejection and AI failure resolve to deterministic behavior.
