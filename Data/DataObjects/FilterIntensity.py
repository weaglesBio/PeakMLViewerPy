from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterIntensity(Filter):
    def __init__(self, intensity_min):
        Filter.__init__(self, Enums.FilterType.FilterIntensity)
        self.intensity_min = intensity_min

    def get_filter_intensity_type_value(self):
        return "Intensity filter"

    def get_filter_intensity_settings_value(self):
        #return str(self.intensity_min) + " (" + str(self.intensity_unit) + ")"
        return str(self.intensity_min)

    def apply_filter_intensity_to_peak_list(self, peak_list):
        filtered_peak_list = []
        for peak in peak_list:
            if float(peak.get_intensity()) > float(self.intensity_min):
                filtered_peak_list.append(peak)
        #return [peak for peak in peak_list if peak.get_intensity() > self.intensity_min]
        return filtered_peak_list