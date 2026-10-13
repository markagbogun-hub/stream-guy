# RadioCastOS 1.80.3 — AI Programme Director

## Purpose

Turn the approved AutoDJ playlist and the station's approved local audio assets into a complete, timed programme rundown.

## Included

- **AI Programme Director** action in AI Broadcast Studio.
- Combines local music tracks with approved news, station IDs, commercials, sweepers, promos, and AI presenter clips.
- Configurable clock rules in the programme-builder API: opening news, station ID cadence, commercial cadence, and sweeper cadence.
- Uses only files that exist locally and music tracks with known positive duration.
- Reports unavailable break types and tracks total duration against the show's target.
- Preserves review-before-queue workflow. The director does not seize live playback or bypass the existing SEND TO QUEUE step.

## Operator workflow

1. Configure a show and its target duration in AI Broadcast Studio.
2. Populate AutoDJ with the station's music playlist.
3. Save approved presenter/news/ID/commercial/sweeper audio assets in the AI Presenter library where applicable.
4. Click **BUILD FULL PROGRAMME**.
5. Review the rundown and any warnings. Use **SEND TO QUEUE** only when ready.

## Safety and capability boundaries

This release builds the timed rundown from existing approved local audio. It does not fabricate missing audio or silently fetch and broadcast unreviewed stories. News must already be available as an approved audio asset for the opening news slot. Automated live submission remains governed by the existing queue workflow.

## Validation

- Python compileall
- release-version consistency check
- AI Programme Director test
- Show Intelligence test
- News bulletin test
- Pre-production tests
- Broadcast queue test
