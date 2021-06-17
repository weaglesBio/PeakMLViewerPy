from Data.DataObjects.Filter import Filter
import Data.Enums as Enums

class FilterMass(Filter):
    def __init__(self, mass_min, mass_max, formula, formula_ppm, mass_charge, filter_option):
        Filter.__init__(self, Enums.FilterType.FilterMass)
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.formula = formula
        self.formula_ppm = formula_ppm
        self.mass_charge = mass_charge
        self.filter_option = filter_option

    def get_filter_mass_type_value(self):
        return "Mass filter"

    def get_filter_mass_settings_value(self):
        if self.filter_option == "mass":
            return str(self.mass_min) + " - " + str(self.mass_max)
        elif self.filter_option == "formula":
            return str(self.formula) + " - " + str(self.formula_ppm)+ " - " + str(self.mass_charge)

    def apply_filter_mass_to_peak_list(self, peak_list):
        filtered_peak_list = []
        for peak in peak_list:

            if self.filter_option == "mass":
                if float(peak.get_mass()) > float(self.mass_min) and float(peak.get_mass()) < float(self.mass_max):
                    filtered_peak_list.append(peak)
            elif self.filter_option == "formula":
                if float(peak.get_nr_peaks()) == float(self.formula_ppm):
                    filtered_peak_list.append(peak)

        return filtered_peak_list