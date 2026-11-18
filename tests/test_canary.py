"""
Unit tests for HoneyClaw Canary Engine.
"""

import pytest
from honeyclaw.core.canary import CanaryEngine


def test_aws_canary_generation_and_verification():
    engine = CanaryEngine(secret_key=b"test-honeyclaw-secret-key-999")
    canary = engine.generate_aws_canary(label="staging-api")

    assert canary["type"] == "AWS_ACCESS_KEY"
    assert canary["access_key_id"].startswith("AKIA")
    assert len(canary["access_key_id"]) == 20
    assert len(canary["secret_access_key"]) == 40

    # Verify authentic token
    is_valid, msg = engine.verify_aws_canary(canary["access_key_id"], label="staging-api")
    assert is_valid
    assert "Verified HoneyClaw canary 'staging-api'" in msg

    # Forged token should fail
    is_invalid, _ = engine.verify_aws_canary("AKIA99999999FAKESIG1", label="staging-api")
    assert not is_invalid


def test_github_and_openai_canaries():
    engine = CanaryEngine()
    gh = engine.generate_github_pat_canary(label="ci-runner")
    assert gh["token"].startswith("ghp_")
    assert len(gh["token"]) == 40

    ai = engine.generate_openai_canary(label="cluster-eval")
    assert ai["token"].startswith("sk-")
