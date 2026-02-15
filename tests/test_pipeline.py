from pathlib import Path

from visionforall.config import load_config
from visionforall.core.events import Frame
from visionforall.core.pipeline import AssistantPipeline
from visionforall.plugins.kb.rag_langchain import LocalRAGKBPlugin
from visionforall.plugins.vision.moondream import MockVisionPlugin


def test_pipeline_describe() -> None:
    pipeline = AssistantPipeline(
        MockVisionPlugin(),
        LocalRAGKBPlugin(Path("."), Path(".vectorstore_test")),
    )
    output = pipeline.describe_scene(Frame(source="unit-test"))
    assert "Mock description" in output


def test_kb_ingest_and_ask(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("Emergency exits are marked with green signs.", encoding="utf-8")

    kb = LocalRAGKBPlugin(kb_root=docs, vector_store_dir=tmp_path / "vs")
    count = kb.ingest(docs)
    assert count >= 1

    answer = kb.ask("Where are emergency exits marked?")
    assert "Best local answer" in answer.answer
    assert answer.sources


def test_load_toml_config(tmp_path: Path) -> None:
    config = tmp_path / "cfg.toml"
    config.write_text(
        '\n'.join(
            [
                'log_level = "DEBUG"',
                'mode = "wake_word"',
                '[privacy]',
                'allow_network = false',
                'telemetry_enabled = false',
            ]
        ),
        encoding="utf-8",
    )
    cfg = load_config(config)
    assert cfg.log_level == "DEBUG"
    assert cfg.mode == "wake_word"
