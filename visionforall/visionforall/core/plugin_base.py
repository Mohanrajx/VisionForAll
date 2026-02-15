"""Base interfaces for plugins."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from visionforall.core.events import Frame, KBAnswer


class Plugin(ABC):
    """Base plugin contract."""

    name: str


class VisionPlugin(Plugin, ABC):
    """Vision model plugin interface."""

    @abstractmethod
    def describe(self, frame: Frame) -> str:
        """Describe visual content."""

    @abstractmethod
    def read_text(self, frame: Frame) -> str:
        """Extract text-oriented description."""


class STTPlugin(Plugin, ABC):
    """Speech-to-text plugin interface."""

    @abstractmethod
    def transcribe(self) -> str:
        """Capture and transcribe user speech."""


class TTSPlugin(Plugin, ABC):
    """Text-to-speech plugin interface."""

    @abstractmethod
    def speak(self, text: str) -> None:
        """Speak text."""


class KBPlugin(Plugin, ABC):
    """Knowledge base plugin interface."""

    @abstractmethod
    def ingest(self, path: Path) -> int:
        """Ingest docs and return number of chunks."""

    @abstractmethod
    def ask(self, question: str) -> KBAnswer:
        """Query KB and return answer with sources."""
