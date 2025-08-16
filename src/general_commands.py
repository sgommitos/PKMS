from datetime import datetime
from pathlib import Path

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
        
        self.BASIC_CMD_DELAY_MS = 250

    # ==================================================== #

    def _create_daily_note(self, daily_note_template_file="templates/daily_note_template.md"):
        # Generate timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d")
        
        # Create daily note filename
        daily_note_filename = f"{self.configurator.pkms_daily_path}{timestamp}{self.configurator.note_format}"

        # If file already exists, then just return the 'daily_note_filename' var (i.e: file path)
        if os.path.exists(daily_note_filename):
            print(fg_text("File already exists; just opening it", BLUE))
            wait_ms(self.BASIC_CMD_DELAY_MS)
            return daily_note_filename

        try:
            # Read template content
            with open(daily_note_template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Create new content with timestamp header
            new_content = f"# {timestamp}\n\n{template_content}"
            
            # Write to new file
            with open(daily_note_filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Created: {daily_note_filename}")
            wait_ms(self.BASIC_CMD_DELAY_MS)
            return daily_note_filename
            
        except FileNotFoundError:
            print(fg_text(f"Error: Template file '{daily_note_template_file}' not found!", RED))
            return None
        except Exception as e:
            print(fg_text(f"Error: {e}", RED))
            return None

    # ==================================================== #

    def print_logo(self) -> None:
        sw_splashscreen = f"""
██████╗ ██╗  ██╗███╗   ███╗███████╗
██╔══██╗██║ ██╔╝████╗ ████║██╔════╝
██████╔╝█████╔╝ ██╔████╔██║███████╗
██╔═══╝ ██╔═██╗ ██║╚██╔╝██║╚════██║
██║     ██║  ██╗██║ ╚═╝ ██║███████║
╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
"""
        print(fg_text(sw_splashscreen, BLUE))

        return

    def print_welcome(self) -> None:
        self.print_logo()
        print(fg_text(f"Welcome back, {self.configurator.user}!", BLUE))

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
        self.print_logo()

        return

    
    def help(self) -> None:
        help_str = f"""
        ===================== General Commands =====================
        - about        → print SW info
        - dependencies → print SW dependencies
        - quit         → quit SW
        - clear        → clear  terminal
        ======================= Notes Commands ======================
        - ls           → list all your notes in setup pkm folder
        - daily        → open (or create, if not exists) daily note
        =============================================================
        """

        print(help_str)

        return

    def dependecies() -> None:
        dependencies_str = f"""
        - ASCII-Art generation: https://patorjk.com/software/taag/
        """

        print(dependencies_str)

        return

    def unrecognized_cmd(self) -> None:
        print(fg_text("Unrecognized cmd!", RED))

        return

    # ==================================================== #

    def ls(self, notes_filter: str) -> None:
        if not notes_filter:
            execute_os_cmd(f"ls {self.configurator.pkms_path} | grep '{self.configurator.note_format}'")
            return
        
        else:
            notes_filter = notes_filter.split(" ")

            if "daily" in notes_filter:
                execute_os_cmd(f"ls {self.configurator.pkms_daily_path} | grep '{self.configurator.note_format}'")
                return
        
        
    
    def daily(self) -> None:
        daily_note_filename = self._create_daily_note()
        
        if daily_note_filename:
            execute_os_cmd(f"{self.configurator.text_editor} {daily_note_filename}")

        return   
    