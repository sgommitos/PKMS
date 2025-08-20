# --- REPL: Autocomplete, History and KeyBindings dependencies --- #
from prompt_toolkit             import prompt
from prompt_toolkit.completion  import WordCompleter
from prompt_toolkit.history     import FileHistory
from prompt_toolkit.key_binding import KeyBindings
import os
# ------------------------------------------------- #

from slibs.os_discriminator     import *
from slibs.timing               import compute_date, wait_ms
from slibs.printl               import fg_text, RED, GREEN, BLUE
from slibs.debug_tools          import not_implemented, not_fully_implemented

from src.configurator           import Configurator

class REPL_Commands:
    
    """
    ░█▀▀░█░█░░░▀█▀░█▀█░▀█▀░▀█▀
    ░▀▀█░█▄█░░░░█░░█░█░░█░░░█░
    ░▀▀▀░▀░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░
    """

    """
    ┏┓ ┏━╸
    ┣┻┓┣╸ 
    ┗━┛┗━╸
    """
    
    def __init__(self, configurator: Configurator):
        self.configurator = configurator

        # --- Define classes attributes --- #

        self.REPL_prompt_keyword = "\nPKMS> "  
        self.BASIC_CMD_DELAY_MS  = 250

        self.commands_dict = {
            # --- General Commands --- #
            
            "help"         : [self.help,              "general_cmd", "Print a list of available cmd (within relative description)"],
            "about"        : [self.about,             "general_cmd", "Print SW info"],
            "credits"      : [self.credits,           "general_cmd", "Print SW credits"],
            "clear"        : [self.clear,             "general_cmd", "Clear REPL terminal"],
            "exit"         : [self.quit,              "general_cmd", "Quit REPL"],
            "quit"         : [self.quit,              "general_cmd", "Quit REPL"],
            "reload"       : [self.reload,            "general_cmd", "Reload SW configuration files"],

            # --- Notes Commands --- #

            "ls"           : [self.ls,                "notes_cmd",       "List all your notes in setup pkm folder"],
            "random"       : [self.random,            "notes_cmd",       "Read a random note from your pkms folder"],
            "daily"        : [self.daily,             "notes_cmd",       "Open (or create, if not exists) daily note"],
        }

        self.general_commands_list = []
        self.notes_commands_list   = []

        self._populate_commands_lists()

        self.user_shortcuts        = {}
        self._populate_user_shortcuts_dict()
        self._setup_keybindigs() 

        self.completer = WordCompleter(list(self.commands_dict.keys()))
        self.history   = FileHistory(configurator.cli_history)

    def _populate_commands_lists(self) -> None:
        for cmd, (function, category, description) in self.commands_dict.items():
            match category:
                case "general_cmd" : self.general_commands_list.append([cmd, description]) 
                case "notes_cmd"   : self.notes_commands_list.append([cmd, description])
                case _             : continue

        return

    def _populate_user_shortcuts_dict(self) -> None:
        
        # Create some temporany structures to perform easily some comparison between our 2 involved dicts
        user_config_file_cmds_list = set(self.configurator.user_shortcuts_bindings.keys())
        sw_implemented_cmds_list   = set(self.commands_dict.keys()) 

        binded_cmds_list           = user_config_file_cmds_list & sw_implemented_cmds_list
        unbinded_cmds_list         = sw_implemented_cmds_list   - user_config_file_cmds_list  
        unavailable_cmds_list      = user_config_file_cmds_list - sw_implemented_cmds_list

        # WITHOUT BLOCKING SW EXECUTION, inform user if some cmds he binded it's not unavailable
        if unavailable_cmds_list:
            for cmd in unavailable_cmds_list:
                print(fg_text(f"ERROR: User cmd {cmd:10} (within its shortcut) it's not unavailable", RED))
            
            print()
        
        # Populate 'self.user_shortcuts' dict
        for cmd in binded_cmds_list:
            self.user_shortcuts.update({cmd : self.configurator.user_shortcuts_bindings[cmd]})
        for cmd in unbinded_cmds_list:
            self.user_shortcuts.update({cmd : ""})

        return 

    def _setup_keybindigs(self) -> None:
        # Initialize KeyBindings registry
        self.bindings = KeyBindings()

        # Create bindings dinamically
        for cmd, shortcut in self.user_shortcuts.items():
            if shortcut != '':
                """
                @NOTE: store for each cycle function pointer in order to avoid its 
                       overwriting(s) ⟹ preventing 'late binding closure' bug
                """
                cmd_function = self.commands_dict[cmd][0] 
            
                self.bindings.add(shortcut.strip())(
                    lambda event, function=cmd_function: ( function(), print(self.REPL_prompt_keyword, end="") )
                )

        return

    """
    ┏━╸┏┳┓╺┳┓┏━┓
    ┃  ┃┃┃ ┃┃┗━┓
    ┗━╸╹ ╹╺┻┛┗━┛
    """

    def get_user_input(self) -> str:
        """
        @brief: get user input, using autocomplete and history features
        """
        return prompt(
            self.REPL_prompt_keyword,
            key_bindings=self.bindings,
            completer=self.completer,
            history=self.history
        )

    def exec_repl_cmd(self, cmd: str):
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
██████╔╝█████╔╝ ██╔████╔██║███████╗   SW version ⇲
██╔═══╝ ██╔═██╗ ██║╚██╔╝██║╚════██║   {self.configurator.sw_version}
██║     ██║  ██╗██║ ╚═╝ ██║███████║
╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ 
"""     
        
        print(fg_text(sw_splashscreen, BLUE))

        return

    def print_welcome(self) -> None:
        self.print_logo()
        print(fg_text(f"Welcome back, {self.configurator.user}!", BLUE))

        return 

    def unrecognized_cmd(self) -> bool:
        print(fg_text("Unrecognized cmd!", RED))

        return True  

    """
    ░█▀▀░█▀▀░█▀█░█▀▀░█▀▄░█▀█░█░░░░░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀
    ░█░█░█▀▀░█░█░█▀▀░█▀▄░█▀█░█░░░░░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█
    ░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
    """

    """
    ┏┓ ┏━╸
    ┣┻┓┣╸ 
    ┗━┛┗━╸
    """

    # Nothing here

    """
    ┏━╸┏┳┓╺┳┓┏━┓
    ┃  ┃┃┃ ┃┃┗━┓
    ┗━╸╹ ╹╺┻┛┗━┛
    """
    
    def reload(self) -> bool:
        if (self.configurator._load_configs()):
            self.clear(is_logo=False)

            while input(fg_text("PKMS successfully reloaded! Press Return to restart REPL: ", GREEN)) is None: pass
            
            self.clear(is_logo=False)
            self.print_welcome()
            
            return True
        
        print(fg_text("Error during SW reload! Please check user configuration files", RED))
        return False

    @not_fully_implemented()
    def about(self) -> bool:
        about_str = f"""
