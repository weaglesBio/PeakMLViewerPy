import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.SetItem import SetItem

class SetDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Name','Color','Parent'])

    def load_data(self, peakml_header, colours):
        try:
            self.clear_datalist()

            # Set measurement colours from sets
            for set_info in peakml_header.sets:
                self.add_item(set_info.id, colours[f"S-{set_info.id}"], None)
                
                for set_measurement_id in set_info.linked_peak_measurement_ids:
                    measurement = peakml_header.get_measurement_by_id(set_measurement_id)

                    if measurement:
                        self.add_item(measurement.label, colours[f"M-{set_measurement_id}"], set_info.id)

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

    def get_checked_status_from_label(self, label: str) -> bool:
        return self.dataframe.loc[self.dataframe["Name"] == label,"Checked"].values[0]
