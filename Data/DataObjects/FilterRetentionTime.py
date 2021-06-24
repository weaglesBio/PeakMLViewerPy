from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterRetentionTime(Filter):
    def __init__(self, min_minu, max_minu, min_sec, max_sec):
        Filter.__init__(self, Enums.FilterType.FilterRetentionTime)

        self.min_minu = min_minu
        self.max_minu = max_minu
        self.min_sec = min_sec
        self.max_sec = max_sec

    def get_filter_retention_time_type_value(self):
        return "Filter Retention Time"

    def get_filter_retention_time_settings_value(self):
        return self.min_sec + ":" + self.min_minu + "-" + self.max_sec + ":" + self.max_minu
    
    def apply_filter_retention_time_to_peak_list(self, peak_list):
        filtered_peak_list = []
        for peak in peak_list:
            peak_minute = peak.get_retention_time_min_int()
            peak_second = peak.get_retention_time_sec_int()  
            filter_min_minu = self.min_minu
            filter_max_minu = self.max_minu
            filter_min_sec = self.min_sec
            filter_max_sec = self.max_sec

            #if peak_hour >:

            #if peak_minute:

            #if float(peak.get_intensity()) > float(self.intensity_min):
            #    filtered_peak_list.append(peak)

        return filtered_peak_list