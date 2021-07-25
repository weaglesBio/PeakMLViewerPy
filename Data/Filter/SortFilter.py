from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

#TODO IMPLEMENT


class SortFilter(BaseFilter):
    def __init__(self, sort_type):
        super().__init__(Enums.FilterType.FilterSort)
        self.sort_type = sort_type

    def get_type_value(self) -> str:
        return "Peak sort"

    def get_settings_value(self) -> str:
        return self.sort_type

    def apply_peak_list(self, peak_list):
        return peak_list