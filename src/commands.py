# --- REPL: Autocomplete, History and KeyBindings dependencies --- #
from prompt_toolkit             import prompt
from prompt_toolkit.completion  import WordCompleter
from prompt_toolkit.history     import FileHistory
from prompt_toolkit.key_binding import KeyBindings
# ------------------------------------------------- #

from pathlib import Path
import os
from datetime import datetime
import re

from slibs.os_discriminator     import *
from slibs.timing               import compute_date, wait_ms
from slibs.printl               import fg_text, bg_text, italic_text, bold_text, RED, GREEN, BLUE
from slibs.debug_tools          import not_implemented, to_reimplement, not_fully_implemented
from slibs.utf8_symbols         import * 

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
            
            "help"         : [self.help,       "general_cmd", "Print a list of available cmd (within relative description)"],
            "about"        : [self.about,      "general_cmd", "Print SW info"],
            "credits"      : [self.credits,    "general_cmd", "Print SW credits"],
            "clear"        : [self.clear,      "general_cmd", "Clear REPL terminal"],
            "exit"         : [self.quit,       "general_cmd", "Quit REPL"],
            "quit"         : [self.quit,       "general_cmd", "Quit REPL"],
            "reload"       : [self.reload,     "general_cmd", "Reload SW configuration files"],

            # --- Notes Commands --- #

            "sanitize"     : [self.sanitize,   "notes_cmd",   "Rename notes and imgs following a pre-defined pattern"],
            "lsn"          : [self.lsn,        "notes_cmd",   "List all your notes in setup pkm folder"],
            "lsi"          : [self.lsi,        "notes_cmd",   "List all your imgs (.png, .jpeg, .jpg) in setup pkm folder"],
            "note"         : [self.note,        "notes_cmd",  "R/W a target note"],
            "imgs"        
            "random"       : [self.random,     "notes_cmd",   "Read a random note from your pkms folder"],
            "daily"        : [self.daily,      "notes_cmd",   "Open (or create, if not exists) daily note"],
        }

        self.general_commands_list = []
        self.notes_commands_list   = []
        self._populate_commands_lists()

        self.pkm_notes_files = {}
        self.pkm_imgs_files  = {}
        self._populate_pkm_file_lists()
        self._compute_pkm_notes_stats()

        self.user_shortcuts        = {}
        self._populate_user_shortcuts_dict()
        self._setup_keybindigs() 

        # --- Completer and history setup --- #

        # REPL commands
        self.cmds_completer   = WordCompleter(list(self.commands_dict.keys()))
        self.cmds_history     = FileHistory(configurator.cmds_history_file)
        
        # Notes
        self.notes_completer  = WordCompleter(list(self.pkm_notes_files.keys()))
        self.notes_history    = FileHistory(configurator.notes_history_file)

        # Imgs
        self.imgs_completer   = WordCompleter(list(self.pkm_imgs_files.keys()))
        self.imgs_history     = FileHistory(configurator.imgs_history_file)

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
            self.user_shortcuts.update({cmd : ''})

        return 

    def _populate_pkm_file_lists(self) -> bool:
        # Empty target dicts
        self.pkm_notes_files = {}
        self.pkm_imgs_files  = {}        
        
        unsorted_files = os.listdir(self.configurator.pkm_path)
        
        #@NOTE: get files based on the order specified in user_config; if blank, it use 'newer' order by default
        match self.configurator.file_list_order.lower():
                case "alphabetic" :
                    sorted_files = sorted(unsorted_files, key=str.lower)
                case "older"      :
                    sorted_files = sorted(unsorted_files, key=lambda x: os.path.getmtime(os.path.join(self.configurator.pkm_path, x)), reverse=False)  
                case "newer"      :
                    sorted_files = sorted(unsorted_files, key=lambda x: os.path.getmtime(os.path.join(self.configurator.pkm_path, x)), reverse=True)  
                case _            :
                    sorted_files = sorted(unsorted_files, key=lambda x: os.path.getmtime(os.path.join(self.configurator.pkm_path, x)), reverse=True)  

        for filename in sorted_files:
            target_filename = filename.lower()
            
            if target_filename.endswith(self.configurator.notes_format):
                # @NOTE: before update dict, check that is a file (i.e: NOT a directory)
                
                filepath = os.path.join(self.configurator.pkm_path, filename)
                if os.path.isfile(filepath):
                    self.pkm_notes_files.update({filename: [filepath, datetime.fromtimestamp(os.stat(filepath).st_mtime).strftime('%Y/%m/%d - %H:%M:%S')]})
            
            elif (target_filename.endswith('.png')) or (target_filename.endswith('.jpg')) or (target_filename.endswith('.jpeg')):
                # @NOTE: before update dict, check that is a file (i.e: NOT a directory)
                
                filepath = os.path.join(self.configurator.pkm_path, filename)
                if os.path.isfile(filepath):
                    self.pkm_imgs_files.update({filename: [filepath, datetime.fromtimestamp(os.stat(filepath).st_mtime).strftime('%Y/%m/%d - %H:%M:%S')]})

        return True
    
    def _compute_pkm_notes_stats(self) -> None:
        datetimes = [note_timestamp for _, (_, note_timestamp) in self.pkm_notes_files.items()]
        
        self.notes_newest_datetime  = max(datetimes)
        notes_newest_datetime_obj   = datetime.strptime(self.notes_newest_datetime, "%Y/%m/%d - %H:%M:%S")
        
        self.notes_oldest_datetime  = min(datetimes)
        notes_oldest_datetime_obj   = datetime.strptime(self.notes_oldest_datetime, "%Y/%m/%d - %H:%M:%S")

        notes_delta_timestamp_obj = notes_newest_datetime_obj - notes_oldest_datetime_obj
        self.notes_delta_timestamp = {
            "years"  : notes_delta_timestamp_obj.days // 365,  
            "months" : notes_delta_timestamp_obj.days // 30,  
            "days"   : notes_delta_timestamp_obj.days
        }

        self.notes_delta_timestamp = {
            # @NOTE: computing date only
            "years"   : (notes_newest_datetime_obj.year - notes_oldest_datetime_obj.year),
            "months"  : (notes_newest_datetime_obj.month - notes_oldest_datetime_obj.month), 
            "days"    : (notes_newest_datetime_obj.day - notes_oldest_datetime_obj.day),
        }  

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
            completer=self.cmds_completer,
            history=self.cmds_history
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
██████╔╝█████╔╝ ██╔████╔██║███████╗   SW version {STYLED_SOUTHWEST_ARROW}
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
        if (self.configurator._load_configs() and self._populate_pkm_file_lists()):
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

    def _sanitize_filename(self, filename) -> str:
        """
        @BRIEF: transform every filename into a str that match
                the following patter: 'word1_word2_word3_'...
        """
        
        # Split filename from its extention
        filename_without_ext, ext = os.path.splitext(filename)

        #@NOTE    : subsistute spaces, dashed e special chars within "_"
        #@WARNING : DO NOT SUBSISTUTE upper case within lower case         
        sanitized = re.sub(r'[^\w\s]', '_', filename_without_ext)  # Remove special chars -> ''
        sanitized = re.sub(r'\s+', '_', sanitized.strip())         # Replace spaces -> underscore
        sanitized = re.sub(r'_+', '_', sanitized)                  # Replace multiple underscore -> single underscore

        sanitized += ext if ext else self.configurator.notes_format
        
        return sanitized.lower()

    def _rename_file(self, directory, old_filepath, old_filename, new_filename) -> str:
        new_filepath = os.path.join(directory, new_filename)
        
        try:
            os.rename(old_filepath, new_filepath)
            print(f"{fg_text(f"            ◦ File '{old_filename}' it's now: '{new_filename}'", GREEN)}")
            return new_filepath
        except FileExistsError:
            print(f"{fg_text(f"            ◦ ERROR: File '{new_filename}' already exists!", RED)}")
            return old_filepath
        except Exception as e:
            print(f"{fg_text(f"            ◦ ERROR while renaming '{old_filename}': {e}", RED)}")
            return old_filepath

    def _write_note(self, note_name, is_new_note) -> None:
        if is_new_note:
            execute_os_cmd(f"{self.configurator.text_editor} \"{self.configurator.pkm_path}/{note_name}\"")
        else:
            execute_os_cmd(f"{self.configurator.text_editor} \"{self.pkm_notes_files[note_name][0]}\"")

        return

    def _read_note(self, note_name) -> None:
        note_path = self.pkm_notes_files[note_name][0]
        longest_line_size = int(execute_and_capture_os_cmd(["wc", "-L" , note_path]).split(" ")[0])

        print(end="\n\n") # @NOTE: add some vertical spacing before printing (i guess it's more readable)

        print(f"{DIVIDER_SYMBOL_UPPER * longest_line_size} ")
        execute_os_cmd(f"{self.configurator.print_tool} \"{note_path}\"")
        print(f"{DIVIDER_SYMBOL_DOWNER * longest_line_size} ")
        
        return
    
    def _has_extension(self, file_name: str) -> str | None:
        file_ext = Path(file_name).suffix
        
        return file_ext if file_ext else None
    
    def _replace_extension(self, file_name: str, target_ext: str) -> str:
        return str(Path(file_name).with_suffix(target_ext))

    def _handle_note_extension(self, note_name: str) -> str:
        note_ext = self._has_extension(note_name)

        if note_ext is None or note_ext != self.configurator.notes_format:
            new_note_name = self._replace_extension(note_name, self.configurator.notes_format)
        else:
            new_note_name = note_name
        
        return new_note_name 

    def _create_daily_note(self, daily_note_template_file: str) -> str | None:
        timestamp = compute_date()
        
        # Create daily note filename
        daily_note_filename = f"{self.configurator.pkm_path}/{timestamp}{self.configurator.notes_format}"
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

    def sanitize(self) -> bool:
        # Make sure the user is aware of what they're doing
        print("   1. Are you sure you want to sanitize your pkm filenames?  [y/n] : ", end="")
        while(True):
            user_input = input()

            match user_input.lower():
                case "y": 
                    break
                case "n":
                    print(fg_text("      Aborting operation", BLUE))
                    wait_ms(self.BASIC_CMD_DELAY_MS)
                    return True
                case _:
                    print("      Invalid input! Please retry: ", end="")

        is_user_check = False
        print("   2. Do you wanna confirm renaming operation for each file? [y/n] : ", end="")
        while(True):
            user_input = input()

            match user_input.lower():
                case "y": 
                    is_user_check = True
                    break
                case "n":
                    break
                case _:
                    print("      Invalid input! Please retry: ", end="")

        print()
        print(fg_text("      Start sanitization process...", BLUE), end="")
        print()
        
        # Handle notes
        tmp_notes_dict = {}
        notes_changed_cnt = 0
        for note_name, (note_path, note_timestamp) in self.pkm_notes_files.items():
            new_note_name = self._sanitize_filename(note_name)

            if new_note_name != note_name:
                if is_user_check:
                    print(f"         ⦁ Do you wanna rename {note_name} -> {new_note_name}? [y/n]: ", end="")
                    while(True):
                        user_input = input()

                        match user_input.lower():
                            case "y": 
                                new_note_path = self._rename_file(self.configurator.pkm_path, note_path, note_name, new_note_name)
                                notes_changed_cnt += 1
                                break
                            case "n":
                                break
                            case _:
                                print("      Invalid input! Please retry: ", end="")
                else:
                    new_note_path = self._rename_file(self.configurator.pkm_path, note_path, note_name, new_note_name)
                    notes_changed_cnt += 1
            else:
                new_note_path = note_path

            tmp_notes_dict[new_note_name] = (note_timestamp, new_note_path)
        self.pkm_notes_files = tmp_notes_dict

        print()
        if   (notes_changed_cnt > 0) : print(f"      A total of {bold_text(notes_changed_cnt)} note(s) was sanitized")
        else                         : print(f"      All notes filenames are already sanitized")                 
        
        # Handle imgs
        tmp_imgs_dict = {}
        imgs_changed_cnt = 0
        for img_name, (img_path, img_timestamp) in self.pkm_imgs_files.items():
            new_img_name = self._sanitize_filename(img_name)

            if new_img_name != img_name:
                if is_user_check:
                    print(f"         ⦁ Do you wanna rename {img_name} -> {new_img_name}? [y/n]: ", end="")
                    while(True):
                        user_input = input()

                        match user_input.lower():
                            case "y": 
                                new_img_path = self._rename_file(self.configurator.pkm_path, img_path, img_name, new_img_name)
                                imgs_changed_cnt += 1
                                break
                            case "n":
                                break
                            case _:
                                print("      Invalid input! Please retry: ", end="")
                else:
                    new_img_path = self._rename_file(self.configurator.pkm_path, img_path, img_name, new_img_name)
                    imgs_changed_cnt += 1
            else:
                new_img_path = img_path

            tmp_imgs_dict[new_img_name] = (img_timestamp, new_img_path)
        self.pkm_imgs_files = tmp_imgs_dict

        print()
        if   (imgs_changed_cnt > 0) : print(f"      A total of {bold_text(imgs_changed_cnt)} img(s) was sanitized")
        else                        : print(f"      All imgs filenames are already sanitized")

        return True
        
        
    def lsn(self) -> bool:
        stats_str = f"""
        \rA total of {bold_text(f"{len(self.pkm_notes_files)} notes")} was found.
        \rYou've been keeping your notes for {self.notes_delta_timestamp["years"]} year(s), {self.notes_delta_timestamp["months"]} month(s), {self.notes_delta_timestamp["days"]} day(s)!
        """
        
        print(stats_str)

        for note, (_, note_timestamp) in self.pkm_notes_files.items():
            print(f"⦁ {(italic_text(note.ljust(50)))} ({note_timestamp})")
        
        return True

    def lsi(self) -> bool:
        stats_str = f"""
        \rA total of {bold_text(f"{len(self.pkm_imgs_files)} imgs")} was found.
        """
        
        print(stats_str)

        for img, (_, img_timestamp) in self.pkm_imgs_files.items():
            print(f"⦁ {(italic_text(img.ljust(50)))} ({img_timestamp})")
        
        return True

    def note(self) -> bool:
        while(True):
            target_note_name = prompt("   1. Write your note's name (TAB for autocompletion, Return to exit): ", completer=self.notes_completer)

            if target_note_name == "":
                print(f"      {fg_text(f"{WARNING_TRIANGLE} Aborting operation", BLUE)}")
                return True # @NOTE: exit from 'note' submenu

            if not target_note_name in self.pkm_notes_files.keys():
                is_new_note = False
                print(f"      {FILLED_BULLET_POINT} Note does not exists. Do you wanna create it? [y/n]: ", end="")
                while(True):
                    user_input = input().lower()

                    match user_input:
                        case "y":
                            is_new_note = True
                            break     
                        case "n":
                            print(f"         {fg_text(f"{WARNING_TRIANGLE} Aborting operation", BLUE)}")
                            return True # @NOTE: exit from 'note' submenu
                        case _:
                            print(f"         {WARNING_TRIANGLE} Invalid input! Please retry: ", end="")
                if is_new_note:
                    self._write_note(self._handle_note_extension(target_note_name), is_new_note=True)
                    return True
            else:
                break
        
        is_read_operation = False
        print("   2. What you wanna do?: [r/w]: ", end="")    
        while(True):
            user_input = input().lower()

            match user_input:
                case "r":
                    is_read_operation = True
                    break     
                case "w":
                    break
                case _:
                    print(f"         {WARNING_TRIANGLE} Invalid input! Please retry: ", end="")
        
        if   is_read_operation : self._read_note(target_note_name)
        else                   : self._write_note(target_note_name, is_new_note=False)

        return True
    
    @not_implemented
    def imgs(self) -> bool:
        target_img_name  = prompt("   1. Write your note's name (TAB for autocompletion): ", completer=self.imgs_completer)

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
    