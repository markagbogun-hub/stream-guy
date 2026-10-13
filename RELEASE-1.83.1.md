# RadioCastOS 1.83.1 — Programme Studio Voice Regeneration

## Added
- Programme Studio REGENERATE now uses the configured `AIPresenter` script/TTS runtime for non-music, non-news segments.
- Rendering runs off-air in a background worker so the UI remains responsive.
- Successful audio is validated, copied to the approved presenter library, and attached to the selected rundown item.
- Duration is measured with the local media probe when available; otherwise the programme uses a conservative spoken-word estimate.
- Audio changes reset the workflow to draft and clear the previous review timestamp.

## Safety boundaries
- Regeneration does not start playback or submit queue items.
- Music assets cannot be voice-regenerated.
- News segments are blocked until validated, current source material can be passed to the generator by a trusted-news adapter.
- Operators must run PREFLIGHT and REVIEW again before authorization.

## Verification
- `python -m py_compile src/gui_ai_programme_studio.py`
- `python scripts/test_ai_broadcast_workflow.py`
- `python scripts/test_ai_programme_director.py`
- `python scripts/check_version.py`
