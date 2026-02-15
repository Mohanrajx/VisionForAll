"""Core inference pipeline wiring plugins together."""

from __future__ import annotations

from visionforall.core.events import Frame, KBAnswer
from visionforall.core.plugin_base import KBPlugin, VisionPlugin


class AssistantPipeline:
    """Simple orchestrator for reusable flows."""

    def __init__(self, vision: VisionPlugin, kb: KBPlugin) -> None:
        self.vision = vision
        self.kb = kb

    def describe_scene(self, frame: Frame) -> str:
        """Generate natural language scene description."""
        return self.vision.describe(frame)

    def read_scene_text(self, frame: Frame) -> str:
        """Read text from frame."""
        return self.vision.read_text(frame)

    def query_kb(self, question: str) -> KBAnswer:
        """Run KB question answering."""
        return self.kb.ask(question)
