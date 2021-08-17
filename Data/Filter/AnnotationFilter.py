from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

from typing import Dict

class AnnotationFilter(BaseFilter):
    def __init__(self, annotation_name: str, annotation_relation: str, annotation_value: str):
        super().__init__(Enums.FilterType.FilterAnnotations)
        self.annotation_name = annotation_name
        self.annotation_relation = annotation_relation
        self.annotation_value = annotation_value

    def get_filter_annotations_type_value(self) -> str:
        return "Filter annotations"

    def get_filter_annotations_settings_value(self) -> str:
        return f"{self.annotation_name} {self.annotation_relation} {self.annotation_value}"

    def apply_to_peak_list(self, peak_dic: Dict[str, Peak]) -> Dict[str, Peak]:
        filtered_peak_dic = {}

        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]

            for ann in peak.annotations:
                
                if ann.label == self.annotation_name:

                    # More than
                    if self.annotation_relation == ">":
                        if ann.value > self.annotation_value:
                            filtered_peak_dic[peak_uid] = peak

                    # Less than
                    elif self.annotation_relation == "<":
                        if ann.value < self.annotation_value:
                            filtered_peak_dic[peak_uid] = peak

                    elif self.annotation_relation == "=":
                        if ann.value == self.annotation_value:
                            filtered_peak_dic[peak_uid] = peak

                    elif self.annotation_relation == "like":
                        if ann.value.contains(self.annotation_value):
                            filtered_peak_dic[peak_uid] = peak

        return filtered_peak_dic