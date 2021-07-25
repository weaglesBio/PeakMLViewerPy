from Data.PeakML.AnnotatableEntity import AnnotatableEntity

class ScanInfo(AnnotatableEntity):
    def __init__(self, polarity: int, retention_time: str):
        AnnotatableEntity.__init__(self)

        # PeakML attributes
        self.polarity = polarity
        self.retention_time = retention_time

    @property
    def polarity(self) -> int:
        return self._polarity
    
    @polarity.setter
    def polarity(self, polarity: int):
        self._polarity = polarity

    @property
    def retention_time(self) -> str:
        return self._retention_time
    
    @retention_time.setter
    def retention_time(self, retention_time: str):
        self._retention_time = retention_time