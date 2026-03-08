"""Runner for llm_forensics"""

# Project libraries
from llm_forensics.docker_manager import docker_manager
from llm_forensics.server import mcp

if __name__ == "__main__":
    docker_manager.start_forensic_container()
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass
    finally:
        docker_manager.stop_forensic_container()
