from pathlib import Path
import tomllib

from slibs.printl import fg_text, RED

class Configurator:
    def __init__(self, user_config_file, sw_data_tree_file):        
        self.user_config_file    = user_config_file
        self.sw_data_tree_file   = sw_data_tree_file

        self.sw_path = Path(__file__).parent.parent.absolute()

        self._load_configs()

        # ====================================================================== #
 
        self.user                    = self.user_config["USER_DATA"]["NAME"]
        
        self.pkm_path                = Path(self.user_config["PATHS"]["PKM"]).expanduser()
        self.daily_path              = f"{self.pkm_path}/{self.user_config["PATHS"]["DAILY"]}"
        self.finances_path           = f"{self.pkm_path}/{self.user_config["PATHS"]["FINANCES"]}"
        
        self.templates_path          = f"{self.sw_path}/{self.user_config["PATHS"]["TEMPLATES"]}"
        
        self.text_editor             = self.user_config["PATHS"]["TEXT_EDITOR"]
        self.notes_format            = self.user_config["FILE_TYPES"]["NOTES"]

        self.file_list_order         = self.user_config["FILE_ORDER"]["LIST"]

        self.user_shortcuts_bindings = self.user_config["SHORTCUTS"] # @NOTE: the result is a dict
        
        # ====================================================================== #

        self.sw_version     = f"v{self.sw_data_tree["VERSION"]["MAJOR"]}.{self.sw_data_tree["VERSION"]["MINOR"]} ({self.sw_data_tree["VERSION"]["BUILD_STR"]})"
        self.cli_history    = self.sw_data_tree["SW_FILES_PATHS"]["HISTORY"]

    def _read_user_config_file(self) -> bool:    
        try:
            with open(self.user_config_file, 'rb') as file:
                self.user_config = tomllib.load(file)
        except FileNotFoundError:
            print(fg_text(f"Config file {self.user_config_file} not found!", RED))
            return False
        
        return True
    
    def _read_sw_data_tree_file(self) -> bool:
        try:
            with open(self.sw_data_tree_file, 'rb') as file:
                self.sw_data_tree = tomllib.load(file)
        except FileNotFoundError:
            print(fg_text(f"Config file {self.sw_data_tree_file} not found!", RED))
            return False
        
        return True
        
    def _load_configs(self) -> bool:
        if ((self._read_user_config_file()) and (self._read_sw_data_tree_file())):
            return True
        
        return False
    
    # ====================================================================== #