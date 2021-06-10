import Chemistry.Enums as enum

CARBON = 0
HYDROGEN = 1
DEUTERIUM = 2
TRITIUM = 3
FLUORINE = 4
NITROGEN = 5
OXYGEN = 6
PHOSPHORUS = 7
CHLORINE = 8
SULFUR = 9
NATRIUM = 10
POTASSIUM = 11
COPPER = 12
CALCIUM = 13
SELENIUM = 14
LITHIUM = 15
BROMIDE = 16
MAGNESIUM = 17
IODINE = 18
IRON = 19
MANGANESE = 20
ZINC = 21
COBALT = 22
NICKEL = 23
TUNGSTEN = 24
BROMINE = 25
SILICON = 26
CESIUM = 27
ARSENIC = 28
CHROMIUM = 29
ALUMINUM = 30
MOLYBDENUM = 31
RUBIDUM = 32
ZIRCONIUM = 33
METHANOL = 34
ACETONITRILE = 35
NR_ELEMENTS = 36

elements = [ ]

class Element:

    def __init__(self, id, name, identifier, molecularweight, massvariance, valency, isotopes):
        self.id = id
        self.name = name
        self.identifier = identifier
        self.molecularweight = molecularweight
        self.massvariance = massvariance
        self.valency = valency
        self.isotopes = isotopes

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_identifier(self):
        return self.identifier

    def get_mass(self, masstype):
        if masstype == enum.Mass.MOLECULAR:
            return self.molecularweight
        else:
            return get_monoisotopic_weight()

    def get_molecularweight(self):
        return self.molecularweight

    def get_massvariance(self):
        return self.massvariance

    def get_valency(self):
        return self.valency

    def get_isotope_count(self):
        return len(self.isotopes)

    def get_isotopes(self):
        return self.isotopes

    #ef get_atomic_mass(self):
    #    return get_atomic_mass()

    #def get_monoisotopicweight(self):
    #    return get_monoisotopicweight(0)

    #def get_abundance(self):
    #    return get_abundance(0)

    # 0 should be the default for these
    def get_isotope(self, index):
        return self.isotopes[index]

    def get_atomic_mass(self, index):
        return self.isotopes[index].atomic_mass

    def get_monoisotopicweight(self, index):
        return self.isotopes[index].monoisotopicweight

    def get_abundance(self, index):
        return self.isotopes[index].abundance





class Isotope:

    def __init__(self, atomic_mass, monoisotopicweight, abundance):
        self.atomic_mass = atomic_mass
        self.monoisotopicweight = monoisotopicweight
        self.abundance = abundance

class NaturalIsotope:

    def __init__(self, name, mass):
        self.name = name
        self.mass = mass

natural_isotopes = [ NaturalIsotope("c13 isotope", getIsotopeMassDifference(CARBON, 1)), NaturalIsotope("n15 isotope", getIsotopeMassDifference(NITROGEN, 1)), NaturalIsotope("o18 isotope", getIsotopeMassDifference(OXYGEN, 2)), NaturalIsotope("n15 isotope", getIsotopeMassDifference(SULFUR, 2))]


ADDUCT = 0
DEDUCT = 1
ADDUCT_DEDUCT = 2

class Derivative:

    def __init__(self,adductdeduct,mer,charge,name,formula,mass):
        self.adductdeduct = adductdeduct
        self.mer = mer
        self.charge = charge
        self.name = name
        self.formula = formula
        self.mass = mass

    def get_mer(self):
        return self.mer

    def get_charge(self):
        return self.charge

    def get_name(self):
        return self.name

    def get_mass(self):
        return self.mass

    def from_derivative(self, derivativemass):
        if self.adductdeduct == ADDUCT:
            return (derivativemass-self.mass)/self.mer
        elif self.adductdeduct == DEDUCT:
            return (derivativemass+self.mass)/self.mer
        else: 
            return [(derivativemass-self.mass)/self.mer, (derivativemass+self.mass)/self.mer]

    def get_mass(self, basepeakmass, charge):
        return (basepeakmass + self.mass) / charge
