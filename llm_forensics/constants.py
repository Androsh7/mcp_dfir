"""Defines constants"""

# Standard libraries
from pathlib import Path

# Directories
PARENT_DIRECTORY = Path(__file__).parent.parent
EVIDENCE_DIRECTORY = PARENT_DIRECTORY / "evidence"
ANALYSIS_DIRECTORY = PARENT_DIRECTORY / "analysis"
SYMBOLS_DIRECTORY = PARENT_DIRECTORY / "symbols"
ARTIFACTS_DIRECTORY = PARENT_DIRECTORY / "artifacts"
WINDOWS_SYMBOLS_DIRECTORY = SYMBOLS_DIRECTORY / "windows"

# Volatility symbols
WINDOWS_SYMBOL_SERVER = "https://msdl.microsoft.com/download/symbols"

# Analysis
COMMAND_LIST_PATH = ANALYSIS_DIRECTORY / "command_list.json"
NOTE_LIST_PATH = ANALYSIS_DIRECTORY / "analyst_note_list.json"

# Version
VERSION = "0.1.0"

# Docker
DOCKER_NAME = "forensics-docker"
DOCKER_IMAGE = f"{DOCKER_NAME}:{VERSION}"
DOCKER_VOLUME_MOUNTS = {
    "evidence": {"external_path": EVIDENCE_DIRECTORY, "internal_path": "/evidence", "permissions": "ro"},
    "analysis": {"external_path": ANALYSIS_DIRECTORY, "internal_path": "/analysis", "permissions": "ro"},
    "symbols": {"external_path": SYMBOLS_DIRECTORY, "internal_path": "/symbols", "permissions": "rw"},
    "artifacts": {"external_path": ARTIFACTS_DIRECTORY, "internal_path": "/artifacts", "permissions": "rw"},
}
