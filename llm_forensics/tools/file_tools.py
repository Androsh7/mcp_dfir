"""Defines file tools"""

# Standard libraries
from pathlib import Path
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.config import config
from llm_forensics.docker_manager import docker_manager
from llm_forensics.tools.models import CommandRecordSummary, FileDetails

def unzip_file(ctx: Context, source_file: str, destination_dir: str) -> CommandRecordSummary:
    """Runs: unzip -X -K <SOURCE_FILE> -d /artifacts/<DESTINATION_FILE_NAME>"""
    if source_file.find("..") != -1 or destination_dir.find("..") != -1:
        raise RuntimeError("Invalid file path, Path traversal is not allowed")
    if not Path(source_file).is_file():
        raise FileNotFoundError("Source file not found")
    if not destination_dir.startswith("/artifacts/"):
        raise RuntimeError("Destination directory must be in /artifacts")
    return docker_manager.exec_stream(ctx=ctx, command_list=["unzip", "-X", "-K", source_file, "-d", destination_dir])

TAR_COMPRESSION_FLAGS = {
    "gz": "--gzip",
    "bz2": "--bzip2",
    "xz": "--xz",
    "lzip": "--lzip",
    "lzma": "--lzma",
    "lzop": "--lzop",
    "zstd": "--zstd",
}

def untar_file(ctx: Context, source_file: str, destination_dir: str, compression: None | Literal["gz", "bz2", "xz", "lzip", "lzma", "lzop", "zstd"] = None) -> CommandRecordSummary:
    """Runs: tar -xf <SOURCE_FILE> -C /artifacts/<DESTINATION_FILE_NAME>"""
    if source_file.find("..") != -1 or destination_dir.find("..") != -1:
        raise RuntimeError("Invalid file path, Path traversal is not allowed")
    if not Path(source_file).is_file():
        raise FileNotFoundError("Source file not found")
    if not destination_dir.startswith("/artifacts/"):
        raise RuntimeError("Destination directory must be in /artifacts")
    if compression is None:
        return docker_manager.exec_stream(ctx=ctx, command_list=["tar", "-xf", source_file, "-C", destination_dir])
    if compression in TAR_COMPRESSION_FLAGS:
        return docker_manager.exec_stream(ctx=ctx, command_list=["tar", "-x", TAR_COMPRESSION_FLAGS[compression], source_file, "-C", destination_dir])
    else:
        raise ValueError(f"Unsupported compression type, {compression} is not supported")
