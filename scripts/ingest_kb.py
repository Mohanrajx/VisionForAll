"""Build local vector/chunk index from docs folder."""

from __future__ import annotations

import argparse
from pathlib import Path

from visionforall.config import load_config
from visionforall.plugins.kb.rag_langchain import LocalRAGKBPlugin


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest local markdown/txt docs")
    parser.add_argument("path", type=Path, help="Path to docs folder")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional config (.toml/.yaml/.json)",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    kb = LocalRAGKBPlugin(cfg.kb_dir, cfg.vector_store_dir)
    count = kb.ingest(args.path)
    print(f"Ingested {count} chunks into {cfg.vector_store_dir}")


if __name__ == "__main__":
    main()
