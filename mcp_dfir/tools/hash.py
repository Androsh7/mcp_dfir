"""Defines hashing tools"""

# Standard libraries
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from mcp_dfir.docker_manager import docker_manager
from mcp_dfir.tools.models import CommandRecordSummary

HASHING_ALGORITHMS = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
]


def get_hash(
    ctx: Context, file_path: str, algorithm: Literal["md5", "sha1", "sha256", "sha512"]
) -> CommandRecordSummary:
    if algorithm.lower() not in HASHING_ALGORITHMS:
        raise KeyError(
            f'Unsupported hashing algorithm "{algorithm}", this function supports: {", ".join(HASHING_ALGORITHMS)}'
        )

    command_list = [f"{algorithm.lower()}sum", file_path]
    return docker_manager.exec_stream(ctx, command_list)
