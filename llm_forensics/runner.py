"""Runner for llm_forensics"""

# Standard libraries
import argparse
from pathlib import Path

# Project libraries
from llm_forensics.constants import VERSION
from llm_forensics.config import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="llm_forensics")
    parser.add_argument("--version", action="version", version=f"llm_forensics v{VERSION}")
    parser.add_argument("-d", "--case-dir", type=Path, default=Path.cwd(), help=f"Working directory for the case, default: {Path.cwd()}")
    args = parser.parse_args()

    # Load config
    config.load(working_directory=args.case_dir)

    # Load MCP server
    from llm_forensics.docker_manager import docker_manager
    from llm_forensics.server import mcp

    # Start the mcp server
    docker_manager.start_forensic_container()
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass
    finally:
        docker_manager.stop_forensic_container()
