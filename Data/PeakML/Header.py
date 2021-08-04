from Data.PeakML.SampleInfo import SampleInfo
from Data.PeakML.ApplicationInfo import ApplicationInfo
from Data.PeakML.MeasurementInfo import MeasurementInfo
from Data.PeakML.SetInfo import SetInfo
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
    def samples(self) -> list[SampleInfo]:
        return self._samples
    
    @property
    def applications(self) -> list[ApplicationInfo]:
        return self._applications

    @property
    def sets(self) -> list[SetInfo]:
        return self._sets

    # @property
    # def profiles(self) -> list[str]:
    #     return self._profiles

    @property
    def measurements(self) -> list[str]:
        return self._measurements

    def add_sample(self, sample: SampleInfo):
        self.samples.append(sample)

    def add_application(self, application: ApplicationInfo):
        self.applications.append(application)

    def add_set(self, set: SetInfo):
        self.sets.append(set)

    # def add_profile(self, profile: str):
    #     self.profiles.append(profile)
    
    def add_measurement(self, measurement: MeasurementInfo):
        self.measurements.append(measurement)

    def get_measurement_by_id(self, measurement_id: int):
        for measurement in self.measurements:
           if measurement.id == str(measurement_id):
               return measurement