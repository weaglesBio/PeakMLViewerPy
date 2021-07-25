from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak
import Utilities as u

class RetentionTimeFilter(BaseFilter):
    def __init__(self, min_minu, max_minu, min_sec, max_sec):
        super().__init__(Enums.FilterType.FilterRetentionTime)

        self.min_minu = min_minu
        self.max_minu = max_minu
        self.min_sec = min_sec
        self.max_sec = max_sec

    def get_type_value(self):
        return "Retention Time"

    def get_settings_value(self):
        return self.min_sec + ":" + self.min_minu + "-" + self.max_sec + ":" + self.max_minu
    
    def apply_to_peak_list(self, peak_dic):
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]
            peak_time = u.format_time_string(peak.retention_time)
            peak_time_split = peak_time.split(":")
            peak_minute = int(peak_time_split[0])
            peak_second = int(peak_time_split[1])
            filter_min_minu = int(self.min_minu)
            filter_max_minu = int(self.max_minu)
            filter_min_sec = int(self.min_sec)
            filter_max_sec = int(self.max_sec)

            # If is greater than minimum minute and less than maximum minute
            if filter_min_minu < peak_minute and filter_max_minu > peak_minute:
                filtered_peak_dic[peak_uid] = peak
            # If equal to maximum minutes, is less than max seconds.
            elif filter_max_minu == peak_minute and filter_max_sec >= peak_second:
                filtered_peak_dic[peak_uid] = peak
            # If equal to minimum minutes, is greater than min seconds seconds.
            elif filter_min_minu == peak_minute and filter_min_sec <= peak_second:
                filtered_peak_dic[peak_uid] = peak

        return filtered_peak_dic