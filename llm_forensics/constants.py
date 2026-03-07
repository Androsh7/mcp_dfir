"""Defines constants"""

# Standard libraries
import os
from pathlib import Path

# Directories
PARENT_DIRECTORY = Path(__file__).parent.parent
EVIDENCE_DIRECTORY = PARENT_DIRECTORY / "evidence"
os.makedirs(EVIDENCE_DIRECTORY, mode=500, exist_ok=True)
ANALYSIS_DIRECTORY = PARENT_DIRECTORY / "analysis"
os.makedirs(ANALYSIS_DIRECTORY, mode=500, exist_ok=True)

# Version
VERSION = "0.1.0"

# Docker
DOCKER_NAME = "forensics-docker"
DOCKER_IMAGE = f'{DOCKER_NAME}:{VERSION}'