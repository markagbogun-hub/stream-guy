# Windows test checklist (1.32 onwards, now including 1.78.x)

The automated tests cannot open the real window. Run through this once on Windows
before going on air with a new build (about 10 minutes, no stream needed).

## Phone status page (1.90.7)
- [ ] Settings > Remote Management: with remote monitoring on, a tick *Also serve a read-only status page for phone browsers* sits above Apply. The page below it (Apply, status line, address) still looks right.
- [ ] Tick it, choose *Local network*, press Apply. On a phone on the same Wi-Fi, open `http://<station PC address>:<port>`: the token box appears. Paste the token and press Connect.
- [ ] While streaming: ON AIR in green, now playing, time on air and bitrate match the desk. Stop the stream: OFF AIR (grey) within ~10 s.
- [ ] Raise an alert (for example stop the audio input): the page shows it in amber or red.
- [ ] Wrong token: the page says it was not accepted. Five wrong tries: LOCKED OUT, and the Fleet Console on another PC is also locked out for about a minute.
- [ ] Untick the page option and Apply: the same address now shows nothing (no page). Fleet Console still works.
- [ ] *Remember on this phone* keeps you signed in after closing the browser; *Forget token* signs you out. Turn the phone sideways: the layout still fits.
- [ ] Windows Firewall: a phone cannot connect until Windows allows RadioCastOS on the private network.

## As-Run copy (1.90.6)
- [ ] Analytics > Open As-Run Report: the window has **Copy selected** and **Copy all** next to Export CSV.
- [ ] Click two or three plays, press **Copy selected** (or Ctrl+C), paste into Excel: only those plays appear, one per row, with a header line.
- [ ] **Copy all** pastes every play in the chosen dates and campaign. The line under the table says how many were copied.
- [ ] Ctrl+A in the table selects every play. With nothing selected, Copy selected says so instead of copying nothing.

## AI Show Builder (1.32 / 1.33)
- [ ] NEW SHOW, then add clips: the same show stays selected after each edit.
- [ ] BUILD FROM AUTODJ on a show that already has items asks before replacing.
- [ ] Rundown lines show start time and length; a deleted audio file shows [AUDIO MISSING].
- [ ] RENAME, DUPLICATE and EXPORT work; the exported .txt opens and lists the scripts.
- [ ] SEND TO QUEUE reports skipped items when audio is missing.

## Playlist drag and drop (1.34)
- [ ] Drag 3 library tracks (Ctrl-click) onto the playlist: amber line shows, tracks land there.
- [ ] Drag playlist rows up/down: order changes, selection stays on the moved rows.
- [ ] Drag playlist rows onto the library table: label says Remove, rows are removed.
- [ ] Press Esc mid-drag: nothing changes. Drag near the edge: the list scrolls.
- [ ] While a track is playing, reorder around it: playback is not interrupted.
- [ ] Click one row of a multi-selection without dragging: selection collapses to that row.
- [ ] Explorer: drop an mp3 and a folder on the playlist and on the library (needs tkinterdnd2).
      If nothing happens, check the log for "Explorer file drop disabled".

## No duplicates (1.35)
- [ ] Add the same track twice by any method: second add is skipped, status says so.
- [ ] Two copies of one song (same artist and title) in different folders: only one gets in.
- [ ] REMOVE DUPLICATES on a playlist with repeats asks, removes, keeps the first copy.
- [ ] Play Now on a track already in the playlist plays that copy.

## Undo / redo (1.36)
- [ ] Shuffle, then Ctrl+Z: the old order returns; Ctrl+Y shuffles back to the same order.
- [ ] Clear the playlist, press the ↶ button: all tracks return.
- [ ] Undo after a drag-and-drop move while a track plays: playback continues, list order reverts.
- [ ] Ctrl+Z works with focus on either table.

## Build
- [ ] local-build.bat (or the GitHub workflow) finishes; installer runs; app starts.

## 1.50 — Station Operations / Remote Management (needs a real Windows check)

The automated tests ran against a stand-in for the window toolkit, so none of the 1.50 pages or Settings cards has been seen on screen yet.

