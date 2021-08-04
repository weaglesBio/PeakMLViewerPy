from Data.View.BaseItem import BaseItem

class PlotIntensityItem(BaseItem):
    def __init__(self, set_id: str = "", set_id_label: str = "", intensity: float = None, intensities_mean: float = None, intensities_neg_conf: float = None, intensities_pos_conf: float = None):
        super().__init__()
        self.set_id = set_id
        self.set_id_labels = set_id_label
        self.intensity = intensity
        self.intensities_mean = intensities_mean
        self.intensities_neg_conf = intensities_neg_conf
        self.intensities_pos_conf = intensities_pos_conf

    @property
    def set_id(self) -> str:
        return self._set_id
    
    @set_id.setter
    def set_id(self, set_id: str):
        self._set_id = set_id

    @property
    def set_id_label(self) -> str:
        return self._set_id_labels
    
    @set_id_label.setter
    def set_id_labels(self, set_id_labels: str):
        self._set_id_labels = set_id_labels

    @property
    def intensity(self) -> float:
        return self._intensity
    
    @intensity.setter
    def intensity(self, intensity: float):
        self._intensity = intensity

    @property
    def intensities_mean(self) -> float:
        return self._intensities_mean
    
    @intensities_mean.setter
    def intensities_mean(self, intensities_mean: float):
        self._intensities_mean = intensities_mean

    @property
    def intensities_neg_conf(self) -> float:
        return self._intensities_neg_conf
    
    @intensities_neg_conf.setter
    def intensities_neg_conf(self, intensities_neg_conf: float):
        self._intensities_neg_conf = intensities_neg_conf

    @property
    def intensities_pos_conf(self) -> float:
        return self._intensities_pos_conf
    
    @intensities_pos_conf.setter
    def intensities_pos_conf(self, intensities_pos_conf: str):
        self._intensities_pos_conf = intensities_pos_conf