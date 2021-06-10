class Molecule:

    def __init__(self, databaseid, name, formula):
        self.databaseid = databaseid
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

    def get_databaseid(self):
        return self.databaseid

    def set_databaseid(self, id):
        self.databaseid = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_formula(self):
        return self.formula

    def set_mass(self, mass):
        self.mass = mass

    def get_mass(self, masstype):
        if self.formula:
            return self.formula.get_mass(masstype)
        return self.mass

    def get_inchi(self):
        return self.inchi

    def set_inchi(self, inchi):
        self.inchi = inchi

    def get_smiles(self):
        return self.smiles

    def set_smiles(self, smiles):
        self.smiles = smiles

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_class_description(self):
        return self.class_description

    def set_class_description(self, class_description):
        self.class_description = class_description

    def get_synonyms(self):
        return self.synonyms

    def set_synonyms(self, synonyms):
        self.synonyms = synonyms

    def get_retention_time(self):
        return self.retention_time

    def set_retention_time(self, retention_time):
        self.retention_time = retention_time

    def get_polarity(self):
        return self.polarity

    def set_polarity(self, polarity):
        self.polarity = polarity