from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterRetentionTime(Filter):
    def __init__(self, min_hr, max_hr, min_minu, max_minu):
        Filter.__init__(self, Enums.FilterType.FilterRetentionTime)
        self.min_hr = min_hr
        self.max_hr = max_hr
        self.min_minu = min_minu
        self.max_minu = max_minu

    def get_filter_retention_time_type_value(self):
        return "Filter Retention Time"

    def get_filter_retention_time_settings_value(self):
        return self.min_hr + ":" + self.min_minu + "-" + self.max_hr + ":" + self.max_minu
    
    def apply_filter_retention_time_to_peak_list(self, peak_list):
        filtered_peak_list = []
        for peak in peak_list:
            peak_hour = peak.get_retention_time_hr_int()  
            peak_minute = peak.get_retention_time_min_int()
            filter_min_hr = self.min_hr
            filter_max_hr = self.max_hr
            filter_min_minu = self.min_minu
            filter_max_minu = self.max_minu

            #if peak_hour >:

            #if peak_minute:

            #if float(peak.get_intensity()) > float(self.intensity_min):
            #    filtered_peak_list.append(peak)

        return filtered_peak_list