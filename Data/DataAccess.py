import gzip
from xml.dom import minidom
import pandas as pd
import os.path

import IO.PeakMLReader as Read
import IO.PeakMLWriter as Write
import IO.MoleculeIO as MolIO
import IO.SettingsIO as SetIO

from Data.DataObjects.FilterMass import FilterMass
from Data.DataObjects.FilterIntensity import FilterIntensity
from Data.DataObjects.FilterRetentionTime import FilterRetentionTime
from Data.DataObjects.FilterNumberDetections import FilterNumberDetections
from Data.DataObjects.FilterAnnotations import FilterAnnotations
from Data.DataObjects.FilterSort import FilterSort
from Data.DataObjects.FilterSortTimeSeries import FilterSortTimeSeries
from Data.Settings import Settings

import Utilities as Utils

# The purpose of this class is to encapsulate all data access logic, the methods here are the one used by the ui layer
# They should be a specific and descriptive in their naming as possible.

class PeakMLData:

    def __init__(self):
        self.peakMLData = None
        self.peakml_obj = None
        self.filepath = None
        self.molecule_database = None

        self.settings = Settings()

        self.df_entry = pd.DataFrame(columns=['UID','Type','Selected','RT','Mass','Intensity','Nrpeaks','HasAnnotation','Checked'])
        self.df_entry.set_index("UID")
        self.df_filter = pd.DataFrame(columns=['ID','Type','Settings'])
        self.df_plot_peak = pd.DataFrame(columns=['UID','Label','RT_values','Intensity_values','Colour','Selected'])
        self.df_plot_peak.set_index("UID")
        self.df_plot_derivative = pd.DataFrame(columns=['Mass','Intensity','Description'])
        self.df_plot_intensity = pd.DataFrame(columns=['SetID','Intensities'])
        self.df_identification = pd.DataFrame(columns=['ID','Formula','PPM','Adduct','Name','Class','Description','Smiles','InChi'])
        self.df_set = pd.DataFrame(columns=['UID','Name','Color','Selected','Parent'])
        self.df_set.set_index("UID")
        self.df_annotation = pd.DataFrame(columns=['Label','Value'])


    def get_entry_view(self):
        return self.df_entry


    def get_filter_view(self):
        return self.df_filter


    def get_plot_peak_view(self):
        return self.df_plot_peak


    def get_plot_derivative_view(self):
        return self.df_plot_derivative


    def get_plot_intensity_view(self):
        return self.df_plot_intensity


    def get_identification_view(self):
        return self.df_identification


    def get_set_view(self):
        return self.df_set


    def get_annotation_view(self):
        return self.df_annotation


    def get_filepath(self):
        return self.filepath


    def get_path(self):
        return os.path.split(self.filepath)[0]


    def get_filename(self):
        return os.path.split(self.filepath)[1]
        

    def set_filepath(self, filepath):
        self.filepath = filepath


    def set_peakml_obj(self, current_obj):
        self.peakml_obj = current_obj


    def get_peakml_obj(self):
        return self.peakml_obj


    def get_molecule_database(self):
        return self.molecule_database 


    def get_nr_peaks(self):
        return self.peakml_obj.get_nr_peaks()


    def get_total_nr_peaks(self):      
        peak_count = 0
        for peak in self.peakml_obj.peaks:
            if peak.get_type() == 'peakset':
                peak_count += len(peak.peaks)
            else:
                peak_count += 1

        return peak_count


    def set_selected_peak(self, peak_id):
        self.peakml_obj.set_selected_peak_uid(peak_id)


    def get_selected_peak(self):
        return self.peakml_obj.get_selected_peak()


    def load_molecule_databases(self):
        self.molecule_database = MolIO.load_molecule_databases()


    def import_from_filepath(self, filepath):
        self.set_filepath(filepath)

        tree_data = None

        # Files can be gzipped, so if unable to read file directly, a second attempt is made with decompression.
        attempt_compressed = False

        try:
            # If errors while attempt to read, requires conversion.
            with open(filepath) as f:
                tree_data = f.read()
        except:
            attempt_compressed = True
            
        if attempt_compressed:
            try:
                with gzip.open(filepath) as g:
                    tree_data = g.read()
                    tree_data = tree_data.decode()
                    tree_data = tree_data.replace('\n','')
                    tree_data = tree_data.replace('\t','')
                    tree_data = tree_data.encode()

                    ## Section for debugging and testing by comparing decoded version with output version.
                    #md_string = minidom.parseString(tree_data)
                    #decoded_output = md_string.toprettyxml(indent="\t")
                    #decoded_output = decoded_output.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
                    #decoded_output = decoded_output.replace("/>"," />")

                    #w = open(self.get_path() + "decoded_" + self.get_filename(), "w")
                    #w.write(decoded_output)
                    #w.close()
            except Exception as err:
                print("Unable to open compressed file.")
                print(err)

        if tree_data is not None:
            try:
                data_obj = Read.importElementTreeFromPeakMLFile(tree_data, filepath)
                self.set_peakml_obj(data_obj)
            except Exception as err:
                print("Unable to convert file to PeakML class stucture.")
                print(err)


    def export_data_object_to_file(self, filepath):

        data_obj = self.get_peakml_obj()
        xml_string = Write.create_xml_from_peakml(data_obj)

        r = open(filepath, "w")
        r.write(xml_string)
        r.close()


    def update_entry_dataframe(self):
        try:
            self.df_entry = self.df_entry.iloc[0:0]

            for peak in self.get_peakml_obj().get_filtered_peaks():
                has_annotation = True if peak.get_specific_annotation('identification') else False
                self.df_entry = self.df_entry.append({"UID": peak.get_uid(), "Type": peak.get_type(), "Selected": peak.if_patternid_set(), "RT": peak.get_retention_time_formatted_string(), "Mass": peak.get_mass(), "Intensity": peak.get_intensity(), "Nrpeaks": peak.get_nr_peaks(), "HasAnnotation": has_annotation, "Checked": peak.get_checked()}, ignore_index=True)
        except Exception as err:
            print("Unable to update entry data")
            print(err)

    def get_filters_list(self):
        self.df_filter = self.df_filter.iloc[0:0]
        for filter in self.get_peakml_obj().get_filters():
            self.df_filter = self.df_filter.append({"ID": filter.get_id_str(), "Type": filter.get_type_value(), "Settings": filter.get_settings_value()}, ignore_index=True)

        return self.df_filter


    # Returns the peak with one of the given list of measurement id's
    def get_peaks_with_measurementids(self, peaks, measurementids):

        measurement_peaks = []

        for peak in peaks:
            peak_has_measurement = False

            peak_data = peak.get_peak_data()
            peak_data_measurementids = peak_data.get_measurementids()

            for peak_data_measurementid in peak_data_measurementids:
                for measurementid in measurementids:
                    if peak_data_measurementid == measurementid:
                        peak_has_measurement = True

            if peak_has_measurement:      
                measurement_peaks.append(peak)

        return measurement_peaks

    def update_plot_data_frames_for_selected_entry(self):
        # Get current peakset
        selected_peakset = self.get_peakml_obj().get_selected_peak()

        #Clear data frames
        self.df_plot_peak = self.df_plot_peak.iloc[0:0]
        self.df_plot_derivative = self.df_plot_derivative.iloc[0:0]
        self.df_plot_intensity = self.df_plot_intensity.iloc[0:0]

         # Plot peak dataframe
        try:
            for peak in selected_peakset.peaks:

                measurement = self.get_peakml_obj().header.get_measurement_by_id(peak.measurementid)
                uid = measurement.get_uid()
                label = measurement.label
                rt_values = peak.peak_data.get_retention_times_formatted_datetime()
                intensity_values = peak.peak_data.get_intensities() 

                colour = measurement.get_colour()
                selected = measurement.get_selected() 

                self.df_plot_peak = self.df_plot_peak.append({"UID": uid,"Label": label, "RT_values": rt_values, "Intensity_values": intensity_values, "Colour" : colour, "Selected" : selected }, ignore_index=True)
        except Exception as err:
            print("Unable to update plot peak data")
            print(err)

        # Plot derivative dataframe
        try:
            peakset_annotation_relationid = self.get_peakml_obj().get_selected_peak().get_specific_annotation('relation.id')

            related_peaks = []

            for peak in self.get_peakml_obj().peaks:
                peak_annotation_relationid = peak.get_specific_annotation('relation.id')

                if peak_annotation_relationid:
                    if peakset_annotation_relationid.value == peak_annotation_relationid.value:
                        related_peaks.append(peak)
                
            for rel_peak in related_peaks:

                mass = rel_peak.get_mass()
                intensity = rel_peak.get_intensity()

                ann_relation = rel_peak.get_specific_annotation('relation.ship')
                ann_reaction = rel_peak.get_specific_annotation('reaction')

                if ann_reaction:
                    description = ann_reaction.value
                elif ann_relation:
                    description = ann_relation.value
                else:
                    description = ""
                
                self.df_plot_derivative = self.df_plot_derivative.append({"Mass": float(mass), "Intensity": float(intensity), "Description": description}, ignore_index=True)
        except Exception as err:
            print("Unable to update plot derivative data")
            print(err)

        # Plot intensity dataframe
        try:           
            peaks = selected_peakset.peaks

            for set in self.get_peakml_obj().header.get_sets():
                
                # Get all the peaks for the set.
                measurement_peaks = self.get_peaks_with_measurementids(peaks, set.get_measurementids())

                intensities = []
                for measurement_peak in measurement_peaks:
                    intensities.append(measurement_peak.get_intensity())

                self.df_plot_intensity = self.df_plot_intensity.append({"SetID": set.get_id(), "Intensities": intensities}, ignore_index=True)
        except Exception as err:
            print("Unable to update plot intensity data")
            print(err)


    def update_data_frames_for_selected_entry(self):
        # Get molecule database
        molecule_database = self.get_molecule_database()

        # Get current peakset
        selected_peakset = self.get_peakml_obj().get_selected_peak()

        #Clear data frames
        self.df_identification = self.df_identification.iloc[0:0]
        self.df_set = self.df_set.iloc[0:0]
        self.df_annotation = self.df_annotation.iloc[0:0]

        # Identification dataframe
        try:
            identification_ids = []
            identification_ppms = []
            identification_adducts = []

            identification_ppm = selected_peakset.get_specific_annotation('ppm')
            if identification_ppm:
                identification_ppms = identification_ppm.value.split(', ')

            identification_adduct = selected_peakset.get_specific_annotation('adduct')
            if identification_adduct:
                identification_adducts = identification_adduct.value.split(', ')

            ppm = ""
            adduct = ""

            # Get peak identification of label 'identification', value is multiple ids
            identification_annotation = selected_peakset.get_specific_annotation('identification')
            if identification_annotation:
                identification_ids = identification_annotation.value.split(', ')

                for i in range(len(identification_ids)):
                
                    id = identification_ids[i]
                    molecule = molecule_database[id]

                    if identification_ppms and len(identification_ppms) > 0:
                        if i < len(identification_ppms):
                            ppm = Utils.convert_float_to_sf(identification_ppms[i])

                    if identification_adducts and len(identification_adducts) > 0:
                        if i < len(identification_adducts):
                            adduct = identification_adducts[i]

                    mol_formula = str(molecule.get_formula())
                    mol_name = molecule.get_name()
                    mol_classdesc = molecule.get_class_description()
                    mol_desc = molecule.get_description()
                    mol_smiles = molecule.get_smiles()
                    mol_inchi = molecule.get_inchi()

                    self.df_identification = self.df_identification.append({"ID": id, "Formula": mol_formula, "PPM": ppm, "Adduct": adduct, "Name": mol_name, "Class": mol_classdesc, "Description": mol_desc , "Smiles": mol_smiles, "InChi": mol_inchi}, ignore_index=True)
            
        except Exception as err:
            print("Unable to update identification data")
            print(err)

        # Set dataframe
        try:
            # Set measurement colours from sets
            for set_info in self.get_peakml_obj().header.get_sets():

                self.df_set = self.df_set.append({"UID": set_info.get_uid(), "Name": set_info.get_id(), "Color": set_info.get_colour(), "Selected": set_info.get_selected(), "Parent": None}, ignore_index=True)

                measurement_peaks = self.get_peaks_with_measurementids(selected_peakset.peaks, set_info.get_measurementids())

                for measurement_peak in measurement_peaks:
                    measurement = self.get_peakml_obj().header.get_measurement_by_id(measurement_peak.get_measurementid())

                    measurement.set_colour(set_info.get_colour())
                    
                    self.df_set = self.df_set.append({"UID": measurement.get_uid(), "Name": measurement.get_label(), "Color": set_info.get_colour(), "Selected": measurement.get_selected(), "Parent": set_info.get_id()}, ignore_index=True)
                
        except Exception as err:
            print("Unable to update set data")
            print(err)

        # Annotation dataframe
        try:
            for annotation in selected_peakset.get_annotations():
                self.df_annotation = self.df_annotation.append({"Label": annotation.get_label(), "Value": annotation.get_value()}, ignore_index=True)
        except Exception as err:
            print("Unable to update annotation data")
            print(err)

    def update_set_selection(self, measurement_uid, selected):
        measurement = self.get_peakml_obj().header.get_measurement_by_uid(measurement_uid)
        measurement.set_selected(selected)
        self.df_plot_peak.at[self.df_plot_peak.index[self.df_plot_peak["UID"] == measurement_uid].tolist()[0], 'Selected'] = selected


    def add_filter_mass(self, mass_min, mass_max, formula, formula_ppm, mass_charge, filter_option):
        self.get_peakml_obj().add_filter(FilterMass(mass_min, mass_max, formula, formula_ppm, mass_charge, filter_option))


    def add_filter_intensity(self, intensity_min):
        self.get_peakml_obj().add_filter(FilterIntensity(intensity_min))


    def add_filter_retention_time(self, retention_time_min_hr, retention_time_max_hr, retention_time_min_minu, retention_time_max_minu):
        self.get_peakml_obj().add_filter(FilterRetentionTime(retention_time_min_hr, retention_time_max_hr, retention_time_min_minu, retention_time_max_minu))


    def add_filter_number_detections(self, detection_number):
        self.get_peakml_obj().add_filter(FilterNumberDetections(detection_number))


    def add_filter_annotations(self, annotation_name, annotation_relation, annotation_value):
        self.get_peakml_obj().add_filter(FilterAnnotations(annotation_name, annotation_relation, annotation_value))


    def add_filter_sort(self):
        print("Not implemented")


    def add_filter_sort_times_series(self):
        print("Not implemented")


    def remove_filter_by_id(self, id):
        self.get_peakml_obj().remove_filter_by_id(id)


    def get_settings_preference_by_name(self, name):
        return self.settings.get_preference_by_name(name)


    def get_settings_database_paths(self):
        database_paths = self.settings.get_database_paths()
        df = pd.DataFrame()
        for path in database_paths:
            head, tail = os.path.split(path)
            df = df.append({"Name": tail, "Path": path}, ignore_index=True)

        return df

    def update_settings(self, decdp, databases):

        self.settings.set_preference_by_name("decdp", decdp)
        self.settings.set_database_paths(databases["Path"].tolist())
        SetIO.write_settings(self.settings)