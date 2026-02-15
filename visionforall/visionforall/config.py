"""Configuration management for VisionForAll."""

from __future__ import annotations

import json
import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PrivacyConfig:
    """Privacy and network policy controls."""

    allow_network: bool = False
    enable_cloud_providers: bool = False
    telemetry_enabled: bool = False


@dataclass(slots=True)
class AppConfig:
    """Runtime config with env and optional yaml/toml/json overrides."""

    app_name: str = "VisionForAll"
    log_level: str = "INFO"
    kb_dir: Path = Path("visionforall/visionforall/data/sample_kb")
    vector_store_dir: Path = Path(".vectorstore")
    mode: str = "push_to_talk"
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _load_structured(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".toml", ".tml"}:
        return tomllib.loads(text)
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError("YAML config requires PyYAML. Install visionforall[yaml].") from exc
        return yaml.safe_load(text) or {}
    raise ValueError(f"Unsupported config format: {suffix}")


def load_config(config_path: Path | None = None) -> AppConfig:
    """Load settings from environment and optional config file."""
    cfg = AppConfig(
        log_level=os.getenv("VFA_LOG_LEVEL", "INFO"),
        kb_dir=Path(os.getenv("VFA_KB_DIR", "visionforall/visionforall/data/sample_kb")),
        vector_store_dir=Path(os.getenv("VFA_VECTOR_STORE_DIR", ".vectorstore")),
        mode=os.getenv("VFA_MODE", "push_to_talk"),
        privacy=PrivacyConfig(
            allow_network=_env_bool("VFA_ALLOW_NETWORK", False),
            enable_cloud_providers=_env_bool("VFA_ENABLE_CLOUD_PROVIDERS", False),
            telemetry_enabled=_env_bool("VFA_TELEMETRY_ENABLED", False),
        ),
    )

    if config_path and config_path.exists():
        content = _load_structured(config_path)
        cfg.log_level = content.get("log_level", cfg.log_level)
        cfg.mode = content.get("mode", cfg.mode)
        if "kb_dir" in content:
            cfg.kb_dir = Path(content["kb_dir"])
        if "vector_store_dir" in content:
            cfg.vector_store_dir = Path(content["vector_store_dir"])
        privacy = content.get("privacy", {})
        if isinstance(privacy, dict):
            cfg.privacy.allow_network = bool(
                privacy.get("allow_network", cfg.privacy.allow_network)
            )
            cfg.privacy.enable_cloud_providers = bool(
                privacy.get("enable_cloud_providers", cfg.privacy.enable_cloud_providers)
            )
            cfg.privacy.telemetry_enabled = bool(
                privacy.get("telemetry_enabled", cfg.privacy.telemetry_enabled)
            )
    return cfg
