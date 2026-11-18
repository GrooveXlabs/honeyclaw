"""
Canary Token Generator & Cryptographic Verifier.
Creates authentic-looking synthetic credentials embedded with HMAC-signed telemetry.
"""

import base64
import hashlib
import hmac
import os
import time
from typing import Any, Dict, Optional, Tuple


class CanaryEngine:
    DEFAULT_SECRET = "honeyclaw-sovereign-canary-secret-2026"

    def __init__(self, secret_key: Optional[bytes] = None):
        key = secret_key or os.environ.get("HONEYCLAW_CANARY_SECRET", self.DEFAULT_SECRET).encode("utf-8")
        self.secret_key = key

    def _sign(self, payload: str) -> str:
        sig = hmac.new(self.secret_key, payload.encode("utf-8"), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(sig[:8]).decode("utf-8").rstrip("=")

    def generate_aws_canary(self, label: str = "prod-agent") -> Dict[str, str]:
        """Generate a realistic AWS Access Key Pair embedded with canary telemetry."""
        epoch_hex = f"{int(time.time()):08x}"
        signature = self._sign(f"aws:{label}:{epoch_hex}")
        # Standard AWS Key ID is 20 chars starting with AKIA
        # 4 + 8 + 8 = 20 characters
        key_id = f"AKIA{epoch_hex.upper()}{signature[:8].upper()}"
        secret_raw = os.urandom(30)
        secret_key = base64.b64encode(secret_raw).decode("utf-8")[:40]

        return {
            "type": "AWS_ACCESS_KEY",
            "label": label,
            "access_key_id": key_id,
            "secret_access_key": secret_key,
        }

    def generate_github_pat_canary(self, label: str = "repo-sync") -> Dict[str, str]:
        """Generate a realistic GitHub classic Personal Access Token."""
        epoch_hex = f"{int(time.time()):08x}"
        signature = self._sign(f"ghp:{label}:{epoch_hex}")
        # Standard ghp_ has 36 alphanumeric characters after prefix
        body = f"{epoch_hex}{signature}{hashlib.sha256(signature.encode()).hexdigest()[:20]}"[:36]
        token = f"ghp_{body}"

        return {
            "type": "GITHUB_PAT",
            "label": label,
            "token": token,
        }

    def generate_openai_canary(self, label: str = "llm-cluster") -> Dict[str, str]:
        """Generate a realistic OpenAI format API token."""
        epoch_hex = f"{int(time.time()):08x}"
        signature = self._sign(f"openai:{label}:{epoch_hex}")
        body = f"proj-{epoch_hex}{signature}{hashlib.sha256(signature.encode()).hexdigest()[:24]}"[:48]
        token = f"sk-{body}"

        return {
            "type": "OPENAI_KEY",
            "label": label,
            "token": token,
        }

    def verify_aws_canary(self, key_id: str, label: str = "prod-agent") -> Tuple[bool, Optional[str]]:
        """Verify if an intercepted AWS key is an authentic HoneyClaw canary."""
        if not key_id.startswith("AKIA") or len(key_id) < 20:
            return False, None

        epoch_hex = key_id[4:12].lower()
        extracted_sig = key_id[12:20].upper()

        expected_sig = self._sign(f"aws:{label}:{epoch_hex}")[:8].upper()
        if hmac.compare_digest(extracted_sig, expected_sig):
            try:
                created_ts = int(epoch_hex, 16)
                created_str = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(created_ts))
                return True, f"Verified HoneyClaw canary '{label}' generated at {created_str}"
            except ValueError:
                return True, f"Verified HoneyClaw canary '{label}'"

        return False, None
