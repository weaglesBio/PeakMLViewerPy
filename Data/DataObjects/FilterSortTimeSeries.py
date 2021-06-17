from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterSortTimeSeries(Filter):
    def __init__(self):
        Filter.__init__(self, Enums.FilterType.FilterSortTimeSeries)

    def get_filter_sort_time_series_type_value(self):
        return ""

    def get_filter_sort_time_series_settings_value(self):
        return ""

    def apply_filter_sort_time_series_to_peak_list(self, peak_list):
        return peak_list