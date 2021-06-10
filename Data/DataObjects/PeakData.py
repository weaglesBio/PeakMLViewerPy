import base64
import Utilities as u

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

    def get_retention_times_formatted_string(self):
        rts = list(map(u.format_time_string,self.retentiontimes))
        return rts

    def get_retention_times_formatted_datetime(self):
        rts = list(map(u.format_time_datetime,self.retentiontimes))
        return rts

    def get_intensities(self):
        intensities = list(map(float,self.intensities))
        return intensities  #Converts from bytes to string