- [ ] **Station Dashboard** page opens; the status strip, Attention panel, tiles and the stations list are readable and nothing overlaps or clips at 100 %, 125 % and 150 % Windows scaling, and when the window is made narrow.
- [ ] The status lamp pulses gently while on air; the strip button turns red and says Stop.
- [ ] Fleet Console rows: a warning row is tinted amber, a fault row red, an idle row dimmed; the selected row is still clearly readable; the empty-state card is centred over the table.
- [ ] Fleet Console buttons grey out sensibly (nothing selected / station off air / station unreachable); right-click menu, Delete and F5 work.
- [ ] Settings cards (Remote Management, Alerts): the dividers, notes and monospace token look right; **Copy address** copies the station URL; status text is green / amber / red.
- [ ] Go Live from the dashboard: the line turns green, time on air counts up, bitrate appears. Stop: it returns to OFF AIR.
- [ ] **Settings → Remote Management**: the card fits; Show / Copy / New token… work; Apply with *This PC only* starts the agent (status line says Listening).
- [ ] From the same PC: `curl -H "Authorization: Bearer <token>" http://127.0.0.1:8765/api/v1/status` returns the station; without the token it returns 401.
- [ ] Choose *Local network*, Apply: Windows Firewall may prompt — allow it. From a second PC, open the same URL with the PC's LAN address.
- [ ] Port already in use (start another program on it): Apply shows a plain message and does not leave the setting switched on.
- [ ] **Remote Go Live / Stop** (tick the box; confirm the warning): from the second PC `POST …/control/stream/stop` while on air is refused without `{"confirm": true}`, works with it; the app log shows `[remote] stop requested`; `GET …/audit` lists it.
- [ ] With the control box off, the same POST returns 403.
- [ ] **Alerts**: with a bad stream address, the dashboard shows an amber/red alert after ~10 s and a toast; Acknowledge Alerts greys it; fix the address and it clears after ~15 s. Webhook: "Send test alert" reaches your test URL.
- [ ] **Fleet Console**: add the second PC (name, `http://<ip>:8765`, token). The row goes green within seconds; Go Live / Stop / Acknowledge Alerts work; unplug its network and the row shows OFFLINE after two missed polls.
- [ ] Close and reopen RadioCastOS: remote settings, alert settings, the fleet list and tokens are all still there; the agent restarts only if it was switched on.
- [ ] Export a deployment package and import it on another PC: the remote agent, fleet list and webhook are **not** switched on there.

## 1.55.0 — Pre-produce breaks, reserve clips (needs a real Windows check)

The automated tests used a fake presenter and a stand-in for the window toolkit, so the window has not been seen and no real voice has been used.

- [ ] **Window:** AI Presenter Studio, production queue: the **PRE-PRODUCE…** button sits under REMOVE without overlap. The window opens, the three number boxes accept values, SAVE closes it and the values are kept after closing and reopening RadioCastOS.
- [ ] **MAKE CLIPS NOW** with a working voice and writer: the Automation log shows the run starting and finishing; the queue lists timed clips at your clock minutes (no news slots) plus the reserve; each plays and sounds right. A Music Link made ahead names no song.
- [ ] **Air by itself:** with AutoDJ and Presenter takeover on, a clip scheduled a few minutes ahead goes on air on the minute and AutoDJ resumes after it. The live clock does not write a second break for that slot.
- [ ] **Run twice:** MAKE CLIPS NOW again straight away adds nothing for covered slots (the log says so).
- [ ] **Live first:** start a run, then let a clock slot come due; the run waits and the live break is not delayed. STOP ends the run and keeps the clips made.
- [ ] **Reserve:** switch off the internet (or break the AI key) shortly before a clock slot: the log says the slot could not be prepared live and a reserve clip airs instead. Reconnect and run again: the reserve is topped up.
- [ ] **Overnight:** tick *Run by itself every day*, set the hour to the next hour, leave RadioCastOS open: the run starts at that hour, once. Close RadioCastOS for a few hours, then reopen: missed clips show SKIPPED and nothing airs in a burst.

## 1.54.0 — Backup news, AI status line, stream presets (needs a real Windows check)

The automated tests used fake feeds and a stand-in for the window toolkit, so none of this has been seen on screen.

