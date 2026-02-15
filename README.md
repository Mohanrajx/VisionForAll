# VisionForAll

VisionForAll is an open-source **Edge-AI accessibility assistant** for visually impaired users and low-connectivity environments. It runs locally, is privacy-first by default, and supports pluggable modules for vision, speech, and local knowledge retrieval.

## Features (MVP)
- Offline-first Typer-based CLI assistant with secure defaults.
- Commands:
  - `visionforall run`
  - `visionforall describe`
  - `visionforall read-text`
  - `visionforall ingest-kb path/to/docs`
  - `visionforall ask "question"`
- Plugin interfaces for `VisionPlugin`, `STTPlugin`, `TTSPlugin`, and `KBPlugin`.
- Moondream wrapper + mock vision plugin for CI.
- Local RAG plugin that uses **LangChain + Chroma** when installed, with a safe offline heuristic fallback when not.
- Config via environment variables + optional `.toml`, `.yaml`, or `.json` file.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
visionforall --help
```

Install feature extras:
```bash
pip install -e .[vision]
pip install -e .[stt]
pip install -e .[tts]
pip install -e .[rag]
pip install -e .[yaml]
```

## Architecture
```text
[Camera Sensor] -> [Vision Plugin] -> [Pipeline] -> [Console + TTS Output]
                                \-> [KB Plugin (LangChain+Chroma or fallback)]
[STT Plugin] ----> [Assistant Intent Router] ----/
```

## Offline mode and privacy
- No cloud calls by default.
- No telemetry by default.
- No sensitive audio is persisted by default.
- Local KB index persists under `.vectorstore/`.

## Config
Environment variables are prefixed with `VFA_`.

Optional config file examples:
```toml
log_level = "INFO"
mode = "push_to_talk"
kb_dir = "visionforall/visionforall/data/sample_kb"
vector_store_dir = ".vectorstore"

[privacy]
allow_network = false
enable_cloud_providers = false
telemetry_enabled = false
```

Use with commands:
```bash
visionforall ask "Where are exits?" --config config.toml
```

## Knowledge base workflow
```bash
visionforall ingest-kb visionforall/visionforall/data/sample_kb
visionforall ask "Where are emergency exits usually marked?"
```


## Publish quick path
1. Run checks:
   ```bash
   PYTHONPATH=visionforall python -m ruff check .
   PYTHONPATH=visionforall python -m pytest -q
   PYTHONPATH=visionforall python -m visionforall.main --help
   ```
2. Push branch and open PR.
3. Use `RELEASE_CHECKLIST.md` for full release/publish steps.

## Hardware notes (Raspberry Pi optional)
- Raspberry Pi 4+ can run CLI and fallback plugins.
- Use smaller local models for low-RAM devices.

## Security baseline
- Apache-2.0 license.
- Lint/tests in CI.
- Security policy in `SECURITY.md`.
- Contribution guidance in `CONTRIBUTING.md`.

## Roadmap
- Better wake-word implementation.
- Better multilingual model packs.
- Haptic output plugins.
- Local web UI and mobile companion.

## License
Apache-2.0. See `LICENSE`.
