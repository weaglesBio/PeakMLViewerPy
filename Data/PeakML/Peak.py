from Data.PeakML.PeakData import PeakData
from Data.PeakML.AnnotatableEntity import AnnotatableEntity

from typing import List

class Peak(AnnotatableEntity):
    def __init__(self, type: str, scan: str, retention_time: str, mass: float, intensity: float, measurement_id: str, pattern_id: str, sha1sum: str, signal: str, peak_data: PeakData):
        AnnotatableEntity.__init__(self)

        # PeakML attributes
        self.type = type
        self.scan = scan
        self.retention_time = retention_time
        self.mass = mass
        self.intensity = intensity
        self.measurement_id = measurement_id
        self.pattern_id = pattern_id
        self.sha1sum = sha1sum
        self.signal = signal
        self.peak_data = peak_data
        
        self.peaks = []
  
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, type: str):
        self._type = type

    @property
    def scan(self) -> str:
        return self._scan
    
    @scan.setter
    def scan(self, scan: str):
        self._scan = scan

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
    def measurement_id(self) -> int:
        return self._measurement_id
    
    @measurement_id.setter
    def measurement_id(self, measurement_id: int):
        self._measurement_id = measurement_id

    @property
    def pattern_id(self) -> int:
        return self._pattern_id
    
    @pattern_id.setter
    def pattern_id(self, pattern_id: int):
        self._pattern_id = pattern_id

    @property
    def sha1sum(self) -> str:
        return self._sha1sum
    
    @sha1sum.setter
    def sha1sum(self, sha1sum: str):
        self._sha1sum = sha1sum

    @property
    def signal(self) -> str:
        return self._signal
    
    @signal.setter
    def signal(self, signal: str):
        self._signal = signal

    @property
    def peak_data(self) -> PeakData:
        return self._peak_data

    @peak_data.setter
    def peak_data(self, peak_data: PeakData):
        self._peak_data = peak_data

    @property
    def set_intensities(self) -> List[float]:
        return self._set_intensities

    @set_intensities.setter
    def set_intensities(self, set_intensities: List[float]):
        self._set_intensities = set_intensities