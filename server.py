#!/usr/bin/env python3
"""
OSHA Compliance MCP Server
Built by contextkits - https://github.com/contextkits/osha-compliance-assistant

MCP server providing OSHA workplace safety compliance tools.
"""

import json
import logging
from typing import Any, Optional
from pathlib import Path

# MCP SDK imports
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, LoggingLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("osha-mcp")

# Load OSHA data
DATA_DIR = Path(__file__).parent / "data"

def load_gold_standard() -> dict:
    """Load the Gold Standard compliance table"""
    gold_path = DATA_DIR / "gold_standard.json"
    if gold_path.exists():
        with open(gold_path) as f:
            return json.load(f)
    return {"regulations": []}

def load_full_context() -> str:
    """Load full OSHA 2201 manual"""
    context_path = DATA_DIR / "osha_context.txt"
    if context_path.exists():
        return context_path.read_text()
    return ""

GOLD_STANDARD = load_gold_standard()
FULL_CONTEXT = load_full_context()

server = Server("osha-compliance-assistant")

# Smart routing logic (from your bot)
def needs_heavy_search(query: str) -> bool:
    """Determines if query needs full context or just Gold Standard"""
    lite_patterns = [
        "guardrail", "railing", "height", "42 inch", "fall protection",
        "ladder", "rung", "extension", "3 feet",
        "exit", "egress", "door", "width", "28 inch",
        "fire extinguisher", "travel distance",
        "eye protection", "safety glasses", "ppe",
        "noise", "hearing", "85 db",
        "forklift", "truck", "training",
        "grinder", "work rest",
        "toilet", "restroom", "sanitation",
        "loto", "lockout", "tagout",
        "hazcom", "sds", "label", "chemical",
        "compressed air", "30 psi",
        "eyewash", "shower", "corrosive",
        "fan", "blade", "mesh",
        "stair", "riser", "tread",
        "oxygen", "acetylene", "cylinder",
        "panel", "breaker", "clearance",
        "cord", "daisy chain",
        "spray", "booth", "paint",
        "blood", "hep b", "vaccine",
        "grain", "bin", "silo",
        "first aid", "clinic",
        "crane", "hoist", "hook"
    ]
    
    query_lower = query.lower()
    for pattern in lite_patterns:
        if pattern in query_lower:
            logger.info(f"✅ LITE mode: '{pattern}'")
            return False
    
    if len(query.split()) < 12:
        logger.info("✅ LITE mode: short question")
        return False
    
    logger.info("⚠️  HEAVY mode: complex/long query")
    return True

def search_gold_standard(query: str) -> Optional[dict]:
    """Search the Gold Standard table"""
    query_lower = query.lower()
    for reg in GOLD_STANDARD.get("regulations", []):
        patterns = reg.get("question_patterns", [])
        for pattern in patterns:
            if pattern.lower() in query_lower:
                return reg
        if reg.get("id", "").lower() in query_lower:
            return reg
    return None

def format_compliance_response(regulation: dict) -> str:
    """Format response in OSHA bot style"""
    decision = regulation.get("decision", "UNKNOWN")
    icon = regulation.get("icon", "❓")
    summary = regulation.get("summary", "")
    citation = regulation.get("citation", "")
    penalty = regulation.get("penalty_range", "")
    
    response = f"{icon} {decision} - Section {citation}\n\n"
    response += f"• {summary}\n"
    if penalty:
        response += f"• Violation penalty: {penalty}\n"
    if "NOT COMPLIANT" in decision or "PROHIBITED" in decision:
        response += f"• Action required: Immediate correction needed\n"
    return response

def search_full_context(query: str) -> str:
    """Search the full OSHA manual"""
    relevant_sections = []
    query_lower = query.lower()
    lines = FULL_CONTEXT.split('\n')
    
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in query_lower.split()):
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            context = '\n'.join(lines[start:end])
            relevant_sections.append(context)
            if len(relevant_sections) >= 3:
                break
    
    if relevant_sections:
        return "\n\n---\n\n".join(relevant_sections)
    return "No specific regulation found. Consult OSHA 1910 standards directly."

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="compliance_check",
            description="Check if a workplace scenario complies with OSHA regulations. Returns YES/NO with citation, penalty risk, and guidance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "Workplace scenario to check (e.g., 'guardrail 40 inches high')"
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["quick", "detailed"],
                        "default": "quick"
                    }
                },
                "required": ["scenario"]
            }
        ),
        Tool(
            name="citation_search",
            description="Look up specific OSHA regulation by citation number (e.g., '1910.147')",
            inputSchema={
                "type": "object",
                "properties": {
                    "citation": {
                        "type": "string",
                        "description": "OSHA regulation number"
                    }
                },
                "required": ["citation"]
            }
        ),
        Tool(
            name="fine_calculator",
            description="Estimate potential OSHA fine amounts for violations",
            inputSchema={
                "type": "object",
                "properties": {
                    "violations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of violations"
                    },
                    "violation_type": {
                        "type": "string",
                        "enum": ["serious", "willful", "repeat", "other"],
                        "default": "serious"
                    }
                },
                "required": ["violations"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    try:
        if name == "compliance_check":
            scenario = arguments.get("scenario", "")
            detail_level = arguments.get("detail_level", "quick")
            
            if not scenario:
                return [TextContent(type="text", text="❌ Error: Provide a scenario")]
            
            use_heavy = detail_level == "detailed" or needs_heavy_search(scenario)
            
            if use_heavy:
                context = search_full_context(scenario)
                response = f"**OSHA Compliance Check (Detailed)**\n\n{context}"
            else:
                regulation = search_gold_standard(scenario)
                if regulation:
                    response = format_compliance_response(regulation)
                else:
                    response = "❓ No direct match. Try 'detailed' mode or rephrase."
            
            return [TextContent(type="text", text=response)]
        
        elif name == "citation_search":
            citation = arguments.get("citation", "")
            if not citation:
                return [TextContent(type="text", text="❌ Provide a citation number")]
            
            for reg in GOLD_STANDARD.get("regulations", []):
                if citation.lower() in reg.get("id", "").lower():
                    response = f"**{reg.get('citation')}**: {reg.get('summary', '')}"
                    return [TextContent(type="text", text=response)]
            
            context = search_full_context(citation)
            return [TextContent(type="text", text=f"**{citation}**\n\n{context}")]
        
        elif name == "fine_calculator":
            violations = arguments.get("violations", [])
            violation_type = arguments.get("violation_type", "serious")
            
            penalty_ranges = {
                "serious": {"min": 1000, "max": 16131},
                "willful": {"min": 10000, "max": 161310},
                "repeat": {"min": 10000, "max": 161310},
                "other": {"min": 100, "max": 16131}
            }
            
            base_range = penalty_ranges.get(violation_type, penalty_ranges["serious"])
            count = len(violations)
            est_min = base_range["min"] * count
            est_max = base_range["max"] * count
            
            response = f"**OSHA Fine Estimate**\n\n"
            response += f"Violations ({count}):\n" + "\n".join(f"- {v}" for v in violations) + "\n\n"
            response += f"**Type**: {violation_type.title()}\n"
            response += f"**Estimated Range**: ${est_min:,} - ${est_max:,}\n"
            
            return [TextContent(type="text", text=response)]
        
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def main():
    """Run the server"""
    logger.info("🚀 Starting OSHA Compliance MCP Server...")
    logger.info(f"📊 Loaded {len(GOLD_STANDARD.get('regulations', []))} regulations")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="osha-compliance-assistant",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
