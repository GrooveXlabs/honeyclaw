# HoneyClaw: Architecture Map & Deception Methodology

## 1. Deception Architecture Overview
HoneyClaw implements an **Active Deception Strategy** for autonomous agentic environments. Rather than passive network traps, HoneyClaw presents high-value semantic decoys tailored to LLM reasoning objectives.

```
┌─────────────────────────────────────────────────────────────┐
│                       CLI & UI LAYER                        │
│                (honeyclaw.cli, Click, Rich)                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    MCP PROTOCOL RUNTIME                     │
│           (honeyclaw.server.DecoyMcpServer, stdio)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     DECOY TOOL SUITE                        │
│  - DecoySecretsVaultTool      (Synthetic AWS/GitHub/OpenAI) │
│  - DecoyDatabaseTool          (Simulated SQL customer PII)  │
│  - DecoyDiagnosticShellTool   (Restricted safe terminal)    │
│  - DecoyFilesystemTool        (Seeded .env & credentials)   │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
┌──────────────▼─────────────┐ ┌──────────────▼───────────────┐
│     CANARY CRYPTOGRAPHY    │ │      AGENT FINGERPRINTER     │
│  - CanaryEngine            │ │  - Interaction cadence (CPS) │
│  - HMAC-SHA256 Token Sign  │ │  - Prompt Injection Detector │
│  - Verification Harness    │ │  - Archetype Classifier      │
└──────────────┬─────────────┘ └──────────────┬───────────────┘
               │                              │
┌──────────────▼──────────────────────────────▼───────────────┐
│                FORENSIC EVENT DISPATCHER                    │
│    (honeyclaw.core.alert.AlertDispatcher, JSONL Telemetry)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Behavioral Profiling & Archetypes

HoneyClaw categorizes autonomous actors into four archetypes:
1. **`PROMPT_INJECTOR` (Critical):** Uses jailbreak triggers (`ignore previous instructions`, `DAN mode`, `developer mode`) attempting to breach host safety guardrails.
2. **`DATA_EXFILTRATOR` (High):** Sequences recon queries across database, vault, and filesystems to maximize data extraction.
3. **`AUTOMATED_SCRAPER` (Medium):** High velocity (> 1.5 calls/sec) brute-force querying without contextual reasoning pauses.
4. **`RECON_BOT` (Medium):** Low-frequency exploratory enumeration.

---

## 3. Cryptographic Canary Assurance
Each canary token generated embeds:
* Epoch timestamp (hex-encoded).
* HMAC signature derived from `HONEYCLAW_CANARY_SECRET`.
* Custom label identifying the deployment vector.

This allows security analysts to prove chain-of-custody for breached credentials during forensics.
