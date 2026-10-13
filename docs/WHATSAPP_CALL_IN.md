# Taking WhatsApp calls on air

RadioCastOS does not talk to WhatsApp itself. The call runs in **WhatsApp Desktop** on the radio PC, and its audio is
routed through a free **virtual audio cable** into a normal RadioCastOS audio source. The **CALLER** button on the On Air
desk then puts that source on and off air.

## One-time setup (Windows 10)

1. Install WhatsApp Desktop on the radio PC and log in with the station's number.
2. Install a virtual audio cable, for example **VB-Cable** (free, vb-audio.com). It adds a playback device
   "CABLE Input" and a recording device "CABLE Output".
3. Start a WhatsApp call (any call, even one you hang up at once) so WhatsApp appears in
   **Windows Settings > System > Sound > App volume and device preferences**. There set WhatsApp:
   - **Output** = CABLE Input (the caller's voice goes into the cable, not your speakers)
   - **Input** = your presenter microphone (so the caller hears you)
4. In RadioCastOS open **Audio**, click **Refresh devices**, and for the source "CABLE Output" tick **enabled** and
   **Caller**. Save.
5. The **CALLER** button appears next to TALK on the On Air desk.

To let the caller also hear the music or the station, use two cables or VoiceMeeter and feed WhatsApp's input from a mix
of the microphone and the programme. Without that the caller hears only you, which is fine for most call-ins.

## On air

- The caller line is closed whenever RadioCastOS starts, so a call never reaches the stream by accident.
- Answer the call in WhatsApp Desktop, talk off air, then press **CALLER OFF AIR** to bring the caller on.
- **CALLER ON AIR**: the caller is heard, your microphone opens and the music fades down (like TALK).
- Press again: the caller is closed, the microphone closes again and the music fades back up.
- Monitor with headphones. If your own speakers are on, they will feed back into the microphone.

## Good to know

- Needs the optional `pycaw` package (same as TALK and the AI presenter microphone ducking).
- Tell callers they are on air. Many countries require consent for broadcasting or recording calls.
- The WhatsApp Business **Calling API** (Meta Cloud API) is a different, server-based route and is not used here.
