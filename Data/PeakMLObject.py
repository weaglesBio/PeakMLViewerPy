import base64
import Utilities as u

# Base objects

class Annotatable():
    def __init__(self):
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations.append(annotation)

class Annotation():
    def __init__(self, unit, ontologyref, label, value, valuetype):
        self.unit = unit
        self.ontologyref = ontologyref
        self.label = label
        self.value = value
        self.valuetype = valuetype

class IPeak(Annotatable):
    def __init__(self, mass, intensity, scanid, retentiontime):
        Annotatable.__init__(self)
        self.mass = mass #double
        self.intensity = intensity #double
        self.scanid = scanid #double
        self.retentiontime = retentiontime #double

class Header(Annotatable):
    def __init__(self, nrpeaks, date, owner, description):
        Annotatable.__init__(self)
        self.nrpeaks = nrpeaks # int
        self.date = date # Date datetime.datetime.now()
        self.owner = owner # string 
        self.description = description # string
        self.samples = []
        self.applications = []
        self.sets = []
        self.profiles = []
        self.measurements = []

    def add_sample(self, sample):
        self.samples.append(sample)

    def add_application(self, application):
        self.applications.append(application)

    def add_set(self, set):
        self.sets.append(set)

    def add_profile(self, profile):
        self.profiles.append(profile)
    
    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def get_measurement_by_id(self, measurement_id):
        for measurement in self.measurements:
           if measurement.id == measurement_id:
               return measurement
    
    def get_set_by_measurementid(self, measurement_id):
        for set in self.sets:
           if set.id == measurement_id:
               return set
            
class SampleInfo():
    def __init__(self, name, annotations):
        self.name = name #string
        self.annotations = annotations #string

class ApplicationInfo():
    def __init__(self, name, version, date, parameters):
        self.name = name #string
        self.version = version #string
        self.date = date #Date
        self.parameters = parameters #string

class SetInfo():
    def __init__(self, id, label, measurementids):
        self.id = id # int
        self.type = label # string
        self.measurementids = measurementids # string

class MeasurementInfo():
    def __init__(self, id, label, sampleid):
        self.id = id # int
        self.label = label # string
        self.sampleid = sampleid 
        self.scans = []
        self.files = []

    def add_scan(self, scan):
        self.scans.append(scan)

    def add_file(self, file):
        self.files.append(file)

class ScanInfo(Annotatable):
    def __init__(self, polarity, retention_time):
        self.polarity = polarity # int
        self.retentiontime = retention_time # string
        Annotatable.__init__(self)

class FileInfo(Annotatable):
    def __init__(self, label, name, location):
        Annotatable.__init__(self)
        self.label = label # string
        self.name = name # string
        self.location = location # string

class Peak(Annotatable):
    def __init__(self, type, scan, retentiontime, mass, intensity, measurementid, patternid, sha1sum, signal, peak_data):
        Annotatable.__init__(self)
        self.type = type
        self.scan = scan
        self.retentiontime = retentiontime
        self.mass = mass
        self.intensity = intensity
        self.measurementid = measurementid
        self.patternid = patternid
        self.sha1sum = sha1sum
        self.signal = signal
        self.peak_data = peak_data
        self.peaks = []
  
    def add_peak(self, peak):
        self.peaks.append(peak)

    def if_patternid_set(self):
        return (self.get_patternid() != 0)

    def get_type(self):
        return self.type

    def get_scanid(self):
        return self.scan

    def get_patternid(self):
        return self.patternid

    def get_mass(self):
        return self.mass

    def get_sha1sum(self):
        return self.sha1sum

    def get_retention_time_formatted(self):
        return u.format_time(self.get_retention_time())

    def get_retention_time(self):
        return self.retentiontime

    def get_intensity(self):
        return self.intensity

    def get_nr_peaks(self):
        return int(len(self.peaks))

class PeakData():
    def __init__(self, type, size):
        self.type = type
        self.size = size
        self.scanids = [] #double[]
        self.retentiontimes = [] #int[]
        self.masses = [] #int[]
        self.intensities = [] #double[]
        self.relativeintensities = [] #double[]
        self.patternids = [] #double[]
        self.measurementids = [] #double[]

    def get_encoded_scanids(self):
        encoded = base64.b64encode(self.scanids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_retentiontimes(self):
        encoded = base64.b64encode(self.retentiontimes)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_masses(self):
        encoded = base64.b64encode(self.masses)
        return encoded.decode("UTF-8")  #Converts from bytes to string
         
    def get_encoded_intensities(self):
        encoded = base64.b64encode(self.intensities)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_relativeintensities(self):
        encoded = base64.b64encode(self.relativeintensities)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_patternids(self):
        encoded = base64.b64encode(self.patternids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_measurementids(self):
        encoded = base64.b64encode(self.measurementids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def add_scanid(self, scanid):
        self.scanids.append(scanid)

    def add_retention_time(self, retention_time):
        self.retentiontimes.append(retention_time)

    def add_mass(self, mass):
        self.masses.append(mass)

    def add_intensity(self, intensity):
        self.intensities.append(intensity)

    def add_relative_intensity(self, relative_intensity):
        self.relativeintensities.append(relative_intensity)
    
    def add_patternid(self, patternid):
        self.patternids.append(patternid)

    def add_measurementid(self, measurementid):
        self.measurementids.append(measurementid)

    def get_retention_times(self):
        return self.retentiontimes

    def get_retention_times_formatted(self):

        rts = list(map(u.format_time,self.retentiontimes))
        #rts = []
        #for rt in range(0,len(self.retentiontimes)):
        #    rts[rt] = u.format_time(self.retentiontimes[rt])
    
        return rts

    def get_intensities(self):
        return self.intensities  #Converts from bytes to string

class PeakML():
    def __init__(self, header, peaks): 
        self.header = header
        if peaks:
            self.peaks = peaks
        else:
            peaks = []

    def get_peak_from_scanid(self, scanid):
        for peak in self.peaks:
           if peak.scanid == scanid:
               return peak

    def get_peak_from_sha1sum(self, sha1sum):
        for peak in self.peaks:
           if peak.sha1sum == sha1sum:
               return peak

