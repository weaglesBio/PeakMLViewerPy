from Data.View.BaseItem import BaseItem

class PlotIntensityLogItem(BaseItem):
    def __init__(self, set_id: str = "", intensities: str = ""):
        super().__init__()

        self.set_id = set_id
        self.intensities = intensities

    @property
    def set_id(self) -> str:
        return self._set_id
    
    @set_id.setter
    def set_id(self, set_id: str):
        self._set_id = set_id

    @property
    def intensities(self) -> str:
        return self._intensities
    
    @intensities.setter
    def intensities(self, intensities: str):
        self._intensities = intensities