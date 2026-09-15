#!/usr/bin/env python3
"""Local voice-to-clipboard bridge for the service workflow.

Hold the configured key, speak, release it, and the transcription is copied to
 the clipboard. The bridge does not send audio or text to a remote service.
"""

from __future__ import annotations

import argparse
from collections import deque
import sys
import threading
import time

try:
    import keyboard
    import numpy as np
    import pyperclip
    import sounddevice as sd
    from faster_whisper import WhisperModel
except ImportError as exc:
    package = str(exc).split("'")[1] if "'" in str(exc) else str(exc)
    print(
        f"Missing dependency: {package}. Install the bridge dependencies with "
        "`python -m pip install -r requirements.txt`."
    )
    raise SystemExit(1) from exc

SAMPLE_RATE = 16_000
MIN_DURATION = 0.3
BUFFER_SECONDS = 0.35
TAIL_SECONDS = 0.35
RELEASE_DEBOUNCE_SECONDS = 0.08
_recording = False
_transcribing = False
_audio_chunks: list[np.ndarray] = []
_recent_chunks: deque[np.ndarray] = deque(maxlen=6)
_audio_lock = threading.Lock()
_model: WhisperModel | None = None


def audio_callback(indata, frames, time_info, status):
    del frames, time_info
    if status:
        print(f"Audio status: {status}", file=sys.stderr)
    with _audio_lock:
        _recent_chunks.append(indata.copy())
        if _recording:
            _audio_chunks.append(indata.copy())


def start_recording() -> float:
    global _recording, _audio_chunks
    with _audio_lock:
        _audio_chunks = list(_recent_chunks)
        _recording = True
    print("Recording... release the key to transcribe.", end="\r")
    return time.monotonic()


def transcribe_and_copy(record_start: float) -> None:
    global _recording, _transcribing
    _transcribing = True
    try:
        time.sleep(TAIL_SECONDS)
        with _audio_lock:
            _recording = False
            chunks = list(_audio_chunks)

        duration = time.monotonic() - record_start
        if duration < MIN_DURATION:
            print("Skipped: key press was too short.")
            return
        if not chunks:
            print("No audio captured.")
            return

        audio = np.concatenate(chunks, axis=0).flatten()
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak < 0.001:
            print("Microphone level is near silent. Check Windows input settings.")
            return
        audio = audio / max(peak, 1.0)
        print("Transcribing...", end="\r")
        segments, _ = _model.transcribe(
            audio,
            beam_size=5,
            language="en",
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            condition_on_previous_text=False,
            temperature=0.0,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        if not text:
            print("Nothing detected.")
            return

        pyperclip.copy(text)
        print(f"Copied: {text}")
    except Exception as exc:
        print(f"Transcription failed: {exc}")
    finally:
        _recording = False
        _transcribing = False
        print("Ready for next recording.")


def load_model(model_name: str, device: str) -> None:
    global _model
    compute_type = "int8" if device == "cpu" else "float16"
    print(f"Loading Whisper model '{model_name}' on {device}...")
    _model = WhisperModel(model_name, device=device, compute_type=compute_type)
    print("Model ready.")


def main() -> int:
    parser = argparse.ArgumentParser(description="OCHRE local voice-to-clipboard bridge")
    parser.add_argument("--model", default="tiny.en")
    parser.add_argument("--key", default="right ctrl")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    args = parser.parse_args()

    load_model(args.model, args.device)
    print(f"Hold {args.key.upper()}, speak, then release. Press Ctrl+C to stop.")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
        blocksize=1024,
    )
    stream.start()
    key_held = False
    record_start = 0.0
    release_started = None

    try:
        while True:
            pressed = keyboard.is_pressed(args.key)
            if pressed and not key_held and not _transcribing:
                key_held = True
                release_started = None
                record_start = start_recording()
            elif pressed and key_held:
                release_started = None
            elif not pressed and key_held and release_started is None:
                release_started = time.monotonic()
            elif (
                not pressed
                and key_held
                and release_started is not None
                and time.monotonic() - release_started >= RELEASE_DEBOUNCE_SECONDS
            ):
                key_held = False
                release_started = None
                threading.Thread(
                    target=transcribe_and_copy,
                    args=(record_start,),
                    daemon=True,
                ).start()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nBridge stopped.")
        return 0
    finally:
        stream.stop()
        stream.close()


if __name__ == "__main__":
    raise SystemExit(main())
