"""Piper TTS plugin with pyttsx3 fallback."""

from __future__ import annotations

from visionforall.core.plugin_base import TTSPlugin


class PiperTTSPlugin(TTSPlugin):
    """Best effort local speech synthesis."""

    name = "piper"

    def speak(self, text: str) -> None:
        try:
            from piper.voice import PiperVoice  # type: ignore # noqa: F401
        except ImportError:
            self._fallback(text)
            return
        # TODO: wire piper model loading + playback for production setup.
        self._fallback(f"[Piper TODO] {text}")

    @staticmethod
    def _fallback(text: str) -> None:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            print(f"TTS: {text}")
