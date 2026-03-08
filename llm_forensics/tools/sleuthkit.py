"""Run sleuthkit commands"""

# Standard libraries
from typing import Literal

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.docker_manager import docker_manager
from llm_forensics.tools.models import CommandRecordTruncated

SLEUTHKIT_COMMANDS = [
    "blkcalc",
    "blkcat",
    "blkls",
    "blkstat",
    "fcat",
    "ffind",
    "fiwalk",
    "fls",
    "fsstat",
    "hfind",
    "icat",
    "ifind",
    "ils",
    "img_cat",
    "img_stat",
    "istat",
    "jcat",
    "jls",
    "jpeg_extract",
    "mactime",
    "mmcat",
    "mmls",
    "mmstat",
    "sigfind",
    "sorter",
    "srch_strings",
    "tsk_comparedir",
    "tsk_gettimes",
    "tsk_loaddb",
    "tsk_recover",
]


def run_sleuthkit_command(
    ctx: Context, tool: Literal[*SLEUTHKIT_COMMANDS], arguments: list[str]
) -> CommandRecordTruncated:
    """Run sleuthkit commands for disk forensics: <tool> <arguments>

    blkcalc - Converts between unallocated disk unit numbers and regular disk unit numbers.
    blkcat - Display the contents of file system data unit in a disk image.
    blkls - List or output file system data units.
    blkstat - Display details of a file system data unit (i.e. block or sector).
    fcat - Output the contents of a file based on its name.
    ffind - Finds the name of the file or directory using a given inode.
    fiwalk - print the filesystem statistics and exit.
    fls - List file and directory names in a disk image.
    fsstat - Display general details of a file system.
    hfind - Lookup a hash value in a hash database.
    icat - Output the contents of a file based on its inode number.
    ifind - Find the meta-data structure that has allocated a given disk unit or file name.
    ils - List inode information.
    img_cat - Output contents of an image file.
    img_stat - Display details of an image file.
    istat - Display details of a meta-data structure (i.e. inode).
    jcat - Show the contents of a block in the file system journal.
    jls - List the contents of a file system journal.
    jpeg_extract - jpeg extractor.
    mactime - Create an ASCII time line of file activity.
    mmcat - Output the contents of a partition to stdout.
    mmls - Display the partition layout of a volume system (partition tables).
    mmstat - Display details about the volume system (partition tables).
    sigfind - Find a binary signature in a file.
    sorter - Sort files in an image into categories based on file type.
    srch_strings - Display printable strings in files.
    tsk_comparedir - compare the contents of a directory with the contents of an image or local device.
    tsk_gettimes - Collect MAC times from a disk image into a body file.
    tsk_loaddb - populate a SQLite database with metadata from a disk image.
    tsk_recover - Export files from an image into a local directory.
    """
    if tool not in SLEUTHKIT_COMMANDS:
        raise KeyError(f"Tool: {tool} not found in command list: {', '.join(list(SLEUTHKIT_COMMANDS.keys()))}")
    return docker_manager.exec_stream(ctx=ctx, command_list=[tool, *arguments])
