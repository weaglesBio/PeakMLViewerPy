from Data.Filter.BaseFilter import BaseFilter
from Data.PeakML.Peak import Peak
from Data.PeakML.PeakML import PeakML
from Data.Settings import Settings
from Data.View.EntryDataView import EntryDataView
from Data.View.FilterDataView import FilterDataView
from Data.View.PlotPeakDataView import PlotPeakDataView
from Data.View.PlotDerivativesDataView import PlotDerivativesDataView
from Data.View.PlotIntensityDataView import PlotIntensityDataView
from Data.View.SetDataView import SetDataView
from Data.View.AnnotationDataView import AnnotationDataView
from Data.View.IdentificationDataView import IdentificationDataView
from Data.Filter.MassFilter import MassFilter
from Data.Filter.IntensityFilter import IntensityFilter
from Data.Filter.RetentionTimeFilter import RetentionTimeFilter
from Data.Filter.NumberDetectionsFilter import NumberDetectionsFilter
from Data.Filter.AnnotationFilter import AnnotationFilter
from Data.Filter.SortFilter import SortFilter
from Data.Filter.SortTimeSeriesFilter import SortTimeSeriesFilter

from typing import Type, List, Dict, Tuple
import copy
import statistics as stats

import IO.MoleculeIO as MolIO
import IO.SettingsIO as SetIO

import Logger as lg
import Utilities as u
import Progress as p

import pandas as pd
import os.path