- [ ] **Provider preset:** Connection page, pick *Icecast (standard)*: server type, username and mount fill in; host, port and password are untouched. Pick *Shoutcast v2 (standard)* and the username and mount clear. The tab looks right (no overlap).
- [ ] **AI Presenter Studio layout:** open it; the News section shows *Backup news feed URLs* between the main feeds and *Allowed news sites*. Section headings still expand and collapse, and the top chips (Voice, Brain, Schedule, News, Script AI, Offline, Persona, Queue) and the missing-key badge jump to the right section.
- [ ] **Backup feeds:** set the main feed to a broken address (e.g. `https://news.invalid/rss`), keep the default backups, prepare a News Bulletin: it succeeds and the Automation log says the main feed failed and the backup is being tried. With an allowed-sites list that excludes the backup outlets, the bulletin fails with a clear message instead.
- [ ] **AI status line:** On Air page, under the stream status. Press GENERATE FULL PROGRAM: it shows fetching news, writing, voicing, then ready. Break the AI key or go offline: a problem shows in amber. It clears itself after about 90 seconds.
- [ ] Settings still save: close and reopen, backup feeds are kept.

## 1.53.1 — Opus and FLAC (needs a real Windows check)

- [ ] **Opus to Icecast2:** set *Codec* to opus, Go Live. The log notes the 48 kHz resample, the stream goes LIVE, and a player (VLC, a browser) plays it.
- [ ] **FLAC to Icecast2:** same with flac; the bitrate readout is several hundred kbps (that is normal).
- [ ] **Shoutcast guard:** with a Shoutcast server and Opus or FLAC chosen, Go Live stops at once with the "Icecast2 only" message and nothing is sent.
- [ ] **Record as FLAC and as Opus**, with and without *New file every N minutes*: the files open in a player.

## 1.53 — Encoder connection, listener count, dead air, split recording (needs a real Windows check)

The automated tests ran against fake servers and a stand-in for the window toolkit, so the new controls have not been seen on screen and no live Icecast or Shoutcast host has been tried.

- [ ] **Blank mount:** clear *Mount point*, Go Live to your host. The log shows `PUT /` (or the `/stream` retry, or `SOURCE`) and the stream goes LIVE; the log says which mount worked.
- [ ] **Slash only:** type `/` as the mount; same result. A mount typed without a slash (`live`) connects as `/live`.
- [ ] **Wrong password:** the log shows one 401 line and a plain hint; it does not retry other mounts.
- [ ] **Shoutcast v1 / v2 host:** connects, and changing the track updates the title on the server's page (v1 title updates are new). A title with accents shows correctly on Icecast.
- [ ] **Keep reconnecting** (Connection page): tick it, unplug the network for a minute, plug it back; the stream returns by itself. Untick: behaviour is as before.
- [ ] **Listener count:** with someone listening, the readout beside the bitrate shows e.g. `· 1 listener` within ~30 s; it disappears when you stop. Check Icecast and Shoutcast hosts if you have both.
- [ ] **Dead air:** set the alert to 10 s, mute the mixer; after ~10 s the log says `[dead air]` and the Dashboard / alerts show a Dead air fault; unmute and it clears.
- [ ] **Capture buffer:** set 200, Go Live and Record with the same device: audio is clean and the log shows no dshow error. Set it back to 0 if the device rejects it.
- [ ] **Split recording:** set 1 minute (use 0 afterwards), record for 3 minutes: three files with their own time stamps, no gap at the joins, each plays from 0:00.
- [ ] **Hide log** (Show log / Hide log, Ctrl+L): the page grows back to the bottom with no empty band, on Traffic & Automation and on Settings.
- [ ] **radiocastctl:** with Remote Management on, `python scripts\radiocastctl.py status` prints one line; `stop` while on air is refused without `--confirm`.

## 1.57.0 - Operator Mode (needs a real Windows check)

