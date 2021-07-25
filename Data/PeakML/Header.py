from Data.PeakML.AnnotatableEntity import AnnotatableEntity

class Header(AnnotatableEntity):
    def __init__(self, nr_peaks: str = "", date: str = "", owner: str = "", description: str = ""):
        AnnotatableEntity.__init__(self)
        
        # PeakML attributes
        self.nr_peaks = nr_peaks
        self.date = date
        self.owner = owner
        self.description = description

        #TODO: Replace these with dictionaries?
        self._samples = []
        self._applications = []
        self._sets = []
        self._profiles = []
        self._measurements = []

    @property
    def nr_peaks(self) -> str:
        return self._nr_peaks
    
    @nr_peaks.setter
    def nr_peaks(self, nr_peaks: str):
        self._nr_peaks = nr_peaks

    @property
    def date(self) -> str:
        return self._date
    
    @date.setter
    def date(self, date: str):
        self._date = date

    @property
    def owner(self) -> str:
        return self._owner
    
    @owner.setter
    def owner(self, owner: str):
        self._owner = owner

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def samples(self) -> list[str]:
        return self._samples
    
    @property
    def applications(self) -> list[str]:
        return self._applications

    @property
    def sets(self) -> list[str]:
        return self._sets

    @property
    def profiles(self) -> list[str]:
        return self._profiles

    @property
    def measurements(self) -> list[str]:
        return self._measurements

    def add_sample(self, sample: str):
        self.samples.append(sample)

    def add_application(self, application: str):
        self.applications.append(application)

    def add_set(self, set: str):
        self.sets.append(set)

    def add_profile(self, profile: str):
        self.profiles.append(profile)
    
    def add_measurement(self, measurement: str):
        self.measurements.append(measurement)

    def get_measurement_by_id(self, measurement_id: int):
        for measurement in self.measurements:
           if measurement.id == str(measurement_id):
               return measurement

    def get_measurement_by_sample_id(self, measurement_sample_id: int):
        for measurement in self.measurements:
           if measurement.sample_id == str(measurement_sample_id):
               return measurement

    def get_measurement_by_uid(self, measurement_uid: int):
        for measurement in self.measurements:
           if measurement.uid == measurement_uid:
               return measurement
    
    def get_set_by_measurement_id(self, measurement_id):
        for set in self.sets:
           if set.id == measurement_id:
               return set