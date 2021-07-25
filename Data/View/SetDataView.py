import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.SetItem import SetItem

class SetDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Name','Color','Parent'])

    #TODO: So not dependent on selected peak
    def load_data(self, selected_peak, peakml_header):
        try:
            self.clear_datalist()

            # Need seperate colours dictionary.


            # Set measurement colours from sets
            for set_info in peakml_header.sets:
                self.add_item(set_info.id, set_info.colour, None)
                measurement_peaks = self._get_peaks_with_measurementids(selected_peak.peaks, set_info.get_measurement_ids())


                # Get measurement ids for a peak
                for measurement_peak in measurement_peaks:
                    measurement = peakml_header.get_measurement_by_id(measurement_peak.measurement_id)
                    measurement.colour = set_info.colour                   
                    self.add_item(measurement.label, set_info.colour, set_info.id)

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update set data: {err}')

    def add_item(self, name, color, parent):
        self.datalist.append(SetItem(name, color, parent))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "Name": item.name,
                                                    "Color": item.color,
                                                    "Parent": item.parent,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)

    # Returns the peak with one of the given list of measurement id's


    #takes list of measurement ids in a set and the subpeaks of the currently selected peak.
    # Each of these sub peaks has a list of measurement ids stored in its peakdata
    # if any of these measurement ids are included in the sets list of measurement ids then it is included.

    # it is a method of filtering the the peak measurement ids

    def _get_peaks_with_measurementids(self, peaks, measurement_ids):

        measurement_peaks = []

        for peak in peaks:
            peak_has_measurement = False

            # the peak data section of a sub peak has a list of measurement ids()
            peak_data_measurement_ids = peak.peak_data.get_measurement_ids()

            for peak_data_measurement_id in peak_data_measurement_ids:
                for measurement_id in measurement_ids:
                    if peak_data_measurement_id == measurement_id:
                        peak_has_measurement = True

            if peak_has_measurement:      
                measurement_peaks.append(peak)

        return measurement_peaks


    def get_checked_status_from_label(self, label: str) -> bool:
        return self.dataframe.loc[self.dataframe["Name"] == label,"Checked"].values[0]
