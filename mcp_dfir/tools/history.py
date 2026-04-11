"""Defines the records mcp routes"""

# Standard libraries
import re

# Third-party libraries
from mcp_dfir.constants import COMMAND_MAX_OUTPUT_BYTES
from mcp_dfir.data_manager import command_history_manager
from mcp_dfir.tools.models import CommandRecordSummary


def get_command_history() -> list[CommandRecordSummary]:
    return command_history_manager.command_summary_list


def get_command_result(
    command_number: int,
    head: int | None,
    head_bytes: int | None,
    tail: int | None,
    tail_bytes: int | None,
    regex: str | None,
    byte_limit=COMMAND_MAX_OUTPUT_BYTES,
) -> str:
    """Allows for parsing of the command result

    Args:
        command_number: The command number
        head: The number of lines from the start to return
        head_bytes: The number of bytes to read from the start (Applied after running head/tail)
        tail: The number of lines from the rear to return
        tail_bytes: The number of bytes to read from the end (Applied after running head/tail)
        regex: An optional regex search
        byte_limit: The maximum number of bytes in the output before throwing an error (set to None to bypass the limit)

    Returns:
        The command result
    """
    if head and tail:
        raise RuntimeError("Cannot set tail and head at the same time")
    if head_bytes and tail_bytes:
        raise RuntimeError("Cannot set tail_bytes and head_bytes at the same time")

    # Get the command result
    content = command_history_manager.get_command(command_number=command_number).result

    # Truncate for head/tail
    if head:
        content = "\n".join(content.split("\n")[:head])
    elif tail:
        content = "\n".join(content.split("\n")[tail:])

    # Truncate for head/tail bytes
    if head_bytes:
        content = content[:head_bytes]
    elif tail_bytes:
        content = content[-tail_bytes:]

    # Regex search
    output = []
    for line in content.split("\n"):
        if regex is None or re.search(regex, line):
            output.append(line)

    output_str = "\n".join(output)

    if byte_limit is not None and len(output_str) >= byte_limit:
        raise RuntimeError(f"Output exceeds maximum size, output was {len(output_str)} bytes")

    return output_str
