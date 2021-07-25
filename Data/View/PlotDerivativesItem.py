from Data.View.BaseItem import BaseItem

class PlotDerivativesItem(BaseItem):
    def __init__(self, mass: str = "", intensity: str = "", description: str = ""):
        super().__init__()
        self.mass = mass
        self.intensity = intensity
        self.description = description

    @property
    def mass(self) -> str:
        return self._mass
    
    @mass.setter
    def mass(self, mass: str):
        self._mass = mass

    @property
    def intensity(self) -> str:
        return self._intensity
    
    @intensity.setter
    def intensity(self, intensity: str):
        self._intensity = intensity

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str):
        self._description = description