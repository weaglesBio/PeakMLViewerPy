import Utilities as Utils
import Data.Enums as Enums

class BaseFilter():
    def __init__(self, filter_type: Enums.FilterType):

        self._uid = Utils.get_new_uuid()
        self._type = filter_type

    @property
    def uid(self) -> str:
        return self._uid

    #def get_type_value(self):
        # if self._type == Enums.FilterType.FilterMass:
        #     return self.get_filter_mass_type_value()
        # elif self._type == Enums.FilterType.FilterIntensity:
        #     return self.get_filter_intensity_type_value()
        # elif self._type == Enums.FilterType.FilterRetentionTime:
        #     return self.get_filter_retention_time_type_value()
        # elif self._type == Enums.FilterType.FilterNumberDetections:
        #     return self.get_filter_number_detections_type_value()
        # elif self._type == Enums.FilterType.FilterAnnotations:
        #     return self.get_filter_annotations_type_value()
        # elif self._type == Enums.FilterType.FilterSort:
        #     return self.get_filter_sort_type_value()
        # elif self._type == Enums.FilterType.FilterSortTimeSeries:
        #     return self.get_filter_sort_time_series_type_value()

    #def get_settings_value(self):
        # if self._type == Enums.FilterType.FilterMass:
        #     return self.get_filter_mass_settings_value()
        # elif self._type == Enums.FilterType.FilterIntensity:
        #     return self.get_filter_intensity_settings_value()
        # elif self._type == Enums.FilterType.FilterRetentionTime:
        #     return self.get_filter_retention_time_settings_value()
        # elif self._type == Enums.FilterType.FilterNumberDetections:
        #     return self.get_filter_number_detections_settings_value()
        # elif self._type == Enums.FilterType.FilterAnnotations:
        #     return self.get_filter_annotations_settings_value()
        # elif self._type == Enums.FilterType.FilterSort:
        #     return self.get_filter_sort_settings_value()
        # elif self._type == Enums.FilterType.FilterSortTimeSeries:
        #     return self.get_filter_sort_time_series_settings_value()

    #def apply_filter_to_peak_list(self, peak_list):
        # if self._type == Enums.FilterType.FilterMass:
        #     return self.apply_filter_mass_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterIntensity:
        #     return self.apply_filter_intensity_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterRetentionTime:
        #     return self.apply_filter_retention_time_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterNumberDetections:
        #     return self.apply_filter_number_detections_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterAnnotations:
        #     return self.apply_filter_annotations_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterSort:
        #     return self.apply_filter_sort_to_peak_list(peak_list)
        # elif self._type == Enums.FilterType.FilterSortTimeSeries:
        #     return self.apply_filter_sort_time_series_to_peak_list(peak_list)