- [ ] Fresh config: app looks exactly like 1.56 (Technician, 14 pages, badge says TECHNICIAN).
- [ ] Settings -> Roles & Operator Lock: set a PIN, set Start in = Operator, close and reopen. App opens on On Air with 3 pages; badge shows OPERATOR with a lock.
- [ ] Click the badge: Producer needs the PIN; wrong PIN is refused; right PIN works; going down needs no PIN.
- [ ] Operator: Ctrl+4 and the Settings page do nothing; Library shows only search/add/refresh/move/shuffle/save/load; the sidebar shows only On Air, Now Playing and Music. As Producer the pages are named Music / Programs / AI Presenter.
- [ ] Credential Manager has an entry "RadioCastOS/RolePin"; config.json has no PIN hash.
- [ ] On Air desk: "Next:" shows the next two playlist tracks; AutoDJ on with an empty playlist shows "chosen by AutoDJ".
- [ ] Emergency / Backup: without sources the two source buttons are greyed with a reason; after setting them in Settings, backup playlist starts from track 1 and station ID plays; Stop all audio silences everything.
- [ ] On Air desk shows STREAM CONNECTED while live. Stop the server (or unplug the network): it changes to RECONNECTING / STREAM DISCONNECTED and a Reconnect button appears; as Operator no log panel or red banner opens. Restore the server and press Reconnect: it returns to STREAM CONNECTED. Also try with a Shoutcast v1 profile.
- [ ] AI row on the On Air desk: Operator sees AUTO PROGRAM, RETURN TO AUTODJ, EMERGENCY STOP only (no gap); Producer/Technician see all five. The AI Presenter line reads READY / ARMED / ON AIR as you start and cancel an AUTO PROGRAM; without a key it says to ask the technician. AI clock breaks (auto clock) still fire while signed in as Operator.
- [ ] Operator header: no "Show log" and no "Save settings" (Ctrl+L does nothing); Player toggle still works; header shows listeners only, no kbps. Stop the server: the header and the On Air strip say STREAM DISCONNECTED / "Press Reconnect" with no host, port or error text. Click the AUDIO and AI chips: a notice says to ask the technician. The On Air desk has no "Scheduler & Commercials" line.
- [ ] Producer header: Show log and Save settings are there; the status is still plain words. Technician: raw status message and everything as in 1.56.
- [ ] Remove the PIN: station returns to Technician start.

## 1.56.0 - Piper presenter voice (needs a real Windows check)

The automated tests use a stand-in for Piper and for the window, so none of this has run against a real Piper install.

- [ ] PIPER SETUP... > Yes (download): Piper and a voice download to %APPDATA%\RadioCastOS\piper, a "Piper ready" message appears, the voice shows as "Piper: en_US-lessac-medium"; TEST VOICE plays it. Offline PC: a clear "could not be downloaded" message.
- [ ] PIPER SETUP... > No (own install): pick your piper.exe and models folder, answer the Windows-voice fallback question (Yes/No is remembered); the check says ready, and the models appear as "Piper: <model>" in the Voice box (engine Offline).
- [ ] TEST VOICE with a Piper voice plays in that voice. Rename piper.exe, TEST again: it fails with a clear message (no Windows voice).
- [ ] Prepare an AI break with a Piper voice: the clip airs in the Piper voice.
- [ ] With piper.exe renamed, prepare a break: it airs in the default Windows voice and the Automation log has a "Piper unavailable" note.
- [ ] Preflight (AI engine row): OK when Piper is ready; warns "will use the Windows voice" when it is not.
- [ ] Engine Online, "Fall back to offline" ticked, no key: the break is spoken by the Piper voice.
- [ ] Long program (Pre-produce or Show Builder) with a Piper voice: one clip, one voice.

## 1.78.x launch checklist (Emergency Media Vault, Failover, Health, Presenter, Operator console)
Run on the built Windows .exe before going on air. About 15 minutes, no stream needed unless noted.

### Build
- [ ] `local-build.bat` finishes; `dist\RadioCastOS\RadioCastOS.exe` starts with no console window.
- [ ] `ffmpeg.exe` and `ffplay.exe` (and `ffprobe.exe` if staged) are inside `dist\RadioCastOS\_internal`.
- [ ] Window title and header show the same version as `src/version.py`.

