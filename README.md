# VisionForAll

VisionForAll is an open-source, offline-first **Edge-AI Accessibility Assistant** built for visually impaired users and low-connectivity environments. It runs locally and is designed to be privacy-safe by default.

---

## What you get
- Local-first CLI assistant (Typer-based command UX).
- Vision workflows: scene description + text-reading.
- Voice pipeline (STT/TTS plugins with graceful fallback behavior).
- Knowledge-base Q&A with local retrieval (LangChain + Chroma when installed, heuristic fallback otherwise).
- Modular plugin architecture so you can swap vision/STT/TTS/KB components.
- Secure-by-default config (no cloud calls, no telemetry by default).

---

## Project structure
```text
visionforall/
  visionforall/
    main.py
    config.py
    core/
    plugins/
    data/sample_kb/
  scripts/
  tests/
  .github/workflows/
```

---

## Step-by-step installation

### 1) Clone and enter repo
```bash
git clone <YOUR_REPO_URL>
cd VisionForAll
```

### 2) Create virtual environment

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install package
```bash
pip install -e .
```

### 4) Verify installation
```bash
visionforall --help
```

### 5) (Optional) Install capability extras
Install only what you need:
```bash
pip install -e .[vision]
pip install -e .[stt]
pip install -e .[tts]
pip install -e .[rag]
pip install -e .[yaml]
```

Or install multiple extras at once:
```bash
pip install -e .[vision,stt,tts,rag,yaml]
```

---

## Step-by-step usage

### A. Quick smoke flow
1. Show CLI commands:
   ```bash
   visionforall --help
   ```
2. Describe a scene:
   ```bash
   visionforall describe
   ```
3. Read text from camera frame:
   ```bash
   visionforall read-text
   ```

### B. Ingest local knowledge and ask questions
1. Ingest docs (markdown/txt):
   ```bash
   visionforall ingest-kb visionforall/visionforall/data/sample_kb
   ```
2. Ask a question:
   ```bash
   visionforall ask "Where are emergency exits usually marked?"
   ```

### C. Run assistant loop
```bash
visionforall run
```
Then follow prompt instructions (`Enter` to interact, `q` to quit).

---

## Configuration (env + config files)

You can configure runtime via environment variables (`VFA_*`) and optional config files (`.toml`, `.yaml`, `.yml`, `.json`).

### Example `config.toml`
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

Use it:
```bash
visionforall ask "Where are exits?" --config config.toml
```

---

## Super UI (local web UI plan)

VisionForAll is currently **CLI-first** for reliability and accessibility in constrained environments.

### Current UI status
- ✅ Production path: terminal/CLI.
- 🔜 “Super UI” local web interface: planned roadmap item (dashboard + large controls + audio state + KB chat panel).

### Proposed Super UI feature set
- High-contrast accessibility theme and keyboard-only navigation.
- One-click actions: Describe, Read Text, Ask KB, Start/Stop listening.
- Live transcript + response panel.
- Privacy indicators (network/cloud disabled badges).
- Local-only mode indicator and model/plugin health checks.

> If you want, a next PR can scaffold `/ui` with a minimal local dashboard (no cloud dependency), keeping CLI as primary backend.

---

## Architecture
```text
[Camera Sensor] -> [Vision Plugin] -> [Pipeline] -> [Console + TTS Output]
                                \-> [KB Plugin (LangChain+Chroma or fallback)]
[STT Plugin] ----> [Assistant Intent Router] ----/
```

---

## Privacy & security defaults
- No cloud calls by default.
- No telemetry by default.
- No sensitive audio persisted by default.
- Local KB index under `.vectorstore/`.

See also: `SECURITY.md` and `CONTRIBUTING.md`.

---

## Publish quick path
1. Run checks:
   ```bash
   PYTHONPATH=visionforall python -m ruff check .
   PYTHONPATH=visionforall python -m pytest -q
   PYTHONPATH=visionforall python -m visionforall.main --help
   ```
2. Push branch and open PR.
3. Use `RELEASE_CHECKLIST.md` for full release/publish steps.

---

## Hardware notes (Raspberry Pi optional)
- Raspberry Pi 4+ can run CLI and fallback plugins.
- Use lighter local models for low-RAM setups.

---

## Roadmap
- Better wake-word implementation.
- Better multilingual model packs.
- Haptic output plugins.
- Local web “Super UI” and mobile companion.

---

## License
Apache-2.0. See `LICENSE`.
