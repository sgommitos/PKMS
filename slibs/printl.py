"""
██      ██ ██████  ██████   █████  ██████  ██ ███████ ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██      ██      
██      ██ ██████  ██████  ███████ ██████  ██ █████   ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██           ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██ ██ ███████ ███████ 
"""

import re

from slibs.timing import compute_timestamp

"""
██████   █████  ████████  █████  
██   ██ ██   ██    ██    ██   ██ 
██   ██ ███████    ██    ███████ 
██   ██ ██   ██    ██    ██   ██ 
██████  ██   ██    ██    ██   ██ 
"""

# =========================== #
# ╔═╗╔╗╔╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗╔═╗ #
# ╠═╣║║║╚═╗║  ║  ╠═╣╠═╣╠╦╝╚═╗ #
# ╩ ╩╝╚╝╚═╝╩  ╚═╝╩ ╩╩ ╩╩╚═╚═╝ # 
# =========================== #

RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

# ====================================================== #

def fg_text(raw_text: str, color: str) -> str:
    return f"{color}{raw_text}{RESET}"

def bg_text(raw_text: str, color: str) -> str:
    return f"{re.sub(r'(\d+)', lambda m: str(int(m.group()) + 10), color)}{raw_text}{RESET}"

def bold_text(raw_text: str) -> str:
    return f"{BOLD}{raw_text}{RESET}"

def italic_text(raw_text: str) -> str:
    return f"{ITALIC}{raw_text}{RESET}"

def underlined_text(raw_text: str) -> str:
    return f"{UNDERLINE}{raw_text}{RESET}"

# ====================================================== #

def nl(nl_num: int = 1) -> None:
    print("", end = ( "\n" * max(0, nl_num)) )

    return

def log(message) -> None:
    print(f"{{{compute_timestamp()}}} [{fg_text("LOG", BLUE)}] {fg_text({message}, BLUE)}")

    return