class DataAccess:

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def entry_view_dataframe(self) -> pd.DataFrame:
        return self._entry_view.dataframe

    @property
    def filter_view_dataframe(self) -> pd.DataFrame:
        return self._filter_view.dataframe
    
    @property
    def plot_peak_view_dataframe(self) -> pd.DataFrame:
        return self._plot_peak_view.dataframe

    @property
    def plot_der_view_dataframe(self) -> pd.DataFrame:
        return self._plot_der_view.dataframe
    
    @property
    def plot_int_view_dataframe(self) -> pd.DataFrame:
        return self._plot_int_view.dataframe
    
    @property
    def set_view_dataframe(self) -> pd.DataFrame:
        return self._set_view.dataframe
    
    @property
    def annotation_view_dataframe(self) -> pd.DataFrame:
        return self._annotation_view.dataframe

    @property
    def identification_view_dataframe(self) -> pd.DataFrame:
        return self._identification_view.dataframe

    @property
    def import_peakml_path(self) -> str:
        return os.path.split(self.import_peakml_filepath)[0]

    @property
    def import_peakml_filename(self) -> str:
        return os.path.split(self.import_peakml_filepath)[1]

    @property
    def import_peakml_filepath(self) -> str:
        return self._import_peakml_filepath

    @import_peakml_filepath.setter
    def import_peakml_filepath(self, import_peakml_filepath: str):
        self._import_peakml_filepath = import_peakml_filepath

    @property
    def import_ipa_filepath(self) -> str:
        return self._import_ipa_filepath

    @import_ipa_filepath.setter
    def import_ipa_filepath(self, import_ipa_filepath: str):
        self._import_ipa_filepath = import_ipa_filepath

    @property
    def export_peakml_filepath(self) -> str:
        return self._export_peakml_filepath

    @export_peakml_filepath.setter
    def export_peakml_filepath(self, export_peakml_filepath: str):
        self._export_peakml_filepath = export_peakml_filepath

    @property
    def selected_entry_uid(self) -> str:
        # Get first row with selected is true from entry
        df = self.entry_view_dataframe
        selected_df = df.loc[df["Selected"] == True]
        return selected_df["UID"].values[0]

    @selected_entry_uid.setter
    def selected_entry_uid(self, uid: str):
        self._entry_view.update_selected(uid)

    @property
    def selected_retention_time(self) -> str:

        peak = self._peakml.peaks[self.selected_entry_uid]

        if u.is_float(peak.retention_time):
            return u.format_time_string(float(peak.retention_time))
        else:
            return None

    @property
    def selected_filter_uid(self) -> str:
        # Get first row with selected is true from entry
        df = self.filter_view_dataframe
        selected_df = df.loc[df["Selected"] == True]
        return selected_df["UID"].values[0]

    @selected_filter_uid.setter
    def selected_filter_uid(self, uid: str):
        self._filter_view.update_selected(uid)

    @property
    def selected_identification_uid(self) -> str:
        # Get first row with selected is true from entry
        df = self.identification_view_dataframe
        selected_df = df.loc[df["Selected"] == True]
        return selected_df["UID"].values[0]

    @selected_identification_uid.setter
    def selected_identification_uid(self, uid: str):
        self._identification_view.update_selected(uid)

    @property
    def nr_peaks_details(self) -> str:
        return f"{str(self._entry_view.nr_peaks)} ({str(self._entry_view.nr_peaks_total)})"

    @property
    def ipa_imported(self) -> bool:
        return self._ipa_imported

    @property
    def prior_probabilities_modified(self) -> bool:
        return self._prior_probabilities_modified

    @property 
    def measurement_colours(self) -> Dict[str, str]:
        return self._measurement_colours

    @property 
    def peak_split_retention_time(self) -> str:
        return self._peak_split_retention_time

    @peak_split_retention_time.setter
    def peak_split_retention_time(self, peak_split_retention_time: str):
        self._peak_split_retention_time = peak_split_retention_time

    def __init__(self):

        self._peakml = PeakML()
        
        self._molecule_database = MolIO.load_molecule_databases()
        self._settings = Settings(SetIO.load_preferences(), SetIO.load_database_paths())
        
        self._filters = []
        self._measurement_colours = {}
        self._ipa_imported = False
        self._prior_probabilities_modified = False

        self._entry_view = EntryDataView()
        self._filter_view = FilterDataView()
        self._plot_peak_view = PlotPeakDataView()
        self._plot_der_view = PlotDerivativesDataView()
        self._plot_int_view = PlotIntensityDataView()
        # self._plot_int_log_view = PlotIntensityLogDataView()      
        self._set_view = SetDataView()
        self._annotation_view = AnnotationDataView()
        self._identification_view = IdentificationDataView()

    # Import Peakml object data
    def import_peakml_data(self):
        try:
            p.update_progress("Importing PeakML file.", 5)
            import_succeded = self._peakml.import_from_file(self.import_peakml_filepath)

            if import_succeded:
                self.assign_measurement_colours()

                p.update_progress("Loading view data.", 20)
                self.load_view_data_from_peakml()

                self._ipa_imported = False
                self._prior_probabilities_modified = False

        except Exception as err:
            lg.log_error(f'An error when importing peakML data: {err}')

    def import_ipa_data(self):
        try:
            p.update_progress("Importing IPA file.", 5)
            self._peakml.import_ipa_from_file(self.import_ipa_filepath)

            p.update_progress("Loading view data.", 20)
            self.load_view_data_from_peakml()

            self._ipa_imported = True
            self._prior_probabilities_modified = False

        except Exception as err:
            lg.log_error(f'An error when importing IPA data: {err}')

    # Load view data from peakml object
    def load_view_data_from_peakml(self):

        try:
            lg.log_progress("Begin load view data from PeakML")

            filtered_peaks = self.filter_peaks(self._peakml.peaks)

            p.update_progress("Loading entry view data", 20)
            self._entry_view.load_data(filtered_peaks)
            lg.log_progress("Entry view data loaded.")

            p.update_progress("Loading filter view data", 27)
            self._filter_view.load_data(self._filters)
            lg.log_progress("Filter view data loaded.")

            p.update_progress("Loading set view data", 30)
            self._set_view.load_data(self._peakml.header, self.measurement_colours)
            lg.log_progress("Set view data loaded.")
            
            self.update_selected_entry()

        except Exception as err:
            lg.log_error(f'An error when loading view data: {err}')

    def assign_measurement_colours(self):
        self._measurement_colours = {}

        set_count = len(self._peakml.header.sets)
        colours = u.get_colours(set_count)

        for i in range(set_count):
            set = self._peakml.header.sets[i]
            self._measurement_colours[f"S-{set.id}"] = colours[i]

            for measurement_id in set.linked_peak_measurement_ids:
                self._measurement_colours[f"M-{measurement_id}"] = colours[i]

    def update_selected_entry(self):

        try:
            lg.log_progress("Begin load view data for selected entry.")

            filtered_peaks = self.filter_peaks(self._peakml.peaks)
            selected_peak = self._peakml.get_peak_by_uid(self.selected_entry_uid)

            p.update_progress("Loading peak plot data", 32)
            self._plot_peak_view.load_plot_data_for_selected_peak(selected_peak, self._peakml.header, self.measurement_colours)
            lg.log_progress("Peak plot data loaded.")

            p.update_progress("Loading derivatives plot data", 35)
            self._plot_der_view.load_plot_data_for_selected_peak(selected_peak, filtered_peaks)
            lg.log_progress("Derivatives plot data loaded.")

            p.update_progress("Loading intensity plot data", 37)
            self._plot_int_view.load_plot_data_for_selected_peak(selected_peak, self._peakml.header)
            lg.log_progress("Intensity plot data loaded.")
            
            p.update_progress("Loading annotation view data", 42)
            self._annotation_view.load_data_for_selected_peak(selected_peak)
            lg.log_progress("Annotation view data loaded.")

            p.update_progress("Loading identification view data", 45)
            self._identification_view.load_data_for_selected_peak(selected_peak, self._molecule_database)
            lg.log_progress("Identification view data loaded.")

        except Exception as err:
            lg.log_error(f'An error when loading selected entry data: {err}')

    # Export PeakML object data to file
    def export_peakml(self):
        self._peakml.export(self.export_peakml_filepath)

    def update_entry_checked_status(self, uid: str, checked: bool):
        self._entry_view.update_checked_status(uid, checked)

    def update_set_checked_status(self, uid: str, checked: bool):
        self._set_view.update_checked_status(uid, checked)

    def update_identification_checked_status(self, uid: str, checked: bool):
        self._identification_view.update_checked_status(uid, checked)

    def check_if_any_checked_entries(self) -> bool:
        return self._entry_view.check_if_any_checked()

    def remove_checked_entries(self):
        for uid_to_delete in self._entry_view.get_checked_entries_uid():
            self._peakml.remove_peak_by_uid(uid_to_delete)

        #TODO: Change to remove the rows and only reload if selected has been removed.

        self.load_view_data_from_peakml()

    def get_selected_identification_details(self) -> Tuple[str, str, str, str]:
        uid, id, prior, notes = self._identification_view.get_details(self.selected_identification_uid)
        return uid, id, prior, notes

    def check_if_any_checked_identifications(self) -> bool:
        return self._identification_view.check_if_any_checked()

    def remove_checked_identifications(self):
        prior_updated = self._identification_view.remove_checked(self.ipa_imported)

        if prior_updated:
            self._prior_probabilities_modified = True

        #Save updated identification dataframe to selected peak. 
        self.update_peak_identifications()

    def update_identification_details(self, uid: str, prior: str, notes: str):
        prior_updated = self._identification_view.update_details(uid, prior, notes)

        if prior_updated:
            self._prior_probabilities_modified = True
        
        #Save updated identification dataframe to selected peak. 
        self.update_peak_identifications()
 
    def update_peak_identifications(self):
        #Save updated identification dataframe to selected peak. 
        ann_identification, ann_ppm, ann_adduct, ann_prior, ann_post, ann_notes = self._identification_view.get_identification_annotations()
        
        peak = self._peakml.peaks[self.selected_entry_uid]
        peak.update_specific_annotation('identification',ann_identification)
        peak.update_specific_annotation('ppm',ann_ppm)
        peak.update_specific_annotation('adduct',ann_adduct)

        peak.update_specific_annotation('prior',ann_prior)
        peak.update_specific_annotation('post',ann_post)
            #self._prior_probabilities_modified = True
        
        peak.update_specific_annotation('notes',ann_notes)
        self._peakml.peaks[self.selected_entry_uid] = peak

    def get_set_checked_status(self, label: str) -> bool:
        return self._set_view.get_checked_status_from_label(label)


    def split_selected_peak_on_retention_time(self):
        
        original_peak = self._peakml.peaks[self.selected_entry_uid]

        try: 
            # Duplicate peak
            peak_lower = self._peakml.peaks[self.selected_entry_uid]
            peak_higher = copy.deepcopy(peak_lower)

            # Remove lower values from peak.
            peak_lower = self.remove_peak_values_by_retention_time(peak_lower, True)

            # Remove higher values from peak.
            peak_higher = self.remove_peak_values_by_retention_time(peak_higher, False)

            self._peakml.peaks[self.selected_entry_uid] = peak_lower
            self._peakml.peaks[u.get_new_uuid()] = peak_higher

            # Reload data from peakml file
            self.load_view_data_from_peakml()

        except Exception as err:
            lg.log_error(f'An error when splitting peak: {err}')
            #restore modified peak
            self._peakml.peaks[self.selected_entry_uid] = original_peak
        
    def remove_peak_values_by_retention_time(self, peak: Peak, keep_lower: bool) -> Peak: 
        
        rt_split = u.format_time_float(self.peak_split_retention_time)

        intensity_values = []
        mass_values = []
        rt_values = []

        updated_peaks = []

        for i in range(len(peak.peaks)):
            child_peak = peak.peaks[i]
            # Filter retention times 
            remaining_retention_times = []
            
            original_count = len(child_peak.peak_data.retention_times)

            for j in range(len(child_peak.peak_data.retention_times)):
                rt_value = child_peak.peak_data.retention_times[j]
                # If less than peak split point and keeping higher
                if rt_value <= rt_split and not keep_lower:
                    continue
                # If more than peak split point and keeping lower
                elif rt_value > rt_split and keep_lower:
                    continue
                else:
                    remaining_retention_times.append(rt_value)

            # Find how many values left, 
            remaining_count = len(remaining_retention_times)

            if remaining_count:

            # Update retention times
                child_peak.peak_data.retention_times = remaining_retention_times

                # Drop all from each in that direction from peakdata
                if keep_lower:
                    child_peak.peak_data.scan_ids = child_peak.peak_data.scan_ids[:remaining_count]
                    child_peak.peak_data.masses = child_peak.peak_data.masses[:remaining_count]
                    child_peak.peak_data.intensities = child_peak.peak_data.intensities[:remaining_count]
                    child_peak.peak_data.relative_intensities = child_peak.peak_data.relative_intensities[:remaining_count]
                    child_peak.peak_data.pattern_ids = child_peak.peak_data.pattern_ids[:remaining_count]
                    child_peak.peak_data.measurement_ids = child_peak.peak_data.measurement_ids[:remaining_count]
                else:
                    child_peak.peak_data.scan_ids = child_peak.peak_data.scan_ids[original_count-remaining_count:]
                    child_peak.peak_data.masses = child_peak.peak_data.masses[original_count-remaining_count:]
                    child_peak.peak_data.intensities = child_peak.peak_data.intensities[original_count-remaining_count:]
                    child_peak.peak_data.relative_intensities = child_peak.peak_data.relative_intensities[original_count-remaining_count:]
                    child_peak.peak_data.pattern_ids = child_peak.peak_data.pattern_ids[original_count-remaining_count:]
                    child_peak.peak_data.measurement_ids = child_peak.peak_data.measurement_ids[original_count-remaining_count:]

                child_peak.retention_time = stats.mean(child_peak.peak_data.retention_times)
                child_peak.mass = stats.mean(child_peak.peak_data.masses)
                child_peak.intensity = max(child_peak.peak_data.intensities)

                rt_values.append(child_peak.retention_time)
                mass_values.append(child_peak.mass)
                intensity_values.append(child_peak.intensity)

                updated_peaks.append(child_peak)

        peak.retention_time = stats.mean(rt_values)
        peak.mass = stats.mean(mass_values)
        peak.intensity = max(intensity_values)

        # Peak is not included if no retention values within the window.
        peak.peaks = updated_peaks
                    
        return peak

