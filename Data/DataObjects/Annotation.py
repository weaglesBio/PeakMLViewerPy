class Annotation():
    def __init__(self, unit, ontologyref, label, value, valuetype):
        self.unit = unit
        self.ontologyref = ontologyref
        self.label = label
        self.value = value
        self.valuetype = valuetype

    def get_label(self):
        return self.label

    def get_value(self):
        return self.value
