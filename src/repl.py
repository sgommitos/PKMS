"""
██      ██ ██████  ██████   █████  ██████  ██ ███████ ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██      ██      
██      ██ ██████  ██████  ███████ ██████  ██ █████   ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██           ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██ ██ ███████ ███████ 
"""

from slibs.os_discriminator import *
from slibs.printl           import *

from src.commands           import REPL_Commands
from src.configurator       import JSON_Configurator

"""
███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████ 
██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██      
█████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████ 
"""

# =============================================================================================== #

def repl() -> None:
    configurator      = JSON_Configurator(user_config_file = "config/user_config.json", sw_data_tree_file = "sw_files/sw_data_tree.json")
    repl_cmd_handler  = REPL_Commands(configurator)

    # ========================================================= #

    repl_cmd_handler.print_welcome()

    while(True):
        user_input = repl_cmd_handler.get_user_input()

        if not repl_cmd_handler.exec_repl_cmd(user_input): fail_return()
    
                            
