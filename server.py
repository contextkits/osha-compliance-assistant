#!/usr/bin/env python3
"""
OSHA Compliance Assistant - MCP Server
Connects to hosted OSHA compliance API.
Get your API key at: https://t.me/osha_saas_v2_bot
"""

import asyncio
import os
import httpx
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY = os.getenv("OSHA_API_KEY", "")
API_URL  = os.getenv("OSHA_API_URL", "https://os.qcguard.xyz/api/compliance_check")

server = Server("osha-compliance-assistant")

# ── Tools ────────────────────────────────────────────────────────────────────

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="compliance_check",
            description=(
                "Check whether a workplace scenario complies with OSHA General Industry "
                "standards (29 CFR 1910). Returns a cited YES/NO verdict, relevant regulation "
                "sections, and corrective actions where required."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "Describe the workplace situation or safety question."
                    }
                },
                "required": ["scenario"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "compliance_check":
        return [TextContent(type="text", text="Unknown tool.")]

    if not API_KEY:
        return [TextContent(type="text", text=(
            "❌ OSHA_API_KEY not set.\n"
            "Get your free API key at: https://t.me/osha_saas_v2_bot"
        ))]

    scenario = arguments.get("scenario", "").strip()
    if not scenario:
        return [TextContent(type="text", text="Please provide a scenario to check.")]

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                API_URL,
                headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
                json={"scenario": scenario}
            )

        if response.status_code == 401:
            return [TextContent(type="text", text=(
                "❌ Invalid API key. Get yours at: https://t.me/osha_saas_v2_bot"
            ))]

        if response.status_code == 429:
            return [TextContent(type="text", text=(
                "🛑 Daily limit reached. Upgrade at: https://t.me/osha_saas_v2_bot"
            ))]

        if response.status_code != 200:
            return [TextContent(type="text", text=f"❌ API error ({response.status_code}). Please try again.")]

        data = response.json()
        answer = data.get("answer") or data.get("response") or data.get("result") or str(data)
        return [TextContent(type="text", text=answer)]

    except httpx.TimeoutException:
        return [TextContent(type="text", text="❌ Request timed out. Please try again.")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="osha-compliance-assistant",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
