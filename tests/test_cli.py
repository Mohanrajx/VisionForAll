from pathlib import Path

from visionforall.main import main


def test_help(capsys) -> None:
    code = main([])
    captured = capsys.readouterr()
    assert code == 0
    assert "VisionForAll offline assistant" in captured.out


def test_describe_command(capsys) -> None:
    code = main(["describe"])
    captured = capsys.readouterr()
    assert code == 0
    assert "Mock description" in captured.out


def test_ingest_command_with_config(tmp_path: Path, capsys) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("Emergency exits are marked with green signs.", encoding="utf-8")

    config = tmp_path / "config.toml"
    config.write_text('vector_store_dir = "' + str(tmp_path / "vstore") + '"', encoding="utf-8")

    code = main(["ingest-kb", str(docs), "--config", str(config)])
    captured = capsys.readouterr()
    assert code == 0
    assert "Ingested" in captured.out
