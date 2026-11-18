"""
Autonomous AI Agent Fingerprinter & Behavioral Profiler.
Analyzes interaction cadence, prompt injection patterns, and reconnaissance velocity.
Fulfills Bhaaratxa Vision / Hunter-Guardian Mandate.
"""

import re
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Deque, Dict, List, Optional


class AttackerArchetype(str, Enum):
    UNKNOWN = "UNKNOWN"
    AUTOMATED_SCRAPER = "AUTOMATED_SCRAPER"
    RECON_BOT = "RECON_BOT"
    DATA_EXFILTRATOR = "DATA_EXFILTRATOR"
    PROMPT_INJECTOR = "PROMPT_INJECTOR"


@dataclass
class AgentProfile:
    session_id: str
    archetype: AttackerArchetype = AttackerArchetype.UNKNOWN
    threat_level: str = "LOW"
    prompt_injection_attempts: int = 0
    recon_depth: int = 0
    calls_count: int = 0
    detected_indicators: List[str] = field(default_factory=list)
    average_velocity_cps: float = 0.0  # calls per second


class AgentFingerprinter:
    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(?:all\s+)?previous\s+(?:instructions|prompts)", re.IGNORECASE),
        re.compile(r"(?:system\s*prompt|hidden\s*instructions|developer\s*mode)", re.IGNORECASE),
        re.compile(r"(?:you\s+are\s+now|act\s+as\s+an\s+unrestricted|DAN\s+mode)", re.IGNORECASE),
        re.compile(r"<\|im_start\|>|<\|im_end\|>|\[INST\]|\[/INST\]", re.IGNORECASE),
        re.compile(r"(?:bypass\s+safety|jailbreak|exfiltrate\s+all)", re.IGNORECASE),
    ]

    RECON_PATTERNS = {
        "credentials": re.compile(r"(?:password|secret|token|api_key|credential|private_key)", re.IGNORECASE),
        "privilege": re.compile(r"(?:admin|root|superuser|sudo|iam|role)", re.IGNORECASE),
        "infrastructure": re.compile(r"(?:database|schema|config|env|backup|vault)", re.IGNORECASE),
    }

    def __init__(self):
        self._sessions: Dict[str, Deque[float]] = {}
        self._profiles: Dict[str, AgentProfile] = {}

    def get_or_create_profile(self, session_id: str) -> AgentProfile:
        if session_id not in self._profiles:
            self._profiles[session_id] = AgentProfile(session_id=session_id)
            self._sessions[session_id] = deque(maxlen=50)
        return self._profiles[session_id]

    def record_interaction(
        self,
        session_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> AgentProfile:
        now = time.time()
        profile = self.get_or_create_profile(session_id)
        timestamps = self._sessions[session_id]
        timestamps.append(now)

        profile.calls_count += 1

        # Calculate velocity
        if len(timestamps) > 1:
            duration = timestamps[-1] - timestamps[0]
            if duration > 0:
                profile.average_velocity_cps = round(len(timestamps) / duration, 2)

        # Inspect arguments stringified
        raw_text = str(arguments)

        # 1. Prompt Injection Detection
        for pat in self.PROMPT_INJECTION_PATTERNS:
            if pat.search(raw_text):
                profile.prompt_injection_attempts += 1
                ind = f"Prompt injection indicator: {pat.pattern}"
                if ind not in profile.detected_indicators:
                    profile.detected_indicators.append(ind)

        # 2. Reconnaissance Analysis
        for category, pat in self.RECON_PATTERNS.items():
            if pat.search(raw_text) or pat.search(tool_name):
                profile.recon_depth += 1
                ind = f"Recon interest detected: {category}"
                if ind not in profile.detected_indicators:
                    profile.detected_indicators.append(ind)

        # 3. Archetype & Threat Classification
        if profile.prompt_injection_attempts > 0:
            profile.archetype = AttackerArchetype.PROMPT_INJECTOR
            profile.threat_level = "CRITICAL"
        elif profile.recon_depth >= 4:
            profile.archetype = AttackerArchetype.DATA_EXFILTRATOR
            profile.threat_level = "HIGH"
        elif profile.average_velocity_cps > 1.5 and profile.calls_count >= 5:
            profile.archetype = AttackerArchetype.AUTOMATED_SCRAPER
            profile.threat_level = "MEDIUM"
        elif profile.recon_depth > 0:
            profile.archetype = AttackerArchetype.RECON_BOT
            profile.threat_level = "MEDIUM"
        else:
            profile.archetype = AttackerArchetype.UNKNOWN
            profile.threat_level = "LOW"

        return profile
