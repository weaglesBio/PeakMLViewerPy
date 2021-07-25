from Data.View.BaseItem import BaseItem

class FilterItem(BaseItem):
    def __init__(self, id: str, type: str = "", settings: str = ""):
        super().__init__()

        self.id = id
        self.type = type
        self.settings = settings

    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, id: str):
        self._id = id

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