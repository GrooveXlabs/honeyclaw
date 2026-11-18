# HoneyClaw: Technical Standard Operating Procedure (SOP)

## 1. Scope & Objective
This SOP defines the operational procedures for deploying HoneyClaw decoy environments, seeding canary credentials into sensitive workflows, and responding to agentic honeypot alerts.

---

## 2. Environment Variables & Setup
* **`HONEYCLAW_CANARY_SECRET`**: Set a strong symmetric secret (32+ bytes) for canary HMAC signing:
  ```bash
  export HONEYCLAW_CANARY_SECRET="sovereign-canary-secret-2026"
  ```
* **`HONEYCLAW_WEBHOOK_URL`** (Optional): Slack/Discord or SIEM webhook for instant notifications.

---

## 3. Deployment Modes

### Mode A: Local MCP Decoy Server (Antigravity / Claude Desktop)
Add HoneyClaw to your MCP server registry:
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

### Mode B: Canary Seeding
Generate canary tokens and plant them in non-production code repositories, internal wiki pages, or decoy repositories:
```bash
honeyclaw generate-canary --type aws --label "github-actions-backup"
honeyclaw generate-canary --type github --label "wiki-sync"
```

---

## 4. Incident Response & Forensics
When a canary or honeypot trigger occurs:
1. Open the event telemetry file:
   ```bash
   honeyclaw events --limit 20
   ```
2. Verify if a leaked credential belongs to HoneyClaw:
   ```bash
   honeyclaw verify-canary --key "AKIA..." --label "github-actions-backup"
   ```
3. Extract the session ID and cross-reference attacker IP / user-agent with perimeter logs.
