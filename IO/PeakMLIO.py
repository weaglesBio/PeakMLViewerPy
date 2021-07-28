import xml.etree.ElementTree as ET
from xml.dom import minidom
import base64
import numpy as np

from Data.PeakML.Header import Header
from Data.PeakML.Annotation import Annotation
from Data.PeakML.Peak import Peak
from Data.PeakML.PeakData import PeakData
from Data.PeakML.SampleInfo import SampleInfo
from Data.PeakML.SetInfo import SetInfo
from Data.PeakML.ApplicationInfo import ApplicationInfo
from Data.PeakML.MeasurementInfo import MeasurementInfo
from Data.PeakML.ScanInfo import ScanInfo
from Data.PeakML.FileInfo import FileInfo

import Utilities as u
import Progress as p
import Logger as lg

#region Reader methods

def showElementValue(tag_name, tag_value):
    if tag_value is not None and tag_value.text is not None: 
        print(tag_name + ": " + tag_value.text)
    else:
        print(tag_name + ": None")

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
        value_type = annotation_element.find("./valuetype")

        #u.trace(f"Import annotation {label.text} {value.text}")

        annotation = Annotation(unit_attribute, ontologyref_attribute, label.text if label.text else "", value.text if value.text else "", value_type.text if value_type.text else "STRING")
        parent_object.add_annotation(annotation)

def add_peaks(parent_element, peakset, parent_peak_num):

    peak_elements = parent_element.findall("./peaks/peak")
    peak_elements_len = len(peak_elements)
    peak_iter = 0
    for peak_element in peak_elements:

        if parent_peak_num is None:
            p.update_progress(f"Importing subpeak {(peak_iter+1)} of {peak_elements_len}")
        else:
            p.update_progress(f"Importing subpeak {peak_iter+1} of {peak_elements_len}, of peak {parent_peak_num}")

        type_attribute = peak_element.attrib["type"]
        scan_element = peak_element.find("./scan")
        retention_time_element = peak_element.find("./retentiontime")
        mass_element = peak_element.find("./mass")
        intensity_element = peak_element.find("./intensity")
        measurement_id_element = peak_element.find("./measurementid")
        pattern_id_element = peak_element.find("./patternid")
        sha1sum_element = peak_element.find("./sha1sum")
        signal_element  = peak_element.find("./signal")

        if scan_element is not None:    
            scan = scan_element.text
        else:
            scan = None
            
        if retention_time_element is not None:         
            retention_time = retention_time_element.text
        else:
            retention_time = None
        
        if mass_element is not None:     
            mass = mass_element.text
        else:
            mass = None
        
        if intensity_element is not None: 
            intensity = intensity_element.text
        else:
            intensity = None
        
        if measurement_id_element is not None: 
            measurement_id = measurement_id_element.text
        else:
            measurement_id = None

        if pattern_id_element is not None: 
            pattern_id = pattern_id_element.text
        else:
            pattern_id = None
        
        if sha1sum_element is not None: 
            sha1sum = sha1sum_element.text
        else:
            sha1sum = None

        if signal_element is not None: 
            signal = signal_element.text
        else:
            signal = None

        peak_data_element = peak_element.find("./peakdata")

        if peak_data_element is not None:
            peak_data_type_attribute = peak_data_element.attrib["type"]
            peak_data_size_attribute = peak_data_element.attrib["size"]

            scanids_element = peak_data_element.find("./scanids")
            retention_times_element = peak_data_element.find("./retentiontimes")
            masses_element = peak_data_element.find("./masses")
            intensities_element = peak_data_element.find("./intensities")
            relative_intensities_element = peak_data_element.find("./relativeintensities")
            pattern_ids_element = peak_data_element.find("./patternids")
            measurement_ids_element = peak_data_element.find("./measurementids")

            peak_data = PeakData(peak_data_type_attribute, peak_data_size_attribute)

            if scanids_element is not None:   
                scanids_decoded_bytes = base64.b64decode(scanids_element.text) 
                peak_data.scan_ids = np.frombuffer(scanids_decoded_bytes, dtype = int)
                
            if retention_times_element is not None:      
                retention_times_decoded_bytes = base64.b64decode(retention_times_element.text)
                peak_data.retention_times = np.frombuffer(retention_times_decoded_bytes, dtype = np.float32)
            
            if masses_element is not None:     
                masses_decoded_bytes = base64.b64decode(masses_element.text)
                peak_data.masses = np.frombuffer(masses_decoded_bytes, dtype = np.float32)
            
            if intensities_element is not None: 
                intensities_decoded_bytes = base64.b64decode(intensities_element.text) 
                peak_data.intensities = np.frombuffer(intensities_decoded_bytes, dtype = np.float32)
            
            if relative_intensities_element is not None: 
                intensities_decoded_bytes = base64.b64decode(relative_intensities_element.text) 
                peak_data.relative_intensities = np.frombuffer(intensities_decoded_bytes, dtype = np.float32)
            
            if pattern_ids_element is not None: 
                pattern_ids_decoded_bytes = base64.b64decode(pattern_ids_element.text) 
                peak_data.pattern_ids = np.frombuffer(pattern_ids_decoded_bytes, dtype = int)
            
            if measurement_ids_element is not None: 
                measurement_ids_decoded_bytes = base64.b64decode(measurement_ids_element.text) 
                peak_data.measurement_ids = np.frombuffer(measurement_ids_decoded_bytes, dtype = int)

            #print(f"Subpeak {(peak_iter+1)} of {peak_elements_len}")
            #print(peak_data.measurement_ids)
        else:
            peak_data = None

        #u.trace(f"Import peak {mass}")

        peak = Peak(type_attribute, scan, retention_time, mass, intensity, measurement_id, pattern_id, sha1sum, signal, peak_data)

        add_peaks(peak_element, peak.peaks, f"{(peak_iter+1)} of {peak_elements_len}")
        add_annotations(peak_element, peak)

        peakset.append(peak)

        peak_iter += 1

