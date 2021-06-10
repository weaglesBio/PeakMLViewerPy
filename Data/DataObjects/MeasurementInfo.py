class MeasurementInfo():
    def __init__(self, id, label, sampleid):
        self.id = id # int
        self.label = label # string
        self.sampleid = sampleid 
        self.scans = []
        self.files = []

    def add_scan(self, scan):
        self.scans.append(scan)

    def add_file(self, file):
        self.files.append(file)