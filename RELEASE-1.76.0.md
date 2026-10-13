# RadioCastOS 1.76.0 — Audio Asset & Operator Workflow

Adds the operator-facing lifecycle around TTS-generated audio assets.

## Added
- Audio asset registration and immutable SHA-256 identity
- Persistent asset records and handoff records
- Audio preview/QA status model
- Explicit operator accept/reject workflow
- Regeneration-required state
- Explicit **Prepare for Broadcast** handoff artifact
- Script/revision/job/asset correlation
- Operator identity and review notes

## Safety boundary
The workflow does **not** import or mutate `BroadcastEngine`, `BroadcastQueue`, `PlayoutEngine`, or any deterministic playout component.

`Prepare for Broadcast` creates a handoff artifact only. A separate deterministic operator workflow must decide whether and when the asset is actually scheduled or played.
