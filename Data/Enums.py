from enum import Enum

class FilterType(Enum):
    FilterMass = 1
    FilterIntensity = 2
    FilterRetentionTime = 3
    FilterNumberDetections = 4
    FilterAnnotations = 5
    FilterSort = 6
    FilterSortTimeSeries = 7

class SortType(Enum):
    MassAsc = 1
    MassDesc = 2
    IntensityAsc = 3
    IntensityDesc = 4
    RetentionTimeAsc = 5
    RetentionTimeDesc = 6

