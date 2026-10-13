# RadioCastOS 1.90.8

## v1.90.8 — Licence gate for the AI Producer, and code signing for releases

### Fixed
- **AI Producer now respects the licence package.** CREATE and APPROVE (Control Center and the AI Producer card), plus the background air, schedule and tick steps, were not covered by the licence gate, so an unlicensed Basic or an Intermediate install could use a Full-package feature. They now need the AI package and show the normal "needs the Full package" message otherwise. New checks in `test_licensing.py` fail if any of these entry points loses its gate.

### Added
- **Code signing.** `installer.iss` signs the installer and uninstaller when `iscc` is given `/DSignToolName`, and `scripts\sign-file.bat` signs a file with `signtool` using either a certificate in the Windows store (`RCOS_SIGN_THUMBPRINT`, preferred for EV and token certificates) or a `.pfx` file (`RCOS_SIGN_PFX`, `RCOS_SIGN_PFX_PASSWORD`). `local-build.bat` signs `RadioCastOS.exe` before building the installer, then the installer itself. Set `RCOS_REQUIRE_SIGNING=1` to make a release build fail rather than produce an unsigned file. See `docs/CODE-SIGNING.md`.
- `test_signing_config.py` checks the installer, the signing script and the build script stay wired together.

### Needs a Windows check
- A signed build on a clean Windows account: right-click the installer and exe, Properties, Digital Signatures, and confirm the timestamp is present.

## v1.90.7 — Read-only status page for phone browsers

