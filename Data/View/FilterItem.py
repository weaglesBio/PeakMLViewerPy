from Data.View.BaseItem import BaseItem

class FilterItem(BaseItem):
    def __init__(self, uid: str, type: str = "", settings: str = ""):
        
        # Set filter uid as filter item uid
        super().__init__(uid)

        self.type = type
        self.settings = settings

    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, type: str):
        self._type = type

    @property
    def settings(self) -> str:
        return self._settings
    
    @settings.setter
    def settings(self, settings: str):
        self._settings = settings