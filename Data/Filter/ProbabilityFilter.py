from Data.Filter.BaseFilter import BaseFilter
import Data.Enums as Enums
from Data.PeakML.Peak import Peak
import Utilities as u
from typing import Dict

class ProbabilityFilter(BaseFilter):
    def __init__(self, prior_min: str, prior_max: str, post_min: str, post_max: str):
        super().__init__(Enums.FilterType.FilterProbability)

        if prior_min is None or prior_min == "":
            self.prior_min = '0.0'
        else:
            self.prior_min = prior_min

        if prior_max is None or prior_max == "":
            self.prior_max = '1.0'
        else:
            self.prior_max = prior_max

        if post_min is None or post_min == "":
            self.post_min = '0.0'
        else:
            self.post_min = post_min

        if post_max is None or post_max == "":
            self.post_max = '1.0'
        else:
            self.post_max = post_max

    def get_type_value(self) -> str:
        return "Probability"

    def get_settings_value(self) -> str:
        return f"Prior: {self.prior_min}-{self.prior_max}; Post: {self.post_min}-{self.post_max}" 

    def apply_to_peak_list(self, peak_dic) -> Dict[str, Peak]:
        
            prior_min = float(self.prior_min)
            prior_max = float(self.prior_max)
            post_min = float(self.post_min)
            post_max = float(self.post_max)

            filtered_peak_dic = {}
            peak_num = 0
            for peak_uid in peak_dic.keys():   
                peak = peak_dic[peak_uid]
                peak_num += 1
                priors = []
                posts = []

                prior_ann = peak.get_specific_annotation("prior")
                post_ann = peak.get_specific_annotation("post")

                if prior_ann is not None:
                    priors = prior_ann.value.split(", ")

                if post_ann is not None:
                    posts = post_ann.value.split(", ")
            
                in_prior = False
                for prior in priors:
                    prior_f = float(prior)
                    if prior_min < prior_f and prior_max > prior_f:
                        in_prior = True
                        break
                
                in_post = False
                for post in posts:
                    post_f = float(post)
                    if post_min < post_f and post_max > post_f:
                        in_post = True
                        break

                if in_prior and in_post:
                    filtered_peak_dic[peak_uid] = peak

            return filtered_peak_dic