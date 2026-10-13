# RadioCastOS 1.90.8 — Licence gate and code signing

**Installing?** See `docs/INSTALL.md` (includes the Windows SmartScreen steps for unsigned builds).

Online radio playout and streaming for Windows: one encode graph, an On Air desk,
automation, commercials, and station health.

## Programme review integrity (1.88.0)

Programme Studio now fingerprints the reviewed rundown and saved schedule snapshot. If the ordered segments, script, audio path, type or duration change after review, authorization is blocked until the current rundown is reviewed again. Preflight also blocks empty/unreadable audio files. Run `python scripts/production_readiness.py` for repeatable source-level checks. These checks do not replace Windows installer validation, actual audio/encoder tests or a supervised 24-hour soak test; see `docs/PRODUCTION-READINESS-1.88.0.md`.

## AI Programme Studio playout bridge (1.86.0)

Programme Studio can explicitly hand the next canonical broadcast-queue item to the local player using **PLAY NEXT QUEUED SEGMENT**. The operator must confirm the handoff; it may interrupt the current asset. Natural player-end callbacks are correlated to the same queued media path and recorded in application telemetry. This bridge does not automatically pre-empt AutoDJ. Player events are not independent encoder/as-run proof; import trusted station logs to confirm aired content.

## Guarded scheduled playout (1.87.0)

`src/scheduled_playout.py` provides an opt-in scheduler-to-player controller. It is disabled by default and blocks dispatch outside automation mode, while AutoDJ is active, or while the canonical queue/player is busy. Retries are bounded and delayed. The dashboard keeps application-level starts/completions separate from independent as-run confirmation. Import trusted station as-run records to confirm aired content; a player callback alone is not encoder proof. Station integration must explicitly enable and call the controller with accurate transport state.

## What matters on air

| Area | Behaviour |
|---|---|
| Encode | One ffmpeg graph for mic, music and caller. Master limiter ~−1 dBTP. |
| Backup | Same encode tees a second Icecast mount when Admin has a backup address. Native source is bypassed automatically for dual mount. |
| Desk timing | One remaining-time rule; named clock posts or WALL; encoder clock and bitrate on the source line. |
| Affidavit | Commercial as-run stores cart length, clean/cut, encoder handoff, seconds sent, listeners. |
| Loudness | New imports are measured; unscanned library carts are scanned in the background. Hot tracks are marked. |
| Health | One Station Health page: stop, stream, silence, backup, vault, incidents. |
| Live TALK/CALLER | Windows fader ducks live; encode graph is not restarted. |

## Checks

```
python scripts/check_version.py
python scripts/test_airchain_fixes.py
python scripts/test_console_timing.py
python scripts/test_live_graph.py
python scripts/test_nowplaying.py
python scripts/test_station_health.py
python scripts/test_asrun_close.py
```

Version history: `CHANGELOG.md`.

## Recent 1.78 series

| Release | Change |
|---|---|
| 1.78.17 | Air clock, shared remaining time, WALL vs clock posts |
| 1.78.18 | Cart loudness gate (AI prepare), backup encode |
| 1.78.19 | Single Station Health page |
| 1.78.20 | One encode graph with duck and limiter |
| 1.78.21 | Encoder clock on desk, nowplaying.json |
| 1.78.22 | Aired cart stamps encoder time |
| 1.78.23–25 | Live mix without reconnect hole; affidavit encoder span; health reads vault |
| 1.78.26 | Backup tee from primary; import loudness; drift alarm |
| 1.78.28 | Dual mount works with native setting on; library rescan |
| 1.78.29–31 | Library keeps measured LUFS and HOT note; drift and LOW shown in red |
| 1.78.32 | BREAK NEXT on the On Air desk; startup SyntaxError fixed |
| 1.78.33 | JINGLE NEXT; NOW card shows the track on air |
| 1.78.34 | Pre-launch polish: title-less library entries kept, current self-test, docs |
| 1.79.0 | Pads & Timers page (12 jingle pads, 4 countdown timers, track-left, top-of-hour); library Add Files and more audio formats |

Older centres (incident, continuity, vault detail) open from Station Health and stay advisory: they do not start playback or bypass Emergency Stop.


## AI Programme Director (v1.80.3)

Use **BUILD FULL PROGRAMME** in AI Broadcast Studio to assemble a timed rundown from the current AutoDJ playlist and approved local AI/news/station-ID/commercial/sweeper assets. Review the duration and any missing-asset warnings before sending the rundown to the broadcast queue. This workflow does not bypass normal playout controls. See `RELEASE-1.80.3.md`.


## AI Broadcast Workflow (v1.82.0)

`src/ai_broadcast_workflow.py` coordinates the full prepare path: approved station assets → configured trusted/fresh news → rendered bulletin and presenter audio → timed programme rundown → review → explicitly authorized queue submission. Provide the station's real feed, voice/TTS, asset-catalogue, and broadcast-engine adapters as callbacks. Missing or invalid news/audio causes a clear failure rather than a fabricated programme. This workflow does not take ownership of live playback.

Run `python scripts/test_ai_broadcast_workflow.py` to validate the workflow contract.


## Programme Studio voice regeneration (v1.83.1)

Select a non-music, non-news presenter segment and choose **REGENERATE** to render its current script with the configured station presenter engine. The resulting file is saved to the approved AI presenter library and attached to the rundown off-air. If the script is changed or audio is regenerated, review status resets: run PREFLIGHT and REVIEW again before authorization. News regeneration remains blocked until a trusted current-news adapter supplies validated source material. This operation does not start playback.


## Live news bulletin and as-run verification (v1.84.0)

In AI Programme Studio, **FETCH + RENDER NEWS** uses the configured HTTPS RSS/Atom feeds, trusted-domain allowlist, freshness limit, and available presenter script/TTS engine to create a real bulletin off-air. The segment is added only after retrieval and audio validation succeed; its source metadata is stored with the rundown item. Run PREFLIGHT and REVIEW again before authorization.

**IMPORT AS-RUN CSV** matches rundown audio to an external broadcast/as-run report by exact media path. Explicit completion statuses are reported separately from start-only events. Queue state by itself is not treated as proof that a segment aired. Scheduling remains a draft until a station scheduler adapter is connected.


## Scheduler integration & broadcast telemetry (v1.85.0)

AI Programme Studio can now save timezone-aware one-time schedule bookings. Bookings remain pending until an operator explicitly chooses **AUTHORIZE AIR**. At the due time, the scheduler dispatches the complete validated rundown to the canonical in-app `BroadcastEngine` queue. Scheduled rundowns require an audio asset for every segment; incomplete bookings are rejected.

The broadcast-domain coordinator emits start/completion events, and Programme Studio records these in a local JSONL telemetry file. The report distinguishes schedule state, queue state, and observed engine events from external as-run confirmation. Engine events are application telemetry, not independent encoder proof. A downstream playout adapter must consume the canonical queue for playback; use external encoder/as-run records for authoritative confirmation that content aired.

Run `python scripts/test_programme_runtime.py` to test booking authorization, due-time dispatch, and telemetry.
