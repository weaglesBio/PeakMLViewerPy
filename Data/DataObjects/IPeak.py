from Data.DataObjects.Annotatable import Annotatable

class IPeak(Annotatable):
    def __init__(self, mass, intensity, scanid, retentiontime):
        Annotatable.__init__(self)
        self.mass = mass #double
        self.intensity = intensity #double
        self.scanid = scanid #double
        self.retentiontime = retentiontime #double