"""Defines the MCP server"""

# Third-party libraries
from mcp.server.fastmcp import FastMCP

# Project libraries
from llm_forensics.tools.file_search import list_files
from llm_forensics.tools.hash import get_hash
from llm_forensics.tools.history import get_command_history, get_command_result
from llm_forensics.tools.notes import (
    add_analyst_note,
    show_analyst_note,
    show_analyst_notes_summary,
    update_analyst_note,
)
from llm_forensics.tools.volatility import download_windows_symbol, run_volatility_command

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
1. Everything whether benign or malicious must be documented, including the commands that were run, the research that was done, and the conclusion with sufficient reasoning
2. Never make any assumptions, if a conclusion cannot be reached on whether a finding is benign or malicious explicitly mark it as needing additional research
3. Never use custom bash or python scripts to parse files, only use the built-in head/tail/regex/truncate options when going through command results

Rules for documenting analyst notes:
1. All notes must be in markdown format
2. Notes should properly document the source of the evidence, the commands that were run, and the research that was done
""",
)

# File search
mcp.add_tool(list_files)

# Hash
mcp.add_tool(get_hash)

# Records
mcp.add_tool(get_command_history)
mcp.add_tool(get_command_result)

# Volatility
mcp.add_tool(run_volatility_command)
mcp.add_tool(download_windows_symbol)

# Notes
mcp.add_tool(show_analyst_notes_summary)
mcp.add_tool(show_analyst_note)
mcp.add_tool(add_analyst_note)
mcp.add_tool(update_analyst_note)
