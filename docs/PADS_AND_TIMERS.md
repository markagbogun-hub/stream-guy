# Pads & Timers (1.79)

Open it from the sidebar (Broadcast group, after On Air).

## Jingle pads

1. Right-click a pad (or tick **EDIT PADS** and click it). Choose a sound file; give it a name and colour if you like. **SAVE**.
2. Press the pad to play it over the music. Press it again to stop it. **STOP PADS** silences every pad.
3. A pad shows elapsed / total time while it plays. At most four play at once.

How it works: the pad plays on the PC's normal output, the same output as the music, and the stream captures both. So the pad's volume follows the player volume slider, and a muted player means silent pads.

Pads do **not** fade the music down. If you want the music lower under a jingle, lower it yourself or use TALK.

The editor's **TEST** button plays the sound for real; if you are on air it asks first.

Pads are saved in `pads.json` and move with a station package.

## Countdown timers

- Click the time (or **START**) to start, **PAUSE** / **RESUME**, **RESET** to go back, **+1:00** to add a minute (before it starts, it lengthens the starting time).
- **SET** changes the name and time. A time can be a length (`3:00`, `90`, `2m30s`) or a time of day (`17:00`, `5pm`); a time of day that has passed today counts to tomorrow.
- Green while running, amber for the last 10 seconds, then red overtime (`+0:07`) until you reset it.
- When a timer reaches zero the player bar says so, on any page. There is no beep on purpose: anything the PC plays also goes to the stream.
- **TRACK LEFT** is the time left in the song on air. **TOP OF HOUR** counts to the next hour.

Presets are saved in `timers.json`. A running timer is not remembered after a restart.

## Library

**Add Files** picks individual songs. **Add Folder**, drag and drop and M3U import use the same list of formats: mp3, wav, flac, ogg, oga, opus, aac, m4a, wma, aif, aiff, mp2.
