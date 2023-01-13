from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants


class ToggleTestMode(UIState):
    def __init__(self, titrator, state):
        super().__init__(titrator, state)
        self.values = {"new_volume": 0}

    def handleKey(self, key):
        self._setNextState(self.previousState, True)

    def loop(self):
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out("Testing: {}".format(constants.IS_TEST), line=1)
        lcd_interface.lcd_out("", line=2)
        lcd_interface.lcd_out("Press any to cont.", line=3)
        lcd_interface.lcd_out("", line=4)
