import pandas as pd
import Utilities as u
import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotIntensityAllItem import PlotIntensityAllItem

class PlotIntensityAllDataView(BaseDataView):
    def __init__(self):
        super().__init__(['SetID','Intensities'])

    def load_plot_data_for_selected_peak(self, selected_peak, peak_header):
        try: 
            self.clear_datalist()
            for set in peak_header.sets:
                
                # Get all the peaks for the set.
                measurement_peaks = self._get_peaks_with_measurement_ids(selected_peak.peaks, set.get_measurement_ids())

                intensities = []
                for peak in measurement_peaks:
                    intensities.append(peak.intensity)

                self.add_item(set.id, intensities)
            
            self.refresh_dataframe()
        except Exception as err:
            lg.log_error(f'Unable to update plot intensity data: {err}')


    def add_item(self, set_id, intensities):
        self.datalist.append(PlotIntensityAllItem(set_id, intensities))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "SetID": item.set_id,
                                                    "Intensities": item.intensities,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)

    # Returns the peak with one of the given list of measurement id's
    def _get_peaks_with_measurement_ids(self, peaks, measurement_ids):

        measurement_peaks = []

        for peak in peaks:
            peak_has_measurement = False
            peak_data_measurement_ids = peak.peak_data.get_measurement_ids()

            for peak_data_measurement_id in peak_data_measurement_ids:
                for measurement_id in measurement_ids:
                    if peak_data_measurement_id == measurement_id:
                        peak_has_measurement = True

            if peak_has_measurement:      
                measurement_peaks.append(peak)

        return measurement_peaks




