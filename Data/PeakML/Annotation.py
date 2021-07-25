import Utilities as u
class Annotation():
    def __init__(self, unit: str = "", ontology_ref: str = "", label: str = "", value: str = "", value_type: str = "STRING"):

        self.unit = unit
        self.ontology_ref = ontology_ref
        self.label = label
        self.value = value
        self.value_type = value_type

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, unit: str):
        self._unit = unit

    @property
    def ontology_ref(self) -> str:
        return self._ontology_ref

    @ontology_ref.setter
    def ontology_ref(self, ontology_ref: str):
        self._ontology_ref = ontology_ref

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def value(self) -> str:

        # If contains commas, treat as list, else treat as single value.
        if "," in self._value:
            if u.is_float(self._value):
                if self._value:
                    values_list = self._value.split(', ')
                    converted_values_float_list = list(map(u.convert_float_to_sf,values_list))
                    converted_values_str_list = list(map(lambda x: str(x), converted_values_float_list))
                    converted_values_string = ", ".join(converted_values_str_list)
                    return converted_values_string
                else:
                    return ""
            else:
                return self._value
                
        # Needs to return these ahead of float check, as will pass as filter, but added mantissa will make matching with measurement id fail.        
        elif u.is_integer(self._value):
            return self._value

        elif u.is_float(self._value):
            return u.convert_float_to_sf(float(self._value))
        else:
            return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @property
    def value_type(self) -> str:
        return self._value_type

    @value_type.setter
    def value_type(self, value_type: str):
        self._value_type = value_type