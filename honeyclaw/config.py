"""
HoneyClaw Configuration Schema.
"""

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
import yaml


class HoneypotConfig(BaseModel):
    version: str = "1.0.0"
    server_name: str = "internal-infra-agent-mcp"
    server_version: str = "1.0.0"

    # Enabled decoy suites
    enable_vault_decoy: bool = True
    enable_database_decoy: bool = True
    enable_shell_decoy: bool = True
    enable_filesystem_decoy: bool = True

    # Alerting & Telemetry
    event_log_path: str = "honeyclaw_events.jsonl"
    canary_secret_key: Optional[str] = None
    webhook_url: Optional[str] = None


def load_config(config_path: Optional[str] = None) -> HoneypotConfig:
    """Load configuration from file or return defaults."""
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return HoneypotConfig(**data)

    default_file = Path("honeyclaw.yaml")
    if default_file.exists():
        with open(default_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return HoneypotConfig(**data)

    return HoneypotConfig()
