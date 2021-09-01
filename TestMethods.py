import unittest

import Utilities as u
import IO.PeakMLIO as pmlio
import TestObjects as testobj

class TestMethods(unittest.TestCase):

    def test_utilities_format_time_string(self):
        self.assertEqual(u.format_time_string(754),"12:34", "Should be 12:34")

    def test_utilities_format_time_int(self):
        self.assertEqual(u.format_time_int("12:34"),754, "Should be 754")

    # Import/Output Method Tests

    def test_peakmlio_import(self):
        # This test imports the test file 'example_peaks' and prodices header_obj, peakset_dict and peak order
        with open("sample_file.peakml") as f:
            tree_data = f.read().encode()

        # Returns header_obj, peakset_dict, peak_order
        header, peak_dict, peak_order = pmlio.import_element_tree_from_peakml_file(tree_data)

        # If the resulting header and peak list (extracted from the peakset dict) match that of the stored object it passes.
        peakml = testobj.get_test_peakml_obj()

        self.assertEqual(peakml.header, header, "Header objects should match")
        self.assertEqual(list(peakml.peaks.values()), list(peak_dict.values()), "Header objects should match")

    def test_peakmlio_export(self):

        peakml = testobj.get_test_peakml_obj()

        xml_string = pmlio.create_xml_from_peakml(peakml.header, list(peakml.peaks.values()))
        
        # Returns finalised xml string
        with open("sample_file.peakml") as f:
            sameple_file_xml = f.read().encode()

        self.assertEqual(sameple_file_xml, xml_string, "XML strings should match")

if __name__ == '__main__':
    unittest.main()