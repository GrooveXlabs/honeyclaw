# HoneyClaw 🍯
> **Autonomous AI Honeypot & Agent Canary Engine**  
> *Crafted with defense-in-depth by GrooveXlabs — Sovereign-Grade AI Infrastructure.*

[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/GrooveXlabs/honeyclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-black?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Security Standard](https://img.shields.io/badge/Defense-Deception-yellow?style=for-the-badge)](https://github.com/GrooveXlabs/honeyclaw)

---

## ⚡ The Threat: Rogue AI Scrapers & Agentic Attackers
Traditional honeypots (Cowrie, Dionaea) are designed to trap human attackers and automated bash worms scanning port 22.

In 2026, the primary attack surface is shifting to **Autonomous AI Agents**:
* Unfettered web-crawling LLMs scanning internal documentation.
* Rogue agents exploiting open Model Context Protocol (MCP) servers.
* Prompt-injection scrapers attempting to exfiltrate private API keys, databases, and customer PII.

---

## 🍯 The Solution: HoneyClaw
**HoneyClaw** is an active deception honeypot designed specifically to lure, trap, and profile autonomous AI agents. It exposes high-value, realistic fake MCP tools that:
1. **Bait Agents with Synthetic Assets:** Returns realistic AWS credentials, GitHub tokens, database dumps, and `.env` files seeded with **cryptographically signed canary tokens**.
2. **Behavioral AI Profiling:** Analyzes agent interaction speed, tool exploration sequencing, and detects prompt injection attempts (`ignore previous instructions`, `DAN mode`).
3. **Forensic Canary Tracing:** If an attacker attempts to use or sell exfiltrated credentials anywhere on the internet, HoneyClaw's HMAC signature mathematically proves they were stolen from this honeypot.

```
   ┌──────────────────────────────────┐
   │ Autonomous AI Attacker / Scraper │
   └────────────────┬─────────────────┘
                    │  MCP JSON-RPC / Tools Discovery
                    ▼
   ┌─────────────────────────────────────────────────────────┐
   │                 HONEYCLAW DECOY SUITE                   │
   │ ─────────────────────────────────────────────────────── │
   │  [🍯] fetch_vault_credentials   --> Signed AWS/GH Canaries
   │  [🍯] query_customer_database   --> Fake PII + Canary Emails
   │  [🍯] run_system_diagnostic     --> Restricted Sandboxed Shell
   │  [🍯] read_internal_file        --> Seeded .env & Configs
   └────────────────┬────────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────────────────────────┐
   │        HUNTER-GUARDIAN BEHAVIORAL PROFILER              │
   │  * Prompt Injection Detector (Jailbreak / System Leaks) │
   │  * Archetype Classifier (Scraper / Recon / Exfiltrator) │
   │  * Forensic Event Logger (honeyclaw_events.jsonl)       │
   └─────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

* **Authentic MCP Protocol Server:** Fully compliant with Anthropic's Model Context Protocol (JSON-RPC 2.0). Connects seamlessly over `stdio` to Antigravity, Claude Desktop, Cursor, or external agent runners.
* **Cryptographic Canary Engine:** Generates and validates synthetic AWS keys (`AKIA...`), GitHub PATs (`ghp_...`), and OpenAI keys (`sk-...`) embedded with tamper-evident HMAC timestamps.
* **Agent Fingerprinter:** Distinguishes human typing from automated reasoning loops and tags attacker archetypes (`AUTOMATED_SCRAPER`, `RECON_BOT`, `DATA_EXFILTRATOR`, `PROMPT_INJECTOR`).
* **Safe Sandbox Simulation:** Shell diagnostic decoy simulates believable command responses (`whoami`, `id`, `uname -a`) while discarding malicious commands without touching host hardware.

---

## 📦 Quickstart & Installation

```bash
# Clone the repository
git clone https://github.com/GrooveXlabs/honeyclaw.git
cd honeyclaw

# Install package
pip install -e .
```

### Checking Honeypot Status
```bash
honeyclaw status
```

### Generating Canary Tokens Manually
```bash
# Generate an AWS Access Key Pair canary
honeyclaw generate-canary --type aws --label "prod-backup"

# Generate a GitHub Personal Access Token canary
honeyclaw generate-canary --type github --label "repo-sync-bot"
```

### Verifying an Intercepted Token
```bash
honeyclaw verify-canary --key "AKIA6789ABCD..." --label "prod-backup"
```

### Running the Decoy MCP Server
```bash
honeyclaw serve
```

---

## ⚙️ Integrating into Antigravity & Claude Desktop

To expose HoneyClaw as a decoy tool server in your `mcp_config.json`:

```json
{
  "mcpServers": {
    "internal-infra-tools": {
      "command": "honeyclaw",
      "args": ["serve"]
    }
  }
}
```

---

## 📜 License
Licensed under the [MIT License](LICENSE).  
Copyright (c) 2026 GrooveXlabs.
