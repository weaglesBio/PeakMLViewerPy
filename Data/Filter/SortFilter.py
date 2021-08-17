from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak
from Data.PeakML.Header import Header

import Utilities as u

from typing import Dict

class SortFilter(BaseFilter):
    def __init__(self, sort_type: str, sort_direction: str):
        super().__init__(Enums.FilterType.FilterSort)
        self.sort_type = sort_type
        self.sort_direction = sort_direction

    def get_type_value(self) -> str:
        return "Peak sort"

    def get_settings_value(self) -> str:
        return f"{self.sort_type} {self.sort_direction}"

    def apply_to_peak_list(self, peak_dic: Dict[str, Peak]) -> Dict[str, Peak]:
        
        # Python dictionaries maintain order by default

        if self.sort_direction == "ASC":
            reverse_sort = False
        elif self.sort_direction == "DESC":
            reverse_sort = True

        if self.sort_type == "Mass":
            sort_peak_dic = dict(sorted(peak_dic.items(), key = lambda x: float(x[1].mass), reverse=reverse_sort))
        elif self.sort_type == "Retention Time":
            sort_peak_dic = dict(sorted(peak_dic.items(), key = lambda x: float(x[1].retention_time), reverse=reverse_sort))
        elif self.sort_type == "Intensity":
            sort_peak_dic = dict(sorted(peak_dic.items(), key = lambda x: float(x[1].intensity), reverse=reverse_sort))
        elif self.sort_type == "Sample Count":
            sort_peak_dic = dict(sorted(peak_dic.items(), key = lambda x: len(x[1].peaks), reverse=reverse_sort))

        return sort_peak_dic