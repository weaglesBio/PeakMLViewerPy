import Utilities as u

class BaseItem():
    def __init__(self, uid: str = None, initial_checked_state: bool = False):
           
        if uid is None:
            self._uid = u.get_new_uuid()
        else:
            self._uid = uid

        self.checked = initial_checked_state
        self.selected = False

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def checked(self) -> bool:
        return self._checked
    
    @checked.setter
    def checked(self, checked: bool):
        self._checked = checked

    @property
    def selected(self) -> bool:
        return self._selected
    
    @selected.setter
    def selected(self, selected: bool):
        self._selected = selected