class PeakML():
    def __init__(self, header, peaks, filepath):
        self.selected_peak = None
        self.filepath = filepath
        self.header = header
        self.filters = []
        self.peaks = peaks if peaks else []

    def get_nr_peaks(self):
        return self.header.nrpeaks

    def set_selected_peak_uid(self, peak_uid):
        self.selected_peak = peak_uid

    def get_selected_peak_uid(self):
        return self.selected_peak

    def get_selected_peak(self):
        for peak in self.peaks:
           if peak.uid == str(self.get_selected_peak_uid()):
               return peak
        
    def get_peak_from_scanid(self, scanid):
        for peak in self.peaks:
           if peak.scanid == scanid:
               return peak

    def get_peak_from_sha1sum(self, sha1sum):
        for peak in self.peaks:
           if peak.sha1sum == sha1sum:
               return peak
                
    def get_filtered_peaks(self):

        filtered_peaks = self.peaks

        for filter in self.filters:
            filtered_peaks = filter.apply_filter_to_peak_list(filtered_peaks)

        return filtered_peaks

    def add_filter(self, filter):
        self.filters.append(filter)

    def get_filters(self):
        return self.filters

    def remove_filter_by_id(self, id):
        [self.filters.pop(i) for i in range(len(self.filters)) if self.filters[i].get_id_str() == id]
