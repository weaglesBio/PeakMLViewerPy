from Data.View.BaseItem import BaseItem

class IdentificationItem(BaseItem):
    def __init__(self, id: int, formula: str = "", ppm: str = "", adduct: str = "", name: str = "", class_desc: str = "", description: str = "", prior: str = "", post: str = "", smiles: str = "", inchi: str = "", notes: str = ""):
        super().__init__()

        self.id = id
        self.formula = formula
        self.ppm = ppm
        self.adduct = adduct
        self.name = name
        self.class_desc = class_desc
        self.description = description
        self.prior = prior
        self.post = post
        self.smiles = smiles
        self.inchi = inchi
        self.notes = notes

        self.prior_modified = False

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def formula(self) -> str:
        return self._formula
    
    @formula.setter
    def formula(self, formula: str):
        self._formula = formula

    @property
    def ppm(self) -> float:
        return self._ppm
    
    @ppm.setter
    def ppm(self, ppm: float):
        self._ppm = ppm

    @property
    def adduct(self) -> str:
        return self._adduct
    
    @adduct.setter
    def adduct(self, adduct: str):
        self._adduct = adduct

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def class_desc(self) -> str:
        return self._class_desc
    
    @class_desc.setter
    def class_desc(self, class_desc: str):
        self._class_desc = class_desc

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def prior(self) -> float:
        return self._prior
    
    @prior.setter
    def prior(self, prior: float):
        self._prior = prior

    @property
    def post(self) -> float:
        return self._post
    
    @post.setter
    def post(self, post: float):
        self._post = post

    @property
    def smiles(self) -> str:
        return self._smiles
    
    @smiles.setter
    def smiles(self, smiles: str):
        self._smiles = smiles

    @property
    def inchi(self) -> str:
        return self._inchi

    @inchi.setter
    def inchi(self, inchi: str):
        self._inchi = inchi

    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, notes: str):
        self._notes = notes

    @property
    def prior_modified(self) -> bool:
        return self._prior_modified
    
    @prior_modified.setter
    def prior_modified(self, prior_modified: bool):
        self._prior_modified = prior_modified




