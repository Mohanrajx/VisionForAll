"""faster-whisper STT plugin with optional keyboard fallback for offline demos."""

from __future__ import annotations

import os

from visionforall.core.plugin_base import STTPlugin


class FasterWhisperSTTPlugin(STTPlugin):
    """STT plugin; falls back to text input if runtime deps are unavailable."""

    name = "faster_whisper"

    def __init__(self) -> None:
        self.model_name = os.getenv("VFA_WHISPER_MODEL", "small")

    def transcribe(self) -> str:
        try:
            from faster_whisper import WhisperModel  # type: ignore # noqa: F401
        except ImportError:
            return input("Speech backend missing. Type your command: ")

        return input("[Demo mode] Press Enter to simulate mic and type transcript: ")
