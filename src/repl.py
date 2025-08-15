"""
██      ██ ██████  ██████   █████  ██████  ██ ███████ ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██      ██      
██      ██ ██████  ██████  ███████ ██████  ██ █████   ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██           ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██ ██ ███████ ███████ 
"""

from slibs.timing         import wait_ms
from slibs.linux_exec     import success_return, failed_return 
from slibs.printl         import *

from src.general_commands import GeneralCommands
from src.configurator     import JSON_Configurator

"""
███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████ 
██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██      
█████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████ 
"""

# =============================================================================================== #

def repl() -> None:
    configurator = JSON_Configurator(main_config_file    = "config/main_config.json", 
                                     sw_info_config_file = "config/sw_info_config.json")
    cmd          = GeneralCommands(configurator)

    # ========================================================= #

    cmd.print_welcome()

    try:
        while(True):
            print(bold_text("\nPKMS > "), end="")
            
            user_input = input().lower()

            match user_input:
                case "help":
                    cmd.help()
                case "about":
                    cmd.about()
                case "depencencies":
                    cmd.dependecies()
                case "exit" | "quit" | "-q":
                    cmd.quit()
                case "clear":
                    cmd.clear()

                # =============================== #
                
                case "ls":
                    cmd.ls()
                case "daily":
                    cmd.daily()
                case _ :
                    cmd.unrecognized_cmd()

    except KeyboardInterrupt:
        pass
                            