### Emergency Media Vault (Diagnostics > Emergency Media Vault)
- [ ] CHOOSE FOLDER, pick a folder with 2 good MP3s: status turns EMERGENCY MEDIA READY with real durations (not "—").
- [ ] Add a silent MP3: row shows WARNING "silent from the start". Add a renamed text file as .mp3: row shows INVALID (could not be decoded).
- [ ] Add an empty .mp3: INVALID "File is empty". Remove the bad files: back to READY within ~10 seconds.
- [ ] Click REFRESH 10 times quickly: the window stays responsive and does not slow down afterwards.
- [ ] Restart the app: the folder you chose is still used.
- [ ] Header chip FALLBACK shows OK (green) when ready, CHECK (amber) with a warning row, NO FALLBACK (red) with no media; one toast appears once per session; clicking the chip opens the Vault.

### Failover Readiness
- [ ] Fallback Audio row reflects the Vault folder (not a default folder).
- [ ] After SAVE SETTINGS, Configuration Backup turns READY (a file appears in the backups folder).
- [ ] Settings > Operator & Reliability > Backup stream: enter `host:8000/live` and save; Backup Stream turns READY. Clear it: WATCH.

### Station Health Center
- [ ] Opens without freezing; tiles show real Streaming / Audio / Storage states.
- [ ] While streaming (needs a stream): Streaming tile follows the real state.

### AI Presenter Command Center
- [ ] Clock ticks; ON AIR / OFF AIR follows the real state.
- [ ] While a track plays: remaining time shows "m:ss remaining of m:ss" and turns red in the last 10 seconds.
- [ ] PREPARE BREAK: button greys out while preparing; the script appears; scrolling it is not reset every half second; select text and it stays selected.
- [ ] With Autopilot on, the safety text still mentions Emergency Stop.
- [ ] Resize the window narrower/wider: the wrapped text follows.

### Operator Control Console
- [ ] NOW card shows "-m:ss left" and counts down.
- [ ] With a commercial/news/sweeper queued 4th or later, the BREAK card shows it; with none, "No break scheduled".
- [ ] Open and close the Health, Incident, Continuity, Failover and Vault windows repeatedly while using Refresh: no errors in the log, no slowdown.

## 1.78.8 - Kokoro presenter voice (needs a real Windows check)

The automated tests use stand-ins for sherpa-onnx, ffmpeg and the network, so none of this has run against a real Kokoro install.

- [ ] AI Presenter Studio > LOCAL VOICES > KOKORO SETUP... > Yes (download): sherpa-onnx and the Kokoro model download to %APPDATA%\RadioCastOS\kokoro (about 400 MB), a "Kokoro ready: 11 voice(s) found" message appears. Offline PC: a clear "could not be downloaded" message.
- [ ] Set the engine to Offline: the Voice box lists "Kokoro: af_bella", "Kokoro: bm_george" and the other speakers. TEST VOICE plays the chosen speaker on this PC's speakers.
- [ ] Move the Speed slider (for example 0.8 and 1.2) and TEST VOICE again: the pace changes (or stays normal if your sherpa-onnx build ignores it).
- [ ] KOKORO SETUP... > No (own files): pick your sherpa-onnx-offline-tts.exe and model folder; the check says ready.
- [ ] Make a presenter break with a Kokoro voice: it airs as normal. Rename the model folder and make another break: it is spoken with the Windows voice and the automation log shows a "Kokoro unavailable" note. TEST VOICE in that state shows the real error instead.
- [ ] A script with a name containing an accented letter (for example "Olá") and curly quotes is spoken without garbled characters.

## 1.78.11 - Live audio sources (needs a real Windows check)

The automated tests use fake Windows audio devices, so none of this has run against real hardware.

- [ ] Go live with a microphone and the music source both on the Audio page. On the On Air desk the AUDIO SOURCES row shows TALK and MUSIC ON.
- [ ] TALK > press (now TALKING): the microphone is live on the stream. Press again: the microphone is silent on the stream and the Windows Sound > Recording tab shows it muted; the Windows level is the same as before.
- [ ] MUSIC ON > press: the music fades out on the stream over about a second; press again and it fades back. The stream never drops.
- [ ] TALK: music fades down to about 20% and the microphone opens. Press TALKING: the music fades back to its original level and the microphone closes.
- [ ] While talking, press MUSIC: it goes to silence; press again: back to the quiet level. End TALK: back to normal.
- [ ] Close the app while ducked: the Windows microphone and the music device are back at their original level and not muted.
- [ ] Kill the app (Task Manager) while ducked, start it again: within a few seconds the levels are back.
- [ ] A PC with no loopback/virtual-cable device: MUSIC and TALK still work through the player volume (a brief gap in the music is expected). With no microphone source on the Audio page the MIC tile is greyed out and says so.

