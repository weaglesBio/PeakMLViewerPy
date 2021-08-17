import base64

from typing import List
class SetInfo():
    def __init__(self, id: int, type: str, measurement_ids_byte_array: bytearray):

        self.id = id
        self.type = type
        self.measurement_ids_byte_array = measurement_ids_byte_array
        self.measurement_ids = measurement_ids_byte_array.tolist()

        # Application methods
        self._linked_peak_measurement_ids = []

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
    def measurement_ids_byte_array(self) -> bytearray:
        return self._measurement_ids_byte_array
    
    @measurement_ids_byte_array.setter
    def measurement_ids_byte_array(self, measurement_ids_byte_array: bytearray):
        self._measurement_ids_byte_array = measurement_ids_byte_array

    @property
    def measurement_ids(self) -> List[str]:
        return self._measurement_ids
    
    @measurement_ids.setter
    def measurement_ids(self, measurement_ids: List[str]):
        self._measurement_ids = measurement_ids

    @property
    def linked_peak_measurement_ids(self) -> List[str]:
        return self._linked_peak_measurement_ids

    @linked_peak_measurement_ids.setter
    def linked_peak_measurement_ids(self, linked_peak_measurement_ids: List[str]):
        self._linked_peak_measurement_ids = linked_peak_measurement_ids

    def add_linked_peak_measurement_ids(self, peak_measurement_id: str):

        if peak_measurement_id not in self.linked_peak_measurement_ids:
            self._linked_peak_measurement_ids.append(peak_measurement_id)

    # Returns string of plain-text (UTF-8) measurementids
    # def get_measurement_ids_str(self):
    #     return ", ".join(self.measurement_ids)

    # Returns measurementids as raw encoded string
    def get_encoded_measurement_ids(self) -> str:
        encoded = base64.b64encode(self.measurement_ids_byte_array)
        return encoded.decode("UTF-8")  #Converts from bytes to string

