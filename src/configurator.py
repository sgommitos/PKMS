from pathlib import Path
import json

class JSON_Configurator:
    def __init__(self, user_config_file, sw_data_tree_file):        
        self.user_config_file    = user_config_file
        self.sw_data_tree_file   = sw_data_tree_file

        self.sw_path = Path(__file__).parent.parent.absolute()

        # ====================================== #

        self._read_user_config_file() 

        self.user            = self.user_config["USER_DATA"]["NAME"]
        
        self.pkm_path        = Path(self.user_config["PATHS"]["PKM"]).expanduser()
        self.daily_path      = f"{self.pkm_path}/{self.user_config["PATHS"]["DAILY"]}"
        self.finances_path   = f"{self.pkm_path}/{self.user_config["PATHS"]["FINANCES"]}"
        
        self.templates_path  = f"{self.sw_path}/{self.user_config["PATHS"]["TEMPLATES"]}"
        
        self.text_editor     = self.user_config["PATHS"]["TEXT_EDITOR"]
        self.notes_format    = self.user_config["FILE_TYPES"]["NOTES"]

        # ====================================== #

        self._read_sw_data_tree_file()

        self.sw_version     = f"v{self.sw_data_tree["VERSION"]["MAJOR"]}.{self.sw_data_tree["VERSION"]["MINOR"]} ({self.sw_data_tree["VERSION"]["BUILD_STR"]})"
        self.cli_history    = self.sw_data_tree["SW_FILES_PATHS"]["HISTORY"]

    def _read_user_config_file(self):    
        with open(self.user_config_file, 'r') as file:
            self.user_config = json.load(file)

        return
    
    def _read_sw_data_tree_file(self):
        with open(self.sw_data_tree_file, 'r') as file:
            self.sw_data_tree = json.load(file)

        return
    
    # ===================================================== #