## 1.78.13 - CALLER button (needs a real Windows check)

Fake devices only in the automated tests. Needs WhatsApp Desktop, a virtual audio cable and a phone to call from. Setup: docs/WHATSAPP_CALL_IN.md.

- [ ] Audio page: the source "CABLE Output" has a Caller checkbox; ticking it and saving makes a CALLER OFF AIR button appear next to TALK on the On Air desk. Untick it: the button disappears and TALK is wide again.
- [ ] With the line ticked and the app just started, call the station's WhatsApp from a phone and answer in WhatsApp Desktop: the caller is NOT heard on the stream (line closed).
- [ ] Press CALLER OFF AIR (now CALLER ON AIR): the caller is heard on the stream, the presenter microphone opens and the music fades to about 20%.
- [ ] Press CALLER ON AIR: the caller is silent on the stream, the microphone closes and the music fades back up.
- [ ] With TALK on, bring the caller on and off: TALK stays on (mic open, music down) afterwards.
- [ ] Close the app while the caller is on air: in Windows Sound > Recording the cable's level and mute are as before.

## 1.78.32 - BREAK NEXT (needs a real Windows check)

- [ ] The app starts (the 1.78.31 zip stopped with a SyntaxError).
- [ ] On Air desk: a BREAKS row with BREAK NEXT. With AutoDJ off it is greyed ("Needs AutoDJ on"); with AutoDJ on and a campaign or commercial pool it is blue.
- [ ] Press it while a song plays: the tile turns amber (BREAK ARMED, N spots), the song finishes, then the spots play and music resumes. The Commercial As-Run Log shows the spots.
- [ ] Press BREAK ARMED before the song ends: it cancels and no break plays.
- [ ] Operator role sees BREAK NEXT; the rundown panel no longer shows READY / ON AIR.

## 1.78.33 - JINGLE NEXT (needs a real Windows check)

- [ ] BREAKS & JINGLES row: BREAK NEXT and JINGLE NEXT side by side. JINGLE NEXT is greyed with a reason when AutoDJ is off or the program has no jingle or sweeper files.
- [ ] Press JINGLE NEXT mid-song: JINGLE ARMED (amber), BREAK NEXT greys out; the song ends, one jingle plays, music resumes. Press JINGLE ARMED before the song ends: it cancels.
- [ ] Arm a break first: JINGLE NEXT greys out until the break has played or is cancelled.
- [ ] Idle desk with a queue: the NOW card says Standby (not the next track); while a song plays NOW shows that song.

## 1.78.x — On Air desk, Station Health, loudness (needs a real Windows check)

- [ ] App starts cleanly (1.78.32 fixed a startup SyntaxError; confirm on the built installer, not only from source).
- [ ] **JINGLE NEXT** (BREAKS & JINGLES row): press with AutoDJ on: it reads JINGLE ARMED and one jingle plays at the next AutoDJ pick. Press again before the pick: it cancels. With AutoDJ off, or no jingle or sweeper pool, it is greyed with a reason.
- [ ] **BREAK NEXT**: arms a break that plays after the current track; press again to cancel; greyed with a reason when AutoDJ is off or no campaign can play. A break and a jingle cannot both be armed: the other button greys out.
- [ ] Program clock: NOW shows the track on air, or Standby when nothing is playing (never the next item). NEXT says "Chosen by AutoDJ" when AutoDJ is on and nothing is queued.
- [ ] **MIC / MUSIC / TALK** buttons: levels restore after TALK ends, after closing the app, and after a crash.
- [ ] **CALLER** button appears only for a source ticked Caller; the mic opens and music ducks while it is on (see docs/WHATSAPP_CALL_IN.md).
- [ ] **Station Health** page shows stop, stream, silence, backup, vault and incidents; the older centres open from it and do not start playback.
- [ ] **Emergency Media Vault**: verified-media view opens; Emergency Stop still wins over anything the vault or centres suggest.
- [ ] **Dual mount**: with a backup address set, the backup mount receives the same encode, including with the native source setting on. Stopping the stream clears the drift and LOW flags.
- [ ] **Loudness**: the library shows measured LUFS and HOT after a rescan and after a restart; a tag refresh keeps the measured value.
- [ ] Encoder clock and bitrate show on the source line; `nowplaying.json` updates; an aired cart stamps encoder time in the as-run affidavit.
- [ ] Kokoro / Piper setup pages open; with neither installed the presenter falls back and the log says why.


