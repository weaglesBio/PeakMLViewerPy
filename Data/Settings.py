import IO.SettingsIO as SetIO
from typing import List

class Settings():
    def __init__(self, preferences: List[str] = [], databases: List[str] = []):
        self.preferences = preferences
        #preferences = SetIO.load_preferences()

        self.appearance_smooth = None
        self.appearance_decdp = None

        for preference in self.preferences:
            if preference[0] == "smooth":
                self.appearance_smooth = preference[1]
            elif preference[0] == "decdp":
                self.appearance_decdp = preference[1]

        self.databases = databases
        #self.databases = SetIO.load_database_paths()

    def get_preference_by_name(self, name: str) -> str:
        if name == "smooth":
            return self.appearance_smooth
        elif name == "decdp":
            return self.appearance_decdp

    def set_preference_by_name(self, name: str, value: str):   
        if name == "smooth":
            self.appearance_smooth = value
        elif name == "decdp":
            self.appearance_decdp = value

    def get_database_paths(self) -> List[str]:
        return self.databases

    def set_database_paths(self, databases: List[str]):
        self.databases = databases



    