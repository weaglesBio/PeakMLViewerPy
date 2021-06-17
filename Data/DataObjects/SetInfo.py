import base64

import Utilities as Utils


class SetInfo():
    def __init__(self, id, label, measurementids, colour):
        self.id = id # int
        self.type = label # string
        self.measurementids = measurementids # string

        # internal
        self.colour = colour
        self.selected = True
        self.uid = Utils.get_new_uuid()

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid

    def get_id(self):
        return self.id

    # Returns string of plain-text (UTF-8) measurementids

    def get_measurementids(self):
        return self.measurementids

    # Returns measurementids as raw encoded string
    def get_encoded_measurementids(self):
        encoded = base64.b64encode(self.measurementids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour

    def get_selected(self):
        return self.selected

    def set_selected(self, selected):
        self.selected = selected