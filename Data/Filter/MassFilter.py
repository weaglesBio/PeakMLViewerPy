from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak

from typing import Dict

class MassFilter(BaseFilter):
    def __init__(self, mass_min: float, mass_max: float): #, formula, formula_ppm, mass_charge, filter_option
        super().__init__(Enums.FilterType.FilterMass)
        self.mass_min = mass_min
        self.mass_max = mass_max
        # self.formula = formula
        # self.formula_ppm = formula_ppm
        # self.mass_charge = mass_charge
        # self.filter_option = filter_option

    def get_type_value(self) -> str:
        return "Mass"

    def get_settings_value(self) -> str:
        #if self.filter_option == "mass":
        return str(self.mass_min) + " - " + str(self.mass_max)
        #elif self.filter_option == "formula":
        #    return str(self.formula) + " - " + str(self.formula_ppm)+ " - " + str(self.mass_charge)

    def apply_to_peak_list(self, peak_dic) -> Dict[str, Peak]:
        filtered_peak_dic = {}
        for peak_uid in peak_dic.keys():   
            peak = peak_dic[peak_uid]

            #if self.filter_option == "mass":
            if float(peak.mass) > float(self.mass_min) and float(peak.mass) < float(self.mass_max):
                filtered_peak_dic[peak_uid] = peak
            #elif self.filter_option == "formula":
            #    if float(peak.get_nr_peaks()) == float(self.formula_ppm):
            #        filtered_peak_list.append(peak)

        return filtered_peak_dic