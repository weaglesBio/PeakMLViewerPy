import xml.etree.ElementTree as ET
from Data.DataObjects.PeakML import PeakML
import base64
import numpy as np

from Data.DataObjects.Header import Header
from Data.DataObjects.Annotation import Annotation
from Data.DataObjects.Peak import Peak
from Data.DataObjects.PeakData import PeakData
from Data.DataObjects.SampleInfo import SampleInfo
from Data.DataObjects.SetInfo import SetInfo
from Data.DataObjects.ApplicationInfo import ApplicationInfo
from Data.DataObjects.MeasurementInfo import MeasurementInfo
from Data.DataObjects.ScanInfo import ScanInfo
from Data.DataObjects.FileInfo import FileInfo


#class PeakMLFile():

def showElementValue(tagname, tagvalue):
    if tagvalue is not None and tagvalue.text is not None: 
        print(tagname + ": " + tagvalue.text)
    else:
        print(tagname + ": None")

# TODO: Add logic for checking it is valid peakml file based on extension and structure.

def add_annotations(parent_element, parent_object):
    for annotation_element in parent_element.findall("./annotations/annotation"):

        if 'unit' in annotation_element.attrib:
            unit_attribute = annotation_element.attrib["unit"]
        else:
            unit_attribute = None

        if 'ontologyref' in annotation_element.attrib:
            ontologyref_attribute = annotation_element.attrib["ontologyref"]
        else:
            ontologyref_attribute = None


        label = annotation_element.find("./label")
        value = annotation_element.find("./value")
        valuetype = annotation_element.find("./valuetype")

        annotation = Annotation(unit_attribute, ontologyref_attribute, label.text, value.text, valuetype.text)
        parent_object.add_annotation(annotation)

def add_peaks(parent_element, peakset):
    for peak_element in parent_element.findall("./peaks/peak"):
        type_attribute = peak_element.attrib["type"]
        scan_element = peak_element.find("./scan")
        retentiontime_element = peak_element.find("./retentiontime")
        mass_element = peak_element.find("./mass")
        intensity_element = peak_element.find("./intensity")
        measurementid_element = peak_element.find("./measurementid")
        patternid_element = peak_element.find("./patternid")
        sha1sum_element = peak_element.find("./sha1sum")
        signal_element  = peak_element.find("./signal")

        if scan_element is not None:    
            scan = scan_element.text
        else:
            scan = None
            
        if retentiontime_element is not None:         
            retentiontime = retentiontime_element.text
        else:
            retentiontime = None
        
        if mass_element is not None:     
            mass = mass_element.text
        else:
            mass = None
        
        if intensity_element is not None: 
            intensity = intensity_element.text
        else:
            intensity = None
        
        if measurementid_element is not None: 
            measurementid = measurementid_element.text
        else:
            measurementid = None

        if patternid_element is not None: 
            patternid = patternid_element.text
        else:
            patternid = None
        
        if sha1sum_element is not None: 
            sha1sum = sha1sum_element.text
        else:
            sha1sum = None

        if signal_element is not None: 
            signal = signal_element.text
        else:
            signal = None

        peakdata_element = peak_element.find("./peakdata")

        if peakdata_element is not None:
            peakdata_type_attribute = peakdata_element.attrib["type"]
            peakdata_size_attribute = peakdata_element.attrib["size"]

            scanids_element = peakdata_element.find("./scanids")
            retentiontimes_element = peakdata_element.find("./retentiontimes")
            masses_element = peakdata_element.find("./masses")
            intensities_element = peakdata_element.find("./intensities")
            relativeintensities_element = peakdata_element.find("./relativeintensities")
            patternids_element = peakdata_element.find("./patternids")
            measurementids_element = peakdata_element.find("./measurementids")

            peak_data = PeakData(peakdata_type_attribute, peakdata_size_attribute)

            if scanids_element is not None:   
                scanids_decoded_bytes = base64.b64decode(scanids_element.text) 
                peak_data.scanids = np.frombuffer(scanids_decoded_bytes, dtype = int)
                
            if retentiontimes_element is not None:      
                retentiontimes_decoded_bytes = base64.b64decode(retentiontimes_element.text)
                peak_data.retentiontimes = np.frombuffer(retentiontimes_decoded_bytes, dtype = np.float32)
            
            if masses_element is not None:     
                masses_decoded_bytes = base64.b64decode(masses_element.text)
                peak_data.masses = np.frombuffer(masses_decoded_bytes, dtype = np.float32)
            
            if intensities_element is not None: 
                intensities_decoded_bytes = base64.b64decode(intensities_element.text) 
                peak_data.intensities = np.frombuffer(intensities_decoded_bytes, dtype = np.float32)
            
            if relativeintensities_element is not None: 
                intensities_decoded_bytes = base64.b64decode(relativeintensities_element.text) 
                peak_data.relativeintensities = np.frombuffer(intensities_decoded_bytes, dtype = np.float32)
            
            if patternids_element is not None: 
                patternids_decoded_bytes = base64.b64decode(patternids_element.text) 
                peak_data.patternids = np.frombuffer(patternids_decoded_bytes, dtype = int)
            
            if measurementids_element is not None: 
                measurementids_decoded_bytes = base64.b64decode(measurementids_element.text) 
                peak_data.measurementids = np.frombuffer(measurementids_decoded_bytes, dtype = int)

        else:
            peak_data = None

        peak = Peak(type_attribute, scan, retentiontime, mass, intensity, measurementid, patternid, sha1sum, signal, peak_data)

        add_peaks(peak_element, peak.peaks)
        add_annotations(peak_element, peak)

        peakset.append(peak)

