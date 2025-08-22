import os
import subprocess

from slibs.printl import fg_text, RED
from slibs.os_discriminator import *

def check_used_terminal_image_support() -> object | None:
    """
    @BRIEF: check if used terminal supports img print
    """

    term = os.environ.get('TERM', '').lower()
    
    # Plan A ⟹ check in pre-defined supported terminal dict (i.e: 'img_supported_terminals')
    if term in img_supported_terminals.keys():
        terminal_class = img_supported_terminals[term]
        if terminal_class is not None:
            return terminal_class()
        return None
    
    # Plan B ⟹ just cry :c
    return None

class KittyTerminal:
    def __init__(self): pass

    def print_image(self, img_path: str) -> None:
        """
        @BRIEF: Print image using Kitty Protocol
        """
        try:
            subprocess.run(['kitty', '+kitten', 'icat', img_path], check=True)
        except Exception as e:
            print(fg_text(f"ERROR: can't print image ⟹ {e}", RED))

        return

# ================================================================================================ #

img_supported_terminals = {
    'xterm-kitty': KittyTerminal,
    'iterm2'     : None,
    'wezterm'    : None,
    'alacritty'  : None
}