def import_element_tree_from_peakml_file(tree_data):

    lg.log_progress(f"Start reading XML")
    p.update_progress(f"Importing header")

    root = ET.fromstring(tree_data)

    header_element = root.find("./header")

    # Create PeakHeader
    nr_peaks = header_element.find("./nrpeaks")
    date = header_element.find("./date")
    owner = header_element.find("./owner")
    description = header_element.find("./description")

    header_obj = Header(nr_peaks.text, date.text, owner.text, description.text)

    add_annotations(header_element, header_obj)

    # Add 'Set Info' records to PeakHeader
    set_elements = header_element.findall("./sets/set")
    set_iter = 0
    for set_element in set_elements:

        p.update_progress(f"Importing header sample {(set_iter+1)} of {len(set_elements)}")

        id = set_element.find("./id")
        type = set_element.find("./type")
        
        measurement_ids_element = set_element.find("./measurementids")
        measurement_ids = []

        if measurement_ids_element is not None: 
            measurement_ids_decoded_bytes = base64.b64decode(measurement_ids_element.text) 
            measurement_ids = np.frombuffer(measurement_ids_decoded_bytes, dtype = int)

        set = SetInfo(id.text, type.text, measurement_ids)
        header_obj.add_set(set)

        set_iter += 1

    # Add 'Sample Info' records to PeakHeader
    sample_elements = header_element.findall("./samples/sample")
    sample_elements_len = len(sample_elements)
    sample_iter = 0
    for sample_element in sample_elements:

        p.update_progress(f"Importing header sample {(sample_iter+1)} of {sample_elements_len}")

        id = sample_element.find("./id")
        annotations = sample_element.find("./annotations")

        sample = SampleInfo(id.text, annotations.text)
        header_obj.add_sample(sample)

        sample_iter += 1

    # Add 'Application Info' records to PeakHeader
    for application_element in header_element.findall("./applications/application"):

        name = application_element.find("./name")
        version = application_element.find("./version")
        date = application_element.find("./date")
        parameters = application_element.find("./parameters")

        application = ApplicationInfo(name.text, version.text, date.text, parameters.text)
        header_obj.add_application(application)

    # Add 'Measurement Info' records to PeakHeader
    measurement_elements = header_element.findall("./measurements/measurement")
    measurement_elements_len = len(measurement_elements)
    measurement_iter = 0
    for measurement_element in measurement_elements:

        p.update_progress(f"Importing header measurement {(measurement_iter+1)} of {measurement_elements_len}")

        id = measurement_element.find("./id")
        label = measurement_element.find("./label")
        sample_id = measurement_element.find("./sampleid")

        measurement = MeasurementInfo(id.text, label.text, sample_id.text)

        for scan_element in measurement_element.findall("./scans/scan"):

            polarity = scan_element.find("./polarity")
            retention_time = scan_element.find("./retentiontime")

            scan = ScanInfo(polarity.text, retention_time.text)
            add_annotations(scan_element, scan)

            measurement.add_scan(scan)

        for file_element in measurement_element.findall("./files/file"):

            label = file_element.find("./label")
            name = file_element.find("./name")
            location = file_element.find("./location")

            file = FileInfo(label.text, name.text, location.text)

            measurement.add_file(file)

        header_obj.add_measurement(measurement)

        measurement_iter += 1

    # Init empty peaksetUnable to update entry data
    peakset = []

    # Add 'Peak' records to peakset list
    add_peaks(root, peakset, None)

    # Finding the peaks linked into sets by measurement id
    for peak in peakset:

        # does the peak data contain the id.
        for subpeak in peak.peaks:

            for set in header_obj.sets:

                for measurement_id in set.measurement_ids:

                    if measurement_id in subpeak.peak_data.measurement_ids:
                        set.add_linked_peak_measurement_ids(subpeak.measurement_id)

    # Convert peakset to dictionary with peak uids.
    peakset_dict = {}

    for peak in peakset:
        uid = u.get_new_uuid()
        peakset_dict[uid] = peak

    lg.log_progress(f"Finish reading XML")

    return header_obj, peakset_dict
        
