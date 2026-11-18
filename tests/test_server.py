"""
Unit tests for Decoy MCP Server protocol compliance.
"""

import json
import pytest
from honeyclaw.config import HoneypotConfig
from honeyclaw.server import DecoyMcpServer


def test_mcp_server_initialize():
    cfg = HoneypotConfig()
    server = DecoyMcpServer(cfg, session_id="test-srv-session")

    resp = server.handle_request({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    })

    assert resp["id"] == 1
    assert resp["result"]["serverInfo"]["name"] == "internal-infra-agent-mcp"
    assert "tools" in resp["result"]["capabilities"]


def test_mcp_server_tools_list():
    cfg = HoneypotConfig()
    server = DecoyMcpServer(cfg, session_id="test-srv-session")

    resp = server.handle_request({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {},
    })

    tools = resp["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "fetch_vault_credentials" in tool_names
    assert "query_customer_database" in tool_names
    assert "run_system_diagnostic" in tool_names
    assert "read_internal_file" in tool_names


def test_mcp_server_tools_call_traps_interaction(tmp_path):
    log_file = str(tmp_path / "events.jsonl")
    cfg = HoneypotConfig(event_log_path=log_file)
    server = DecoyMcpServer(cfg, session_id="test-srv-session")

    resp = server.handle_request({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "fetch_vault_credentials",
            "arguments": {"service": "aws"},
        },
    })

    assert resp["id"] == 3
    content = resp["result"]["content"][0]["text"]
    assert "aws_access_key_id" in content

    # Verify event logged
    with open(log_file, "r", encoding="utf-8") as f:
        log_line = f.readline()
        event = json.loads(log_line)
        assert event["event_type"] == "HONEYPOT_BAIT_TRIGGERED"
        assert event["tool_name"] == "fetch_vault_credentials"
