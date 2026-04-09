"""Defines constants"""

VERSION = "0.1.0"

# Volatility symbols
WINDOWS_SYMBOL_SERVER = "https://msdl.microsoft.com/download/symbols"
LINUX_SYMBOL_REPO_BASE_URL = "https://raw.githubusercontent.com/Abyss-W4tcher/volatility3-symbols/refs/heads/master"
LINUX_SYMBOL_MAP_SOURCE = f"{LINUX_SYMBOL_REPO_BASE_URL}/banners/banners_plain.json"

# Command output limit
COMMAND_MAX_OUTPUT_BYTES = 4 * 1024 * 1024 # 4 MB