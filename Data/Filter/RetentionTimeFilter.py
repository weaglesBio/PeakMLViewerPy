from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak
import Utilities as u

from typing import Dict

class RetentionTimeFilter(BaseFilter):
    def __init__(self, min_sec: int, max_sec: int, min_minu: int, max_minu: int):
        super().__init__(Enums.FilterType.FilterRetentionTime)

        self.min_minu = min_minu
        self.max_minu = max_minu
        self.min_sec = min_sec
        self.max_sec = max_sec

    def get_type_value(self) -> str:
        return "Retention Time"

    def get_settings_value(self) -> str:
        return f"{self.min_minu}:{self.min_sec}-{self.max_minu}:{self.max_sec}"
    
    def apply_to_peak_list(self, peak_dic: Dict[str, Peak]) -> Dict[str, Peak]:
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   

            peak = peak_dic[peak_uid]
            peak_time = u.format_time_string(peak.retention_time)
            peak_time_split = peak_time.split(":")
            peak_minute = int(peak_time_split[0])
            peak_second = int(peak_time_split[1])

            # If is greater than minimum minute and less than maximum minute
            if self.min_minu < peak_minute and self.max_minu > peak_minute:
                filtered_peak_dic[peak_uid] = peak
            # If equal to maximum minutes, is less than max seconds.
            elif self.max_minu == peak_minute and self.max_sec >= peak_second:
                filtered_peak_dic[peak_uid] = peak
            # If equal to minimum minutes, is greater than min seconds seconds.
            elif self.min_minu == peak_minute and self.min_sec <= peak_second:
                filtered_peak_dic[peak_uid] = peak

        return filtered_peak_dic