class SampleInfo():
    def __init__(self, name: str, annotations: str):

        # PeakML attributes
        self.name = name
        self.annotations = annotations

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def annotations(self) -> str:
        return self._annotations
    
    @annotations.setter
    def annotations(self, annotations: str):
        self._annotations = annotations
