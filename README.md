# OSHA Compliance Assistant (MCP Server)

MCP server providing OSHA workplace safety compliance tools.

## Installation
```bash
pip install mcp
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "osha-compliance": {
      "command": "python",
      "args": ["/path/to/osha-compliance-assistant/server.py"]
    }
  }
}
```

## Tools

- `compliance_check`: Check if scenario complies with OSHA
- `citation_search`: Look up specific regulations
- `fine_calculator`: Estimate violation penalties

## Example

**User**: Is a 40-inch guardrail compliant?

**Claude + OSHA MCP**: ❌ NOT COMPLIANT - Section 1910.23(e)(1)

- Top rail must be 42 inches (±3 inches). Your 40-inch rail is below minimum.
- Violation penalty: $7,000-$15,000
- Action required: Immediate correction needed
