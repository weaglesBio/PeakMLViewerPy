from Data.PeakML.Peak import Peak

import IO.PeakMLIO as PeakMLIO
import IO.IPAIO as IPAIO

import Logger as lg
import gzip

class PeakML():
    def __init__(self):
        self.selected_peak = None
        self.header = None
        self.peaks = None

    @property
    def header(self) -> str:
        return self._header
    
    @header.setter
    def header(self, header: str):
        self._header = header

    @property
    def peaks(self) -> dict[str, Peak]:
        return self._peaks

    @peaks.setter
    def peaks(self, peaks: dict[str, Peak]):
        self._peaks = peaks

    def get_peak_by_uid(self, uid) -> Peak:
        return self.peaks[uid]

    def remove_peak_by_uid(self, uid):
        del self.peaks[uid]

    def import_from_file(self, filepath):
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
                    # md_string = minidom.parseString(tree_data)
                    # decoded_output = md_string.toprettyxml(indent="\t")
                    # decoded_output = decoded_output.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
                    # decoded_output = decoded_output.replace("/>"," />")

                    # w = open(self.get_path() + "decoded_" + self.get_filename(), "w")
                    # w.write(decoded_output)
                    # w.close()
            except Exception as err:
                lg.log_error(f'Unable to open compressed file: {err}')

        if tree_data is not None:
            try:
                header, peaks = PeakMLIO.import_element_tree_from_peakml_file(tree_data)
                self.header = header
                self.peaks = peaks

            except Exception as err:
                lg.log_error(f'Unable to convert file to PeakML class stucture: {err}')

    def import_ipa_from_file(self, filepath):
        IPAIO.import_ipa_rdata_from_filepath(filepath=filepath, peakml_peaks=self.peaks)
    
    def export(self, filepath):

        #Select peaks to include based on checks and filters.

        r = open(filepath, "w")
        # Pass header and peaks list
        #TODO Consider how to persist ordering of peaks
        r.write(PeakMLIO.create_xml_from_peakml(self.header, list(self.peaks.values())))
        r.close()

    