def importElementTreeFromPeakMLFile(tree_data,filepath):

    root = ET.fromstring(tree_data)

    header_element = root.find("./header")

    # Create PeakHeader
    nrpeaks = header_element.find("./nrpeaks")
    date = header_element.find("./date")
    owner = header_element.find("./owner")
    description = header_element.find("./description")

    header_obj = Header(nrpeaks.text, date.text, owner.text, description.text)

    add_annotations(header_element, header_obj)

    # Add 'Set Info' records to PeakHeader
    for set_element in header_element.findall("./sets/set"):

        id = set_element.find("./id")
        type = set_element.find("./type")
        measurementids = set_element.find("./measurementids")

        set = SetInfo(id.text, type.text, measurementids.text)
        header_obj.add_set(set)

    # Add 'Sample Info' records to PeakHeader
    for sample_element in header_element.findall("./samples/sample"):

        id = sample_element.find("./id")
        annotations = sample_element.find("./annotations")

        sample = SampleInfo(id.text, annotations.text)
        header_obj.add_sample(sample)

    # Add 'Application Info' records to PeakHeader
    for application_element in header_element.findall("./applications/application"):

        name = application_element.find("./name")
        version = application_element.find("./version")
        date = application_element.find("./date")
        parameters = application_element.find("./parameters")

        application = ApplicationInfo(name.text, version.text, date.text, parameters.text)
        header_obj.add_application(application)

    # Add 'Measurement Info' records to PeakHeader
    for measurement_element in header_element.findall("./measurements/measurement"):

        id = measurement_element.find("./id")
        label = measurement_element.find("./label")
        sampleid = measurement_element.find("./sampleid")

        measurement = MeasurementInfo(id.text, label.text, sampleid.text)

        for scan_element in measurement_element.findall("./scans/scan"):

            polarity = scan_element.find("./polarity")
            retentiontime = scan_element.find("./retentiontime")

            scan = ScanInfo(polarity.text, retentiontime.text)
            add_annotations(scan_element, scan)

            measurement.add_scan(scan)

        for file_element in measurement_element.findall("./files/file"):

            label = file_element.find("./label")
            name = file_element.find("./name")
            location = file_element.find("./location")

            file = FileInfo(label.text, name.text, location.text)

            measurement.add_file(file)

        header_obj.add_measurement(measurement)

    peakset = []

    # Add 'Peak' records
    add_peaks(root, peakset)

    return PeakML(header_obj, peakset,filepath)
        

# Need to create test file to see that conversion process is correct, checking every node.