# Need to create test file to see that conversion process is correct, checking every node.

#endregion

#region Write methods

def prettify(etree):
    et_string = ET.tostring(etree)
    md_string = minidom.parseString(et_string)
    return md_string.toprettyxml(indent="\t")

def finalise_xml_formatting(input_string: str):

    updated_top_string = input_string.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
    updated_empty_nodes = updated_top_string.replace("/>"," />")
    #split_header_and_peaks = updated_empty_nodes.replace('</header>','</header>\n')

    return updated_empty_nodes

def add_annotation_nodes(parent_element, parent_object):
    if parent_object.annotations:
        annotations = ET.SubElement(parent_element, 'annotations')

        for annotation_obj in parent_object.annotations:
            annotation = ET.SubElement(annotations, 'annotation')

            if annotation_obj.unit is not None:
                annotation.set('unit', annotation_obj.unit)

            if annotation_obj.ontology_ref is not None:
                annotation.set('ontologyref', annotation_obj.ontology_ref)

            #u.trace(f"Export annotation {label.text} {value.text}")

            label = ET.SubElement(annotation, 'label')
            label.text = annotation_obj.label
            value = ET.SubElement(annotation, 'value')
            value.text = annotation_obj.value
            value_type = ET.SubElement(annotation, 'valuetype')
            value_type.text = annotation_obj.value_type

