import Utilities as u
import Logger as lg
import math as m

from Data.View.BaseDataView import BaseDataView
from Data.View.EntryItem import EntryItem

class EntryDataView(BaseDataView):
    def __init__(self):

        self._mass_min = None
        self._mass_max = None
        self._intensity_min = None
        self._intensity_max = None
        self._retention_time_min = None
        self._retention_time_max = None
        self._sample_count_min = None
        self._sample_count_max = None

        super().__init__(['Type','RT','Mass','Intensity','Nrpeaks','HasAnnotation'])

    # @property
    # def selected_peak_uid(self):
    #     return self._selected_peak_uid

    # @selected_peak_uid.setter
    # def selected_peak_uid(self, selected_peak_uid: str):
    #     self._selected_peak_uid = selected_peak_uid

    @property
    def nr_peaks(self) -> int:
        return len(self.dataframe)

    @property
    def nr_peaks_total(self) -> int:
        return self.dataframe["Nrpeaks"].sum()

    @property
    def mass_min(self) -> float:
        return self._mass_min

    @property
    def mass_max(self) -> float:
        return self._mass_max

    @property
    def intensity_min(self) -> float:
        return self._intensity_min

    @property
    def intensity_max(self) -> float:
        return self._intensity_max

    @property
    def retention_time_min(self) -> float:
        return self._retention_time_min

    @property
    def retention_time_max(self) -> float:
        return self._retention_time_max

    @property
    def sample_count_min(self) -> float:
        return self._sample_count_min

    @property
    def sample_count_max(self) -> float:
        return self._sample_count_max
    
    def load_data(self, peak_dic):
        try: 
            self.clear_datalist()

            self._mass_min = None
            self._mass_max = None
            self._intensity_min = None
            self._intensity_max = None

            # Loop through peakml peak dictionary
            for peak_uid in peak_dic.keys():
                
                peak = peak_dic[peak_uid]
                type = peak.type
                retention_time = u.format_time_string(peak.retention_time)
                mass = peak.mass
                intensity = peak.intensity
                nr_peaks = round(len(peak.peaks))
                has_annotation = True if peak.get_specific_annotation('identification') else False

                self.add_item(peak_uid, type, retention_time, mass, intensity, nr_peaks, has_annotation)
            
                mass = float(mass)
                intensity = float(intensity)

                if self.mass_min is None and self.mass_max is None:
                    self._mass_min = m.floor(mass)
                    self._mass_max = m.ceil(mass)
                elif self.mass_min > mass:
                    self._mass_min = m.floor(mass)
                elif self.mass_max < mass:
                    self._mass_max = m.ceil(mass)

                if self.intensity_min is None and self.intensity_max is None:
                    self._intensity_min = m.floor(intensity)   
                    self._intensity_max = m.ceil(intensity)    
                elif self.intensity_min > intensity:
                    self._intensity_min = m.floor(intensity)
                elif self.intensity_max < intensity:
                    self._intensity_max = m.ceil(intensity)

                if self.retention_time_min is None and self.retention_time_max is None:
                    self._retention_time_min = retention_time   
                    self._retention_time_max = retention_time   
                elif self.retention_time_min > retention_time:
                    self._retention_time_min = retention_time
                elif self.retention_time_max < retention_time:
                    self._retention_time_max = retention_time

                if self.sample_count_min is None and self.sample_count_max is None:
                    self._sample_count_min = nr_peaks   
                    self._sample_count_max = nr_peaks   
                elif self.sample_count_min > nr_peaks:
                    self._sample_count_min = nr_peaks
                elif self.sample_count_max < nr_peaks:
                    self._sample_count_max = nr_peaks

            self.refresh_dataframe()
        except Exception as err:
            lg.log_error(f'Unable to load entry data: {err}')

    def add_item(self, uid, type, retention_time, mass, intensity, nr_peaks, has_annotation):
        self.datalist.append(EntryItem(uid, type, retention_time, mass, intensity, nr_peaks, has_annotation))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "Type": item.type,
                                                    "RT": item.retention_time,
                                                    "Mass": u.convert_float_to_sf(item.mass),
                                                    "Intensity": u.convert_float_to_sf(item.intensity),
                                                    "Nrpeaks": item.nr_peaks,
                                                    "HasAnnotation": item.has_annotation,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)

        # If no items are selected, 
        if len(self.dataframe.loc[self.dataframe["Selected"] == True]) == 0:  
            # set the first one as selected.
            self.dataframe.at[0, 'Selected'] = True

    def get_checked_entries_uid(self):
        selected_df = self.dataframe.loc[self.dataframe["Checked"] == True]
        return selected_df["UID"].tolist()

    
    def check_if_any_checked(self):
        for item in self.datalist:
            if item.checked == True:
                return True

        return False