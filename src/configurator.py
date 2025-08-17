import json

class JSON_Configurator:
    def __init__(self, user_config_file, sw_data_tree_file):
        self.user_config_file    = user_config_file
        self.sw_data_tree_file   = sw_data_tree_file

        self._read_user_config_file() 

        self.user            = self.user_config["USER_DATA"]["NAME"]
        self.pkms_path       = self.user_config["PATHS"]["PKM"]
        self.pkms_daily_path = self.user_config["PATHS"]["DAILY"]
        self.text_editor     = self.user_config["PATHS"]["TEXT_EDITOR"]
        self.note_format     = self.user_config["FILE_TYPES"]["NOTES"]

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