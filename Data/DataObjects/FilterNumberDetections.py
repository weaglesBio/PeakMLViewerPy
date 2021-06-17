from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterNumberDetections(Filter):
    def __init__(self, detection_number):
        Filter.__init__(self, Enums.FilterType.FilterNumberDetections)
        self.detection_number = detection_number

    def get_filter_number_detections_type_value(self):
        return "Number of detections"

    def get_filter_number_detections_settings_value(self):
        return self.detection_number

    def apply_filter_number_detections_to_peak_list(self, peak_list):
        filtered_peak_list = []
        for peak in peak_list:
            if int(peak.get_nr_peaks()) == int(self.detection_number):
                filtered_peak_list.append(peak)
        #return [peak for peak in peak_list if peak.get_intensity() > self.intensity_min]
        return filtered_peak_list
