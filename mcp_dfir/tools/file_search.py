"""File search mcp functions"""

# Standard libraries
from pathlib import Path
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from mcp_dfir.config import config
from mcp_dfir.docker_manager import docker_manager
from mcp_dfir.tools.models import CommandRecordSummary, FileDetails


def list_files(path: Literal["artifacts", "symbols", "evidence"]) -> list[FileDetails]:
    valid_paths = [volume.name for volume in config.docker_volumes]

    # Select volume
    selected_volume = None
    for volume in config.docker_volumes:
        if volume.name == path:
            selected_volume = volume
            break
    if selected_volume is None:
        raise RuntimeError(f"Invalid path {path}, valid paths are {valid_paths}")

    out_list = []
    for dir_path, _, file_name_list in selected_volume.external_path.walk():
        for file_name in file_name_list:
            external_file_path = Path(dir_path / file_name)
            internal_file_path = (
                f"/{path}/{str(external_file_path.relative_to(selected_volume.external_path)).replace('\\', '/')}"
            )
            out_list.append(
                FileDetails(
                    name=file_name,
                    path=internal_file_path,
                    size=external_file_path.stat().st_size,
                )
            )
    return out_list


def run_strings(ctx: Context, arguments: list[str]) -> CommandRecordSummary:
    """Runs: strings <arguments>"""
    return docker_manager.exec_stream(ctx=ctx, command_list=["strings", *arguments])


def run_grep(ctx: Context, arguments: list[str]) -> CommandRecordSummary:
    """Runs: grep <arguments>"""
    return docker_manager.exec_stream(ctx=ctx, command_list=["grep", *arguments])


def run_find(ctx: Context, arguments: list[str]) -> CommandRecordSummary:
    """Runs: find <arguments>"""
    if " ".join(arguments).find("-exec") != -1:
        raise RuntimeError("Cannot run exec in find")
    return docker_manager.exec_stream(ctx=ctx, command_list=["find", *arguments])
