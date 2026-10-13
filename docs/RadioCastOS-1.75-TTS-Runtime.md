# RadioCastOS 1.75.0 — Voice/TTS Runtime

## Workflow

`PresenterScript (approved) → TTS Runtime → Audio Asset → Audio QA`

Only scripts with explicit `status == approved` are accepted. The runtime records the
script ID/revision, provider, voice profile, cache key, generation state, asset path and
QA result.

## Voice profile

- Provider
- Voice ID
- Language / locale
- Speed
- Pitch metadata
- Style metadata
- Provider-neutral pronunciation substitutions

## Providers

The runtime uses a small provider interface. 1.75 ships adapters for the existing
Windows SAPI and Piper presenter engines. External providers can be registered through
`FunctionProvider` or the same interface.

## Caching

The cache key is derived from the approved script identity/content, revision, voice
configuration and provider. A valid cached asset is returned without a second TTS call.

## Audio QA

The runtime validates file presence/size and supported format. WAV assets are inspected
for duration, sample rate, channels, silence and clipping. Other formats use optional
Mutagen metadata when installed.

## Safety boundary

The TTS runtime does not import or control the Broadcast Engine or Broadcast Queue. It
cannot start, stop, select, skip, reorder, insert or remove broadcast items. A `ready`
or `cached` job is only an audio asset. Broadcast insertion remains an explicit,
deterministic operator/workflow action outside the AI/TTS layer.
