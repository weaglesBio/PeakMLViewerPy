import base64
class SetInfo():
    def __init__(self, id, label, measurementids):
        self.id = id # int
        self.type = label # string
        self.measurementids = measurementids # string

    def get_setid(self):
        return self.id

    def get_measurementids(self):
        return self.measurementids

    def get_encoded_measurementids(self):
        encoded = base64.b64encode(self.measurementids)
        return encoded.decode("UTF-8")  #Converts from bytes to string