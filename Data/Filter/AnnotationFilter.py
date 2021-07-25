from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums

class AnnotationFilter(BaseFilter):
    def __init__(self, annotation_name, annotation_relation, annotation_value):
        super().__init__(Enums.FilterType.FilterAnnotations)
        self.annotation_name = annotation_name
        self.annotation_relation = annotation_relation
        self.annotation_value = annotation_value

    def get_filter_annotations_type_value(self):
        return "Filter annotations"

    def get_filter_annotations_settings_value(self):
        return " ".join(["" if self.annotation_name is None else self.annotation_name, "" if self.annotation_relation is None else self.annotation_relation, "" if self.annotation_value is None else self.annotation_value])

    def apply_filter_annotations_to_peak_list(self, peak_list):
        return peak_list