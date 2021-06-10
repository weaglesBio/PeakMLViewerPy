from Data.DataObjects.Annotatable import Annotatable

class ScanInfo(Annotatable):
    def __init__(self, polarity, retention_time):
        self.polarity = polarity # int
        self.retentiontime = retention_time # string
        Annotatable.__init__(self)