def add_peak_nodes(parent_element, peak_list: list[Peak]):

    peaks = ET.SubElement(parent_element, 'peaks')

    for peak_obj in peak_list:
        peak = ET.SubElement(peaks, 'peak')
        peak.set('type', peak_obj.type)

        if peak_obj.scan is not None:
            scan = ET.SubElement(peak, 'scan')
            scan.text = peak_obj.scan

        if peak_obj.scan is not None:
            retention_time = ET.SubElement(peak, 'retentiontime')
            retention_time.text = peak_obj.retention_time

        if peak_obj.mass is not None:
            mass = ET.SubElement(peak, 'mass')
            mass.text = peak_obj.mass

        if peak_obj.intensity is not None:
            intensity = ET.SubElement(peak, 'intensity')
            intensity.text = peak_obj.intensity

        if peak_obj.pattern_id is not None:
            pattern_id = ET.SubElement(peak, 'patternid')
            pattern_id.text = peak_obj.pattern_id

        if peak_obj.measurement_id is not None:
            measurement_id = ET.SubElement(peak, 'measurementid')
            measurement_id.text = peak_obj.measurement_id

        if peak_obj.sha1sum is not None:
            sha1sum = ET.SubElement(peak, 'sha1sum')
            sha1sum.text = peak_obj.sha1sum

        #u.trace(f"Export peak {mass.text} {mass.text}")

        add_annotation_nodes(peak, peak_obj)

        if peak_obj.signal is not None:
            signal = ET.SubElement(peak, 'signal')
            signal.text = peak_obj.signal

        add_peak_nodes(peak, peak_obj.peaks)

        if peak_obj.peak_data is not None:
            peak_data = ET.SubElement(peak, 'peakdata')
            peak_data.set('type', peak_obj.peak_data.type)
            peak_data.set('size', peak_obj.peak_data.size)

            if peak_obj.peak_data.scan_ids is not None:
                scanids = ET.SubElement(peak_data, 'scanids')
                scanids.text = peak_obj.peak_data.get_encoded_scan_ids()

            if peak_obj.peak_data.retention_times is not None:
                retention_times = ET.SubElement(peak_data, 'retentiontimes')
                retention_times.text = peak_obj.peak_data.get_encoded_retention_times()

            if peak_obj.peak_data.masses is not None:
                masses = ET.SubElement(peak_data, 'masses')
                masses.text = peak_obj.peak_data.get_encoded_masses()

            if peak_obj.peak_data.intensities is not None:
                intensities = ET.SubElement(peak_data, 'intensities')
                intensities.text = peak_obj.peak_data.get_encoded_intensities()

            if peak_obj.peak_data.relative_intensities is not None:
                relative_intensities = ET.SubElement(peak_data, 'relativeintensities')
                relative_intensities.text = peak_obj.peak_data.get_encoded_relative_intensities()

            if peak_obj.peak_data.pattern_ids is not None:
                pattern_ids = ET.SubElement(peak_data, 'patternids')
                pattern_ids.text = peak_obj.peak_data.get_encoded_pattern_ids()

            if peak_obj.peak_data.measurement_ids is not None:
                measurement_ids = ET.SubElement(peak_data, 'measurementids')
                measurement_ids.text = peak_obj.peak_data.get_encoded_measurement_ids()             

def create_xml_from_peakml(data_header, data_peaks_list):
    
    u.trace(f"Start writing XML")

    peakml = ET.Element('peakml')
    peakml.set('version', "1.0.0")
    header = ET.SubElement(peakml, 'header')

    nr_peaks = ET.SubElement(header, 'nrpeaks')

    #TODO: Update this to reflect excluded peaks
    nr_peaks.text = data_header.nr_peaks
    date = ET.SubElement(header, 'date')
    date.text = data_header.date
    owner = ET.SubElement(header, 'owner')
    owner.text = data_header.owner
    description = ET.SubElement(header, 'description')
    description.text = data_header.description

    sets = ET.SubElement(header, 'sets')

    for set_obj in data_header.sets: 
        set = ET.SubElement(sets, 'set')

        id = ET.SubElement(set, 'id')
        id.text = set_obj.id
        type = ET.SubElement(set, 'type')
        type.text = set_obj.type
        measurement_ids = ET.SubElement(set, 'measurementids')
        measurement_ids.text = set_obj.get_encoded_measurement_ids()

    measurements = ET.SubElement(header, 'measurements')

    for measurement_obj in data_header.measurements:
        measurement = ET.SubElement(measurements, 'measurement')

        id = ET.SubElement(measurement, 'id')
        id.text = measurement_obj.id
        label = ET.SubElement(measurement, 'label')
        label.text = measurement_obj.label
        sample_id = ET.SubElement(measurement, 'sampleid')
        sample_id.text = measurement_obj.sample_id

        scans = ET.SubElement(measurement, 'scans')

        for scan_obj in measurement_obj.scans:
            scan = ET.SubElement(scans, 'scan')

            polarity = ET.SubElement(scan, 'polarity')
            polarity.text = scan_obj.polarity
            retention_time = ET.SubElement(scan, 'retentiontime')
            retention_time.text = scan_obj.retention_time

            add_annotation_nodes(scan, scan_obj)

        files = ET.SubElement(measurement, 'files')

        for file_obj in measurement_obj.files:
            file = ET.SubElement(files, 'file')

            label = ET.SubElement(file, 'label')
            label.text = file_obj.label
            name = ET.SubElement(file, 'name')
            name.text = file_obj.name
            location = ET.SubElement(file, 'location')
            location.text = file_obj.location

    add_annotation_nodes(header, data_header)
    
    # Settings as parameters the peakml xml object and a list of peak data objects
    add_peak_nodes(peakml, data_peaks_list)

    prettified_xml = prettify(peakml)
    finalised_xml = finalise_xml_formatting(prettified_xml)

    u.trace(f"Finish writing XML")

    return finalised_xml

#endregion