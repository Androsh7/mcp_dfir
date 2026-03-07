"""Defines hashing tools"""

# Third-party libraries
from typing import Literal

from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.server import mcp
from llm_forensics.docker_manager import docker_manager

HASHING_ALGORITHMS = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
]

@mcp.tool()
def get_hash(ctx: Context, file_path: str, algorithm: Literal["md5", "sha1", "sha256", "sha512"]) -> str:
    """Get the hash of a file"""
    if algorithm.lower() not in HASHING_ALGORITHMS:
        raise KeyError(f'Unsupported hashing algorithm "{algorithm}", this function supports: {", ".join(HASHING_ALGORITHMS)}')
    return docker_manager.exec_stream(ctx, [f'{algorithm.lower()}sum', file_path])
