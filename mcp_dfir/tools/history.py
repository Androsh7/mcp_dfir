"""Defines the records mcp routes"""

# Standard libraries
import re

# Third-party libraries
from mcp_dfir.data_manager import command_history_manager
from mcp_dfir.tools.models import CommandRecordSummary


def get_command_history() -> list[CommandRecordSummary]:
    return command_history_manager.command_summary_list


def get_command_result(command_number: int, head: int | None, tail: int | None, regex: str | None) -> str:
    if head and tail:
        raise RuntimeError("Cannot set tail and head at the same time")

    # Get the command result
    content = command_history_manager.get_command(command_number=command_number).result

    # Truncate for head/tail
    if head:
        content = "\n".join(content.split("\n")[:head])
    elif tail:
        content = "\n".join(content.split("\n")[tail:])

    # Regex search
    output = []
    for line in content.split("\n"):
        if regex is None or re.search(regex, line):
            output.append(line)

    return "\n".join(output)
