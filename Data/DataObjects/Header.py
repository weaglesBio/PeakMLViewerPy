from Data.DataObjects.Annotatable import Annotatable

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

    def get_sets(self):
        return self.sets

    def add_set(self, set):
        self.sets.append(set)

    def add_profile(self, profile):
        self.profiles.append(profile)
    
    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def get_measurement_by_id(self, measurement_id):
        for measurement in self.measurements:
           if measurement.id == str(measurement_id):
               return measurement

    def get_measurement_by_sampleid(self, measurement_sampleid):
        for measurement in self.measurements:
           if measurement.sampleid == str(measurement_sampleid):
               return measurement

    def get_measurement_by_uid(self, measurement_uid):
        for measurement in self.measurements:
           if measurement.get_uid() == measurement_uid:
               return measurement
    
    def get_set_by_measurementid(self, measurement_id):
        for set in self.sets:
           if set.id == measurement_id:
               return set

    def get_measurements(self):
        return self.measurements
            
