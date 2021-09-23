import Utilities as Utils
import Data.Enums as Enums

class BaseFilter():
    def __init__(self, filter_type: Enums.FilterType):

        self._uid = Utils.get_new_uuid()
        self._type = filter_type

    @property
    def uid(self) -> str:
        return self._uid