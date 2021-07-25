from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak


#TODO IMPLEMENT

class SortTimeSeriesFilter(BaseFilter):
    def __init__(self):
        super().__init__(Enums.FilterType.FilterSortTimeSeries)

    def get_filter_sort_time_series_type_value(self):
        return ""

    def get_filter_sort_time_series_settings_value(self):
        return ""

    def apply_filter_sort_time_series_to_peak_list(self, peak_list):
        return peak_list