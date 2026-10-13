# RadioCastOS 1.70.0 — Show Intelligence

## Summary

RadioCastOS 1.70 adds an operator-ready Show Intelligence board built from an immutable BroadcastQueue snapshot.

### Added

- Upcoming clock awareness from current, next, and upcoming BroadcastItems.
- Presenter brief, news brief, music context, talking points, segment preparation, and social previews.
- Consolidated immutable `ShowBoard` with per-element AI/fallback status.
- Queue revision correlation and advisory `intelligence.show_board` publication.

### Safety

- Show Intelligence never selects, inserts, removes, or mutates BroadcastItems.
- It consumes a copied queue snapshot and publishes advisory data only.
- Every board element can fall back independently.
- AI failure, timeout, disabled AI, or missing providers cannot block deterministic playout, reliability recovery, or emergency handling.
