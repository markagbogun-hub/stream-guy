"""
clone_worker.py — offline voice-cloning worker for RadioCastOS.

RadioCastOS itself runs on the Python standard library only. Voice cloning needs a
neural model (PyTorch etc.), so it lives in a *separate* Python environment that you set
up once, and RadioCastOS runs this script with that environment's python.exe:

    python clone_worker.py --backend chatterbox --text-file in.txt --reference ref.wav --out out.wav

Backends
    chatterbox   Resemble AI Chatterbox (MIT licence, English). pip install chatterbox-tts
    xtts         Coqui XTTS-v2 (multilingual). pip install coqui-tts
                 NOTE: the XTTS-v2 model weights are licensed non-commercial (CPML).
    tone         No model. Writes a short beep so you can test the plumbing.

Two ways to run it
    one-shot   (default)  load the model, render one file, exit.
    --serve               stay alive and render many requests, so the model is loaded ONCE.
                          Protocol: one JSON object per line on stdin / stdout (see serve()).
                          Library chatter that would corrupt stdout is redirected to stderr.
                          The worker exits when stdin closes, so it never outlives RadioCastOS.

Only use a reference recording of a person who has agreed to have their voice cloned.

This file must stay importable without torch: heavy imports happen inside the backends.
Exit code 0 = ok; anything else = failure with a one-line reason on stderr.
"""
from __future__ import annotations

import argparse
import math
import re
import struct
import sys
import wave

MAX_CHUNK_CHARS = 280          # neural TTS drifts on long inputs; render sentence groups
SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")


def split_sentences(text: str, limit: int = MAX_CHUNK_CHARS) -> list[str]:
    """Group sentences into chunks of at most ``limit`` characters.

    A single sentence longer than ``limit`` is split on commas/semicolons, then on spaces,
    so no chunk ever exceeds the limit and no words are lost.
    """
    clean = " ".join((text or "").split())
    if not clean:
        return []
    pieces: list[str] = []
    for sent in SENTENCE_END.split(clean):
        while len(sent) > limit:
            cut = max(sent.rfind(sep, 0, limit) for sep in (", ", "; ", ": "))
            if cut < limit // 3:
                cut = sent.rfind(" ", 0, limit)
            if cut <= 0:
                cut = limit
            pieces.append(sent[:cut + 1].strip())
            sent = sent[cut + 1:].strip()
        if sent:
            pieces.append(sent)
    chunks: list[str] = []
    cur = ""
    for p in pieces:
        if cur and len(cur) + 1 + len(p) > limit:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def pick_device(requested: str) -> str:
    """'auto' -> cuda if PyTorch sees a GPU, else cpu. Explicit values pass through."""
    if requested and requested != "auto":
        return requested
    try:
        import torch  # type: ignore
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def write_wav(path: str, samples, rate: int) -> None:
    """Write mono float samples (-1..1) as 16-bit PCM. Accepts any iterable of floats."""
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(int(rate))
        frames = bytearray()
        for s in samples:
            v = max(-1.0, min(1.0, float(s)))
            frames += struct.pack("<h", int(v * 32767))
        w.writeframes(bytes(frames))


# ── backends: load() once, synth() many times ──────────────────────────────

_LOADS = {"count": 0}          # how many times a model was loaded in this process (diagnostics)


def load_tone(device):
    _LOADS["count"] += 1
    print("tone model loaded")          # deliberate stdout noise: serve mode must survive it
    return object()


def synth_tone(model, chunks, reference, language, out):
    rate = 24000
    samples = []
    for i, _chunk in enumerate(chunks):
        n = int(rate * 0.4)
        samples += [0.3 * math.sin(2 * math.pi * (440 + 60 * (i % 4)) * t / rate) for t in range(n)]
        samples += [0.0] * int(rate * 0.1)
    write_wav(out, samples, rate)


def load_chatterbox(device):
    from chatterbox.tts import ChatterboxTTS  # type: ignore
    model = ChatterboxTTS.from_pretrained(device=device)
    _LOADS["count"] += 1
    return model


def synth_chatterbox(model, chunks, reference, language, out):
    import torch  # type: ignore
    import torchaudio as ta  # type: ignore
    parts = []
    for chunk in chunks:
        parts.append(model.generate(chunk, audio_prompt_path=reference))
        parts.append(torch.zeros(1, int(model.sr * 0.15)))     # short breath between chunks
    ta.save(out, torch.cat(parts, dim=-1), model.sr)


def load_xtts(device):
    from TTS.api import TTS  # type: ignore
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    _LOADS["count"] += 1
    return tts


