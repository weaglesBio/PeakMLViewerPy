import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotIntensityLogItem import PlotIntensityLogItem

class PlotIntensityLogDataView(BaseDataView):
    def __init__(self):
        super().__init__(['SetID','Intensities'])

    def load_plot_data_for_selected_peak(self, selected_peak, peakml_header):
        try:  
            
            self.clear_datalist()

            for set in peakml_header.sets:
                intensities = []
                for peak in selected_peak.peaks:
                    if peak.measurement_id in set.linked_peak_measurement_ids:
                        intensities.append(peak.intensity)

                self.add_item(set.id, intensities)

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update plot intensity data: {err}')


    def add_item(self, set_id, intensities):
        self.datalist.append(PlotIntensityLogItem(set_id, intensities))

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




