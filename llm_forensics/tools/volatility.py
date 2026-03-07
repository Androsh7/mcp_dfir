"""Defines volatility tools"""

# Standard libraries
import re

# Third-party libraries
from mcp.server.fastmcp import Context

# Project libraries
from llm_forensics.server import mcp
from llm_forensics.docker_manager import docker_manager

@mcp.tool()
def run_volatility_command(ctx: Context, arguments: list[str]) -> str:
    """
    Run a Volatility 3 command against a memory image for forensic analysis.

    ## What is Volatility?
    Volatility is the industry-standard open-source memory forensics framework. It
    analyzes RAM dumps (memory images) captured from live systems. Because an attacker
    cannot easily hide from RAM the way they can hide from disk (rootkits, file deletion,
    encryption), memory analysis often reveals running processes, network connections,
    injected code, encryption keys, credentials, and malware that would otherwise be
    invisible.

    ## Command structure
    Arguments are passed exactly as you would type them after `vol` on the command line,
    split into a list — one token per element. Shell operators (|, >, <) are blocked.

    Typical form:
        ["-f", "<path/to/memory.img>", "<Plugin>", "<plugin-options>"]

    Example — list all running processes from a Windows image:
        ["-f", "/evidence/win10.mem", "windows.pslist.PsList"]

    ## Specifying the memory image (-f)
    Always pass `-f <image_path>` as the first two arguments unless you are only
    checking version/help. The image path must be accessible inside the Docker container
    that runs Volatility. Ask the user for the path if you do not know it.

    ## Plugin naming convention
    Volatility 3 plugins follow the pattern:  <OS>.<module>.<ClassName>
      - `windows.*`  — Windows memory images
      - `linux.*`    — Linux memory images
      - `mac.*`      — macOS memory images

    You can omit the class name suffix and Volatility will resolve it automatically,
    e.g. `windows.pslist` works the same as `windows.pslist.PsList`.

    ## Essential Windows plugins (most common investigations)

    ### Process analysis
    - `windows.pslist`        — List all processes (PID, PPID, name, start time)
    - `windows.pstree`        — Same data as pslist displayed as a parent/child tree
    - `windows.psscan`        — Scan pool tags to find processes hidden from pslist (rootkit detection)
    - `windows.cmdline`       — Command-line arguments for each process
    - `windows.dlllist`       — DLLs loaded by each process (use --pid to filter)
    - `windows.handles`       — Open handles (files, registry keys, mutexes) per process
    - `windows.dumpfiles`     — Extract files from memory (use --physaddr or --virtaddr)
    - `windows.malfind`       — Find memory regions with RWX permissions and MZ/PE headers — high-signal indicator of injected shellcode or packed malware

    ### Network
    - `windows.netstat`       — Active/recently closed TCP/UDP connections with owning PID
    - `windows.netscan`       — Pool-tag scan for network structures, finds more connections than netstat

    ### Registry
    - `windows.registry.hivelist`   — List loaded registry hives and their virtual addresses
    - `windows.registry.printkey`   — Print keys/values from a hive (use --key to specify path)
    - `windows.registry.userassist` — Decode UserAssist entries (recently executed programs)

    ### Drivers and kernel
    - `windows.modules`       — Loaded kernel modules (drivers)
    - `windows.driverscan`    — Scan for driver objects, finds hidden drivers
    - `windows.ssdt`          — System Service Descriptor Table — detect SSDT hooks (rootkits)
    - `windows.callbacks`     — Kernel notification callbacks registered by drivers

    ### Malware / credential hunting
    - `windows.malfind`       — (see above) primary malware injection detector
    - `windows.vadinfo`       — Virtual Address Descriptor tree — full memory map of a process
    - `windows.hashdump`      — Dump NTLM password hashes from the SAM hive
    - `windows.lsadump`       — Extract LSA secrets from registry
    - `windows.cachedump`     — Cached domain credentials

    ### File system artifacts
    - `windows.filescan`      — Scan for FILE_OBJECT structures (recovers paths of open files)
    - `windows.mftscan.MFTScan` — Scan for MFT entries (NTFS file records in memory)

    ## Essential Linux plugins
    - `linux.pslist`          — List processes
    - `linux.psscan`          — Scan for hidden processes
    - `linux.bash`            — Recover bash history from memory
    - `linux.netstat`         — Network connections
    - `linux.lsmod`           — Loaded kernel modules
    - `linux.check_syscall`   — Detect syscall table hooks

    ## Common flags
    - `--pid <PID>`           — Filter output to a specific process ID
    - `--name <pattern>`      — Filter by process name
    - `--dump`                — Write extracted artifacts to disk (combined with dumpfiles, etc.)
    - `-o <output_dir>`       — Directory to write dumped files
    - `--output csv`          — Machine-readable CSV output

    ## Useful utility commands
    - `["-h"]`                            — Print help and version
    - `["-f", "image", "-h"]`             — List all available plugins for that image's OS
    - `["isfinfo"]`                       — Show available Intermediate Symbol Format files

    ## Typical investigative workflow
    1. Identify the OS: run `windows.info` (or `linux.info`) to confirm image type and build.
    2. Enumerate processes: `windows.pslist` then `windows.psscan` — compare for hidden entries.
    3. Check network: `windows.netscan` to find suspicious outbound connections and their owning PID.
    4. Inspect suspicious process: `windows.cmdline --pid <X>`, `windows.dlllist --pid <X>`, `windows.malfind --pid <X>`.
    5. Extract artifacts: `windows.dumpfiles` to carve out injected DLLs or suspicious executables.
    6. Check persistence: `windows.registry.printkey` on Run/RunOnce keys, `windows.hashdump` for credentials.
    """
    if re.search(r'(\||>|<)', "".join(arguments)):
        raise RuntimeError('Invalid character in argument, no ">", "<", or "|" characters are allowed')
    return docker_manager.exec_stream(command_list=['vol', *arguments], ctx=ctx)
