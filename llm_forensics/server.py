"""Defines the MCP server"""

# Third-party libraries
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("llm-forensics", auth=None)
