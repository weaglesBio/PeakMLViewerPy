from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterRetentionTime(Filter):
    def __init__(self, range_min, range_max):
        Filter.__init__(self, Enums.FilterType.FilterRetentionTime)
        self.range_min = range_min
        self.range_max = range_max

    def get_filter_retention_time_type_value(self):
        return "Filter Retention Time"

    def get_filter_retention_time_settings_value(self):
        return self.range_min + "-" + self.range_max
    
    def apply_filter_retention_time_to_peak_list(self, peak_list):
        return peak_list