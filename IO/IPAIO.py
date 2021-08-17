import rdata
import pandas as pd
import pyreadr as pr

import Logger as lg
from Data.PeakML.Annotation import Annotation
from Data.PeakML.Peak import Peak

from typing import Dict

def import_ipa_rdata_from_filepath(filepath: str, peakml_peaks: Dict[str, Peak]):
    try:
        parsed = rdata.parser.parse_file(filepath)
        converted = rdata.conversion.convert(parsed)
        annot_dict = converted.get('Final.res')

        for peak_key in peakml_peaks.keys():
            peak = peakml_peaks[peak_key]
            id = peak.get_specific_annotation('id')

            annot_entry = annot_dict.get(id.value)

            if annot_entry and len(annot_entry) > 0:
                entry_num = int(len(annot_entry)/9)

                iden_values = []
                adduct_values = []
                ppm_values = []
                prior_values = []
                post_values = []

                for i in range(entry_num):
                    row_num = int(i)
                    iden_entry = annot_entry[(0*entry_num)+row_num]
                    iden_values.append(iden_entry)

                    if iden_entry != "unknown":
                        adduct_value = annot_entry[(2*entry_num)+row_num]
                        if adduct_value:
                            adduct_values.append(adduct_value)
                        else:
                            adduct_values.append("")

                        ppm_value = annot_entry[(5*entry_num)+row_num]
                        if ppm_value:
                            ppm_values.append(ppm_value)
                        else:
                            ppm_values.append("")

                    prior_value = annot_entry[(7*entry_num)+row_num]
                    if prior_value:
                        prior_values.append(prior_value)
                    else:
                        prior_values.append("")

                    post_value = annot_entry[(8*entry_num)+row_num]
                    if post_value:
                        post_values.append(post_value)
                    else:
                        post_values.append("")

                update_annotation(peak, 'identification', ", ".join(iden_values))
                update_annotation(peak, 'adduct', ", ".join(adduct_values))
                update_annotation(peak, 'ppm', ", ".join(ppm_values))
                update_annotation(peak, 'prior', ", ".join(prior_values))
                update_annotation(peak, 'post', ", ".join(post_values))
                
    except Exception as err:
        lg.log_error(f'Error importing IPA file: {err}')

def update_annotation(parent, ann_label, ann_value):
    if parent.get_specific_annotation(ann_label):
        parent.update_specific_annotation(ann_label, ann_value)  
    else:
        parent.add_annotation(Annotation("", "", ann_label, ann_value, "STRING"))

# Export inputs for 'hits'
def export_ipa_input_data(export_filepath: str, peakml_peaks: list[Peak]):
    try:
        df = pd.DataFrame(columns=["m/z","RT","Int","relation.id","id"])

        for peak in peakml_peaks:

            peak_mass = float(peak.mass)
            peak_retention_time = float(peak.retention_time)
            peak_intensity = float(peak.intensity)
            peak_relation_id = int(peak.get_specific_annotation("relation.id").value)
            peak_id = int(peak.get_specific_annotation("id").value)

            df = df.append({"m/z": peak_mass, "RT": peak_retention_time, "Int": peak_intensity, "relation.id": peak_relation_id, "id": peak_id}, ignore_index=True)

        pr.write_rdata(export_filepath, df, df_name="dataset")

    except Exception as err:
        lg.log_error(f'Error exporting entries file for IPA: {err}')

# Export inputs for 'priors'
def export_ipa_input_priors_data(export_filepath: str, peakml_peaks: list[Peak]):
    try:
        df = pd.DataFrame(columns=["Mass_ID","Molecule_ID","Prior"])

        for peak in peakml_peaks:

            id_ann = peak.get_specific_annotation("id")

            identification_ann = peak.get_specific_annotation("identification")
            if identification_ann is not None:
                identifications = identification_ann.value.split(", ")

            prior_ann = peak.get_specific_annotation("prior")
            if prior_ann is not None:
                priors = prior_ann.value.split(", ")

            for i in range(len(identifications)):
                df = df.append({"Mass_ID": id_ann.value, "Molecule_ID": identifications[i], "Prior": priors[i]}, ignore_index=True)

        pr.write_rdata(export_filepath, df, df_name="dataset")

    except Exception as err:
        lg.log_error(f'Error exporting exporting priors file for IPA: {err}')
