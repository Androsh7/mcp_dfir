"""Defines volatility tools"""

# Standard libraries
import json
import lzma
import re
from http import HTTPStatus

# Third-party libraries
import requests
from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field

# Project libraries
from mcp_dfir.config import config
from mcp_dfir.constants import LINUX_SYMBOL_MAP_SOURCE, LINUX_SYMBOL_REPO_BASE_URL, WINDOWS_SYMBOL_SERVER
from mcp_dfir.docker_manager import docker_manager
from mcp_dfir.tools.models import CommandRecordSummary


def run_volatility_command(ctx: Context, arguments: list[str]) -> CommandRecordSummary:
    """Runs volatility3: vol -s /symbols -r jsonl <arguments>

    - To analyze a file you must specify the path using `-f /evidence/example.mem`
    - Volatility3 does not come with many built-in symbols so they may need to be manually downloaded
    """
    return docker_manager.exec_stream(command_list=["vol", "-s", "/symbols", "-r", "jsonl", *arguments], ctx=ctx)


def _run_volatility_pdbconv_command(ctx: Context, arguments: list[str]) -> CommandRecordSummary:
    return docker_manager.exec_stream(command_list=["pdbconv", *arguments], ctx=ctx)


def _download_windows_pdb(ctx: Context, pdb_name: str, guid: str, age: int) -> str:
    """Downloads a pdb file and returns the internal path"""
    guid = guid.replace("-", "")  # Normalize path
    url = f"{WINDOWS_SYMBOL_SERVER}/{pdb_name}/{guid}{age}/{pdb_name}"
    ctx.report_progress(f"Pulling symbol from {url}")
    output_file_name = f"{guid}_{pdb_name}"
    external_path = config.windows_symbols_directory / "raw" / output_file_name
    external_path.parent.mkdir(mode=500, parents=True, exist_ok=True)
    internal_path = f"/symbols/windows/raw/{output_file_name}"

    response = requests.get(url)

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise RuntimeError(
            f"PDB not found on symbol server. Check that pdb_name and guid are correct.\nURL attempted: {url}"
        )

    response.raise_for_status()
    external_path.write_bytes(response.content)

    ctx.report_progress(f"Saved pdb file to {internal_path}")

    return internal_path


def download_windows_symbol(
    ctx: Context, pdb_name: str, guid: str, age: int, overwrite: bool = False
) -> CommandRecordSummary:
    """Downloads windows symbols for volatility to `/symbols`"""

    # Set correct naming convention and directory tree for volatility parsing
    output_file_name = f"{guid}-{age}.json.xz"
    output_file_external_path = config.windows_symbols_directory / pdb_name / output_file_name
    output_file_internal_path = f"/symbols/windows/{pdb_name}/{output_file_name}"
    if output_file_external_path.exists() and not overwrite:
        raise RuntimeError(
            f"File {output_file_internal_path} already exists, it can be used by volatility with the `-s /symbols` "
            "argument, set overwrite to True to overwrite this file"
        )
    else:
        output_file_external_path.parent.mkdir(mode=500, parents=True, exist_ok=True)

    # Download pdb
    internal_path = _download_windows_pdb(ctx=ctx, pdb_name=pdb_name, guid=guid, age=age)

    # Run conversion to symbol file
    pdbconv_output = _run_volatility_pdbconv_command(
        ctx=ctx,
        arguments=["-f", internal_path, "-g", guid, "-o", output_file_internal_path],
    )

    # Change "unknown.pdb" to correct pdb name
    data = lzma.decompress(output_file_external_path.read_bytes())
    data = data.replace(b"unknown.pdb", pdb_name.encode("utf-8"))
    output_file_external_path.write_bytes(lzma.compress(data))

    return pdbconv_output


class SymbolSearchResult(BaseModel):
    symbol_name: str = Field(
        examples=[
            "Linux version 5.15.0-1065-oracle (buildd@lcy02-amd64-029) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #71~20.04.1-Ubuntu SMP Mon Jul 29 16:34:02 UTC 2024 (Ubuntu 5.15.0-1065.71~20.04.1-oracle 5.15.160)"
        ]
    )
    file_path_list: list[str] = Field(
        examples=[["Ubuntu/amd64/5.15.0/1065/oracle/Ubuntu_5.15.0-1065-oracle_5.15.0-1065.71~20.04.1_amd64.json.xz"]]
    )


def search_linux_symbols(ctx: Context, regex: str) -> list[SymbolSearchResult]:
    """Load linux symbol map from Abyss-W4tcher/volatility3-symbols and search for symbols matching the regex"""

    # Download symbol map if it doesn't exist
    if not config.linux_symbol_map_json.exists():
        ctx.report_progress("Downloading linux symbol map from github.com/Abyss-W4tcher/volatility3-symbols")
        response = requests.get(url=LINUX_SYMBOL_MAP_SOURCE)
        response.raise_for_status()
        config.linux_symbols_directory.mkdir(mode=500, parents=True, exist_ok=True)
        config.linux_symbol_map_json.write_bytes(response.content)

    # Parse the symbol map
    with open(config.linux_symbol_map_json, encoding="utf-8") as symbol_map_file:
        symbol_map: dict = json.load(symbol_map_file)

    # Return the a list of matches
    out_list = []
    for symbol_name, file_path_list in symbol_map.items():
        if re.search(regex, symbol_name):
            out_list.append(SymbolSearchResult(symbol_name=symbol_name, file_path_list=file_path_list))

    return out_list


def download_linux_symbol(ctx: Context, symbol_path: str) -> str:
    """Download a symbol map from the Abyss-W4tcher/volatility3-symbols repository"""

    # Download json file from repo
    url = f"{LINUX_SYMBOL_REPO_BASE_URL}/{symbol_path}"
    ctx.report_progress(f"Downloading symbol from {url}")
    response = requests.get(url=url)
    response.raise_for_status()

    # Save json file
    config.linux_symbols_directory.mkdir(mode=500, parents=True, exist_ok=True)
    file_name = symbol_path.rsplit("/", maxsplit=1)[-1]
    file_path = config.linux_symbols_directory / file_name
    file_path.write_bytes(response.content)

    return f"Successfully downloaded symbol file {file_name} ({file_path.stat().st_size} bytes) from {url}"
