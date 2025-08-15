import os

from slibs.timing     import wait_ms

from src.configurator import JSON_Configurator

from slibs.printl     import *

from slibs.debug_tools import not_implemented, not_fully_implemented

# --------------------------------- #
# ---- Discrimite which OS is ----- # 
# ------ running this script ------ #
# --------------------------------- #

import platform

match platform.system():
    case "Linux":
        from slibs.linux_exec   import * 
    case "Darwin":   
        from slibs.macos_exec   import *
    case "Windows":
        from slibs.windows_exec import *
    case _:          
        print(fg_text(f"OS NOT recognized ⟹ aborting SW execution"), RED)
        failed_return()
        
class GeneralCommands:

    def __init__(self, configurator: JSON_Configurator):
        self.configurator = configurator

        # --------------------------------- #
        # --- Define classes attributes --- #
        # --------------------------------- #
        
        self.BASIC_CMD_DELAY_MS = 200

    def print_welcome(self) -> None:
        sw_splashscreen = f"""
██████╗ ██╗  ██╗███╗   ███╗███████╗
██╔══██╗██║ ██╔╝████╗ ████║██╔════╝
██████╔╝█████╔╝ ██╔████╔██║███████╗
██╔═══╝ ██╔═██╗ ██║╚██╔╝██║╚════██║
██║     ██║  ██╗██║ ╚═╝ ██║███████║
╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝

Welcome back, {self.configurator.user}!
"""

        print(fg_text(sw_splashscreen, BLUE))

        return   

    @not_fully_implemented()
    def about(self) -> None:
        print(f"- SW Version: {self.configurator.sw_version}")
        print("- Author: - sgommitos© (https://github.com/sgommitos)")

    def quit(self) -> None:
        print("\r\033[KBye by(t)e!")  # @NOTE: delete ^C from REPL output  
        wait_ms(self.BASIC_CMD_DELAY_MS)
        self.clear()
        
        success_return()

    def clear(self) -> None:
        execute_os_cmd("clear")

    
    def help(self) -> None:
        help_str = f"""
        ==================== General Commands ====================
        - about        → print SW info
        - dependencies → print SW dependencies
        - quit         → quit SW
        - clear        → clear  terminal
        ===================== Notes Commands =====================
        - ls           → list all your notes in setup pkm folder
        ==========================================================
        """

        print(help_str)

        return

    def dependecies() -> None:
        dependencies_str = f"""
        - ASCII-Art generation: https://patorjk.com/software/taag/
        """

        print(dependencies_str)

        return

    # ==================================================== #

    def ls(self) -> None:
        print


    def unrecognized_cmd(self) -> None:
        print("Unrecognized cmd!")

        return