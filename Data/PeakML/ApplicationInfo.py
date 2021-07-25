class ApplicationInfo():
    def __init__(self, name: str, version: str, date: str, parameters: str):
        
        # PeakML attributes
        self.name = name
        self.version = version
        self.date = date
        self.parameters = parameters

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def version(self) -> str:
        return self._version
    
    @version.setter
    def version(self, version: str):
        self._version = version

    @property
    def date(self) -> str:
        return self._date
    
    @date.setter
    def date(self, date: str):
        self._date = date

    @property
    def parameters(self) -> str:
        return self._parameters
    
    @parameters.setter
    def parameters(self, parameters: str):
        self._parameters = parameters