# RadioCastOS 1.84.0 — Live News Bulletin & As-Run Verification

## Added
- Programme Studio can fetch current headlines from configured HTTPS RSS/Atom feeds using the station's domain allowlist and freshness settings.
- The configured presenter script/TTS runtime renders a real news bulletin off-air. The rundown only changes after successful news retrieval, script generation, and audio-file validation.
- News segments retain source titles, publishers, links, publication metadata, retrieval timestamp, and story count.
- Programme Studio can import a station/broadcast-engine as-run CSV and correlate records to rundown assets by exact normalized media path.
- Air reporting separates queue state, confirmed complete as-run records, and start-only records.

## Safety
- News retrieval and TTS failures fail closed; no fabricated headline/audio placeholders are inserted.
- Adding or updating a bulletin returns the programme to draft and invalidates review; operators must rerun PREFLIGHT and REVIEW before authorization.
- `clean` as-run events are treated as started, not completed, because the existing commercial log defines clean as a full start rather than proof of full duration.
- An external as-run file is evidence only to the extent of its own event/status fields. The import does not start playback, connect a scheduler, or prove listener reception.

## Verification
- Python syntax compilation for `src/*.py`
- Programme air-report tests (5 cases)
- Programme Studio live-news integration checks
- AI Broadcast Workflow, AI Programme Director, Programme Studio regeneration, news feed, queue, and Studio layout regression tests
- Version consistency check

Note: the full GUI-oriented test sweep cannot run in a headless environment without a display server; the tested non-GUI regressions passed.
