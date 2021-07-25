import rdata
import Logger as lg
from Data.PeakML.Annotation import Annotation


def import_ipa_rdata_from_filepath(filepath, peakml_peaks):
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
                        adduct_values.append(annot_entry[(2*entry_num)+row_num])
                        ppm_values.append(annot_entry[(5*entry_num)+row_num])

                    prior_values.append(annot_entry[(7*entry_num)+row_num])
                    post_values.append(annot_entry[(8*entry_num)+row_num])

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