"""File search mcp functions"""

# Standard libraries
import os
from typing import Literal

# Project libraries
from llm_forensics.constants import DOCKER_VOLUME_MOUNTS
from llm_forensics.tools.models import FileDetails


def list_files(path: Literal["evidence", "symbols"]) -> list[FileDetails]:
    if path not in list(DOCKER_VOLUME_MOUNTS.keys()):
        raise RuntimeError(f"Invalid path {path}, valid paths are {list(DOCKER_VOLUME_MOUNTS.keys())}")
    out_list = []
    for file_name in os.listdir(DOCKER_VOLUME_MOUNTS[path]["external_path"]):
        out_list.append(
            FileDetails(
                name=file_name,
                path=f"{DOCKER_VOLUME_MOUNTS[path]['internal_path']}/{file_name}",
                size=os.path.getsize(DOCKER_VOLUME_MOUNTS[path]["external_path"] / file_name),
            )
        )
    return out_list
