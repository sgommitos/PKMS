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
    configurator      = JSON_Configurator(main_config_file = "config/main_config.json", sw_info_config_file = "config/sw_info_config.json")
    repl_cmd_handler  = REPL_Commands(configurator)

    # ========================================================= #

    repl_cmd_handler.print_welcome()

    while(True):
        print(bold_text("\nPKMS > "), end="")
        
        user_input = input()
        
        if not repl_cmd_handler.exec_repl_cmd(user_input): fail_return()
    
                            
