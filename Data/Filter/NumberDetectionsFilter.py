from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

class NumberDetectionsFilter(BaseFilter):
    def __init__(self, detection_number):
        super().__init__(Enums.FilterType.FilterNumberDetections)
        self.detection_number = detection_number

    def get_type_value(self) -> str:
        return "Samples"

    def get_settings_value(self) -> str:
        return self.detection_number

    def apply_to_peak_list(self, peak_dic: dict[str, Peak]) -> dict[str, Peak]:
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]
            if int(round(len(peak.peaks))) == int(self.detection_number):
                filtered_peak_dic[peak_uid] = peak

        return filtered_peak_dic
