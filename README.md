# OSHA Compliance Assistant (MCP Server)

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io)

Give Claude instant access to OSHA General Industry compliance knowledge (29 CFR 1910). Ask workplace safety questions and get cited verdicts with regulation sections and corrective actions.

---

## Get Your API Key

**Free tier available — no credit card required.**

| Tier | Daily Calls | Price |
|------|------------|-------|
| Sandbox | 50/day | Free |
| Developer | 5,000/day | $49/mo |
| Team | 20,000/day | $149/mo |
| Enterprise | Unlimited | $499/mo |

---

## Installation

```bash
pip install mcp httpx
```

---

## Claude Desktop Setup

Add to `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osha-compliance": {
      "command": "python",
      "args": ["/path/to/osha-compliance-assistant/server.py"],
      "env": {
        "OSHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

## Available Tool

### `compliance_check`

Check whether a workplace scenario complies with OSHA General Industry standards.

**Input:**
```json
{
  "scenario": "Describe the workplace situation or safety question"
}
```

**Output:** Cited compliance verdict with relevant regulation section and recommended actions.

---

## Coverage

OSHA 29 CFR 1910 General Industry standards including fall protection, machine guarding, electrical safety, lockout/tagout, PPE, fire safety, hazard communication, forklifts, and more.

---

## Disclaimer

AI-generated guidance only. Not a substitute for official OSHA publications or certified safety inspections. Always verify with a qualified safety professional.

---

## License

MIT — see [LICENSE](LICENSE)

An MCP server that gives Claude instant access to OSHA General Industry compliance knowledge (29 CFR 1910). Ask any workplace safety question and get a cited YES/NO verdict with the relevant regulation section and corrective actions.

---

## What It Does

Claude can answer questions like:

- *"Do I need guardrails on a 4-foot platform?"* → `✅ YES - Section 1910.23(c)(1)`
- *"Can I store propane cylinders near an exit door?"* → `❌ NO - Section 1910.253(b)`
- *"Is automatic restart after a power outage allowed on saws?"* → `❌ NO - Section 1910.213(a)(9)`

Covers 30+ high-priority OSHA 1910 topics including fall protection, lockout/tagout, electrical safety, machine guarding, fire extinguishers, forklifts, PPE, hazard communication, and more.

---

## Get Your API Key

**Free tier available.** Get your API key instantly via Telegram:

📧 Email gcsmst at gmail.com with subject "MCP API Key" to get your free Sandbox key

| Tier | Daily Queries | Price |
|------|--------------|-------|
| Free | 5/day | Free |
| Starter | 100/day | $9/mo |
| Pro | 1,000/day | $29/mo |
| Enterprise | Unlimited | $99/mo |

---

## Installation

```bash
pip install mcp httpx
```

---

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osha-compliance": {
      "command": "python",
      "args": ["/path/to/osha-compliance-assistant/server.py"],
      "env": {
        "OSHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace `/path/to/osha-compliance-assistant/server.py` with the actual path where you cloned this repo.

---

## Available Tool

### `compliance_check`

Check whether a workplace scenario complies with OSHA General Industry standards.

**Input:**
```json
{
  "scenario": "string — describe the workplace situation or safety question"
}
```

**Output:**

Plain text response with:
- ✅ YES or ❌ NO verdict
- Cited OSHA section (e.g. `Section 1910.23(c)(1)`)
- 3 bullet points with specific requirements
- Corrective actions where applicable

**Example:**

```
User: Do workers need hard hats when doing electrical panel work?

Claude (via OSHA MCP):
❌ NO - Section 1910.135
- Hard hats (ANSI Z89.1) required when overhead electrical hazard exists
- Electrical panel work requires Class E rated hard hat for arc flash protection
- Employer must conduct hazard assessment before work begins (1910.132(d))

⚠️ AI analysis only — verify with official OSHA standards or a safety professional.
```

---

## Topics Covered

| Section | Topic |
|---------|-------|
| 1910.23 | Guardrails & Fall Protection |
| 1910.25 | Portable Ladders |
| 1910.36-37 | Exit Routes & Doors |
| 1910.95 | Noise & Hearing Conservation |
| 1910.133 | Eye & Face Protection |
| 1910.135 | Head Protection |
| 1910.147 | Lockout/Tagout (LOTO) |
| 1910.157 | Fire Extinguishers |
| 1910.178 | Forklifts |
| 1910.212 | Machine Guarding |
| 1910.215 | Grinders |
| 1910.242 | Compressed Air |
| 1910.253 | Oxygen & Fuel Cylinders |
| 1910.303 | Electrical Safety |
| 1910.1200 | Hazard Communication (SDS) |
| 5(a)(1) | General Duty Clause |

---

## Disclaimer

This tool provides AI-generated compliance guidance based on OSHA 1910 General Industry standards. It is **not a substitute** for professional safety consultation, official OSHA publications, or certified safety inspections. Always verify with official OSHA standards or a qualified safety professional before making compliance decisions.

---

## License

MIT License — see [LICENSE](LICENSE)
