"""
Abstract Base Protocol for HoneyClaw Decoy Tools.
"""

from typing import Any, Dict, Protocol


class DecoyTool(Protocol):
    name: str
    description: str
    input_schema: Dict[str, Any]

    def execute(self, arguments: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Execute the decoy action, return convincing fake telemetry, and record the trap."""
        ...
