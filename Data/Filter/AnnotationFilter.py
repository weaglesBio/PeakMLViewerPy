from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

class AnnotationFilter(BaseFilter):
    def __init__(self, annotation_name: str, annotation_relation: str, annotation_value: str):
        super().__init__(Enums.FilterType.FilterAnnotations)
        self.annotation_name = annotation_name
        self.annotation_relation = annotation_relation
        self.annotation_value = annotation_value

    def get_filter_annotations_type_value(self) -> str:
        return "Filter annotations"

    def get_filter_annotations_settings_value(self) -> str:
        return " ".join(["" if self.annotation_name is None else self.annotation_name, "" if self.annotation_relation is None else self.annotation_relation, "" if self.annotation_value is None else self.annotation_value])

    def apply_filter_annotations_to_peak_list(self, peak_dic: dict[str, Peak]) -> dict[str, Peak]:
        return peak_dic