## 1.79.0 — Pads & Timers, library

- [ ] Pads & Timers opens from the sidebar; it looks right (pad grid, six timer cards) at your usual window size and at 125% / 150% scaling.
- [ ] Right-click an empty pad, choose an mp3, SAVE: the pad shows its name. Restart the app: it is still there.
- [ ] While streaming with music playing, press the pad: listeners hear it over the music. Press it again mid-play: it stops.
- [ ] Pad with a missing file shows "File missing"; pressing it says why instead of failing.
- [ ] STOP PADS and Emergency Stop both silence a playing pad.
- [ ] EDIT PADS ticked: clicking a pad opens the editor instead of playing.
- [ ] Timer: START, PAUSE, RESUME, RESET, +1:00. At zero the card flashes red, counts up, and the player bar announces it, also from another page. No sound is made.
- [ ] A time-of-day timer set to two minutes ahead finishes on the clock minute.
- [ ] TRACK LEFT follows the song on air; TOP OF HOUR reaches 0:00 on the hour.
- [ ] Library: **Add Files** with an mp3, a .wma and an .opus: all three appear; adding them again adds nothing.
- [ ] Operator login sees Pads & Timers; Ctrl+1..4 switch the four operator pages.

## 1.79.1 - Local voices and sidebar (needs a real Windows check)

- [ ] Make the window short: a slim scrollbar appears on the right of the sidebar page list; the wheel and dragging it scroll to the last page. Make the window tall again: the scrollbar disappears.
- [ ] AI Presenter Studio shows a LOCAL VOICES section (open) with PC VOICE, PIPER and KOKORO blocks, and a "Local voices" chip in the quick-jump bar.
- [ ] PC VOICE: REFRESH VOICES shows how many Windows voices there are; TEST PC VOICE speaks on this PC's speakers; WINDOWS SPEECH SETTINGS opens Windows speech settings.
- [ ] PIPER: paste or BROWSE the program and voices folder; the status line says "Files found: N voice(s)"; CHECK says ready; TEST speaks a sample; Save AI Settings keeps the paths after a restart.
- [ ] KOKORO: the same with the Kokoro program and model folder; KOKORO SETUP… download fills the fields in.
- [ ] "If Piper fails, use the PC voice" / "If Kokoro fails, use the PC voice" are kept separately after Save.

## 1.79.2 - Readability and keyboard access (needs a real Windows check)

- [ ] Hints, captions and idle labels (the dimmest grey text) are easy to read on every page, and disabled buttons still look clearly disabled.
- [ ] Press Tab: focus moves through the play, pause, stop, previous, next and mute buttons; the focused one shows a ring, and Space or Enter presses it.
- [ ] Click the volume slider, then press Left/Right: volume moves one step each time; Page Up/Page Down move five; Home/End go to the ends. Ctrl+Left/Right still seeks.
- [ ] Hover a control at the very top or right edge of the screen (and on a second monitor): the tooltip stays fully visible. Tab to a button: its tooltip appears too.

## 1.79.4 - Modern flat buttons (needs a real Windows check)

- [ ] Buttons on every page look flat (no raised edge): standard, quiet (Ghost), amber (Accent), red (Danger) and green (Success).
- [ ] Hover lightens a button and its edge; pressing darkens it; moving off restores it.
- [ ] Tab to a button: a clear ring shows and there is no dashed box inside it. The amber buttons show a dark ring.
- [ ] A disabled button (for example Go Live while a test runs, or the playlist arrows with no selection) looks recessed and its text is dim but readable.
- [ ] Nothing is cut off or pushed out of view on the On Air, Library, Automation and AI Presenter Studio pages at the smallest window size.

