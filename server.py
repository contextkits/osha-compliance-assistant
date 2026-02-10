from mcp.server.fastmcp import FastMCP
import json
import os
server_name = os.path.basename(os.getcwd()).replace("-", " ").title()
mcp = FastMCP(f"{server_name} Reference")
DATA_FILE = "data.json"
@mcp.tool()
def search_reference(query: str) -> str:
    if not os.path.exists(DATA_FILE): return "Database empty."
    with open(DATA_FILE, 'r') as f: data = json.load(f)
    results = [item for item in data if query.lower() in str(item).lower()]
    return json.dumps(results[:5], indent=2)
if __name__ == "__main__": mcp.run()
