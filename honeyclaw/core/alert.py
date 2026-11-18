"""
Forensic Event Logger & Alert Dispatcher for HoneyClaw.
"""

import json
import os
import time
from typing import Any, Dict, Optional


class AlertDispatcher:
    def __init__(self, log_path: str = "honeyclaw_events.jsonl", webhook_url: Optional[str] = None):
        self.log_path = log_path
        self.webhook_url = webhook_url or os.environ.get("HONEYCLAW_WEBHOOK_URL")

    def dispatch_alert(
        self,
        event_type: str,
        session_id: str,
        tool_name: str,
        profile_summary: Dict[str, Any],
        payload_details: Dict[str, Any],
    ) -> Dict[str, Any]:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "session_id": session_id,
            "tool_name": tool_name,
            "profile": profile_summary,
            "details": payload_details,
        }

        # Write to JSON-Lines event log
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

        # Future: Webhook dispatch via urllib if webhook_url configured
        return event
