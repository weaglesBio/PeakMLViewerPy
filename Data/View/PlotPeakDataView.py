import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotPeakItem import PlotPeakItem

class PlotPeakDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Label','RT_values','Intensity_values','Colour'])

    def load_plot_data_for_selected_peak(self, peak, peakml_header, colours):
        
        try:
            self.clear_datalist()

            for peak in peak.peaks:
                measurement = peakml_header.get_measurement_by_id(peak.measurement_id)
                label = measurement.label
                retention_times = peak.peak_data.get_retention_times_formatted_datetime() 
                intensities = peak.peak_data.get_intensities()

                self.add_item(label, retention_times, intensities, colours[f"M-{measurement.id}"])

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update plot peak data: {err}')

    def add_item(self, label, retention_times, intensities, color):
        self.datalist.append(PlotPeakItem(label, retention_times, intensities, color))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "Label": item.label,
                                                    "RT_values": item.rt_values,
                                                    "Intensity_values": item.intensity_values,
                                                    "Colour": item.colour,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)





