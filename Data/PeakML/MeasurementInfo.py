from Data.PeakML.FileInfo import FileInfo
from Data.PeakML.ScanInfo import ScanInfo

class MeasurementInfo():
    def __init__(self, id: int, label: str, sample_id: int):

        # PeakML attributes
        self.id = id
        self.label = label
        self.sample_id = sample_id

        self._scans = []
        self._files = []

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def label(self) -> str:
        return self._label
    
    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def sample_id(self) -> int:
        return self._sample_id
    
    @sample_id.setter
    def sample_id(self, sample_id: int):
        self._sample_id = sample_id

    @property
    def scans(self) -> list[ScanInfo]:
        return self._scans

    def add_scan(self, scan: ScanInfo):
        self.scans.append(scan)

    @property
    def files(self) -> list[FileInfo]:
        return self._files

    def add_file(self, file: FileInfo):
        self.files.append(file)