# MCP DFIR

MCP DFIR (Digital Forensics Incident Response) is an MCP server that gives AI agents the tools to perform memory, disk, and artifact forensics. It runs forensics tools inside an isolated Docker container and exposes them over the MCP stdio transport.

# Features

- Memory forensics via [Volatility3](https://github.com/volatilityfoundation/volatility3)
- Disk forensics via [The Sleuth Kit](https://www.sleuthkit.org/)
- File search with `strings`, `grep`, and `find`
- Automatic Windows symbol downloading and conversion
- Persistent command history — the agent never re-runs commands already completed
- Analyst notes — the agent records findings in structured markdown notes

# Requirements

- [Docker](https://www.docker.com/) must be installed and running

# Setup

## Claude Desktop config

Add the following to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "llm-forensics": {
      "command": "python3",
      "args": ["-m", "llm_forensics", "--case-dir", "/path/to/your/case"]
    }
  }
}
```

Replace `/path/to/your/case` with the directory containing your evidence files (see [Case Directory Layout](#case-directory-layout) below).

## Case directory layout

The MCP server expects evidence and artifacts to be organized under a case directory:

```
my_case/
├── evidence/    # Place memory dumps, disk images, etc. here (read-only)
├── artifacts/   # Output location for extracted files (read-write)
├── symbols/     # Volatility symbol files (auto-populated on download)
└── analysis/    # Command history and analyst notes (auto-generated)
```

Place all evidence files (`.mem`, `.img`, `.e01`, etc.) inside the `evidence/` directory before starting a session.

# Args

```
usage: llm_forensics [-h] [--version] [-d CASE_DIR]

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --case-dir CASE_DIR
                        Working directory for the case, default: current directory
```

# MCP Tools

| Tool                         | Description                                                |
| ---------------------------- | ---------------------------------------------------------- |
| `run_volatility_command`     | Runs Volatility3 (`vol`) for memory forensics              |
| `download_windows_symbol`    | Downloads and converts Windows PDB symbols for Volatility3 |
| `run_sleuthkit_command`      | Runs any Sleuth Kit tool for disk forensics                |
| `run_strings`                | Runs `strings` on a file                                   |
| `run_grep`                   | Runs `grep` on files                                       |
| `run_find`                   | Runs `find` to search for files                            |
| `list_files`                 | Lists files in `evidence`, `artifacts`, or `symbols`       |
| `get_hash`                   | Computes a hash of a file                                  |
| `get_command_history`        | Returns all previously run commands                        |
| `get_command_result`         | Returns the output of a specific past command              |
| `show_analyst_notes_summary` | Lists all analyst notes                                    |
| `show_analyst_note`          | Retrieves the content of a specific analyst note           |
| `add_analyst_note`           | Creates a new analyst note                                 |
| `update_analyst_note`        | Updates an existing analyst note                           |

# Build from source

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate
# Activate (Windows)
.venv/Scripts/activate.ps1

# Install dependencies
pip install .[dev]

# Run
python3 -m llm_forensics --case-dir /path/to/your/case
```
