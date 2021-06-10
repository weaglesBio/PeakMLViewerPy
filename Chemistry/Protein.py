class Protein:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.geneid = None
        self.products = []
        self.cofactors = []
        self.inhibitors = []
        self.substrates = []

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_geneid(self):
        return self.geneid

    # Products
    
    def get_products(self):
        return self.products

    def add_product(self, product):
        self.products.append(product)

    def empty_products(self):
        self.products.clear()
    
    # Co-Factors

    def get_products(self):
        return self.products

    def add_product(self, product):
        self.products.append(product)

    def empty_products(self):
        self.products.clear()

    # Inhibitors

    def get_inhibitors(self):
        return self.inhibitors

    def add_inhibitor(self, inhibitor):
        self.inhibitors.append(inhibitor)

    def empty_inhibitors(self):
        self.inhibitors.clear()

    # Substrates

    def get_substrates(self):
        return self.substrates

    def add_substate(self, substrate):
        self.substrates.append(substrate)

    def empty_substrates(self):
        self.substrates.clear()