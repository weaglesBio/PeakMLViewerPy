import base64

class SetInfo():
    def __init__(self, id: int, type: str, measurement_ids: str, colour: str):

        # PeakML attributes
        self.id = id
        self.type = type
        self.measurement_ids = measurement_ids

        # Application attributes
        self.colour = colour
        self.selected = True

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, type: str):
        self._type = type

    @property
    def colour(self) -> str:
        return self._colour
    
    @colour.setter
    def colour(self, colour: str):
        self._colour = colour

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, selected: bool):
        self._selected = selected

    def toggle_selected_status(self):
        if self.selected:
            self._selected = True
        else:
            self._selected = False

    # Returns string of plain-text (UTF-8) measurementids

    def get_measurement_ids(self):
        return self.measurement_ids

    # Returns measurementids as raw encoded string
    def get_encoded_measurement_ids(self):
        encoded = base64.b64encode(self.measurement_ids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