## 1.80.0 - Simpler commercial entry (needs a real Windows check)

- [ ] Automation -> Commercial Campaigns -> **Add Campaign** opens ONE window (no chain of pop-ups), centred over the manager, with the name box ready to type in.
- [ ] ADD AUDIO FILES… lets you pick two mp3 files at once; both appear in the list and the name is filled in from the first file. Open it again: the picker starts in the same folder.
- [ ] Select two tracks on the Library page first, then Add Campaign: they are already listed, and the name is suggested.
- [ ] Press 1 week: From is today and To is six days later. Press Always: both are empty.
- [ ] Press Create campaign with nothing filled in: a red message appears inside the window (nothing closes). Fix it and press Enter: the campaign appears in the list, selected.
- [ ] A name already in use, a date typed as 9 Oct, and a letter in Plays per day each give a clear red message. An error in More options opens that section by itself.
- [ ] Select a campaign, press **Edit / Add Spots** (or double-click it): add a third audio file and change the end date. After Save, the list and detail panel show the new dates and its played / missed counts are unchanged.
- [ ] Play a commercial break: the new spot is logged in the Commercial As-Run Log under the right campaign.
- [ ] Break Composer and Remove Campaign are both visible and work (they no longer overlap).
- [ ] After closing the form, the Campaign Manager is still the only window you can click (modal).

## 1.80.1 - On Air desk polish (needs a real Windows check)
- [ ] The header has no Go Live button; GO LIVE on the On Air desk and Ctrl+G still start and stop the stream.
- [ ] Press TAKEOVER: the tile shows `TAKEOVER` / `ACTIVE · press to release` with nothing cut off; press it again and it releases (with AutoDJ on or off), at 1366x768 and larger.
- [ ] STATION ID, AI ON AIR and RETURN TO AUTODJ tiles show their text fully (icon beside the title).
- [ ] On a short window the On Air page scrolls (wheel and scrollbar) down to the AI Presenter and Breaks rows; on a tall window there is no scrollbar.
- [ ] PREVIOUS and NEXT show their sub-lines and line up with PLAY and STOP.

## Automation setup (1.90.2 - 1.90.4)
- [ ] The line of ticks under the master switches fits on one row, and the three buttons below it (Quick commercial setup, Demo setup, Replace demo files) are not cut off at the smallest window size.
- [ ] Press any button on the Automation page: it flashes green for a moment. LIVE TAKEOVER turns red (RELEASE TAKEOVER) while a takeover is on.
- [ ] **Music** with nothing selected in the Library: a warning line appears at the top of the page. With tracks selected: "Added N tracks", and the Music button shows a tick.
- [ ] Schedule: tick Mon-Fri, press Morning, press **Add to schedule**: five rows appear and the week bar fills in. Press it again: "already in the schedule", no doubles. Add an overlapping slot for another program: a confirmation names both entries. Tab to a day chip and press Space: it toggles.
- [ ] Type `6am` and `18:30` in From / To: both are accepted. Type `banana`: the warning names it.
- [ ] **Clear all (run 24/7)** asks first, and the hint then says AutoDJ runs all day, every day.
- [ ] Ads every 3 songs, spots 2: type the numbers (no arrows), press Tab: "Saved: 2 ads every 3 songs..." appears. With AutoDJ running and a campaign set, an ad break plays after 3 songs.
- [ ] **Quick commercial setup:** add two audio files, leave Normal, press Create: the campaign appears under Commercial Campaigns and the checklist shows "Commercials: 1 campaign". With no files chosen, the red message explains.
- [ ] **Demo setup** (off air): builds the audio with a progress line, shows the amber DEMO bar. Enable AutoDJ: songs, an ad break about every 2 songs, jingles and IDs. **Restore my setup** returns the previous programs, schedule and campaigns exactly.
- [ ] **Replace demo files:** select one demo song, Replace with a file of your own: the row disappears from the demo list, the count drops by one, and NEXT 10 can now play your file. Select 3 rows and choose 3 files: swapped in order. Select 3 rows and choose 2 files: an explanation, nothing changed.
- [ ] **Keep demo as my setup** says how many demo files remain. After keeping, Replace demo files still works.
