import pandas as pd
import Utilities as u
import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.FilterItem import FilterItem
from Data.Filter.BaseFilter import BaseFilter

class FilterDataView(BaseDataView):
    def __init__(self):
        super().__init__(['ID','Type','Settings'])

    def load_data(self, filters: list[BaseFilter]):    
        try: 
            self.clear_datalist()
            
            for filter in filters:
                self.add_item(filter.uid,filter.get_type_value(),filter.get_settings_value())
        
            self.refresh_dataframe()
        except Exception as err:
            lg.log_error(f'Unable to load filter data: {err}')

    def add_item(self, id, type, settings):
        self.datalist.append(FilterItem(id, type, settings))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "ID": item.id,
                                                    "Type": item.type,
                                                    "Settings": item.settings,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)




