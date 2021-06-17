from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterSort(Filter):
    def __init__(self, sort_type):
        Filter.__init__(self, Enums.FilterType.FilterSort)
        self.sort_type = sort_type

    def get_filter_sort_type_value(self):
        return "Peak sort"

    def get_filter_sort_settings_value(self):
        return self.sort_type

    def apply_filter_sort_to_peak_list(self, peak_list):
        return peak_list