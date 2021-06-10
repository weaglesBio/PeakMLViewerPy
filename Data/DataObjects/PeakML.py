class PeakML():
    def __init__(self, header, peaks, filepath):
        self.selected_peak = None
        self.filepath = filepath
        self.header = header
        if peaks:
            self.peaks = peaks
        else:
            self.peaks = []

    def get_nr_peaks(self):
        return "0"

    def set_selected_peak(self, peak_id):
        self.selected_peak = peak_id

    def get_selected_peak(self):
        return self.selected_peak

    def get_peak_from_scanid(self, scanid):
        for peak in self.peaks:
           if peak.scanid == scanid:
               return peak

    def get_peak_from_sha1sum(self, sha1sum):
        for peak in self.peaks:
           if peak.sha1sum == sha1sum:
               return peak

