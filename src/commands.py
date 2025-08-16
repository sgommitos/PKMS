from datetime import datetime
from pathlib import Path

from slibs.os_discriminator import *

from slibs.timing     import wait_ms

from src.configurator import JSON_Configurator

from slibs.printl     import *

from slibs.debug_tools import not_implemented, not_fully_implemented

# --------------------------------- #
# ---- Discrimite which OS is ----- # 
# ------ running this script ------ #
# --------------------------------- #
        
class REPL_Commands:
    def __init__(self, configurator: JSON_Configurator):
        self.configurator = configurator

        # --------------------------------- #
        # --- Define classes attributes --- #
        # --------------------------------- #
        
        self.BASIC_CMD_DELAY_MS = 250

        self.commands_dict = {
            # --- General Commands --- #
            
            "help"         : [self.help,              "general_command", "Print a list of available cmd (within relative description)"],
            "about"        : [self.about,             "general_command", "Print SW info"],
            "depencencies" : [self.dependecies,       "general_command", "Print SW dependencies"],
            "clear"        : [self.clear,             "general_command", "Clear REPL terminal"],
            "exit"         : [self.quit,              "general_command", "Quit REPL"],
            "quit"         : [self.quit,              "general_command", "Quit REPL"],

            # --- Notes Commands --- #

            "ls"           : [self.ls,                "notes_cmd",       "List all your notes in setup pkm folder"],
            "daily"        : [self.daily,             "notes_cmd",       "Open (or create, if not exists) daily note"],
        }

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

    def exec_repl_cmd(self, cmd):
        cmd = cmd.lower().strip()
        
        if cmd in self.commands_dict:
            func, category, description = self.commands_dict[cmd]
            return func()
        else:
            self.unrecognized_cmd()
            return True

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
    def about(self) -> bool:
        print(f"- SW Version: {self.configurator.sw_version}")
        print("- Author: - sgommitos© (https://github.com/sgommitos)")

        return True

    def quit(self) -> None:
        print("\r\033[KBye by(t)e!")  # @NOTE: delete ^C from REPL output  
        wait_ms(self.BASIC_CMD_DELAY_MS)
        self.clear()
        
        success_return()

    def clear(self, is_logo=False) -> bool:
        execute_os_cmd("clear")
        
        if is_logo:
            self.print_logo()

        return True

    @not_fully_implemented()
    def help(self) -> bool:
        for cmd, (function, category, description) in self.commands_dict.items():
            print(f"{cmd:14} ⟹   {description}")

        return True

    @not_fully_implemented()
    def dependecies() -> bool:
        dependencies_str = f"""
        - ASCII-Art generation                           ⟹ https://patorjk.com/software/taag/
        - Moebius Triangle ASCII-Art (by Michael Naylor) ⟹ https://www.asciiart.eu/art-and-design/escher
        """

        print(dependencies_str)

        return True

    def unrecognized_cmd(self) -> bool:
        print(fg_text("Unrecognized cmd!", RED))

        return True

    # ==================================================== #

    def ls(self) -> bool:
        execute_os_cmd(f"ls {self.configurator.pkms_path} | grep '{self.configurator.note_format}'")
        
        return True
        
    def daily(self) -> bool:
        daily_note_filename = self._create_daily_note()
        
        if daily_note_filename:
            execute_os_cmd(f"{self.configurator.text_editor} {daily_note_filename}")

        return True  
    