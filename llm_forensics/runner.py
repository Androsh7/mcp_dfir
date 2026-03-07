"""Argument runner for llm_forensics"""

# Standard libraries
from time import sleep

# Project libraries
from llm_forensics.server import mcp
from llm_forensics.docker_manager import docker_manager
from llm_forensics.tools import hash, volatility

if __name__ == "__main__":
    docker_manager.start_forensic_container()
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass
    finally:
        docker_manager.stop_forensic_container()
