from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak
from Data.PeakML.Annotation import Annotation
from scipy.stats import pearsonr

from typing import Dict, List

class SortTimeSeriesFilter(BaseFilter):
    def __init__(self, set_values: List[float]):
        super().__init__(Enums.FilterType.FilterSortTimeSeries)
        self.set_values = set_values

    def get_type_value(self) -> str:
        return "Sort time-series"

    def get_settings_value(self) -> str:
        return f"DESC by annotation"

    def apply_to_peak_list(self, peak_dic: Dict[str, Peak]) -> Dict[str, Peak]:
        sort_peak_dic = {}

        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]
            
            # Calculate pearsons correlation between series set by filter and that calculated for this peak
            correlation, _ = pearsonr(peak.set_intensities, self.set_values)

            # Save to peak annotation
            ts_ann = peak.get_specific_annotation("timeseries.correlation")
            if ts_ann:
                ts_ann.value = str(correlation)
            else:
                peak.add_annotation(Annotation(label = "timeseries.correlation", value = str(correlation), value_type = "STRING"))

        # Then sort by this annotation value descending.
        sort_peak_dic = dict(sorted(peak_dic.items(), key = lambda x: x[1].get_specific_annotation("timeseries.correlation").value, reverse=True))

        return sort_peak_dic