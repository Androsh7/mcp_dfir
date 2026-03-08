"""Management CLI for the MCP server"""

# Standard libraries
import argparse
from pathlib import Path

# Project libraries
from llm_forensics.constants import VERSION

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="forensics_mcp_manager", description="This is a management CLI for the MCP forensics server"
    )
    parser.add_argument("--version", action="version", version=f"LLM Forensics {VERSION}")
    subparser = parser.add_subparsers(title="Manage")

    # Symbol commands
    symbol_parser = subparser.add_parser(name="symbol")
    symbol_parser.add_argument("ls", action="store_true", help="Recursively list all symbols at /symbols")
    symbol_parser.add_argument("rm", action="store_true", help="Delete a specified symbol file")
    symbol_parser.add_argument("upload", action="store_true", help="Upload a symbol file to /symbols")

    # Evidence commands
    evidence_parser = subparser.add_parser(name="evidence")
    evidence_parser.add_argument("ls", action="store_true", help="Recursively list all evidence at /evidence")
    evidence_parser.add_argument("rm", type=str, help="Delete a specified evidence file")
    evidence_parser.add_argument("upload", type=Path, help="Upload an evidence file to /evidence")

    # Docker commands
    docker_parser = subparser.add_parser(name="docker")
    docker_parser.add_argument("status", action="store_true", help="Show the current state of the docker container")
    docker_parser.add_argument("restart", action="store_true", help="Restart the docker container")
    docker_parser.add_argument("rebuild", action="store_true", help="Rebuild the docker container")

    # History commands
    history_parser = subparser.add_parser(name="history")
    history_parser.add_argument("show", action="store_true", help="Show all history (truncated)")
    history_parser.add_argument("show-output", type=str, help="Show the output of a specific command")
    history_parser.add_argument("dump", action="store_true", help="Show all untruncated history")
    history_parser.add_argument("clear", action="store_true", help="Clear the command history")

    args = parser.parse_args()
    parser.print_help()
