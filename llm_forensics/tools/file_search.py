"""File search mcp functions"""

# Standard libraries
from pathlib import Path
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.constants import DOCKER_VOLUME_MOUNTS
from llm_forensics.docker_manager import docker_manager
from llm_forensics.tools.models import CommandRecordTruncated, FileDetails


def list_files(path: Literal[*list(DOCKER_VOLUME_MOUNTS.keys())]) -> list[FileDetails]:
    if path not in list(DOCKER_VOLUME_MOUNTS.keys()):
        raise RuntimeError(f"Invalid path {path}, valid paths are {list(DOCKER_VOLUME_MOUNTS.keys())}")
    out_list = []
    for dir_path, _, file_name_list in DOCKER_VOLUME_MOUNTS[path]["external_path"].walk():
        for file_name in file_name_list:
            external_file_path = Path(dir_path / file_name)
            internal_file_path = f"/{path}/{str(external_file_path.relative_to(DOCKER_VOLUME_MOUNTS[path]['external_path'])).replace('\\', '/')}"
            out_list.append(
                FileDetails(
                    name=file_name,
                    path=internal_file_path,
                    size=external_file_path.stat().st_size,
                )
            )
    return out_list


def run_strings(ctx: Context, arguments: list[str]) -> CommandRecordTruncated:
    """Runs: strings <arguments>"""
    return docker_manager.exec_stream(ctx=ctx, command_list=["strings", *arguments])


def run_grep(ctx: Context, arguments: list[str]) -> CommandRecordTruncated:
    """Runs: grep <arguments>"""
    return docker_manager.exec_stream(ctx=ctx, command_list=["grep", *arguments])


def run_find(ctx: Context, arguments: list[str]) -> CommandRecordTruncated:
    """Runs: find <arguments>"""
    if " ".join(arguments).find("-exec") != -1:
        raise RuntimeError("Cannot run exec in find")
    return docker_manager.exec_stream(ctx=ctx, command_list=["find", *arguments])
