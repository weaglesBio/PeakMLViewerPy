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
                self.add_item(filter.uid, filter.get_type_value(), filter.get_settings_value())
        
            self.refresh_dataframe()
        except Exception as err:
            lg.log_error(f'Unable to load filter data: {err}')

    def add_item(self, filter_id, type, settings):
        self.datalist.append(FilterItem(filter_id, type, settings))

    def refresh_dataframe(self):
        self.clear_dataframe()

        if len(self.datalist) > 0:
            for item in self.datalist:
                self.dataframe = self.dataframe.append({
                                                        "UID": item.uid,
                                                        "Type": item.type,
                                                        "Settings": item.settings,
                                                        "Selected": item.selected,
                                                        "Checked": item.checked,
                                                    }, ignore_index=True)

            # If no items are selected,                                        
            if len(self.dataframe.loc[self.dataframe["Selected"] == True]) == 0:
                # set the first one as selected.
                self.dataframe.at[0, 'Selected'] = True