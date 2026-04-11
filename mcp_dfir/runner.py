"""Runner for llm_forensics"""

# Standard libraries
import argparse
import shutil
import sys
from pathlib import Path

# Project libraries
from mcp_dfir.config import config
from mcp_dfir.constants import VERSION


def main():
    parser = argparse.ArgumentParser(prog="mcp-dfir", description="MCP Server for Performing Memory and Disk Forensics")
    parser.add_argument("--version", action="version", version=f"mcp-dfir v{VERSION}")
    parser.add_argument(
        "-d", "--case-dir", type=Path, default=Path.cwd(), help=f"Working directory for the case, default: {Path.cwd()}"
    )
    parser.add_argument("--init", action="store_true", help="Create case directories then exit")
    parser.add_argument(
        "--clear-case-dir", action="store_true", help="Clear the case directory before starting the server"
    )
    parser.add_argument(
        "--clear-docker", action="store_true", help="Clear the forensics docker container before starting the server"
    )
    args = parser.parse_args()

    if args.clear_case_dir:
        user_input = input(
            f"Are you sure you want to clear the case directory {args.case_dir}? This action cannot be undone. Type 'yes' to confirm: "
        )
        if user_input != "yes":
            parser.exit(status=1, message="Case directory not cleared")
        for path in "artifacts", "analysis", "evidence", "symbols":
            shutil.rmtree(args.case_dir / path, ignore_errors=True)
        print("Case directory cleared")
        sys.exit(0)

    # Load config
    config.load(working_directory=args.case_dir)

    if args.init:
        sys.exit(0)

    if args.clear_docker:
        from mcp_dfir.docker_manager import docker_manager

        docker_manager.clear_forensic_container()
        sys.exit(0)

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
