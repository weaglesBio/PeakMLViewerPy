import unittest

import Utilities as u

import IO.PeakMLIO as pmlio

class TestMethods(unittest.TestCase):

    def test_utilities_format_time_string(self):
        self.assertEqual(u.format_time_string(754),"12:34", "Should be 12:34")

    def test_utilities_format_time_int(self):
        self.assertEqual(u.format_time_int("12:34"),754, "Should be 754")

    def test_peakmlio_import(self):

        
        pmlio.import_element_tree_from_peakml_file()

        #Returns header_obj, peakset_dict, peak_order


    def test_peakmlio_export(self):


        pmlio.create_xml_from_peakml()

        # Returns finalised xml string

if __name__ == '__main__':
    unittest.main()