"""CLI entrypoint for VisionForAll."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Annotated, Any

from visionforall.config import load_config
from visionforall.core.assistant import Assistant
from visionforall.core.pipeline import AssistantPipeline
from visionforall.plugins.kb.rag_langchain import LocalRAGKBPlugin
from visionforall.plugins.sensors.camera_opencv import CameraSensor
from visionforall.plugins.stt.faster_whisper import FasterWhisperSTTPlugin
from visionforall.plugins.tts.piper import PiperTTSPlugin
from visionforall.plugins.vision.moondream import MockVisionPlugin

try:
    import typer

    _TYPER_AVAILABLE = True
except ImportError:
    typer = None  # type: ignore[assignment]
    _TYPER_AVAILABLE = False


def _build_assistant(config_path: Path | None = None) -> Assistant:
    cfg = load_config(config_path)
    vision = MockVisionPlugin()
    kb = LocalRAGKBPlugin(cfg.kb_dir, cfg.vector_store_dir)
    pipeline = AssistantPipeline(vision=vision, kb=kb)
    return Assistant(pipeline=pipeline, stt=FasterWhisperSTTPlugin(), tts=PiperTTSPlugin())


def _cmd_run(config: Path | None = None) -> int:
    _build_assistant(config).run_loop()
    return 0


def _cmd_describe(config: Path | None = None) -> int:
    assistant = _build_assistant(config)
    frame = CameraSensor().capture_frame()
    print(assistant.pipeline.describe_scene(frame))
    return 0


def _cmd_read_text(config: Path | None = None) -> int:
    assistant = _build_assistant(config)
    frame = CameraSensor().capture_frame()
    print(assistant.pipeline.read_scene_text(frame))
    return 0


def _cmd_ingest(path: Path, config: Path | None = None) -> int:
    cfg = load_config(config)
    kb = LocalRAGKBPlugin(cfg.kb_dir, cfg.vector_store_dir)
    count = kb.ingest(path)
    print(f"Ingested {count} chunks into {cfg.vector_store_dir}")
    return 0


def _cmd_ask(question: str, config: Path | None = None) -> int:
    cfg = load_config(config)
    kb = LocalRAGKBPlugin(cfg.kb_dir, cfg.vector_store_dir)
    answer = kb.ask(question)
    print(answer.answer)
    if answer.sources:
        print("\nCitations:")
        for src in answer.sources:
            print(f"- {src.filename}: {src.snippet}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Argparse compatibility parser used as a fallback/runtime compatibility path."""
    parser = argparse.ArgumentParser(
        prog="visionforall",
        description="VisionForAll offline assistant",
    )
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Start assistant loop")
    run.add_argument("--config", type=Path, default=None)

    describe = sub.add_parser("describe", help="Capture frame and describe")
    describe.add_argument("--config", type=Path, default=None)

    read_text = sub.add_parser("read-text", help="Capture frame and extract text")
    read_text.add_argument("--config", type=Path, default=None)

    ingest = sub.add_parser("ingest-kb", help="Ingest markdown/txt docs")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--config", type=Path, default=None)

    ask_cmd = sub.add_parser("ask", help="Ask local KB")
    ask_cmd.add_argument("question")
    ask_cmd.add_argument("--config", type=Path, default=None)
    return parser


def _main_argparse(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return _cmd_run(args.config)
    if args.command == "describe":
        return _cmd_describe(args.config)
    if args.command == "read-text":
        return _cmd_read_text(args.config)
    if args.command == "ingest-kb":
        return _cmd_ingest(args.path, args.config)
    if args.command == "ask":
        return _cmd_ask(args.question, args.config)

    parser.print_help()
    return 0


if _TYPER_AVAILABLE:
    app = typer.Typer(help="VisionForAll: Offline-first Edge-AI accessibility assistant.")
    ConfigPathOption = Annotated[Path | None, typer.Option(help="Optional config path.")]

    @app.command("run")
    def run_command(config: ConfigPathOption = None) -> None:
        _cmd_run(config)

    @app.command("describe")
    def describe_command(config: ConfigPathOption = None) -> None:
        _cmd_describe(config)

    @app.command("read-text")
    def read_text_command(config: ConfigPathOption = None) -> None:
        _cmd_read_text(config)

    @app.command("ingest-kb")
    def ingest_command(path: Path, config: ConfigPathOption = None) -> None:
        _cmd_ingest(path, config)

    @app.command("ask")
    def ask_command(question: str, config: ConfigPathOption = None) -> None:
        _cmd_ask(question, config)


def main(argv: list[str] | None = None) -> int:
    """Console script entrypoint.

    - Uses Typer app by default when available and no explicit argv is supplied.
    - Uses argparse fallback for compatibility/testing and environments without Typer.
    """
    if argv is not None or not _TYPER_AVAILABLE:
        return _main_argparse(argv)

    assert typer is not None
    app_obj: Any = app
    try:
        app_obj(standalone_mode=False)
    except typer.Exit as exc:  # pragma: no cover
        return int(exc.exit_code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
