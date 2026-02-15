"""Top-level assistant loop and intent routing."""

from __future__ import annotations

from dataclasses import dataclass

from visionforall.core.pipeline import AssistantPipeline
from visionforall.core.plugin_base import STTPlugin, TTSPlugin
from visionforall.plugins.output.console import ConsoleOutput
from visionforall.plugins.sensors.camera_opencv import CameraSensor


@dataclass(slots=True)
class Assistant:
    """Runtime assistant with push-to-talk interaction."""

    pipeline: AssistantPipeline
    stt: STTPlugin
    tts: TTSPlugin

    def _route_intent(self, text: str) -> str:
        lowered = text.lower()
        if any(k in lowered for k in ["describe", "scene", "around me"]):
            return "describe"
        if any(k in lowered for k in ["read text", "ocr", "read"]):
            return "read_text"
        if any(k in lowered for k in ["ask", "question", "what is"]):
            return "ask_kb"
        return "help"

    def run_once(self) -> str:
        """Run one interaction cycle and return response text."""
        command = self.stt.transcribe()
        intent = self._route_intent(command)
        output = ConsoleOutput()
        camera = CameraSensor()

        if intent == "describe":
            result = self.pipeline.describe_scene(camera.capture_frame())
        elif intent == "read_text":
            result = self.pipeline.read_scene_text(camera.capture_frame())
        elif intent == "ask_kb":
            answer = self.pipeline.query_kb(command)
            citations = ", ".join(s.filename for s in answer.sources) if answer.sources else "none"
            result = f"{answer.answer}\nSources: {citations}"
        else:
            result = (
                "Say one of: describe scene, read text, or ask a knowledge question. "
                "Example: 'ask what are emergency exits?'"
            )

        output.render(result)
        self.tts.speak(result)
        return result

    def run_loop(self) -> None:
        """Run assistant loop in push-to-talk mode."""
        print("VisionForAll running. Press Enter to speak, 'q' to quit.")
        while True:
            key = input("> ").strip().lower()
            if key == "q":
                break
            _ = self.run_once()
