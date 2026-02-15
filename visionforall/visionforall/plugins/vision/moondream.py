"""Moondream vision plugin wrapper with graceful dependency checks."""

from __future__ import annotations

import os

from visionforall.core.events import Frame
from visionforall.core.plugin_base import VisionPlugin


class MoondreamVisionPlugin(VisionPlugin):
    """Pluggable Moondream integration.

    This module intentionally avoids importing moondream globally so the package
    can run without vision extras.
    """

    name = "moondream"

    def __init__(self) -> None:
        self.model_path = os.getenv("VFA_MOONDREAM_MODEL_PATH")

    def _ensure_available(self) -> None:
        try:
            import moondream as _md  # type: ignore # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Moondream is not installed. Install with `pip install visionforall[vision]` "
                "and configure VFA_MOONDREAM_MODEL_PATH."
            ) from exc

    def describe(self, frame: Frame) -> str:
        self._ensure_available()
        return f"[Moondream TODO] Describe frame from {frame.source}."

    def read_text(self, frame: Frame) -> str:
        self._ensure_available()
        return f"[Moondream TODO] Read text in frame from {frame.source}."


class MockVisionPlugin(VisionPlugin):
    """Deterministic plugin for CI/tests."""

    name = "mock_vision"

    def describe(self, frame: Frame) -> str:
        return f"Mock description for frame source={frame.source}."

    def read_text(self, frame: Frame) -> str:
        return "Mock extracted text: EXIT -> Main Hall"
