"""Runner for llm_forensics"""

# Standard libraries
import argparse
from pathlib import Path

# Project libraries
from mcp_dfir.constants import VERSION
from mcp_dfir.config import config


def main():
    parser = argparse.ArgumentParser(prog="mcp-dfir", description="MCP Server for Performing Memory and Disk Forensics")
    parser.add_argument("--version", action="version", version=f"MCP DFIR v{VERSION}")
    parser.add_argument("-d", "--case-dir", type=Path, default=Path.cwd(), help=f"Working directory for the case, default: {Path.cwd()}")
    args = parser.parse_args()

    # Load config
    config.load(working_directory=args.case_dir)

    # Load MCP server
    from mcp_dfir.docker_manager import docker_manager
    from mcp_dfir.server import mcp

    # Start the mcp server
    docker_manager.start_forensic_container()
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass
    finally:
        docker_manager.stop_forensic_container()


if __name__ == "__main__":
    main()