### Added
- **Phone status page.** Settings > Remote Management has a new tick, *Also serve a read-only status page for phone browsers* (off by default, and only works while remote monitoring is on). Open the station address (for example `http://192.168.1.20:8765`) in a phone browser and paste the access token. The page shows ON AIR / OFF AIR / CONNECTING / RECONNECTING / STREAM ERROR, now playing, time on air, bitrate, listeners (when the server reports them), reconnects, health, and active alerts. It refreshes every 5 seconds, pauses while the tab is hidden, and warns when the station's own figures have gone stale or the station cannot be reached.
- **Read-only by design.** The page only reads `/api/v1/status` and `/api/v1/alerts`; it has no buttons that change anything, and Go Live / Stop are not reachable from it.
- **Safety.** The page is a fixed shell with no station data; the numbers come from the same token-protected API. The token goes in an Authorization header, never in the web address, and is kept for this browser tab only unless *Remember on this phone* is ticked. Strict content-security policy (only the page's own script and style, connections back to the station only), no-store, no-referrer and no-index headers, and all station text is shown as plain text. Wrong tokens count toward the existing lock-out. With the tick off, every path still answers 401, as before.
- Plain HTTP is not encrypted: over the internet use a VPN or an HTTPS reverse proxy.

### Tests
- New `test_status_page.py` (real loopback sockets, the page's headers and security policy, and the page script run against a stub browser when Node is installed). Needs the Windows and phone check in `docs/WINDOWS_TEST_CHECKLIST.md` (1.90.7).

## v1.90.6 — Copy plays from the As-Run log

### Added
- **Copy selected** and **Copy all** in the Commercial As-Run Log window. The plays paste straight into Excel, an email or a chat as tab-separated columns (Date, Time, Campaign, Spot, Program, Duration, Status). **Ctrl+C** on the table copies the selected plays and **Ctrl+A** selects them all. The window says how many plays were copied. Export CSV and Print Report are unchanged.

### Tests
- New `test_asrun_copy.py`. Needs the Windows check in `docs/WINDOWS_TEST_CHECKLIST.md` (1.90.6).

## v1.90.5 — AI Presenter Studio polish

### Changed
- **Clearer tooltips** on controls that had none: Break type, personality, slogan, presenter name, AI Clock Auto, Cancel on LIVE takeover, the approve-bulletin button, PREPARE AI BREAK, SAVE TO LIBRARY, CLEAR PREPARED BREAK, program name and length, Pull current web news, GENERATE FULL PROGRAM, and the main and backup news feed boxes.
- **Wording.** "Break" is now "Break type", "Break per minute" is "Break by minute", "Claims/rules to avoid" is "Claims to avoid", and the engine choice "Offline (Windows)" is "Offline (free)", because the offline engine now covers Windows, Piper and Kokoro voices.
- No layout, setting or behaviour change.

## v1.90.4 — Automation setup polish

### Changed
- **The setup checklist wraps cleanly.** The ticks sit on one line and the three buttons (Quick commercial setup, Demo setup, Replace demo files) on their own line, so nothing is cut off on a narrow window.
- **The missing-files check can no longer slow the page.** It runs in the background (at most once a minute, or at once when the files change) and is limited to 3,000 files, so a slow or disconnected drive cannot freeze Automation. It shows "Files: checking…" until the first result.
- **Day chips work from the keyboard** (Tab to a day, Space or Enter to tick it).

### Added
- `docs/AUTOMATION-QUICK-START.md`: three short routes (try the demo, build it yourself, check it), and the Windows checklist now covers every new Automation control.

### Tests
- `test_automation_setup.py` covers the bounded missing-file count.

## v1.90.3 — Replace demo files one by one

### Added
- **Replace demo files…** (Automation page, and in the amber demo bar). Instead of throwing the demo away and starting from nothing, a customer can swap each demo file for one of their own:
  - Select a demo file, press **Replace with my file(s)…** and pick audio (or press **Replace with Library selection**). The new file takes the demo file's place **everywhere it is used** (every program list and every campaign), in the same position, and the rest of the demo keeps playing.
  - One row can take several files. To swap many rows at once, select N rows and choose N files (matched in the order shown).
  - **Remove selected** takes a demo file out of the setup (the audio file itself is not deleted).
  - The list says what is still **DEMO** and what is **yours**, with a running count ("18 demo files left to replace"); **Show my own files too** lists everything.
  - **Drop 'DEMO •' from names** tidies the program and campaign names (the schedule follows; a name that would clash is left alone).
- **Keep demo as my setup** now says how many demo files are still in use. Replace demo files stays available afterwards, so a customer can carry on swapping over days.
- The demo tour has two new steps (make it yours; keep or restore).

### Tests
- New `test_demo_replace.py`.

## v1.90.2 — Easier Automation setup, a working Music button, and a demo

### Fixed
- **The Music button (Program & content) did nothing.** It tried to save into a program field that does not exist, so the press failed silently. It now adds tracks to the program's playlist.
- **"Ads every N songs" and "ID every N songs" did nothing** on any normal install: the engine only read them when no imaging rules existed. They now keep two clearly named imaging rules up to date (Ad Break, Station ID), typing a number counts (not only the arrows), and an imaging rule's **count** (for example 2 ads per break) is now honoured by the scheduler.
- **News files and campaign booked spots / rate per spot were lost on restart.** They were saved but never read back.
- **Silent presses now say why.** A coloured line at the top of the Automation page explains what a button did, or why it could not (nothing selected, AutoDJ off, name already used, bad time), and any unexpected error is shown there too instead of only in the log. Every button also turns green for a moment when pressed.
- LIVE TAKEOVER no longer shows "Playing next ✓" when AutoDJ is off.

### Added
- **Schedule builder.** Tick the days (or Every day / Weekdays / Weekend), pick a time block (All day, Morning, Afternoon, Evening, Overnight) or type a time such as 6am or 18:30, choose the program, press **Add to schedule**. Overlaps are flagged before they are saved, duplicates are skipped, and a **week-at-a-glance** bar plus a plain sentence show what is covered (and that gaps mean silence).
- **Quick commercial setup.** One window: choose the audio, name it, pick how long it runs, pick Light / Normal / Heavy pacing. Creates the campaign and the ad rules together.
- **Setup checklist** under the master switches: music, station IDs and jingles, commercials, schedule coverage, missing files.
- **Demo setup.** One click loads a ready-made station (two programs, a full-week schedule, 28 short generated audio files, three commercial campaigns, fast pacing) so every part of Automation can be tried. Your own setup is copied aside first and comes back exactly as it was with **Restore my setup**; **Keep demo as my setup** makes it permanent.

### Tests
- New `test_automation_setup.py`, `test_automation_demo.py`, `test_automation_setup_ui.py`.

## v1.90.1 — Automation page buttons now respond

### Fixed
- **Buttons on the Automation page now change when you press them.** Before, most of them did their job but looked the same, so it seemed nothing had happened.
  - **LIVE TAKEOVER** is now a toggle: it turns into a red **RELEASE TAKEOVER** while the takeover is on, and pressing it again releases it (it used to only log "already active").
  - **AI PRESENTER** shows PREPARING…, then ON AIR IN Ns, then AI ON AIR, and is locked while the presenter is busy.
  - **Return to AutoDJ** says "Already on AutoDJ" (or "AutoDJ is off") when there is nothing to return from.
  - **Play Next, Emergency Stop, Refresh Preview, Save Program, Add, Remove Selected** and the **category assign buttons** briefly show a tick (for example "✓ 3 added", "Saved ✓") so a press is acknowledged. Remove Selected says "Select a row first" when nothing is selected.
  - **Enable 24/7 AutoDJ** and **Presenter takeover** now update the status line and the log at once, and the two tick boxes always show what is really saved, even when the On Air desk or an AI prompt changed it.

### Tests
- New `test_automation_buttons.py`.

# RadioCastOS 1.90.0

## v1.90.0 — One-button AI Producer

### Added
- **CREATE, then APPROVE.** The AI Presenter can now make four things with one button each way:
  - **PRESENTER LIVE** — a short link for what is playing; on air the moment you approve it.
  - **TOP-OF-HOUR NEWS** — a bulletin written only from current headlines (no headlines, no bulletin). Held until the next :00; approved up to 3 minutes after :00 it airs at once. A note warns when the headlines will be 30+ minutes old at air time.
  - **FULL PROGRAMME** — the long presenter-led programme with current news; on air when approved.
  - **SHOW** — a hosted show (opening, music links, news, close) spread over the show length. The news lands on the top of the hour when that falls inside the show. Pieces are queued, and the show is saved in Show Builder.
- Where: the new **ONE-BUTTON AI PRODUCER** card on the Presenter Desk page, and three big tiles on the On Air desk (kind picker, CREATE, APPROVE).
- Nothing airs from CREATE. Approval is one press by a Producer. EMERGENCY STOP cancels a job waiting for approval and anything the producer had lined up.

### Notes
- With AutoDJ automation and Presenter takeover on, approved news and show pieces go through the normal production queue (they survive a restart; a piece that misses its time by more than its grace is skipped, never aired late in a burst). With automation off, RadioCastOS times them itself and must stay open.
- Show links never name a song, because the clock, not the AI, decides which songs surround them.

### Tests
- New `test_ai_producer.py`. `test_console_widgets.py` now expects 22 tiles.

## v1.89.8 — Sidebar scrollbar visible again
- **Fixed: the sidebar page list showed no scroll line.** The slim scrollbar was created before the page list inside the same canvas, so Tk stacked the list on top and hid it. The bar is now raised above the list whenever pages are out of view. Mouse wheel scrolling is unchanged.
- The sidebar's height check now subtracts the MENU button, so on short windows the buttons tighten (and the shortcut hint hides) before pages are pushed out of view.

## v1.89.7 — TAKEOVER tile can be released
- **Fixed: the TAKEOVER tile stuck on ACTIVE.** Pressing it while a takeover was on air only logged "already active", so the only way out was RETURN TO AUTODJ, which is hidden on the compact console. The tile is now a toggle: press it again to release the takeover. It works with AutoDJ on or off and is not Producer-gated.
- The active tile now reads `ACTIVE · press to release` (it used to say "AutoDJ paused", which was wrong when AutoDJ was off).

## v1.89.6 — Compact One-Screen Operator Console
- **The On-Air Console control area now fits one screen without scrolling.** It had grown to seven stacked rows of tall buttons (about 330 px); it is now a four-row control strip (about 130 px).
  1. **Master row:** AUTO RADIO button, the programme times and a one-line status, side by side.
  2. **Live actions:** PREPARE BREAK, LOAD APPROVED, PRESENTER ON AIR, RETURN TO AUTODJ.
  3. **Manual modes:** AUTO PROGRAM, AI SHOW, AUTOPILOT in one row.
  4. **Two slim settings:** Auto-run prepared AI shows; Go live on start.
  5. CANCEL GO-LIVE still appears only while the go-live countdown runs, and takes no room otherwise.
- Button labels are short ("AUTO PROGRAM", "AI SHOW", "AUTOPILOT ON", "AUTO RADIO ON"); the full explanations moved into tooltips. Heavy button padding is gone; the script preview shows 3 lines instead of 4.
- Every button keeps its name and function. Nothing was removed.
- Added a layout guard test so the strip cannot quietly grow again.
- The Presenter Command Center tab is unchanged.

## v1.89.5 — AUTO RADIO: One Button for News, Shows and Programmes
- **New: AUTO RADIO button** at the top of the AI Presenter On-Air Console. One press (after a confirmation that lists exactly what will run) starts the whole station:
  - AutoDJ plays the music and the presenter may take over (the existing Autopilot);
  - news bulletin at :00, station ID at :15, music links at :30 and :45, using your news feeds when they are set;
  - a complete presenter programme is written, voiced and put on air at the times you choose (default 06:10, 12:10, 18:10);
  - the offline backup voice is armed, so a failed online AI does not leave a gap.
- Click again to stop. The presenter stops and AutoDJ keeps playing music. Turning Autopilot off by hand also ends Auto Radio.
- **Programmes at** box: 24-hour times, comma-separated. A slot starts up to 2 minutes early and up to 25 minutes late, then it is skipped, so an old programme is never aired at the wrong time. A slot never starts twice, even after a restart.
- It adds no new route to the air. Programmes use the existing AUTO PROGRAM path, so the countdown, EMERGENCY STOP, manual takeover and the "another break is on air" checks all still apply. Nothing starts while the operator has manual control.
- Licence gating follows the existing AI features.
- Existing buttons (AUTO PROGRAM, CREATE + AIR COMPLETE AI SHOW, AUTOPILOT) are unchanged.
- Added scheduling and controller tests.

## v1.89.4 — Backup Offline Voice Setting
- **New: Backup voice** in the AI settings (Offline Voice section). Pick the offline voice (Windows, Piper, Kokoro or a cloned voice) that speaks when the online AI fails: no credit, no internet, key refused. Before, the offline voice could only be chosen after switching the whole engine to Offline.
- A line next to it states whether the backup is armed: "Backup ON: if the online AI fails, breaks use <voice>" or "Backup OFF: an online failure shows an error". It is armed with the existing **Fall back to offline** tick box.
- **TEST BACKUP** plays a sample in the backup voice on this PC's speakers, never on air.
- The no-credit message now points to these two settings.
- Not changed: Fall back to offline is still off unless you tick it.

## v1.89.3 — Clear Operator Messages & Setup Errors Stop Retrying
- **Fixed: endless "Encoder could not start" loop.** With Force Reconnect on, a setup problem such as "No active audio source. Enable at least one mixer device before going live." (or ffmpeg missing) was retried every few seconds and hidden behind a generic banner. Setup errors now stop and keep their message on screen; real connection drops still retry.
- **AI Presenter errors in plain words.** An exhausted OpenAI balance (429 insufficient_quota) no longer shows raw JSON. It now explains that the account has no credit, and what to do (add credit, or switch to the offline voice/script). Rate-limit, bad-key, model-not-found and server errors are explained too. The full response stays in the log.
- The status strip no longer cuts messages at 44 characters ("Retr…"); it now allows 120.
- Added tests for the retry fix, the error wording and the status text.

## v1.89.2 — Station Package Dialog Polish
- The Import dialog no longer promises an overwrite choice that does not exist; it now says existing files on this PC are kept and only missing ones are added.
- Long export/import paths and messages in Station Profiles and Deployment wrap instead of running off the card.
- Visual result not checked on a Windows screen (code-level change only).

## v1.89.1 — Deployment Package Hardening & Playout Tracking Fixes
- **Fixed: hash-check bypass.** A member named with backslashes (for example `data\\library.json`) was invisible to the SHA-256 check but was still written by import. Verified packages now refuse any backslash, absolute, drive-letter, `..`, case-insensitive-duplicate or undeclared member.
- **Fixed: unbounded memory during verification.** Inspecting a package read every member fully into memory before any size limit applied. Members are now streamed and capped while hashing.
- **Fixed: half-applied imports.** A package that failed validation partway (for example a bad station file after `config.json`) had already replaced `config.json`. Everything is now validated and staged first; a failed import changes nothing.
- Verification and import now read the package once, so the file cannot change between the check and the write.
- Redaction now also covers the operator PIN hash, `*_password` / `*_secret` / `*_token` / `*_api_key` keys, and `user:password@` embedded in URLs. Ordinary settings such as `max_tokens` are not touched.
- The Import dialog now states whether the package is verified or an unverified legacy package before you confirm.
- Export removes its temporary file if writing fails.
- **Fixed: scheduled playout.** A file that airs more than once is now tracked per airing (completion and as-run confirmation no longer pile onto the first one). A path-only as-run row can no longer confirm an item that never started. An item that fails all retries is dropped from the queue and audited (`skipped_after_retries`) instead of blocking every item behind it; pass `skip_exhausted=False` to keep the old behaviour.
- `scripts/validate_imports.py` falls back to the test stand-in when `tkinter` is not installed, so the readiness suite runs on headless machines.
- Added regression tests for all of the above.


## v1.89.0 — Verified Deployment & Recovery Packages
- Deployment exports now include SHA-256 digests for every packaged data file after secret redaction.
- Deployment inspection/import verifies the manifest file list and every digest before writing configuration, refusing altered, truncated, duplicate-member, or inconsistent packages.
- Added an explicit integrity status for new verified packages and legacy schema-1 packages without hashes; legacy packages remain compatible but are clearly marked unverified.
- Added regression coverage for tampering, missing/extra files, duplicate archive entries, and backward compatibility.
- This integrity check detects accidental damage or content changes; it is not a digital signature and does not establish who created a package.

## v1.88.0 — Programme Review Integrity & Production Readiness
- Added a stable SHA-256 fingerprint of programme identity and ordered rundown content, including segment scripts, audio paths, types and durations.
- Programme review records the exact rundown fingerprint; authorization is blocked if the rundown has changed since review, preventing stale approval from authorizing modified content.
- Scheduled bookings persist the rundown fingerprint and authorization checks it before changing booking state, preventing a stale schedule snapshot from being authorized after edits.
- Programme preflight now accepts the supported audio/audio_path field variants and blocks empty or unreadable audio files in addition to missing media and invalid durations.
- Added regression tests for fingerprint stability, edit/order sensitivity and booking fingerprint persistence.
- Production readiness is documented separately; Windows installer builds, target-station audio devices, encoder delivery and real as-run reconciliation still require validation on the actual station machine.

## v1.87.0 — Guarded Scheduled Playout & As-Run Reconciliation
- Added a disabled-by-default scheduler controller that only dispatches due canonical queue items after explicit enablement and only when station mode, AutoDJ, player, and queue gates permit it.
- Added bounded retry/backoff for rejected or failed dispatch attempts and an optional JSONL audit trail.
- Added dashboard counts that distinguish scheduled/dispatched/started/player-completed items from independently confirmed as-run items.
- Added exact-path/item-ID reconciliation for imported as-run rows; start-only rows never count as completed/confirmed.
- Added tests for disabled defaults, station/AutoDJ safety gates, due-time handling, retry backoff, and independent as-run confirmation.
- Integration boundary: station startup does not automatically enable this controller. A station-specific caller must wire it to the player callback and pass accurate station/AutoDJ state. Player completion is not encoder proof.

# RadioCastOS 1.87.0

## v1.86.0 — Live Playout Bridge & End-to-End Verification
- Added an explicit operator-confirmed bridge from the canonical broadcast queue to the existing local PlaylistPlayer.
- Natural player-end callbacks complete only the matching tracked queue item and write start/completion telemetry.
- Added failure telemetry for missing media, rejected starts, player exceptions, and queue races.
- Added a Programme Studio PLAY NEXT QUEUED SEGMENT action with interruption warning and expanded queue/telemetry reporting.
- Added regression coverage for confirmation gating, queue identity, failed starts, and natural completion.
- Live encoder confirmation remains dependent on independent station as-run/encoder evidence; playout bridge is operator-triggered and does not auto-preempt AutoDJ.

# RadioCastOS 1.85.0

## v1.85.0 — Scheduler Integration & Broadcast Telemetry
- Added persistent one-time AI Programme Studio schedule bookings with timezone-aware due-time validation.
- Bookings require explicit AUTHORIZE AIR before dispatch to the canonical BroadcastEngine queue.
- Added broadcast-engine start/completion/failure telemetry JSONL recorder and programme report counts.
- Fixed PLAYOUT_ENDED payload to retain the item that actually completed.
- Clarified that queue dispatch and engine events are not equivalent to independent encoder/as-run proof.

# RadioCastOS 1.84.0

## v1.84.0 — Live News Bulletin & As-Run Verification

- Added Programme Studio FETCH + RENDER NEWS: retrieves headlines from configured HTTPS RSS/Atom feeds, applies configured trusted-domain and freshness rules, generates a bulletin script with the configured presenter engine, and synthesizes real audio off-air.
- The bulletin is inserted into the selected rundown only after news retrieval, script generation, and audio validation all succeed. Source titles, publishers, links, publication metadata, retrieval timestamp, and story count are retained with the segment.
- News failures fail closed: no placeholder headline/audio is added, and the programme remains unapproved until preflight and review are repeated.
- Added IMPORT AS-RUN CSV to correlate external broadcast logs to rundown items by exact normalized media path. Only explicit completion statuses count as confirmed aired; started-only records are reported separately. Queue state alone is never promoted to on-air confirmation.
- Added regression tests for exact-path matching, completion versus start-only statuses, invalid log schemas, and the Programme Studio integration entry points.

## Integration boundary

- Live news retrieval and voice rendering use the station's configured feeds, trust settings, and available AI Presenter/TTS runtime. Internet availability and provider credentials remain station-environment dependencies.
- As-run confirmation requires importing a real broadcast-engine/as-run CSV with media-path and status columns. The importer does not itself create playout events or claim that a stream reached listeners.
- Scheduling remains a draft-only workflow unless the station scheduler adapter is separately configured.

## v1.83.1 — Programme Studio Voice Regeneration

- Connected the Programme Studio's REGENERATE action to the station's configured presenter script/TTS engine.
- Regenerated audio is rendered off-air, saved into the approved presenter library, and attached to the selected rundown segment.
- Changing rendered audio resets programme review state; preflight and REVIEW must pass again before authorization.
- Regeneration refuses MUSIC assets and NEWS segments without the trusted-news material adapter; it does not fabricate current headlines.
- The action reports failures, validates the resulting audio file, measures duration when the local media probe is available, and never starts playback.

## v1.83.0 — AI Programme Studio

## Added
- Dedicated Programme Studio tab in AI Studio with one-click creation from Morning Show, Drive-Time Show, News Programme, Talk Show, and Overnight Automation templates.
- Timed rundown review and reordering, independent audio preview, script editing, and preflight validation.
- Explicit Review, Schedule Draft, and Authorize Air workflow with confirmation before existing production-queue handoff.
- Queue reporting separates pending/queued items from queue items marked PLAYED and explicitly warns that PLAYED is not independent broadcast/as-run confirmation.
- Adapter boundaries are disclosed in the UI: current-news retrieval, new TTS rendering, active scheduler integration, and independent on-air/as-run confirmation must be connected/configured separately.

## Safety and integration notes
- Programme creation uses the station's current AutoDJ playlist and existing approved local clips; it does not fabricate missing audio or news.
- Schedule Draft saves a proposed time in programme metadata and does not claim to activate the station scheduler.
- Authorize Air submits eligible non-music segments to the existing AI production queue only after local asset preflight and operator confirmation. It does not start playback.

---

# RadioCastOS 1.82.0

## v1.82.0 — End-to-End AI Broadcast Workflow

- Added `ai_broadcast_workflow.py` to orchestrate approved asset discovery, configured fresh/trusted news retrieval, bulletin audio generation, presenter-link rendering, timed rundown planning, review, and controlled queue handoff.
- Added durable per-run workflow records and stage callbacks for UI progress reporting.
- News-led runs fail closed when no trusted news provider, validated stories, or real bulletin audio is available; they do not silently misrepresent a show as current-news ready.
- Added strict asset-kind validation, plan/run matching, explicit operator authorization, and duplicate-submission guards at the workflow layer.
- The workflow is playout-engine agnostic: station-specific feed, TTS, media-library, and queue adapters are injected rather than guessed. It never starts/stops live playback.

### Known capability boundary

This release provides the end-to-end orchestration API and regression coverage. Connecting the station's specific news/TTS/media-library adapters to a polished GUI wizard still requires those runtime integrations to be configured. Queue submission does not guarantee that the encoder or stream is live.

## v1.81.0 — AI Programme Director & Controlled Air Handoff

- Added a reusable programme-director service that assembles a timed rundown from real, approved local music, news, presenter, station-ID, sweeper, commercial and promo assets.
- Added configurable programme duration, station-ID cadence, sweeper cadence, commercial-break cadence, opening news and closing presenter-link rules.
- Added an auditable JSON rundown manifest with segment offsets, asset metadata, duration, warnings and run correlation.
- Added strict asset checks: missing files, unapproved assets and invalid durations are rejected; the director never fabricates audio for unavailable assets.
- Added explicit per-run authorization before queue handoff and duplicate-run protection.
- Kept playback ownership in the existing deterministic broadcast engine; the director does not start, stop, or take over live playback.

### Known capability boundary

This service orchestrates supplied assets. It does not itself fetch or fact-check news, synthesize voice audio, or create missing music/commercial assets; upstream news/TTS workflows must supply those assets. Handoff is a queue submission, not a guarantee that a station's output device or stream is live.



## v1.80.3 — AI Programme Director & Timed Clock

- Added a deterministic full-programme clock builder that combines real AutoDJ music with approved local news, station IDs, commercials, sweepers, promos, and AI presenter clips.
- Added configurable station-ID, commercial, and sweeper cadence; optional news-at-opening; missing asset warnings; and target-duration accounting.
- The director never invents audio, never queues missing files, and does not take over live playback. Existing show review and queue handoff remain in control.
- Release validation includes programme-clock tests, version consistency, source compilation, and ZIP integrity.


## v1.80.1 — On Air desk polish

### Changed
- The header **Go Live** button is gone; GO LIVE stays on the On Air desk, the dashboard and Ctrl+G.
- **TAKEOVER** tile no longer clips: one-column tiles put the icon beside the title, and the wording is shorter (`TAKEOVER` / `ACTIVE · AutoDJ paused`).
- PREVIOUS and NEXT now have a sub-line, so the transport row lines up.

### Fixed
- The On Air desk now **scrolls** on short windows. Before, the AI Presenter, Breaks & Jingles rows and the rundown could be cut off with no way to reach them.

## v1.80.0 — Simpler entry of new commercial spots

### Changed
- **One window instead of eight questions.** Add Campaign (Automation → Commercial Campaigns) used to ask for the name, start date, end date, daily limit, hourly limit, priority, length, booked count and rate in nine separate pop-ups, and it refused to start unless you had first selected the audio files on the Library page. It is now a single form:
  1. **Campaign name** (filled in from the first audio file's name if you leave it empty).
  2. **Advert audio files**: ADD AUDIO FILES… opens the file picker (several files at once, and it remembers the folder). If tracks are selected on the Library page, they are already in the list, or can be added with one button.
  3. **When should it run?** From / To dates, or one click on 1 week, 2 weeks, 1 month, 3 months or Always.
  4. **Plays per day** (0 = no limit).
  - **More options** (closed until needed): plays per hour, priority, spot length, booked spots, rate per spot.
- Mistakes are shown in red inside the form, so nothing typed is lost. All problems are checked together: a missing name or audio file, a file that is not audio or cannot be found, a duplicate campaign name, bad dates, an end date before the start, and numbers that are not numbers. Enter creates the campaign and Esc cancels.
- A warning (with a Save anyway choice) appears when an end date has already passed, when a spot file is already in another campaign (the as-run report counts it under that campaign), or when plays per hour is higher than plays per day.

### Added
- **Edit / Add Spots** (also a double-click on a campaign): change a campaign's dates, limits and audio files, or add a new spot to a running campaign. Until now the only way to change a campaign was to delete and recreate it. Counters, plays and make-good history are kept.

### Fixed
- In the Campaign Manager the Break Composer button sat under the Remove Campaign button and could not be pressed from there. The buttons are rearranged in four rows.

### Tests
- New `test_commercial_form.py` (the form's rules and the window). The Tk stand-in gained the few window methods the form uses.

# RadioCastOS 1.79.4

## v1.79.4 — Modern flat buttons

### Changed
- **All buttons have a flat, modern look.** The old raised bevel and the dashed focus box are gone. Each button is a flat fill with a thin edge that brightens on hover, goes darker when pressed, and shows a clear ring when focused with the keyboard (amber, or dark on the amber buttons). Disabled buttons are visibly recessed instead of keeping their colour.
- The label on red (Danger) buttons is lighter so it stays readable on hover and pressed; every button label now has at least 4.5:1 contrast in every state.
- One place defines the button styles (`theme_polish._buttons`); the older copy in `app_gui.py` is removed. Spacing and fonts are unchanged, so no page layout moves.

### Tests
- New `test_button_styles.py`: flat look in every state, state order, contrast of labels and focus rings, and unchanged padding.

# RadioCastOS 1.79.3

## v1.79.3 — Library drop message lists every supported format

### Fixed
- Dropping something that is not audio onto the Library or Playlist from Windows Explorer said only "mp3, wav, flac, ogg, aac, m4a", although wma, opus, oga, aif, aiff and mp2 have been accepted since 1.79.0. The message now lists the formats the library really accepts.

### Tests
- `test_gui_alerts.py` no longer fails now and then: it waits for the test alert itself instead of assuming it is the first webhook call.

# RadioCastOS 1.79.2

## v1.79.2 — Readability and keyboard access

### Changed
- **Dimmest text is now readable.** The tertiary grey used for hints, captions, idle states and disabled labels (209 places) was only 2.8:1 against the panels, below the 4.5:1 accessibility minimum. It is now `#80848c` (4.6:1 or better on every surface) and is still clearly dimmer than the normal secondary text.
- **Tooltips stay on screen.** They are centred over the control, nudged sideways at the screen edge, and drop below the control when there is no room above (also on a second monitor). They also appear when a control is reached with the keyboard.

### Added
- **Sliders work from the keyboard** (volume, seek and the other sliders): Left/Down and Right/Up move one step, Page Up/Page Down five, Home/End jump to the ends. Ctrl+arrow still belongs to the app's seek and volume shortcuts.
- **Transport buttons (play, pause, stop, previous, next, mute) can be reached with Tab and pressed with Space or Enter.** A focused slider or button shows an amber focus ring.

### Tests
- New `test_ui_accessibility.py`: checks the contrast of every text colour against the three surfaces, and the slider and button key handling.

# RadioCastOS 1.79.1

## v1.79.1 — Local voices settings area, scrollable sidebar

### Added
- **LOCAL VOICES** section in the AI Presenter Studio (open by default, and a "Local voices" chip in the quick-jump bar). Until now Piper and Kokoro could only be set up through dialog boxes behind two small buttons in a collapsed section. Each engine now has a visible block:
  - **PC VOICE** (Windows voices): how many are installed, REFRESH VOICES, TEST PC VOICE, and WINDOWS SPEECH SETTINGS to add more.
  - **PIPER**: the program and voices folder (type, paste or BROWSE), a status line, PIPER SETUP… (download or own install), CHECK (starts it once), TEST (speaks a sample on this PC's speakers, never on air), and "If Piper fails, use the PC voice".
  - **KOKORO**: the same for the Kokoro program and model folder, with KOKORO SETUP… (download).
- The fields are written by Save AI Settings and also by CHECK, TEST and SETUP, so a test always uses what is on screen. Quotes and spaces around pasted paths are removed.
- The status lines only look at files (nothing is started until you press CHECK).

### Changed
- The sidebar page list shows a slim scrollbar on its right edge whenever some pages are out of view (wheel, drag and the Up/Down keys on a focused page button already scrolled it). It disappears when everything fits.
- PIPER SETUP and KOKORO SETUP moved from the OFFLINE VOICE section into LOCAL VOICES. Persona & Style and the queue sections moved down two rows.

### Tests
- New `test_local_voices.py` and `test_sidebar_scroll.py`; `test_ai_studio_layout.py` also checks the new fields.

# RadioCastOS 1.79.0

## v1.79.0 — Jingle pads, countdown timers, and a library that sees every audio file

### Added
- **Pads & Timers page** (Broadcast group, right after On Air; Operator and up).
- **Twelve jingle / sweeper pads.** Press a pad and its sound plays over the music; press it again to stop it. Right-click a pad (or tick EDIT PADS, for touch screens) to set its name, sound file, colour and volume. Pads follow the player volume slider, show elapsed / total time while playing, and keep their settings in `pads.json`. STOP PADS silences them all; Emergency Stop and closing the app do too. At most four pads play at once.
- **Four countdown timers** that count a length of time (`3:00`, `90`, `2m30s`) or count down to a time of day (`17:00`, `5pm`). They go amber in the last 10 seconds and keep counting up in red overtime (+0:07) at zero. Click the time, or press START / PAUSE / RESUME; RESET and +1:00 are beside it. Presets are saved in `timers.json`. When a timer reaches zero the dock says so on any page.
- **TRACK LEFT** and **TOP OF HOUR** read-outs on the same page.
- **Library: Add Files.** Pick individual songs instead of a whole folder.

### Changed
- The library now accepts `.wma`, `.opus`, `.oga`, `.aif`, `.aiff` and `.mp2` as well as mp3, wav, flac, ogg, aac and m4a, everywhere it takes files: Add Files, Add Folder, drag and drop and M3U import.
- Ctrl+3 and above each move down one page, because Pads & Timers is the third page. `pads.json` and `timers.json` are included in station packages.

### Notes
- Pad sound and timers never play a sound of their own through the PC output except the pad file you chose: the timer alert is visual only, because anything the PC plays also goes to the stream.
- Pads do not fade the music. RadioCastOS can only fade the music by changing its capture device's volume, and a jingle on the same device would be faded with it.
- The TEST button in the pad editor asks first when you are on air.

### Tests
- New: `test_jingle_pads.py`, `test_countdown_timers.py`, `test_library_formats.py`. `test_roles.py` expects the new page.

# RadioCastOS 1.78.34

## v1.78.34 — Pre-launch polish

### Fixed
- A library.json track entry with no title was silently dropped on load. It now keeps its file name as the title.

### Tests
- `scripts/selftest.py` now checks that a library.json with an unknown field loads (forward compatible) and that truly broken JSON is backed up as unreadable.

### Packaging
- `test_results/` is no longer shipped (and is git-ignored).
- Windows test checklist extended to 1.78.x (JINGLE NEXT, BREAK NEXT, Vault, Station Health, loudness, dual mount).
- `docs/RadioCastOS-Quick-Start-and-User-Guide.pdf` rewritten for 1.78.34 (was 1.53.2): roles, the 17-page menu, every On Air button (MIC, MUSIC, TALK, CALLER, BREAK NEXT, JINGLE NEXT, STATION ID), the program clock, backup stream, one-graph encode and limiter, loudness, Station Health and the Emergency Media Vault, Piper and Kokoro voices, current shortcuts and troubleshooting.

# RadioCastOS 1.78.33

## v1.78.33 — JINGLE NEXT, NOW card fix, tests

### Added
- **JINGLE NEXT** button beside BREAK NEXT (BREAKS & JINGLES row, every role). It arms one jingle from the program's jingle pool (its sweeper pool if it has no jingles) for the next AutoDJ pick; press again (JINGLE ARMED) to cancel. A jingle and a break cannot both be armed: the other button greys out with the reason.
- `AutomationEngine.request_imaging()`, `cancel_imaging()`, `imaging_pending()`, `imaging_available()`.

### Fixed
- The NOW card of the program clock showed the next queued item when the queue had no current item. It now shows the track the player is on, or Standby.
- NEXT / FOLLOWING fall back to the player's playlist when the broadcast queue is empty (this lived in the removed "NEXT ON AIR" line); NEXT says "Chosen by AutoDJ" when AutoDJ is on and nothing is queued.

### Removed
- The unused `_cc_paint_up_next` (its label was removed in 1.78.30).

### Tests
- `test_listeners_and_deadair.py` knew nothing of the default master limiter; it now checks both the plain and the limited graph.
- `test_ai_queue`, `test_autosave`, `test_console_refresh` and `test_player_track` fall back to the `_tkstub` stand-in when tkinter is missing, so the whole suite runs headless (117 scripts pass).
- `test_operator_console_domain_queue.py` now tests the real program-clock painter.

# RadioCastOS 1.78.32

## v1.78.32 — BREAK NEXT on the On Air desk, startup fix

### Added
- **BREAK NEXT** button on the On Air desk (new BREAKS row, every role). It arms a commercial break for the next AutoDJ pick: the break plays after the track that is playing now, with the clock's number of spots. It uses the same campaign pacing, daily / hourly limits, anti-repeat rules and as-run logging as a clock break. Press again (BREAK ARMED) to cancel.
- The button is greyed with a reason when AutoDJ is off or no campaign / commercial pool can play right now.
- `AutomationEngine.request_break()`, `cancel_break()`, `break_pending()`, `break_available()`.

### Removed
- The READY / ON AIR label in the rundown panel. The status strip already shows it.

### Fixed
- **The app did not start.** `app_gui.py` had a function above its module docstring and `gui_automation.py` had an import above its docstring, so the `from __future__ import annotations` line that follows was a SyntaxError. Both are moved below it.

### Tests
- New `scripts/test_manual_break.py`; BREAK tile cases in `test_console_logic.py` and `test_console_widgets.py`.
- `test_operator_presenter_polish.py` stand-in updated for the 1.78.30 program clock (`_cc_cfg`, `_cc_transport`).

# RadioCastOS 1.78.31

## v1.78.31 — LUFS column & drift label

### Added
- Library table has a LUFS column. Measured carts show the integrated level; hot carts append HOT.
- While live, the header stats line shows LOW or DRIFT (in red) when bitrate is under half target or the encoder clock has stalled / drifted from the playhead.

### Tests
- Existing loudness field tests still apply.

# RadioCastOS 1.78.30

## v1.78.30 — Loudness keep & clear drift

### Fixed
- Refreshing library tags no longer wipes `lufs` and `loudness_note`.
- Stop stream clears encoder drift and low-bitrate flags so the On Air line does not stay red off air.

### Tests
- `scripts/test_library_loudness_fields.py` covers tag refresh.

# RadioCastOS 1.78.29

## v1.78.29 — Loudness persistence

### Fixed
- `Track` now has `lufs` and `loudness_note` fields, so measured loudness is written to `library.json` and reloaded. Earlier cuts measured carts but `asdict` dropped the values on save.

### Tests
- `scripts/test_library_loudness_fields.py`

# RadioCastOS 1.78.28

## v1.78.28 — Path match and scale

### Fixed
- Closing an as-run row matches the cart path case-insensitively, so Windows path spelling cannot leave a spot open forever.
- Loading the library ignores unknown JSON fields instead of failing the whole catalogue.
- NOW PLAYING and clock card titles use scaled wrap lengths for 100% and 150% UI scale.

### Tests
- `scripts/test_asrun_close.py` covers mixed path case.

# RadioCastOS 1.78.27

## v1.78.27 — Dual mount & library loudness

### Fixed
- A configured backup mount forces the muxer encode path so dual-mount works even when Native source is left on. Capture devices are still opened once.
- Up to ten unscanned library tracks are measured a few seconds after load; hot carts are marked. New imports were already measured in 1.78.26.
- README describes the current on-air behaviour instead of the 1.78.13 feature list.

### Tests
- Existing airchain and timing scripts; version check.

# RadioCastOS 1.78.26

## v1.78.26 — Airchain

### Fixed
- The backup mount is fed from the same ffmpeg process as the primary (tee). Capture devices are not opened twice. Native source mode still cannot dual-mount; turn native source off to enable the backup path.
- New library carts are measured for loudness at import. Hot files are marked in the track note.
- While live, a stalled encoder clock or a playhead/encoder span drift over 300 ms turns the On Air source line red.

### Tests
- `scripts/test_airchain_fixes.py`

# RadioCastOS 1.78.25

## v1.78.25 — No reconnect hole

### Fixed
- TALK and CALLER no longer kill ffmpeg. The live duck stays on the Windows fader. The encode graph still picks up the state on the next Go Live.
- A closed commercial uses encoder time at the end minus encoder time at the handoff. If that clock went backwards, the cart length is kept and marked `sent_by=cart`.
- Station Health counts the configured fallback files and reads encoder silence. It no longer always reports the vault as empty.

### Tests
- `scripts/test_live_graph.py` expects fader, not rebuild.
- `scripts/test_asrun_close.py` expects the encoder span.

# RadioCastOS 1.78.24

## v1.78.24 — Seconds sent

### Added
- When a commercial ends, or the next item overlaps it, the as-run row is closed with `sent=` seconds and `listeners=` if a count is known. The cart length stays in duration. A row already closed is left alone.

### Tests
- `scripts/test_asrun_close.py`

# RadioCastOS 1.78.23

## v1.78.23 — Live mix rebuild

### Changed
- Pressing TALK or CALLER while on air rebuilds the encode graph with the new duck and caller level. The reconnect skips the drop backoff and does not stop the desk. Off air, the state is stored for the next Go Live.

### Tests
- `scripts/test_live_graph.py`

# RadioCastOS 1.78.22

## v1.78.22 — Aired cart

### Changed
- Starting a cart writes `nowplaying.json` from that cart, with the encoder clock at the handoff. AI clips still do not become the title.
- A commercial as-run row stores `cart|enc=mm:ss` so the affidavit shows the encoder time when the spot was handed to air.

### Tests
- `scripts/test_nowplaying.py` covers the encoder stamp.

# RadioCastOS 1.78.21

## v1.78.21 — Encoder clock

### Added
- The On Air source line shows encoder time and bitrate while live (`ENC 12:04 · 128 kbps`). Under half the configured bitrate the line turns red.
- `nowplaying.json` in the station data folder is rewritten from the encoder stats: title, artist, cart, encoder clock, bitrate, on air. A site can poll that file.

### Tests
- `scripts/test_nowplaying.py`

# RadioCastOS 1.78.20

## v1.78.20 — One encode graph

### Changed
- The encode filter is one graph for every capture: mic, music and the caller line. Music ducks while TALK or CALLER is open at Go Live. A caller line that is closed is sent at zero, not omitted. A master limiter sits at about -1 dBTP after the mix.
- Go Live copies the current TALK and CALLER state into that graph. Changing them mid-stream still uses the Windows fader; the graph is rebuilt on the next Go Live.

### Tests
- `scripts/test_mixer_graph.py`

# RadioCastOS 1.78.19

## v1.78.19 — Station Health

### Changed
- The diagnostics row now has one Station Health button. It shows Emergency Stop, the primary stream, silence, the backup mount, emergency media and open incidents. Incidents, Continuity, Failover, Vault and the old detail center open from that page. None of them start playback.

### Tests
- `scripts/test_station_health.py`

# RadioCastOS 1.78.18

## v1.78.18 — Loudness and backup mount

### Added
- Cart loudness. Music targets -16 LUFS, talk -19 LUFS, true-peak -1 dBTP. Preparing an accepted asset measures it when ffmpeg is available and refuses a cart more than 3 dB hot. A missing ffmpeg does not block prepare.
- Backup encode. If Admin has a backup stream address, Go Live starts a second encoder to that host:port/mount and Stop tears it down. A backup failure is logged and does not take the primary off air.

### Tests
- `scripts/test_loudness_backup.py` for the loudnorm summary and the backup address.

# RadioCastOS 1.78.17

## v1.78.17 — Air clock and affidavit

### Changed
- The progress bar, time left and the NOW card use one remaining-time rule. Remaining time is time until the segue (duration minus overlap), not until the file ends.
- Exactly on the hour the chip shows 0:00, then counts the next hour. A loaded clock names the next post (NEWS IN 4:10). With no clock it is labelled WALL so it is not mistaken for the traffic log.
- Stopped does not paint a countdown. Paused freezes the time. Takeover uses its own position and does not invent a duration.

### Added
- Commercial as-run rows now store duration and status (clean or cut). The log window and the printable report show both. Older logs still open.

### Tests
- `scripts/test_console_timing.py` covers the post, overlap, stop, pause, takeover and clock labels.
- `scripts/test_asrun_affidavit.py` covers the new columns and a legacy file.

# RadioCastOS 1.78.16

## v1.78.16 — On Air timing

### Added
- NOW PLAYING progress bar with time played, time left (turns red in the last 15 s) and **HOUR IN mm:ss**, the countdown to the top of the hour (amber under 5 min, bright under 1 min).
- UTC time beside the date in the status strip.
- Unknown duration (live source) shows an empty bar and no countdown, never a made-up one.

### Tests
- `scripts/test_console_timing.py` for the timing maths.

# RadioCastOS 1.78.15

## v1.78.15 — Operator On Air desk polish

### Changed
- NOW PLAYING and MASTER MONITOR now split the width 50/50, so they line up with the 8-column button grid and the four clock cards below.
- Small captions (section headers, NOW/NEXT/FOLLOWING/BREAK cards, NOW PLAYING and MASTER MONITOR labels) now follow the UI scale like the rest of the desk.
- Track and card titles wrap to the width of their card instead of a fixed pixel width.
- The desk repaints a label only when its text or colour changed (it refreshes four times a second), which cuts redraws and flicker.

### Fixed
- A garbled code comment about the removed MIC tile; spacing between two methods.

### Not changed
- No button, role rule or behaviour changed. Not checked on screen: the build environment has no display, so please look at the desk on Windows at 100% and 150% scaling.

# RadioCastOS 1.78.14

## v1.78.14 — On Air desk tidy-up and STATION ID button

### Added
- **STATION ID** button on the On Air desk. It plays the station ID file chosen in Settings (the same file and player call as the Fallback / Backup window). If music is playing it asks first, because the ID replaces it. Greyed out, with the reason, when no file is set or the file is missing.

### Changed
- **LIVE TAKEOVER** is now Producer-only. It could offer to switch on a Producer-level Automation setting, which sidestepped role gating. Operators use TALK; for them STATION ID takes the freed slot.
- The emergency window button is now **FALLBACK / BACKUP** (calm colour, no siren) so it is not confused with the red **EMERGENCY STOP** tile. The window and the Settings card use the same name.

### Removed
- The "Artist — Title" line in the top status strip and the "NEXT ON AIR" line at the bottom. NOW PLAYING, the NEXT/FOLLOWING cards and the dock already show them.
- MIC, MUTE, VOL − and VOL + tiles are no longer built or repainted four times a second. TALK, MUSIC and the dock cover them; their logic and the dock controls are unchanged.
- Stray row weights that stretched the program-clock row and the AUDIO SOURCES header.

### Not changed
- No manual commercial-break / news button: there is no handler for it, and adding one would touch the scheduler and queue. Operators still wait for the clock or the AI.

### Tests
- Updated tile counts; new checks for the STATION ID tile states, role layout, the Producer gate on LIVE TAKEOVER and the confirm-before-cutting behaviour.

# RadioCastOS 1.78.13

## v1.78.13 — CALLER button for phone-in lines (WhatsApp)

### Added
- **CALLER** button on the On Air desk. It appears only when an audio source is ticked **Caller** on the Audio page (a new checkbox on each source), for example WhatsApp Desktop's call audio routed through a virtual cable. See `docs/WHATSAPP_CALL_IN.md`.
- **CALLER ON AIR**: the caller is heard, the microphone opens and the music fades down (like TALK). **CALLER OFF AIR**: the line closes, the microphone closes again if the caller opened it, and the music returns (unless TALK is on).
- The caller line is closed whenever the app starts or a source is ticked as Caller, so a call never reaches the stream before the host presses CALLER. Original levels are restored on close and after a crash, as for TALK.
- New phone icon; the AUDIO SOURCES row re-flows (TALK, MUSIC, CALLER) when a caller line exists.

### Notes
- RadioCastOS does not connect to WhatsApp. The call runs in WhatsApp Desktop; RadioCastOS only controls the audio. Needs the optional `pycaw` package, like TALK.

### Tests
- Caller on/off, microphone and music interplay, TALK overlap, start-up close, restore, and tile states.

# RadioCastOS 1.78.12

## v1.78.12 — One TALK button

### Changed
- The AUDIO SOURCES row now has just **TALK** (large) and **MUSIC**. TALK already opened the microphone, so a separate MIC button only duplicated it.
- **TALK** opens the microphone and fades the music down; **TALKING** (press again) closes the microphone and fades the music back up. Setting `talk_closes_mic` (default on) controls the closing; with it off the microphone is left as it was.
- The microphone is left as it is until the first TALK. If there is no microphone source, TALK still fades the music.

# RadioCastOS 1.78.11

## v1.78.11 — Live audio sources: MIC, MUSIC, TALK

### Added
- New **AUDIO SOURCES** row on the On Air desk:
  - **MIC LIVE / MIC MUTED** — mute or unmute the microphone on air without touching the stream.
  - **MUSIC ON / MUSIC MUTED** — fade the music out and back.
  - **TALK** — for a live presenter: the microphone goes live and the music fades down to 20% (setting `talk_duck_percent`); press **TALKING** to fade the music back up. The microphone stays live.
- Smooth fades (about 0.8 s), no stream restart. Works on the Windows capture devices FFmpeg already records (the microphone and the loopback / virtual-cable device that carries the music), the same mechanism the AI presenter uses; needs the existing optional `pycaw` package.
- If the music is not on such a device, MUSIC and TALK fall back to the player volume (the player restarts at the same spot, so there is a brief gap).
- Safety: original levels and mute flags are saved, restored when TALK ends and when the app closes, and kept in a small file so a crash cannot leave the mic muted or the music low; the next start puts them back.

### Tests
- `scripts/test_source_control.py` (fakes for the Windows endpoints): mute, fades, TALK, fallback, close, crash recovery, shared endpoints, cancelled fades. Console logic and widget tests extended.

# RadioCastOS 1.78.10

## v1.78.10 — Collapsible page list

### Changed
- The page list on the left can now be folded to a thin rail with the ☰ MENU button (or Ctrl+B), giving the work area the full width. It starts folded; the choice is remembered. Ctrl+1…9 and Ctrl+PgUp/PgDn still switch pages while it is folded. Ctrl+B is ignored while typing in a text box.

# RadioCastOS 1.78.9

## v1.78.9 — Cleaner On Air desk

### Changed
- The On Air (Operator Control Console) desk no longer shows the MUTE, VOLUME − and VOLUME + tiles. Volume and mute stay one click away in the always-visible bottom dock (slider, mute button, Ctrl+↑/↓).
- PREV, PLAY, STOP and NEXT are now four large tiles across the transport row.
- Removed the text-only TRANSPORT card from the top. Takeover is still shown by the TAKEOVER label on NOW PLAYING and the output label on the master monitor.

### Tests
- Console widget test updated: 13 tiles on the desk, none of them volume/mute.

# RadioCastOS 1.78.8

## v1.78.8 — Kokoro offline presenter voice

### Added
- **Kokoro** as a second offline neural presenter voice, beside Piper and the Windows voices. Voices appear in the AI Presenter Studio Voice box as `Kokoro: <speaker>` (for example `Kokoro: af_bella`, `Kokoro: bm_george`) once the offline engine is selected.
- **KOKORO SETUP…** button (OFFLINE VOICE section). DOWNLOAD fetches the official sherpa-onnx Windows program and the Kokoro English model into your own AppData folder (about 400 MB, one time). Or point it at your own `sherpa-onnx-offline-tts.exe` and Kokoro model folder. A newer multi-language Kokoro model folder is also recognised (English speakers offered).
- Same safety net as Piper: if Kokoro is missing or fails during a break, the break is spoken with the default Windows voice and a note goes to the automation log (switchable). TEST VOICE never falls back, so it shows the real error.
- Start-up check and the "presenter unavailable" hint understand Kokoro voices.
- `src/kokoro_voice.py`; new settings `kokoro_exe`, `kokoro_model_dir`, `kokoro_fallback_windows`.

### Notes
- Nothing is bundled or linked: Kokoro and sherpa-onnx run as a separate program on your PC. See THIRD-PARTY-NOTICES.txt.
- Long scripts are spoken in sentence-sized pieces and joined. Accented letters and curly quotes are simplified to plain ASCII before speaking, because Windows passes program arguments in the ANSI code page.
- The Speed slider is passed to Kokoro when it is not 1.0; a sherpa-onnx build that does not accept it is retried at normal speed.

### Tests
- `scripts/test_kokoro_voice.py` (voices, readiness, text handling, command building, speed retry, chunk joining, download and archive safety) and `scripts/test_kokoro_presenter.py` (routing, availability, Windows fallback, start-up check). No Kokoro, ffmpeg or network needed.

# RadioCastOS 1.78.7

## v1.78.7 — Launch readiness: Vault depth, backup stream, fallback chip

### Added
- Emergency Media Vault now decodes the first 30 seconds of every file and flags audio that cannot be decoded (INVALID) or is silent from the start (WARNING). Results are cached per file, so repeat refreshes are cheap and only changed files are re-checked.
- Backup stream setting (Settings > Operator & Reliability). Failover Readiness checks that a valid address is configured instead of always showing WATCH. Advisory only: nothing connects to it.
- Header "FALLBACK" chip (OK / CHECK / NO FALLBACK) fed by the Vault in the background; one toast per session when fallback audio needs attention. Clicking it opens the Vault.
- Windows launch checklist for the 1.78 series in `docs/WINDOWS_TEST_CHECKLIST.md`.

### Tests
- Real-audio tests (tone, silence, corrupt file, cache), backup stream validation and chip behaviour.

# RadioCastOS 1.78.6

## v1.78.6 — Operator & Presenter UI polish

### AI Presenter Command Center
- The script box is rewritten only when the script changes, so scrolling and text selection are no longer reset twice a second; long scripts now have a scrollbar.
- Remaining time shows "of total" and turns red in the last 10 seconds.
- Prepare Break and Take Presenter On Air are greyed out when the app would refuse them anyway (preparing / already on air).
- Autopilot status no longer hides the Emergency Stop reminder.
- Wrapped text follows the window width; refresh failures are logged once instead of being swallowed, and the refresh loop stops when the app closes.
- AUTO PROGRAM refreshes the page even if the action fails.

### Operator Control Console
- Program clock NOW card shows time left on the current item.
- BREAK card shows the next break anywhere in the queue, not only when it is exactly fourth.
- Program clock detail text is slightly larger for readability.

# RadioCastOS 1.78.5

## v1.78.5 — Emergency Media Vault & Health Center fixes

### Fixes
- Emergency Media Vault and Failover Readiness now verify the audio the station has actually configured (Settings emergency media folder, station ID file, Autopilot fallback audio). Previously a lookup on the wrong object always fell back to a default folder.
- Station Health Center now reads the real application settings and stream state (it was passed the window's `config` method, so preflight/storage checks reported false results).
- Failover Readiness now finds the real configuration backups instead of always reporting none.
- Vault duration check no longer needs ffprobe on PATH: it uses a bundled ffprobe when present and falls back to `ffmpeg -i`.
- Vault and Health Center scans run off the UI thread, so the window no longer freezes while files are probed.
- Manual Refresh no longer stacks extra auto-refresh timers in the Health, Incident, Continuity, Failover and Vault windows; closed windows are never touched.
- Presenter audio concat no longer flashes a console window on Windows.

### Added
- Emergency Media Vault "Choose folder…" button (saved as `admin.emergency_media_path`).

### Build / docs
- `build.spec` lists every application module and bundles `ffprobe.exe` when staged in `assets/`; `local-build.bat` stages it automatically.
- Added the missing RELEASE-1.78.3.md and RELEASE-1.78.5.md.

# RadioCastOS 1.78.4

### Fixes and polish
- Fixed a NameError on the Presenter Command page (missing `FONT_MONO_LG` import).
- Removed a duplicated `_ai_autopilot_auto_run_changed` handler.
- Replaced bare `except:` clauses in the metadata editor with explicit exceptions.
- Version-pinned tests now assert a minimum version instead of an exact one.
- Three headless tests now set up `sys.path` so they run standalone.
- Emergency Media Vault: header-only WAV files are now flagged invalid, files are opened to confirm readability, and ffprobe no longer flashes a console window on Windows.
- README refreshed for the 1.78 series.

## v1.78.4 — Premium Emergency Media Vault
- Added advisory emergency/fallback media verification and verified playlist view.
- Added file readability, supported-format, size and duration checks with ffprobe support when available.
- Added Emergency Media Vault to Diagnostics.
- Preserved strict separation from deterministic playout, scheduler, stream switching and Emergency Stop.

# RadioCastOS 1.78.3

## v1.78.3 — Broadcast Failover Readiness & Backup Media Manager

- Added deterministic, advisory failover readiness checks.
- Added verified fallback-audio, configuration-backup, last-known-good, and backup-stream readiness indicators.
- Added controlled operator recovery checklist UI.
- Preserved deterministic playout, scheduler, and Emergency Stop authority.


## v1.78.2 — Broadcast Recovery & Continuity Center

- Added advisory continuity readiness and prioritized recovery recommendations.
- Added Emergency Stop awareness without bypass behavior.
- Preserved deterministic scheduler/playout authority.


# Changelog

## 1.78.1 — Broadcast Incident & Alert Center
- Added executive Incident & Alert Center.
- Added persistent operator acknowledgement and recovery visibility.
- Preserved existing AlertEngine lifecycle and playout authority.

1.78.0 — Broadcast Reliability & Station Health Center

- Added read-only Station Health Center aggregation.
- Added engineering health tiles for streaming, audio, automation, media runtime, storage, broadcast queue, media library and configuration backup.
- Preserved deterministic scheduler/playout authority and Emergency Stop behavior.

# RadioCastOS 1.77.9

## v1.77.9 — Premium Executive Broadcast Operations
- Added read-only Executive Broadcast Operations command center.
- Unified On Air, next item, traffic risk, commercial delivery, make-good exposure and AI Presenter readiness.
- Added prioritized commercial actions using existing Traffic Intelligence.
- Preserved deterministic scheduler and playout authority.

# RadioCastOS 1.77.8 — Commercial Revenue & Delivery Dashboard

- Added advisory commercial revenue/delivery portfolio metrics.
- Added booked spot and optional rate-per-spot campaign metadata.
- Added executive delivery dashboard with exposure visibility.
- Preserved deterministic scheduler and playout authority.

# RadioCastOS 1.77.5

## v1.77.5 — Premium Commercial Break Composer

- Added producer-facing Commercial Break Composer.
- Added break capacity, booked seconds, remaining inventory and fit/over-capacity status.
- Added visual insert sequencing with move/remove controls.
- Added commercial, sponsor, station ID, jingle, sweeper, promo and AI Presenter insert types.
- Composer is advisory only and does not control playout or scheduler authority.

# RadioCastOS 1.77.4

## v1.77.4 — Premium Commercial Break Planner

- Added a visual Commercial Break Planner to Traffic & Automation.
- Shows hourly commercial-break capacity, booked seconds, open inventory, and alert states.
- Surfaces make-good pressure and eligible campaign inventory before spots reach air.
- Keeps the planner advisory-only; scheduler and playout remain authoritative.
- Added producer-friendly refresh and break detail views.

# RadioCastOS 1.77.1

## v1.77.1 — Premium AI Presenter Command Center

- Added a dedicated Presenter Command Center for producer/operator workflows.
- Added a large broadcast clock with ON AIR / OFF AIR state, current item, next item, progress and remaining time.
- Added a focused presenter-break workspace with approved script visibility and live readiness state.
- Added direct routing to the existing Prepare, Load, Take On Air and Auto Program actions.
- Added presenter engine readiness and broadcast-safety status without changing playout ownership.
- Added role-aware navigation and regression coverage for the new page.
- Preserved the existing deterministic playout, emergency-stop and AI takeover safety boundaries.

# RadioCastOS 1.77.0

## v1.77.0 — AI Presenter Autopilot

- Added one-button full-show preparation with persistent show state and manifests.
- Added requested defaults: full mode, authorized clone voice, verified news, station announcements, and music introductions/transitions.
- Added HTTPS/attribution/domain validation for retrieved news before it can enter a show.
- Added explicit clone-consent gating.
- Added supervised running and explicit automatic-running opt-in.
- Added last-known-good show-asset recovery for automatic runs.
- Added approved presenter-asset playout interfaces without queue mutation authority.

### Scope boundary
- 1.77 runs a prepared continuous presenter audio asset. It does not autonomously choose, reorder, insert, skip, or remove individual music tracks. Those remain under deterministic AutoDJ/scheduler control.
- Voice cloning is available only when an authorized clone profile and configured clone runtime are present.

# RadioCastOS 1.76.0

## v1.76.0 — Audio Asset & Operator Workflow

- Added persistent TTS audio asset registration with SHA-256 identity.
- Added operator accept/reject and regeneration-required workflow.
- Added script/revision/job/asset correlation and review audit metadata.
- Added explicit `Prepare for Broadcast` handoff artifacts.
- Preserved strict separation from deterministic broadcast playout.

### Safety

- `Prepare for Broadcast` creates a handoff record only; it does not insert or play audio.
- The workflow has no Broadcast Engine, Broadcast Queue, or Playout Engine dependency.

# RadioCastOS 1.75.0

## v1.75.0 — Voice/TTS Runtime

- Added approval-gated TTS runtime for Presenter Assist scripts.
- Added provider abstraction with adapters for Windows SAPI and Piper.
- Added voice profile controls for provider, voice, locale, speed, pitch, style and pronunciation substitutions.
- Added generation lifecycle, script/revision correlation and durable job records.
- Added content-addressed caching for repeat generation with identical script/voice/provider configuration.
- Added audio QA for file validity, duration, channels, silence and clipping checks.
- Added generated-audio preview/asset metadata without any playout authority.

### Safety

- TTS accepts only explicitly operator-approved PresenterScript artifacts.
- TTS creates and validates audio assets but never starts, stops, selects, skips, reorders, inserts or removes broadcast items.
- Broadcast Engine and Broadcast Queue remain completely outside the TTS runtime.
- A successful TTS job is an independent audio asset; broadcast insertion remains an explicit deterministic workflow decision.

# RadioCastOS 1.74.0

## v1.74.0 — Copilot Voice & Presenter Assist

- Added previewable presenter scripts with configurable target length and style.
- Added deterministic read-time estimation and script trimming.
- Added preview/edit/approve workflow with explicit operator approval state.
- Added contextual intro, outro, transition, news-link, and handoff script generation.
- Added voice-readiness metadata without coupling to audio playback or playout authority.

### Safety

- Generated scripts are advisory artifacts until explicitly approved by the operator.
- Voice/presenter assistance never starts, stops, selects, skips, or mutates deterministic playout.
- Audio synthesis is intentionally decoupled from the broadcast engine.


## v1.73.0 — Copilot Intelligence Engine

- Added contextual segment classification for music, news, talk, breaks, imaging, and open states.
- Added deterministic presenter handoff suggestions with standby, soon, imminent, and now timing states.
- Added prioritized breaking/developing-news advisories with urgency classification.
- Added contextual talking-point refresh using current/next queue context, show, station, and prioritized news.
- Added confidence and intelligence-status indicators to the operator copilot surface.

### Safety

- Copilot Intelligence consumes immutable queue snapshots only.
- It never selects, inserts, removes, reorders, skips, or mutates authoritative playout state.
- Contextual analysis is advisory and can fail or be disabled without interrupting deterministic playout.

# RadioCastOS 1.72.0

## v1.72.0 — Copilot Operator UI

- Added a dedicated Live Show Copilot operator workspace.
- Added live current/next display, remaining-time and presenter-cue countdowns.
- Added advisory transition-cue list with individual and bulk acknowledgement.
- Added live talking-point and breaking/developing-news panels.
- Added operator-editable show context and headline input for advisory refresh.
- Added queue-revision and advisory-status visibility.

### Safety

- The operator UI exposes no queue insert, remove, reorder, skip, or playout-authority action through the copilot.
- Acknowledgement changes only advisory copilot state.
- Copilot updates remain asynchronous and cannot block deterministic playout.

# RadioCastOS 1.71.0

## v1.71.0 — Live Show Copilot

- Added real-time current/next awareness from authoritative queue snapshots.
- Added presenter cue timing based on observed current-item duration.
- Added periodic live talking-point refresh and optional presenter intelligence.
- Added breaking-news advisory detection from supplied headlines.
- Added transition cues with deterministic due timing.
- Added operator acknowledgement state for copilot cues.
- Added stale-refresh protection using queue revision correlation.

### Safety

- Live Show Copilot never selects, inserts, removes, reorders, or mutates queue items.
- Copilot work is asynchronous and advisory only; deterministic playout never waits for AI.
- AI/provider failure falls back to deterministic cues.
- Operator acknowledgement changes only copilot advisory state.

# RadioCastOS 1.77.7

## v1.77.7 — Premium Commercial Traffic Intelligence
- Added deterministic campaign delivery-risk scoring with transparent reasons.
- Added LOW / WATCH / HIGH / CRITICAL traffic risk levels.
- Added prioritized “FIX THESE 3 THINGS” producer guidance.
- Added Traffic Intelligence to Commercial Campaign Manager.
- Preserved advisory-only separation from deterministic scheduler and playout.

# RadioCastOS 1.70.0

## v1.70.0 — Show Intelligence

- Added operator-ready Show Intelligence boards from immutable queue snapshots.
- Added upcoming clock awareness, presenter/news briefs, music context, talking points, segment preparation, and social previews.
- Added independent per-element AI/fallback status and queue revision correlation.
- Added advisory show-board event publication without queue or playout mutation.


## v1.69.0 — Intelligence Orchestration

- Added show-level advisory intelligence orchestration.
- Added shared context and dependency ordering across intelligence capabilities.
- Added consolidated advisory packages and cancellation.
- Added strict safe continuation/fallback behavior.

## v1.68.0 — Intelligence Runtime

- Added asynchronous live Intelligence Runtime bridge to the BroadcastEvent bus.
- Added strict intelligence deadlines with deterministic fallback.
- Added per-capability runtime health, latency, timeout and fallback metrics.
- Added intelligence state and health broadcast-domain events.
- Added runtime notifications and request/runtime correlation IDs.
- Intelligence work never blocks deterministic playout or reliability recovery.

## 1.76.0 — Audio Asset & Operator Workflow
- Added persistent TTS audio asset records with SHA-256 identity.
- Added explicit operator accept/reject and regeneration workflow.
- Added script/revision/job/asset correlation and review audit metadata.
- Added controlled `Prepare for Broadcast` handoff artifact.
- Preserved strict separation from deterministic broadcast playout.
