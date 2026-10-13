# RadioCastOS 1.89.0 — Verified Deployment & Recovery Packages

## Added / improved
- New deployment exports include SHA-256 digests for all included data files, calculated from the exact bytes written to the archive after redaction.
- Package inspection and import verify declared members and hashes before any configuration file is written.
- Duplicate ZIP member names, missing/extra declared files, malformed digest maps, and changed file contents are rejected.
- Older schema-1 packages without hashes remain supported and are marked `legacy_unverified` in inspection results.
- Added `scripts/test_deployment_integrity.py` and included it in the source-level readiness checks.

## Safety boundary
SHA-256 checks detect accidental corruption and unauthorized content changes relative to the manifest, but the manifest is not signed. Do not treat a verified package as proof of publisher identity. Import remains explicit; this release does not automatically restore a package or overwrite local files.

## Validation limitations
Source-level validation does not certify the Windows installer, physical audio devices, stream encoder, network/power recovery, or a 24-hour station soak test. Those checks remain required on the actual broadcast computer.
