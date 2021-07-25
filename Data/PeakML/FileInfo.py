from Data.PeakML.AnnotatableEntity import AnnotatableEntity

class FileInfo(AnnotatableEntity):
    def __init__(self, label: str, name: str, location: str):
        AnnotatableEntity.__init__(self)

        # PeakML attributes
        self.label = label
        self.name = name
        self.location = location

    @property
    def label(self) -> str:
        return self._label
    
    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def location(self) -> str:
        return self._location
    
    @location.setter
    def location(self, location: str):
        self._location = location