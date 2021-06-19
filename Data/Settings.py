import IO.SettingsIO as SetIO

class Settings():
    def __init__(self):
        preferences = []
        preferences = SetIO.load_preferences()

        self.appearance_smooth = None
        self.appearance_decdp = None

        for preference in preferences:
            if preference[0] == "smooth":
                self.appearance_smooth = preference[1]
            elif preference[0] == "decdp":
                self.appearance_decdp = preference[1]

        self.databases = []
        self.databases = SetIO.load_database_paths()

    def get_preference_by_name(self, name):   
        if name == "smooth":
            return self.appearance_smooth
        elif name == "decdp":
            return self.appearance_decdp

    def set_preference_by_name(self, name, value):   
        if name == "smooth":
            self.appearance_smooth = value
        elif name == "decdp":
            self.appearance_decdp = value

    def get_database_paths(self):
        return self.databases

    def set_database_paths(self, databases):
        self.databases = databases



    