"""Defines hashing tools"""

# Standard libraries
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

from llm_forensics.docker_manager import docker_manager

# Project libraries
from llm_forensics.tools.models import CommandRecordTruncated

HASHING_ALGORITHMS = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
]


def get_hash(
    ctx: Context, file_path: str, algorithm: Literal["md5", "sha1", "sha256", "sha512"]
) -> CommandRecordTruncated:
    if algorithm.lower() not in HASHING_ALGORITHMS:
        raise KeyError(
            f'Unsupported hashing algorithm "{algorithm}", this function supports: {", ".join(HASHING_ALGORITHMS)}'
        )

    command_list = [f"{algorithm.lower()}sum", file_path]
    return docker_manager.exec_stream(ctx, command_list, truncate=None)
