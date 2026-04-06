"""Defines the MCP server"""

# Third-party libraries
from mcp.server.fastmcp import FastMCP

# Project libraries
from mcp_dfir.tools.file_search import list_files, run_find, run_grep, run_strings
from mcp_dfir.tools.file_tools import untar_file, unzip_file
from mcp_dfir.tools.hash import get_hash
from mcp_dfir.tools.history import get_command_history, get_command_result
from mcp_dfir.tools.notes import (
    add_analyst_note,
    show_analyst_note,
    show_analyst_notes_summary,
    update_analyst_note,
)
from mcp_dfir.tools.sleuthkit import run_sleuthkit_command
from mcp_dfir.tools.volatility import download_windows_symbol, run_volatility_command

# Create MCP server
mcp = FastMCP(
    "llm-forensics",
    auth=None,
    instructions="""\
You are a host forensics agent tasked with performing memory, disk, and artifact forensics.

Before beginning analysis always perform the following tasks:
1. Perform an inventory of all evidence, ask the user for specific details on how, when, and where the evidence was acquired
2. Review all previous commands that have already been run, commands should never be re-run unless the evidence has been updated or the commands were run incorrectly
3. Review all analyst notes to not perform duplicate analysis

While performing analysis follow these rules:
1. Create an analyst note (markdown format) after every finding whether benign, malicious, or if additional research is needed
2. Never make any assumptions, if a conclusion cannot be reached on whether a finding is benign or malicious explicitly mark it as needing additional research
3. Never use custom bash or python scripts to parse files, only use the built-in head/tail/regex/truncate options when going through command results
4. All artifacts should be saved under /artifacts
""",
)

# File search
mcp.add_tool(list_files)
mcp.add_tool(run_strings)
mcp.add_tool(run_grep)
mcp.add_tool(run_find)

# File tools
mcp.add_tool(unzip_file)
mcp.add_tool(untar_file)

# Hash
mcp.add_tool(get_hash)

# Records
mcp.add_tool(get_command_history)
mcp.add_tool(get_command_result)

# Volatility
mcp.add_tool(run_volatility_command)
mcp.add_tool(download_windows_symbol)

# Sleuthkit
mcp.add_tool(run_sleuthkit_command)

# Notes
mcp.add_tool(show_analyst_notes_summary)
mcp.add_tool(show_analyst_note)
mcp.add_tool(add_analyst_note)
mcp.add_tool(update_analyst_note)
