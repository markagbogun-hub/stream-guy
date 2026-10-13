# RadioCastOS 1.88.0 — Programme Review Integrity & Production Readiness

## Added / improved
- Stable SHA-256 content fingerprint for programme identity and ordered rundown segments.
- Review records the content fingerprint. Authorization blocks if the rundown changes after review and requires a fresh review.
- Scheduled bookings store their source rundown fingerprint. A stale or legacy booking without a matching fingerprint is not authorized; create a new schedule draft after reviewing the current rundown.
- Programme Studio preflight now blocks empty/unreadable audio files and supports both `audio` and `audio_path` fields.
- Regression tests cover fingerprint stability, script/order changes, and persisted booking fingerprints.

## Safety
- AI remains an advisory/off-air production assistant. It does not directly mutate the authoritative broadcast queue without the existing explicit operator workflow.
- Scheduled dispatch remains gated by explicit authorization and due time.
- Local file checks, review fingerprints, queue telemetry and player completion do not prove that the encoder transmitted audio or that listeners received it.

## Release validation status
- Python source compilation: validated in the development environment.
- Version/changelog consistency: validated in the development environment.
- Source imports: validated in the development environment.
- Focused scheduler, programme runtime, news, preflight and broadcast-engine tests: validated in the development environment.
- Windows installer, GUI behavior on a Windows desktop, audio-device compatibility, encoder integration, 24/7 soak testing and real-station as-run verification: **not validated here; required before production deployment**.
