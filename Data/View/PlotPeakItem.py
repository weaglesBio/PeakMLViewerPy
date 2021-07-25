from Data.View.BaseItem import BaseItem

class PlotPeakItem(BaseItem):
    def __init__(self, label: str, rt_values: str = "", intensity_values: str = "", colour: str = ""):
        super().__init__()

        self.label = label
        self.rt_values = rt_values
        self.intensity_values = intensity_values
        self.colour = colour

    @property
    def label(self) -> str:
        return self._label
    
    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def rt_values(self) -> str:
        return self._rt_values
    
    @rt_values.setter
    def rt_values(self, rt_values: str):
        self._rt_values = rt_values

    @property
    def intensity_values(self) -> str:
        return self._intensity_values
    
    @intensity_values.setter
    def intensity_values(self, intensity_values: str):
        self._intensity_values = intensity_values

    @property
    def colour(self) -> str:
        return self._colour
    
    @colour.setter
    def colour(self, colour: str):
        self._colour = colour