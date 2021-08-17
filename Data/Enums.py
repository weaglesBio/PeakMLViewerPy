from enum import Enum

class FilterType(Enum):
    FilterMass = 1
    FilterIntensity = 2
    FilterRetentionTime = 3
    FilterNumberDetections = 4
    FilterAnnotations = 5
    FilterProbability = 6
    FilterSort = 7
    FilterSortTimeSeries = 8

class SortType(Enum):
    MassAsc = 1
    MassDesc = 2
    IntensityAsc = 3
    IntensityDesc = 4
    RetentionTimeAsc = 5
    RetentionTimeDesc = 6

