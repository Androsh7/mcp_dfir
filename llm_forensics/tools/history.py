"""Defines the records mcp routes"""

# Standard libraries
import re

# Third-party libraries
from llm_forensics.data_manager import CommandRecord, CommandRecordTruncated, data_manager


def get_command_history(truncate: int | None = 50) -> list[CommandRecordTruncated]:
    out_list = []
    for record in data_manager.command_list:
        out_list.append(record.truncate(truncate))
    return out_list


def get_command_result(command: str, head: int | None, tail: int | None, regex: str | None) -> str:
    if head and tail:
        raise RuntimeError("Cannot set tail and head at the same time")

    # Get the command result
    content = ""
    for command_record in data_manager.command_list:
        if command_record.command == command:
            content = command_record.result
            break
    if len(content) == 0:
        raise RuntimeError(f"Cannot find command: {command} in history")

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
