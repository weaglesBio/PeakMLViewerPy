import Utilities as u
import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.IdentificationItem import IdentificationItem

class IdentificationDataView(BaseDataView):
    def __init__(self):
        super().__init__(['ID','Formula','PPM','Adduct','Name','Class','Description','Prior','Post','Smiles','InChi','Notes'])

    def load_data_for_selected_peak(self, peak, molecule_database):
        try:
            self.clear_datalist()

            iden_ids = []
            iden_ppms = []
            iden_adducts = []
            iden_priors = []
            iden_posts = []

            # Get peak identification of label 'identification', value is multiple ids
            iden_ann = peak.get_specific_annotation('identification')
            if iden_ann:

                # Get list of PPM values from annotation
                iden_ppm = peak.get_specific_annotation('ppm')
                if iden_ppm:
                    iden_ppms = iden_ppm.value.split(', ')

                # Get list of adduct values from annotation
                iden_adduct = peak.get_specific_annotation('adduct')
                if iden_adduct:
                    iden_adducts = iden_adduct.value.split(', ')

                # Get list of prior probability values from annotation
                iden_prior = peak.get_specific_annotation('prior')
                if iden_prior:
                    iden_priors = iden_prior.value.split(', ')

                # Get list of posterior probability values from annotation
                iden_post = peak.get_specific_annotation('post')
                if iden_post:
                    iden_posts = iden_post.value.split(', ')

                # Get list of notes values from annotation
                iden_notes = peak.get_specific_annotation('notes')
                if iden_notes:
                    iden_notes = iden_notes.value.split(', ')

                iden_ids = iden_ann.value.split(', ')
                iden_count = len(iden_ids)

                lg.log_progress(f'{iden_count} identities found.')

                for i in range(iden_count):
                    formula = ""
                    ppm = ""
                    adduct = ""
                    name = ""
                    class_desc = ""
                    description = ""
                    prior = ""
                    post = ""
                    smiles = ""
                    inchi = ""
                    notes = ""

                    id = iden_ids[i]
                    molecule = molecule_database[id]

                    # Populate details from molecule database.
                    if molecule is not None:
                        formula = molecule.formula
                        name = molecule.name
                        class_desc = molecule.class_description if molecule.class_description is not None else ""
                        description = molecule.description if molecule.description is not None else ""
                        smiles = molecule.smiles
                        inchi = molecule.inchi

                    if iden_ppms and len(iden_ppms) > 0:
                        if len(iden_ppms) == 1:
                            ppm = u.convert_float_to_sf(iden_ppms[0])
                        elif i < len(iden_ppms):
                            ppm = u.convert_float_to_sf(iden_ppms[i])

                    if iden_adducts and len(iden_adducts) > 0:
                        if len(iden_adducts) == 1:
                            adduct = iden_adducts[0]
                        elif i < len(iden_adducts):
                            adduct = iden_adducts[i]

                    if iden_priors and len(iden_priors) > 0:
                        if i < len(iden_priors):
                            prior = u.to_float(iden_priors[i])

                    if iden_posts and len(iden_posts) > 0:
                        if i < len(iden_posts):
                            post = u.to_float(iden_posts[i])

                    if iden_notes and len(iden_notes) > 0:
                        if i < len(iden_notes):
                            notes = iden_notes[i]

                    self.add_item(id, formula, ppm, adduct, name, class_desc, description, prior, post, smiles, inchi, notes)

            else:
                lg.log_progress(f'No "identification" annotation found.')

            # Reload dataframe after all added.
            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to load identification data from peakML object: {err}')

    def add_item(self, id, formula, ppm, adduct, name, class_desc, description, prior, post, smiles, inchi, notes):
        self.datalist.append(IdentificationItem(id, formula, ppm, adduct, name, class_desc, description, prior, post, smiles, inchi, notes))

    def refresh_dataframe(self):
        self.clear_dataframe()

        if len(self.datalist) > 0:
            for item in self.datalist:
                self.dataframe = self.dataframe.append({
                                                        "UID": item.uid,
                                                        "ID": item.id,
                                                        "Formula": item.formula,
                                                        "PPM": item.ppm,
                                                        "Adduct": item.adduct,
                                                        "Name": item.name,
                                                        "Class": item.class_desc,
                                                        "Description": item.description,
                                                        "Prior": round(item.prior,2) if item.prior is not None and item.prior != "" else "",
                                                        "Post": round(item.post,2) if item.post is not None and item.post != "" else "",
                                                        "Smiles": item.smiles,
                                                        "InChi": item.inchi,
                                                        "Notes": item.notes,
                                                        "Selected": item.selected,
                                                        "Checked": item.checked,
                                                    }, ignore_index=True)

            # If no items are selected,
            if len(self.dataframe.loc[self.dataframe["Selected"] == True]) == 0:
                # set the first one as selected.
                self.dataframe.at[0, 'Selected'] = True

    def get_details(self, uid):
        row = self.dataframe.loc[self.dataframe["UID"] == uid]
        return uid, row["ID"].values[0], row["Prior"].values[0], row["Notes"].values[0]

    def update_details(self, uid, prior, notes):

        if u.is_float(prior):
            prior_val = float(prior)
        else:
            prior_val = None
        
        prior_changed = False

        for item in self.datalist:
            if item.uid == uid:
                if prior_val != item.prior:
                    prior_changed = True
                
                item.prior = prior_val
                item.notes = notes

                break

        if prior_changed:
            self.recalculate_priors(uid)

        self.refresh_dataframe()

        return prior_changed

    def remove_checked(self, ipa_imported):
        current_list = self.datalist
        amended_list = []
        for item in current_list:
            if item.checked == False:
                amended_list.append(item)

        self.datalist = amended_list

        if ipa_imported:
            self.recalculate_priors(None)

        self.refresh_dataframe()

        # Deletion after IPA import will update prior.
        return ipa_imported

    def check_if_any_checked(self):
        for item in self.datalist:
            if item.checked == True:
                return True

        return False

    def get_identification_annotations(self):

        ann_identification = ", ".join(self.dataframe["ID"].tolist())

        #TODO: Ask if adduct/ppm are always the same for each identification
        #ann_ppm = ", ".join([str(x) for x in self.dataframe["PPM"].tolist()])
        #ann_adduct = ", ".join(self.dataframe["Adduct"].tolist())

        # Returned as stringyfied list with one value as this is how it is stored in the annotation.
        ann_ppm = str(self.dataframe.at[0,"PPM"])
        ann_adduct = str(self.dataframe.at[0,"Adduct"])

        ann_prior = ", ".join([str(x) for x in self.dataframe["Prior"].tolist()])
        ann_post = ", ".join([str(x) for x in self.dataframe["Post"].tolist()])

        ann_notes = ", ".join(self.dataframe["Notes"].tolist())

        return ann_identification, ann_ppm, ann_adduct, ann_prior, ann_post, ann_notes


    def recalculate_priors(self, updated_identification_uid):

        # Need to be able to handle the total being 0.
        updated_item_list = []
        curr_prior_total = 0
        empty_values = 0
        target = 1
        updated_value = 0

        for item in self.datalist:

            if item.uid == updated_identification_uid:
                updated_value = item.prior

            if item.prior is None:
                # Get number of identities without set prior probability
                empty_values += 1
            else:
                # Get total of all priors.
                curr_prior_total += (item.prior if item.prior is not None else 0)

        # If any identification without prior probability values set.
        if empty_values > 0:
            for item in self.datalist:
                updated_item = item

                if item.prior is None:
                    # Update all rows without value with missing prior probability percentage divided between them
                    updated_item.prior = (target - curr_prior_total)/empty_values

                updated_item_list.append(updated_item)

        elif updated_value is None:
            #If updated value is none then deletion has occured so all remaining rows can be used for calculation
            for item in self.datalist:
                updated_item = item

                # Apply adjustment to each prior value.
                updated_item.prior = (target/curr_prior_total)*updated_item.prior

                updated_item_list.append(updated_item)

        else:
            #Update target all other values are adjusting to to account for manually updated. 
            target = 1-updated_value

            for item in self.datalist:
                updated_item = item

                # Apply adjustment to each prior value, aside from updated.
                if item.uid != updated_identification_uid:
                    updated_item.prior = (target/(curr_prior_total-updated_value))*updated_item.prior

                updated_item_list.append(updated_item)

        self.datalist = updated_item_list

        tot_prob = 0
        for item in self.datalist:
            lg.log_progress(f"{item.id} is {item.prior}")
            tot_prob += item.prior

        lg.log_progress(f"Total is {tot_prob}")

        # Check if all other prior values are blank
        # If so set the all to the remaining slices of the pie
        # If a value has been updated remove from the outstanding calculation.
        # It is possible that all values rather than the added are blank.
        # If an edited value sets it 0 it should be set to 0 probability.