#region Filters

    def add_filter(self, filter: Type[BaseFilter]):
        self._filters.append(filter)
        self.load_view_data_from_peakml()

    def add_filter_mass(self, mass_min: float, mass_max: float): #, formula, formula_ppm, mass_charge, filter_option
        self.add_filter(MassFilter(mass_min, mass_max)) #, formula, formula_ppm, mass_charge, filter_option

    def add_filter_intensity(self, intensity_min: float):
        self.add_filter(IntensityFilter(intensity_min))

    def add_filter_retention_time(self, retention_time_min_hr: int, retention_time_max_hr: int, retention_time_min_minu: int, retention_time_max_minu: int):
        self.add_filter(RetentionTimeFilter(retention_time_min_hr, retention_time_max_hr, retention_time_min_minu, retention_time_max_minu))

    def add_filter_number_detections(self, detection_number: int):
        self.add_filter(NumberDetectionsFilter(detection_number))

    # def add_filter_annotations(self, annotation_name, annotation_relation, annotation_value):
    #     self.add_filter(AnnotationFilter(annotation_name, annotation_relation, annotation_value))

    # def add_filter_sort(self):
    #     print("Not implemented")

    # def add_filter_sort_times_series(self):
    #     print("Not implemented")

    def remove_filter_by_id(self, id: str):
        updated_filter_list = []
        for filter in self._filters:
            if filter.uid != id:
                updated_filter_list.append(filter)

        self._filters = updated_filter_list
        self.load_view_data_from_peakml()

    def get_min_max_mass(self) -> Tuple[int, int]:
        return self._entry_view.mass_min, self._entry_view.mass_max

    def get_min_max_intensity(self) -> Tuple[int, int]:
        return self._entry_view.intensity_min, self._entry_view.intensity_max

    def get_min_max_retention_time(self) -> Tuple[str, str]:
        return self._entry_view.retention_time_min, self._entry_view.retention_time_max

    def get_min_max_samples_count(self) -> Tuple[int, int]:
        return self._entry_view.sample_count_min, self._entry_view.sample_count_max

    def filter_peaks(self, peaks_dic: Dict[str, Peak]):
    
        for filter in self._filters:
            peaks_dic = filter.apply_to_peak_list(peaks_dic)

        return peaks_dic

#endregion

#region Settings
    def get_settings_preference_by_name(self, name: str):
        return self.settings.get_preference_by_name(name)

    def get_settings_database_paths(self) -> str:
        database_paths = self.settings.get_database_paths()
        df = pd.DataFrame()
        for path in database_paths:
            filename = os.path.split(path)[1]
            df = df.append({"Name": filename, "Path": path}, ignore_index=True)

        return df

    def update_settings(self, decdp: int, databases: List[str]):

        self.settings.set_preference_by_name("decdp", decdp)
        self.settings.set_database_paths(databases["Path"].tolist())
        SetIO.write_settings(self.settings)

#endregion

