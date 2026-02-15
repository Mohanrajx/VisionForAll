"""Event and data types used across assistant components."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Frame:
    """Represents a captured image frame."""

    source: str
    payload: object | None = None


@dataclass(slots=True)
class KBSource:
    """Represents one knowledge citation."""

    filename: str
    snippet: str
    path: Path | None = None


@dataclass(slots=True)
class KBAnswer:
    """Response from KB with answer text and citations."""

    answer: str
    sources: list[KBSource]
