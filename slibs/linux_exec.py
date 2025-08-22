"""
██      ██ ██████  ██████   █████  ██████  ██ ███████ ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██      ██      
██      ██ ██████  ██████  ███████ ██████  ██ █████   ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██           ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██ ██ ███████ ███████ 
"""

import sys
import os
from pathlib import Path
import subprocess

"""
███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████ 
██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██      
█████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████ 
"""

def is_folder_exists(folder_path: str) -> bool:
    return Path(folder_path).is_dir()

def create_folder(folder_path: str):
    Path(folder_path).mkdir(exist_ok=True)

def execute_os_cmd(cmd: str) -> None:
    os.system(cmd)

    return

def execute_and_capture_os_cmd(cmd: list) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

# ======================================= #

def success_return() -> None:
    sys.exit(0)

def fail_return() -> None:
    sys.exit(1)