⦁ SW Version: {self.configurator.sw_version}
⦁ Author: - sgommitos© (https://github.com/sgommitos)
"""
        
        print(about_str)

        return True

    def quit(self) -> None:
        print("\r\033[KBye by(t)e!")  # @NOTE: delete ^C from REPL output  
        wait_ms(self.BASIC_CMD_DELAY_MS)
        self.clear(is_logo=False)
        
        success_return()

    def clear(self, is_logo=True) -> bool:
        execute_os_cmd("clear")
        
        if is_logo:
            self.print_logo()

        return True

    def help(self) -> bool:
        print("\n================================ General Commands ================================\n")
        for cmd, description in self.general_commands_list:
            print(f"⦁ {cmd:10} ({self.user_shortcuts[cmd]:3}) ⟹   {description}")

        print("\n================================= Notes Commands =================================\n")
        for cmd, description in self.notes_commands_list:
            print(f"⦁ {cmd:10} ({self.user_shortcuts[cmd]:3}) ⟹   {description}")
        
        print("\n==================================================================================\n")

        return True

    def credits(self) -> bool:
        dependencies_str = f"""
        ======================================== Assets ======================================= 
        
        ⦁ ASCII-Art (font: Shadow) ⟹ https://patorjk.com/software/taag
            ◦ Fonts: 'Shadow' (Logo), 'Pagga' (code comments subsection), 'Future' (code comments subsubsections)'
        
        ====================================== Python libs ====================================
        
        ⦁ prompt-toolkit           ⟹ https://github.com/prompt-toolkit/python-prompt-toolkit
        """

        print(dependencies_str)

        return True

    """
    ░█▀█░█▀█░▀█▀░█▀▀░█▀▀░░░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀
    ░█░█░█░█░░█░░█▀▀░▀▀█░░░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█
    ░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
    """
    
    """
    ┏┓ ┏━╸
    ┣┻┓┣╸ 
    ┗━┛┗━╸
    """

    def _create_daily_note(self, daily_note_template_file: str) -> str | None:
        timestamp = compute_date()
        
        # Create daily note filename
        daily_note_filename = f"{self.configurator.daily_path}/{timestamp}{self.configurator.notes_format}"
        print(daily_note_filename)

        # If file already exists, then just return the 'daily_note_filename' var (i.e: file path)
        if os.path.exists(daily_note_filename):
            print(fg_text("File already exists; just opening it", BLUE))
            wait_ms(self.BASIC_CMD_DELAY_MS)
            return daily_note_filename

        try:
            # Read template content
            with open(daily_note_template_file, 'r', encoding='utf-8') as file:
                template_content = file.read()
            
            # Create new content with timestamp header
            new_content = f"# {timestamp}\n\n{template_content}"
            
            # Write to new file
            with open(daily_note_filename, 'w', encoding='utf-8') as file:
                file.write(new_content)
                
            print(f"Created: {daily_note_filename}")
            wait_ms(self.BASIC_CMD_DELAY_MS)
            return daily_note_filename
        except FileNotFoundError:
            print(fg_text(f"Error: '{daily_note_template_file}' or {daily_note_filename} not found!", RED))
            return None
        except Exception as e:
            print(fg_text(f"Error: {e}", RED))
            return None

    """
    ┏━╸┏┳┓╺┳┓┏━┓
    ┃  ┃┃┃ ┃┃┗━┓
    ┗━╸╹ ╹╺┻┛┗━┛
    """

    def ls(self) -> bool:
        execute_os_cmd(f"ls {self.configurator.pkm_path} | grep '{self.configurator.notes_format}'")
        
        return True

    @not_implemented
    def random(self) -> bool:
        pass

    def daily(self) -> bool:
        daily_note_template_file = f"{self.configurator.templates_path}/{self.configurator.user_config["TEMPLATES"]["DAILY_NOTE_TEMPLATE"]}{self.configurator.notes_format}"
        daily_note_filename = self._create_daily_note(daily_note_template_file = daily_note_template_file)
        
        if daily_note_filename:
            execute_os_cmd(f"{self.configurator.text_editor} {daily_note_filename}")

        return True  
    