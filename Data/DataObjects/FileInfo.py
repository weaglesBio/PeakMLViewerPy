from Data.DataObjects.Annotatable import Annotatable

class FileInfo(Annotatable):
    def __init__(self, label, name, location):
        Annotatable.__init__(self)
        self.label = label # string
        self.name = name # string
        self.location = location # string