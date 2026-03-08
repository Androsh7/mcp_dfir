"""Defines volatility tools"""

# Standard libraries
import lzma
from http import HTTPStatus

# Third-party libraries
import requests
from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.constants import WINDOWS_SYMBOL_SERVER, WINDOWS_SYMBOLS_DIRECTORY
from llm_forensics.data_manager import CommandRecord, CommandRecordTruncated
from llm_forensics.docker_manager import docker_manager


def run_volatility_command(ctx: Context, arguments: list[str]) -> CommandRecordTruncated:
    """Runs volatility3: vol -s /symbols -r jsonl <arguments>

    - To analyze a file you must specify the path using `-f /evidence/example.mem`
    - Volatility3 does not come with many built-in symbols so they may need to be manually downloaded
    """
    return docker_manager.exec_stream(command_list=["vol", "-s", "/symbols", "-r", "jsonl", *arguments], ctx=ctx)


def _run_volatility_pdbconv_command(ctx: Context, arguments: list[str]) -> CommandRecord:
    return docker_manager.exec_stream(command_list=["pdbconv", *arguments], ctx=ctx)


def _download_windows_pdb(ctx: Context, pdb_name: str, guid: str, age: int) -> str:
    """Downloads a pdb file and returns the internal path"""
    guid = guid.replace("-", "")  # Normalize path
    url = f"{WINDOWS_SYMBOL_SERVER}/{pdb_name}/{guid}{age}/{pdb_name}"
    ctx.report_progress(f"Pulling symbol from {url}")
    output_file_name = f'{guid}_{pdb_name}' 
    external_path = WINDOWS_SYMBOLS_DIRECTORY / "raw" / output_file_name
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
) -> CommandRecordTruncated:
    """Downloads windows symbols for volatility to `/symbols`"""
    
    # Set correct naming convention and directory tree for volatility parsing
    output_file_name = f'{guid}-{age}.json.xz'
    output_file_external_path = WINDOWS_SYMBOLS_DIRECTORY / pdb_name / output_file_name
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
