from numpy.lib.twodim_base import mask_indices
import IO.MoleculeIO
import gzip
from xml.dom import minidom
import pandas as pd
import os.path

import IO.PeakMLReader as Read
import IO.PeakMLWriter as Write
import IO.MoleculeIO as MolIO

# The purpose of this class is to encapsulate all data access logic, the methods here are the one used by the ui layer
# They should be a specific and descriptive in their naming as possible.

class PeakMLData:

    def __init__(self):
        self.peakMLData = None
        self.peakml_obj = None
        self.filepath = None
        self.molecule_database = None

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

        path =  filepath.rsplit("\\")[1]
        filename = filepath.rsplit("\\")[2]

        data_obj = self.get_peakml_obj()

        print("Generating output xml")
        xml_string = Write.CreateXMLObjectFromPeakMLObject(data_obj)

        print("Saving XML...")
        r = open(path + "Reconstructed_" + filename, "w")
        r.write(xml_string)
        r.close()
        print("XML Saved")

        # use panda dataframe for data - better than current object structure for queries?
        # Will need to examine the complexity of the required queries.

    def get_entry_list(self):
        peakml_obj = self.get_peakml_obj()

        df = pd.DataFrame()

        for peak_obj in peakml_obj.peaks:

            selected = peak_obj.if_patternid_set()
            sha1sum = peak_obj.get_sha1sum()
            scanid = peak_obj.get_scanid()
            type = peak_obj.get_type()
            rt = peak_obj.get_retention_time_formatted_string()
            mass = peak_obj.get_mass()
            intensity = peak_obj.get_intensity()
            nr_peaks = peak_obj.get_nr_peaks()

            df = df.append({"Scanid": scanid, "Sha1sum": sha1sum, "Type": type, "Selected": selected, "RT": rt, "Mass": mass, "Intensity": intensity, "Nrpeaks": nr_peaks}, ignore_index=True)

        #print(df)
        return df
        #Apply filters

    def get_peak_plot(self): 
        peakml_obj = self.get_peakml_obj()
        selected_peak = peakml_obj.get_selected_peak()
        peakset_obj = peakml_obj.get_peak_from_sha1sum(selected_peak)
       
        df = pd.DataFrame()

        for peak_obj in peakset_obj.peaks:
            
            #print("measurementid: " + peak_obj.measurementid)

            measurement_obj = peakml_obj.header.get_measurement_by_id(peak_obj.measurementid)
            #set_obj = peakml_obj.header.get_set_by_measurementid(peak_obj.measurementid)
            
            label = measurement_obj.label
            rt_values = peak_obj.peak_data.get_retention_times_formatted_datetime()
            intensity_values = peak_obj.peak_data.get_intensities() 

            df = df.append({"Label": label, "RT_values": rt_values, "Intensity_values": intensity_values}, ignore_index=True)

        #print(df)
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

            #for measurementid in measurementids:
            #    if peak.get_measurementid() == measurementid:
            #        peak_has_measurement = True

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

                df = df.append({"SetID": set.get_setid(), "Intensities": intensities}, ignore_index=True)
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

                if annotation_ppms and len(annotation_ppms) > 0:
                    ppm = annotation_ppms[i]
                else:
                    ppm = None

                if annotation_adducts and len(annotation_adducts) > 0:
                    adduct = annotation_adducts[i]
                else:
                    adduct = None

                mol_formula = str(molecule.get_formula())
                mol_name = molecule.get_name()
                mol_classdesc = molecule.get_class_description()
                mol_desc = molecule.get_description()

                df = df.append({"ID": id, "Formula": mol_formula, "PPM": ppm, "Adduct": adduct, "Name": mol_name, "Class": mol_classdesc, "Description": mol_desc}, ignore_index=True)
            except Exception as err:
                print(err)

        return df


    def get_peak_set_data_by_selected_peak(self):
        print("Not implemented")


        #database = 
        #get databases


        
        print("not")


        #get annotation

    
#
 #       peakset_obj = peakml_obj.get_peak_from_sha1sum(sha1sum)
 #      
 #       
#
 #       for peak_obj in peakset_obj.peaks:
 #           
 #           print("measurementid: " + peak_obj.measurementid)
#
 #           measurement_obj = peakml_obj.header.get_measurement_by_id(peak_obj.measurementid)
 #           #set_obj = peakml_obj.header.get_set_by_measurementid(peak_obj.measurementid)
 #           
 #           label = measurement_obj.label
 #           rt_values = peak_obj.peak_data.get_retention_times_formatted()
 #           intensity_values = peak_obj.peak_data.get_intensities() 
#
 #           df = df.append({"Label": label, "RT_values": rt_values, "Intensity_values": intensity_values}, ignore_index=True)
#
 #       print(df)
 #       return df

    #def add_filter(self):


## Need logic section for visibility of lines.



#Can there be more than two layers of peaks.



    #def remove_filter:















































        #get peaks
        peakml_obj.peaks