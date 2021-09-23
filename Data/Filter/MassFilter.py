from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

from typing import Dict

class MassFilter(BaseFilter):
    def __init__(self, mass_min: float, mass_max: float):
        super().__init__(Enums.FilterType.FilterMass)
        self.mass_min = mass_min
        self.mass_max = mass_max

    def get_type_value(self) -> str:
        return "Mass"

    def get_settings_value(self) -> str:
        return str(self.mass_min) + " - " + str(self.mass_max)

    def apply_to_peak_list(self, peak_dic) -> Dict[str, Peak]:
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]

            if float(peak.mass) > float(self.mass_min) and float(peak.mass) < float(self.mass_max):
                filtered_peak_dic[peak_uid] = peak

        return filtered_peak_dic