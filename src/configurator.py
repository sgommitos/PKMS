import json

class JSON_Configurator:
    def __init__(self, main_config_file, sw_info_config_file):
        self.main_config_file    = main_config_file
        self.sw_info_config_file = sw_info_config_file

        self._read_main_config() 

        self.user         = self.main_config["USER_DATA"]["NAME"]
        self.pkms_path    = self.main_config["PATHS"]["PKM"]
        self.text_editor  = self.main_config["PATHS"]["TEXT_EDITOR"]
        self.note_format  = self.main_config["FILE_TYPES"]["NOTES"]

        # ====================================== #

        self._read_sw_info_config()

        self.sw_version     = f"v{self.sw_info_config["VERSION"]["MAJOR"]}.{self.sw_info_config["VERSION"]["MINOR"]}"  

    def _read_main_config(self):    
        with open(self.main_config_file, 'r') as file:
            self.main_config = json.load(file)

        return
    
    def _read_sw_info_config(self):
        with open(self.sw_info_config_file, 'r') as file:
            self.sw_info_config = json.load(file)

        return
    
    # ===================================================== #