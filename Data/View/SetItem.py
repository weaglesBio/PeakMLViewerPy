from Data.View.BaseItem import BaseItem

class SetItem(BaseItem):
    def __init__(self, name: str, color: str = "", parent: str = None):
        super().__init__(initial_checked_state = True)

        self.name = name
        self.color = color
        self.parent = parent

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, color: str):
        self._color = color

    @property
    def parent(self) -> str:
        return self._parent
    
    @parent.setter
    def parent(self, parent: str):
        self._parent = parent