# The purpose of this class is to encapsulate all data access logic, the methods here are the one used by the ui layer
# They should be a specific and descriptive in their naming as possible.

import gzip
from xml.dom import minidom
import pandas as pd

import Data.PeakMLReader as PMLRead
import Data.PeakMLWriter as PMLWrite

class PeakMLData:

    def __init__(self):
        self.peakMLData = None

    def set_peakml_obj(self, current_obj):
        self.peakml_obj = current_obj

    def get_peakml_obj(self):
        return self.peakml_obj

    def import_file_to_data_object(self, filepath):

        path =  filepath.rsplit("\\")[1]
        filename = filepath.rsplit("\\")[2]
   
        try:
            # If errors while attempt to read, requires conversion.
            with open(filepath) as f:
                print(f.readline())

            with open(filepath) as f:
                tree_data = f.read()
        except:
            with gzip.open(filepath) as g:
                tree_data = g.read()
                tree_data = tree_data.decode()
                tree_data = tree_data.replace('\n','')
                tree_data = tree_data.replace('\t','')
                tree_data = tree_data.encode()
                md_string = minidom.parseString(tree_data)
                decoded_output = md_string.toprettyxml(indent="\t")
                decoded_output = decoded_output.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
                decoded_output = decoded_output.replace("/>"," />")

                w = open(path + "decoded_" + filename, "w")
                w.write(decoded_output)
                w.close()

        #Import file
        print("Importing xml")
        data_obj = PMLRead.importElementTreeFromPeakMLFile(tree_data)

        self.set_peakml_obj(data_obj)

    def export_data_object_to_file(self, filepath):

        path =  filepath.rsplit("\\")[1]
        filename = filepath.rsplit("\\")[2]

        data_obj = self.get_peakml_obj()

        print("Generating output xml")
        xml_string = PMLWrite.CreateXMLObjectFromPeakMLObject(data_obj)

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
            rt = peak_obj.get_retention_time_formatted()
            mass = peak_obj.get_mass()
            intensity = peak_obj.get_intensity()
            nr_peaks = peak_obj.get_nr_peaks()

            df = df.append({"Scanid": scanid, "Sha1sum": sha1sum, "Type": type, "Selected": selected, "RT": rt, "Mass": mass, "Intensity": intensity, "Nr peaks": nr_peaks}, ignore_index=True)

        print(df)
        return df
        #Apply filters

    def get_peak_graph_data_by_scanid(self, sha1sum): 
        peakml_obj = self.get_peakml_obj()

        peakset_obj = peakml_obj.get_peak_from_sha1sum(sha1sum)
       
        df = pd.DataFrame()

        for peak_obj in peakset_obj.peaks:
            
            print("measurementid: " + peak_obj.measurementid)

            measurement_obj = peakml_obj.header.get_measurement_by_id(peak_obj.measurementid)
            #set_obj = peakml_obj.header.get_set_by_measurementid(peak_obj.measurementid)
            
            label = measurement_obj.label
            rt_values = peak_obj.peak_data.get_retention_times_formatted()
            intensity_values = peak_obj.peak_data.get_intensities() 

            df = df.append({"Label": label, "RT_values": rt_values, "Intensity_values": intensity_values}, ignore_index=True)

        print(df)
        return df

    #def add_filter(self):


## Need logic section for visibility of lines.



#Can there be more than two layers of peaks.



    #def remove_filter:















































        #get peaks
        peakml_obj.peaks