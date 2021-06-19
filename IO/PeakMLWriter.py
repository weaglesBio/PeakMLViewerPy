import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(etree):
    et_string = ET.tostring(etree)
    md_string = minidom.parseString(et_string)
    return md_string.toprettyxml(indent="\t")

def finalise_xml_formatting(input_string):

    updated_top_string = input_string.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
    updated_empty_nodes = updated_top_string.replace("/>"," />")
    split_header_and_peaks = updated_empty_nodes.replace('</header>','</header>\n')

    return updated_empty_nodes

def add_annotation_nodes(parent_element, parent_object):
    if parent_object.annotations:
        annotations = ET.SubElement(parent_element, 'annotations')

        for annotation_obj in parent_object.annotations:
            annotation = ET.SubElement(annotations, 'annotation')

            if annotation_obj.unit is not None:
                annotation.set('unit', annotation_obj.unit)

            if annotation_obj.ontologyref is not None:
                annotation.set('ontologyref', annotation_obj.ontologyref)

            label = ET.SubElement(annotation, 'label')
            label.text = annotation_obj.label
            value = ET.SubElement(annotation, 'value')
            value.text = annotation_obj.value
            valuetype = ET.SubElement(annotation, 'valuetype')
            valuetype.text = annotation_obj.valuetype

def add_peak_nodes(parent_element, parent_object):

    if parent_object.peaks:

        peaks = ET.SubElement(parent_element, 'peaks')

        for peak_obj in parent_object.peaks:
            peak = ET.SubElement(peaks, 'peak')
            peak.set('type', peak_obj.type)

            if peak_obj.scan is not None:
                scan = ET.SubElement(peak, 'scan')
                scan.text = peak_obj.scan

            if peak_obj.scan is not None:
                retentiontime = ET.SubElement(peak, 'retentiontime')
                retentiontime.text = peak_obj.retentiontime

            if peak_obj.mass is not None:
                mass = ET.SubElement(peak, 'mass')
                mass.text = peak_obj.mass

            if peak_obj.intensity is not None:
                intensity = ET.SubElement(peak, 'intensity')
                intensity.text = peak_obj.intensity

            if peak_obj.patternid is not None:
                patternid = ET.SubElement(peak, 'patternid')
                patternid.text = peak_obj.patternid

            if peak_obj.measurementid is not None:
                measurementid = ET.SubElement(peak, 'measurementid')
                measurementid.text = peak_obj.measurementid

            if peak_obj.sha1sum is not None:
                sha1sum = ET.SubElement(peak, 'sha1sum')
                sha1sum.text = peak_obj.sha1sum

            add_annotation_nodes(peak, peak_obj)

            if peak_obj.signal is not None:
                signal = ET.SubElement(peak, 'signal')
                signal.text = peak_obj.signal

            add_peak_nodes(peak, peak_obj)

            if peak_obj.peak_data is not None:
                peakdata = ET.SubElement(peak, 'peakdata')
                peakdata.set('type', peak_obj.peak_data.type)
                peakdata.set('size', peak_obj.peak_data.size)

                if peak_obj.peak_data.scanids is not None:
                    scanids = ET.SubElement(peakdata, 'scanids')
                    scanids.text = peak_obj.peak_data.get_encoded_scanids()

                if peak_obj.peak_data.retentiontimes is not None:
                    retentiontimes = ET.SubElement(peakdata, 'retentiontimes')
                    retentiontimes.text = peak_obj.peak_data.get_encoded_retentiontimes()

                if peak_obj.peak_data.masses is not None:
                    masses = ET.SubElement(peakdata, 'masses')
                    masses.text = peak_obj.peak_data.get_encoded_masses()

                if peak_obj.peak_data.intensities is not None:
                    intensities = ET.SubElement(peakdata, 'intensities')
                    intensities.text = peak_obj.peak_data.get_encoded_intensities()

                if peak_obj.peak_data.relativeintensities is not None:
                    relativeintensities = ET.SubElement(peakdata, 'relativeintensities')
                    relativeintensities.text = peak_obj.peak_data.get_encoded_relativeintensities()

                if peak_obj.peak_data.patternids is not None:
                    patternids = ET.SubElement(peakdata, 'patternids')
                    patternids.text = peak_obj.peak_data.get_encoded_patternids()

                if peak_obj.peak_data.measurementids is not None:
                    measurementids = ET.SubElement(peakdata, 'measurementids')
                    measurementids.text = peak_obj.peak_data.get_encoded_measurementids()             

def create_xml_from_peakml(data_obj):
    
    peakml = ET.Element('peakml')
    peakml.set('version', "1.0.0")
    header = ET.SubElement(peakml, 'header')

    nrpeaks = ET.SubElement(header, 'nrpeaks')
    nrpeaks.text = data_obj.header.nrpeaks
    date = ET.SubElement(header, 'date')
    date.text = data_obj.header.date
    owner = ET.SubElement(header, 'owner')
    owner.text = data_obj.header.owner
    description = ET.SubElement(header, 'description')
    description.text = data_obj.header.description

    sets = ET.SubElement(header, 'sets')

    for set_obj in data_obj.header.sets: 
        set = ET.SubElement(sets, 'set')

        id = ET.SubElement(set, 'id')
        id.text = set_obj.id
        type = ET.SubElement(set, 'type')
        type.text = set_obj.type
        measurementids = ET.SubElement(set, 'measurementids')
        measurementids.text = set_obj.measurementids

    measurements = ET.SubElement(header, 'measurements')

    for measurement_obj in data_obj.header.measurements:
        measurement = ET.SubElement(measurements, 'measurement')

        id = ET.SubElement(measurement, 'id')
        id.text = measurement_obj.id
        label = ET.SubElement(measurement, 'label')
        label.text = measurement_obj.label
        sampleid = ET.SubElement(measurement, 'sampleid')
        sampleid.text = measurement_obj.sampleid

        scans = ET.SubElement(measurement, 'scans')

        for scan_obj in measurement_obj.scans:
            scan = ET.SubElement(scans, 'scan')

            polarity = ET.SubElement(scan, 'polarity')
            polarity.text = scan_obj.polarity
            retentiontime = ET.SubElement(scan, 'retentiontime')
            retentiontime.text = scan_obj.retentiontime

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

    add_annotation_nodes(header, data_obj.header)
    
    add_peak_nodes(peakml, data_obj)

    return finalise_xml_formatting(prettify(peakml))