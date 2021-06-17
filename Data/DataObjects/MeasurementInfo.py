import Utilities as Utils

class MeasurementInfo():
    def __init__(self, id, label, sampleid):
        self.id = id
        self.label = label
        self.sampleid = sampleid 
        self.scans = []
        self.files = []
        self.selected = True

        self.uid = Utils.get_new_uuid()
        self.colour = None

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid

    def add_scan(self, scan):
        self.scans.append(scan)

    def add_file(self, file):
        self.files.append(file)

    def get_sampleid(self):
        return self.sampleid

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_selected(self):
        return self.selected

    def set_selected(self, selected):
        self.selected = selected

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour