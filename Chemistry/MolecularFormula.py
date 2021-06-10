


class SubFormula:
    def __init__(self, name, charge, default_n, elements):
        self.name = name
        self.charge = charge
        self.defaultn = default_n
        self.elements = elements

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
    
    def get_charge(self):
        return self.charge

    def set_charge(self, charge):
        self.charge = charge
    
    def get_default_n(self):
        return self.default_n

    def set_default_n(self, default_n):
        self.default_n = default_n

    def get_mass(self, masstype):
        print("Not implemented")



    def set_name(self, name):
        self.name = name