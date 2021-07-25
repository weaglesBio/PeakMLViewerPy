from Data.View.BaseItem import BaseItem

class EntryItem(BaseItem):
    def __init__(self, uid: str, type: int, retention_time: str = "", mass: str = "", intensity: str = "", nr_peaks: str = "", has_annotation: bool = False):
        
        # Set peak uid as entry item uid
        super().__init__(uid)

        self.type = type
        self.retention_time = retention_time
        self.mass = mass
        self.intensity = intensity
        self.nr_peaks = nr_peaks
        self.has_annotation = has_annotation

    @property
    def type(self) -> int:
        return self._type
    
    @type.setter
    def type(self, type: int):
        self._type = type

    @property
    def retention_time(self) -> str:
        return self._retention_time
    
    @retention_time.setter
    def retention_time(self, retention_time: str):
        self._retention_time = retention_time

    @property
    def mass(self) -> float:
        return self._mass
    
    @mass.setter
    def mass(self, mass: float):
        self._mass = mass

    @property
    def intensity(self) -> float:
        return self._intensity
    
    @intensity.setter
    def intensity(self, intensity: float):
        self._intensity = intensity

    @property
    def nr_peaks(self) -> str:
        return self._nr_peaks
    
    @nr_peaks.setter
    def nr_peaks(self, nr_peaks: str):
        self._nr_peaks = nr_peaks

    @property
    def has_annotation(self) -> bool:
        return self._has_annotation
    
    @has_annotation.setter
    def has_annotation(self, has_annotation: bool):
        self._has_annotation = has_annotation