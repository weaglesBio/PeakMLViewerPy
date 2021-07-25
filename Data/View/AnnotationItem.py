from Data.View.BaseItem import BaseItem

class AnnotationItem(BaseItem):
    def __init__(self, label: str, value: str = ""):
        super().__init__()

        self.label = label
        self.value = value

    @property
    def label(self) -> str:
        return self._label
    
    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value: str):
        self._value = value