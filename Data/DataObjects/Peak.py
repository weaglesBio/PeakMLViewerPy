import Utilities as Utils
from Data.DataObjects.Annotatable import Annotatable

class Peak(Annotatable):
    def __init__(self, type, scan, retentiontime, mass, intensity, measurementid, patternid, sha1sum, signal, peak_data):
        Annotatable.__init__(self)
        self.type = type
        self.scan = scan
        self.retentiontime = retentiontime
        self.mass = mass
        self.intensity = intensity
        self.measurementid = measurementid
        self.patternid = patternid
        self.sha1sum = sha1sum
        self.signal = signal
        self.peak_data = peak_data
        self.checked = False
        self.peaks = []
        self.uid = Utils.get_new_uuid()
  
    def get_uid(self):
        return self.uid

    def add_peak(self, peak):
        self.peaks.append(peak)

    def if_patternid_set(self):
        return round(self.get_patternid() != 0)

    def get_type(self):
        return self.type

    def get_scanid(self):
        return self.scan

    def get_patternid(self):
        return self.patternid

    def get_mass(self):
        return Utils.convert_float_to_sf(self.mass)

    def get_sha1sum(self):
        return self.sha1sum

    def get_retention_time_formatted_string(self):
        return Utils.format_time_string(self.get_retention_time())

    def get_retention_time_formatted_datetime(self):
        return Utils.format_time_datetime(self.get_retention_time())

    def get_retention_time_hr_int(self):
        return Utils.format_time_hr_int(self.get_retention_time())

    def get_retention_time_min_int(self):
        return Utils.format_time_min_int(self.get_retention_time())

    def get_retention_time(self):
        return self.retentiontime

    def get_intensity(self):
        return Utils.convert_float_to_sf(self.intensity)

    def get_nr_peaks(self):
        return round(len(self.peaks))

    def get_peak_data(self):
        return self.peak_data

    def get_measurementid(self):
        return self.measurementid

    def get_checked(self):
        return self.checked

    def set_checked(self, checked):
        self.checked = checked