def synth_xtts(model, chunks, reference, language, out):
    import numpy as np  # type: ignore
    rate = int(getattr(getattr(model, "synthesizer", None), "output_sample_rate", 24000) or 24000)
    audio = []
    for chunk in chunks:
        wav = model.tts(text=chunk, speaker_wav=reference, language=language or "en")
        audio.append(np.asarray(wav, dtype="float32"))
        audio.append(np.zeros(int(rate * 0.15), dtype="float32"))
    write_wav(out, np.concatenate(audio), rate)


BACKENDS = {
    "tone": (load_tone, synth_tone),
    "chatterbox": (load_chatterbox, synth_chatterbox),
    "xtts": (load_xtts, synth_xtts),
}


def render_file(model, backend, text_file, reference, language, out) -> None:
    """Read the text file, split it, and synthesize into ``out`` with an already-loaded model."""
    with open(text_file, "r", encoding="utf-8") as fh:
        chunks = split_sentences(fh.read())
    if not chunks:
        raise ValueError("there is no text to speak")
    if backend != "tone" and not reference:
        raise ValueError("a reference recording of the voice is required")
    BACKENDS[backend][1](model, chunks, reference, language, out)


def serve(backend: str, device: str, stdin, proto) -> int:
    """Request loop. One JSON object per line.

    request : {"id": 1, "cmd": "speak", "text_file": ..., "reference": ..., "out": ..., "language": "en"}
              {"id": 2, "cmd": "warm"}      load the model now, render nothing
              {"id": 3, "cmd": "quit"}
    response: {"id": 1, "ok": true, "loads": 1, "seconds": 3.2}   or   {"id": 1, "ok": false, "error": "..."}
    The first line written is {"ready": true, "backend": ..., "device": ...}.
    The model is loaded on first use and then kept; a failed load is retried on the next request.
    """
    import json
    import time

    def send(obj) -> None:
        proto.write(json.dumps(obj) + "\n")
        proto.flush()

    dev = pick_device(device) if backend != "tone" else "cpu"
    send({"ready": True, "backend": backend, "device": dev})
    model = None
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            send({"id": None, "ok": False, "error": "bad request"})
            continue
        rid, cmd = req.get("id"), req.get("cmd", "speak")
        if cmd == "quit":
            send({"id": rid, "ok": True, "loads": _LOADS["count"]})
            return 0
        t0 = time.time()
        try:
            if model is None:
                model = BACKENDS[backend][0](dev)
            if cmd == "speak":
                render_file(model, backend, req["text_file"], req.get("reference"),
                            req.get("language") or "en", req["out"])
            elif cmd != "warm":
                raise ValueError(f"unknown command {cmd}")
            send({"id": rid, "ok": True, "loads": _LOADS["count"], "seconds": round(time.time() - t0, 2)})
        except Exception as exc:
            send({"id": rid, "ok": False, "error": f"{type(exc).__name__}: {exc}"[:400],
                  "loads": _LOADS["count"]})
    return 0                     # stdin closed: RadioCastOS is gone, so are we


def check_backend(name: str, device: str) -> int:
    """--check: report whether the backend's libraries import, and which device it would use."""
    if name == "tone":
        print("ok tone (no model; plumbing test only)")
        return 0
    try:
        if name == "chatterbox":
            import chatterbox.tts  # type: ignore  # noqa: F401
        elif name == "xtts":
            import TTS.api  # type: ignore  # noqa: F401
        else:
            print(f"unknown backend {name}", file=sys.stderr)
            return 2
    except Exception as exc:
        print(f"{name} is not installed in this Python: {exc}", file=sys.stderr)
        return 3
    print(f"ok {name} on {pick_device(device)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="RadioCastOS voice-cloning worker")
    ap.add_argument("--backend", default="chatterbox", choices=sorted(BACKENDS))
    ap.add_argument("--text-file")
    ap.add_argument("--reference")
    ap.add_argument("--out")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--language", default="en")
    ap.add_argument("--check", action="store_true", help="only verify the backend can be imported")
    ap.add_argument("--serve", action="store_true", help="stay alive and render JSON-line requests from stdin")
    args = ap.parse_args(argv)
    if args.check:
        return check_backend(args.backend, args.device)
    if args.serve:
        proto, sys.stdout = sys.stdout, sys.stderr      # libraries print; only JSON may use the real stdout
        for stream, mode in ((sys.stdin, "r"), (proto, "w")):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass
        return serve(args.backend, args.device, sys.stdin, proto)
    if not (args.text_file and args.out):
        print("--text-file and --out are required", file=sys.stderr)
        return 2
    if args.backend != "tone" and not args.reference:
        print("--reference (a recording of the voice) is required", file=sys.stderr)
        return 2
    try:
        model = BACKENDS[args.backend][0](pick_device(args.device))
        render_file(model, args.backend, args.text_file, args.reference, args.language, args.out)
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}"[:400], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
