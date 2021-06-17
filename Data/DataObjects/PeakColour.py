
class PeakColour():
    def __init__(self, sampleid, measurementid, colour, selected):
        self.sampleid = sampleid
        self.measurementid = measurementid
        self.colour = colour
        self.selected = selected

    def get_sampleid(self):
        return self.sampleid

    def get_measurementId(self):
        return self.measurementid

    def get_colour(self):
        return self.colour

    def get_selected(self):
        return self.selected

    def set_selected(self, selected):
        self.selected = selected