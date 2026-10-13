# RadioCastOS 1.89.0 — Production Readiness Review

## Release focus

This release hardens deployment/export packages against accidental corruption and content changes. Newly exported packages carry SHA-256 hashes for every `data/` member. Inspection and import verify the manifest file list and digests before any configuration data is written.

## What integrity validation means

- `verified`: all declared files exist, no unexpected data members exist, and each file matches its declared SHA-256 digest.
- `legacy_unverified`: the package uses the supported schema-1 format but has no integrity map. It remains compatible for migration, but its contents have not been checked against hashes.
- Invalid or altered new-format packages are refused before import writes any files.

SHA-256 here detects content mismatch; it is **not** a digital signature. A verified manifest does not prove who created the package or protect against an attacker who can replace both the data and its manifest.

## Source-level checks completed

- Python compilation (`python -m compileall -q src scripts`)
- Release version consistency
- Import validation
- Existing scheduled playout, programme runtime/review, news, broadcast engine/queue, preflight and deployment safety checks
- New deployment integrity tests for tampering, missing members, duplicate ZIP names, secret redaction before hashing, and legacy compatibility

Run `python scripts/production_readiness.py` from the extracted release directory to repeat the focused suite.

## Still required on the station computer

- Build and launch the Windows installer on a clean Windows account.
- Back up station data and test a migration using a copy of the package before changing the live station.
- Verify audio device, player-to-encoder route, off-air monitoring, stream reconnect, power/network recovery and real as-run reconciliation.
- Run a supervised 24-hour soak test before unattended operation.

No source-level test can establish that the actual FM transmitter or online listeners received audio. Continue to use independent encoder/as-run evidence for that confirmation.
