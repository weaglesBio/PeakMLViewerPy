class Molecule:

    def __init__(self, database_id: str, name: str, formula: str):
        self.database_id = database_id
        self.name = name
        self.formula = formula
        self.mass = None
        self.inchi = None
        self.smiles = None
        self.description = None
        self.class_description = None
        self.synonyms = None
        self.retention_time = None
        self.polarity = None

    @property
    def database_id(self) -> str:
        return self._database_id

    @database_id.setter
    def database_id(self, database_id: str):
        self._database_id = database_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def formula(self) -> str:
        return self._formula

    @formula.setter
    def formula(self, formula: str):
        self._formula = formula

    @property
    def mass(self) -> str:
        return self._mass

    @mass.setter
    def mass(self, mass: str):
        self._mass = mass

    @property
    def inchi(self) -> str:
        return self._inchi

    @inchi.setter
    def inchi(self, inchi: str):
        self._inchi = inchi

    @property
    def smiles(self) -> str:
        return self._smiles

    @smiles.setter
    def smiles(self, smiles: str):
        self._smiles = smiles

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def class_description(self) -> str:
        return self._class_description

    @class_description.setter
    def class_description(self, class_description: str):
        self._class_description = class_description

    @property
    def synonyms(self) -> str:
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms: str):
        self._synonyms = synonyms

    @property
    def retention_time(self) -> float:
        return self._retention_time

    @retention_time.setter
    def retention_time(self, retention_time: float):
        self._retention_time = retention_time

    @property
    def polarity(self) -> str:
        return self._polarity

    @polarity.setter
    def polarity(self, polarity: str):
        self._polarity = polarity