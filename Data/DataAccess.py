from Data.DataObjects.PeakColour import PeakColour
from numpy.lib.twodim_base import mask_indices
import IO.MoleculeIO
import gzip
from xml.dom import minidom
import pandas as pd
import os.path

import IO.PeakMLReader as Read
import IO.PeakMLWriter as Write
import IO.MoleculeIO as MolIO

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
        self.peakml_obj.set_selected_peak(peak_id)

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
                print(err)

        if tree_data is not None:
            try:
                data_obj = Read.importElementTreeFromPeakMLFile(tree_data, filepath)
                self.set_peakml_obj(data_obj)
            except Exception as err:
                print("Unable to convert file to PeakML class stucture.")
                print(err)

    def export_data_object_to_file(self, filepath):

        head, tail = os.path.split(filepath)

        data_obj = self.get_peakml_obj()

        print("Generating output xml")
        xml_string = Write.create_xml_from_peakml(data_obj)

        print("Saving XML...")
        r = open(head + tail, "w")
        r.write(xml_string)
        r.close()
        print("XML Saved")

        # use panda dataframe for data - better than current object structure for queries?
        # Will need to examine the complexity of the required queries.

    def get_entry_list(self):

        df = pd.DataFrame()

        for peak_obj in self.get_peakml_obj().get_filtered_peaks():

            selected = peak_obj.if_patternid_set()
            
            sha1sum = peak_obj.get_sha1sum()
            scanid = peak_obj.get_scanid()
            type = peak_obj.get_type()
            rt = peak_obj.get_retention_time_formatted_string()
            mass = peak_obj.get_mass()
            intensity = peak_obj.get_intensity()
            nr_peaks = peak_obj.get_nr_peaks()
            checked = peak_obj.get_checked()

            if peak_obj.get_specific_annotation('identification'):
                has_annotation = True
            else:
                has_annotation = False

            df = df.append({"Scanid": scanid, "Sha1sum": sha1sum, "Type": type, "Selected": selected, "RT": rt, "Mass": mass, "Intensity": intensity, "Nrpeaks": nr_peaks, "HasAnnotation": has_annotation, "Checked": checked}, ignore_index=True)

        return df

    def get_filters_list(self):
        df = pd.DataFrame()
        for filter in self.get_peakml_obj().get_filters():
            df = df.append({"ID": filter.get_id_str(), "Type": filter.get_type_value(), "Settings": filter.get_settings_value()}, ignore_index=True)
        return df

    def get_peak_plot(self): 
        peakml_obj = self.get_peakml_obj()
        selected_peak = peakml_obj.get_selected_peak()
        peakset_obj = peakml_obj.get_peak_from_sha1sum(selected_peak)
       
        df = pd.DataFrame()

        for peak_obj in peakset_obj.peaks:

            measurement_obj = peakml_obj.header.get_measurement_by_id(peak_obj.measurementid)

            label = measurement_obj.label
            rt_values = peak_obj.peak_data.get_retention_times_formatted_datetime()
            intensity_values = peak_obj.peak_data.get_intensities() 

            colour = measurement_obj.get_colour()
            selected = measurement_obj.get_selected() 

            df = df.append({"Label": label, "RT_values": rt_values, "Intensity_values": intensity_values, "Colour" : colour, "Selected" : selected }, ignore_index=True)

        return df

    def get_derivatives_plot(self):
        peakml_obj = self.get_peakml_obj()
        selected_peak = peakml_obj.get_selected_peak()
        peak_main = peakml_obj.get_peak_from_sha1sum(selected_peak)
        peakset_annotation_relationid = peak_main.get_specific_annotation('relation.id')

        df = pd.DataFrame()

        related_peaks = []

        for peak in peakml_obj.peaks:
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
            
            df = df.append({"Mass": float(mass), "Intensity": float(intensity), "Description": description}, ignore_index=True)
        
        return df

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

    def get_intensity_plot(self):
        
        try:
            peakml_obj = self.get_peakml_obj()
            selected_peak = peakml_obj.get_selected_peak()
            peakset = peakml_obj.get_peak_from_sha1sum(selected_peak)
            peaks = peakset.peaks
            df = pd.DataFrame()

            for set in peakml_obj.header.get_sets():
                
                # Get all the peaks for the set.
                measurement_peaks = self.get_peaks_with_measurementids(peaks, set.get_measurementids())

                intensities = []
                for measurement_peak in measurement_peaks:
                    intensities.append(measurement_peak.get_intensity())

                df = df.append({"SetID": set.get_id(), "Intensities": intensities}, ignore_index=True)
        except Exception as err:
            print(err)

        return df

    def get_identification(self):
        
        # Get current peak
        peakml_obj = self.get_peakml_obj()
        selected_peak = peakml_obj.get_selected_peak()
        peakset_obj = peakml_obj.get_peak_from_sha1sum(selected_peak)

        # Get molecule database
        molecule_database = self.get_molecule_database()

        annotation_ids = []
        annotation_ppms = []
        annotation_adducts = []

        # Get peak annotation of label 'identification', value is multiple ids
        annotation_identification = peakset_obj.get_specific_annotation('identification')
        if annotation_identification:
            annotation_ids = annotation_identification.value.split(', ')
        else:
            return None

        annotation_ppm = peakset_obj.get_specific_annotation('ppm')
        if annotation_ppm:
            annotation_ppms = annotation_ppm.value.split(', ')

        annotation_adduct = peakset_obj.get_specific_annotation('adduct')
        if annotation_adduct:
            annotation_adducts = annotation_adduct.value.split(', ')
        
        df = pd.DataFrame()

        for i in range(len(annotation_ids)):
            try:
                id = annotation_ids[i]
                molecule = molecule_database[id]
                ppm = annotation_ppms[i] if annotation_ppms and len(annotation_ppms) > 0 else None
                adduct = annotation_adducts[i] if annotation_adducts and len(annotation_adducts) > 0 else None

                mol_formula = str(molecule.get_formula())
                mol_name = molecule.get_name()
                mol_classdesc = molecule.get_class_description()
                mol_desc = molecule.get_description()
                mol_smiles = molecule.get_smiles()
                mol_inchi = molecule.get_inchi()

                df = df.append({"ID": id, "Formula": mol_formula, "PPM": ppm, "Adduct": adduct, "Name": mol_name, "Class": mol_classdesc, "Description": mol_desc , "Smiles": mol_smiles, "InChi": mol_inchi}, ignore_index=True)
            except Exception as err:
                print(err)

        return df

    def get_sets(self):
        try:
            df = pd.DataFrame()
            peakml_obj = self.get_peakml_obj()
            selected_peak = peakml_obj.get_selected_peak()
            peakset = peakml_obj.get_peak_from_sha1sum(selected_peak)


            # Set measurement colours from sets
            for set_info in peakml_obj.header.get_sets():

                df = df.append({"UID": set_info.get_uid(), "Name": set_info.get_id(), "Color": set_info.get_colour(), "Selected": set_info.get_selected(), "Parent": None}, ignore_index=True)

                measurement_peaks = self.get_peaks_with_measurementids(peakset.peaks, set_info.get_measurementids())

                for measurement_peak in measurement_peaks:
                    measurement = peakml_obj.header.get_measurement_by_id(measurement_peak.get_measurementid())

                    measurement.set_colour(set_info.get_colour())
                    
                    df = df.append({"UID": measurement.get_uid(), "Name": measurement.get_label(), "Color": set_info.get_colour(), "Selected": measurement.get_selected(), "Parent": set_info.get_id()}, ignore_index=True)
                
        except Exception as err:
            print(err)

        return df

    def get_details(self):

        try:
            peakml_obj = self.get_peakml_obj()
            selected_peak = peakml_obj.get_selected_peak()
            peakset = peakml_obj.get_peak_from_sha1sum(selected_peak)
            df = pd.DataFrame()

            for annotation in peakset.get_annotations():
                df = df.append({"Label": annotation.get_label(), "Value": annotation.get_value()}, ignore_index=True)

        except Exception as err:
            print(err)

        return df

    #def update_peakcolour_selection(self, sampleid, selected):
    #    self.get_peakml_obj().set_peak_colour_selection_by_sampleid(sampleid,selected)

    def update_set_selection(self, measurement_sampleid, selected):

        measurement = self.get_peakml_obj().header.get_measurement_by_sampleid(measurement_sampleid)
        measurement.set_selected(selected)

        #self.get_peakml_obj().set_peak_colour_selection_by_sampleid(sampleid,selected)  

    def get_peak_set_data_by_selected_peak(self):
        print("Not implemented")

    def add_filter_mass(self, mass_min, mass_max, formula, formula_ppm, mass_charge, filter_option):
        self.get_peakml_obj().add_filter(FilterMass(mass_min, mass_max, formula, formula_ppm, mass_charge, filter_option))

    def add_filter_intensity(self, intensity_min, intensity_unit):
        self.get_peakml_obj().add_filter(FilterIntensity(intensity_min, intensity_unit))

    def add_filter_retention_time(self, range_min, range_max):
        self.get_peakml_obj().add_filter(FilterRetentionTime(range_min, range_max))

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