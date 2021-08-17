from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

from typing import Dict

class IntensityFilter(BaseFilter):
    def __init__(self, intensity_min: float):
        super().__init__(Enums.FilterType.FilterIntensity)
        self.intensity_min = intensity_min

    def get_type_value(self) -> str:
        return "Intensity"

    def get_settings_value(self) -> str:
        return f">{self.intensity_min}"

    def apply_to_peak_list(self, peak_dic: Dict[str, Peak]) -> Dict[str, Peak]:
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]
            if float(peak.intensity) > float(self.intensity_min):
                filtered_peak_dic[peak_uid] = peak
        return filtered_peak_dic