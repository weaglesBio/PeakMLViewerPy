import pandas as pd

from Data.View.BaseItem import BaseItem

from typing import List

class BaseDataView():
    def __init__(self, dataframe_columns: List[str]):
            self.datalist = []
            dataframe_columns.insert(0, 'UID')
            dataframe_columns.append('Selected')
            dataframe_columns.append('Checked')
            self.dataframe = pd.DataFrame(columns=dataframe_columns) 
            self.dataframe.set_index('UID') 

    @property
    def datalist(self) -> List[BaseItem]:
        return self._datalist
    
    @datalist.setter
    def datalist(self, datalist: List[BaseItem]):
        self._datalist = datalist

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe
    
    def clear_datalist(self):
        self.datalist = []

    def clear_dataframe(self):
        self.dataframe = self.dataframe.iloc[0:0]

    def update_selected(self, uid: str):   

        # Update datalist
        for item in self.datalist:
            if item.uid == uid :
                item.selected = True
            else:
                item.selected = False

        # Update dataframe
        # Set all values to false
        self.dataframe.loc[:,'Selected'] = False
        
        # Set row based on uid values
        self.dataframe.loc[self.dataframe["UID"] == uid, 'Selected'] = True

    def update_checked_status(self, uid: str, checked: bool):
        # Update datalist
        for item in self.datalist:
            if item.uid == uid:
                item.checked = checked

        # Update dataframe
        self.dataframe.loc[self.dataframe["UID"] == uid, 'Checked'] = checked