"""Runs the MCP server in development mode"""

# Standard libraries
import os
import subprocess
from pathlib import Path

PARENT_DIRECTORY = Path(__file__).parent
os.environ["SERVER_PORT"] = "7778"
os.environ["CLIENT_PORT"] = "7777"

try:
    subprocess.run(f"mcp dev {str(PARENT_DIRECTORY / 'llm_forensics' / 'server.py').replace('\\', '/')}", check=True)
except KeyboardInterrupt:
    pass
