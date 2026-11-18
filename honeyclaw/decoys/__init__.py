"""
Decoy Tools Suite for HoneyClaw.
"""

from honeyclaw.decoys.base import DecoyTool
from honeyclaw.decoys.secrets import DecoySecretsVaultTool
from honeyclaw.decoys.database import DecoyDatabaseTool
from honeyclaw.decoys.shell import DecoyDiagnosticShellTool
from honeyclaw.decoys.filesystem import DecoyFilesystemTool

__all__ = [
    "DecoyTool",
    "DecoySecretsVaultTool",
    "DecoyDatabaseTool",
    "DecoyDiagnosticShellTool",
    "DecoyFilesystemTool",
]
